package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.List;

/** Load the checked static diagnostic translations without replacing existing translations. */
@Component
class DiagnosticTranslationSeed {
    private final JdbcTemplate db;
    private final ObjectMapper json;
    DiagnosticTranslationSeed(JdbcTemplate db, ObjectMapper json) { this.db = db; this.json = json; }

    @EventListener(ApplicationReadyEvent.class)
    @org.springframework.transaction.annotation.Transactional
    public void seed() throws IOException {
        db.update("insert into content_translations(source_hash,locale,kind,translated_text) values(?,?,'diagnostic',?) on conflict do nothing", Hashing.sha256("Не знаю\u0000"), "fr", "Je ne sais pas");
        db.update("insert into content_translations(source_hash,locale,kind,translated_text) values(?,?,'diagnostic',?) on conflict do nothing", Hashing.sha256("Не знаю\u0000"), "ar-SD", "لا أعرف");
        seedFile("diagnostic-translations.json", "diagnostic");
        seedFile("skill-translations.json", "skill-title");
    }

    private void seedFile(String name, String kind) throws IOException {
        var resource = new ClassPathResource(name);
        if (!resource.exists()) return;
        try (var in = resource.getInputStream()) {
            var root = json.readTree(in);
            for (String locale : List.of("fr", "ar-SD")) {
                var entries = root.path(locale).fields();
                while (entries.hasNext()) {
                    var entry = entries.next();
                    if (entry.getValue().isTextual() && !entry.getValue().asText().isBlank())
                        db.update("insert into content_translations(source_hash,locale,kind,translated_text) values(?,?,?,?) on conflict do nothing",
                                Hashing.sha256(entry.getKey() + "\u0000"), locale, kind, entry.getValue().asText());
                }
            }
        }
    }
}
