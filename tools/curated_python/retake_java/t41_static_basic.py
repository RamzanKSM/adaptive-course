"""STATIC_BASIC — «static» (Java). Taught before: everything up to static methods of Solution, classes, creating
objects, constructors, this, private fields, getters and setters. Here: a static method of another class is called
through the class name without creating an object; a static field is one for the whole class — a counter of created
objects that gives each one its number; a shared value changed once through the class name reaches every object.
Static state lives between runs of main, so the check resets it before each run (`reset`). Not yet: inheritance,
interfaces, collections, exceptions."""
from java_tasks import JavaOutputTask

SKILL = "STATIC_BASIC"


def find_class(name: str) -> str:
    return (f'Class<?> c = cls("{name}");\n'
            f'need(c != null, "Создай класс {name} ниже класса Solution (после его закрывающей скобки) и без слова public");\n')


def need_field(cls: str, name: str, java_type: str, why: str, static: bool = False) -> str:
    """A field of the class with this name and type: static (one for the class) or an ordinary one (one per object)."""
    code = (f'{{ Field f = null; try {{ f = c.getDeclaredField("{name}"); }} catch (NoSuchFieldException e) {{ }}\n'
            f'  need(f != null && f.getType() == {java_type}.class, "Объяви в классе {cls} поле {"static " if static else ""}{java_type} {name} — {why}");\n')
    if static:
        code += f'  need(Modifier.isStatic(f.getModifiers()), "Сделай поле {name} статическим: static {java_type} {name} — {why}"); }}\n'
    else:
        code += f'  need(!Modifier.isStatic(f.getModifiers()), "Объяви поле {name} в классе {cls} без слова static — тогда у каждого объекта будет своё значение"); }}\n'
    return code


def need_method(cls: str, returns: str, name: str, params: list[str], why: str, static: bool = False) -> str:
    types = ", ".join(f"{p.split()[0]}.class" for p in params)
    signature = f"{'static ' if static else ''}{returns} {name}({', '.join(params)})"
    code = (f'{{ Method m = null; try {{ m = c.getDeclaredMethod("{name}"{", " + types if types else ""}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(m != null && m.getReturnType() == {returns}.class, "Добавь в класс {cls} метод {signature} — {why}");\n')
    if static:
        code += (f'  need(Modifier.isStatic(m.getModifiers()), "Сделай метод {name} статическим: {signature} — '
                 f'тогда его вызывают через имя класса, без создания объекта"); }}\n')
    else:
        code += f'  need(!Modifier.isStatic(m.getModifiers()), "Метод {name} в классе {cls} пиши без слова static — он работает с полями своего объекта"); }}\n'
    return code


def need_constructor(cls: str, params: list[str], why: str) -> str:
    types = ", ".join(f"{p.split()[0]}.class" for p in params)
    return (f'{{ Constructor<?> k = null; try {{ k = c.getDeclaredConstructor({types}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(k != null, "Добавь в класс {cls} конструктор {cls}({", ".join(params)}) — {why}"); }}\n')



# ───────── League points ─────────

LEAGUE = '''class League {
    static int points(int wins, int draws) {
        return wins * 3 + draws;
    }
}'''

LEAGUE_MAIN = '''for (int i = 0; i < teams.length; i++) {
    System.out.println(teams[i] + ": " + League.points(wins[i], draws[i]) + " points");
}'''

# ───────── Jump record ─────────

JUMP = '''class Jump {
    static int record = 0;
    String athlete;
    int cm;
    boolean newRecord;

    Jump(String athlete, int cm) {
        this.athlete = athlete;
        this.cm = cm;
        if (cm > record) {
            record = cm;
            this.newRecord = true;
        }
    }
}'''

JUMP_MAIN = '''for (int i = 0; i < athletes.length; i++) {
    Jump jump = new Jump(athletes[i], results[i]);
    if (jump.newRecord) {
        System.out.println(jump.athlete + ": " + jump.cm + " cm, new record");
    } else {
        System.out.println(jump.athlete + ": " + jump.cm + " cm");
    }
}
System.out.println("Record: " + Jump.record + " cm");'''

