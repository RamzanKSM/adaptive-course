"""PY_TYPE_CONVERSION — «Преобразование типов». Taught before: print, variables, arithmetic, int/float, strings.
Not yet: f-strings, // and %, conditions, loops, functions."""
from build import OutputTask

SKILL = "PY_TYPE_CONVERSION"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-tc-rt-graduation", title="Сколько лет до выпуска",
        given=["now", "grad"],
        variants=[{"now": '"2026"', "grad": '"2030"'}, {"now": '"2025"', "grad": '"2027"'}, {"now": '"2026"', "grad": '"2036"'}],
        hidden=[{"now": '"2026"', "grad": '"2026"'}, {"now": '"2024"', "grad": '"2029"'}, {"now": '"2030"', "grad": '"2041"'}],
        intro="Ученик заполнил на сайте школы форму: текущий год и год выпуска. Из формы они пришли строками: "
              "`now = {now}` и `grad = {grad}`. Нужно показать, сколько лет осталось до выпуска.",
        steps=["Преврати строки `now` и `grad` в целые числа с помощью `int()`.",
               "Выведи через запятую `Years left:` и разность: год выпуска минус текущий год. "
               "Например, для `\"2020\"` и `\"2023\"` это `Years left: 3`."],
        hint='`int("2030")` превращает строку `"2030"` в число `2030`, и его уже можно вычитать. '
             "Из большего года вычитай меньший: из года выпуска — текущий.",
        solution='print("Years left:", int(grad) - int(now))',
        wrong=[("вычитает в обратном порядке — получается отрицательное число",
                'print("Years left:", int(now) - int(grad))'),
               ("склеивает строки вместо вычитания", 'print("Years left:", grad + now)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-tc-rt-digital-clock", title="Электронные часы",
        given=["hours", "minutes"],
        variants=[{"hours": "14", "minutes": "35"}, {"hours": "9", "minutes": "50"}, {"hours": "23", "minutes": "10"}],
        hidden=[{"hours": "0", "minutes": "45"}, {"hours": "12", "minutes": "12"}, {"hours": "7", "minutes": "59"}],
        intro="Электронные часы хранят время двумя числами: часы `hours = {hours}` и минуты `minutes = {minutes}`. "
              "На экран время нужно вывести одной строкой через двоеточие, без пробелов.",
        steps=["Преврати `hours` и `minutes` в строки с помощью `str()`.",
               "Склей через `+` слово `Time: `, часы, `\":\"` и минуты и выведи результат. "
               "Например, для 8 часов 25 минут это `Time: 8:25`."],
        hint='Число нельзя приклеить к строке через `+`: Python остановится с ошибкой `TypeError`. '
             '`str(25)` превращает число в строку `"25"`, и её уже можно склеивать: `str(8) + ":" + str(25)` даёт `"8:25"`.',
        solution='print("Time: " + str(hours) + ":" + str(minutes))',
        wrong=[("печатает через запятую — вокруг двоеточия появляются пробелы",
                'print("Time:", hours, ":", minutes)'),
               ("забывает двоеточие между часами и минутами",
                'print("Time: " + str(hours) + str(minutes))'),
               ("складывает часы и минуты как числа",
                'print("Time: " + str(hours + minutes))')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-tc-rt-sale-price", title="Цена со скидкой",
        given=["price", "discount"],
        variants=[{"price": '"1200"', "discount": '"15"'}, {"price": '"800"', "discount": '"30"'},
                  {"price": '"999"', "discount": '"10"'}],
        hidden=[{"price": '"500"', "discount": '"0"'}, {"price": '"350"', "discount": '"50"'},
                {"price": '"1000"', "discount": '"33"'}],
        intro="Интернет-магазин получил из базы цену товара и скидку в процентах строками: `price = {price}` руб. "
              "и `discount = {discount}` процентов. На карточке товара нужно показать старую и новую цену.",
        steps=["Преврати `price` и `discount` в целые числа с помощью `int()`.",
               "Посчитай новую цену `new_price`. Сначала найди, сколько процентов цены остаётся: 100 минус скидка — "
               "эту разность возьми в скобки. Затем умножь цену на неё и раздели на 100.",
               "Выведи одной строкой, склеив через `+`: `Was `, старую цену (строку `price` можно взять как есть), "
               "` rub, now `, новую цену, превращённую в строку через `str()`, и ` rub`. "
               "Например, для `\"200\"` и `\"10\"` нужно вывести `Was 200 rub, now 180.0 rub`."],
        hint="Деление через `/` всегда даёт дробное число, поэтому новая цена будет с точкой, например `180.0`. "
             "Без скобок `int(price) * 100 - int(discount) / 100` сначала выполнит умножение и деление, и получится "
             "совсем другое число.",
        solution='new_price = int(price) * (100 - int(discount)) / 100\nprint("Was " + price + " rub, now " + str(new_price) + " rub")',
        wrong=[("вычитает скидку в рублях, а не в процентах",
                'new_price = int(price) - int(discount)\nprint("Was " + price + " rub, now " + str(new_price) + " rub")'),
               ("забывает скобки вокруг разности",
                'new_price = int(price) * 100 - int(discount) / 100\nprint("Was " + price + " rub, now " + str(new_price) + " rub")'),
               ("считает саму скидку вместо новой цены",
                'new_price = int(price) * int(discount) / 100\nprint("Was " + price + " rub, now " + str(new_price) + " rub")')],
    ),
]
