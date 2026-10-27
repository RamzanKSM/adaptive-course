"""THROW_BASIC — «Выброс исключения throw» (Java). Taught before: everything up to try/catch and finally, methods,
classes with private fields and setters. Here: a method reports a bad value itself with
throw new IllegalArgumentException("своё сообщение"), and main catches it and prints e.getMessage() — our own text,
never one of Java's. The checks call the method through reflection to make sure it really throws. Not yet: throws."""
from java_tasks import JavaOutputTask

SKILL = "THROW_BASIC"


def with_methods(main: str, methods: str) -> str:
    """Body of main followed by more static methods of Solution (the template's closing brace ends the last one)."""
    body = methods.strip()
    assert body.endswith("}")
    return main.rstrip() + "\n}\n\n" + body[:-1].rstrip()


# ── 1. Аттракцион ──
RIDE_MAIN = ('try {\n    checkHeight(height);\n    System.out.println("Welcome aboard, height " + height + " cm");\n'
             '} catch (IllegalArgumentException e) {\n    System.out.println("Sorry: " + e.getMessage());\n}')
RIDE_CHECK = """static void checkHeight(int height) {
    if (height < 120) {
        throw new IllegalArgumentException("need 120 cm, you are " + height + " cm");
    }
}"""
RIDE_CHECKS = """Method m = null;
try { m = Solution.class.getDeclaredMethod("checkHeight", int.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()), "Добавь в класс Solution метод static void checkHeight(int height): проверка роста должна жить в нём");
m.setAccessible(true);
boolean thrown = false;
try { m.invoke(null, 100); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
need(thrown, "Метод checkHeight должен выбрасывать IllegalArgumentException через throw, если рост меньше 120 см");
try { m.invoke(null, 150); } catch (InvocationTargetException e) { need(false, "Для роста 150 см метод checkHeight не должен выбрасывать исключение"); }"""

# ── 2. Банкомат ──
ATM_MAIN = ('try {\n    int left = withdraw(balance, amount);\n    System.out.println("Withdrawn: " + amount + " rub");\n'
            '    System.out.println("Left: " + left + " rub");\n'
            '} catch (IllegalArgumentException e) {\n    System.out.println("Error: " + e.getMessage());\n}')
ATM_METHOD = """static int withdraw(int balance, int amount) {
    if (amount % 100 != 0) {
        throw new IllegalArgumentException("the ATM gives only multiples of 100 rub");
    }
    if (amount > balance) {
        throw new IllegalArgumentException("not enough money, balance " + balance + " rub");
    }
    return balance - amount;
}"""
ATM_CHECKS = """Method m = null;
try { m = Solution.class.getDeclaredMethod("withdraw", int.class, int.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, "Добавь в класс Solution метод static int withdraw(int balance, int amount): он возвращает, сколько останется на карте");
m.setAccessible(true);
for (int[] bad : new int[][]{{1000, 150}, {1000, 1100}}) {
  boolean thrown = false;
  try { m.invoke(null, bad[0], bad[1]); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
  need(thrown, "Метод withdraw должен выбрасывать IllegalArgumentException через throw, если сумма не кратна 100 или больше, чем на карте");
}
Object left = null;
try { left = m.invoke(null, 1000, 300); } catch (InvocationTargetException e) { }
need(Integer.valueOf(700).equals(left), "withdraw(1000, 300) должен вернуть 700 — столько останется на карте");"""

# ── 3. Плейлист ──
PLAYLIST = """class Playlist {
    private List<String> songs = new ArrayList<>();
    private int limit;

    Playlist(int limit) {
        this.limit = limit;
    }

    void add(String song) {
        if (songs.contains(song)) {
            throw new IllegalArgumentException("Already in the playlist: " + song);
        }
        if (songs.size() >= limit) {
            throw new IllegalArgumentException("Playlist is full, skipped: " + song);
        }
        songs.add(song);
    }

    int size() {
        return songs.size();
    }
}"""
PLAYLIST_MAIN = ('Playlist playlist = new Playlist(limit);\nfor (String song : requests) {\n    try {\n'
                 '        playlist.add(song);\n        System.out.println("Added: " + song);\n'
                 '    } catch (IllegalArgumentException e) {\n        System.out.println(e.getMessage());\n    }\n}\n'
                 'System.out.println("Songs: " + playlist.size());')
