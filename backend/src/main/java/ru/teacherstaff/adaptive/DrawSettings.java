package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import java.util.*;

/**
 * Settings of «Жребий», one set for every group, kept as JSON in app_settings under {@link #KEY}. The owner wants no
 * limits on the values, only defaults; a value is refused only when it means nothing (a negative time, no winners,
 * a percent outside 0–100, a grade that does not exist). Rules: backend/README.md, «Жребий».
 */
@Component
class DrawSettings {
  static final String KEY = "draw_settings";

  /**
   * @param spinSeconds a spin that picks a winner, and the decisive drop-out
   * @param mode ARROW (the arrow picks the winners) or ELIMINATION (the name under the arrow drops out until the winners are left)
   * @param eliminationSeconds every other drop-out
   * @param winners how many win one run
   * @param autoNext the next spin of a run starts by itself (false: the teacher starts every spin)
   * @param topPercent the share of the attended students not called to the board who get on the wheel by points
   * @param minPoints the fewest points that still make the top
   * @param boardMinGrade the lowest grade at the board that puts the student on the wheel
   * @param defaultPrize the prize when the teacher names none
   * @param surprisePrize the projected wheel hides the prize until the winners are known
   * @param sound sounds of the wheel; volume 0–100
   */
  record Values(double spinSeconds, String mode, double eliminationSeconds, int winners, boolean autoNext, double topPercent, int minPoints,
                int boardMinGrade, String defaultPrize, boolean surprisePrize, boolean sound, int volume) {}

  static final Values DEFAULTS = new Values(6.5, "ARROW", 2, 1, false, 20, 1, 5, "Шоколадка", true, true, 70);

  private final JdbcTemplate db; private final ObjectMapper json;
  DrawSettings(JdbcTemplate db, ObjectMapper json) { this.db = db; this.json = json; }

  /** The stored settings over the defaults: a value missing from the stored JSON keeps its default. */
  Values current() {
    var stored = db.queryForList("select value from app_settings where key=?", String.class, KEY);
    if (stored.isEmpty()) return DEFAULTS;
    try {
      Map<String, Object> values = new LinkedHashMap<>(map(DEFAULTS));
      values.putAll(json.readValue(stored.getFirst(), Map.class));
      return validate(values);
    } catch (ApiError e) { return DEFAULTS; } catch (Exception e) { throw new IllegalStateException(e); }
  }

  /** GET /api/admin/draw/settings. */
  Map<String, Object> view() { var v = new LinkedHashMap<>(map(current())); v.put("defaults", map(DEFAULTS)); return v; }

  /** PUT /api/admin/draw/settings: the given values over the current ones. */
  Map<String, Object> save(Map<String, Object> body) {
    if (body == null) throw new ApiError("INVALID_DRAW_SETTINGS", "Нужны настройки жребия");
    Map<String, Object> values = new LinkedHashMap<>(map(current()));
    for (var e : body.entrySet()) if (values.containsKey(e.getKey())) values.put(e.getKey(), e.getValue());
    var valid = validate(values);
    try { db.update("insert into app_settings(key,value) values(?,?) on conflict(key) do update set value=excluded.value", KEY, json.writeValueAsString(map(valid))); }
    catch (Exception e) { throw new IllegalStateException(e); }
    return view();
  }

  private static Values validate(Map<String, Object> v) {
    String mode = text(v, "mode");
    if (!mode.equals("ARROW") && !mode.equals("ELIMINATION")) throw bad("Формат — «Стрелка» или «Выбывание»");
    String prize = text(v, "defaultPrize").strip().replaceAll("\\s+", " ");
    return new Values(number(v, "spinSeconds", 0, Double.MAX_VALUE), mode, number(v, "eliminationSeconds", 0, Double.MAX_VALUE),
        (int) whole(v, "winners", 1), flag(v, "autoNext"), number(v, "topPercent", 0, 100), (int) whole(v, "minPoints", 0),
        (int) number(whole(v, "boardMinGrade", 2), "boardMinGrade", 2, 5), prize.isEmpty() ? DEFAULTS.defaultPrize() : prize,
        flag(v, "surprisePrize"), flag(v, "sound"), (int) number(whole(v, "volume", 0), "volume", 0, 100));
  }
  private static double number(Map<String, Object> v, String key, double min, double max) {
    if (!(v.get(key) instanceof Number n) || !Double.isFinite(n.doubleValue())) throw bad(key + " — число");
    return number(n.doubleValue(), key, min, max);
  }
  private static double number(double value, String key, double min, double max) {
    if (value < min || value > max) throw bad(key + (max == Double.MAX_VALUE ? " — не меньше " + fmt(min) : " — от " + fmt(min) + " до " + fmt(max)));
    return value;
  }
  private static long whole(Map<String, Object> v, String key, long min) {
    double d = number(v, key, min, Double.MAX_VALUE);
    if (d != Math.floor(d) || d > Integer.MAX_VALUE) throw bad(key + " — целое число");
    return (long) d;
  }
  private static boolean flag(Map<String, Object> v, String key) { if (!(v.get(key) instanceof Boolean b)) throw bad(key + " — да или нет"); return b; }
  private static String text(Map<String, Object> v, String key) { if (!(v.get(key) instanceof String s)) throw bad(key + " — текст"); return s; }
  private static String fmt(double d) { return d == Math.floor(d) ? String.valueOf((long) d) : String.valueOf(d); }
  private static final Map<String, String> TITLES = Map.ofEntries(Map.entry("spinSeconds", "Время прокрутки"), Map.entry("mode", "Формат"),
      Map.entry("eliminationSeconds", "Время выбывания"), Map.entry("winners", "Число победителей"), Map.entry("autoNext", "Следующая прокрутка"),
      Map.entry("topPercent", "Доля топа"), Map.entry("minPoints", "Минимум баллов"), Map.entry("boardMinGrade", "Оценка у доски"),
      Map.entry("defaultPrize", "Приз по умолчанию"), Map.entry("surprisePrize", "Приз-сюрприз"), Map.entry("sound", "Звуки"), Map.entry("volume", "Громкость"));
  private static ApiError bad(String message) {
    String key = message.split(" ", 2)[0];
    return new ApiError("INVALID_DRAW_SETTINGS", TITLES.containsKey(key) ? "«" + TITLES.get(key) + "»" + message.substring(key.length()) : message);
  }
  private static Map<String, Object> map(Values s) {
    var m = new LinkedHashMap<String, Object>();
    m.put("spinSeconds", s.spinSeconds()); m.put("mode", s.mode()); m.put("eliminationSeconds", s.eliminationSeconds()); m.put("winners", s.winners());
    m.put("autoNext", s.autoNext()); m.put("topPercent", s.topPercent()); m.put("minPoints", s.minPoints()); m.put("boardMinGrade", s.boardMinGrade());
    m.put("defaultPrize", s.defaultPrize()); m.put("surprisePrize", s.surprisePrize()); m.put("sound", s.sound()); m.put("volume", s.volume());
    return m;
  }
}
