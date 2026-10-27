"""METHOD_PARAMETERS — «Параметры и возвращаемое значение» (Java): несколько параметров разных типов, их порядок,
возврат int или String через return. Taught before: everything up to own static methods (conditions, loops, arrays,
/ and %, strings). Not yet: own classes."""
from java_tasks import JavaFunctionTask

SKILL = "METHOD_PARAMETERS"

TICKET = ("public class Solution {{\n    static String ticket(String name, int age) {{\n"
          "        if (age < 7) {{\n            return name + \", \" + age + \": free\";\n        }}\n"
          "        if (age < 18) {{\n            return name + \", \" + age + \": {child} rub\";\n        }}\n"
          "        return name + \", \" + age + \": {adult} rub\";\n    }}\n}}\n")

BAR = ("public class Solution {{\n    static String progressBar(int done, int total) {{\n"
       "        int filled = done * {width} / total;\n        String bar = \"[\";\n"
       "        for (int i = 0; i < filled; i++) {{\n            bar += \"#\";\n        }}\n"
       "        for (int i = 0; i < {width} - filled; i++) {{\n            bar += \".\";\n        }}\n"
       "        return bar + \"] \" + done * 100 / total + \"%\";\n    }}\n}}\n")

TASKS = [
    JavaFunctionTask(
        skill=SKILL, difficulty=1, slug="java-mp-rt-trip-share", title="Бензин на всех",
        function="share",
        variants=[{"perKm": 6}, {"perKm": 8}, {"perKm": 5}],
        intro="Друзья едут на машине за город. Бензин обходится в {perKm} руб. за километр, и стоимость поездки делят "
              "поровну на всех, кто едет. Нужен метод, который считает долю одного человека.",
        steps=["Допиши метод `share(int km, int people)`: `km` — длина поездки в километрах, `people` — сколько человек "
               "едет (всегда больше 0).",
               "Верни, сколько рублей платит один человек: стоимость всей поездки ({perKm} руб. за километр), делённая "
               "нацело на `people`.",
               "Не меняй порядок параметров: в вызове `share(120, 4)` первое число — километры, второе — люди."],
        hint="Параметры — это обычные переменные внутри метода, а их значения приходят из вызова. Сначала посчитай "
             "стоимость всей поездки, а потом раздели её на число людей.",
        starter="public class Solution {{\n    static int share(int km, int people) {{\n        // Напиши решение здесь\n"
                "        return 0;\n    }}\n}}\n",
        solution="public class Solution {{\n    static int share(int km, int people) {{\n"
                 "        return km * {perKm} / people;\n    }}\n}}\n",
        inputs=["120, 4", "300, 3", "50, 1", "200, 5", "90, 2", "10, 7", "400, 8"],
        wrong=[("переставил параметры местами: километры считаются как люди",
                "public class Solution {{\n    static int share(int km, int people) {{\n"
                "        return people * {perKm} / km;\n    }}\n}}\n"),
               ("забыл разделить: возвращает стоимость всей поездки",
                "public class Solution {{\n    static int share(int km, int people) {{\n"
                "        return km * {perKm};\n    }}\n}}\n")],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=2, slug="java-mp-rt-zoo-ticket", title="Билет в зоопарк",
        function="ticket",
        variants=[{"child": 150, "adult": 400}, {"child": 200, "adult": 500}, {"child": 120, "adult": 350}],
        intro="Касса зоопарка печатает на билете имя посетителя, его возраст и цену. Детям до 7 лет вход бесплатный, "
              "с 7 до 17 лет включительно билет стоит {child} руб., а с 18 лет — {adult} руб.",
        steps=["Допиши метод `ticket(String name, int age)`: `name` — имя посетителя, `age` — его возраст.",
               "Если `age` меньше 7, верни строку вида `Anya, 5: free`.",
               "Если `age` от 7 до 17, верни строку вида `Anya, 12: {child} rub`, а с 18 лет — `Anya, 30: {adult} rub`. "
               "Имя и возраст в строке — из параметров."],
        hint="`return` сразу завершает метод, поэтому проверки удобно писать подряд: сначала самые маленькие, потом "
             "школьники, а в конце — всем остальным. 17-летний ещё платит как ребёнок.",
        starter="public class Solution {{\n    static String ticket(String name, int age) {{\n        // Напиши решение здесь\n"
                "        return \"\";\n    }}\n}}\n",
        solution=TICKET,
        inputs=['"Anya", 5', '"Boris", 12', '"Vika", 30', '"Gosha", 7', '"Dasha", 6', '"Egor", 17', '"Ira", 18', '"Lev", 0'],
        wrong=[("<= 7 вместо < 7: семилетний проходит бесплатно",
                TICKET.replace("age < 7", "age <= 7")),
               ("< 17 вместо < 18: 17-летний платит как взрослый",
                TICKET.replace("age < 18", "age < 17"))],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=3, slug="java-mp-rt-progress-bar", title="Полоска загрузки",
        function="progressBar",
        variants=[{"width": 10}, {"width": 20}, {"width": 5}],
        intro="Программа установки показывает, как идёт загрузка файлов, полоской из {width} клеток: заполненные "
              "клетки — `#`, пустые — `.`. После полоски пишется процент.",
        steps=["Допиши метод `progressBar(int done, int total)`: загружено `done` файлов из `total` (`total` всегда "
               "больше 0, а `done` — от 0 до `total`).",
               "Число заполненных клеток — `done * {width} / total` (нацело), остальные клетки до {width} пустые.",
               "Процент — `done * 100 / total` (нацело).",
               "Верни строку: `[`, заполненные клетки, пустые клетки, `] `, процент и знак `%` — как в примерах ниже."],
        hint="Строку собери двумя циклами: первый добавляет `#`, второй — `.`. Умножай раньше, чем делишь: "
             "`2 / 5 * 10` в целых числах даёт 0, а `2 * 10 / 5` — 4.",
        starter="public class Solution {{\n    static String progressBar(int done, int total) {{\n        // Напиши решение здесь\n"
                "        return \"\";\n    }}\n}}\n",
        solution=BAR,
        inputs=["2, 5", "0, 3", "7, 7", "1, 3", "9, 10", "5, 8", "3, 4"],
        wrong=[("делит раньше, чем умножает: заполненных клеток почти всегда 0",
                BAR.replace("done * {width} / total", "done / total * {width}")),
               ("пустых клеток столько же, сколько во всей полоске: полоска получается слишком длинной",
                BAR.replace("i < {width} - filled", "i < {width}"))],
    ),
]
