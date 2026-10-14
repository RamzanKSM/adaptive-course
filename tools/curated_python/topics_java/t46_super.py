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
        return name + ": " + salary + " rub";
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
System.out.println("Transport: " + courier.getTransport());"""

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
System.out.println("Captain: " + cap.getName() + ", number " + cap.getNumber());
System.out.println("Total players: " + Player.count);"""

GARAGE = """\
class Vehicle {
    private String name;
    private int wheels;

    Vehicle(String name, int wheels) {
        this.name = name;
        this.wheels = wheels;
    }

    String info() {
        return name + ", wheels: " + wheels;
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
        return super.info() + ", top speed " + speed + " km/h";
    }
}"""

GARAGE_MAIN = """\
Vehicle[] garage = {new Vehicle(car, 4), new Motorbike(bike, speed)};
for (Vehicle vehicle : garage) {
    System.out.println(vehicle.info());
}"""

TICKET = """\
class Ticket {
    private String route;
    private int price;

    Ticket(String route, int price) {
        this.route = route;
        this.price = price;
    }

    String info() {
        return route + ": " + price + " rub";
    }
}

class StudentTicket extends Ticket {
    StudentTicket(String route, int price) {
        super(route, price / 2);
    }
}"""

TICKET_MAIN = """\
Ticket adult = new Ticket(route, price);
StudentTicket student = new StudentTicket(route, price);
System.out.println("Adult: " + adult.info());
System.out.println("Student: " + student.info());"""

CARD = """\
class Card {
    private int points;

    Card(int points) {
        this.points = points;
    }

    void buy(int sum) {
        points += sum / 100;
    }

    int getPoints() {
        return points;
    }
}

class GoldCard extends Card {
    GoldCard(int points) {
        super(points + 500);
    }

    @Override
    void buy(int sum) {
        super.buy(sum * 2);
    }
}"""

CARD_MAIN = """\
Card card = new Card(start);
GoldCard gold = new GoldCard(start);
for (int sum : purchases) {
    card.buy(sum);
    gold.buy(sum);
}
System.out.println("Regular card: " + card.getPoints() + " points");
System.out.println("Gold card: " + gold.getPoints() + " points");"""

COFFEE = """\
class Drink {
    private String name;
    private int price;

    Drink(String name, int price) {
        this.name = name;
        this.price = price;
    }

    int getPrice() {
        return price;
    }

    String info() {
        return name;
    }
}

class Coffee extends Drink {
    private int shots;

    Coffee(String name, int shots) {
        super(name, 100);
        this.shots = shots;
    }

    @Override
    int getPrice() {
        return super.getPrice() + 40 * (shots - 1);
    }

    @Override
    String info() {
        return super.info() + ", shots: " + shots;
    }
}

class Latte extends Coffee {
    private String syrup;

    Latte(int shots, String syrup) {
        super("latte", shots);
        this.syrup = syrup;
    }

    @Override
    int getPrice() {
        return super.getPrice() + 60;
    }

    @Override
    String info() {
        return super.info() + ", syrup: " + syrup;
    }
}"""

