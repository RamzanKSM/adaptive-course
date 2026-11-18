package ru.teacherstaff.adaptive;

import org.junit.jupiter.api.Test;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class TranslationLocaleTest {
    @RestController static class Probe {
        @GetMapping(value = "/locale", produces = MediaType.TEXT_PLAIN_VALUE)
        String locale() { return ContentTranslations.locale(LocaleContextHolder.getLocale()); }
    }

    @Test void mvcReadsRequestLanguageWithoutDependingOnProgrammingCourse() throws Exception {
        var mvc = MockMvcBuilders.standaloneSetup(new Probe()).build();
        mvc.perform(get("/locale").header("Accept-Language", "fr"))
                .andExpect(status().isOk()).andExpect(content().string("fr"));
        mvc.perform(get("/locale").header("Accept-Language", "ar-SD"))
                .andExpect(status().isOk()).andExpect(content().string("ar-SD"));
        mvc.perform(get("/locale").header("Accept-Language", "en"))
                .andExpect(status().isOk()).andExpect(content().string("ru"));
    }
}
