package ru.teacherstaff.adaptive;

import java.util.Locale;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.jdbc.core.JdbcTemplate;

/** On-demand translation of explicitly selected platform content with protected literals and a durable cache. */
final class ContentTranslations {
    private static final Logger log = LoggerFactory.getLogger(ContentTranslations.class);
    private final JdbcTemplate db;
    private final LlmTutor tutor;
    private static final java.util.concurrent.Semaphore TRANSLATING = new java.util.concurrent.Semaphore(1, true);
    private static final java.util.concurrent.Semaphore QUEUED = new java.util.concurrent.Semaphore(8);
    private static final java.util.concurrent.atomic.AtomicLong FALLBACKS = new java.util.concurrent.atomic.AtomicLong();
    private static final java.util.Set<String> WARMING = java.util.concurrent.ConcurrentHashMap.newKeySet();
    private static final java.util.Map<String, Long> LAST_WARM = new java.util.concurrent.ConcurrentHashMap<>();

    private static boolean acquire() {
        if (!QUEUED.tryAcquire()) return false;
        try {
            if (TRANSLATING.tryAcquire(240, java.util.concurrent.TimeUnit.SECONDS)) return true;
        } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        QUEUED.release();
        return false;
    }
    private static void release() { TRANSLATING.release(); QUEUED.release(); }

    ContentTranslations(JdbcTemplate db) { this(db, null); }
    ContentTranslations(JdbcTemplate db, LlmTutor tutor) { this.db = db; this.tutor = tutor; }

    static String locale(Locale locale) {
        return switch (locale.getLanguage()) {
            case "fr" -> "fr";
            case "ar" -> "ar-SD";
            default -> "ru";
        };
    }

    String text(String source) { return text(source, "content", java.util.List.of()); }

    String text(String source, String kind, java.util.List<String> literals) {
        if (source == null || source.isEmpty()) return source;
        String locale = locale(LocaleContextHolder.getLocale());
        if ("ru".equals(locale)) return source;
        var canonicalLiterals = literals.stream().filter(java.util.Objects::nonNull).distinct().sorted().toList();
        String hash = Hashing.sha256(source + "\u0000" + String.join("\u0000", canonicalLiterals));
        var rows = db.queryForList("select translated_text from content_translations where source_hash=? and locale=? and kind=?", String.class, hash, locale, kind);
        if (!rows.isEmpty()) return rows.getFirst();
        if (tutor instanceof CodexAppServerTutor codex && acquire()) {
            try {
                var afterWait = db.queryForList("select translated_text from content_translations where source_hash=? and locale=? and kind=?", String.class, hash, locale, kind);
                if (!afterWait.isEmpty()) return afterWait.getFirst();
                var protectedText = UiTranslationsController.protect(source, canonicalLiterals);
                for (int attempt = 0; attempt < 2; attempt++) {
                    var answer = codex.translateText(java.util.List.of(protectedText.text()), locale);
                    String translated = UiTranslationsController.restore(protectedText, answer.getFirst());
                    if (translated != null) {
                        db.update("insert into content_translations(source_hash,locale,kind,translated_text) values(?,?,?,?) on conflict do nothing", hash, locale, kind, translated);
                        return translated;
                    }
                    log.warn("Invalid translation placeholders locale={} sourceHash={} attempt={}", locale, hash, attempt + 1);
                }
            } catch (RuntimeException e) {
                log.warn("Content translation failed locale={} sourceHash={}", locale, hash);
            } finally { release(); }
        }
        log.warn("Content translation fallback locale={} sourceHash={} total={}", locale, hash, FALLBACKS.incrementAndGet());
        return source;
    }
    String taskStatement(String source, Object taskId) {
        if (source == null || taskId == null || "ru".equals(locale(LocaleContextHolder.getLocale()))) return source;
        var literals = new java.util.ArrayList<String>();
        var goals = db.queryForList("select goal_json from tasks where id=?", String.class, taskId);
        if (!goals.isEmpty() && goals.getFirst() != null) {
            var goal = TaskGoal.fromJson(new com.fasterxml.jackson.databind.ObjectMapper(), goals.getFirst());
            if (goal != null && goal.expectedOutput() != null) {
                addExpected(literals, goal.expectedOutput());
            }
        }
        for (String expected : db.queryForList("select expected from task_cases where task_id=?", String.class, taskId)) {
            if (expected != null && !expected.isBlank()) addExpected(literals, expected);
        }
        boolean fencedExample = java.util.regex.Pattern.compile("(?s)```[^`]*```").matcher(source).find();
        if (!fencedExample && literals.stream().noneMatch(value -> value != null && !value.isBlank())) {
            log.warn("Task statement translation skipped: no structured expected output or fenced example task={} totalFallbacks={}", taskId, FALLBACKS.incrementAndGet());
            return source;
        }
        return text(source, "task-statement", literals);
    }

