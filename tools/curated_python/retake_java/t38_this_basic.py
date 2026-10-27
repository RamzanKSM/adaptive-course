"""THIS_BASIC — «Ключевое слово this» (Java). Taught before: everything up to static methods of Solution, classes,
creating objects, constructors. Here: a parameter named like a field hides the field, and `this.field` reaches the
field of the current object — in a constructor and in methods that change the object; `this` is the object the
method was called on, as opposed to another object passed in as a parameter. Not yet: private, static fields."""
from java_tasks import JavaOutputTask

SKILL = "THIS_BASIC"


def find_class(name: str) -> str:
    return (f'Class<?> c = cls("{name}");\n'
            f'need(c != null, "Создай класс {name} ниже класса Solution (после его закрывающей скобки) и без слова public");\n')


def need_field(cls: str, name: str, java_type: str, why: str) -> str:
    """An instance (non-static) field of the class with this name and type."""
    return (f'{{ Field f = null; try {{ f = c.getDeclaredField("{name}"); }} catch (NoSuchFieldException e) {{ }}\n'
            f'  need(f != null && f.getType() == {java_type}.class, "Объяви в классе {cls} поле {java_type} {name} — {why}");\n'
            f'  need(!Modifier.isStatic(f.getModifiers()), "Объяви поле {name} в классе {cls} без слова static — тогда у каждого объекта будет своё значение"); }}\n')


def _types(cls: str, params: list[str]) -> str:
    return ", ".join("c" if p.split()[0] == cls else f"{p.split()[0]}.class" for p in params)


def need_constructor(cls: str, params: list[str], why: str) -> str:
    return (f'{{ Constructor<?> k = null; try {{ k = c.getDeclaredConstructor({_types(cls, params)}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(k != null, "Добавь в класс {cls} конструктор {cls}({", ".join(params)}) — {why}"); }}\n')


def need_method(cls: str, returns: str, name: str, params: list[str], why: str) -> str:
    """A non-static method with these parameter types and return type."""
    types = _types(cls, params)
    return (f'{{ Method m = null; try {{ m = c.getDeclaredMethod("{name}"{", " + types if types else ""}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(m != null && m.getReturnType() == {returns}.class, "Добавь в класс {cls} метод {returns} {name}({", ".join(params)}) — {why}");\n'
            f'  need(!Modifier.isStatic(m.getModifiers()), "Метод {name} в классе {cls} пиши без слова static — он работает с полями своего объекта"); }}\n')


def need_built(cls: str, params: list[str], args: str, expect: dict[str, str], message: str) -> str:
    """Creates an object with this constructor and compares its fields with the expected values (Java source)."""
    code = (f'{{ Constructor<?> k = c.getDeclaredConstructor({_types(cls, params)}); k.setAccessible(true);\n'
            f'  Object o = null; try {{ o = k.newInstance({args}); }} catch (Exception e) {{ }}\n')
    conditions = []
    for i, (name, value) in enumerate(expect.items()):
        code += f'  Field f{i} = c.getDeclaredField("{name}"); f{i}.setAccessible(true);\n'
        conditions.append(f"Objects.equals(f{i}.get(o), {value})")
    return code + f'  need(o != null && {" && ".join(conditions)}, "{message}"); }}\n'


# ───────── Game profile ─────────


# ───────── Movie length ─────────

MOVIE = '''class Movie {
    String title;
    int minutes;

    Movie(String title, int minutes) {
        this.title = title;
        this.minutes = minutes;
    }

    int hours() {
        return this.minutes / 60;
    }
}'''

MOVIE_MAIN = '''Movie movie = new Movie(title, minutes);
System.out.println("Movie: " + movie.title);
System.out.println("Length: " + movie.hours() + " h " + movie.minutes % 60 + " min");'''

# ───────── Kettle ─────────

KETTLE = '''class Kettle {
    String brand;
    int water;

    Kettle(String brand, int water) {
        this.brand = brand;
        this.water = water;
    }

    int pour(int water) {
        int spilled = 0;
        this.water += water;
        if (this.water > 1700) {
            spilled = this.water - 1700;
            this.water = 1700;
        }
        return spilled;
    }
}'''

KETTLE_MAIN = '''Kettle kettle = new Kettle(brand, start);
for (int i = 0; i < pours.length; i++) {
    int spilled = kettle.pour(pours[i]);
    if (spilled > 0) {
        System.out.println("+" + pours[i] + " ml, spilled " + spilled + " ml");
    } else {
        System.out.println("+" + pours[i] + " ml");
    }
}
System.out.println(kettle.brand + ": " + kettle.water + " ml");'''

