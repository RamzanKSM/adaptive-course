package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.jdbc.core.JdbcTemplate;
import org.sqlite.SQLiteDataSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class DiagnosticTranslationSeedTest {
    @Test void loadsBuiltInTranslationsIdempotently() throws Exception {
        var source = new SQLiteDataSource();
        source.setUrl("jdbc:sqlite:file:seed-" + UUID.randomUUID() + "?mode=memory&cache=shared");
        try (var keepAlive = source.getConnection()) {
            var db = new JdbcTemplate(source);
            db.execute("create table content_translations(source_hash text,locale text,kind text,translated_text text,primary key(source_hash,locale,kind))");
            var seed = new DiagnosticTranslationSeed(db, new ObjectMapper());
            seed.seed();
            int before = db.queryForObject("select count(*) from content_translations", Integer.class);
            var mapper = new ObjectMapper();
            for (String file : new String[]{"diagnostic-translations.json", "skill-translations.json"}) {
                try (var in = getClass().getResourceAsStream("/" + file)) {
                    if (in == null) continue;
                    var catalog = mapper.readTree(in);
                    String kind = file.startsWith("diagnostic") ? "diagnostic" : "skill-title";
                    for (String locale : new String[]{"fr", "ar-SD"}) {
                        var entries = catalog.path(locale).fields();
                        while (entries.hasNext()) {
                            var entry = entries.next();
                            assertEquals(entry.getValue().asText(), db.queryForObject("select translated_text from content_translations where source_hash=? and locale=? and kind=?", String.class, Hashing.sha256(entry.getKey() + "\u0000"), locale, kind));
                        }
                    }
                }
            }
            seed.seed();
            assertEquals(before, db.queryForObject("select count(*) from content_translations", Integer.class));
            assertEquals("Je ne sais pas", db.queryForObject("select translated_text from content_translations where source_hash=? and locale='fr' and kind='diagnostic'", String.class, Hashing.sha256("Не знаю\u0000")));
        }
    }
}