    private static void addExpected(java.util.List<String> literals, String value) {
        if (value == null || value.isBlank()) return;
        literals.add(value);
        literals.add(value.strip());
        for (String line : value.split("\\R")) if (!line.isBlank()) literals.add(line);
        try {
            var parsed = new com.fasterxml.jackson.databind.ObjectMapper().readTree(value);
            if (parsed != null && parsed.isTextual() && !parsed.asText().isBlank()) literals.add(parsed.asText());
        } catch (java.io.IOException ignored) {
            // Expected output is usually plain text, not a JSON value.
        }
        String trimmed = value.strip();
        if (trimmed.length() > 2 && trimmed.charAt(0) == '\'' && trimmed.charAt(trimmed.length() - 1) == '\'')
            literals.add(trimmed.substring(1, trimmed.length() - 1));
    }

    java.util.List<String> cachedTexts(java.util.List<String> sources, String kind) {
        String locale = locale(LocaleContextHolder.getLocale());
        if ("ru".equals(locale)) return sources;
        var out = new java.util.ArrayList<String>();
        var missing = new java.util.LinkedHashSet<String>();
        for (String source : sources) {
            var rows = db.queryForList("select translated_text from content_translations where source_hash=? and locale=? and kind=?", String.class, Hashing.sha256(source + "\u0000"), locale, kind);
            if (rows.isEmpty()) { out.add(source); missing.add(source); } else out.add(rows.getFirst());
        }
        if (!missing.isEmpty()) {
            log.warn("Missing cached translations kind={} locale={} count={}", kind, locale, missing.size());
            String key = kind + ":" + locale;
            long now = System.currentTimeMillis();
            if (tutor instanceof CodexAppServerTutor && now - LAST_WARM.getOrDefault(key, 0L) > 300_000 && WARMING.add(key)) {
                LAST_WARM.put(key, now);
                BackgroundThreads.named("translation-warm-" + key).newThread(() -> {
                    try {
                        LocaleContextHolder.setLocale(Locale.forLanguageTag(locale));
                        texts(new java.util.ArrayList<>(missing), kind);
                    } finally { LocaleContextHolder.resetLocaleContext(); WARMING.remove(key); }
                }).start();
            }
        }
        return out;
    }

    java.util.List<String> texts(java.util.List<String> sources, String kind) {
        String locale = locale(LocaleContextHolder.getLocale());
        if ("ru".equals(locale)) return sources;
        var out = new java.util.ArrayList<>(sources);
        var missing = new java.util.LinkedHashMap<String, java.util.List<Integer>>();
        for (int i = 0; i < sources.size(); i++) {
            String source = sources.get(i);
            String hash = Hashing.sha256(source + "\u0000");
            var rows = db.queryForList("select translated_text from content_translations where source_hash=? and locale=? and kind=?", String.class, hash, locale, kind);
            if (!rows.isEmpty()) out.set(i, rows.getFirst());
            else missing.computeIfAbsent(source, x -> new java.util.ArrayList<>()).add(i);
        }
        if (missing.isEmpty() || !(tutor instanceof CodexAppServerTutor codex) || !acquire()) return out;
        try {
            var entries = new java.util.ArrayList<>(missing.entrySet());
            for (int start = 0; start < entries.size(); start += 30) {
                var group = entries.subList(start, Math.min(entries.size(), start + 30));
                var protectedTexts = group.stream().map(e -> UiTranslationsController.protect(e.getKey())).toList();
                var answers = codex.translateText(protectedTexts.stream().map(UiTranslationsController.Protected::text).toList(), locale);
                for (int i = 0; i < group.size(); i++) {
                    String translated = UiTranslationsController.restore(protectedTexts.get(i), answers.get(i));
                    if (translated == null) continue;
                    var entry = group.get(i);
                    db.update("insert into content_translations(source_hash,locale,kind,translated_text) values(?,?,?,?) on conflict do nothing", Hashing.sha256(entry.getKey() + "\u0000"), locale, kind, translated);
                    for (int index : entry.getValue()) out.set(index, translated);
                }
            }
        } catch (RuntimeException e) {
            log.warn("Content batch translation failed locale={} remaining={}", locale, missing.size());
        } finally { release(); }
        return out;
    }

}
