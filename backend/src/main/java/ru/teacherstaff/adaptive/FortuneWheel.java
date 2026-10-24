package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;
import org.springframework.stereotype.Component;
import java.security.SecureRandom;
import java.text.Collator;
import java.time.Clock;
import java.util.*;
import java.util.random.RandomGenerator;

/**
 * «Колесо фортуны» of a saved pair: a chocolate for one student among those who earned a chance — a 5 at the board in the
 * pair's window, or the top {@link #TOP_PERCENT}% by the pair's points among the attended students not called to the
 * board (at least one point; ties at the border pass). Every student of the group takes part, whether in the session or
 * not. The teacher may add or remove names before the spin; the server picks the winner and keeps the spin. Teacher
 * starts it, the projected wheel shows names only. The rules: backend/README.md, «Колесо фортуны».
 */
@Component
class FortuneWheel {
  static final int TOP_PERCENT = 20, MAX_NAMES = 60;

  private final JdbcTemplate db; private final PairWork pairs; private final Clock clock; private final ObjectMapper json;
  private final RandomGenerator random = new SecureRandom();
  FortuneWheel(JdbcTemplate db, PairWork pairs, Clock clock, ObjectMapper json) { this.db = db; this.pairs = pairs; this.clock = clock; this.json = json; }

  /** The size of the top: TOP_PERCENT of the pool, rounded up. */
  static int topCount(int pool) { return (pool * TOP_PERCENT + 99) / 100; }

  /** The lowest points that still make the top, ties included; null when nobody makes it (an empty pool or no points). */
  static Integer threshold(List<Integer> points) {
    int k = topCount(points.size());
    if (k == 0) return null;
    int border = points.stream().sorted(Comparator.reverseOrder()).toList().get(k - 1);
    return Math.max(border, 1);
  }

  /** A board test of the window: its student was called (a cancelled or expired call does not count) and maybe graded. */
  private record Board(String grade, String status) {}

  /** GET /api/admin/pairs/{id}/wheel: who is on the wheel and why, the rest of the group to add by hand, the spins. */
  Map<String, Object> wheel(long pairId) {
    var head = pairs.saved(pairId);
    var users = db.queryForList("select id from users where role='STUDENT' and group_name=? order by id", Long.class, head.group());
    var rows = pairs.rowsOf(head.language(), head.window(), users);
    var board = board(users, head.window());
    var pool = rows.stream().filter(r -> r.attended() && !board.containsKey(r.userId())).toList();
    Integer threshold = threshold(pool.stream().map(PairWork.Row::points).toList());

    var collator = Collator.getInstance(Locale.forLanguageTag("ru"));
    Comparator<PairWork.Row> byName = Comparator.comparing((PairWork.Row r) -> r.name() == null ? "" : r.name(), collator).thenComparing(PairWork.Row::login);
    var candidates = new ArrayList<Map<String, Object>>(); var called = new ArrayList<Map<String, Object>>(); var others = new ArrayList<Map<String, Object>>();
    for (var r : rows.stream().sorted(byName).toList()) {
      var b = board.get(r.userId());
      var person = obj("userId", r.userId(), "login", r.login(), "displayName", r.name(), "attended", r.attended(), "points", r.points(), "grade", b == null ? null : b.grade());
      if (b != null && "5".equals(b.grade())) { person.put("reason", "BOARD"); candidates.add(person); }
      else if (b == null && r.attended() && threshold != null && r.points() >= threshold) { person.put("reason", "TOP"); candidates.add(person); }
      else (b != null ? called : others).add(person);
    }
    // The top by points first, then the 5s at the board, each by name: the order of the list; the wheel shuffles its own.
    candidates.sort(Comparator.comparing((Map<String, Object> c) -> "BOARD".equals(c.get("reason"))));
    return obj("pairId", pairId, "group", head.group(), "language", head.language().name(),
        "startsAt", PairWork.iso(head.window().start()), "endsAt", PairWork.iso(head.window().end()),
        "topPercent", TOP_PERCENT, "pool", pool.size(), "topCount", topCount(pool.size()), "threshold", threshold,
        "candidates", candidates, "called", called, "others", others, "spins", spins(pairId));
  }

