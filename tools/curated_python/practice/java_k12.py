"""Training attestation («Тренировочная аттестация»), Java, topics 1–12 (up to LOGICAL_AND): println, variables,
assignment, arithmetic, execution order, primitive types (double, boolean, an (int) cast), String (+, toUpperCase,
substring, indexOf), / and %, += -=, if/else, comparison operators, &&. Theme: shopping, online orders and
discounts — every story is different, and different from the attestation pool. Each reference solution uses every
topic in a natural way; hidden value sets hit both sides of every part of the && condition and its boundaries.
Not yet: || and !, switch, loops, arrays, own methods and classes, equals."""
import textwrap

from java_tasks import JavaOutputTask

SKILL = "LOGICAL_AND"


def code(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


def swap(text: str, old: str, new: str) -> str:
    assert old in text, old
    return text.replace(old, new)


BOXES = code("""
    String login = email.substring(0, email.indexOf("@"));
    int total = items * itemPrice;
    int boxes = items / 6;
    int extra = items % 6;
    double kg = items * itemWeight / 1000.0;
    String delivery = "";
    if (total >= 5000 && kg <= 20) {
        delivery = "free";
    } else {
        delivery = "500 rub";
        total += 500;
    }
    System.out.println("Customer: " + login);
    System.out.println("Boxes: " + boxes + " full + " + extra + " items");
    System.out.println("Weight: " + kg + " kg");
    System.out.println("Delivery: " + delivery);
    System.out.println("To pay: " + total + " rub");
""")

INSTALMENT = code("""
    String name = item.substring(0, 1).toUpperCase() + item.substring(1);
    boolean noFee = price >= 20000 && months <= 6;
    int total = price;
    String plan = "";
    if (noFee) {
        plan = "no fee";
    } else {
        plan = "plus 10%";
        total += total / 10;
    }
    int monthly = total / months;
    int last = monthly + total % months;
    System.out.println("Item: " + name);
    System.out.println("Plan: " + plan);
    System.out.println("Total: " + total + " rub");
    System.out.println("Payments: " + (months - 1) + " x " + monthly + " rub");
    System.out.println("Last payment: " + last + " rub");
""")

INSTALMENT_EARLY = code("""
    String name = item.substring(0, 1).toUpperCase() + item.substring(1);
    boolean noFee = price >= 20000 && months <= 6;
    int total = price;
    int monthly = total / months;
    int last = monthly + total % months;
    String plan = "";
    if (noFee) {
        plan = "no fee";
    } else {
        plan = "plus 10%";
        total += total / 10;
    }
    System.out.println("Item: " + name);
    System.out.println("Plan: " + plan);
    System.out.println("Total: " + total + " rub");
    System.out.println("Payments: " + (months - 1) + " x " + monthly + " rub");
    System.out.println("Last payment: " + last + " rub");
""")

SCALES = code("""
    String label = product.substring(0, 3).toUpperCase();
    double kg = grams / 1000.0;
    int kop = grams * pricePerKg / 10;
    String price = "";
    if (hour >= 20 && grams >= 1000) {
        price = "evening -25%";
        kop -= kop / 4;
    } else {
        price = "regular";
    }
    int rub = kop / 100;
    int rest = kop % 100;
    System.out.println("Code: " + label);
    System.out.println("Weight: " + kg + " kg");
    System.out.println("Price: " + price);
    System.out.println("To pay: " + rub + " rub " + rest + " kop");
""")

SCALES_EARLY = code("""
    String label = product.substring(0, 3).toUpperCase();
    double kg = grams / 1000.0;
    int kop = grams * pricePerKg / 10;
    int rub = kop / 100;
    int rest = kop % 100;
    String price = "";
    if (hour >= 20 && grams >= 1000) {
        price = "evening -25%";
        kop -= kop / 4;
    } else {
        price = "regular";
    }
    System.out.println("Code: " + label);
    System.out.println("Weight: " + kg + " kg");
    System.out.println("Price: " + price);
    System.out.println("To pay: " + rub + " rub " + rest + " kop");
""")

HALF = code("""
    int pairs = qty / 2;
    int single = qty % 2;
    double cost = pairs * price * 1.5 + single * price;
    int pay = (int) cost;
    String coupon = "";
    if (pay >= 2000 && day <= 15) {
        coupon = "applied";
        pay -= 300;
    } else {
        coupon = "not valid";
    }
    System.out.println("Receipt for " + buyer.toUpperCase());
    System.out.println("Pairs: " + pairs + ", single: " + single);
    System.out.println("Cost: " + cost + " rub");
    System.out.println("Coupon: " + coupon);
    System.out.println("To pay: " + pay + " rub");
""")

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac12-boxes", title="Заказ уезжает со склада",
        given=[("String", "email"), ("int", "items"), ("int", "itemPrice"), ("int", "itemWeight")],
        variants=[{"email": '"anya@mail.ru"', "items": "14", "itemPrice": "450", "itemWeight": "750"}],
        hidden=[{"email": '"boris@post.ru"', "items": "10", "itemPrice": "500", "itemWeight": "1000"},
                {"email": '"dima.ivanov@mail.ru"', "items": "9", "itemPrice": "555", "itemWeight": "500"},
                {"email": '"lena@gmail.com"', "items": "16", "itemPrice": "400", "itemWeight": "1250"},
                {"email": '"oleg77@mail.ru"', "items": "12", "itemPrice": "1000", "itemWeight": "1750"},
                {"email": '"kira@ya.ru"', "items": "3", "itemPrice": "900", "itemWeight": "8000"}],
        intro="Склад интернет-магазина собирает заказ. Почта покупателя записана в поле `email`, сколько одинаковых "
              "товаров он заказал — в поле `items`, цена одного товара в рублях — в поле `itemPrice`, вес одного "
              "товара в граммах — в поле `itemWeight`. В одну коробку помещается 6 товаров. Доставка бесплатная, если "
              "заказ стоит не меньше 5000 руб. и весит не больше 20 кг, иначе она стоит 500 руб.",
        steps=["Имя покупателя — часть почты до знака `@`: `email.substring(0, email.indexOf(\"@\"))`.",
               "Посчитай стоимость заказа: `items * itemPrice`.",
               "Раздели товары на полные коробки по 6 штук (`/ 6`) и товары, которые остались сверх них (`% 6`).",
               "Посчитай вес заказа в килограммах в переменной типа `double`: `items * itemWeight / 1000.0`.",
               "Если стоимость не меньше 5000 **и** вес не больше 20 кг, доставка — `free`. Иначе доставка — "
               "`500 rub`, и к стоимости прибавь 500 через `+=`. Обе проверки — в одном условии через `&&`.",
               "Выведи пять строк: `Customer: …` (имя из почты), `Boxes: … full + … items`, `Weight: … kg`, "
               "`Delivery: …`, `To pay: … rub`."],
        hint="Точка в `1000.0` делает деление дробным: `10500 / 1000.0` — это `10.5`, а `10500 / 1000` — просто `10`. "
             "Заказ ровно на 5000 руб. или ровно в 20 кг ещё везут бесплатно.",
        solution=BOXES,
        wrong=[("> 5000 вместо >= 5000: заказ ровно на 5000 руб. платит за доставку",
                swap(BOXES, "total >= 5000", "total > 5000")),
               ("|| вместо &&: бесплатно везут и дешёвый заказ, и слишком тяжёлый",
                swap(BOXES, "total >= 5000 && kg <= 20", "total >= 5000 || kg <= 20")),
               ("вес через / 1000: целое деление теряет граммы",
                swap(BOXES, "items * itemWeight / 1000.0", "items * itemWeight / 1000"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac12-instalment", title="Рассрочка на технику",
        given=[("String", "item"), ("int", "price"), ("int", "months")],
        variants=[{"item": '"laptop"', "price": "45990", "months": "4"}],
        hidden=[{"item": '"phone"', "price": "20000", "months": "6"},
                {"item": '"tablet"', "price": "19999", "months": "3"},
                {"item": '"camera"', "price": "36000", "months": "7"},
                {"item": '"printer"', "price": "80000", "months": "12"},
                {"item": '"drone"', "price": "30500", "months": "5"},
                {"item": '"fridge"', "price": "15000", "months": "10"}],
        intro="Интернет-магазин продаёт технику в рассрочку. Название товара записано в поле `item`, цена в рублях — "
              "в поле `price`, на сколько месяцев оформлена рассрочка — в поле `months`. Без переплаты рассрочку дают "
              "на покупку от 20000 руб. и не больше чем на 6 месяцев, иначе к цене добавляется 10 процентов. Платить "
              "нужно каждый месяц поровну, а то, что не делится поровну, добавляется к последнему платежу.",
        steps=["Сделай название с большой буквы: первую букву `item.substring(0, 1)` переведи в верхний регистр "
               "через `toUpperCase()` и приклей к ней остаток названия `item.substring(1)`.",
               "Заведи переменную типа `boolean` с именем `noFee`: цена не меньше 20000 **и** месяцев не больше 6 — "
               "одно выражение через `&&`.",
               "Заведи `total`, равную цене. Если `noFee` истинно, план — `no fee`. Иначе план — `plus 10%`, "
               "и к `total` прибавь его десятую часть (`total / 10`) через `+=`.",
               "После условия посчитай обычный платёж за месяц: `total / months`. Последний платёж — это обычный "
               "платёж плюс остаток `total % months`.",
               "Выведи пять строк: `Item: …`, `Plan: …`, `Total: … rub`, `Payments: … x … rub` (сначала число "
               "обычных платежей — на один меньше, чем месяцев, — потом сумма одного платежа), `Last payment: … rub`."],
        hint="Переменная типа `boolean` сама является условием: `if (noFee)`. Число `months - 1` внутри строки возьми "
             "в скобки, иначе Java начнёт склеивать текст. Покупка ровно на 20000 руб. на 6 месяцев — ещё без переплаты.",
        solution=INSTALMENT,
        wrong=[("< 6 вместо <= 6: рассрочка ровно на 6 месяцев идёт с переплатой",
                swap(INSTALMENT, "months <= 6", "months < 6")),
               ("|| вместо &&: без переплаты и дешёвая покупка, и долгая рассрочка",
                swap(INSTALMENT, "price >= 20000 && months <= 6", "price >= 20000 || months <= 6")),
               ("платежи посчитаны до того, как к цене добавили 10 процентов", INSTALMENT_EARLY)],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac12-scales", title="Весы в овощном отделе",
        given=[("String", "product"), ("int", "grams"), ("int", "pricePerKg"), ("int", "hour")],
        variants=[{"product": '"tomatoes"', "grams": "1340", "pricePerKg": "189", "hour": "21"}],
        hidden=[{"product": '"apples"', "grams": "1000", "pricePerKg": "120", "hour": "20"},
                {"product": '"bananas"', "grams": "999", "pricePerKg": "150", "hour": "22"},
                {"product": '"carrots"', "grams": "2500", "pricePerKg": "60", "hour": "19"},
                {"product": '"lemons"', "grams": "480", "pricePerKg": "299", "hour": "10"},
                {"product": '"grapes"', "grams": "1875", "pricePerKg": "340", "hour": "23"}],
        intro="Покупатель кладёт овощи или фрукты на весы в магазине, и весы печатают наклейку. Название товара записано в поле "
              "`product`, вес в граммах — в поле `grams`, цена за килограмм в рублях — в поле `pricePerKg`, который "
              "сейчас час (от 0 до 23) — в поле `hour`. С 20 часов на покупку от 1 кг действует вечерняя скидка "
              "25 процентов.",
        steps=["Код товара — первые три буквы названия большими буквами: `product.substring(0, 3)`, затем "
               "`toUpperCase()`.",
               "Запиши вес в килограммах в переменную типа `double`: `grams / 1000.0`.",
               "Посчитай цену покупки в копейках целым числом: `grams * pricePerKg / 10` (в рубле 100 копеек, "
               "в килограмме 1000 граммов).",
               "Если сейчас не меньше 20 часов **и** вес не меньше 1000 граммов, цена — `evening -25%`, и из копеек "
               "вычти их четверть (`/ 4`) через `-=`. Иначе цена — `regular`. Обе проверки — в одном условии через `&&`.",
               "После условия раздели копейки на рубли (`/ 100`) и оставшиеся копейки (`% 100`).",
               "Выведи четыре строки: `Code: …`, `Weight: … kg`, `Price: …`, `To pay: … rub … kop`."],
        hint="Порядок строк важен: сначала скидка, потом рубли и копейки — иначе на наклейке окажется цена без скидки. "
             "Ровно в 20 часов и ровно за 1 кг скидка уже действует.",
        solution=SCALES,
        wrong=[("> 20 вместо >= 20: в 20 часов скидки ещё нет",
                swap(SCALES, "hour >= 20", "hour > 20")),
               ("|| вместо &&: скидка и днём, и на маленький вес",
                swap(SCALES, "hour >= 20 && grams >= 1000", "hour >= 20 || grams >= 1000")),
               ("рубли и копейки посчитаны до скидки", SCALES_EARLY)],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac12-halfprice", title="Второй товар за полцены",
        given=[("String", "buyer"), ("int", "price"), ("int", "qty"), ("int", "day")],
        variants=[{"buyer": '"Vera"', "price": "1299", "qty": "3", "day": "12"}],
        hidden=[{"buyer": '"Ilya"', "price": "1333", "qty": "2", "day": "3"},
                {"buyer": '"Nina"', "price": "800", "qty": "3", "day": "10"},
                {"buyer": '"Pasha"', "price": "2490", "qty": "4", "day": "15"},
                {"buyer": '"Rita"', "price": "999", "qty": "5", "day": "16"},
                {"buyer": '"Sasha"', "price": "4999", "qty": "1", "day": "20"},
                {"buyer": '"Timur"', "price": "1555", "qty": "6", "day": "1"}],
        intro="В магазине одежды акция: в каждой паре одинаковых товаров второй стоит полцены. А ещё у покупателя есть "
              "купон на 300 руб.: он действует до 15-го числа включительно и только для покупки от 2000 руб. Имя "
              "покупателя записано в поле `buyer`, цена одного товара в рублях — в поле `price`, сколько одинаковых "
              "товаров он берёт — в поле `qty`, какое сегодня число месяца — в поле `day`.",
        steps=["Посчитай `pairs` — сколько пар складывается из товаров (`qty / 2`), и `single` — сколько товаров "
               "остаётся без пары (`qty % 2`).",
               "Стоимость — дробное число типа `double`: каждая пара стоит полторы цены (`pairs * price * 1.5`), "
               "к этому прибавь цену товаров без пары (`single * price`).",
               "Сумма к оплате — целые рубли: приведи стоимость к `int` через `(int)` (копейки магазин не берёт).",
               "Если сумма к оплате не меньше 2000 **и** сегодня не позже 15-го числа, купон — `applied`, и из суммы "
               "вычти 300 через `-=`. Иначе купон — `not valid`. Обе проверки — в одном условии через `&&`.",
               "Выведи пять строк: `Receipt for …` (имя большими буквами), `Pairs: …, single: …`, `Cost: … rub` "
               "(дробная стоимость), `Coupon: …`, `To pay: … rub`."],
        hint="`(int)` отбрасывает дробную часть, не округляя: из 3247.5 получится 3247. Пятнадцатого числа купон ещё "
             "действует.",
        solution=HALF,
        wrong=[("< 15 вместо <= 15: пятнадцатого числа купон уже не действует",
                swap(HALF, "day <= 15", "day < 15")),
               ("|| вместо &&: купон срабатывает и после 15-го, и на маленькую покупку",
                swap(HALF, "pay >= 2000 && day <= 15", "pay >= 2000 || day <= 15")),
               ("pay =- 300 вместо pay -= 300: в сумму записывается минус 300",
                swap(HALF, "pay -= 300;", "pay =- 300;"))],
        constructs=["if"],
    ),
]