KETTLE_BEHAVIOUR = '''{ Constructor<?> k = c.getDeclaredConstructor(String.class, int.class); k.setAccessible(true);
  Object o = null; try { o = k.newInstance("T", 1000); } catch (Exception e) { }
  Field fw = c.getDeclaredField("water"); fw.setAccessible(true);
  need(o != null && Objects.equals(fw.get(o), 1000), "Конструктор Kettle должен записать параметры в поля объекта: this.brand = brand; и this.water = water;");
  Method p = c.getDeclaredMethod("pour", int.class); p.setAccessible(true);
  Object r1 = null, r2 = null; try { r1 = p.invoke(o, 500); r2 = p.invoke(o, 300); } catch (Exception e) { }
  need(Objects.equals(r1, 0) && Objects.equals(r2, 100) && Objects.equals(fw.get(o), 1700), "Метод pour(int water) должен прибавлять параметр water к полю this.water, не давать ему стать больше 1700 и возвращать, сколько пролилось"); }
'''

# ───────── Chess rating ─────────

CHESS = '''class ChessPlayer {
    String name;
    int rating;

    ChessPlayer(String name, int rating) {
        this.name = name;
        this.rating = rating;
    }

    int beat(ChessPlayer other) {
        int bonus = 10;
        if (other.rating > this.rating) {
            bonus = 20;
        }
        this.rating += bonus;
        other.rating -= bonus;
        return bonus;
    }
}'''

CHESS_MAIN = '''ChessPlayer first = new ChessPlayer(name1, rating1);
ChessPlayer second = new ChessPlayer(name2, rating2);
for (int i = 0; i < winners.length; i++) {
    ChessPlayer winner;
    ChessPlayer loser;
    if (winners[i] == 1) {
        winner = first;
        loser = second;
    } else {
        winner = second;
        loser = first;
    }
    int bonus = winner.beat(loser);
    System.out.println(winner.name + " beats " + loser.name + ": +" + bonus);
}
System.out.println(first.name + ": " + first.rating);
System.out.println(second.name + ": " + second.rating);'''

