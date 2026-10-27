"""PY_LOGICAL_AND — «Логическое and». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, += -=, f-strings, if/else, comparison operators.
Not yet: or/not, elif, truthiness of non-bool values, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_LOGICAL_AND"
AND = [("And", "Используй and, чтобы объединить проверки в одном условии")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-and-rt-cabin-bag", title="Ручная кладь в самолёт",
        given=["weight", "length"],
        variants=[{"weight": "8", "length": "50"}, {"weight": "12", "length": "45"}, {"weight": "7", "length": "60"}],
        hidden=[{"weight": "10", "length": "55"}, {"weight": "11", "length": "55"}, {"weight": "10", "length": "56"},
                {"weight": "3", "length": "30"}],
        intro="Авиакомпания пускает сумку в салон, только если она весит не больше 10 кг **и** её длина не больше 55 см. "
              "Сумка пассажира весит `weight = {weight}` кг, её длина — `length = {length}` см.",
        steps=["Выведи через `print` с запятой `Weight OK:` и результат сравнения: вес не больше 10.",
               "Выведи `Size OK:` и результат сравнения: длина не больше 55.",
               "Если оба условия выполнены одновременно, выведи `Take it to the cabin`, иначе — `Check it in`. "
               "Объедини обе проверки в одном условии с помощью `and`.",
               "Например, для 10 кг и 56 см программа выводит `Weight OK: True`, `Size OK: False`, `Check it in`."],
        hint="`and` даёт `True`, только когда истинны обе части: `True and False` — это `False`. "
             "«Не больше 10» — это `<= 10`: сумка ровно 10 кг ещё проходит.",
        solution='print("Weight OK:", weight <= 10)\nprint("Size OK:", length <= 55)\nif weight <= 10 and length <= 55:\n'
                 '    print("Take it to the cabin")\nelse:\n    print("Check it in")',
        wrong=[("проверяет только вес, про длину забыли",
                'print("Weight OK:", weight <= 10)\nprint("Size OK:", length <= 55)\nif weight <= 10:\n'
                '    print("Take it to the cabin")\nelse:\n    print("Check it in")'),
               ("строгое сравнение в условии: сумку ровно 10 кг не пускают",
                'print("Weight OK:", weight <= 10)\nprint("Size OK:", length <= 55)\nif weight < 10 and length <= 55:\n'
                '    print("Take it to the cabin")\nelse:\n    print("Check it in")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-and-rt-garden-watering", title="Автополив огорода",
        given=["humidity", "rain"],
        variants=[{"humidity": "22", "rain": "0"}, {"humidity": "18", "rain": "4"}, {"humidity": "35", "rain": "0"}],
        hidden=[{"humidity": "30", "rain": "0"}, {"humidity": "29", "rain": "0"}, {"humidity": "5", "rain": "1"},
                {"humidity": "60", "rain": "12"}],
        intro="Автополив включается, только если влажность почвы меньше 30% **и** за ночь не было дождя (выпало 0 мм). "
              "Датчик показывает влажность `humidity = {humidity}` %, а дождь за ночь — `rain = {rain}` мм. "
              "Поливать нужно тем дольше, чем суше земля: по 2 минуты на каждый процент, которого не хватает до 30.",
        steps=["С помощью f-строк выведи `Humidity: <humidity>%` и `Dry: <True/False>` — результат сравнения "
               "«`humidity` меньше 30».",
               "Если влажность меньше 30 **и** `rain` равен 0, посчитай время полива `minutes` — `30 - humidity`, "
               "умноженное на 2, и выведи `Watering for <minutes> min`.",
               "Иначе выведи `No watering`.",
               "Например, для влажности 29% без дождя программа выводит `Humidity: 29%`, `Dry: True`, "
               "`Watering for 2 min`."],
        hint="Обе проверки пишутся полностью: `humidity < 30 and rain == 0`. Влажность ровно 30% — уже не сухо, "
             "поэтому сравнение строгое `<`. Разность `30 - humidity` возьми в скобки перед умножением.",
        solution='print(f"Humidity: {humidity}%")\nprint(f"Dry: {humidity < 30}")\nif humidity < 30 and rain == 0:\n'
                 '    minutes = (30 - humidity) * 2\n    print(f"Watering for {minutes} min")\nelse:\n    print("No watering")',
        wrong=[("не проверяет дождь — поливает и после ливня",
                'print(f"Humidity: {humidity}%")\nprint(f"Dry: {humidity < 30}")\nif humidity < 30:\n'
                '    minutes = (30 - humidity) * 2\n    print(f"Watering for {minutes} min")\nelse:\n    print("No watering")'),
               ("<= вместо <: при ровно 30% поливает 0 минут",
                'print(f"Humidity: {humidity}%")\nprint(f"Dry: {humidity < 30}")\nif humidity <= 30 and rain == 0:\n'
                '    minutes = (30 - humidity) * 2\n    print(f"Watering for {minutes} min")\nelse:\n    print("No watering")'),
               ("забывает скобки — умножается только влажность",
                'print(f"Humidity: {humidity}%")\nprint(f"Dry: {humidity < 30}")\nif humidity < 30 and rain == 0:\n'
                '    minutes = 30 - humidity * 2\n    print(f"Watering for {minutes} min")\nelse:\n    print("No watering")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-and-rt-button-click", title="Попал ли клик в кнопку",
        given=["x", "y", "left", "top", "width", "height"],
        variants=[{"x": "130", "y": "215", "left": "100", "top": "200", "width": "80", "height": "30"},
                  {"x": "250", "y": "40", "left": "200", "top": "50", "width": "120", "height": "40"},
                  {"x": "64", "y": "90", "left": "20", "top": "70", "width": "40", "height": "25"}],
        hidden=[{"x": "100", "y": "200", "left": "100", "top": "200", "width": "80", "height": "30"},
                {"x": "180", "y": "210", "left": "100", "top": "200", "width": "80", "height": "30"},
                {"x": "179", "y": "229", "left": "100", "top": "200", "width": "80", "height": "30"},
                {"x": "150", "y": "230", "left": "100", "top": "200", "width": "80", "height": "30"},
                {"x": "99", "y": "260", "left": "100", "top": "200", "width": "80", "height": "30"}],
        intro="Программа рисует на экране прямоугольную кнопку: её левый верхний угол в точке (`left = {left}`, "
              "`top = {top}`), ширина `width = {width}` и высота `height = {height}` пикселей. Координата `x` растёт вправо, "
              "`y` — вниз. Пользователь кликнул в точку (`x = {x}`, `y = {y}`). Пиксели кнопки — от `left` до "
              "`left + width - 1` по горизонтали и от `top` до `top + height - 1` по вертикали.",
        steps=["Выведи f-строкой `Click: <x>, <y>`.",
               "Выведи f-строкой `Inside X: <True/False>` — `x` не меньше `left` **и** `x` меньше `left + width`.",
               "Выведи f-строкой `Inside Y: <True/False>` — `y` не меньше `top` **и** `y` меньше `top + height`.",
               "Если выполнены все четыре условия сразу, выведи `Button pressed` и f-строкой `Offset: <x - left>, <y - top>` "
               "(где внутри кнопки был клик). Иначе выведи `Missed`.",
               "Например, для кнопки 100, 200, 80, 30 и клика в точку 100, 200 программа выводит `Click: 100, 200`, "
               "`Inside X: True`, `Inside Y: True`, `Button pressed`, `Offset: 0, 0`."],
        hint="Через `and` можно соединить четыре проверки: `x >= left and x < left + width and y >= top and y < top + height`. "
             "Правая граница не входит: при ширине 80 и `left = 100` последний пиксель кнопки — 179, а 180 — уже мимо.",
        solution='print(f"Click: {x}, {y}")\nprint(f"Inside X: {x >= left and x < left + width}")\n'
                 'print(f"Inside Y: {y >= top and y < top + height}")\n'
                 'if x >= left and x < left + width and y >= top and y < top + height:\n'
                 '    print("Button pressed")\n    print(f"Offset: {x - left}, {y - top}")\nelse:\n    print("Missed")',
        wrong=[("<= вместо <: клик на пиксель правее кнопки засчитывается",
                'print(f"Click: {x}, {y}")\nprint(f"Inside X: {x >= left and x <= left + width}")\n'
                'print(f"Inside Y: {y >= top and y <= top + height}")\n'
                'if x >= left and x <= left + width and y >= top and y <= top + height:\n'
                '    print("Button pressed")\n    print(f"Offset: {x - left}, {y - top}")\nelse:\n    print("Missed")'),
               ("в условии проверяет только x",
                'print(f"Click: {x}, {y}")\nprint(f"Inside X: {x >= left and x < left + width}")\n'
                'print(f"Inside Y: {y >= top and y < top + height}")\n'
                'if x >= left and x < left + width:\n'
                '    print("Button pressed")\n    print(f"Offset: {x - left}, {y - top}")\nelse:\n    print("Missed")'),
               ("сравнивает с шириной, забыв прибавить left",
                'print(f"Click: {x}, {y}")\nprint(f"Inside X: {x >= left and x < width}")\n'
                'print(f"Inside Y: {y >= top and y < top + height}")\n'
                'if x >= left and x < width and y >= top and y < top + height:\n'
                '    print("Button pressed")\n    print(f"Offset: {x - left}, {y - top}")\nelse:\n    print("Missed")')],
        constructs=["if"],
        must_use=AND,
    ),
]
