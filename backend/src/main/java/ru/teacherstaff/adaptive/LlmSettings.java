package ru.teacherstaff.adaptive;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import java.util.*;

/**
 * LLM settings an admin can change at runtime, stored in app_settings. Environment values are the defaults until
 * an admin overrides them.
 * <ul>
 *   <li>reasoning effort per purpose (chat, task generation incl. repair, explanations);</li>
 *   <li>rate limits, independent of each other: assistant (chat) messages per student per hour and per day;
 *       course-wide generations per hour of tasks (incl. repairs) and, separately, of explanations (lectures). The whole
 *       course. 0 means no limit. Usage is counted from llm_calls, so limits survive restarts.</li>
 * </ul>
 */
@Component
class LlmSettings {
  static final List<String> EFFORT_PURPOSES = List.of("CHAT", "TASK", "EXPLANATION");
  /** Used when the model's own list cannot be read: levels every reasoning model accepts. */
  static final List<String> FALLBACK_EFFORTS = List.of("low", "medium", "high");
  static final List<String> LIMIT_KEYS = List.of("chatPerHour", "chatPerDay", "tasksPerHour", "explanationsPerHour");
  private static final Map<String, Integer> LIMIT_MAX = Map.of("chatPerHour", 1000, "chatPerDay", 10_000, "tasksPerHour", 10_000, "explanationsPerHour", 10_000);

  private final JdbcTemplate db;
  private final Map<String, String> defaultEfforts;
  private final Map<String, Integer> defaultLimits;
  private final String defaultModel;
  private final List<String> extraModels;

  LlmSettings(JdbcTemplate db,
              @Value("${app.llm.model}") String defaultModel,
              @Value("${app.llm.extra-models:gpt-5.6-terra}") String extraModels,
              @Value("${app.llm.reasoning-effort:medium}") String fallback,
              @Value("${app.llm.reasoning-effort-chat:low}") String chat,
              @Value("${app.llm.reasoning-effort-task:high}") String task,
              @Value("${app.llm.reasoning-effort-explanation:medium}") String explanation,
              @Value("${app.llm.limits.chat-per-hour:30}") int chatPerHour,
              @Value("${app.llm.limits.chat-per-day:150}") int chatPerDay,
              @Value("${app.llm.limits.tasks-per-hour:100}") int tasksPerHour,
              @Value("${app.llm.limits.explanations-per-hour:30}") int explanationsPerHour) {
    this.db = db;
    this.defaultModel = defaultModel;
    this.extraModels = Arrays.stream(extraModels.split(",")).map(String::strip).filter(m -> !m.isEmpty()).distinct().toList();
    this.defaultEfforts = Map.of("CHAT", or(chat, fallback), "TASK", or(task, fallback), "EXPLANATION", or(explanation, fallback));
    this.defaultLimits = Map.of("chatPerHour", chatPerHour, "chatPerDay", chatPerDay, "tasksPerHour", tasksPerHour, "explanationsPerHour", explanationsPerHour);
  }
  private static String or(String value, String fallback) { return value == null || value.isBlank() ? fallback : value; }

  /** The model for every LLM call; CODEX_MODEL until an admin picks another one. */
  String model() { return stored("llm_model").orElse(defaultModel); }
  String defaultModel() { return defaultModel; }
  /** Models always offered in the admin even if the App Server does not list them (APP_LLM_EXTRA_MODELS). */
  List<String> extraModels() { return extraModels; }

  /** TASK_REPAIR uses the task generation level. */
  String effort(String purpose) {
    String key = "TASK_REPAIR".equals(purpose) ? "TASK" : purpose;
    return stored("llm_effort_" + key).orElse(defaultEfforts.getOrDefault(key, defaultEfforts.get("TASK")));
  }
  Map<String, String> efforts() { var map = new LinkedHashMap<String, String>(); for (String p : EFFORT_PURPOSES) map.put(p, effort(p)); return map; }
  Map<String, String> defaultEfforts() { var map = new LinkedHashMap<String, String>(); for (String p : EFFORT_PURPOSES) map.put(p, defaultEfforts.get(p)); return map; }

  int limit(String key) { return stored("llm_limit_" + key).map(Integer::parseInt).orElse(defaultLimits.get(key)); }
  Map<String, Integer> limits() { var map = new LinkedHashMap<String, Integer>(); for (String k : LIMIT_KEYS) map.put(k, limit(k)); return map; }
  Map<String, Integer> defaultLimits() { var map = new LinkedHashMap<String, Integer>(); for (String k : LIMIT_KEYS) map.put(k, defaultLimits.get(k)); return map; }

