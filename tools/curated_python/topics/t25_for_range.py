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
]
