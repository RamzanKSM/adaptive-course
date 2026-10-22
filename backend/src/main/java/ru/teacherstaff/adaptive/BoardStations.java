package ru.teacherstaff.adaptive;

import jakarta.servlet.http.Cookie;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import java.security.SecureRandom;
import java.time.*;
import java.util.*;

/**
 * «Компьютер у доски»: a browser of the classroom PC the teacher turned into a board station. It holds the cookie
 * adaptive_station (Path=/api/station, a random token; the table keeps its SHA-256) and sees only the active calls and
 * the test running at it (BoardTests.station*): the student walks up, starts his test there without signing in, and the
 * station goes back to waiting after the finish. A revoked station is no station. Rules: backend/README.md, «К доске».
 */
@Component
class BoardStations {
  private static final Logger log = LoggerFactory.getLogger(BoardStations.class);
  static final String COOKIE = "adaptive_station", PATH = "/api/station", DEFAULT_NAME = "Компьютер у доски";
  static final int NAME_MAX = 60;
  static final Duration COOKIE_AGE = Duration.ofDays(365), SEEN_EVERY = Duration.ofMinutes(1);

  private final JdbcTemplate db; private final Clock clock; private final boolean secureCookie;
  private final SecureRandom random = new SecureRandom();
  BoardStations(JdbcTemplate db, Clock clock, @Value("${app.cookie-secure}") boolean secureCookie) { this.db = db; this.clock = clock; this.secureCookie = secureCookie; }

  /** The paths a station authenticates for: /api/station and below. */
  static boolean path(String uri) { return uri.equals(PATH) || uri.startsWith(PATH + "/"); }

  /** The station of a cookie token, {id, name}, or null (no token, unknown, revoked); notes that it was seen, at most once a minute. */
  Map<String, Object> authenticate(String token) {
    if (token == null || token.isBlank()) return null;
    var rows = db.queryForList("select id,name,last_seen_at from board_stations where token_hash=? and revoked_at is null", Hashing.sha256(token));
    if (rows.isEmpty()) return null;
    var row = rows.getFirst(); Instant now = clock.instant();
    if (row.get("last_seen_at") == null || Instant.parse((String) row.get("last_seen_at")).isBefore(now.minus(SEEN_EVERY)))
      db.update("update board_stations set last_seen_at=? where id=?", iso(now), row.get("id"));
    return obj("id", ((Number) row.get("id")).longValue(), "name", row.get("name"));
  }

  /** POST /api/admin/board/stations: a new station; the cookie goes to this browser with the response. */
  Map<String, Object> create(long admin, Map<String, Object> body, jakarta.servlet.http.HttpServletResponse response) {
    Object value = body == null ? null : body.get("name");
    if (value != null && !(value instanceof String)) throw new ApiError("INVALID_STATION_NAME", "Название — строка до " + NAME_MAX + " символов");
    String name = value == null || ((String) value).isBlank() ? DEFAULT_NAME : ((String) value).strip();
    if (name.length() > NAME_MAX) throw new ApiError("INVALID_STATION_NAME", "Название — строка до " + NAME_MAX + " символов");
    byte[] bytes = new byte[32]; random.nextBytes(bytes);
    String token = Base64.getUrlEncoder().withoutPadding().encodeToString(bytes), now = iso(clock.instant());
    long id = db.queryForObject("insert into board_stations(name,token_hash,created_by,created_at) values(?,?,?,?) returning id", Long.class, name, Hashing.sha256(token), admin, now);
    response.addCookie(cookie(token, COOKIE_AGE));
    log.info("Board station {} «{}» created by admin {}", id, name, admin);
    return obj("id", id, "name", name, "createdAt", now);
  }

  /** GET /api/admin/board/stations: the stations not revoked. */
  Map<String, Object> list() {
    return obj("stations", db.query("select id,name,created_at,last_seen_at from board_stations where revoked_at is null order by id",
        (rs, i) -> obj("id", rs.getLong(1), "name", rs.getString(2), "createdAt", rs.getString(3), "lastSeenAt", rs.getString(4))));
  }

  /** DELETE /api/admin/board/stations/{id}: the station stops being one (its browser gets 401 on /api/station). */
  Map<String, Object> revoke(long id) {
    if (db.update("update board_stations set revoked_at=? where id=? and revoked_at is null", iso(clock.instant()), id) == 0
        && db.queryForObject("select count(*) from board_stations where id=?", Integer.class, id) == 0) throw new NotFoundError("BOARD_STATION_NOT_FOUND", "Компьютер у доски не найден");
    return obj("revoked", true);
  }

  /** DELETE /api/station: this browser leaves station mode — its station is revoked and the cookie cleared. */
  void leave(long id, jakarta.servlet.http.HttpServletResponse response) {
    db.update("update board_stations set revoked_at=? where id=? and revoked_at is null", iso(clock.instant()), id);
    response.addCookie(cookie("", Duration.ZERO));
    log.info("Board station {} left station mode", id);
  }

  private Cookie cookie(String token, Duration age) {
    Cookie c = new Cookie(COOKIE, token); c.setHttpOnly(true); c.setPath(PATH); c.setMaxAge((int) age.toSeconds()); c.setSecure(secureCookie); return c;
  }
  private static String iso(Instant at) { return PairWork.iso(at); }
  private static Map<String, Object> obj(Object... entries) { var m = new LinkedHashMap<String, Object>(); for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]); return m; }
}
