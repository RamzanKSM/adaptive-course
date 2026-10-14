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


GARDEN = """\
interface Shape {
    int area();
}

class Square implements Shape {
    private int side;

    Square(int side) {
        this.side = side;
    }

    @Override
    public int area() {
        return side * side;
    }
}

class Rectangle implements Shape {
    private int width;
    private int length;

    Rectangle(int width, int length) {
        this.width = width;
        this.length = length;
    }

    @Override
    public int area() {
        return width * length;
    }
}"""

GARDEN_MAIN = """\
Shape bed = new Square(side);
Shape lawn = new Rectangle(width, length);
System.out.println("Bed: " + bed.area() + " sq m");
System.out.println("Lawn: " + lawn.area() + " sq m");
System.out.println("Total: " + (bed.area() + lawn.area()) + " sq m");"""

# A beginner who knows inheritance makes Shape a class with a dummy method: the output is the same.
GARDEN_AS_CLASS = (GARDEN.replace("interface Shape {\n    int area();\n}",
                                  "class Shape {\n    public int area() {\n        return 0;\n    }\n}")
                   .replace("implements Shape", "extends Shape"))

TAXI = """\
interface Tariff {
    String name();

    int cost(int km);
}

class Economy implements Tariff {
    @Override
    public String name() {
        return "Economy";
    }

    @Override
    public int cost(int km) {
        return 100 + 20 * km;
    }
}

class Mini implements Tariff {
    @Override
    public String name() {
        return "Mini";
    }

    @Override
    public int cost(int km) {
        return 30 * km;
    }
}

class Flat implements Tariff {
    @Override
    public String name() {
        return "Flat";
    }

    @Override
    public int cost(int km) {
        return 450;
    }
}"""

TAXI_MAIN = """\
Tariff[] tariffs = {new Economy(), new Mini(), new Flat()};
Tariff best = tariffs[0];
for (Tariff tariff : tariffs) {
    System.out.println(tariff.name() + ": " + tariff.cost(km) + " rub");
    if (tariff.cost(km) < best.cost(km)) {
        best = tariff;
    }
}
System.out.println("Cheapest: " + best.name());"""

POND = """\
interface Swimmer {
    int swim(int minutes);
}

interface Flyer {
    int fly(int minutes);
}

class Duck implements Swimmer, Flyer {
    @Override
    public int swim(int minutes) {
        return 20 * minutes;
    }

    @Override
    public int fly(int minutes) {
        return 900 * minutes;
    }
}

class Fish implements Swimmer {
    @Override
    public int swim(int minutes) {
        return 60 * minutes;
    }
}

class Pigeon implements Flyer {
    @Override
    public int fly(int minutes) {
        return 1000 * minutes;
    }
}"""

POND_MAIN = """\
Duck duck = new Duck();
System.out.println("Duck: " + duck.swim(waterMinutes) + " m on water and " + duck.fly(airMinutes) + " m in the air");
Swimmer[] swimmers = {duck, new Fish()};
Flyer[] flyers = {duck, new Pigeon()};
int water = 0;
for (Swimmer swimmer : swimmers) {
    water += swimmer.swim(waterMinutes);
}
int air = 0;
for (Flyer flyer : flyers) {
    air += flyer.fly(airMinutes);
}
System.out.println("On water in total: " + water + " m");
System.out.println("In the air in total: " + air + " m");"""

PHONE = """\
interface Signal {
    String alert(String contact);
}

class Ring implements Signal {
    @Override
    public String alert(String contact) {
        return "RING RING: call from " + contact;
    }
}

class Vibrate implements Signal {
    @Override
    public String alert(String contact) {
        return "bzz-bzz: call from " + contact;
    }
}"""

PHONE_MAIN = """\
Signal signal;
if (silent) {
    signal = new Vibrate();
} else {
    signal = new Ring();
}
System.out.println(signal.alert(contact));"""

PHONE_AS_CLASS = (PHONE.replace("interface Signal {\n    String alert(String contact);\n}",
                                'class Signal {\n    public String alert(String contact) {\n        return "";\n    }\n}')
                  .replace("implements Signal", "extends Signal"))