JUMP_BEHAVIOUR = '''{ setStatic("Jump", "record", 0);
  Constructor<?> k = c.getDeclaredConstructor(String.class, int.class); k.setAccessible(true);
  Object a = null, b = null, d = null; try { a = k.newInstance("A", 300); b = k.newInstance("B", 280); d = k.newInstance("D", 300); } catch (Exception e) { }
  Field fr = c.getDeclaredField("record"); fr.setAccessible(true);
  Field fn = c.getDeclaredField("newRecord"); fn.setAccessible(true);
  need(d != null && Objects.equals(fr.get(null), 300) && Objects.equals(fn.get(a), true) && Objects.equals(fn.get(b), false) && Objects.equals(fn.get(d), false),
       "Конструктор Jump должен обновлять общий рекорд record, только если прыжок дальше рекорда, и тогда отмечать newRecord = true");
  setStatic("Jump", "record", 0); }
'''

# ───────── Hall booking ─────────

BOOKING = '''class Booking {
    static int freeSeats = 0;
    static int confirmed = 0;
    String name;
    int seats;
    boolean ok;

    Booking(String name, int seats) {
        this.name = name;
        this.seats = seats;
        if (seats <= freeSeats) {
            freeSeats -= seats;
            confirmed++;
            this.ok = true;
        }
    }

    static void open(int capacity) {
        freeSeats = capacity;
        confirmed = 0;
    }
}'''

BOOKING_MAIN = '''Booking.open(capacity);
for (int i = 0; i < names.length; i++) {
    Booking booking = new Booking(names[i], seats[i]);
    if (booking.ok) {
        System.out.println(booking.name + ": seats " + booking.seats + ", confirmed");
    } else {
        System.out.println(booking.name + ": seats " + booking.seats + ", declined");
    }
}
System.out.println("Confirmed: " + Booking.confirmed);
System.out.println("Free seats: " + Booking.freeSeats);'''

