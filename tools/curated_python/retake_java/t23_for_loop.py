"""FOR_LOOP_BASIC — «Цикл for» (Java). Taught before: println, variables, assignment, arithmetic, primitive types, String,
/ and %, += -= ++, if/else, comparisons, && || !, switch. The point: the three parts of the for header (start,
condition, step), inclusive bounds, a step other than 1, if inside the loop body.
Not yet: accumulating a result in a loop, while, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "FOR_LOOP_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-for-rt-times-table", title="Строчка таблицы умножения",
        given=[("int", "number"), ("int", "upTo")],
        variants=[{"number": "3", "upTo": "5"}, {"number": "7", "upTo": "4"}, {"number": "6", "upTo": "9"}],
        hidden=[{"number": "2", "upTo": "1"}, {"number": "9", "upTo": "3"}, {"number": "4", "upTo": "10"},
                {"number": "8", "upTo": "6"}],
        intro="Маша учит таблицу умножения и просит распечатать ей подсказку: число `number`, умноженное по очереди "
              "на 1, 2, 3 и так далее до `upTo` включительно.",
        steps=["Напиши цикл `for`, который перебирает множители от 1 до `upTo` включительно.",
               "На каждом шаге выведи отдельной строкой пример с ответом в формате `3 x 2 = 6`: `number`, ` x `, "
               "множитель, ` = ` и произведение."],
        hint="Условие в заголовке `for` проверяется перед каждым шагом. Подумай, какой знак сравнения нужен, чтобы "
             "последним был множитель `upTo`. Произведение возьми в скобки, чтобы числа перемножились, а не склеились.",
        solution='for (int i = 1; i <= upTo; i++) {\n    System.out.println(number + " x " + i + " = " + (number * i));\n}',
        wrong=[("< вместо <=: последняя строчка таблицы пропадает",
                'for (int i = 1; i < upTo; i++) {\n    System.out.println(number + " x " + i + " = " + (number * i));\n}'),
               ("отсчёт с нуля: появляется лишняя строчка с умножением на 0",
                'for (int i = 0; i <= upTo; i++) {\n    System.out.println(number + " x " + i + " = " + (number * i));\n}')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-for-rt-fahrenheit-table", title="Шкала Фаренгейта",
        given=[("int", "from"), ("int", "to")],
        variants=[{"from": "0", "to": "20"}, {"from": "-10", "to": "10"}, {"from": "25", "to": "40"}],
        hidden=[{"from": "5", "to": "5"}, {"from": "-20", "to": "0"}, {"from": "30", "to": "45"},
                {"from": "100", "to": "110"}],
        intro="Аня собирается в путешествие в США, где температуру меряют в градусах Фаренгейта. Она хочет табличку "
              "перевода: градусы Цельсия от `from` до `to` включительно с шагом 5 (оба числа делятся на 5).",
        steps=["Напиши цикл `for`, который начинается с `from` и на каждом шаге увеличивает градусы на 5.",
               "Цикл должен идти, пока градусы не больше `to`.",
               "На каждом шаге посчитай градусы Фаренгейта по формуле `c * 9 / 5 + 32` и выведи строку в формате "
               "`20 C = 68 F`."],
        hint="Третья часть заголовка `for` не обязана быть `i++`: там можно написать `c += 5`. Для чисел, кратных 5, "
             "формула даёт целое число, так что хватит типа `int`.",
        solution='for (int c = from; c <= to; c += 5) {\n    System.out.println(c + " C = " + (c * 9 / 5 + 32) + " F");\n}',
        wrong=[("< вместо <=: последняя строчка таблицы пропадает",
                'for (int c = from; c < to; c += 5) {\n    System.out.println(c + " C = " + (c * 9 / 5 + 32) + " F");\n}'),
               ("шаг 1 вместо 5: в таблице каждый градус подряд",
                'for (int c = from; c <= to; c++) {\n    System.out.println(c + " C = " + (c * 9 / 5 + 32) + " F");\n}')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-for-rt-guard-rounds", title="Обходы охранника",
        given=[("int", "start"), ("int", "every"), ("int", "rounds")],
        variants=[{"start": "20", "every": "3", "rounds": "4"}, {"start": "22", "every": "2", "rounds": "5"},
                  {"start": "18", "every": "4", "rounds": "3"}],
        hidden=[{"start": "23", "every": "1", "rounds": "8"}, {"start": "9", "every": "2", "rounds": "3"},
                {"start": "0", "every": "6", "rounds": "4"}, {"start": "21", "every": "5", "rounds": "2"},
                {"start": "12", "every": "12", "rounds": "1"}],
        intro="Охранник склада делает `rounds` обходов: первый — в `start` часов, а каждый следующий — через `every` "
              "часов после предыдущего. Часы идут от 0 до 23: после 23 часов снова начинаются 0 часов.",
        steps=["Перебери циклом `for` номера обходов от 1 до `rounds` включительно.",
               "Для каждого обхода посчитай час: `start` плюс номер обхода минус 1, умноженный на `every`, и возьми "
               "остаток от деления этой суммы на 24.",
               "Если час меньше 6, выведи `Round …: …:00 (night)`, иначе — `Round …: …:00`. Вместо многоточий — "
               "номер обхода и час, например `Round 2: 1:00 (night)`."],
        hint="Остаток от деления на 24 «заворачивает» часы: 25 % 24 даёт 1. Ровно 6:00 уже не ночь.",
        solution='for (int r = 1; r <= rounds; r++) {\n    int hour = (start + (r - 1) * every) % 24;\n    if (hour < 6) {\n'
                 '        System.out.println("Round " + r + ": " + hour + ":00 (night)");\n    } else {\n'
                 '        System.out.println("Round " + r + ": " + hour + ":00");\n    }\n}',
        wrong=[("без остатка от деления на 24: после полуночи получается 25:00",
                'for (int r = 1; r <= rounds; r++) {\n    int hour = start + (r - 1) * every;\n    if (hour < 6) {\n'
                '        System.out.println("Round " + r + ": " + hour + ":00 (night)");\n    } else {\n'
                '        System.out.println("Round " + r + ": " + hour + ":00");\n    }\n}'),
               ("<= 6 вместо < 6: обход в 6:00 тоже назван ночным",
                'for (int r = 1; r <= rounds; r++) {\n    int hour = (start + (r - 1) * every) % 24;\n    if (hour <= 6) {\n'
                '        System.out.println("Round " + r + ": " + hour + ":00 (night)");\n    } else {\n'
                '        System.out.println("Round " + r + ": " + hour + ":00");\n    }\n}')],
        constructs=["for", "if"],
    ),
]
