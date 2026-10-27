"""Attestation tier Java, topics 1–14 (up to SWITCH_BASIC «Оператор switch»). Every story is one integrative «Напиши код»
task for about 10 minutes that uses: println, variables, assignment, arithmetic, execution order, primitive types
(char / double with an (int) cast / boolean), String (gluing with +, toUpperCase), / and %, += -= ++, if/else,
comparisons, &&, || (and !), switch with default. Theme: food, cafes and cooking — every story different.
Not yet: loops (for, while), arrays, own methods and classes, equals on strings (strings are compared only in switch)."""
from java_tasks import JavaOutputTask
from topics_java.t22_switch import uses_switch

SKILL = "SWITCH_BASIC"

COFFEE = """int price;
switch (drink) {
    case "latte": price = 180; break;
    case "cappuccino": price = 170; break;
    default: price = 120;
}
if (size == 'L') { price += 40; }
int total = price * cups;
if (hour >= 8 && hour < 10) { total -= total / 10; }
System.out.println(drink.toUpperCase() + " " + size + " x" + cups + ": " + total + " rub");
if (cups >= 4 || total >= 500) {
    System.out.println("Gift: cookie");
} else {
    System.out.println("Gift: none");
}"""

PIZZA = """int slices = guests * 3;
int pizzas = slices / 8;
if (slices % 8 > 0) { pizzas++; }
int price;
switch (kind) {
    case "margherita": price = 450; break;
    case "pepperoni": price = 550; break;
    default: price = 500;
}
int total = pizzas * price;
boolean freeDelivery = total >= 2000 && distanceKm <= 5;
if (!freeDelivery) { total += 200; }
System.out.println("Pizzas: " + pizzas + " x " + kind + ", total: " + total + " rub");
if (guests >= 10 || total >= 2300) {
    System.out.println("Bonus: tiramisu");
} else {
    System.out.println("Bonus: none");
}"""

OVEN = """int cook;
switch (dish) {
    case "soup": cook = 40; break;
    case "pie": cook = 50; break;
    default: cook = 30;
}
int ready = hour * 60 + minute + cook;
String time = ready / 60 + ":";
if (ready % 60 < 10) { time += "0"; }
time += ready % 60;
System.out.println(dish + " ready at " + time);
boolean dinner = ready / 60 >= 18 && ready / 60 < 21;
if (dinner) {
    System.out.println("Just in time for dinner");
} else {
    System.out.println("Not dinner time");
}
if (ready / 60 >= 22 || ready / 60 < 7) { System.out.println("Cook quietly, everyone is asleep"); }"""

BAKERY = """int grams;
switch (bread) {
    case "rye": grams = 400; break;
    case "wheat": grams = 500; break;
    default: grams = 300;
}
int flour = (int) (flourKg * 1000);
flour -= 200;
int loaves = flour / grams;
System.out.println(bread + ": " + loaves + " loaves, " + flour % grams + " g left");
if (loaves >= orders) {
    System.out.println("Orders: done");
} else {
    System.out.println("Orders: short by " + (orders - loaves));
}
if (loaves >= orders && flour % grams == 0) { System.out.println("No flour wasted"); }
if (loaves < orders || flour % grams < 100) { System.out.println("Buy flour today"); }"""

BILL = """int sum = bill;
if (hour >= 12 && hour < 16) { sum -= sum / 5; }
int percent;
switch (service) {
    case 'A', 'a': percent = 15; break;
    case 'B', 'b': percent = 10; break;
    default: percent = 5;
}
if (people >= 6 || sum >= 5000) { percent += 5; }
int total = sum + sum * percent / 100;
System.out.println("Total: " + total + " rub, each pays " + total / people + " rub");
if (total % people > 0) {
    System.out.println("Left to pay: " + total % people + " rub");
} else {
    System.out.println("Split evenly");
}"""

PANCAKES = """double milk = portions * 0.25;
int eggs = portions / 2 + portions % 2;
System.out.println("Milk: " + milk + " l, eggs: " + eggs);
int price;
switch (topping) {
    case "jam": price = 20; break;
    case "honey": price = 30; break;
    default: price = 0;
}
int cost = price * portions;
if (price > 0 && portions >= 5) { cost -= 20; }
System.out.println("Topping: " + cost + " rub");
if (eggs > eggsAtHome || price > 0) {
    System.out.println("Shop: needed");
} else {
    System.out.println("Shop: not needed");
}"""


TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att14-coffee", title="Заказ в кофейне",
        given=[("String", "drink"), ("char", "size"), ("int", "cups"), ("int", "hour")],
        variants=[{"drink": '"latte"', "size": "'L'", "cups": "3", "hour": "9"}],
        hidden=[{"drink": '"espresso"', "size": "'S'", "cups": "4", "hour": "10"},
                {"drink": '"cappuccino"', "size": "'S'", "cups": "3", "hour": "8"},
                {"drink": '"cappuccino"', "size": "'S'", "cups": "3", "hour": "10"},
                {"drink": '"tea"', "size": "'L'", "cups": "1", "hour": "7"},
                {"drink": '"mocha"', "size": "'S'", "cups": "2", "hour": "12"}],
        intro="Кассир кофейни пробивает заказ. Напиток записан строкой в поле `drink`, размер стакана — символом в поле "
              "`size` (`'S'` — маленький, `'L'` — большой), число стаканов — в `cups`, час заказа (от 0 до 23) — в `hour`.",
        steps=["Сделай `switch` по `drink` и сохрани цену одного стакана в `price`: `\"latte\"` — 180, "
               "`\"cappuccino\"` — 170, любой другой напиток (`default`) — 120.",
               "Если `size` равен `'L'`, прибавь к `price` 40.",
               "Посчитай `total` — цену всех стаканов. Если час заказа от 8 включительно до 10 не включая, уменьши "
               "`total` на `total / 10` (утренняя скидка).",
               "Выведи напиток большими буквами, пробел, размер, ` x` с числом стаканов, двоеточие и сумму, "
               "например `LATTE L x3: 594 rub`.",
               "Если стаканов 4 или больше или `total` не меньше 500, выведи `Gift: cookie`, иначе — `Gift: none`."],
        hint="Большие буквы даёт `drink.toUpperCase()`. Не забудь `break` в каждой ветке `case`.",
        solution=COFFEE,
        wrong=[("утренняя скидка и в 10 часов (hour <= 10)", COFFEE.replace("hour < 10", "hour <= 10")),
               ("подарок только когда выполнены оба условия (&& вместо ||)",
                COFFEE.replace("cups >= 4 || total >= 500", "cups >= 4 && total >= 500")),
               ("забыта надбавка за большой стакан", COFFEE.replace("if (size == 'L') { price += 40; }\n", ""))],
        constructs=["if"],
        checks=uses_switch("drink"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att14-pizza", title="Пицца на вечеринку",
        given=[("int", "guests"), ("String", "kind"), ("int", "distanceKm")],
        variants=[{"guests": "7", "kind": '"pepperoni"', "distanceKm": "4"}],
        hidden=[{"guests": "9", "kind": '"hawaiian"', "distanceKm": "5"},
                {"guests": "9", "kind": '"pepperoni"', "distanceKm": "6"},
                {"guests": "9", "kind": '"pepperoni"', "distanceKm": "3"},
                {"guests": "16", "kind": '"margherita"', "distanceKm": "2"},
                {"guests": "1", "kind": '"margherita"', "distanceKm": "0"},
                {"guests": "10", "kind": '"margherita"', "distanceKm": "2"}],
        intro="Ты заказываешь пиццу на вечеринку. Число гостей записано в поле `guests`, вид пиццы — строкой в поле "
              "`kind`, расстояние до пиццерии в километрах — в `distanceKm`. В пицце 8 кусков, каждый гость съест 3 куска.",
        steps=["Посчитай нужные куски и число целых пицц: куски `/ 8`. Если остаток от деления кусков на 8 больше "
               "нуля, добавь ещё одну пиццу (`++`).",
               "Сделай `switch` по `kind` и узнай цену пиццы: `\"margherita\"` — 450, `\"pepperoni\"` — 550, "
               "любая другая (`default`) — 500. Посчитай `total` — цену всех пицц.",
               "Доставка бесплатна, если `total` не меньше 2000 и расстояние не больше 5 км; иначе прибавь к `total` 200.",
               "Выведи `Pizzas: … x …, total: … rub` (число пицц, вид, сумма), например "
               "`Pizzas: 3 x pepperoni, total: 1850 rub`.",
               "Если гостей 10 или больше или `total` (уже с доставкой) не меньше 2300, выведи `Bonus: tiramisu`, "
               "иначе — `Bonus: none`."],
        hint="Условие бесплатной доставки удобно сохранить в переменную `boolean`, а доставку добавлять, когда она "
             "не бесплатна: `!freeDelivery`.",
        solution=PIZZA,
        wrong=[("всегда добавляет лишнюю пиццу, даже когда куски делятся поровну",
                PIZZA.replace("if (slices % 8 > 0) { pizzas++; }", "pizzas++;")),
               ("бесплатная доставка при одном из условий (|| вместо &&)",
                PIZZA.replace("total >= 2000 && distanceKm <= 5", "total >= 2000 || distanceKm <= 5")),
               ("граница расстояния строгая: ровно 5 км уже платно",
                PIZZA.replace("distanceKm <= 5", "distanceKm < 5"))],
        constructs=["if"],
        checks=uses_switch("kind"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att14-oven", title="Когда будет готов ужин",
        given=[("String", "dish"), ("int", "hour"), ("int", "minute")],
        variants=[{"dish": '"soup"', "hour": "17", "minute": "35"}],
        hidden=[{"dish": '"pasta"', "hour": "20", "minute": "35"},
                {"dish": '"pie"', "hour": "17", "minute": "10"},
                {"dish": '"soup"', "hour": "21", "minute": "20"},
                {"dish": '"omelette"', "hour": "5", "minute": "45"},
                {"dish": '"pie"', "hour": "6", "minute": "10"},
                {"dish": '"soup"', "hour": "20", "minute": "0"}],
        intro="Ты начинаешь готовить и хочешь знать, когда блюдо будет готово. Блюдо записано строкой в поле `dish`, "
              "время начала — в полях `hour` (часы) и `minute` (минуты). Блюдо всегда готово в тот же день.",
        steps=["Сделай `switch` по `dish` и сохрани время готовки в минутах в `cook`: `\"soup\"` — 40, `\"pie\"` — 50, "
               "любое другое блюдо (`default`) — 30.",
               "Посчитай `ready` — минуты от полуночи до готовности. Час готовности — `ready / 60`, минуты — `ready % 60`.",
               "Собери строку времени: час и двоеточие; если минут меньше 10, допиши `0` (`+=`); затем допиши минуты. "
               "Выведи `… ready at …`, например `soup ready at 18:15` или `pasta ready at 21:05`.",
               "Если час готовности от 18 включительно до 21 не включая, выведи `Just in time for dinner`, иначе — "
               "`Not dinner time`.",
               "Если час готовности 22 или больше или меньше 7, выведи ещё `Cook quietly, everyone is asleep`."],
        hint="Число, склеенное со строкой, становится текстом: `ready / 60 + \":\"` даёт, например, `\"18:\"`.",
        solution=OVEN,
        wrong=[("нет ведущего нуля: 21:05 печатается как 21:5",
                OVEN.replace("if (ready % 60 < 10) { time += \"0\"; }\n", "")),
               ("ужин включает и 21 час (<= 21)", OVEN.replace("ready / 60 < 21", "ready / 60 <= 21")),
               ("«ночь» только при обоих условиях (&& вместо ||)",
                OVEN.replace("ready / 60 >= 22 || ready / 60 < 7", "ready / 60 >= 22 && ready / 60 < 7"))],
        constructs=["if"],
        checks=uses_switch("dish"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att14-bakery", title="Хлеб из запаса муки",
        given=[("String", "bread"), ("double", "flourKg"), ("int", "orders")],
        variants=[{"bread": '"wheat"', "flourKg": "5.25", "orders": "12"}],
        hidden=[{"bread": '"bun"', "flourKg": "2.0", "orders": "6"},
                {"bread": '"rye"', "flourKg": "3.5", "orders": "6"},
                {"bread": '"rye"', "flourKg": "1.0", "orders": "3"},
                {"bread": '"wheat"', "flourKg": "1.25", "orders": "1"},
                {"bread": '"pretzel"', "flourKg": "1.5", "orders": "2"},
                {"bread": '"pretzel"', "flourKg": "1.5", "orders": "5"}],
        intro="Пекарь решает, сколько буханок испечь. Сорт хлеба записан строкой в поле `bread`, запас муки в "
              "килограммах — дробным числом в поле `flourKg`, число заказанных буханок — в `orders`.",
        steps=["Сделай `switch` по `bread` и узнай граммы муки на буханку: `\"rye\"` — 400, `\"wheat\"` — 500, "
               "любой другой сорт (`default`) — 300.",
               "Переведи муку в граммы целым числом: `(int) (flourKg * 1000)`, затем отними 200 г на подсыпку стола (`-=`).",
               "Посчитай целые буханки (`/`) и выведи `…: … loaves, … g left` — сорт, буханки и остаток муки (`%`), "
               "например `wheat: 10 loaves, 50 g left`.",
               "Если буханок хватает на заказы, выведи `Orders: done`, иначе — `Orders: short by …` (сколько не хватает).",
               "Если буханок хватает и остаток муки ровно 0, выведи `No flour wasted`. Если буханок не хватает или "
               "остаток меньше 100 г, выведи `Buy flour today`."],
        hint="Скобки в `(int) (flourKg * 1000)` важны: без них сначала отбросится дробная часть килограммов.",
        solution=BAKERY,
        wrong=[("приведение к int без скобок: дробная часть килограммов теряется",
                BAKERY.replace("(int) (flourKg * 1000)", "(int) flourKg * 1000")),
               ("мука на исходе уже при 100 г (<= 100)", BAKERY.replace("flour % grams < 100", "flour % grams <= 100")),
               ("покупать муку только при обоих условиях (&& вместо ||)",
                BAKERY.replace("loaves < orders || flour", "loaves < orders && flour"))],
        constructs=["if"],
        checks=uses_switch("bread"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att14-bill", title="Счёт в кафе на компанию",
        given=[("char", "service"), ("int", "bill"), ("int", "people"), ("int", "hour")],
        variants=[{"service": "'b'", "bill": "4200", "people": "5", "hour": "13"}],
        hidden=[{"service": "'A'", "bill": "6000", "people": "3", "hour": "16"},
                {"service": "'a'", "bill": "2000", "people": "6", "hour": "12"},
                {"service": "'C'", "bill": "1000", "people": "4", "hour": "11"},
                {"service": "'B'", "bill": "5000", "people": "2", "hour": "15"},
                {"service": "'x'", "bill": "5000", "people": "1", "hour": "18"}],
        intro="Компания друзей пообедала в кафе и делит счёт поровну. Сумма по меню записана в поле `bill`, число "
              "людей — в `people`, час (от 0 до 23) — в `hour`, а оценка обслуживания — буквой в поле `service` "
              "(заглавной или строчной).",
        steps=["Заведи `sum` со значением `bill`. Если час от 12 включительно до 16 не включая (бизнес-ланч), "
               "уменьши `sum` на `sum / 5`.",
               "Сделай `switch` по `service` и выбери процент чаевых `percent`: `'A'` или `'a'` — 15, "
               "`'B'` или `'b'` — 10, любая другая буква (`default`) — 5.",
               "Если людей 6 или больше или `sum` не меньше 5000, прибавь к `percent` 5.",
               "Сумма с чаевыми: `sum + sum * percent / 100`. Выведи `Total: … rub, each pays … rub` "
               "(доля каждого — целочисленное деление), например `Total: 3696 rub, each pays 739 rub`.",
               "Если от деления остаются рубли, выведи `Left to pay: … rub` (остаток), иначе — `Split evenly`."],
        hint="Несколько значений в одной ветке пишутся через запятую: `case 'A', 'a':`.",
        solution=BILL,
        wrong=[("ланч до 16 часов включительно (hour <= 16)", BILL.replace("hour < 16", "hour <= 16")),
               ("в switch только заглавные буквы", BILL.replace("'A', 'a'", "'A'").replace("'B', 'b'", "'B'")),
               ("надбавка только при обоих условиях (&& вместо ||)",
                BILL.replace("people >= 6 || sum >= 5000", "people >= 6 && sum >= 5000"))],
        constructs=["if"],
        checks=uses_switch("service"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att14-pancakes", title="Блины на завтрак",
        given=[("int", "portions"), ("String", "topping"), ("int", "eggsAtHome")],
        variants=[{"portions": "5", "topping": '"honey"', "eggsAtHome": "2"}],
        hidden=[{"portions": "4", "topping": '"jam"', "eggsAtHome": "2"},
                {"portions": "6", "topping": '"plain"', "eggsAtHome": "5"},
                {"portions": "1", "topping": '"nothing"', "eggsAtHome": "0"},
                {"portions": "5", "topping": '"jam"', "eggsAtHome": "3"},
                {"portions": "7", "topping": '"plain"', "eggsAtHome": "3"}],
        intro="Ты печёшь блины на завтрак. Число порций записано в поле `portions`, начинка — строкой в поле "
              "`topping`, сколько яиц есть дома — в `eggsAtHome`.",
        steps=["На порцию нужно 0.25 л молока (переменная `double`), а яиц — одно на каждые две порции с округлением "
               "вверх: `portions / 2 + portions % 2`. Выведи `Milk: … l, eggs: …`, например `Milk: 1.25 l, eggs: 3`.",
               "Сделай `switch` по `topping` и узнай цену начинки на порцию: `\"jam\"` — 20, `\"honey\"` — 30, "
               "любая другая (`default`) — 0. Стоимость начинки — цена, умноженная на `portions`.",
               "Если начинка платная (цена больше 0) и порций не меньше 5, уменьши стоимость на 20 (купон). "
               "Выведи `Topping: … rub`.",
               "Если нужно больше яиц, чем есть дома, или начинка платная, выведи `Shop: needed`, иначе — "
               "`Shop: not needed`."],
        hint="Число `double` печатается с точкой: `1.0`, `1.25` — так и нужно.",
        solution=PANCAKES,
        wrong=[("яйца без округления вверх: portions / 2", PANCAKES.replace(" + portions % 2", "")),
               ("купон и для бесплатной начинки: стоимость уходит в минус",
                PANCAKES.replace("price > 0 && portions >= 5", "portions >= 5")),
               ("магазин нужен только при обоих условиях (&& вместо ||)",
                PANCAKES.replace("eggs > eggsAtHome || price > 0", "eggs > eggsAtHome && price > 0"))],
        constructs=["if"],
        checks=uses_switch("topping"),
    ),
]
