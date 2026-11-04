"""PY_WHILE_LOOP_BASIC — «Цикл while». Taught before: print, variables, assignment, arithmetic, int/float, strings,
type conversion, // and %, += -=, f-strings, if/else, comparisons, and/or/not, elif, truthiness, for + range,
accumulator. Here: a while loop that repeats while a condition holds, when the number of steps is not known in advance.
Not yet: break/continue, lists, string slicing and methods, functions."""
from build import OutputTask

SKILL = "PY_WHILE_LOOP_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-wh-printer", title="Бумага в принтере",
        given=["sheets", "per_job"],
        variants=[{"sheets": "20", "per_job": "6"}, {"sheets": "30", "per_job": "10"}, {"sheets": "17", "per_job": "5"}],
        hidden=[{"sheets": "3", "per_job": "5"}, {"sheets": "12", "per_job": "4"}, {"sheets": "25", "per_job": "7"}],
        intro="В лотке принтера `sheets = {sheets}` листов. Каждое задание печатается на `per_job = {per_job}` листах. "
              "Принтер берёт задания одно за другим, пока для очередного задания хватает бумаги.",
        steps=["Заведи счётчик заданий `job` со значением 1.",
               "Напиши цикл `while`, который повторяется, пока листов `sheets` хватает на целое задание.",
               "В цикле отними от `sheets` листы задания, выведи строку вида `Job 1: 14 sheets left` "
               "и увеличь `job` на 1.",
               "После цикла выведи `Add paper`"],
        hint="Если листов ровно столько, сколько нужно на задание, его ещё можно напечатать: условие — "
             "«листов больше или равно `per_job`». Цикл `while` проверяет условие перед каждым повтором.",
        solution='job = 1\nwhile sheets >= per_job:\n    sheets -= per_job\n'
                 '    print(f"Job {job}: {sheets} sheets left")\n    job += 1\nprint("Add paper")',
        wrong=[("строгое сравнение: когда листов ровно на одно задание, оно не печатается",
                'job = 1\nwhile sheets > per_job:\n    sheets -= per_job\n'
                '    print(f"Job {job}: {sheets} sheets left")\n    job += 1\nprint("Add paper")'),
               ("счётчик заданий начинается с 0",
                'job = 0\nwhile sheets >= per_job:\n    sheets -= per_job\n'
                '    print(f"Job {job}: {sheets} sheets left")\n    job += 1\nprint("Add paper")'),
               ("печатает остаток до того, как отнять листы",
                'job = 1\nwhile sheets >= per_job:\n    print(f"Job {job}: {sheets} sheets left")\n'
                '    sheets -= per_job\n    job += 1\nprint("Add paper")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-wh-rumor", title="Новость разлетается",
        given=["people", "town"],
        variants=[{"people": "3", "town": "50"}, {"people": "1", "town": "16"}, {"people": "5", "town": "100"}],
        hidden=[{"people": "10", "town": "5"}, {"people": "2", "town": "64"}, {"people": "7", "town": "30"}],
        intro="В первый день новость знают `people = {people}` человек, а каждый следующий день число знающих удваивается. "
              "В посёлке живут `town = {town}` человек. Узнаем, в какой день новость узнают все.",
        steps=["Заведи переменную `day` со значением 1.",
               "Пока знающих меньше, чем жителей посёлка, повторяй в цикле `while`: удвой `people`, увеличь `day` на 1 "
               "и выведи строку вида `Day 2: 6 people`",
               "После цикла выведи `Everyone knows on day 6`"],
        hint="Цикл должен остановиться, как только `people` стало не меньше `town`: условие продолжения — `people < town`. "
             "Если знающих сразу хватает, цикл не выполнится ни разу.",
        solution='day = 1\nwhile people < town:\n    people = people * 2\n    day += 1\n'
                 '    print(f"Day {day}: {people} people")\nprint(f"Everyone knows on day {day}")',
        wrong=[("нестрогое сравнение: когда знающих ровно столько, сколько жителей, цикл делает лишний день",
                'day = 1\nwhile people <= town:\n    people = people * 2\n    day += 1\n'
                '    print(f"Day {day}: {people} people")\nprint(f"Everyone knows on day {day}")'),
               ("прибавляет 2 вместо удвоения",
                'day = 1\nwhile people < town:\n    people = people + 2\n    day += 1\n'
                '    print(f"Day {day}: {people} people")\nprint(f"Everyone knows on day {day}")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-wh-bike", title="Копим на велосипед",
        given=["saved", "monthly", "price"],
        variants=[{"saved": "1500", "monthly": "2000", "price": "9000"},
                  {"saved": "0", "monthly": "3000", "price": "12000"},
                  {"saved": "2000", "monthly": "1500", "price": "6500"}],
        hidden=[{"saved": "10000", "monthly": "1000", "price": "8000"},
                {"saved": "500", "monthly": "700", "price": "4000"},
                {"saved": "0", "monthly": "2500", "price": "10000"}],
        intro="Гоша копит на велосипед за `price = {price}` рублей. Сейчас у него `saved = {saved}` рублей, "
              "и каждый месяц он откладывает ещё `monthly = {monthly}` рублей.",
        steps=["Заведи счётчик месяцев `months` со значением 0.",
               "Пока накоплено меньше цены велосипеда, повторяй в цикле `while`: прибавь к `saved` месячный взнос "
               "и увеличь `months` на 1.",
               "После цикла выведи три строки: `Months: 4`, `Saved: 9500 rub` и сдачу после покупки — "
               "накопленное минус цена — в виде `Change: 500 rub`"],
        hint="Если денег уже хватает, копить не нужно: цикл не выполнится ни разу, и `months` останется 0. "
             "Когда накоплено ровно столько, сколько стоит велосипед, денег уже хватает.",
        solution='months = 0\nwhile saved < price:\n    saved += monthly\n    months += 1\n'
                 'print(f"Months: {months}")\nprint(f"Saved: {saved} rub")\nprint(f"Change: {saved - price} rub")',
        wrong=[("нестрогое сравнение: при точно накопленной сумме копит ещё месяц",
                'months = 0\nwhile saved <= price:\n    saved += monthly\n    months += 1\n'
                'print(f"Months: {months}")\nprint(f"Saved: {saved} rub")\nprint(f"Change: {saved - price} rub")'),
               ("вычитает в обратном порядке: сдача получается отрицательной",
                'months = 0\nwhile saved < price:\n    saved += monthly\n    months += 1\n'
                'print(f"Months: {months}")\nprint(f"Saved: {saved} rub")\nprint(f"Change: {price - saved} rub")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-wh-bounce", title="Прыгающий мяч",
        given=["height", "min_h"],
        variants=[{"height": "200", "min_h": "20"}, {"height": "160", "min_h": "10"}, {"height": "90", "min_h": "5"}],
        hidden=[{"height": "30", "min_h": "20"}, {"height": "1000", "min_h": "100"}, {"height": "64", "min_h": "8"}],
        intro="Мяч уронили с высоты `height = {height}` см. После каждого удара о пол он подпрыгивает на половину "
              "предыдущей высоты (сантиметры округляются вниз, как при делении нацело). Отскок заметен, "
              "пока его высота не меньше `min_h = {min_h}` см.",
        steps=["Заведи счётчик отскоков `bounces` со значением 0 и переменную `h` — высоту первого отскока: "
               "`height`, делённая нацело на 2.",
               "Пока отскок заметен, повторяй в цикле `while`: увеличь `bounces` на 1, выведи строку вида "
               "`Bounce 1: 100 cm` и посчитай высоту следующего отскока — `h`, делённая нацело на 2.",
               "После цикла выведи `Bounces: 3`"],
        hint="Сам бросок с высоты `height` — ещё не отскок: первый отскок имеет высоту `height // 2`. "
             "Отскок ровно в `min_h` см тоже заметен.",
        solution='bounces = 0\nh = height // 2\nwhile h >= min_h:\n    bounces += 1\n'
                 '    print(f"Bounce {bounces}: {h} cm")\n    h = h // 2\nprint(f"Bounces: {bounces}")',
        wrong=[("считает отскоком сам бросок с высоты height",
                'bounces = 0\nh = height\nwhile h >= min_h:\n    bounces += 1\n'
                '    print(f"Bounce {bounces}: {h} cm")\n    h = h // 2\nprint(f"Bounces: {bounces}")'),
               ("строгое сравнение: отскок ровно в min_h см не засчитан",
                'bounces = 0\nh = height // 2\nwhile h > min_h:\n    bounces += 1\n'
                '    print(f"Bounce {bounces}: {h} cm")\n    h = h // 2\nprint(f"Bounces: {bounces}")'),
               ("делит через /: высоты становятся дробными",
                'bounces = 0\nh = height // 2\nwhile h >= min_h:\n    bounces += 1\n'
                '    print(f"Bounce {bounces}: {h} cm")\n    h = h / 2\nprint(f"Bounces: {bounces}")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-wh-digits", title="Контрольная сумма посылки",
        given=["number"],
        variants=[{"number": "4825"}, {"number": "90317"}, {"number": "777"}],
        hidden=[{"number": "5"}, {"number": "1000"}, {"number": "123456"}],
        intro="На почте у каждой посылки есть номер `number = {number}`. Для проверки сотрудник считает, сколько в номере "
              "цифр и чему равна их сумма. Сделай это программой, не превращая число в строку.",
        steps=["Заведи два накопителя со значением 0: `total` — сумма цифр, и `count` — количество цифр.",
               "Пока `number` больше 0, повторяй в цикле `while`: прибавь к `total` последнюю цифру числа "
               "(остаток от деления на 10), отбрось эту цифру делением нацело на 10 и увеличь `count` на 1.",
               "После цикла выведи `Digits: 4` и следующей строкой `Sum: 19`"],
        hint="`4825 % 10` даёт последнюю цифру 5, а `4825 // 10` даёт 482 — число без последней цифры. "
             "Когда цифры кончатся, число станет 0, и цикл остановится.",
        solution='total = 0\ncount = 0\nwhile number > 0:\n    total += number % 10\n    number = number // 10\n'
                 '    count += 1\nprint(f"Digits: {count}")\nprint(f"Sum: {total}")',
        wrong=[("прибавляет число без последней цифры вместо самой цифры",
                'total = 0\ncount = 0\nwhile number > 0:\n    total += number // 10\n    number = number // 10\n'
                '    count += 1\nprint(f"Digits: {count}")\nprint(f"Sum: {total}")'),
               ("условие number > 9: первая цифра числа не учитывается",
                'total = 0\ncount = 0\nwhile number > 9:\n    total += number % 10\n    number = number // 10\n'
                '    count += 1\nprint(f"Digits: {count}")\nprint(f"Sum: {total}")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-wh-loan", title="Возвращаем долг",
        given=["debt", "pay", "percent"],
        variants=[{"debt": "10000", "pay": "3000", "percent": "10"},
                  {"debt": "5000", "pay": "2100", "percent": "5"},
                  {"debt": "8000", "pay": "2500", "percent": "2"}],
        hidden=[{"debt": "2000", "pay": "2200", "percent": "10"},
                {"debt": "3000", "pay": "1000", "percent": "0"},
                {"debt": "500", "pay": "1000", "percent": "20"}],
        intro="Тимур взял в долг `debt = {debt}` рублей. В начале каждого месяца к долгу добавляются `percent = {percent}` % "
              "(копейки отбрасываются), а потом Тимур платит `pay = {pay}` рублей. Если долг уже не больше платежа, "
              "Тимур закрывает его последним платежом.",
        steps=["Заведи счётчик месяцев `month` со значением 0.",
               "Пока `debt` больше 0, повторяй в цикле `while`: увеличь `month` на 1 и прибавь к долгу проценты "
               "`debt * percent // 100`.",
               "Если теперь долг не больше `pay`, выведи строку вида `Month 5: last payment 789 rub` и обнули `debt`.",
               "Иначе отними от долга `pay` и выведи строку вида `Month 1: 8000 rub left`",
               "После цикла выведи строку вида `Paid off in 5 months`"],
        hint="Сначала проценты, потом платёж. Долг ровно в `pay` рублей закрывается последним платежом: "
             "«не больше» — это `<=`. Когда `debt` станет 0, цикл остановится.",
        solution='month = 0\nwhile debt > 0:\n    month += 1\n    debt += debt * percent // 100\n'
                 '    if debt <= pay:\n        print(f"Month {month}: last payment {debt} rub")\n        debt = 0\n'
                 '    else:\n        debt -= pay\n        print(f"Month {month}: {debt} rub left")\n'
                 'print(f"Paid off in {month} months")',
        wrong=[("строгое сравнение: долг ровно в pay рублей не считается последним платежом",
                'month = 0\nwhile debt > 0:\n    month += 1\n    debt += debt * percent // 100\n'
                '    if debt < pay:\n        print(f"Month {month}: last payment {debt} rub")\n        debt = 0\n'
                '    else:\n        debt -= pay\n        print(f"Month {month}: {debt} rub left")\n'
                'print(f"Paid off in {month} months")'),
               ("заменяет долг процентами вместо того, чтобы прибавить их",
                'month = 0\nwhile debt > 0:\n    month += 1\n    debt = debt * percent // 100\n'
                '    if debt <= pay:\n        print(f"Month {month}: last payment {debt} rub")\n        debt = 0\n'
                '    else:\n        debt -= pay\n        print(f"Month {month}: {debt} rub left")\n'
                'print(f"Paid off in {month} months")')],
        constructs=["while", "if"],
    ),
]
