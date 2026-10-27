package ru.teacherstaff.adaptive;

import java.util.*;

/**
 * The kinds of items of a test at the board and what makes a bank task fit one (pure functions, no database).
 * <ul>
 * <li>{@code parsons} «Собери программу»: the starter has one placeholder line, the reference = the starter with that line
 * replaced by one block of 4–12 meaningful lines; the student orders those lines (plus maybe one extra line taken from a
 * wrong solution that replaces exactly one line of the block).</li>
 * <li>{@code fix} «Исправь ошибку»: a wrong solution of the bank whose line diff from the reference is the smallest
 * (at most 2 changed lines).</li>
 * <li>{@code code} «Напиши код»: a regular task; a short one (≤ 10 meaningful lines added to the starter) preferred.</li>
 * </ul>
 * Lines are compared without blank and comment-only lines and without whitespace at the ends (Python keeps the
 * indentation: it is syntax there). Rules: backend/README.md, «К доске».
 */
final class BoardItems {
  private BoardItems() {}

  /** minutes: the kind's share of the test time; weight: its share of the grade; difficulties: the bank difficulty preferred, in order. */
  record Kind(String name, String title, int minutes, int weight, List<Integer> difficulties) {}
  static final List<Kind> KINDS = List.of(
      new Kind("parsons", "Собери программу", 2, 1, List.of(2, 1, 3)),
      new Kind("fix", "Исправь ошибку", 2, 2, List.of(2, 1, 3)),
      new Kind("code", "Напиши код", 3, 3, List.of(2, 3, 1)));
  static final List<String> ALL = KINDS.stream().map(Kind::name).toList();
  static final Set<String> PLACEHOLDERS = Set.of("# Напиши решение здесь", "// Напиши решение здесь");
  static final int BLOCK_MIN = 4, BLOCK_MAX = 12, FIX_MAX_CHANGED = 2, SHORT_CODE_LINES = 10, TRIVIAL_CODE_LINES = 3;

  static Kind kind(String name) { return KINDS.stream().filter(k -> k.name().equals(name)).findFirst().orElseThrow(() -> new IllegalArgumentException(name)); }
  static int seconds(List<String> kinds) { return kinds.stream().mapToInt(k -> kind(k).minutes()).sum() * 60; }
  /** The chosen kinds of a request in the canonical order; null → all three. */
  static List<String> parse(Object value) {
    if (value == null) return ALL;
    if (!(value instanceof List<?> list) || list.isEmpty()) throw new ApiError("INVALID_KINDS", "Выбери хотя бы одно задание");
    for (Object k : list) if (!(k instanceof String s) || !ALL.contains(s)) throw new ApiError("INVALID_KINDS", "Неизвестное задание: " + k + " (parsons, fix, code)");
    return ALL.stream().filter(list::contains).toList();
  }

  // ---------------------------------------------------------------- grade

  /** Grade by percent of the points: ≥ 90 → 5, ≥ 75 → 4, ≥ 50 → 3, else 2. */
  static int grade(double percent) { return percent >= 90 ? 5 : percent >= 75 ? 4 : percent >= 50 ? 3 : 2; }
  /** scores: kind → 0, 0.5 or 1; the percent of Σ weight × score from Σ weights of the kinds. */
  static double percent(Map<String, Double> scores) {
    double points = 0; int max = 0;
    for (var e : scores.entrySet()) { points += kind(e.getKey()).weight() * e.getValue(); max += kind(e.getKey()).weight(); }
    return max == 0 ? 0 : points / max * 100;
  }

  // ---------------------------------------------------------------- lines

  static List<String> lines(String text) { return Arrays.asList((text == null ? "" : text).replace("\r\n", "\n").split("\n", -1)); }
  static boolean meaningful(Language lang, String line) {
    String s = line.strip();
    return !s.isEmpty() && !s.startsWith(lang == Language.PYTHON ? "#" : "//");
  }
  /** A line as compared: no whitespace at the ends; Python keeps the indentation. */
  static String normalized(Language lang, String line) { return lang == Language.PYTHON ? line.stripTrailing() : line.strip(); }

