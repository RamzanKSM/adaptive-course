"""Integrative tasks (the task of a topic's 3rd iteration), Python, course topics 9–11: PY_INTEGER_DIVISION (// and %),
PY_ASSIGNMENT_OPERATORS (+= -=), PY_FSTRINGS. Topic X is at the core of each family, 1–2 earlier topics do real work:
- // and %: + type conversion and arithmetic (buns on baking trays), + arithmetic with parentheses (cubes in a box),
  + strings and type conversion (watering reminder);
- += -=: + type conversion and // (flour in a bakery), + strings `*` and `+` (scheme of a yard parking),
  + strings and str() (dates of duties in a month);
- f-strings: + // % and arithmetic (baker's percentages), + strings len()/`*` and float `/` (label on a box),
  + type conversion and // (airport parking).
Not yet: += -= and f-strings in the // % families, f-strings in the += -= families; format specifiers like :.2f,
round(), conditions, comparisons, loops, lists, functions.
Theme domains: bakery and recipes; time and calendars; parking; packing boxes."""
from build import OutputTask

DIV = "PY_INTEGER_DIVISION"
AUG = "PY_ASSIGNMENT_OPERATORS"
FSTR = "PY_FSTRINGS"
MUST_DIV = [("FloorDiv", "Используй деление нацело //"), ("Mod", "Используй остаток от деления %")]
MUST_AUG = [("AugAssign", "Используй составное присваивание (+= или -=), чтобы изменить переменную")]
MUST_FSTR = [("JoinedStr", "Используй f-строку: f\"...{переменная}...\"")]

