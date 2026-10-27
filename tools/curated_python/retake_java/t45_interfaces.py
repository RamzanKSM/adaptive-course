"""INTERFACE_BASIC — «Интерфейсы» (Java). Taught before: everything up to classes, objects, constructors, this,
private fields, getters/setters, static, inheritance, overriding, polymorphism through a parent-type array. Here:
`interface Name { int method(); }` — a set of methods without bodies; `class X implements Name` must write all of them
(as public); a variable or array of the interface type holds objects of any implementing classes; one class may
implement several interfaces. Not yet: super (next topic), default methods, collections. The student writes the
interfaces and classes after Solution."""
from java_tasks import JavaOutputTask

SKILL = "INTERFACE_BASIC"


def _listed(names: tuple[str, ...]) -> str:
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " и " + names[-1]


def exist(interfaces: tuple[str, ...], classes: tuple[str, ...]) -> str:
    what = (("интерфейс " if len(interfaces) == 1 else "интерфейсы ") + _listed(interfaces) + " и "
            + ("класс " if len(classes) == 1 else "классы ") + _listed(classes))
    condition = " && ".join(f'cls("{n}") != null' for n in interfaces + classes)
    return f'need({condition}, "Опиши {what} отдельно — ниже класса Solution, после его закрывающей скобки, и без слова public");\n'


def interface(name: str) -> str:
    return (f'need(cls("{name}").isInterface(), "Сделай {name} интерфейсом: напиши interface {name}, а не class {name} — '
            f'интерфейс только перечисляет методы, которые обязаны написать классы");\n')


def implements(cls_name: str, *interfaces: str) -> str:
    condition = " && ".join(f'cls("{i}").isAssignableFrom(cls("{cls_name}"))' for i in interfaces)
    listed = ", ".join(interfaces)
    what = "интерфейс" if len(interfaces) == 1 else "интерфейсы"
    return (f'need({condition}, "Класс {cls_name} должен реализовать {what} {_listed(interfaces)}: '
            f'напиши class {cls_name} implements {listed}");\n')


def declares(cls_name: str, method: str) -> str:
    return f'Arrays.stream(cls("{cls_name}").getDeclaredMethods()).anyMatch(m -> m.getName().equals("{method}"))'




LUGGAGE = """\
interface Item {
    int weight();
}

class Suitcase implements Item {
    private int kg;

    Suitcase(int kg) {
        this.kg = kg;
    }

    @Override
    public int weight() {
        return kg;
    }
}

class Backpack implements Item {
    private int books;

    Backpack(int books) {
        this.books = books;
    }

    @Override
    public int weight() {
        return 2 + books;
    }
}"""

LUGGAGE_MAIN = """\
Item suitcase = new Suitcase(kg);
Item backpack = new Backpack(books);
System.out.println("Suitcase: " + suitcase.weight() + " kg");
System.out.println("Backpack: " + backpack.weight() + " kg");
System.out.println("Total: " + (suitcase.weight() + backpack.weight()) + " kg");"""

LUGGAGE_AS_CLASS = (LUGGAGE.replace("interface Item {\n    int weight();\n}",
                                    "class Item {\n    public int weight() {\n        return 0;\n    }\n}")
                    .replace("implements Item", "extends Item"))

SENSORS = """\
interface Sensor {
    String name();

    boolean alarm(int value);
}

class Smoke implements Sensor {
    @Override
    public String name() {
        return "Smoke";
    }

    @Override
    public boolean alarm(int value) {
        return value > 50;
    }
}

class Temperature implements Sensor {
    @Override
    public String name() {
        return "Temperature";
    }

    @Override
    public boolean alarm(int value) {
        return value < 5 || value > 60;
    }
}

class Water implements Sensor {
    @Override
    public String name() {
        return "Water";
    }

    @Override
    public boolean alarm(int value) {
        return value > 0;
    }
}"""

SENSORS_MAIN = """\
Sensor[] sensors = {new Smoke(), new Temperature(), new Water()};
int alarms = 0;
for (int i = 0; i < sensors.length; i++) {
    if (sensors[i].alarm(readings[i])) {
        System.out.println(sensors[i].name() + ": " + readings[i] + ", ALARM");
        alarms++;
    } else {
        System.out.println(sensors[i].name() + ": " + readings[i] + ", ok");
    }
}
System.out.println("Alarms: " + alarms);"""

KITCHEN = """\
interface Boiler {
    String name();

    int boil(int liters);
}

interface Grill {
    String name();

    int grill(int pieces);
}

class Multicooker implements Boiler, Grill {
    @Override
    public String name() {
        return "Multicooker";
    }

    @Override
    public int boil(int liters) {
        return 5 + 2 * liters;
    }

    @Override
    public int grill(int pieces) {
        return 4 * pieces;
    }
}

class Kettle implements Boiler {
    @Override
    public String name() {
        return "Kettle";
    }

    @Override
    public int boil(int liters) {
        return 4 * liters;
    }
}

class Toaster implements Grill {
    @Override
    public String name() {
        return "Toaster";
    }

    @Override
    public int grill(int pieces) {
        return 5 + pieces;
    }
}"""

