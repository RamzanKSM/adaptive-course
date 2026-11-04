"""PY_ARITHMETIC_BASIC — «Арифметика». Taught before: print (several values, sep=, end=), variables, assignment.
Here: + - * /, the order of operations and parentheses, a result kept in a variable and used further.
Not yet: int/float in detail, // and %, += -=, type conversion, string concatenation, f-strings, conditions, loops."""
from build import OutputTask

SKILL = "PY_ARITHMETIC_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ar-pizza-night", title="Пицца для друзей",
        given=["pizza", "juice", "friends"],
        variants=[{"pizza": "550", "juice": "90", "friends": "4"}, {"pizza": "720", "juice": "110", "friends": "3"},
                  {"pizza": "480", "juice": "75", "friends": "6"}],
        hidden=[{"pizza": "600", "juice": "100", "friends": "5"}, {"pizza": "999", "juice": "60", "friends": "2"},
                {"pizza": "350", "juice": "120", "friends": "8"}],
        intro="Друзья собираются вечером. Они заказывают 2 одинаковые пиццы по `pizza = {pizza}` руб. и по бутылке сока "
              "на каждого: бутылка стоит `juice = {juice}` руб., а друзей `friends = {friends}`.",
        steps=["Посчитай стоимость пицц: цена одной пиццы, умноженная на 2. Сохрани в переменную `pizzas`.",
               "Посчитай стоимость сока: цена бутылки, умноженная на число друзей. Сохрани в переменную `drinks`.",
               "Посчитай общую сумму `total` — сложи `pizzas` и `drinks`.",
               "Выведи три строки: `Pizzas:` и `pizzas`, `Drinks:` и `drinks`, `Total:` и `total`."],
        hint="Умножение в Python — это `*`, сложение — `+`. Результат вычисления можно сохранить в переменную "
             "и потом использовать дальше: `total = pizzas + drinks`.",
        solution='pizzas = pizza * 2\ndrinks = juice * friends\ntotal = pizzas + drinks\nprint("Pizzas:", pizzas)\n'
                 'print("Drinks:", drinks)\nprint("Total:", total)',
        wrong=[("складывает вместо умножения",
                'pizzas = pizza * 2\ndrinks = juice + friends\ntotal = pizzas + drinks\nprint("Pizzas:", pizzas)\n'
                'print("Drinks:", drinks)\nprint("Total:", total)'),
               ("забывает, что пицц две",
                'pizzas = pizza\ndrinks = juice * friends\ntotal = pizzas + drinks\nprint("Pizzas:", pizzas)\n'
                'print("Drinks:", drinks)\nprint("Total:", total)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ar-age-facts", title="Сколько мне лет",
        given=["birth_year", "this_year"],
        variants=[{"birth_year": "2007", "this_year": "2026"}, {"birth_year": "2010", "this_year": "2026"},
                  {"birth_year": "1999", "this_year": "2025"}],
        hidden=[{"birth_year": "2000", "this_year": "2026"}, {"birth_year": "2015", "this_year": "2024"},
                {"birth_year": "1985", "this_year": "2030"}],
        intro="Анкета на сайте по году рождения считает несколько фактов о пользователе. Год рождения — "
              "`birth_year = {birth_year}`, текущий год — `this_year = {this_year}`. Будем считать, что день рождения "
              "в этом году уже прошёл.",
        steps=["Посчитай возраст `age`: текущий год минус год рождения.",
               "Посчитай `next_age` — сколько лет будет через год: `age` плюс 1.",
               "Посчитай `months` — сколько полных месяцев прожито: `age`, умноженный на 12.",
               "Выведи три строки: `Age:` и `age`, `Next year:` и `next_age`, `Months:` и `months`."],
        hint="При вычитании важен порядок: `2026 - 2010` даёт `16`, а `2010 - 2026` даёт `-16`. "
             "Из большего года вычитай меньший.",
        solution='age = this_year - birth_year\nnext_age = age + 1\nmonths = age * 12\nprint("Age:", age)\n'
                 'print("Next year:", next_age)\nprint("Months:", months)',
        wrong=[("вычитает в обратном порядке — возраст отрицательный",
                'age = birth_year - this_year\nnext_age = age + 1\nmonths = age * 12\nprint("Age:", age)\n'
                'print("Next year:", next_age)\nprint("Months:", months)'),
               ("считает месяцы от следующего года",
                'age = this_year - birth_year\nnext_age = age + 1\nmonths = next_age * 12\nprint("Age:", age)\n'
                'print("Next year:", next_age)\nprint("Months:", months)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ar-room-repair", title="Ремонт комнаты",
        given=["length", "width", "height"],
        variants=[{"length": "5", "width": "4", "height": "3"}, {"length": "6", "width": "3", "height": "3"},
                  {"length": "4", "width": "4", "height": "2"}],
        hidden=[{"length": "7", "width": "5", "height": "3"}, {"length": "3", "width": "2", "height": "4"},
                {"length": "10", "width": "6", "height": "3"}],
        intro="Семья делает ремонт. Комната — прямоугольник длиной `length = {length}` м и шириной `width = {width}` м, "
              "высота потолка `height = {height}` м. Нужно узнать площадь пола (для ламината) и площадь всех четырёх "
              "стен (для обоев).",
        steps=["Посчитай `floor` — площадь пола: длина, умноженная на ширину.",
               "Посчитай `walls` — площадь стен: периметр комнаты, умноженный на высоту. "
               "Периметр — это 2, умноженное на сумму длины и ширины, сумму возьми в скобки.",
               "Посчитай `total` — сумму `floor` и `walls`.",
               "Выведи три строки: `Floor:`, `floor` и `m2`; `Walls:`, `walls` и `m2`; `Total:`, `total` и `m2`. "
               "Например: `Floor: 6 m2`."],
        hint="Умножение выполняется раньше сложения: `2 * 5 + 4` — это `14`, а `2 * (5 + 4)` — это `18`. "
             "Поэтому сумму длины и ширины обязательно возьми в скобки.",
        solution='floor = length * width\nwalls = 2 * (length + width) * height\ntotal = floor + walls\n'
                 'print("Floor:", floor, "m2")\nprint("Walls:", walls, "m2")\nprint("Total:", total, "m2")',
        wrong=[("забывает скобки — умножение выполняется раньше сложения",
                'floor = length * width\nwalls = 2 * length + width * height\ntotal = floor + walls\n'
                'print("Floor:", floor, "m2")\nprint("Walls:", walls, "m2")\nprint("Total:", total, "m2")'),
               ("забывает умножить периметр на высоту",
                'floor = length * width\nwalls = 2 * (length + width)\ntotal = floor + walls\n'
                'print("Floor:", floor, "m2")\nprint("Walls:", walls, "m2")\nprint("Total:", total, "m2")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ar-quarter-grades", title="Средняя оценка за четверть",
        given=["g1", "g2", "g3", "g4"],
        variants=[{"g1": "5", "g2": "4", "g3": "4", "g4": "3"}, {"g1": "3", "g2": "5", "g3": "5", "g4": "5"},
                  {"g1": "4", "g2": "4", "g3": "2", "g4": "5"}],
        hidden=[{"g1": "5", "g2": "5", "g3": "5", "g4": "5"}, {"g1": "2", "g2": "3", "g3": "4", "g4": "5"},
                {"g1": "3", "g2": "3", "g3": "4", "g4": "3"}],
        intro="За четверть по математике у ученика четыре оценки: `g1 = {g1}`, `g2 = {g2}`, `g3 = {g3}`, `g4 = {g4}`. "
              "Электронный дневник показывает их сумму и среднюю оценку.",
        steps=["Выведи `Grades:` и все четыре оценки одним `print`.",
               "Посчитай `total` — сумму четырёх оценок.",
               "Посчитай `average` — сумму, делённую на 4. Деление в Python — это `/`.",
               "Выведи `Sum:` и `total`, затем `Average:` и `average`. "
               "Деление через `/` всегда даёт дробное число, например `Average: 4.0`."],
        hint="Если записать всё одной строкой `g1 + g2 + g3 + g4 / 4`, на 4 разделится только последняя оценка: "
             "деление выполняется раньше сложения. Поэтому сначала посчитай сумму, а потом дели её.",
        solution='print("Grades:", g1, g2, g3, g4)\ntotal = g1 + g2 + g3 + g4\naverage = total / 4\n'
                 'print("Sum:", total)\nprint("Average:", average)',
        wrong=[("делит на 4 только последнюю оценку",
                'print("Grades:", g1, g2, g3, g4)\ntotal = g1 + g2 + g3 + g4\naverage = g1 + g2 + g3 + g4 / 4\n'
                'print("Sum:", total)\nprint("Average:", average)'),
               ("делит на 3 вместо 4",
                'print("Grades:", g1, g2, g3, g4)\ntotal = g1 + g2 + g3 + g4\naverage = total / 3\n'
                'print("Sum:", total)\nprint("Average:", average)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ar-taxi-split", title="Такси на всех",
        given=["start", "per_km", "km", "wait", "people"],
        variants=[{"start": "100", "per_km": "25", "km": "12", "wait": "5", "people": "4"},
                  {"start": "150", "per_km": "30", "km": "8", "wait": "10", "people": "2"},
                  {"start": "90", "per_km": "20", "km": "15", "wait": "3", "people": "5"}],
        hidden=[{"start": "120", "per_km": "18", "km": "20", "wait": "0", "people": "4"},
                {"start": "200", "per_km": "35", "km": "4", "wait": "7", "people": "1"},
                {"start": "80", "per_km": "22", "km": "9", "wait": "12", "people": "2"}],
        intro="Компания друзей едет на такси и делит счёт поровну. Посадка стоит `start = {start}` руб., каждый километр — "
              "`per_km = {per_km}` руб., ехать `km = {km}` км. Таксист ждал `wait = {wait}` мин., минута ожидания стоит 8 руб. "
              "Друзей `people = {people}`.",
        steps=["Посчитай `ride` — стоимость километров: цена километра, умноженная на число километров.",
               "Посчитай `waiting` — стоимость ожидания: минуты, умноженные на 8.",
               "Посчитай `total` — посадка плюс `ride` плюс `waiting`.",
               "Посчитай `share` — сколько платит каждый: `total`, делённый на `people`.",
               "Выведи четыре строки: `Ride:` и `ride`, `Waiting:` и `waiting`, `Total:` и `total`, `Each pays:` и `share`. "
               "Доля считается через `/`, поэтому она дробная, например `Each pays: 150.0`."],
        hint="Делить на число друзей нужно всю сумму. Запись `start + ride + waiting / people` разделит только ожидание: "
             "деление выполняется раньше сложения. Посчитай `total` отдельно или возьми сумму в скобки.",
        solution='ride = per_km * km\nwaiting = wait * 8\ntotal = start + ride + waiting\nshare = total / people\n'
                 'print("Ride:", ride)\nprint("Waiting:", waiting)\nprint("Total:", total)\nprint("Each pays:", share)',
        wrong=[("делит на друзей только ожидание — забыты скобки",
                'ride = per_km * km\nwaiting = wait * 8\ntotal = start + ride + waiting\nshare = start + ride + waiting / people\n'
                'print("Ride:", ride)\nprint("Waiting:", waiting)\nprint("Total:", total)\nprint("Each pays:", share)'),
               ("забывает плату за посадку",
                'ride = per_km * km\nwaiting = wait * 8\ntotal = ride + waiting\nshare = total / people\n'
                'print("Ride:", ride)\nprint("Waiting:", waiting)\nprint("Total:", total)\nprint("Each pays:", share)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ar-fahrenheit", title="Погода для гостя из США",
        given=["kazan", "sochi"],
        variants=[{"kazan": "10", "sochi": "25"}, {"kazan": "-5", "sochi": "15"}, {"kazan": "20", "sochi": "30"}],
        hidden=[{"kazan": "0", "sochi": "5"}, {"kazan": "-20", "sochi": "10"}, {"kazan": "15", "sochi": "35"}],
        intro="К тебе приезжает друг из США, он привык к градусам Фаренгейта. Сегодня в Казани `kazan = {kazan}` градусов "
              "Цельсия, в Сочи — `sochi = {sochi}`. Перевести Цельсий в Фаренгейт: умножить на 9, разделить на 5 "
              "и прибавить 32.",
        steps=["Посчитай `kazan_f` — температуру в Казани по Фаренгейту.",
               "Посчитай `sochi_f` — температуру в Сочи по Фаренгейту.",
               "Посчитай `diff` — на сколько градусов Цельсия в Сочи теплее: Сочи минус Казань.",
               "Выведи три строки: `Kazan:`, `kazan_f` и `F`; `Sochi:`, `sochi_f` и `F`; `Sochi is warmer by`, `diff` и `C`. "
               "Например, для 0 градусов строка будет `Kazan: 32.0 F` — после деления через `/` число дробное."],
        hint="Формула пишется без скобок: `kazan * 9 / 5 + 32`. Умножение и деление выполняются раньше сложения, "
             "поэтому 32 прибавится в самом конце. А `kazan * 9 / (5 + 32)` разделит на 37 — это уже другая формула.",
        solution='kazan_f = kazan * 9 / 5 + 32\nsochi_f = sochi * 9 / 5 + 32\ndiff = sochi - kazan\n'
                 'print("Kazan:", kazan_f, "F")\nprint("Sochi:", sochi_f, "F")\nprint("Sochi is warmer by", diff, "C")',
        wrong=[("прибавляет 32 до умножения",
                'kazan_f = kazan * 9 / 5 + 32\nsochi_f = (sochi + 32) * 9 / 5\ndiff = sochi - kazan\n'
                'print("Kazan:", kazan_f, "F")\nprint("Sochi:", sochi_f, "F")\nprint("Sochi is warmer by", diff, "C")'),
               ("считает разницу по Фаренгейту, а не по Цельсию",
                'kazan_f = kazan * 9 / 5 + 32\nsochi_f = sochi * 9 / 5 + 32\ndiff = sochi_f - kazan_f\n'
                'print("Kazan:", kazan_f, "F")\nprint("Sochi:", sochi_f, "F")\nprint("Sochi is warmer by", diff, "C")')],
    ),
]