  /** Validates everything first, then saves; an invalid value changes nothing. */
  void update(String model, Map<String, String> efforts, Map<String, Integer> limits, List<String> allowedEfforts) {
    if (efforts != null) for (var e : efforts.entrySet()) {
      if (!EFFORT_PURPOSES.contains(e.getKey())) throw new ApiError("INVALID_SETTING", "Неизвестное назначение: " + e.getKey());
      if (!allowedEfforts.contains(e.getValue())) throw new ApiError("INVALID_SETTING", "Модель не поддерживает уровень размышлений «" + e.getValue() + "»");
    }
    if (limits != null) for (var l : limits.entrySet()) {
      if (!LIMIT_KEYS.contains(l.getKey())) throw new ApiError("INVALID_SETTING", "Неизвестный лимит: " + l.getKey());
      if (l.getValue() == null || l.getValue() < 0 || l.getValue() > LIMIT_MAX.get(l.getKey())) throw new ApiError("INVALID_SETTING", "Лимит должен быть от 0 до " + LIMIT_MAX.get(l.getKey()));
    }
    if (model != null) save("llm_model", model);
    if (efforts != null) efforts.forEach((purpose, value) -> save("llm_effort_" + purpose, value));
    if (limits != null) limits.forEach((key, value) -> save("llm_limit_" + key, String.valueOf(value)));
  }

  /** How much of the student's chat allowance is used; retryAfterSeconds is set only when a limit is reached. */
  record ChatQuota(int hourUsed, int hourLimit, int dayUsed, int dayLimit, long retryAfterSeconds) {
    boolean allowed() { return retryAfterSeconds == 0; }
    Map<String, Object> view() {
      var m = new LinkedHashMap<String, Object>();
      m.put("hourUsed", hourUsed); m.put("hourLimit", hourLimit); m.put("dayUsed", dayUsed); m.put("dayLimit", dayLimit); m.put("retryAfterSeconds", retryAfterSeconds);
      return m;
    }
  }

  ChatQuota chatQuota(long userId) {
    int hourLimit = limit("chatPerHour"), dayLimit = limit("chatPerDay");
    int hourUsed = count("select count(*) from llm_calls where user_id=? and purpose='CHAT' and created_at>=datetime('now','-1 hour')", userId);
    int dayUsed = count("select count(*) from llm_calls where user_id=? and purpose='CHAT' and created_at>=datetime('now','-1 day')", userId);
    long retry = 0;
    // Rolling windows: the wait ends when the oldest call that still counts leaves the window.
    if (hourLimit > 0 && hourUsed >= hourLimit) retry = Math.max(retry, secondsUntilFree(userId, "-1 hour", hourLimit, 3600));
    if (dayLimit > 0 && dayUsed >= dayLimit) retry = Math.max(retry, secondsUntilFree(userId, "-1 day", dayLimit, 86_400));
    return new ChatQuota(hourUsed, hourLimit, dayUsed, dayLimit, retry);
  }
  private long secondsUntilFree(long userId, String window, int limit, long windowSeconds) {
    Long age = db.queryForObject("select cast(strftime('%s','now') - strftime('%s', created_at) as integer) from llm_calls where user_id=? and purpose='CHAT' and created_at>=datetime('now',?) order by created_at desc limit 1 offset ?",
        Long.class, userId, window, limit - 1);
    return Math.max(1, windowSeconds - (age == null ? 0 : age));
  }

  /** Course-wide budget for generating tasks (new ones and repairs of old ones) in the last hour; chat does not count. */
  boolean taskGenerationAllowed() { int limit = limit("tasksPerHour"); return limit == 0 || tasksLastHour() < limit; }
  /** Course-wide budget for generating topic explanations (lectures) in the last hour; separate from tasks and chat. */
  boolean explanationGenerationAllowed() { int limit = limit("explanationsPerHour"); return limit == 0 || explanationsLastHour() < limit; }
  int tasksLastHour() { return count("select count(*) from llm_calls where purpose in ('TASK','TASK_REPAIR') and created_at>=datetime('now','-1 hour')"); }
  int explanationsLastHour() { return count("select count(*) from llm_calls where purpose='EXPLANATION' and created_at>=datetime('now','-1 hour')"); }

  private Optional<String> stored(String key) { return db.queryForList("select value from app_settings where key=?", String.class, key).stream().findFirst(); }
  private void save(String key, String value) { db.update("insert into app_settings(key,value) values(?,?) on conflict(key) do update set value=excluded.value", key, value); }
  private int count(String sql, Object... args) { return db.queryForObject(sql, Integer.class, args); }
}
