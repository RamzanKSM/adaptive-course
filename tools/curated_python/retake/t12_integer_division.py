"""PY_INTEGER_DIVISION — «Деление // и остаток %». Taught before: print (several values separated by commas), variables,
assignment, arithmetic, order of execution, int/float (`/` gives a float), strings, type conversion.
Not yet: += -=, f-strings, conditions, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_INTEGER_DIVISION"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-id-rt-metro-trips", title="Поездки на метро",
        given=["money", "fare"],
        variants=[{"money": "500", "fare": "65"}, {"money": "300", "fare": "46"}, {"money": "1000", "fare": "80"}],
        hidden=[{"money": "130", "fare": "65"}, {"money": "40", "fare": "50"}, {"money": "777", "fare": "70"}],
        intro="У Камилы на транспортной карте `money = {money}` руб., одна поездка на метро стоит `fare = {fare}` руб. "
              "Ей интересно, сколько поездок она сможет сделать и сколько денег останется на карте.",
        steps=["Посчитай число поездок `trips` — `money`, делённые на `fare` нацело (`//`).",
               "Посчитай, сколько останется на карте: `left` — остаток от деления `money` на `fare` (`%`).",
               "Выведи три строки через запятую в `print`: `Trips:` и `trips`, `Spent:` и сколько рублей уйдёт на эти "
               "поездки (`trips`, умноженные на `fare`), `Left:` и `left`. Например, для 100 руб. при цене 30 это "
               "`Trips: 3`, `Spent: 90` и `Left: 10`."],
        hint="`//` делит нацело и отбрасывает дробную часть: `100 // 30` даёт `3`. `%` даёт остаток: `100 % 30` — это `10`. "
             "Обычное деление `/` здесь не подходит: `100 / 30` даёт дробное число, а поездок бывает только целое число.",
        solution='trips = money // fare\nleft = money % fare\nprint("Trips:", trips)\nprint("Spent:", trips * fare)\n'
                 'print("Left:", left)',
        wrong=[("делит через `/` — поездок получается дробное число",
                'trips = money / fare\nleft = money % fare\nprint("Trips:", trips)\nprint("Spent:", trips * fare)\n'
                'print("Left:", left)'),
               ("путает `//` и `%`: остаток считает делением нацело",
                'trips = money // fare\nleft = money // fare\nprint("Trips:", trips)\nprint("Spent:", trips * fare)\n'
                'print("Left:", left)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-id-rt-kopecks", title="Рубли и копейки",
        given=["price", "count"],
        variants=[{"price": "12345", "count": "3"}, {"price": "8950", "count": "4"}, {"price": "4999", "count": "2"}],
        hidden=[{"price": "100", "count": "1"}, {"price": "99", "count": "5"}, {"price": "25075", "count": "4"},
                {"price": "1234", "count": "7"}],
        intro="Касса магазина хранит цены в копейках, чтобы не было дробей: одна упаковка кофе стоит `price = {price}` коп., "
              "покупатель берёт `count = {count}` упаковки. В чеке цену пишут в рублях и копейках (в рубле 100 копеек).",
        steps=["Разложи цену одной упаковки: `rub` — `price`, делённая нацело на 100, `kop` — остаток от деления `price` на 100.",
               "Посчитай стоимость всей покупки в копейках: `total` — `price`, умноженная на `count`.",
               "Разложи `total` так же: `total_rub` и `total_kop`.",
               "Выведи две строки через запятую: `Price:`, `rub`, `rub`, `kop`, `kop` и `Total:`, `total_rub`, `rub`, "
               "`total_kop`, `kop`. Например, для цены 250 коп. и 3 упаковок это `Price: 2 rub 50 kop` и "
               "`Total: 7 rub 50 kop`."],
        hint="Сначала перемножь копейки, а раскладывай на рубли и копейки уже итог: `250 * 3` даёт `750`, "
             "`750 // 100` — `7` руб., `750 % 100` — `50` коп. Если умножить на `count` отдельно рубли и копейки, "
             "копеек может стать больше 100.",
        solution='rub = price // 100\nkop = price % 100\ntotal = price * count\ntotal_rub = total // 100\n'
                 'total_kop = total % 100\nprint("Price:", rub, "rub", kop, "kop")\nprint("Total:", total_rub, "rub", total_kop, "kop")',
        wrong=[("умножает отдельно рубли и копейки — копеек бывает больше 100",
                'rub = price // 100\nkop = price % 100\ntotal = price * count\ntotal_rub = rub * count\n'
                'total_kop = kop * count\nprint("Price:", rub, "rub", kop, "kop")\nprint("Total:", total_rub, "rub", total_kop, "kop")'),
               ("делит на 1000 вместо 100",
                'rub = price // 1000\nkop = price % 1000\ntotal = price * count\ntotal_rub = total // 1000\n'
                'total_kop = total % 1000\nprint("Price:", rub, "rub", kop, "kop")\nprint("Total:", total_rub, "rub", total_kop, "kop")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-id-rt-theater-seat", title="Ряд и место в зале",
        given=["ticket", "per_row"],
        variants=[{"ticket": "47", "per_row": "12"}, {"ticket": "100", "per_row": "15"}, {"ticket": "23", "per_row": "8"}],
        hidden=[{"ticket": "12", "per_row": "12"}, {"ticket": "1", "per_row": "10"}, {"ticket": "13", "per_row": "12"},
                {"ticket": "60", "per_row": "20"}],
        intro="В школьном актовом зале места пронумерованы подряд с 1: в первом ряду места с 1 по `per_row`, во втором — "
              "следующие и так далее. В каждом ряду `per_row = {per_row}` мест. На билете Глеба номер `ticket = {ticket}`. "
              "Нужно найти ряд и место в ряду.",
        steps=["Нумерация начинается с 1, а считать удобнее с 0, поэтому заведи `index` — `ticket` минус 1.",
               "Посчитай ряд `row`: `index`, делённый нацело на `per_row`, плюс 1.",
               "Посчитай место в ряду `seat`: остаток от деления `index` на `per_row`, плюс 1.",
               "Выведи четыре строки через запятую: `Ticket:` и `ticket`, `Row:` и `row`, `Seat:` и `seat`, `Seats to the right:` "
               "и сколько мест в ряду правее Глеба (`per_row` минус `seat`). Например, для билета 10 при 4 местах в ряду это "
               "`Ticket: 10`, `Row: 3`, `Seat: 2` и `Seats to the right: 2`."],
        hint="Проверь крайний случай: последний билет первого ряда. Если делить сам `ticket`, то при 12 местах в ряду "
             "`12 // 12` даст `1`, и билет 12 уедет во второй ряд, а `12 % 12` даст место `0`. С `index` всё сходится: "
             "`11 // 12` — это `0`, плюс 1 — первый ряд, `11 % 12` — это `11`, плюс 1 — место 12.",
        solution='index = ticket - 1\nrow = index // per_row + 1\nseat = index % per_row + 1\nprint("Ticket:", ticket)\n'
                 'print("Row:", row)\nprint("Seat:", seat)\nprint("Seats to the right:", per_row - seat)',
        wrong=[("делит сам номер билета — последний билет ряда уезжает в следующий ряд",
                'row = ticket // per_row + 1\nseat = ticket % per_row\nprint("Ticket:", ticket)\n'
                'print("Row:", row)\nprint("Seat:", seat)\nprint("Seats to the right:", per_row - seat)'),
               ("забывает прибавить 1 к ряду — ряды считаются с нуля",
                'index = ticket - 1\nrow = index // per_row\nseat = index % per_row + 1\nprint("Ticket:", ticket)\n'
                'print("Row:", row)\nprint("Seat:", seat)\nprint("Seats to the right:", per_row - seat)'),
               ("путает // и % — ряд считает остатком",
                'index = ticket - 1\nrow = index % per_row + 1\nseat = index // per_row + 1\nprint("Ticket:", ticket)\n'
                'print("Row:", row)\nprint("Seat:", seat)\nprint("Seats to the right:", per_row - seat)')],
    ),
]
