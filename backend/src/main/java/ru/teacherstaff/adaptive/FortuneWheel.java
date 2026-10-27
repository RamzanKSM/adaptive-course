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
 * «Жребий» (a wheel; «Колесо фортуны» before the owner renamed it) of a saved pair: a prize (a chocolate unless the
 * teacher names another) for students who earned a chance — a good enough grade at the board in the pair's window, or
 * the top share by the pair's points among the attended students not called to the board (ties at the border pass).
 * Every student of the group takes part, whether in the session or not; the teacher may add or remove names. A draw is
 * a run of steps the teacher starts one by one: in ARROW mode every step picks a winner, in ELIMINATION mode every step
 * drops out a name until the winners are left. The server picks every step; a winner not in class is marked absent and
 * the next step draws a replacement from every name of the run that has not won. Settings: {@link DrawSettings}. The
 * projected wheel shows names and the prize only. The rules: backend/README.md, «Жребий».
 */
@Component
class FortuneWheel {
  static final int MAX_PRIZE = 200;

  private final JdbcTemplate db; private final PairWork pairs; private final DrawSettings settings; private final Clock clock; private final ObjectMapper json;
  private final RandomGenerator random = new SecureRandom();
  FortuneWheel(JdbcTemplate db, PairWork pairs, DrawSettings settings, Clock clock, ObjectMapper json) {
    this.db = db; this.pairs = pairs; this.settings = settings; this.clock = clock; this.json = json;
  }

  /** The size of the top: the given percent of the pool, rounded up. */
  static int topCount(int pool, double percent) { return (int) Math.ceil(pool * percent / 100 - 1e-9); }

  /** The lowest points that still make the top, ties included, and at least minPoints; null when nobody makes it (an empty pool or top). */
  static Integer threshold(List<Integer> points, double percent, int minPoints) {
    int k = topCount(points.size(), percent);
    if (k == 0) return null;
    int border = points.stream().sorted(Comparator.reverseOrder()).toList().get(k - 1);
    return Math.max(border, minPoints);
  }

  /** GET /api/admin/pairs/{id}/wheel: who is on the wheel and why, the rest of the group to add by hand, the runs, the settings. */
  Map<String, Object> wheel(long pairId) {
    var head = pairs.saved(pairId); var s = settings.current();
    var users = db.queryForList("select id from users where role='STUDENT' and group_name=? order by id", Long.class, head.group());
    var rows = pairs.rowsOf(head.language(), head.window(), users);
    var board = board(users, head.window());
    var pool = rows.stream().filter(r -> r.attended() && !board.containsKey(r.userId())).toList();
    Integer threshold = threshold(pool.stream().map(PairWork.Row::points).toList(), s.topPercent(), s.minPoints());

    var collator = Collator.getInstance(Locale.forLanguageTag("ru"));
    Comparator<PairWork.Row> byName = Comparator.comparing((PairWork.Row r) -> r.name() == null ? "" : r.name(), collator).thenComparing(PairWork.Row::login);
    var candidates = new ArrayList<Map<String, Object>>(); var called = new ArrayList<Map<String, Object>>(); var others = new ArrayList<Map<String, Object>>();
    for (var r : rows.stream().sorted(byName).toList()) {
      boolean wasCalled = board.containsKey(r.userId()); Integer grade = board.get(r.userId());
      var person = obj("userId", r.userId(), "login", r.login(), "displayName", r.name(), "attended", r.attended(), "points", r.points(), "grade", grade == null ? null : String.valueOf(grade));
      if (grade != null && grade >= s.boardMinGrade()) { person.put("reason", "BOARD"); candidates.add(person); }
      else if (!wasCalled && r.attended() && threshold != null && r.points() >= threshold) { person.put("reason", "TOP"); candidates.add(person); }
      else (wasCalled ? called : others).add(person);
    }
    // The top by points first, then the grades at the board, each by name: the order of the list; the wheel shuffles its own.
    candidates.sort(Comparator.comparing((Map<String, Object> c) -> "BOARD".equals(c.get("reason"))));
    return obj("pairId", pairId, "group", head.group(), "language", head.language().name(),
        "startsAt", PairWork.iso(head.window().start()), "endsAt", PairWork.iso(head.window().end()),
        "topPercent", s.topPercent(), "minPoints", s.minPoints(), "boardMinGrade", s.boardMinGrade(),
        "pool", pool.size(), "topCount", topCount(pool.size(), s.topPercent()), "threshold", threshold,
        "candidates", candidates, "called", called, "others", others, "runs", runs(pairId), "prize", s.defaultPrize(), "settings", settings.view());
  }

  // ---------------------------------------------------------------- runs

