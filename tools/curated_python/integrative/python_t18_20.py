"""Integrative tasks of the 3rd iteration, Python, topics 18–20: PY_FOR_RANGE, PY_ACCUMULATOR_PATTERN,
PY_WHILE_LOOP_BASIC. One story per family; the topic of `skill` is at the core and 1–2 earlier topics do real work:
- for + range: with elif and comparisons (greenhouse rows), with // % and and/elif (chess boards), with int(), //
  and if/else (pedometer table) — every line is computed from the loop variable, nothing is accumulated;
- accumulator: with % // and if (savings account), with // and if/comparison (mint in a greenhouse), with // % and
  if (round-robin tournament);
- while: with the accumulator and // % (walk with a speed-up), with and and if/else (deposit up to a goal), with // %
  and the accumulator (knockout tournament).
Not yet: in the for tasks — accumulating a result in a loop and while; in the accumulator tasks — while; everywhere —
break/continue, lists, string indexing, slices and methods, functions, round(), format specifiers like :.2f.
Theme domains: plants and greenhouse; deposits and savings; tournaments; step counters."""
from build import OutputTask

FOR = "PY_FOR_RANGE"
ACC = "PY_ACCUMULATOR_PATTERN"
WHILE = "PY_WHILE_LOOP_BASIC"

