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


# ───────── Temperature ─────────

TEMPERATURE = '''class Temperature {
    static int toFahrenheit(int celsius) {
        return celsius * 9 / 5 + 32;
    }
}'''

TEMPERATURE_MAIN = '''for (int i = 0; i < celsius.length; i++) {
    System.out.println(celsius[i] + " C = " + Temperature.toFahrenheit(celsius[i]) + " F");
}'''

# ───────── Exhibition visitors ─────────

VISITOR = '''class Visitor {
    static int count = 0;
    int number;
    String name;

    Visitor(String name) {
        count++;
        this.number = count;
        this.name = name;
    }
}'''

VISITOR_MAIN = '''for (int i = 0; i < names.length; i++) {
    Visitor visitor = new Visitor(names[i]);
    System.out.println("Visitor #" + visitor.number + ": " + visitor.name);
}
System.out.println("Total visitors: " + Visitor.count);'''

VISITOR_OWN_COUNTER = '''int total = 0;
for (int i = 0; i < names.length; i++) {
    Visitor visitor = new Visitor(names[i]);
    System.out.println("Visitor #" + visitor.number + ": " + visitor.name);
    total = visitor.count;
}
System.out.println("Total visitors: " + total);'''

VISITOR_BEHAVIOUR = '''{ setStatic("Visitor", "count", 0);
  Constructor<?> k = c.getDeclaredConstructor(String.class); k.setAccessible(true);
  Object a = null, b = null; try { a = k.newInstance("A"); b = k.newInstance("B"); } catch (Exception e) { }
  Field fc = c.getDeclaredField("count"); fc.setAccessible(true);
  Field fnum = c.getDeclaredField("number"); fnum.setAccessible(true);
  Field fname = c.getDeclaredField("name"); fname.setAccessible(true);
  need(b != null && Objects.equals(fc.get(null), 2) && Objects.equals(fnum.get(a), 1) && Objects.equals(fnum.get(b), 2) && Objects.equals(fname.get(b), "B"),
       "Конструктор Visitor должен увеличивать общий счётчик count на 1, записывать его новое значение в number и сохранять имя");
  setStatic("Visitor", "count", 0); }
'''

# ───────── Pass score ─────────

EXAM = '''class Exam {
    static int passScore = 60;
    String student;
    int score;

    Exam(String student, int score) {
        this.student = student;
        this.score = score;
    }

    boolean passed() {
        return score >= passScore;
    }
}'''

EXAM_MAIN = '''Exam[] exams = new Exam[names.length];
for (int i = 0; i < names.length; i++) {
    exams[i] = new Exam(names[i], scores[i]);
}
System.out.println("Pass mark: " + Exam.passScore);
int passed = 0;
for (int i = 0; i < exams.length; i++) {
    if (exams[i].passed()) {
        System.out.println(exams[i].student + ": " + exams[i].score + ", pass");
        passed++;
    } else {
        System.out.println(exams[i].student + ": " + exams[i].score + ", fail");
    }
}
System.out.println("Passed: " + passed);
Exam.passScore = newPass;
System.out.println("New pass mark: " + Exam.passScore);
passed = 0;
for (int i = 0; i < exams.length; i++) {
    if (exams[i].passed()) {
        passed++;
    }
}
System.out.println("Passed: " + passed);'''

# ───────── Sleep ─────────

SLEEP = '''class Sleep {
    static int hours(int bedtime, int wakeUp) {
        return (wakeUp - bedtime + 24) % 24;
    }
}'''

SLEEP_MAIN = '''for (int i = 0; i < bedtimes.length; i++) {
    System.out.println("Night " + (i + 1) + ": " + Sleep.hours(bedtimes[i], wakeUps[i]) + " h");
}'''

# ───────── Donations ─────────

DONATION = '''class Donation {
    static int total = 0;
    static int count = 0;
    String donor;
    int amount;

    Donation(String donor, int amount) {
        this.donor = donor;
        this.amount = amount;
        total += amount;
        count++;
    }
}'''

DONATION_MAIN = '''for (int i = 0; i < donors.length; i++) {
    Donation donation = new Donation(donors[i], amounts[i]);
    System.out.println(donation.donor + " gave " + donation.amount + " rub, total " + Donation.total + " rub");
}
System.out.println("Donations: " + Donation.count + ", total: " + Donation.total + " rub");'''

