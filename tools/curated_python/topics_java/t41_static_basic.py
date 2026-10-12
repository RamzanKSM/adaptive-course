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
    System.out.println(celsius[i] + " по Цельсию = " + Temperature.toFahrenheit(celsius[i]) + " по Фаренгейту");
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
    System.out.println("Посетитель №" + visitor.number + ": " + visitor.name);
}
System.out.println("Всего посетителей: " + Visitor.count);'''

VISITOR_OWN_COUNTER = '''int total = 0;
for (int i = 0; i < names.length; i++) {
    Visitor visitor = new Visitor(names[i]);
    System.out.println("Посетитель №" + visitor.number + ": " + visitor.name);
    total = visitor.count;
}
System.out.println("Всего посетителей: " + total);'''

VISITOR_BEHAVIOUR = '''{ setStatic("Visitor", "count", 0);
  Constructor<?> k = c.getDeclaredConstructor(String.class); k.setAccessible(true);
  Object a = null, b = null; try { a = k.newInstance("А"); b = k.newInstance("Б"); } catch (Exception e) { }
  Field fc = c.getDeclaredField("count"); fc.setAccessible(true);
  Field fnum = c.getDeclaredField("number"); fnum.setAccessible(true);
  Field fname = c.getDeclaredField("name"); fname.setAccessible(true);
  need(b != null && Objects.equals(fc.get(null), 2) && Objects.equals(fnum.get(a), 1) && Objects.equals(fnum.get(b), 2) && Objects.equals(fname.get(b), "Б"),
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
System.out.println("Порог: " + Exam.passScore);
int passed = 0;
for (int i = 0; i < exams.length; i++) {
    if (exams[i].passed()) {
        System.out.println(exams[i].student + ": " + exams[i].score + ", зачёт");
        passed++;
    } else {
        System.out.println(exams[i].student + ": " + exams[i].score + ", незачёт");
    }
}
System.out.println("Сдали: " + passed);
Exam.passScore = newPass;
System.out.println("Новый порог: " + Exam.passScore);
passed = 0;
for (int i = 0; i < exams.length; i++) {
    if (exams[i].passed()) {
        passed++;
    }
}
System.out.println("Сдали: " + passed);'''

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
               "Для каждой температуры из массива `celsius` выведи строку вида `20 по Цельсию = 68 по Фаренгейту`."],
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
        variants=[{"names": '{"Аня", "Борис", "Вика"}'},
                  {"names": '{"Глеб", "Дина"}'},
                  {"names": '{"Егор", "Жанна", "Захар", "Ира", "Кира"}'}],
        hidden=[{"names": '{"Лена"}'}, {"names": "{}"}, {"names": '{"Марк", "Нина", "Олег", "Поля"}'}],
        intro="На входе на выставку каждому гостю выдают браслет с номером: первый гость получает №1, второй — №2 и так далее. "
              "Номер берётся из общего счётчика, который один на всех гостей, — такое поле делают статическим. Имена гостей "
              "в порядке прихода записаны в массиве `names`.",
        steps=["Ниже класса `Solution` создай класс `Visitor` (без `public`) с обычными полями `int number` и `String name` "
               "и статическим полем `static int count = 0` — общим счётчиком гостей.",
               "Добавь конструктор `Visitor(String name)`: он увеличивает `count` на 1, записывает новое значение счётчика "
               "в поле `number` этого гостя и сохраняет имя.",
               "В `main` для каждого имени из `names` создай `new Visitor(...)` и выведи строку вида `Посетитель №1: Аня` — "
               "с полями этого объекта.",
               "Последней строкой выведи строку вида `Всего посетителей: 3` со значением счётчика, прочитанным через имя "
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
        variants=[{"names": '{"Аня", "Борис", "Вика"}', "scores": "{72, 55, 60}", "newPass": "70"},
                  {"names": '{"Глеб", "Дина", "Егор", "Женя"}', "scores": "{90, 64, 59, 75}", "newPass": "50"},
                  {"names": '{"Зоя", "Илья"}', "scores": "{80, 65}", "newPass": "65"}],
        hidden=[{"names": '{"Кира"}', "scores": "{59}", "newPass": "59"},
                {"names": '{"Лев", "Мия", "Ной"}', "scores": "{100, 61, 70}", "newPass": "100"},
                {"names": '{"Ося", "Пётр", "Рая", "Сеня", "Тома"}', "scores": "{30, 60, 45, 61, 99}", "newPass": "45"},
                {"names": '{"Уна", "Фёдор"}', "scores": "{0, 100}", "newPass": "60"}],
        intro="Учитель проверил контрольную: зачёт ставят тем, кто набрал не меньше проходного балла. Проходной балл один "
              "для всех учеников — сначала он 60, но потом комиссия меняет его на `newPass`. Имена учеников записаны "
              "в массиве `names`, их баллы — в массиве `scores` под теми же номерами.",
        steps=["Ниже класса `Solution` создай класс `Exam` (без `public`) со статическим полем `static int passScore = 60`, "
               "обычными полями `String student` и `int score` и конструктором `Exam(String student, int score)`.",
               "Добавь метод `boolean passed()`: он возвращает `true`, если `score` не меньше `passScore`.",
               "В `main` создай массив объектов `Exam` для всех учеников. Выведи строку вида `Порог: 60` (значение `Exam.passScore`), "
               "потом для каждого ученика строку вида `Аня: 72, зачёт` или `Борис: 55, незачёт`, а затем строку вида "
               "`Сдали: 2` — сколько учеников получили зачёт.",
               "Поменяй порог один раз для всех: `Exam.passScore = newPass;`. Выведи строку вида `Новый порог: 70` и снова "
               "`Сдали: …` — посчитай зачёты заново тем же методом `passed()` у тех же объектов, новых не создавай."],
        hint="Статическое поле хранится в классе, а не в каждом объекте, поэтому одна строка `Exam.passScore = newPass;` "
             "меняет порог сразу для всех: метод `passed()` у каждого объекта прочитает уже новое значение.",
        solution=EXAM_MAIN,
        classes=EXAM,
        wrong=[("порог — обычное поле, и новый порог получил только первый ученик",
                EXAM_MAIN.replace("Exam.passScore = newPass;", "exams[0].passScore = newPass;")
                         .replace('"Порог: " + Exam.passScore', '"Порог: " + exams[0].passScore')
                         .replace('"Новый порог: " + Exam.passScore', '"Новый порог: " + exams[0].passScore'),
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
]
