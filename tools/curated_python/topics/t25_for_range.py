"""PY_FOR_RANGE — «Цикл for и range». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, += -=, f-strings, if/else, comparisons, and/or/not, elif, truthiness.
Not yet: accumulating a result in a loop, while, break/continue, lists, functions."""
from build import OutputTask

SKILL = "PY_FOR_RANGE"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-for-notebooks", title="Подписываем тетради",
        given=["n"],
        variants=[{"n": "5"}, {"n": "3"}, {"n": "7"}],
        hidden=[{"n": "1"}, {"n": "4"}, {"n": "6"}],
        intro="Учительница раздаёт тетради и подписывает на каждой номер, начиная с 1. Сколько всего тетрадей, записано в `n = {n}`.",
        steps=["Напиши цикл `for` с `range`, который перебирает числа от 1 до `n` включительно.",
               "На каждом шаге выведи отдельной строкой надпись вида `Notebook 1`: слово `Notebook`, пробел и номер."],
        hint="`range(a, b)` выдаёт числа от `a` до `b - 1`: правая граница в него не входит. "
             "Подумай, какое число написать справа, чтобы последней была тетрадь с номером `n`.",
        solution='for i in range(1, n + 1):\n    print(f"Notebook {i}")',
        wrong=[("range(n) начинает с 0 и не доходит до n",
                'for i in range(n):\n    print(f"Notebook {i}")'),
               ("правая граница не входит в range: последняя тетрадь пропущена",
                'for i in range(1, n):\n    print(f"Notebook {i}")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-for-countdown", title="Обратный отсчёт",
        given=["start"],
        variants=[{"start": "5"}, {"start": "3"}, {"start": "8"}],
        hidden=[{"start": "1"}, {"start": "4"}, {"start": "9"}],
        intro="Перед запуском ракеты ведут обратный отсчёт. Он начинается с числа `start = {start}`.",
        steps=["С помощью цикла `for` и `range` выведи числа от `start` до 1 по убыванию, каждое на отдельной строке.",
               "После цикла выведи одной строкой `Liftoff!`"],
        hint="У `range` может быть третье число — шаг. Если шаг отрицательный, числа идут по убыванию: "
             "`range(20, 5, -5)` даёт 20, 15, 10. Вторая граница по-прежнему не входит.",
        solution='for i in range(start, 0, -1):\n    print(i)\nprint("Liftoff!")',
        wrong=[("останавливается на 2: единица не выводится",
                'for i in range(start, 1, -1):\n    print(i)\nprint("Liftoff!")'),
               ("«Liftoff!» внутри цикла — печатается после каждого числа",
                'for i in range(start, 0, -1):\n    print(i)\n    print("Liftoff!")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-for-clap", title="Игра «Clap»",
        given=["n", "k"],
        variants=[{"n": "10", "k": "3"}, {"n": "7", "k": "2"}, {"n": "9", "k": "4"}],
        hidden=[{"n": "5", "k": "5"}, {"n": "6", "k": "3"}, {"n": "8", "k": "3"}, {"n": "4", "k": "2"}],
        intro="Ребята по очереди называют числа от 1 до `n = {n}`. Но если число делится на `k = {k}` без остатка, "
              "вместо него нужно сказать «Clap».",
        steps=["Перебери циклом `for` числа от 1 до `n` включительно.",
               "Если число делится на `k` без остатка, выведи слово `Clap`.",
               "Иначе выведи само число.",
               "Каждое слово или число выводи на отдельной строке."],
        hint="Внутри цикла можно писать `if` и `else` — с дополнительным отступом. "
             "Число `i` делится на `k` без остатка, когда `i % k` равно 0.",
        solution='for i in range(1, n + 1):\n    if i % k == 0:\n        print("Clap")\n    else:\n        print(i)',
        wrong=[("нет else: число печатается и после «Clap»",
                'for i in range(1, n + 1):\n    if i % k == 0:\n        print("Clap")\n    print(i)'),
               ("цикл от 0 до n - 1: лишний «Clap» в начале и нет последнего числа",
                'for i in range(n):\n    if i % k == 0:\n        print("Clap")\n    else:\n        print(i)')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-for-times-table", title="Строка таблицы умножения",
        given=["n"],
        variants=[{"n": "7"}, {"n": "4"}, {"n": "9"}],
        hidden=[{"n": "1"}, {"n": "6"}, {"n": "12"}],
        intro="Петя учит таблицу умножения и хочет распечатать шпаргалку для числа `n = {n}` — "
              "как оно умножается на числа от 1 до 10.",
        steps=["Напиши цикл `for` с `range`, который перебирает множители от 1 до 10 включительно.",
               "На каждом шаге выведи отдельной строкой пример вида `3 x 4 = 12`: число `n`, пробел, буква `x`, "
               "пробел, множитель, ` = ` и произведение."],
        hint="`range(1, 10)` остановится на 9, потому что правая граница не входит. "
             "В f-строке в фигурных скобках можно сразу посчитать произведение: `{{n * i}}`.",
        solution='for i in range(1, 11):\n    print(f"{n} x {i} = {n * i}")',
        wrong=[("правая граница не входит в range: нет строки с 10",
                'for i in range(1, 10):\n    print(f"{n} x {i} = {n * i}")'),
               ("range(10) начинает с 0 и не доходит до 10",
                'for i in range(10):\n    print(f"{n} x {i} = {n * i}")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-for-even-houses", title="Чётная сторона улицы",
        given=["last"],
        variants=[{"last": "10"}, {"last": "7"}, {"last": "14"}],
        hidden=[{"last": "2"}, {"last": "3"}, {"last": "12"}, {"last": "9"}],
        intro="Почтальон разносит письма по чётной стороне улицы: в дома 2, 4, 6 и так далее. "
              "Самый большой номер дома на улице — `last = {last}` (он может быть и нечётным).",
        steps=["С помощью цикла `for` и `range` с шагом 2 перебери номера 2, 4, 6, … — все чётные номера, "
               "которые не больше `last`.",
               "Каждый номер выведи на отдельной строке в виде `House 4`.",
               "После цикла выведи одной строкой `Round finished`"],
        hint="Третье число в `range` — шаг: `range(5, 20, 5)` даёт 5, 10, 15. Правая граница не входит, "
             "поэтому, чтобы дом с номером `last` попал в обход, справа нужно поставить `last + 1`.",
        solution='for house in range(2, last + 1, 2):\n    print(f"House {house}")\nprint("Round finished")',
        wrong=[("правая граница last: последний чётный дом пропущен",
                'for house in range(2, last, 2):\n    print(f"House {house}")\nprint("Round finished")'),
               ("начинает с 0: появляется дом с номером 0",
                'for house in range(0, last + 1, 2):\n    print(f"House {house}")\nprint("Round finished")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-for-evening-frost", title="Вечерний прогноз",
        given=["t", "drop"],
        variants=[{"t": "5", "drop": "2"}, {"t": "3", "drop": "1"}, {"t": "8", "drop": "3"}],
        hidden=[{"t": "4", "drop": "2"}, {"t": "10", "drop": "1"}, {"t": "0", "drop": "1"}, {"t": "12", "drop": "4"}],
        intro="В 18:00 на улице `t = {t}` градусов, и каждый час до полуночи становится холоднее на `drop = {drop}` градуса. "
              "Метеостанция печатает прогноз по часам с 18 до 23 и предупреждает о гололёде, когда температура ниже нуля.",
        steps=["Перебери циклом `for` часы от 18 до 23 включительно.",
               "На каждом шаге посчитай температуру: `t` минус `drop`, умноженное на число часов, прошедших с 18:00.",
               "Если температура ниже 0, выведи строку вида `21:00 -1 C, ice`.",
               "Иначе выведи строку вида `19:00 3 C` — без предупреждения."],
        hint="Сколько часов прошло с 18:00 — это `hour - 18`: в 18 часов прошло 0 часов, в 19 — 1 час. "
             "Ровно 0 градусов — ещё не «ниже нуля», предупреждения нет.",
        solution='for hour in range(18, 24):\n    temp = t - (hour - 18) * drop\n    if temp < 0:\n'
                 '        print(f"{hour}:00 {temp} C, ice")\n    else:\n        print(f"{hour}:00 {temp} C")',
        wrong=[("правая граница 23 не входит в range: нет прогноза на 23:00",
                'for hour in range(18, 23):\n    temp = t - (hour - 18) * drop\n    if temp < 0:\n'
                '        print(f"{hour}:00 {temp} C, ice")\n    else:\n        print(f"{hour}:00 {temp} C")'),
               ("нестрогое сравнение: при 0 градусов тоже предупреждает о гололёде",
                'for hour in range(18, 24):\n    temp = t - (hour - 18) * drop\n    if temp <= 0:\n'
                '        print(f"{hour}:00 {temp} C, ice")\n    else:\n        print(f"{hour}:00 {temp} C")')],
        constructs=["for"],
    ),
]
