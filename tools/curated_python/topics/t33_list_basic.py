"""PY_LIST_BASIC — «Списки». Taught before: print, variables, arithmetic, int/float, strings, type conversion, // and %,
+= -=, f-strings, conditions, for + range, accumulator, while, break/continue, list indexes (from 0, negative, len,
changing an element). Here: creating a list (empty or with values), append, len, the in / not in check, printing a list.
Not yet: iterating a list with for, string slicing and methods, functions, insert/remove/sort and list slices."""
from build import OutputTask

SKILL = "PY_LIST_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lb-shopping", title="Корзина покупок",
        given=["extra"],
        variants=[{"extra": '"apples"'}, {"extra": '"cheese"'}, {"extra": '"tea"'}],
        hidden=[{"extra": '"eggs"'}, {"extra": '"rice"'}, {"extra": '"juice"'}],
        intro="Мама попросила купить хлеб и молоко, а ещё одну покупку ты выбираешь сам — она записана в переменной "
              "`extra = {extra}`. Собери корзину в виде списка.",
        steps=["Создай пустой список `basket`.",
               "Добавь в него через `append` по порядку: строку `\"bread\"`, строку `\"milk\"` и покупку из переменной `extra`.",
               "Выведи весь список командой `print(basket)`.",
               "Следующей строкой выведи число покупок в виде `Items: 3` — посчитай его через `len`."],
        hint="Пустой список создают так: `basket = []`. Метод `append` добавляет элемент в конец списка: "
             "`basket.append(\"bread\")`. Чтобы добавить значение переменной, пиши её имя без кавычек.",
        solution='basket = []\nbasket.append("bread")\nbasket.append("milk")\nbasket.append(extra)\n'
                 'print(basket)\nprint(f"Items: {len(basket)}")',
        wrong=[("добавляет строку \"extra\" вместо значения переменной",
                'basket = []\nbasket.append("bread")\nbasket.append("milk")\nbasket.append("extra")\n'
                'print(basket)\nprint(f"Items: {len(basket)}")'),
               ("добавляет свою покупку первой: порядок в списке другой",
                'basket = []\nbasket.append(extra)\nbasket.append("bread")\nbasket.append("milk")\n'
                'print(basket)\nprint(f"Items: {len(basket)}")')],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lb-guests", title="Список гостей",
        given=["guests", "name"],
        variants=[{"guests": '["Anya", "Boris", "Vika"]', "name": '"Gosha"'},
                  {"guests": '["Lev", "Mila", "Nina", "Oleg"]', "name": '"Mila"'},
                  {"guests": '["Rita", "Sonya"]', "name": '"Timur"'}],
        hidden=[{"guests": "[]", "name": '"Ira"'}, {"guests": '["Max", "Eva"]', "name": '"Eva"'},
                {"guests": '["Dina", "Yana", "Fil"]', "name": '"Zoya"'}],
        intro="Даша собирает гостей на день рождения. Список приглашённых — `guests`. Ей звонит `name = {name}` "
              "и просится в гости. Одного человека нельзя записать в список дважды.",
        steps=["Проверь через `in`, есть ли `name` в списке `guests`.",
               "Если есть, выведи строку вида `Mila is already on the list`",
               "Иначе добавь `name` в конец списка через `append` и выведи строку вида `Gosha added`",
               "После этого в любом случае выведи весь список командой `print(guests)` и следующей строкой "
               "число гостей в виде `Guests: 4`"],
        hint="Выражение `name in guests` даёт `True`, если такой элемент в списке есть. "
             "Последние две строки пишутся без отступа — после `if` / `else`, а не внутри них.",
        solution='if name in guests:\n    print(f"{name} is already on the list")\nelse:\n    guests.append(name)\n'
                 '    print(f"{name} added")\nprint(guests)\nprint(f"Guests: {len(guests)}")',
        wrong=[("перепутано условие: not in вместо in",
                'if name not in guests:\n    print(f"{name} is already on the list")\nelse:\n    guests.append(name)\n'
                '    print(f"{name} added")\nprint(guests)\nprint(f"Guests: {len(guests)}")'),
               ("добавляет строку \"name\" вместо значения переменной",
                'if name in guests:\n    print(f"{name} is already on the list")\nelse:\n    guests.append("name")\n'
                '    print(f"{name} added")\nprint(guests)\nprint(f"Guests: {len(guests)}")')],
        constructs=["list", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lb-bus", title="Расписание автобуса",
        given=["start", "step"],
        variants=[{"start": "5", "step": "15"}, {"start": "0", "step": "20"}, {"start": "10", "step": "12"}],
        hidden=[{"start": "59", "step": "30"}, {"start": "3", "step": "7"}, {"start": "0", "step": "60"}],
        intro="Автобус отходит от остановки в `start = {start}` минут каждого часа, а потом каждые `step = {step}` минут, "
              "пока не кончится час (минута меньше 60). Составь расписание на один час в виде списка минут.",
        steps=["Создай пустой список `times`.",
               "Циклом `for` с `range` перебери минуты от `start` до конца часа с шагом `step` и добавь каждую в `times` "
               "через `append`.",
               "Выведи три строки: `Departures: [5, 20, 35, 50]`, число рейсов `Buses per hour: 4` (через `len`) и минуту "
               "последнего рейса `Last bus: 50` (последний элемент списка)."],
        hint="`range(start, 60, step)` выдаёт `start`, `start + step`, … и останавливается до 60. "
             "Последний элемент списка — `times[-1]`.",
        solution='times = []\nfor minute in range(start, 60, step):\n    times.append(minute)\n'
                 'print(f"Departures: {times}")\nprint(f"Buses per hour: {len(times)}")\nprint(f"Last bus: {times[-1]}")',
        wrong=[("список сразу начинается с первого рейса: он попадает в расписание дважды",
                'times = [start]\nfor minute in range(start, 60, step):\n    times.append(minute)\n'
                'print(f"Departures: {times}")\nprint(f"Buses per hour: {len(times)}")\nprint(f"Last bus: {times[-1]}")'),
               ("добавляет в список шаг, а не минуту",
                'times = []\nfor minute in range(start, 60, step):\n    times.append(step)\n'
                'print(f"Departures: {times}")\nprint(f"Buses per hour: {len(times)}")\nprint(f"Last bus: {times[-1]}")')],
        constructs=["list", "for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lb-teams", title="Две команды",
        given=["players"],
        variants=[{"players": "7"}, {"players": "10"}, {"players": "5"}],
        hidden=[{"players": "1"}, {"players": "2"}, {"players": "11"}],
        intro="Физрук делит класс на две команды по номерам в журнале: нечётные номера идут в команду A, чётные — "
              "в команду B. Всего в классе `players = {players}` учеников с номерами от 1 до `players`.",
        steps=["Создай два пустых списка: `team_a` и `team_b`.",
               "Циклом `for` перебери номера от 1 до `players` включительно.",
               "Нечётный номер добавь в `team_a`, чётный — в `team_b`.",
               "После цикла выведи две строки вида `Team A: [1, 3, 5, 7]` и `Team B: [2, 4, 6]`"],
        hint="Номер нечётный, когда остаток от деления на 2 равен 1: `n % 2 == 1`. "
             "Список можно вывести прямо в f-строке: `{{team_a}}`.",
        solution='team_a = []\nteam_b = []\nfor player in range(1, players + 1):\n    if player % 2 == 1:\n'
                 '        team_a.append(player)\n    else:\n        team_b.append(player)\n'
                 'print(f"Team A: {team_a}")\nprint(f"Team B: {team_b}")',
        wrong=[("в ветке else добавляет тоже в команду A",
                'team_a = []\nteam_b = []\nfor player in range(1, players + 1):\n    if player % 2 == 1:\n'
                '        team_a.append(player)\n    else:\n        team_a.append(player)\n'
                'print(f"Team A: {team_a}")\nprint(f"Team B: {team_b}")'),
               ("правая граница не входит в range: последний ученик без команды",
                'team_a = []\nteam_b = []\nfor player in range(1, players):\n    if player % 2 == 1:\n'
                '        team_a.append(player)\n    else:\n        team_b.append(player)\n'
                'print(f"Team A: {team_a}")\nprint(f"Team B: {team_b}")')],
        constructs=["list", "for", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lb-sale", title="Цена куртки падает",
        given=["price", "percent", "min_price"],
        variants=[{"price": "5000", "percent": "10", "min_price": "3500"},
                  {"price": "2000", "percent": "25", "min_price": "800"},
                  {"price": "1000", "percent": "50", "min_price": "250"}],
        hidden=[{"price": "3000", "percent": "10", "min_price": "3000"},
                {"price": "800", "percent": "20", "min_price": "400"},
                {"price": "6000", "percent": "30", "min_price": "1000"}],
        intro="Куртка стоит `price = {price}` рублей. Каждую неделю магазин снижает цену на `percent = {percent}` % "
              "(копейки отбрасываются), но только пока цена выше `min_price = {min_price}` рублей. "
              "Запиши историю цен в список.",
        steps=["Создай список `prices`, в котором сразу лежит начальная цена `price`.",
               "Пока `price` больше `min_price`, повторяй в цикле `while`: уменьши `price` на `price * percent // 100` "
               "и добавь новую цену в конец списка.",
               "Выведи три строки: `Prices: [5000, 4500, 4050, 3645, 3281]`, число недель снижения `Weeks: 4` "
               "(цен в списке на одну больше, чем недель) и `Final price: 3281 rub` — последний элемент списка."],
        hint="Список со значением создают так: `prices = [price]`. Когда цена стала ровно `min_price`, "
             "она уже не выше — снижение прекращается.",
        solution='prices = [price]\nwhile price > min_price:\n    price = price - price * percent // 100\n'
                 '    prices.append(price)\nprint(f"Prices: {prices}")\nprint(f"Weeks: {len(prices) - 1}")\n'
                 'print(f"Final price: {prices[-1]} rub")',
        wrong=[("начинает с пустого списка: начальной цены нет в истории",
                'prices = []\nwhile price > min_price:\n    price = price - price * percent // 100\n'
                '    prices.append(price)\nprint(f"Prices: {prices}")\nprint(f"Weeks: {len(prices) - 1}")\n'
                'print(f"Final price: {prices[-1]} rub")'),
               ("нестрогое сравнение: цену, равную min_price, снижает ещё раз",
                'prices = [price]\nwhile price >= min_price:\n    price = price - price * percent // 100\n'
                '    prices.append(price)\nprint(f"Prices: {prices}")\nprint(f"Weeks: {len(prices) - 1}")\n'
                'print(f"Final price: {prices[-1]} rub")'),
               ("считает недели по длине списка: на одну больше",
                'prices = [price]\nwhile price > min_price:\n    price = price - price * percent // 100\n'
                '    prices.append(price)\nprint(f"Prices: {prices}")\nprint(f"Weeks: {len(prices)}")\n'
                'print(f"Final price: {prices[-1]} rub")')],
        constructs=["list", "while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lb-groups", title="Делим класс на группы",
        given=["students"],
        variants=[{"students": "12"}, {"students": "15"}, {"students": "18"}],
        hidden=[{"students": "2"}, {"students": "9"}, {"students": "30"}],
        intro="На экскурсии класс из `students = {students}` человек нужно разбить на группы поровну, без остатка. "
              "Учительница хочет знать все возможные размеры группы — от 1 человека до всего класса сразу. "
              "В классе не меньше двух учеников.",
        steps=["Создай пустой список `sizes`.",
               "Циклом `for` перебери размеры от 1 до `students` включительно и добавь в `sizes` каждый размер, "
               "на который `students` делится без остатка.",
               "Выведи `Group sizes: [1, 2, 3, 4, 6, 12]` и следующей строкой `Options: 6` — длину списка.",
               "Если вариантов всего два (по одному человеку или весь класс), выведи `No equal groups`. Иначе выведи "
               "самый маленький настоящий размер группы — второй элемент списка — в виде `Smallest group: 2`"],
        hint="`students % size == 0` — проверка, что класс делится на группы размера `size` без остатка. "
             "Первый элемент списка всегда 1, поэтому настоящая маленькая группа лежит под индексом 1.",
        solution='sizes = []\nfor size in range(1, students + 1):\n    if students % size == 0:\n        sizes.append(size)\n'
                 'print(f"Group sizes: {sizes}")\nprint(f"Options: {len(sizes)}")\nif len(sizes) == 2:\n'
                 '    print("No equal groups")\nelse:\n    print(f"Smallest group: {sizes[1]}")',
        wrong=[("правая граница не входит в range: вариант «весь класс» потерян",
                'sizes = []\nfor size in range(1, students):\n    if students % size == 0:\n        sizes.append(size)\n'
                'print(f"Group sizes: {sizes}")\nprint(f"Options: {len(sizes)}")\nif len(sizes) == 2:\n'
                '    print("No equal groups")\nelse:\n    print(f"Smallest group: {sizes[1]}")'),
               ("берёт первый элемент списка: группа из одного человека",
                'sizes = []\nfor size in range(1, students + 1):\n    if students % size == 0:\n        sizes.append(size)\n'
                'print(f"Group sizes: {sizes}")\nprint(f"Options: {len(sizes)}")\nif len(sizes) == 2:\n'
                '    print("No equal groups")\nelse:\n    print(f"Smallest group: {sizes[0]}")')],
        constructs=["list", "for", "if"],
    ),
]
