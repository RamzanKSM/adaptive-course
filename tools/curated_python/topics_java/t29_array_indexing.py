"""ARRAY_INDEXING — «Индексы массива» (Java). Taught before: println, variables, arithmetic, types, String, / and %,
+= ++, conditions, switch, for, accumulator, while, loop termination. Here: an element by index, indexes from 0,
a number counted from 1 turned into an index, changing an element. Not yet: .length (ARRAY_BASIC), iterating an
array, own methods — so the tasks only read elements at indexes known from the statement or from given numbers."""
from java_tasks import JavaOutputTask

SKILL = "ARRAY_INDEXING"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ai-podium", title="Пьедестал почёта",
        given=[("String[]", "finish")],
        variants=[{"finish": '{"Anya", "Boris", "Vika", "Gosha", "Dasha"}'},
                  {"finish": '{"Oleg", "Mila", "Timur", "Sonya"}'},
                  {"finish": '{"Katya", "Lyova", "Nina", "Petya", "Rita", "Stas"}'}],
        hidden=[{"finish": '{"Ira", "Gleb", "Zoya"}'},
                {"finish": '{"Max", "Eva", "Yana", "Lev", "Osya", "Fil", "Yulya"}'},
                {"finish": '{"Dina", "Artyom", "Vera", "Grisha"}'}],
        intro="Лыжная гонка закончилась. В массиве `finish` записаны имена лыжников в том порядке, в котором они "
              "пересекли финиш: самый первый элемент — победитель. Трёх лучших награждают на пьедестале.",
        steps=["Выведи три строки: `Gold: …`, `Silver: …` и `Bronze: …` — вместо многоточия имена тех, кто финишировал "
               "первым, вторым и третьим.",
               "Бери имена из массива `finish` по индексу. Участников гонки может быть больше или меньше, чем в заготовке, "
               "но всегда не меньше трёх."],
        hint="Индексы элементов массива начинаются с нуля. Например, в массиве `{{\"red\", \"green\", \"blue\"}}` "
             "элемент с индексом 1 — это `\"green\"`, а вовсе не `\"red\"`.",
        solution='System.out.println("Gold: " + finish[0]);\nSystem.out.println("Silver: " + finish[1]);\n'
                 'System.out.println("Bronze: " + finish[2]);',
        wrong=[("считает индексы с единицы: золото получает второй лыжник",
                'System.out.println("Gold: " + finish[1]);\nSystem.out.println("Silver: " + finish[2]);\n'
                'System.out.println("Bronze: " + finish[3]);'),
               ("скопировал строку и не поправил индекс: бронзу получает серебряный призёр",
                'System.out.println("Gold: " + finish[0]);\nSystem.out.println("Silver: " + finish[1]);\n'
                'System.out.println("Bronze: " + finish[1]);')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ai-lessons", title="Какой сейчас урок",
        given=[("String[]", "lessons"), ("int", "number")],
        variants=[{"lessons": '{"Math", "Russian", "Physics", "History", "Music"}', "number": "3"},
                  {"lessons": '{"Biology", "Literature", "Algebra", "Chemistry", "PE", "English"}', "number": "2"},
                  {"lessons": '{"Geography", "Geometry", "Computer Science", "Social Studies"}', "number": "1"}],
        hidden=[{"lessons": '{"Drawing", "Reading", "Crafts"}', "number": "2"},
                {"lessons": '{"Algebra", "Physics", "Chemistry", "Biology", "History", "Art", "Music"}', "number": "6"},
                {"lessons": '{"English", "Math"}', "number": "1"},
                {"lessons": '{"Crafts", "Literature", "PE", "Math"}', "number": "3"}],
        intro="В массиве `lessons` записано расписание уроков на сегодня по порядку. Сейчас идёт урок номер {number} "
              "(поле `number`) — в школе уроки нумеруют с 1.",
        steps=["Выведи строку `Now: …` — название урока с номером `number`. Помни: номера уроков начинаются с 1, "
               "а индексы массива — с 0.",
               "Следующей строкой выведи `Next: …` — название следующего урока. Урок номер `number` никогда не бывает "
               "последним, так что следующий урок есть всегда.",
               "Индекс вычисляй из `number`: при другом номере урока программа должна вывести другие уроки."],
        hint="Первый урок лежит в массиве под индексом 0, второй — под индексом 1: индекс всегда на единицу меньше номера. "
             "А следующий урок стоит сразу за текущим, и его индекс на единицу больше.",
        solution='System.out.println("Now: " + lessons[number - 1]);\nSystem.out.println("Next: " + lessons[number]);',
        wrong=[("путает номер урока с индексом: печатает следующий урок вместо текущего",
                'System.out.println("Now: " + lessons[number]);\nSystem.out.println("Next: " + lessons[number + 1]);'),
               ("берёт индексы из примера, а не вычисляет их из number",
                'System.out.println("Now: " + lessons[2]);\nSystem.out.println("Next: " + lessons[3]);')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ai-relay-swap", title="Замена в эстафете",
        given=[("String[]", "team"), ("int", "a"), ("int", "b")],
        variants=[{"team": '{"Anya", "Boris", "Vika", "Gosha", "Dasha"}', "a": "2", "b": "4"},
                  {"team": '{"Oleg", "Mila", "Timur", "Sonya", "Egor"}', "a": "1", "b": "3"},
                  {"team": '{"Katya", "Lyova", "Nina", "Petya", "Rita", "Stas"}', "a": "3", "b": "5"}],
        hidden=[{"team": '{"Ira", "Gleb", "Zoya"}', "a": "1", "b": "3"},
                {"team": '{"Max", "Eva", "Yana", "Lev", "Osya", "Fil", "Yulya"}', "a": "4", "b": "7"},
                {"team": '{"Dina", "Artyom"}', "a": "1", "b": "2"},
                {"team": '{"Vera", "Grisha", "Danya", "Ksyusha"}', "a": "2", "b": "3"}],
        intro="Бегуны эстафетной команды записаны в массив `team` по порядку этапов: кто бежит первый этап, кто второй "
              "и так далее. Перед стартом тренер решил поменять местами бегунов на этапах {a} и {b} (поля `a` и `b`). "
              "Этапы нумеруются с 1.",
        steps=["Поменяй местами элементы массива `team` для этапов `a` и `b`. Индекс элемента на 1 меньше номера этапа.",
               "Чтобы при обмене не потерять ни одного имени, сначала сохрани один из элементов во вспомогательную "
               "переменную типа `String`.",
               "После обмена выведи три строки: `Stage {a}: …` и `Stage {b}: …` — кто теперь бежит эти этапы, "
               "а потом `First stage: …` — кто теперь бежит первым. Номера этапов в строках бери из `a` и `b`."],
        hint="Если сразу записать в элемент для этапа `a` бегуна с этапа `b`, прежнее имя пропадёт: в массиве окажутся "
             "два одинаковых имени. Поэтому сначала скопируй его в отдельную переменную, а уже потом меняй элементы.",
        solution='String temp = team[a - 1];\nteam[a - 1] = team[b - 1];\nteam[b - 1] = temp;\n'
                 'System.out.println("Stage " + a + ": " + team[a - 1]);\nSystem.out.println("Stage " + b + ": " + team[b - 1]);\n'
                 'System.out.println("First stage: " + team[0]);',
        wrong=[("меняет без вспомогательной переменной: одно имя теряется, а другое оказывается на двух этапах",
                'team[a - 1] = team[b - 1];\nteam[b - 1] = team[a - 1];\n'
                'System.out.println("Stage " + a + ": " + team[a - 1]);\nSystem.out.println("Stage " + b + ": " + team[b - 1]);\n'
                'System.out.println("First stage: " + team[0]);'),
               ("использует номер этапа как индекс: меняет не тех бегунов",
                'String temp = team[a];\nteam[a] = team[b];\nteam[b] = temp;\n'
                'System.out.println("Stage " + a + ": " + team[a]);\nSystem.out.println("Stage " + b + ": " + team[b]);\n'
                'System.out.println("First stage: " + team[0]);')],
        constructs=["list"],
    ),
]