COUPONS = """\
interface Coupon {
    String label();

    int apply(int price);
}

class Minus implements Coupon {
    private int amount;

    Minus(int amount) {
        this.amount = amount;
    }

    @Override
    public String label() {
        return "-" + amount + " rub";
    }

    @Override
    public int apply(int price) {
        if (price < amount) {
            return 0;
        }
        return price - amount;
    }
}

class Percent implements Coupon {
    private int percent;

    Percent(int percent) {
        this.percent = percent;
    }

    @Override
    public String label() {
        return "-" + percent + "%";
    }

    @Override
    public int apply(int price) {
        return price - price * percent / 100;
    }
}"""

COUPONS_MAIN = """\
System.out.println("Price: " + price + " rub");
Coupon[] coupons = {new Minus(amount), new Percent(percent)};
int total = price;
for (Coupon coupon : coupons) {
    total = coupon.apply(total);
    System.out.println(coupon.label() + ": " + total + " rub");
}"""

GADGETS = """\
interface Rechargeable {
    String name();

    int level();

    void charge(int minutes);
}

class Phone implements Rechargeable {
    private int level;

    Phone(int level) {
        this.level = level;
    }

    @Override
    public String name() {
        return "Phone";
    }

    @Override
    public int level() {
        return level;
    }

    @Override
    public void charge(int minutes) {
        level += 2 * minutes;
        if (level > 100) {
            level = 100;
        }
    }
}

class Watch implements Rechargeable {
    private int level;

    Watch(int level) {
        this.level = level;
    }

    @Override
    public String name() {
        return "Watch";
    }

    @Override
    public int level() {
        return level;
    }

    @Override
    public void charge(int minutes) {
        level += 5 * minutes;
        if (level > 100) {
            level = 100;
        }
    }
}

class Headphones implements Rechargeable {
    private int level;

    Headphones(int level) {
        this.level = level;
    }

    @Override
    public String name() {
        return "Headphones";
    }

    @Override
    public int level() {
        return level;
    }

    @Override
    public void charge(int minutes) {
        level += 10 * minutes;
        if (level > 100) {
            level = 100;
        }
    }
}"""

