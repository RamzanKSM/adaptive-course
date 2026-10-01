package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpServer;
import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;

import java.net.InetSocketAddress;
import java.net.SocketException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicBoolean;

import static org.junit.jupiter.api.Assertions.*;

class PistonCodeRunnerHttpTest {
  @Test void statusUsesPlainHttp11WithoutH2cUpgrade() throws Exception {
    AtomicBoolean h2cUpgrade = new AtomicBoolean();
    AtomicBoolean http11 = new AtomicBoolean();
    HttpServer server;
    try {
      server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
    } catch (SocketException e) {
      Assumptions.assumeTrue(false, "test sandbox does not permit a local TCP listener");
      return;
    }
    server.createContext("/api/v2/", exchange -> {
      http11.set("HTTP/1.1".equals(exchange.getProtocol()));
      h2cUpgrade.set(exchange.getRequestHeaders().containsKey("Upgrade") || exchange.getRequestHeaders().containsKey("HTTP2-Settings"));
      String body = exchange.getRequestURI().getPath().endsWith("/runtimes")
          ? "[{\"language\":\"java\",\"version\":\"15.0.2\"}]"
          : "{\"compile\":{\"code\":0,\"output\":\"\"},\"run\":{\"code\":0,\"output\":\"READY\"}}";
      byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
      exchange.sendResponseHeaders(200, bytes.length);
      exchange.getResponseBody().write(bytes);
      exchange.close();
    });
    server.start();
    try {
      PistonCodeRunner runner = new PistonCodeRunner(new ObjectMapper(), "http://127.0.0.1:" + server.getAddress().getPort(), "", 1_000, 1_000, 64_000_000, 64_000_000);
      assertTrue(runner.status().available());
      assertTrue(http11.get());
      assertFalse(h2cUpgrade.get());
    } finally {
      server.stop(0);
    }
  }
}