TASKS = [
    # ───────── 9. // and % ─────────
    OutputTask(
        skill=DIV, difficulty=3, slug="py-int-intdiv-trays", title="Булочки на противнях",
        given=["order", "rows", "cols"],
        variants=[{"order": '"47"', "rows": "3", "cols": "4"}],
        hidden=[{"order": '"7"', "rows": "2", "cols": "5"},
                {"order": '"60"', "rows": "3", "cols": "4"},
                {"order": '"100"', "rows": "4", "cols": "6"},
                {"order": '"56"', "rows": "3", "cols": "4"},
                {"order": '"38"', "rows": "5", "cols": "3"}],
        intro="Пекарня печёт булочки по заказам с сайта, и число булочек в заказе пришло с сайта строкой: "
              "`order = {order}`. На противень булочки кладут ровными рядами: `rows = {rows}` ряда по "
              "`cols = {cols}` булочки. Сначала заполняют целые противни, а оставшиеся булочки кладут на последний "
              "противень — тоже рядами по `cols` штук, и в конце может остаться неполный ряд.",
        steps=["Преврати `order` в целое число и сохрани в `buns`. Посчитай, сколько булочек помещается на один "
               "противень: `tray` — `rows`, умноженное на `cols`.",
               "Посчитай число полных противней `full` — `buns`, делённое нацело на `tray`, — и сколько булочек попадёт "
               "на последний противень: `last` — остаток от деления `buns` на `tray`.",
               "Выведи через `print` с запятой `Full trays:` и `full`, затем `Last tray:` и `last`.",
               "Выведи `Full rows:` и число полных рядов на последнем противне (`last`, делённое нацело на `cols`), "
               "затем `Extra:` и число булочек в неполном ряду (остаток от деления `last` на `cols`). "
               "Например, для заказа `\"7\"` и противня из 2 рядов по 5 булочек программа выводит `Full trays: 0`, "
               "`Last tray: 7`, `Full rows: 1`, `Extra: 2`."],
        hint="Со строкой `\"47\"` деление не работает, нужен `int(order)`. Ряды считай только из `last`: "
             "`buns // cols` дало бы ряды на всех противнях сразу.",
        solution='buns = int(order)\ntray = rows * cols\nfull = buns // tray\nlast = buns % tray\n'
                 'print("Full trays:", full)\nprint("Last tray:", last)\n'
                 'print("Full rows:", last // cols)\nprint("Extra:", last % cols)',
        wrong=[("ряды посчитаны из всего заказа, а не из последнего противня",
                'buns = int(order)\ntray = rows * cols\nfull = buns // tray\nlast = buns % tray\n'
                'print("Full trays:", full)\nprint("Last tray:", last)\n'
                'print("Full rows:", buns // cols)\nprint("Extra:", last % cols)'),
               ("на противне rows + cols булочек вместо rows * cols",
                'buns = int(order)\ntray = rows + cols\nfull = buns // tray\nlast = buns % tray\n'
                'print("Full trays:", full)\nprint("Last tray:", last)\n'
                'print("Full rows:", last // cols)\nprint("Extra:", last % cols)'),
               ("противни посчитаны через / — получается дробь",
                'buns = int(order)\ntray = rows * cols\nfull = buns / tray\nlast = buns % tray\n'
                'print("Full trays:", full)\nprint("Last tray:", last)\n'
                'print("Full rows:", last // cols)\nprint("Extra:", last % cols)'),
               ("булочки последнего противня посчитаны через // вместо остатка",
                'buns = int(order)\ntray = rows * cols\nfull = buns // tray\nlast = buns // tray\n'
                'print("Full trays:", full)\nprint("Last tray:", last)\n'
                'print("Full rows:", last // cols)\nprint("Extra:", last % cols)')],
        must_use=MUST_DIV,
    ),
    OutputTask(
        skill=DIV, difficulty=3, slug="py-int-intdiv-cubes", title="Кубики в коробке",
        given=["side", "length", "width", "height"],
        variants=[{"side": "8", "length": "40", "width": "30", "height": "25"}],
        hidden=[{"side": "10", "length": "50", "width": "40", "height": "30"},
                {"side": "30", "length": "70", "width": "40", "height": "25"},
                {"side": "6", "length": "45", "width": "20", "height": "13"},
                {"side": "5", "length": "32", "width": "24", "height": "19"},
                {"side": "12", "length": "60", "width": "36", "height": "12"}],
        intro="На фабрике игрушек деревянные кубики со стороной `side = {side}` см укладывают в коробку длиной "
              "`length = {length}`, шириной `width = {width}` и высотой `height = {height}` см. Кубики ставят "
              "ровными рядами и слоями, повернуть или распилить кубик нельзя. Кладовщик прикинул число кубиков "
              "«по объёму», а нужно узнать, сколько их войдёт на самом деле.",
        steps=["Посчитай, сколько кубиков встанет вдоль длины коробки (`along` — `length`, делённая нацело на `side`), "
               "вдоль ширины (`across` — из `width`) и сколько слоёв поместится по высоте (`layers` — из `height`).",
               "Посчитай, сколько всего кубиков войдёт: `fit` — произведение `along`, `across` и `layers`.",
               "Посчитай прикидку кладовщика `by_volume`: объём коробки (`length * width * height`), делённый нацело "
               "на объём кубика (`side * side * side`). Объём кубика возьми в скобки.",
               "Выведи через `print` с запятой три строки: `Fit:`, `along`, `x`, `across`, `x`, `layers`, `=`, `fit` "
               "и `cubes`; затем `Gap on top:`, остаток от деления `height` на `side` и `cm`; затем `By volume:`, "
               "`by_volume` и `cubes`. Например, для кубика 10 см и коробки 50 × 40 × 30 см программа выводит "
               "`Fit: 5 x 4 x 3 = 60 cubes`, `Gap on top: 0 cm`, `By volume: 60 cubes`."],
        hint="Деление нацело отбрасывает неполный кубик: `25 // 8` даёт `3` слоя, а `25 % 8` — `1` см пустоты сверху. "
             "Без скобок `... // side * side * side` Python сначала разделит на `side`, а потом умножит.",
        solution='along = length // side\nacross = width // side\nlayers = height // side\n'
                 'fit = along * across * layers\nby_volume = length * width * height // (side * side * side)\n'
                 'print("Fit:", along, "x", across, "x", layers, "=", fit, "cubes")\n'
                 'print("Gap on top:", height % side, "cm")\nprint("By volume:", by_volume, "cubes")',
        wrong=[("объём кубика без скобок — Python делит только на side, а потом умножает",
                'along = length // side\nacross = width // side\nlayers = height // side\n'
                'fit = along * across * layers\nby_volume = length * width * height // side * side * side\n'
                'print("Fit:", along, "x", across, "x", layers, "=", fit, "cubes")\n'
                'print("Gap on top:", height % side, "cm")\nprint("By volume:", by_volume, "cubes")'),
               ("пустота сверху посчитана через // — получается число слоёв",
                'along = length // side\nacross = width // side\nlayers = height // side\n'
                'fit = along * across * layers\nby_volume = length * width * height // (side * side * side)\n'
                'print("Fit:", along, "x", across, "x", layers, "=", fit, "cubes")\n'
                'print("Gap on top:", height // side, "cm")\nprint("By volume:", by_volume, "cubes")'),
               ("в fit взята прикидка по объёму",
                'along = length // side\nacross = width // side\nlayers = height // side\n'
                'by_volume = length * width * height // (side * side * side)\nfit = by_volume\n'
                'print("Fit:", along, "x", across, "x", layers, "=", fit, "cubes")\n'
                'print("Gap on top:", height % side, "cm")\nprint("By volume:", by_volume, "cubes")'),
               ("ряды посчитаны через / — получаются дробные кубики",
                'along = length / side\nacross = width / side\nlayers = height / side\n'
                'fit = along * across * layers\nby_volume = length * width * height // (side * side * side)\n'
                'print("Fit:", along, "x", across, "x", layers, "=", fit, "cubes")\n'
                'print("Gap on top:", height % side, "cm")\nprint("By volume:", by_volume, "cubes")')],
        must_use=MUST_DIV,
    ),
    OutputTask(
        skill=DIV, difficulty=3, slug="py-int-intdiv-watering", title="Напоминание о поливе",
        given=["plant", "every", "bought", "today"],
        variants=[{"plant": '"Ficus"', "every": "4", "bought": "270", "today": '"301"'}],
        hidden=[{"plant": '"Cactus"', "every": "10", "bought": "100", "today": '"120"'},
                {"plant": '"Aloe"', "every": "7", "bought": "1", "today": '"360"'},
                {"plant": '"Mint"', "every": "2", "bought": "200", "today": '"203"'},
                {"plant": '"Orchid"', "every": "6", "bought": "15", "today": '"26"'},
                {"plant": '"Basil"', "every": "3", "bought": "330", "today": '"333"'}],
        intro="Приложение-напоминалка следит за поливом комнатных цветов. Цветок `plant = {plant}` поливают каждые "
              "`every = {every}` дня. Его купили в `bought = {bought}`-й день года и с тех пор поливают строго "
              "по графику: первый раз — через `every` дней после покупки, потом ещё через `every` дней и так далее. "
              "Номер сегодняшнего дня в году календарь телефона отдаёт строкой: `today = {today}`.",
        steps=["Склей через `+` название цветка, `: every `, число `every` (превращённое в строку с помощью `str()`) "
               "и ` days` и выведи, например `Cactus: every 10 days`.",
               "Преврати `today` в целое число и посчитай, сколько дней цветок живёт дома: `days` — сегодняшний день "
               "минус `bought`.",
               "Посчитай число поливов `times` — `days`, делённое нацело на `every`, — и сколько дней прошло после "
               "последнего полива: `since` — остаток от деления `days` на `every`.",
               "Выведи через `print` с запятой `Waterings:` и `times`, `Days since last:` и `since`, "
               "`Days to next:` и сколько дней осталось до следующего полива (`every` минус `since`). "
               "Например, если цветок дома 20 дней и его поливают каждые 10 дней, программа выводит `Waterings: 2`, "
               "`Days since last: 0`, `Days to next: 10`."],
        hint="Число со строкой через `+` не склеится: `str(4)` даёт строку `\"4\"`. "
             "`31 // 4` даёт `7` поливов, а `31 % 4` — `3` дня после последнего полива.",
        solution='print(plant + ": every " + str(every) + " days")\ndays = int(today) - bought\n'
                 'times = days // every\nsince = days % every\nprint("Waterings:", times)\n'
                 'print("Days since last:", since)\nprint("Days to next:", every - since)',
        wrong=[("до следующего полива выводит сам остаток",
                'print(plant + ": every " + str(every) + " days")\ndays = int(today) - bought\n'
                'times = days // every\nsince = days % every\nprint("Waterings:", times)\n'
                'print("Days since last:", since)\nprint("Days to next:", since)'),
               ("забыт день покупки — дни считаются с начала года",
                'print(plant + ": every " + str(every) + " days")\ndays = int(today)\n'
                'times = days // every\nsince = days % every\nprint("Waterings:", times)\n'
                'print("Days since last:", since)\nprint("Days to next:", every - since)'),
               ("дни после полива посчитаны через // вместо остатка",
                'print(plant + ": every " + str(every) + " days")\ndays = int(today) - bought\n'
                'times = days // every\nsince = days // every\nprint("Waterings:", times)\n'
                'print("Days since last:", since)\nprint("Days to next:", every - since)'),
               ("поливы посчитаны через / — получается дробь",
                'print(plant + ": every " + str(every) + " days")\ndays = int(today) - bought\n'
                'times = days / every\nsince = days % every\nprint("Waterings:", times)\n'
                'print("Days since last:", since)\nprint("Days to next:", every - since)')],
        must_use=MUST_DIV,
    ),

    # ───────── 10. += -= ─────────
    OutputTask(
        skill=AUG, difficulty=3, slug="py-int-augassign-flour", title="Мука в пекарне",
        given=["sack", "per_loaf", "morning", "evening"],
        variants=[{"sack": '"25"', "per_loaf": "450", "morning": "20", "evening": "30"}],
        hidden=[{"sack": '"10"', "per_loaf": "500", "morning": "0", "evening": "40"},
                {"sack": '"50"', "per_loaf": "400", "morning": "100", "evening": "120"},
                {"sack": '"20"', "per_loaf": "350", "morning": "57", "evening": "50"},
                {"sack": '"5"', "per_loaf": "250", "morning": "16", "evening": "10"},
                {"sack": '"30"', "per_loaf": "600", "morning": "45", "evening": "50"}],
        intro="Пекарня начинает день с мешком муки. Вес мешка в килограммах пекарь переписал из накладной, и программа "
              "получила его строкой: `sack = {sack}`. На один батон уходит `per_loaf = {per_loaf}` г муки. Утром "
              "испекли `morning = {morning}` батонов, в обед привезли ещё один такой же мешок, а вечером испекли "
              "`evening = {evening}` батонов.",
        steps=["Преврати `sack` в целое число и переведи в граммы (умножь на 1000) — это `flour`. Выведи через `print` "
               "с запятой `Flour:`, `flour` и `g`.",
               "Утро: вычти из `flour` муку на утренние батоны (`morning * per_loaf`) с помощью `-=` и выведи "
               "`After morning:`, `flour` и `g`.",
               "Обед и вечер: прибавь к `flour` вес нового мешка в граммах с помощью `+=`, затем вычти муку на вечерние "
               "батоны с помощью `-=`. Выведи `After evening:`, `flour` и `g`.",
               "Выведи `Enough for:`, сколько ещё целых батонов можно испечь из оставшейся муки (`flour`, делённая "
               "нацело на `per_loaf`), и `loaves`. Например, если осталось 1000 г, а на батон уходит 400 г, последняя "
               "строка — `Enough for: 2 loaves`."],
        hint="`flour -= morning * per_loaf` — то же, что `flour = flour - morning * per_loaf`. Новый мешок тоже "
             "весит `int(sack)` килограммов, а в `flour` хранятся граммы — не забудь умножить на 1000.",
        solution='flour = int(sack) * 1000\nprint("Flour:", flour, "g")\nflour -= morning * per_loaf\n'
                 'print("After morning:", flour, "g")\nflour += int(sack) * 1000\nflour -= evening * per_loaf\n'
                 'print("After evening:", flour, "g")\nprint("Enough for:", flour // per_loaf, "loaves")',
        wrong=[("забыт мешок, привезённый в обед",
                'flour = int(sack) * 1000\nprint("Flour:", flour, "g")\nflour -= morning * per_loaf\n'
                'print("After morning:", flour, "g")\nflour -= evening * per_loaf\n'
                'print("After evening:", flour, "g")\nprint("Enough for:", flour // per_loaf, "loaves")'),
               ("новый мешок прибавлен в килограммах, а не в граммах",
                'flour = int(sack) * 1000\nprint("Flour:", flour, "g")\nflour -= morning * per_loaf\n'
                'print("After morning:", flour, "g")\nflour += int(sack)\nflour -= evening * per_loaf\n'
                'print("After evening:", flour, "g")\nprint("Enough for:", flour // per_loaf, "loaves")'),
               ("вычитает число батонов, а не муку на них",
                'flour = int(sack) * 1000\nprint("Flour:", flour, "g")\nflour -= morning\n'
                'print("After morning:", flour, "g")\nflour += int(sack) * 1000\nflour -= evening\n'
                'print("After evening:", flour, "g")\nprint("Enough for:", flour // per_loaf, "loaves")'),
               ("утром пишет = вместо -= — в flour попадает мука на батоны",
                'flour = int(sack) * 1000\nprint("Flour:", flour, "g")\nflour = morning * per_loaf\n'
                'print("After morning:", flour, "g")\nflour += int(sack) * 1000\nflour -= evening * per_loaf\n'
                'print("After evening:", flour, "g")\nprint("Enough for:", flour // per_loaf, "loaves")'),
               ("батоны посчитаны через / — получается дробь",
                'flour = int(sack) * 1000\nprint("Flour:", flour, "g")\nflour -= morning * per_loaf\n'
                'print("After morning:", flour, "g")\nflour += int(sack) * 1000\nflour -= evening * per_loaf\n'
                'print("After evening:", flour, "g")\nprint("Enough for:", flour / per_loaf, "loaves")')],
        must_use=MUST_AUG,
    ),
    OutputTask(
        skill=AUG, difficulty=3, slug="py-int-augassign-yard", title="Парковка во дворе",
        given=["places", "cars", "leave", "come"],
        variants=[{"places": "12", "cars": "10", "leave": "7", "come": "3"}],
        hidden=[{"places": "5", "cars": "5", "leave": "5", "come": "2"},
                {"places": "8", "cars": "3", "leave": "0", "come": "5"},
                {"places": "20", "cars": "14", "leave": "9", "come": "6"},
                {"places": "6", "cars": "0", "leave": "0", "come": "1"},
                {"places": "10", "cars": "7", "leave": "2", "come": "5"}],
        intro="Во дворе дома парковка на `places = {places}` мест. Ночью на ней стоят `cars = {cars}` машин. Утром "
              "`leave = {leave}` машин уезжают на работу, а днём во двор заезжают машины гостей: `come = {come}`. "
              "Дворник рисует для домового чата схему парковки: `#` — занятое место, `.` — свободное.",
        steps=["Посчитай, сколько мест свободно ночью: `free` — `places` минус `cars`. Выведи через `print` с запятой "
               "`Night:` и схему — строку из `cars` знаков `#` и `free` точек, склеенных через `+`. Например, для "
               "3 машин и 2 свободных мест схема — `###..`.",
               "Утро: уменьши `cars` на `leave` с помощью `-=` и увеличь `free` на столько же с помощью `+=`. "
               "Выведи `Morning:` и новую схему.",
               "День: увеличь `cars` на `come` с помощью `+=` и уменьши `free` на `come` с помощью `-=`. "
               "Выведи `Day:` и схему.",
               "Последней строкой выведи `Free:`, `free`, `of` и `places`, например `Free: 2 of 5`."],
        hint="`\"#\" * 3` даёт `###`, а `\"#\" * 3 + \".\" * 2` — `###..`. Когда машина уезжает, занятых мест "
             "становится меньше, а свободных — больше: меняй обе переменные.",
        solution='free = places - cars\nprint("Night:", "#" * cars + "." * free)\ncars -= leave\nfree += leave\n'
                 'print("Morning:", "#" * cars + "." * free)\ncars += come\nfree -= come\n'
                 'print("Day:", "#" * cars + "." * free)\nprint("Free:", free, "of", places)',
        wrong=[("утром не освобождает места: free не меняется",
                'free = places - cars\nprint("Night:", "#" * cars + "." * free)\ncars -= leave\n'
                'print("Morning:", "#" * cars + "." * free)\ncars += come\nfree -= come\n'
                'print("Day:", "#" * cars + "." * free)\nprint("Free:", free, "of", places)'),
               ("днём свободных мест тоже прибавляется",
                'free = places - cars\nprint("Night:", "#" * cars + "." * free)\ncars -= leave\nfree += leave\n'
                'print("Morning:", "#" * cars + "." * free)\ncars += come\nfree += come\n'
                'print("Day:", "#" * cars + "." * free)\nprint("Free:", free, "of", places)'),
               ("пишет =- вместо -= — в cars попадает число со знаком минус",
                'free = places - cars\nprint("Night:", "#" * cars + "." * free)\ncars =- leave\nfree += leave\n'
                'print("Morning:", "#" * cars + "." * free)\ncars += come\nfree -= come\n'
                'print("Day:", "#" * cars + "." * free)\nprint("Free:", free, "of", places)')],
        must_use=MUST_AUG,
    ),
    OutputTask(
        skill=AUG, difficulty=3, slug="py-int-augassign-duty", title="График дежурств",
        given=["month", "days", "first", "step"],
        variants=[{"month": '"March"', "days": "31", "first": "4", "step": "10"}],
        hidden=[{"month": '"May"', "days": "31", "first": "2", "step": "12"},
                {"month": '"February"', "days": "28", "first": "1", "step": "10"},
                {"month": '"April"', "days": "30", "first": "5", "step": "11"},
                {"month": '"June"', "days": "30", "first": "1", "step": "14"},
                {"month": '"December"', "days": "31", "first": "7", "step": "12"}],
        intro="Аня дежурит в общежитии через равные промежутки — каждые `step = {step}` дней. Первое дежурство в месяце "
              "`month = {month}` выпало на `first = {first}`-е число. Всего дней в этом месяце: `days = {days}`, и в него "
              "помещаются ровно три дежурства. Нужно составить строку с датами дежурств и узнать, на какое число "
              "следующего месяца выпадет четвёртое.",
        steps=["Заведи переменную `day` со значением `first` и строку `plan`: название месяца, двоеточие, пробел и "
               "номер дня, превращённый в строку с помощью `str()`. Например, `May: 2`.",
               "Добавь второе дежурство: прибавь к `day` шаг `step` с помощью `+=`, затем допиши в конец `plan` "
               "с помощью `+=` запятую, пробел и новый номер дня. Точно так же добавь третье дежурство.",
               "Выведи `plan`. Например, для мая, первого дежурства 2-го числа и шага 12 дней получится `May: 2, 14, 26`.",
               "Четвёртое дежурство уже в следующем месяце: прибавь к `day` ещё `step` с помощью `+=`, вычти из `day` "
               "число дней месяца с помощью `-=` и выведи через `print` с запятой `Next month: day` и `day`. "
               "Для примера выше (в мае 31 день) это `Next month: day 7`."],
        hint="`plan += \", \" + str(day)` дописывает текст в конец строки — так же, как `+=` прибавляет к числу. "
             "Число к строке через `+` не приклеится, поэтому нужен `str(day)`.",
        solution='day = first\nplan = month + ": " + str(day)\nday += step\nplan += ", " + str(day)\nday += step\n'
                 'plan += ", " + str(day)\nprint(plan)\nday += step\nday -= days\nprint("Next month: day", day)',
        wrong=[("второй датой затирает строку вместо того, чтобы дописать",
                'day = first\nplan = month + ": " + str(day)\nday += step\nplan = ", " + str(day)\nday += step\n'
                'plan += ", " + str(day)\nprint(plan)\nday += step\nday -= days\nprint("Next month: day", day)'),
               ("пишет str(day + step), но не сохраняет новый день",
                'day = first\nplan = month + ": " + str(day)\nplan += ", " + str(day + step)\n'
                'plan += ", " + str(day + step)\nprint(plan)\nday += step\nday -= days\nprint("Next month: day", day)'),
               ("забыто вычесть дни месяца",
                'day = first\nplan = month + ": " + str(day)\nday += step\nplan += ", " + str(day)\nday += step\n'
                'plan += ", " + str(day)\nprint(plan)\nday += step\nprint("Next month: day", day)'),
               ("после запятой нет пробела",
                'day = first\nplan = month + ": " + str(day)\nday += step\nplan += "," + str(day)\nday += step\n'
                'plan += "," + str(day)\nprint(plan)\nday += step\nday -= days\nprint("Next month: day", day)')],
        must_use=MUST_AUG,
    ),

    # ───────── 11. f-strings ─────────
    OutputTask(
        skill=FSTR, difficulty=3, slug="py-int-fstrings-hydration", title="Пекарские проценты",
        given=["bread", "flour", "water", "salt", "loaves"],
        variants=[{"bread": '"Ciabatta"', "flour": "800", "water": "600", "salt": "16", "loaves": "5"}],
        hidden=[{"bread": '"Rye"', "flour": "1000", "water": "700", "salt": "20", "loaves": "4"},
                {"bread": '"Baguette"', "flour": "500", "water": "340", "salt": "10", "loaves": "3"},
                {"bread": '"Focaccia"', "flour": "750", "water": "610", "salt": "15", "loaves": "4"},
                {"bread": '"Brioche"', "flour": "300", "water": "150", "salt": "6", "loaves": "6"},
                {"bread": '"Sourdough"', "flour": "900", "water": "711", "salt": "18", "loaves": "5"}],
        intro="Пекари записывают рецепты «пекарскими процентами»: воду считают в процентах от веса муки. Для хлеба "
              "`bread = {bread}` взяли `flour = {flour}` г муки, `water = {water}` г воды и `salt = {salt}` г соли. "
              "Из всего теста пекарь делает `loaves = {loaves}` одинаковых буханок, каждая весит целое число граммов, "
              "а лишние граммы теста он отщипывает.",
        steps=["Посчитай вес теста `dough` — сумму муки, воды и соли.",
               "Посчитай влажность теста `hydration` — вес воды в процентах от веса муки: `water * 100 // flour`.",
               "Посчитай вес одной буханки `piece` — `dough`, делённое нацело на `loaves`, — и сколько граммов теста "
               "останется: `rest` — остаток от деления `dough` на `loaves`.",
               "С помощью f-строк выведи три строки: `<bread>: <dough> g of dough`, `Hydration: <hydration>%` и "
               "`<loaves> loaves x <piece> g, <rest> g left`. Например, для 1000 г муки, 700 г воды, 20 г соли и "
               "4 буханок вторая и третья строки — `Hydration: 70%` и `4 loaves x 430 g, 0 g left`."],
        hint="Сначала умножай на 100, потом дели нацело: `600 // 800 * 100` даёт `0`, а `600 * 100 // 800` — `75`. "
             "Знак `%` в тексте f-строки — обычный символ: `f\"Hydration: {{hydration}}%\"`.",
        solution='dough = flour + water + salt\nhydration = water * 100 // flour\npiece = dough // loaves\n'
                 'rest = dough % loaves\nprint(f"{bread}: {dough} g of dough")\nprint(f"Hydration: {hydration}%")\n'
                 'print(f"{loaves} loaves x {piece} g, {rest} g left")',
        wrong=[("сначала делит нацело, потом умножает на 100 — влажность получается 0%",
                'dough = flour + water + salt\nhydration = water // flour * 100\npiece = dough // loaves\n'
                'rest = dough % loaves\nprint(f"{bread}: {dough} g of dough")\nprint(f"Hydration: {hydration}%")\n'
                'print(f"{loaves} loaves x {piece} g, {rest} g left")'),
               ("забыта соль в весе теста",
                'dough = flour + water\nhydration = water * 100 // flour\npiece = dough // loaves\n'
                'rest = dough % loaves\nprint(f"{bread}: {dough} g of dough")\nprint(f"Hydration: {hydration}%")\n'
                'print(f"{loaves} loaves x {piece} g, {rest} g left")'),
               ("вес буханки посчитан через / — получается дробь",
                'dough = flour + water + salt\nhydration = water * 100 // flour\npiece = dough / loaves\n'
                'rest = dough % loaves\nprint(f"{bread}: {dough} g of dough")\nprint(f"Hydration: {hydration}%")\n'
                'print(f"{loaves} loaves x {piece} g, {rest} g left")'),
               ("пропущена буква f — печатаются фигурные скобки",
                'dough = flour + water + salt\nhydration = water * 100 // flour\npiece = dough // loaves\n'
                'rest = dough % loaves\nprint(f"{bread}: {dough} g of dough")\nprint("Hydration: {hydration}%")\n'
                'print(f"{loaves} loaves x {piece} g, {rest} g left")')],
        must_use=MUST_FSTR,
    ),
    OutputTask(
        skill=FSTR, difficulty=3, slug="py-int-fstrings-label", title="Наклейка на коробку",
        given=["number", "item", "count", "each", "box"],
        variants=[{"number": "17", "item": '"Teapot"', "count": "4", "each": "650", "box": "300"}],
        hidden=[{"number": "5", "item": '"Cup"', "count": "2", "each": "500", "box": "250"},
                {"number": "120", "item": '"Salad bowl"', "count": "3", "each": "1000", "box": "1000"},
                {"number": "9", "item": '"Plate"', "count": "12", "each": "380", "box": "450"},
                {"number": "48", "item": '"Frying pan"', "count": "1", "each": "1850", "box": "375"},
                {"number": "1003", "item": '"Glass"', "count": "6", "each": "215", "box": "99"}],
        intro="Интернет-магазин посуды печатает наклейки на коробки с заказами. В коробке номер `number = {number}` "
              "лежат `count = {count}` шт. товара `item = {item}`, каждый предмет весит `each = {each}` г, а пустая коробка "
              "с упаковкой — `box = {box}` г.",
        steps=["Сохрани в переменную `title` f-строку `Box #<number>: <item>` и выведи её.",
               "Под заголовком выведи строку из знаков `=` такой же длины, как `title` (длину даёт `len()`).",
               "Посчитай общий вес коробки `total` в граммах: пустая коробка плюс все предметы (`count`, умноженное "
               "на `each`).",
               "С помощью f-строк выведи `Items: <count> x <each> g` и `Total: <total> g = <total / 1000> kg` — "
               "килограммы посчитай прямо в фигурных скобках обычным делением. Например, для 2 предметов по 500 г "
               "в коробке 250 г последние строки — `Items: 2 x 500 g` и `Total: 1250 g = 1.25 kg`."],
        hint="f-строку можно сохранить в переменную, как любую строку: `title = f\"Box #{{number}}: {{item}}\"`. "
             "`\"=\" * 3` даёт `===`. Деление `/` всегда даёт дробное число: `3000 / 1000` — это `3.0`.",
        solution='title = f"Box #{number}: {item}"\nprint(title)\nprint("=" * len(title))\n'
                 'total = box + count * each\nprint(f"Items: {count} x {each} g")\n'
                 'print(f"Total: {total} g = {total / 1000} kg")',
        wrong=[("черта длиной с название товара, а не с заголовок",
                'title = f"Box #{number}: {item}"\nprint(title)\nprint("=" * len(item))\n'
                'total = box + count * each\nprint(f"Items: {count} x {each} g")\n'
                'print(f"Total: {total} g = {total / 1000} kg")'),
               ("скобки не там: к числу предметов прибавлена коробка",
                'title = f"Box #{number}: {item}"\nprint(title)\nprint("=" * len(title))\n'
                'total = (box + count) * each\nprint(f"Items: {count} x {each} g")\n'
                'print(f"Total: {total} g = {total / 1000} kg")'),
               ("килограммы посчитаны через // — дробная часть теряется",
                'title = f"Box #{number}: {item}"\nprint(title)\nprint("=" * len(title))\n'
                'total = box + count * each\nprint(f"Items: {count} x {each} g")\n'
                'print(f"Total: {total} g = {total // 1000} kg")'),
               ("забыт вес пустой коробки",
                'title = f"Box #{number}: {item}"\nprint(title)\nprint("=" * len(title))\n'
                'total = count * each\nprint(f"Items: {count} x {each} g")\n'
                'print(f"Total: {total} g = {total / 1000} kg")')],
        must_use=MUST_FSTR,
    ),
    OutputTask(
        skill=FSTR, difficulty=3, slug="py-int-fstrings-airport", title="Парковка в аэропорту",
        given=["car", "days", "per_day"],
        variants=[{"car": '"Kia Rio"', "days": '"9"', "per_day": "350"}],
        hidden=[{"car": '"Lada Vesta"', "days": '"14"', "per_day": "200"},
                {"car": '"Skoda Octavia"', "days": '"6"', "per_day": "400"},
                {"car": '"Haval Jolion"', "days": '"7"', "per_day": "500"},
                {"car": '"Toyota Camry"', "days": '"20"', "per_day": "300"},
                {"car": '"Mini Cooper"', "days": '"13"', "per_day": "280"}],
        intro="Семья улетает в отпуск и оставляет машину `car = {car}` на парковке аэропорта. Сайт бронирования "
              "прислал число дней стоянки строкой: `days = {days}`. День стоянки стоит `per_day = {per_day}` руб., "
              "а за каждую полную неделю (7 дней) парковка дарит один бесплатный день.",
        steps=["Преврати `days` в целое число и сохрани в `stay`.",
               "Посчитай бесплатные дни `free` — `stay`, делённое нацело на 7, — и сумму к оплате `cost`: платные дни "
               "(`stay - free`), умноженные на `per_day`.",
               "С помощью f-строк выведи четыре строки: `Parking: <car>, <stay> days`, `Free days: <free>`, "
               "`To pay: <cost> rub` и `Saved: <free * per_day> rub` — экономию посчитай прямо в фигурных скобках. "
               "Например, для стоянки на `\"14\"` дней по 200 руб. последние три строки — `Free days: 2`, "
               "`To pay: 2400 rub`, `Saved: 400 rub`."],
        hint="Со строкой `\"9\"` деление не работает, нужен `int(days)`. `9 // 7` даёт `1` полную неделю — значит, "
             "один бесплатный день. Без скобок `stay - free * per_day` Python сначала умножит, а потом вычтет.",
        solution='stay = int(days)\nfree = stay // 7\ncost = (stay - free) * per_day\n'
                 'print(f"Parking: {car}, {stay} days")\nprint(f"Free days: {free}")\nprint(f"To pay: {cost} rub")\n'
                 'print(f"Saved: {free * per_day} rub")',
        wrong=[("бесплатные дни не вычтены из оплаты",
                'stay = int(days)\nfree = stay // 7\ncost = stay * per_day\n'
                'print(f"Parking: {car}, {stay} days")\nprint(f"Free days: {free}")\nprint(f"To pay: {cost} rub")\n'
                'print(f"Saved: {free * per_day} rub")'),
               ("бесплатные дни посчитаны остатком % вместо деления нацело",
                'stay = int(days)\nfree = stay % 7\ncost = (stay - free) * per_day\n'
                'print(f"Parking: {car}, {stay} days")\nprint(f"Free days: {free}")\nprint(f"To pay: {cost} rub")\n'
                'print(f"Saved: {free * per_day} rub")'),
               ("нет скобок: stay - free * per_day",
                'stay = int(days)\nfree = stay // 7\ncost = stay - free * per_day\n'
                'print(f"Parking: {car}, {stay} days")\nprint(f"Free days: {free}")\nprint(f"To pay: {cost} rub")\n'
                'print(f"Saved: {free * per_day} rub")'),
               ("пропущена буква f в последней строке",
                'stay = int(days)\nfree = stay // 7\ncost = (stay - free) * per_day\n'
                'print(f"Parking: {car}, {stay} days")\nprint(f"Free days: {free}")\nprint(f"To pay: {cost} rub")\n'
                'print("Saved: {free * per_day} rub")')],
        must_use=MUST_FSTR,
    ),
]