COFFEE_MAIN = """\
Drink[] order = {new Drink("tea", 80), new Coffee("espresso", shots), new Latte(shots, syrup)};
int total = 0;
for (Drink drink : order) {
    System.out.println(drink.info() + " - " + drink.getPrice() + " rub");
    total += drink.getPrice();
}
System.out.println("Total: " + total + " rub");"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-super-courier", title="Курьер службы доставки",
        given=[("String", "name"), ("int", "salary"), ("String", "transport")],
        variants=[{"name": '"Oleg"', "salary": "45000", "transport": '"bike"'},
                  {"name": '"Masha"', "salary": "52000", "transport": '"scooter"'},
                  {"name": '"Boris"', "salary": "61000", "transport": '"moped"'}],
        hidden=[{"name": '"Liza"', "salary": "38000", "transport": '"skateboard"'},
                {"name": '"Rustam"', "salary": "70500", "transport": '"car"'},
                {"name": '"Ksyusha"', "salary": "40000", "transport": '"e-bike"'}],
        intro="В службе доставки работают сотрудники: у каждого есть имя и зарплата. Курьер — тоже сотрудник, только "
              "у него есть ещё и транспорт. Имя и зарплату курьера пусть сохраняет класс-родитель, а курьер добавит "
              "только своё.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Employee` без слова `public`. Дай ему "
               "закрытые поля `private String name` и `private int salary`, конструктор `Employee(String name, int salary)`, "
               "который их заполняет, и метод `String info()`, который возвращает строку вида `Oleg: 45000 rub`",
               "Опиши класс `Courier` — наследник `Employee` — с полем `private String transport` и конструктором "
               "`Courier(String name, int salary, String transport)`. Первой строкой конструктора вызови "
               "`super(name, salary);` — родитель сам заполнит имя и зарплату, — а потом сохрани транспорт.",
               "Добавь в `Courier` геттер `String getTransport()`.",
               "В `main` создай `Courier courier = new Courier(name, salary, transport);` и выведи две строки: результат "
               "`courier.info()` и строку вида `Transport: bike`."],
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
        variants=[{"players": '{"Anya", "Vika", "Sveta"}', "captain": '"Lena"', "number": "10"},
                  {"players": '{"Petya", "Kolya"}', "captain": '"Sasha"', "number": "7"},
                  {"players": '{"Dasha", "Masha", "Glasha", "Natasha", "Pasha"}', "captain": '"Misha"', "number": "1"}],
        hidden=[{"players": "{}", "captain": '"Gosha"', "number": "9"},
                {"players": '{"Ira"}', "captain": '"Yulya"', "number": "23"},
                {"players": '{"Lyova", "Tima", "Roma", "Zhenya"}', "captain": '"Fedya"', "number": "4"}],
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
               "Выведи строку вида `Captain: Lena, number 10`, а затем строку вида `Total players: 4` — число возьми "
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
        variants=[{"car": '"Lada"', "bike": '"Ural"', "speed": "180"},
                  {"car": '"Niva"', "bike": '"Yava"', "speed": "120"},
                  {"car": '"Volga"', "bike": '"Minsk"', "speed": "95"}],
        hidden=[{"car": '"Moskvich"', "bike": '"Dnepr"', "speed": "150"},
                {"car": '"Gazel"', "bike": '"Sova"', "speed": "60"},
                {"car": '"Zhiguli"', "bike": '"Voskhod"', "speed": "110"}],
        intro="Программа описывает транспорт в гараже: машину `car` и мотоцикл `bike`. У каждого транспорта есть название "
              "и число колёс. Мотоцикл — тоже транспорт, но у него всегда 2 колеса, а в описании нужна ещё и максимальная "
              "скорость `speed`. Описание мотоцикла должно продолжать описание родителя, а не повторять его код.",
        steps=["Ниже класса `Solution` опиши класс `Vehicle` (без `public`) с закрытыми полями `private String name` и "
               "`private int wheels`, конструктором `Vehicle(String name, int wheels)` и методом `String info()`, который "
               "возвращает строку вида `Lada, wheels: 4`.",
               "Опиши класс `Motorbike` — наследник `Vehicle` — с полем `private int speed` и конструктором "
               "`Motorbike(String name, int speed)`: первой строкой вызови `super(name, 2);`, а потом сохрани скорость.",
               "Переопредели в `Motorbike` метод `String info()` (с `@Override`): пусть он берёт строку родителя через "
               "`super.info()` и дописывает к ней `, top speed 180 km/h` — со скоростью из поля `speed`.",
               "В `main` создай массив `Vehicle[] garage = {{new Vehicle(car, 4), new Motorbike(bike, speed)}};` и одним "
               "циклом выведи `info()` каждого транспорта."],
        hint="`super(...)` вызывает конструктор родителя, а `super.info()` — версию метода из родителя, даже если в "
             "наследнике он переопределён. Без `super.` вызов `info()` внутри `info()` вызывал бы сам себя бесконечно.",
        solution=GARAGE_MAIN, classes=GARAGE,
        wrong=[("в info мотоцикла не вызывает super.info() — пропадают название и колёса",
                GARAGE_MAIN, GARAGE.replace('return super.info() + ", top speed " + speed + " km/h";',
                                            'return "top speed " + speed + " km/h";')),
               ("передаёт родителю 4 колеса — скопировал вызов из машины",
                GARAGE_MAIN, GARAGE.replace("super(name, 2);", "super(name, 4);"))],
        constructs=["class", "for"],
        checks=exist("Vehicle", "Motorbike")
        + extends("Motorbike", "Vehicle")
        + no_empty_constructor("Vehicle", "Vehicle(String name, int wheels)", "super(name, 2)")
        + private_fields("Vehicle", "name", "wheels")
        + f'need({declares("Motorbike", "info")}, "Переопредели в Motorbike метод String info() с пометкой @Override и допиши в нём скорость к super.info()");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-super-student-ticket", title="Студенческий билет на поезд",
        given=[("String", "route"), ("int", "price")],
        variants=[{"route": '"Kazan - Sochi"', "price": "3000"},
                  {"route": '"Moscow - Tver"', "price": "850"},
                  {"route": '"Perm - Ufa"', "price": "1250"}],
        hidden=[{"route": '"Omsk - Tomsk"', "price": "1001"},
                {"route": '"Pskov - Luga"', "price": "4400"},
                {"route": '"Tula - Oryol"', "price": "1"}],
        intro="Железная дорога продаёт билеты по маршруту `route` за `price` руб. Студенческий билет — это тот же "
              "билет, только за полцены. Хранить маршрут и цену и составлять описание умеет обычный билет, "
              "а студенческий только передаёт ему уменьшенную цену.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Ticket` без слова `public`. Дай ему "
               "закрытые поля `private String route` и `private int price`, конструктор `Ticket(String route, int price)` "
               "и метод `String info()`, который возвращает строку вида `Kazan - Sochi: 3000 rub`.",
               "Опиши класс `StudentTicket` — наследник `Ticket` — с конструктором `StudentTicket(String route, int price)`. "
               "Своих полей у него нет: в конструкторе вызови `super(route, price / 2);` — родитель сохранит маршрут "
               "и половину цены (деление целое).",
               "В `main` создай обычный билет `new Ticket(route, price)` и студенческий `new StudentTicket(route, price)` "
               "и выведи две строки: `Adult: ` и `info()` обычного билета, затем `Student: ` и `info()` студенческого — "
               "например `Student: Kazan - Sochi: 1500 rub`."],
        hint="В `super(...)` можно передать не только параметры как есть, но и выражение: родитель получит уже "
             "посчитанную половину цены. Метод `info()` студенческий билет наследует и сам не пишет.",
        solution=TICKET_MAIN, classes=TICKET,
        wrong=[("передаёт родителю полную цену — студенческий билет стоит как обычный",
                TICKET_MAIN, TICKET.replace("super(route, price / 2);", "super(route, price);")),
               ("умножает на 1 / 2 — при целом делении это 0, и билет становится бесплатным",
                TICKET_MAIN, TICKET.replace("super(route, price / 2);", "super(route, price * (1 / 2));"))],
        constructs=["class"],
        checks=exist("Ticket", "StudentTicket")
        + extends("StudentTicket", "Ticket")
        + no_empty_constructor("Ticket", "Ticket(String route, int price)", "super(route, price / 2)")
        + private_fields("Ticket", "route", "price"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-super-gold-card", title="Золотая бонусная карта",
        given=[("int", "start"), ("int[]", "purchases")],
        variants=[{"start": "0", "purchases": "{350, 1200, 99}"},
                  {"start": "40", "purchases": "{500, 500}"},
                  {"start": "15", "purchases": "{2750, 180, 620, 75}"}],
        hidden=[{"start": "100", "purchases": "{}"},
                {"start": "0", "purchases": "{50}"},
                {"start": "7", "purchases": "{1000, 1000, 1000}"},
                {"start": "250", "purchases": "{149, 151}"}],
        intro="Магазин выдаёт бонусные карты: за каждые полные 100 руб. покупки на карту начисляется 1 балл. Золотая "
              "карта — та же карта, но при выдаче на неё сразу дарят 500 баллов, а баллы за покупки начисляются "
              "в двойном размере. Покупатель с `start` баллами завёл обе карты и сделал покупки `purchases` (в рублях).",
        steps=["Ниже класса `Solution` опиши класс `Card` (без `public`) с закрытым полем `private int points`, "
               "конструктором `Card(int points)`, методом `void buy(int sum)`, который прибавляет к баллам "
               "`sum / 100`, и геттером `int getPoints()`.",
               "Опиши класс `GoldCard` — наследник `Card` — с конструктором `GoldCard(int points)`, который вызывает "
               "`super(points + 500);` — подарочные баллы.",
               "Переопредели в `GoldCard` метод `void buy(int sum)` (с `@Override`): пусть он вызывает родительский "
               "метод `super.buy(sum * 2);` — баллы начисляются как за вдвое большую покупку.",
               "В `main` создай `Card card = new Card(start);` и `GoldCard gold = new GoldCard(start);`, в одном цикле "
               "проведи каждую покупку из `purchases` по обеим картам и выведи строки вида `Regular card: 15 points` "
               "и `Gold card: 532 points`."],
        hint="Поле `points` закрыто в `Card`, поэтому `GoldCard` не может прибавить баллы сам — он просит родителя "
             "сделать это через `super.buy(...)`. Без `super.` метод `buy` вызывал бы сам себя бесконечно.",
        solution=CARD_MAIN, classes=CARD,
        wrong=[("передаёт родителю только points — подарочные 500 баллов не начислены",
                CARD_MAIN, CARD.replace("super(points + 500);", "super(points);")),
               ("переопределил buy, но вызывает super.buy(sum) — баллы не удваиваются",
                CARD_MAIN, CARD.replace("super.buy(sum * 2);", "super.buy(sum);"))],
        constructs=["class", "for"],
        checks=exist("Card", "GoldCard")
        + extends("GoldCard", "Card")
        + no_empty_constructor("Card", "Card(int points)", "super(points + 500)")
        + private_fields("Card", "points")
        + f'need({declares("GoldCard", "buy")}, "Переопредели в GoldCard метод void buy(int sum) с пометкой @Override и вызови в нём super.buy(sum * 2)");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-super-coffee-latte", title="Кофе, латте и чай",
        given=[("int", "shots"), ("String", "syrup")],
        variants=[{"shots": "2", "syrup": '"vanilla"'},
                  {"shots": "1", "syrup": '"caramel"'},
                  {"shots": "3", "syrup": '"coconut"'}],
        hidden=[{"shots": "4", "syrup": '"cherry"'},
                {"shots": "1", "syrup": '"mint"'},
                {"shots": "5", "syrup": '"maple"'}],
        intro="Кофейня описывает напитки в программе. У каждого напитка есть название и цена. Кофе — это напиток "
              "с порциями эспрессо: каждая порция сверх первой добавляет 40 руб. Латте — это кофе с молоком "
              "(+60 руб.) и сиропом. Гость заказал чай, эспрессо и латте; порций эспрессо в кофе — `shots`, "
              "сироп для латте — `syrup`.",
        steps=["Ниже класса `Solution` опиши класс `Drink` (без `public`) с закрытыми полями `private String name` и "
               "`private int price`, конструктором `Drink(String name, int price)`, методом `int getPrice()`, который "
               "возвращает цену, и методом `String info()`, который возвращает название.",
               "Опиши класс `Coffee extends Drink` с полем `private int shots` и конструктором "
               "`Coffee(String name, int shots)`: первой строкой вызови `super(name, 100);` — базовая цена кофе "
               "100 руб. Переопредели `getPrice()`: `super.getPrice() + 40 * (shots - 1)`, и `info()`: "
               "`super.info()` и дописка `, shots: 2`.",
               "Опиши класс `Latte extends Coffee` с полем `private String syrup` и конструктором "
               "`Latte(int shots, String syrup)`: первой строкой вызови `super(\"latte\", shots);`. Переопредели "
               "`getPrice()` — цена кофе через `super.getPrice()` плюс 60 — и `info()` — `super.info()` и дописка "
               "`, syrup: vanilla`.",
               "В `main` создай массив `Drink[] order = {{new Drink(\"tea\", 80), new Coffee(\"espresso\", shots), "
               "new Latte(shots, syrup)}};`. Одним циклом выведи для каждого напитка строку вида "
               "`espresso, shots: 2 - 140 rub` — `info()`, ` - ` и цену, а последней строкой — `Total: 440 rub`."],
        hint="`super.getPrice()` в `Latte` вызывает версию из `Coffee`, а та через свой `super.getPrice()` — версию "
             "из `Drink`. Каждый класс добавляет только своё, поэтому цена и описание латте собираются по цепочке.",
        solution=COFFEE_MAIN, classes=COFFEE,
        wrong=[("в info латте не вызывает super.info() — пропадают порции эспрессо",
                COFFEE_MAIN, COFFEE.replace('return super.info() + ", syrup: " + syrup;',
                                            'return "latte, syrup: " + syrup;')),
               ("считает цену латте от базовых 100 руб., а не от цены кофе — лишние порции не учтены",
                COFFEE_MAIN, COFFEE.replace("return super.getPrice() + 60;", "return 100 + 60;"))],
        constructs=["class", "for"],
        checks=exist("Drink", "Coffee", "Latte")
        + extends("Coffee", "Drink") + extends("Latte", "Coffee")
        + no_empty_constructor("Drink", "Drink(String name, int price)", "super(name, 100)")
        + private_fields("Drink", "name", "price")
        + f'need({declares("Latte", "getPrice")} && {declares("Latte", "info")}, "Переопредели в Latte методы getPrice() и info() с пометкой @Override и опирайся в них на super");\n',
    ),
]
