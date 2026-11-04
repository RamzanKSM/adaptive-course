"""PY_INTEGER_DIVISION — «Деление // и остаток %». Taught before: print (several values separated by commas), variables,
assignment, arithmetic, order of execution, int/float (`/` gives a float), strings, type conversion.
Not yet: += -=, f-strings, conditions, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_INTEGER_DIVISION"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-id-egg-boxes", title="Яйца по коробкам",
        given=["eggs", "box"],
        variants=[{"eggs": "47", "box": "10"}, {"eggs": "64", "box": "6"}, {"eggs": "100", "box": "12"}],
        hidden=[{"eggs": "30", "box": "10"}, {"eggs": "5", "box": "6"}, {"eggs": "131", "box": "20"}],
        intro="На птицеферме собрали `eggs = {eggs}` яиц. Их раскладывают в коробки по `box = {box}` штук. "
              "В продажу идут только полные коробки, а оставшиеся яйца забирают на кухню.",
        steps=["Посчитай число полных коробок `boxes` — `eggs`, делённые на `box` нацело (`//`).",
               "Посчитай, сколько яиц не поместилось в полные коробки: `left` — остаток от деления `eggs` на `box` (`%`).",
               "Выведи три строки через запятую в `print`: `Eggs:` и `eggs`, `Full boxes:` и `boxes`, `Left over:` и `left`. "
               "Например, для 25 яиц по 10 это `Eggs: 25`, `Full boxes: 2` и `Left over: 5`."],
        hint="`//` делит нацело и отбрасывает дробную часть: `25 // 10` даёт `2`. `%` даёт остаток: `25 % 10` — это `5`. "
             "Обычное деление `/` здесь не подходит: `25 / 10` даёт `2.5`, а половины коробки не бывает.",
        solution='boxes = eggs // box\nleft = eggs % box\nprint("Eggs:", eggs)\nprint("Full boxes:", boxes)\n'
                 'print("Left over:", left)',
        wrong=[("делит через `/` — коробок получается дробное число",
                'boxes = eggs / box\nleft = eggs % box\nprint("Eggs:", eggs)\nprint("Full boxes:", boxes)\n'
                'print("Left over:", left)'),
               ("путает `//` и `%`: остаток считает делением нацело",
                'boxes = eggs // box\nleft = eggs // box\nprint("Eggs:", eggs)\nprint("Full boxes:", boxes)\n'
                'print("Left over:", left)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-id-movie-length", title="Сколько идёт фильм",
        given=["title", "minutes"],
        variants=[{"title": '"Space Trip"', "minutes": "135"}, {"title": '"The Old Bridge"', "minutes": "98"},
                  {"title": '"Winter Tale"', "minutes": "172"}],
        hidden=[{"title": '"Short Film"', "minutes": "45"}, {"title": '"Two Hours"', "minutes": "120"},
                {"title": '"Epic"', "minutes": "201"}],
        intro="В афише кинотеатра длительность фильма `title = {title}` записана в минутах: `minutes = {minutes}`. "
              "Зрителям удобнее видеть часы и минуты.",
        steps=["Посчитай полные часы `hours` — `minutes`, делённые нацело на 60.",
               "Посчитай оставшиеся минуты `rest` — остаток от деления `minutes` на 60.",
               "Выведи название фильма `title`.",
               "Выведи через запятую `Length:` и `minutes` и `min`.",
               "Выведи через запятую `That is:`, `hours`, `h`, `rest` и `min`. Например, для 75 минут это "
               "`Length: 75 min` и `That is: 1 h 15 min`."],
        hint="В часе 60 минут, поэтому делим на 60, а не на 100. `75 // 60` даёт `1` час, `75 % 60` — `15` минут.",
        solution='hours = minutes // 60\nrest = minutes % 60\nprint(title)\nprint("Length:", minutes, "min")\n'
                 'print("That is:", hours, "h", rest, "min")',
        wrong=[("считает в часе 100 минут",
                'hours = minutes // 100\nrest = minutes % 100\nprint(title)\nprint("Length:", minutes, "min")\n'
                'print("That is:", hours, "h", rest, "min")'),
               ("вместо остатка печатает все минуты",
                'hours = minutes // 60\nrest = minutes % 60\nprint(title)\nprint("Length:", minutes, "min")\n'
                'print("That is:", hours, "h", minutes, "min")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-id-coin-change", title="Сдача монетами и купюрами",
        given=["change"],
        variants=[{"change": "387"}, {"change": "154"}, {"change": "903"}],
        hidden=[{"change": "100"}, {"change": "9"}, {"change": "760"}, {"change": "45"}],
        intro="Кассир выдаёт сдачу `change = {change}` руб. купюрами по 100 руб., монетами по 10 руб. и по 1 руб. "
              "Он всегда даёт как можно больше крупных денег. Нужно посчитать, сколько штук каждого номинала он выдаст.",
        steps=["Посчитай число сторублёвок `hundreds` — `change`, делённая нацело на 100.",
               "Посчитай, сколько рублей останется после них: `rest` — остаток от деления `change` на 100.",
               "Из `rest` посчитай число десяток `tens` (деление нацело на 10) и число рублёвых монет `ones` (остаток от деления на 10).",
               "Выведи три строки через запятую: `100 rub:` и `hundreds`, `10 rub:` и `tens`, `1 rub:` и `ones`. "
               "Например, для сдачи 256 руб. это `100 rub: 2`, `10 rub: 5` и `1 rub: 6`."],
        hint="Десятки нужно считать из остатка после сторублёвок, а не из всей сдачи: `256 // 10` даёт `25` — "
             "это все десятки вместе с теми, что уже выданы сторублёвками. А `256 % 100` даёт `56`, и `56 // 10` — это `5`.",
        solution='hundreds = change // 100\nrest = change % 100\ntens = rest // 10\nones = rest % 10\n'
                 'print("100 rub:", hundreds)\nprint("10 rub:", tens)\nprint("1 rub:", ones)',
        wrong=[("считает десятки из всей сдачи, а не из остатка",
                'hundreds = change // 100\nrest = change % 100\ntens = change // 10\nones = rest % 10\n'
                'print("100 rub:", hundreds)\nprint("10 rub:", tens)\nprint("1 rub:", ones)'),
               ("остаток после сторублёвок считает делением нацело",
                'hundreds = change // 100\nrest = change // 100\ntens = rest // 10\nones = rest % 10\n'
                'print("100 rub:", hundreds)\nprint("10 rub:", tens)\nprint("1 rub:", ones)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-id-clock-later", title="Который будет час",
        given=["hour", "passed"],
        variants=[{"hour": "21", "passed": "7"}, {"hour": "9", "passed": "30"}, {"hour": "14", "passed": "58"}],
        hidden=[{"hour": "0", "passed": "5"}, {"hour": "23", "passed": "1"}, {"hour": "12", "passed": "36"}, {"hour": "18", "passed": "72"}],
        intro="Поезд отправляется в `hour = {hour}` часов и едет `passed = {passed}` часов. Часы на вокзале показывают "
              "время от 0 до 23: после 23 часов снова идёт 0. Нужно узнать, в котором часу поезд приедет и сколько "
              "раз за дорогу наступит полночь.",
        steps=["Посчитай `total` — `hour` плюс `passed`.",
               "Посчитай, сколько раз наступит полночь: `days` — `total`, делённое нацело на 24.",
               "Посчитай час прибытия `arrive` — остаток от деления `total` на 24.",
               "Выведи три строки через запятую: `Departure:` и `hour`, `Midnights:` и `days`, `Arrival:` и `arrive`. "
               "Например, для отправления в 20 и 10 часов в пути это `Departure: 20`, `Midnights: 1` и `Arrival: 6`."],
        hint="Сначала сложи часы и только потом бери остаток. Без скобок `hour + passed % 24` Python возьмёт остаток "
             "только от `passed`: у `%` приоритет выше, чем у `+`. Ровно 24 часа дают `24 % 24`, то есть `0`.",
        solution='total = hour + passed\ndays = total // 24\narrive = total % 24\nprint("Departure:", hour)\n'
                 'print("Midnights:", days)\nprint("Arrival:", arrive)',
        wrong=[("берёт остаток только от времени в пути, без часа отправления",
                'total = hour + passed\ndays = total // 24\narrive = hour + passed % 24\nprint("Departure:", hour)\n'
                'print("Midnights:", days)\nprint("Arrival:", arrive)'),
               ("считает полночи по времени в пути, без часа отправления",
                'total = hour + passed\ndays = passed // 24\narrive = total % 24\nprint("Departure:", hour)\n'
                'print("Midnights:", days)\nprint("Arrival:", arrive)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-id-lucky-ticket", title="Цифры номера билета",
        given=["number"],
        variants=[{"number": "352"}, {"number": "907"}, {"number": "118"}],
        hidden=[{"number": "100"}, {"number": "999"}, {"number": "405"}, {"number": "260"}],
        intro="У Тимура трёхзначный номер автобусного билета: `number = {number}`. Он хочет узнать сумму цифр "
              "номера. Для этого номер нужно разобрать на цифры — без строк, только `//` и `%`.",
        steps=["Найди цифру сотен `hundreds` — `number`, делённый нацело на 100.",
               "Найди цифру десятков `tens`: сначала раздели `number` нацело на 10, затем возьми остаток от деления на 10.",
               "Найди цифру единиц `ones` — остаток от деления `number` на 10.",
               "Выведи четыре строки через запятую: `Hundreds:` и `hundreds`, `Tens:` и `tens`, `Ones:` и `ones`, "
               "`Sum:` и сумму трёх цифр. Например, для 254 это `Hundreds: 2`, `Tens: 5`, `Ones: 4` и `Sum: 11`."],
        hint="`254 // 10` даёт `25` — последняя цифра отброшена, а `25 % 10` даёт `5`. Это и есть цифра десятков. "
             "Если написать только `number // 10`, получится `25`, а не одна цифра.",
        solution='hundreds = number // 100\ntens = number // 10 % 10\nones = number % 10\nprint("Hundreds:", hundreds)\n'
                 'print("Tens:", tens)\nprint("Ones:", ones)\nprint("Sum:", hundreds + tens + ones)',
        wrong=[("не берёт остаток: вместо цифры десятков получается двузначное число",
                'hundreds = number // 100\ntens = number // 10\nones = number % 10\nprint("Hundreds:", hundreds)\n'
                'print("Tens:", tens)\nprint("Ones:", ones)\nprint("Sum:", hundreds + tens + ones)'),
               ("ищет цифру единиц делением нацело вместо остатка",
                'hundreds = number // 100\ntens = number // 10 % 10\nones = number // 10\nprint("Hundreds:", hundreds)\n'
                'print("Tens:", tens)\nprint("Ones:", ones)\nprint("Sum:", hundreds + tens + ones)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-id-marathon-time", title="Время на марафоне",
        given=["runner", "seconds"],
        variants=[{"runner": '"Anya"', "seconds": "13529"}, {"runner": '"Boris"', "seconds": "10984"},
                  {"runner": '"Mila"', "seconds": "16207"}],
        hidden=[{"runner": '"Oleg"', "seconds": "3600"}, {"runner": '"Ivan"', "seconds": "59"}, {"runner": '"Daria"', "seconds": "7261"},
                {"runner": '"Timur"', "seconds": "18000"}],
        intro="Секундомер марафона показывает время бегуна `runner = {runner}` одним числом — в секундах: "
              "`seconds = {seconds}`. Для таблицы результатов время нужно разложить на часы, минуты и секунды.",
        steps=["Посчитай часы `hours` — `seconds`, делённые нацело на 3600 (столько секунд в часе).",
               "Посчитай минуты `minutes`: возьми остаток от деления `seconds` на 3600 и раздели его нацело на 60.",
               "Посчитай секунды `secs` — остаток от деления `seconds` на 60.",
               "Выведи первой строкой имя бегуна `runner`, а второй — через запятую `Time:`, `hours`, `h`, `minutes`, `min`, `secs` и `s`.",
               "Последней строкой выведи через запятую `Check:` и время, собранное обратно в секунды: `hours * 3600` "
               "плюс `minutes * 60` плюс `secs`. Например, для 3725 секунд это `Time: 1 h 2 min 5 s` и `Check: 3725`."],
        hint="Минуты считаем только из того, что осталось после полных часов: `3725 % 3600` даёт `125`, а `125 // 60` — `2`. "
             "Если разделить на 60 все секунды сразу, получится `62` — сюда попадут минуты, уже вошедшие в часы.",
        solution='hours = seconds // 3600\nminutes = seconds % 3600 // 60\nsecs = seconds % 60\nprint(runner)\n'
                 'print("Time:", hours, "h", minutes, "min", secs, "s")\nprint("Check:", hours * 3600 + minutes * 60 + secs)',
        wrong=[("делит на 60 все секунды — в минуты попадают и часы",
                'hours = seconds // 3600\nminutes = seconds // 60\nsecs = seconds % 60\nprint(runner)\n'
                'print("Time:", hours, "h", minutes, "min", secs, "s")\nprint("Check:", hours * 3600 + minutes * 60 + secs)'),
               ("делит через `/` — часы получаются дробными",
                'hours = seconds / 3600\nminutes = seconds % 3600 // 60\nsecs = seconds % 60\nprint(runner)\n'
                'print("Time:", hours, "h", minutes, "min", secs, "s")\nprint("Check:", hours * 3600 + minutes * 60 + secs)')],
    ),
]