  private record Step(long userId, String kind, boolean absent) {}
  private record Run(long id, long pairId, String mode, int winners, String prize, List<Long> names, String createdAt, List<Step> steps) {
    List<Step> wins() { return steps.stream().filter(s -> s.kind().equals("WIN")).toList(); }
    long activeWins() { return wins().stream().filter(s -> !s.absent()).count(); }
    /** After a winner was marked absent every name that has not won is on the wheel again, and a step picks a winner. */
    boolean replacing() { return wins().stream().anyMatch(Step::absent); }
    /** The names on the wheel now, in wheel order. */
    List<Long> wheel() {
      var gone = new HashSet<Long>();
      for (var s : steps) if (s.kind().equals("WIN") || s.kind().equals("OUT") && mode.equals("ELIMINATION") && !replacing()) gone.add(s.userId());
      return names.stream().filter(n -> !gone.contains(n)).toList();
    }
    boolean finished() { return activeWins() >= winners || wheel().isEmpty(); }
  }

  /** POST /api/admin/pairs/{id}/wheel/runs {userIds, prize}: a new run over the names in wheel order, with the mode and the winners of the settings. */
  Map<String, Object> start(long pairId, Map<String, Object> body, long adminId) {
    var head = pairs.saved(pairId); var s = settings.current();
    if (body == null || !(body.get("userIds") instanceof List<?> list) || list.isEmpty()) throw new ApiError("INVALID_WHEEL", "На колесе нет ни одного имени");
    var ids = new ArrayList<Long>();
    for (Object v : list) {
      if (!(v instanceof Number n) || n.doubleValue() != n.longValue()) throw new ApiError("INVALID_WHEEL", "userIds — номера студентов");
      if (ids.contains(n.longValue())) throw new ApiError("INVALID_WHEEL", "Имя на колесе повторяется");
      ids.add(n.longValue());
    }
    if (body.get("prize") != null && !(body.get("prize") instanceof String)) throw new ApiError("INVALID_WHEEL", "prize — название приза");
    String prize = body.get("prize") == null ? "" : ((String) body.get("prize")).strip().replaceAll("\\s+", " ");
    if (prize.length() > MAX_PRIZE) throw new ApiError("INVALID_WHEEL", "Название приза — не длиннее " + MAX_PRIZE + " символов");
    int known = db.queryForObject("select count(*) from users where role='STUDENT' and group_name=? and id in (" + String.join(",", Collections.nCopies(ids.size(), "?")) + ")",
        Integer.class, concat(head.group(), ids));
    if (known != ids.size()) throw new ApiError("INVALID_WHEEL", "На колесе только студенты группы " + head.group());
    long id = db.queryForObject("insert into draw_runs(pair_id,mode,winners,prize,names_json,created_by,created_at) values(?,?,?,?,?,?,?) returning id", Long.class,
        pairId, s.mode(), s.winners(), prize.isEmpty() ? s.defaultPrize() : prize, write(ids), adminId, now());
    return obj("run", view(run(pairId, id)));
  }

  /**
   * POST /api/admin/pairs/{id}/wheel/runs/{runId}/step: the next step. ARROW (or a replacement): a winner at random from the
   * wheel. ELIMINATION: a name at random drops out; when as many names are left as winners are still wanted, they win.
   */
  Map<String, Object> step(long pairId, long runId) {
    var run = run(pairId, runId);
    if (run.finished()) throw new ApiError("DRAW_FINISHED", "Жребий уже брошен: победители выявлены");
    var wheel = run.wheel(); long need = run.winners() - run.activeWins();
    Map<String, Object> pick = null; var won = new ArrayList<Long>();
    if (run.mode().equals("ARROW") || run.replacing()) {
      long user = wheel.get(random.nextInt(wheel.size())); insert(runId, user, "WIN"); won.add(user);
      pick = obj("userId", user, "kind", "WIN");
    } else {
      var left = new ArrayList<>(wheel);
      if (left.size() > need) {
        long user = left.remove(random.nextInt(left.size())); insert(runId, user, "OUT");
        pick = obj("userId", user, "kind", "OUT");
      }
      if (left.size() <= need) for (long user : left) { insert(runId, user, "WIN"); won.add(user); }
    }
    return obj("pick", pick, "won", won, "run", view(run(pairId, runId)));
  }

  /** POST /api/admin/pairs/{id}/wheel/runs/{runId}/absent {userId}: a winner is not in class; the next step draws a replacement. */
  Map<String, Object> absent(long pairId, long runId, Map<String, Object> body) {
    run(pairId, runId);
    if (body == null || !(body.get("userId") instanceof Number n)) throw new ApiError("INVALID_WHEEL", "userId — номер победителя");
    if (db.update("update draw_steps set absent=1 where run_id=? and user_id=? and kind='WIN' and absent=0", runId, n.longValue()) == 0)
      throw new ApiError("INVALID_WHEEL", "Этот студент не победитель этого жребия");
    return obj("run", view(run(pairId, runId)));
  }

  /** DELETE /api/admin/pairs/{id}/wheel/runs/{runId}: the run and its steps. */
  Map<String, Object> delete(long pairId, long runId) {
    run(pairId, runId);
    db.update("delete from draw_steps where run_id=?", runId);
    db.update("delete from draw_runs where id=?", runId);
    return obj("deleted", true, "runs", runs(pairId));
  }

