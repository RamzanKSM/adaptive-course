"""PY_NUMBER_TYPES — «Числа: int и float». Taught before: print (several values separated by commas), variables,
assignment, arithmetic, order of execution. Here: whole and fractional numbers, the point in 2.5, `/` always gives a
float (10 / 2 is 5.0), int with float gives float. Not yet: strings beyond literals, int()/float()/str(), round(),
// and %, += -=, f-strings, conditions, loops, functions."""
from build import OutputTask

SKILL = "PY_NUMBER_TYPES"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-nt-average-mark", title="Средний балл за четверть",
        given=["m1", "m2", "m3", "m4"],
        variants=[{"m1": "5", "m2": "4", "m3": "4", "m4": "5"}, {"m1": "3", "m2": "4", "m3": "5", "m4": "5"},
                  {"m1": "4", "m2": "4", "m3": "3", "m4": "4"}],
        hidden=[{"m1": "5", "m2": "5", "m3": "5", "m4": "5"}, {"m1": "2", "m2": "3", "m3": "3", "m4": "3"},
                {"m1": "5", "m2": "4", "m3": "3", "m4": "2"}],
        intro="У Бориса за четверть четыре оценки по математике: `m1 = {m1}`, `m2 = {m2}`, `m3 = {m3}` и `m4 = {m4}`. "
              "Все они целые числа (`int`), а средний балл получится дробным (`float`).",
        steps=["Посчитай сумму оценок в переменную `total`.",
               "Посчитай средний балл `average`: `total`, делённый на 4 через `/`.",
               "Выведи `Sum:` и `total`, затем второй строкой `Average:` и `average`.",
               "Третьей строкой выведи `Doubled:` и `average`, умноженный на 2. Например, для оценок 5, 5, 4, 4 "
               "программа выводит `Sum: 18`, `Average: 4.5` и `Doubled: 9.0`."],
        hint="Деление через `/` в Python всегда даёт `float`, даже если делится нацело: `20 / 4` — это `5.0`, "
             "а не `5`. А дальше `float`, умноженный на целое число, тоже остаётся `float`. "
             "Без скобок `m1 + m2 + m3 + m4 / 4` поделит на 4 только последнюю оценку.",
        solution='total = m1 + m2 + m3 + m4\naverage = total / 4\nprint("Sum:", total)\nprint("Average:", average)\n'
                 'print("Doubled:", average * 2)',
        wrong=[("делит на 4 только последнюю оценку — забыл, что деление выполняется раньше сложения",
                'total = m1 + m2 + m3 + m4\naverage = m1 + m2 + m3 + m4 / 4\nprint("Sum:", total)\nprint("Average:", average)\n'
                'print("Doubled:", average * 2)'),
               ("делит на 3, хотя оценок четыре",
                'total = m1 + m2 + m3 + m4\naverage = total / 3\nprint("Sum:", total)\nprint("Average:", average)\n'
                'print("Doubled:", average * 2)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-nt-fabric", title="Ткань для штор",
        given=["meters", "price", "money"],
        variants=[{"meters": "2.5", "price": "340", "money": "1000"}, {"meters": "3.5", "price": "200", "money": "800"},
                  {"meters": "1.25", "price": "480", "money": "700"}],
        hidden=[{"meters": "4.0", "price": "150", "money": "600"}, {"meters": "0.5", "price": "90", "money": "100"},
                {"meters": "6.75", "price": "400", "money": "3000"}],
        intro="Мама покупает ткань для штор. Нужно `meters = {meters}` м, метр стоит `price = {price}` руб., "
              "а у мамы с собой `money = {money}` руб. Длина — дробное число (`float`), цена и деньги — целые (`int`).",
        steps=["Посчитай стоимость ткани `cost`: `meters`, умноженные на `price`.",
               "Посчитай сдачу `change`: `money` минус `cost`.",
               "Выведи три строки: `Meters:` и `meters`, `Cost:` и `cost`, `Change:` и `change`. "
               "Например, для 1.5 м по 100 руб. и 200 руб. с собой это `Meters: 1.5`, `Cost: 150.0` и `Change: 50.0`."],
        hint="Если в выражении есть хотя бы один `float`, результат тоже `float`: `1.5 * 100` даёт `150.0`. "
             "Поэтому и стоимость, и сдача выводятся с точкой — так и должно быть.",
        solution='cost = meters * price\nchange = money - cost\nprint("Meters:", meters)\nprint("Cost:", cost)\n'
                 'print("Change:", change)',
        wrong=[("вычитает из денег цену одного метра вместо стоимости ткани",
                'cost = meters * price\nchange = money - price\nprint("Meters:", meters)\nprint("Cost:", cost)\n'
                'print("Change:", change)'),
               ("складывает метры и цену вместо умножения",
                'cost = meters + price\nchange = money - cost\nprint("Meters:", meters)\nprint("Cost:", cost)\n'
                'print("Change:", change)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-nt-bike-speed", title="Скорость велосипедиста",
        given=["distance", "minutes"],
        variants=[{"distance": "12", "minutes": "45"}, {"distance": "9", "minutes": "30"}, {"distance": "27", "minutes": "90"}],
        hidden=[{"distance": "15", "minutes": "60"}, {"distance": "6", "minutes": "15"}, {"distance": "40", "minutes": "150"}],
        intro="Аня проехала на велосипеде `distance = {distance}` км за `minutes = {minutes}` минут. "
              "Нужно узнать её скорость в км/ч и сколько она проедет за 2 часа с той же скоростью.",
        steps=["Переведи минуты в часы: `hours` — это `minutes`, делённые на 60. В часе 60 минут, а не 100.",
               "Посчитай скорость `speed`: `distance`, делённая на `hours`.",
               "Выведи три строки: `Time:`, `hours` и `h`; `Speed:`, `speed` и `km/h`; `In 2 hours:`, `speed`, "
               "умноженная на 2, и `km`. Значения в `print` разделяй запятыми. Например, для 10 км за 30 минут это "
               "`Time: 0.5 h`, `Speed: 20.0 km/h` и `In 2 hours: 40.0 km`."],
        hint="`30 / 60` даёт `0.5` — это `float`, и всё, что посчитано из него, тоже будет `float`. "
             "Частая ошибка — делить минуты на 100: 30 минут — это половина часа, а не 0.3 часа.",
        solution='hours = minutes / 60\nspeed = distance / hours\nprint("Time:", hours, "h")\n'
                 'print("Speed:", speed, "km/h")\nprint("In 2 hours:", speed * 2, "km")',
        wrong=[("переводит минуты в часы делением на 100",
                'hours = minutes / 100\nspeed = distance / hours\nprint("Time:", hours, "h")\n'
                'print("Speed:", speed, "km/h")\nprint("In 2 hours:", speed * 2, "km")'),
               ("делит расстояние на минуты, а не на часы",
                'hours = minutes / 60\nspeed = distance / minutes\nprint("Time:", hours, "h")\n'
                'print("Speed:", speed, "km/h")\nprint("In 2 hours:", speed * 2, "km")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-nt-split-bill", title="Счёт в кафе на компанию",
        given=["bill", "friends"],
        variants=[{"bill": "3200", "friends": "4"}, {"bill": "1500", "friends": "3"}, {"bill": "2700", "friends": "6"}],
        hidden=[{"bill": "1000", "friends": "1"}, {"bill": "4500", "friends": "5"}, {"bill": "1800", "friends": "8"}],
        intro="Друзья поужинали в кафе, счёт — `bill = {bill}` руб. Они оставляют официанту чаевые 10 процентов от счёта "
              "и делят всю сумму поровну на `friends = {friends}` человек.",
        steps=["Посчитай чаевые `tip`: `bill`, делённый на 10.",
               "Посчитай всю сумму `total`: `bill` плюс `tip`.",
               "Посчитай долю каждого `share`: `total`, делённая на `friends`.",
               "Выведи три строки: `Tip:` и `tip`, `Total:` и `total`, `Each pays:` и `share`. "
               "Например, для счёта 1000 на двоих это `Tip: 100.0`, `Total: 1100.0` и `Each pays: 550.0`."],
        hint="10 процентов — это десятая часть, то есть `bill / 10`, а не `bill + 10`. После деления через `/` "
             "получается `float`, поэтому и сумма, и доля выводятся с точкой.",
        solution='tip = bill / 10\ntotal = bill + tip\nshare = total / friends\nprint("Tip:", tip)\n'
                 'print("Total:", total)\nprint("Each pays:", share)',
        wrong=[("делит на всех только счёт без чаевых",
                'tip = bill / 10\ntotal = bill + tip\nshare = bill / friends\nprint("Tip:", tip)\n'
                'print("Total:", total)\nprint("Each pays:", share)'),
               ("прибавляет 10 рублей вместо 10 процентов",
                'tip = bill / 10\ntotal = bill + 10\nshare = total / friends\nprint("Tip:", tip)\n'
                'print("Total:", total)\nprint("Each pays:", share)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-nt-paint-room", title="Краска для комнаты",
        given=["length", "width", "height", "price"],
        variants=[{"length": "4.5", "width": "3.5", "height": "2.5", "price": "320"},
                  {"length": "5.0", "width": "3.0", "height": "3.0", "price": "250"},
                  {"length": "3.5", "width": "2.5", "height": "2.5", "price": "400"}],
        hidden=[{"length": "4.0", "width": "4.0", "height": "2.5", "price": "300"},
                {"length": "6.5", "width": "3.5", "height": "3.0", "price": "200"},
                {"length": "2.0", "width": "2.0", "height": "2.0", "price": "500"}],
        intro="Борис красит стены комнаты. Комната длиной `length = {length}` м, шириной `width = {width}` м и высотой "
              "`height = {height}` м. Одного литра краски хватает на 8 квадратных метров, литр стоит `price = {price}` руб. "
              "Пол, потолок, окна и дверь не считаем.",
        steps=["Посчитай периметр комнаты `perimeter`: удвоенная сумма `length` и `width`.",
               "Посчитай площадь стен `walls`: `perimeter`, умноженный на `height`.",
               "Посчитай, сколько литров краски нужно: `paint` — это `walls`, делённая на 8.",
               "Посчитай стоимость `cost`: `paint`, умноженная на `price`.",
               "Выведи три строки: `Walls:`, `walls` и `m2`; `Paint:`, `paint` и `l`; `Cost:`, `cost` и `rub`. "
               "Например, для комнаты 3.0 на 1.0 высотой 2.0 и цены 100 это `Walls: 16.0 m2`, `Paint: 2.0 l` "
               "и `Cost: 200.0 rub`."],
        hint="У комнаты четыре стены: две длиной `length` и две длиной `width`, поэтому периметр — `2 * (length + width)`. "
             "Без скобок `2 * length + width` удвоит только длину. Все размеры дробные, так что ответы будут `float`.",
        solution='perimeter = 2 * (length + width)\nwalls = perimeter * height\npaint = walls / 8\ncost = paint * price\n'
                 'print("Walls:", walls, "m2")\nprint("Paint:", paint, "l")\nprint("Cost:", cost, "rub")',
        wrong=[("забывает скобки: удваивает только длину",
                'perimeter = 2 * length + width\nwalls = perimeter * height\npaint = walls / 8\ncost = paint * price\n'
                'print("Walls:", walls, "m2")\nprint("Paint:", paint, "l")\nprint("Cost:", cost, "rub")'),
               ("умножает площадь на 8 вместо деления",
                'perimeter = 2 * (length + width)\nwalls = perimeter * height\npaint = walls * 8\ncost = paint * price\n'
                'print("Walls:", walls, "m2")\nprint("Paint:", paint, "l")\nprint("Cost:", cost, "rub")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-nt-fahrenheit", title="Погода для гостя из США",
        given=["morning", "evening"],
        variants=[{"morning": "10", "evening": "25"}, {"morning": "-5", "evening": "15"}, {"morning": "20", "evening": "30"}],
        hidden=[{"morning": "0", "evening": "0"}, {"morning": "-20", "evening": "-5"}, {"morning": "35", "evening": "10"}],
        intro="К Ане приехал друг из США, он привык к градусам Фаренгейта. Утром было `morning = {morning}` градусов "
              "Цельсия, вечером — `evening = {evening}`. Градусы Фаренгейта получаются так: градусы Цельсия умножить на 9, "
              "разделить на 5 и прибавить 32.",
        steps=["Переведи утреннюю температуру в Фаренгейты: `morning_f` — это `morning * 9 / 5 + 32`.",
               "Так же переведи вечернюю температуру в `evening_f`.",
               "Посчитай среднюю температуру за день по Фаренгейту `middle`: сумма `morning_f` и `evening_f`, делённая на 2.",
               "Выведи три строки: `Morning:`, `morning_f` и `F`; `Evening:`, `evening_f` и `F`; `Middle:`, `middle` и `F`. "
               "Например, для 0 и 10 градусов это `Morning: 32.0 F`, `Evening: 50.0 F` и `Middle: 41.0 F`."],
        hint="Порядок действий важен: сначала умножение и деление, потом `+ 32`. Если написать `(morning + 32) * 9 / 5`, "
             "получится другое число. Из-за деления через `/` все ответы — `float`, даже `50.0`.",
        solution='morning_f = morning * 9 / 5 + 32\nevening_f = evening * 9 / 5 + 32\nmiddle = (morning_f + evening_f) / 2\n'
                 'print("Morning:", morning_f, "F")\nprint("Evening:", evening_f, "F")\nprint("Middle:", middle, "F")',
        wrong=[("прибавляет 32 до умножения",
                'morning_f = morning * 9 / 5 + 32\nevening_f = (evening + 32) * 9 / 5\nmiddle = (morning_f + evening_f) / 2\n'
                'print("Morning:", morning_f, "F")\nprint("Evening:", evening_f, "F")\nprint("Middle:", middle, "F")'),
               ("забывает скобки: делит на 2 только вечернюю температуру",
                'morning_f = morning * 9 / 5 + 32\nevening_f = evening * 9 / 5 + 32\nmiddle = morning_f + evening_f / 2\n'
                'print("Morning:", morning_f, "F")\nprint("Evening:", evening_f, "F")\nprint("Middle:", middle, "F")')],
    ),
]
