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
]
