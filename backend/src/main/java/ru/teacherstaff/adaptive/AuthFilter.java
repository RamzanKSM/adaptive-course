package ru.teacherstaff.adaptive;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import java.io.IOException;
import java.time.Instant;
import java.util.Map;

@Component
public class AuthFilter extends OncePerRequestFilter {
  private final JdbcTemplate db;
  public AuthFilter(JdbcTemplate db) { this.db = db; }
  @Override protected boolean shouldNotFilter(HttpServletRequest r) { return !r.getRequestURI().startsWith("/api/") || r.getRequestURI().equals("/api/auth/login"); }
  @Override protected void doFilterInternal(HttpServletRequest r, HttpServletResponse s, FilterChain chain) throws ServletException, IOException {
    String token = null;
    if (r.getCookies() != null) for (Cookie c : r.getCookies()) if ("adaptive_session".equals(c.getName())) token = c.getValue();
    if (token == null) { s.sendError(HttpStatus.UNAUTHORIZED.value(), "Authentication required"); return; }
    var rows = db.queryForList("select u.id,u.login,u.role,u.display_name,u.llm_enabled from sessions x join users u on u.id=x.user_id where x.token_hash=? and x.expires_at>?", Hashing.sha256(token), Instant.now().toString());
    if (rows.isEmpty()) { s.sendError(HttpStatus.UNAUTHORIZED.value(), "Session expired"); return; }
    r.setAttribute("user", rows.getFirst()); chain.doFilter(r, s);
  }
}
final class Hashing {
  private Hashing() {}
  static String sha256(String value) { try { var d=java.security.MessageDigest.getInstance("SHA-256"); return java.util.HexFormat.of().formatHex(d.digest(value.getBytes(java.nio.charset.StandardCharsets.UTF_8))); } catch(Exception e) { throw new IllegalStateException(e); } }
}