BOOKING_BEHAVIOUR = '''{ Method open = c.getDeclaredMethod("open", int.class); open.setAccessible(true);
  Constructor<?> k = c.getDeclaredConstructor(String.class, int.class); k.setAccessible(true);
  Field ff = c.getDeclaredField("freeSeats"); ff.setAccessible(true);
  Field fc = c.getDeclaredField("confirmed"); fc.setAccessible(true);
  try { open.invoke(null, 10); k.newInstance("A", 6); k.newInstance("B", 5); k.newInstance("C", 4); } catch (Exception e) { }
  need(Objects.equals(ff.get(null), 0) && Objects.equals(fc.get(null), 2),
       "Конструктор Booking должен подтверждать бронь, только если мест хватает: уменьшать общее freeSeats и увеличивать общий счётчик confirmed");
  setStatic("Booking", "freeSeats", 0); setStatic("Booking", "confirmed", 0); }
'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-static-rt-league-points", title="Турнирная таблица",
        given=[("String[]", "teams"), ("int[]", "wins"), ("int[]", "draws")],
        variants=[{"teams": '{"Lions", "Tigers", "Bears"}', "wins": "{4, 2, 0}", "draws": "{1, 3, 5}"},
                  {"teams": '{"Comets", "Rockets"}', "wins": "{6, 5}", "draws": "{0, 2}"},
                  {"teams": '{"Wolves", "Foxes", "Eagles", "Sharks"}', "wins": "{3, 1, 7, 2}", "draws": "{2, 0, 1, 4}"}],
        hidden=[{"teams": '{"Owls"}', "wins": "{0}", "draws": "{0}"},
                {"teams": '{"Hawks", "Bisons"}', "wins": "{10, 0}", "draws": "{0, 9}"},
                {"teams": '{"Ravens", "Lynx", "Seals"}', "wins": "{1, 2, 3}", "draws": "{1, 2, 3}"}],
        intro="В школьном футбольном турнире за победу дают 3 очка, за ничью — 1, за поражение — 0. Посчитать очки — просто "
              "формула, объект для этого не нужен, поэтому метод делают статическим и вызывают через имя класса. Названия "
              "команд записаны в массиве `teams`, число побед — в `wins`, число ничьих — в `draws`, всё под одними номерами.",
        steps=["Ниже класса `Solution` создай класс `League` (без `public`) со статическим методом "
               "`static int points(int wins, int draws)`. Он возвращает `wins * 3 + draws`.",
               "В `main` не создавай объект `League`: вызывай метод через имя класса — `League.points(...)`.",
               "Для каждой команды выведи строку вида `Lions: 13 points`."],
        hint="Статический метод принадлежит классу, а не объекту, — как методы самого `Solution`, которые ты уже вызывал "
             "без `new`. Перед именем метода другого класса пиши имя класса и точку.",
        solution=LEAGUE_MAIN,
        classes=LEAGUE,
        wrong=[("метод без static — пришлось создавать объект, хотя он не нужен",
                LEAGUE_MAIN.replace("League.points(", "new League().points("),
                LEAGUE.replace("    static int points", "    int points")),
               ("перепутал веса: ничья стоит 3 очка, а победа — 1",
                LEAGUE_MAIN, LEAGUE.replace("wins * 3 + draws", "wins + draws * 3"))],
        constructs=["class"],
        checks=find_class("League")
               + need_method("League", "int", "points", ["int wins", "int draws"], "он считает очки команды", static=True),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-static-rt-jump-record", title="Рекорд по прыжкам",
        given=[("String[]", "athletes"), ("int[]", "results")],
        variants=[{"athletes": '{"Anya", "Boris", "Vika", "Gosha"}', "results": "{350, 320, 380, 380}"},
                  {"athletes": '{"Gleb", "Dina", "Egor"}', "results": "{410, 420, 430}"},
                  {"athletes": '{"Zoya", "Ilya"}', "results": "{300, 290}"}],
        hidden=[{"athletes": '{"Kira"}', "results": "{250}"},
                {"athletes": "{}", "results": "{}"},
                {"athletes": '{"Lev", "Mia", "Nik", "Olya", "Petya"}', "results": "{280, 310, 305, 311, 311}"}],
        intro="На соревнованиях по прыжкам в длину судья следит за рекордом дня. Рекорд один на всех участников, поэтому его "
              "хранят в статическом поле, а результат каждого прыжка — в обычном. Имена участников в порядке выступления "
              "записаны в массиве `athletes`, результаты в сантиметрах — в `results`.",
        steps=["Ниже класса `Solution` создай класс `Jump` (без `public`) со статическим полем `static int record = 0` и "
               "обычными полями `String athlete`, `int cm` и `boolean newRecord`.",
               "Добавь конструктор `Jump(String athlete, int cm)`: он сохраняет имя и результат, а если `cm` строго больше "
               "`record`, записывает `cm` в `record` и ставит этому прыжку `newRecord = true`.",
               "В `main` для каждого участника создай `new Jump(...)`. Если прыжок побил рекорд, выведи строку вида "
               "`Anya: 350 cm, new record`, иначе — строку вида `Boris: 320 cm`.",
               "Последней строкой выведи строку вида `Record: 380 cm` — значение статического поля через имя класса: `Jump.record`."],
        hint="Статическое поле одно на весь класс: каждый новый прыжок сравнивается с одним и тем же `record`, который "
             "оставили предыдущие прыжки. Повторить рекорд — не значит его побить.",
        solution=JUMP_MAIN,
        classes=JUMP,
        wrong=[("record — обычное поле: у каждого прыжка свой рекорд, и любой прыжок его «бьёт»",
                JUMP_MAIN.replace('System.out.println("Record: " + Jump.record + " cm");',
                                  'int best = 0;\nfor (int i = 0; i < results.length; i++) {\n    if (results[i] > best) {\n        best = results[i];\n    }\n}\nSystem.out.println("Record: " + best + " cm");'),
                JUMP.replace("    static int record = 0;", "    int record = 0;")),
               ("нестрогое сравнение: повторение рекорда тоже считается новым рекордом",
                JUMP_MAIN, JUMP.replace("cm > record", "cm >= record"))],
        constructs=["class"],
        checks=find_class("Jump")
               + need_field("Jump", "record", "int", "рекорд один на всех участников", static=True)
               + need_field("Jump", "athlete", "String", "имя участника")
               + need_field("Jump", "cm", "int", "результат прыжка")
               + need_field("Jump", "newRecord", "boolean", "побил ли этот прыжок рекорд")
               + need_constructor("Jump", ["String athlete", "int cm"], "он сохраняет прыжок и обновляет рекорд")
               + JUMP_BEHAVIOUR,
        reset='setStatic("Jump", "record", 0);',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-static-rt-hall-booking", title="Бронь мест в зале",
        given=[("int", "capacity"), ("String[]", "names"), ("int[]", "seats")],
        variants=[{"capacity": "10", "names": '{"Anya", "Boris", "Vika", "Gosha"}', "seats": "{4, 7, 6, 1}"},
                  {"capacity": "20", "names": '{"Gleb", "Dina", "Egor"}', "seats": "{20, 1, 3}"},
                  {"capacity": "8", "names": '{"Zoya", "Ilya", "Kira"}', "seats": "{3, 3, 3}"}],
        hidden=[{"capacity": "5", "names": '{"Lev"}', "seats": "{5}"},
                {"capacity": "0", "names": '{"Mia", "Nik"}', "seats": "{1, 2}"},
                {"capacity": "12", "names": "{}", "seats": "{}"},
                {"capacity": "15", "names": '{"Olya", "Petya", "Rita", "Sasha", "Tanya"}', "seats": "{16, 9, 7, 6, 1}"}],
        intro="В лектории `capacity` мест, и зрители бронируют их онлайн по очереди. Бронь подтверждают, только если "
              "свободных мест хватает на всю компанию, иначе её отклоняют. Свободные места и число подтверждённых броней — "
              "одни на весь зал, поэтому их хранят в статических полях. Имена — в массиве `names`, сколько мест хочет "
              "каждый — в `seats`.",
        steps=["Ниже класса `Solution` создай класс `Booking` (без `public`) со статическими полями `static int freeSeats = 0` и "
               "`static int confirmed = 0` и обычными полями `String name`, `int seats` и `boolean ok`.",
               "Добавь статический метод `static void open(int capacity)`: он записывает `capacity` в `freeSeats` и обнуляет "
               "`confirmed`. Добавь конструктор `Booking(String name, int seats)`: он сохраняет имя и число мест, а если "
               "`seats` не больше `freeSeats`, уменьшает `freeSeats`, увеличивает `confirmed` и ставит `ok = true`.",
               "В `main` сначала вызови `Booking.open(capacity)`. Потом для каждого зрителя создай `new Booking(...)` и выведи "
               "строку вида `Anya: seats 4, confirmed` или `Boris: seats 7, declined`.",
               "В конце выведи строки вида `Confirmed: 2` и `Free seats: 0` — значения статических полей через имя класса."],
        hint="Каждая бронь видит то `freeSeats`, что осталось после предыдущих: статическое поле одно на всех. "
             "Если мест осталось ровно столько, сколько просят, бронь подтверждается.",
        solution=BOOKING_MAIN,
        classes=BOOKING,
        wrong=[("строгое сравнение: когда мест ровно столько, сколько просят, бронь отклоняется",
                BOOKING_MAIN, BOOKING.replace("seats <= freeSeats", "seats < freeSeats")),
               ("не уменьшает freeSeats — все брони сравниваются с полным залом",
                BOOKING_MAIN, BOOKING.replace("            freeSeats -= seats;\n", ""))],
        constructs=["class"],
        checks=find_class("Booking")
               + need_field("Booking", "freeSeats", "int", "свободные места одни на весь зал", static=True)
               + need_field("Booking", "confirmed", "int", "счётчик подтверждённых броней один на весь зал", static=True)
               + need_field("Booking", "name", "String", "имя зрителя")
               + need_field("Booking", "seats", "int", "сколько мест просит зритель")
               + need_field("Booking", "ok", "boolean", "подтверждена ли бронь")
               + need_method("Booking", "void", "open", ["int capacity"], "он открывает продажу на весь зал", static=True)
               + need_constructor("Booking", ["String name", "int seats"], "он подтверждает бронь, если мест хватает")
               + BOOKING_BEHAVIOUR,
        reset='setStatic("Booking", "freeSeats", 0);\nsetStatic("Booking", "confirmed", 0);',
    ),
]
