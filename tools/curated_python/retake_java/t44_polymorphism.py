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



UNITS = """\
class Unit {
    String title() {
        return "Unit";
    }

    int convert(int meters) {
        return 0;
    }
}

class Centimeters extends Unit {
    @Override
    String title() {
        return "Centimeters";
    }

    @Override
    int convert(int meters) {
        return meters * 100;
    }
}

class Decimeters extends Unit {
    @Override
    String title() {
        return "Decimeters";
    }

    @Override
    int convert(int meters) {
        return meters * 10;
    }
}

class Millimeters extends Unit {
    @Override
    String title() {
        return "Millimeters";
    }

    @Override
    int convert(int meters) {
        return meters * 1000;
    }
}"""

UNITS_MAIN = """\
Unit[] units = {new Centimeters(), new Decimeters(), new Millimeters()};
for (Unit unit : units) {
    System.out.println(unit.title() + ": " + unit.convert(meters));
}"""

PROMOS = """\
class Promo {
    String title() {
        return "No promo";
    }

    int finalPrice(int price) {
        return price;
    }
}

class Percent extends Promo {
    @Override
    String title() {
        return "Minus 15%";
    }

    @Override
    int finalPrice(int price) {
        return price - price * 15 / 100;
    }
}

class Fixed extends Promo {
    @Override
    String title() {
        return "Minus 300 rub";
    }

    @Override
    int finalPrice(int price) {
        int result = price - 300;
        if (result < 0) {
            result = 0;
        }
        return result;
    }
}"""

PROMOS_MAIN = """\
Promo[] promos = {new Promo(), new Percent(), new Fixed()};
Promo best = promos[0];
for (Promo promo : promos) {
    System.out.println(promo.title() + ": " + promo.finalPrice(price) + " rub");
    if (promo.finalPrice(price) < best.finalPrice(price)) {
        best = promo;
    }
}
System.out.println("Best: " + best.title());"""

GARDEN = """\
class Crop {
    int bushes;

    String title() {
        return "Crop";
    }

    int harvest() {
        return 0;
    }

    int water() {
        return 0;
    }
}

class Tomato extends Crop {
    @Override
    String title() {
        return "Tomato";
    }

    @Override
    int harvest() {
        return bushes * 4;
    }

    @Override
    int water() {
        return bushes * 3;
    }
}

class Cucumber extends Crop {
    @Override
    String title() {
        return "Cucumber";
    }

    @Override
    int harvest() {
        return bushes * 3;
    }

    @Override
    int water() {
        return bushes * 5;
    }
}

class Pepper extends Crop {
    @Override
    String title() {
        return "Pepper";
    }

    @Override
    int harvest() {
        return bushes * 2;
    }

    @Override
    int water() {
        return bushes * 2;
    }
}"""