DONATION_OWN_TOTAL = '''int count = 0;
int total = 0;
for (int i = 0; i < donors.length; i++) {
    Donation donation = new Donation(donors[i], amounts[i]);
    System.out.println(donation.donor + " gave " + donation.amount + " rub, total " + donation.total + " rub");
    count = Donation.count;
    total = donation.total;
}
System.out.println("Donations: " + count + ", total: " + total + " rub");'''

DONATION_BEHAVIOUR = '''{ setStatic("Donation", "total", 0); setStatic("Donation", "count", 0);
  Constructor<?> k = c.getDeclaredConstructor(String.class, int.class); k.setAccessible(true);
  try { k.newInstance("A", 100); k.newInstance("B", 50); } catch (Exception e) { }
  Field ft = c.getDeclaredField("total"); ft.setAccessible(true);
  Field fc = c.getDeclaredField("count"); fc.setAccessible(true);
  need(Objects.equals(ft.get(null), 150) && Objects.equals(fc.get(null), 2),
       "Конструктор Donation должен прибавлять сумму к общему полю total и увеличивать общий счётчик count на 1");
  setStatic("Donation", "total", 0); setStatic("Donation", "count", 0); }
'''

# ───────── Dollar prices ─────────

PRICE = '''class Price {
    static int rate = 90;
    String item;
    int dollars;

    Price(String item, int dollars) {
        this.item = item;
        this.dollars = dollars;
    }

    int rubles() {
        return dollars * rate;
    }

    static void setRate(int newRate) {
        if (newRate > 0) {
            rate = newRate;
        }
    }
}'''