  /** GET and PUT /api/admin/draw/settings. */
  Map<String, Object> settings() { return settings.view(); }
  Map<String, Object> saveSettings(Map<String, Object> body) { return settings.save(body); }

  private void insert(long runId, long user, String kind) { db.update("insert into draw_steps(run_id,user_id,kind,created_at) values(?,?,?,?)", runId, user, kind, now()); }

  private Run run(long pairId, long runId) {
    var runs = loadRuns("r.pair_id=? and r.id=?", pairId, runId);
    if (runs.isEmpty()) throw new NotFoundError("DRAW_NOT_FOUND", "Жребий не найден");
    return runs.getFirst();
  }
  private List<Run> loadRuns(String where, Object... params) {
    var runs = db.query("select r.id,r.pair_id,r.mode,r.winners,r.prize,r.names_json,r.created_at from draw_runs r where " + where + " order by r.id",
        (rs, i) -> new Run(rs.getLong(1), rs.getLong(2), rs.getString(3), rs.getInt(4), rs.getString(5), read(rs.getString(6)), rs.getString(7), new ArrayList<>()), params);
    if (runs.isEmpty()) return runs;
    Map<Long, Run> byId = new HashMap<>(); for (var r : runs) byId.put(r.id(), r);
    db.query("select run_id,user_id,kind,absent from draw_steps where run_id in (" + String.join(",", Collections.nCopies(runs.size(), "?")) + ") order by id",
        (RowCallbackHandler) rs -> byId.get(rs.getLong(1)).steps().add(new Step(rs.getLong(2), rs.getString(3), rs.getInt(4) == 1)), byId.keySet().toArray());
    return runs;
  }
  private List<Map<String, Object>> runs(long pairId) { return loadRuns("r.pair_id=?", pairId).stream().map(this::view).toList(); }

  /** A run as the panel and the stage need it: the wheel now, the drop-outs in order, the winners with names. */
  private Map<String, Object> view(Run r) {
    var ids = r.wins().stream().map(Step::userId).toList();
    Map<Long, String[]> people = new HashMap<>();
    if (!ids.isEmpty()) db.query("select id,login,display_name from users where id in (" + String.join(",", Collections.nCopies(ids.size(), "?")) + ")",
        (RowCallbackHandler) rs -> people.put(rs.getLong(1), new String[]{rs.getString(2), rs.getString(3)}), ids.toArray());
    var wins = r.wins().stream().map(s -> obj("userId", s.userId(), "login", people.get(s.userId())[0], "displayName", people.get(s.userId())[1], "absent", s.absent())).toList();
    return obj("id", r.id(), "mode", r.mode(), "winners", r.winners(), "prize", r.prize() == null ? DrawSettings.DEFAULTS.defaultPrize() : r.prize(),
        "names", r.names(), "wheel", r.wheel(), "outs", r.steps().stream().filter(s -> s.kind().equals("OUT")).map(Step::userId).toList(),
        "wins", wins, "replacing", r.replacing(), "finished", r.finished(), "createdAt", r.createdAt());
  }

  // ---------------------------------------------------------------- board

  /** The window's board tests (not attestations) of the given students: the best final grade of each called student (null — not graded yet). */
  private Map<Long, Integer> board(List<Long> users, PairWork.Window w) {
    Map<Long, Integer> result = new HashMap<>();
    if (users.isEmpty()) return result;
    db.query("select user_id,final_grade from board_tests where status not in ('CANCELLED','EXPIRED') and format='TEST' and user_id in (" + String.join(",", Collections.nCopies(users.size(), "?")) + ")"
        + " and cast(strftime('%s',called_at) as integer) between ? and ?",
        (RowCallbackHandler) rs -> {
          long user = rs.getLong(1); String grade = rs.getString(2);
          Integer g = grade == null ? null : Integer.valueOf(grade), old = result.get(user);
          result.put(user, old == null ? g : g == null ? old : Math.max(old, g));
        }, concat(null, users, w.start().getEpochSecond(), w.end().getEpochSecond()));
    return result;
  }

  private String now() { return PairWork.iso(clock.instant()); }
  private static Object[] concat(Object first, List<Long> middle, Object... rest) {
    var all = new ArrayList<Object>(); if (first != null) all.add(first); all.addAll(middle); all.addAll(Arrays.asList(rest)); return all.toArray();
  }
  private String write(List<Long> ids) { try { return json.writeValueAsString(ids); } catch (Exception e) { throw new IllegalStateException(e); } }
  private List<Long> read(String text) { try { return json.readValue(text, new TypeReference<List<Long>>() {}); } catch (Exception e) { throw new IllegalStateException(e); } }
  private static Map<String, Object> obj(Object... entries) { var m = new LinkedHashMap<String, Object>(); for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]); return m; }
}