PLAYLIST_CHECKS = """Class<?> c = cls("Playlist");
need(c != null, "Создай класс Playlist: он хранит песни и сам проверяет каждую новую");
Method add = null;
try { add = c.getDeclaredMethod("add", String.class); } catch (NoSuchMethodException e) { }
need(add != null, "Добавь в класс Playlist метод void add(String song)");
Object playlist = null;
try { Constructor<?> k = c.getDeclaredConstructor(int.class); k.setAccessible(true); playlist = k.newInstance(1); } catch (NoSuchMethodException | InvocationTargetException e) { }
need(playlist != null, "Добавь в класс Playlist конструктор Playlist(int limit)");
add.setAccessible(true);
try { add.invoke(playlist, "Song A"); } catch (InvocationTargetException e) { need(false, "В пустой плейлист на 1 песню метод add должен добавлять песню без исключения"); }
boolean thrown = false;
try { add.invoke(playlist, "Song A"); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
need(thrown, "Метод add должен выбрасывать IllegalArgumentException через throw, если такая песня уже есть в плейлисте");
thrown = false;
try { add.invoke(playlist, "Song B"); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
need(thrown, "Метод add должен выбрасывать IllegalArgumentException через throw, если плейлист уже заполнен");"""


TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-throw-rt-ride-height", title="Рост для аттракциона",
        given=[("int", "height")],
        variants=[{"height": "135"}, {"height": "110"}, {"height": "160"}],
        hidden=[{"height": "120"}, {"height": "119"}, {"height": "95"}, {"height": "181"}],
        intro="На американские горки пускают только тех, чей рост не меньше 120 см. Рост посетителя записан в поле "
              "`height`. Проверку вынеси в отдельный метод: если рост не подходит, он должен сообщить об этом исключением.",
        steps=["Добавь в класс `Solution` метод `static void checkHeight(int height)`. Если рост меньше 120, он "
               "выбрасывает исключение с сообщением вида `need 120 cm, you are 110 cm` (с числом из `height`): "
               "`throw new IllegalArgumentException(\"need 120 cm, you are \" + height + \" cm\");`",
               "В `main` в блоке `try` вызови `checkHeight(height)`, а следующей строкой выведи строку вида "
               "`Welcome aboard, height 135 cm`.",
               "В блоке `catch (IllegalArgumentException e)` выведи `Sorry: ` и текст исключения — его возвращает "
               "`e.getMessage()`."],
        hint="После `throw` метод сразу прерывается, строка приветствия в `try` пропускается, и Java переходит в "
             "`catch`. Посетитель ростом ровно 120 см проходит.",
        solution=with_methods(RIDE_MAIN, RIDE_CHECK),
        wrong=[("нестрогая граница height <= 120 — посетителя ровно 120 см не пускают",
                with_methods(RIDE_MAIN, RIDE_CHECK.replace("height < 120", "height <= 120"))),
               ("печатает приветствие до проверки — при отказе выводятся обе строки",
                with_methods('try {\n    System.out.println("Welcome aboard, height " + height + " cm");\n'
                             '    checkHeight(height);\n} catch (IllegalArgumentException e) {\n'
                             '    System.out.println("Sorry: " + e.getMessage());\n}', RIDE_CHECK))],
        constructs=["try", "function", "if"],
        checks=RIDE_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-throw-rt-atm-withdraw", title="Снять деньги в банкомате",
        given=[("int", "balance"), ("int", "amount")],
        variants=[{"balance": "1200", "amount": "500"}, {"balance": "3000", "amount": "750"},
                  {"balance": "400", "amount": "1000"}],
        hidden=[{"balance": "900", "amount": "900"}, {"balance": "900", "amount": "1000"},
                {"balance": "5000", "amount": "50"}, {"balance": "0", "amount": "100"},
                {"balance": "2500", "amount": "2400"}],
        intro="Банкомат выдаёт деньги только купюрами по 100 руб. На карте лежит `balance` руб., а человек хочет снять "
              "`amount` руб. Метод выдачи отказывает в двух случаях, и в каждом — со своим объяснением.",
        steps=["Добавь в класс `Solution` метод `static int withdraw(int balance, int amount)`, который возвращает, "
               "сколько рублей останется на карте.",
               "Если `amount` не делится на 100 без остатка, метод выбрасывает `IllegalArgumentException` с сообщением "
               "`the ATM gives only multiples of 100 rub`.",
               "Если `amount` больше `balance`, метод выбрасывает `IllegalArgumentException` с сообщением вида "
               "`not enough money, balance 400 rub` — с числом из `balance`.",
               "В `main` в блоке `try` вызови `withdraw(balance, amount)` и выведи две строки: `Withdrawn: 500 rub` и "
               "`Left: 700 rub`. В `catch` выведи `Error: ` и сообщение исключения."],
        hint="Делится ли число на 100, покажет остаток `amount % 100`. Снять всё до последнего рубля можно — "
             "отказ только тогда, когда просят больше, чем есть.",
        solution=with_methods(ATM_MAIN, ATM_METHOD),
        wrong=[("нестрогая граница amount >= balance — нельзя снять всё до последнего рубля",
                with_methods(ATM_MAIN, ATM_METHOD.replace("amount > balance", "amount >= balance"))),
               ("печатает «Withdrawn» до вызова withdraw — при отказе появляется лишняя строка",
                with_methods('try {\n    System.out.println("Withdrawn: " + amount + " rub");\n'
                             '    int left = withdraw(balance, amount);\n    System.out.println("Left: " + left + " rub");\n'
                             '} catch (IllegalArgumentException e) {\n    System.out.println("Error: " + e.getMessage());\n}',
                             ATM_METHOD))],
        constructs=["try", "function", "if"],
        checks=ATM_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-throw-rt-party-playlist", title="Плейлист для вечеринки",
        given=[("int", "limit"), ("List<String>", "requests")],
        variants=[{"limit": "3", "requests": 'new ArrayList<>(List.of("Sun", "Rain", "Sun", "Wind", "Snow"))'},
                  {"limit": "2", "requests": 'new ArrayList<>(List.of("Road", "Road", "Sea"))'},
                  {"limit": "4", "requests": 'new ArrayList<>(List.of("Fire", "Ice", "Stone", "Ice", "Gold", "Fire", "Sky"))'}],
        hidden=[{"limit": "3", "requests": "new ArrayList<>()"},
                {"limit": "1", "requests": 'new ArrayList<>(List.of("One", "Two", "One"))'},
                {"limit": "5", "requests": 'new ArrayList<>(List.of("A", "B", "C", "D", "E"))'},
                {"limit": "2", "requests": 'new ArrayList<>(List.of("X", "X", "X", "Y", "Z", "Y"))'}],
        intro="На вечеринке гости по очереди заказывают песни — заказы лежат в списке `requests`. В плейлист помещается "
              "не больше `limit` песен, и одна песня не должна звучать дважды. Плейлист сам проверяет каждую песню "
              "и сообщает о проблеме исключением.",
        steps=["Создай класс `Playlist` с приватным списком `private List<String> songs = new ArrayList<>();`, "
               "приватным полем `limit`, конструктором `Playlist(int limit)` и методом `int size()` — сколько песен "
               "в плейлисте.",
               "Добавь метод `void add(String song)`: если такая песня уже есть в списке, он выбрасывает "
               "`IllegalArgumentException` с сообщением вида `Already in the playlist: Sun`; иначе если в списке уже "
               "`limit` песен — с сообщением вида `Playlist is full, skipped: Snow`; иначе добавляет песню.",
               "В `main` создай один плейлист и для каждой песни из `requests` в блоке `try` вызови `add` и выведи "
               "строку вида `Added: Sun`; в `catch` выведи только сообщение исключения.",
               "После всех заказов выведи строку вида `Songs: 3`."],
        hint="Порядок проверок важен: повтор проверяется первым, поэтому повторный заказ в полном плейлисте "
             "получает сообщение про повтор. И `try` ставь внутри цикла — тогда отказ одной песне не мешает остальным.",
        solution=PLAYLIST_MAIN,
        classes=PLAYLIST,
        wrong=[("проверяет заполненность через > вместо >= — в плейлист влезает лишняя песня",
                PLAYLIST_MAIN, PLAYLIST.replace("songs.size() >= limit", "songs.size() > limit")),
               ("try вокруг всего цикла — после первого отказа остальные заказы не обрабатываются",
                'Playlist playlist = new Playlist(limit);\ntry {\n    for (String song : requests) {\n'
                '        playlist.add(song);\n        System.out.println("Added: " + song);\n    }\n'
                '} catch (IllegalArgumentException e) {\n    System.out.println(e.getMessage());\n}\n'
                'System.out.println("Songs: " + playlist.size());'),
               ("проверяет заполненность раньше повтора — повторный заказ в полном плейлисте получает не ту причину",
                PLAYLIST_MAIN, PLAYLIST.replace(
                    '        if (songs.contains(song)) {\n            throw new IllegalArgumentException("Already in the playlist: " + song);\n        }\n'
                    '        if (songs.size() >= limit) {\n            throw new IllegalArgumentException("Playlist is full, skipped: " + song);\n        }\n',
                    '        if (songs.size() >= limit) {\n            throw new IllegalArgumentException("Playlist is full, skipped: " + song);\n        }\n'
                    '        if (songs.contains(song)) {\n            throw new IllegalArgumentException("Already in the playlist: " + song);\n        }\n'))],
        constructs=["try", "class", "for"],
        checks=PLAYLIST_CHECKS,
    ),
]
