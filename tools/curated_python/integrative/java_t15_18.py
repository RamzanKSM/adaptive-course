"""Integrative tasks (the task of a topic's 3rd iteration), Java, topics 15–18: for, accumulating in a loop, while,
loop termination. Each family has its topic at the core and 1–2 earlier topics doing real work:
- FOR_LOOP_BASIC: double and an (int) cast + && (furnace); / and % + || (boats); String substring/length +
  arithmetic (smartwatch ticker). Not yet: accumulating in a loop, while, arrays, own methods.
- ACCUMULATOR_PATTERN: % + || (night shift); % + && (savings bonus); switch + / (hotel bill).
  Not yet: while, break, arrays, own methods.
- WHILE_LOOP_BASIC: accumulating + / with an if (update download); accumulating + integer percent (laptop that gets
  dearer); % + if (factory order without Sundays). Not yet: break/continue, arrays, own methods.
- LOOP_TERMINATION: double + break (hike before sunset); accumulating + / and % + break (game levels before bedtime);
  && in the loop condition + accumulating (bike savings before summer). Not yet: arrays, own methods.
Theme domains: factory and production, hotels and tourism, gadgets and batteries, savings plans — the three stories
of a topic are in three different domains. Strings are compared only in switch (no equals yet); every loop of the
references and wrong solutions stops for every value set."""
import textwrap

from java_tasks import JavaOutputTask
from topics_java.t22_switch import uses_switch


