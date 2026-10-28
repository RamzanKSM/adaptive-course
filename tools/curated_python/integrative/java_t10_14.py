"""Integrative tasks (the task of a topic's 3rd iteration), Java, topics 10–14: IF_ELSE_BASIC «Условия if / else»,
COMPARISON_OPERATORS «Операторы сравнения», LOGICAL_AND «Логическое И (&&)», LOGICAL_OR «Логическое ИЛИ (||)» (and !),
SWITCH_BASIC «Оператор switch». Each family: the topic at the core plus 1–2 earlier topics doing real work, one value
set, about 4–5 minutes; hidden value sets hit every branch and boundary.

IF_ELSE_BASIC (one if/else, a comparison in the condition) is joined by / and % (a calf's age in weeks), % and +=
(round-up savings of a bank card), String length/substring/toUpperCase (a film title on a ticket). Not yet: else if,
&& || !, switch.
COMPARISON_OPERATORS (== != < > <= >=, an if / else if / else chain, an if inside else) is joined by += -= and the
order of statements (visitors in a museum hall), / (egg size by the average weight), / % and ++ (months of saving).
Not yet: && || !, switch.
LOGICAL_AND (one condition of 2–3 parts joined with &&) is joined by arithmetic and / (a family ticket to a theatre),
double division (a museum guide's bonus), arithmetic with / and % (shearing sheep). Not yet: || and !, switch.
LOGICAL_OR (|| and !) is joined by / and % (a night card payment), *= += and their order (cinema club points),
/ for a percent and an average (a batch of apples). Not yet: switch.
SWITCH_BASIC (case with break, two labels for one branch, default) is joined by / and % (an audio guide number),
charAt/toUpperCase and -= (a cinema promo code), double with an (int) cast and / (currency exchange).
Not yet (all): loops, arrays, own methods and classes, equals on strings (strings are compared only in switch).

Theme domains: garden and farm; savings and bank cards; cinema and theatre; museums."""
import textwrap

from java_tasks import JavaOutputTask
from topics_java.t22_switch import SWITCH_CHECK, uses_switch