  /** POST /api/admin/pairs/{id}/wheel/spin {userIds}: the names in wheel order; one wins at random and the spin is kept. */
  Map<String, Object> spin(long pairId, Map<String, Object> body, long adminId) {
    var head = pairs.saved(pairId);
    if (body == null || !(body.get("userIds") instanceof List<?> list) || list.isEmpty()) throw new ApiError("INVALID_WHEEL", "На колесе нет ни одного имени");
    var ids = new ArrayList<Long>();
    for (Object v : list) {
      if (!(v instanceof Number n) || n.doubleValue() != n.longValue()) throw new ApiError("INVALID_WHEEL", "userIds — номера студентов");
      if (ids.contains(n.longValue())) throw new ApiError("INVALID_WHEEL", "Имя на колесе повторяется");
      ids.add(n.longValue());
    }
    if (ids.size() > MAX_NAMES) throw new ApiError("INVALID_WHEEL", "На колесе не больше " + MAX_NAMES + " имён");
    int known = db.queryForObject("select count(*) from users where role='STUDENT' and group_name=? and id in (" + String.join(",", Collections.nCopies(ids.size(), "?")) + ")",
        Integer.class, concat(head.group(), ids));
    if (known != ids.size()) throw new ApiError("INVALID_WHEEL", "На колесе только студенты группы " + head.group());
    int index = random.nextInt(ids.size()); long winner = ids.get(index);
    db.update("insert into wheel_spins(pair_id,user_id,candidates_json,spun_by,spun_at) values(?,?,?,?,?)", pairId, winner, write(ids), adminId, PairWork.iso(clock.instant()));
    var person = db.queryForMap("select id as userId,login,display_name as displayName from users where id=?", winner);
    return obj("winner", obj("userId", winner, "login", person.get("login"), "displayName", person.get("displayName")), "index", index, "spins", spins(pairId));
  }

  /** The window's board tests of the given students by student: a 5 if any test got one, else the latest grade. */
  private Map<Long, Board> board(List<Long> users, PairWork.Window w) {
    Map<Long, Board> result = new HashMap<>();
    if (users.isEmpty()) return result;
    db.query("select user_id,final_grade,status from board_tests where status not in ('CANCELLED','EXPIRED') and user_id in (" + String.join(",", Collections.nCopies(users.size(), "?")) + ")"
        + " and cast(strftime('%s',called_at) as integer) between ? and ? order by called_at,id",
        (RowCallbackHandler) rs -> {
          long user = rs.getLong(1); var b = new Board(rs.getString(2), rs.getString(3)); var old = result.get(user);
          if (old == null || !"5".equals(old.grade()) && b.grade() != null) result.put(user, b);
        }, concat(null, users, w.start().getEpochSecond(), w.end().getEpochSecond()));
    return result;
  }

  private List<Map<String, Object>> spins(long pairId) {
    return db.query("select w.id,w.user_id,u.login,u.display_name,w.candidates_json,w.spun_at from wheel_spins w join users u on u.id=w.user_id where w.pair_id=? order by w.id",
        (rs, i) -> obj("id", rs.getLong(1), "userId", rs.getLong(2), "login", rs.getString(3), "displayName", rs.getString(4), "names", read(rs.getString(5)).size(), "spunAt", rs.getString(6)), pairId);
  }

  private static Object[] concat(Object first, List<Long> middle, Object... rest) {
    var all = new ArrayList<Object>(); if (first != null) all.add(first); all.addAll(middle); all.addAll(Arrays.asList(rest)); return all.toArray();
  }
  private String write(List<Long> ids) { try { return json.writeValueAsString(ids); } catch (Exception e) { throw new IllegalStateException(e); } }
  private List<Long> read(String text) { try { return json.readValue(text, new TypeReference<List<Long>>() {}); } catch (Exception e) { throw new IllegalStateException(e); } }
  private static Map<String, Object> obj(Object... entries) { var m = new LinkedHashMap<String, Object>(); for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]); return m; }
}
