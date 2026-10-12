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
               "На каждом шаге выведи отдельной строкой надпись `Место 1`, `Место 2` и так далее: слово `Место`, "
               "пробел и номер."],
        hint="Условие в заголовке `for` проверяется перед каждым шагом, и цикл идёт, пока оно верно. "
             "Подумай, какой знак сравнения нужен, чтобы последним было место с номером `seats`.",
        solution='for (int i = 1; i <= seats; i++) {\n    System.out.println("Место " + i);\n}',
        wrong=[("< вместо <=: последнее место не подписано",
                'for (int i = 1; i < seats; i++) {\n    System.out.println("Место " + i);\n}'),
               ("отсчёт с нуля: появляется «Место 0», а последнего места нет",
                'for (int i = 0; i < seats; i++) {\n    System.out.println("Место " + i);\n}')],
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
               "На каждом шаге выведи строку `Полить в день …` с номером дня."],
        hint="Третья часть заголовка `for` не обязана быть `i++`: там можно написать, например, `day += 2` — "
             "тогда номер дня будет расти на 2.",
        solution='for (int day = 1; day <= days; day += every) {\n    System.out.println("Полить в день " + day);\n}',
        wrong=[("< вместо <=: полив в последний день отпуска пропадает",
                'for (int day = 1; day < days; day += every) {\n    System.out.println("Полить в день " + day);\n}'),
               ("начинает с every, а не с 1: в первый день кактус не полит",
                'for (int day = every; day <= days; day += every) {\n    System.out.println("Полить в день " + day);\n}')],
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
               "Если это последняя минута тренировки, выведи `Минута …: заминка`.",
               "Иначе, если номер минуты не больше `warmup`, выведи `Минута …: разминка`.",
               "Во всех остальных случаях выведи `Минута …: бег`. Вместо многоточия — номер минуты."],
        hint="Внутри цикла можно писать `if`, `else if` и `else`. Порядок проверок важен: последняя минута — всегда "
             "заминка, даже если разминка длится до самого конца.",
        solution='for (int i = 1; i <= minutes; i++) {\n    if (i == minutes) {\n        System.out.println("Минута " + i + ": заминка");\n'
                 '    } else if (i <= warmup) {\n        System.out.println("Минута " + i + ": разминка");\n    } else {\n'
                 '        System.out.println("Минута " + i + ": бег");\n    }\n}',
        wrong=[("< вместо <= для разминки: разминка на минуту короче",
                'for (int i = 1; i <= minutes; i++) {\n    if (i == minutes) {\n        System.out.println("Минута " + i + ": заминка");\n'
                '    } else if (i < warmup) {\n        System.out.println("Минута " + i + ": разминка");\n    } else {\n'
                '        System.out.println("Минута " + i + ": бег");\n    }\n}'),
               ("разминка проверяется первой: если она длится до конца, заминки нет",
                'for (int i = 1; i <= minutes; i++) {\n    if (i <= warmup) {\n        System.out.println("Минута " + i + ": разминка");\n'
                '    } else if (i == minutes) {\n        System.out.println("Минута " + i + ": заминка");\n    } else {\n'
                '        System.out.println("Минута " + i + ": бег");\n    }\n}')],
        constructs=["for", "if"],
    ),
]
