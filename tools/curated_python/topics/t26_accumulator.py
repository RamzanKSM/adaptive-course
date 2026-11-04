"""PY_ACCUMULATOR_PATTERN — «Накопление результата в цикле». Taught before: print, variables, assignment, arithmetic,
int/float, strings, type conversion, // and %, += -=, f-strings, if/else, comparisons, and/or/not, elif, truthiness,
for + range. Here: a sum, a counter or a product started before the loop and updated on every step.
Not yet: while, break/continue, lists, string slicing and methods, functions."""
from build import OutputTask

SKILL = "PY_ACCUMULATOR_PATTERN"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-acc-piggy-bank", title="Копилка",
        given=["start", "weekly", "weeks"],
        variants=[{"start": "200", "weekly": "100", "weeks": "3"}, {"start": "150", "weekly": "50", "weeks": "4"},
                  {"start": "80", "weekly": "40", "weeks": "5"}],
        hidden=[{"start": "0", "weekly": "30", "weeks": "2"}, {"start": "500", "weekly": "25", "weeks": "6"},
                {"start": "10", "weekly": "10", "weeks": "1"}],
        intro="В копилке у Ани уже лежит `start = {start}` рублей. Каждую неделю она добавляет туда `weekly = {weekly}` "
              "рублей, и так `weeks = {weeks}` недель подряд.",
        steps=["Заведи переменную `total` и положи в неё сумму, которая уже лежит в копилке, — `start`.",
               "Напиши цикл `for` с `range`, который перебирает номера недель от 1 до `weeks` включительно.",
               "На каждом шаге прибавь к `total` недельный взнос через `+=` и выведи строку вида `Week 1: 300 rub` — "
               "номер недели и сумму в копилке после взноса.",
               "После цикла выведи итог в виде `Total: 500 rub`"],
        hint="Переменную-накопитель заводят до цикла, а внутри цикла только увеличивают. "
             "Копилка не пустая: начальное значение `total` — это `start`, а не 0.",
        solution='total = start\nfor week in range(1, weeks + 1):\n    total += weekly\n'
                 '    print(f"Week {week}: {total} rub")\nprint(f"Total: {total} rub")',
        wrong=[("считает с пустой копилки: забыта начальная сумма start",
                'total = 0\nfor week in range(1, weeks + 1):\n    total += weekly\n'
                '    print(f"Week {week}: {total} rub")\nprint(f"Total: {total} rub")'),
               ("правая граница не входит в range: последняя неделя пропущена",
                'total = start\nfor week in range(1, weeks):\n    total += weekly\n'
                '    print(f"Week {week}: {total} rub")\nprint(f"Total: {total} rub")'),
               ("печатает сумму до взноса, а не после",
                'total = start\nfor week in range(1, weeks + 1):\n    print(f"Week {week}: {total} rub")\n'
                '    total += weekly\nprint(f"Total: {total} rub")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-acc-game-levels", title="Очки за уровни",
        given=["levels", "bonus"],
        variants=[{"levels": "5", "bonus": "10"}, {"levels": "4", "bonus": "25"}, {"levels": "6", "bonus": "5"}],
        hidden=[{"levels": "1", "bonus": "7"}, {"levels": "3", "bonus": "100"}, {"levels": "10", "bonus": "2"}],
        intro="В игре `levels = {levels}` уровней. За уровень с номером 1 игрок получает `bonus = {bonus}` очков, "
              "за уровень 2 — вдвое больше, за уровень 3 — втрое больше: за уровень с номером `i` дают `i * bonus` очков. "
              "Игрок прошёл все уровни.",
        steps=["Заведи переменную `score` со значением 0.",
               "Циклом `for` перебери номера уровней от 1 до `levels` включительно и на каждом шаге прибавляй к `score` "
               "очки за этот уровень.",
               "После цикла выведи сумму очков в виде `Score: 150`",
               "Следующей строкой выведи, сколько очков в среднем приходится на один уровень (деление нацело `//`), "
               "в виде `Average per level: 30`"],
        hint="К накопителю прибавляют через `+=`: `score += ...`. Если написать `score = ...`, "
             "в переменной останутся только очки за последний уровень.",
        solution='score = 0\nfor level in range(1, levels + 1):\n    score += level * bonus\n'
                 'print(f"Score: {score}")\nprint(f"Average per level: {score // levels}")',
        wrong=[("прибавляет одинаковый bonus за каждый уровень, забыв умножить на номер уровня",
                'score = 0\nfor level in range(1, levels + 1):\n    score += bonus\n'
                'print(f"Score: {score}")\nprint(f"Average per level: {score // levels}")'),
               ("перезаписывает score вместо накопления: остаются очки только за последний уровень",
                'score = 0\nfor level in range(1, levels + 1):\n    score = level * bonus\n'
                'print(f"Score: {score}")\nprint(f"Average per level: {score // levels}")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-acc-free-coffee", title="Каждая k-я чашка бесплатно",
        given=["cups", "price", "k"],
        variants=[{"cups": "12", "price": "150", "k": "5"}, {"cups": "20", "price": "120", "k": "4"},
                  {"cups": "9", "price": "200", "k": "3"}],
        hidden=[{"cups": "4", "price": "100", "k": "5"}, {"cups": "10", "price": "90", "k": "10"},
                {"cups": "7", "price": "110", "k": "7"}, {"cups": "15", "price": "80", "k": "1"}],
        intro="В кофейне акция: каждая `k`-я чашка за день бесплатная — чашки с номерами, которые делятся на `k = {k}` "
              "без остатка. За день продали `cups = {cups}` чашек, обычная чашка стоит `price = {price}` рублей.",
        steps=["Заведи два накопителя со значением 0: `free` — сколько чашек отдали бесплатно, и `revenue` — "
               "сколько денег получила кофейня.",
               "Циклом `for` перебери номера чашек от 1 до `cups` включительно.",
               "Если номер чашки делится на `k` без остатка, увеличь `free` на 1. Иначе прибавь к `revenue` цену чашки.",
               "После цикла выведи `Free cups: 2` и следующей строкой `Revenue: 1500 rub`"],
        hint="Число `n` делится на `k` без остатка, когда `n % k == 0`. Оба накопителя заводят до цикла, "
             "а меняют внутри цикла — каждый в своей ветке `if` / `else`.",
        solution='free = 0\nrevenue = 0\nfor cup in range(1, cups + 1):\n    if cup % k == 0:\n        free += 1\n'
                 '    else:\n        revenue += price\nprint(f"Free cups: {free}")\nprint(f"Revenue: {revenue} rub")',
        wrong=[("правая граница не входит в range: последняя чашка не учтена",
                'free = 0\nrevenue = 0\nfor cup in range(1, cups):\n    if cup % k == 0:\n        free += 1\n'
                '    else:\n        revenue += price\nprint(f"Free cups: {free}")\nprint(f"Revenue: {revenue} rub")'),
               ("перезаписывает выручку вместо накопления: в ней остаётся цена одной чашки",
                'free = 0\nrevenue = 0\nfor cup in range(1, cups + 1):\n    if cup % k == 0:\n        free += 1\n'
                '    else:\n        revenue = price\nprint(f"Free cups: {free}")\nprint(f"Revenue: {revenue} rub")')],
        constructs=["for", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-acc-queue-orders", title="Сколькими способами встать в очередь",
        given=["friends"],
        variants=[{"friends": "4"}, {"friends": "5"}, {"friends": "6"}],
        hidden=[{"friends": "1"}, {"friends": "3"}, {"friends": "7"}],
        intro="`friends = {friends}` друзей встают в очередь в кино. Сколькими разными способами они могут встать? "
              "Один человек встаёт одним способом, двое — 1 * 2 способами, трое — 1 * 2 * 3, и так далее: "
              "ответ — произведение всех чисел от 1 до `friends`.",
        steps=["Заведи накопитель `ways` для произведения. Подумай, с какого числа его начать.",
               "Циклом `for` перебери числа `i` от 1 до `friends` включительно и на каждом шаге умножай `ways` на `i`: "
               "`ways = ways * i`.",
               "Сразу после умножения выведи строку вида `3: 6` — сколько человек уже учтено и сколько способов для них.",
               "После цикла выведи `Orders: 24`"],
        hint="Накопитель суммы начинают с 0, а накопитель произведения — с 1: умножение на 0 всегда даёт 0.",
        solution='ways = 1\nfor i in range(1, friends + 1):\n    ways = ways * i\n    print(f"{i}: {ways}")\n'
                 'print(f"Orders: {ways}")',
        wrong=[("начинает произведение с 0: все ответы получаются нулями",
                'ways = 0\nfor i in range(1, friends + 1):\n    ways = ways * i\n    print(f"{i}: {ways}")\n'
                'print(f"Orders: {ways}")'),
               ("складывает вместо умножения",
                'ways = 1\nfor i in range(1, friends + 1):\n    ways = ways + i\n    print(f"{i}: {ways}")\n'
                'print(f"Orders: {ways}")'),
               ("печатает до умножения: значения сдвинуты на шаг",
                'ways = 1\nfor i in range(1, friends + 1):\n    print(f"{i}: {ways}")\n    ways = ways * i\n'
                'print(f"Orders: {ways}")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-acc-run-plan", title="План пробежек",
        given=["first", "add", "days", "long"],
        variants=[{"first": "3", "add": "1", "days": "7", "long": "6"},
                  {"first": "2", "add": "2", "days": "5", "long": "6"},
                  {"first": "5", "add": "0", "days": "4", "long": "5"}],
        hidden=[{"first": "1", "add": "3", "days": "4", "long": "10"},
                {"first": "10", "add": "5", "days": "1", "long": "12"},
                {"first": "4", "add": "2", "days": "6", "long": "9"}],
        intro="Борис готовится к забегу. В первый день он пробегает `first = {first}` км, а каждый следующий день — "
              "на `add = {add}` км больше, чем накануне. Тренировки идут `days = {days}` дней. "
              "Пробежку длиной `long = {long}` км и больше он называет длинной.",
        steps=["Заведи два накопителя со значением 0: `total` — сколько всего километров, и `long_runs` — "
               "сколько было длинных пробежек.",
               "Циклом `for` перебери дни от 1 до `days` включительно.",
               "На каждом шаге посчитай дистанцию дня: `first` плюс `add`, умноженное на число дней, прошедших с первого. "
               "Прибавь её к `total`, а если она не меньше `long`, увеличь `long_runs` на 1.",
               "После цикла выведи три строки: `Total: 42 km`, `Long runs: 4` и среднюю дистанцию за день "
               "(деление нацело `//`) в виде `Average: 6 km`"],
        hint="В первый день с первого прошло 0 дней, во второй — 1 день: это `day - 1`. "
             "«Не меньше» — это `>=`: пробежка ровно в `long` км тоже длинная.",
        solution='total = 0\nlong_runs = 0\nfor day in range(1, days + 1):\n    km = first + (day - 1) * add\n'
                 '    total += km\n    if km >= long:\n        long_runs += 1\n'
                 'print(f"Total: {total} km")\nprint(f"Long runs: {long_runs}")\nprint(f"Average: {total // days} km")',
        wrong=[("ошибка на единицу: в первый день уже прибавлен add",
                'total = 0\nlong_runs = 0\nfor day in range(1, days + 1):\n    km = first + day * add\n'
                '    total += km\n    if km >= long:\n        long_runs += 1\n'
                'print(f"Total: {total} km")\nprint(f"Long runs: {long_runs}")\nprint(f"Average: {total // days} km")'),
               ("строгое сравнение: пробежка ровно в long км не считается длинной",
                'total = 0\nlong_runs = 0\nfor day in range(1, days + 1):\n    km = first + (day - 1) * add\n'
                '    total += km\n    if km > long:\n        long_runs += 1\n'
                'print(f"Total: {total} km")\nprint(f"Long runs: {long_runs}")\nprint(f"Average: {total // days} km")'),
               ("перезаписывает total вместо накопления",
                'total = 0\nlong_runs = 0\nfor day in range(1, days + 1):\n    km = first + (day - 1) * add\n'
                '    total = km\n    if km >= long:\n        long_runs += 1\n'
                'print(f"Total: {total} km")\nprint(f"Long runs: {long_runs}")\nprint(f"Average: {total // days} km")')],
        constructs=["for", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-acc-deposit", title="Вклад с процентами",
        given=["deposit", "percent", "years"],
        variants=[{"deposit": "10000", "percent": "10", "years": "3"},
                  {"deposit": "5000", "percent": "20", "years": "2"},
                  {"deposit": "8000", "percent": "5", "years": "4"}],
        hidden=[{"deposit": "1000", "percent": "10", "years": "1"},
                {"deposit": "2000", "percent": "50", "years": "3"},
                {"deposit": "7000", "percent": "3", "years": "5"}],
        intro="Вика положила в банк `deposit = {deposit}` рублей на `years = {years}` лет под `percent = {percent}` % годовых. "
              "В конце каждого года банк начисляет проценты на всю сумму, которая лежит на счёте в этот момент, "
              "включая проценты прошлых лет. Копейки банк отбрасывает.",
        steps=["Заведи переменную `balance` и положи в неё начальную сумму `deposit`.",
               "Циклом `for` перебери годы от 1 до `years` включительно.",
               "На каждом шаге посчитай проценты за год: `balance * percent // 100`, прибавь их к `balance` и выведи "
               "строку вида `Year 1: 11000 rub`",
               "После цикла выведи, сколько всего заработано процентами — итоговая сумма минус вклад — "
               "в виде `Interest: 3310 rub`"],
        hint="Проценты каждого года считают от текущего `balance`, а не от начального вклада: так на проценты тоже "
             "начисляются проценты. Деление нацело `//` отбрасывает копейки и оставляет число целым.",
        solution='balance = deposit\nfor year in range(1, years + 1):\n    interest = balance * percent // 100\n'
                 '    balance += interest\n    print(f"Year {year}: {balance} rub")\n'
                 'print(f"Interest: {balance - deposit} rub")',
        wrong=[("считает проценты всегда от начального вклада, а не от текущей суммы",
                'balance = deposit\nfor year in range(1, years + 1):\n    interest = deposit * percent // 100\n'
                '    balance += interest\n    print(f"Year {year}: {balance} rub")\n'
                'print(f"Interest: {balance - deposit} rub")'),
               ("делит через /: суммы печатаются дробными числами",
                'balance = deposit\nfor year in range(1, years + 1):\n    interest = balance * percent / 100\n'
                '    balance += interest\n    print(f"Year {year}: {balance} rub")\n'
                'print(f"Interest: {balance - deposit} rub")'),
               ("печатает итоговую сумму вместо заработанных процентов",
                'balance = deposit\nfor year in range(1, years + 1):\n    interest = balance * percent // 100\n'
                '    balance += interest\n    print(f"Year {year}: {balance} rub")\n'
                'print(f"Interest: {balance} rub")')],
        constructs=["for"],
    ),
]