GARDEN_MAIN = """\
Crop[] crops = new Crop[beds.length];
for (int i = 0; i < beds.length; i++) {
    if (beds[i].equals("tomato")) {
        crops[i] = new Tomato();
    } else if (beds[i].equals("cucumber")) {
        crops[i] = new Cucumber();
    } else {
        crops[i] = new Pepper();
    }
    crops[i].bushes = bushes[i];
}
int harvest = 0;
int water = 0;
for (Crop crop : crops) {
    System.out.println(crop.title() + ": bushes " + crop.bushes + ", " + crop.harvest() + " kg");
    harvest += crop.harvest();
    water += crop.water();
}
System.out.println("Harvest: " + harvest + " kg, water: " + water + " l a day");"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-poly-rt-meter-units", title="Перевод метров",
        given=[("int", "meters")],
        variants=[{"meters": "3"}, {"meters": "12"}, {"meters": "7"}],
        hidden=[{"meters": "1"}, {"meters": "0"}, {"meters": "250"}],
        intro="Мастер измерил длину полки — `meters` метров — и хочет записать её сразу в сантиметрах, дециметрах и "
              "миллиметрах. Каждая единица переводит метры по-своему, а показать все три варианта нужно одним циклом.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Unit` без слова `public`, с двумя методами: "
               "`String title()` возвращает `Unit`, а `int convert(int meters)` возвращает `0`.",
               "Опиши трёх наследников `Unit` и переопредели в каждом оба метода (с `@Override`): `Centimeters` — название "
               "`Centimeters`, метры умножаются на 100; `Decimeters` — `Decimeters`, на 10; `Millimeters` — `Millimeters`, на 1000.",
               "В `main` создай массив родительского типа: `Unit[] units = {{new Centimeters(), new Decimeters(), new Millimeters()}};`",
               "Одним циклом `for` пройди по массиву и для каждой единицы выведи строку вида `Centimeters: 300`. "
               "Методы `title()` и `convert(meters)` вызывай только внутри этого цикла."],
        hint="Переменная цикла имеет тип `Unit`, но по очереди указывает на объекты трёх разных классов. Вызов "
             "`unit.convert(meters)` один и тот же, а Java каждый раз берёт версию метода из класса текущего объекта.",
        solution=UNITS_MAIN, classes=UNITS,
        wrong=[("в Decimeters забыл переопределить title — вместо названия печатается `Unit`",
                UNITS_MAIN, UNITS.replace('class Decimeters extends Unit {\n    @Override\n    String title() {\n        return "Decimeters";\n    }\n\n',
                                          'class Decimeters extends Unit {\n')),
               ("опечатка в имени метода у миллиметров и нет @Override — выходит 0",
                UNITS_MAIN, UNITS.replace("    @Override\n    int convert(int meters) {\n        return meters * 1000;",
                                          "    int converts(int meters) {\n        return meters * 1000;"))],
        constructs=["class", "for"],
        checks=exist("Unit", "Centimeters", "Decimeters", "Millimeters") + children("Unit", "Centimeters", "Decimeters", "Millimeters"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-poly-rt-promo-codes", title="Промокоды",
        given=[("int", "price")],
        variants=[{"price": "1000"}, {"price": "3000"}, {"price": "250"}],
        hidden=[{"price": "2000"}, {"price": "2500"}, {"price": "0"}, {"price": "300"}, {"price": "10000"}],
        intro="В корзине интернет-магазина товаров на `price` руб. У покупателя два промокода: один снижает цену на 15%, "
              "другой — на 300 руб. Можно и не применять промокод вовсе. Нужно показать все три варианта одним циклом "
              "и выбрать самый выгодный.",
        steps=["Ниже класса `Solution` опиши класс `Promo` (без `public`) с методами `String title()`, который возвращает "
               "`No promo`, и `int finalPrice(int price)`, который возвращает `price` без изменений.",
               "Опиши класс `Percent` — наследник `Promo`: `title()` возвращает `Minus 15%`, а `finalPrice` — "
               "`price - price * 15 / 100`.",
               "Опиши класс `Fixed` — наследник `Promo`: `title()` возвращает `Minus 300 rub`, а `finalPrice` — цену "
               "минус 300, но не меньше 0.",
               "В `main` создай массив `Promo[] promos = {{new Promo(), new Percent(), new Fixed()}};` и одним циклом выведи для "
               "каждого варианта строку вида `Minus 15%: 850 rub`. В этом же цикле найди вариант с самой низкой ценой.",
               "Последней строкой выведи строку вида `Best: Minus 300 rub`. Если цены равны, побеждает тот вариант, что в "
               "массиве раньше."],
        hint="Храни лучший вариант в переменной `Promo best = promos[0];` и заменяй его, только если цена строго меньше. "
             "В цикле не проверяй, какой это промокод, — просто вызывай `finalPrice(price)`.",
        solution=PROMOS_MAIN, classes=PROMOS,
        wrong=[("при равных ценах выбирает последний вариант, а не первый",
                PROMOS_MAIN.replace("promo.finalPrice(price) < best.finalPrice(price)", "promo.finalPrice(price) <= best.finalPrice(price)")),
               ("забыл, что цена не бывает меньше 0, — у дешёвой корзины выходит отрицательная цена",
                PROMOS_MAIN, PROMOS.replace("        if (result < 0) {\n            result = 0;\n        }\n", ""))],
        constructs=["class", "for"],
        checks=exist("Promo", "Percent", "Fixed") + children("Promo", "Percent", "Fixed"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-poly-rt-vegetable-garden", title="Огород",
        given=[("String[]", "beds"), ("int[]", "bushes")],
        variants=[{"beds": '{"tomato", "cucumber", "pepper"}', "bushes": "{5, 4, 6}"},
                  {"beds": '{"cucumber", "cucumber"}', "bushes": "{3, 7}"},
                  {"beds": '{"pepper", "tomato", "tomato", "cucumber"}', "bushes": "{2, 10, 1, 8}"}],
        hidden=[{"beds": '{"tomato"}', "bushes": "{1}"},
                {"beds": "{}", "bushes": "{}"},
                {"beds": '{"pepper", "cucumber", "tomato", "pepper", "cucumber"}', "bushes": "{4, 2, 3, 9, 1}"}],
        intro="На огороде несколько грядок. В массиве `beds` записано, что растёт на каждой грядке (`tomato`, `cucumber` "
              "или `pepper`), а в `bushes` — сколько там кустов. Урожай и полив каждая культура считает по-своему: "
              "с куста томатов 4 кг, огурцов 3 кг, перца 2 кг; поливать куст томатов нужно 3 л в день, огурцов 5 л, перца 2 л.",
        steps=["Ниже класса `Solution` опиши класс `Crop` (без `public`) с полем `int bushes` и методами `String title()` "
               "(возвращает `Crop`), `int harvest()` и `int water()` (оба возвращают `0`).",
               "Опиши трёх наследников `Crop` — `Tomato`, `Cucumber` и `Pepper` — и переопредели в каждом все три метода: "
               "название (`Tomato`, `Cucumber`, `Pepper`), урожай в кг и полив в литрах — кусты, умноженные на числа из условия.",
               "В `main` создай массив `Crop[] crops = new Crop[beds.length];`. Пройди по `beds`: для `tomato` положи в "
               "`crops[i]` новый `Tomato`, для `cucumber` — `Cucumber`, для `pepper` — `Pepper`, и запиши в его поле "
               "`bushes` число из `bushes`.",
               "Вторым циклом пройди по `crops` и для каждой грядки выведи строку вида `Tomato: bushes 5, 20 kg`. Там же "
               "складывай урожай и полив всех грядок, не проверяя, какая это культура.",
               "Последней строкой выведи строку вида `Harvest: 44 kg, water: 47 l a day`."],
        hint="Выбирать класс через `if` нужно только один раз — когда создаёшь грядки из строк (строки сравнивай через "
             "`equals`). Дальше каждый объект сам знает свой урожай и полив, поэтому во втором цикле хватит "
             "`crop.harvest()` и `crop.water()`.",
        solution=GARDEN_MAIN, classes=GARDEN,
        wrong=[("опечатка в имени метода полива у огурцов и нет @Override — огурцы как будто не поливают",
                GARDEN_MAIN, GARDEN.replace("    @Override\n    int water() {\n        return bushes * 5;",
                                            "    int waters() {\n        return bushes * 5;")),
               ("для перца создаёт томаты — забыл третью ветку",
                GARDEN_MAIN.replace("        crops[i] = new Pepper();", "        crops[i] = new Tomato();"))],
        constructs=["class", "for"],
        checks=exist("Crop", "Tomato", "Cucumber", "Pepper") + children("Crop", "Tomato", "Cucumber", "Pepper"),
    ),
]
