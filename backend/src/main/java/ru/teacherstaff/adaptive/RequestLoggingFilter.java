package ru.teacherstaff.adaptive;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import java.io.IOException;
import java.security.SecureRandom;
import java.util.HexFormat;

/**
 * One line per API request with status and duration. Runs before AuthFilter so every log line of the request
 * (including LLM and runner logs) carries the same requestId; AuthFilter adds the userId.
 */
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
class RequestLoggingFilter extends OncePerRequestFilter {
  private static final Logger log = LoggerFactory.getLogger("http");
  private static final SecureRandom random = new SecureRandom();

  @Override protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain) throws ServletException, IOException {
    byte[] id = new byte[4]; random.nextBytes(id);
    String requestId = HexFormat.of().formatHex(id);
    MDC.put("requestId", requestId);
    response.setHeader("X-Request-Id", requestId);
    long started = System.nanoTime();
    try { chain.doFilter(request, response); }
    finally {
      long ms = (System.nanoTime() - started) / 1_000_000;
      String uri = request.getRequestURI(), query = request.getQueryString();
      String line = "{} {}{} -> {} in {} ms";
      Object[] args = { request.getMethod(), uri, query == null ? "" : "?" + query, response.getStatus(), ms };
      if (!uri.startsWith("/api/")) log.debug(line, args);
      else if (response.getStatus() >= 500) log.warn(line, args);
      else log.info(line, args);
      MDC.clear();
    }
  }
}
