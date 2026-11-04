"""PY_LIST_ITERATION — «Перебор списка». Taught before: print, variables, arithmetic, int/float, strings, type conversion,
// and %, += -=, f-strings, conditions, for + range, accumulator, while, break/continue, list indexes, lists (creating,
append, len, in). Here: for item in list — visiting every element, summing, counting, finding the best, filtering into
a new list. Not yet: sum/max/min, string slicing and methods, functions, insert/remove/sort and list slices."""
from build import OutputTask

SKILL = "PY_LIST_ITERATION"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lit-receipt", title="Чек из магазина",
        given=["prices"],
        variants=[{"prices": "[120, 45, 300]"}, {"prices": "[99, 250, 60, 15]"}, {"prices": "[500, 75]"}],
        hidden=[{"prices": "[10]"}, {"prices": "[1, 2, 3, 4, 5]"}, {"prices": "[250, 250]"}],
        intro="Касса печатает чек. Цены покупок в рублях записаны в список `prices`. Покупок может быть сколько угодно.",
        steps=["Заведи накопитель `total` со значением 0.",
               "Перебери список циклом `for price in prices:`",
               "Для каждой покупки выведи строку вида `Item: 120 rub` и прибавь её цену к `total`.",
               "После цикла выведи `Total: 465 rub`"],
        hint="В цикле `for price in prices:` переменная `price` по очереди становится каждым элементом списка — "
             "индексы не нужны. Итог печатается один раз, поэтому `print` с ним пишется без отступа, после цикла.",
        solution='total = 0\nfor price in prices:\n    print(f"Item: {price} rub")\n    total += price\n'
                 'print(f"Total: {total} rub")',
        wrong=[("перезаписывает total вместо накопления: в итоге цена последней покупки",
                'total = 0\nfor price in prices:\n    print(f"Item: {price} rub")\n    total = price\n'
                'print(f"Total: {total} rub")'),
               ("печатает весь список вместо одной покупки",
                'total = 0\nfor price in prices:\n    print(f"Item: {prices} rub")\n    total += price\n'
                'print(f"Total: {total} rub")')],
        constructs=["list", "for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lit-roll-call", title="Перекличка",
        given=["names"],
        variants=[{"names": '["Anya", "Boris", "Vika"]'}, {"names": '["Lev", "Mila", "Nina", "Oleg", "Petya"]'},
                  {"names": '["Rita", "Sonya", "Timur", "Egor"]'}],
        hidden=[{"names": '["Ira"]'}, {"names": '["Max", "Eva"]'}, {"names": '["Dina", "Yana", "Fil", "Zoya", "Gleb", "Kira"]'}],
        intro="Староста проводит перекличку. Имена пришедших записаны в список `names` — в том порядке, "
              "в каком они отозвались.",
        steps=["Заведи счётчик `count` со значением 0.",
               "Перебери список циклом `for name in names:`",
               "Для каждого имени увеличь `count` на 1 и выведи строку вида `1. Anya` — порядковый номер, точку, "
               "пробел и имя.",
               "После цикла выведи `Present: 3`"],
        hint="Сначала увеличь счётчик, потом печатай: тогда первое имя получит номер 1. "
             "Внутри цикла печатай `name` — один элемент, а не весь список `names`.",
        solution='count = 0\nfor name in names:\n    count += 1\n    print(f"{count}. {name}")\nprint(f"Present: {count}")',
        wrong=[("счётчик начинается с 1: номера и итог на единицу больше",
                'count = 1\nfor name in names:\n    count += 1\n    print(f"{count}. {name}")\nprint(f"Present: {count}")'),
               ("печатает весь список вместо одного имени",
                'count = 0\nfor name in names:\n    count += 1\n    print(f"{count}. {names}")\nprint(f"Present: {count}")')],
        constructs=["list", "for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lit-norm", title="Норматив по бегу",
        given=["times", "norm"],
        variants=[{"times": "[12, 15, 14, 18, 13]", "norm": "14"}, {"times": "[9, 11, 10, 12]", "norm": "10"},
                  {"times": "[20, 17, 19, 18]", "norm": "18"}],
        hidden=[{"times": "[10]", "norm": "10"}, {"times": "[16, 15, 17]", "norm": "14"},
                {"times": "[11, 12, 13, 14, 15]", "norm": "13"}],
        intro="Класс бежал 60 метров. Время каждого в секундах записано в список `times`. Норматив сдан, если время "
              "не больше `norm = {norm}` секунд.",
        steps=["Создай пустой список `passed` и счётчик `failed` со значением 0.",
               "Перебери список `times` циклом `for`.",
               "Если время не больше `norm`, добавь его в `passed`. Иначе увеличь `failed` на 1.",
               "После цикла выведи `Passed: [12, 14, 13]` и следующей строкой `Failed: 2`"],
        hint="«Не больше» — это `<=`: время ровно `norm` секунд — норматив сдан. "
             "В `passed` добавляй время бегуна, а не сам норматив.",
        solution='passed = []\nfailed = 0\nfor time in times:\n    if time <= norm:\n        passed.append(time)\n'
                 '    else:\n        failed += 1\nprint(f"Passed: {passed}")\nprint(f"Failed: {failed}")',
        wrong=[("строгое сравнение: время ровно norm не засчитано",
                'passed = []\nfailed = 0\nfor time in times:\n    if time < norm:\n        passed.append(time)\n'
                '    else:\n        failed += 1\nprint(f"Passed: {passed}")\nprint(f"Failed: {failed}")'),
               ("добавляет в список норматив вместо времени бегуна",
                'passed = []\nfailed = 0\nfor time in times:\n    if time <= norm:\n        passed.append(norm)\n'
                '    else:\n        failed += 1\nprint(f"Passed: {passed}")\nprint(f"Failed: {failed}")')],
        constructs=["list", "for", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lit-passwords", title="Проверка паролей",
        given=["passwords", "min_len"],
        variants=[{"passwords": '["qwerty", "sunflower7", "cat", "dragon12"]', "min_len": "8"},
                  {"passwords": '["abc123", "summer2026", "x"]', "min_len": "6"},
                  {"passwords": '["letmein", "blue_sky_42", "hello"]', "min_len": "7"}],
        hidden=[{"passwords": '["a"]', "min_len": "1"}, {"passwords": '["short", "tiny"]', "min_len": "10"},
                {"passwords": '["12345678", "pass", "secret_key"]', "min_len": "8"}],
        intro="Сайт проверяет пароли пользователей. Пароли записаны в список `passwords`. Пароль годится, "
              "если в нём не меньше `min_len = {min_len}` символов.",
        steps=["Заведи счётчик `strong` со значением 0.",
               "Перебери список `passwords` циклом `for`.",
               "Если длина пароля не меньше `min_len`, увеличь `strong` на 1 и выведи строку вида `sunflower7: ok`. "
               "Иначе выведи строку вида `qwerty: too short`",
               "После цикла выведи `Strong: 2 of 4` — сколько паролей годится и сколько их всего."],
        hint="Длину строки даёт `len`, как и длину списка. Следи, чью длину берёшь: `len(password)` — "
             "длина одного пароля, `len(passwords)` — сколько паролей в списке.",
        solution='strong = 0\nfor password in passwords:\n    if len(password) >= min_len:\n        strong += 1\n'
                 '        print(f"{password}: ok")\n    else:\n        print(f"{password}: too short")\n'
                 'print(f"Strong: {strong} of {len(passwords)}")',
        wrong=[("строгое сравнение: пароль длиной ровно min_len считается коротким",
                'strong = 0\nfor password in passwords:\n    if len(password) > min_len:\n        strong += 1\n'
                '        print(f"{password}: ok")\n    else:\n        print(f"{password}: too short")\n'
                'print(f"Strong: {strong} of {len(passwords)}")'),
               ("проверяет длину всего списка, а не пароля",
                'strong = 0\nfor password in passwords:\n    if len(passwords) >= min_len:\n        strong += 1\n'
                '        print(f"{password}: ok")\n    else:\n        print(f"{password}: too short")\n'
                'print(f"Strong: {strong} of {len(passwords)}")')],
        constructs=["list", "for", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lit-long-jump", title="Лучший прыжок",
        given=["jumps"],
        variants=[{"jumps": "[310, 345, 330, 345, 320]"}, {"jumps": "[280, 295, 301]"}, {"jumps": "[402, 398, 410, 405]"}],
        hidden=[{"jumps": "[300]"}, {"jumps": "[250, 260, 260, 255]"}, {"jumps": "[500, 480, 470]"}],
        intro="Аня прыгает в длину. Результаты попыток в сантиметрах записаны в список `jumps` по порядку. "
              "Нужно найти лучший результат и номер попытки, в которой он был впервые показан. "
              "Попытки нумеруются с 1. Готовую функцию `max` не используй — найди лучший прыжок сам.",
        steps=["Заведи `best` — результат первой попытки, `number` со значением 1 (номер лучшей попытки) "
               "и счётчик попыток `attempt` со значением 0.",
               "Перебери список `jumps` циклом `for`. На каждом шаге сначала увеличь `attempt` на 1.",
               "Если прыжок дальше, чем `best`, запомни его в `best`, а номер попытки — в `number`.",
               "После цикла выведи `Best jump: 345 cm` и следующей строкой `Attempt: 2`"],
        hint="Сравнивай строго, через `>`: если такой же результат повторится позже, номер лучшей попытки "
             "должен остаться прежним.",
        solution='best = jumps[0]\nnumber = 1\nattempt = 0\nfor jump in jumps:\n    attempt += 1\n    if jump > best:\n'
                 '        best = jump\n        number = attempt\nprint(f"Best jump: {best} cm")\nprint(f"Attempt: {number}")',
        wrong=[("нестрогое сравнение: при повторе результата запоминает более позднюю попытку",
                'best = jumps[0]\nnumber = 1\nattempt = 0\nfor jump in jumps:\n    attempt += 1\n    if jump >= best:\n'
                '        best = jump\n        number = attempt\nprint(f"Best jump: {best} cm")\nprint(f"Attempt: {number}")'),
               ("счётчик попыток начинается с 1: номер на единицу больше",
                'best = jumps[0]\nnumber = 1\nattempt = 1\nfor jump in jumps:\n    attempt += 1\n    if jump > best:\n'
                '        best = jump\n        number = attempt\nprint(f"Best jump: {best} cm")\nprint(f"Attempt: {number}")')],
        constructs=["list", "for", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lit-card", title="Баланс карты",
        given=["balance", "operations"],
        variants=[{"balance": "500", "operations": "[-200, -400, 300, -100]"},
                  {"balance": "1000", "operations": "[-300, 500, -1200, 100]"},
                  {"balance": "200", "operations": "[100, -50, 30]"}],
        hidden=[{"balance": "0", "operations": "[-10]"}, {"balance": "100", "operations": "[-150, -20, 400]"},
                {"balance": "50", "operations": "[25, 25]"},
                {"balance": "300", "operations": "[-300, 40]"}],
        intro="На карте у Егора `balance = {balance}` рублей. В списке `operations` записаны операции по порядку: "
              "положительное число — пополнение, отрицательное — покупка. Банк разрешает уходить в минус.",
        steps=["Заведи `lowest` — самый маленький баланс, сначала равный `balance`, и счётчик `below` со значением 0.",
               "Перебери операции циклом `for`. Каждую прибавь к `balance` и выведи строку вида `Balance: 300 rub`",
               "Если баланс стал меньше 0, увеличь `below` на 1. Если он меньше `lowest`, запомни его в `lowest`.",
               "После цикла выведи `Times below zero: 1` и следующей строкой `Lowest: -100 rub`"],
        hint="Покупка уже записана со знаком минус, поэтому любую операцию просто прибавляют: `balance += op`. "
             "Ноль — это ещё не минус. Начальный баланс тоже может оказаться самым маленьким.",
        solution='lowest = balance\nbelow = 0\nfor op in operations:\n    balance += op\n    print(f"Balance: {balance} rub")\n'
                 '    if balance < 0:\n        below += 1\n    if balance < lowest:\n        lowest = balance\n'
                 'print(f"Times below zero: {below}")\nprint(f"Lowest: {lowest} rub")',
        wrong=[("нестрогое сравнение: нулевой баланс считается минусом",
                'lowest = balance\nbelow = 0\nfor op in operations:\n    balance += op\n    print(f"Balance: {balance} rub")\n'
                '    if balance <= 0:\n        below += 1\n    if balance < lowest:\n        lowest = balance\n'
                'print(f"Times below zero: {below}")\nprint(f"Lowest: {lowest} rub")'),
               ("начинает поиск минимума с 0, а не с начального баланса",
                'lowest = 0\nbelow = 0\nfor op in operations:\n    balance += op\n    print(f"Balance: {balance} rub")\n'
                '    if balance < 0:\n        below += 1\n    if balance < lowest:\n        lowest = balance\n'
                'print(f"Times below zero: {below}")\nprint(f"Lowest: {lowest} rub")'),
               ("заменяет баланс операцией вместо того, чтобы прибавить её",
                'lowest = balance\nbelow = 0\nfor op in operations:\n    balance = op\n    print(f"Balance: {balance} rub")\n'
                '    if balance < 0:\n        below += 1\n    if balance < lowest:\n        lowest = balance\n'
                'print(f"Times below zero: {below}")\nprint(f"Lowest: {lowest} rub")')],
        constructs=["list", "for", "if"],
    ),
]
