"""PY_TUPLE_BASIC — «Кортежи». Taught before: everything up to list operations (conditions, loops, lists and their
methods, slices, string methods, functions, classes). Here: creating a tuple, indexing, unpacking (also in a for header),
immutability and list()/tuple(). Not yet: sets, dicts, comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_TUPLE_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-tup-photo-size", title="Размер фотографии",
        given=["size"],
        variants=[{"size": "(1920, 1080)"}, {"size": "(1080, 1350)"}, {"size": "(800, 800)"}],
        hidden=[{"size": "(640, 480)"}, {"size": "(720, 1280)"}, {"size": "(1200, 1200)"}, {"size": "(3000, 2000)"}],
        intro="Фоторедактор хранит размер картинки в пикселях в кортеже `size`: первым стоит ширина, вторым — высота. "
              "Размер картинки не должен случайно поменяться, поэтому для него и выбран кортеж.",
        steps=["Распакуй кортеж `size` одной строкой в две переменные: сначала ширина `width`, потом высота `height` — "
               "в кортеже они стоят именно в таком порядке.",
               "Выведи строку вида `Size: 500 x 300` — сначала ширина, потом высота.",
               "Следующей строкой выведи `Landscape photo`, если ширина больше высоты, `Portrait photo`, "
               "если меньше, и `Square photo`, если они равны."],
        hint="Распаковка раскладывает элементы кортежа по переменным по порядку: после `a, b = (5, 9)` в `a` окажется 5, "
             "а в `b` — 9. Переменных слева должно быть ровно столько, сколько элементов в кортеже.",
        solution='width, height = size\nprint(f"Size: {width} x {height}")\nif width > height:\n'
                 '    print("Landscape photo")\nelif width < height:\n    print("Portrait photo")\nelse:\n'
                 '    print("Square photo")',
        wrong=[("распаковывает в обратном порядке — ширина и высота путаются",
                'height, width = size\nprint(f"Size: {width} x {height}")\nif width > height:\n'
                '    print("Landscape photo")\nelif width < height:\n    print("Portrait photo")\nelse:\n'
                '    print("Square photo")'),
               ("печатает кортеж целиком вместо ширины и высоты",
                'width, height = size\nprint(f"Size: {size}")\nif width > height:\n'
                '    print("Landscape photo")\nelif width < height:\n    print("Portrait photo")\nelse:\n'
                '    print("Square photo")')],
        must_use=[("re:(?m)^\\s*\\(?\\s*\\w+\\s*,\\s*\\w+\\s*\\)?\\s*=[^=]",
                   "Достань ширину и высоту распаковкой кортежа — одной строкой вида a, b = кортеж, без обращения по индексам.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-tup-menu-price", title="Новая цена в меню",
        given=["prices", "number", "new_price"],
        variants=[{"prices": "(120, 250, 80, 45)", "number": "2", "new_price": "270"},
                  {"prices": "(60, 75, 110)", "number": "3", "new_price": "95"},
                  {"prices": "(300, 150, 220, 90, 180)", "number": "1", "new_price": "320"}],
        hidden=[{"prices": "(50, 70)", "number": "2", "new_price": "65"},
                {"prices": "(200, 210, 220, 230, 240, 250)", "number": "4", "new_price": "199"},
                {"prices": "(99, 199, 299)", "number": "1", "new_price": "149"}],
        intro="Кафе хранит цены блюд из меню в кортеже `prices` — так их нельзя случайно испортить в программе. "
              "Блюда нумеруются с 1 в том же порядке, что и цены. Повар решил, что блюдо с номером `number` "
              "теперь будет стоить `new_price` рублей.",
        steps=["Кортеж изменить нельзя: команда `prices[0] = 100` остановит программу с ошибкой `TypeError`. "
               "Поэтому сделай из кортежа список с помощью `list()`.",
               "Замени в этом списке цену блюда с номером `number` на `new_price`. Помни: блюда нумеруются с 1, а индексы — с 0.",
               "Преврати список обратно в кортеж с помощью `tuple()` и выведи получившийся кортеж через `print`."],
        hint="Кортеж и список легко превращаются друг в друга: `list((1, 2))` даёт список `[1, 2]`, а `tuple([1, 2])` — "
             "кортеж `(1, 2)`. Список можно менять, а из изменённого списка потом получится новый кортеж.",
        solution="menu = list(prices)\nmenu[number - 1] = new_price\nprices = tuple(menu)\nprint(prices)",
        wrong=[("забыл превратить список обратно в кортеж — печатаются квадратные скобки",
                "menu = list(prices)\nmenu[number - 1] = new_price\nprint(menu)"),
               ("меняет список-копию, а печатает старый кортеж — цена не изменилась",
                "menu = list(prices)\nmenu[number - 1] = new_price\nprint(prices)")],
        must_use=[("re:\\btuple\\(", "Преврати изменённый список обратно в кортеж через tuple(): цены должны остаться кортежем, "
                                     "чтобы их нельзя было случайно испортить.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-tup-receipt", title="Чек из магазина",
        given=["cart"],
        variants=[{"cart": '[("bread", 45, 2), ("milk", 89, 1), ("apples", 120, 3)]'},
                  {"cart": '[("notebook", 30, 5), ("pen", 25, 4)]'},
                  {"cart": '[("juice", 110, 2), ("cookies", 75, 1), ("bananas", 95, 2), ("water", 40, 6)]'}],
        hidden=[{"cart": '[("cheese", 300, 1)]'},
                {"cart": '[("soap", 60, 3), ("toothpaste", 150, 2), ("sponge", 20, 10), ("shampoo", 280, 1), ("cream", 199, 2)]'},
                {"cart": '[("watermelon", 250, 1), ("melon", 180, 2), ("cherries", 400, 1)]'}],
        intro="Касса пробила покупки и записала их в список `cart`. Каждая покупка — кортеж из трёх значений: "
              "название товара, цена за одну штуку и количество. Нужно напечатать чек.",
        steps=["Пройди циклом `for` по списку `cart`. Каждый кортеж распакуй прямо в заголовке цикла в три переменные — "
               "в том же порядке, в котором значения стоят в кортеже.",
               "Для каждой покупки выведи строку вида `tea: 2 pcs, 600 rub` — название, количество и стоимость покупки "
               "(цена за штуку, умноженная на количество).",
               "После цикла выведи строку вида `Total: 1000 rub` с общей стоимостью всех покупок."],
        hint="Распаковка работает и в заголовке цикла: `for a, b in [(1, 2), (3, 4)]:` на каждом шаге раскладывает "
             "очередной кортеж по переменным `a` и `b`. Общую сумму удобно копить в переменной, которая до цикла равна 0.",
        solution='total = 0\nfor name, price, count in cart:\n    cost = price * count\n'
                 '    print(f"{name}: {count} pcs, {cost} rub")\n    total += cost\nprint(f"Total: {total} rub")',
        wrong=[("путает порядок при распаковке — цена и количество меняются местами",
                'total = 0\nfor name, count, price in cart:\n    cost = price * count\n'
                '    print(f"{name}: {count} pcs, {cost} rub")\n    total += cost\nprint(f"Total: {total} rub")'),
               ("в итог складывает цены за штуку и забывает про количество",
                'total = 0\nfor name, price, count in cart:\n    cost = price * count\n'
                '    print(f"{name}: {count} pcs, {cost} rub")\n    total += price\nprint(f"Total: {total} rub")')],
        constructs=["for"],
        must_use=[("re:(?m)^\\s*(?:for\\s+)?\\(?\\s*\\w+\\s*,\\s*\\w+\\s*,\\s*\\w+\\s*\\)?\\s*(?:=[^=]|in\\b)",
                   "Распакуй каждый кортеж в три переменные — например, прямо в заголовке цикла: "
                   "for название, цена, количество in cart. Так не придётся обращаться к элементам по индексам.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-tup-birthday", title="День рождения",
        given=["birthday", "now_year"],
        variants=[{"birthday": "(14, 3, 2011)", "now_year": "2026"},
                  {"birthday": "(2, 12, 2009)", "now_year": "2025"},
                  {"birthday": "(30, 7, 2014)", "now_year": "2026"}],
        hidden=[{"birthday": "(1, 1, 2000)", "now_year": "2024"},
                {"birthday": "(28, 2, 2012)", "now_year": "2027"},
                {"birthday": "(31, 12, 2010)", "now_year": "2026"},
                {"birthday": "(9, 6, 2008)", "now_year": "2023"}],
        intro="В анкете ученика дата рождения записана кортежем `birthday` из трёх чисел: день, месяц и год. "
              "Сейчас идёт `now_year` год. Нужно вывести дату и узнать, сколько лет исполнится ученику в этом году.",
        steps=["Распакуй кортеж `birthday` одной строкой в три переменные: `day`, `month` и `year` — именно в таком порядке "
               "числа стоят в кортеже.",
               "Выведи строку вида `Born: 14.3.2011` — день, месяц и год через точку.",
               "Следующей строкой выведи строку вида `Turns 15 this year` — разницу между `now_year` и годом рождения.",
               "Последней строкой выведи `Winter birthday`, если месяц — 12, 1 или 2, иначе `Not a winter birthday`."],
        hint="После `a, b, c = (7, 8, 9)` в `a` будет 7, в `b` — 8, в `c` — 9. Зимние месяцы — декабрь (12), январь (1) "
             "и февраль (2): декабрь стоит в конце года, поэтому одной проверкой «меньше трёх» не обойтись.",
        solution='day, month, year = birthday\nprint(f"Born: {day}.{month}.{year}")\n'
                 'print(f"Turns {now_year - year} this year")\nif month == 12 or month <= 2:\n'
                 '    print("Winter birthday")\nelse:\n    print("Not a winter birthday")',
        wrong=[("путает день и месяц при распаковке",
                'month, day, year = birthday\nprint(f"Born: {day}.{month}.{year}")\n'
                'print(f"Turns {now_year - year} this year")\nif month == 12 or month <= 2:\n'
                '    print("Winter birthday")\nelse:\n    print("Not a winter birthday")'),
               ("забывает про декабрь — зимними считает только январь и февраль",
                'day, month, year = birthday\nprint(f"Born: {day}.{month}.{year}")\n'
                'print(f"Turns {now_year - year} this year")\nif month <= 2:\n'
                '    print("Winter birthday")\nelse:\n    print("Not a winter birthday")')],
        must_use=[("re:(?m)^\\s*\\(?\\s*\\w+\\s*,\\s*\\w+\\s*,\\s*\\w+\\s*\\)?\\s*=[^=]",
                   "Достань день, месяц и год распаковкой кортежа — одной строкой вида a, b, c = кортеж.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-tup-min-max-temp", title="Самая холодная и самая тёплая ночь",
        given=["temps"],
        variants=[{"temps": "[3, -2, 5, 0, -4, 1]"},
                  {"temps": "[12, 15, 9, 14]"},
                  {"temps": "[-8, -3, -11, -5, -6]"}],
        hidden=[{"temps": "[7]"},
                {"temps": "[20, 22, 18, 25, 21, 19, 24]"},
                {"temps": "[-1, -1, -1]"},
                {"temps": "[0, 10, -10, 5]"}],
        intro="Метеостанция записала ночные температуры за несколько дней в список `temps`. Нужна функция, которая "
              "за один проход находит и самую низкую, и самую высокую температуру и возвращает их сразу обе — кортежем.",
        steps=["Напиши функцию `extremes(values)`. Сначала и самой низкой, и самой высокой считай первую температуру "
               "списка `values`, потом пройди циклом по всем температурам и обнови оба значения, где нужно.",
               "Функция возвращает кортеж из двух чисел: сначала самая низкая температура, потом самая высокая — "
               "`return low, high`.",
               "Вызови функцию для `temps` и распакуй результат одной строкой в две переменные.",
               "Выведи строку вида `Min: -4, max: 5, range: 9` — самую низкую, самую высокую температуру и разницу между ними."],
        hint="`return a, b` возвращает кортеж `(a, b)`, и его сразу можно распаковать: `x, y = f()`. Не начинай поиск "
             "с нуля: если все температуры выше нуля, ноль окажется «самой низкой», хотя его в списке нет.",
        solution='def extremes(values):\n    low = values[0]\n    high = values[0]\n    for value in values:\n'
                 '        if value < low:\n            low = value\n        if value > high:\n            high = value\n'
                 '    return low, high\n\n\nlow, high = extremes(temps)\nprint(f"Min: {low}, max: {high}, range: {high - low}")',
        wrong=[("возвращает кортеж в обратном порядке — минимум и максимум меняются местами",
                'def extremes(values):\n    low = values[0]\n    high = values[0]\n    for value in values:\n'
                '        if value < low:\n            low = value\n        if value > high:\n            high = value\n'
                '    return high, low\n\n\nlow, high = extremes(temps)\nprint(f"Min: {low}, max: {high}, range: {high - low}")'),
               ("начинает поиск с нуля — для тёплых и морозных дней ответ неверный",
                'def extremes(values):\n    low = 0\n    high = 0\n    for value in values:\n'
                '        if value < low:\n            low = value\n        if value > high:\n            high = value\n'
                '    return low, high\n\n\nlow, high = extremes(temps)\nprint(f"Min: {low}, max: {high}, range: {high - low}")')],
        constructs=["function", "for"],
        must_use=[("re:(?m)^\\s*return\\s*\\(?\\s*\\w+\\s*,", "Верни обе температуры сразу кортежем: return low, high."),
                  ("re:(?m)^\\s*\\(?\\s*\\w+\\s*,\\s*\\w+\\s*\\)?\\s*=[^=]",
                   "Распакуй результат функции одной строкой в две переменные.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-tup-football-season", title="Футбольный сезон",
        given=["matches"],
        variants=[{"matches": "[(3, 1), (0, 0), (1, 2), (4, 0)]"},
                  {"matches": "[(2, 2), (1, 0), (0, 3)]"},
                  {"matches": "[(1, 1), (5, 2), (2, 1), (0, 1), (3, 0)]"}],
        hidden=[{"matches": "[(0, 1), (2, 3)]"},
                {"matches": "[(0, 0)]"},
                {"matches": "[(2, 0), (3, 1), (1, 0), (4, 4)]"},
                {"matches": "[(1, 0), (6, 6), (0, 2), (5, 1)]"}],
        intro="Школьная команда сыграла сезон. Результаты матчей записаны в список `matches`: каждый матч — кортеж "
              "из двух чисел, сначала забитые голы, потом пропущенные. За победу дают 3 очка, за ничью 1, за поражение 0.",
        steps=["Пройди циклом `for` по `matches`, распаковывая каждый кортеж прямо в заголовке цикла в две переменные.",
               "Для каждого матча выведи строку вида `3:1 win`, `0:0 draw` или `1:2 loss` и прибавь к общему числу очков "
               "3, 1 или 0.",
               "Запоминай самую крупную победу — матч, где разница забитых и пропущенных голов больше всего, — как кортеж "
               "из двух чисел: забитые и пропущенные голы. При равной разнице остаётся победа, которая была раньше.",
               "После цикла выведи строку вида `Points: 7`, а затем строку вида `Best win: 4:0` или `No wins`, "
               "если команда не выиграла ни разу."],
        hint="Начни с `best = None` — победы ещё не было. Победа лучше запомненной, если `best` ещё `None` или её разница "
             "голов строго больше. Из запомненного кортежа два числа потом можно достать распаковкой.",
        solution='points = 0\nbest = None\nfor scored, missed in matches:\n    if scored > missed:\n'
                 '        print(f"{scored}:{missed} win")\n        points += 3\n'
                 '        if best is None or scored - missed > best[0] - best[1]:\n            best = (scored, missed)\n'
                 '    elif scored == missed:\n        print(f"{scored}:{missed} draw")\n        points += 1\n'
                 '    else:\n        print(f"{scored}:{missed} loss")\nprint(f"Points: {points}")\n'
                 'if best is None:\n    print("No wins")\nelse:\n    goals_for, goals_against = best\n'
                 '    print(f"Best win: {goals_for}:{goals_against}")',
        wrong=[("запоминает самую результативную победу по числу забитых голов, а не по разнице",
                'points = 0\nbest = None\nfor scored, missed in matches:\n    if scored > missed:\n'
                '        print(f"{scored}:{missed} win")\n        points += 3\n'
                '        if best is None or scored > best[0]:\n            best = (scored, missed)\n'
                '    elif scored == missed:\n        print(f"{scored}:{missed} draw")\n        points += 1\n'
                '    else:\n        print(f"{scored}:{missed} loss")\nprint(f"Points: {points}")\n'
                'if best is None:\n    print("No wins")\nelse:\n    goals_for, goals_against = best\n'
                '    print(f"Best win: {goals_for}:{goals_against}")'),
               ("за ничью не даёт очков",
                'points = 0\nbest = None\nfor scored, missed in matches:\n    if scored > missed:\n'
                '        print(f"{scored}:{missed} win")\n        points += 3\n'
                '        if best is None or scored - missed > best[0] - best[1]:\n            best = (scored, missed)\n'
                '    elif scored == missed:\n        print(f"{scored}:{missed} draw")\n'
                '    else:\n        print(f"{scored}:{missed} loss")\nprint(f"Points: {points}")\n'
                'if best is None:\n    print("No wins")\nelse:\n    goals_for, goals_against = best\n'
                '    print(f"Best win: {goals_for}:{goals_against}")'),
               ("при равной разнице заменяет победу на более позднюю",
                'points = 0\nbest = None\nfor scored, missed in matches:\n    if scored > missed:\n'
                '        print(f"{scored}:{missed} win")\n        points += 3\n'
                '        if best is None or scored - missed >= best[0] - best[1]:\n            best = (scored, missed)\n'
                '    elif scored == missed:\n        print(f"{scored}:{missed} draw")\n        points += 1\n'
                '    else:\n        print(f"{scored}:{missed} loss")\nprint(f"Points: {points}")\n'
                'if best is None:\n    print("No wins")\nelse:\n    goals_for, goals_against = best\n'
                '    print(f"Best win: {goals_for}:{goals_against}")')],
        constructs=["for"],
        must_use=[("re:(?m)^\\s*for\\s+\\(?\\s*\\w+\\s*,\\s*\\w+\\s*\\)?\\s*in\\b",
                   "Распакуй каждый матч прямо в заголовке цикла: for забитые, пропущенные in matches.")],
    ),
]
