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
]
