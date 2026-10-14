"""PY_FUNCTION_RETURN — «return и print». Taught before: everything up to functions that print (conditions, loops,
lists, slices, string methods, def with parameters). Here: return a value instead of printing it. Not yet: default
values and keyword arguments."""
from build import FunctionTask

SKILL = "PY_FUNCTION_RETURN"

TASKS = [
    FunctionTask(
        skill=SKILL, difficulty=1, slug="py-ret-trip-cost", title="Стоимость поездок",
        function="trip_cost",
        variants=[{"price": 35}, {"price": 46}, {"price": 60}],
        intro="Одна поездка на автобусе стоит {price} руб. Приложение-кошелёк заранее считает, сколько денег уйдёт "
              "на несколько поездок, и потом использует это число в других расчётах — поэтому функция должна "
              "вернуть его, а не напечатать.",
        steps=["Допиши функцию `trip_cost(trips)`: параметр `trips` — количество поездок (целое число).",
               "Функция должна вернуть через `return` стоимость всех поездок целым числом: `trips`, умноженное на {price}."],
        hint="`print` только показывает число на экране, а `return` отдаёт его тому, кто вызвал функцию: "
             "после `x = trip_cost(2)` в переменной `x` окажется результат. Функция без `return` возвращает `None`.",
        starter="def trip_cost(trips):\n    # Напиши решение здесь\n    pass\n",
        solution="def trip_cost(trips):\n    return trips * {price}\n",
        inputs=["2", "10", "1", "0", "7", "23"],
        wrong=[("печатает стоимость вместо return", "def trip_cost(trips):\n    print(trips * {price})\n"),
               ("возвращает строку вместо числа", "def trip_cost(trips):\n    return str(trips * {price})\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=2, slug="py-ret-school-login", title="Логин для школьного сайта",
        function="make_login",
        variants=[{"school": 12}, {"school": 57}, {"school": 239}],
        intro="На сайте школы №{school} каждому ученику выдают логин. Его собирает функция, а сайт потом "
              "сохраняет полученную строку — поэтому логин нужно вернуть, а не напечатать.",
        steps=["Допиши функцию `make_login(surname, grade)`: `surname` — фамилия ученика (строка), "
               "`grade` — номер класса (целое число).",
               "Логин состоит из номера школы {school}, дефиса, первых трёх букв фамилии маленькими буквами "
               "и сразу за ними номера класса — без пробелов. Например, для фамилии `Petrov` и 7 класса логин — `{school}-pet7`.",
               "Верни логин через `return` как строку."],
        hint="Вспомни срезы строк и метод `.lower()`. Номер класса — число, поэтому перед склейкой со строкой "
             "его нужно превратить в строку через `str()` — или собрать логин в f-строке.",
        starter="def make_login(surname, grade):\n    # Напиши решение здесь\n    pass\n",
        solution='def make_login(surname, grade):\n    return "{school}-" + surname[:3].lower() + str(grade)\n',
        inputs=['"Petrov", 7', '"Smirnova", 11', '"Ivanov", 5', '"Kuznetsova", 9', '"ORLOV", 6', '"Yolkin", 10'],
        wrong=[("печатает логин вместо return",
                'def make_login(surname, grade):\n    print("{school}-" + surname[:3].lower() + str(grade))\n'),
               ("не делает буквы маленькими",
                'def make_login(surname, grade):\n    return "{school}-" + surname[:3] + str(grade)\n')],
    ),
    FunctionTask(
        skill=SKILL, difficulty=3, slug="py-ret-museum-ticket", title="Цена билета в музей",
        function="ticket_price",
        variants=[{"child": 150, "adult": 300}, {"child": 200, "adult": 450}, {"child": 100, "adult": 250}],
        intro="В музее цена билета зависит от возраста посетителя. Касса вызывает твою функцию для каждого посетителя "
              "и складывает полученные цены в чек — поэтому функция должна возвращать число.",
        steps=["Допиши функцию `ticket_price(age)`: она получает возраст посетителя (целое число) "
               "и возвращает цену билета в рублях целым числом.",
               "Детям младше 7 лет вход бесплатный — верни `0`. С 7 до 17 лет включительно билет стоит {child} руб.",
               "С 18 до 64 лет включительно билет стоит {adult} руб., а с 65 лет — снова {child} руб."],
        hint="`return` сразу завершает функцию, поэтому удобно проверять возраст по порядку через `if`, `elif` и `else` "
             "и в каждой ветке возвращать свою цену. Убедись, что число возвращается в любой ветке — "
             "иначе для кого-то функция вернёт `None`.",
        starter="def ticket_price(age):\n    # Напиши решение здесь\n    pass\n",
        solution="def ticket_price(age):\n    if age < 7:\n        return 0\n    elif age < 18:\n        return {child}\n"
                 "    elif age < 65:\n        return {adult}\n    else:\n        return {child}\n",
        inputs=["12", "35", "5", "7", "17", "18", "64", "65", "80"],
        wrong=[("печатает цену вместо return",
                "def ticket_price(age):\n    if age < 7:\n        print(0)\n    elif age < 18:\n        print({child})\n"
                "    elif age < 65:\n        print({adult})\n    else:\n        print({child})\n"),
               ("нет ветки для посетителей от 65 лет — для них функция возвращает None",
                "def ticket_price(age):\n    if age < 7:\n        return 0\n    elif age < 18:\n        return {child}\n"
                "    elif age < 65:\n        return {adult}\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=1, slug="py-ret-coffee-change", title="Сдача в кофейне",
        function="change",
        variants=[{"price": 120}, {"price": 150}, {"price": 180}],
        intro="Стакан кофе стоит {price} руб. Касса вызывает функцию, чтобы узнать сдачу, и потом сама решает, "
              "какими монетами её выдать, — поэтому сдачу нужно вернуть, а не напечатать.",
        steps=["Допиши функцию `change(paid)`: параметр `paid` — сколько рублей дал покупатель (не меньше цены кофе).",
               "Функция должна вернуть через `return` сдачу целым числом: `paid` минус {price}."],
        hint="После `x = change(500)` в переменной `x` должна оказаться сдача. Если функция только печатает, "
             "в `x` попадёт `None`: функция без `return` ничего не возвращает.",
        starter="def change(paid):\n    # Напиши решение здесь\n    pass\n",
        solution="def change(paid):\n    return paid - {price}\n",
        inputs=["200", "500", "1000", "300", "250", "180"],
        wrong=[("печатает сдачу вместо return", "def change(paid):\n    print(paid - {price})\n"),
               ("вычитает в обратном порядке — сдача отрицательная", "def change(paid):\n    return {price} - paid\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=2, slug="py-ret-hide-card", title="Номер карты в SMS",
        function="hide_card",
        variants=[{"keep": 4}, {"keep": 3}, {"keep": 2}],
        intro="Банк присылает SMS о покупках, но не показывает номер карты целиком: видны только последние {keep} цифры, "
              "а остальные заменены звёздочками. Строку для SMS собирает функция, а отправляет её другая часть "
              "программы — поэтому строку нужно вернуть.",
        steps=["Допиши функцию `hide_card(number)`: `number` — номер карты, строка из цифр (длина может быть разной).",
               "Верни строку той же длины: сначала столько звёздочек `*`, сколько цифр скрыто, "
               "а потом последние {keep} цифры номера. Посмотри на примеры ниже."],
        hint="Последние цифры даёт срез с отрицательным началом: `number[-{keep}:]`. Число звёздочек — длина номера "
             "минус {keep}, а строку из одинаковых символов получают умножением: `\"*\" * 3` даёт `\"***\"`.",
        starter="def hide_card(number):\n    # Напиши решение здесь\n    pass\n",
        solution='def hide_card(number):\n    return "*" * (len(number) - {keep}) + number[-{keep}:]\n',
        inputs=['"1234567890123456"', '"4000123412341234"', '"9876543210"', '"55554444"', '"220012345678"', '"10203040"'],
        wrong=[("печатает строку вместо return",
                'def hide_card(number):\n    print("*" * (len(number) - {keep}) + number[-{keep}:])\n'),
               ("показывает первые цифры вместо последних",
                'def hide_card(number):\n    return number[:{keep}] + "*" * (len(number) - {keep})\n')],
    ),
    FunctionTask(
        skill=SKILL, difficulty=3, slug="py-ret-steps-goal", title="День, когда цель выполнена",
        function="goal_day",
        variants=[{"goal": 10000}, {"goal": 15000}, {"goal": 5000}],
        intro="Фитнес-браслет записывает, сколько шагов человек прошёл за каждый день, и хочет поздравить его, "
              "когда за всё время наберётся {goal} шагов. Функция находит номер этого дня и возвращает его приложению.",
        steps=["Допиши функцию `goal_day(steps)`: `steps` — список, где `steps[0]` — шаги за первый день, "
               "`steps[1]` — за второй и так далее.",
               "Складывай шаги день за днём. Как только сумма стала {goal} или больше, сразу верни номер этого дня — "
               "дни нумеруются с 1.",
               "Если и за все дни сумма не дошла до {goal}, верни `-1`."],
        hint="`return` внутри цикла сразу завершает функцию — дальше цикл уже не идёт. А `return -1` пиши после цикла: "
             "до него дело дойдёт, только если цель так и не была выполнена. Номер дня на 1 больше индекса.",
        starter="def goal_day(steps):\n    # Напиши решение здесь\n    pass\n",
        solution="def goal_day(steps):\n    total = 0\n    for i in range(len(steps)):\n        total += steps[i]\n"
                 "        if total >= {goal}:\n            return i + 1\n    return -1\n",
        inputs=["[3000, 4000, 2000, 6000, 1000]", "[1000, 2000]", "[5000, 5000, 5000]", "[20000]",
                "[4000, 1000, 4000, 1000, 5000, 3000]", "[]", "[2500, 2500, 2500, 2500, 2500, 2500]"],
        wrong=[("возвращает индекс, а не номер дня (на 1 меньше)",
                "def goal_day(steps):\n    total = 0\n    for i in range(len(steps)):\n        total += steps[i]\n"
                "        if total >= {goal}:\n            return i\n    return -1\n"),
               ("нет return -1 после цикла — если цель не выполнена, функция возвращает None",
                "def goal_day(steps):\n    total = 0\n    for i in range(len(steps)):\n        total += steps[i]\n"
                "        if total >= {goal}:\n            return i + 1\n")],
    ),
]
