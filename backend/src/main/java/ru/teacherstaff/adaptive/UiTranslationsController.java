package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.Semaphore;
import java.util.regex.Pattern;

@RestController
@RequestMapping("/api/i18n")
class UiTranslationsController {
    private static final org.slf4j.Logger log = org.slf4j.LoggerFactory.getLogger(UiTranslationsController.class);
    private static final java.util.concurrent.atomic.AtomicLong FALLBACKS = new java.util.concurrent.atomic.AtomicLong();
    private static final Pattern PROTECTED = Pattern.compile("(?s)```.*?```|`[^`]+`|(?m)^[ \t]*(?:(?:public|private|class|def|return|if|elif|else|for|while|import|from|print|System\\.out\\.println?|//)\\b|//)[^\\r\\n]*|(?m)^[ \t]*[\\x20-\\x7e]+$|\\{[^{}\\n]+}|%[a-zA-Z]|</?[^>]+>|\"[\\x20-\\x7e]*\"|\u0027[\\x20-\\x7e]*\u0027|\\b[A-Za-z_][A-Za-z_0-9.]*\\b|\\d+(?:[.,:]\\d+)*");
    private final JdbcTemplate db;
    private final LlmTutor tutor;
    private final Set<String> allowed;
    private final Semaphore translating = new Semaphore(1, true);
    private final Semaphore queued = new Semaphore(8);
    private long windowStart;
    private int requests;

    UiTranslationsController(JdbcTemplate db, LlmTutor tutor, ObjectMapper mapper) throws IOException {
        this.db = db;
        this.tutor = tutor;
        var resource = new ClassPathResource("ui-ru.json");
        if (resource.exists()) {
            var root = mapper.readTree(resource.getInputStream());
            var values = new HashSet<String>();
            collect(root, values);
            allowed = Set.copyOf(values);
        } else allowed = Set.of();
    }

    private static void collect(com.fasterxml.jackson.databind.JsonNode node, Set<String> values) {
        if (node.isTextual()) values.add(node.asText());
        else if (node.isContainerNode()) node.elements().forEachRemaining(child -> collect(child, values));
    }

    record Request(String locale, List<String> texts) {}

    @PostMapping("/batch")
    Map<String, Object> batch(@RequestBody Request request) {
        if (request == null || !("fr".equals(request.locale()) || "ar-SD".equals(request.locale())) || request.texts() == null
                || request.texts().size() > 50 || request.texts().stream().anyMatch(s -> s == null || s.length() > 320 || !allowed.contains(s))
                || request.texts().stream().mapToInt(String::length).sum() > 4000)
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Invalid translation request");
        synchronized (this) {
            long now = System.currentTimeMillis();
            if (now - windowStart >= 60_000) { windowStart = now; requests = 0; }
            if (++requests > 60) throw new ResponseStatusException(HttpStatus.TOO_MANY_REQUESTS);
        }
        var result = new ArrayList<String>(request.texts());
        var missing = new LinkedHashMap<String, List<Integer>>();
        for (int i = 0; i < result.size(); i++) {
            String source = result.get(i);
            var rows = db.queryForList("select translated_text from content_translations where source_hash=? and locale=? and kind='ui'", String.class, Hashing.sha256(source), request.locale());
            if (!rows.isEmpty()) result.set(i, rows.getFirst());
            else missing.computeIfAbsent(source, k -> new ArrayList<>()).add(i);
        }
        if (!missing.isEmpty() && queued.tryAcquire()) {
            boolean acquired = false;
            try {
                acquired = translating.tryAcquire(240, java.util.concurrent.TimeUnit.SECONDS);
                if (!acquired) return Map.of("translations", result);
                // A previous request may have populated the same entries while this one waited.
                for (var it = missing.entrySet().iterator(); it.hasNext();) {
                    var entry = it.next();
                    var cached = db.queryForList("select translated_text from content_translations where source_hash=? and locale=? and kind='ui'", String.class, Hashing.sha256(entry.getKey()), request.locale());
                    if (!cached.isEmpty()) { for (int index : entry.getValue()) result.set(index, cached.getFirst()); it.remove(); }
                }
                if (missing.isEmpty()) return Map.of("translations", result);
                var protectedTexts = missing.keySet().stream().map(UiTranslationsController::protect).toList();
                if (!(tutor instanceof CodexAppServerTutor codex)) return Map.of("translations", result);
                var translated = codex.translateText(protectedTexts.stream().map(Protected::text).toList(), request.locale());
                int i = 0;
                for (var entry : missing.entrySet()) {
                    String text = restore(protectedTexts.get(i), translated.get(i++));
                    if (text == null) continue;
                    db.update("insert into content_translations(source_hash,locale,kind,translated_text) values(?,?,'ui',?) on conflict do nothing", Hashing.sha256(entry.getKey()), request.locale(), text);
                    for (int index : entry.getValue()) result.set(index, text);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } catch (RuntimeException ignored) {
                // An unavailable or invalid translation is never cached.
            } finally { if (acquired) translating.release(); queued.release(); }
        }
        long fallback = 0;
        for (int i = 0; i < result.size(); i++) if (result.get(i).equals(request.texts().get(i))) fallback++;
        if (fallback > 0) log.info("UI translation fallback locale={} count={} total={}", request.locale(), fallback, FALLBACKS.addAndGet(fallback));
        return Map.of("translations", result);
    }

    record Protected(String text, List<String> values) {}
    static Protected protect(String source) { return protect(source, List.of()); }
    static Protected protect(String source, List<String> literals) {
        String prefix = literals.stream().filter(s -> s != null && !s.isBlank() )
                .distinct().sorted(Comparator.comparingInt(String::length).reversed())
                .map(Pattern::quote).collect(java.util.stream.Collectors.joining("|"));
        Pattern pattern = prefix.isEmpty() ? PROTECTED : Pattern.compile("(?:" + prefix + ")|(?:" + PROTECTED.pattern() + ")");
        var matcher = pattern.matcher(source);
        var out = new StringBuilder();
        var values = new ArrayList<String>();
        while (matcher.find()) {
            String marker = "⟦PH" + values.size() + "⟧";
            values.add(matcher.group());
            matcher.appendReplacement(out, java.util.regex.Matcher.quoteReplacement(marker));
        }
        matcher.appendTail(out);
        return new Protected(out.toString(), values);
    }
    static String restore(Protected protectedText, String translated) {
        int previous = -1;
        for (int i = 0; i < protectedText.values().size(); i++) {
            String marker = "⟦PH" + i + "⟧";
            int first = translated.indexOf(marker);
            if (first <= previous || first != translated.lastIndexOf(marker)) return null;
            previous = first;
        }
        for (int i = 0; i < protectedText.values().size(); i++)
            translated = translated.replace("⟦PH" + i + "⟧", protectedText.values().get(i));
        return translated.contains("⟦PH") ? null : translated;
    }
}
