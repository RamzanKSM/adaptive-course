"""PY_LIST_ITERATION — «Перебор списка». Taught before: print, variables, arithmetic, int/float, strings, type conversion,
// and %, += -=, f-strings, conditions, for + range, accumulator, while, break/continue, list indexes, lists (creating,
append, len, in). Here: for item in list — visiting every element, summing, counting, finding the best, filtering into
a new list. Not yet: sum/max/min, string slicing and methods, functions, insert/remove/sort and list slices."""
from build import OutputTask

SKILL = "PY_LIST_ITERATION"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lit-rt-sale-tags", title="Ценники со скидкой",
        given=["prices"],
        variants=[{"prices": "[500, 1200, 90]"}, {"prices": "[350, 80, 2000, 640]"}, {"prices": "[1500, 999]"}],
        hidden=[{"prices": "[10]"}, {"prices": "[100, 200, 300, 400, 500]"}, {"prices": "[55, 5]"}],
        intro="В магазине распродажа: всё на 10 % дешевле (копейки отбрасываются). Продавщица печатает новые ценники. "
              "Старые цены в рублях записаны в список `prices`. Товаров может быть сколько угодно.",
        steps=["Перебери список циклом `for price in prices:`",
               "Для каждой цены посчитай новую: цена минус `price // 10`. Выведи строку вида `500 -> 450 rub`",
               "После цикла выведи, сколько ценников напечатано, в виде `Tags: 3` (через `len`)."],
        hint="В цикле `for price in prices:` переменная `price` по очереди становится каждым элементом списка — "
             "индексы не нужны. Строку `Tags` печатают один раз, поэтому она пишется без отступа, после цикла.",
        solution='for price in prices:\n    new_price = price - price // 10\n    print(f"{price} -> {new_price} rub")\n'
                 'print(f"Tags: {len(prices)}")',
        wrong=[("печатает размер скидки вместо новой цены",
                'for price in prices:\n    new_price = price // 10\n    print(f"{price} -> {new_price} rub")\n'
                'print(f"Tags: {len(prices)}")'),
               ("строка с числом ценников внутри цикла: печатается после каждого ценника",
                'for price in prices:\n    new_price = price - price // 10\n    print(f"{price} -> {new_price} rub")\n'
                '    print(f"Tags: {len(prices)}")')],
        constructs=["list", "for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lit-rt-rainfall", title="Дождливые дни",
        given=["rain"],
        variants=[{"rain": "[0, 5, 12, 0, 3, 0, 8]"}, {"rain": "[2, 0, 0, 0, 15]"}, {"rain": "[0, 0, 7, 1]"}],
        hidden=[{"rain": "[0]"}, {"rain": "[4]"}, {"rain": "[0, 0, 0]"}, {"rain": "[10, 20, 30, 1]"}],
        intro="Метеостанция записала, сколько миллиметров дождя выпало за каждый день, в список `rain`. "
              "День без дождя записан как 0. Дней может быть сколько угодно.",
        steps=["Заведи два накопителя со значением 0: `rainy` — число дождливых дней и `total` — сколько всего "
               "миллиметров выпало.",
               "Перебери список `rain` циклом `for`. Если в этот день дождь был (больше 0 мм), увеличь `rainy` на 1. "
               "Количество осадков каждого дня прибавь к `total`.",
               "После цикла выведи три строки: `Rainy days: 4`, `Dry days: 3` (все дни минус дождливые, "
               "дней всего — длина списка) и `Total: 28 mm`"],
        hint="Сухой день — это 0 мм, он не дождливый. Прибавлять к `total` можно все дни подряд: ноль сумму не меняет. "
             "Число сухих дней удобно посчитать после цикла: `len(rain) - rainy`.",
        solution='rainy = 0\ntotal = 0\nfor mm in rain:\n    if mm > 0:\n        rainy += 1\n    total += mm\n'
                 'print(f"Rainy days: {rainy}")\nprint(f"Dry days: {len(rain) - rainy}")\nprint(f"Total: {total} mm")',
        wrong=[("нестрогое сравнение: сухие дни тоже считаются дождливыми",
                'rainy = 0\ntotal = 0\nfor mm in rain:\n    if mm >= 0:\n        rainy += 1\n    total += mm\n'
                'print(f"Rainy days: {rainy}")\nprint(f"Dry days: {len(rain) - rainy}")\nprint(f"Total: {total} mm")'),
               ("перезаписывает total вместо накопления",
                'rainy = 0\ntotal = 0\nfor mm in rain:\n    if mm > 0:\n        rainy += 1\n    total = mm\n'
                'print(f"Rainy days: {rainy}")\nprint(f"Dry days: {len(rain) - rainy}")\nprint(f"Total: {total} mm")'),
               ("сухие дни — это все дни из списка",
                'rainy = 0\ntotal = 0\nfor mm in rain:\n    if mm > 0:\n        rainy += 1\n    total += mm\n'
                'print(f"Rainy days: {rainy}")\nprint(f"Dry days: {len(rain)}")\nprint(f"Total: {total} mm")')],
        constructs=["list", "for", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lit-rt-sales-growth", title="Рост продаж подряд",
        given=["sales"],
        variants=[{"sales": "[10, 12, 15, 9, 11, 14, 18, 7]"}, {"sales": "[5, 4, 6, 8, 3]"},
                  {"sales": "[20, 21, 22, 23, 24]"}],
        hidden=[{"sales": "[7]"}, {"sales": "[9, 8, 7, 6]"}, {"sales": "[3, 3, 4, 4, 5]"},
                {"sales": "[1, 2, 1, 2, 3, 1]"}],
        intro="Кофейня записывает, сколько чашек продала за каждый день, в список `sales` по порядку. Хозяин хочет знать, "
              "в скольких днях продажи выросли по сравнению с предыдущим днём и сколько дней подряд длился самый долгий рост. "
              "Серия роста — это несколько дней подряд, каждый из которых продал больше предыдущего; первый день серии "
              "тоже считается, поэтому одиночный день — это серия длиной 1.",
        steps=["Заведи переменные: `prev` — продажи первого дня (`sales[0]`), `grew = 0` — сколько дней был рост, "
               "`streak = 1` — длина текущей серии и `best = 1` — длина самой долгой серии.",
               "Перебери список `sales` циклом `for`. Если продажи дня больше `prev`, увеличь `grew` и `streak` на 1, "
               "а если `streak` стал больше `best`, запомни его в `best`. Иначе начни серию заново: `streak = 1`.",
               "В конце каждого шага (в любом случае) запомни продажи этого дня в `prev`.",
               "После цикла выведи две строки: `Growth days: 5` и `Longest streak: 4`"],
        hint="Первый элемент сравнивается сам с собой: он не больше `prev`, поэтому на первом шаге просто начнётся серия "
             "длиной 1. Если не обновлять `prev`, каждый день будет сравниваться с первым, а не со вчерашним. "
             "Одинаковые продажи — это не рост: сравнение строгое.",
        solution='prev = sales[0]\ngrew = 0\nstreak = 1\nbest = 1\nfor day in sales:\n    if day > prev:\n'
                 '        grew += 1\n        streak += 1\n        if streak > best:\n            best = streak\n'
                 '    else:\n        streak = 1\n    prev = day\n'
                 'print(f"Growth days: {grew}")\nprint(f"Longest streak: {best}")',
        wrong=[("не обновляет prev: каждый день сравнивается с первым",
                'prev = sales[0]\ngrew = 0\nstreak = 1\nbest = 1\nfor day in sales:\n    if day > prev:\n'
                '        grew += 1\n        streak += 1\n        if streak > best:\n            best = streak\n'
                '    else:\n        streak = 1\n'
                'print(f"Growth days: {grew}")\nprint(f"Longest streak: {best}")'),
               ("нестрогое сравнение: одинаковые продажи считаются ростом",
                'prev = sales[0]\ngrew = 0\nstreak = 1\nbest = 1\nfor day in sales:\n    if day >= prev:\n'
                '        grew += 1\n        streak += 1\n        if streak > best:\n            best = streak\n'
                '    else:\n        streak = 1\n    prev = day\n'
                'print(f"Growth days: {grew}")\nprint(f"Longest streak: {best}")'),
               ("не начинает серию заново после спада",
                'prev = sales[0]\ngrew = 0\nstreak = 1\nbest = 1\nfor day in sales:\n    if day > prev:\n'
                '        grew += 1\n        streak += 1\n        if streak > best:\n            best = streak\n'
                '    prev = day\n'
                'print(f"Growth days: {grew}")\nprint(f"Longest streak: {best}")')],
        constructs=["list", "for", "if"],
    ),
]
