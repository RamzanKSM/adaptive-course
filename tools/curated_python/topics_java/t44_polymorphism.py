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

GREETINGS = """\
class Greeting {
    String language() {
        return "Unknown";
    }

    String hello(String name) {
        return name;
    }
}

class English extends Greeting {
    @Override
    String language() {
        return "English";
    }

    @Override
    String hello(String name) {
        return "Hello, " + name + "!";
    }
}

class Spanish extends Greeting {
    @Override
    String language() {
        return "Spanish";
    }

    @Override
    String hello(String name) {
        return "Hola, " + name + "!";
    }
}

class French extends Greeting {
    @Override
    String language() {
        return "French";
    }

    @Override
    String hello(String name) {
        return "Bonjour, " + name + "!";
    }
}"""

GREETINGS_MAIN = """\
Greeting[] greetings = {new English(), new Spanish(), new French()};
for (Greeting greeting : greetings) {
    System.out.println(greeting.language() + ": " + greeting.hello(guest));
}"""

TARIFFS = """\
class Tariff {
    String title() {
        return "Tariff";
    }

    int cost(int minutes) {
        return 0;
    }
}

class PerMinute extends Tariff {
    @Override
    String title() {
        return "Per minute";
    }

    @Override
    int cost(int minutes) {
        return minutes * 3;
    }
}

class Bundle extends Tariff {
    @Override
    String title() {
        return "Bundle";
    }

    @Override
    int cost(int minutes) {
        if (minutes <= 200) {
            return 300;
        }
        return 300 + (minutes - 200) * 2;
    }
}

class Unlimited extends Tariff {
    @Override
    String title() {
        return "Unlimited";
    }

    @Override
    int cost(int minutes) {
        return 550;
    }
}"""

TARIFFS_MAIN = """\
Tariff[] tariffs = {new PerMinute(), new Bundle(), new Unlimited()};
Tariff best = tariffs[0];
for (Tariff tariff : tariffs) {
    System.out.println(tariff.title() + ": " + tariff.cost(minutes) + " rub");
    if (tariff.cost(minutes) < best.cost(minutes)) {
        best = tariff;
    }
}
System.out.println("Best: " + best.title());"""

ACTIVITIES = """\
class Activity {
    int minutes;

    String title() {
        return "Activity";
    }

    int calories() {
        return 0;
    }
}

class Running extends Activity {
    @Override
    String title() {
        return "Running";
    }

    @Override
    int calories() {
        return minutes * 10;
    }
}

class Swimming extends Activity {
    @Override
    String title() {
        return "Swimming";
    }

    @Override
    int calories() {
        return minutes * 8;
    }
}

class Yoga extends Activity {
    @Override
    String title() {
        return "Yoga";
    }

    @Override
    int calories() {
        return 20 + minutes * 3;
    }
}"""

