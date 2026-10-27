"""ACCUMULATOR_PATTERN — «Накопление результата в цикле» (Java). Taught before: println, variables, assignment,
arithmetic, primitive types, String, / and %, += -= ++, if/else, comparisons, && || !, switch, for. The point: a
variable created before the loop, changed with += on every step (or only when a condition holds) and printed after it.
Not yet: while, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "ACCUMULATOR_PATTERN"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-accum-rt-cube-pyramid", title="Пирамида из кубиков",
        given=[("int", "layers")],
        variants=[{"layers": "3"}, {"layers": "5"}, {"layers": "4"}],
        hidden=[{"layers": "1"}, {"layers": "2"}, {"layers": "6"}, {"layers": "10"}],
        intro="Лёва строит пирамиду из кубиков. Верхний слой — один кубик, второй сверху — квадрат 2 на 2, третий — "
              "квадрат 3 на 3 и так далее. Всего в пирамиде `layers` слоёв.",
        steps=["До цикла заведи переменную `cubes` со значением 0.",
               "Циклом `for` перебери номера слоёв от 1 до `layers` включительно и на каждом шаге добавляй к `cubes` "
               "число кубиков в слое — номер слоя, умноженный сам на себя, — с помощью `+=`.",
               "После цикла выведи две строки: `Layers: …` и `Cubes needed: …`."],
        hint="В слое с номером 3 лежит 3 * 3 = 9 кубиков. Сумма копится в переменной, созданной до цикла, а печатается "
             "после него — когда все слои уже посчитаны.",
        solution='int cubes = 0;\nfor (int i = 1; i <= layers; i++) {\n    cubes += i * i;\n}\n'
                 'System.out.println("Layers: " + layers);\nSystem.out.println("Cubes needed: " + cubes);',
        wrong=[("= вместо +=: считаются кубики только нижнего слоя",
                'int cubes = 0;\nfor (int i = 1; i <= layers; i++) {\n    cubes = i * i;\n}\n'
                'System.out.println("Layers: " + layers);\nSystem.out.println("Cubes needed: " + cubes);'),
               ("добавляет номер слоя, а не квадрат: в каждом слое будто одна линия кубиков",
                'int cubes = 0;\nfor (int i = 1; i <= layers; i++) {\n    cubes += i;\n}\n'
                'System.out.println("Layers: " + layers);\nSystem.out.println("Cubes needed: " + cubes);')],
        constructs=["for", "augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-accum-rt-stairs-rests", title="Подъём по лестнице",
        given=[("int", "floor"), ("int", "steps")],
        variants=[{"floor": "12", "steps": "18"}, {"floor": "7", "steps": "20"}, {"floor": "16", "steps": "16"}],
        hidden=[{"floor": "5", "steps": "20"}, {"floor": "6", "steps": "10"}, {"floor": "2", "steps": "15"},
                {"floor": "10", "steps": "12"}, {"floor": "11", "steps": "12"}],
        intro="Лифт сломался, и Петя поднимается пешком с 1-го этажа на этаж `floor`. Между соседними этажами — `steps` "
              "ступенек. На каждом этаже, номер которого делится на 5, Петя останавливается отдохнуть — но не на "
              "последнем этаже: там он уже дома.",
        steps=["До цикла заведи две переменные со значением 0: сколько ступенек пройдено и сколько было остановок.",
               "Перебери циклом `for` этажи, на которые Петя поднимается, — от 2 до `floor` включительно. На каждом "
               "шаге добавляй `steps` к числу ступенек.",
               "Если номер этажа делится на 5 **и** это не этаж `floor`, увеличь число остановок на 1.",
               "После цикла выведи две строки: `Steps: …` и `Rests: …`."],
        hint="Цикл начинается с 2: на 1-й этаж подниматься не нужно, Петя уже там. Чтобы проверить два условия сразу, "
             "соедини их через `&&`.",
        solution='int walked = 0;\nint rests = 0;\nfor (int f = 2; f <= floor; f++) {\n    walked += steps;\n'
                 '    if (f % 5 == 0 && f != floor) {\n        rests++;\n    }\n}\nSystem.out.println("Steps: " + walked);\n'
                 'System.out.println("Rests: " + rests);',
        wrong=[("цикл с 1-го этажа: лишний пролёт ступенек",
                'int walked = 0;\nint rests = 0;\nfor (int f = 1; f <= floor; f++) {\n    walked += steps;\n'
                '    if (f % 5 == 0 && f != floor) {\n        rests++;\n    }\n}\nSystem.out.println("Steps: " + walked);\n'
                'System.out.println("Rests: " + rests);'),
               ("останавливается и на последнем этаже",
                'int walked = 0;\nint rests = 0;\nfor (int f = 2; f <= floor; f++) {\n    walked += steps;\n'
                '    if (f % 5 == 0) {\n        rests++;\n    }\n}\nSystem.out.println("Steps: " + walked);\n'
                'System.out.println("Rests: " + rests);')],
        constructs=["for", "if", "augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-accum-rt-running-weeks", title="Беговой план с разгрузкой",
        given=[("int", "km"), ("int", "add"), ("int", "weeks")],
        variants=[{"km": "10", "add": "2", "weeks": "5"}, {"km": "8", "add": "3", "weeks": "4"},
                  {"km": "15", "add": "1", "weeks": "6"}],
        hidden=[{"km": "20", "add": "0", "weeks": "3"}, {"km": "5", "add": "5", "weeks": "8"},
                {"km": "12", "add": "4", "weeks": "1"}, {"km": "9", "add": "2", "weeks": "4"}],
        intro="Тренер составил Ксюше беговой план на `weeks` недель. В первую неделю она пробегает `km` км, и каждую "
              "следующую неделю план растёт на `add` км. Но каждая четвёртая неделя (4-я, 8-я…) — разгрузочная: "
              "в неё Ксюша бегает только половину плана (нацело).",
        steps=["До цикла заведи переменную `plan` со значением `km` и переменную `total` со значением 0.",
               "Перебери циклом `for` недели от 1 до `weeks` включительно. Если номер недели делится на 4, Ксюша "
               "пробегает `plan / 2` км, иначе — `plan` км.",
               "Выведи строку `Week …: … km` с номером недели и тем, сколько Ксюша пробежит, и добавь это число к `total`.",
               "В конце шага увеличь `plan` на `add` — даже после разгрузочной недели.",
               "После цикла выведи `Total: … km`."],
        hint="Заведи внутри цикла переменную для пробега этой недели и присвой ей значение в `if`/`else`. "
             "К `total` добавляй именно её, а `plan` меняй только последней строкой шага.",
        solution='int plan = km;\nint total = 0;\nfor (int week = 1; week <= weeks; week++) {\n    int run = plan;\n'
                 '    if (week % 4 == 0) {\n        run = plan / 2;\n    }\n    System.out.println("Week " + week + ": " + run + " km");\n'
                 '    total += run;\n    plan += add;\n}\nSystem.out.println("Total: " + total + " km");',
        wrong=[("в сумму идёт полный план: разгрузочная неделя считается целиком",
                'int plan = km;\nint total = 0;\nfor (int week = 1; week <= weeks; week++) {\n    int run = plan;\n'
                '    if (week % 4 == 0) {\n        run = plan / 2;\n    }\n    System.out.println("Week " + week + ": " + run + " km");\n'
                '    total += plan;\n    plan += add;\n}\nSystem.out.println("Total: " + total + " km");'),
               ("план растёт в начале шага: уже первая неделя длиннее на add",
                'int plan = km;\nint total = 0;\nfor (int week = 1; week <= weeks; week++) {\n    plan += add;\n    int run = plan;\n'
                '    if (week % 4 == 0) {\n        run = plan / 2;\n    }\n    System.out.println("Week " + week + ": " + run + " km");\n'
                '    total += run;\n}\nSystem.out.println("Total: " + total + " km");')],
        constructs=["for", "if", "augmented_assignment"],
    ),
]
