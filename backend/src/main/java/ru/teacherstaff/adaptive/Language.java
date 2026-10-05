package ru.teacherstaff.adaptive;

import java.util.Locale;

/** A course track. Rows without an explicit language belong to JAVA, the original course. */
enum Language {
  JAVA("Java", "java"),
  PYTHON("Python", "python");

  final String title;
  final String pistonLanguage;

  Language(String title, String pistonLanguage) { this.title = title; this.pistonLanguage = pistonLanguage; }

  /** Unknown or missing values fall back to JAVA so older clients keep working. */
  static Language parse(String value) {
    if (value == null || value.isBlank()) return JAVA;
    try { return valueOf(value.trim().toUpperCase(Locale.ROOT)); }
    catch (IllegalArgumentException e) { throw new ApiError("UNKNOWN_LANGUAGE", "Неизвестный язык курса"); }
  }

  static Language of(Object stored) { return stored == null ? JAVA : valueOf(stored.toString()); }
}
