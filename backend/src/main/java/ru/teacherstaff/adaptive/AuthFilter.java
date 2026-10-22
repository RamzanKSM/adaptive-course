package ru.teacherstaff.adaptive;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Who makes an /api request: a user by the adaptive_session cookie (request attribute «user»), or — on /api/station/** —
 * a board station by the adaptive_station cookie (attribute «station», BoardStations; the user's session is ignored
 * there). Sessions slide: a request moves the session's end to now + app.session-hours and re-sends the cookie, so an
 * active user is never signed out (at most once an hour per session).
 */
@Component
public class AuthFilter extends OncePerRequestFilter {
  static final String SESSION_COOKIE = "adaptive_session";
  private final JdbcTemplate db; private final BoardStations stations; private final long sessionHours; private final boolean secureCookie;
  public AuthFilter(JdbcTemplate db, BoardStations stations, @Value("${app.session-hours}") long sessionHours, @Value("${app.cookie-secure}") boolean secureCookie) {
    this.db = db; this.stations = stations; this.sessionHours = sessionHours; this.secureCookie = secureCookie;
  }
  @Override protected boolean shouldNotFilter(HttpServletRequest r) { return !r.getRequestURI().startsWith("/api/") || r.getRequestURI().equals("/api/auth/login"); }
  @Override protected void doFilterInternal(HttpServletRequest r, HttpServletResponse s, FilterChain chain) throws ServletException, IOException {
    if (BoardStations.path(r.getRequestURI())) {
      var station = stations.authenticate(cookie(r, BoardStations.COOKIE));
      if (station == null) { s.sendError(HttpStatus.UNAUTHORIZED.value(), "Board station required"); return; }
      r.setAttribute("station", station); LogContext.station(station.get("id"), station.get("name")); chain.doFilter(r, s); return;
    }
    String token = cookie(r, SESSION_COOKIE);
    if (token == null) { s.sendError(HttpStatus.UNAUTHORIZED.value(), "Authentication required"); return; }
    Instant now = Instant.now();
    var rows = db.queryForList("select u.id,u.login,u.role,u.display_name,u.llm_enabled,u.hard_mode_allowed,u.hard_mode_on,x.expires_at from sessions x join users u on u.id=x.user_id where x.token_hash=? and x.expires_at>?", Hashing.sha256(token), now.toString());
    if (rows.isEmpty()) { s.sendError(HttpStatus.UNAUTHORIZED.value(), "Session expired"); return; }
    var user = rows.getFirst();
    Duration lifetime = Duration.ofHours(sessionHours);
    if (Instant.parse((String) user.remove("expires_at")).isBefore(now.plus(lifetime).minus(Duration.ofHours(1)))) {
      db.update("update sessions set expires_at=? where token_hash=?", now.plus(lifetime).toString(), Hashing.sha256(token));
      s.addCookie(sessionCookie(token, lifetime, secureCookie));
    }
    r.setAttribute("user", user); traceUser(r, user); chain.doFilter(r, s);
  }
  /** The session cookie as login sets it and a sliding session re-sends it. */
  static Cookie sessionCookie(String token, Duration lifetime, boolean secure) {
    Cookie c = new Cookie(SESSION_COOKIE, token); c.setHttpOnly(true); c.setPath("/api"); c.setMaxAge((int) lifetime.toSeconds()); c.setSecure(secure); return c;
  }
  static String cookie(HttpServletRequest r, String name) {
    if (r.getCookies() != null) for (Cookie c : r.getCookies()) if (name.equals(c.getName())) return c.getValue();
    return null;
  }
  private static final Pattern MANAGED_STUDENT = Pattern.compile("^/api/admin/students/(\\d+)(/.*)?$");
  /** Log lines of a student request name the student; admin requests name the admin and, if any, the student being managed. */
  private void traceUser(HttpServletRequest r, Map<String, Object> user) {
    if ("STUDENT".equals(user.get("role"))) { LogContext.student(user.get("id"), user.get("login")); return; }
    LogContext.admin(user.get("login"));
    Matcher m = MANAGED_STUDENT.matcher(r.getRequestURI());
    if (!m.matches()) return;
    long id = Long.parseLong(m.group(1));
    var login = db.queryForList("select login from users where id=?", String.class, id);
    LogContext.student(id, login.isEmpty() ? null : login.getFirst());
  }
}
final class Hashing {
  private Hashing() {}
  static String sha256(String value) { try { var d=java.security.MessageDigest.getInstance("SHA-256"); return java.util.HexFormat.of().formatHex(d.digest(value.getBytes(java.nio.charset.StandardCharsets.UTF_8))); } catch(Exception e) { throw new IllegalStateException(e); } }
}
