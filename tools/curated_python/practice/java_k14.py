"""Training attestation («Тренировочная аттестация»), Java, topics 1–14 (up to SWITCH_BASIC «Оператор switch»). Every
story is one integrative «Напиши код» task of the real attestation's size (about 10 minutes) that uses: println,
variables, assignment, arithmetic, execution order, primitive types (char / double / boolean), String (gluing with +,
toUpperCase, a char glued to a string), / and %, += -=, if/else (else if), comparisons, &&, || and switch with default.
Theme: animals, pets and nature — every story different, and different from the secret attestation pool.
Not yet: loops (for, while), arrays, own methods and classes, equals on strings (strings are compared only in switch)."""
from java_tasks import JavaOutputTask
from topics_java.t22_switch import uses_switch

SKILL = "SWITCH_BASIC"

WALK = """System.out.println("Dogs: " + dogs + " x " + size + ", " + minutes / 60 + " h " + minutes % 60 + " min");
int price;
switch (size) {
    case 'S': price = 150; break;
    case 'M': price = 200; break;
    default: price = 250;
}
int total = price * dogs * minutes / 30;
if (dogs >= 2 && minutes >= 60) {
    total -= total / 10;
    System.out.println("Discount: 10%");
} else {
    System.out.println("Discount: none");
}
if (hour >= 22 || hour < 7) { total += 100; }
System.out.println("Total: " + total + " rub");"""

FEEDER = """int daily;
switch (bird) {
    case "sparrow": daily = 60; break;
    case "bullfinch": daily = 30; break;
    default: daily = 40;
}
if (temp <= -10 || snow) { daily += daily / 2; }
System.out.println(bird + ": " + daily + " g a day, " + daily * 7 + " g a week");
int days = seeds / daily;
System.out.println("Seeds for " + days + " days, " + seeds % daily + " g left");
if (days < 7 && daily >= 60) {
    System.out.println("Buy a big bag");
} else if (days < 7) {
    System.out.println("Buy a small bag");
} else {
    System.out.println("Enough for a week");
}"""

SHELTER = """char block;
switch (kind) {
    case "cat": block = 'C'; break;
    case "dog": block = 'D'; break;
    default: block = 'S';
}
String cage = block + "-" + (number / 8 + 1) + "-" + (number % 8 + 1);
System.out.println(kind.toUpperCase() + " #" + number + ": cage " + cage);
int quarantine = 14;
if (vaccinated && months >= 3) { quarantine -= 7; }
System.out.println("Quarantine: " + quarantine + " days");
if (months < 3 || months >= 120) {
    System.out.println("Vet: every week");
} else {
    System.out.println("Vet: every month");
}"""

INCUBATOR = """int period;
switch (bird) {
    case "chicken": period = 21; break;
    case "duck": period = 28; break;
    case "quail": period = 17; break;
    default: period = 30;
}
System.out.println(bird + ": " + period / 7 + " weeks " + period % 7 + " days");
int hatch = day + period;
if (hatch > 30) {
    hatch -= 30;
    System.out.println("Chicks: day " + hatch + " of next month");
} else {
    System.out.println("Chicks: day " + hatch + " of this month");
}
if (temp >= 37.2 && temp <= 37.8) {
    System.out.println("Temperature: OK");
} else {
    System.out.println("Temperature: check the heater");
}
if (temp > 37.8 || humidity > 65) { System.out.println("Open the lid a little"); }"""


TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac14-walk", title="Выгул собак",
        given=[("char", "size"), ("int", "dogs"), ("int", "minutes"), ("int", "hour")],
        variants=[{"size": "'M'", "dogs": "2", "minutes": "75", "hour": "19"}],
        hidden=[{"size": "'S'", "dogs": "1", "minutes": "45", "hour": "6"},
                {"size": "'L'", "dogs": "3", "minutes": "60", "hour": "22"},
                {"size": "'M'", "dogs": "1", "minutes": "60", "hour": "7"},
                {"size": "'X'", "dogs": "2", "minutes": "50", "hour": "21"},
                {"size": "'S'", "dogs": "2", "minutes": "120", "hour": "0"},
                {"size": "'L'", "dogs": "2", "minutes": "90", "hour": "12"}],
        intro="Сервис выгула собак считает цену прогулки. Размер собаки записан буквой в поле `size` (`'S'` — "
              "маленькая, `'M'` — средняя, `'L'` — большая), число собак одного хозяина — в `dogs`, длительность "
              "прогулки в минутах — в `minutes`, час начала прогулки (от 0 до 23) — в `hour`.",
        steps=["Выведи первую строку — число собак, букву размера и длительность прогулки в часах и минутах, "
               "например `Dogs: 2 x M, 1 h 15 min`.",
               "Сделай `switch` по `size` и сохрани в `price` цену прогулки одной собаки за 30 минут: `'S'` — 150, "
               "`'M'` — 200, любая другая буква (`default`) — 250.",
               "Посчитай `total = price * dogs * minutes / 30` — сначала умножай, потом дели: так 45 минут стоят "
               "в полтора раза дороже 30.",
               "Если собак 2 или больше и прогулка длится не меньше 60 минут, уменьши `total` на `total / 10` и "
               "выведи `Discount: 10%`, иначе выведи `Discount: none`.",
               "Если час начала 22 или больше или меньше 7 (ночная прогулка), прибавь к `total` 100 — уже после "
               "скидки. Выведи `Total: … rub`, например `Total: 900 rub`."],
        hint="Часы — это `minutes / 60`, оставшиеся минуты — `minutes % 60`. Буква `size` (тип `char`), склеенная "
             "со строкой, печатается как буква.",
        solution=WALK,
        wrong=[("скидка при одном из условий (|| вместо &&)",
                WALK.replace("dogs >= 2 && minutes >= 60", "dogs >= 2 || minutes >= 60")),
               ("сначала делит минуты на 30: 45 минут считаются как 30",
                WALK.replace("price * dogs * minutes / 30", "price * dogs * (minutes / 30)")),
               ("ночная надбавка только после 22 часов (hour > 22)", WALK.replace("hour >= 22", "hour > 22")),
               ("ночная надбавка прибавлена до скидки, и скидка срезает и её",
                WALK.replace("if (hour >= 22 || hour < 7) { total += 100; }\n", "")
                    .replace("int total = price * dogs * minutes / 30;\n",
                             "int total = price * dogs * minutes / 30;\nif (hour >= 22 || hour < 7) { total += 100; }\n"))],
        constructs=["if"],
        checks=uses_switch("size"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac14-feeder", title="Кормушка для птиц зимой",
        given=[("String", "bird"), ("int", "seeds"), ("int", "temp"), ("boolean", "snow")],
        variants=[{"bird": '"sparrow"', "seeds": "500", "temp": "-12", "snow": "false"}],
        hidden=[{"bird": '"bullfinch"', "seeds": "300", "temp": "-10", "snow": "false"},
                {"bird": '"pigeon"', "seeds": "400", "temp": "-5", "snow": "true"},
                {"bird": '"sparrow"', "seeds": "420", "temp": "0", "snow": "false"},
                {"bird": '"bullfinch"', "seeds": "100", "temp": "-20", "snow": "true"},
                {"bird": '"magpie"', "seeds": "200", "temp": "1", "snow": "false"},
                {"bird": '"crow"', "seeds": "1000", "temp": "2", "snow": "false"},
                {"bird": '"sparrow"', "seeds": "59", "temp": "-3", "snow": "false"}],
        intro="Зимой ты подкармливаешь птиц у окна. Какие птицы прилетают на кормушку, записано строкой в поле `bird`, "
              "сколько граммов семечек осталось — в `seeds`, температура на улице — в `temp`, идёт ли снег — "
              "в `snow` (`true` или `false`).",
        steps=["Сделай `switch` по `bird` и сохрани в `daily`, сколько граммов корма стайка съедает за день: "
               "`\"sparrow\"` — 60, `\"bullfinch\"` — 30, любая другая птица (`default`) — 40.",
               "В мороз (температура −10 и ниже) или в снегопад птицы едят в полтора раза больше: тогда прибавь к "
               "`daily` его половину, `daily / 2` (`+=`).",
               "Выведи птицу, корм на день и корм на неделю (`daily * 7`), например "
               "`sparrow: 90 g a day, 630 g a week`.",
               "Посчитай, на сколько полных дней хватит семечек (`/`) и сколько граммов останется (`%`), и выведи "
               "`Seeds for … days, … g left`, например `Seeds for 5 days, 50 g left`.",
               "Если семечек хватит меньше чем на 7 дней и птицы съедают 60 г в день или больше, выведи "
               "`Buy a big bag`; если меньше чем на 7 дней, но птицы съедают меньше 60 г — `Buy a small bag`; "
               "иначе — `Enough for a week`."],
        hint="Поле `snow` уже имеет тип `boolean`, его можно писать в условии без сравнения: `temp <= -10 || snow`.",
        solution=FEEDER,
        wrong=[("мороз только ниже −10 (temp < -10)", FEEDER.replace("temp <= -10", "temp < -10")),
               ("больше корма только когда и мороз, и снег (&& вместо ||)",
                FEEDER.replace("temp <= -10 || snow", "temp <= -10 && snow")),
               ("большой мешок только больше 60 г в день (daily > 60)", FEEDER.replace("daily >= 60", "daily > 60")),
               ("ровно 7 дней считаются нехваткой (days <= 7)", FEEDER.replace("days < 7 &&", "days <= 7 &&")
                .replace("} else if (days < 7) {", "} else if (days <= 7) {"))],
        constructs=["if"],
        checks=uses_switch("bird"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac14-shelter", title="Новичок в приюте",
        given=[("String", "kind"), ("int", "number"), ("int", "months"), ("boolean", "vaccinated")],
        variants=[{"kind": '"cat"', "number": "21", "months": "14", "vaccinated": "true"}],
        hidden=[{"kind": '"dog"', "number": "8", "months": "3", "vaccinated": "true"},
                {"kind": '"rabbit"', "number": "7", "months": "2", "vaccinated": "true"},
                {"kind": '"dog"', "number": "0", "months": "120", "vaccinated": "false"},
                {"kind": '"cat"', "number": "39", "months": "119", "vaccinated": "true"},
                {"kind": '"parrot"', "number": "16", "months": "30", "vaccinated": "false"},
                {"kind": '"cat"', "number": "15", "months": "1", "vaccinated": "false"}],
        intro="Волонтёр приюта для животных оформляет новичка. Вид животного записан строкой в поле `kind`, его номер "
              "в приюте (номера идут с нуля) — в `number`, возраст в месяцах — в `months`, привито ли животное — "
              "в `vaccinated` (`true` или `false`).",
        steps=["Сделай `switch` по `kind` и сохрани букву блока в переменную `block` типа `char`: `\"cat\"` — `'C'`, "
               "`\"dog\"` — `'D'`, любой другой вид (`default`) — `'S'`.",
               "Клетки в блоке стоят рядами по 8: ряд — `number / 8 + 1`, место в ряду — `number % 8 + 1`. "
               "Собери строку `cage`: буква блока, ряд и место через дефис, например `C-3-6`.",
               "Выведи вид большими буквами, номер и клетку, например `CAT #21: cage C-3-6`.",
               "Карантин длится 14 дней. Если животное привито и ему не меньше 3 месяцев, сократи карантин на 7 дней "
               "(`-=`). Выведи `Quarantine: … days`.",
               "Если животному меньше 3 месяцев или не меньше 120 месяцев (10 лет), выведи `Vet: every week`, иначе — "
               "`Vet: every month`."],
        hint="Дефис пиши в двойных кавычках: `block + \"-\"` — это строка. В одинарных кавычках `'-'` — тоже символ, "
             "и Java сложит два `char` как числа.",
        solution=SHELTER,
        wrong=[("дефис в одинарных кавычках: два char складываются как числа",
                SHELTER.replace('block + "-" + (number', "block + '-' + (number")),
               ("место в ряду без +1: нумерация мест с нуля", SHELTER.replace("(number % 8 + 1)", "(number % 8)")),
               ("карантин короче при одном из условий (|| вместо &&)",
                SHELTER.replace("vaccinated && months >= 3", "vaccinated || months >= 3")),
               ("еженедельный осмотр только старше 120 месяцев (months > 120)",
                SHELTER.replace("months >= 120", "months > 120"))],
        constructs=["if"],
        checks=uses_switch("kind"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac14-incubator", title="Яйца в инкубаторе",
        given=[("String", "bird"), ("int", "day"), ("double", "temp"), ("int", "humidity")],
        variants=[{"bird": '"quail"', "day": "20", "temp": "37.5", "humidity": "70"}],
        hidden=[{"bird": '"chicken"', "day": "9", "temp": "37.2", "humidity": "65"},
                {"bird": '"duck"', "day": "1", "temp": "37.8", "humidity": "50"},
                {"bird": '"goose"', "day": "5", "temp": "38.1", "humidity": "55"},
                {"bird": '"quail"', "day": "14", "temp": "36.9", "humidity": "60"},
                {"bird": '"chicken"', "day": "25", "temp": "37.4", "humidity": "80"},
                {"bird": '"turkey"', "day": "1", "temp": "37.0", "humidity": "66"}],
        intro="На ферме заложили яйца в инкубатор. Птица записана строкой в поле `bird`, день месяца, когда заложили "
              "яйца, — в `day` (считай, что в каждом месяце 30 дней), температура в инкубаторе — дробным числом "
              "в `temp`, влажность в процентах — в `humidity`.",
        steps=["Сделай `switch` по `bird` и сохрани в `period`, сколько дней высиживаются яйца: `\"chicken\"` — 21, "
               "`\"duck\"` — 28, `\"quail\"` — 17, любая другая птица (`default`) — 30.",
               "Выведи птицу и этот срок в полных неделях и оставшихся днях, например `quail: 2 weeks 3 days`.",
               "Посчитай день вылупления `hatch` — `day` плюс срок. Если получилось больше 30, отними от `hatch` 30 "
               "(`-=`) и выведи `Chicks: day … of next month`, иначе выведи `Chicks: day … of this month`.",
               "Если температура от 37.2 до 37.8 включительно, выведи `Temperature: OK`, иначе — "
               "`Temperature: check the heater`.",
               "Если температура выше 37.8 или влажность больше 65, выведи ещё `Open the lid a little`."],
        hint="Полные недели — `period / 7`, оставшиеся дни — `period % 7`. Дробное число сравнивается так же, "
             "как целое: `temp >= 37.2`.",
        solution=INCUBATOR,
        wrong=[("следующий месяц уже с 30-го дня (hatch >= 30)", INCUBATOR.replace("hatch > 30", "hatch >= 30")),
               ("37.2 градуса считаются холодом (temp > 37.2)", INCUBATOR.replace("temp >= 37.2", "temp > 37.2")),
               ("крышку открывает только когда и жарко, и влажно (&& вместо ||)",
                INCUBATOR.replace("temp > 37.8 || humidity > 65", "temp > 37.8 && humidity > 65")),
               ("забыто отнять 30: день вылупления больше 30",
                INCUBATOR.replace("    hatch -= 30;\n", ""))],
        constructs=["if"],
        checks=uses_switch("bird"),
    ),
]
