package ru.teacherstaff.adaptive;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import java.security.SecureRandom;
import java.time.*;
import java.util.*;

/**
 * «Компьютер у доски»: a tab of the classroom PC's browser the teacher turned into a board station, for as long as the tab
 * is open. The tab keeps a random token in sessionStorage and sends it in X-Board-Station (the table keeps its SHA-256);
 * it sees only the active calls and the test running at it (BoardTests.station*): the student walks up, starts his test
 * there without signing in, and the station goes back to waiting after the finish. While nobody is called it projects the
 * relay the teacher put on the board (CodeRelay.onBoard). A closed tab takes the token with it: the station drops off the
 * teacher's list after ONLINE and its row is deleted after LIFETIME without requests. Rules: backend/README.md, «К доске».
 */
@Component
class BoardStations {
  private static final Logger log = LoggerFactory.getLogger(BoardStations.class);
  static final String HEADER = "X-Board-Station", PATH = "/api/station", NAME = "Компьютер у доски";
  static final Duration SEEN_EVERY = Duration.ofMinutes(1), ONLINE = Duration.ofMinutes(3), LIFETIME = Duration.ofHours(1);

  private final JdbcTemplate db; private final Clock clock;
  private final SecureRandom random = new SecureRandom();
  BoardStations(JdbcTemplate db, Clock clock) { this.db = db; this.clock = clock; }

  /** The paths a station authenticates for: /api/station and below. */
  static boolean path(String uri) { return uri.equals(PATH) || uri.startsWith(PATH + "/"); }

  /** The station of a token, {id, name}, or null (no token, unknown, silent for LIFETIME); notes that it was seen, at most once a minute. */
  Map<String, Object> authenticate(String token) {
    if (token == null || token.isBlank()) return null;
    Instant now = clock.instant();
    var rows = db.queryForList("select id,name,last_seen_at from board_stations where token_hash=? and last_seen_at>=?", Hashing.sha256(token), iso(now.minus(LIFETIME)));
    if (rows.isEmpty()) return null;
    var row = rows.getFirst();
    if (Instant.parse((String) row.get("last_seen_at")).isBefore(now.minus(SEEN_EVERY))) {
      db.update("update board_stations set last_seen_at=? where id=?", iso(now), row.get("id"));
      deleteSilent(now);
    }
    return obj("id", ((Number) row.get("id")).longValue(), "name", row.get("name"));
  }

  /** POST /api/admin/board/stations: a new station; the token goes to this tab with the response and is never shown again. */
  Map<String, Object> create(long admin) {
    Instant at = clock.instant(); deleteSilent(at);
    byte[] bytes = new byte[32]; random.nextBytes(bytes);
    String token = Base64.getUrlEncoder().withoutPadding().encodeToString(bytes), now = iso(at);
    long id = db.queryForObject("insert into board_stations(name,token_hash,created_by,created_at,last_seen_at) values(?,?,?,?,?) returning id", Long.class, NAME, Hashing.sha256(token), admin, now, now);
    log.info("Board station {} created by admin {}", id, admin);
    return obj("id", id, "name", NAME, "createdAt", now, "token", token);
  }

  /** GET /api/admin/board/stations: the stations online now. */
  Map<String, Object> list() {
    Instant now = clock.instant(); deleteSilent(now);
    return obj("stations", db.query("select id,name,created_at,last_seen_at from board_stations where last_seen_at>=? order by id",
        (rs, i) -> obj("id", rs.getLong(1), "name", rs.getString(2), "createdAt", rs.getString(3), "lastSeenAt", rs.getString(4)), iso(now.minus(ONLINE))));
  }

  /** DELETE /api/admin/board/stations/{id}: the station stops being one (its tab gets 401 on /api/station). */
  Map<String, Object> revoke(long id) {
    if (db.update("delete from board_stations where id=?", id) == 0) throw new NotFoundError("BOARD_STATION_NOT_FOUND", "Компьютер у доски не найден");
    return obj("revoked", true);
  }

  /** DELETE /api/station: this tab leaves station mode. */
  void leave(long id) {
    db.update("delete from board_stations where id=?", id);
    log.info("Board station {} left station mode", id);
  }

  private void deleteSilent(Instant now) { db.update("delete from board_stations where last_seen_at<?", iso(now.minus(LIFETIME))); }
  private static String iso(Instant at) { return PairWork.iso(at); }
  private static Map<String, Object> obj(Object... entries) { var m = new LinkedHashMap<String, Object>(); for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]); return m; }
}
