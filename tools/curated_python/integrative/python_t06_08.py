"""Integrative tasks (the 3rd iteration of a topic), Python, topics 6–8: PY_NUMBER_TYPES, PY_STRING_BASIC,
PY_TYPE_CONVERSION. Each task has its topic at the core and 1–2 earlier topics doing real work: print with sep= / end=,
assignment (a copy keeps the old value), arithmetic with parentheses, order of execution (a variable does not
recalculate by itself), int/float. About 4–5 minutes each, one value set each (key «integ:<slug>»).
Not yet: // and %, += -=, f-strings, round(), string indexing / slices / methods, conditions, loops, lists, functions;
and in PY_NUMBER_TYPES tasks also string gluing, len() and int()/float()/str(), in PY_STRING_BASIC tasks int()/float()/str().
Theme domains: utilities bills, aquarium and pets, trip budgets, printing and stationery."""
from build import OutputTask

NUM = "PY_NUMBER_TYPES"
STR = "PY_STRING_BASIC"
CONV = "PY_TYPE_CONVERSION"

TASKS = [
    # ───────── 6. Числа: int и float ─────────
    OutputTask(
        skill=NUM, difficulty=3, slug="py-int-numbers-electric", title="Свет по новому тарифу",
        given=["old", "new", "rate"],
        variants=[{"old": "3420", "new": "3604", "rate": "6.25"}],
        hidden=[{"old": "1000", "new": "1000", "rate": "5.5"},
                {"old": "2500", "new": "2580", "rate": "7.0"},
                {"old": "980", "new": "1220", "rate": "4.75"},
                {"old": "0", "new": "37", "rate": "8.25"}],
        intro="В прошлом месяце счётчик электричества в квартире Бориса показывал `old = {old}` кВт·ч, а сейчас — "
              "`new = {new}`. Показания — целые числа, а киловатт-час стоит `rate = {rate}` руб. — это дробное число. "
              "С нового года тариф вырастет на 0.5 руб., и Борис хочет узнать, сколько он будет платить за такой же "
              "расход.",
        steps=["Выведи показания одной строкой: `old` и `new` одним `print` с `sep=\" -> \"`, например `3420 -> 3604`.",
               "Посчитай расход `used` — `new` минус `old` — и стоимость `cost` — `used`, умноженный на `rate`. "
               "Выведи `Used:`, `used` и `kWh`, а следующей строкой `Cost:`, `cost` и `rub`.",
               "Тариф растёт: присвой `rate` новое значение `rate + 0.5`. Посчитай `new_cost` — тот же расход по новому "
               "тарифу — и выведи `New cost:`, `new_cost` и `rub`.",
               "Последней строкой выведи `Difference:`, разницу `new_cost - cost` и `rub`. Например, для расхода 10 кВт·ч "
               "по 5.0 руб. строки после показаний — `Used: 10 kWh`, `Cost: 50.0 rub`, `New cost: 55.0 rub` и "
               "`Difference: 5.0 rub`."],
        hint="`used` — разность целых чисел, поэтому печатается без точки. А целое, умноженное на дробное, даёт `float`: "
             "`184 * 6.25` — это `1150.0`. Переменная `cost` не пересчитывается сама, когда меняется `rate`: "
             "новую стоимость нужно посчитать отдельной строкой уже после нового тарифа.",
        solution='print(old, new, sep=" -> ")\nused = new - old\ncost = used * rate\nprint("Used:", used, "kWh")\n'
                 'print("Cost:", cost, "rub")\nrate = rate + 0.5\nnew_cost = used * rate\n'
                 'print("New cost:", new_cost, "rub")\nprint("Difference:", new_cost - cost, "rub")',
        wrong=[("не пересчитывает стоимость после смены тарифа — думает, что `cost` обновился сам",
                'print(old, new, sep=" -> ")\nused = new - old\ncost = used * rate\nprint("Used:", used, "kWh")\n'
                'print("Cost:", cost, "rub")\nrate = rate + 0.5\nnew_cost = cost\n'
                'print("New cost:", new_cost, "rub")\nprint("Difference:", new_cost - cost, "rub")'),
               ("прибавляет 0.5 руб. ко всему счёту, а не к цене каждого киловатт-часа",
                'print(old, new, sep=" -> ")\nused = new - old\ncost = used * rate\nprint("Used:", used, "kWh")\n'
                'print("Cost:", cost, "rub")\nrate = rate + 0.5\nnew_cost = cost + 0.5\n'
                'print("New cost:", new_cost, "rub")\nprint("Difference:", new_cost - cost, "rub")'),
               ("забывает sep — показания печатаются через пробел",
                'print(old, new)\nused = new - old\ncost = used * rate\nprint("Used:", used, "kWh")\n'
                'print("Cost:", cost, "rub")\nrate = rate + 0.5\nnew_cost = used * rate\n'
                'print("New cost:", new_cost, "rub")\nprint("Difference:", new_cost - cost, "rub")')],
    ),
    OutputTask(
        skill=NUM, difficulty=3, slug="py-int-numbers-aquarium", title="Новый аквариум",
        given=["length", "width", "height", "fish"],
        variants=[{"length": "60", "width": "30", "height": "40", "fish": "12"}],
        hidden=[{"length": "40", "width": "25", "height": "30", "fish": "5"},
                {"length": "100", "width": "40", "height": "50", "fish": "30"},
                {"length": "50", "width": "20", "height": "25", "fish": "8"},
                {"length": "45", "width": "30", "height": "35", "fish": "1"}],
        intro="Мила купила аквариум: длина `length = {length}` см, ширина `width = {width}` см, высота "
              "`height = {height}` см. Воду наливают не до краёв, а на 5 см ниже верха. В аквариуме будут жить "
              "`fish = {fish}` рыбок. В одном литре 1000 кубических сантиметров.",
        steps=["Первой строкой выведи размеры в виде `Size: 60x30x40`: сначала напечатай `Size:` с `end=\" \"`, "
               "чтобы строка не закончилась, а потом длину, ширину и высоту одним `print` с `sep=\"x\"`.",
               "Посчитай полный объём `volume` в литрах: перемножь длину, ширину и высоту и раздели на 1000.",
               "Посчитай объём воды `water` так же, но вместо `height` возьми высоту воды `height - 5` (в скобках).",
               "Посчитай, сколько литров воды приходится на одну рыбку: `per_fish` — `water`, делённая на `fish`.",
               "Выведи три строки: `Volume:`, `volume` и `l`; `Water:`, `water` и `l`; `Per fish:`, `per_fish` и `l`. "
               "Например, для аквариума 80x35x45 и 16 рыбок это `Volume: 126.0 l`, `Water: 112.0 l` и `Per fish: 7.0 l`."],
        hint="Деление `/` всегда даёт `float`, даже если делится нацело: `72000 / 1000` — это `72.0`. Скобки в "
             "`(height - 5)` обязательны: без них Python сначала перемножит все размеры, а потом вычтет из произведения "
             "`5 / 1000`.",
        solution='print("Size:", end=" ")\nprint(length, width, height, sep="x")\n'
                 'volume = length * width * height / 1000\nwater = length * width * (height - 5) / 1000\n'
                 'per_fish = water / fish\nprint("Volume:", volume, "l")\nprint("Water:", water, "l")\n'
                 'print("Per fish:", per_fish, "l")',
        wrong=[("забывает скобки вокруг `height - 5`",
                'print("Size:", end=" ")\nprint(length, width, height, sep="x")\n'
                'volume = length * width * height / 1000\nwater = length * width * height - 5 / 1000\n'
                'per_fish = water / fish\nprint("Volume:", volume, "l")\nprint("Water:", water, "l")\n'
                'print("Per fish:", per_fish, "l")'),
               ("на одну рыбку делит полный объём, а не воду",
                'print("Size:", end=" ")\nprint(length, width, height, sep="x")\n'
                'volume = length * width * height / 1000\nwater = length * width * (height - 5) / 1000\n'
                'per_fish = volume / fish\nprint("Volume:", volume, "l")\nprint("Water:", water, "l")\n'
                'print("Per fish:", per_fish, "l")'),
               ("забывает end — размеры уходят на следующую строку",
                'print("Size:")\nprint(length, width, height, sep="x")\n'
                'volume = length * width * height / 1000\nwater = length * width * (height - 5) / 1000\n'
                'per_fish = water / fish\nprint("Volume:", volume, "l")\nprint("Water:", water, "l")\n'
                'print("Per fish:", per_fish, "l")')],
    ),
    OutputTask(
        skill=NUM, difficulty=3, slug="py-int-numbers-sochi", title="Деньги на поездку в Сочи",
        given=["budget", "days", "first"],
        variants=[{"budget": "12000", "days": "5", "first": "3200"}],
        hidden=[{"budget": "10000", "days": "4", "first": "2500"},
                {"budget": "9000", "days": "2", "first": "0"},
                {"budget": "15000", "days": "6", "first": "5000"},
                {"budget": "7000", "days": "8", "first": "700"},
                {"budget": "21000", "days": "3", "first": "12000"}],
        intro="Аня едет в Сочи на `days = {days}` дней. На еду и развлечения у неё `budget = {budget}` руб., и она хочет "
              "тратить каждый день поровну. В первый день она потратила `first = {first}` руб. и пересчитывает, "
              "сколько можно тратить в каждый из оставшихся дней.",
        steps=["Посчитай дневную норму `per_day` — `budget`, делённый на `days`, — и сразу скопируй её в переменную "
               "`plan`: `plan = per_day`.",
               "Посчитай, сколько денег осталось после первого дня, — `left`, и сколько дней осталось без первого, — `days_left`.",
               "Присвой `per_day` новую норму: `left`, делённое на `days_left`.",
               "Выведи четыре строки: `Plan:`, `plan` и `rub`; `Left:`, `left` и `rub`; `New plan:`, `per_day` и `rub`; "
               "`Change:`, разницу `per_day - plan` и `rub`. Например, для 1000 руб. на 2 дня и 600 руб. в первый день "
               "это `Plan: 500.0 rub`, `Left: 400 rub`, `New plan: 400.0 rub` и `Change: -100.0 rub`."],
        hint="`plan = per_day` копирует значение, которое лежит в `per_day` сейчас: когда потом `per_day` получит новое "
             "значение, `plan` останется прежним. Поэтому копию делай до пересчёта. `/` даёт `float` даже при делении "
             "нацело (`12000 / 5` — это `2400.0`), а `left` — разность целых чисел, он печатается без точки.",
        solution='per_day = budget / days\nplan = per_day\nleft = budget - first\ndays_left = days - 1\n'
                 'per_day = left / days_left\nprint("Plan:", plan, "rub")\nprint("Left:", left, "rub")\n'
                 'print("New plan:", per_day, "rub")\nprint("Change:", per_day - plan, "rub")',
        wrong=[("копирует норму в `plan` уже после пересчёта — план совпадает с новой нормой",
                'per_day = budget / days\nleft = budget - first\ndays_left = days - 1\n'
                'per_day = left / days_left\nplan = per_day\nprint("Plan:", plan, "rub")\nprint("Left:", left, "rub")\n'
                'print("New plan:", per_day, "rub")\nprint("Change:", per_day - plan, "rub")'),
               ("делит остаток на все дни, а не на оставшиеся",
                'per_day = budget / days\nplan = per_day\nleft = budget - first\ndays_left = days - 1\n'
                'per_day = left / days\nprint("Plan:", plan, "rub")\nprint("Left:", left, "rub")\n'
                'print("New plan:", per_day, "rub")\nprint("Change:", per_day - plan, "rub")'),
               ("забывает вычесть траты первого дня",
                'per_day = budget / days\nplan = per_day\nleft = budget\ndays_left = days - 1\n'
                'per_day = left / days_left\nprint("Plan:", plan, "rub")\nprint("Left:", left, "rub")\n'
                'print("New plan:", per_day, "rub")\nprint("Change:", per_day - plan, "rub")')],
    ),

    # ───────── 7. Строки ─────────
    OutputTask(
        skill=STR, difficulty=3, slug="py-int-strings-banner", title="Растяжка на день рождения",
        given=["words", "name", "price"],
        variants=[{"words": '"HAPPY BIRTHDAY"', "name": '"ANYA"', "price": "4.5"}],
        hidden=[{"words": '"GOOD LUCK"', "name": '"BORIS"', "price": "5.0"},
                {"words": '"WELCOME HOME"', "name": '"DAD"', "price": "3.5"},
                {"words": '"CONGRATULATIONS"', "name": '"OLGA IVANOVNA"', "price": "4.0"},
                {"words": '"GO"', "name": '"TEAM"', "price": "10.0"}],
        intro="Для праздника в копицентре печатают растяжку из листов A4: на каждом листе одна большая буква или знак, "
              "а на месте пробела — пустой лист. Поздравление — `words = {words}`, имя — `name = {name}`. Печать "
              "одного листа стоит `price = {price}` руб., ширина листа — 21 см, листы вешают в ряд вплотную.",
        steps=["Склей текст растяжки `text`: `words`, запятую с пробелом `\", \"`, `name` и `\"!\"` — и выведи его.",
               "Листов нужно столько, сколько символов в `text` (пробелы, запятая и `!` тоже занимают по листу). "
               "Сохрани `len(text)` в `sheets` и выведи через запятую `Sheets:` и `sheets`.",
               "Посчитай стоимость печати `cost` — `sheets`, умноженное на `price`, — и выведи через запятую `Cost:`, `cost` и `rub`.",
               "Посчитай длину растяжки в метрах: `sheets * 21 / 100` — и выведи через запятую `Length:`, длину и `m`. Например, для "
               "`\"HI\"`, `\"MOM\"` и цены 5.0 программа выводит `HI, MOM!`, `Sheets: 8`, `Cost: 40.0 rub` и "
               "`Length: 1.68 m`."],
        hint="`len()` считает все символы строки: буквы, пробелы, запятую и `!`. Цена дробная, поэтому и стоимость "
             "дробная: `21 * 4.5` — это `94.5`. Деление `/` всегда даёт дробное число.",
        solution='text = words + ", " + name + "!"\nprint(text)\nsheets = len(text)\nprint("Sheets:", sheets)\n'
                 'cost = sheets * price\nprint("Cost:", cost, "rub")\nprint("Length:", sheets * 21 / 100, "m")',
        wrong=[("забывает пробел после запятой — листов на один меньше",
                'text = words + "," + name + "!"\nprint(text)\nsheets = len(text)\nprint("Sheets:", sheets)\n'
                'cost = sheets * price\nprint("Cost:", cost, "rub")\nprint("Length:", sheets * 21 / 100, "m")'),
               ("считает листы только по буквам поздравления и имени, без запятой, пробела и `!`",
                'text = words + ", " + name + "!"\nprint(text)\nsheets = len(words) + len(name)\nprint("Sheets:", sheets)\n'
                'cost = sheets * price\nprint("Cost:", cost, "rub")\nprint("Length:", sheets * 21 / 100, "m")'),
               ("переводит сантиметры в метры делением на 1000",
                'text = words + ", " + name + "!"\nprint(text)\nsheets = len(text)\nprint("Sheets:", sheets)\n'
                'cost = sheets * price\nprint("Cost:", cost, "rub")\nprint("Length:", sheets * 21 / 1000, "m")')],
    ),
    OutputTask(
        skill=STR, difficulty=3, slug="py-int-strings-poster", title="Объявление о пропаже кота",
        given=["name", "color", "phone", "tabs"],
        variants=[{"name": '"Barsik"', "color": '"ginger"', "phone": '"89031234567"', "tabs": "4"}],
        hidden=[{"name": '"Murka"', "color": '"black"', "phone": '"234567"', "tabs": "1"},
                {"name": '"Tom"', "color": '"grey"', "phone": '"+79161234567"', "tabs": "5"},
                {"name": '"Snowball"', "color": '"white"', "phone": '"5550199"', "tabs": "3"},
                {"name": '"Ryzhik"', "color": '"ginger and white"', "phone": '"89990001122"', "tabs": "6"}],
        intro="У Даши пропал кот `name = {name}`, окрас — `color = {color}`. Она печатает объявление, а внизу листа "
              "делает отрывные полоски: телефон `phone = {phone}` повторяется на `tabs = {tabs}` полосках, полоски "
              "разделены вертикальной чертой `|`.",
        steps=["Склей строку `info` из `name`, `\", \"`, `color` и `\" cat\"` и выведи её, например `Pushok, white cat`.",
               "Выведи склейку `\"Call \"` и `phone`.",
               "Собери отрывные полоски в переменную `strip`: одна полоска — это склейка `\"| \"`, `phone` и пробела "
               "`\" \"`. Возьми эту склейку в скобки, умножь на `tabs` и в конце приклей ещё одну черту `\"|\"`. "
               "Пока не выводи.",
               "Выведи линию отреза — знак `-`, повторённый столько раз, сколько символов в `strip`, — и под ней сам "
               "`strip`. Например, для телефона `\"123\"` и 2 полосок эти две строки — `-------------` и `| 123 | 123 |`."],
        hint="`*` выполняется раньше `+`, как и с числами: без скобок повторится только последний пробел. "
             "Длину линии отреза даёт `len(strip)`, поэтому `strip` нужно собрать раньше, чем печатать линию.",
        solution='info = name + ", " + color + " cat"\nprint(info)\nprint("Call " + phone)\n'
                 'strip = ("| " + phone + " ") * tabs + "|"\nprint("-" * len(strip))\nprint(strip)',
        wrong=[("без скобок — повторяется только пробел после телефона",
                'info = name + ", " + color + " cat"\nprint(info)\nprint("Call " + phone)\n'
                'strip = "| " + phone + " " * tabs + "|"\nprint("-" * len(strip))\nprint(strip)'),
               ("линия отреза длиной в телефон, а не во все полоски",
                'info = name + ", " + color + " cat"\nprint(info)\nprint("Call " + phone)\n'
                'strip = ("| " + phone + " ") * tabs + "|"\nprint("-" * len(phone))\nprint(strip)'),
               ("забывает последнюю черту справа",
                'info = name + ", " + color + " cat"\nprint(info)\nprint("Call " + phone)\n'
                'strip = ("| " + phone + " ") * tabs\nprint("-" * len(strip))\nprint(strip)')],
    ),
    OutputTask(
        skill=STR, difficulty=3, slug="py-int-strings-route", title="Маршрут на выходные",
        given=["start", "first", "second", "cost1", "cost2"],
        variants=[{"start": '"Moscow"', "first": '"Vladimir"', "second": '"Suzdal"', "cost1": "650", "cost2": "280"}],
        hidden=[{"start": '"Kazan"', "first": '"Sviyazhsk"', "second": '"Innopolis"', "cost1": "300", "cost2": "150"},
                {"start": '"Sochi"', "first": '"Adler"', "second": '"Krasnaya Polyana"', "cost1": "50", "cost2": "120"},
                {"start": '"Yaroslavl"', "first": '"Rostov"', "second": '"Pereslavl"', "cost1": "420", "cost2": "0"},
                {"start": '"Saint Petersburg"', "first": '"Pushkin"', "second": '"Pavlovsk"', "cost1": "85", "cost2": "45"}],
        intro="Борис планирует поездку на выходные: из `start = {start}` на электричке в `first = {first}`, а оттуда на "
              "автобусе в `second = {second}`. Билет на электричку стоит `cost1 = {cost1}` руб., на автобус — "
              "`cost2 = {cost2}` руб. Обратно он поедет тем же путём и по тем же ценам.",
        steps=["Заведи переменную `route` со значением `start`. Затем присвой `route` новое значение — склейку `route`, "
               "`\" -> \"` и `first` — и выведи `route`.",
               "Так же допиши к `route` стрелку `\" -> \"` и `second` и выведи `route` ещё раз.",
               "Под маршрутом выведи черту — знак `=`, повторённый столько раз, сколько символов во всём маршруте.",
               "Выведи через запятую `Tickets:`, стоимость всех билетов туда и обратно и `rub`. Например, для билетов по 100 и 50 руб. "
               "это `Tickets: 300 rub`."],
        hint="`route = route + \" -> \" + first` берёт старое значение `route`, дописывает к нему стрелку и город и "
             "кладёт результат обратно в `route`. Черту считай после того, как дописан последний город. Туда и обратно — "
             "это сумма двух билетов, умноженная на 2, со скобками.",
        solution='route = start\nroute = route + " -> " + first\nprint(route)\nroute = route + " -> " + second\n'
                 'print(route)\nprint("=" * len(route))\nprint("Tickets:", (cost1 + cost2) * 2, "rub")',
        wrong=[("черту считает по маршруту до второго города",
                'route = start\nroute = route + " -> " + first\nline = "=" * len(route)\nprint(route)\n'
                'route = route + " -> " + second\nprint(route)\nprint(line)\nprint("Tickets:", (cost1 + cost2) * 2, "rub")'),
               ("без скобок — удваивает только автобусный билет",
                'route = start\nroute = route + " -> " + first\nprint(route)\nroute = route + " -> " + second\n'
                'print(route)\nprint("=" * len(route))\nprint("Tickets:", cost1 + cost2 * 2, "rub")'),
               ("стрелка без пробелов вокруг",
                'route = start\nroute = route + "->" + first\nprint(route)\nroute = route + "->" + second\n'
                'print(route)\nprint("=" * len(route))\nprint("Tickets:", (cost1 + cost2) * 2, "rub")')],
    ),

    # ───────── 8. Преобразование типов ─────────
    OutputTask(
        skill=CONV, difficulty=3, slug="py-int-convert-receipt", title="QR-код на квитанции",
        given=["account", "kop", "people"],
        variants=[{"account": '"000481"', "kop": '"245075"', "people": "2"}],
        hidden=[{"account": '"000001"', "kop": '"100000"', "people": "1"},
                {"account": '"070070"', "kop": '"317050"', "people": "4"},
                {"account": '"500200"', "kop": '"157000"', "people": "5"},
                {"account": '"000999"', "kop": '"89925"', "people": "3"}],
        intro="Соседи по квартире платят за коммунальные услуги через приложение банка. Приложение прочитало QR-код "
              "на квитанции, и все данные пришли строками: номер лицевого счёта `account = {account}` и сумма "
              "в копейках `kop = {kop}`. Банк берёт за оплату 30 руб. комиссии, а всё вместе соседи делят поровну "
              "на `people = {people}` человек.",
        steps=["Выведи склейку `\"Account: \"` и `account` — номер приклей как есть, нули в начале должны остаться.",
               "Преврати `kop` в целое число и раздели на 100 — это сумма в рублях `rub`. Выведи склейку `\"Bill: \"`, "
               "`rub` (через `str()`) и `\" rub\"`.",
               "Посчитай `total` — `rub` плюс 30 руб. комиссии, и долю каждого `share` — `total`, делённое на `people`.",
               "Выведи так же склейкой через `+` строки `Total: <total> rub` и `Each: <share> rub`. Например, для "
               "`\"50000\"` копеек на двоих это `Bill: 500.0 rub`, `Total: 530.0 rub` и `Each: 265.0 rub`."],
        hint="`int(\"000481\")` — это число `481`, нули пропадут, поэтому номер счёта приклеивай как строку. "
             "Деление `/` даёт `float`: `int(\"100000\") / 100` — это `1000.0`. Чтобы приклеить число к тексту через `+`, "
             "преврати его в строку: `str(1000.0)` даёт `\"1000.0\"`. Комиссию прибавляй к рублям, а не к копейкам.",
        solution='print("Account: " + account)\nrub = int(kop) / 100\nprint("Bill: " + str(rub) + " rub")\n'
                 'total = rub + 30\nshare = total / people\nprint("Total: " + str(total) + " rub")\n'
                 'print("Each: " + str(share) + " rub")',
        wrong=[("приклеивает номер счёта после `int()` — нули в начале пропадают",
                'print("Account: " + str(int(account)))\nrub = int(kop) / 100\nprint("Bill: " + str(rub) + " rub")\n'
                'total = rub + 30\nshare = total / people\nprint("Total: " + str(total) + " rub")\n'
                'print("Each: " + str(share) + " rub")'),
               ("прибавляет комиссию к копейкам — получается 30 копеек, а не 30 рублей",
                'print("Account: " + account)\nrub = int(kop) / 100\nprint("Bill: " + str(rub) + " rub")\n'
                'total = (int(kop) + 30) / 100\nshare = total / people\nprint("Total: " + str(total) + " rub")\n'
                'print("Each: " + str(share) + " rub")'),
               ("делит на соседей сумму без комиссии",
                'print("Account: " + account)\nrub = int(kop) / 100\nprint("Bill: " + str(rub) + " rub")\n'
                'total = rub + 30\nshare = rub / people\nprint("Total: " + str(total) + " rub")\n'
                'print("Each: " + str(share) + " rub")')],
    ),
    OutputTask(
        skill=CONV, difficulty=3, slug="py-int-convert-cartridge", title="Картридж в принтере",
        given=["printed", "capacity", "price"],
        variants=[{"printed": '"1830"', "capacity": '"2500"', "price": "3150"}],
        hidden=[{"printed": '"0"', "capacity": '"1000"', "price": "2500"},
                {"printed": '"2000"', "capacity": '"2000"', "price": "3000"},
                {"printed": '"1592"', "capacity": '"1600"', "price": "2400"},
                {"printed": '"375"', "capacity": '"3000"', "price": "5400"},
                {"printed": '"1250"', "capacity": '"5000"', "price": "6250"}],
        intro="Офисный принтер показывает на экране, сколько страниц уже напечатал картридж: `printed = {printed}`. "
              "Ресурс картриджа написан на коробке: `capacity = {capacity}` страниц. Оба значения программа получила "
              "строками. Картридж стоит `price = {price}` руб.",
        steps=["Выведи склейкой через `+` строку вида `Printed: 1830 of 2500` — `printed` и `capacity` приклей как есть.",
               "Преврати `printed` в целое число `done`, а `capacity` — в целое число `total`. Посчитай, сколько страниц "
               "ещё можно напечатать, — `left`.",
               "Посчитай, сколько процентов ресурса осталось: `percent = left * 100 / total`, и цену одной страницы "
               "`page` — `price`, делённую на `total`.",
               "Выведи склейкой через `+` строку `Left: <left> pages, <percent>%` (числа — через `str()`), а затем через "
               "`print` с запятыми `Page cost:`, `page` и `rub`. Например, для 600 напечатанных страниц из 1200 и цены 1800 это "
               "`Left: 600 pages, 50.0%` и `Page cost: 1.5 rub`."],
        hint="Строки `printed` и `capacity` в первую строку приклеивай как есть, а считать можно только числа: "
             "`int(\"1830\")` даёт `1830`. Сначала умножай на 100, потом дели: `670 * 100 / 2500` — это `26.8`. "
             "Процент приклеивай через `str()`, а не через `int()`: `int()` отбросит дробную часть.",
        solution='print("Printed: " + printed + " of " + capacity)\ndone = int(printed)\ntotal = int(capacity)\n'
                 'left = total - done\npercent = left * 100 / total\npage = price / total\n'
                 'print("Left: " + str(left) + " pages, " + str(percent) + "%")\nprint("Page cost:", page, "rub")',
        wrong=[("процент считает от напечатанных страниц, а не от оставшихся",
                'print("Printed: " + printed + " of " + capacity)\ndone = int(printed)\ntotal = int(capacity)\n'
                'left = total - done\npercent = done * 100 / total\npage = price / total\n'
                'print("Left: " + str(left) + " pages, " + str(percent) + "%")\nprint("Page cost:", page, "rub")'),
               ("приклеивает процент через `str(int(...))` — дробная часть пропадает",
                'print("Printed: " + printed + " of " + capacity)\ndone = int(printed)\ntotal = int(capacity)\n'
                'left = total - done\npercent = left * 100 / total\npage = price / total\n'
                'print("Left: " + str(left) + " pages, " + str(int(percent)) + "%")\nprint("Page cost:", page, "rub")'),
               ("забывает умножить на 100 — получается доля, а не проценты",
                'print("Printed: " + printed + " of " + capacity)\ndone = int(printed)\ntotal = int(capacity)\n'
                'left = total - done\npercent = left / total\npage = price / total\n'
                'print("Left: " + str(left) + " pages, " + str(percent) + "%")\nprint("Page cost:", page, "rub")')],
    ),
    OutputTask(
        skill=CONV, difficulty=3, slug="py-int-convert-puppy", title="Корм для щенка",
        given=["bag", "portion", "price"],
        variants=[{"bag": '"2.1"', "portion": '"40"', "price": "1260"}],
        hidden=[{"bag": '"2.0"', "portion": '"50"', "price": "1200"},
                {"bag": '"1.75"', "portion": '"40"', "price": "1400"},
                {"bag": '"6.5"', "portion": '"100"', "price": "1950"},
                {"bag": '"0.6"', "portion": '"20"', "price": "330"}],
        intro="Тимур купил щенку пакет корма. Вес пакета в килограммах написан на упаковке, а дневную порцию в граммах "
              "ветеринар записал в карточку — оба значения пришли в программу строками: `bag = {bag}` и "
              "`portion = {portion}`. Пакет стоит `price = {price}` руб. Через месяц щенок подрастёт и будет съедать "
              "в день на 30 г больше.",
        steps=["Выведи склейку `\"Bag: \"`, `bag` и `\" kg\"` — строку `bag` приклей как есть.",
               "Преврати `bag` в дробное число и переведи в граммы (умножь на 1000) — это `grams`. Преврати `portion` "
               "в целое число `daily`.",
               "Посчитай, на сколько дней хватит пакета, — `days` (`grams`, делённое на `daily`), и сколько стоит корм "
               "на один день, — `cost` (`price`, делённая на `days`). Выведи склейкой через `+` строку "
               "`Lasts: <days> days, <cost> rub per day` (числа — через `str()`).",
               "Щенок подрос: присвой `daily` значение `daily + 30`, заново посчитай `days` и выведи склейкой "
               "`Later: <days> days`. Например, для `\"1.2\"` кг и порции `\"30\"` г при цене 600 программа выводит "
               "`Bag: 1.2 kg`, `Lasts: 40.0 days, 15.0 rub per day` и `Later: 20.0 days`."],
        hint="`float(\"2.1\")` даёт число `2.1`, а `int(\"40\")` — число `40`. Деление `/` всегда даёт дробное число, "
             "поэтому дни печатаются с точкой. `days` не пересчитается сам, когда изменится `daily`: после нового "
             "значения `daily` посчитай `days` ещё раз.",
        solution='print("Bag: " + bag + " kg")\ngrams = float(bag) * 1000\ndaily = int(portion)\ndays = grams / daily\n'
                 'cost = price / days\nprint("Lasts: " + str(days) + " days, " + str(cost) + " rub per day")\n'
                 'daily = daily + 30\ndays = grams / daily\nprint("Later: " + str(days) + " days")',
        wrong=[("после того как щенок подрос, не пересчитывает `days`",
                'print("Bag: " + bag + " kg")\ngrams = float(bag) * 1000\ndaily = int(portion)\ndays = grams / daily\n'
                'cost = price / days\nprint("Lasts: " + str(days) + " days, " + str(cost) + " rub per day")\n'
                'daily = daily + 30\nprint("Later: " + str(days) + " days")'),
               ("переводит килограммы в граммы умножением на 100",
                'print("Bag: " + bag + " kg")\ngrams = float(bag) * 100\ndaily = int(portion)\ndays = grams / daily\n'
                'cost = price / days\nprint("Lasts: " + str(days) + " days, " + str(cost) + " rub per day")\n'
                'daily = daily + 30\ndays = grams / daily\nprint("Later: " + str(days) + " days")'),
               ("цену дня считает делением дней на цену",
                'print("Bag: " + bag + " kg")\ngrams = float(bag) * 1000\ndaily = int(portion)\ndays = grams / daily\n'
                'cost = days / price\nprint("Lasts: " + str(days) + " days, " + str(cost) + " rub per day")\n'
                'daily = daily + 30\ndays = grams / daily\nprint("Later: " + str(days) + " days")')],
    ),
]
