package ru.teacherstaff.adaptive;

import java.util.List;
import java.util.Locale;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.jdbc.core.JdbcTemplate;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

class ContentTranslationsTest {
    @Test void cachedTitleReturnsBeforeSlowModel() {
        var db = mock(JdbcTemplate.class);
        var tutor = mock(CodexAppServerTutor.class);
        var release = new java.util.concurrent.CountDownLatch(1);
        when(db.queryForList(anyString(), eq(String.class), any(), any(), any())).thenReturn(List.of());
        when(tutor.translateText(anyList(), eq("fr"))).thenAnswer(call -> {
            release.await(5, java.util.concurrent.TimeUnit.SECONDS);
            return List.of("Titre");
        });
        LocaleContextHolder.setLocale(Locale.FRENCH);
        try {
            assertTimeoutPreemptively(java.time.Duration.ofSeconds(1),
                    () -> assertEquals("Заголовок", new ContentTranslations(db, tutor).cachedText("Заголовок", "task-title")));
        } finally { release.countDown(); }
    }
    @AfterEach void clearLocale() { LocaleContextHolder.resetLocaleContext(); }

    @Test void localeAndMissingTranslationFallBackToSource() {
        var db = mock(JdbcTemplate.class);
        var translations = new ContentTranslations(db);
        LocaleContextHolder.setLocale(Locale.forLanguageTag("fr"));
        when(db.queryForList(anyString(), eq(String.class), any(), any(), any())).thenReturn(List.of());
        assertEquals("Задание", translations.text("Задание"));
        verify(db).queryForList(anyString(), eq(String.class), eq(Hashing.sha256("Задание\u0000")), eq("fr"), eq("content"));
        assertEquals("ar-SD", ContentTranslations.locale(Locale.forLanguageTag("ar-SD")));
        assertEquals("ru", ContentTranslations.locale(Locale.ENGLISH));
    }

    @Test void reviewedTranslationIsReturnedOnlyForExactSourceAndLocale() {
        var db = mock(JdbcTemplate.class);
        var translations = new ContentTranslations(db);
        LocaleContextHolder.setLocale(Locale.forLanguageTag("fr"));
        when(db.queryForList(anyString(), eq(String.class), eq(Hashing.sha256("Привет\u0000")), eq("fr"), eq("content")))
                .thenReturn(List.of("Bonjour"));
        assertEquals("Bonjour", translations.text("Привет"));
        LocaleContextHolder.setLocale(Locale.forLanguageTag("ru"));
        assertEquals("Привет", translations.text("Привет"));
    }
    @Test void protectsCodeAndExactOutputAndRejectsLostTokens() {
        String source = "Выведи Результат: готово, используя `print(2)`\n```python\nprint(2)\n```";
        var value = UiTranslationsController.protect(source, List.of("Результат: готово"));
        assertFalse(value.text().contains("Результат: готово"));
        assertFalse(value.text().contains("print(2)"));
        assertEquals(source, UiTranslationsController.restore(value, value.text()));
        assertNull(UiTranslationsController.restore(value, value.text().replace("⟦PH0⟧", "")));
    }

    @Test void protectsUnfencedCodeLinesWithNonAsciiComments() {
        String source = "Напиши код:\nprint(2)  # ответ\nSystem.out.println(2); // ответ";
        var value = UiTranslationsController.protect(source);
        assertFalse(value.text().contains("ответ"));
        assertEquals(source, UiTranslationsController.restore(value, value.text()));
    }

    @Test void lostPlaceholderIsRetriedAndNeverCached() {
        var db = mock(JdbcTemplate.class);
        var tutor = mock(CodexAppServerTutor.class);
        when(db.queryForList(anyString(), eq(String.class), any(), any(), any())).thenReturn(List.of());
        when(tutor.translateText(anyList(), eq("fr"))).thenReturn(List.of("Texte sans marqueur"));
        LocaleContextHolder.setLocale(Locale.forLanguageTag("fr"));
        String source = "Выведи `print(2)`";
        assertEquals(source, new ContentTranslations(db, tutor).text(source));
        verify(tutor, times(2)).translateText(anyList(), eq("fr"));
        verify(db, never()).update(anyString(), any(), any(), any(), any());
    }

