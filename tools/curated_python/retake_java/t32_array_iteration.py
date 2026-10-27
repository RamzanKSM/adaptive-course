"""ARRAY_ITERATION — «Перебор массива» (Java): цикл for-each и цикл по индексам, сумма, подсчёт по условию, поиск
минимума. Taught before: everything up to arrays (indexes, .length, new int[n], filling in a loop), conditions,
loops, break. Not yet: own methods."""
from java_tasks import JavaOutputTask

SKILL = "ARRAY_ITERATION"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-it-rt-word-lengths", title="Длина слов в диктанте",
        given=[("String[]", "words")],
        variants=[{"words": '{"cat", "window", "sun", "garden"}'}, {"words": '{"river", "boat", "island"}'},
                  {"words": '{"red", "green", "blue", "yellow", "white"}'}],
        hidden=[{"words": '{"a"}'}, {"words": '{"hello", "world"}'},
                {"words": '{"one", "two", "three", "four", "five", "six", "seven"}'}],
        intro="Учительница английского продиктовала слова, и они лежат в массиве `words`. Маша хочет проверить, "
              "сколько букв в каждом слове и сколько букв она написала всего.",
        steps=["Заведи до цикла переменную для общего числа букв со значением 0.",
               "Пройди по массиву циклом `for-each` и для каждого слова выведи строку в формате `window - 6` — "
               "слово, пробел, дефис, пробел и число букв в нём. Добавь это число к общему.",
               "После цикла выведи `Letters in total: …`."],
        hint="В цикле `for (String word : words)` переменная `word` по очереди становится каждым словом. "
             "Число букв в строке даёт `word.length()` — со скобками, это метод строки.",
        solution='int total = 0;\nfor (String word : words) {\n    System.out.println(word + " - " + word.length());\n'
                 '    total += word.length();\n}\nSystem.out.println("Letters in total: " + total);',
        wrong=[("= вместо +=: в итоге оказывается длина только последнего слова",
                'int total = 0;\nfor (String word : words) {\n    System.out.println(word + " - " + word.length());\n'
                '    total = word.length();\n}\nSystem.out.println("Letters in total: " + total);'),
               ("считает слова, а не буквы: прибавляет по 1",
                'int total = 0;\nfor (String word : words) {\n    System.out.println(word + " - " + word.length());\n'
                '    total++;\n}\nSystem.out.println("Letters in total: " + total);')],
        constructs=["list", "for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-it-rt-guest-list", title="Список гостей",
        given=[("String[]", "guests"), ("String", "name")],
        variants=[{"guests": '{"Anya", "Boris", "Vika", "Gosha", "Dasha"}', "name": '"Vika"'},
                  {"guests": '{"Oleg", "Mila", "Timur", "Sonya"}', "name": '"Egor"'},
                  {"guests": '{"Katya", "Lyova", "Nina", "Lyova", "Rita"}', "name": '"Lyova"'}],
        hidden=[{"guests": '{"Ira"}', "name": '"Ira"'}, {"guests": '{"Max", "Eva", "Yana"}', "name": '"Yana"'},
                {"guests": '{"Dina", "Artyom", "Dina", "Vera"}', "name": '"Dina"'},
                {"guests": '{"Fedya", "Liza", "Roma"}', "name": '"Anya"'},
                {"guests": '{"Gleb", "Zoya", "Lev", "Osya", "Zoya", "Fil"}', "name": '"Zoya"'}],
        intro="На входе в клуб охранник ищет гостя в списке `guests`. Имя гостя, который пришёл, записано в поле `name`. "
              "В списке могут быть тёзки — тогда нужен тот, кто записан раньше.",
        steps=["Заведи переменную `place` со значением 0 — это будет номер гостя в списке (с 1), а 0 значит «не нашёлся».",
               "Пройди по массиву циклом с индексом. Как только элемент равен `name`, запиши в `place` номер этого "
               "элемента (на 1 больше индекса) и выйди из цикла командой `break`.",
               "После цикла: если `place` больше 0, выведи `Name is number … on the list` (вместо Name — значение "
               "`name`), иначе выведи `Name is not on the list`."],
        hint="Строки сравнивают методом `equals`: `guests[i].equals(name)`. А `break` нужен, чтобы тёзка дальше по "
             "списку не перезаписал уже найденный номер.",
        solution='int place = 0;\nfor (int i = 0; i < guests.length; i++) {\n    if (guests[i].equals(name)) {\n        place = i + 1;\n'
                 '        break;\n    }\n}\nif (place > 0) {\n    System.out.println(name + " is number " + place + " on the list");\n} else {\n'
                 '    System.out.println(name + " is not on the list");\n}',
        wrong=[("нет break: находит последнего тёзку, а не первого",
                'int place = 0;\nfor (int i = 0; i < guests.length; i++) {\n    if (guests[i].equals(name)) {\n        place = i + 1;\n'
                '    }\n}\nif (place > 0) {\n    System.out.println(name + " is number " + place + " on the list");\n} else {\n'
                '    System.out.println(name + " is not on the list");\n}'),
               ("записывает индекс, а не номер: первый в списке гость считается ненайденным",
                'int place = 0;\nfor (int i = 0; i < guests.length; i++) {\n    if (guests[i].equals(name)) {\n        place = i;\n'
                '        break;\n    }\n}\nif (place > 0) {\n    System.out.println(name + " is number " + place + " on the list");\n} else {\n'
                '    System.out.println(name + " is not on the list");\n}')],
        constructs=["list", "for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-it-rt-cafe-good-days", title="Удачные дни кафе",
        given=[("int[]", "revenue")],
        variants=[{"revenue": "{400, 650, 300, 720, 530}"}, {"revenue": "{900, 850, 1200, 700, 950, 1000}"},
                  {"revenue": "{150, 300, 90, 210}"}],
        hidden=[{"revenue": "{500}"}, {"revenue": "{300, 300, 300}"}, {"revenue": "{100, 200, 300}"},
                {"revenue": "{1000, 10, 10, 10, 10}"}, {"revenue": "{50, 70, 60, 80, 40, 90, 30}"}],
        intro="Хозяйка кафе записала выручку за каждый день в тысячах рублей — массив `revenue`. Удачным она называет "
              "день, когда выручка больше средней за все дни.",
        steps=["Первым циклом посчитай сумму всех элементов, а среднюю выручку — как сумму, делённую нацело на число "
               "дней. Выведи `Average: …`.",
               "Вторым циклом с индексом пройди по массиву и для каждого дня, где выручка больше средней, выведи "
               "`Good day …: …` — номер дня (на 1 больше индекса) и выручку.",
               "После второго цикла выведи `Good days: …` — сколько таких дней."],
        hint="Сравнивать со средней можно только тогда, когда сумма уже посчитана целиком, — поэтому циклов два. "
             "День, когда выручка ровно равна средней, удачным не считается.",
        solution='int sum = 0;\nfor (int r : revenue) {\n    sum += r;\n}\nint average = sum / revenue.length;\n'
                 'System.out.println("Average: " + average);\nint good = 0;\nfor (int i = 0; i < revenue.length; i++) {\n'
                 '    if (revenue[i] > average) {\n        System.out.println("Good day " + (i + 1) + ": " + revenue[i]);\n        good++;\n'
                 '    }\n}\nSystem.out.println("Good days: " + good);',
        wrong=[(">= вместо >: день ровно со средней выручкой считается удачным",
                'int sum = 0;\nfor (int r : revenue) {\n    sum += r;\n}\nint average = sum / revenue.length;\n'
                'System.out.println("Average: " + average);\nint good = 0;\nfor (int i = 0; i < revenue.length; i++) {\n'
                '    if (revenue[i] >= average) {\n        System.out.println("Good day " + (i + 1) + ": " + revenue[i]);\n        good++;\n'
                '    }\n}\nSystem.out.println("Good days: " + good);'),
               ("делит сумму на число дней минус 1: средняя получается завышенной",
                'int sum = 0;\nfor (int r : revenue) {\n    sum += r;\n}\nint average = sum / (revenue.length - 1);\n'
                'System.out.println("Average: " + average);\nint good = 0;\nfor (int i = 0; i < revenue.length; i++) {\n'
                '    if (revenue[i] > average) {\n        System.out.println("Good day " + (i + 1) + ": " + revenue[i]);\n        good++;\n'
                '    }\n}\nSystem.out.println("Good days: " + good);')],
        constructs=["list", "for", "if"],
    ),
]
