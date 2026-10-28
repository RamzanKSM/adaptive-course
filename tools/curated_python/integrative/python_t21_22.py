"""Integrative tasks (3rd iteration), Python, topics 21 PY_LOOP_CONTROL («break и continue») and 22 PY_LOOP_TERMINATION
(«Завершение цикла»). Each task has its topic at the core and 1–2 earlier topics doing real work:
- break/continue: a search stopped by break with a found flag and `not` (+ %, and), boarding stopped by break
  (+ % for odd/even, if/else, accumulator), continue over digits taken with % and // (+ accumulator, f-strings);
- loop termination: change given coin by coin with an elif chain (+ int() of a string), a while with two conditions
  joined by and (+ if/else after the loop), a while whose step grows every time (+ +=, an elif rating).
Not yet: lists, string indexing, slicing and methods, functions, for … else.
Theme domains: quizzes, queues and elevators, robots and sensors, vending machines."""
from build import OutputTask

LOOP_CONTROL = "PY_LOOP_CONTROL"
LOOP_TERMINATION = "PY_LOOP_TERMINATION"

TASKS = [
    # ───────── 21. break и continue ─────────
    OutputTask(
        skill=LOOP_CONTROL, difficulty=3, slug="py-int-loopctl-candy-riddle", title="Загадка про конфеты",
        given=["a", "ra", "b", "rb", "limit"],
        variants=[{"a": "4", "ra": "3", "b": "7", "rb": "2", "limit": "60"}],
        hidden=[{"a": "3", "ra": "2", "b": "5", "rb": "3", "limit": "50"},
                {"a": "4", "ra": "3", "b": "6", "rb": "5", "limit": "11"},
                {"a": "2", "ra": "1", "b": "4", "rb": "2", "limit": "30"},
                {"a": "7", "ra": "1", "b": "9", "rb": "2", "limit": "20"},
                {"a": "3", "ra": "0", "b": "4", "rb": "1", "limit": "40"}],
        intro="В детской викторине есть загадка: «В коробке не больше `limit = {limit}` конфет. Если раздать их по "
              "`a = {a}` штуки, останется `ra = {ra}`, а если по `b = {b}` штук — останется `rb = {rb}`. "
              "Сколько конфет в коробке?» Подходящих чисел может быть несколько, а может не оказаться ни одного. "
              "Ведущий проверяет загадку программой: нужно найти самое маленькое подходящее число.",
        steps=["Заведи переменную `found = False` — нашёлся ли ответ.",
               "Перебери циклом `for` числа `n` от 1 до `limit` включительно.",
               "Если остаток от деления `n` на `a` равен `ra` и остаток от деления `n` на `b` равен `rb`, выведи "
               "строку вида `Answer: 23`, запиши `found = True` и сразу останови перебор командой `break`.",
               "После цикла, если ответ так и не нашёлся (`not found`), выведи строку вида `No answer up to 50`."],
        hint="Без `break` цикл продолжит перебор и выведет все подходящие числа, а нужно только первое — самое маленькое. "
             "Число `limit` тоже надо проверить, поэтому вторая граница `range` — `limit + 1`. Переменная `found` "
             "нужна, чтобы после цикла узнать, нашёлся ли ответ.",
        solution='found = False\nfor n in range(1, limit + 1):\n    if n % a == ra and n % b == rb:\n'
                 '        print(f"Answer: {n}")\n        found = True\n        break\nif not found:\n'
                 '    print(f"No answer up to {limit}")',
        wrong=[("нет break: выводятся все подходящие числа",
                'found = False\nfor n in range(1, limit + 1):\n    if n % a == ra and n % b == rb:\n'
                '        print(f"Answer: {n}")\n        found = True\nif not found:\n'
                '    print(f"No answer up to {limit}")'),
               ("range(1, limit): само число limit не проверяется",
                'found = False\nfor n in range(1, limit):\n    if n % a == ra and n % b == rb:\n'
                '        print(f"Answer: {n}")\n        found = True\n        break\nif not found:\n'
                '    print(f"No answer up to {limit}")'),
               ("or вместо and: хватает одного остатка из двух",
                'found = False\nfor n in range(1, limit + 1):\n    if n % a == ra or n % b == rb:\n'
                '        print(f"Answer: {n}")\n        found = True\n        break\nif not found:\n'
                '    print(f"No answer up to {limit}")'),
               ("строка No answer печатается всегда, без проверки found",
                'for n in range(1, limit + 1):\n    if n % a == ra and n % b == rb:\n'
                '        print(f"Answer: {n}")\n        break\nprint(f"No answer up to {limit}")')],
        constructs=["for", "if"],
        must_use=[("Break", "Используй break, чтобы остановить перебор, когда ответ найден")],
    ),
    OutputTask(
        skill=LOOP_CONTROL, difficulty=3, slug="py-int-loopctl-lift-load", title="Очередь к лифту",
        given=["people", "adult", "child", "limit"],
        variants=[{"people": "7", "adult": "75", "child": "35", "limit": "300"}],
        hidden=[{"people": "3", "adult": "80", "child": "30", "limit": "400"},
                {"people": "6", "adult": "80", "child": "40", "limit": "200"},
                {"people": "5", "adult": "90", "child": "30", "limit": "150"},
                {"people": "8", "adult": "85", "child": "30", "limit": "350"},
                {"people": "1", "adult": "100", "child": "50", "limit": "100"}],
        intro="К лифту в торговом центре выстроилась очередь из `people = {people}` человек — родители с детьми. "
              "Люди с нечётными номерами в очереди (1-й, 3-й, …) — взрослые, каждый весит `adult = {adult}` кг, "
              "а с чётными — дети, по `child = {child}` кг. Лифт выдерживает `limit = {limit}` кг. Заходят строго "
              "по очереди: если человек не помещается, он и все, кто стоит за ним, ждут следующего лифта — "
              "обгонять нельзя.",
        steps=["Заведи вес в лифте `load = 0` и перебери номера людей `n` циклом `for` от 1 до `people` включительно.",
               "Узнай вес человека `weight`: если `n` нечётное (остаток от деления на 2 равен 1), это `adult`, "
               "иначе — `child`.",
               "Если `load + weight` больше `limit`, выведи строку вида `Person 6 waits` и останови посадку командой "
               "`break`. Иначе прибавь `weight` к `load` и выведи строку вида `Person 1 in, load 75 kg`.",
               "После цикла выведи строку вида `Lift goes up with 295 kg`."],
        hint="Ровно `limit` кг лифт ещё выдерживает, поэтому сравнение строгое: `>`. `continue` здесь не подходит: "
             "он пропустил бы взрослого, а лёгкого ребёнка за ним пустил бы вперёд. Если поместились все, цикл "
             "закончится сам и строки про ожидание не будет.",
        solution='load = 0\nfor n in range(1, people + 1):\n    if n % 2 == 1:\n        weight = adult\n    else:\n'
                 '        weight = child\n    if load + weight > limit:\n        print(f"Person {n} waits")\n'
                 '        break\n    load += weight\n    print(f"Person {n} in, load {load} kg")\n'
                 'print(f"Lift goes up with {load} kg")',
        wrong=[("continue вместо break: лёгкий ребёнок обгоняет взрослого",
                'load = 0\nfor n in range(1, people + 1):\n    if n % 2 == 1:\n        weight = adult\n    else:\n'
                '        weight = child\n    if load + weight > limit:\n        print(f"Person {n} waits")\n'
                '        continue\n    load += weight\n    print(f"Person {n} in, load {load} kg")\n'
                'print(f"Lift goes up with {load} kg")'),
               ("нестрогое сравнение: при весе ровно limit человек не заходит",
                'load = 0\nfor n in range(1, people + 1):\n    if n % 2 == 1:\n        weight = adult\n    else:\n'
                '        weight = child\n    if load + weight >= limit:\n        print(f"Person {n} waits")\n'
                '        break\n    load += weight\n    print(f"Person {n} in, load {load} kg")\n'
                'print(f"Lift goes up with {load} kg")'),
               ("перепутаны взрослые и дети: чётные номера считаются взрослыми",
                'load = 0\nfor n in range(1, people + 1):\n    if n % 2 == 0:\n        weight = adult\n    else:\n'
                '        weight = child\n    if load + weight > limit:\n        print(f"Person {n} waits")\n'
                '        break\n    load += weight\n    print(f"Person {n} in, load {load} kg")\n'
                'print(f"Lift goes up with {load} kg")'),
               ("вес прибавлен до проверки: в итог попадает и тот, кто ждёт",
                'load = 0\nfor n in range(1, people + 1):\n    if n % 2 == 1:\n        weight = adult\n    else:\n'
                '        weight = child\n    load += weight\n    if load > limit:\n        print(f"Person {n} waits")\n'
                '        break\n    print(f"Person {n} in, load {load} kg")\n'
                'print(f"Lift goes up with {load} kg")')],
        constructs=["for", "if"],
        must_use=[("Break", "Используй break, чтобы остановить посадку, когда следующий человек не помещается")],
    ),
    OutputTask(
        skill=LOOP_CONTROL, difficulty=3, slug="py-int-loopctl-rain-sensor", title="Датчик дождя на метеостанции",
        given=["hours", "signal"],
        variants=[{"hours": "6", "signal": "30204"}],
        hidden=[{"hours": "4", "signal": "1234"},
                {"hours": "5", "signal": "50"},
                {"hours": "3", "signal": "0"},
                {"hours": "7", "signal": "7000301"},
                {"hours": "2", "signal": "99"}],
        intro="Робот-метеостанция в поле записывает, сколько миллиметров дождя выпало за каждый час, и раз в "
              "`hours = {hours}` часов передаёт на базу одно число `signal = {signal}` — по цифре на час. "
              "Передатчик шлёт цифры задом наперёд: последняя цифра числа — первый час, предпоследняя — второй "
              "и так далее. Цифра 0 значит, что в этот час дождя не было. Нули в начале числа не пишутся, поэтому "
              "цифр может быть меньше, чем часов: недостающие часы — сухие.",
        steps=["Заведи сумму осадков `total = 0` и перебери номера часов `hour` циклом `for` от 1 до `hours` "
               "включительно.",
               "На каждом шаге сначала возьми последнюю цифру `signal` (остаток от деления на 10) в переменную `mm` "
               "и отбрось эту цифру от `signal` (раздели `signal` нацело на 10).",
               "Если `mm` равно 0, пропусти этот час командой `continue`. Иначе прибавь `mm` к `total` и выведи "
               "строку вида `Hour 3: 2 mm`.",
               "После цикла выведи строку вида `Total: 9 mm`."],
        hint="`30204 % 10` даёт 4, а `30204 // 10` — 3020. Отбрасывай цифру до `continue`: команды ниже `continue` "
             "в сухой час не выполняются, и тогда следующий час прочитал бы ту же цифру. Когда цифры кончились, "
             "`signal` равен 0, и все оставшиеся часы дают 0.",
        solution='total = 0\nfor hour in range(1, hours + 1):\n    mm = signal % 10\n    signal //= 10\n'
                 '    if mm == 0:\n        continue\n    total += mm\n    print(f"Hour {hour}: {mm} mm")\n'
                 'print(f"Total: {total} mm")',
        wrong=[("break вместо continue: отчёт обрывается на первом сухом часе",
                'total = 0\nfor hour in range(1, hours + 1):\n    mm = signal % 10\n    signal //= 10\n'
                '    if mm == 0:\n        break\n    total += mm\n    print(f"Hour {hour}: {mm} mm")\n'
                'print(f"Total: {total} mm")'),
               ("цифра отбрасывается после continue: после сухого часа число больше не укорачивается",
                'total = 0\nfor hour in range(1, hours + 1):\n    mm = signal % 10\n    if mm == 0:\n'
                '        continue\n    signal //= 10\n    total += mm\n    print(f"Hour {hour}: {mm} mm")\n'
                'print(f"Total: {total} mm")'),
               ("номер часа считается своим счётчиком только для дождливых часов",
                'total = 0\nhour = 0\nfor step in range(1, hours + 1):\n    mm = signal % 10\n    signal //= 10\n'
                '    if mm == 0:\n        continue\n    hour += 1\n    total += mm\n    print(f"Hour {hour}: {mm} mm")\n'
                'print(f"Total: {total} mm")')],
        constructs=["for", "if"],
        must_use=[("Continue", "Используй continue, чтобы пропустить час без дождя")],
    ),

    # ───────── 22. Завершение цикла ─────────
    OutputTask(
        skill=LOOP_TERMINATION, difficulty=3, slug="py-int-loopend-coin-change", title="Сдача в автомате с напитками",
        given=["price", "paid"],
        variants=[{"price": "82", "paid": '"100"'}],
        hidden=[{"price": "50", "paid": '"50"'},
                {"price": "90", "paid": '"100"'},
                {"price": "45", "paid": '"50"'},
                {"price": "63", "paid": '"100"'},
                {"price": "96", "paid": '"100"'}],
        intro="Автомат продаёт напитки. Выбранный напиток стоит `price = {price}` руб. Купюроприёмник распознал "
              "внесённые деньги и записал сумму строкой: `paid = {paid}`. Сдачу автомат выдаёт по одной монете, "
              "и каждый раз — самой крупной, которая не больше оставшейся сдачи. Монеты в автомате есть только "
              "по 10, 5 и 1 руб.",
        steps=["Преврати `paid` в целое число, отними `price` и сохрани сдачу в `change`. Выведи строку вида "
               "`Change: 18 rub`.",
               "Пока `change` больше 0, выбирай монету `coin`: если `change` не меньше 10, это 10, иначе если "
               "не меньше 5 — 5, иначе — 1.",
               "Выведи монету строкой вида `Coin: 5 rub` и отними её от `change`.",
               "После цикла выведи `Take your drink`."],
        hint="Монету выбирай заново на каждом шаге цикла: сдача уменьшается, и крупная монета может стать для неё "
             "слишком большой. Так сдача каждый раз уменьшается хотя бы на 1 и не уходит в минус, поэтому цикл "
             "остановится ровно на 0. Если сдачи нет, цикл не выполнится ни разу.",
        solution='change = int(paid) - price\nprint(f"Change: {change} rub")\nwhile change > 0:\n'
                 '    if change >= 10:\n        coin = 10\n    elif change >= 5:\n        coin = 5\n    else:\n'
                 '        coin = 1\n    print(f"Coin: {coin} rub")\n    change -= coin\nprint("Take your drink")',
        wrong=[("строгие сравнения: монета 10 не выдаётся при сдаче ровно 10",
                'change = int(paid) - price\nprint(f"Change: {change} rub")\nwhile change > 0:\n'
                '    if change > 10:\n        coin = 10\n    elif change > 5:\n        coin = 5\n    else:\n'
                '        coin = 1\n    print(f"Coin: {coin} rub")\n    change -= coin\nprint("Take your drink")'),
               ("условие change >= 0: после нуля выдаётся лишняя монета",
                'change = int(paid) - price\nprint(f"Change: {change} rub")\nwhile change >= 0:\n'
                '    if change >= 10:\n        coin = 10\n    elif change >= 5:\n        coin = 5\n    else:\n'
                '        coin = 1\n    print(f"Coin: {coin} rub")\n    change -= coin\nprint("Take your drink")'),
               ("монета выбрана один раз до цикла: сдача проскакивает ниже нуля",
                'change = int(paid) - price\nprint(f"Change: {change} rub")\nif change >= 10:\n    coin = 10\n'
                'elif change >= 5:\n    coin = 5\nelse:\n    coin = 1\nwhile change > 0:\n'
                '    print(f"Coin: {coin} rub")\n    change -= coin\nprint("Take your drink")')],
        constructs=["while", "if"],
    ),
    OutputTask(
        skill=LOOP_TERMINATION, difficulty=3, slug="py-int-loopend-robot-vacuum", title="Робот-пылесос и заряд",
        given=["area", "speed", "battery", "use"],
        variants=[{"area": "30", "speed": "4", "battery": "70", "use": "8"}],
        hidden=[{"area": "20", "speed": "5", "battery": "90", "use": "10"},
                {"area": "22", "speed": "5", "battery": "100", "use": "5"},
                {"area": "50", "speed": "6", "battery": "50", "use": "10"},
                {"area": "12", "speed": "3", "battery": "15", "use": "5"},
                {"area": "9", "speed": "3", "battery": "35", "use": "5"}],
        intro="Робот-пылесос убирает комнату: неубранной площади осталось `area = {area}` кв. м. За минуту робот "
              "убирает `speed = {speed}` кв. м и тратит `use = {use}` % заряда, сейчас заряд `battery = {battery}` %. "
              "Робот работает, пока комната не убрана и заряд больше 20 %. Как только заряд стал 20 % или меньше, "
              "робот уезжает на базу, даже если не доубирал.",
        steps=["Заведи счётчик минут `minutes = 0`.",
               "Напиши цикл `while`, который работает, пока `area` больше 0 и при этом `battery` больше 20 — "
               "два условия через `and`.",
               "В цикле прибавь к `minutes` 1, уменьши `area` на `speed`, а `battery` — на `use`.",
               "После цикла выведи строку вида `Minutes: 7, battery: 14%`. Затем, если `area` больше 0, выведи "
               "строку вида `Not cleaned: 2 m2`, а иначе — `Room is clean`."],
        hint="Цикл закончится, когда хотя бы одно из условий станет ложным: комната убрана или заряд упал. За последнюю "
             "минуту робот может убрать больше, чем оставалось, и `area` уйдёт в минус — это тоже убранная комната. "
             "При заряде ровно 20 % робот уже не работает.",
        solution='minutes = 0\nwhile area > 0 and battery > 20:\n    minutes += 1\n    area -= speed\n'
                 '    battery -= use\nprint(f"Minutes: {minutes}, battery: {battery}%")\nif area > 0:\n'
                 '    print(f"Not cleaned: {area} m2")\nelse:\n    print("Room is clean")',
        wrong=[("or вместо and: робот работает, пока верно хотя бы одно условие",
                'minutes = 0\nwhile area > 0 or battery > 20:\n    minutes += 1\n    area -= speed\n'
                '    battery -= use\nprint(f"Minutes: {minutes}, battery: {battery}%")\nif area > 0:\n'
                '    print(f"Not cleaned: {area} m2")\nelse:\n    print("Room is clean")'),
               ("условие battery >= 20: при заряде ровно 20 % робот работает лишнюю минуту",
                'minutes = 0\nwhile area > 0 and battery >= 20:\n    minutes += 1\n    area -= speed\n'
                '    battery -= use\nprint(f"Minutes: {minutes}, battery: {battery}%")\nif area > 0:\n'
                '    print(f"Not cleaned: {area} m2")\nelse:\n    print("Room is clean")'),
               ("после цикла проверка area == 0: площадь в минусе считается неубранной",
                'minutes = 0\nwhile area > 0 and battery > 20:\n    minutes += 1\n    area -= speed\n'
                '    battery -= use\nprint(f"Minutes: {minutes}, battery: {battery}%")\nif area == 0:\n'
                '    print("Room is clean")\nelse:\n    print(f"Not cleaned: {area} m2")')],
        constructs=["while", "if"],
    ),
    OutputTask(
        skill=LOOP_TERMINATION, difficulty=3, slug="py-int-loopend-quiz-blitz", title="Блиц в финале викторины",
        given=["seconds", "first", "extra"],
        variants=[{"seconds": "60", "first": "5", "extra": "4"}],
        hidden=[{"seconds": "60", "first": "6", "extra": "3"},
                {"seconds": "31", "first": "8", "extra": "2"},
                {"seconds": "10", "first": "12", "extra": "1"},
                {"seconds": "45", "first": "4", "extra": "0"},
                {"seconds": "20", "first": "7", "extra": "5"}],
        intro="В финале школьной викторины команда играет блиц: на него даётся `seconds = {seconds}` секунд. "
              "Вопросы становятся всё длиннее: на первый нужно `first = {first}` секунд, а на каждый следующий — "
              "на `extra = {extra}` секунд больше, чем на предыдущий. Команда берёт следующий вопрос, только если "
              "на него хватает оставшегося времени, а когда не хватает — блиц заканчивается.",
        steps=["Заведи счётчик ответов `answered = 0` и время на очередной вопрос `need = first`.",
               "Пока оставшееся время `seconds` не меньше `need`, повторяй: отними `need` от `seconds`, прибавь "
               "к `answered` 1 и увеличь `need` на `extra`.",
               "После цикла выведи строку вида `Answered: 4, unused: 16 s`.",
               "Выведи оценку команды: если ответов 5 или больше — `Rating: gold`, иначе если 3 или больше — "
               "`Rating: silver`, иначе — `Rating: bronze`."],
        hint="Каждый шаг цикла отнимает от `seconds` не меньше `first` секунд, поэтому время когда-нибудь кончится "
             "и цикл остановится. Если времени осталось ровно столько, сколько нужно, вопрос команда ещё берёт — "
             "сравнение `>=`. Время на следующий вопрос увеличивай после того, как отнял время текущего.",
        solution='answered = 0\nneed = first\nwhile seconds >= need:\n    seconds -= need\n    answered += 1\n'
                 '    need += extra\nprint(f"Answered: {answered}, unused: {seconds} s")\nif answered >= 5:\n'
                 '    print("Rating: gold")\nelif answered >= 3:\n    print("Rating: silver")\nelse:\n'
                 '    print("Rating: bronze")',
        wrong=[("строгое сравнение: вопрос, на который времени ровно хватает, не берётся",
                'answered = 0\nneed = first\nwhile seconds > need:\n    seconds -= need\n    answered += 1\n'
                '    need += extra\nprint(f"Answered: {answered}, unused: {seconds} s")\nif answered >= 5:\n'
                '    print("Rating: gold")\nelif answered >= 3:\n    print("Rating: silver")\nelse:\n'
                '    print("Rating: bronze")'),
               ("время на вопрос не растёт: все вопросы по first секунд",
                'answered = 0\nneed = first\nwhile seconds >= need:\n    seconds -= need\n    answered += 1\n'
                'print(f"Answered: {answered}, unused: {seconds} s")\nif answered >= 5:\n'
                '    print("Rating: gold")\nelif answered >= 3:\n    print("Rating: silver")\nelse:\n'
                '    print("Rating: bronze")'),
               ("время на вопрос увеличено до вычитания: первый вопрос стоит first + extra",
                'answered = 0\nneed = first\nwhile seconds >= need:\n    need += extra\n    seconds -= need\n'
                '    answered += 1\nprint(f"Answered: {answered}, unused: {seconds} s")\nif answered >= 5:\n'
                '    print("Rating: gold")\nelif answered >= 3:\n    print("Rating: silver")\nelse:\n'
                '    print("Rating: bronze")'),
               ("строгие границы оценки: 5 ответов — уже не gold",
                'answered = 0\nneed = first\nwhile seconds >= need:\n    seconds -= need\n    answered += 1\n'
                '    need += extra\nprint(f"Answered: {answered}, unused: {seconds} s")\nif answered > 5:\n'
                '    print("Rating: gold")\nelif answered > 3:\n    print("Rating: silver")\nelse:\n'
                '    print("Rating: bronze")')],
        constructs=["while", "if"],
    ),
]