GADGETS_MAIN = """\
Rechargeable[] gadgets = {new Phone(phone), new Watch(watch), new Headphones(headphones)};
int full = 0;
for (Rechargeable gadget : gadgets) {
    gadget.charge(minutes);
    System.out.println(gadget.name() + ": " + gadget.level() + "%");
    if (gadget.level() == 100) {
        full++;
    }
}
System.out.println("Fully charged: " + full);"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-intf-garden-area", title="Грядка и газон",
        given=[("int", "side"), ("int", "width"), ("int", "length")],
        variants=[{"side": "4", "width": "3", "length": "8"},
                  {"side": "5", "width": "6", "length": "10"},
                  {"side": "3", "width": "2", "length": "7"}],
        hidden=[{"side": "1", "width": "1", "length": "1"},
                {"side": "10", "width": "4", "length": "12"},
                {"side": "2", "width": "9", "length": "9"},
                {"side": "7", "width": "5", "length": "3"}],
        intro="На даче есть квадратная грядка со стороной `side` метров и прямоугольный газон размером `width` на "
              "`length` метров. Чтобы купить удобрение, нужно знать площадь каждого участка и их общую площадь.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши интерфейс `Shape` с одним методом `int area();` — "
               "в интерфейсе у метода нет тела, только заголовок и точка с запятой. Интерфейс и классы в этой задаче "
               "пиши без слова `public` перед ними.",
               "Опиши класс `Square`, который реализует этот интерфейс: `class Square implements Shape`. Сохрани сторону "
               "квадрата в поле через конструктор `Square(int side)` и напиши метод `public int area()` — площадь квадрата.",
               "Так же опиши класс `Rectangle implements Shape` с конструктором `Rectangle(int width, int length)` и "
               "методом `public int area()` — площадь прямоугольника.",
               "В `main` создай `Shape bed = new Square(side);` и `Shape lawn = new Rectangle(width, length);` и выведи "
               "три строки вида `Bed: 16 sq m`, `Lawn: 24 sq m` и `Total: 40 sq m` — площади возьми из `area()`."],
        hint="Интерфейс — это обещание: каждый класс, который его реализует, обязан написать все его методы. Методы "
             "интерфейса всегда открытые, поэтому в классах их пишут с `public` — без него программа не скомпилируется.",
        solution=GARDEN_MAIN, classes=GARDEN,
        wrong=[("склеивает площади как строки в итоговой сумме — вместо 40 получается 1624",
                GARDEN_MAIN.replace('"Total: " + (bed.area() + lawn.area()) + " sq m"',
                                    '"Total: " + bed.area() + lawn.area() + " sq m"')),
               ("сделал Shape обычным классом-родителем вместо интерфейса",
                GARDEN_MAIN, GARDEN_AS_CLASS)],
        constructs=["class"],
        checks=exist(("Shape",), ("Square", "Rectangle"))
        + interface("Shape")
        + implements("Square", "Shape") + implements("Rectangle", "Shape")
        + f'need({declares("Shape", "area")}, "Объяви в интерфейсе Shape метод int area(); — его обязаны написать все фигуры");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-intf-taxi-tariff", title="Тарифы такси",
        given=[("int", "km")],
        variants=[{"km": "3"}, {"km": "12"}, {"km": "25"}],
        hidden=[{"km": "10"}, {"km": "17"}, {"km": "18"}, {"km": "1"}],
        intro="Приложение такси предлагает три тарифа, и каждый считает цену по-своему. Поездка будет длиной `km` "
              "километров. Покажи цены всех тарифов и подскажи, какой из них выгоднее.",
        steps=["Ниже класса `Solution` опиши интерфейс `Tariff` (без `public` перед ним) с двумя методами без тела: `String name();` и "
               "`int cost(int km);`.",
               "Опиши три класса, которые реализуют `Tariff` (например, `class Economy implements Tariff`), и напиши в "
               "каждом оба метода с `public`: `Economy` — название `Economy`, цена — 100 руб. за посадку плюс 20 руб. "
               "за километр; `Mini` — `Mini`, 30 руб. за километр; `Flat` — `Flat`, 450 руб. за любую поездку.",
               "В `main` создай массив `Tariff[] tariffs = {{new Economy(), new Mini(), new Flat()}};` и одним циклом "
               "выведи для каждого тарифа строку вида `Economy: 160 rub` — цену поездки на `km` километров.",
               "В том же цикле найди самый дешёвый тариф; если несколько тарифов стоят одинаково, выбери тот, что "
               "в массиве раньше. Последней строкой выведи строку вида `Cheapest: Mini` — с названием этого тарифа."],
        hint="Заведи переменную `Tariff best = tariffs[0];` и в цикле заменяй её, только если текущий тариф строго "
             "дешевле. Тип переменной — интерфейс: в неё можно положить объект любого класса, который его реализует.",
        solution=TAXI_MAIN, classes=TAXI,
        wrong=[("при равной цене выбирает более поздний тариф — сравнивает через <=",
                TAXI_MAIN.replace("if (tariff.cost(km) < best.cost(km))", "if (tariff.cost(km) <= best.cost(km))")),
               ("перепутал знак сравнения — ищет самый дорогой тариф",
                TAXI_MAIN.replace("if (tariff.cost(km) < best.cost(km))", "if (tariff.cost(km) > best.cost(km))"))],
        constructs=["class", "for", "if"],
        checks=exist(("Tariff",), ("Economy", "Mini", "Flat"))
        + interface("Tariff")
        + implements("Economy", "Tariff") + implements("Mini", "Tariff") + implements("Flat", "Tariff"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-intf-pond-duck", title="Утка, рыба и голубь",
        given=[("int", "waterMinutes"), ("int", "airMinutes")],
        variants=[{"waterMinutes": "5", "airMinutes": "3"},
                  {"waterMinutes": "2", "airMinutes": "4"},
                  {"waterMinutes": "10", "airMinutes": "1"}],
        hidden=[{"waterMinutes": "1", "airMinutes": "1"},
                {"waterMinutes": "7", "airMinutes": "7"},
                {"waterMinutes": "0", "airMinutes": "6"},
                {"waterMinutes": "4", "airMinutes": "0"}],
        intro="Школьники на экскурсии наблюдают за обитателями пруда: утка умеет и плавать, и летать, рыба только "
              "плавает, а голубь только летает. В поле `waterMinutes` записано, сколько минут животные плавают, "
              "а в `airMinutes` — сколько минут летают.",
        steps=["Ниже класса `Solution` опиши два интерфейса (без `public` перед ними): `Swimmer` с методом `int swim(int minutes);` и `Flyer` "
               "с методом `int fly(int minutes);`. Оба метода возвращают, сколько метров животное преодолеет за "
               "`minutes` минут.",
               "Опиши класс `Duck`, который реализует сразу оба интерфейса: `class Duck implements Swimmer, Flyer`. "
               "Утка проплывает 20 метров в минуту и пролетает 900 метров в минуту.",
               "Опиши класс `Fish implements Swimmer` — рыба проплывает 60 метров в минуту — и класс "
               "`Pigeon implements Flyer` — голубь пролетает 1000 метров в минуту. Методы интерфейсов пиши с `public`.",
               "В `main` создай одну утку `Duck duck = new Duck();` и выведи строку вида "
               "`Duck: 100 m on water and 2700 m in the air` — утка плавает `waterMinutes` минут, а летает `airMinutes` минут.",
               "Создай массивы `Swimmer[] swimmers = {{duck, new Fish()}};` и `Flyer[] flyers = {{duck, new Pigeon()}};`. "
               "Циклами посчитай, сколько метров все пловцы проплывут за `waterMinutes` минут и сколько все летуны "
               "пролетят за `airMinutes` минут, и выведи две строки вида `On water in total: 400 m` и "
               "`In the air in total: 5700 m`."],
        hint="Одна и та же утка лежит в обоих массивах: для массива `Swimmer[]` она пловец, а для `Flyer[]` — летун. "
             "Родительский класс у класса может быть только один, а интерфейсов он может реализовать сколько угодно.",
        solution=POND_MAIN, classes=POND,
        wrong=[("скопировал цикл пловцов и в цикле летунов тоже передаёт waterMinutes",
                POND_MAIN.replace("air += flyer.fly(airMinutes);", "air += flyer.fly(waterMinutes);")),
               ("не положил утку в массив летунов — её полёт не попал в общий итог",
                POND_MAIN.replace("Flyer[] flyers = {duck, new Pigeon()};", "Flyer[] flyers = {new Pigeon()};"))],
        constructs=["class", "for"],
        checks=exist(("Swimmer", "Flyer"), ("Duck", "Fish", "Pigeon"))
        + interface("Swimmer") + interface("Flyer")
        + implements("Duck", "Swimmer", "Flyer") + implements("Fish", "Swimmer") + implements("Pigeon", "Flyer"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-intf-phone-signal", title="Звонок или вибрация",
        given=[("String", "contact"), ("boolean", "silent")],
        variants=[{"contact": '"Anya"', "silent": "false"},
                  {"contact": '"Boris"', "silent": "true"},
                  {"contact": '"Grandma"', "silent": "false"}],
        hidden=[{"contact": '"Vika"', "silent": "true"},
                {"contact": '"Dad"', "silent": "false"},
                {"contact": '"Coach"', "silent": "true"}],
        intro="Телефон сообщает о входящем звонке по-разному: в обычном режиме он звонит, а в беззвучном — только "
              "вибрирует. Кто звонит, записано в поле `contact`, а включён ли беззвучный режим — в поле `silent`.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши интерфейс `Signal` с одним методом "
               "`String alert(String contact);` — без тела. Интерфейс и классы пиши без слова `public` перед ними.",
               "Опиши класс `Ring implements Signal`: его метод `public String alert(String contact)` возвращает строку "
               "вида `RING RING: call from Anya`.",
               "Опиши класс `Vibrate implements Signal`: его метод `alert` возвращает строку вида "
               "`bzz-bzz: call from Anya`.",
               "В `main` объяви переменную `Signal signal;`. Если `silent` равно `true`, положи в неё `new Vibrate()`, "
               "иначе — `new Ring()`. Затем выведи `signal.alert(contact)`."],
        hint="Переменная типа интерфейса может хранить объект любого класса, который его реализует. Вызов "
             "`signal.alert(...)` один и тот же, а что именно напечатается, решает объект, который в ней лежит.",
        solution=PHONE_MAIN, classes=PHONE,
        wrong=[("перепутал ветки — в беззвучном режиме телефон звонит",
                PHONE_MAIN.replace("new Vibrate();\n} else {\n    signal = new Ring();",
                                   "new Ring();\n} else {\n    signal = new Vibrate();")),
               ("сделал Signal обычным классом-родителем вместо интерфейса",
                PHONE_MAIN, PHONE_AS_CLASS)],
        constructs=["class", "if"],
        checks=exist(("Signal",), ("Ring", "Vibrate"))
        + interface("Signal")
        + implements("Ring", "Signal") + implements("Vibrate", "Signal")
        + f'need({declares("Signal", "alert")}, "Объяви в интерфейсе Signal метод String alert(String contact); — его обязаны написать оба класса");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-intf-shop-coupons", title="Два купона в магазине",
        given=[("int", "price"), ("int", "amount"), ("int", "percent")],
        variants=[{"price": "1500", "amount": "200", "percent": "10"},
                  {"price": "800", "amount": "300", "percent": "25"},
                  {"price": "2400", "amount": "500", "percent": "15"}],
        hidden=[{"price": "300", "amount": "500", "percent": "10"},
                {"price": "500", "amount": "500", "percent": "50"},
                {"price": "1000", "amount": "0", "percent": "0"},
                {"price": "999", "amount": "99", "percent": "50"}],
        intro="Покупка стоит `price` руб., а у покупателя два купона: один уменьшает цену на `amount` руб., другой — "
              "на `percent` процентов. Касса применяет купоны по очереди: второй купон считается от цены, которая "
              "получилась после первого.",
        steps=["Ниже класса `Solution` опиши интерфейс `Coupon` (без `public`) с двумя методами без тела: "
               "`String label();` и `int apply(int price);` — `apply` возвращает цену после купона.",
               "Опиши класс `Minus implements Coupon` с полем для суммы и конструктором `Minus(int amount)`. "
               "Его `label()` возвращает строку вида `-200 rub`, а `apply` вычитает сумму из цены; если цена меньше "
               "суммы, `apply` возвращает `0` — цена не бывает отрицательной.",
               "Опиши класс `Percent implements Coupon` с конструктором `Percent(int percent)`. Его `label()` "
               "возвращает строку вида `-10%`, а `apply` возвращает `price - price * percent / 100`. Методы "
               "интерфейса в классах пиши с `public`.",
               "В `main` выведи строку вида `Price: 1500 rub`, создай массив "
               "`Coupon[] coupons = {{new Minus(amount), new Percent(percent)}};` и одним циклом применяй купоны "
               "по очереди к текущей цене. После каждого купона выведи строку вида `-200 rub: 1300 rub` — его "
               "`label()` и цену после него."],
        hint="Заведи переменную `total = price` и в цикле записывай в неё результат `coupon.apply(total)`: тогда "
             "каждый следующий купон получит цену, уже уменьшенную предыдущим.",
        solution=COUPONS_MAIN, classes=COUPONS,
        wrong=[("применяет каждый купон к исходной цене, а не к цене после предыдущего купона",
                COUPONS_MAIN.replace("total = coupon.apply(total);", "total = coupon.apply(price);")),
               ("купон на сумму уводит цену в минус, если сумма больше цены",
                COUPONS_MAIN, COUPONS.replace("        if (price < amount) {\n            return 0;\n        }\n", ""))],
        constructs=["class", "for", "if"],
        checks=exist(("Coupon",), ("Minus", "Percent"))
        + interface("Coupon")
        + implements("Minus", "Coupon") + implements("Percent", "Coupon"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-intf-gadget-charge", title="Зарядная станция",
        given=[("int", "phone"), ("int", "watch"), ("int", "headphones"), ("int", "minutes")],
        variants=[{"phone": "40", "watch": "70", "headphones": "20", "minutes": "15"},
                  {"phone": "10", "watch": "5", "headphones": "50", "minutes": "10"},
                  {"phone": "85", "watch": "30", "headphones": "0", "minutes": "5"}],
        hidden=[{"phone": "50", "watch": "50", "headphones": "50", "minutes": "0"},
                {"phone": "98", "watch": "96", "headphones": "95", "minutes": "1"},
                {"phone": "100", "watch": "100", "headphones": "100", "minutes": "3"},
                {"phone": "0", "watch": "0", "headphones": "0", "minutes": "50"}],
        intro="На зарядной станции заряжаются телефон, часы и наушники. Их заряд в процентах сейчас записан в полях "
              "`phone`, `watch` и `headphones`, а заряжать их будут `minutes` минут. Каждое устройство заряжается "
              "со своей скоростью, но больше 100% заряд не поднимается.",
        steps=["Ниже класса `Solution` опиши интерфейс `Rechargeable` (без `public`) с тремя методами без тела: "
               "`String name();`, `int level();` и `void charge(int minutes);`.",
               "Опиши классы `Phone`, `Watch` и `Headphones`, которые реализуют `Rechargeable`. У каждого — закрытое "
               "поле с зарядом и конструктор с начальным зарядом, например `Phone(int level)`. `name()` возвращает "
               "`Phone`, `Watch` или `Headphones`, `level()` — текущий заряд.",
               "Метод `charge` увеличивает заряд: телефон — на 2% в минуту, часы — на 5%, наушники — на 10%. Если "
               "заряд получился больше 100, он становится ровно 100. Методы интерфейса пиши с `public`.",
               "В `main` создай массив `Rechargeable[] gadgets = {{new Phone(phone), new Watch(watch), "
               "new Headphones(headphones)}};`. Одним циклом заряди каждое устройство `minutes` минут и после "
               "зарядки выведи строку вида `Phone: 70%`.",
               "Последней строкой выведи строку вида `Fully charged: 2` — сколько устройств зарядилось до 100%."],
        hint="Каждый класс по-своему пишет `charge`, а цикл в `main` об этом не знает: он просто вызывает "
             "`gadget.charge(minutes)` у объекта типа `Rechargeable`. Ограничение в 100% проверяй сразу после "
             "увеличения заряда.",
        solution=GADGETS_MAIN, classes=GADGETS,
        wrong=[("не ограничивает заряд сотней — устройства заряжаются больше 100%",
                GADGETS_MAIN, GADGETS.replace("        if (level > 100) {\n            level = 100;\n        }\n", "")),
               ("выводит заряд до зарядки, а заряжает уже после печати",
                GADGETS_MAIN.replace("    gadget.charge(minutes);\n    System.out.println(gadget.name() + \": \" + gadget.level() + \"%\");\n",
                                     "    System.out.println(gadget.name() + \": \" + gadget.level() + \"%\");\n    gadget.charge(minutes);\n"))],
        constructs=["class", "for", "if"],
        checks=exist(("Rechargeable",), ("Phone", "Watch", "Headphones"))
        + interface("Rechargeable")
        + implements("Phone", "Rechargeable") + implements("Watch", "Rechargeable")
        + implements("Headphones", "Rechargeable")
        + f'need({declares("Rechargeable", "charge")}, "Объяви в интерфейсе Rechargeable метод void charge(int minutes); — его пишет каждый класс по-своему");\n',
    ),
]