ACTIVITIES_MAIN = """\
Activity[] week = new Activity[kinds.length];
for (int i = 0; i < kinds.length; i++) {
    if (kinds[i].equals("run")) {
        week[i] = new Running();
    } else if (kinds[i].equals("swim")) {
        week[i] = new Swimming();
    } else {
        week[i] = new Yoga();
    }
    week[i].minutes = minutes[i];
}
int total = 0;
Activity best = week[0];
for (Activity activity : week) {
    System.out.println(activity.title() + " " + activity.minutes + " min: " + activity.calories() + " kcal");
    total += activity.calories();
    if (activity.calories() > best.calories()) {
        best = activity;
    }
}
System.out.println("Total: " + total + " kcal");
System.out.println("Best: " + best.title());"""

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
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-poly-hello-languages", title="Приветствие на трёх языках",
        given=[("String", "guest")],
        variants=[{"guest": '"Anya"'}, {"guest": '"Boris"'}, {"guest": '"Maria"'}],
        hidden=[{"guest": '"Timur"'}, {"guest": '"Pablo"'}, {"guest": '"Zoe"'}],
        intro="Гостиница встречает гостей на табло сразу на трёх языках: английском, испанском и французском. Каждый язык "
              "здоровается по-своему, а табло выводит все приветствия одним циклом. Имя гостя записано в поле `guest`.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Greeting` без слова `public`, с двумя "
               "методами: `String language()` возвращает `Unknown`, а `String hello(String name)` возвращает просто `name`.",
               "Опиши трёх наследников `Greeting` и переопредели в каждом оба метода (с `@Override`): `English` — язык "
               "`English`, приветствие вида `Hello, Anya!`; `Spanish` — `Spanish` и `Hola, Anya!`; `French` — `French` "
               "и `Bonjour, Anya!`.",
               "В `main` создай массив родительского типа: `Greeting[] greetings = {{new English(), new Spanish(), new French()}};`",
               "Одним циклом `for` пройди по массиву и для каждого языка выведи строку вида `English: Hello, Anya!` — "
               "имя возьми из `guest`. Методы вызывай только внутри этого цикла."],
        hint="Переменная цикла имеет тип `Greeting`, но по очереди указывает на объекты трёх разных классов. "
             "Вызов `greeting.hello(guest)` один и тот же, а Java каждый раз берёт версию метода из класса текущего объекта.",
        solution=GREETINGS_MAIN, classes=GREETINGS,
        wrong=[("в French забыл переопределить language — вместо названия языка печатается `Unknown`",
                GREETINGS_MAIN, GREETINGS.replace('class French extends Greeting {\n    @Override\n    String language() {\n        return "French";\n    }\n\n',
                                                  'class French extends Greeting {\n')),
               ("опечатка в имени метода у испанского и нет @Override — печатается только имя",
                GREETINGS_MAIN, GREETINGS.replace('    @Override\n    String hello(String name) {\n        return "Hola, " + name + "!";',
                                                  '    String helo(String name) {\n        return "Hola, " + name + "!";'))],
        constructs=["class", "for"],
        checks=exist("Greeting", "English", "Spanish", "French") + children("Greeting", "English", "Spanish", "French"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-poly-phone-tariffs", title="Выбор тарифа",
        given=[("int", "minutes")],
        variants=[{"minutes": "150"}, {"minutes": "260"}, {"minutes": "90"}],
        hidden=[{"minutes": "200"}, {"minutes": "201"}, {"minutes": "500"}, {"minutes": "0"}, {"minutes": "325"}],
        intro="Оператор связи предлагает три тарифа, и плата за месяц у каждого считается по-своему. Ты говоришь по телефону "
              "примерно `minutes` минут в месяц и хочешь увидеть цену на всех тарифах и выбрать самый дешёвый.",
        steps=["Ниже класса `Solution` опиши класс `Tariff` (без `public`) с методами `String title()`, который возвращает "
               "`Tariff`, и `int cost(int minutes)`, который возвращает `0`.",
               "Опиши трёх наследников `Tariff` и переопредели в каждом оба метода: `PerMinute` — название `Per minute`, "
               "3 руб. за минуту; `Bundle` — название `Bundle`, 300 руб., если минут не больше 200, а за каждую минуту "
               "сверх 200 ещё по 2 руб.; `Unlimited` — название `Unlimited`, всегда 550 руб.",
               "В `main` создай массив `Tariff[] tariffs = {{new PerMinute(), new Bundle(), new Unlimited()}};` и одним циклом "
               "выведи для каждого тарифа строку вида `Per minute: 450 rub`.",
               "В том же цикле найди самый дешёвый тариф (при равной цене — тот, что раньше в массиве): заведи до цикла "
               "`Tariff best = tariffs[0];`. После цикла выведи строку вида `Best: Bundle`."],
        hint="Внутри цикла не проверяй, какой это тариф: `tariff.cost(minutes)` сам вызовет нужную версию метода. "
             "Переменная `best` — тоже типа `Tariff`, и `best.title()` вернёт название именно того тарифа, на который она указывает.",
        solution=TARIFFS_MAIN, classes=TARIFFS,
        wrong=[("в Bundle граница строгая — ровно 200 минут уже считаются сверх пакета",
                TARIFFS_MAIN, TARIFFS.replace("if (minutes <= 200) {\n            return 300;\n        }\n        return 300 + (minutes - 200) * 2;",
                                              "if (minutes < 200) {\n            return 300;\n        }\n        return 300 + (minutes - 199) * 2;")),
               ("ищет самый дорогой тариф вместо самого дешёвого",
                TARIFFS_MAIN.replace("tariff.cost(minutes) < best.cost(minutes)", "tariff.cost(minutes) > best.cost(minutes)"))],
        constructs=["class", "for"],
        checks=exist("Tariff", "PerMinute", "Bundle", "Unlimited") + children("Tariff", "PerMinute", "Bundle", "Unlimited"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-poly-fitness-week", title="Тренировки за неделю",
        given=[("String[]", "kinds"), ("int[]", "minutes")],
        variants=[{"kinds": '{"run", "yoga", "swim"}', "minutes": "{30, 60, 45}"},
                  {"kinds": '{"swim", "swim", "run", "yoga"}', "minutes": "{20, 50, 25, 40}"},
                  {"kinds": '{"yoga", "run"}', "minutes": "{90, 15}"}],
        hidden=[{"kinds": '{"run"}', "minutes": "{10}"},
                {"kinds": '{"yoga", "yoga", "swim"}', "minutes": "{30, 100, 40}"},
                {"kinds": '{"swim", "run", "yoga", "run", "swim"}', "minutes": "{60, 48, 20, 50, 10}"},
                {"kinds": '{"run", "swim"}', "minutes": "{40, 50}"}],
        intro="Фитнес-браслет записал твои тренировки за неделю: в массиве `kinds` — вид тренировки (`run` — бег, `swim` — "
              "плавание, `yoga` — йога), а в `minutes` — сколько минут она длилась. Калории каждый вид спорта считает "
              "по-своему, а итоги нужно подвести одним циклом.",
        steps=["Ниже класса `Solution` опиши класс `Activity` (без `public`) с полем `int minutes` и методами `String title()`, "
               "который возвращает `Activity`, и `int calories()`, который возвращает `0`.",
               "Опиши трёх наследников `Activity` и переопредели в каждом оба метода: `Running` — название `Running`, "
               "10 ккал в минуту; `Swimming` — `Swimming`, 8 ккал в минуту; `Yoga` — `Yoga`, 20 ккал плюс 3 ккал в минуту.",
               "В `main` создай массив `Activity[] week = new Activity[kinds.length];`. Пройди по `kinds` по индексам: для "
               "`run` положи в `week[i]` новый `Running`, для `swim` — `Swimming`, для `yoga` — `Yoga`, и запиши в его поле "
               "`minutes` значение `minutes[i]`.",
               "Вторым циклом пройди по `week` и для каждой тренировки выведи строку вида `Running 30 min: 300 kcal`. В этом "
               "цикле не проверяй вид тренировки — просто вызывай `title()` и `calories()`.",
               "В конце выведи строку вида `Total: 860 kcal` — сумму калорий, и строку вида `Best: Swimming` — тренировку, "
               "сжёгшую больше всего калорий (при равенстве — более раннюю)."],
        hint="Выбирать класс через `if` нужно только при создании объектов из строк (сравнивай через `equals`). Для лучшей "
             "тренировки заведи `Activity best = week[0];` и заменяй её, когда встретишь тренировку с большим числом калорий.",
        solution=ACTIVITIES_MAIN, classes=ACTIVITIES,
        wrong=[("опечатка в имени метода у йоги и нет @Override — её калории считаются как у Activity, то есть 0",
                ACTIVITIES_MAIN, ACTIVITIES.replace("    @Override\n    int calories() {\n        return 20 + minutes * 3;",
                                                    "    int calorie() {\n        return 20 + minutes * 3;")),
               ("в Yoga забыл про 20 ккал за разминку",
                ACTIVITIES_MAIN, ACTIVITIES.replace("return 20 + minutes * 3;", "return minutes * 3;"))],
        constructs=["class", "for"],
        checks=exist("Activity", "Running", "Swimming", "Yoga") + children("Activity", "Running", "Swimming", "Yoga"),
    ),
]