def code(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


def swap(text: str, old: str, new: str) -> str:
    assert old in text, old
    return text.replace(old, new)


# ───────── 15. Цикл for ─────────

FURNACE = code("""
    for (int minute = 1; minute <= minutes; minute++) {
        int t = (int) (start + rate * minute);
        if (t >= 800 && t <= 900) {
            System.out.println("Minute " + minute + ": " + t + " C - load");
        } else {
            System.out.println("Minute " + minute + ": " + t + " C - skip");
        }
    }
""")

BOATS = code("""
    for (int i = 1; i <= tourists; i++) {
        int boat = (i - 1) / perBoat + 1;
        System.out.println("Tourist " + i + ": boat " + boat);
        if (i % perBoat == 0 || i == tourists) {
            System.out.println("Boat " + boat + " departs");
        }
    }
""")

TICKER = code("""
    for (int i = 0; i + width <= message.length(); i++) {
        System.out.println((i + 1) + ": [" + message.substring(i, i + width) + "]");
    }
    System.out.println("Frames: " + (message.length() - width + 1));
""")

# ───────── 16. Накопление результата в цикле ─────────

NIGHT_SHIFT = code("""
    int parts = 0;
    int night = 0;
    for (int i = 0; i < hours; i++) {
        int clock = (start + i) % 24;
        if (clock >= 22 || clock < 6) {
            parts += perHour / 2;
            night++;
        } else {
            parts += perHour;
        }
    }
    System.out.println("Night hours: " + night);
    System.out.println("Parts: " + parts);
""")

BONUS = code("""
    int balance = 0;
    int bonuses = 0;
    for (int month = 1; month <= months; month++) {
        balance += perMonth;
        if (month % 3 == 0 && balance >= limit) {
            balance += bonus;
            bonuses++;
        }
    }
    System.out.println("Balance: " + balance + " rub");
    System.out.println("Bonuses: " + bonuses);
""")

HOTEL_BILL = code("""
    int price;
    switch (category) {
        case "economy": price = 2000; break;
        case "standard": price = 3500; break;
        default: price = 6000;
    }
    int total = 0;
    for (int night = 1; night <= nights; night++) {
        if (night >= 4) {
            total += price - price / 10;
        } else {
            total += price;
        }
    }
    System.out.println("Category: " + category + ", " + price + " rub per night");
    System.out.println("Nights: " + nights + ", total: " + total + " rub");
""")

# ───────── 17. Цикл while ─────────

UPDATE = code("""
    int loaded = 0;
    int minute = 0;
    while (loaded < size) {
        minute++;
        loaded += speed;
        speed += 2;
        int percent = loaded * 100 / size;
        if (percent > 100) {
            percent = 100;
        }
        System.out.println("Minute " + minute + ": " + percent + "%");
    }
    System.out.println("Update ready in " + minute + " min");
""")

LAPTOP = code("""
    int saved = 0;
    int months = 0;
    while (saved < price) {
        months++;
        saved += perMonth;
        price += price * percent / 100;
    }
    System.out.println("Months: " + months);
    System.out.println("Price: " + price + " rub");
    System.out.println("Left over: " + (saved - price) + " rub");
""")

ORDER = code("""
    int made = 0;
    int day = 0;
    int sundays = 0;
    while (made < order) {
        day++;
        if (day % 7 == 0) {
            sundays++;
        } else {
            made += perDay;
        }
    }
    System.out.println("Done on day " + day);
    System.out.println("Sundays off: " + sundays);
    System.out.println("Extra parts: " + (made - order));
""")

# ───────── 18. Завершение цикла ─────────

HIKE = code("""
    double walked = 0;
    int hour = start;
    while (walked < distance) {
        if (hour >= sunset) {
            break;
        }
        walked += speed;
        hour++;
    }
    if (walked >= distance) {
        System.out.println("At the shelter by " + hour + ":00");
    } else {
        System.out.println("Camp at " + walked + " km");
        System.out.println("Left: " + (distance - walked) + " km");
    }
""")

CONSOLE = code("""
    int played = 0;
    int level = 0;
    int next = first;
    while (level < levels) {
        if (played + next > limit) {
            break;
        }
        played += next;
        level++;
        next += 5;
    }
    System.out.println("Levels passed: " + level + " of " + levels);
    System.out.println("Time: " + played / 60 + " h " + played % 60 + " min");
    if (level == levels) {
        System.out.println("Game completed!");
    }
""")

BIKE = code("""
    int saved = 0;
    int week = 0;
    int pay = first;
    while (saved < price && week < weeks) {
        week++;
        saved += pay;
        pay += 100;
    }
    if (saved >= price) {
        System.out.println("Bike bought in week " + week);
        System.out.println("Change: " + (saved - price) + " rub");
    } else {
        System.out.println("Summer came: " + saved + " of " + price + " rub");
    }
""")

TASKS = [
    # ───────── FOR_LOOP_BASIC ─────────
    JavaOutputTask(
        skill="FOR_LOOP_BASIC", difficulty=3, slug="java-int-for-furnace", title="Печь для закалки деталей",
        given=[("int", "start"), ("double", "rate"), ("int", "minutes")],
        variants=[{"start": "600", "rate": "47.5", "minutes": "8"}],
        hidden=[{"start": "700", "rate": "25.0", "minutes": "4"},
                {"start": "850", "rate": "12.5", "minutes": "4"},
                {"start": "880", "rate": "20.5", "minutes": "2"},
                {"start": "760", "rate": "39.5", "minutes": "3"},
                {"start": "300", "rate": "100.0", "minutes": "7"}],
        intro="В цехе закаливают стальные детали. В начале смены печь нагрета до `start` градусов и каждую минуту "
              "становится горячее на `rate` градусов — это дробное число. На табло печи видны только целые градусы, "
              "а загружать детали можно, когда на табло от 800 до 900 градусов включительно. Мастеру нужен план "
              "на `minutes` минут.",
        steps=["Перебери циклом `for` номера минут `minute` от 1 до `minutes` включительно.",
               "Посчитай температуру на этой минуте: `start + rate * minute`. Это дробное число — приведи его к `int` "
               "через `(int)` (скобки вокруг всего выражения) и сохрани в целую переменную: это число на табло.",
               "Если число на табло не меньше 800 **и** не больше 900, выведи строку вида `Minute 5: 837 C - load`, "
               "иначе — `Minute 1: 647 C - skip`. Обе проверки — в одном условии через `&&`."],
        hint="`(int)` отбрасывает дробную часть, не округляя: 837.5 станет 837. С границами сравнивай уже целое "
             "число с табло: 900.5 градуса на табло выглядят как 900, и это ещё подходит.",
        solution=FURNACE,
        wrong=[("|| вместо &&: подходящей оказывается любая температура",
                swap(FURNACE, "t >= 800 && t <= 900", "t >= 800 || t <= 900")),
               ("строгие сравнения: ровно 800 и ровно 900 градусов не подходят",
                swap(FURNACE, "t >= 800 && t <= 900", "t > 800 && t < 900")),
               ("сравнивает дробную температуру, а не число с табло: 900.5 уже не подходит",
                swap(FURNACE, "int t = (int) (start + rate * minute);\n    if (t >= 800 && t <= 900)",
                     "double temp = start + rate * minute;\n    int t = (int) temp;\n    if (temp >= 800 && temp <= 900)"))],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill="FOR_LOOP_BASIC", difficulty=3, slug="java-int-for-boats", title="Туристы садятся в лодки",
        given=[("int", "tourists"), ("int", "perBoat")],
        variants=[{"tourists": "6", "perBoat": "4"}],
        hidden=[{"tourists": "8", "perBoat": "4"},
                {"tourists": "3", "perBoat": "5"},
                {"tourists": "1", "perBoat": "1"},
                {"tourists": "4", "perBoat": "1"},
                {"tourists": "10", "perBoat": "3"}],
        intro="На лодочной станции группу туристов сажают в лодки по очереди: первые `perBoat` человек — в лодку 1, "
              "следующие — в лодку 2 и так далее. Лодка отплывает, как только заполнится; последняя может уйти и "
              "неполной. Сколько туристов в группе, записано в поле `tourists`, сколько мест в лодке — в поле `perBoat`.",
        steps=["Перебери циклом `for` номера туристов `i` от 1 до `tourists` включительно.",
               "Номер лодки туриста посчитай так: `(i - 1) / perBoat + 1`. Выведи строку вида "
               "`Tourist 5: boat 2`.",
               "Если на этом туристе лодка заполнилась (`i` делится на `perBoat` без остатка) **или** это "
               "последний турист, сразу после его строки выведи `Boat 2 departs` с номером его лодки. Обе проверки — "
               "в одном условии через `||`."],
        hint="`- 1` нужен, чтобы турист, занявший последнее место, остался в своей лодке: при 4 местах у четвёртого "
             "туриста `(4 - 1) / 4 + 1` равно 1. Делится ли число без остатка, покажет `%`: `8 % 4 == 0`.",
        solution=BOATS,
        wrong=[("лодка отплывает только заполненной: последняя неполная лодка так и не уходит",
                swap(BOATS, "i % perBoat == 0 || i == tourists", "i % perBoat == 0")),
               ("номер лодки без - 1: турист, занявший последнее место, попадает в следующую лодку",
                swap(BOATS, "(i - 1) / perBoat + 1", "i / perBoat + 1")),
               ("&& вместо ||: лодка отплывает, только если она полная и турист последний",
                swap(BOATS, "i % perBoat == 0 || i == tourists", "i % perBoat == 0 && i == tourists"))],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill="FOR_LOOP_BASIC", difficulty=3, slug="java-int-for-watch-ticker", title="Бегущая строка на смарт-часах",
        given=[("String", "message"), ("int", "width")],
        variants=[{"message": '"CALL MOM"', "width": "5"}],
        hidden=[{"message": '"LOW BATTERY"', "width": "6"},
                {"message": '"HI"', "width": "2"},
                {"message": '"NEW SMS"', "width": "3"},
                {"message": '"RUN 5 KM"', "width": "8"},
                {"message": '"MEET AT 7"', "width": "1"}],
        intro="На смарт-часы пришло уведомление — его текст записан в поле `message`. Экран часов узкий и вмещает "
              "только `width` символов (поле `width`; сообщение не короче экрана). Поэтому часы прокручивают текст: "
              "каждый следующий кадр начинается на один символ правее, пока на экране не покажется конец сообщения.",
        steps=["Перебери циклом `for` позицию начала кадра `i`: от 0 и дальше на 1, пока кадр помещается в сообщение, "
               "то есть пока `i + width` не больше длины `message`.",
               "Для каждой позиции выведи строку вида `1: [CALL ]`: номер кадра (кадры считаем с 1), двоеточие, "
               "пробел и в квадратных скобках `width` символов сообщения, начиная с позиции `i`.",
               "После цикла выведи строку `Frames: 4` — сколько всего кадров: длина сообщения минус `width` плюс 1."],
        hint="Второе число в `substring` — индекс, перед которым подстрока заканчивается, а не её длина: "
             "`\"WATCH\".substring(1, 4)` — это `\"ATC\"`. Если сообщение ровно по ширине экрана, кадр один.",
        solution=TICKER,
        wrong=[("< вместо <=: последний кадр с концом сообщения не показывается",
                swap(TICKER, "i + width <= message.length()", "i + width < message.length()")),
               ("substring(i, width): второе число принято за длину, а не за индекс конца",
                swap(TICKER, "message.substring(i, i + width)", "message.substring(i, width)")),
               ("номер кадра i, а не i + 1: кадры нумеруются с нуля",
                swap(TICKER, "(i + 1) + \": [\"", "i + \": [\""))],
        constructs=["for"],
    ),

    # ───────── ACCUMULATOR_PATTERN ─────────
    JavaOutputTask(
        skill="ACCUMULATOR_PATTERN", difficulty=3, slug="java-int-accum-night-shift", title="Ночная смена на заводе",
        given=[("int", "start"), ("int", "hours"), ("int", "perHour")],
        variants=[{"start": "18", "hours": "8", "perHour": "150"}],
        hidden=[{"start": "6", "hours": "10", "perHour": "120"},
                {"start": "21", "hours": "2", "perHour": "101"},
                {"start": "4", "hours": "3", "perHour": "80"},
                {"start": "20", "hours": "12", "perHour": "90"},
                {"start": "23", "hours": "26", "perHour": "60"}],
        intro="Линия на заводе запускается в `start` часов (от 0 до 23) и работает `hours` часов подряд. В дневные часы "
              "она выпускает `perHour` деталей в час, а в ночные — с 22 до 6 часов — вдвое меньше: `perHour / 2` "
              "(целым делением).",
        steps=["До цикла заведи две переменные со значением 0: сколько выпущено деталей и сколько было ночных часов.",
               "Перебери циклом `for` часы работы: `i` от 0, пока `i < hours`. Время на часах в этот час — "
               "`(start + i) % 24`: после 23 снова начинается 0.",
               "Если это время не меньше 22 **или** меньше 6, час ночной: прибавь к деталям `perHour / 2` и увеличь "
               "счётчик ночных часов на 1. Иначе прибавь `perHour`. Обе проверки — в одном условии через `||`.",
               "После цикла выведи две строки: `Night hours: 4` и `Parts: 900` со своими числами."],
        hint="`25 % 24` равно 1: остаток от деления на 24 превращает «25 часов» в час ночи. Час, который начинается "
             "в 6:00, уже дневной, а начинающийся в 22:00 — ночной.",
        solution=NIGHT_SHIFT,
        wrong=[("&& вместо ||: время не бывает сразу не меньше 22 и меньше 6, ночных часов нет",
                swap(NIGHT_SHIFT, "clock >= 22 || clock < 6", "clock >= 22 && clock < 6")),
               ("> 22 вместо >= 22: час с 22:00 считается дневным",
                swap(NIGHT_SHIFT, "clock >= 22", "clock > 22")),
               ("без % 24: часы после полуночи (24, 25…) не считаются ночными",
                swap(NIGHT_SHIFT, "(start + i) % 24", "start + i"))],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill="ACCUMULATOR_PATTERN", difficulty=3, slug="java-int-accum-quarter-bonus", title="Копим со стипендии",
        given=[("int", "perMonth"), ("int", "months"), ("int", "limit"), ("int", "bonus")],
        variants=[{"perMonth": "2000", "months": "7", "limit": "10000", "bonus": "500"}],
        hidden=[{"perMonth": "1000", "months": "6", "limit": "6000", "bonus": "300"},
                {"perMonth": "5000", "months": "12", "limit": "10000", "bonus": "1000"},
                {"perMonth": "3000", "months": "2", "limit": "0", "bonus": "700"},
                {"perMonth": "1500", "months": "9", "limit": "5000", "bonus": "250"},
                {"perMonth": "900", "months": "5", "limit": "3000", "bonus": "100"}],
        intro="Лена копит со стипендии: каждый месяц она кладёт на накопительный счёт `perMonth` руб. Раз в квартал — "
              "в 3-й, 6-й, 9-й… месяц — банк дарит бонус `bonus` руб., но только если на счёте в этот момент уже не "
              "меньше `limit` руб. Копить Лена будет `months` месяцев.",
        steps=["До цикла заведи две переменные со значением 0: сумму на счёте `balance` и счётчик полученных бонусов.",
               "Перебери циклом `for` месяцы от 1 до `months` включительно. Каждый месяц сначала прибавь к `balance` "
               "взнос `perMonth`.",
               "Потом проверь: если номер месяца делится на 3 без остатка **и** `balance` не меньше `limit`, прибавь "
               "к `balance` бонус и увеличь счётчик бонусов на 1. Обе проверки — в одном условии через `&&`.",
               "После цикла выведи две строки: `Balance: 14500 rub` и `Bonuses: 1` со своими числами."],
        hint="Порядок важен: бонус проверяется, когда взнос этого месяца уже на счёте. Если на счёте ровно `limit`, "
             "бонус положен.",
        solution=BONUS,
        wrong=[("бонус проверяется до взноса этого месяца",
                swap(BONUS, "    balance += perMonth;\n    if (month % 3 == 0 && balance >= limit) {",
                     "    if (month % 3 == 0 && balance >= limit) {\n        balance += perMonth;")),
               ("> вместо >=: при ровно limit рублях бонуса нет",
                swap(BONUS, "balance >= limit", "balance > limit")),
               ("|| вместо &&: бонус каждый квартал и каждый месяц, когда денег достаточно",
                swap(BONUS, "month % 3 == 0 && balance >= limit", "month % 3 == 0 || balance >= limit"))],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill="ACCUMULATOR_PATTERN", difficulty=3, slug="java-int-accum-hotel-bill", title="Счёт за проживание в отеле",
        given=[("String", "category"), ("int", "nights")],
        variants=[{"category": '"standard"', "nights": "5"}],
        hidden=[{"category": '"economy"', "nights": "3"},
                {"category": '"economy"', "nights": "4"},
                {"category": '"suite"', "nights": "1"},
                {"category": '"deluxe"', "nights": "7"},
                {"category": '"standard"', "nights": "10"}],
        intro="Гость уезжает из отеля, и администратор готовит счёт. Категория номера записана в поле `category`, "
              "сколько ночей прожил гость — в поле `nights`. Ночь стоит 2000 руб. в категории `\"economy\"`, "
              "3500 руб. в `\"standard\"` и 6000 руб. в любой другой. Начиная с 4-й ночи каждая ночь на 10% дешевле.",
        steps=["Заведи переменную `price` — цену одной ночи — и выбери её значение оператором `switch` по полю `category`: `\"economy\"` — 2000, `\"standard\"` — "
               "3500, любое другое значение (`default`) — 6000.",
               "До цикла заведи переменную для суммы со значением 0. Перебери циклом `for` ночи от 1 до `nights` "
               "включительно: за первые три ночи прибавляй к сумме полную цену, а начиная с 4-й — цену без её "
               "десятой части (`price - price / 10`).",
               "После цикла выведи две строки: `Category: standard, 3500 rub per night` и "
               "`Nights: 5, total: 16800 rub` со своими значениями."],
        hint="В конце каждой ветки `case` нужен `break`, иначе выполнится и следующая ветка. Четвёртая ночь — уже "
             "со скидкой.",
        solution=HOTEL_BILL,
        wrong=[("скидка уже с 3-й ночи",
                swap(HOTEL_BILL, "night >= 4", "night >= 3")),
               ("= вместо +=: в сумме остаётся только последняя ночь",
                swap(HOTEL_BILL, "        total += price - price / 10;\n    } else {\n        total += price;",
                     "        total = price - price / 10;\n    } else {\n        total = price;")),
               ("нет break в ветках switch: любая категория стоит 6000",
                swap(HOTEL_BILL, 'case "economy": price = 2000; break;\n    case "standard": price = 3500; break;',
                     'case "economy": price = 2000;\n    case "standard": price = 3500;'))],
        constructs=["for", "if"],
        checks=uses_switch("category"),
    ),

    # ───────── WHILE_LOOP_BASIC ─────────
    JavaOutputTask(
        skill="WHILE_LOOP_BASIC", difficulty=3, slug="java-int-while-update", title="Загрузка обновления",
        given=[("int", "size"), ("int", "speed")],
        variants=[{"size": "120", "speed": "20"}],
        hidden=[{"size": "50", "speed": "50"},
                {"size": "30", "speed": "100"},
                {"size": "42", "speed": "20"},
                {"size": "44", "speed": "10"},
                {"size": "200", "speed": "10"}],
        intro="Телефон скачивает обновление размером `size` МБ. В первую минуту скорость загрузки — `speed` МБ "
              "в минуту, а каждую следующую минуту она вырастает на 2 МБ. Сначала ничего не скачано.",
        steps=["Заведи две переменные со значением 0: `loaded` — сколько мегабайт скачано, и `minute` — сколько прошло минут.",
               "Цикл `while` работает, пока `loaded` меньше `size`. В каждом повторе: увеличь число минут на 1, прибавь "
               "к `loaded` текущую скорость `speed`, а затем увеличь `speed` на 2.",
               "В конце каждого повтора выведи строку вида `Minute 2: 35%` — процент скачанного (`loaded * 100 / size`, "
               "целым делением). Больше 100 процентов не бывает: если получилось больше, выведи 100.",
               "После цикла выведи `Update ready in 5 min` со своим числом минут."],
        hint="Сколько понадобится минут, заранее неизвестно, — поэтому здесь `while`. Если скачано ровно `size`, "
             "загрузка закончена, лишняя минута не нужна.",
        solution=UPDATE,
        wrong=[("<= вместо <: когда скачано ровно size, появляется лишняя минута",
                swap(UPDATE, "while (loaded < size)", "while (loaded <= size)")),
               ("процент не ограничен: в последней строке бывает больше 100%",
                swap(UPDATE, "    if (percent > 100) {\n        percent = 100;\n    }\n", "")),
               ("скорость растёт до прибавления: уже в первую минуту скачано speed + 2",
                swap(UPDATE, "    loaded += speed;\n    speed += 2;", "    speed += 2;\n    loaded += speed;"))],
        constructs=["while", "if"],
    ),
    JavaOutputTask(
        skill="WHILE_LOOP_BASIC", difficulty=3, slug="java-int-while-laptop", title="Копим на дорожающий ноутбук",
        given=[("int", "price"), ("int", "perMonth"), ("int", "percent")],
        variants=[{"price": "10000", "perMonth": "2500", "percent": "2"}],
        hidden=[{"price": "1000", "perMonth": "1010", "percent": "1"},
                {"price": "5000", "perMonth": "1000", "percent": "0"},
                {"price": "30000", "perMonth": "6000", "percent": "5"},
                {"price": "800", "perMonth": "1000", "percent": "10"},
                {"price": "20000", "perMonth": "3000", "percent": "3"}],
        intro="Саша копит на ноутбук, который сейчас стоит `price` руб. Каждый месяц он откладывает `perMonth` руб., "
              "но и ноутбук за месяц дорожает на `percent` процентов. Как только в конце месяца накопления станут "
              "не меньше цены, Саша покупает ноутбук. Сначала накоплений нет.",
        steps=["Заведи две переменные со значением 0: накопления и число месяцев.",
               "Цикл `while` работает, пока накоплений меньше `price`. В каждом повторе: увеличь число месяцев на 1, "
               "добавь к накоплениям `perMonth` и подними цену — прибавь к `price` её `percent` процентов: "
               "`price * percent / 100` (сначала умножение, потом целое деление).",
               "После цикла выведи три строки: `Months: 5`, `Price: 11040 rub` (цена в момент покупки) и "
               "`Left over: 1460 rub` — сколько денег останется после покупки."],
        hint="Поле `price` можно менять, как обычную переменную. Порядок в `price * percent / 100` важен: "
             "`percent / 100` при делении целых даёт 0, и ноутбук бы не дорожал.",
        solution=LAPTOP,
        wrong=[("<= вместо <: когда накоплено ровно столько, сколько стоит ноутбук, копит лишний месяц",
                swap(LAPTOP, "while (saved < price)", "while (saved <= price)")),
               ("percent / 100 целым делением даёт 0: цена не растёт",
                swap(LAPTOP, "price * percent / 100", "price * (percent / 100)")),
               ("месяцы считаются с 1: месяцев на один больше",
                swap(LAPTOP, "int months = 0;", "int months = 1;"))],
        constructs=["while"],
    ),
    JavaOutputTask(
        skill="WHILE_LOOP_BASIC", difficulty=3, slug="java-int-while-order", title="Заказ без работы по воскресеньям",
        given=[("int", "order"), ("int", "perDay")],
        variants=[{"order": "1000", "perDay": "120"}],
        hidden=[{"order": "600", "perDay": "100"},
                {"order": "50", "perDay": "200"},
                {"order": "2000", "perDay": "150"},
                {"order": "700", "perDay": "100"},
                {"order": "1300", "perDay": "110"}],
        intro="Завод получил заказ на `order` деталей и начал его выполнять в понедельник. Каждый день цех делает "
              "`perDay` деталей, кроме воскресений: 7-й, 14-й, 21-й… день — выходной.",
        steps=["Заведи три переменные со значением 0: сколько деталей сделано, номер дня и число выходных воскресений.",
               "Цикл `while` работает, пока сделано меньше `order`. В каждом повторе сначала увеличь номер дня на 1. "
               "Если номер дня делится на 7 без остатка, это воскресенье — увеличь число воскресений на 1. Иначе "
               "прибавь к сделанному `perDay`.",
               "После цикла выведи три строки: `Done on day 10`, `Sundays off: 1` и `Extra parts: 80` — на сколько "
               "деталей сделано больше заказа."],
        hint="Номер дня увеличивай в самом начале повтора: тогда первый день — это день 1, а не 0. Если деталей "
             "сделано ровно `order`, заказ выполнен.",
        solution=ORDER,
        wrong=[("воскресенья не пропускаются: цех работает каждый день",
                swap(ORDER, "    if (day % 7 == 0) {\n        sundays++;\n    } else {\n        made += perDay;\n    }",
                     "    made += perDay;")),
               ("<= вместо <: когда сделано ровно order, цех работает лишний день",
                swap(ORDER, "while (made < order)", "while (made <= order)")),
               ("номер дня растёт в конце повтора: самый первый день считается воскресеньем",
                swap(ORDER, "    day++;\n    if (day % 7 == 0) {\n        sundays++;\n    } else {\n        made += perDay;\n    }",
                     "    if (day % 7 == 0) {\n        sundays++;\n    } else {\n        made += perDay;\n    }\n    day++;"))],
        constructs=["while", "if"],
    ),

    # ───────── LOOP_TERMINATION ─────────
    JavaOutputTask(
        skill="LOOP_TERMINATION", difficulty=3, slug="java-int-lt-hike", title="Успеть к приюту до заката",
        given=[("double", "distance"), ("double", "speed"), ("int", "start"), ("int", "sunset")],
        variants=[{"distance": "20.5", "speed": "2.5", "start": "10", "sunset": "17"}],
        hidden=[{"distance": "12.0", "speed": "3.0", "start": "8", "sunset": "18"},
                {"distance": "15.0", "speed": "2.5", "start": "9", "sunset": "15"},
                {"distance": "10.5", "speed": "2.0", "start": "17", "sunset": "20"},
                {"distance": "1.5", "speed": "4.0", "start": "12", "sunset": "13"},
                {"distance": "8.0", "speed": "3.5", "start": "19", "sunset": "19"},
                {"distance": "9.75", "speed": "1.25", "start": "6", "sunset": "14"}],
        intro="Туристы идут к горному приюту. До него `distance` км, за час группа проходит `speed` км — оба числа "
              "дробные. Вышли в `start` часов, а в `sunset` часов закат: в темноте идти нельзя, и группа ставит "
              "палатку там, где её застал закат.",
        steps=["Заведи переменную `walked` типа `double` со значением 0 — сколько километров пройдено, и переменную "
               "`hour`, равную `start`.",
               "Цикл `while` работает, пока `walked` меньше `distance`. В начале каждого повтора проверь: если `hour` "
               "не меньше `sunset`, наступил закат — выйди из цикла командой `break`. Иначе прибавь к `walked` "
               "значение `speed` и увеличь `hour` на 1.",
               "После цикла: если `walked` не меньше `distance`, группа дошла — выведи `At the shelter by 15:00` "
               "(вместо 15 — значение `hour`). Иначе выведи две строки: `Camp at 17.5 km` и `Left: 3.0 km` — "
               "сколько километров осталось до приюта."],
        hint="У цикла два выхода: условие `walked < distance` перестаёт выполняться, когда группа дошла, а `break` "
             "срабатывает на закате. Поэтому после цикла по `walked` видно, каким выходом он закончился. Число типа "
             "`double` печатается с точкой: `3.0`.",
        solution=HIKE,
        wrong=[("> вместо >=: группа идёт ещё час после заката",
                swap(HIKE, "hour >= sunset", "hour > sunset")),
               ("после цикла решает по часу, а не по пройденному пути: дошедшие ровно к закату ставят палатку",
                swap(HIKE, "if (walked >= distance) {", "if (hour < sunset) {")),
               ("walked типа int: дробная часть каждого часа пути теряется",
                swap(HIKE, "double walked = 0;", "int walked = 0;"))],
        constructs=["while", "if"],
    ),
    JavaOutputTask(
        skill="LOOP_TERMINATION", difficulty=3, slug="java-int-lt-console", title="Уровни игры до отбоя",
        given=[("int", "levels"), ("int", "first"), ("int", "limit")],
        variants=[{"levels": "10", "first": "10", "limit": "110"}],
        hidden=[{"levels": "3", "first": "20", "limit": "120"},
                {"levels": "8", "first": "15", "limit": "75"},
                {"levels": "6", "first": "10", "limit": "45"},
                {"levels": "4", "first": "30", "limit": "20"},
                {"levels": "5", "first": "10", "limit": "100"},
                {"levels": "2", "first": "50", "limit": "200"}],
        intro="Дима играет на приставке в игру из `levels` уровней. Первый уровень проходится за `first` минут, "
              "а каждый следующий — на 5 минут дольше предыдущего. Мама разрешила играть не больше `limit` минут, "
              "а начатый уровень бросать нельзя: если следующий уровень не успеть пройти до конца, Дима его не начинает.",
        steps=["Заведи переменные: `played` со значением 0 (сколько минут сыграно), `level` со значением 0 (сколько "
               "уровней пройдено) и `next`, равную `first` (сколько минут займёт следующий уровень).",
               "Цикл `while` работает, пока `level` меньше `levels`. В начале каждого повтора проверь: если "
               "`played + next` больше `limit`, следующий уровень не успеть — выйди из цикла командой `break`. "
               "Иначе прибавь `next` к `played`, увеличь `level` на 1, а `next` — на 5.",
               "После цикла выведи две строки: `Levels passed: 5 of 10` и `Time: 1 h 40 min` — сыгранные минуты "
               "в часах (`/ 60`) и минутах (`% 60`).",
               "Если пройдены все уровни, выведи последней строкой `Game completed!`."],
        hint="Проверяй время вместе со следующим уровнем: `played + next`. Если уровень заканчивается ровно "
             "на `limit` минуте, его ещё можно пройти.",
        solution=CONSOLE,
        wrong=[(">= вместо >: уровень, который заканчивается ровно в срок, не начинается",
                swap(CONSOLE, "played + next > limit", "played + next >= limit")),
               ("проверяет только уже сыгранное время: начинает уровень, который не успеет закончить",
                swap(CONSOLE, "played + next > limit", "played >= limit")),
               ("next растёт до прибавления: первый уровень длится first + 5 минут",
                swap(CONSOLE, "    played += next;\n    level++;\n    next += 5;",
                     "    next += 5;\n    played += next;\n    level++;"))],
        constructs=["while", "if"],
    ),
    JavaOutputTask(
        skill="LOOP_TERMINATION", difficulty=3, slug="java-int-lt-bike-fund", title="Копим на велосипед к лету",
        given=[("int", "price"), ("int", "first"), ("int", "weeks")],
        variants=[{"price": "5000", "first": "500", "weeks": "10"}],
        hidden=[{"price": "5000", "first": "500", "weeks": "6"},
                {"price": "4500", "first": "500", "weeks": "6"},
                {"price": "1000", "first": "2000", "weeks": "3"},
                {"price": "3000", "first": "100", "weeks": "0"},
                {"price": "8000", "first": "300", "weeks": "12"}],
        intro="Петя копит на велосипед за `price` руб. В первую неделю он откладывает `first` руб., а каждую "
              "следующую — на 100 руб. больше, чем в предыдущую. До лета `weeks` недель, и дольше Петя копить не будет.",
        steps=["Заведи переменные: `saved` со значением 0, `week` со значением 0 и `pay`, равную `first` "
               "(взнос этой недели).",
               "Цикл `while` работает, пока накоплено меньше `price` **и** номер недели меньше `weeks` — обе проверки "
               "в одном условии через `&&`. В каждом повторе: увеличь `week` на 1, прибавь `pay` к `saved`, затем "
               "увеличь `pay` на 100.",
               "После цикла: если накоплено не меньше `price`, выведи две строки — `Bike bought in week 7` и "
               "`Change: 600 rub` (сколько денег останется после покупки). Иначе выведи одну строку вида "
               "`Summer came: 4500 of 5000 rub` — сколько накоплено и сколько стоит велосипед."],
        hint="Цикл остановится по одной из двух причин: денег хватило или недели кончились. После цикла проверяй "
             "деньги, а не номер недели: в последнюю неделю денег может хватить ровно.",
        solution=BIKE,
        wrong=[("|| вместо &&: Петя копит и после начала лета, пока не хватит денег",
                swap(BIKE, "saved < price && week < weeks", "saved < price || week < weeks")),
               ("после цикла проверяет номер недели, а не деньги: покупка в последнюю неделю теряется",
                swap(BIKE, "if (saved >= price) {", "if (week < weeks) {")),
               ("взнос растёт до прибавления: в первую неделю отложено first + 100",
                swap(BIKE, "    saved += pay;\n    pay += 100;", "    pay += 100;\n    saved += pay;"))],
        constructs=["while", "if"],
    ),
]
