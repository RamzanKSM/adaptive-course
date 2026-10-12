"""CONSTRUCTOR_BASIC — «Конструкторы» (Java). Taught before: everything up to static methods of Solution, classes with
fields and methods, creating objects with `new`. Here: a constructor fills the fields when the object is created;
it has the class's name and no return type; it may set fields that are not passed (a default) or computed ones;
a class may have two constructors with different parameters. Parameters are named differently from the fields —
`this` is the next topic. Not yet: this, private, static fields."""
from java_tasks import JavaOutputTask

SKILL = "CONSTRUCTOR_BASIC"


def find_class(name: str) -> str:
    return (f'Class<?> c = cls("{name}");\n'
            f'need(c != null, "Создай класс {name} ниже класса Solution (после его закрывающей скобки) и без слова public");\n')


def need_field(cls: str, name: str, java_type: str, why: str) -> str:
    """An instance (non-static) field of the class with this name and type."""
    return (f'{{ Field f = null; try {{ f = c.getDeclaredField("{name}"); }} catch (NoSuchFieldException e) {{ }}\n'
            f'  need(f != null && f.getType() == {java_type}.class, "Объяви в классе {cls} поле {java_type} {name} — {why}");\n'
            f'  need(!Modifier.isStatic(f.getModifiers()), "Объяви поле {name} в классе {cls} без слова static — тогда у каждого объекта будет своё значение"); }}\n')


def _types(params: list[str]) -> str:
    return ", ".join(f"{p.split()[0]}.class" for p in params)


def need_constructor(cls: str, params: list[str], why: str) -> str:
    return (f'{{ Constructor<?> k = null; try {{ k = c.getDeclaredConstructor({_types(params)}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(k != null, "Добавь в класс {cls} конструктор {cls}({", ".join(params)}) — {why}"); }}\n')


def need_built(params: list[str], args: str, expect: dict[str, str], message: str) -> str:
    """Creates an object with this constructor and compares its fields with the expected values (Java source)."""
    code = (f'{{ Constructor<?> k = c.getDeclaredConstructor({_types(params)}); k.setAccessible(true);\n'
            f'  Object o = null; try {{ o = k.newInstance({args}); }} catch (Exception e) {{ }}\n')
    conditions = []
    for i, (name, value) in enumerate(expect.items()):
        code += f'  Field f{i} = c.getDeclaredField("{name}"); f{i}.setAccessible(true);\n'
        conditions.append(f"Objects.equals(f{i}.get(o), {value})")
    return code + f'  need(o != null && {" && ".join(conditions)}, "{message}"); }}\n'


# ───────── Swimming pool membership ─────────

MEMBERSHIP = '''class Membership {
    String owner;
    int months;
    int visits;

    Membership(String ownerName, int monthCount) {
        owner = ownerName;
        months = monthCount;
        visits = monthCount * 8;
    }
}'''

MEMBERSHIP_MAIN = '''Membership card = new Membership(owner, months);
System.out.println("Абонемент: " + card.owner);
System.out.println("Срок: " + card.months + " мес.");
System.out.println("Посещений: " + card.visits);'''

MEMBERSHIP_PARAMS = ["String ownerName", "int monthCount"]

# ───────── Price tags ─────────

PRICE_TAG = '''class PriceTag {
    String name;
    int price;
    int salePrice;

    PriceTag(String productName, int fullPrice, int percent) {
        name = productName;
        price = fullPrice;
        salePrice = fullPrice - fullPrice * percent / 100;
    }
}'''

PRICE_TAG_MAIN = '''System.out.println("Скидка " + discount + "%");
for (int i = 0; i < names.length; i++) {
    PriceTag tag = new PriceTag(names[i], prices[i], discount);
    System.out.println(tag.name + ": было " + tag.price + " руб., стало " + tag.salePrice + " руб.");
}'''

PRICE_TAG_PARAMS = ["String productName", "int fullPrice", "int percent"]

# ───────── Marathon ─────────

RUNNER = '''class Runner {
    String name;
    int km;

    Runner(String runnerName) {
        name = runnerName;
        km = 5;
    }

    Runner(String runnerName, int distance) {
        name = runnerName;
        km = distance;
    }
}'''

