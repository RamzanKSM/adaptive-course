"""SUPER_BASIC — «Ключевое слово super» (Java). Taught before: everything up to classes, objects, constructors, this,
private fields, getters/setters, static, inheritance, overriding, polymorphism, interfaces. Here: the parent has only a
constructor with parameters and private fields, so the child's constructor must call super(...) first to let the parent
fill its part (and run its code, e.g. a shared counter); an overriding method extends the parent's result through
super.method(). Not yet: collections, exceptions. The student writes the classes after Solution."""
from java_tasks import JavaOutputTask

SKILL = "SUPER_BASIC"


def exist(*names: str) -> str:
    listed = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " и " + names[-1]
    what = "класс" if len(names) == 1 else "классы"
    condition = " && ".join(f'cls("{n}") != null' for n in names)
    return (f'need({condition}, "Опиши {what} {listed} отдельно — ниже класса Solution, после его закрывающей скобки, '
            f'и без слова public");\n')


def extends(child: str, parent: str) -> str:
    return (f'need(cls("{child}").getSuperclass() == cls("{parent}"), '
            f'"Сделай {child} наследником {parent}: напиши class {child} extends {parent}");\n')


def no_empty_constructor(parent: str, signature: str, call: str) -> str:
    return (f'need(Arrays.stream(cls("{parent}").getDeclaredConstructors()).noneMatch(k -> k.getParameterCount() == 0), '
            f'"Оставь в {parent} только конструктор {signature}, без пустого: наследник должен передать данные родителю через {call}");\n')


def private_fields(owner: str, *fields: str) -> str:
    variable = f"private{owner}"
    listed = " и ".join(fields)
    probe = " && ".join(f'Modifier.isPrivate(cls("{owner}").getDeclaredField("{f}").getModifiers())' for f in fields)
    return (f'boolean {variable};\n'
            f'try {{ {variable} = {probe}; }} catch (NoSuchFieldException e) {{ {variable} = false; }}\n'
            f'need({variable}, "Объяви в {owner} закрытые поля {listed} (private): их заполняет и читает только сам {owner}, '
            f'а наследник пользуется super");\n')


def declares(cls_name: str, method: str) -> str:
    return f'Arrays.stream(cls("{cls_name}").getDeclaredMethods()).anyMatch(m -> m.getName().equals("{method}"))'


COURIER = """\
class Employee {
    private String name;
    private int salary;

    Employee(String name, int salary) {
        this.name = name;
        this.salary = salary;
    }

    String info() {
        return name + ": " + salary + " руб.";
    }
}

class Courier extends Employee {
    private String transport;

    Courier(String name, int salary, String transport) {
        super(name, salary);
        this.transport = transport;
    }

    String getTransport() {
        return transport;
    }
}"""

COURIER_MAIN = """\
Courier courier = new Courier(name, salary, transport);
System.out.println(courier.info());
System.out.println("Транспорт: " + courier.getTransport());"""

# A beginner's way round super: an empty parent constructor, open fields, and the child fills them itself.
COURIER_NO_SUPER = (COURIER.replace("    private String name;\n    private int salary;\n\n    Employee(String name, int salary) {",
                                    "    String name;\n    int salary;\n\n    Employee() {\n    }\n\n    Employee(String name, int salary) {")
                    .replace("        super(name, salary);\n", "        this.name = name;\n        this.salary = salary;\n"))

CAPTAIN = """\
class Player {
    static int count = 0;
    private String name;

    Player(String name) {
        this.name = name;
        count++;
    }

    String getName() {
        return name;
    }
}

class Captain extends Player {
    private int number;

    Captain(String name, int number) {
        super(name);
        this.number = number;
    }

    int getNumber() {
        return number;
    }
}"""

CAPTAIN_MAIN = """\
for (String name : players) {
    new Player(name);
}
Captain cap = new Captain(captain, number);
System.out.println("Капитан: " + cap.getName() + ", номер " + cap.getNumber());
System.out.println("Всего игроков: " + Player.count);"""

GARAGE = """\
class Vehicle {
    private String name;
    private int wheels;

    Vehicle(String name, int wheels) {
        this.name = name;
        this.wheels = wheels;
    }

    String info() {
        return name + ", колёс: " + wheels;
    }
}

class Motorbike extends Vehicle {
    private int speed;

    Motorbike(String name, int speed) {
        super(name, 2);
        this.speed = speed;
    }

    @Override
    String info() {
        return super.info() + ", скорость до " + speed + " км/ч";
    }
}"""

