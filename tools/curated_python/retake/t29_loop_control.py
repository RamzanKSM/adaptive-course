"""PY_LOOP_CONTROL — «break и continue». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, += -=, f-strings, if/elif/else, comparisons, and/or/not, truthiness, for + range, accumulator, while.
Not yet: lists, string slicing and methods, functions."""
from build import OutputTask

SKILL = "PY_LOOP_CONTROL"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lc-rt-full-bus", title="Посадка в автобус",
        given=["people", "seats"],
        variants=[{"people": "7", "seats": "4"}, {"people": "5", "seats": "6"}, {"people": "6", "seats": "2"}],
        hidden=[{"people": "3", "seats": "3"}, {"people": "4", "seats": "3"}, {"people": "8", "seats": "1"}],
        intro="На остановке стоят `people = {people}` пассажиров, а в маршрутке осталось `seats = {seats}` свободных мест. "
              "Пассажиры заходят по одному, пока есть места.",
        steps=["Перебери циклом `for` номера пассажиров от 1 до `people` включительно.",
               "Если номер пассажира больше `seats`, мест уже нет: выведи `Bus is full` и останови цикл командой `break`.",
               "Иначе выведи строку вида `Passenger 1 is in`"],
        hint="`break` выходит из цикла сразу, поэтому `Bus is full` выведется ровно один раз. "
             "Пассажир с номером, равным `seats`, ещё садится — на последнее место. Если мест хватает всем, "
             "цикл закончится сам и `Bus is full` не появится.",
        solution='for p in range(1, people + 1):\n    if p > seats:\n        print("Bus is full")\n        break\n'
                 '    print(f"Passenger {p} is in")',
        wrong=[("continue вместо break: «Bus is full» печатается для каждого оставшегося пассажира",
                'for p in range(1, people + 1):\n    if p > seats:\n        print("Bus is full")\n        continue\n'
                '    print(f"Passenger {p} is in")'),
               ("нестрогое сравнение: последнее свободное место остаётся пустым",
                'for p in range(1, people + 1):\n    if p >= seats:\n        print("Bus is full")\n        break\n'
                '    print(f"Passenger {p} is in")')],
        constructs=["for"],
        must_use=[("Break", "Используй break, чтобы остановить посадку, когда мест нет")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lc-rt-pin-guess", title="Забытый PIN-код",
        given=["start", "code"],
        variants=[{"start": "4170", "code": "4173"}, {"start": "1205", "code": "1205"}, {"start": "8830", "code": "8899"}],
        hidden=[{"start": "5000", "code": "5004"}, {"start": "5000", "code": "5005"}, {"start": "3333", "code": "3333"},
                {"start": "7210", "code": "7212"}, {"start": "2000", "code": "1999"}],
        intro="Дима забыл PIN-код от телефона, но помнит, что он чуть больше `start = {start}`. Он пробует подряд "
              "`start`, `start + 1`, `start + 2` и так далее. Телефон даёт всего 5 попыток. "
              "Настоящий код — `code = {code}`.",
        steps=["Перебери циклом `for` номера попыток от 1 до 5 включительно.",
               "На каждой попытке посчитай пробуемый код: `start` плюс номер попытки минус 1.",
               "Если он равен `code`, выведи строку вида `Attempt 4: 4173 - unlocked` и останови цикл командой `break`.",
               "Иначе выведи строку вида `Attempt 1: 4170 - wrong`"],
        hint="На первой попытке Дима пробует сам `start`, поэтому прибавлять нужно `attempt - 1`. "
             "Без `break` после правильного кода цикл продолжит перебор и напечатает лишние попытки.",
        solution='for attempt in range(1, 6):\n    guess = start + attempt - 1\n    if guess == code:\n'
                 '        print(f"Attempt {attempt}: {guess} - unlocked")\n        break\n'
                 '    print(f"Attempt {attempt}: {guess} - wrong")',
        wrong=[("нет break: после правильного кода перебор продолжается",
                'for attempt in range(1, 6):\n    guess = start + attempt - 1\n    if guess == code:\n'
                '        print(f"Attempt {attempt}: {guess} - unlocked")\n'
                '    else:\n        print(f"Attempt {attempt}: {guess} - wrong")'),
               ("ошибка на единицу: первой пробует start + 1",
                'for attempt in range(1, 6):\n    guess = start + attempt\n    if guess == code:\n'
                '        print(f"Attempt {attempt}: {guess} - unlocked")\n        break\n'
                '    print(f"Attempt {attempt}: {guess} - wrong")'),
               ("range(1, 5): только 4 попытки",
                'for attempt in range(1, 5):\n    guess = start + attempt - 1\n    if guess == code:\n'
                '        print(f"Attempt {attempt}: {guess} - unlocked")\n        break\n'
                '    print(f"Attempt {attempt}: {guess} - wrong")')],
        constructs=["for", "if"],
        must_use=[("Break", "Используй break, чтобы остановить перебор, когда код подошёл")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lc-rt-fence-paint", title="Красим забор",
        given=["boards", "k", "paint", "per_board"],
        variants=[{"boards": "10", "k": "4", "paint": "1000", "per_board": "150"},
                  {"boards": "12", "k": "5", "paint": "2000", "per_board": "200"},
                  {"boards": "8", "k": "3", "paint": "500", "per_board": "120"}],
        hidden=[{"boards": "6", "k": "2", "paint": "300", "per_board": "100"},
                {"boards": "9", "k": "3", "paint": "250", "per_board": "100"},
                {"boards": "5", "k": "10", "paint": "1000", "per_board": "100"},
                {"boards": "15", "k": "4", "paint": "700", "per_board": "90"}],
        intro="Костя красит забор из `boards = {boards}` досок, они пронумерованы от 1. Каждая `k = {k}`-я доска "
              "(номер делится на `k` без остатка) сломана — её не красят, её заменят позже. На одну доску уходит "
              "`per_board = {per_board}` мл краски, а в банке `paint = {paint}` мл.",
        steps=["Заведи счётчик покрашенных досок `painted` со значением 0.",
               "Перебери циклом `for` номера досок от 1 до `boards` включительно.",
               "Если доска сломана, пропусти её командой `continue`.",
               "Если краски меньше, чем нужно на одну доску, выведи строку вида `Out of paint at board 9` "
               "и останови цикл командой `break`.",
               "Иначе отними краску на доску от `paint` и увеличь `painted` на 1.",
               "После цикла выведи две строки: `Painted: 6 boards` и `Paint left: 100 ml`"],
        hint="Порядок проверок важен: сначала сломанная доска (на неё краска не нужна), потом — хватает ли краски. "
             "Краски ровно на одну доску хватает. Если краски хватило на весь забор, цикл закончится сам, "
             "и строки про конец краски не будет.",
        solution='painted = 0\nfor board in range(1, boards + 1):\n    if board % k == 0:\n        continue\n'
                 '    if paint < per_board:\n        print(f"Out of paint at board {board}")\n        break\n'
                 '    paint -= per_board\n    painted += 1\n'
                 'print(f"Painted: {painted} boards")\nprint(f"Paint left: {paint} ml")',
        wrong=[("break вместо continue: работа обрывается на первой сломанной доске",
                'painted = 0\nfor board in range(1, boards + 1):\n    if board % k == 0:\n        break\n'
                '    if paint < per_board:\n        print(f"Out of paint at board {board}")\n        break\n'
                '    paint -= per_board\n    painted += 1\n'
                'print(f"Painted: {painted} boards")\nprint(f"Paint left: {paint} ml")'),
               ("continue вместо break: строка про конец краски печатается для каждой оставшейся доски",
                'painted = 0\nfor board in range(1, boards + 1):\n    if board % k == 0:\n        continue\n'
                '    if paint < per_board:\n        print(f"Out of paint at board {board}")\n        continue\n'
                '    paint -= per_board\n    painted += 1\n'
                'print(f"Painted: {painted} boards")\nprint(f"Paint left: {paint} ml")'),
               ("нестрогое сравнение: краски ровно на доску не хватает",
                'painted = 0\nfor board in range(1, boards + 1):\n    if board % k == 0:\n        continue\n'
                '    if paint <= per_board:\n        print(f"Out of paint at board {board}")\n        break\n'
                '    paint -= per_board\n    painted += 1\n'
                'print(f"Painted: {painted} boards")\nprint(f"Paint left: {paint} ml")')],
        constructs=["for"],
        must_use=[("Break", "Используй break, чтобы остановить работу, когда кончилась краска"),
                  ("Continue", "Используй continue, чтобы пропустить сломанную доску")],
    ),
]
