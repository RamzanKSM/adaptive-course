"""PY_COMPARISON_OPERATORS — «Операторы сравнения». Taught before: print, variables, arithmetic, int/float, strings,
type conversion, // and %, += -=, f-strings, if/else.
Not yet: and/or/not, elif, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_COMPARISON_OPERATORS"
CMP = [("Compare", "Используй операторы сравнения: ==, !=, <, >, <=, >=")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-cmp-exam-score", title="Результат экзамена",
        given=["score", "last"],
        variants=[{"score": "72", "last": "65"}, {"score": "60", "last": "81"}, {"score": "100", "last": "100"}],
        hidden=[{"score": "59", "last": "59"}, {"score": "60", "last": "60"}, {"score": "88", "last": "90"},
                {"score": "100", "last": "40"}],
        intro="После экзамена ученик получил `score = {score}` баллов из 100, а в прошлый раз у него было `last = {last}`. "
              "Экзамен сдан, если набрано 60 баллов или больше.",
        steps=["Выведи через `print` с запятой `Passed:` и результат сравнения: набрано ли 60 или больше.",
               "Выведи `Perfect:` и результат сравнения: равен ли `score` ровно 100.",
               "Выведи `Better:` и результат сравнения: больше ли `score`, чем `last`.",
               "Выведи `Same:` и результат сравнения: равен ли `score` значению `last`.",
               "Например, для 59 и 59 баллов программа выводит `Passed: False`, `Perfect: False`, `Better: False`, "
               "`Same: True`."],
        hint="Сравнение само по себе — это значение `True` или `False`, его можно сразу напечатать: "
             "`print(\"Big:\", x > 10)`. «60 или больше» — это `>=`, а проверка на равенство — двойное `==`.",
        solution='print("Passed:", score >= 60)\nprint("Perfect:", score == 100)\nprint("Better:", score > last)\n'
                 'print("Same:", score == last)',
        wrong=[("строгое сравнение: ровно 60 баллов не считается сдачей",
                'print("Passed:", score > 60)\nprint("Perfect:", score == 100)\nprint("Better:", score > last)\n'
                'print("Same:", score == last)'),
               ("!= вместо == в последней строке",
                'print("Passed:", score >= 60)\nprint("Perfect:", score == 100)\nprint("Better:", score > last)\n'
                'print("Same:", score != last)')],
        must_use=CMP,
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-cmp-lift-load", title="Перегруз лифта",
        given=["weight"],
        variants=[{"weight": "320"}, {"weight": "455"}, {"weight": "400"}],
        hidden=[{"weight": "399"}, {"weight": "401"}, {"weight": "400"}, {"weight": "0"}],
        intro="Лифт выдерживает 400 кг. Датчик измерил, сколько весят люди в кабине: `weight = {weight}` кг. "
              "Табло лифта показывает несколько строк.",
        steps=["Выведи `Load:`, `weight` и `kg` через `print` с запятыми.",
               "Выведи `Overload:` и результат сравнения: больше ли вес, чем 400.",
               "Выведи `Full:` и результат сравнения: равен ли вес ровно 400.",
               "Выведи `Room left:` и результат сравнения: меньше ли вес, чем 400.",
               "Например, для 400 кг программа выводит `Load: 400 kg`, `Overload: False`, `Full: True`, `Room left: False`."],
        hint="Ровно 400 кг — это ещё не перегруз: «больше» — это `>`, а не `>=`. "
             "Проверка на равенство пишется двумя знаками `==`: один знак `=` — это присваивание.",
        solution='print("Load:", weight, "kg")\nprint("Overload:", weight > 400)\nprint("Full:", weight == 400)\n'
                 'print("Room left:", weight < 400)',
        wrong=[(">= вместо >: ровно 400 кг считается перегрузом",
                'print("Load:", weight, "kg")\nprint("Overload:", weight >= 400)\nprint("Full:", weight == 400)\n'
                'print("Room left:", weight < 400)'),
               ("<= вместо <: при ровно 400 кг будто есть место",
                'print("Load:", weight, "kg")\nprint("Overload:", weight > 400)\nprint("Full:", weight == 400)\n'
                'print("Room left:", weight <= 400)')],
        must_use=CMP,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-cmp-new-password", title="Смена пароля",
        given=["old", "password", "confirm"],
        variants=[{"old": '"cat2020"', "password": '"sun_rise7"', "confirm": '"sun_rise7"'},
                  {"old": '"qwerty"', "password": '"qwerty"', "confirm": '"qwerty"'},
                  {"old": '"blue42"', "password": '"green42"', "confirm": '"Green42"'}],
        hidden=[{"old": '"a1"', "password": '"b2"', "confirm": '"b2"'}, {"old": '"same"', "password": '"same"', "confirm": '"sam"'},
                {"old": '"x"', "password": '"y"', "confirm": '"z"'}, {"old": '"pass"', "password": '"pass"', "confirm": '"pass"'}],
        intro="Пользователь меняет пароль на сайте. Старый пароль — `old = {old}`, новый — `password = {password}`, "
              "а для проверки новый пароль введён ещё раз: `confirm = {confirm}`. Строки сравниваются с учётом "
              "больших и маленьких букв.",
        steps=["Выведи через `print` с запятой `Match:` и результат сравнения: совпадают ли `password` и `confirm`.",
               "Выведи `Changed:` и результат сравнения: отличается ли `password` от `old` (оператор `!=`).",
               "Если `password` равен `confirm`, выведи `Saved`, иначе выведи `Try again`.",
               "Например, для `old = \"a1\"`, `password = \"b2\"`, `confirm = \"b2\"` программа выводит `Match: True`, "
               "`Changed: True`, `Saved`."],
        hint="Строки сравниваются так же, как числа: `\"abc\" == \"abc\"` даёт `True`, а `\"Abc\" == \"abc\"` — `False`. "
             "Оператор `!=` значит «не равно».",
        solution='print("Match:", password == confirm)\nprint("Changed:", password != old)\nif password == confirm:\n'
                 '    print("Saved")\nelse:\n    print("Try again")',
        wrong=[("== вместо != : проверяет, что пароль НЕ изменился",
                'print("Match:", password == confirm)\nprint("Changed:", password == old)\nif password == confirm:\n'
                '    print("Saved")\nelse:\n    print("Try again")'),
               ("в условии != вместо ==: ветки срабатывают наоборот",
                'print("Match:", password == confirm)\nprint("Changed:", password != old)\nif password != confirm:\n'
                '    print("Saved")\nelse:\n    print("Try again")')],
        constructs=["if"],
        must_use=CMP,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-cmp-two-shops", title="Где дешевле",
        given=["price_a", "price_b", "budget"],
        variants=[{"price_a": "1290", "price_b": "1150", "budget": "1500"},
                  {"price_a": "780", "price_b": "845", "budget": "700"},
                  {"price_a": "2400", "price_b": "2600", "budget": "2400"}],
        hidden=[{"price_a": "500", "price_b": "500", "budget": "500"}, {"price_a": "999", "price_b": "1000", "budget": "998"},
                {"price_a": "300", "price_b": "250", "budget": "1000"}, {"price_a": "70", "price_b": "60", "budget": "60"}],
        intro="Аня хочет купить наушники. В первом магазине они стоят `price_a = {price_a}` руб., во втором — "
              "`price_b = {price_b}` руб. У Ани есть `budget = {budget}` руб.",
        steps=["Если `price_a` меньше или равна `price_b`, положи в переменную `best` цену `price_a`, иначе — `price_b`.",
               "Выведи `Best price:` и `best` через `print` с запятой.",
               "Выведи `Fits budget:` и результат сравнения: хватает ли денег, то есть меньше ли `best` бюджета или равна ему.",
               "Выведи `Difference:` и разность бюджета и `best` (она может быть отрицательной).",
               "Например, для цен 300 и 250 и бюджета 1000 программа выводит `Best price: 250`, `Fits budget: True`, "
               "`Difference: 750`."],
        hint="«Меньше или равно» — это `<=`. Если цена ровно равна бюджету, денег хватает. "
             "Сначала найди лучшую цену в `if`/`else`, а потом печатай три строки.",
        solution='if price_a <= price_b:\n    best = price_a\nelse:\n    best = price_b\nprint("Best price:", best)\n'
                 'print("Fits budget:", best <= budget)\nprint("Difference:", budget - best)',
        wrong=[("строгое сравнение: если цена равна бюджету, денег будто не хватает",
                'if price_a <= price_b:\n    best = price_a\nelse:\n    best = price_b\nprint("Best price:", best)\n'
                'print("Fits budget:", best < budget)\nprint("Difference:", budget - best)'),
               ("знак сравнения перевёрнут — выбирается более дорогой магазин",
                'if price_a >= price_b:\n    best = price_a\nelse:\n    best = price_b\nprint("Best price:", best)\n'
                'print("Fits budget:", best <= budget)\nprint("Difference:", budget - best)')],
        constructs=["if"],
        must_use=CMP,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-cmp-taxi-or-bus", title="Такси или автобус",
        given=["people", "ticket", "taxi_price"],
        variants=[{"people": "3", "ticket": "60", "taxi_price": "450"}, {"people": "4", "ticket": "55", "taxi_price": "390"},
                  {"people": "2", "ticket": "70", "taxi_price": "200"}],
        hidden=[{"people": "5", "ticket": "50", "taxi_price": "250"}, {"people": "1", "ticket": "45", "taxi_price": "600"},
                {"people": "6", "ticket": "65", "taxi_price": "300"}, {"people": "3", "ticket": "40", "taxi_price": "130"}],
        intro="Компания друзей едет в аквапарк и обратно. На автобусе билет стоит `ticket = {ticket}` руб. на человека "
              "в одну сторону, друзей `people = {people}`. Такси в одну сторону стоит `taxi_price = {taxi_price}` руб. "
              "на всю компанию. Нужно выбрать, на чём ехать туда и обратно.",
        steps=["Посчитай стоимость автобуса туда и обратно для всех: `people * ticket * 2` — и сохрани в `bus`.",
               "Посчитай стоимость такси туда и обратно: `taxi_price * 2` — и сохрани в `taxi`.",
               "С помощью f-строк выведи `Bus: <bus> rub`, `Taxi: <taxi> rub` и `Same cost: <True/False>` — "
               "результат сравнения `bus == taxi`.",
               "Если такси строго дешевле автобуса, выведи `Take a taxi, save <bus - taxi> rub`, иначе выведи "
               "`Take the bus, save <taxi - bus> rub`.",
               "Например, для 5 человек, билета 50 руб. и такси 250 руб. программа выводит `Bus: 500 rub`, "
               "`Taxi: 500 rub`, `Same cost: True`, `Take the bus, save 0 rub`."],
        hint="В f-строку можно вставить и сравнение, и разность: `f\"Same cost: {{bus == taxi}}\"`. "
             "Если цены равны, условие «такси строго дешевле» (`<`) ложно — выбирается автобус.",
        solution='bus = people * ticket * 2\ntaxi = taxi_price * 2\nprint(f"Bus: {bus} rub")\nprint(f"Taxi: {taxi} rub")\n'
                 'print(f"Same cost: {bus == taxi}")\nif taxi < bus:\n    print(f"Take a taxi, save {bus - taxi} rub")\n'
                 'else:\n    print(f"Take the bus, save {taxi - bus} rub")',
        wrong=[("знак перевёрнут: выбирает более дорогой вариант, экономия отрицательная",
                'bus = people * ticket * 2\ntaxi = taxi_price * 2\nprint(f"Bus: {bus} rub")\nprint(f"Taxi: {taxi} rub")\n'
                'print(f"Same cost: {bus == taxi}")\nif taxi > bus:\n    print(f"Take a taxi, save {bus - taxi} rub")\n'
                'else:\n    print(f"Take the bus, save {taxi - bus} rub")'),
               ("забывает про дорогу обратно на автобусе",
                'bus = people * ticket\ntaxi = taxi_price * 2\nprint(f"Bus: {bus} rub")\nprint(f"Taxi: {taxi} rub")\n'
                'print(f"Same cost: {bus == taxi}")\nif taxi < bus:\n    print(f"Take a taxi, save {bus - taxi} rub")\n'
                'else:\n    print(f"Take the bus, save {taxi - bus} rub")'),
               ("<= вместо <: при равной цене выбирает такси",
                'bus = people * ticket * 2\ntaxi = taxi_price * 2\nprint(f"Bus: {bus} rub")\nprint(f"Taxi: {taxi} rub")\n'
                'print(f"Same cost: {bus == taxi}")\nif taxi <= bus:\n    print(f"Take a taxi, save {bus - taxi} rub")\n'
                'else:\n    print(f"Take the bus, save {taxi - bus} rub")')],
        constructs=["if"],
        must_use=CMP,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-cmp-room-heating", title="Обогреватель в комнате",
        given=["current", "target", "speed"],
        variants=[{"current": "17", "target": "22", "speed": "6"}, {"current": "24", "target": "21", "speed": "5"},
                  {"current": "12", "target": "20", "speed": "4"}],
        hidden=[{"current": "20", "target": "20", "speed": "3"}, {"current": "19", "target": "20", "speed": "10"},
                {"current": "26", "target": "18", "speed": "7"}, {"current": "5", "target": "23", "speed": "2"}],
        intro="Умный обогреватель сравнивает температуру в комнате `current = {current}` с желаемой `target = {target}` "
              "градусов. На каждый градус нагрева у него уходит `speed = {speed}` минут.",
        steps=["Посчитай, на сколько градусов нужно нагреть комнату: `target - current` — и сохрани в `diff`.",
               "С помощью f-строк выведи `Need heating: <True/False>` — меньше ли `current`, чем `target`, "
               "и `Already warm: <True/False>` — больше ли `current`, чем `target`, или равна ей.",
               "Если `current` меньше `target`, выведи `Heat by <diff> degrees` и `Time: <diff * speed> min`.",
               "Иначе выведи одну строку `Heating off`.",
               "Например, для 19, 20 и 10 программа выводит `Need heating: True`, `Already warm: False`, "
               "`Heat by 1 degrees`, `Time: 10 min`."],
        hint="«Больше или равно» — это `>=`. Если температура уже равна желаемой, греть не нужно: "
             "условие `current < target` ложно, и выполняется `else`.",
        solution='diff = target - current\nprint(f"Need heating: {current < target}")\n'
                 'print(f"Already warm: {current >= target}")\nif current < target:\n'
                 '    print(f"Heat by {diff} degrees")\n    print(f"Time: {diff * speed} min")\nelse:\n    print("Heating off")',
        wrong=[("<= вместо <: при равной температуре включает нагрев на 0 градусов",
                'diff = target - current\nprint(f"Need heating: {current < target}")\n'
                'print(f"Already warm: {current >= target}")\nif current <= target:\n'
                '    print(f"Heat by {diff} degrees")\n    print(f"Time: {diff * speed} min")\nelse:\n    print("Heating off")'),
               ("вычитает в обратном порядке — разница отрицательная",
                'diff = current - target\nprint(f"Need heating: {current < target}")\n'
                'print(f"Already warm: {current >= target}")\nif current < target:\n'
                '    print(f"Heat by {diff} degrees")\n    print(f"Time: {diff * speed} min")\nelse:\n    print("Heating off")')],
        constructs=["if"],
        must_use=CMP,
    ),
]