GARAGE_MAIN = """\
Vehicle[] garage = {new Vehicle(car, 4), new Motorbike(bike, speed)};
for (Vehicle vehicle : garage) {
    System.out.println(vehicle.info());
}"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-super-courier", title="Курьер службы доставки",
        given=[("String", "name"), ("int", "salary"), ("String", "transport")],
        variants=[{"name": '"Олег"', "salary": "45000", "transport": '"велосипед"'},
                  {"name": '"Марина"', "salary": "52000", "transport": '"самокат"'},
                  {"name": '"Артём"', "salary": "61000", "transport": '"мотороллер"'}],
        hidden=[{"name": '"Лиза"', "salary": "38000", "transport": '"скутер"'},
                {"name": '"Рустам"', "salary": "70500", "transport": '"автомобиль"'},
                {"name": '"Ксюша"', "salary": "40000", "transport": '"электровелосипед"'}],
        intro="В службе доставки работают сотрудники: у каждого есть имя и зарплата. Курьер — тоже сотрудник, только "
              "у него есть ещё и транспорт. Имя и зарплату курьера пусть сохраняет класс-родитель, а курьер добавит "
              "только своё.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Employee` без слова `public`. Дай ему "
               "закрытые поля `private String name` и `private int salary`, конструктор `Employee(String name, int salary)`, "
               "который их заполняет, и метод `String info()`, который возвращает строку вида `Олег: 45000 руб.`",
               "Опиши класс `Courier` — наследник `Employee` — с полем `private String transport` и конструктором "
               "`Courier(String name, int salary, String transport)`. Первой строкой конструктора вызови "
               "`super(name, salary);` — родитель сам заполнит имя и зарплату, — а потом сохрани транспорт.",
               "Добавь в `Courier` геттер `String getTransport()`.",
               "В `main` создай `Courier courier = new Courier(name, salary, transport);` и выведи две строки: результат "
               "`courier.info()` и строку вида `Транспорт: велосипед`."],
        hint="Поля `name` и `salary` закрыты в `Employee`, поэтому `Courier` не может записать их сам. `super(name, salary)` "
             "вызывает конструктор родителя для того же самого объекта — и родитель заполняет свою часть.",
        solution=COURIER_MAIN, classes=COURIER,
        wrong=[("забыл сохранить транспорт в конструкторе курьера — печатается null",
                COURIER_MAIN, COURIER.replace("        this.transport = transport;\n", "")),
               ("добавил в Employee пустой конструктор и заполняет поля в Courier сам, без super",
                COURIER_MAIN, COURIER_NO_SUPER)],
        constructs=["class"],
        checks=exist("Employee", "Courier")
        + extends("Courier", "Employee")
        + no_empty_constructor("Employee", "Employee(String name, int salary)", "super(name, salary)")
        + private_fields("Employee", "name", "salary"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-super-team-captain", title="Капитан команды",
        given=[("String[]", "players"), ("String", "captain"), ("int", "number")],
        variants=[{"players": '{"Аня", "Вика", "Света"}', "captain": '"Лена"', "number": "10"},
                  {"players": '{"Петя", "Коля"}', "captain": '"Саша"', "number": "7"},
                  {"players": '{"Даша", "Маша", "Глаша", "Наташа", "Паша"}', "captain": '"Миша"', "number": "1"}],
        hidden=[{"players": "{}", "captain": '"Гоша"', "number": "9"},
                {"players": '{"Ира"}', "captain": '"Юля"', "number": "23"},
                {"players": '{"Лёва", "Тима", "Рома", "Женя"}', "captain": '"Федя"', "number": "4"}],
        intro="Школьная футбольная команда записывает игроков. Класс игрока сам считает, сколько игроков создано. "
              "Капитан — тоже игрок, только у него есть ещё номер на капитанской повязке. Важно, чтобы капитан тоже "
              "попал в общий счёт. Имена игроков записаны в массиве `players`, имя капитана — в `captain`, его номер — "
              "в `number`.",
        steps=["Ниже класса `Solution` опиши класс `Player` (без `public`) со статическим полем `static int count = 0;` "
               "и закрытым полем `private String name`. В конструкторе `Player(String name)` сохрани имя и увеличь "
               "`count` на 1. Добавь геттер `String getName()`.",
               "Опиши класс `Captain` — наследник `Player` — с полем `private int number`, геттером `int getNumber()` "
               "и конструктором `Captain(String name, int number)`. Первой строкой в нём вызови `super(name);`, а потом "
               "сохрани номер. Счётчик в `Captain` сам не трогай — это уже делает родитель.",
               "В `main` создай объект `Player` для каждого имени из массива `players`, а потом капитана: "
               "`Captain cap = new Captain(captain, number);`.",
               "Выведи строку вида `Капитан: Лена, номер 10`, а затем строку вида `Всего игроков: 4` — число возьми "
               "из `Player.count`."],
        hint="`super(name)` запускает конструктор `Player` и для капитана — вместе с увеличением счётчика. Поэтому капитан "
             "попадает в общий счёт сам. Если увеличить счётчик ещё и в `Captain`, капитана посчитают дважды.",
        solution=CAPTAIN_MAIN, classes=CAPTAIN,
        wrong=[("вызывает super(name) и ещё раз сам увеличивает счётчик — капитан посчитан дважды",
                CAPTAIN_MAIN, CAPTAIN.replace("        super(name);\n", "        super(name);\n        count++;\n")),
               ("добавил в Player пустой конструктор и не вызвал super(name) — капитан без имени и не попал в счётчик",
                CAPTAIN_MAIN, CAPTAIN.replace("    Player(String name) {", "    Player() {\n    }\n\n    Player(String name) {")
                                     .replace("        super(name);\n", ""))],
        constructs=["class", "for"],
        checks=exist("Player", "Captain")
        + extends("Captain", "Player")
        + no_empty_constructor("Player", "Player(String name)", "super(name)"),
        reset='setStatic("Player", "count", 0);',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-super-motorbike", title="Мотоцикл в гараже",
        given=[("String", "car"), ("String", "bike"), ("int", "speed")],
        variants=[{"car": '"Лада"', "bike": '"Урал"', "speed": "180"},
                  {"car": '"Нива"', "bike": '"Ява"', "speed": "120"},
                  {"car": '"Волга"', "bike": '"Минск"', "speed": "95"}],
        hidden=[{"car": '"Москвич"', "bike": '"Днепр"', "speed": "150"},
                {"car": '"Газель"', "bike": '"Сова"', "speed": "60"},
                {"car": '"Жигули"', "bike": '"Восход"', "speed": "110"}],
        intro="Программа описывает транспорт в гараже: машину `car` и мотоцикл `bike`. У каждого транспорта есть название "
              "и число колёс. Мотоцикл — тоже транспорт, но у него всегда 2 колеса, а в описании нужна ещё и максимальная "
              "скорость `speed`. Описание мотоцикла должно продолжать описание родителя, а не повторять его код.",
        steps=["Ниже класса `Solution` опиши класс `Vehicle` (без `public`) с закрытыми полями `private String name` и "
               "`private int wheels`, конструктором `Vehicle(String name, int wheels)` и методом `String info()`, который "
               "возвращает строку вида `Лада, колёс: 4`.",
               "Опиши класс `Motorbike` — наследник `Vehicle` — с полем `private int speed` и конструктором "
               "`Motorbike(String name, int speed)`: первой строкой вызови `super(name, 2);`, а потом сохрани скорость.",
               "Переопредели в `Motorbike` метод `String info()` (с `@Override`): пусть он берёт строку родителя через "
               "`super.info()` и дописывает к ней `, скорость до 180 км/ч` — со скоростью из поля `speed`.",
               "В `main` создай массив `Vehicle[] garage = {{new Vehicle(car, 4), new Motorbike(bike, speed)}};` и одним "
               "циклом выведи `info()` каждого транспорта."],
        hint="`super(...)` вызывает конструктор родителя, а `super.info()` — версию метода из родителя, даже если в "
             "наследнике он переопределён. Без `super.` вызов `info()` внутри `info()` вызывал бы сам себя бесконечно.",
        solution=GARAGE_MAIN, classes=GARAGE,
        wrong=[("в info мотоцикла не вызывает super.info() — пропадают название и колёса",
                GARAGE_MAIN, GARAGE.replace('return super.info() + ", скорость до " + speed + " км/ч";',
                                            'return "скорость до " + speed + " км/ч";')),
               ("передаёт родителю 4 колеса — скопировал вызов из машины",
                GARAGE_MAIN, GARAGE.replace("super(name, 2);", "super(name, 4);"))],
        constructs=["class", "for"],
        checks=exist("Vehicle", "Motorbike")
        + extends("Motorbike", "Vehicle")
        + no_empty_constructor("Vehicle", "Vehicle(String name, int wheels)", "super(name, 2)")
        + private_fields("Vehicle", "name", "wheels")
        + f'need({declares("Motorbike", "info")}, "Переопредели в Motorbike метод String info() с пометкой @Override и допиши в нём скорость к super.info()");\n',
    ),
]
