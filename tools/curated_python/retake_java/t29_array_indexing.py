"""ARRAY_INDEXING — «Индексы массива» (Java). Taught before: println, variables, arithmetic, types, String, / and %,
+= ++, conditions, switch, for, accumulator, while, loop termination. Here: an element by index, indexes from 0,
a number counted from 1 turned into an index, changing an element. Not yet: .length (ARRAY_BASIC), iterating an
array, own methods — so the tasks only read elements at indexes known from the statement or from given numbers."""
from java_tasks import JavaOutputTask

SKILL = "ARRAY_INDEXING"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ai-rt-safe-code", title="Код от сейфа",
        given=[("int[]", "code")],
        variants=[{"code": "{4, 7, 1, 9}"}, {"code": "{2, 0, 5, 3}"}, {"code": "{8, 6, 6, 1}"}],
        hidden=[{"code": "{1, 2, 3, 4}"}, {"code": "{9, 9, 0, 0}"}, {"code": "{0, 5, 8, 2}"}, {"code": "{3, 1, 4, 1}"}],
        intro="Код от школьного сейфа — четыре цифры, они записаны в массив `code` по порядку. Завхоз оставляет "
              "сменщику не весь код, а подсказку по нему.",
        steps=["Выведи строку `First digit: …` — первую цифру кода.",
               "Выведи строку `Last digit: …` — четвёртую, последнюю цифру.",
               "Выведи строку `Middle sum: …` — сумму второй и третьей цифр.",
               "Бери цифры из массива `code` по индексу."],
        hint="Индексы начинаются с нуля: первая цифра — `code[0]`. Значит, у четвёртой цифры индекс 3. "
             "Сумму в строке возьми в скобки, иначе цифры склеятся.",
        solution='System.out.println("First digit: " + code[0]);\nSystem.out.println("Last digit: " + code[3]);\n'
                 'System.out.println("Middle sum: " + (code[1] + code[2]));',
        wrong=[("считает индексы с единицы для первой цифры: выводит вторую",
                'System.out.println("First digit: " + code[1]);\nSystem.out.println("Last digit: " + code[3]);\n'
                'System.out.println("Middle sum: " + (code[1] + code[2]));'),
               ("средние цифры по индексам 2 и 3: складывает третью и четвёртую",
                'System.out.println("First digit: " + code[0]);\nSystem.out.println("Last digit: " + code[3]);\n'
                'System.out.println("Middle sum: " + (code[2] + code[3]));')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ai-rt-doctor-queue", title="Очередь к врачу",
        given=[("String[]", "queue"), ("int", "place")],
        variants=[{"queue": '{"Anya", "Boris", "Vika", "Gosha", "Dasha"}', "place": "3"},
                  {"queue": '{"Oleg", "Mila", "Timur", "Sonya"}', "place": "2"},
                  {"queue": '{"Katya", "Lyova", "Nina", "Petya", "Rita", "Stas"}', "place": "4"}],
        hidden=[{"queue": '{"Ira", "Gleb", "Zoya"}', "place": "2"},
                {"queue": '{"Max", "Eva", "Yana", "Lev", "Osya", "Fil", "Yulya"}', "place": "6"},
                {"queue": '{"Dina", "Artyom", "Vera", "Grisha"}', "place": "3"},
                {"queue": '{"Fedya", "Liza", "Roma", "Tanya", "Yura"}', "place": "4"}],
        intro="В массиве `queue` записаны имена людей в очереди к врачу — по порядку, начиная с того, кто стоит первым. "
              "Ты стоишь на месте номер {place} (поле `place`), места считают с 1. Ты никогда не первый и не последний.",
        steps=["Выведи строку `Me: …` — имя человека на месте `place`.",
               "Выведи строку `Before me: …` — кто стоит прямо перед тобой.",
               "Выведи строку `After me: …` — кто стоит прямо за тобой.",
               "Индексы вычисляй из `place`: при другом месте программа должна вывести других людей."],
        hint="Место номер 1 — это индекс 0, поэтому твой индекс — `place - 1`. Тот, кто перед тобой, стоит на один "
             "индекс левее, а тот, кто за тобой, — на один правее.",
        solution='System.out.println("Me: " + queue[place - 1]);\nSystem.out.println("Before me: " + queue[place - 2]);\n'
                 'System.out.println("After me: " + queue[place]);',
        wrong=[("использует номер места как индекс: всё сдвинуто на одного человека",
                'System.out.println("Me: " + queue[place]);\nSystem.out.println("Before me: " + queue[place - 1]);\n'
                'System.out.println("After me: " + queue[place + 1]);'),
               ("перепутал соседей: перед тобой и за тобой поменялись местами",
                'System.out.println("Me: " + queue[place - 1]);\nSystem.out.println("Before me: " + queue[place]);\n'
                'System.out.println("After me: " + queue[place - 2]);')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ai-rt-league-table", title="Очки в турнире",
        given=[("int[]", "points"), ("int", "home"), ("int", "guest"), ("int", "homeGoals"), ("int", "guestGoals")],
        variants=[{"points": "{7, 4, 9, 3}", "home": "2", "guest": "4", "homeGoals": "2", "guestGoals": "1"},
                  {"points": "{10, 6, 6, 2, 5}", "home": "1", "guest": "3", "homeGoals": "0", "guestGoals": "3"},
                  {"points": "{4, 8, 1}", "home": "3", "guest": "1", "homeGoals": "2", "guestGoals": "2"}],
        hidden=[{"points": "{0, 0}", "home": "1", "guest": "2", "homeGoals": "1", "guestGoals": "1"},
                {"points": "{5, 2, 9, 7}", "home": "4", "guest": "1", "homeGoals": "3", "guestGoals": "0"},
                {"points": "{1, 2, 3, 4, 5, 6}", "home": "5", "guest": "6", "homeGoals": "1", "guestGoals": "4"},
                {"points": "{12, 3, 3}", "home": "2", "guest": "3", "homeGoals": "0", "guestGoals": "0"}],
        intro="В школьном турнире по футболу команды пронумерованы с 1, а их очки записаны в массив `points`. "
              "Сыграли команды номер {home} (поле `home`) и {guest} (поле `guest`), счёт {homeGoals}:{guestGoals} "
              "(поля `homeGoals` и `guestGoals`). За победу дают 3 очка, за ничью — по 1 очку обеим, за поражение — 0.",
        steps=["Добавь очки за матч прямо в массив `points`: победителю — 3, а при ничьей — по 1 обеим командам.",
               "Выведи строку `Team {home}: … points` и строку `Team {guest}: … points` — сколько очков теперь у этих "
               "команд. Номера команд в строках бери из `home` и `guest`.",
               "Последней строкой выведи `Team 1 now: …` — сколько очков теперь у команды номер 1."],
        hint="Индекс команды на 1 меньше её номера. Элемент массива меняется так же, как переменная: "
             "`points[i] += 3;`. Исходов три — победа хозяев, победа гостей и ничья, — так что пригодится `else if`.",
        solution='if (homeGoals > guestGoals) {\n    points[home - 1] += 3;\n} else if (homeGoals < guestGoals) {\n'
                 '    points[guest - 1] += 3;\n} else {\n    points[home - 1] += 1;\n    points[guest - 1] += 1;\n}\n'
                 'System.out.println("Team " + home + ": " + points[home - 1] + " points");\n'
                 'System.out.println("Team " + guest + ": " + points[guest - 1] + " points");\n'
                 'System.out.println("Team 1 now: " + points[0]);',
        wrong=[("нет ветки для ничьей: при равном счёте 3 очка получают гости",
                'if (homeGoals > guestGoals) {\n    points[home - 1] += 3;\n} else {\n    points[guest - 1] += 3;\n}\n'
                'System.out.println("Team " + home + ": " + points[home - 1] + " points");\n'
                'System.out.println("Team " + guest + ": " + points[guest - 1] + " points");\n'
                'System.out.println("Team 1 now: " + points[0]);'),
               ("считает очки в отдельных переменных и не меняет массив: у команды 1 очки не растут",
                'int h = points[home - 1];\nint g = points[guest - 1];\nif (homeGoals > guestGoals) {\n    h += 3;\n'
                '} else if (homeGoals < guestGoals) {\n    g += 3;\n} else {\n    h += 1;\n    g += 1;\n}\n'
                'System.out.println("Team " + home + ": " + h + " points");\n'
                'System.out.println("Team " + guest + ": " + g + " points");\n'
                'System.out.println("Team 1 now: " + points[0]);')],
        constructs=["list", "if"],
    ),
]
