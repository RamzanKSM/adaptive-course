"""POLYMORPHISM_BASIC — «Полиморфизм» (Java). Taught before: everything up to classes, objects, constructors, this,
private fields, getters/setters, static, inheritance, overriding with @Override. Here: objects of different child
classes in one array of the parent type; one loop calls the same method on each and every object answers in its own way
— no checks of «who is who». Not yet: interfaces, super (next topics) — so parents have no constructor with parameters
and the objects keep their data in inherited fields or get it through method parameters. The student writes the classes
after Solution."""
from java_tasks import JavaOutputTask

SKILL = "POLYMORPHISM_BASIC"


def exist(*names: str) -> str:
    listed = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " и " + names[-1]
    what = "класс" if len(names) == 1 else "классы"
    condition = " && ".join(f'cls("{n}") != null' for n in names)
    return f'need({condition}, "Опиши {what} {listed} отдельно — ниже класса Solution, после его закрывающей скобки, и без слова public");\n'


def children(parent: str, *kids: str) -> str:
    listed = ", ".join(kids[:-1]) + " и " + kids[-1]
    condition = " && ".join(f'cls("{k}").getSuperclass() == cls("{parent}")' for k in kids)
    return (f'need({condition}, "Сделай {listed} наследниками {parent} (class {kids[0]} extends {parent}): '
            f'тогда их объекты поместятся в один массив типа {parent}[]");\n')


ROUTE = """\
class Transport {
    String title() {
        return "Transport";
    }

    int minutes(int km) {
        return 0;
    }
}

class Walk extends Transport {
    @Override
    String title() {
        return "On foot";
    }

    @Override
    int minutes(int km) {
        return km * 12;
    }
}

class Bike extends Transport {
    @Override
    String title() {
        return "By bike";
    }

    @Override
    int minutes(int km) {
        return km * 4;
    }
}

class Bus extends Transport {
    @Override
    String title() {
        return "By bus";
    }

    @Override
    int minutes(int km) {
        return 10 + km * 2;
    }
}"""

ROUTE_MAIN = """\
Transport[] ways = {new Walk(), new Bike(), new Bus()};
for (Transport way : ways) {
    System.out.println(way.title() + ": " + way.minutes(km) + " min");
}"""

PAYMENTS = """\
class Payment {
    String title() {
        return "Payment";
    }

    int fee(int amount) {
        return 0;
    }
}

class Cash extends Payment {
    @Override
    String title() {
        return "Cash";
    }
}

class Card extends Payment {
    @Override
    String title() {
        return "Card";
    }

    @Override
    int fee(int amount) {
        return amount / 100;
    }
}

class Transfer extends Payment {
    @Override
    String title() {
        return "Transfer";
    }

    @Override
    int fee(int amount) {
        int result = amount * 2 / 100;
        if (result < 30) {
            result = 30;
        }
        return result;
    }
}"""

PAYMENTS_MAIN = """\
Payment[] payments = {new Cash(), new Card(), new Transfer()};
for (Payment payment : payments) {
    int fee = payment.fee(amount);
    System.out.println(payment.title() + ": fee " + fee + " rub, total " + (amount + fee) + " rub");
}"""

HEROES = """\
class Hero {
    int level;

    String title() {
        return "Hero";
    }

    int damage() {
        return 0;
    }
}

class Warrior extends Hero {
    @Override
    String title() {
        return "Warrior";
    }

    @Override
    int damage() {
        return 10 * level;
    }
}

class Mage extends Hero {
    @Override
    String title() {
        return "Mage";
    }

    @Override
    int damage() {
        return 25 + 5 * level;
    }
}

class Archer extends Hero {
    @Override
    String title() {
        return "Archer";
    }

    @Override
    int damage() {
        return 15 * level;
    }
}"""

