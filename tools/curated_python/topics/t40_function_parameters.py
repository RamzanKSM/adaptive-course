"""PY_FUNCTION_PARAMETERS — «Параметры функций». Taught before: everything up to return (conditions, loops, lists,
slices, string methods, def, return). Here: several parameters, default values, keyword arguments."""
from build import FunctionTask

SKILL = "PY_FUNCTION_PARAMETERS"

TASKS = [
    FunctionTask(
        skill=SKILL, difficulty=1, slug="py-par-quiz-score", title="Счёт в викторине",
        function="quiz_score",
        variants=[{"plus": 10, "minus": 5}, {"plus": 3, "minus": 1}, {"plus": 100, "minus": 30}],
        intro="В школьной викторине каждый правильный ответ приносит игроку +{plus} к счёту, "
              "а каждый неправильный отнимает {minus}. Нужна функция, которая считает итоговый счёт.",
        steps=["Допиши функцию `quiz_score(right, wrong)`: `right` — количество правильных ответов, "
               "`wrong` — количество неправильных.",
               "Верни итоговый счёт целым числом: {plus} за каждый правильный ответ минус {minus} "
               "за каждый неправильный. Счёт может получиться и отрицательным.",
               "Функцию вызывают и с именованными аргументами, например `quiz_score(wrong=1, right=4)`, "
               "поэтому не меняй названия и порядок параметров."],
        hint="При вызове с именами (`quiz_score(wrong=1, right=4)`) Python раскладывает значения по параметрам "
             "с такими же именами, а не по порядку. Внутри функции просто используй `right` и `wrong` как обычные переменные.",
        starter="def quiz_score(right, wrong):\n    # Напиши решение здесь\n    pass\n",
        solution="def quiz_score(right, wrong):\n    return right * {plus} - wrong * {minus}\n",
        inputs=["5, 2", "wrong=1, right=4", "0, 3", "8, 0", "wrong=6, right=6", "right=2, wrong=9"],
        public=3,
        wrong=[("переставил параметры местами: правильные и неправильные ответы путаются",
                "def quiz_score(wrong, right):\n    return right * {plus} - wrong * {minus}\n"),
               ("прибавляет штраф вместо того, чтобы вычитать",
                "def quiz_score(right, wrong):\n    return right * {plus} + wrong * {minus}\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=2, slug="py-par-bike-rent", title="Аренда велосипеда",
        function="rent_cost",
        variants=[{"price": 150}, {"price": 200}, {"price": 120}],
        intro="В прокате велосипедов час аренды обычно стоит {price} руб. Но в выходные и праздники цена другая — "
              "тогда её передают в функцию отдельно.",
        steps=["Допиши функцию `rent_cost(hours, price={price})`: `hours` — на сколько часов взяли велосипед, "
               "`price` — цена одного часа. Значение по умолчанию {price} уже стоит в заготовке.",
               "Если цену не передали, функция считает по {price} руб. за час. Если передали — например, "
               "`rent_cost(3, 90)` или `rent_cost(3, price=90)`, — считает по переданной цене.",
               "Верни стоимость аренды целым числом: количество часов, умноженное на цену часа."],
        hint="Внутри функции используй параметр `price`, а не число {price}: если цену передали при вызове, "
             "в `price` окажется она, а если не передали — значение по умолчанию.",
        starter="def rent_cost(hours, price={price}):\n    # Напиши решение здесь\n    pass\n",
        solution="def rent_cost(hours, price={price}):\n    return hours * price\n",
        inputs=["2", "3, 90", "hours=5", "1, price=250", "price=80, hours=4", "0"],
        public=3,
        wrong=[("использует число из условия вместо параметра price — переданная цена не учитывается",
                "def rent_cost(hours, price={price}):\n    return hours * {price}\n"),
               ("убрал значение по умолчанию — вызов с одним аргументом падает с ошибкой",
                "def rent_cost(hours, price):\n    return hours * price\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=3, slug="py-par-delivery", title="Стоимость доставки",
        function="delivery_cost",
        variants=[{"per_kg": 20, "per_km": 5}, {"per_kg": 30, "per_km": 4}, {"per_kg": 15, "per_km": 8}],
        intro="Служба доставки считает цену посылки по весу и расстоянию. Чаще всего посылки везут на 10 км "
              "обычной доставкой, поэтому эти значения сделаны параметрами по умолчанию.",
        steps=["Допиши функцию `delivery_cost(weight, distance=10, express=False)`: `weight` — вес посылки в килограммах, "
               "`distance` — расстояние в километрах (по умолчанию 10), `express` — нужна ли срочная доставка "
               "(по умолчанию нет).",
               "Обычная доставка стоит {per_kg} руб. за каждый килограмм плюс {per_km} руб. за каждый километр.",
               "Если `express` равно `True`, вся стоимость удваивается.",
               "Верни итоговую стоимость целым числом. Функцию могут вызвать и с именованными аргументами, "
               "например `delivery_cost(2, express=True)`."],
        hint="Сначала посчитай обычную стоимость и сохрани её в переменную. Потом проверь `express` через `if` "
             "и, если нужно, запиши в ту же переменную удвоенное значение. Значения по умолчанию подставятся сами, "
             "когда аргумент не передан.",
        starter="def delivery_cost(weight, distance=10, express=False):\n    # Напиши решение здесь\n    pass\n",
        solution="def delivery_cost(weight, distance=10, express=False):\n    cost = weight * {per_kg} + distance * {per_km}\n"
                 "    if express:\n        cost = cost * 2\n    return cost\n",
        inputs=["2", "3, 20", "1, express=True", "5, 0, True", "weight=4, distance=15",
                "express=True, distance=1, weight=10", "0, 7"],
        public=3,
        wrong=[("пишет `cost * 2`, но не сохраняет результат — срочная доставка стоит как обычная",
                "def delivery_cost(weight, distance=10, express=False):\n    cost = weight * {per_kg} + distance * {per_km}\n"
                "    if express:\n        cost * 2\n    return cost\n"),
               ("всегда считает 10 км вместо параметра distance",
                "def delivery_cost(weight, distance=10, express=False):\n    cost = weight * {per_kg} + 10 * {per_km}\n"
                "    if express:\n        cost = cost * 2\n    return cost\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=1, slug="py-par-split-bill", title="Делим счёт в кафе",
        function="split_bill",
        variants=[{"tip": 50}, {"tip": 30}, {"tip": 100}],
        intro="Друзья поужинали в кафе и делят счёт поровну. Кроме своей доли, каждый оставляет официанту "
              "{tip} руб. чаевых. Нужна функция, которая считает, сколько платит один человек.",
        steps=["Допиши функцию `split_bill(total, people)`: `total` — сумма счёта в рублях, `people` — сколько человек "
               "делят счёт.",
               "Верни целым числом, сколько платит один человек: `total`, делённое нацело на `people`, плюс {tip} руб. чаевых.",
               "Функцию вызывают и с именованными аргументами, например `split_bill(people=3, total=900)`, "
               "поэтому не меняй названия и порядок параметров."],
        hint="При вызове с именами Python кладёт значение в параметр с таким же именем, в каком бы порядке их ни написали. "
             "Чаевые прибавляются к доле каждого, а не к общему счёту: сначала раздели, потом прибавь.",
        starter="def split_bill(total, people):\n    # Напиши решение здесь\n    pass\n",
        solution="def split_bill(total, people):\n    return total // people + {tip}\n",
        inputs=["1200, 4", "people=3, total=900", "500, 1", "total=2000, people=5", "1000, 3", "people=2, total=750"],
        public=3,
        wrong=[("переставил параметры местами: счёт и число людей путаются",
                "def split_bill(people, total):\n    return total // people + {tip}\n"),
               ("делит чаевые вместе со счётом — каждому достаётся только часть чаевых",
                "def split_bill(total, people):\n    return (total + {tip}) // people\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=2, slug="py-par-cake-boxes", title="Коробки для пирожных",
        function="boxes_needed",
        variants=[{"size": 6}, {"size": 4}, {"size": 9}],
        intro="Кондитерская упаковывает пирожные в коробки. Обычная коробка вмещает {size} штук, но для больших заказов "
              "берут коробки другого размера — тогда размер передают в функцию отдельно.",
        steps=["Допиши функцию `boxes_needed(cakes, size={size})`: `cakes` — сколько пирожных нужно упаковать, "
               "`size` — сколько пирожных помещается в одну коробку. Значение по умолчанию {size} уже стоит в заготовке.",
               "Сначала посчитай полные коробки: `cakes`, делённое нацело на `size`. Если после этого остались "
               "пирожные (остаток от деления не 0), им нужна ещё одна неполная коробка.",
               "Верни число коробок целым числом. Функцию вызывают и так: `boxes_needed(20)`, "
               "и так: `boxes_needed(50, 8)` или `boxes_needed(50, size=8)`."],
        hint="Внутри функции используй параметр `size`, а не число {size}: если размер передали при вызове, "
             "в `size` окажется он. Остаток от деления даёт `%`.",
        starter="def boxes_needed(cakes, size={size}):\n    # Напиши решение здесь\n    pass\n",
        solution="def boxes_needed(cakes, size={size}):\n    boxes = cakes // size\n    if cakes % size != 0:\n"
                 "        boxes += 1\n    return boxes\n",
        inputs=["20", "50, 8", "cakes=36", "7, size=7", "size=10, cakes=45", "0", "1"],
        public=3,
        wrong=[("использует число из условия вместо параметра size — переданный размер не учитывается",
                "def boxes_needed(cakes, size={size}):\n    boxes = cakes // {size}\n    if cakes % {size} != 0:\n"
                "        boxes += 1\n    return boxes\n"),
               ("забывает про неполную коробку для оставшихся пирожных",
                "def boxes_needed(cakes, size={size}):\n    return cakes // size\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=3, slug="py-par-letter-greeting", title="Обращение в письме",
        function="greeting",
        variants=[{"word": "Dear"}, {"word": "Hello"}, {"word": "Hi"}],
        intro="Школа рассылает родителям письма, и каждое начинается с обращения. Чаще всего пишут `{word}` и полное имя, "
              "но иногда нужно другое приветствие или короткая форма с первой буквой имени.",
        steps=["Допиши функцию `greeting(name, surname, word=\"{word}\", short=False)`: `name` — имя, `surname` — фамилия, "
               "`word` — слово приветствия (по умолчанию `{word}`), `short` — нужна ли короткая форма (по умолчанию нет).",
               "Обычно функция возвращает приветствие, пробел, имя, пробел и фамилию, например `{word} Anna Petrova`.",
               "Если `short` равно `True`, вместо имени ставится его первая буква с точкой: `{word} A. Petrova`.",
               "Функцию вызывают по-разному, например `greeting(\"Gleb\", \"Lebedev\", short=True)` "
               "или `greeting(surname=\"Kim\", name=\"Egor\", word=\"Hey\")`."],
        hint="Первая буква строки — `name[0]`. Удобно сначала положить в переменную то, что будет на месте имени "
             "(всё имя или букву с точкой), а потом собрать строку через f-строку. Используй параметр `word`, "
             "а не слово `{word}` в кавычках — иначе переданное приветствие потеряется.",
        starter="def greeting(name, surname, word=\"{word}\", short=False):\n    # Напиши решение здесь\n    pass\n",
        solution="def greeting(name, surname, word=\"{word}\", short=False):\n    if short:\n        first = name[0] + \".\"\n"
                 "    else:\n        first = name\n    return f\"{{word}} {{first}} {{surname}}\"\n",
        inputs=['"Anna", "Petrova"', '"Boris", "Ivanov", short=True', '"Vika", "Orlova", "Good day"',
                'surname="Kim", name="Egor", word="Hey"', '"Dina", "Sokolova", short=True, word="Miss"',
                '"Timur", "Belov", "Mr", True'],
        public=3,
        wrong=[("всегда пишет приветствие по умолчанию — переданное слово не учитывается",
                "def greeting(name, surname, word=\"{word}\", short=False):\n    if short:\n        first = name[0] + \".\"\n"
                "    else:\n        first = name\n    return \"{word} \" + first + \" \" + surname\n"),
               ("в короткой форме забывает точку после буквы",
                "def greeting(name, surname, word=\"{word}\", short=False):\n    if short:\n        first = name[0]\n"
                "    else:\n        first = name\n    return f\"{{word}} {{first}} {{surname}}\"\n")],
    ),
]
