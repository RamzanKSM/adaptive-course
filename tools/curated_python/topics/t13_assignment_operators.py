"""PY_ASSIGNMENT_OPERATORS — «Составное присваивание += -=». Taught before: print, variables, assignment, arithmetic,
order of execution, int/float, strings, type conversion, // and %.
Not yet: f-strings, conditions, comparisons, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_ASSIGNMENT_OPERATORS"
AUG = [("AugAssign", "Используй составное присваивание (+=, -=, *=, //=, %=), чтобы изменить переменную")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ao-piggy-bank", title="Копилка",
        given=["balance", "weekly", "gift"],
        variants=[{"balance": "200", "weekly": "150", "gift": "120"}, {"balance": "50", "weekly": "100", "gift": "80"},
                  {"balance": "340", "weekly": "75", "gift": "300"}],
        hidden=[{"balance": "0", "weekly": "10", "gift": "5"}, {"balance": "1000", "weekly": "250", "gift": "900"},
                {"balance": "35", "weekly": "40", "gift": "60"}],
        intro="Маша копит деньги в копилке. Сейчас в ней `balance = {balance}` руб. Каждую неделю Маша кладёт туда "
              "`weekly = {weekly}` руб., а после второй недели тратит `gift = {gift}` руб. на подарок другу.",
        steps=["Добавь к `balance` недельные деньги с помощью `+=` и выведи `Week 1:` и баланс через `print` с запятой.",
               "Ещё раз добавь `weekly` и выведи `Week 2:` и баланс.",
               "Вычти стоимость подарка с помощью `-=` и выведи `After gift:` и баланс.",
               "Например, для баланса 100, недельных 10 и подарка 5 программа выводит `Week 1: 110`, `Week 2: 120`, "
               "`After gift: 115`."],
        hint="`x += 5` — короткая запись для `x = x + 5`: к старому значению прибавляется 5. "
             "А `x = 5` просто стирает старое значение. `print(\"Week 1:\", balance)` сам ставит пробел между частями.",
        solution='balance += weekly\nprint("Week 1:", balance)\nbalance += weekly\nprint("Week 2:", balance)\n'
                 'balance -= gift\nprint("After gift:", balance)',
        wrong=[("прибавляет подарок вместо того, чтобы вычесть",
                'balance += weekly\nprint("Week 1:", balance)\nbalance += weekly\nprint("Week 2:", balance)\n'
                'balance += gift\nprint("After gift:", balance)'),
               ("на первой неделе затирает баланс вместо того, чтобы прибавить",
                'balance = weekly\nprint("Week 1:", balance)\nbalance += weekly\nprint("Week 2:", balance)\n'
                'balance -= gift\nprint("After gift:", balance)')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ao-bus-stops", title="Пассажиры в автобусе",
        given=["passengers", "enter", "leave"],
        variants=[{"passengers": "12", "enter": "5", "leave": "8"}, {"passengers": "30", "enter": "7", "leave": "15"},
                  {"passengers": "4", "enter": "9", "leave": "3"}],
        hidden=[{"passengers": "0", "enter": "6", "leave": "2"}, {"passengers": "20", "enter": "1", "leave": "20"},
                {"passengers": "45", "enter": "12", "leave": "30"}],
        intro="Водитель автобуса считает пассажиров. Сейчас в салоне `passengers = {passengers}` человек. "
              "На первой остановке входят `enter = {enter}` человек. На второй остановке выходят `leave = {leave}` "
              "человек, а потом снова входят `enter` человек.",
        steps=["Первая остановка: прибавь `enter` к `passengers` с помощью `+=` и выведи `Stop 1:` и число пассажиров "
               "(через `print` с запятой).",
               "Вторая остановка: вычти `leave` с помощью `-=`, затем прибавь `enter` с помощью `+=`.",
               "Выведи `Stop 2:` и число пассажиров.",
               "Например, для 10 пассажиров, `enter = 2` и `leave = 5` программа выводит `Stop 1: 12` и `Stop 2: 9`."],
        hint="Пиши именно `+=`, а не `=+`: запись `x =+ 5` Python читает как `x = +5`, то есть просто кладёт в `x` число 5.",
        solution='passengers += enter\nprint("Stop 1:", passengers)\npassengers -= leave\npassengers += enter\n'
                 'print("Stop 2:", passengers)',
        wrong=[("пишет =+ вместо += — старое число пассажиров теряется",
                'passengers =+ enter\nprint("Stop 1:", passengers)\npassengers -= leave\npassengers += enter\n'
                'print("Stop 2:", passengers)'),
               ("на второй остановке забывает про вошедших",
                'passengers += enter\nprint("Stop 1:", passengers)\npassengers -= leave\n'
                'print("Stop 2:", passengers)')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ao-game-score", title="Очки в игре",
        given=["score", "level_points", "penalty"],
        variants=[{"score": "0", "level_points": "150", "penalty": "70"}, {"score": "40", "level_points": "200", "penalty": "125"},
                  {"score": "15", "level_points": "90", "penalty": "33"}],
        hidden=[{"score": "10", "level_points": "5", "penalty": "1"}, {"score": "100", "level_points": "300", "penalty": "500"},
                {"score": "7", "level_points": "60", "penalty": "0"}],
        intro="В компьютерной игре у игрока сейчас `score = {score}` очков. За каждый пройденный уровень дают "
              "`level_points = {level_points}` очков. Игрок прошёл два уровня, потом получил бонус — все очки удвоились, "
              "а в конце его оштрафовали на `penalty = {penalty}` очков.",
        steps=["Прибавь очки за первый уровень с помощью `+=` и выведи `Level 1:` и очки (через `print` с запятой).",
               "Прибавь очки за второй уровень и выведи `Level 2:` и очки.",
               "Удвой очки с помощью `*=` и выведи `Bonus:` и очки.",
               "Вычти штраф с помощью `-=` и выведи `Final:` и очки.",
               "Например, для 0 очков, 10 за уровень и штрафа 5 программа выводит `Level 1: 10`, `Level 2: 20`, "
               "`Bonus: 40`, `Final: 35`."],
        hint="`x *= 2` — то же, что `x = x * 2`. Порядок важен: штраф вычитается уже после удвоения, иначе удвоится и он.",
        solution='score += level_points\nprint("Level 1:", score)\nscore += level_points\nprint("Level 2:", score)\n'
                 'score *= 2\nprint("Bonus:", score)\nscore -= penalty\nprint("Final:", score)',
        wrong=[("прибавляет 2 вместо удвоения",
                'score += level_points\nprint("Level 1:", score)\nscore += level_points\nprint("Level 2:", score)\n'
                'score += 2\nprint("Bonus:", score)\nscore -= penalty\nprint("Final:", score)'),
               ("за второй уровень снова кладёт очки одного уровня вместо прибавления",
                'score += level_points\nprint("Level 1:", score)\nscore = level_points\nprint("Level 2:", score)\n'
                'score *= 2\nprint("Bonus:", score)\nscore -= penalty\nprint("Final:", score)')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ao-recipe-guests", title="Рецепт на всех гостей",
        given=["flour", "sugar", "guests"],
        variants=[{"flour": "250", "sugar": "90", "guests": "6"}, {"flour": "300", "sugar": "150", "guests": "10"},
                  {"flour": "180", "sugar": "70", "guests": "3"}],
        hidden=[{"flour": "400", "sugar": "100", "guests": "4"}, {"flour": "125", "sugar": "55", "guests": "7"},
                {"flour": "500", "sugar": "210", "guests": "2"}],
        intro="Рецепт пирога рассчитан на 4 человек: в нём `flour = {flour}` г муки и `sugar = {sugar}` г сахара. "
              "А в гости придут `guests = {guests}` человек. Нужно пересчитать продукты на всех гостей.",
        steps=["Умножь `flour` на `guests` с помощью `*=`, а потом раздели на 4 нацело с помощью `//=` "
               "(лишние доли грамма отбрасываются).",
               "Точно так же пересчитай `sugar`: сначала `*=`, потом `//=`.",
               "Выведи две строки через `print` с запятыми: `Flour:`, мука и `g`, затем `Sugar:`, сахар и `g`.",
               "Например, для 100 г муки, 40 г сахара и 6 гостей программа выводит `Flour: 150 g` и `Sugar: 60 g`."],
        hint="Сначала умножай, потом дели: если сначала разделить нацело, дробная часть потеряется раньше времени. "
             "Деление `/=` дало бы дробное число вроде `375.0`, а нам нужно целое — поэтому `//=`.",
        solution='flour *= guests\nflour //= 4\nsugar *= guests\nsugar //= 4\n'
                 'print("Flour:", flour, "g")\nprint("Sugar:", sugar, "g")',
        wrong=[("делит муку через /= — получается дробное число",
                'flour *= guests\nflour /= 4\nsugar *= guests\nsugar //= 4\n'
                'print("Flour:", flour, "g")\nprint("Sugar:", sugar, "g")'),
               ("сахар делит на 4, но забывает умножить на число гостей",
                'flour *= guests\nflour //= 4\nsugar //= 4\n'
                'print("Flour:", flour, "g")\nprint("Sugar:", sugar, "g")')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ao-shop-discount", title="Покупка со скидкой",
        given=["bread", "milk"],
        variants=[{"bread": "45", "milk": "89"}, {"bread": "52", "milk": "76"}, {"bread": "38", "milk": "95"}],
        hidden=[{"bread": "40", "milk": "100"}, {"bread": "61", "milk": "64"}, {"bread": "5", "milk": "3"}],
        intro="Покупатель берёт 2 батона хлеба по `bread = {bread}` руб. и 3 пакета молока по `milk = {milk}` руб. "
              "Магазин даёт скидку 10% от суммы покупки, копейки скидки отбрасываются.",
        steps=["Заведи переменную `total = 0`.",
               "Прибавь к `total` стоимость хлеба (`bread * 2`), а потом стоимость молока (`milk * 3`) — каждый раз с помощью `+=`.",
               "Выведи `Sum:`, `total` и `rub` (через `print` с запятыми).",
               "Посчитай скидку: `total`, делённое нацело на 10, — и сохрани её в переменную `discount`. "
               "Вычти её из `total` с помощью `-=`.",
               "Выведи `Discount:`, скидку и `rub`, затем `To pay:`, `total` и `rub`.",
               "Например, для суммы 200 руб. программа выводит `Sum: 200 rub`, `Discount: 20 rub`, `To pay: 180 rub`."],
        hint="10% от числа — это число, делённое на 10; деление нацело `//` отбрасывает копейки. "
             "Если написать `total = milk * 3`, стоимость хлеба пропадёт — нужно именно `+=`.",
        solution='total = 0\ntotal += bread * 2\ntotal += milk * 3\nprint("Sum:", total, "rub")\n'
                 'discount = total // 10\ntotal -= discount\nprint("Discount:", discount, "rub")\nprint("To pay:", total, "rub")',
        wrong=[("перезаписывает сумму стоимостью молока вместо прибавления",
                'total = 0\ntotal += bread * 2\ntotal = milk * 3\nprint("Sum:", total, "rub")\n'
                'discount = total // 10\ntotal -= discount\nprint("Discount:", discount, "rub")\nprint("To pay:", total, "rub")'),
               ("берёт остаток % вместо деления нацело",
                'total = 0\ntotal += bread * 2\ntotal += milk * 3\nprint("Sum:", total, "rub")\n'
                'discount = total % 10\ntotal -= discount\nprint("Discount:", discount, "rub")\nprint("To pay:", total, "rub")')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ao-running-laps", title="Три круга на стадионе",
        given=["lap1", "lap2", "lap3"],
        variants=[{"lap1": "95", "lap2": "102", "lap3": "88"}, {"lap1": "130", "lap2": "125", "lap3": "141"},
                  {"lap1": "70", "lap2": "64", "lap3": "59"}],
        hidden=[{"lap1": "20", "lap2": "20", "lap3": "20"}, {"lap1": "200", "lap2": "190", "lap3": "210"},
                {"lap1": "15", "lap2": "17", "lap3": "9"}],
        intro="Бегун пробежал три круга по стадиону. Время каждого круга в секундах: `lap1 = {lap1}`, `lap2 = {lap2}` "
              "и `lap3 = {lap3}`. Тренеру нужно общее время — сначала в секундах, а потом в минутах и секундах.",
        steps=["Заведи переменную `total` и положи в неё `lap1`.",
               "Прибавь к `total` второй и третий круг — каждый отдельной строкой с `+=`.",
               "Выведи `Total:`, `total` и `s` (через `print` с запятыми).",
               "Сохрани в переменную `minutes` целое число минут: `total`, делённое нацело на 60.",
               "Оставь в `total` только остаток секунд с помощью `%=` и выведи `Time:`, минуты, `min`, секунды и `s`.",
               "Например, для кругов 50, 40 и 35 секунд программа выводит `Total: 125 s` и `Time: 2 min 5 s`."],
        hint="Порядок важен: минуты нужно посчитать до того, как `total %= 60` оставит в `total` только остаток. "
             "`125 // 60` даёт `2`, а `125 % 60` даёт `5`.",
        solution='total = lap1\ntotal += lap2\ntotal += lap3\nprint("Total:", total, "s")\n'
                 'minutes = total // 60\ntotal %= 60\nprint("Time:", minutes, "min", total, "s")',
        wrong=[("оставляет в total частное //= вместо остатка",
                'total = lap1\ntotal += lap2\ntotal += lap3\nprint("Total:", total, "s")\n'
                'minutes = total // 60\ntotal //= 60\nprint("Time:", minutes, "min", total, "s")'),
               ("берёт остаток раньше, чем считает минуты",
                'total = lap1\ntotal += lap2\ntotal += lap3\nprint("Total:", total, "s")\n'
                'total %= 60\nminutes = total // 60\nprint("Time:", minutes, "min", total, "s")')],
        must_use=AUG,
    ),
]