HEROES_MAIN = """\
Hero[] heroes = new Hero[team.length];
for (int i = 0; i < team.length; i++) {
    if (team[i].equals("warrior")) {
        heroes[i] = new Warrior();
    } else if (team[i].equals("mage")) {
        heroes[i] = new Mage();
    } else {
        heroes[i] = new Archer();
    }
    heroes[i].level = level;
}
int total = 0;
for (Hero hero : heroes) {
    int hit = hero.damage();
    System.out.println(hero.title() + ": damage " + hit);
    total += hit;
}
System.out.println("Team damage: " + total);"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-poly-school-route", title="Дорога до школы",
        given=[("int", "km")],
        variants=[{"km": "3"}, {"km": "5"}, {"km": "2"}],
        hidden=[{"km": "1"}, {"km": "10"}, {"km": "4"}],
        intro="До школы `km` километров. Добраться можно пешком, на велосипеде или на автобусе, и время в пути "
              "у каждого способа считается по-своему. Программа должна показать все три варианта одним циклом.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Transport` без слова `public`, с двумя методами: `String title()` возвращает "
               "`Transport`, а `int minutes(int km)` возвращает `0`.",
               "Опиши трёх наследников `Transport` и переопредели в каждом оба метода (с `@Override`): `Walk` — название "
               "`On foot`, 12 минут на каждый километр; `Bike` — `By bike`, 4 минуты на километр; `Bus` — "
               "`By bus`, 10 минут ожидания плюс 2 минуты на километр.",
               "В `main` создай массив родительского типа: `Transport[] ways = {{new Walk(), new Bike(), new Bus()}};`",
               "Одним циклом `for` пройди по массиву и для каждого способа выведи строку вида `On foot: 36 min` — "
               "расстояние возьми из `km`. Методы `title()` и `minutes(km)` вызывай только внутри этого цикла."],
        hint="Переменная цикла имеет тип `Transport`, но на самом деле по очереди указывает на пешую прогулку, велосипед "
             "и автобус. Строка `way.minutes(km)` одна и та же, а Java каждый раз вызывает версию метода из класса "
             "текущего объекта.",
        solution=ROUTE_MAIN, classes=ROUTE,
        wrong=[("в Bike забыл переопределить title — вместо названия печатается `Transport`",
                ROUTE_MAIN, ROUTE.replace('class Bike extends Transport {\n    @Override\n    String title() {\n        return "By bike";\n    }\n\n',
                                          'class Bike extends Transport {\n')),
               ("опечатка в имени метода у автобуса и нет @Override — автобус едет 0 минут",
                ROUTE_MAIN, ROUTE.replace("    @Override\n    int minutes(int km) {\n        return 10 + km * 2;",
                                          "    int minute(int km) {\n        return 10 + km * 2;"))],
        constructs=["class", "for"],
        checks=exist("Transport", "Walk", "Bike", "Bus") + children("Transport", "Walk", "Bike", "Bus"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-poly-payment-fee", title="Комиссия за оплату",
        given=[("int", "amount")],
        variants=[{"amount": "2500"}, {"amount": "900"}, {"amount": "4000"}],
        hidden=[{"amount": "1000"}, {"amount": "15000"}, {"amount": "99"}, {"amount": "1500"}],
        intro="Интернет-магазин предлагает оплатить заказ на `amount` рублей тремя способами: наличными курьеру, картой "
              "или банковским переводом. Комиссия у каждого способа своя, а показать покупателю все варианты нужно "
              "одинаково — одним циклом.",
        steps=["Ниже класса `Solution` опиши класс `Payment` (без `public`) с методами `String title()`, который возвращает `Payment`, "
               "и `int fee(int amount)`, который возвращает комиссию `0`.",
               "Опиши класс `Cash` — наследник `Payment` — и переопредели в нём только `title()`: `Cash`. Метод `fee` "
               "в нём не пиши: наличными платят без комиссии.",
               "Опиши класс `Card` — наследник `Payment`: `title()` возвращает `Card`, а `fee` — комиссию 1%, то есть "
               "`amount / 100`.",
               "Опиши класс `Transfer` — наследник `Payment`: `title()` возвращает `Transfer`, а `fee` — комиссию 2%, "
               "то есть `amount * 2 / 100`, но не меньше 30 руб.",
               "В `main` создай массив `Payment[] payments = {{new Cash(), new Card(), new Transfer()}};` и одним циклом "
               "выведи для каждого способа строку вида `Card: fee 25 rub, total 2525 rub` Внутри цикла не "
               "проверяй, какой это способ, — просто вызывай `fee(amount)`."],
        hint="У `Cash` нет своего `fee`, поэтому для него сработает версия из `Payment`, а у `Card` и `Transfer` — их "
             "собственные. Чтобы не вызывать метод дважды, сохрани комиссию в переменную и используй её и для комиссии, "
             "и для суммы к оплате.",
        solution=PAYMENTS_MAIN, classes=PAYMENTS,
        wrong=[("проверяет способ оплаты через if и берёт комиссию только у карты — перевод получается бесплатным",
                PAYMENTS_MAIN.replace("    int fee = payment.fee(amount);\n",
                                      '    int fee = 0;\n    if (payment.title().equals("Card")) {\n'
                                      '        fee = payment.fee(amount);\n    }\n')),
               ("забыл про минимальную комиссию перевода — на маленьких суммах она меньше 30 руб.",
                PAYMENTS_MAIN, PAYMENTS.replace("        if (result < 30) {\n            result = 30;\n        }\n", ""))],
        constructs=["class", "for"],
        checks=exist("Payment", "Cash", "Card", "Transfer") + children("Payment", "Cash", "Card", "Transfer"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-poly-hero-squad", title="Отряд героев",
        given=[("String[]", "team"), ("int", "level")],
        variants=[{"team": '{"warrior", "mage", "archer"}', "level": "2"},
                  {"team": '{"mage", "mage", "warrior"}', "level": "1"},
                  {"team": '{"archer", "warrior", "archer", "mage"}', "level": "3"}],
        hidden=[{"team": '{"warrior"}', "level": "5"},
                {"team": '{"archer", "mage"}', "level": "1"},
                {"team": '{"mage", "warrior", "archer", "warrior", "mage"}', "level": "4"}],
        intro="Ты собираешь отряд для похода. В массиве `team` записано, кто идёт в отряд, а в `level` — уровень всех "
              "героев. Каждый тип героя наносит урон по-своему, а программа должна посчитать урон всего отряда.",
        steps=["Ниже класса `Solution` опиши класс `Hero` (без `public`) с полем `int level` и методами `String title()`, который "
               "возвращает `Hero`, и `int damage()`, который возвращает `0`.",
               "Опиши трёх наследников `Hero` и переопредели в каждом оба метода: `Warrior` — название `Warrior`, урон — уровень, "
               "умноженный на 10; `Mage` — название `Mage`, урон — 25 плюс уровень, умноженный на 5; `Archer` — название `Archer`, урон — "
               "уровень, умноженный на 15.",
               "В `main` создай массив `Hero[] heroes = new Hero[team.length];`. Пройди по `team` по индексам: для "
               "строки `warrior` положи в `heroes[i]` новый `Warrior`, для `mage` — `Mage`, для `archer` — `Archer`. "
               "Потом запиши в поле `level` этого героя значение из `level`.",
               "Вторым циклом пройди по `heroes`: для каждого героя выведи строку вида `Warrior: damage 20` и прибавь его "
               "урон к общему. В этом цикле не проверяй, кто есть кто, — просто вызывай `title()` и `damage()`.",
               "Последней строкой выведи общий урон в виде `Team damage: 85`."],
        hint="Выбирать класс через `if` нужно только один раз — когда создаёшь героев из строк (строки сравнивай через "
             "`equals`). Дальше каждый объект сам знает свой урон и своё название, поэтому во втором цикле хватит "
             "`hero.damage()` и `hero.title()`.",
        solution=HEROES_MAIN, classes=HEROES,
        wrong=[("опечатка в имени метода у лучника и нет @Override — его урон считается как у Hero, то есть 0",
                HEROES_MAIN, HEROES.replace("    @Override\n    int damage() {\n        return 15 * level;",
                                            "    int damge() {\n        return 15 * level;")),
               ("обнуляет общий урон внутри цикла — в итоге остаётся урон только последнего героя",
                HEROES_MAIN.replace("int total = 0;\nfor (Hero hero : heroes) {\n",
                                    "int total = 0;\nfor (Hero hero : heroes) {\n    total = 0;\n"))],
        constructs=["class", "for"],
        checks=exist("Hero", "Warrior", "Mage", "Archer") + children("Hero", "Warrior", "Mage", "Archer"),
    ),
]
