"""PY_LIST_BASIC — «Списки». Taught before: print, variables, arithmetic, int/float, strings, type conversion, // and %,
+= -=, f-strings, conditions, for + range, accumulator, while, break/continue, list indexes (from 0, negative, len,
changing an element). Here: creating a list (empty or with values), append, len, the in / not in check, printing a list.
Not yet: iterating a list with for, string slicing and methods, functions, insert/remove/sort and list slices."""
from build import OutputTask

SKILL = "PY_LIST_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lb-rt-pizza-toppings", title="Начинка для пиццы",
        given=["topping"],
        variants=[{"topping": '"olives"'}, {"topping": '"ham"'}, {"topping": '"mushrooms"'}],
        hidden=[{"topping": '"pepper"'}, {"topping": '"olives"'}, {"topping": '"corn"'}],
        intro="Ты собираешь пиццу в приложении. Сыр и томаты кладут всегда, а третью начинку ты выбираешь сам — "
              "она записана в переменной `topping = {topping}`.",
        steps=["Создай список `pizza`, в котором сразу лежат две строки: `\"cheese\"` и `\"tomato\"`.",
               "Добавь в конец списка выбранную начинку через `append`.",
               "Выведи весь список командой `print(pizza)`.",
               "Следующей строкой выведи число начинок в виде `Toppings: 3` — посчитай его через `len`.",
               "Последней строкой выведи, есть ли в пицце оливки, в виде `Olives: True` или `Olives: False` — "
               "проверь это через `\"olives\" in pizza`."],
        hint="Список со значениями создают в квадратных скобках через запятую: `pizza = [\"cheese\", \"tomato\"]`. "
             "Чтобы добавить значение переменной, пиши её имя без кавычек: `pizza.append(topping)`. "
             "Выражение с `in` можно сразу подставить в f-строку.",
        solution='pizza = ["cheese", "tomato"]\npizza.append(topping)\nprint(pizza)\n'
                 'print(f"Toppings: {len(pizza)}")\nprint(f"Olives: {\'olives\' in pizza}")',
        wrong=[("добавляет строку \"topping\" вместо значения переменной",
                'pizza = ["cheese", "tomato"]\npizza.append("topping")\nprint(pizza)\n'
                'print(f"Toppings: {len(pizza)}")\nprint(f"Olives: {\'olives\' in pizza}")'),
               ("всегда пишет, что оливки есть",
                'pizza = ["cheese", "tomato"]\npizza.append(topping)\nprint(pizza)\n'
                'print(f"Toppings: {len(pizza)}")\nprint("Olives: True")'),
               ("забыта начинка по выбору: в списке только сыр и томаты",
                'pizza = ["cheese", "tomato"]\nprint(pizza)\n'
                'print(f"Toppings: {len(pizza)}")\nprint(f"Olives: {\'olives\' in pizza}")')],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lb-rt-free-seats", title="Свободные места в ряду",
        given=["seats", "taken"],
        variants=[{"seats": "8", "taken": "[2, 3, 7]"}, {"seats": "6", "taken": "[1, 6]"},
                  {"seats": "10", "taken": "[4, 5, 6, 9]"}],
        hidden=[{"seats": "3", "taken": "[]"}, {"seats": "4", "taken": "[1, 2, 3, 4]"}, {"seats": "7", "taken": "[7]"},
                {"seats": "5", "taken": "[2, 4]"}],
        intro="В ряду театра `seats = {seats}` мест с номерами от 1 до `seats`. Номера уже проданных мест записаны "
              "в списке `taken`. Кассир хочет увидеть все свободные места ряда.",
        steps=["Создай пустой список `free`.",
               "Циклом `for` перебери номера мест от 1 до `seats` включительно. Если номера нет в списке `taken` "
               "(проверь через `not in`), добавь его в `free` через `append`.",
               "После цикла выведи две строки: `Free seats: [1, 4, 5, 6, 8]` и число свободных мест `Free: 5` "
               "(через `len`).",
               "Если свободных мест нет, список просто будет пустым: `Free seats: []` и `Free: 0`."],
        hint="`seat not in taken` даёт `True`, если такого номера в списке проданных нет. "
             "Список можно вывести прямо в f-строке: `{{free}}`.",
        solution='free = []\nfor seat in range(1, seats + 1):\n    if seat not in taken:\n        free.append(seat)\n'
                 'print(f"Free seats: {free}")\nprint(f"Free: {len(free)}")',
        wrong=[("in вместо not in: собирает проданные места",
                'free = []\nfor seat in range(1, seats + 1):\n    if seat in taken:\n        free.append(seat)\n'
                'print(f"Free seats: {free}")\nprint(f"Free: {len(free)}")'),
               ("правая граница не входит в range: последнее место не проверяется",
                'free = []\nfor seat in range(1, seats):\n    if seat not in taken:\n        free.append(seat)\n'
                'print(f"Free seats: {free}")\nprint(f"Free: {len(free)}")')],
        constructs=["list", "for", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lb-rt-rabbits", title="Кролики Фибоначчи",
        given=["limit"],
        variants=[{"limit": "10"}, {"limit": "50"}, {"limit": "21"}],
        hidden=[{"limit": "1"}, {"limit": "2"}, {"limit": "100"}, {"limit": "13"}],
        intro="На ферме считают пары кроликов по месяцам. В первый и во второй месяц там по 1 паре, а дальше каждый месяц "
              "пар становится столько, сколько было в два предыдущих месяца вместе. Запиши в список число пар по месяцам, "
              "пока оно не превышает `limit = {limit}`.",
        steps=["Создай список `pairs`, в котором сразу лежат две единицы: `[1, 1]`.",
               "Пока сумма двух последних элементов списка не больше `limit`, повторяй в цикле `while`: "
               "добавь эту сумму в конец списка через `append`.",
               "Выведи три строки: `Pairs: [1, 1, 2, 3, 5, 8]`, число месяцев `Months: 6` (длина списка) и "
               "последнее число пар `Last: 8`"],
        hint="Два последних элемента списка — `pairs[-1]` и `pairs[-2]`. После каждого `append` они сдвигаются сами, "
             "поэтому условие `while` каждый раз проверяет новую сумму. Сумма, ровно равная `limit`, ещё подходит.",
        solution='pairs = [1, 1]\nwhile pairs[-1] + pairs[-2] <= limit:\n    pairs.append(pairs[-1] + pairs[-2])\n'
                 'print(f"Pairs: {pairs}")\nprint(f"Months: {len(pairs)}")\nprint(f"Last: {pairs[-1]}")',
        wrong=[("строгое сравнение: число, ровно равное limit, не попадает в список",
                'pairs = [1, 1]\nwhile pairs[-1] + pairs[-2] < limit:\n    pairs.append(pairs[-1] + pairs[-2])\n'
                'print(f"Pairs: {pairs}")\nprint(f"Months: {len(pairs)}")\nprint(f"Last: {pairs[-1]}")'),
               ("удваивает последнее число вместо суммы двух последних",
                'pairs = [1, 1]\nwhile pairs[-1] * 2 <= limit:\n    pairs.append(pairs[-1] * 2)\n'
                'print(f"Pairs: {pairs}")\nprint(f"Months: {len(pairs)}")\nprint(f"Last: {pairs[-1]}")'),
               ("берёт первый элемент вместо последнего",
                'pairs = [1, 1]\nwhile pairs[-1] + pairs[-2] <= limit:\n    pairs.append(pairs[-1] + pairs[-2])\n'
                'print(f"Pairs: {pairs}")\nprint(f"Months: {len(pairs)}")\nprint(f"Last: {pairs[0]}")')],
        constructs=["list", "while"],
    ),
]
