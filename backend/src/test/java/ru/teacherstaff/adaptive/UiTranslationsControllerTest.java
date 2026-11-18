package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.server.ResponseStatusException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.mock;

class UiTranslationsControllerTest {
    @Test void onlyBundledUiTextCanBeSentForTranslation() throws Exception {
        var controller = new UiTranslationsController(mock(JdbcTemplate.class), null, new ObjectMapper());
        assertThrows(ResponseStatusException.class,
                () -> controller.batch(new UiTranslationsController.Request("fr", List.of("Чужой пользовательский текст"))));
        assertThrows(ResponseStatusException.class,
                () -> controller.batch(new UiTranslationsController.Request("en", List.of("Темы"))));
    }
}
