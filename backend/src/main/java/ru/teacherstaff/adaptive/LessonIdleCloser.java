package ru.teacherstaff.adaptive;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.DisposableBean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;
import java.time.Instant;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/** Once a minute finishes lessons left without activity for app.lesson.idle-minutes (see ApiController.finishIdleLessons). */
@Component
class LessonIdleCloser implements ApplicationRunner, DisposableBean {
  private static final Logger log = LoggerFactory.getLogger(LessonIdleCloser.class);
  private final ApiController api;
  private final boolean enabled;
  private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor(Thread.ofVirtual().name("lesson-idle").factory());

  LessonIdleCloser(ApiController api, @Value("${app.lesson.idle-close.enabled:true}") boolean enabled) { this.api = api; this.enabled = enabled; }

  @Override public void run(ApplicationArguments args) {
    if (!enabled) return;
    scheduler.scheduleWithFixedDelay(() -> {
      try { api.finishIdleLessons(Instant.now()); }
      catch (Exception e) { log.error("Idle lesson check failed", e); }
    }, 60, 60, TimeUnit.SECONDS);
  }

  @Override public void destroy() { scheduler.shutdownNow(); }
}