    @Test void taskWithoutStructuredExpectedOutputRemainsRussian() {
        var db = mock(JdbcTemplate.class);
        var tutor = mock(CodexAppServerTutor.class);
        when(db.queryForList(anyString(), eq(String.class), any())).thenReturn(List.of());
        LocaleContextHolder.setLocale(Locale.forLanguageTag("fr"));
        String statement = "Выведи результат";
        assertEquals(statement, new ContentTranslations(db, tutor).taskStatement(statement, 42L));
        verify(tutor, never()).translateText(anyList(), anyString());
    }

    @Test void taskExpectedTextIsMaskedBeforeTranslation() {
        var db = mock(JdbcTemplate.class);
        var tutor = mock(CodexAppServerTutor.class);
        when(db.queryForList(contains("select goal_json"), eq(String.class), any())).thenReturn(List.of("{\"kind\":\"OUTPUT_TEXT\",\"expectedOutput\":\"Привет\\n\"}"));
        when(db.queryForList(contains("select expected"), eq(String.class), any())).thenReturn(List.of());
        when(db.queryForList(contains("content_translations"), eq(String.class), any(), any(), any())).thenReturn(List.of());
        when(tutor.translateText(anyList(), eq("fr"))).thenAnswer(call -> {
            List<String> texts = call.getArgument(0);
            assertFalse(texts.getFirst().contains("Привет"));
            return texts;
        });
        LocaleContextHolder.setLocale(Locale.forLanguageTag("fr"));
        String statement = "Напечатай Привет";
        assertEquals(statement, new ContentTranslations(db, tutor).taskStatement(statement, 7L));
        verify(tutor).translateText(anyList(), eq("fr"));
    }

    @Test void fencedExampleAllowsTranslationAndPreservesBlockAndNumbers() {
        var db = mock(JdbcTemplate.class);
        var tutor = mock(CodexAppServerTutor.class);
        when(db.queryForList(anyString(), eq(String.class), any())).thenReturn(List.of());
        when(db.queryForList(contains("content_translations"), eq(String.class), any(), any(), any())).thenReturn(List.of());
        when(tutor.translateText(anyList(), eq("fr"))).thenAnswer(call -> {
            List<String> texts = call.getArgument(0);
            assertFalse(texts.getFirst().contains("9"));
            assertFalse(texts.getFirst().contains("```"));
            return List.of(texts.getFirst().replace("Выведи", "Affiche"));
        });
        LocaleContextHolder.setLocale(Locale.forLanguageTag("fr"));
        String statement = "Выведи 9:\n```text\n9\n```";
        assertEquals("Affiche 9:\n```text\n9\n```", new ContentTranslations(db, tutor).taskStatement(statement, 37L));
    }

    @Test void cacheKeyDoesNotDependOnExpectedLiteralOrderOrDuplicates() {
        var db = mock(JdbcTemplate.class);
        when(db.queryForList(anyString(), eq(String.class), any(), any(), any())).thenReturn(List.of());
        LocaleContextHolder.setLocale(Locale.forLanguageTag("fr"));
        var translations = new ContentTranslations(db);
        translations.text("Условие", "task-statement", List.of("два", "один", "два"));
        translations.text("Условие", "task-statement", List.of("один", "два"));
        var hashes = org.mockito.ArgumentCaptor.forClass(String.class);
        verify(db, times(2)).queryForList(anyString(), eq(String.class), hashes.capture(), eq("fr"), eq("task-statement"));
        assertEquals(hashes.getAllValues().get(0), hashes.getAllValues().get(1));
    }

}
