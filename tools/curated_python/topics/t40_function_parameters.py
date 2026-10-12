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
]