RUNNER_MAIN = '''int total = 0;
for (int i = 0; i < names.length; i++) {
    Runner runner;
    if (distances[i] == 0) {
        runner = new Runner(names[i]);
    } else {
        runner = new Runner(names[i], distances[i]);
    }
    System.out.println(runner.name + ": " + runner.km + " км");
    total += runner.km;
}
System.out.println("Всего километров: " + total);'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ctor-pool-membership", title="Абонемент в бассейн",
        given=[("String", "owner"), ("int", "months")],
        variants=[{"owner": '"Аня"', "months": "3"}, {"owner": '"Кирилл"', "months": "6"}, {"owner": '"Оля"', "months": "1"}],
        hidden=[{"owner": '"Тимур"', "months": "12"}, {"owner": '"Зоя"', "months": "2"}, {"owner": '"Марат"', "months": "9"}],
        intro="Бассейн продаёт абонементы на несколько месяцев, и в каждом месяце по абонементу можно прийти 8 раз. "
              "Когда абонемент оформляют, в нём сразу записывают владельца, срок и число посещений — для этого "
              "в классе делают конструктор. Имя владельца — в поле `owner`, срок в месяцах — в поле `months`.",
        steps=["Ниже класса `Solution` создай класс `Membership` (без `public`) с полями `String owner`, `int months` и `int visits`.",
               "Добавь в класс конструктор `Membership(String ownerName, int monthCount)`. Он сохраняет имя в поле `owner`, "
               "срок — в поле `months`, а в поле `visits` записывает число посещений: по 8 на каждый месяц.",
               "В `main` создай абонемент одной строкой: `Membership card = new Membership(owner, months);`.",
               "Выведи три строки вида `Абонемент: Аня`, `Срок: 3 мес.` и `Посещений: 24` — значения бери из полей объекта `card`."],
        hint="Конструктор пишется как метод без типа результата, а его имя совпадает с именем класса. Внутри не объявляй "
             "переменные заново: строка `int visits = …` создаст новую переменную внутри конструктора, а поле объекта "
             "так и останется нулём.",
        solution=MEMBERSHIP_MAIN,
        classes=MEMBERSHIP,
        wrong=[("в конструкторе забыл сохранить срок — поле months остаётся 0",
                MEMBERSHIP_MAIN, MEMBERSHIP.replace("        months = monthCount;\n", "")),
               ("в конструкторе объявил новую переменную `int visits` вместо записи в поле — посещений 0",
                MEMBERSHIP_MAIN, MEMBERSHIP.replace("        visits = monthCount * 8;", "        int visits = monthCount * 8;"))],
        constructs=["class"],
        checks=find_class("Membership")
               + need_field("Membership", "owner", "String", "владелец абонемента")
               + need_field("Membership", "months", "int", "срок абонемента в месяцах")
               + need_field("Membership", "visits", "int", "сколько раз можно прийти в бассейн")
               + need_constructor("Membership", MEMBERSHIP_PARAMS, "он заполняет поля, когда создаётся объект")
               + need_built(MEMBERSHIP_PARAMS, '"Тест", 2', {"owner": '"Тест"', "months": "2", "visits": "16"},
                            "Конструктор Membership должен сам заполнить поля owner, months и visits — по 8 посещений на каждый месяц"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ctor-sale-price-tags", title="Ценники на распродаже",
        given=[("String[]", "names"), ("int[]", "prices"), ("int", "discount")],
        variants=[{"names": '{"Чай", "Мёд", "Сыр"}', "prices": "{200, 450, 600}", "discount": "10"},
                  {"names": '{"Кофе", "Печенье"}', "prices": "{500, 120}", "discount": "25"},
                  {"names": '{"Хлеб", "Масло", "Молоко", "Яйца"}', "prices": "{60, 240, 90, 130}", "discount": "20"}],
        hidden=[{"names": '{"Рис"}', "prices": "{100}", "discount": "5"},
                {"names": '{"Сок", "Каша", "Шоколад"}', "prices": "{150, 80, 95}", "discount": "20"},
                {"names": '{"Торт", "Конфеты"}', "prices": "{1000, 300}", "discount": "50"},
                {"names": '{"Вода"}', "prices": "{40}", "discount": "0"}],
        intro="В магазине распродажа: на все товары скидка `discount` процентов, и для каждого товара нужно напечатать "
              "новый ценник. Названия товаров — в массиве `names`, обычные цены — в массиве `prices` под теми же номерами.",
        steps=["Ниже класса `Solution` создай класс `PriceTag` (без `public`) с полями `String name`, `int price` и `int salePrice`.",
               "Добавь конструктор `PriceTag(String productName, int fullPrice, int percent)`. Он сохраняет название и обычную "
               "цену, а в `salePrice` записывает цену со скидкой. Скидка в рублях — это `fullPrice * percent / 100` "
               "(дробная часть отбрасывается).",
               "Первой строкой выведи строку вида `Скидка 10%` с числом из `discount`.",
               "Потом в цикле для каждого товара создай ценник `new PriceTag(names[i], prices[i], discount)` и выведи "
               "строку вида `Чай: было 200 руб., стало 180 руб.` — с полями этого ценника."],
        hint="Порядок действий важен: `fullPrice * percent / 100` сначала умножает, потом делит. Если сначала разделить "
             "`percent / 100`, целочисленное деление даст 0 — и скидка пропадёт.",
        solution=PRICE_TAG_MAIN,
        classes=PRICE_TAG,
        wrong=[("делит процент на 100 раньше умножения — целочисленное деление даёт 0, и скидки нет",
                PRICE_TAG_MAIN, PRICE_TAG.replace("fullPrice * percent / 100", "fullPrice * (percent / 100)")),
               ("вычитает из цены сам процент, а не рубли скидки",
                PRICE_TAG_MAIN, PRICE_TAG.replace("fullPrice - fullPrice * percent / 100", "fullPrice - percent"))],
        constructs=["class"],
        checks=find_class("PriceTag")
               + need_field("PriceTag", "name", "String", "название товара")
               + need_field("PriceTag", "price", "int", "обычная цена")
               + need_field("PriceTag", "salePrice", "int", "цена со скидкой")
               + need_constructor("PriceTag", PRICE_TAG_PARAMS, "он заполняет ценник, когда создаётся объект")
               + need_built(PRICE_TAG_PARAMS, '"Тест", 200, 10', {"name": '"Тест"', "price": "200", "salePrice": "180"},
                            "Конструктор PriceTag должен сам заполнить поля name, price и salePrice — цена со скидкой равна fullPrice - fullPrice * percent / 100"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ctor-marathon-signup", title="Запись на марафон",
        given=[("String[]", "names"), ("int[]", "distances")],
        variants=[{"names": '{"Аня", "Борис", "Вика"}', "distances": "{10, 0, 21}"},
                  {"names": '{"Глеб", "Дина"}', "distances": "{0, 42}"},
                  {"names": '{"Егор", "Жанна", "Захар", "Ира"}', "distances": "{5, 10, 0, 0}"}],
        hidden=[{"names": '{"Кира"}', "distances": "{0}"},
                {"names": '{"Лена", "Марк"}', "distances": "{42, 21}"},
                {"names": '{"Нил", "Оля", "Петя"}', "distances": "{0, 0, 10}"},
                {"names": '{"Рита", "Саша", "Тая", "Уля", "Федя"}', "distances": "{3, 0, 15, 0, 1}"}],
        intro="На городской марафон можно записаться на любую дистанцию, а кто дистанцию не выбрал, бежит 5 км. "
              "Имена участников — в массиве `names`, выбранные дистанции в километрах — в массиве `distances` "
              "под теми же номерами; 0 значит, что дистанцию не выбрали.",
        steps=["Ниже класса `Solution` создай класс `Runner` (без `public`) с полями `String name` и `int km`.",
               "Сделай в классе два конструктора. `Runner(String runnerName)` сохраняет имя и ставит дистанцию 5 км. "
               "`Runner(String runnerName, int distance)` сохраняет имя и переданную дистанцию.",
               "В `main` пройди циклом по участникам и создай для каждого объект: если в `distances` стоит 0 — конструктором "
               "с одним параметром, иначе — конструктором с двумя. Для каждого участника выведи строку вида `Аня: 10 км`.",
               "Последней строкой выведи строку вида `Всего километров: 36` — сумму полей `km` всех участников."],
        hint="В классе может быть несколько конструкторов, если у них разные параметры. Java сама выберет нужный по тому, "
             "сколько аргументов и каких типов ты передал в `new Runner(...)`.",
        solution=RUNNER_MAIN,
        classes=RUNNER,
        wrong=[("в конструкторе с одним параметром забыл поставить 5 км — дистанция остаётся 0",
                RUNNER_MAIN, RUNNER.replace("        km = 5;\n", "")),
               ("складывает числа из массива distances, а не дистанции участников — пятёрки не попадают в сумму",
                RUNNER_MAIN.replace("total += runner.km;", "total += distances[i];"))],
        constructs=["class"],
        checks=find_class("Runner")
               + need_field("Runner", "name", "String", "имя участника")
               + need_field("Runner", "km", "int", "дистанция в километрах")
               + need_constructor("Runner", ["String runnerName"], "для тех, кто не выбрал дистанцию: он ставит 5 км")
               + need_constructor("Runner", ["String runnerName", "int distance"], "для тех, кто выбрал дистанцию")
               + need_built(["String runnerName"], '"Тест"', {"name": '"Тест"', "km": "5"},
                            "Конструктор Runner(String runnerName) должен сохранить имя и сам поставить дистанцию 5 км")
               + need_built(["String runnerName", "int distance"], '"Тест", 21', {"name": '"Тест"', "km": "21"},
                            "Конструктор Runner(String runnerName, int distance) должен сохранить имя и переданную дистанцию"),
    ),
]
