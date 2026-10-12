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
               "и сразу за ними номера класса — без пробелов. Например, для Петрова из 7 класса логин — `{school}-пет7`.",
               "Верни логин через `return` как строку."],
        hint="Вспомни срезы строк и метод `.lower()`. Номер класса — число, поэтому перед склейкой со строкой "
             "его нужно превратить в строку через `str()` — или собрать логин в f-строке.",
        starter="def make_login(surname, grade):\n    # Напиши решение здесь\n    pass\n",
        solution='def make_login(surname, grade):\n    return "{school}-" + surname[:3].lower() + str(grade)\n',
        inputs=['"Петров", 7', '"Смирнова", 11', '"Иванов", 5', '"Кузнецова", 9', '"ОРЛОВ", 6', '"Ёлкин", 10'],
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
]