TASKS = [
    # ───────── 18. Цикл for и range ─────────
    OutputTask(
        skill=FOR, difficulty=3, slug="py-int-for-greenhouse-rows", title="Таблички на рядах теплицы",
        given=["rows", "per_row", "pots"],
        variants=[{"rows": "5", "per_row": "6", "pots": "20"}],
        hidden=[{"rows": "3", "per_row": "4", "pots": "12"},
                {"rows": "4", "per_row": "5", "pots": "3"},
                {"rows": "4", "per_row": "5", "pots": "10"},
                {"rows": "6", "per_row": "8", "pots": "35"},
                {"rows": "2", "per_row": "10", "pots": "0"}],
        intro="В теплице `rows = {rows}` рядов, в каждом ряду `per_row = {per_row}` мест для горшков. Привезли "
              "`pots = {pots}` горшков с рассадой, и места хватит на все. Места пронумерованы с 1 подряд по всем рядам: "
              "в первом ряду места с 1 по `per_row`, во втором — следующие `per_row` номеров, и так далее. Горшки "
              "ставят по порядку, начиная с места 1, а на каждый ряд вешают табличку.",
        steps=["Перебери циклом `for` номера рядов `row` от 1 до `rows` включительно.",
               "Для ряда посчитай номер его первого места `first = (row - 1) * per_row + 1` и последнего места "
               "`last = row * per_row`.",
               "Если `last` не больше `pots`, ряд заполнен целиком: выведи строку вида `Row 1: pots 1-6`.",
               "Иначе, если `first` не больше `pots`, ряд заполнен частично: последний горшок в нём — номер `pots`, "
               "а свободных мест `last - pots`. Выведи строку вида `Row 4: pots 19-20, 4 free`.",
               "Иначе в ряду нет ни одного горшка: выведи строку вида `Row 5: empty`. Например, для 3 рядов по 4 места "
               "и 6 горшков программа выводит `Row 1: pots 1-4`, `Row 2: pots 5-6, 2 free`, `Row 3: empty`."],
        hint="Три случая — это `if`, `elif` и `else` внутри цикла. Ряд, где последнее место ровно `pots`, заполнен "
             "целиком: «не больше» — это `<=`.",
        solution='for row in range(1, rows + 1):\n    first = (row - 1) * per_row + 1\n    last = row * per_row\n'
                 '    if last <= pots:\n        print(f"Row {row}: pots {first}-{last}")\n    elif first <= pots:\n'
                 '        print(f"Row {row}: pots {first}-{pots}, {last - pots} free")\n    else:\n'
                 '        print(f"Row {row}: empty")',
        wrong=[("строгое сравнение: ряд, заполненный ровно до последнего места, считается неполным",
                'for row in range(1, rows + 1):\n    first = (row - 1) * per_row + 1\n    last = row * per_row\n'
                '    if last < pots:\n        print(f"Row {row}: pots {first}-{last}")\n    elif first <= pots:\n'
                '        print(f"Row {row}: pots {first}-{pots}, {last - pots} free")\n    else:\n'
                '        print(f"Row {row}: empty")'),
               ("первое место без + 1: номера сдвинуты, первый ряд начинается с 0",
                'for row in range(1, rows + 1):\n    first = (row - 1) * per_row\n    last = row * per_row\n'
                '    if last <= pots:\n        print(f"Row {row}: pots {first}-{last}")\n    elif first <= pots:\n'
                '        print(f"Row {row}: pots {first}-{pots}, {last - pots} free")\n    else:\n'
                '        print(f"Row {row}: empty")'),
               ("нет ветки для пустого ряда: пустой ряд печатается как неполный",
                'for row in range(1, rows + 1):\n    first = (row - 1) * per_row + 1\n    last = row * per_row\n'
                '    if last <= pots:\n        print(f"Row {row}: pots {first}-{last}")\n    else:\n'
                '        print(f"Row {row}: pots {first}-{pots}, {last - pots} free")'),
               ("правая граница не входит в range: последний ряд без таблички",
                'for row in range(1, rows):\n    first = (row - 1) * per_row + 1\n    last = row * per_row\n'
                '    if last <= pots:\n        print(f"Row {row}: pots {first}-{last}")\n    elif first <= pots:\n'
                '        print(f"Row {row}: pots {first}-{pots}, {last - pots} free")\n    else:\n'
                '        print(f"Row {row}: empty")')],
        constructs=["for", "if"],
    ),
    OutputTask(
        skill=FOR, difficulty=3, slug="py-int-for-chess-boards", title="Рассадка на шахматном турнире",
        given=["players", "first"],
        variants=[{"players": "7", "first": "11"}],
        hidden=[{"players": "6", "first": "1"},
                {"players": "1", "first": "5"},
                {"players": "2", "first": "20"},
                {"players": "9", "first": "3"},
                {"players": "4", "first": "8"}],
        intro="На школьном шахматном турнире младшая группа из `players = {players}` игроков садится за доски, начиная "
              "с доски номер `first = {first}`. Игроков рассаживают парами по номерам: 1 и 2 — за первую доску группы, "
              "3 и 4 — за следующую, и так далее. Игрок с нечётным номером играет белыми, с чётным — чёрными. "
              "Если игроков нечётное число, последнему не хватает пары, и в этом туре он отдыхает.",
        steps=["Перебери циклом `for` номера игроков `p` от 1 до `players` включительно.",
               "Посчитай номер доски игрока: `board = first + (p - 1) // 2`.",
               "Если это последний игрок (`p == players`) и всего игроков нечётное число, выведи строку вида "
               "`Player 3: rest`.",
               "Иначе, если номер игрока нечётный, выведи строку вида `Player 1: board 4, white`, а если чётный — "
               "`Player 2: board 4, black`. Например, для 3 игроков с доски 4 программа выводит "
               "`Player 1: board 4, white`, `Player 2: board 4, black`, `Player 3: rest`."],
        hint="Чётность проверяют остатком: `p % 2 == 1` — номер нечётный. Для игроков 1 и 2 `(p - 1) // 2` даёт 0, "
             "для 3 и 4 — 1: так пара садится за одну доску. Две части условия про отдых соединяет `and`.",
        solution='for p in range(1, players + 1):\n    board = first + (p - 1) // 2\n'
                 '    if p == players and players % 2 == 1:\n        print(f"Player {p}: rest")\n'
                 '    elif p % 2 == 1:\n        print(f"Player {p}: board {board}, white")\n    else:\n'
                 '        print(f"Player {p}: board {board}, black")',
        wrong=[("нет проверки на нечётность: последний игрок отдыхает и при чётном числе игроков",
                'for p in range(1, players + 1):\n    board = first + (p - 1) // 2\n'
                '    if p == players:\n        print(f"Player {p}: rest")\n'
                '    elif p % 2 == 1:\n        print(f"Player {p}: board {board}, white")\n    else:\n'
                '        print(f"Player {p}: board {board}, black")'),
               ("нет отдыха: последний игрок без пары получает доску",
                'for p in range(1, players + 1):\n    board = first + (p - 1) // 2\n'
                '    if p % 2 == 1:\n        print(f"Player {p}: board {board}, white")\n    else:\n'
                '        print(f"Player {p}: board {board}, black")'),
               ("доска first + p // 2: игроки одной пары оказываются за разными досками",
                'for p in range(1, players + 1):\n    board = first + p // 2\n'
                '    if p == players and players % 2 == 1:\n        print(f"Player {p}: rest")\n'
                '    elif p % 2 == 1:\n        print(f"Player {p}: board {board}, white")\n    else:\n'
                '        print(f"Player {p}: board {board}, black")'),
               ("цвета перепутаны: нечётные играют чёрными",
                'for p in range(1, players + 1):\n    board = first + (p - 1) // 2\n'
                '    if p == players and players % 2 == 1:\n        print(f"Player {p}: rest")\n'
                '    elif p % 2 == 0:\n        print(f"Player {p}: board {board}, white")\n    else:\n'
                '        print(f"Player {p}: board {board}, black")')],
        constructs=["for", "if"],
    ),
    OutputTask(
        skill=FOR, difficulty=3, slug="py-int-for-pedometer-table", title="Таблица шагомера",
        given=["steps", "stride", "goal"],
        variants=[{"steps": '"5400"', "stride": "70", "goal": "4000"}],
        hidden=[{"steps": '"999"', "stride": "75", "goal": "5000"},
                {"steps": '"3000"', "stride": "60", "goal": "3000"},
                {"steps": '"7250"', "stride": "80", "goal": "10000"},
                {"steps": '"12000"', "stride": "65", "goal": "1500"},
                {"steps": '"2000"', "stride": "72", "goal": "1000"}],
        intro="Шагомер на часах Оли передаёт в приложение число шагов за день строкой: `steps = {steps}`. Длина шага "
              "Оли — `stride = {stride}` см, цель на день — `goal = {goal}` шагов. Приложение строит таблицу прогулки: "
              "на каждой полной тысяче шагов показывает, сколько метров пройдено и сколько шагов оставалось до цели.",
        steps=["Преврати `steps` в целое число и сохрани в `total`.",
               "Циклом `for` с `range` с шагом 1000 перебери отметки `mark`: 1000, 2000, 3000, … — все полные тысячи, "
               "которые не больше `total`.",
               "На каждой отметке посчитай пройденные метры: `mark * stride // 100` (в метре 100 см). Если `mark` "
               "меньше `goal`, выведи строку `<mark> steps: <meters> m, <left> to goal`, где `<meters>` — метры, "
               "а `<left>` — сколько шагов осталось до цели; иначе — строку `<mark> steps: <meters> m, goal done`.",
               "После цикла выведи итог дня — все шаги и метры за весь день — в виде `Total: <total> steps, <meters> m`. "
               "Например, для `\"6500\"` шагов, шага 75 см и цели 6000 таблица кончается строками "
               "`5000 steps: 3750 m, 1000 to goal`, `6000 steps: 4500 m, goal done`, `Total: 6500 steps, 4875 m`."],
        hint="Третье число в `range` — шаг: `range(5, 16, 5)` даёт 5, 10, 15. Правая граница не входит, поэтому, чтобы "
             "отметка, равная `total`, попала в таблицу, справа нужно поставить `total + 1`. На отметке, равной цели, "
             "цель уже выполнена.",
        solution='total = int(steps)\nfor mark in range(1000, total + 1, 1000):\n    meters = mark * stride // 100\n'
                 '    if mark < goal:\n        print(f"{mark} steps: {meters} m, {goal - mark} to goal")\n    else:\n'
                 '        print(f"{mark} steps: {meters} m, goal done")\n'
                 'print(f"Total: {total} steps, {total * stride // 100} m")',
        wrong=[("правая граница total не входит в range: ровная тысяча в конце пропущена",
                'total = int(steps)\nfor mark in range(1000, total, 1000):\n    meters = mark * stride // 100\n'
                '    if mark < goal:\n        print(f"{mark} steps: {meters} m, {goal - mark} to goal")\n    else:\n'
                '        print(f"{mark} steps: {meters} m, goal done")\n'
                'print(f"Total: {total} steps, {total * stride // 100} m")'),
               ("нестрогое сравнение: на отметке, равной цели, пишет «0 to goal»",
                'total = int(steps)\nfor mark in range(1000, total + 1, 1000):\n    meters = mark * stride // 100\n'
                '    if mark <= goal:\n        print(f"{mark} steps: {meters} m, {goal - mark} to goal")\n    else:\n'
                '        print(f"{mark} steps: {meters} m, goal done")\n'
                'print(f"Total: {total} steps, {total * stride // 100} m")'),
               ("метры не поделены на 100: выводятся сантиметры",
                'total = int(steps)\nfor mark in range(1000, total + 1, 1000):\n    meters = mark * stride\n'
                '    if mark < goal:\n        print(f"{mark} steps: {meters} m, {goal - mark} to goal")\n    else:\n'
                '        print(f"{mark} steps: {meters} m, goal done")\n'
                'print(f"Total: {total} steps, {total * stride} m")'),
               ("range начинается с 0: в таблице лишняя строка «0 steps»",
                'total = int(steps)\nfor mark in range(0, total + 1, 1000):\n    meters = mark * stride // 100\n'
                '    if mark < goal:\n        print(f"{mark} steps: {meters} m, {goal - mark} to goal")\n    else:\n'
                '        print(f"{mark} steps: {meters} m, goal done")\n'
                'print(f"Total: {total} steps, {total * stride // 100} m")')],
        constructs=["for", "if"],
    ),

    # ───────── 19. Накопление результата в цикле ─────────
    OutputTask(
        skill=ACC, difficulty=3, slug="py-int-acc-savings-account", title="Накопительный счёт",
        given=["monthly", "percent", "months"],
        variants=[{"monthly": "5000", "percent": "2", "months": "8"}],
        hidden=[{"monthly": "3000", "percent": "5", "months": "2"},
                {"monthly": "1000", "percent": "10", "months": "3"},
                {"monthly": "2000", "percent": "3", "months": "12"},
                {"monthly": "10000", "percent": "1", "months": "7"},
                {"monthly": "4000", "percent": "4", "months": "6"}],
        intro="Дима открыл накопительный счёт и в конце каждого месяца кладёт на него `monthly = {monthly}` руб. "
              "Раз в три месяца — в 3-й, 6-й, 9-й… месяц — банк сразу после взноса начисляет `percent = {percent}` % "
              "на всю сумму на счёте (копейки отбрасывает). Дима копит `months = {months}` месяцев.",
        steps=["Заведи накопитель `balance` со значением 0 — сколько денег на счёте.",
               "Циклом `for` перебери номера месяцев `month` от 1 до `months` включительно; каждый месяц прибавляй "
               "к `balance` взнос `monthly`.",
               "Если номер месяца делится на 3 без остатка, после взноса посчитай проценты "
               "`bonus = balance * percent // 100`, прибавь их к `balance` и выведи строку вида "
               "`Month 3: +150 rub, balance 3150 rub`.",
               "После цикла выведи `Balance: <balance> rub` и сколько из этой суммы дали проценты — всё, что на счёте, "
               "минус все взносы (`monthly * months`), — в виде `Interest: <…> rub`. Например, для взносов по 1000 руб. "
               "под 5 % за 4 месяца программа выводит `Month 3: +150 rub, balance 3150 rub`, `Balance: 4150 rub`, "
               "`Interest: 150 rub`."],
        hint="Месяц с номером `month` делится на 3 без остатка, когда `month % 3 == 0`. Проценты считают от всего "
             "`balance` после взноса, а не от одного взноса.",
        solution='balance = 0\nfor month in range(1, months + 1):\n    balance += monthly\n    if month % 3 == 0:\n'
                 '        bonus = balance * percent // 100\n        balance += bonus\n'
                 '        print(f"Month {month}: +{bonus} rub, balance {balance} rub")\n'
                 'print(f"Balance: {balance} rub")\nprint(f"Interest: {balance - monthly * months} rub")',
        wrong=[("проценты считаются от одного взноса monthly, а не от всего счёта",
                'balance = 0\nfor month in range(1, months + 1):\n    balance += monthly\n    if month % 3 == 0:\n'
                '        bonus = monthly * percent // 100\n        balance += bonus\n'
                '        print(f"Month {month}: +{bonus} rub, balance {balance} rub")\n'
                'print(f"Balance: {balance} rub")\nprint(f"Interest: {balance - monthly * months} rub")'),
               ("проценты начислены до взноса этого месяца",
                'balance = 0\nfor month in range(1, months + 1):\n    if month % 3 == 0:\n'
                '        bonus = balance * percent // 100\n        balance += bonus\n'
                '        print(f"Month {month}: +{bonus} rub, balance {balance} rub")\n    balance += monthly\n'
                'print(f"Balance: {balance} rub")\nprint(f"Interest: {balance - monthly * months} rub")'),
               ("проценты не прибавлены к счёту",
                'balance = 0\nfor month in range(1, months + 1):\n    balance += monthly\n    if month % 3 == 0:\n'
                '        bonus = balance * percent // 100\n'
                '        print(f"Month {month}: +{bonus} rub, balance {balance} rub")\n'
                'print(f"Balance: {balance} rub")\nprint(f"Interest: {balance - monthly * months} rub")'),
               ("правая граница не входит в range: последний месяц не учтён",
                'balance = 0\nfor month in range(1, months):\n    balance += monthly\n    if month % 3 == 0:\n'
                '        bonus = balance * percent // 100\n        balance += bonus\n'
                '        print(f"Month {month}: +{bonus} rub, balance {balance} rub")\n'
                'print(f"Balance: {balance} rub")\nprint(f"Interest: {balance - monthly * months} rub")')],
        constructs=["for", "if"],
    ),
    OutputTask(
        skill=ACC, difficulty=3, slug="py-int-acc-greenhouse-mint", title="Мята в теплице",
        given=["height", "grow", "max_h", "days"],
        variants=[{"height": "8", "grow": "3", "max_h": "20", "days": "10"}],
        hidden=[{"height": "5", "grow": "2", "max_h": "30", "days": "5"},
                {"height": "10", "grow": "5", "max_h": "15", "days": "4"},
                {"height": "1", "grow": "10", "max_h": "12", "days": "6"},
                {"height": "20", "grow": "1", "max_h": "20", "days": "3"},
                {"height": "6", "grow": "4", "max_h": "25", "days": "9"}],
        intro="В теплице растёт мята высотой `height = {height}` см. Каждый день она подрастает на `grow = {grow}` см. "
              "Как только после очередного дня мята достигает `max_h = {max_h}` см или выше, садовник срезает её "
              "наполовину (сантиметры округляются вниз, как при делении нацело). Посмотрим, что будет за "
              "`days = {days}` дней.",
        steps=["Заведи счётчик срезов `cuts` со значением 0.",
               "Циклом `for` перебери дни `day` от 1 до `days` включительно; каждый день прибавляй к `height` "
               "прирост `grow`.",
               "Если после этого `height` не меньше `max_h`, выведи строку с высотой до среза и после — например, "
               "если на 3-й день мята выросла до 21 см: `Day 3: 21 cm, cut to 10 cm`, — затем срежь мяту: "
               "`height = height // 2` — и увеличь `cuts` на 1.",
               "После цикла выведи `Height: <height> cm` и `Cuts: <cuts>`. Например, если мята срезана один раз и "
               "сейчас её высота 13 см: `Height: 13 cm`, `Cuts: 1`."],
        hint="`height` здесь тоже накопитель: каждый день к нему прибавляют прирост. Мята ровно в `max_h` см уже "
             "срезается: «не меньше» — это `>=`. `21 // 2` даёт `10`.",
        solution='cuts = 0\nfor day in range(1, days + 1):\n    height += grow\n    if height >= max_h:\n'
                 '        print(f"Day {day}: {height} cm, cut to {height // 2} cm")\n        height = height // 2\n'
                 '        cuts += 1\nprint(f"Height: {height} cm")\nprint(f"Cuts: {cuts}")',
        wrong=[("строгое сравнение: мяту ровно в max_h см не срезают",
                'cuts = 0\nfor day in range(1, days + 1):\n    height += grow\n    if height > max_h:\n'
                '        print(f"Day {day}: {height} cm, cut to {height // 2} cm")\n        height = height // 2\n'
                '        cuts += 1\nprint(f"Height: {height} cm")\nprint(f"Cuts: {cuts}")'),
               ("срезает до половины max_h, а не до половины своей высоты",
                'cuts = 0\nfor day in range(1, days + 1):\n    height += grow\n    if height >= max_h:\n'
                '        print(f"Day {day}: {height} cm, cut to {max_h // 2} cm")\n        height = max_h // 2\n'
                '        cuts += 1\nprint(f"Height: {height} cm")\nprint(f"Cuts: {cuts}")'),
               ("счётчик срезов не накапливается: cuts = 1",
                'cuts = 0\nfor day in range(1, days + 1):\n    height += grow\n    if height >= max_h:\n'
                '        print(f"Day {day}: {height} cm, cut to {height // 2} cm")\n        height = height // 2\n'
                '        cuts = 1\nprint(f"Height: {height} cm")\nprint(f"Cuts: {cuts}")'),
               ("проверка до прироста: мята, доросшая до max_h, срезается только на следующий день",
                'cuts = 0\nfor day in range(1, days + 1):\n    if height >= max_h:\n'
                '        print(f"Day {day}: {height} cm, cut to {height // 2} cm")\n        height = height // 2\n'
                '        cuts += 1\n    height += grow\nprint(f"Height: {height} cm")\nprint(f"Cuts: {cuts}")')],
        constructs=["for", "if"],
    ),
    OutputTask(
        skill=ACC, difficulty=3, slug="py-int-acc-round-robin", title="Круговой турнир по настольному теннису",
        given=["players", "per_day"],
        variants=[{"players": "6", "per_day": "4"}],
        hidden=[{"players": "2", "per_day": "3"},
                {"players": "5", "per_day": "5"},
                {"players": "8", "per_day": "6"},
                {"players": "4", "per_day": "6"},
                {"players": "3", "per_day": "2"}],
        intro="В клубе настольного тенниса проходит круговой турнир: каждый из `players = {players}` игроков "
              "встречается с каждым другим ровно один раз. Судья считает матчи так: игроки «приходят» по номерам, "
              "и игрок с номером `p` добавляет `p - 1` матчей — с каждым, кто пришёл раньше него. За день на столах "
              "клуба успевают сыграть `per_day = {per_day}` матчей.",
        steps=["Заведи накопитель `matches` со значением 0.",
               "Циклом `for` перебери номера игроков `p` от 1 до `players` включительно: прибавляй к `matches` число "
               "`p - 1` и выводи строку вида `Player 3 joins, matches: 3`.",
               "После цикла посчитай число дней турнира `days`: `matches`, делённое нацело на `per_day`. Если остаток "
               "от этого деления не 0, оставшимся матчам нужен ещё один день — прибавь его к `days` с помощью `+=`.",
               "Выведи `Days: <days>`. Например, для 4 игроков и 4 матчей в день программа выводит "
               "`Player 1 joins, matches: 0`, `Player 2 joins, matches: 1`, `Player 3 joins, matches: 3`, "
               "`Player 4 joins, matches: 6`, `Days: 2`."],
        hint="Первый игрок пока ни с кем не играет: `p - 1` для него 0. `15 // 4` — это 3 полных дня, а `15 % 4` — "
             "ещё 3 матча, которым нужен четвёртый день.",
        solution='matches = 0\nfor p in range(1, players + 1):\n    matches += p - 1\n'
                 '    print(f"Player {p} joins, matches: {matches}")\ndays = matches // per_day\n'
                 'if matches % per_day != 0:\n    days += 1\nprint(f"Days: {days}")',
        wrong=[("прибавляет p вместо p - 1: каждый будто играет и сам с собой",
                'matches = 0\nfor p in range(1, players + 1):\n    matches += p\n'
                '    print(f"Player {p} joins, matches: {matches}")\ndays = matches // per_day\n'
                'if matches % per_day != 0:\n    days += 1\nprint(f"Days: {days}")'),
               ("забыт неполный последний день",
                'matches = 0\nfor p in range(1, players + 1):\n    matches += p - 1\n'
                '    print(f"Player {p} joins, matches: {matches}")\ndays = matches // per_day\n'
                'print(f"Days: {days}")'),
               ("перезаписывает matches вместо накопления",
                'matches = 0\nfor p in range(1, players + 1):\n    matches = p - 1\n'
                '    print(f"Player {p} joins, matches: {matches}")\ndays = matches // per_day\n'
                'if matches % per_day != 0:\n    days += 1\nprint(f"Days: {days}")'),
               ("лишний день добавляется всегда, даже когда матчи делятся на дни поровну",
                'matches = 0\nfor p in range(1, players + 1):\n    matches += p - 1\n'
                '    print(f"Player {p} joins, matches: {matches}")\ndays = matches // per_day\n'
                'days += 1\nprint(f"Days: {days}")')],
        constructs=["for", "if"],
    ),

    # ───────── 20. Цикл while ─────────
    OutputTask(
        skill=WHILE, difficulty=3, slug="py-int-while-speed-walk", title="Ходьба с разгоном",
        given=["pace", "add", "goal"],
        variants=[{"pace": "90", "add": "10", "goal": "6000"}],
        hidden=[{"pace": "100", "add": "0", "goal": "3000"},
                {"pace": "120", "add": "20", "goal": "500"},
                {"pace": "60", "add": "5", "goal": "9000"},
                {"pace": "80", "add": "10", "goal": "3801"},
                {"pace": "100", "add": "25", "goal": "14500"}],
        intro="Лена тренируется ходьбой со шагомером. Первые 10 минут она идёт в темпе `pace = {pace}` шагов в минуту, "
              "а каждые следующие 10 минут ускоряется ещё на `add = {add}` шагов в минуту. Шагомер подводит итог "
              "раз в 10 минут, и тренировка заканчивается на том итоге, где шагов стало `goal = {goal}` или больше.",
        steps=["Заведи два накопителя со значением 0: `total` — сколько шагов пройдено, и `minutes` — сколько минут "
               "идёт тренировка.",
               "Пока `total` меньше `goal`, повторяй в цикле `while`: прибавь к `total` шаги за 10 минут в нынешнем "
               "темпе (`pace * 10`), прибавь к `minutes` 10 и выведи строку вида `<minutes> min: <total> steps`.",
               "Последним действием в цикле ускорься: увеличь `pace` на `add`.",
               "После цикла выведи время тренировки в часах и минутах: часы — это `minutes`, делённое нацело на 60, "
               "минуты — остаток от деления на 60. Например, при темпе 100 и ускорении на 10 шагов в минуту для цели "
               "2000 шагов программа выводит `10 min: 1000 steps`, `20 min: 2100 steps`, `Time: 0 h 20 min`."],
        hint="Если шагов стало ровно `goal`, цель уже выполнена и цикл должен остановиться: условие продолжения — "
             "`total < goal`. Шаги считают в старом темпе, а ускоряются только после этого.",
        solution='total = 0\nminutes = 0\nwhile total < goal:\n    total += pace * 10\n    minutes += 10\n'
                 '    print(f"{minutes} min: {total} steps")\n    pace += add\n'
                 'print(f"Time: {minutes // 60} h {minutes % 60} min")',
        wrong=[("нестрогое сравнение: при ровно goal шагах тренировка идёт ещё 10 минут",
                'total = 0\nminutes = 0\nwhile total <= goal:\n    total += pace * 10\n    minutes += 10\n'
                '    print(f"{minutes} min: {total} steps")\n    pace += add\n'
                'print(f"Time: {minutes // 60} h {minutes % 60} min")'),
               ("ускоряется до того, как посчитать шаги",
                'total = 0\nminutes = 0\nwhile total < goal:\n    pace += add\n    total += pace * 10\n'
                '    minutes += 10\n    print(f"{minutes} min: {total} steps")\n'
                'print(f"Time: {minutes // 60} h {minutes % 60} min")'),
               ("часы посчитаны через / — получается дробь",
                'total = 0\nminutes = 0\nwhile total < goal:\n    total += pace * 10\n    minutes += 10\n'
                '    print(f"{minutes} min: {total} steps")\n    pace += add\n'
                'print(f"Time: {minutes / 60} h {minutes % 60} min")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=WHILE, difficulty=3, slug="py-int-while-deposit-goal", title="Вклад до цели",
        given=["balance", "percent", "goal", "limit"],
        variants=[{"balance": "50000", "percent": "8", "goal": "70000", "limit": "6"}],
        hidden=[{"balance": "1000", "percent": "10", "goal": "1210", "limit": "5"},
                {"balance": "20000", "percent": "5", "goal": "30000", "limit": "3"},
                {"balance": "10000", "percent": "10", "goal": "13310", "limit": "3"},
                {"balance": "80000", "percent": "7", "goal": "50000", "limit": "4"},
                {"balance": "3000", "percent": "20", "goal": "9000", "limit": "4"}],
        intro="Света положила на вклад `balance = {balance}` руб. под `percent = {percent}` % годовых: в конце каждого "
              "года банк прибавляет к вкладу проценты от суммы на нём (копейки отбрасывает). Света копит до цели "
              "`goal = {goal}` руб., но вклад открыт не больше чем на `limit = {limit}` лет.",
        steps=["Заведи счётчик лет `years` со значением 0.",
               "Пока на вкладе меньше `goal` **и** прошло меньше `limit` лет, повторяй в цикле `while`: увеличь `years` "
               "на 1, прибавь к `balance` проценты за год — `balance * percent // 100` — и выведи строку вида "
               "`Year <years>: <balance> rub`.",
               "После цикла проверь, накоплено ли не меньше `goal`: если да, выведи строку вида "
               "`Goal reached, years: 3`, иначе — сколько не хватило до цели, в виде `Short by 6848 rub`. Например, "
               "для 20000 руб. под 5 % с целью 30000 руб. на 3 года программа выводит `Year 1: 21000 rub`, "
               "`Year 2: 22050 rub`, `Year 3: 23152 rub`, `Short by 6848 rub`."],
        hint="Оба условия продолжения соединяет `and`: цикл останавливается, как только одно из них нарушится. "
             "Цель может быть достигнута ровно в последний год вклада — поэтому после цикла проверяй сумму, "
             "а не число лет. Если денег сразу хватает, цикл не выполнится ни разу.",
        solution='years = 0\nwhile balance < goal and years < limit:\n    years += 1\n'
                 '    balance += balance * percent // 100\n    print(f"Year {years}: {balance} rub")\n'
                 'if balance >= goal:\n    print(f"Goal reached, years: {years}")\nelse:\n'
                 '    print(f"Short by {goal - balance} rub")',
        wrong=[("нестрогое сравнение: при сумме ровно goal вклад копит ещё год",
                'years = 0\nwhile balance <= goal and years < limit:\n    years += 1\n'
                '    balance += balance * percent // 100\n    print(f"Year {years}: {balance} rub")\n'
                'if balance >= goal:\n    print(f"Goal reached, years: {years}")\nelse:\n'
                '    print(f"Short by {goal - balance} rub")'),
               ("после цикла проверяет годы, а не сумму: цель в последний год вклада не засчитана",
                'years = 0\nwhile balance < goal and years < limit:\n    years += 1\n'
                '    balance += balance * percent // 100\n    print(f"Year {years}: {balance} rub")\n'
                'if years < limit:\n    print(f"Goal reached, years: {years}")\nelse:\n'
                '    print(f"Short by {goal - balance} rub")'),
               ("забыт срок вклада: копит, пока не достигнет цели",
                'years = 0\nwhile balance < goal:\n    years += 1\n'
                '    balance += balance * percent // 100\n    print(f"Year {years}: {balance} rub")\n'
                'if balance >= goal:\n    print(f"Goal reached, years: {years}")\nelse:\n'
                '    print(f"Short by {goal - balance} rub")')],
        constructs=["while", "if"],
    ),
    OutputTask(
        skill=WHILE, difficulty=3, slug="py-int-while-knockout", title="Турнир на выбывание",
        given=["teams"],
        variants=[{"teams": "12"}],
        hidden=[{"teams": "1"}, {"teams": "2"}, {"teams": "5"}, {"teams": "16"}, {"teams": "7"}],
        intro="Турнир по мини-футболу идёт по олимпийской системе, заявились `teams = {teams}` команд. В каждом круге "
              "команды разбиваются на пары, каждая пара играет один матч, проигравший выбывает. Если команд нечётное "
              "число, одной команде не хватает пары — она проходит в следующий круг без игры. Круги идут, пока не "
              "останется одна команда — чемпион.",
        steps=["Заведи два накопителя со значением 0: `rounds` — сколько сыграно кругов, и `total` — сколько всего "
               "сыграно матчей.",
               "Пока команд больше одной, повторяй в цикле `while`: посчитай матчи круга `games` — это `teams`, "
               "делённое нацело на 2. В следующий круг выходят победители матчей и команда без пары, если она была: "
               "новое `teams` — это `games` плюс остаток от деления старого `teams` на 2.",
               "В том же цикле увеличь `rounds` на 1, прибавь `games` к `total` и выведи строку вида "
               "`Round 1: games 3, teams left 4` — уже с новым числом команд.",
               "После цикла выведи `Rounds: <rounds>` и `Games: <total>`. Например, для 7 команд: "
               "`Round 1: games 3, teams left 4`, `Round 2: games 2, teams left 2`, `Round 3: games 1, teams left 1`, "
               "`Rounds: 3`, `Games: 6`."],
        hint="`teams % 2` равно 1, когда команд нечётное число, и 0 — когда чётное. Посчитай `games` раньше, чем "
             "меняешь `teams`. Если команда всего одна, цикл не выполнится ни разу.",
        solution='rounds = 0\ntotal = 0\nwhile teams > 1:\n    games = teams // 2\n    teams = games + teams % 2\n'
                 '    rounds += 1\n    total += games\n    print(f"Round {rounds}: games {games}, teams left {teams}")\n'
                 'print(f"Rounds: {rounds}")\nprint(f"Games: {total}")',
        wrong=[("команда без пары пропадает: teams = teams // 2",
                'rounds = 0\ntotal = 0\nwhile teams > 1:\n    games = teams // 2\n    teams = teams // 2\n'
                '    rounds += 1\n    total += games\n    print(f"Round {rounds}: games {games}, teams left {teams}")\n'
                'print(f"Rounds: {rounds}")\nprint(f"Games: {total}")'),
               ("печатает число команд до круга, а не после",
                'rounds = 0\ntotal = 0\nwhile teams > 1:\n    games = teams // 2\n    rounds += 1\n    total += games\n'
                '    print(f"Round {rounds}: games {games}, teams left {teams}")\n    teams = games + teams % 2\n'
                'print(f"Rounds: {rounds}")\nprint(f"Games: {total}")'),
               ("матчи не накапливаются: Games показывает только последний круг",
                'rounds = 0\ntotal = 0\nwhile teams > 1:\n    games = teams // 2\n    teams = games + teams % 2\n'
                '    rounds += 1\n    total = games\n    print(f"Round {rounds}: games {games}, teams left {teams}")\n'
                'print(f"Rounds: {rounds}")\nprint(f"Games: {total}")')],
        constructs=["while"],
    ),
]
