"""METHOD_PARAMETERS — «Параметры и возвращаемое значение» (Java): несколько параметров разных типов, их порядок,
возврат int или String через return. Taught before: everything up to own static methods (conditions, loops, arrays,
/ and %, strings). Not yet: own classes."""
from java_tasks import JavaFunctionTask

SKILL = "METHOD_PARAMETERS"

TASKS = [
    JavaFunctionTask(
        skill=SKILL, difficulty=1, slug="java-mp-pizza-order", title="Заказ в пиццерии",
        function="orderCost",
        variants=[{"pizza": 450, "drink": 120}, {"pizza": 520, "drink": 90}, {"pizza": 390, "drink": 150}],
        intro="В пиццерии одна пицца стоит {pizza} руб., а напиток — {drink} руб. Кассиру нужен метод, который "
              "по количеству пицц и напитков считает сумму заказа.",
        steps=["Допиши метод `orderCost(int pizzas, int drinks)`: параметр `pizzas` — сколько заказали пицц, "
               "`drinks` — сколько напитков.",
               "Верни стоимость заказа в рублях: {pizza} руб. за каждую пиццу плюс {drink} руб. за каждый напиток.",
               "Не меняй порядок параметров: в вызове `orderCost(2, 3)` первое число — это пиццы, второе — напитки."],
        hint="Параметры — это обычные переменные внутри метода, только их значения приходят из вызова: "
             "при вызове `orderCost(2, 3)` переменная `pizzas` получит 2, а `drinks` — 3.",
        starter="public class Solution {{\n    static int orderCost(int pizzas, int drinks) {{\n"
                "        // Напиши решение здесь\n        return 0;\n    }}\n}}\n",
        solution="public class Solution {{\n    static int orderCost(int pizzas, int drinks) {{\n"
                 "        return pizzas * {pizza} + drinks * {drink};\n    }}\n}}\n",
        inputs=["2, 3", "1, 0", "0, 4", "3, 1", "5, 5", "0, 0", "4, 2"],
        wrong=[("переставил параметры местами: пиццы считаются как напитки",
                "public class Solution {{\n    static int orderCost(int drinks, int pizzas) {{\n"
                "        return pizzas * {pizza} + drinks * {drink};\n    }}\n}}\n"),
               ("считает напитки по цене пиццы",
                "public class Solution {{\n    static int orderCost(int pizzas, int drinks) {{\n"
                "        return (pizzas + drinks) * {pizza};\n    }}\n}}\n")],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=2, slug="java-mp-test-result", title="Результат теста",
        function="testResult",
        variants=[{"pass": 60}, {"pass": 70}, {"pass": 50}],
        intro="После онлайн-теста каждый ученик видит строку со своим результатом. Зачёт ставят, если правильных "
              "ответов {pass}% или больше.",
        steps=["Допиши метод `testResult(String name, int correct, int total)`: `name` — имя ученика, `correct` — "
               "сколько верных ответов, `total` — сколько всего было вопросов (всегда больше 0).",
               "Посчитай процент правильных ответов целым числом, дробную часть отбрось: например, 7 верных из 9 — это 77%.",
               "Если процент {pass} или больше, верни строку вида `Anya: pass (80%)`, иначе — `Anya: fail (40%)`, "
               "с именем и процентом этого ученика."],
        hint="Следи за порядком действий: при делении целых чисел дробная часть отбрасывается сразу, поэтому "
             "`7 / 10 * 100` даёт 0, а `7 * 100 / 10` — 70.",
        starter="public class Solution {{\n    static String testResult(String name, int correct, int total) {{\n"
                "        // Напиши решение здесь\n        return \"\";\n    }}\n}}\n",
        solution="public class Solution {{\n    static String testResult(String name, int correct, int total) {{\n"
                 "        int percent = correct * 100 / total;\n        if (percent >= {pass}) {{\n"
                 "            return name + \": pass (\" + percent + \"%)\";\n        }}\n"
                 "        return name + \": fail (\" + percent + \"%)\";\n    }}\n}}\n",
        inputs=['"Anya", 8, 10', '"Boris", 4, 10', '"Vika", 3, 5', '"Gosha", 7, 10', '"Dasha", 1, 2', '"Egor", 7, 9',
                '"Zhanna", 0, 12', '"Zoya", 20, 20', '"Ira", 2, 3'],
        wrong=[("делит раньше, чем умножает: из-за целочисленного деления процент почти всегда 0",
                "public class Solution {{\n    static String testResult(String name, int correct, int total) {{\n"
                "        int percent = correct / total * 100;\n        if (percent >= {pass}) {{\n"
                "            return name + \": pass (\" + percent + \"%)\";\n        }}\n"
                "        return name + \": fail (\" + percent + \"%)\";\n    }}\n}}\n"),
               ("строгое сравнение: ровно проходной процент не засчитывается",
                "public class Solution {{\n    static String testResult(String name, int correct, int total) {{\n"
                "        int percent = correct * 100 / total;\n        if (percent > {pass}) {{\n"
                "            return name + \": pass (\" + percent + \"%)\";\n        }}\n"
                "        return name + \": fail (\" + percent + \"%)\";\n    }}\n}}\n")],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=3, slug="java-mp-taxi-fare", title="Цена поездки на такси",
        function="taxiFare",
        variants=[{"base": 100, "perKm": 25, "free": 3, "perMin": 10},
                  {"base": 150, "perKm": 20, "free": 5, "perMin": 8},
                  {"base": 90, "perKm": 30, "free": 2, "perMin": 15}],
        intro="Такси считает цену поездки так: посадка стоит {base} руб., каждый километр — {perKm} руб. "
              "А ещё машина может ждать пассажира: первые {free} мин. ожидания бесплатные, "
              "а каждая следующая минута стоит {perMin} руб.",
        steps=["Допиши метод `taxiFare(int km, int waiting)`: `km` — длина поездки в километрах, `waiting` — "
               "сколько минут машина ждала пассажира.",
               "Верни цену поездки в рублях: посадка, плюс плата за километры, плюс плата за платные минуты ожидания.",
               "Платные — только минуты сверх {free} бесплатных. Если машина ждала {free} мин. или меньше, "
               "за ожидание платить не нужно."],
        hint="Сначала посчитай, сколько минут ожидания платные: это `waiting` минус {free}. Но если это число вышло "
             "нулём или отрицательным, платных минут нет — проверь это с помощью `if`.",
        starter="public class Solution {{\n    static int taxiFare(int km, int waiting) {{\n"
                "        // Напиши решение здесь\n        return 0;\n    }}\n}}\n",
        solution="public class Solution {{\n    static int taxiFare(int km, int waiting) {{\n"
                 "        int fare = {base} + km * {perKm};\n        if (waiting > {free}) {{\n"
                 "            fare += (waiting - {free}) * {perMin};\n        }}\n        return fare;\n    }}\n}}\n",
        inputs=["5, 0", "10, 7", "0, 3", "12, 2", "1, 15", "20, 5", "3, 4"],
        wrong=[("берёт плату за все минуты ожидания, забыв про бесплатные",
                "public class Solution {{\n    static int taxiFare(int km, int waiting) {{\n"
                "        int fare = {base} + km * {perKm};\n        fare += waiting * {perMin};\n"
                "        return fare;\n    }}\n}}\n"),
               ("вычитает бесплатные минуты без проверки: при коротком ожидании цена уменьшается",
                "public class Solution {{\n    static int taxiFare(int km, int waiting) {{\n"
                "        int fare = {base} + km * {perKm};\n        fare += (waiting - {free}) * {perMin};\n"
                "        return fare;\n    }}\n}}\n")],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=1, slug="java-mp-fruit-sticker", title="Ценник на весах",
        function="sticker",
        variants=[{"price": 120}, {"price": 95}, {"price": 160}],
        intro="На рынке весы печатают наклейку для пакета с фруктами: название, вес и цену. Килограмм любых фруктов "
              "у этого продавца стоит {price} руб.",
        steps=["Допиши метод `sticker(String fruit, int kg)`: `fruit` — название фруктов, `kg` — сколько килограммов "
               "в пакете.",
               "Верни строку вида `Apples, 3 kg: 360 rub` — название, вес и стоимость пакета ({price} руб. за килограмм).",
               "Сначала идёт название, потом вес: в вызове `sticker(\"Pears\", 2)` строка — это фрукты, число — килограммы."],
        hint="Строку можно собрать из частей через `+`: и текст, и значения параметров, и результат умножения. "
             "Умножение возьми в скобки, чтобы оно посчиталось до склейки.",
        starter="public class Solution {{\n    static String sticker(String fruit, int kg) {{\n"
                "        // Напиши решение здесь\n        return \"\";\n    }}\n}}\n",
        solution="public class Solution {{\n    static String sticker(String fruit, int kg) {{\n"
                 "        return fruit + \", \" + kg + \" kg: \" + (kg * {price}) + \" rub\";\n    }}\n}}\n",
        inputs=['"Apples", 3', '"Pears", 2', '"Plums", 1', '"Cherries", 5', '"Grapes", 4', '"Peaches", 7'],
        wrong=[("пишет цену за килограмм вместо стоимости всего пакета",
                "public class Solution {{\n    static String sticker(String fruit, int kg) {{\n"
                "        return fruit + \", \" + kg + \" kg: \" + {price} + \" rub\";\n    }}\n}}\n"),
               ("пропустил запятую после названия",
                "public class Solution {{\n    static String sticker(String fruit, int kg) {{\n"
                "        return fruit + \" \" + kg + \" kg: \" + (kg * {price}) + \" rub\";\n    }}\n}}\n")],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=2, slug="java-mp-parcel-delivery", title="Доставка посылки",
        function="deliveryCost",
        variants=[{"base": 200, "perKg": 50}, {"base": 150, "perKg": 40}, {"base": 300, "perKg": 60}],
        intro="Служба доставки считает цену посылки так: {base} руб. за оформление плюс {perKg} руб. за каждый килограмм. "
              "Если клиент выбрал срочную доставку, вся сумма удваивается.",
        steps=["Допиши метод `deliveryCost(int kg, boolean express)`: `kg` — вес посылки в килограммах, `express` — "
               "`true`, если доставка срочная, и `false`, если обычная.",
               "Посчитай обычную цену: {base} руб. плюс {perKg} руб. за каждый килограмм.",
               "Если `express` равно `true`, верни эту цену, умноженную на 2, иначе верни её как есть."],
        hint="Параметр типа `boolean` можно сразу поставить в условие: `if (express)` выполнится, когда в вызове "
             "передали `true`. Удваивать нужно всю сумму, вместе с оформлением.",
        starter="public class Solution {{\n    static int deliveryCost(int kg, boolean express) {{\n"
                "        // Напиши решение здесь\n        return 0;\n    }}\n}}\n",
        solution="public class Solution {{\n    static int deliveryCost(int kg, boolean express) {{\n"
                 "        int cost = {base} + kg * {perKg};\n        if (express) {{\n            return cost * 2;\n"
                 "        }}\n        return cost;\n    }}\n}}\n",
        inputs=["3, false", "3, true", "1, false", "10, true", "0, true", "7, false", "5, true"],
        wrong=[("удваивает только плату за вес, а оформление — нет",
                "public class Solution {{\n    static int deliveryCost(int kg, boolean express) {{\n"
                "        if (express) {{\n            return {base} + kg * {perKg} * 2;\n        }}\n"
                "        return {base} + kg * {perKg};\n    }}\n}}\n"),
               ("не обращает внимания на параметр express",
                "public class Solution {{\n    static int deliveryCost(int kg, boolean express) {{\n"
                "        return {base} + kg * {perKg};\n    }}\n}}\n")],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=3, slug="java-mp-lessons-end", title="Когда закончатся уроки",
        function="endTime",
        variants=[{"len": 45, "brk": 10}, {"len": 40, "brk": 5}, {"len": 45, "brk": 15}],
        intro="Урок длится {len} минут, а между уроками перемена {brk} минут. Школьный бот по времени начала "
              "и числу уроков говорит, во сколько закончится последний урок.",
        steps=["Допиши метод `endTime(int hour, int minute, int lessons)`: первый урок начинается в `hour` часов "
               "`minute` минут, всего уроков `lessons` (от 1 до 8). Все уроки заканчиваются в тот же день.",
               "Перемены бывают только между уроками: после последнего урока перемены нет.",
               "Верни время конца последнего урока строкой вида `HH:MM` — часы и минуты всегда двумя цифрами: "
               "`09:05`, `13:40`."],
        hint="Переведи время начала в минуты от полуночи, прибавь длительность всех уроков и перемен, а потом "
             "получи часы делением на 60 и минуты остатком. Если число меньше 10, добавь перед ним `\"0\"`.",
        starter="public class Solution {{\n    static String endTime(int hour, int minute, int lessons) {{\n"
                "        // Напиши решение здесь\n        return \"\";\n    }}\n}}\n",
        solution="public class Solution {{\n    static String endTime(int hour, int minute, int lessons) {{\n"
                 "        int total = hour * 60 + minute + lessons * {len} + (lessons - 1) * {brk};\n"
                 "        int h = total / 60;\n        int m = total % 60;\n"
                 "        String hh = h < 10 ? \"0\" + h : \"\" + h;\n        String mm = m < 10 ? \"0\" + m : \"\" + m;\n"
                 "        return hh + \":\" + mm;\n    }}\n}}\n",
        inputs=["8, 30, 1", "8, 0, 4", "9, 5, 2", "13, 0, 3", "7, 50, 1", "8, 15, 6", "12, 40, 5", "10, 20, 1", "10, 25, 1"],
        wrong=[("считает перемену и после последнего урока",
                "public class Solution {{\n    static String endTime(int hour, int minute, int lessons) {{\n"
                "        int total = hour * 60 + minute + lessons * ({len} + {brk});\n"
                "        int h = total / 60;\n        int m = total % 60;\n"
                "        String hh = h < 10 ? \"0\" + h : \"\" + h;\n        String mm = m < 10 ? \"0\" + m : \"\" + m;\n"
                "        return hh + \":\" + mm;\n    }}\n}}\n"),
               ("не дописывает ведущий ноль: 9:5 вместо 09:05",
                "public class Solution {{\n    static String endTime(int hour, int minute, int lessons) {{\n"
                "        int total = hour * 60 + minute + lessons * {len} + (lessons - 1) * {brk};\n"
                "        return total / 60 + \":\" + total % 60;\n    }}\n}}\n")],
    ),
]
