"""Integrative tasks (the 3rd iteration of a topic), Java, topics 6–9: PRIMITIVE_TYPES, STRING_BASIC, INTEGER_DIVISION,
ASSIGNMENT_OPERATORS. Each family has the topic of its `skill` at the core and 1–2 earlier topics doing real work:
- PRIMITIVE_TYPES (double, char, an (int) cast) + arithmetic with parentheses, execution order, reassigning a field;
  not yet: String variables and methods, int / int and %, += ++, if/else, loops;
- STRING_BASIC (+, length, charAt, substring, indexOf, toUpperCase) + char / double and arithmetic; not yet: / and % on
  int, += ++, if/else, equals, loops;
- INTEGER_DIVISION (/ and %) + arithmetic, execution order, double, toUpperCase; not yet: += ++, if/else, loops;
- ASSIGNMENT_OPERATORS (+= -= *= %= ++) + / and %, saving a value before it changes; not yet: if/else, comparisons, loops.
Themes: post and delivery, health and the clinic, repair and construction, banking — the three stories of a topic are in
three different themes. One value set per family (the pool's rule), the hidden sets cover remainders of 0, a zero
amount and the other boundaries of each story."""
import textwrap

from java_tasks import JavaOutputTask


def code(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


def swap(text: str, old: str, new: str) -> str:
    assert old in text, old
    return text.replace(old, new)


# ───────── 6. PRIMITIVE_TYPES ─────────

BMI = code("""
    double bmi = weight / (height * height);
    int index = (int) bmi;
    System.out.println("Weight: " + weight + " kg, BMI: " + index);
    weight = weight - lost;
    bmi = weight / (height * height);
    index = (int) bmi;
    System.out.println("New weight: " + weight + " kg, BMI: " + index);
""")

EXCHANGE = code("""
    rubles = rubles - 150;
    int dollars = (int) (rubles / rate);
    double change = rubles - dollars * rate;
    System.out.println("For exchange: " + rubles + " rub");
    System.out.println("Dollars: " + dollars);
    System.out.println("Change: " + change + " rub");
""")

COURIER = code("""
    double bag = parcels * parcelWeight;
    System.out.println("Entrance " + entrance + ": bag " + bag + " kg");
    parcels = parcels - drop;
    entrance = (char) (entrance + 1);
    bag = parcels * parcelWeight;
    System.out.println("Entrance " + entrance + ": bag " + bag + " kg");
    int pay = (int) (drop * parcelWeight) * 40;
    System.out.println("Pay: " + pay + " rub");
""")

# ───────── 7. STRING_BASIC ─────────

SMS = code("""
    String hello = name.substring(0, 1).toUpperCase() + name.substring(1);
    String code = track.toUpperCase();
    String pin = code.substring(code.length() - 4);
    double storage = days * tariff;
    System.out.println(hello + ", parcel " + code + " is waiting");
    System.out.println("PIN: " + pin);
    System.out.println("Storage: " + storage + " rub");
""")

SCREEN = code("""
    int space = patient.indexOf(" ");
    String first = patient.substring(0, space).toUpperCase();
    char initial = patient.charAt(space + 1);
    String code = doctor.substring(0, 1).toUpperCase() + ticket;
    int wait = (ticket - current) * 15;
    System.out.println(code + ": " + first + " " + initial + ".");
    System.out.println("Wait: " + wait + " min");
""")

PLATE = code("""
    String plate = street.toUpperCase() + " " + house;
    int chars = plate.length();
    double width = (chars + 2) * 0.25;
    int cost = chars * 150 + 500;
    System.out.println("Plate: " + plate);
    System.out.println("Characters: " + chars);
    System.out.println("Width: " + width + " m");
    System.out.println("Cost: " + cost + " rub");
""")

# ───────── 8. INTEGER_DIVISION ─────────

TILES = code("""
    int perRow = length / tile;
    int side = length % tile;
    int rows = height / tile;
    int top = height % tile;
    int whole = perRow * rows;
    double cost = whole * price;
    System.out.println("Row: " + perRow + " tiles + " + side + " cm");
    System.out.println("Rows: " + rows + " + " + top + " cm");
    System.out.println("Whole tiles: " + whole + ", cost: " + cost + " rub");
""")

ROUTE = code("""
    int breaks = houses / 10;
    int total = houses * perHouse + breaks * 15;
    int hours = total / 60;
    int minutes = total % 60;
    System.out.println("Postman: " + postman.toUpperCase());
    System.out.println("Houses: " + houses + ", breaks: " + breaks);
    System.out.println("Route: " + hours + " h " + minutes + " min");
""")

KOPECKS = code("""
    int rub = balance / 100;
    int kop = balance % 100;
    System.out.println("Balance: " + rub + " rub " + kop + " kop");
    balance = balance - payment;
    rub = balance / 100;
    kop = balance % 100;
    System.out.println("After payment: " + rub + " rub " + kop + " kop");
    int points = payment / 10000;
    System.out.println("Points: " + points);
""")

# ───────── 9. ASSIGNMENT_OPERATORS ─────────

CASHBACK = code("""
    balance -= price;
    purchases++;
    bonus += price * 5 / 100;
    balance += bonus / 100 * 100;
    bonus %= 100;
    System.out.println("Balance: " + balance + " rub");
    System.out.println("Bonus: " + bonus);
    System.out.println("Purchases: " + purchases);
""")

NEWBORN = code("""
    int birth = grams;
    grams -= loss * 3;
    grams += gain * 4;
    int change = grams - birth;
    System.out.println("Birth: " + birth / 1000 + " kg " + birth % 1000 + " g");
    System.out.println("Day 7: " + grams / 1000 + " kg " + grams % 1000 + " g");
    System.out.println("Change: " + change + " g");
""")

ESTIMATE = code("""
    int cost = area * tilePrice;
    cost += cost / 10;
    cost += hours * 600;
    cost *= 2;
    budget -= cost;
    System.out.println("Cost: " + cost + " rub");
    System.out.println("Left: " + budget + " rub");
""")

TASKS = [
    # ── 6. PRIMITIVE_TYPES ──
    JavaOutputTask(
        skill="PRIMITIVE_TYPES", difficulty=3, slug="java-int-types-bmi", title="Индекс массы тела на приёме",
        given=[("double", "weight"), ("double", "height"), ("double", "lost")],
        variants=[{"weight": "92.5", "height": "1.8", "lost": "6.5"}],
        hidden=[{"weight": "70.0", "height": "1.75", "lost": "0.0"},
                {"weight": "120.0", "height": "2.0", "lost": "20.0"},
                {"weight": "100.5", "height": "1.9", "lost": "10.5"},
                {"weight": "55.5", "height": "1.6", "lost": "2.5"}],
        intro="Терапевт следит за весом пациента. Вес в килограммах записан в поле `weight`, рост в метрах — в поле "
              "`height`, а на сколько килограммов пациент похудел за месяц диеты — в поле `lost` (все три — дробные "
              "числа). Индекс массы тела — это вес, делённый на квадрат роста; в карточку пишут только его целую часть.",
        steps=["Заведи `double bmi` — индекс массы тела: `weight / (height * height)`. Заведи `int index` — его целую "
               "часть: приведи `bmi` к `int` через `(int)`.",
               "Выведи строку `Weight: … kg, BMI: …` — вес и целую часть индекса.",
               "Пациент похудел: уменьши `weight` на `lost` (`weight = weight - lost;`).",
               "Снова посчитай `bmi` и `index` — уже для нового веса — и выведи строку `New weight: … kg, BMI: …`."],
        hint="`(int)` отбрасывает дробную часть, не округляя: 28.9 станет 28. Индекс считается от того веса, который "
             "лежит в `weight` в этот момент, поэтому после изменения веса его нужно посчитать заново.",
        solution=BMI,
        wrong=[("нет скобок: weight / height * height — это снова вес, а не индекс",
                swap(BMI, "weight / (height * height)", "weight / height * height")),
               ("индекс не пересчитан после похудения: во второй строке старое значение",
                swap(BMI, "bmi = weight / (height * height);\nindex = (int) bmi;\nSystem.out.println(\"New",
                     "System.out.println(\"New")),
               ("выведен дробный индекс вместо его целой части", swap(BMI, "BMI: \" + index", "BMI: \" + bmi"))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill="PRIMITIVE_TYPES", difficulty=3, slug="java-int-types-exchange", title="Доллары в обменном пункте",
        given=[("int", "rubles"), ("double", "rate")],
        variants=[{"rubles": "5000", "rate": "92.5"}],
        hidden=[{"rubles": "9400", "rate": "92.5"},
                {"rubles": "200", "rate": "90.25"},
                {"rubles": "15000", "rate": "100.75"},
                {"rubles": "3000", "rate": "88.0"}],
        intro="Клиент меняет в банке рубли на доллары. Он принёс `rubles` рублей, курс — `rate` рублей за доллар "
              "(дробное число). Сначала банк берёт за обмен комиссию 150 рублей. На остальные деньги он выдаёт только "
              "целые доллары, а то, чего не хватило на целый доллар, возвращает рублями.",
        steps=["Отними комиссию от денег клиента: `rubles = rubles - 150;`.",
               "Заведи `int dollars` — сколько целых долларов выдаст банк: раздели `rubles` на `rate` и приведи "
               "результат к `int` через `(int)` (скобки вокруг всего деления).",
               "Заведи `double change` — сдачу в рублях: из `rubles` вычти стоимость выданных долларов (`dollars`, "
               "умноженное на `rate`).",
               "Выведи три строки: `For exchange: … rub` (деньги после комиссии), `Dollars: …`, `Change: … rub`."],
        hint="`(int) (rubles / rate)` сначала делит, а потом отбрасывает дробную часть: из 52.4 получится 52. "
             "Комиссия снимается до обмена, поэтому доллары считаются уже из уменьшенной суммы.",
        solution=EXCHANGE,
        wrong=[("комиссия снята после расчёта долларов: доллары посчитаны из всей суммы",
                swap(EXCHANGE, "rubles = rubles - 150;\nint dollars = (int) (rubles / rate);",
                     "int dollars = (int) (rubles / rate);\nrubles = rubles - 150;")),
               ("нет скобок в сдаче: (rubles - dollars) * rate вместо rubles - dollars * rate",
                swap(EXCHANGE, "rubles - dollars * rate", "(rubles - dollars) * rate")),
               ("сдача сохранена в int через (int): дробная часть теряется",
                swap(EXCHANGE, "double change = rubles - dollars * rate;", "int change = (int) (rubles - dollars * rate);"))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill="PRIMITIVE_TYPES", difficulty=3, slug="java-int-types-courier", title="Курьер в большом доме",
        given=[("char", "entrance"), ("int", "parcels"), ("int", "drop"), ("double", "parcelWeight")],
        variants=[{"entrance": "'C'", "parcels": "8", "drop": "3", "parcelWeight": "2.5"}],
        hidden=[{"entrance": "'A'", "parcels": "5", "drop": "0", "parcelWeight": "1.5"},
                {"entrance": "'K'", "parcels": "6", "drop": "6", "parcelWeight": "2.0"},
                {"entrance": "'X'", "parcels": "12", "drop": "5", "parcelWeight": "0.75"},
                {"entrance": "'F'", "parcels": "9", "drop": "4", "parcelWeight": "3.25"}],
        intro="Курьер разносит посылки по большому дому; подъезды в нём обозначены буквами по порядку: A, B, C… Курьер "
              "стоит у подъезда `entrance` (поле типа `char`), в сумке у него `parcels` одинаковых посылок, каждая "
              "весит `parcelWeight` кг (дробное число). В этом подъезде он отдаёт `drop` посылок. За работу ему платят "
              "40 рублей за каждый полный килограмм отданных посылок.",
        steps=["Заведи `double bag` — вес сумки: `parcels` умножить на `parcelWeight`. Выведи строку "
               "`Entrance …: bag … kg` — букву подъезда и вес сумки.",
               "Курьер отдал посылки: уменьши `parcels` на `drop`. Потом он идёт к следующей букве: "
               "`entrance = (char) (entrance + 1);`.",
               "Снова посчитай `bag` и выведи такую же строку — уже для нового подъезда.",
               "Заведи `int pay` — сколько заработал курьер: вес отданных посылок (`drop * parcelWeight`) приведи "
               "к `int` и умножь на 40. Выведи `Pay: … rub`."],
        hint="`entrance + 1` — это уже число (код буквы), а `(char)` превращает его обратно в букву: из `C` получится "
             "`D`. Приведение `(int)` бери в скобки вместе с произведением: `(int) 7.5` — это 7.",
        solution=COURIER,
        wrong=[("без приведения (char): вместо буквы подъезда печатается её код",
                swap(COURIER, "entrance = (char) (entrance + 1);\nbag = parcels * parcelWeight;\n"
                              "System.out.println(\"Entrance \" + entrance",
                     "bag = parcels * parcelWeight;\nSystem.out.println(\"Entrance \" + (entrance + 1)")),
               ("вес сумки не пересчитан после того, как курьер отдал посылки",
                swap(COURIER, "entrance = (char) (entrance + 1);\nbag = parcels * parcelWeight;",
                     "entrance = (char) (entrance + 1);")),
               ("(int) применён ко всей сумме: дробные килограммы тоже оплачены",
                swap(COURIER, "(int) (drop * parcelWeight) * 40", "(int) (drop * parcelWeight * 40)"))],
        constructs=["assignment"],
    ),

    # ── 7. STRING_BASIC ──
    JavaOutputTask(
        skill="STRING_BASIC", difficulty=3, slug="java-int-str-sms", title="СМС о посылке в постамате",
        given=[("String", "name"), ("String", "track"), ("int", "days"), ("double", "tariff")],
        variants=[{"name": '"anna"', "track": '"ra644000115ru"', "days": "3", "tariff": "12.5"}],
        hidden=[{"name": '"boris"', "track": '"cp123456789cn"', "days": "0", "tariff": "15.0"},
                {"name": '"li"', "track": '"80085592123456"', "days": "5", "tariff": "10.5"},
                {"name": '"olga"', "track": '"ea100200300ru"', "days": "7", "tariff": "12.5"},
                {"name": '"timur"', "track": '"1401234567"', "days": "1", "tariff": "20.0"}],
        intro="Посылка пришла в постамат, и почта отправляет получателю СМС. Имя получателя записано в поле `name`, "
              "трек-номер посылки — в поле `track`; оператор ввёл их маленькими буквами. Трек-номера бывают разной "
              "длины. Посылка лежит в постамате `days` дней, день хранения стоит `tariff` рублей (дробное число).",
        steps=["Заведи строку `hello` — имя с большой буквы: первая буква (`name.substring(0, 1)`) большими буквами "
               "и остальная часть имени (`name.substring(1)`) — например `Anna`.",
               "Заведи строку `code` — трек-номер большими буквами.",
               "Заведи строку `pin` — код ячейки: последние четыре символа `code`. С какого символа начинать, узнай "
               "через `code.length()`.",
               "Заведи `double storage` — плату за хранение: `days` умножить на `tariff`.",
               "Выведи три строки: `…, parcel … is waiting` (имя и трек-номер), `PIN: …`, `Storage: … rub`."],
        hint="`s.substring(a)` берёт символы от номера `a` до конца строки. У строки из 13 символов последние четыре "
             "начинаются с номера 9 — это `length() - 4`, и так для строки любой длины.",
        solution=SMS,
        wrong=[("код ячейки — только три символа: конец substring не включается",
                swap(SMS, "code.substring(code.length() - 4)", "code.substring(code.length() - 4, code.length() - 1)")),
               ("код ячейки взят с номера 9: для трек-номера другой длины это не последние четыре символа",
                swap(SMS, "code.substring(code.length() - 4)", "code.substring(9)")),
               ("имя целиком большими буквами", swap(SMS, "name.substring(0, 1).toUpperCase() + name.substring(1)",
                                                     "name.toUpperCase()"))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill="STRING_BASIC", difficulty=3, slug="java-int-str-screen", title="Табло очереди в поликлинике",
        given=[("String", "patient"), ("String", "doctor"), ("int", "ticket"), ("int", "current")],
        variants=[{"patient": '"Anna Petrova"', "doctor": '"surgeon"', "ticket": "17", "current": "14"}],
        hidden=[{"patient": '"Li Wu"', "doctor": '"dentist"', "ticket": "5", "current": "4"},
                {"patient": '"Konstantin Ivanov"', "doctor": '"therapist"', "ticket": "30", "current": "30"},
                {"patient": '"Maria Sokolova"', "doctor": '"neurologist"', "ticket": "102", "current": "95"},
                {"patient": '"Oleg Kim"', "doctor": '"oculist"', "ticket": "9", "current": "1"}],
        intro="Над кабинетами поликлиники висит табло очереди. Чтобы не показывать всем полное имя, табло пишет имя "
              "пациента большими буквами и только первую букву фамилии. Имя и фамилия пациента через один пробел "
              "записаны в поле `patient`, врач — в поле `doctor` (маленькими буквами), номер талона пациента — в поле "
              "`ticket`, номер талона того, кто сейчас в кабинете, — в поле `current`. Один приём длится 15 минут.",
        steps=["Заведи `int space` — номер пробела в `patient` (метод `indexOf`).",
               "Заведи строку `first` — имя (всё, что до пробела) большими буквами, и `char initial` — первую букву "
               "фамилии: символ сразу после пробела (`charAt`).",
               "Заведи строку `code` — код талона: первая буква врача большими буквами и номер талона, например `S17`.",
               "Заведи `int wait` — сколько минут ждать: разность `ticket` и `current`, умноженная на 15.",
               "Выведи две строки. Первая — код, двоеточие, пробел, имя, пробел, буква фамилии и точка, как `S17: ANNA P.`; "
               "вторая — `Wait: … min`."],
        hint="Символы считаются с нуля, а сам `space` — это пробел, поэтому первая буква фамилии — "
             "`charAt(space + 1)`. Разность возьми в скобки: умножение выполняется раньше вычитания.",
        solution=SCREEN,
        wrong=[("charAt(space): вместо буквы фамилии берётся пробел",
                swap(SCREEN, "patient.charAt(space + 1)", "patient.charAt(space)")),
               ("имя взято вместе с пробелом: конец substring сдвинут на один",
                swap(SCREEN, "patient.substring(0, space)", "patient.substring(0, space + 1)")),
               ("нет скобок: на 15 умножается только current", swap(SCREEN, "(ticket - current) * 15",
                                                                     "ticket - current * 15"))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill="STRING_BASIC", difficulty=3, slug="java-int-str-plate", title="Табличка на новый дом",
        given=[("String", "street"), ("int", "house")],
        variants=[{"street": '"Sadovaya"', "house": "17"}],
        hidden=[{"street": '"Mira"', "house": "5"},
                {"street": '"Lugovaya"', "house": "120"},
                {"street": '"Pervomayskaya"', "house": "1"},
                {"street": '"Tikhaya"', "house": "9"}],
        intro="Строители сдают новый дом и заказывают на фасад табличку с адресом: название улицы большими буквами, "
              "пробел и номер дома. Улица (одно слово) записана в поле `street`, номер дома — в поле `house`. Каждый "
              "символ таблички — буква, цифра или пробел — занимает 0.25 м, и по краям оставляют ещё по одному пустому "
              "месту такой же ширины. Изготовление стоит 150 рублей за символ и ещё 500 рублей за установку.",
        steps=["Заведи строку `plate`: улица большими буквами, пробел и номер дома.",
               "Заведи `int chars` — сколько символов в `plate` (метод `length()`). Цифры номера дома, приклеенного "
               "к строке, — тоже символы.",
               "Заведи `double width` — ширину таблички в метрах: число символов плюс 2 пустых места, умноженное "
               "на `0.25`.",
               "Заведи `int cost` — цену таблички: `chars` умножить на 150 и прибавить 500.",
               "Выведи четыре строки: `Plate: …`, `Characters: …`, `Width: … m`, `Cost: … rub`."],
        hint="Число, приклеенное к строке через `+`, становится текстом: `\"A \" + 17` — это строка `A 17` из четырёх "
             "символов. Сумму в ширине возьми в скобки, иначе 2 сначала умножится на 0.25.",
        solution=PLATE,
        wrong=[("посчитана длина одной улицы: пробел и цифры номера не учтены",
                swap(PLATE, "int chars = plate.length();", "int chars = street.length();")),
               ("нет скобок: к числу символов прибавлено 2 * 0.25", swap(PLATE, "(chars + 2) * 0.25", "chars + 2 * 0.25")),
               ("нет пробела между улицей и номером дома",
                swap(PLATE, "street.toUpperCase() + \" \" + house", "street.toUpperCase() + house"))],
        constructs=["assignment"],
    ),

    # ── 8. INTEGER_DIVISION ──
    JavaOutputTask(
        skill="INTEGER_DIVISION", difficulty=3, slug="java-int-div-tiles", title="Плитка на стену в ванной",
        given=[("int", "length"), ("int", "height"), ("int", "tile"), ("double", "price")],
        variants=[{"length": "250", "height": "276", "tile": "30", "price": "45.5"}],
        hidden=[{"length": "300", "height": "240", "tile": "30", "price": "50.0"},
                {"length": "185", "height": "250", "tile": "20", "price": "62.5"},
                {"length": "120", "height": "200", "tile": "25", "price": "38.25"},
                {"length": "275", "height": "260", "tile": "40", "price": "99.75"}],
        intro="Плиточник облицовывает стену в ванной квадратной плиткой. Длина стены в сантиметрах записана в поле "
              "`length`, высота — в поле `height`, сторона плитки — в поле `tile`, цена одной плитки в рублях — в "
              "дробном поле `price`. Целые плитки кладут рядами от угла; у края каждого ряда и под потолком остаются "
              "узкие полоски — их потом закроют обрезками.",
        steps=["Заведи `int perRow` — сколько целых плиток помещается в один ряд по длине стены, и `int side` — "
               "ширину полоски у края ряда в сантиметрах (то, что остаётся от деления).",
               "Так же по высоте стены: `int rows` — число полных рядов и `int top` — высоту полоски под потолком.",
               "Заведи `int whole` — сколько всего целых плиток (`perRow` умножить на `rows`), и `double cost` — их "
               "стоимость (`whole` умножить на `price`).",
               "Выведи три строки: `Row: … tiles + … cm`, `Rows: … + … cm`, `Whole tiles: …, cost: … rub`."],
        hint="`250 / 30` — это 8: деление целых чисел отбрасывает дробную часть, а `250 % 30` — это 10, остаток. "
             "Если плитка укладывается ровно, остаток равен 0.",
        solution=TILES,
        wrong=[("перепутаны / и %: плиток в ряду столько, сколько сантиметров в полоске",
                swap(TILES, "int perRow = length / tile;\nint side = length % tile;",
                     "int perRow = length % tile;\nint side = length / tile;")),
               ("ряды посчитаны по длине стены, а не по высоте", swap(TILES, "int rows = height / tile;",
                                                                      "int rows = length / tile;")),
               ("цена плитки обрезана через (int): копейки потеряны", swap(TILES, "whole * price", "whole * (int) price"))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill="INTEGER_DIVISION", difficulty=3, slug="java-int-div-route", title="Маршрут почтальона",
        given=[("String", "postman"), ("int", "houses"), ("int", "perHouse")],
        variants=[{"postman": '"Boris"', "houses": "23", "perHouse": "11"}],
        hidden=[{"postman": '"Anna"', "houses": "9", "perHouse": "6"},
                {"postman": '"Gleb"', "houses": "10", "perHouse": "12"},
                {"postman": '"Vera"', "houses": "30", "perHouse": "7"},
                {"postman": '"Ilya"', "houses": "45", "perHouse": "4"}],
        intro="Почтальон разносит письма по своему участку. Его имя записано в поле `postman`, сколько домов на "
              "маршруте — в поле `houses`, сколько минут он тратит на один дом — в поле `perHouse`. После каждых "
              "полных 10 домов он отдыхает 15 минут.",
        steps=["Заведи `int breaks` — число перерывов: сколько полных десятков в `houses`.",
               "Заведи `int total` — время всего маршрута в минутах: время на все дома плюс 15 минут на каждый перерыв.",
               "Разложи `total` на полные часы `int hours` и оставшиеся минуты `int minutes`.",
               "Выведи три строки: `Postman: …` (имя большими буквами), `Houses: …, breaks: …`, `Route: … h … min`."],
        hint="Полные десятки — это целое деление на 10: из 23 домов получается 2. В часе 60 минут: `total / 60` — "
             "полные часы, `total % 60` — минуты сверх них.",
        solution=ROUTE,
        wrong=[("перерывы через %: получается последняя цифра числа домов",
                swap(ROUTE, "int breaks = houses / 10;", "int breaks = houses % 10;")),
               ("часы и минуты перепутаны", swap(ROUTE, "int hours = total / 60;\nint minutes = total % 60;",
                                                 "int hours = total % 60;\nint minutes = total / 60;")),
               ("в часе 100 минут: деление на 100 вместо 60",
                swap(ROUTE, "int hours = total / 60;\nint minutes = total % 60;",
                     "int hours = total / 100;\nint minutes = total % 100;"))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill="INTEGER_DIVISION", difficulty=3, slug="java-int-div-kopecks", title="Баланс в копейках",
        given=[("int", "balance"), ("int", "payment")],
        variants=[{"balance": "258075", "payment": "124550"}],
        hidden=[{"balance": "100000", "payment": "100000"},
                {"balance": "50005", "payment": "9999"},
                {"balance": "1234567", "payment": "10000"},
                {"balance": "30099", "payment": "30000"}],
        intro="Банк хранит деньги на счёте в копейках — целым числом, чтобы не ошибаться с дробями. На счёте клиента "
              "`balance` копеек, он оплачивает покупку на `payment` копеек (денег хватает). В приложении сумму "
              "показывают в рублях и копейках, а за каждые полные 100 рублей покупки банк начисляет 1 бонусный балл.",
        steps=["Заведи `int rub` и `int kop` — сколько полных рублей в `balance` и сколько копеек сверх них (в рубле "
               "100 копеек). Выведи `Balance: … rub … kop`.",
               "Спиши покупку со счёта: `balance = balance - payment;`.",
               "Снова посчитай `rub` и `kop` — уже для нового `balance` — и выведи `After payment: … rub … kop`.",
               "Заведи `int points` — бонусные баллы: сколько полных 100 рублей в покупке (100 рублей — это 10000 "
               "копеек). Выведи `Points: …`."],
        hint="`258075 / 100` — это 2580 рублей, а `258075 % 100` — 75 копеек. Переменные `rub` и `kop` сами не "
             "меняются, когда меняется `balance`: их нужно посчитать заново.",
        solution=KOPECKS,
        wrong=[("рубли и копейки не пересчитаны после оплаты: во второй строке старый баланс",
                swap(KOPECKS, "\nrub = balance / 100;\nkop = balance % 100;", "")),
               ("баллы за каждый рубль, а не за каждые 100 рублей",
                swap(KOPECKS, "payment / 10000", "payment / 100")),
               ("рубли и копейки перепутаны: / и % местами",
                swap(swap(KOPECKS, "rub = balance / 100;", "rub = balance % 100;"), "kop = balance % 100;",
                     "kop = balance / 100;"))],
        constructs=["assignment"],
    ),

    # ── 9. ASSIGNMENT_OPERATORS ──
    JavaOutputTask(
        skill="ASSIGNMENT_OPERATORS", difficulty=3, slug="java-int-aug-cashback", title="Кешбэк по карте",
        given=[("int", "balance"), ("int", "bonus"), ("int", "purchases"), ("int", "price")],
        variants=[{"balance": "3200", "bonus": "80", "purchases": "12", "price": "1990"}],
        hidden=[{"balance": "5000", "bonus": "10", "purchases": "0", "price": "1000"},
                {"balance": "2000", "bonus": "95", "purchases": "7", "price": "100"},
                {"balance": "10000", "bonus": "99", "purchases": "30", "price": "19"},
                {"balance": "8000", "bonus": "70", "purchases": "3", "price": "2690"}],
        intro="У клиента на банковской карте `balance` рублей, накоплено `bonus` бонусов, а в этом месяце он сделал "
              "уже `purchases` покупок. Сейчас он покупает товар за `price` рублей. Банк возвращает 5 процентов "
              "покупки бонусами (дробная часть отбрасывается), а каждые полные 100 бонусов переводит на карту "
              "как 100 рублей.",
        steps=["Спиши покупку с карты операцией `-=` и увеличь `purchases` на 1 операцией `++`.",
               "Прибавь к `bonus` кешбэк `price * 5 / 100` операцией `+=`.",
               "Переведи полные сотни бонусов в рубли: прибавь к `balance` `bonus / 100 * 100` операцией `+=`, "
               "а потом оставь в `bonus` только остаток от деления на 100 операцией `%=`.",
               "Выведи три строки: `Balance: … rub`, `Bonus: …`, `Purchases: …`."],
        hint="Порядок важен: если сначала выполнить `bonus %= 100;`, сотен в `bonus` уже не останется. И умножай до "
             "деления: в `price / 100 * 5` целое деление съест часть кешбэка.",
        solution=CASHBACK,
        wrong=[("сначала %=, потом перевод: сотни бонусов пропадают, а не переходят на карту",
                swap(CASHBACK, "balance += bonus / 100 * 100;\nbonus %= 100;",
                     "bonus %= 100;\nbalance += bonus / 100 * 100;")),
               ("/= вместо %=: в bonus остаётся число сотен, а не остаток",
                swap(CASHBACK, "bonus %= 100;", "bonus /= 100;")),
               ("кешбэк price / 100 * 5: целое деление до умножения теряет часть бонусов",
                swap(CASHBACK, "price * 5 / 100", "price / 100 * 5"))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill="ASSIGNMENT_OPERATORS", difficulty=3, slug="java-int-aug-newborn", title="Вес малыша в роддоме",
        given=[("int", "grams"), ("int", "loss"), ("int", "gain")],
        variants=[{"grams": "3350", "loss": "60", "gain": "75"}],
        hidden=[{"grams": "3000", "loss": "40", "gain": "30"},
                {"grams": "2950", "loss": "50", "gain": "25"},
                {"grams": "4020", "loss": "70", "gain": "90"},
                {"grams": "3480", "loss": "0", "gain": "60"}],
        intro="В роддоме малыша взвешивают каждый день. При рождении он весил `grams` граммов. Первые 3 дня "
              "новорождённые немного худеют — этот малыш терял по `loss` граммов в день, — а следующие 4 дня он "
              "прибавлял по `gain` граммов в день. В карточку вес пишут в килограммах и граммах.",
        steps=["Запомни вес при рождении: `int birth = grams;` — дальше `grams` будет меняться.",
               "Отними от `grams` потерю за первые 3 дня (`loss * 3`) операцией `-=`, затем прибавь то, что он "
               "набрал за следующие 4 дня (`gain * 4`), операцией `+=`.",
               "Заведи `int change` — на сколько граммов изменился вес за неделю: `grams` минус `birth`.",
               "Выведи три строки: `Birth: … kg … g` (вес при рождении), `Day 7: … kg … g` (вес сейчас), "
               "`Change: … g`. Килограммы — это `/ 1000`, граммы сверх них — `% 1000`."],
        hint="`grams -= loss * 3;` — то же, что `grams = grams - loss * 3;`. Не перепутай с `=-`: `grams =- 180;` "
             "просто запишет в `grams` число -180. Вес при рождении сохрани до того, как `grams` изменится.",
        solution=NEWBORN,
        wrong=[("вес при рождении сохранён после изменений: в birth уже вес седьмого дня",
                swap(NEWBORN, "int birth = grams;\ngrams -= loss * 3;\ngrams += gain * 4;",
                     "grams -= loss * 3;\ngrams += gain * 4;\nint birth = grams;")),
               ("=- вместо -=: в grams записывается отрицательная потеря",
                swap(NEWBORN, "grams -= loss * 3;", "grams =- loss * 3;")),
               ("килограммы через / 100 и % 100", swap(swap(NEWBORN, "/ 1000", "/ 100"), "% 1000", "% 100"))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill="ASSIGNMENT_OPERATORS", difficulty=3, slug="java-int-aug-estimate", title="Смета на ремонт двух санузлов",
        given=[("int", "budget"), ("int", "area"), ("int", "tilePrice"), ("int", "hours")],
        variants=[{"budget": "60000", "area": "6", "tilePrice": "1450", "hours": "8"}],
        hidden=[{"budget": "40000", "area": "5", "tilePrice": "1255", "hours": "0"},
                {"budget": "30000", "area": "4", "tilePrice": "1000", "hours": "5"},
                {"budget": "25000", "area": "7", "tilePrice": "999", "hours": "3"},
                {"budget": "15800", "area": "5", "tilePrice": "1000", "hours": "4"}],
        intro="Бригада делает ремонт в квартире, где два одинаковых санузла. На один санузел нужно `area` квадратных "
              "метров плитки по `tilePrice` рублей за метр; плитку берут с запасом в десятую часть (считают в целых "
              "рублях, дробная часть отбрасывается). В каждом санузле мастер работает `hours` часов по 600 рублей. "
              "Хозяин выделил на весь ремонт `budget` рублей.",
        steps=["Заведи `int cost` — стоимость плитки для одного санузла: `area` умножить на `tilePrice`.",
               "Прибавь к `cost` запас — десятую часть самой `cost` (`cost / 10`) — операцией `+=`. Потом так же "
               "операцией `+=` прибавь работу мастера (`hours * 600`).",
               "Санузлов два: удвой `cost` операцией `*=`.",
               "Отними `cost` от `budget` операцией `-=`.",
               "Выведи две строки: `Cost: … rub` и `Left: … rub` (что осталось от бюджета)."],
        hint="`cost += cost / 10;` сначала считает правую часть по старому `cost`, а потом прибавляет: из 8700 "
             "получится 9570. Удваивай, когда в `cost` уже есть и плитка, и работа.",
        solution=ESTIMATE,
        wrong=[("запас прибавлен как 10 рублей, а не как десятая часть стоимости",
                swap(ESTIMATE, "cost += cost / 10;", "cost += 10;")),
               ("=+ вместо +=: стоимость плитки затёрта стоимостью работы",
                swap(ESTIMATE, "cost += hours * 600;", "cost =+ hours * 600;")),
               ("удвоено до работы мастера: работа посчитана только за один санузел",
                swap(ESTIMATE, "cost += hours * 600;\ncost *= 2;", "cost *= 2;\ncost += hours * 600;"))],
        constructs=["augmented_assignment"],
    ),
]