CHESS_BEHAVIOUR = '''{ Constructor<?> k = c.getDeclaredConstructor(String.class, int.class); k.setAccessible(true);
  Method beat = c.getDeclaredMethod("beat", c); beat.setAccessible(true);
  Field fr = c.getDeclaredField("rating"); fr.setAccessible(true);
  Object a = null, b = null, r = null;
  try { a = k.newInstance("A", 1500); b = k.newInstance("B", 1400); r = beat.invoke(a, b); } catch (Exception e) { }
  need(a != null && Objects.equals(r, 10) && Objects.equals(fr.get(a), 1510) && Objects.equals(fr.get(b), 1390), "Метод beat(other) должен прибавлять очки победителю this и отнимать у other — 10 очков, если рейтинг соперника не выше");
  Object r2 = null; try { r2 = beat.invoke(b, a); } catch (Exception e) { }
  need(Objects.equals(r2, 20) && Objects.equals(fr.get(b), 1410) && Objects.equals(fr.get(a), 1490), "Если у соперника other рейтинг выше, чем у this, победитель получает 20 очков, а проигравший их теряет"); }
'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-this-rt-movie-length", title="Длина фильма",
        given=[("String", "title"), ("int", "minutes")],
        variants=[{"title": '"Interstellar"', "minutes": "169"}, {"title": '"Shrek"', "minutes": "90"},
                  {"title": '"Up"', "minutes": "96"}],
        hidden=[{"title": '"Short"', "minutes": "45"}, {"title": '"Titanic"', "minutes": "195"},
                {"title": '"Avatar"', "minutes": "162"}, {"title": '"Cartoon"', "minutes": "120"}],
        intro="В кинотеатре на афише пишут длину фильма в часах и минутах, а в базе она хранится одним числом минут. "
              "Название фильма записано в поле `title`, длина в минутах — в поле `minutes`.",
        steps=["Ниже класса `Solution` создай класс `Movie` (без `public`) с полями `String title` и `int minutes`.",
               "Добавь конструктор `Movie(String title, int minutes)` — параметры называются так же, как поля. Запиши их "
               "в поля через `this`: `this.title = title;` и так же для `minutes`.",
               "Добавь метод `int hours()`: он возвращает, сколько полных часов в фильме, — `this.minutes / 60`.",
               "В `main` создай фильм `new Movie(title, minutes)` и выведи две строки вида `Movie: Interstellar` и "
               "`Length: 2 h 49 min`. Часы получи вызовом `hours()`, а оставшиеся минуты — как остаток `minutes % 60` "
               "от поля объекта."],
        hint="В конструкторе имя `minutes` без точки — это параметр, он закрывает поле с тем же именем. Строка "
             "`minutes = minutes;` присвоит параметр самому себе, а поле останется нулём. Поле объекта — это `this.minutes`.",
        solution=MOVIE_MAIN,
        classes=MOVIE,
        wrong=[("в конструкторе забыл this у минут: `minutes = minutes;` — поле остаётся 0",
                MOVIE_MAIN, MOVIE.replace("this.minutes = minutes;", "minutes = minutes;")),
               ("в hours() берёт остаток вместо деления",
                MOVIE_MAIN, MOVIE.replace("return this.minutes / 60;", "return this.minutes % 60;"))],
        constructs=["class"],
        checks=find_class("Movie")
               + need_field("Movie", "title", "String", "название фильма")
               + need_field("Movie", "minutes", "int", "длина фильма в минутах")
               + need_constructor("Movie", ["String title", "int minutes"], "он заполняет поля, когда создаётся объект")
               + need_built("Movie", ["String title", "int minutes"], '"Test", 130', {"title": '"Test"', "minutes": "130"},
                            "Конструктор Movie должен записать параметры в поля объекта: this.title = title; и this.minutes = minutes;")
               + need_method("Movie", "int", "hours", [], "он возвращает число полных часов"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-this-rt-kettle-pour", title="Полный чайник",
        given=[("String", "brand"), ("int", "start"), ("int[]", "pours")],
        variants=[{"brand": '"Bosch"', "start": "500", "pours": "{400, 600, 300}"},
                  {"brand": '"Tefal"', "start": "0", "pours": "{1000, 500, 500}"},
                  {"brand": '"Vitek"', "start": "1200", "pours": "{200, 100}"}],
        hidden=[{"brand": '"Polaris"', "start": "1700", "pours": "{100}"},
                {"brand": '"Scarlett"', "start": "1000", "pours": "{700, 1}"},
                {"brand": '"Kitfort"', "start": "300", "pours": "{}"},
                {"brand": '"Redmond"', "start": "0", "pours": "{250, 250, 250, 250, 250, 250, 250, 250}"}],
        intro="В чайник помещается не больше 1700 мл воды. Сейчас в чайнике марки `brand` уже `start` мл, и в него "
              "по очереди подливают воду из кружек — объёмы по порядку записаны в массиве `pours`. Что не поместилось, "
              "проливается.",
        steps=["Ниже класса `Solution` создай класс `Kettle` (без `public`) с полями `String brand` и `int water` и "
               "конструктором `Kettle(String brand, int water)`, который записывает параметры в поля через `this`.",
               "Добавь метод `int pour(int water)` — параметр называется так же, как поле. Метод прибавляет параметр `water` "
               "к полю `this.water`; если в поле стало больше 1700, он оставляет в поле 1700 и возвращает, сколько "
               "миллилитров пролилось, а иначе возвращает 0.",
               "В `main` создай чайник `new Kettle(brand, start)` и для каждого числа из `pours` вызови `pour`. Если что-то "
               "пролилось, выведи строку вида `+300 ml, spilled 100 ml`, иначе — строку вида `+400 ml`.",
               "Последней строкой выведи строку вида `Bosch: 1700 ml` — марку и сколько воды в чайнике в конце."],
        hint="В методе `pour` есть два `water`: просто `water` — это параметр, сколько подливают сейчас, а `this.water` — "
             "сколько воды уже в чайнике. Сначала посчитай, сколько пролилось (`this.water - 1700`), и только потом "
             "поставь в поле 1700.",
        solution=KETTLE_MAIN,
        classes=KETTLE,
        wrong=[("в pour забыл this: `water += water;` удваивает параметр, а воды в чайнике не прибавляется",
                KETTLE_MAIN, KETTLE.replace("        this.water += water;\n        if (this.water > 1700)",
                                            "        water += water;\n        if (this.water > 1700)")),
               ("сначала ставит в поле 1700, а потом считает пролитое — выходит 0",
                KETTLE_MAIN, KETTLE.replace("            spilled = this.water - 1700;\n            this.water = 1700;",
                                            "            this.water = 1700;\n            spilled = this.water - 1700;"))],
        constructs=["class"],
        checks=find_class("Kettle")
               + need_field("Kettle", "brand", "String", "марка чайника")
               + need_field("Kettle", "water", "int", "сколько воды в чайнике")
               + need_constructor("Kettle", ["String brand", "int water"], "он заполняет поля, когда создаётся объект")
               + need_method("Kettle", "int", "pour", ["int water"], "он подливает воду и возвращает, сколько пролилось")
               + KETTLE_BEHAVIOUR,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-this-rt-chess-rating", title="Шахматный рейтинг",
        given=[("String", "name1"), ("int", "rating1"), ("String", "name2"), ("int", "rating2"), ("int[]", "winners")],
        variants=[{"name1": '"Anya"', "rating1": "1500", "name2": '"Boris"', "rating2": "1480", "winners": "{2, 2, 1}"},
                  {"name1": '"Gleb"', "rating1": "1200", "name2": '"Nina"', "rating2": "1300", "winners": "{1, 1, 2, 1}"},
                  {"name1": '"Sveta"', "rating1": "1600", "name2": '"Artem"', "rating2": "1600", "winners": "{1, 2}"}],
        hidden=[{"name1": '"Dasha"', "rating1": "1000", "name2": '"Egor"', "rating2": "1010", "winners": "{1}"},
                {"name1": '"Kira"', "rating1": "1450", "name2": '"Lesha"', "rating2": "1450", "winners": "{2}"},
                {"name1": '"Roma"', "rating1": "1700", "name2": '"Yulya"', "rating2": "1500", "winners": "{}"},
                {"name1": '"Vanya"', "rating1": "1395", "name2": '"Tanya"', "rating2": "1400", "winners": "{2, 1, 1, 1, 2, 2}"}],
        intro="Двое шахматистов, `name1` с рейтингом `rating1` и `name2` с рейтингом `rating2`, сыграли несколько партий. "
              "Кто выиграл каждую партию, по порядку записано в массиве `winners`: 1 — первый, 2 — второй. Победитель "
              "забирает у проигравшего 10 очков рейтинга, а если обыграл соперника с более высоким рейтингом — 20.",
        steps=["Ниже класса `Solution` создай класс `ChessPlayer` (без `public`) с полями `String name` и `int rating` и "
               "конструктором `ChessPlayer(String name, int rating)`, который записывает параметры в поля через `this`.",
               "Добавь метод `int beat(ChessPlayer other)`. Победитель — это `this`, проигравший — `other`. Метод берёт "
               "бонус 10, а если `other.rating` больше `this.rating` — 20; прибавляет бонус к рейтингу `this`, отнимает его "
               "у `other` и возвращает бонус.",
               "В `main` создай игроков `first` и `second`. Для каждой партии выбери победителя и проигравшего по числу из "
               "`winners`, вызови у победителя `beat` и выведи строку вида `Boris beats Anya: +20`.",
               "В конце выведи две строки вида `Anya: 1490` — итоговый рейтинг первого игрока, потом второго."],
        hint="В вызове `winner.beat(loser)` внутри метода `this` — это `winner`, а `other` — `loser`. Рейтинги сравнивай до "
             "того, как их меняешь. При равных рейтингах бонус обычный, 10 очков.",
        solution=CHESS_MAIN,
        classes=CHESS,
        wrong=[("сравнивает рейтинги наоборот: 20 очков даёт за победу над более слабым",
                CHESS_MAIN, CHESS.replace("other.rating > this.rating", "this.rating > other.rating")),
               ("перепутал this и other: очки прибавляются проигравшему",
                CHESS_MAIN, CHESS.replace("this.rating += bonus;\n        other.rating -= bonus;",
                                          "this.rating -= bonus;\n        other.rating += bonus;"))],
        constructs=["class", "for"],
        checks=find_class("ChessPlayer")
               + need_field("ChessPlayer", "name", "String", "имя шахматиста")
               + need_field("ChessPlayer", "rating", "int", "рейтинг шахматиста")
               + need_constructor("ChessPlayer", ["String name", "int rating"], "он заполняет поля, когда создаётся объект")
               + need_built("ChessPlayer", ["String name", "int rating"], '"Test", 1234', {"name": '"Test"', "rating": "1234"},
                            "Конструктор ChessPlayer должен записать параметры в поля объекта: this.name = name; и this.rating = rating;")
               + need_method("ChessPlayer", "int", "beat", ["ChessPlayer other"], "он переносит очки рейтинга от other к this")
               + CHESS_BEHAVIOUR,
    ),
]