def code(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


def swap(text: str, old: str, new: str) -> str:
    assert old in text, old
    return text.replace(old, new)


def switch_on(what: str) -> str:
    return SWITCH_CHECK % (f"Используй оператор switch по {what}: выбор одного варианта из многих "
                           f"по значению так читается проще, чем цепочка if")


# ───────── IF_ELSE_BASIC ─────────

CALF = code("""
    System.out.println("Age: " + days / 7 + " weeks " + days % 7 + " days");
    if (days >= 60) {
        System.out.println("Move to the herd");
    } else {
        System.out.println("Days left: " + (60 - days));
        System.out.println("Milk needed: " + (60 - days) * 6 + " l");
    }
""")

ROUNDUP = code("""
    int rest = price % 100;
    int toSavings;
    if (rest == 0) {
        toSavings = 0;
    } else {
        toSavings = 100 - rest;
    }
    savings += toSavings;
    System.out.println("Charged: " + (price + toSavings) + " rub");
    System.out.println("To savings: " + toSavings + " rub");
    System.out.println("Savings: " + savings + " rub");
""")

TICKET = code("""
    String name = film.toUpperCase();
    if (name.length() > 12) {
        System.out.println("Film: " + name.substring(0, 12) + "...");
    } else {
        System.out.println("Film: " + name);
    }
    System.out.println("Row " + row + ", seat " + seat);
""")

# ───────── COMPARISON_OPERATORS ─────────

HALL = code("""
    inside += came;
    System.out.println("After the tour came in: " + inside);
    inside -= left;
    System.out.println("Now: " + inside);
    if (inside > 60) {
        System.out.println("Too many: " + (inside - 60) + " over the limit");
    } else if (inside == 60) {
        System.out.println("The hall is full");
    } else {
        System.out.println("Free places: " + (60 - inside));
    }
""")

EGGS = code("""
    int average = grams / eggs;
    System.out.println("Average: " + average + " g");
    String size;
    if (average < 45) {
        size = "S";
    } else if (average < 55) {
        size = "M";
    } else if (average < 65) {
        size = "L";
    } else {
        size = "XL";
    }
    System.out.println("Size: " + size);
""")

SAVINGS = code("""
    if (saved >= goal) {
        System.out.println("Goal reached");
    } else {
        int left = goal - saved;
        System.out.println("Left: " + left + " rub");
        int months = left / monthly;
        if (left % monthly != 0) {
            months++;
        }
        System.out.println("Months: " + months);
    }
""")

# ───────── LOGICAL_AND ─────────

FAMILY = code("""
    int total = adults * 450 + kids * 250;
    if (adults == 2 && kids >= 2 && kids <= 3) {
        System.out.println("Family ticket");
        total = 1300;
    } else {
        System.out.println("Separate tickets");
    }
    System.out.println("Total: " + total + " rub");
    System.out.println("Per person: " + total / (adults + kids) + " rub");
""")

GUIDE = code("""
    double average = points;
    average = average / reviews;
    System.out.println("Reviews: " + reviews + ", average: " + average);
    if (reviews >= 20 && average >= 4.5) {
        System.out.println("Bonus: 5000 rub");
    } else {
        System.out.println("No bonus yet");
    }
""")

SHEEP = code("""
    int wool = months * 12;
    System.out.println("Wool: " + wool / 10 + " cm " + wool % 10 + " mm");
    if (wool >= 60 && currentMonth >= 5 && currentMonth <= 6) {
        System.out.println("Time to shear");
    } else {
        System.out.println("Not now");
    }
""")

# ───────── LOGICAL_OR ─────────

PAYMENT = code("""
    int hour = time / 100;
    int minute = time % 100;
    System.out.println("Payment: " + amount + " rub at " + hour + " h " + minute + " min");
    if (!trusted || amount >= 15000 || hour < 6) {
        System.out.println("Confirm by SMS");
    } else {
        System.out.println("Approved");
    }
""")

BONUS = code("""
    int bonus = tickets * 50;
    if (day == 1 || birthday) {
        bonus *= 2;
    }
    points += bonus;
    System.out.println("Bonus: " + bonus + " points");
    System.out.println("Card: " + points + " points");
""")

APPLES = code("""
    int percent = bruised * 100 / apples;
    int average = grams / apples;
    System.out.println("Bruised: " + percent + "%");
    System.out.println("Average: " + average + " g");
    if (percent > 5 || average < 150) {
        System.out.println("Batch returned");
    } else {
        System.out.println("Batch accepted");
    }
""")

# ───────── SWITCH_BASIC ─────────

AUDIOGUIDE = code("""
    int floor = number / 100;
    int exhibit = number % 100;
    switch (floor) {
        case 1:
            System.out.println("Floor 1: Ancient world");
            break;
        case 2:
            System.out.println("Floor 2: Middle Ages");
            break;
        case 3:
        case 4:
            System.out.println("Floor " + floor + ": Modern art");
            break;
        default:
            System.out.println("Floor " + floor + ": no exhibition");
    }
    System.out.println("Exhibit: " + exhibit);
""")

PROMO = code("""
    char letter = promo.toUpperCase().charAt(0);
    int discount = 0;
    switch (letter) {
        case 'S':
            discount = 100;
            break;
        case 'K':
        case 'C':
            discount = 150;
            break;
        case 'B':
            discount = price;
            break;
        default:
            discount = 0;
    }
    price -= discount;
    System.out.println("Code: " + letter);
    System.out.println("Discount: " + discount + " rub");
    System.out.println("To pay: " + price + " rub");
""")

CURRENCY = code("""
    double rate = 0;
    switch (currency) {
        case "USD":
            rate = 90.5;
            break;
        case "EUR":
            rate = 98.25;
            break;
        case "CNY":
            rate = 12.4;
            break;
        default:
            rate = 0;
    }
    if (rate == 0) {
        System.out.println("Unknown currency");
    } else {
        int rub = (int) (amount * rate);
        System.out.println(amount + " " + currency + " = " + rub + " rub");
        System.out.println("You get: " + (rub - rub / 100) + " rub");
    }
""")

TASKS = [
    # ───── IF_ELSE_BASIC ─────
    JavaOutputTask(
        skill="IF_ELSE_BASIC", difficulty=3, slug="java-int-if-calf", title="Телёнок и общее стадо",
        given=[("int", "days")],
        variants=[{"days": "45"}],
        hidden=[{"days": "60"}, {"days": "59"}, {"days": "0"}, {"days": "90"}, {"days": "14"}],
        intro="На ферме телёнка первые 60 дней держат отдельно от стада и поят молоком — по 6 л в день, а потом "
              "переводят в общий коровник. Сколько дней телёнку, записано в поле `days`.",
        steps=["Выведи возраст телёнка в полных неделях и оставшихся днях: `Age: … weeks … days` "
               "(недели — `days / 7`, дни — `days % 7`).",
               "Если телёнку 60 дней или больше, выведи `Move to the herd`.",
               "Иначе выведи две строки: `Days left: …` — сколько дней осталось до 60, и `Milk needed: … l` — "
               "сколько молока телёнок выпьет за эти дни."],
        hint="Телёнка ровно 60 дней уже переводят. Дней до перевода — `60 - days`; в строке возьми это выражение "
             "в скобки, чтобы Java вычла числа, а не склеила их с текстом.",
        solution=CALF,
        wrong=[("> вместо >=: телёнка ровно 60 дней ещё не переводят",
                swap(CALF, "days >= 60", "days > 60")),
               ("недели и дни перепутаны: / и % поменяны местами",
                swap(CALF, '"Age: " + days / 7 + " weeks " + days % 7', '"Age: " + days % 7 + " weeks " + days / 7')),
               ("молоко посчитано за прожитые дни, а не за оставшиеся",
                swap(CALF, "(60 - days) * 6", "days * 6"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill="IF_ELSE_BASIC", difficulty=3, slug="java-int-if-roundup", title="Копилка с округлением",
        given=[("int", "price"), ("int", "savings")],
        variants=[{"price": "437", "savings": "1250"}],
        hidden=[{"price": "400", "savings": "1000"}, {"price": "401", "savings": "0"}, {"price": "99", "savings": "20"},
                {"price": "1999", "savings": "5"}, {"price": "50", "savings": "50"}],
        intro="К банковской карте подключена копилка с округлением: каждая покупка округляется вверх до целых сотен "
              "рублей, и разница уходит в копилку. Цена покупки записана в поле `price`, сколько уже лежит в копилке — "
              "в поле `savings`.",
        steps=["Найди остаток от деления цены на 100: `price % 100`.",
               "Если остаток равен 0, в копилку уходит 0 руб. Иначе в копилку уходит 100 минус остаток.",
               "Прибавь эту сумму к `savings` через `+=`.",
               "Выведи три строки: `Charged: … rub` (цена плюс сумма для копилки), `To savings: … rub` и "
               "`Savings: … rub`."],
        hint="Покупка за 400 руб. уже круглая — в копилку уходит 0 руб., а не 100. Заведи переменную для суммы "
             "в копилку до `if`, а в ветках только присвой ей значение.",
        solution=ROUNDUP,
        wrong=[("без проверки на круглую цену: за 400 руб. в копилку уходит 100",
                swap(ROUNDUP, "if (rest == 0) {\n    toSavings = 0;\n} else {\n    toSavings = 100 - rest;\n}",
                     "toSavings = 100 - rest;")),
               ("price / 100 вместо price % 100: берёт число сотен, а не остаток",
                swap(ROUNDUP, "int rest = price % 100;", "int rest = price / 100;")),
               ("сумма без скобок: цена и округление склеиваются в строку",
                swap(ROUNDUP, '"Charged: " + (price + toSavings)', '"Charged: " + price + toSavings'))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill="IF_ELSE_BASIC", difficulty=3, slug="java-int-if-ticket", title="Название фильма на билете",
        given=[("String", "film"), ("int", "row"), ("int", "seat")],
        variants=[{"film": '"The Snow Queen"', "row": "7", "seat": "12"}],
        hidden=[{"film": '"Ocean Dreams"', "row": "3", "seat": "8"},
                {"film": '"Mountain Song"', "row": "10", "seat": "1"},
                {"film": '"Up"', "row": "1", "seat": "15"},
                {"film": '"Space Cats"', "row": "5", "seat": "5"},
                {"film": '"Return of the Red Fox"', "row": "12", "seat": "20"}],
        intro="Касса кинотеатра печатает билет. Название фильма на нём пишут большими буквами, и помещается только "
              "12 символов названия. Название записано в поле `film`, ряд и место — в полях `row` и `seat`.",
        steps=["Переведи название в большие буквы: `film.toUpperCase()`.",
               "Если в названии больше 12 символов (`length()`), оставь первые 12 (`substring(0, 12)`) и допиши "
               "три точки `...`. Иначе название остаётся целиком.",
               "Выведи две строки: `Film: …` (название для билета) и `Row …, seat …`, например `Row 7, seat 12`."],
        hint="Название ровно из 12 символов помещается целиком. `substring(0, 12)` берёт символы с индексами "
             "от 0 до 11 — ровно 12 штук. Большими буквами название должно быть в обеих ветках.",
        solution=TICKET,
        wrong=[(">= вместо >: название ровно из 12 символов тоже обрезается",
                swap(TICKET, "name.length() > 12", "name.length() >= 12")),
               ("substring(0, 11): на билете остаётся 11 символов",
                swap(TICKET, "name.substring(0, 12)", "name.substring(0, 11)")),
               ("короткое название печатается как есть, без больших букв",
                swap(TICKET, 'System.out.println("Film: " + name);', 'System.out.println("Film: " + film);'))],
        constructs=["if"],
    ),
    # ───── COMPARISON_OPERATORS ─────
    JavaOutputTask(
        skill="COMPARISON_OPERATORS", difficulty=3, slug="java-int-compare-hall", title="Посетители в зале музея",
        given=[("int", "inside"), ("int", "came"), ("int", "left")],
        variants=[{"inside": "38", "came": "25", "left": "7"}],
        hidden=[{"inside": "40", "came": "30", "left": "10"}, {"inside": "50", "came": "20", "left": "9"},
                {"inside": "55", "came": "12", "left": "8"}, {"inside": "20", "came": "0", "left": "20"},
                {"inside": "60", "came": "15", "left": "0"}],
        intro="В зале с главной картиной музея одновременно может быть не больше 60 человек. Сколько посетителей "
              "сейчас в зале, записано в поле `inside`. Потом в зал вошла экскурсия из `came` человек, а затем "
              "`left` человек вышли.",
        steps=["Прибавь экскурсию к `inside` через `+=` и выведи `After the tour came in: …`.",
               "Отними от `inside` ушедших через `-=` и выведи `Now: …`.",
               "Сравни, сколько людей в зале теперь, с 60: если больше — выведи `Too many: … over the limit` "
               "(на сколько больше 60); если ровно 60 — `The hall is full`; если меньше — `Free places: …`."],
        hint="Исходов три — подойдут `if`, `else if` и `else`. Равенство в Java пишется двумя знаками: `==`. "
             "Каждую строку печатай сразу после своего изменения `inside`.",
        solution=HALL,
        wrong=[(">= вместо >: при ровно 60 людях пишет «Too many: 0 over the limit»",
                swap(HALL, "inside > 60", "inside >= 60")),
               ("первая строка напечатана до прихода экскурсии",
                swap(HALL, 'inside += came;\nSystem.out.println("After the tour came in: " + inside);',
                     'System.out.println("After the tour came in: " + inside);\ninside += came;')),
               ("свободные места считаются как inside - 60: получается отрицательное число",
                swap(HALL, '"Free places: " + (60 - inside)', '"Free places: " + (inside - 60)'))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill="COMPARISON_OPERATORS", difficulty=3, slug="java-int-compare-eggs", title="Размер яиц на упаковке",
        given=[("int", "eggs"), ("int", "grams")],
        variants=[{"eggs": "30", "grams": "1740"}],
        hidden=[{"eggs": "10", "grams": "450"}, {"eggs": "10", "grams": "449"}, {"eggs": "30", "grams": "1650"},
                {"eggs": "30", "grams": "1649"}, {"eggs": "20", "grams": "1300"}, {"eggs": "20", "grams": "1299"},
                {"eggs": "6", "grams": "420"}],
        intro="На птицеферме взвешивают лоток с яйцами и по среднему весу яйца решают, какой размер написать на упаковке. "
              "Сколько яиц в лотке, записано в поле `eggs`, сколько весят все эти яйца вместе (в граммах) — "
              "в поле `grams`.",
        steps=["Посчитай средний вес яйца целым числом: `grams / eggs`. Выведи `Average: … g`.",
               "Выбери размер по среднему весу: меньше 45 г — `S`, от 45 до 54 г — `M`, от 55 до 64 г — `L`, "
               "65 г и больше — `XL`.",
               "Выведи `Size: …`, например `Size: L`."],
        hint="В цепочке `if` / `else if` выполняется первая подходящая ветка, поэтому проверяй границы по порядку — "
             "от маленьких яиц к большим. Яйцо ровно 45 г — уже `M`, ровно 65 г — уже `XL`.",
        solution=EGGS,
        wrong=[("<= вместо <: яйцо ровно 45 г (55, 65 г) попадает в размер меньше",
                swap(swap(swap(EGGS, "average < 45", "average <= 45"), "average < 55", "average <= 55"),
                     "average < 65", "average <= 65")),
               ("проверки в обратном порядке: всё от 45 г считается размером M",
                code("""
                    int average = grams / eggs;
                    System.out.println("Average: " + average + " g");
                    String size;
                    if (average >= 45) {
                        size = "M";
                    } else if (average >= 55) {
                        size = "L";
                    } else if (average >= 65) {
                        size = "XL";
                    } else {
                        size = "S";
                    }
                    System.out.println("Size: " + size);
                """)),
               ("% вместо /: вместо среднего веса берётся остаток",
                swap(EGGS, "int average = grams / eggs;", "int average = grams % eggs;"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill="COMPARISON_OPERATORS", difficulty=3, slug="java-int-compare-savings", title="Сколько месяцев копить",
        given=[("int", "goal"), ("int", "saved"), ("int", "monthly")],
        variants=[{"goal": "30000", "saved": "12500", "monthly": "4000"}],
        hidden=[{"goal": "25000", "saved": "25000", "monthly": "3000"}, {"goal": "20000", "saved": "21000", "monthly": "1000"},
                {"goal": "20000", "saved": "8000", "monthly": "3000"}, {"goal": "10000", "saved": "9000", "monthly": "2500"},
                {"goal": "15000", "saved": "0", "monthly": "5000"}, {"goal": "15000", "saved": "1", "monthly": "5000"}],
        intro="Аня копит на велосипед на накопительном счёте в банке. Сколько стоит велосипед, записано в поле `goal`, "
              "сколько уже накоплено — в поле `saved`, сколько Аня откладывает каждый месяц — в поле `monthly`.",
        steps=["Если накоплено не меньше, чем стоит велосипед, выведи одну строку `Goal reached` и больше ничего.",
               "Иначе посчитай, сколько осталось накопить, — сохрани `goal - saved` в переменную `left` — "
               "и выведи `Left: … rub`.",
               "Посчитай, сколько месяцев ещё копить: `left / monthly`. Если остаток `left % monthly` не равен 0, "
               "нужен ещё один месяц — прибавь его через `++`. Выведи `Months: …`."],
        hint="«Не равно» в Java — это `!=`. Если осталось 9000 руб., а в месяц Аня откладывает 3000, хватит 3 месяцев, "
             "а если осталось 9500 руб. — понадобится 4. Второй `if` можно написать внутри ветки `else`.",
        solution=SAVINGS,
        wrong=[("> вместо >=: при ровно накопленной сумме пишет «Left: 0 rub»",
                swap(SAVINGS, "saved >= goal", "saved > goal")),
               ("неполный месяц не учтён: месяцы — только left / monthly",
                swap(SAVINGS, "if (left % monthly != 0) {\n        months++;\n    }\n", "")),
               ("== вместо !=: лишний месяц добавляется, когда делится без остатка",
                swap(SAVINGS, "left % monthly != 0", "left % monthly == 0"))],
        constructs=["if"],
    ),
    # ───── LOGICAL_AND ─────
    JavaOutputTask(
        skill="LOGICAL_AND", difficulty=3, slug="java-int-and-family", title="Семейный билет в театр",
        given=[("int", "adults"), ("int", "kids")],
        variants=[{"adults": "2", "kids": "3"}],
        hidden=[{"adults": "2", "kids": "2"}, {"adults": "2", "kids": "1"}, {"adults": "2", "kids": "4"},
                {"adults": "1", "kids": "2"}, {"adults": "3", "kids": "3"}, {"adults": "2", "kids": "0"}],
        intro="Детский театр продаёт билеты: взрослый — 450 руб., детский — 250 руб. Есть и семейный билет за 1300 руб.: "
              "его можно взять, если идут ровно двое взрослых и двое или трое детей. Сколько взрослых идёт на спектакль, "
              "записано в поле `adults`, сколько детей — в поле `kids`.",
        steps=["Посчитай обычную цену: `adults` взрослых билетов по 450 руб. и `kids` детских по 250 руб.",
               "Если взрослых ровно 2 **и** детей не меньше 2 **и** не больше 3, выведи `Family ticket`, и цена "
               "становится 1300 руб. Иначе выведи `Separate tickets`, цена остаётся обычной. Все проверки — "
               "в одном условии через `&&`.",
               "Выведи `Total: … rub` и `Per person: … rub` — цену, делённую на число людей, целым числом."],
        hint="Для «от 2 до 3» нужны две проверки: `kids >= 2 && kids <= 3`. Число людей — `adults + kids`; "
             "когда делишь на него, возьми его в скобки.",
        solution=FAMILY,
        wrong=[("> вместо >=: с двумя детьми семейный билет не дают",
                swap(FAMILY, "kids >= 2", "kids > 2")),
               ("потеряна проверка взрослых: трое взрослых тоже получают семейный билет",
                swap(FAMILY, "adults == 2 && kids >= 2", "kids >= 2")),
               ("без скобок: цена делится только на взрослых, а дети прибавляются",
                swap(FAMILY, "total / (adults + kids)", "total / adults + kids"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill="LOGICAL_AND", difficulty=3, slug="java-int-and-guide", title="Премия экскурсоводу",
        given=[("int", "points"), ("int", "reviews")],
        variants=[{"points": "92", "reviews": "20"}],
        hidden=[{"points": "90", "reviews": "20"}, {"points": "89", "reviews": "20"}, {"points": "95", "reviews": "19"},
                {"points": "115", "reviews": "25"}, {"points": "100", "reviews": "25"}, {"points": "57", "reviews": "12"}],
        intro="Посетители музея оценивают экскурсию от 1 до 5. Экскурсовод получает премию 5000 руб., если у него "
              "не меньше 20 отзывов и средняя оценка не ниже 4.5. Сумма всех его оценок записана в поле `points`, "
              "число отзывов — в поле `reviews`.",
        steps=["Посчитай среднюю оценку дробным числом: сохрани сумму оценок в переменную типа `double` "
               "(`double average = points;`) и раздели её на `reviews`.",
               "Выведи `Reviews: …, average: …` — число отзывов и среднюю, например `Reviews: 20, average: 4.6`.",
               "Если отзывов не меньше 20 **и** средняя не меньше 4.5, выведи `Bonus: 5000 rub`. Иначе выведи "
               "`No bonus yet`. Обе проверки — в одном условии через `&&`."],
        hint="`points / reviews` — деление двух `int`, дробная часть пропадёт: из 92 / 20 получится 4, а не 4.6. "
             "Ровно 20 отзывов и ровно 4.5 — премия уже положена.",
        solution=GUIDE,
        wrong=[("средняя посчитана делением int на int: дробная часть теряется",
                swap(GUIDE, "double average = points;\naverage = average / reviews;", "int average = points / reviews;")),
               ("> вместо >= для отзывов: ровно 20 отзывов не дают премию",
                swap(GUIDE, "reviews >= 20", "reviews > 20")),
               ("> вместо >= для средней: ровно 4.5 не даёт премию",
                swap(GUIDE, "average >= 4.5", "average > 4.5"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill="LOGICAL_AND", difficulty=3, slug="java-int-and-sheep", title="Стрижка овец",
        given=[("int", "months"), ("int", "currentMonth")],
        variants=[{"months": "7", "currentMonth": "6"}],
        hidden=[{"months": "5", "currentMonth": "5"}, {"months": "4", "currentMonth": "5"}, {"months": "8", "currentMonth": "4"},
                {"months": "8", "currentMonth": "7"}, {"months": "11", "currentMonth": "6"}, {"months": "0", "currentMonth": "6"}],
        intro="Шерсть у овец отрастает на 12 мм в месяц. Фермер стрижёт овец, только когда шерсть не короче 60 мм "
              "и только в мае или июне (5-й и 6-й месяцы). Сколько месяцев прошло с прошлой стрижки, записано в поле "
              "`months`, номер текущего месяца — в поле `currentMonth`.",
        steps=["Посчитай длину шерсти в миллиметрах: `months * 12`.",
               "Выведи её сантиметрами и миллиметрами: `Wool: … cm … mm` (в сантиметре 10 мм).",
               "Если шерсть не короче 60 мм **и** месяц не раньше 5-го **и** не позже 6-го, выведи `Time to shear`. "
               "Иначе выведи `Not now`. Все проверки — в одном условии через `&&`."],
        hint="Сантиметры — `/ 10`, оставшиеся миллиметры — `% 10`. «Май или июнь» — это месяц от 5 до 6: "
             "`currentMonth >= 5 && currentMonth <= 6`. Шерсть ровно 60 мм уже можно стричь.",
        solution=SHEEP,
        wrong=[("> вместо >=: шерсть ровно 60 мм не стригут",
                swap(SHEEP, "wool >= 60", "wool > 60")),
               ("потеряна верхняя граница месяца: стрижёт и в июле",
                swap(SHEEP, " && currentMonth <= 6", "")),
               ("сравнивает месяцы, а не миллиметры: months >= 60",
                swap(SHEEP, "wool >= 60 &&", "months >= 60 &&"))],
        constructs=["if"],
    ),
    # ───── LOGICAL_OR ─────
    JavaOutputTask(
        skill="LOGICAL_OR", difficulty=3, slug="java-int-or-payment", title="Подозрительный платёж",
        given=[("int", "amount"), ("int", "time"), ("boolean", "trusted")],
        variants=[{"amount": "2400", "time": "540", "trusted": "true"}],
        hidden=[{"amount": "2400", "time": "600", "trusted": "true"}, {"amount": "14999", "time": "1230", "trusted": "true"},
                {"amount": "15000", "time": "1230", "trusted": "true"}, {"amount": "500", "time": "1015", "trusted": "false"},
                {"amount": "500", "time": "0", "trusted": "true"}, {"amount": "100", "time": "2359", "trusted": "true"}],
        intro="Банк просит подтвердить платёж по карте кодом из SMS, если платёж кажется подозрительным. Сумма платежа "
              "записана в поле `amount`, время — числом в поле `time` (`2315` значит 23:15, а `540` — 5:40), "
              "а в поле `trusted` — `true`, если платят с привычного телефона хозяина карты.",
        steps=["Получи часы (`time / 100`) и минуты (`time % 100`) и выведи `Payment: … rub at … h … min`, "
               "например `Payment: 2400 rub at 5 h 40 min`.",
               "Платёж подозрительный, если он **не** с привычного телефона, **или** сумма не меньше 15000 руб., "
               "**или** он сделан ночью — раньше 6 часов утра.",
               "Для подозрительного платежа выведи `Confirm by SMS`, иначе — `Approved`. Всё условие — одно, "
               "через `||` и `!`."],
        hint="`!trusted` читается как «не с привычного телефона». Ровно в 6:00 уже утро, а платёж ровно на 15000 руб. "
             "уже подозрительный.",
        solution=PAYMENT,
        wrong=[("&& вместо ||: SMS просят, только если подозрительно всё сразу",
                swap(PAYMENT, "!trusted || amount >= 15000 || hour < 6", "!trusted && amount >= 15000 && hour < 6")),
               ("потерян !: SMS просят как раз с привычного телефона",
                swap(PAYMENT, "!trusted ||", "trusted ||")),
               ("<= 6 вместо < 6: платёж ровно в 6:00 считается ночным",
                swap(PAYMENT, "hour < 6", "hour <= 6"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill="LOGICAL_OR", difficulty=3, slug="java-int-or-bonus", title="Бонусы киноклуба",
        given=[("int", "tickets"), ("int", "day"), ("boolean", "birthday"), ("int", "points")],
        variants=[{"tickets": "3", "day": "1", "birthday": "false", "points": "420"}],
        hidden=[{"tickets": "3", "day": "2", "birthday": "false", "points": "420"},
                {"tickets": "2", "day": "7", "birthday": "true", "points": "0"},
                {"tickets": "1", "day": "1", "birthday": "true", "points": "100"},
                {"tickets": "4", "day": "5", "birthday": "false", "points": "1000"},
                {"tickets": "5", "day": "3", "birthday": "true", "points": "10"}],
        intro="По карте киноклуба за каждый купленный билет начисляют 50 бонусов, а по понедельникам и в день рождения "
              "владельца карты — вдвое больше. Сколько билетов куплено, записано в поле `tickets`, день недели "
              "(1 — понедельник, 7 — воскресенье) — в поле `day`, в поле `birthday` — `true`, если у владельца "
              "сегодня день рождения, а сколько бонусов уже на карте — в поле `points`.",
        steps=["Посчитай бонусы за покупку: по 50 за каждый билет.",
               "Если сегодня понедельник **или** у владельца день рождения, удвой бонусы через `*=`. "
               "Обе проверки — в одном условии через `||`.",
               "Только после этого прибавь бонусы к `points` через `+=`.",
               "Выведи две строки: `Bonus: … points` и `Card: … points`."],
        hint="Условие с `||` верно, если верна хотя бы одна его часть. Порядок важен: если прибавить бонусы к карте "
             "до удвоения, на карту попадёт только половина.",
        solution=BONUS,
        wrong=[("&& вместо ||: бонусы удваиваются, только если день рождения выпал на понедельник",
                swap(BONUS, "day == 1 || birthday", "day == 1 && birthday")),
               ("бонусы прибавлены к карте до удвоения",
                code("""
                    int bonus = tickets * 50;
                    points += bonus;
                    if (day == 1 || birthday) {
                        bonus *= 2;
                    }
                    System.out.println("Bonus: " + bonus + " points");
                    System.out.println("Card: " + points + " points");
                """)),
               ("забыт день рождения: удваивает только по понедельникам",
                swap(BONUS, "day == 1 || birthday", "day == 1"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill="LOGICAL_OR", difficulty=3, slug="java-int-or-apples", title="Партия яблок для магазина",
        given=[("int", "apples"), ("int", "bruised"), ("int", "grams")],
        variants=[{"apples": "200", "bruised": "8", "grams": "34000"}],
        hidden=[{"apples": "200", "bruised": "10", "grams": "30000"}, {"apples": "200", "bruised": "12", "grams": "36000"},
                {"apples": "100", "bruised": "0", "grams": "14900"}, {"apples": "300", "bruised": "18", "grams": "45000"},
                {"apples": "50", "bruised": "0", "grams": "9000"}, {"apples": "100", "bruised": "6", "grams": "20000"}],
        intro="Магазин принимает у фермера партию яблок и возвращает её, если в ней больше 5% мятых яблок или "
              "средний вес яблока меньше 150 г. Сколько яблок в партии, записано в поле `apples`, сколько из них "
              "мятых — в поле `bruised`, вес всей партии в граммах — в поле `grams`.",
        steps=["Посчитай процент мятых яблок целым числом: `bruised * 100 / apples` (сначала умножай, потом дели). "
               "Выведи `Bruised: …%`.",
               "Посчитай средний вес яблока целым числом: `grams / apples`. Выведи `Average: … g`.",
               "Если мятых больше 5% **или** средний вес меньше 150 г, выведи `Batch returned`. Иначе выведи "
               "`Batch accepted`. Обе проверки — в одном условии через `||`."],
        hint="Если сначала разделить `bruised / apples`, целочисленное деление даст 0. Ровно 5% мятых и средний вес "
             "ровно 150 г партию ещё не портят.",
        solution=APPLES,
        wrong=[("&& вместо ||: партию возвращают, только если плохо и то, и другое",
                swap(APPLES, "percent > 5 || average < 150", "percent > 5 && average < 150")),
               ("сначала деление: bruised / apples * 100 всегда даёт 0",
                swap(APPLES, "bruised * 100 / apples", "bruised / apples * 100")),
               (">= вместо >: ровно 5% мятых возвращают",
                swap(APPLES, "percent > 5", "percent >= 5"))],
        constructs=["if"],
    ),
    # ───── SWITCH_BASIC ─────
    JavaOutputTask(
        skill="SWITCH_BASIC", difficulty=3, slug="java-int-switch-audioguide", title="Номер в аудиогиде музея",
        given=[("int", "number")],
        variants=[{"number": "214"}],
        hidden=[{"number": "305"}, {"number": "412"}, {"number": "101"}, {"number": "199"}, {"number": "507"},
                {"number": "20"}, {"number": "300"}],
        intro="В аудиогиде музея у каждого экспоната номер из трёх цифр: первая цифра — этаж, две последние — номер "
              "экспоната на этаже (номер 305 — экспонат 5 на 3-м этаже). Номер, который набрал посетитель, записан "
              "в поле `number`.",
        steps=["Получи этаж (`number / 100`) и номер экспоната на этаже (`number % 100`).",
               "Сделай `switch` по этажу и выведи `Floor …: ` и название выставки: на 1-м этаже — `Ancient world`, "
               "на 2-м — `Middle Ages`, на 3-м и 4-м — `Modern art` (одна ветка на оба этажа), на любом другом "
               "(ветка `default`) — `no exhibition`. Например: `Floor 2: Middle Ages`.",
               "Последней строкой выведи `Exhibit: …` — номер экспоната на этаже."],
        hint="Две метки подряд — `case 3:` и `case 4:` — ведут в одну ветку. Заканчивай каждую ветку командой `break`, "
             "иначе Java выполнит и следующую.",
        solution=AUDIOGUIDE,
        wrong=[("нет break после 2-го этажа: печатается ещё и Modern art",
                swap(AUDIOGUIDE, '"Floor 2: Middle Ages");\n        break;\n', '"Floor 2: Middle Ages");\n')),
               ("этаж и экспонат перепутаны: / и % поменяны местами",
                swap(AUDIOGUIDE, "int floor = number / 100;\nint exhibit = number % 100;",
                     "int floor = number % 100;\nint exhibit = number / 100;")),
               ("нет метки case 4: 4-й этаж считается этажом без выставки",
                swap(AUDIOGUIDE, "    case 3:\n    case 4:\n", "    case 3:\n"))],
        checks=switch_on("номеру этажа"),
    ),
    JavaOutputTask(
        skill="SWITCH_BASIC", difficulty=3, slug="java-int-switch-promo", title="Промокод на билет в кино",
        given=[("int", "price"), ("String", "promo")],
        variants=[{"price": "450", "promo": '"kids2026"'}],
        hidden=[{"price": "400", "promo": '"STUDENT"'}, {"price": "350", "promo": '"child"'},
                {"price": "500", "promo": '"Birthday"'}, {"price": "380", "promo": '"school5"'},
                {"price": "450", "promo": '"VIP"'}, {"price": "300", "promo": '"CHILD7"'}],
        intro="Онлайн-касса кинотеатра принимает промокоды. Вид скидки определяет первая буква кода, а зритель может "
              "набрать её и большой, и маленькой. Цена билета записана в поле `price`, промокод — в поле `promo`.",
        steps=["Возьми первую букву кода большой — `promo.toUpperCase().charAt(0)` — и сохрани её в переменную "
               "типа `char`.",
               "Сделай `switch` по этой букве: `'S'` (студент) — скидка 100 руб., `'K'` и `'C'` (дети) — скидка "
               "150 руб., `'B'` (день рождения) — скидка равна всей цене, любая другая буква (`default`) — скидки нет.",
               "Отними скидку от `price` через `-=`.",
               "Выведи три строки: `Code: …` (буква), `Discount: … rub` и `To pay: … rub`."],
        hint="Заведи до `switch` переменную `discount` со значением 0, а в ветках только присваивай ей скидку. "
             "Буквы в `case` пиши в одинарных кавычках: `case 'S':`.",
        solution=PROMO,
        wrong=[("без toUpperCase: маленькая буква попадает в default",
                swap(PROMO, "promo.toUpperCase().charAt(0)", "promo.charAt(0)")),
               ("нет break после 'S': студенческая скидка становится детской",
                swap(PROMO, "discount = 100;\n        break;\n", "discount = 100;\n")),
               ("нет break после детской скидки: детский билет становится бесплатным",
                swap(PROMO, "discount = 150;\n        break;\n", "discount = 150;\n"))],
        checks=switch_on("первой букве промокода"),
    ),
    JavaOutputTask(
        skill="SWITCH_BASIC", difficulty=3, slug="java-int-switch-currency", title="Обмен валюты в банке",
        given=[("String", "currency"), ("int", "amount")],
        variants=[{"currency": '"USD"', "amount": "100"}],
        hidden=[{"currency": '"EUR"', "amount": "40"}, {"currency": '"CNY"', "amount": "1000"},
                {"currency": '"USD"', "amount": "3"}, {"currency": '"GBP"', "amount": "100"},
                {"currency": '"CNY"', "amount": "7"}, {"currency": '"EUR"', "amount": "1"}],
        intro="В отделении банка меняют валюту на рубли по курсу дня, а за обмен банк берёт 1%. Код валюты записан "
              "строкой в поле `currency`, сколько единиц валюты принёс клиент — в поле `amount`.",
        steps=["Сделай `switch` по `currency` и сохрани курс в переменную типа `double`: `\"USD\"` — 90.5, "
               "`\"EUR\"` — 98.25, `\"CNY\"` — 12.4 руб. за единицу.",
               "Для любого другого кода (ветка `default`) выведи одну строку `Unknown currency` и больше ничего.",
               "Иначе посчитай рубли: `amount`, умноженное на курс, и отбрось копейки приведением `(int)`.",
               "Выведи две строки: сумму с кодом и рубли, например `100 USD = 9050 rub`, и `You get: … rub` — "
               "рубли минус комиссия 1% (комиссия целым числом: рубли `/ 100`)."],
        hint="Заведи курс до `switch` со значением 0 и в ветках только присваивай его. После `switch` курс 0 означает "
             "неизвестную валюту — это удобно проверить обычным `if`. Приведение `(int)` ставь перед скобками со всем "
             "произведением.",
        solution=CURRENCY,
        wrong=[("нет break после USD: доллар считается по курсу евро",
                swap(CURRENCY, "rate = 90.5;\n        break;\n", "rate = 90.5;\n")),
               ("без (int): рубли печатаются дробным числом",
                swap(swap(CURRENCY, "int rub = (int) (amount * rate);", "double rub = amount * rate;"),
                     '"You get: " + (rub - rub / 100)', '"You get: " + (int) (rub - rub / 100)')),
               ("комиссия как остаток: rub % 100 вместо rub / 100",
                swap(CURRENCY, "rub - rub / 100", "rub - rub % 100"))],
        checks=uses_switch("currency"),
    ),
]
