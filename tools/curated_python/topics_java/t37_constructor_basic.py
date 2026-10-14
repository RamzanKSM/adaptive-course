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
System.out.println("Membership: " + card.owner);
System.out.println("Term: " + card.months + " months");
System.out.println("Visits: " + card.visits);'''

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

PRICE_TAG_MAIN = '''System.out.println("Sale " + discount + "%");
for (int i = 0; i < names.length; i++) {
    PriceTag tag = new PriceTag(names[i], prices[i], discount);
    System.out.println(tag.name + ": was " + tag.price + " rub, now " + tag.salePrice + " rub");
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
    System.out.println(runner.name + ": " + runner.km + " km");
    total += runner.km;
}
System.out.println("Total km: " + total);'''

# ───────── Parcel ─────────

PARCEL = '''class Parcel {
    String receiver;
    String city;
    String status;

    Parcel(String receiverName, String cityName) {
        receiver = receiverName;
        city = cityName;
        status = "accepted";
    }
}'''

PARCEL_MAIN = '''Parcel parcel = new Parcel(receiver, city);
System.out.println("Parcel for " + parcel.receiver);
System.out.println("City: " + parcel.city);
System.out.println("Status: " + parcel.status);'''

PARCEL_PARAMS = ["String receiverName", "String cityName"]

# ───────── Fuel ─────────

TRIP = '''class Trip {
    String route;
    int km;
    int liters;
    int per100;

    Trip(String routeName, int distance, int fuel) {
        route = routeName;
        km = distance;
        liters = fuel;
        per100 = fuel * 100 / distance;
    }
}'''

TRIP_MAIN = '''for (int i = 0; i < routes.length; i++) {
    Trip trip = new Trip(routes[i], distances[i], fuel[i]);
    System.out.println(trip.route + ": " + trip.km + " km, " + trip.liters + " l, " + trip.per100 + " l per 100 km");
}'''

TRIP_PARAMS = ["String routeName", "int distance", "int fuel"]

# ───────── Exams ─────────

EXAM = '''class Exam {
    String subject;
    int best;
    int average;

    Exam(String subjectName, int[] scores) {
        subject = subjectName;
        int sum = 0;
        best = scores[0];
        for (int score : scores) {
            sum += score;
            if (score > best) {
                best = score;
            }
        }
        average = sum / scores.length;
    }
}'''

EXAM_MAIN = '''Exam first = new Exam(subject1, scores1);
Exam second = new Exam(subject2, scores2);
System.out.println(first.subject + ": best " + first.best + ", average " + first.average);
System.out.println(second.subject + ": best " + second.best + ", average " + second.average);
if (first.average > second.average) {
    System.out.println("Better: " + first.subject);
} else if (second.average > first.average) {
    System.out.println("Better: " + second.subject);
} else {
    System.out.println("Equal");
}'''

EXAM_PARAMS = ["String subjectName", "int[] scores"]

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ctor-pool-membership", title="Абонемент в бассейн",
        given=[("String", "owner"), ("int", "months")],
        variants=[{"owner": '"Anya"', "months": "3"}, {"owner": '"Kirill"', "months": "6"}, {"owner": '"Olya"', "months": "1"}],
        hidden=[{"owner": '"Timur"', "months": "12"}, {"owner": '"Zoya"', "months": "2"}, {"owner": '"Marat"', "months": "9"}],
        intro="Бассейн продаёт абонементы на несколько месяцев, и в каждом месяце по абонементу можно прийти 8 раз. "
              "Когда абонемент оформляют, в нём сразу записывают владельца, срок и число посещений — для этого "
              "в классе делают конструктор. Имя владельца — в поле `owner`, срок в месяцах — в поле `months`.",
        steps=["Ниже класса `Solution` создай класс `Membership` (без `public`) с полями `String owner`, `int months` и `int visits`.",
               "Добавь в класс конструктор `Membership(String ownerName, int monthCount)`. Он сохраняет имя в поле `owner`, "
               "срок — в поле `months`, а в поле `visits` записывает число посещений: по 8 на каждый месяц.",
               "В `main` создай абонемент одной строкой: `Membership card = new Membership(owner, months);`.",
               "Выведи три строки вида `Membership: Anya`, `Term: 3 months` и `Visits: 24` — значения бери из полей объекта `card`."],
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
               + need_built(MEMBERSHIP_PARAMS, '"Test", 2', {"owner": '"Test"', "months": "2", "visits": "16"},
                            "Конструктор Membership должен сам заполнить поля owner, months и visits — по 8 посещений на каждый месяц"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ctor-sale-price-tags", title="Ценники на распродаже",
        given=[("String[]", "names"), ("int[]", "prices"), ("int", "discount")],
        variants=[{"names": '{"Tea", "Honey", "Cheese"}', "prices": "{200, 450, 600}", "discount": "10"},
                  {"names": '{"Coffee", "Cookies"}', "prices": "{500, 120}", "discount": "25"},
                  {"names": '{"Bread", "Butter", "Milk", "Eggs"}', "prices": "{60, 240, 90, 130}", "discount": "20"}],
        hidden=[{"names": '{"Rice"}', "prices": "{100}", "discount": "5"},
                {"names": '{"Juice", "Porridge", "Chocolate"}', "prices": "{150, 80, 95}", "discount": "20"},
                {"names": '{"Cake", "Candy"}', "prices": "{1000, 300}", "discount": "50"},
                {"names": '{"Water"}', "prices": "{40}", "discount": "0"}],
        intro="В магазине распродажа: на все товары скидка `discount` процентов, и для каждого товара нужно напечатать "
              "новый ценник. Названия товаров — в массиве `names`, обычные цены — в массиве `prices` под теми же номерами.",
        steps=["Ниже класса `Solution` создай класс `PriceTag` (без `public`) с полями `String name`, `int price` и `int salePrice`.",
               "Добавь конструктор `PriceTag(String productName, int fullPrice, int percent)`. Он сохраняет название и обычную "
               "цену, а в `salePrice` записывает цену со скидкой. Скидка в рублях — это `fullPrice * percent / 100` "
               "(дробная часть отбрасывается).",
               "Первой строкой выведи строку вида `Sale 10%` с числом из `discount`.",
               "Потом в цикле для каждого товара создай ценник `new PriceTag(names[i], prices[i], discount)` и выведи "
               "строку вида `Tea: was 200 rub, now 180 rub` — с полями этого ценника."],
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
               + need_built(PRICE_TAG_PARAMS, '"Test", 200, 10', {"name": '"Test"', "price": "200", "salePrice": "180"},
                            "Конструктор PriceTag должен сам заполнить поля name, price и salePrice — цена со скидкой равна fullPrice - fullPrice * percent / 100"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ctor-marathon-signup", title="Запись на марафон",
        given=[("String[]", "names"), ("int[]", "distances")],
        variants=[{"names": '{"Anya", "Boris", "Vika"}', "distances": "{10, 0, 21}"},
                  {"names": '{"Gleb", "Dina"}', "distances": "{0, 42}"},
                  {"names": '{"Egor", "Zhanna", "Zakhar", "Ira"}', "distances": "{5, 10, 0, 0}"}],
        hidden=[{"names": '{"Kira"}', "distances": "{0}"},
                {"names": '{"Lena", "Mark"}', "distances": "{42, 21}"},
                {"names": '{"Nil", "Olya", "Petya"}', "distances": "{0, 0, 10}"},
                {"names": '{"Rita", "Sasha", "Taya", "Ulya", "Fedya"}', "distances": "{3, 0, 15, 0, 1}"}],
        intro="На городской марафон можно записаться на любую дистанцию, а кто дистанцию не выбрал, бежит 5 км. "
              "Имена участников — в массиве `names`, выбранные дистанции в километрах — в массиве `distances` "
              "под теми же номерами; 0 значит, что дистанцию не выбрали.",
        steps=["Ниже класса `Solution` создай класс `Runner` (без `public`) с полями `String name` и `int km`.",
               "Сделай в классе два конструктора. `Runner(String runnerName)` сохраняет имя и ставит дистанцию 5 км. "
               "`Runner(String runnerName, int distance)` сохраняет имя и переданную дистанцию.",
               "В `main` пройди циклом по участникам и создай для каждого объект: если в `distances` стоит 0 — конструктором "
               "с одним параметром, иначе — конструктором с двумя. Для каждого участника выведи строку вида `Anya: 10 km`.",
               "Последней строкой выведи строку вида `Total km: 36` — сумму полей `km` всех участников."],
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
               + need_built(["String runnerName"], '"Test"', {"name": '"Test"', "km": "5"},
                            "Конструктор Runner(String runnerName) должен сохранить имя и сам поставить дистанцию 5 км")
               + need_built(["String runnerName", "int distance"], '"Test", 21', {"name": '"Test"', "km": "21"},
                            "Конструктор Runner(String runnerName, int distance) должен сохранить имя и переданную дистанцию"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ctor-parcel-accepted", title="Приём посылки",
        given=[("String", "receiver"), ("String", "city")],
        variants=[{"receiver": '"Anya"', "city": '"Kazan"'}, {"receiver": '"Boris"', "city": '"Sochi"'},
                  {"receiver": '"Liza"', "city": '"Omsk"'}],
        hidden=[{"receiver": '"Timur"', "city": '"Tula"'}, {"receiver": '"Zoya"', "city": '"Perm"'},
                {"receiver": '"Marat"', "city": '"Samara"'}],
        intro="На почте принимают посылку: записывают получателя и город, а статус у только что принятой посылки всегда "
              "один — `accepted`. Пусть всё это делает конструктор. Получатель записан в поле `receiver`, город — в поле `city`.",
        steps=["Ниже класса `Solution` создай класс `Parcel` (без `public`) с полями `String receiver`, `String city` "
               "и `String status`.",
               "Добавь конструктор `Parcel(String receiverName, String cityName)`. Он сохраняет получателя и город в поля, "
               "а в поле `status` сам записывает строку `\"accepted\"` — её не передают при создании.",
               "В `main` создай посылку одной строкой: `Parcel parcel = new Parcel(receiver, city);`.",
               "Выведи три строки вида `Parcel for Anya`, `City: Kazan` и `Status: accepted` — значения бери из полей "
               "объекта `parcel`."],
        hint="Конструктор может заполнить поле и тем, чего нет среди его параметров. Только не пиши перед полем тип: "
             "`String status = ...` внутри конструктора создаст новую переменную, а поле останется `null`.",
        solution=PARCEL_MAIN,
        classes=PARCEL,
        wrong=[("в конструкторе забыл сохранить город — поле city остаётся null",
                PARCEL_MAIN, PARCEL.replace("        city = cityName;\n", "")),
               ("в конструкторе объявил новую переменную `String status` вместо записи в поле",
                PARCEL_MAIN, PARCEL.replace('        status = "accepted";', '        String status = "accepted";'))],
        constructs=["class"],
        checks=find_class("Parcel")
               + need_field("Parcel", "receiver", "String", "получатель посылки")
               + need_field("Parcel", "city", "String", "город доставки")
               + need_field("Parcel", "status", "String", "статус посылки")
               + need_constructor("Parcel", PARCEL_PARAMS, "он заполняет поля, когда посылку принимают")
               + need_built(PARCEL_PARAMS, '"Test", "Town"', {"receiver": '"Test"', "city": '"Town"', "status": '"accepted"'},
                            "Конструктор Parcel должен сам заполнить поля receiver, city и status — статус всегда accepted"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ctor-fuel-trips", title="Расход бензина",
        given=[("String[]", "routes"), ("int[]", "distances"), ("int[]", "fuel")],
        variants=[{"routes": '{"Kazan", "Tver"}', "distances": "{800, 170}", "fuel": "{64, 17}"},
                  {"routes": '{"Sochi", "Anapa", "Yalta"}', "distances": "{1600, 300, 900}", "fuel": "{112, 27, 81}"},
                  {"routes": '{"Pskov", "Ufa", "Omsk", "Tula"}', "distances": "{700, 1300, 2700, 180}", "fuel": "{49, 117, 189, 18}"}],
        hidden=[{"routes": '{"Kirov"}', "distances": "{900}", "fuel": "{90}"},
                {"routes": '{"Orel", "Perm"}', "distances": "{360, 1400}", "fuel": "{25, 140}"},
                {"routes": '{"Chita", "Tomsk", "Kursk"}', "distances": "{150, 50, 530}", "fuel": "{12, 6, 37}"}],
        intro="Водитель записывает свои поездки: куда ехал (массив `routes`), сколько километров проехал (массив "
              "`distances`) и сколько литров бензина потратил (массив `fuel`) — всё под одинаковыми номерами. Ему "
              "интересно, сколько машина тратит на 100 км в каждой поездке.",
        steps=["Ниже класса `Solution` создай класс `Trip` (без `public`) с полями `String route`, `int km`, `int liters` "
               "и `int per100`.",
               "Добавь конструктор `Trip(String routeName, int distance, int fuel)`. Он сохраняет маршрут, километры и литры, "
               "а в `per100` записывает расход на 100 км: `fuel * 100 / distance` (дробная часть отбрасывается).",
               "В `main` в цикле создай для каждой поездки объект `new Trip(routes[i], distances[i], fuel[i])` и выведи строку "
               "вида `Kazan: 800 km, 64 l, 8 l per 100 km` — с полями этого объекта."],
        hint="Аргументы в `new Trip(...)` попадают в параметры конструктора строго по порядку: первый — маршрут, "
             "второй — километры, третий — литры.",
        solution=TRIP_MAIN,
        classes=TRIP,
        wrong=[("сначала делит литры на километры — целочисленное деление даёт 0",
                TRIP_MAIN, TRIP.replace("fuel * 100 / distance", "fuel / distance * 100")),
               ("перепутал порядок аргументов: километры и литры поменялись местами",
                TRIP_MAIN.replace("new Trip(routes[i], distances[i], fuel[i])", "new Trip(routes[i], fuel[i], distances[i])"))],
        constructs=["class", "for"],
        checks=find_class("Trip")
               + need_field("Trip", "route", "String", "куда ехал водитель")
               + need_field("Trip", "km", "int", "сколько километров")
               + need_field("Trip", "liters", "int", "сколько литров бензина")
               + need_field("Trip", "per100", "int", "расход на 100 км")
               + need_constructor("Trip", TRIP_PARAMS, "он заполняет поля поездки при создании")
               + need_built(TRIP_PARAMS, '"Test", 200, 15', {"route": '"Test"', "km": "200", "liters": "15", "per100": "7"},
                            "Конструктор Trip должен сам заполнить поля route, km, liters и per100 — расход равен fuel * 100 / distance"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ctor-exam-stats", title="Итоги двух экзаменов",
        given=[("String", "subject1"), ("int[]", "scores1"), ("String", "subject2"), ("int[]", "scores2")],
        variants=[{"subject1": '"Math"', "scores1": "{70, 95, 81, 66}", "subject2": '"History"', "scores2": "{88, 74, 90}"},
                  {"subject1": '"Physics"', "scores1": "{55, 61, 90}", "subject2": '"Biology"', "scores2": "{72, 68, 70, 80, 65}"},
                  {"subject1": '"English"', "scores1": "{91, 87}", "subject2": '"Chemistry"', "scores2": "{60, 99, 75}"}],
        hidden=[{"subject1": '"Art"', "scores1": "{50}", "subject2": '"Music"', "scores2": "{40, 60}"},
                {"subject1": '"Drawing"', "scores1": "{100, 30, 80}", "subject2": '"Geography"', "scores2": "{77, 79}"},
                {"subject1": '"Literature"', "scores1": "{64, 70, 58, 92, 81, 77}", "subject2": '"Algebra"', "scores2": "{85}"},
                {"subject1": '"Economics"', "scores1": "{60, 61}", "subject2": '"Law"', "scores2": "{99, 20}"}],
        intro="Учитель сравнивает результаты двух экзаменов: `subject1` с баллами `scores1` и `subject2` с баллами "
              "`scores2`. Как только экзамен заносится в программу, по баллам сразу должны считаться лучший и средний "
              "балл — это работа для конструктора.",
        steps=["Ниже класса `Solution` создай класс `Exam` (без `public`) с полями `String subject`, `int best` и `int average`.",
               "Добавь конструктор `Exam(String subjectName, int[] scores)`. Он сохраняет предмет, а по массиву `scores` "
               "(в нём всегда есть хотя бы одно число) находит в цикле лучший балл и средний — сумму, делённую на количество, "
               "дробную часть отбрось.",
               "В `main` создай два объекта: `new Exam(subject1, scores1)` и `new Exam(subject2, scores2)`. Выведи для каждого "
               "строку вида `Math: best 95, average 78`.",
               "Третьей строкой выведи `Better: Math` с предметом, у которого средний балл выше, а если средние равны — `Equal`."],
        hint="Внутри конструктора можно писать любой код — циклы, условия, вспомогательные переменные. Сумму держи "
             "в обычной переменной, а результат запиши в поля `best` и `average` без указания типа.",
        solution=EXAM_MAIN,
        classes=EXAM,
        wrong=[("в конструкторе объявил новую переменную `int best` — поле best остаётся 0",
                EXAM_MAIN, EXAM.replace("        best = scores[0];", "        int best = scores[0];")),
               ("сравнивает экзамены по лучшему баллу, а не по среднему",
                EXAM_MAIN.replace("first.average > second.average", "first.best > second.best")
                         .replace("second.average > first.average", "second.best > first.best"))],
        constructs=["class", "for"],
        checks=find_class("Exam")
               + need_field("Exam", "subject", "String", "название предмета")
               + need_field("Exam", "best", "int", "лучший балл")
               + need_field("Exam", "average", "int", "средний балл")
               + need_constructor("Exam", EXAM_PARAMS, "он считает итоги экзамена при создании")
               + need_built(EXAM_PARAMS, '"Test", new int[]{60, 90, 70}', {"subject": '"Test"', "best": "90", "average": "73"},
                            "Конструктор Exam должен сам заполнить поля subject, best и average — лучший и средний балл по массиву"),
    ),
]
