"""Training attestation («Тренировочная аттестация»), Python, topics 1–11 (up to PY_FSTRINGS): print, variables,
assignment, arithmetic, order of execution, int/float, strings (+, *, len), type conversion (int(), str()), // and %,
+= -=, f-strings. Every story is different (office work, salaries and money) and new — not a story of the real
attestation pool; each reference solution uses all of these in a small program.
Not yet: format specifiers like :.2f, round(), conditions, comparisons, logical operators, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_FSTRINGS"
MUST = [("JoinedStr", "Используй f-строку: f\"...{переменная}...\""),
        ("AugAssign", "Используй составное присваивание (+= или -=), чтобы изменить переменную"),
        ("FloorDiv", "Используй деление нацело //"),
        ("Mod", "Используй остаток от деления %")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac11-timesheet", title="Табель и переработка",
        given=["name", "minutes", "rate", "norm"],
        variants=[{"name": '"Oleg Smirnov"', "minutes": '"10230"', "rate": "400", "norm": "160"}],
        hidden=[{"name": '"Ilya Kim"', "minutes": '"9600"', "rate": "350", "norm": "160"},
                {"name": '"Vera Lis"', "minutes": '"10859"', "rate": "333", "norm": "168"},
                {"name": '"Dina Orlova"', "minutes": '"9659"', "rate": "500", "norm": "160"},
                {"name": '"Boris"', "minutes": '"8461"', "rate": "455", "norm": "140"}],
        intro="Бухгалтер считает зарплату за месяц по табелю. Турникет на входе в офис посчитал, сколько минут "
              "отработал сотрудник `name = {name}`, и выдал это число строкой: `minutes = {minutes}`. Час работы стоит "
              "`rate = {rate}` руб., норма за месяц — `norm = {norm}` часов, и в этом месяце сотрудник отработал "
              "не меньше нормы. Неполный час не оплачивается, а часы сверх нормы (переработку) платят в полуторном размере.",
        steps=["Склей через `+` строку `Timesheet: ` и `name` и выведи, например `Timesheet: Ilya Kim`.",
               "Преврати `minutes` в целое число. Посчитай, сколько полных часов отработано, — `hours` (минуты, "
               "делённые нацело на 60), и сколько минут осталось сверх них, — `rest` (остаток от деления на 60).",
               "Посчитай переработку `overtime`: `hours` минус `norm`.",
               "Сохрани в `pay` оплату нормы: `norm * rate`. Затем прибавь к `pay` оплату переработки "
               "`overtime * rate * 1.5` с помощью `+=`.",
               "С помощью f-строк выведи `Worked: <hours> h <rest> min`, `Overtime: <overtime> h` и `Pay: <pay> rub`. "
               "Например, для `\"8461\"` минут, 455 руб. за час и нормы 140 часов программа выводит "
               "`Worked: 141 h 1 min`, `Overtime: 1 h`, `Pay: 64382.5 rub`."],
        hint="`int(\"10230\") // 60` даёт `170` полных часов, а `int(\"10230\") % 60` — `30` минут сверх них. "
             "Целое число, умноженное на дробное `1.5`, даёт дробное, поэтому зарплата выводится с точкой: `70000.0`.",
        solution='print("Timesheet: " + name)\nhours = int(minutes) // 60\nrest = int(minutes) % 60\n'
                 'overtime = hours - norm\npay = norm * rate\npay += overtime * rate * 1.5\n'
                 'print(f"Worked: {hours} h {rest} min")\nprint(f"Overtime: {overtime} h")\nprint(f"Pay: {pay} rub")',
        wrong=[("переработка оплачена как обычные часы, без 1.5",
                'print("Timesheet: " + name)\nhours = int(minutes) // 60\nrest = int(minutes) % 60\n'
                'overtime = hours - norm\npay = norm * rate\npay += overtime * rate\n'
                'print(f"Worked: {hours} h {rest} min")\nprint(f"Overtime: {overtime} h")\nprint(f"Pay: {pay} rub")'),
               ("минуты сверх часов посчитаны через // вместо остатка",
                'print("Timesheet: " + name)\nhours = int(minutes) // 60\nrest = int(minutes) // 60\n'
                'overtime = hours - norm\npay = norm * rate\npay += overtime * rate * 1.5\n'
                'print(f"Worked: {hours} h {rest} min")\nprint(f"Overtime: {overtime} h")\nprint(f"Pay: {pay} rub")'),
               ("часы посчитаны через / — неполный час тоже оплачен",
                'print("Timesheet: " + name)\nhours = int(minutes) / 60\nrest = int(minutes) % 60\n'
                'overtime = hours - norm\npay = norm * rate\npay += overtime * rate * 1.5\n'
                'print(f"Worked: {hours} h {rest} min")\nprint(f"Overtime: {overtime} h")\nprint(f"Pay: {pay} rub")')],
        must_use=MUST,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac11-double-print", title="Двусторонняя печать",
        given=["doc", "pages", "copies", "price"],
        variants=[{"doc": '"Annual report"', "pages": '"37"', "copies": "12", "price": "2.5"}],
        hidden=[{"doc": '"Contract"', "pages": '"40"', "copies": "3", "price": "2.5"},
                {"doc": '"Memo"', "pages": '"1"', "copies": "25", "price": "1.5"},
                {"doc": '"Price list"', "pages": '"15"', "copies": "1", "price": "4.0"},
                {"doc": '"Staff guide"', "pages": '"120"', "copies": "7", "price": "1.75"}],
        intro="Офис-менеджер печатает к совещанию документ `doc = {doc}`. Число страниц он взял из окна печати, "
              "поэтому оно записано строкой: `pages = {pages}`. Нужно `copies = {copies}` копий. Принтер печатает "
              "с двух сторон листа: на одном листе две страницы, а если страниц нечётное число, последняя страница "
              "занимает отдельный лист. Ещё 5 листов уходят на пробную печать, а один лист бумаги стоит "
              "`price = {price}` руб.",
        steps=["Склей через `+` название документа, `: `, строку `pages`, ` pages x `, число копий (преврати его "
               "в строку с помощью `str()`) и ` copies` и выведи, например `Contract: 40 pages x 3 copies`.",
               "Посчитай, сколько листов уходит на одну копию, — `per_copy`: число страниц (превращённое в целое "
               "число), делённое нацело на 2, плюс остаток от деления числа страниц на 2.",
               "Посчитай `sheets` — листы на все копии (`per_copy` умножить на `copies`) — и прибавь к ним "
               "5 листов на пробную печать с помощью `+=`.",
               "Только после этого посчитай стоимость бумаги `cost`: `sheets * price`.",
               "С помощью f-строк выведи `Sheets per copy: <per_copy>`, `Sheets: <sheets>` и `Cost: <cost> rub`. "
               "Например, для 15 страниц, одной копии и цены 4.0 руб. за лист — `Sheets per copy: 8`, "
               "`Sheets: 13`, `Cost: 52.0 rub`."],
        hint="`37 // 2` даёт `18` листов, заполненных с двух сторон, а `37 % 2` — `1`: ещё один лист для последней "
             "страницы. Для чётного числа страниц остаток равен 0. Цена дробная, поэтому и стоимость дробная: "
             "`13 * 4.0` даёт `52.0`.",
        solution='print(doc + ": " + pages + " pages x " + str(copies) + " copies")\n'
                 'per_copy = int(pages) // 2 + int(pages) % 2\nsheets = per_copy * copies\nsheets += 5\n'
                 'cost = sheets * price\nprint(f"Sheets per copy: {per_copy}")\nprint(f"Sheets: {sheets}")\n'
                 'print(f"Cost: {cost} rub")',
        wrong=[("забыт лист для последней нечётной страницы",
                'print(doc + ": " + pages + " pages x " + str(copies) + " copies")\n'
                'per_copy = int(pages) // 2\nsheets = per_copy * copies\nsheets += 5\n'
                'cost = sheets * price\nprint(f"Sheets per copy: {per_copy}")\nprint(f"Sheets: {sheets}")\n'
                'print(f"Cost: {cost} rub")'),
               ("листы на копию посчитаны через / — получается дробь",
                'print(doc + ": " + pages + " pages x " + str(copies) + " copies")\n'
                'per_copy = int(pages) / 2 + int(pages) % 2\nsheets = per_copy * copies\nsheets += 5\n'
                'cost = sheets * price\nprint(f"Sheets per copy: {per_copy}")\nprint(f"Sheets: {sheets}")\n'
                'print(f"Cost: {cost} rub")'),
               ("стоимость посчитана до того, как прибавлены пробные листы",
                'print(doc + ": " + pages + " pages x " + str(copies) + " copies")\n'
                'per_copy = int(pages) // 2 + int(pages) % 2\nsheets = per_copy * copies\ncost = sheets * price\n'
                'sheets += 5\nprint(f"Sheets per copy: {per_copy}")\nprint(f"Sheets: {sheets}")\n'
                'print(f"Cost: {cost} rub")')],
        must_use=MUST,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac11-seniority", title="Надбавка за стаж",
        given=["name", "months", "salary", "percent"],
        variants=[{"name": '"Pavel Orlov"', "months": '"77"', "salary": "64000", "percent": "3"}],
        hidden=[{"name": '"Anna Belova"', "months": '"11"', "salary": "45000", "percent": "4"},
                {"name": '"Ivan Petrov"', "months": '"12"', "salary": "50000", "percent": "5"},
                {"name": '"Lena Kuz"', "months": '"239"', "salary": "81250", "percent": "2"},
                {"name": '"Mark"', "months": '"30"', "salary": "47375", "percent": "3"}],
        intro="Отдел кадров начисляет надбавку за стаж. Стаж сотрудника `name = {name}` в месяцах пришёл из кадровой "
              "программы строкой: `months = {months}`. Оклад — `salary = {salary}` руб., а за каждый **полный** год "
              "стажа к окладу добавляют `percent = {percent}` процента оклада. В карточке сотрудника рисуют "
              "по звёздочке за каждый полный год.",
        steps=["Склей через `+` строку `Employee: ` и `name` и выведи, например `Employee: Ivan Petrov`.",
               "Преврати `months` в целое число. Посчитай полные годы стажа `years` (месяцы, делённые нацело на 12) "
               "и оставшиеся месяцы `rest` (остаток от деления на 12). С помощью f-строки выведи "
               "`Experience: <years> years <rest> months`.",
               "Сохрани в `stars` строку из `years` звёздочек — повтори строку `*` умножением — и выведи через `+` "
               "строку `Stars: ` и `stars`, например `Stars: **`.",
               "Посчитай надбавку `bonus`: `salary * years * percent / 100`. Сохрани в `total` оклад `salary` "
               "и прибавь к `total` надбавку с помощью `+=`.",
               "С помощью f-строк выведи `Bonus: <bonus> rub` и `Salary: <total> rub`. Например, для стажа "
               "`\"30\"` месяцев, оклада 47375 руб. и 3% за год программа выводит `Experience: 2 years 6 months`, "
               "`Stars: **`, `Bonus: 2842.5 rub`, `Salary: 50217.5 rub`."],
        hint="`77 // 12` даёт `6` полных лет, а `77 % 12` — `5` месяцев сверх них. `\"*\" * 3` даёт `***`. "
             "Деление `/` всегда даёт дробное число, поэтому надбавка и оклад с ней выводятся с точкой: `11520.0`.",
        solution='print("Employee: " + name)\nyears = int(months) // 12\nrest = int(months) % 12\n'
                 'print(f"Experience: {years} years {rest} months")\nstars = "*" * years\nprint("Stars: " + stars)\n'
                 'bonus = salary * years * percent / 100\ntotal = salary\ntotal += bonus\n'
                 'print(f"Bonus: {bonus} rub")\nprint(f"Salary: {total} rub")',
        wrong=[("надбавка посчитана за каждый месяц, а не за полный год",
                'print("Employee: " + name)\nyears = int(months) // 12\nrest = int(months) % 12\n'
                'print(f"Experience: {years} years {rest} months")\nstars = "*" * years\nprint("Stars: " + stars)\n'
                'bonus = salary * int(months) * percent / 100\ntotal = salary\ntotal += bonus\n'
                'print(f"Bonus: {bonus} rub")\nprint(f"Salary: {total} rub")'),
               ("оставшиеся месяцы посчитаны через // вместо остатка",
                'print("Employee: " + name)\nyears = int(months) // 12\nrest = int(months) // 12\n'
                'print(f"Experience: {years} years {rest} months")\nstars = "*" * years\nprint("Stars: " + stars)\n'
                'bonus = salary * years * percent / 100\ntotal = salary\ntotal += bonus\n'
                'print(f"Bonus: {bonus} rub")\nprint(f"Salary: {total} rub")'),
               ("надбавка затирает оклад вместо того, чтобы прибавиться к нему",
                'print("Employee: " + name)\nyears = int(months) // 12\nrest = int(months) % 12\n'
                'print(f"Experience: {years} years {rest} months")\nstars = "*" * years\nprint("Stars: " + stars)\n'
                'bonus = salary * years * percent / 100\ntotal = bonus\n'
                'print(f"Bonus: {bonus} rub")\nprint(f"Salary: {total} rub")')],
        must_use=MUST,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac11-supplier-payment", title="Оплата счёта поставщику",
        given=["supplier", "amount", "fee", "balance"],
        variants=[{"supplier": '"Paper Plus"', "amount": '"1847350"', "fee": "1.5", "balance": "5000000"}],
        hidden=[{"supplier": '"Office Lab"', "amount": '"100000"', "fee": "2.5", "balance": "300000"},
                {"supplier": '"Clean Team"', "amount": '"99"', "fee": "1.5", "balance": "1000"},
                {"supplier": '"Coffee Box"', "amount": '"523417"', "fee": "0", "balance": "1000000"},
                {"supplier": '"Print Hub"', "amount": '"2000001"', "fee": "0.75", "balance": "2015001"}],
        intro="Бухгалтер оплачивает счёт поставщика `supplier = {supplier}`. Банковская программа хранит суммы "
              "в копейках, чтобы не было дробей (1 руб. = 100 коп.), и выдала сумму счёта строкой: `amount = {amount}`. "
              "За перевод банк берёт комиссию `fee = {fee}` процента от суммы и отбрасывает доли копейки. "
              "На счёте компании `balance = {balance}` коп. — этого хватает на оплату вместе с комиссией.",
        steps=["Склей через `+` строку `Payment to ` и `supplier`, сохрани результат в `title` и выведи его. "
               "Под ним выведи строку из знаков `-` такой же длины, как `title` (длину даёт `len()`).",
               "Преврати `amount` в целое число и сохрани в `kop`. Посчитай комиссию в копейках: "
               "`commission = int(kop * fee / 100)` — `int()` отбросит доли копейки.",
               "Прибавь комиссию к `kop` с помощью `+=` — теперь это весь платёж. Вычти платёж из `balance` "
               "с помощью `-=`.",
               "С помощью f-строк выведи `Fee: <commission> kop`, `Paid: <kop // 100> rub <kop % 100> kop` и "
               "`Balance: <balance // 100> rub <balance % 100> kop`: рубли — это копейки, делённые нацело на 100, "
               "а копейки — остаток от деления на 100.",
               "Например, для счёта на `\"100000\"` коп., комиссии 2.5% и 300000 коп. на счёте программа выводит "
               "`Fee: 2500 kop`, `Paid: 1025 rub 0 kop`, `Balance: 1975 rub 0 kop`."],
        hint="`1875060 // 100` даёт `18750` рублей, а `1875060 % 100` — `60` копеек. Вычисления можно писать прямо "
             "в фигурных скобках: `f\"{{kop // 100}}\"`. `kop * fee / 100` — дробное число, а `int(27710.25)` даёт `27710`.",
        solution='title = "Payment to " + supplier\nprint(title)\nprint("-" * len(title))\nkop = int(amount)\n'
                 'commission = int(kop * fee / 100)\nkop += commission\nbalance -= kop\n'
                 'print(f"Fee: {commission} kop")\nprint(f"Paid: {kop // 100} rub {kop % 100} kop")\n'
                 'print(f"Balance: {balance // 100} rub {balance % 100} kop")',
        wrong=[("со счёта списана только сумма счёта, без комиссии",
                'title = "Payment to " + supplier\nprint(title)\nprint("-" * len(title))\nkop = int(amount)\n'
                'commission = int(kop * fee / 100)\nbalance -= kop\nkop += commission\n'
                'print(f"Fee: {commission} kop")\nprint(f"Paid: {kop // 100} rub {kop % 100} kop")\n'
                'print(f"Balance: {balance // 100} rub {balance % 100} kop")'),
               ("копейки посчитаны через // вместо остатка",
                'title = "Payment to " + supplier\nprint(title)\nprint("-" * len(title))\nkop = int(amount)\n'
                'commission = int(kop * fee / 100)\nkop += commission\nbalance -= kop\n'
                'print(f"Fee: {commission} kop")\nprint(f"Paid: {kop // 100} rub {kop // 100} kop")\n'
                'print(f"Balance: {balance // 100} rub {balance // 100} kop")'),
               ("комиссия делится на 10 вместо 100",
                'title = "Payment to " + supplier\nprint(title)\nprint("-" * len(title))\nkop = int(amount)\n'
                'commission = int(kop * fee / 10)\nkop += commission\nbalance -= kop\n'
                'print(f"Fee: {commission} kop")\nprint(f"Paid: {kop // 100} rub {kop % 100} kop")\n'
                'print(f"Balance: {balance // 100} rub {balance % 100} kop")')],
        must_use=MUST,
    ),
]