PRICE_MAIN = '''Price[] prices = new Price[items.length];
for (int i = 0; i < items.length; i++) {
    prices[i] = new Price(items[i], dollars[i]);
}
for (int round = 0; round < 2; round++) {
    if (round == 1) {
        Price.setRate(newRate);
    }
    System.out.println("Rate: " + Price.rate);
    int total = 0;
    for (int i = 0; i < prices.length; i++) {
        System.out.println(prices[i].item + ": " + prices[i].dollars + " $ = " + prices[i].rubles() + " rub");
        total += prices[i].rubles();
    }
    System.out.println("Total: " + total + " rub");
}'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-static-fahrenheit", title="Градусы по Фаренгейту",
        given=[("int[]", "celsius")],
        variants=[{"celsius": "{20, 25, -10}"}, {"celsius": "{0, 100}"}, {"celsius": "{35, -40, 15, 5}"}],
        hidden=[{"celsius": "{-5}"}, {"celsius": "{30, 10, -20, 40, 45}"}, {"celsius": "{50, 60}"}, {"celsius": "{-15, 0}"}],
        intro="Ты переписываешься с другом из США, а там температуру измеряют в градусах Фаренгейта. Переводить приходится "
              "часто, но никакой «объект-термометр» для этого не нужен — это просто формула. Такие методы в Java делают "
              "статическими: они принадлежат классу, и их вызывают без `new`. Температуры по Цельсию записаны в массиве `celsius`.",
        steps=["Ниже класса `Solution` создай класс `Temperature` (без `public`) со статическим методом "
               "`static int toFahrenheit(int celsius)`. Он возвращает `celsius * 9 / 5 + 32` — все температуры в задаче "
               "делятся на 5, поэтому результат получается целым.",
               "В `main` не создавай объект `Temperature`: вызывай метод через имя класса — `Temperature.toFahrenheit(...)`.",
               "Для каждой температуры из массива `celsius` выведи строку вида `20 C = 68 F`."],
        hint="Методы класса `Solution` ты уже вызывал без всякого объекта — потому что они `static`. С методом другого "
             "класса всё так же, только перед именем метода пишут имя класса и точку.",
        solution=TEMPERATURE_MAIN,
        classes=TEMPERATURE,
        wrong=[("метод без static — пришлось создавать объект, хотя он не нужен",
                TEMPERATURE_MAIN.replace("Temperature.toFahrenheit(celsius[i])", "new Temperature().toFahrenheit(celsius[i])"),
                TEMPERATURE.replace("    static int toFahrenheit", "    int toFahrenheit")),
               ("скобки вокруг 9 / 5 — целочисленное деление даёт 1, и формула ломается",
                TEMPERATURE_MAIN, TEMPERATURE.replace("celsius * 9 / 5 + 32", "celsius * (9 / 5) + 32"))],
        constructs=["class"],
        checks=find_class("Temperature")
               + need_method("Temperature", "int", "toFahrenheit", ["int celsius"], "он переводит градусы Цельсия в градусы Фаренгейта", static=True),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-static-visitor-counter", title="Браслеты на выставке",
        given=[("String[]", "names")],
        variants=[{"names": '{"Anya", "Boris", "Vika"}'},
                  {"names": '{"Gleb", "Dina"}'},
                  {"names": '{"Egor", "Zhanna", "Zakhar", "Ira", "Kira"}'}],
        hidden=[{"names": '{"Lena"}'}, {"names": "{}"}, {"names": '{"Mark", "Nina", "Oleg", "Polya"}'}],
        intro="На входе на выставку каждому гостю выдают браслет с номером: первый гость получает №1, второй — №2 и так далее. "
              "Номер берётся из общего счётчика, который один на всех гостей, — такое поле делают статическим. Имена гостей "
              "в порядке прихода записаны в массиве `names`.",
        steps=["Ниже класса `Solution` создай класс `Visitor` (без `public`) с обычными полями `int number` и `String name` "
               "и статическим полем `static int count = 0` — общим счётчиком гостей.",
               "Добавь конструктор `Visitor(String name)`: он увеличивает `count` на 1, записывает новое значение счётчика "
               "в поле `number` этого гостя и сохраняет имя.",
               "В `main` для каждого имени из `names` создай `new Visitor(...)` и выведи строку вида `Visitor #1: Anya` — "
               "с полями этого объекта.",
               "Последней строкой выведи строку вида `Total visitors: 3` со значением счётчика, прочитанным через имя "
               "класса: `Visitor.count`."],
        hint="Обычное поле у каждого объекта своё, а статическое — одно на весь класс. Поэтому `count` не начинается "
             "заново с каждым новым гостем, а продолжает расти, и следующий гость получает следующий номер.",
        solution=VISITOR_MAIN,
        classes=VISITOR,
        wrong=[("счётчик count — обычное поле: у каждого гостя свой счётчик, и все получают №1",
                VISITOR_OWN_COUNTER, VISITOR.replace("    static int count = 0;", "    int count = 0;")),
               ("номер берётся до увеличения счётчика — нумерация начинается с 0",
                VISITOR_MAIN, VISITOR.replace("        count++;\n        this.number = count;", "        this.number = count;\n        count++;"))],
        constructs=["class"],
        checks=find_class("Visitor")
               + need_field("Visitor", "count", "int", "один общий счётчик для всех гостей", static=True)
               + need_field("Visitor", "number", "int", "номер браслета этого гостя")
               + need_field("Visitor", "name", "String", "имя гостя")
               + need_constructor("Visitor", ["String name"], "он выдаёт гостю следующий номер")
               + VISITOR_BEHAVIOUR,
        reset='setStatic("Visitor", "count", 0);',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-static-pass-score", title="Проходной балл",
        given=[("String[]", "names"), ("int[]", "scores"), ("int", "newPass")],
        variants=[{"names": '{"Anya", "Boris", "Vika"}', "scores": "{72, 55, 60}", "newPass": "70"},
                  {"names": '{"Gleb", "Dina", "Egor", "Zhenya"}', "scores": "{90, 64, 59, 75}", "newPass": "50"},
                  {"names": '{"Zoya", "Ilya"}', "scores": "{80, 65}", "newPass": "65"}],
        hidden=[{"names": '{"Kira"}', "scores": "{59}", "newPass": "59"},
                {"names": '{"Lev", "Mia", "Noy"}', "scores": "{100, 61, 70}", "newPass": "100"},
                {"names": '{"Osya", "Petr", "Raya", "Senya", "Toma"}', "scores": "{30, 60, 45, 61, 99}", "newPass": "45"},
                {"names": '{"Una", "Fedor"}', "scores": "{0, 100}", "newPass": "60"}],
        intro="Учитель проверил контрольную: зачёт ставят тем, кто набрал не меньше проходного балла. Проходной балл один "
              "для всех учеников — сначала он 60, но потом комиссия меняет его на `newPass`. Имена учеников записаны "
              "в массиве `names`, их баллы — в массиве `scores` под теми же номерами.",
        steps=["Ниже класса `Solution` создай класс `Exam` (без `public`) со статическим полем `static int passScore = 60`, "
               "обычными полями `String student` и `int score` и конструктором `Exam(String student, int score)`.",
               "Добавь метод `boolean passed()`: он возвращает `true`, если `score` не меньше `passScore`.",
               "В `main` создай массив объектов `Exam` для всех учеников. Выведи строку вида `Pass mark: 60` (значение `Exam.passScore`), "
               "потом для каждого ученика строку вида `Anya: 72, pass` или `Boris: 55, fail`, а затем строку вида "
               "`Passed: 2` — сколько учеников получили зачёт.",
               "Поменяй порог один раз для всех: `Exam.passScore = newPass;`. Выведи строку вида `New pass mark: 70` и снова "
               "`Passed: …` — посчитай зачёты заново тем же методом `passed()` у тех же объектов, новых не создавай."],
        hint="Статическое поле хранится в классе, а не в каждом объекте, поэтому одна строка `Exam.passScore = newPass;` "
             "меняет порог сразу для всех: метод `passed()` у каждого объекта прочитает уже новое значение.",
        solution=EXAM_MAIN,
        classes=EXAM,
        wrong=[("порог — обычное поле, и новый порог получил только первый ученик",
                EXAM_MAIN.replace("Exam.passScore = newPass;", "exams[0].passScore = newPass;")
                         .replace('"Pass mark: " + Exam.passScore', '"Pass mark: " + exams[0].passScore')
                         .replace('"New pass mark: " + Exam.passScore', '"New pass mark: " + exams[0].passScore'),
                EXAM.replace("    static int passScore = 60;", "    int passScore = 60;")),
               ("строгое сравнение: ровно проходной балл не даёт зачёта",
                EXAM_MAIN, EXAM.replace("score >= passScore", "score > passScore"))],
        constructs=["class"],
        checks=find_class("Exam")
               + need_field("Exam", "passScore", "int", "проходной балл один для всех экзаменов", static=True)
               + need_field("Exam", "student", "String", "имя ученика")
               + need_field("Exam", "score", "int", "балл ученика")
               + need_constructor("Exam", ["String student", "int score"], "он заполняет поля, когда создаётся объект")
               + need_method("Exam", "boolean", "passed", [], "он сравнивает балл ученика с общим проходным баллом"),
        reset='setStatic("Exam", "passScore", 60);',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-static-sleep-hours", title="Сколько я спал",
        given=[("int[]", "bedtimes"), ("int[]", "wakeUps")],
        variants=[{"bedtimes": "{23, 22, 1}", "wakeUps": "{7, 6, 9}"},
                  {"bedtimes": "{0, 21}", "wakeUps": "{8, 5}"},
                  {"bedtimes": "{22, 23, 23, 2}", "wakeUps": "{7, 8, 6, 10}"}],
        hidden=[{"bedtimes": "{20}", "wakeUps": "{4}"},
                {"bedtimes": "{3, 23, 0}", "wakeUps": "{11, 23, 0}"},
                {"bedtimes": "{12, 21}", "wakeUps": "{14, 9}"},
                {"bedtimes": "{22, 22, 22, 22, 22}", "wakeUps": "{6, 7, 8, 5, 9}"}],
        intro="Ты записываешь, во сколько лёг спать и во сколько проснулся, — целыми часами от 0 до 23. Посчитать, сколько "
              "часов длился сон, — просто формула, для неё не нужен никакой объект. Такой метод делают статическим и вызывают "
              "через имя класса. Время отхода ко сну по ночам записано в массиве `bedtimes`, время подъёма — в `wakeUps`.",
        steps=["Ниже класса `Solution` создай класс `Sleep` (без `public`) со статическим методом "
               "`static int hours(int bedtime, int wakeUp)`. Он возвращает `(wakeUp - bedtime + 24) % 24` — "
               "так сон через полночь (с 23 до 7) тоже считается правильно: 8 часов.",
               "В `main` не создавай объект `Sleep`: вызывай метод через имя класса — `Sleep.hours(...)`.",
               "Для каждой ночи выведи строку вида `Night 1: 8 h` — номер ночи (с единицы) и сколько часов длился сон."],
        hint="Если лёг в 23, а встал в 7, то `7 - 23` даёт -16. Прибавив 24, получаешь 8, а остаток от деления на 24 "
             "нужен для ночей, когда лёг уже после полуночи: `9 - 1 + 24 = 32`, а спал ты 8 часов.",
        solution=SLEEP_MAIN,
        classes=SLEEP,
        wrong=[("метод без static — пришлось создавать объект, хотя он не нужен",
                SLEEP_MAIN.replace("Sleep.hours(", "new Sleep().hours("),
                SLEEP.replace("    static int hours", "    int hours")),
               ("забыл прибавить 24 — сон через полночь выходит отрицательным",
                SLEEP_MAIN, SLEEP.replace("(wakeUp - bedtime + 24) % 24", "(wakeUp - bedtime) % 24"))],
        constructs=["class"],
        checks=find_class("Sleep")
               + need_method("Sleep", "int", "hours", ["int bedtime", "int wakeUp"], "он считает, сколько часов длился сон", static=True),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-static-charity-total", title="Сбор на приют",
        given=[("String[]", "donors"), ("int[]", "amounts")],
        variants=[{"donors": '{"Anya", "Boris", "Vika"}', "amounts": "{100, 250, 50}"},
                  {"donors": '{"Gleb", "Dina"}', "amounts": "{500, 300}"},
                  {"donors": '{"Egor", "Zhanna", "Zakhar", "Ira"}', "amounts": "{70, 30, 200, 100}"}],
        hidden=[{"donors": '{"Lena"}', "amounts": "{1000}"},
                {"donors": "{}", "amounts": "{}"},
                {"donors": '{"Mark", "Nina", "Oleg", "Polya", "Roma"}', "amounts": "{10, 20, 30, 40, 50}"}],
        intro="Школа собирает деньги на корм для приюта. Каждое пожертвование — отдельный объект с именем и суммой, "
              "а общая собранная сумма и число пожертвований — одни на всех, поэтому их хранят в статических полях. "
              "Имена жертвователей записаны в массиве `donors`, суммы — в `amounts` под теми же номерами.",
        steps=["Ниже класса `Solution` создай класс `Donation` (без `public`) с обычными полями `String donor` и `int amount` "
               "и статическими полями `static int total = 0` и `static int count = 0`.",
               "Добавь конструктор `Donation(String donor, int amount)`: он сохраняет имя и сумму, прибавляет сумму к `total` "
               "и увеличивает `count` на 1.",
               "В `main` для каждого жертвователя создай `new Donation(...)` и выведи строку вида "
               "`Anya gave 100 rub, total 100 rub` — сумму этого объекта и общую сумму `Donation.total` после него.",
               "Последней строкой выведи строку вида `Donations: 3, total: 400 rub` — значения статических полей через имя класса."],
        hint="Статическое поле одно на весь класс: каждый новый объект прибавляет к тому же самому `total`, поэтому общая "
             "сумма растёт от пожертвования к пожертвованию.",
        solution=DONATION_MAIN,
        classes=DONATION,
        wrong=[("total — обычное поле: у каждого пожертвования свой «итог», равный его сумме",
                DONATION_OWN_TOTAL, DONATION.replace("    static int total = 0;", "    int total = 0;")),
               ("в конструкторе `total = amount;` — итог перезаписывается, а не накапливается",
                DONATION_MAIN, DONATION.replace("        total += amount;", "        total = amount;"))],
        constructs=["class"],
        checks=find_class("Donation")
               + need_field("Donation", "total", "int", "общая сумма всех пожертвований", static=True)
               + need_field("Donation", "count", "int", "число всех пожертвований", static=True)
               + need_field("Donation", "donor", "String", "имя жертвователя")
               + need_field("Donation", "amount", "int", "сумма этого пожертвования")
               + need_constructor("Donation", ["String donor", "int amount"], "он сохраняет пожертвование и пополняет общий итог")
               + DONATION_BEHAVIOUR,
        reset='setStatic("Donation", "total", 0);\nsetStatic("Donation", "count", 0);',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-static-dollar-rate", title="Цены в долларах",
        given=[("String[]", "items"), ("int[]", "dollars"), ("int", "newRate")],
        variants=[{"items": '{"Book", "Game"}', "dollars": "{20, 50}", "newRate": "95"},
                  {"items": '{"Lamp", "Mouse", "Cable"}', "dollars": "{15, 10, 3}", "newRate": "0"},
                  {"items": '{"Watch"}', "dollars": "{120}", "newRate": "88"}],
        hidden=[{"items": '{"Pen", "Bag"}', "dollars": "{2, 40}", "newRate": "-5"},
                {"items": '{"Phone", "Case", "Glass", "Charger"}', "dollars": "{300, 12, 8, 25}", "newRate": "100"},
                {"items": '{"Kite"}', "dollars": "{9}", "newRate": "1"},
                {"items": "{}", "dollars": "{}", "newRate": "92"}],
        intro="Ты присматриваешь товары в иностранном магазине, где цены в долларах. Курс доллара один для всех товаров — "
              "сначала 90 руб., но потом он меняется на `newRate`. Если новый курс не больше 0, это ошибка, и курс остаётся "
              "прежним. Названия товаров записаны в массиве `items`, цены в долларах — в `dollars`.",
        steps=["Ниже класса `Solution` создай класс `Price` (без `public`) со статическим полем `static int rate = 90`, "
               "обычными полями `String item` и `int dollars` и конструктором `Price(String item, int dollars)`.",
               "Добавь обычный метод `int rubles()` — цена в рублях по текущему курсу, и статический метод "
               "`static void setRate(int newRate)`, который меняет курс, только если `newRate` больше 0.",
               "В `main` создай массив объектов `Price` для всех товаров. Выведи строку вида `Rate: 90`, для каждого товара "
               "строку вида `Book: 20 $ = 1800 rub` и строку вида `Total: 6300 rub` — сумму всех цен в рублях.",
               "Вызови `Price.setRate(newRate)` и выведи те же строки ещё раз — для тех же объектов, новых не создавай."],
        hint="Статический метод работает со статическими полями класса и вызывается через имя класса. Поменяв `rate` "
             "один раз, ты меняешь его для всех объектов сразу: `rubles()` у каждого прочитает новый курс.",
        solution=PRICE_MAIN,
        classes=PRICE,
        wrong=[("setRate не проверяет курс — курс 0 или отрицательный тоже записывается",
                PRICE_MAIN, PRICE.replace("        if (newRate > 0) {\n            rate = newRate;\n        }", "        rate = newRate;")),
               ("курс — обычное поле, и новый курс получил только первый товар",
                PRICE_MAIN.replace("        Price.setRate(newRate);", "        if (newRate > 0 && prices.length > 0) {\n            prices[0].rate = newRate;\n        }")
                          .replace('"Rate: " + Price.rate', '"Rate: " + (prices.length > 0 ? prices[0].rate : 90)'),
                PRICE.replace("    static int rate = 90;", "    int rate = 90;")
                     .replace("    static void setRate(int newRate) {\n        if (newRate > 0) {\n            rate = newRate;\n        }\n    }\n", ""))],
        constructs=["class", "for"],
        checks=find_class("Price")
               + need_field("Price", "rate", "int", "курс доллара один для всех товаров", static=True)
               + need_field("Price", "item", "String", "название товара")
               + need_field("Price", "dollars", "int", "цена в долларах")
               + need_constructor("Price", ["String item", "int dollars"], "он заполняет поля, когда создаётся объект")
               + need_method("Price", "int", "rubles", [], "он считает цену в рублях по общему курсу")
               + need_method("Price", "void", "setRate", ["int newRate"], "он меняет курс для всех товаров сразу", static=True),
        reset='setStatic("Price", "rate", 90);',
    ),
]
