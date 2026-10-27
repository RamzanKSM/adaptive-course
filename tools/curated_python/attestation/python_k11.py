"""Attestation, Python, topics 1–11 (up to PY_FSTRINGS): print, variables, assignment, arithmetic, order of execution,
int/float, strings (+, *, len), type conversion (int(), float()), // and %, += -=, f-strings.
Every story is different (cooking, shops and markets); each reference solution uses all of these in a small program.
Not yet: format specifiers like :.2f, round(), conditions, comparisons, logical operators, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_FSTRINGS"
MUST = [("JoinedStr", "Используй f-строку: f\"...{переменная}...\""),
        ("AugAssign", "Используй составное присваивание (+= или -=), чтобы изменить переменную"),
        ("FloorDiv", "Используй деление нацело //"),
        ("Mod", "Используй остаток от деления %")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att11-pancakes", title="Блины для гостей",
        given=["guests", "each", "plate", "milk"],
        variants=[{"guests": '"6"', "each": "3", "plate": "6", "milk": "40"}],
        hidden=[{"guests": '"1"', "each": "2", "plate": "4", "milk": "50"},
                {"guests": '"12"', "each": "4", "plate": "5", "milk": "35"},
                {"guests": '"3"', "each": "5", "plate": "8", "milk": "60"},
                {"guests": '"10"', "each": "1", "plate": "5", "milk": "45"}],
        intro="Бабушка печёт блины для гостей. Число гостей пришло сообщением в чате, поэтому оно записано строкой: "
              "`guests = {guests}`. Каждому гостю достанется `each = {each}` блина, на одну тарелку помещается "
              "`plate = {plate}` блинов, а на один блин уходит `milk = {milk}` мл молока.",
        steps=["Склей через `+` строку `Pancakes, guests: ` и `guests`, сохрани результат в переменную `title` "
               "и выведи его.",
               "Под заголовком выведи строку из знаков `-` такой же длины, как `title` (длину даёт `len()`).",
               "Преврати `guests` в целое число, умножь на `each` и сохрани в `pancakes`. "
               "Бабушка печёт ещё 2 блина на пробу: прибавь их к `pancakes` с помощью `+=`.",
               "Посчитай, сколько тарелок заполнится целиком (`pancakes`, делённое нацело на `plate`), — это `plates`, и сколько "
               "блинов останется на последней неполной тарелке (остаток от деления) — это `extra`.",
               "Посчитай молоко в литрах: `pancakes * milk / 1000` — и сохрани в `liters`.",
               "С помощью f-строк выведи `Pancakes: <pancakes>`, `Full plates: <plates>, extra: <extra>` и "
               "`Milk: <liters> l`. Например, для 10 блинов, тарелок по 4 блина и 50 мл на блин — `Pancakes: 10`, "
               "`Full plates: 2, extra: 2`, `Milk: 0.5 l`."],
        hint="`guests` — строка, поэтому в заголовок её можно приклеить как есть, а для умножения нужен `int(guests)`. "
             "`\"-\" * 5` даёт `-----`. Деление `/` даёт дробное число, а `//` отбросило бы дробную часть литров.",
        solution='title = "Pancakes, guests: " + guests\nprint(title)\nprint("-" * len(title))\n'
                 'pancakes = int(guests) * each\npancakes += 2\nplates = pancakes // plate\nextra = pancakes % plate\n'
                 'liters = pancakes * milk / 1000\nprint(f"Pancakes: {pancakes}")\n'
                 'print(f"Full plates: {plates}, extra: {extra}")\nprint(f"Milk: {liters} l")',
        wrong=[("забыты 2 пробных блина",
                'title = "Pancakes, guests: " + guests\nprint(title)\nprint("-" * len(title))\n'
                'pancakes = int(guests) * each\nplates = pancakes // plate\nextra = pancakes % plate\n'
                'liters = pancakes * milk / 1000\nprint(f"Pancakes: {pancakes}")\n'
                'print(f"Full plates: {plates}, extra: {extra}")\nprint(f"Milk: {liters} l")'),
               ("остаток посчитан через // — получается то же число тарелок",
                'title = "Pancakes, guests: " + guests\nprint(title)\nprint("-" * len(title))\n'
                'pancakes = int(guests) * each\npancakes += 2\nplates = pancakes // plate\nextra = pancakes // plate\n'
                'liters = pancakes * milk / 1000\nprint(f"Pancakes: {pancakes}")\n'
                'print(f"Full plates: {plates}, extra: {extra}")\nprint(f"Milk: {liters} l")'),
               ("литры посчитаны через // — дробная часть теряется",
                'title = "Pancakes, guests: " + guests\nprint(title)\nprint("-" * len(title))\n'
                'pancakes = int(guests) * each\npancakes += 2\nplates = pancakes // plate\nextra = pancakes % plate\n'
                'liters = pancakes * milk // 1000\nprint(f"Pancakes: {pancakes}")\n'
                'print(f"Full plates: {plates}, extra: {extra}")\nprint(f"Milk: {liters} l")')],
        must_use=MUST,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att11-market-scales", title="Весы на рынке",
        given=["fruit", "grams", "price", "cash"],
        variants=[{"fruit": '"Apples"', "grams": '"2400"', "price": "85", "cash": "500"}],
        hidden=[{"fruit": '"Pears"', "grams": '"1000"', "price": "120", "cash": "200"},
                {"fruit": '"Plums"', "grams": '"750"', "price": "160", "cash": "1000"},
                {"fruit": '"Figs"', "grams": '"1999"', "price": "100", "cash": "500"},
                {"fruit": '"Lemons"', "grams": '"2000"', "price": "50", "cash": "110"}],
        intro="На рынке продавец взвешивает фрукты `fruit = {fruit}`. Электронные весы выдают вес в граммах строкой: "
              "`grams = {grams}`. Килограмм стоит `price = {price}` руб., покупатель даёт `cash = {cash}` руб. "
              "Копейки продавец не считает, а за пакет берёт ещё 10 руб. Сдачу он выдаёт купюрами по 50 руб. "
              "и мелочью.",
        steps=["Склей через `+` название фрукта, `, `, строку `grams` и ` g` и выведи, например `Pears, 1000 g`.",
               "Посчитай вес в килограммах: `int(grams) / 1000` — и сохрани в `kg`.",
               "Посчитай цену в рублях без копеек: `int(grams) * price // 1000` — и сохрани в `cost`. "
               "Прибавь к `cost` 10 руб. за пакет с помощью `+=`.",
               "Посчитай сдачу `change` (деньги покупателя минус `cost`), число купюр по 50 руб. `notes` "
               "(`change`, делённое нацело на 50) и мелочь `coins` (остаток от деления на 50).",
               "С помощью f-строк выведи `Weight: <kg> kg`, `To pay: <cost> rub` и "
               "`Change: <notes> x 50 rub + <coins> rub`. Например, для 1000 г по 120 руб. и 200 руб. от покупателя — "
               "`Weight: 1.0 kg`, `To pay: 130 rub`, `Change: 1 x 50 rub + 20 rub`."],
        hint="Вес пришёл строкой, поэтому в первую строку его можно приклеить как есть, а для расчётов нужен `int(grams)`. "
             "Сначала умножай на цену, потом дели нацело на 1000: так теряются только копейки.",
        solution='print(fruit + ", " + grams + " g")\nkg = int(grams) / 1000\ncost = int(grams) * price // 1000\n'
                 'cost += 10\nchange = cash - cost\nnotes = change // 50\ncoins = change % 50\n'
                 'print(f"Weight: {kg} kg")\nprint(f"To pay: {cost} rub")\n'
                 'print(f"Change: {notes} x 50 rub + {coins} rub")',
        wrong=[("забыт пакет за 10 руб.",
                'print(fruit + ", " + grams + " g")\nkg = int(grams) / 1000\ncost = int(grams) * price // 1000\n'
                'change = cash - cost\nnotes = change // 50\ncoins = change % 50\n'
                'print(f"Weight: {kg} kg")\nprint(f"To pay: {cost} rub")\n'
                'print(f"Change: {notes} x 50 rub + {coins} rub")'),
               ("вес в килограммах посчитан через // — граммы теряются",
                'print(fruit + ", " + grams + " g")\nkg = int(grams) // 1000\ncost = int(grams) * price // 1000\n'
                'cost += 10\nchange = cash - cost\nnotes = change // 50\ncoins = change % 50\n'
                'print(f"Weight: {kg} kg")\nprint(f"To pay: {cost} rub")\n'
                'print(f"Change: {notes} x 50 rub + {coins} rub")'),
               ("мелочь посчитана через // вместо остатка",
                'print(fruit + ", " + grams + " g")\nkg = int(grams) / 1000\ncost = int(grams) * price // 1000\n'
                'cost += 10\nchange = cash - cost\nnotes = change // 50\ncoins = change // 50\n'
                'print(f"Weight: {kg} kg")\nprint(f"To pay: {cost} rub")\n'
                'print(f"Change: {notes} x 50 rub + {coins} rub")')],
        must_use=MUST,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att11-bakery-bread", title="Хлеб в пекарне",
        given=["start_h", "start_m", "rise", "bake"],
        variants=[{"start_h": '"7"', "start_m": '"40"', "rise": "90", "bake": "45"}],
        hidden=[{"start_h": '"6"', "start_m": '"00"', "rise": "60", "bake": "30"},
                {"start_h": '"9"', "start_m": '"55"', "rise": "45", "bake": "30"},
                {"start_h": '"8"', "start_m": '"45"', "rise": "30", "bake": "30"},
                {"start_h": '"11"', "start_m": '"05"', "rise": "100", "bake": "35"}],
        intro="Пекарь ставит тесто для хлеба. Время начала он прочитал с часов, поэтому часы и минуты записаны строками: "
              "`start_h = {start_h}` и `start_m = {start_m}`. Тесто поднимается `rise = {rise}` минут, печётся "
              "`bake = {bake}` минут, а потом хлеб ещё 15 минут остывает.",
        steps=["Склей через `+` строку `Start: `, `start_h`, двоеточие и `start_m` и выведи, например `Start: 6:00`.",
               "Сохрани в `total` сумму `rise` и `bake`, затем прибавь к `total` 15 минут остывания с помощью `+=`.",
               "Переведи время начала в минуты от полуночи: часы (превращённые в целое число) умножь на 60 и прибавь "
               "минуты (тоже превращённые в число). Прибавь `total` и сохрани в `finish`.",
               "С помощью f-строк выведи `Total: <total> min = <total / 60> h` и `Ready: <finish // 60> h <finish % 60> min`, "
               "где часы готовности — `finish`, делённое нацело на 60, а минуты — остаток от деления на 60.",
               "Например, для начала в `\"6\"`:`\"00\"`, подъёма 60 и выпечки 30 минут программа выводит `Start: 6:00`, "
               "`Total: 105 min = 1.75 h`, `Ready: 7 h 45 min`."],
        hint="`int(\"05\")` даёт число `5`, а строки `start_h` и `start_m` в первой строке склеивай как есть. "
             "Вычисления можно писать прямо в фигурных скобках: `f\"{{finish // 60}}\"`.",
        solution='print("Start: " + start_h + ":" + start_m)\ntotal = rise + bake\ntotal += 15\n'
                 'finish = int(start_h) * 60 + int(start_m) + total\n'
                 'print(f"Total: {total} min = {total / 60} h")\nprint(f"Ready: {finish // 60} h {finish % 60} min")',
        wrong=[("забыты 15 минут остывания",
                'print("Start: " + start_h + ":" + start_m)\ntotal = rise + bake\n'
                'finish = int(start_h) * 60 + int(start_m) + total\n'
                'print(f"Total: {total} min = {total / 60} h")\nprint(f"Ready: {finish // 60} h {finish % 60} min")'),
               ("часы начала не переведены в минуты",
                'print("Start: " + start_h + ":" + start_m)\ntotal = rise + bake\ntotal += 15\n'
                'finish = int(start_h) + int(start_m) + total\n'
                'print(f"Total: {total} min = {total / 60} h")\nprint(f"Ready: {finish // 60} h {finish % 60} min")'),
               ("часы готовности посчитаны через / — получается дробь",
                'print("Start: " + start_h + ":" + start_m)\ntotal = rise + bake\ntotal += 15\n'
                'finish = int(start_h) * 60 + int(start_m) + total\n'
                'print(f"Total: {total} min = {total / 60} h")\nprint(f"Ready: {finish / 60} h {finish % 60} min")')],
        must_use=MUST,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att11-loyalty-card", title="Бонусная карта магазина",
        given=["card", "total", "points"],
        variants=[{"card": '"4821"', "total": '"1847"', "points": "120"}],
        hidden=[{"card": '"0007"', "total": '"99"', "points": "0"},
                {"card": '"5310"', "total": '"2500"', "points": "35"},
                {"card": '"9999"', "total": '"100"', "points": "10"},
                {"card": '"1204"', "total": '"3456"', "points": "999"}],
        intro="Касса продуктового магазина печатает отчёт по бонусной карте. Последние цифры карты — `card = {card}`, "
              "сумма покупки пришла из кассы строкой: `total = {total}` руб. На карте уже `points = {points}` баллов. "
              "За каждые полные 100 руб. покупки начисляется 5 баллов, а ещё возвращается кешбэк 3% от суммы.",
        steps=["Склей через `+` строку `Card **** ` и `card` и выведи, например `Card **** 0007`.",
               "Преврати `total` в целое число и сохрани в `spent`.",
               "Посчитай бонус: `spent`, делённое нацело на 100, умножь на 5 и сохрани в `bonus`. "
               "Прибавь бонус к `points` с помощью `+=`.",
               "Посчитай кешбэк `cashback`: `spent * 3 / 100` — и сколько рублей не хватает до следующей полной сотни, "
               "`to_next`: 100 минус остаток от деления `spent` на 100.",
               "С помощью f-строк выведи `Purchase: <spent> rub`, `Bonus: +<bonus>, points: <points>`, "
               "`Cashback: <cashback> rub` и `To next 100: <to_next> rub`. "
               "Например, для покупки на 250 руб. и 10 баллов — `Purchase: 250 rub`, `Bonus: +10, points: 20`, "
               "`Cashback: 7.5 rub`, `To next 100: 50 rub`."],
        hint="`card` — строка, поэтому `\"Card **** \" + card` склеится без `str()`, и нули в начале сохранятся. "
             "`1847 // 100` даёт `18` полных сотен, а `1847 % 100` — `47` рублей сверх них.",
        solution='print("Card **** " + card)\nspent = int(total)\nbonus = spent // 100 * 5\npoints += bonus\n'
                 'cashback = spent * 3 / 100\nto_next = 100 - spent % 100\nprint(f"Purchase: {spent} rub")\n'
                 'print(f"Bonus: +{bonus}, points: {points}")\nprint(f"Cashback: {cashback} rub")\n'
                 'print(f"To next 100: {to_next} rub")',
        wrong=[("баллы не умножены на 5 — по баллу за сотню",
                'print("Card **** " + card)\nspent = int(total)\nbonus = spent // 100\npoints += bonus\n'
                'cashback = spent * 3 / 100\nto_next = 100 - spent % 100\nprint(f"Purchase: {spent} rub")\n'
                'print(f"Bonus: +{bonus}, points: {points}")\nprint(f"Cashback: {cashback} rub")\n'
                'print(f"To next 100: {to_next} rub")'),
               ("до следующей сотни выводит сам остаток",
                'print("Card **** " + card)\nspent = int(total)\nbonus = spent // 100 * 5\npoints += bonus\n'
                'cashback = spent * 3 / 100\nto_next = spent % 100\nprint(f"Purchase: {spent} rub")\n'
                'print(f"Bonus: +{bonus}, points: {points}")\nprint(f"Cashback: {cashback} rub")\n'
                'print(f"To next 100: {to_next} rub")'),
               ("бонус затирает старые баллы вместо того, чтобы прибавиться",
                'print("Card **** " + card)\nspent = int(total)\nbonus = spent // 100 * 5\npoints = bonus\n'
                'cashback = spent * 3 / 100\nto_next = 100 - spent % 100\nprint(f"Purchase: {spent} rub")\n'
                'print(f"Bonus: +{bonus}, points: {points}")\nprint(f"Cashback: {cashback} rub")\n'
                'print(f"To next 100: {to_next} rub")')],
        must_use=MUST,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att11-jam-jars", title="Варенье по банкам",
        given=["name", "berries", "jar", "gift"],
        variants=[{"name": '"Cherry"', "berries": '"3.5"', "jar": "400", "gift": "2"}],
        hidden=[{"name": '"Raspberry"', "berries": '"2.0"', "jar": "500", "gift": "1"},
                {"name": '"Plum"', "berries": '"1.25"', "jar": "250", "gift": "3"},
                {"name": '"Apricot"', "berries": '"4.5"', "jar": "700", "gift": "0"},
                {"name": '"Currant"', "berries": '"0.5"', "jar": "300", "gift": "1"}],
        intro="Мама варит варенье `name = {name}`. Ягоды взвесили на кухонных весах, вес в килограммах записан строкой: "
              "`berries = {berries}`. Сахара кладут вдвое меньше, чем ягод. Варенье разливают в банки по "
              "`jar = {jar}` г, и `gift = {gift}` банки сразу отдают бабушке.",
        steps=["Склей через `+` `name` и строку ` jam` и выведи, например `Plum jam`.",
               "Преврати `berries` в дробное число с помощью `float()` и сохрани в `kg`. Сахар — `kg / 2`, "
               "сохрани в `sugar`.",
               "Посчитай вес варенья в граммах: `(kg + sugar) * 1000`, преврати его в целое число с помощью `int()` "
               "и сохрани в `jam`.",
               "Посчитай, сколько банок заполнится целиком (`jam`, делённое нацело на `jar`), — это `jars`, и сколько граммов "
               "останется в кастрюле (остаток от деления) — это `left`.",
               "С помощью f-строк выведи `Berries: <kg> kg, sugar: <sugar> kg`, `Jam: <jam> g` и "
               "`Jars: <jars>, left in the pot: <left> g`.",
               "Отними от числа банок подарок бабушке с помощью `-=` и выведи `Jars for us: <jars>`. "
               "Например, для `\"2.0\"` кг ягод, банок по 500 г и одной банки бабушке программа выводит "
               "`Berries: 2.0 kg, sugar: 1.0 kg`, `Jam: 3000 g`, `Jars: 6, left in the pot: 0 g`, `Jars for us: 5`."],
        hint="`float(\"3.5\")` даёт число `3.5`, а `int(5250.0)` — целое `5250`. "
             "Строка с банками для бабушки печатается после `-=`, а строка `Jars: ...` — до него.",
        solution='print(name + " jam")\nkg = float(berries)\nsugar = kg / 2\njam = int((kg + sugar) * 1000)\n'
                 'jars = jam // jar\nleft = jam % jar\nprint(f"Berries: {kg} kg, sugar: {sugar} kg")\n'
                 'print(f"Jam: {jam} g")\nprint(f"Jars: {jars}, left in the pot: {left} g")\njars -= gift\n'
                 'print(f"Jars for us: {jars}")',
        wrong=[("сахара положено вдвое больше вместо вдвое меньше",
                'print(name + " jam")\nkg = float(berries)\nsugar = kg * 2\njam = int((kg + sugar) * 1000)\n'
                'jars = jam // jar\nleft = jam % jar\nprint(f"Berries: {kg} kg, sugar: {sugar} kg")\n'
                'print(f"Jam: {jam} g")\nprint(f"Jars: {jars}, left in the pot: {left} g")\njars -= gift\n'
                'print(f"Jars for us: {jars}")'),
               ("банки бабушке отняты до печати строки Jars",
                'print(name + " jam")\nkg = float(berries)\nsugar = kg / 2\njam = int((kg + sugar) * 1000)\n'
                'jars = jam // jar\nleft = jam % jar\njars -= gift\nprint(f"Berries: {kg} kg, sugar: {sugar} kg")\n'
                'print(f"Jam: {jam} g")\nprint(f"Jars: {jars}, left in the pot: {left} g")\n'
                'print(f"Jars for us: {jars}")'),
               ("забыт сахар в весе варенья",
                'print(name + " jam")\nkg = float(berries)\nsugar = kg / 2\njam = int(kg * 1000)\n'
                'jars = jam // jar\nleft = jam % jar\nprint(f"Berries: {kg} kg, sugar: {sugar} kg")\n'
                'print(f"Jam: {jam} g")\nprint(f"Jars: {jars}, left in the pot: {left} g")\njars -= gift\n'
                'print(f"Jars for us: {jars}")')],
        must_use=MUST,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att11-coffee-shift", title="Смена в кофейне",
        given=["cups", "price", "rent", "beans"],
        variants=[{"cups": '"48"', "price": "180", "rent": "2500", "beans": "9"}],
        hidden=[{"cups": '"100"', "price": "150", "rent": "3000", "beans": "8"},
                {"cups": '"15"', "price": "200", "rent": "2500", "beans": "10"},
                {"cups": '"125"', "price": "120", "rent": "5000", "beans": "12"},
                {"cups": '"30"', "price": "250", "rent": "1000", "beans": "7"}],
        intro="Бариста закрывает смену в кофейне. Касса выдала число проданных чашек строкой: `cups = {cups}`. "
              "Чашка кофе стоит `price = {price}` руб., аренда точки за день — `rent = {rent}` руб., "
              "на одну чашку уходит `beans = {beans}` г зёрен. Зёрна продаются пачками по 250 г.",
        steps=["Склей через `+` строку `Cups sold: ` и `cups` и выведи, например `Cups sold: 15`.",
               "Преврати `cups` в целое число и сохрани в `sold`. Посчитай выручку `income` — `sold`, умноженное "
               "на `price`, — и вычти из неё аренду с помощью `-=`.",
               "Посчитай расход зёрен в граммах `used` (`sold` умножить на `beans`) и в килограммах `kg` (`used / 1000`).",
               "Посчитай, сколько целых пачек по 250 г ушло, `packs` (`used`, делённое нацело на 250), и сколько граммов "
               "взяли из следующей пачки, `rest` (остаток от деления на 250).",
               "С помощью f-строк выведи `Income: <income> rub`, `Beans: <kg> kg` и "
               "`Packs: <packs> full + <rest> g`. Например, для 15 чашек по 200 руб., аренды 2500 руб. и "
               "10 г на чашку — `Income: 500 rub`, `Beans: 0.15 kg`, `Packs: 0 full + 150 g`."],
        hint="`cups` — строка: в первую строку её можно приклеить как есть, а умножать надо `int(cups)`. "
             "`income -= rent` — то же, что `income = income - rent`.",
        solution='print("Cups sold: " + cups)\nsold = int(cups)\nincome = sold * price\nincome -= rent\n'
                 'used = sold * beans\nkg = used / 1000\npacks = used // 250\nrest = used % 250\n'
                 'print(f"Income: {income} rub")\nprint(f"Beans: {kg} kg")\nprint(f"Packs: {packs} full + {rest} g")',
        wrong=[("забыта аренда",
                'print("Cups sold: " + cups)\nsold = int(cups)\nincome = sold * price\n'
                'used = sold * beans\nkg = used / 1000\npacks = used // 250\nrest = used % 250\n'
                'print(f"Income: {income} rub")\nprint(f"Beans: {kg} kg")\nprint(f"Packs: {packs} full + {rest} g")'),
               ("пачки посчитаны через / — получается дробь",
                'print("Cups sold: " + cups)\nsold = int(cups)\nincome = sold * price\nincome -= rent\n'
                'used = sold * beans\nkg = used / 1000\npacks = used / 250\nrest = used % 250\n'
                'print(f"Income: {income} rub")\nprint(f"Beans: {kg} kg")\nprint(f"Packs: {packs} full + {rest} g")'),
               ("килограммы посчитаны через // — граммы теряются",
                'print("Cups sold: " + cups)\nsold = int(cups)\nincome = sold * price\nincome -= rent\n'
                'used = sold * beans\nkg = used // 1000\npacks = used // 250\nrest = used % 250\n'
                'print(f"Income: {income} rub")\nprint(f"Beans: {kg} kg")\nprint(f"Packs: {packs} full + {rest} g")')],
        must_use=MUST,
    ),
]