KITCHEN_MAIN = """\
Multicooker cooker = new Multicooker();
System.out.println("Multicooker: water " + cooker.boil(liters) + " min, grill " + cooker.grill(pieces) + " min");
Boiler[] boilers = {cooker, new Kettle()};
Grill[] grills = {cooker, new Toaster()};
Boiler bestBoiler = boilers[0];
for (Boiler boiler : boilers) {
    if (boiler.boil(liters) < bestBoiler.boil(liters)) {
        bestBoiler = boiler;
    }
}
Grill bestGrill = grills[0];
for (Grill grill : grills) {
    if (grill.grill(pieces) < bestGrill.grill(pieces)) {
        bestGrill = grill;
    }
}
System.out.println("Fastest for water: " + bestBoiler.name() + ", " + bestBoiler.boil(liters) + " min");
System.out.println("Fastest for grill: " + bestGrill.name() + ", " + bestGrill.grill(pieces) + " min");"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-intf-rt-flight-luggage", title="Багаж в самолёт",
        given=[("int", "kg"), ("int", "books")],
        variants=[{"kg": "18", "books": "3"}, {"kg": "23", "books": "0"}, {"kg": "12", "books": "5"}],
        hidden=[{"kg": "1", "books": "1"}, {"kg": "30", "books": "8"}, {"kg": "9", "books": "2"}],
        intro="Перед полётом нужно взвесить багаж: чемодан и рюкзак. Чемодан взвесили сразу — `kg` килограммов. "
              "Рюкзак сам весит 2 кг, а в нём `books` книг по 1 кг. Вес у них считается по-разному, но обе вещи — "
              "багаж, у которого можно узнать вес.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши интерфейс `Item` с одним методом `int weight();` — "
               "без тела, только заголовок и точка с запятой. Интерфейс и классы в этой задаче пиши без слова `public` перед ними.",
               "Опиши класс `Suitcase implements Item` с закрытым полем, конструктором `Suitcase(int kg)` и методом "
               "`public int weight()`, который возвращает вес чемодана.",
               "Опиши класс `Backpack implements Item` с конструктором `Backpack(int books)` и методом `public int weight()`: "
               "2 кг плюс по 1 кг за каждую книгу.",
               "В `main` создай `Item suitcase = new Suitcase(kg);` и `Item backpack = new Backpack(books);` и выведи три "
               "строки вида `Suitcase: 18 kg`, `Backpack: 5 kg` и `Total: 23 kg` — вес возьми из `weight()`."],
        hint="Интерфейс — это обещание: класс, который его реализует, обязан написать все его методы. Методы интерфейса "
             "открытые, поэтому в классах их пишут с `public`. Сумму в последней строке возьми в скобки, иначе числа "
             "склеятся как строки.",
        solution=LUGGAGE_MAIN, classes=LUGGAGE,
        wrong=[("склеивает веса как строки в итоговой сумме — вместо 23 получается 185",
                LUGGAGE_MAIN.replace('"Total: " + (suitcase.weight() + backpack.weight()) + " kg"',
                                     '"Total: " + suitcase.weight() + backpack.weight() + " kg"')),
               ("сделал Item обычным классом-родителем вместо интерфейса",
                LUGGAGE_MAIN, LUGGAGE_AS_CLASS)],
        constructs=["class"],
        checks=exist(("Item",), ("Suitcase", "Backpack"))
        + interface("Item")
        + implements("Suitcase", "Item") + implements("Backpack", "Item")
        + f'need({declares("Item", "weight")}, "Объяви в интерфейсе Item метод int weight(); — его обязаны написать все вещи");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-intf-rt-smart-home", title="Умный дом",
        given=[("int[]", "readings")],
        variants=[{"readings": "{10, 22, 0}"}, {"readings": "{70, 3, 1}"}, {"readings": "{50, 61, 0}"}],
        hidden=[{"readings": "{50, 30, 0}"}, {"readings": "{51, 5, 0}"}, {"readings": "{0, 60, 2}"}, {"readings": "{100, 4, 0}"}, {"readings": "{20, 25, 0}"}],
        intro="В умном доме стоят три датчика: дыма, температуры и протечки. Каждый решает по-своему, пора ли поднимать "
              "тревогу. Показания всех трёх по порядку записаны в массиве `readings`: дым, температура в градусах, "
              "вода на полу в миллиметрах.",
        steps=["Ниже класса `Solution` опиши интерфейс `Sensor` (без `public` перед ним) с двумя методами без тела: "
               "`String name();` и `boolean alarm(int value);`.",
               "Опиши три класса, которые реализуют `Sensor`, и напиши в каждом оба метода с `public`: `Smoke` — название "
               "`Smoke`, тревога, если значение больше 50; `Temperature` — `Temperature`, тревога, если меньше 5 или больше 60; "
               "`Water` — `Water`, тревога, если больше 0.",
               "В `main` создай массив `Sensor[] sensors = {{new Smoke(), new Temperature(), new Water()}};`. Одним циклом "
               "по индексам передай каждому датчику его показание из `readings` с тем же номером и выведи строку вида "
               "`Smoke: 10, ok` или `Smoke: 70, ALARM`.",
               "Последней строкой выведи строку вида `Alarms: 0` — сколько датчиков подняли тревогу."],
        hint="Массив имеет тип интерфейса, поэтому в нём лежат объекты трёх разных классов. Вызов "
             "`sensors[i].alarm(readings[i])` один и тот же, а правило тревоги каждый объект применяет своё.",
        solution=SENSORS_MAIN, classes=SENSORS,
        wrong=[("датчик температуры проверяет только жару и не замечает холод",
                SENSORS_MAIN, SENSORS.replace("return value < 5 || value > 60;", "return value > 60;")),
               ("нестрогое сравнение у датчика дыма: 50 уже считается тревогой",
                SENSORS_MAIN, SENSORS.replace("return value > 50;", "return value >= 50;"))],
        constructs=["class", "for", "if"],
        checks=exist(("Sensor",), ("Smoke", "Temperature", "Water"))
        + interface("Sensor")
        + implements("Smoke", "Sensor") + implements("Temperature", "Sensor") + implements("Water", "Sensor"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-intf-rt-multicooker", title="Мультиварка на кухне",
        given=[("int", "liters"), ("int", "pieces")],
        variants=[{"liters": "1", "pieces": "4"}, {"liters": "3", "pieces": "1"}, {"liters": "2", "pieces": "2"}],
        hidden=[{"liters": "5", "pieces": "3"}, {"liters": "1", "pieces": "1"},
                {"liters": "4", "pieces": "5"}, {"liters": "6", "pieces": "0"}],
        intro="На кухне есть мультиварка, чайник и тостер. Мультиварка умеет и кипятить воду, и жарить, чайник только "
              "кипятит, а тостер только жарит. Нужно вскипятить `liters` литров воды и поджарить `pieces` кусочков хлеба "
              "и узнать, какой прибор справится с каждым делом быстрее.",
        steps=["Ниже класса `Solution` опиши два интерфейса (без `public` перед ними): `Boiler` с методами `String name();` и "
               "`int boil(int liters);` и `Grill` с методами `String name();` и `int grill(int pieces);`. Оба метода "
               "возвращают минуты.",
               "Опиши класс `Multicooker implements Boiler, Grill`: название `Multicooker`, кипятит за `5 + 2 * liters` минут, "
               "жарит за `4 * pieces` минут. Метод `name()` нужен обоим интерфейсам, но в классе его пишут один раз.",
               "Опиши класс `Kettle implements Boiler` (название `Kettle`, кипятит за `4 * liters` минут) и класс "
               "`Toaster implements Grill` (название `Toaster`, жарит за `5 + pieces` минут). Методы пиши с `public`.",
               "В `main` создай `Multicooker cooker = new Multicooker();` и выведи строку вида "
               "`Multicooker: water 7 min, grill 16 min`.",
               "Создай массивы `Boiler[] boilers = {{cooker, new Kettle()}};` и `Grill[] grills = {{cooker, new Toaster()}};`. "
               "Циклами найди самый быстрый прибор в каждом массиве и выведи "
               "две строки вида `Fastest for water: Kettle, 4 min` и `Fastest for grill: Toaster, 9 min`."],
        hint="Одна и та же мультиварка лежит в обоих массивах: для `Boiler[]` она кипятильник, а для `Grill[]` — гриль. "
             "Родительский класс у класса может быть только один, а интерфейсов — сколько угодно.",
        solution=KITCHEN_MAIN, classes=KITCHEN,
        wrong=[("не положил мультиварку в массив грилей — жарит всегда тостер",
                KITCHEN_MAIN.replace("Grill[] grills = {cooker, new Toaster()};", "Grill[] grills = {new Toaster()};")),
               ("скопировал цикл кипячения и в цикле грилей передаёт liters вместо pieces",
                KITCHEN_MAIN.replace("    if (grill.grill(pieces) < bestGrill.grill(pieces)) {", "    if (grill.grill(liters) < bestGrill.grill(liters)) {"))],
        constructs=["class", "for"],
        checks=exist(("Boiler", "Grill"), ("Multicooker", "Kettle", "Toaster"))
        + interface("Boiler") + interface("Grill")
        + implements("Multicooker", "Boiler", "Grill") + implements("Kettle", "Boiler") + implements("Toaster", "Grill"),
    ),
]