  /** A change between two programs: the meaningful lines of the first removed and of the second added there (indices in the meaningful lines). */
  record Hunk(List<Integer> removed, List<Integer> added) { int changed() { return Math.max(removed.size(), added.size()); } }
  /** The line diff (LCS) of the meaningful lines of two programs. */
  static List<Hunk> diff(Language lang, List<String> a, List<String> b) {
    var x = a.stream().map(l -> normalized(lang, l)).toList(); var y = b.stream().map(l -> normalized(lang, l)).toList();
    int n = x.size(), m = y.size(); int[][] lcs = new int[n + 1][m + 1];
    for (int i = n - 1; i >= 0; i--) for (int j = m - 1; j >= 0; j--) lcs[i][j] = x.get(i).equals(y.get(j)) ? lcs[i + 1][j + 1] + 1 : Math.max(lcs[i + 1][j], lcs[i][j + 1]);
    var hunks = new ArrayList<Hunk>(); var removed = new ArrayList<Integer>(); var added = new ArrayList<Integer>();
    int i = 0, j = 0;
    while (i < n || j < m) {
      if (i < n && j < m && x.get(i).equals(y.get(j))) {
        if (!removed.isEmpty() || !added.isEmpty()) { hunks.add(new Hunk(List.copyOf(removed), List.copyOf(added))); removed.clear(); added.clear(); }
        i++; j++;
      } else if (j < m && (i == n || lcs[i][j + 1] >= lcs[i + 1][j])) added.add(j++);
      else removed.add(i++);
    }
    if (!removed.isEmpty() || !added.isEmpty()) hunks.add(new Hunk(List.copyOf(removed), List.copyOf(added)));
    return hunks;
  }
  static List<String> meaningfulLines(Language lang, String program) { return lines(program).stream().filter(l -> meaningful(lang, l)).toList(); }
  /** How many lines a wrong solution changes in the reference (Σ per change of max(removed, added)); 0 — no meaningful difference. */
  static int changed(Language lang, String reference, String wrong) { return diff(lang, meaningfulLines(lang, reference), meaningfulLines(lang, wrong)).stream().mapToInt(Hunk::changed).sum(); }

  // ---------------------------------------------------------------- kinds

  /** A wrong solution of the bank. */
  record Wrong(String description, String source) {}

  /** The bug of a fix item: the wrong solution with the fewest changed lines (1..FIX_MAX_CHANGED), the first of equals; null — none fits. */
  record Bug(String program, String description, int changed) {}
  static Bug bug(Language lang, String reference, List<Wrong> wrong) {
    if (reference == null || reference.isBlank()) return null;
    Bug best = null;
    for (var w : wrong) {
      if (w.source() == null || w.source().isBlank()) continue;
      int changed = changed(lang, reference, w.source());
      if (changed >= 1 && changed <= FIX_MAX_CHANGED && (best == null || changed < best.changed())) best = new Bug(w.source(), w.description(), changed);
    }
    return best;
  }

  /** A parsons item: before + the block lines in order + after is the reference; extra — the extra line (null when none). */
  record Parsons(String before, String after, List<String> block, String extra) {}
  static Parsons parsons(Language lang, String starter, String reference, List<Wrong> wrong) {
    if (starter == null || reference == null || reference.isBlank()) return null;
    var s = lines(starter); var r = lines(reference);
    var at = new ArrayList<Integer>();
    for (int i = 0; i < s.size(); i++) if (PLACEHOLDERS.contains(s.get(i).strip())) at.add(i);
    if (at.size() != 1) return null;
    int p = at.getFirst(), tail = s.size() - p - 1;
    if (r.size() < p + tail) return null;
    for (int i = 0; i < p; i++) if (!r.get(i).stripTrailing().equals(s.get(i).stripTrailing())) return null;
    for (int i = 0; i < tail; i++) if (!r.get(r.size() - tail + i).stripTrailing().equals(s.get(p + 1 + i).stripTrailing())) return null;
    var block = r.subList(p, r.size() - tail).stream().filter(l -> meaningful(lang, l)).map(String::stripTrailing).toList();
    if (block.size() < BLOCK_MIN || block.size() > BLOCK_MAX) return null;
    // The extra line: a wrong solution replacing exactly one line of the block by a line unlike every line of the block.
    int from = (int) s.subList(0, p).stream().filter(l -> meaningful(lang, l)).count();
    var ref = meaningfulLines(lang, reference); var texts = new HashSet<String>(); for (var l : block) texts.add(l.strip());
    String extra = null;
    for (var w : wrong) {
      if (w.source() == null) continue;
      var other = meaningfulLines(lang, w.source()); var hunks = diff(lang, ref, other);
      if (hunks.size() != 1 || hunks.getFirst().removed().size() != 1 || hunks.getFirst().added().size() != 1) continue;
      int replaced = hunks.getFirst().removed().getFirst(); String line = other.get(hunks.getFirst().added().getFirst()).stripTrailing();
      if (replaced >= from && replaced < from + block.size() && !texts.contains(line.strip())) { extra = line; break; }
    }
    return new Parsons(String.join("\n", s.subList(0, p)), String.join("\n", s.subList(p + 1, s.size())), block, extra);
  }
  /** The program a student assembled: before + the placed lines + after, joined with «\n». */
  static String assemble(String before, List<String> placed, String after) {
    var all = new ArrayList<String>(lines(before)); if (before == null || before.isEmpty()) all.clear();
    all.addAll(placed); all.addAll(lines(after));
    return String.join("\n", all);
  }

  /** Meaningful lines a reference adds to its starter; null when the reference is unknown. */
  static Integer added(Language lang, String starter, String reference) {
    if (reference == null || reference.isBlank()) return null;
    return Math.max(0, meaningfulLines(lang, reference).size() - meaningfulLines(lang, starter).size());
  }
}
