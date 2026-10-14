"""FOR_LOOP_BASIC — «Цикл for» (Java). Taught before: println, variables, assignment, arithmetic, primitive types, String,
/ and %, += -= ++, if/else, comparisons, && || !, switch. The point: the three parts of the for header (start,
condition, step), inclusive bounds, a step other than 1, if inside the loop body.
Not yet: accumulating a result in a loop, while, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "FOR_LOOP_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-for-cinema-seats", title="Номера мест в ряду",
        given=[("int", "seats")],
        variants=[{"seats": "5"}, {"seats": "3"}, {"seats": "8"}],
        hidden=[{"seats": "1"}, {"seats": "4"}, {"seats": "6"}, {"seats": "10"}],
        intro="В новом кинотеатре нужно подписать кресла в ряду номерами, начиная с 1. "
              "Сколько кресел в ряду, записано в поле `seats`.",
        steps=["Напиши цикл `for`, который перебирает числа от 1 до `seats` включительно.",
               "На каждом шаге выведи отдельной строкой надпись `Seat 1`, `Seat 2` и так далее: слово `Seat`, "
               "пробел и номер."],
        hint="Условие в заголовке `for` проверяется перед каждым шагом, и цикл идёт, пока оно верно. "
             "Подумай, какой знак сравнения нужен, чтобы последним было место с номером `seats`.",
        solution='for (int i = 1; i <= seats; i++) {\n    System.out.println("Seat " + i);\n}',
        wrong=[("< вместо <=: последнее место не подписано",
                'for (int i = 1; i < seats; i++) {\n    System.out.println("Seat " + i);\n}'),
               ("отсчёт с нуля: появляется «Seat 0», а последнего места нет",
                'for (int i = 0; i < seats; i++) {\n    System.out.println("Seat " + i);\n}')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-for-cactus-watering", title="Полив кактуса в отпуске",
        given=[("int", "days"), ("int", "every")],
        variants=[{"days": "10", "every": "3"}, {"days": "14", "every": "4"}, {"days": "7", "every": "2"}],
        hidden=[{"days": "5", "every": "5"}, {"days": "1", "every": "3"}, {"days": "12", "every": "3"},
                {"days": "9", "every": "4"}, {"days": "20", "every": "7"}],
        intro="Аня уезжает в отпуск на `days` дней и просит соседку поливать кактус: первый раз — в день 1, "
              "а дальше раз в `every` дней. Нужно составить для соседки список дней полива.",
        steps=["Напиши цикл `for`, который начинается с дня 1 и на каждом шаге увеличивает номер дня на `every`.",
               "Цикл должен идти, пока номер дня не больше `days`.",
               "На каждом шаге выведи строку `Water on day …` с номером дня."],
        hint="Третья часть заголовка `for` не обязана быть `i++`: там можно написать, например, `day += 2` — "
             "тогда номер дня будет расти на 2.",
        solution='for (int day = 1; day <= days; day += every) {\n    System.out.println("Water on day " + day);\n}',
        wrong=[("< вместо <=: полив в последний день отпуска пропадает",
                'for (int day = 1; day < days; day += every) {\n    System.out.println("Water on day " + day);\n}'),
               ("начинает с every, а не с 1: в первый день кактус не полит",
                'for (int day = every; day <= days; day += every) {\n    System.out.println("Water on day " + day);\n}')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-for-running-plan", title="План пробежки по минутам",
        given=[("int", "minutes"), ("int", "warmup")],
        variants=[{"minutes": "6", "warmup": "2"}, {"minutes": "8", "warmup": "3"}, {"minutes": "5", "warmup": "1"}],
        hidden=[{"minutes": "3", "warmup": "1"}, {"minutes": "2", "warmup": "1"}, {"minutes": "4", "warmup": "4"},
                {"minutes": "10", "warmup": "2"}, {"minutes": "1", "warmup": "1"}],
        intro="Тренер расписывает пробежку по минутам. Тренировка длится `minutes` минут: первые `warmup` минут — "
              "разминка, последняя минута — заминка, а всё остальное время — бег.",
        steps=["Перебери циклом `for` номера минут от 1 до `minutes` включительно.",
               "Если это последняя минута тренировки, выведи `Minute …: cool-down`.",
               "Иначе, если номер минуты не больше `warmup`, выведи `Minute …: warm-up`.",
               "Во всех остальных случаях выведи `Minute …: run`. Вместо многоточия — номер минуты."],
        hint="Внутри цикла можно писать `if`, `else if` и `else`. Порядок проверок важен: последняя минута — всегда "
             "заминка, даже если разминка длится до самого конца.",
        solution='for (int i = 1; i <= minutes; i++) {\n    if (i == minutes) {\n        System.out.println("Minute " + i + ": cool-down");\n'
                 '    } else if (i <= warmup) {\n        System.out.println("Minute " + i + ": warm-up");\n    } else {\n'
                 '        System.out.println("Minute " + i + ": run");\n    }\n}',
        wrong=[("< вместо <= для разминки: разминка на минуту короче",
                'for (int i = 1; i <= minutes; i++) {\n    if (i == minutes) {\n        System.out.println("Minute " + i + ": cool-down");\n'
                '    } else if (i < warmup) {\n        System.out.println("Minute " + i + ": warm-up");\n    } else {\n'
                '        System.out.println("Minute " + i + ": run");\n    }\n}'),
               ("разминка проверяется первой: если она длится до конца, заминки нет",
                'for (int i = 1; i <= minutes; i++) {\n    if (i <= warmup) {\n        System.out.println("Minute " + i + ": warm-up");\n'
                '    } else if (i == minutes) {\n        System.out.println("Minute " + i + ": cool-down");\n    } else {\n'
                '        System.out.println("Minute " + i + ": run");\n    }\n}')],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-for-rocket-countdown", title="Обратный отсчёт",
        given=[("int", "start")],
        variants=[{"start": "5"}, {"start": "3"}, {"start": "7"}],
        hidden=[{"start": "1"}, {"start": "2"}, {"start": "4"}, {"start": "10"}],
        intro="Перед запуском модели ракеты Борис ведёт обратный отсчёт. С какого числа начинать, записано в поле `start`.",
        steps=["Напиши цикл `for`, который перебирает числа от `start` вниз до 1 включительно и выводит каждое отдельной строкой.",
               "После цикла выведи `Liftoff!`."],
        hint="Счётчик цикла может уменьшаться: начни с `start`, а в третьей части заголовка напиши `i--`. "
             "Подумай, какое условие нужно, чтобы последним было число 1, а не 0.",
        solution='for (int i = start; i >= 1; i--) {\n    System.out.println(i);\n}\nSystem.out.println("Liftoff!");',
        wrong=[("условие i >= 0: перед стартом выводится лишний 0",
                'for (int i = start; i >= 0; i--) {\n    System.out.println(i);\n}\nSystem.out.println("Liftoff!");'),
               ("условие i > 1: единица пропадает",
                'for (int i = start; i > 1; i--) {\n    System.out.println(i);\n}\nSystem.out.println("Liftoff!");')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-for-bus-timetable", title="Расписание автобуса",
        given=[("int", "hour"), ("int", "interval")],
        variants=[{"hour": "9", "interval": "15"}, {"hour": "14", "interval": "20"}, {"hour": "7", "interval": "12"}],
        hidden=[{"hour": "8", "interval": "5"}, {"hour": "18", "interval": "30"}, {"hour": "6", "interval": "60"},
                {"hour": "11", "interval": "25"}, {"hour": "22", "interval": "7"}],
        intro="Автобус отходит от остановки каждые `interval` минут, первый рейс часа — ровно в начале часа. "
              "Нужно напечатать расписание на один час — час записан в поле `hour`.",
        steps=["Напиши цикл `for` по минутам: начни с 0 и на каждом шаге увеличивай минуты на `interval`, "
               "пока минут меньше 60.",
               "На каждом шаге выведи время отправления: час, двоеточие и минуты, например `9:15`.",
               "Минуты всегда пиши двумя цифрами: если минут меньше 10, перед ними нужен 0 — `9:00`, `8:05`."],
        hint="Третья часть заголовка `for` может быть `m += interval`. Для двух цифр внутри цикла пригодится `if`: "
             "при `m < 10` печатай `hour + \":0\" + m`.",
        solution='for (int m = 0; m < 60; m += interval) {\n    if (m < 10) {\n        System.out.println(hour + ":0" + m);\n'
                 '    } else {\n        System.out.println(hour + ":" + m);\n    }\n}',
        wrong=[("нет нуля перед минутами: выводит 9:0 вместо 9:00",
                'for (int m = 0; m < 60; m += interval) {\n    System.out.println(hour + ":" + m);\n}'),
               ("<= 60 вместо < 60: появляется время вида 9:60",
                'for (int m = 0; m <= 60; m += interval) {\n    if (m < 10) {\n        System.out.println(hour + ":0" + m);\n'
                '    } else {\n        System.out.println(hour + ":" + m);\n    }\n}')],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-for-reading-plan", title="План чтения книги",
        given=[("int", "pages"), ("int", "perDay")],
        variants=[{"pages": "90", "perDay": "20"}, {"pages": "60", "perDay": "15"}, {"pages": "100", "perDay": "30"}],
        hidden=[{"pages": "10", "perDay": "20"}, {"pages": "40", "perDay": "20"}, {"pages": "41", "perDay": "20"},
                {"pages": "25", "perDay": "7"}, {"pages": "1", "perDay": "1"}],
        intro="Вера хочет прочитать книгу из `pages` страниц, читая по `perDay` страниц в день. В последний день "
              "может остаться меньше страниц. Составь ей план по дням.",
        steps=["Посчитай число дней: `pages / perDay`, и если `pages` делится на `perDay` с остатком, прибавь ещё 1 день.",
               "Перебери циклом `for` номера дней от 1 до этого числа включительно.",
               "Для каждого дня посчитай первую страницу (номер дня минус 1, умноженный на `perDay`, плюс 1) и последнюю "
               "(номер дня, умноженный на `perDay`, но не больше `pages`). Выведи `Day …: pages …-…`, например `Day 2: pages 21-40`.",
               "После цикла выведи `Finished in … days`."],
        hint="Остаток от деления даёт `%`: если `pages % perDay != 0`, нужен ещё один день. Последнюю страницу "
             "поправь внутри цикла обычным `if`: если она получилась больше `pages`, сделай её равной `pages`.",
        solution='int days = pages / perDay;\nif (pages % perDay != 0) {\n    days++;\n}\nfor (int day = 1; day <= days; day++) {\n'
                 '    int from = (day - 1) * perDay + 1;\n    int to = day * perDay;\n    if (to > pages) {\n        to = pages;\n    }\n'
                 '    System.out.println("Day " + day + ": pages " + from + "-" + to);\n}\nSystem.out.println("Finished in " + days + " days");',
        wrong=[("не добавляет день для остатка страниц: конец книги не попадает в план",
                'int days = pages / perDay;\nfor (int day = 1; day <= days; day++) {\n'
                '    int from = (day - 1) * perDay + 1;\n    int to = day * perDay;\n    if (to > pages) {\n        to = pages;\n    }\n'
                '    System.out.println("Day " + day + ": pages " + from + "-" + to);\n}\nSystem.out.println("Finished in " + days + " days");'),
               ("не ограничивает последний день: план заканчивается на странице, которой нет",
                'int days = pages / perDay;\nif (pages % perDay != 0) {\n    days++;\n}\nfor (int day = 1; day <= days; day++) {\n'
                '    int from = (day - 1) * perDay + 1;\n    int to = day * perDay;\n'
                '    System.out.println("Day " + day + ": pages " + from + "-" + to);\n}\nSystem.out.println("Finished in " + days + " days");')],
        constructs=["for", "if"],
    ),
]
