"""Training attestation («Тренировочная аттестация»), Python, topics 1–14 (up to PY_LOGICAL_AND) — theme: science,
space and technology. Each task touches every topic of the tier: print with several values, own variables, assignment,
arithmetic, order of execution, int/float (`/` or a float factor gives a float), strings glued with `+`, int()/str(),
// and %, += -=, f-strings, if/else, comparison operators, and.
Not yet: or/not, elif, truthiness of non-bool values, loops, lists, string methods and slices, functions, :.2f."""
from build import OutputTask

SKILL = "PY_LOGICAL_AND"
AND = [("And", "Используй and, чтобы объединить проверки в одном условии")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac14-rover", title="Марсоход едет к кратеру",
        given=["rover", "distance", "speed", "battery"],
        variants=[{"rover": '"Iskra"', "distance": '"1250"', "speed": "50", "battery": "70"}],
        hidden=[{"rover": '"Zarya"', "distance": '"900"', "speed": "40", "battery": "47"},
                {"rover": '"Vostok"', "distance": '"1500"', "speed": "50", "battery": "90"},
                {"rover": '"Sokol"', "distance": '"2480"', "speed": "80", "battery": "95"},
                {"rover": '"Rassvet"', "distance": '"760"', "speed": "40", "battery": "35"},
                {"rover": '"Luch"', "distance": '"45"', "speed": "30", "battery": "25"}],
        intro="Марсоход `rover = {rover}` должен доехать до кратера. Центр управления передал расстояние до кратера "
              "в метрах строкой: `distance = {distance}`. Марсоход едет со скоростью `speed = {speed}` метров в час, "
              "заряд батареи — `battery = {battery}` процентов. В пути его заряжают солнечные панели, но после каждых "
              "полных 100 метров он останавливается сделать снимок, и каждая остановка тратит 3 процента заряда. "
              "Через 30 часов начнётся пылевая буря.",
        steps=["Преврати `distance` в целое число через `int()` и сохрани в `d`.",
               "Выведи склейкой строк через `+` строку `<rover>: <d> m to the crater`; число `d` перед склейкой "
               "преврати в строку через `str()`. Например: `Zarya: 900 m to the crater`.",
               "Посчитай число остановок `stops` (деление `//` на 100) и длину последнего отрезка пути `tail` "
               "(остаток `%` от деления на 100). Выведи через `print` с запятыми: `Stops:`, `stops`, "
               "`last stretch:`, `tail`, `m` — например `Stops: 9 last stretch: 0 m`.",
               "Посчитай время в пути `hours = d / speed` и выведи f-строкой `Drive time: <hours> h` — например "
               "`Drive time: 22.5 h`.",
               "Уменьши `battery` на заряд, потраченный на остановки (`stops * 3`), через `-=`.",
               "Если после этого заряда осталось не меньше 20 процентов **и** дорога займёт не больше 30 часов, "
               "выведи f-строкой `Go! Battery at the crater: <battery>%`. Иначе выведи `Stay and charge`."],
        hint="`1250 // 100` — это 12 остановок, `1250 % 100` — последние 50 м. Деление `/` даёт дробное число: "
             "`900 / 40` — это `22.5`, а `1250 / 50` — `25.0`. Ровно 20 процентов заряда и ровно 30 часов в пути "
             "ещё подходят.",
        solution='d = int(distance)\nprint(rover + ": " + str(d) + " m to the crater")\nstops = d // 100\ntail = d % 100\n'
                 'print("Stops:", stops, "last stretch:", tail, "m")\nhours = d / speed\n'
                 'print(f"Drive time: {hours} h")\nbattery -= stops * 3\nif battery >= 20 and hours <= 30:\n'
                 '    print(f"Go! Battery at the crater: {battery}%")\nelse:\n    print("Stay and charge")',
        wrong=[("строгое сравнение: с зарядом ровно 20 процентов марсоход не едет",
                'd = int(distance)\nprint(rover + ": " + str(d) + " m to the crater")\nstops = d // 100\ntail = d % 100\n'
                'print("Stops:", stops, "last stretch:", tail, "m")\nhours = d / speed\n'
                'print(f"Drive time: {hours} h")\nbattery -= stops * 3\nif battery > 20 and hours <= 30:\n'
                '    print(f"Go! Battery at the crater: {battery}%")\nelse:\n    print("Stay and charge")'),
               ("забыт расход заряда на остановки",
                'd = int(distance)\nprint(rover + ": " + str(d) + " m to the crater")\nstops = d // 100\ntail = d % 100\n'
                'print("Stops:", stops, "last stretch:", tail, "m")\nhours = d / speed\n'
                'print(f"Drive time: {hours} h")\nif battery >= 20 and hours <= 30:\n'
                '    print(f"Go! Battery at the crater: {battery}%")\nelse:\n    print("Stay and charge")'),
               ("забыта проверка времени до бури",
                'd = int(distance)\nprint(rover + ": " + str(d) + " m to the crater")\nstops = d // 100\ntail = d % 100\n'
                'print("Stops:", stops, "last stretch:", tail, "m")\nhours = d / speed\n'
                'print(f"Drive time: {hours} h")\nbattery -= stops * 3\nif battery >= 20:\n'
                '    print(f"Go! Battery at the crater: {battery}%")\nelse:\n    print("Stay and charge")'),
               ("целочисленное деление вместо / : время в пути печатается без дробной части",
                'd = int(distance)\nprint(rover + ": " + str(d) + " m to the crater")\nstops = d // 100\ntail = d % 100\n'
                'print("Stops:", stops, "last stretch:", tail, "m")\nhours = d // speed\n'
                'print(f"Drive time: {hours} h")\nbattery -= stops * 3\nif battery >= 20 and hours <= 30:\n'
                '    print(f"Go! Battery at the crater: {battery}%")\nelse:\n    print("Stay and charge")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac14-station", title="Вода на орбитальной станции",
        given=["station", "water", "crew", "ship", "on_time"],
        variants=[{"station": '"Mir"', "water": '"500"', "crew": "4", "ship": "30", "on_time": "True"}],
        hidden=[{"station": '"Salyut"', "water": '"420"', "crew": "6", "ship": "30", "on_time": "True"},
                {"station": '"Zarya"', "water": '"300"', "crew": "5", "ship": "29", "on_time": "True"},
                {"station": '"Skylab"', "water": '"1000"', "crew": "4", "ship": "40", "on_time": "False"},
                {"station": '"Unity"', "water": '"0"', "crew": "2", "ship": "21", "on_time": "True"},
                {"station": '"Kosmos"', "water": '"230"', "crew": "5", "ship": "12", "on_time": "False"}],
        intro="На орбитальной станции `station = {station}` живут `crew = {crew}` космонавтов, каждый тратит 3 литра "
              "воды в день. Датчик бака передаёт запас воды в литрах строкой: `water = {water}`. Грузовой корабль "
              "с водой прилетит через `ship = {ship}` дней, а летит ли он по графику, записано в `on_time = {on_time}`.",
        steps=["Преврати `water` в целое число через `int()` и сохрани в `tank`. Система очистки вернула в бак ещё "
               "120 литров: увеличь `tank` на 120 через `+=`.",
               "Выведи склейкой строк через `+` строку `<station> tank: <tank> l`; число `tank` перед склейкой "
               "преврати в строку через `str()`. Например: `Salyut tank: 540 l`.",
               "Сохрани в `daily`, сколько литров экипаж тратит за день (`crew * 3`). Посчитай, на сколько полных "
               "дней хватит воды, — `days` (деление `//` на `daily`), и сколько литров останется сверх них — `rest` "
               "(остаток `%` от деления на `daily`).",
               "Выведи через `print` с запятыми: `Water for`, `days`, `days and`, `rest`, `l` — например "
               "`Water for 30 days and 0 l`.",
               "Выведи f-строкой `Per astronaut: <tank / crew> l` — например `Per astronaut: 90.0 l`.",
               "Если воды хватит до прилёта корабля (`days` не меньше `ship`) **и** корабль летит по графику "
               "(`on_time`), выведи `Water is fine`.",
               "Иначе экипаж переходит на экономию: каждый космонавт тратит на 1 литр в день меньше. Уменьши `daily` "
               "на `crew` через `-=` и выведи f-строкой `Save water: enough for <tank // daily> days`. Например, "
               "если в баке 420 литров, а космонавтов 5: `Save water: enough for 42 days`."],
        hint="`620 // 12` — это 51 полный день, `620 % 12` — 8 литров сверх них. Деление `/` даёт дробное число: "
             "`540 / 6` — это `90.0`. Если воды хватает ровно до дня прилёта корабля, этого достаточно. "
             "`on_time` уже равно `True` или `False` — сравнивать его с `True` не нужно.",
        solution='tank = int(water)\ntank += 120\nprint(station + " tank: " + str(tank) + " l")\ndaily = crew * 3\n'
                 'days = tank // daily\nrest = tank % daily\nprint("Water for", days, "days and", rest, "l")\n'
                 'print(f"Per astronaut: {tank / crew} l")\nif days >= ship and on_time:\n    print("Water is fine")\n'
                 'else:\n    daily -= crew\n    print(f"Save water: enough for {tank // daily} days")',
        wrong=[("строгое сравнение: если воды хватает ровно до прилёта корабля, экипаж всё равно экономит",
                'tank = int(water)\ntank += 120\nprint(station + " tank: " + str(tank) + " l")\ndaily = crew * 3\n'
                'days = tank // daily\nrest = tank % daily\nprint("Water for", days, "days and", rest, "l")\n'
                'print(f"Per astronaut: {tank / crew} l")\nif days > ship and on_time:\n    print("Water is fine")\n'
                'else:\n    daily -= crew\n    print(f"Save water: enough for {tank // daily} days")'),
               ("забыты 120 литров из системы очистки",
                'tank = int(water)\nprint(station + " tank: " + str(tank) + " l")\ndaily = crew * 3\n'
                'days = tank // daily\nrest = tank % daily\nprint("Water for", days, "days and", rest, "l")\n'
                'print(f"Per astronaut: {tank / crew} l")\nif days >= ship and on_time:\n    print("Water is fine")\n'
                'else:\n    daily -= crew\n    print(f"Save water: enough for {tank // daily} days")'),
               ("забыта проверка, летит ли корабль по графику",
                'tank = int(water)\ntank += 120\nprint(station + " tank: " + str(tank) + " l")\ndaily = crew * 3\n'
                'days = tank // daily\nrest = tank % daily\nprint("Water for", days, "days and", rest, "l")\n'
                'print(f"Per astronaut: {tank / crew} l")\nif days >= ship:\n    print("Water is fine")\n'
                'else:\n    daily -= crew\n    print(f"Save water: enough for {tank // daily} days")'),
               ("при экономии уменьшает расход на 1 литр на весь экипаж, а не на каждого",
                'tank = int(water)\ntank += 120\nprint(station + " tank: " + str(tank) + " l")\ndaily = crew * 3\n'
                'days = tank // daily\nrest = tank % daily\nprint("Water for", days, "days and", rest, "l")\n'
                'print(f"Per astronaut: {tank / crew} l")\nif days >= ship and on_time:\n    print("Water is fine")\n'
                'else:\n    daily -= 1\n    print(f"Save water: enough for {tank // daily} days")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac14-sprouts", title="Рассада для опыта",
        given=["plant", "seeds", "temp", "humidity"],
        variants=[{"plant": '"wheat"', "seeds": '"130"', "temp": "22", "humidity": "70"}],
        hidden=[{"plant": '"pea"', "seeds": '"96"', "temp": "18", "humidity": "60"},
                {"plant": '"oat"', "seeds": '"200"', "temp": "25", "humidity": "75"},
                {"plant": '"rye"', "seeds": '"50"', "temp": "26", "humidity": "80"},
                {"plant": '"bean"', "seeds": '"23"', "temp": "17", "humidity": "65"},
                {"plant": '"corn"', "seeds": '"144"', "temp": "21", "humidity": "59"}],
        intro="Биолаборатория проращивает семена `plant = {plant}` для опыта. Число семян пришло из заявки строкой: "
              "`seeds = {seeds}`. Семена сажают в лотки по 24 ячейки, а лишние — в отдельный горшок. Каждому лотку "
              "нужно 0.75 литра воды в день. В камере для проращивания сейчас `temp = {temp}` градусов и влажность "
              "`humidity = {humidity}` процентов. При хороших условиях ростки появляются через 5 дней.",
        steps=["Преврати `seeds` в целое число через `int()` и сохрани в `n`.",
               "Посчитай число полных лотков `trays` (деление `//` на 24) и число семян для горшка `spare` "
               "(остаток `%` от деления на 24).",
               "Выведи склейкой строк через `+` строку `<plant>: <trays> trays`; число `trays` перед склейкой "
               "преврати в строку через `str()`. Например: `pea: 4 trays`.",
               "Выведи через `print` с запятой: `Seeds in the pot:` и `spare` — например `Seeds in the pot: 0`.",
               "Посчитай воду на день `water = trays * 0.75` и выведи f-строкой `Water: <water> l a day` — "
               "например `Water: 3.0 l a day`.",
               "Сохрани в `days` число 5. Если температура от 18 до 25 градусов включительно **и** влажность "
               "не меньше 60 процентов, выведи `Good conditions`. Иначе ростки появятся на 3 дня позже: увеличь "
               "`days` на 3 через `+=` и выведи `Bad conditions`.",
               "В конце (в любом случае) выведи f-строкой `Sprouts in <days> days`."],
        hint="`130 // 24` — это 5 лотков, `130 % 24` — 10 семян в горшок. Целое число, умноженное на дробное, "
             "даёт дробное: `4 * 0.75` — это `3.0`. «От 18 до 25 включительно» — это две проверки: `temp >= 18` "
             "и `temp <= 25`; вместе с влажностью получается три проверки через `and`.",
        solution='n = int(seeds)\ntrays = n // 24\nspare = n % 24\nprint(plant + ": " + str(trays) + " trays")\n'
                 'print("Seeds in the pot:", spare)\nwater = trays * 0.75\nprint(f"Water: {water} l a day")\ndays = 5\n'
                 'if temp >= 18 and temp <= 25 and humidity >= 60:\n    print("Good conditions")\nelse:\n'
                 '    days += 3\n    print("Bad conditions")\nprint(f"Sprouts in {days} days")',
        wrong=[("строгое сравнение: ровно 25 градусов уже считается жарой",
                'n = int(seeds)\ntrays = n // 24\nspare = n % 24\nprint(plant + ": " + str(trays) + " trays")\n'
                'print("Seeds in the pot:", spare)\nwater = trays * 0.75\nprint(f"Water: {water} l a day")\ndays = 5\n'
                'if temp >= 18 and temp < 25 and humidity >= 60:\n    print("Good conditions")\nelse:\n'
                '    days += 3\n    print("Bad conditions")\nprint(f"Sprouts in {days} days")'),
               ("проверяет только нижнюю границу температуры",
                'n = int(seeds)\ntrays = n // 24\nspare = n % 24\nprint(plant + ": " + str(trays) + " trays")\n'
                'print("Seeds in the pot:", spare)\nwater = trays * 0.75\nprint(f"Water: {water} l a day")\ndays = 5\n'
                'if temp >= 18 and humidity >= 60:\n    print("Good conditions")\nelse:\n'
                '    days += 3\n    print("Bad conditions")\nprint(f"Sprouts in {days} days")'),
               ("забыта проверка влажности",
                'n = int(seeds)\ntrays = n // 24\nspare = n % 24\nprint(plant + ": " + str(trays) + " trays")\n'
                'print("Seeds in the pot:", spare)\nwater = trays * 0.75\nprint(f"Water: {water} l a day")\ndays = 5\n'
                'if temp >= 18 and temp <= 25:\n    print("Good conditions")\nelse:\n'
                '    days += 3\n    print("Bad conditions")\nprint(f"Sprouts in {days} days")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac14-update", title="Обновление программы",
        given=["app", "size", "free", "network"],
        variants=[{"app": '"Photon"', "size": '"2600"', "free": "8000", "network": '"wifi"'}],
        hidden=[{"app": '"Nova"', "size": '"1050"', "free": "2400", "network": '"cable"'},
                {"app": '"Atlas"', "size": '"250"', "free": "799", "network": '"wifi"'},
                {"app": '"Orbit"', "size": '"3900"', "free": "20000", "network": '"mobile"'},
                {"app": '"Pixel"', "size": '"10"', "free": "500", "network": '"wifi"'},
                {"app": '"Quark"', "size": '"655"', "free": "1000", "network": '"mobile"'}],
        intro="Программа `app = {app}` скачивает обновление на ноутбук. Сервер передаёт размер обновления в мегабайтах "
              "строкой: `size = {size}`, и к нему всегда добавляется пакет языков на 150 МБ. Файл качается частями "
              "по 400 МБ со скоростью 40 МБ в секунду. На диске свободно `free = {free}` МБ, а для установки нужно "
              "вдвое больше места, чем весит обновление. Сеть записана в `network = {network}`, она бывает `\"wifi\"`, "
              "`\"cable\"` или `\"mobile\"`; по мобильной сети обновление не ставят.",
        steps=["Преврати `size` в целое число через `int()` и сохрани в `mb`. Добавь пакет языков: увеличь `mb` "
               "на 150 через `+=`.",
               "Выведи склейкой строк через `+` строку `<app> update: <mb> MB`; число `mb` перед склейкой преврати "
               "в строку через `str()`. Например: `Nova update: 1200 MB`.",
               "Посчитай число полных частей `parts` (деление `//` на 400) и размер последней, неполной части `rest` "
               "(остаток `%` от деления на 400). Выведи через `print` с запятыми: `Parts:`, `parts`, `and`, `rest`, "
               "`MB` — например `Parts: 3 and 0 MB`.",
               "Посчитай время загрузки `seconds = mb / 40` и выведи f-строкой `Download: <seconds> s` — например "
               "`Download: 30.0 s`.",
               "Если места на диске хватает (`mb * 2` не больше `free`) **и** сеть не мобильная (`network` не равна "
               "`\"mobile\"`), выведи `Installing now`, иначе — `Update later`."],
        hint="`2750 // 400` — это 6 полных частей, `2750 % 400` — 350 МБ в последней. Деление `/` даёт дробное число: "
             "`1200 / 40` — это `30.0`. Если места ровно вдвое больше, чем весит обновление, установка возможна. "
             "Не равно — это `!=`; сеть `\"cable\"` тоже подходит.",
        solution='mb = int(size)\nmb += 150\nprint(app + " update: " + str(mb) + " MB")\nparts = mb // 400\nrest = mb % 400\n'
                 'print("Parts:", parts, "and", rest, "MB")\nseconds = mb / 40\nprint(f"Download: {seconds} s")\n'
                 'if mb * 2 <= free and network != "mobile":\n    print("Installing now")\nelse:\n    print("Update later")',
        wrong=[("строгое сравнение: когда места ровно вдвое больше, обновление не ставится",
                'mb = int(size)\nmb += 150\nprint(app + " update: " + str(mb) + " MB")\nparts = mb // 400\nrest = mb % 400\n'
                'print("Parts:", parts, "and", rest, "MB")\nseconds = mb / 40\nprint(f"Download: {seconds} s")\n'
                'if mb * 2 < free and network != "mobile":\n    print("Installing now")\nelse:\n    print("Update later")'),
               ("пускает только Wi-Fi: по кабелю обновление тоже не ставится",
                'mb = int(size)\nmb += 150\nprint(app + " update: " + str(mb) + " MB")\nparts = mb // 400\nrest = mb % 400\n'
                'print("Parts:", parts, "and", rest, "MB")\nseconds = mb / 40\nprint(f"Download: {seconds} s")\n'
                'if mb * 2 <= free and network == "wifi":\n    print("Installing now")\nelse:\n    print("Update later")'),
               ("сравнивает место с размером обновления, а не с удвоенным",
                'mb = int(size)\nmb += 150\nprint(app + " update: " + str(mb) + " MB")\nparts = mb // 400\nrest = mb % 400\n'
                'print("Parts:", parts, "and", rest, "MB")\nseconds = mb / 40\nprint(f"Download: {seconds} s")\n'
                'if mb <= free and network != "mobile":\n    print("Installing now")\nelse:\n    print("Update later")'),
               ("забыта проверка сети",
                'mb = int(size)\nmb += 150\nprint(app + " update: " + str(mb) + " MB")\nparts = mb // 400\nrest = mb % 400\n'
                'print("Parts:", parts, "and", rest, "MB")\nseconds = mb / 40\nprint(f"Download: {seconds} s")\n'
                'if mb * 2 <= free:\n    print("Installing now")\nelse:\n    print("Update later")')],
        constructs=["if"],
        must_use=AND,
    ),
]
