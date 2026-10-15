package ru.teacherstaff.adaptive;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.DisposableBean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * Every 15 s expires board calls and finishes board tests whose time is over even when nobody looks at them (see
 * BoardTests.settle; every board request does the same lazily). At startup it also resumes checks and assessments a
 * restart interrupted.
 */
@Component
class BoardTestFinisher implements ApplicationRunner, DisposableBean {
  private static final Logger log = LoggerFactory.getLogger(BoardTestFinisher.class);
  private final BoardTests board;
  private final boolean enabled;
  // A platform thread, not a virtual one: see BackgroundThreads.
  private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor(BackgroundThreads.named("board-finish"));

  BoardTestFinisher(BoardTests board, @Value("${app.board.auto-finish.enabled:true}") boolean enabled) { this.board = board; this.enabled = enabled; }

  @Override public void run(ApplicationArguments args) {
    if (!enabled) return;
    scheduler.scheduleWithFixedDelay(() -> {
      try { board.settle(); }
      catch (Exception e) { log.error("Board test check failed", e); }
    }, 5, 15, TimeUnit.SECONDS);
  }

  @Override public void destroy() { scheduler.shutdownNow(); }
}
