"""PY_BASIC_CODE_READING — «Вывод с print». Taught before: nothing, this is the first topic. The starter already holds the
given values in variables; the student only passes them to print (several arguments, an empty print(), sep= and end=).
Not yet: creating own variables, assignment, arithmetic, string concatenation, f-strings, conditions, loops."""
from build import OutputTask

SKILL = "PY_BASIC_CODE_READING"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-pr-boarding-pass", title="Посадочный талон",
        given=["name", "flight", "seat"],
        variants=[{"name": '"Anya Petrova"', "flight": '"SU 1402"', "seat": '"14C"'},
                  {"name": '"Boris Orlov"', "flight": '"S7 2051"', "seat": '"3A"'},
                  {"name": '"Dina Sokolova"', "flight": '"U6 318"', "seat": '"22F"'}],
        hidden=[{"name": '"Ivan Belov"', "flight": '"SU 7"', "seat": '"1B"'},
                {"name": '"Olga Frolova"', "flight": '"DP 404"', "seat": '"30D"'},
                {"name": '"Timur Ziyatdinov"', "flight": '"S7 99"', "seat": '"12E"'}],
        intro="Авиакомпания печатает посадочный талон. Данные пассажира уже лежат в заготовке: имя `name = {name}`, "
              "рейс `flight = {flight}` и место `seat = {seat}`.",
        steps=["Первой строкой выведи заголовок `BOARDING PASS`.",
               "Второй строкой выведи `Passenger:` и имя пассажира.",
               "Третьей строкой выведи `Flight:` и номер рейса.",
               "Четвёртой строкой выведи `Seat:` и место. Например, для места `\"5A\"` строка будет `Seat: 5A`."],
        hint='В `print` можно передать несколько значений через запятую — Python выведет их через пробел: '
             '`print("Seat:", seat)`. Имя переменной пиши без кавычек: `print("seat")` выведет само слово `seat`.',
        solution='print("BOARDING PASS")\nprint("Passenger:", name)\nprint("Flight:", flight)\nprint("Seat:", seat)',
        wrong=[("берёт имя переменной в кавычки и печатает слово seat",
                'print("BOARDING PASS")\nprint("Passenger:", name)\nprint("Flight:", flight)\nprint("Seat:", "seat")'),
               ("путает порядок строк: место печатается раньше рейса",
                'print("BOARDING PASS")\nprint("Passenger:", name)\nprint("Seat:", seat)\nprint("Flight:", flight)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-pr-recipe-card", title="Карточка рецепта",
        given=["dish", "minutes", "portions"],
        variants=[{"dish": '"Pancakes"', "minutes": "25", "portions": "4"},
                  {"dish": '"Borscht"', "minutes": "90", "portions": "6"},
                  {"dish": '"Omelette"', "minutes": "10", "portions": "2"}],
        hidden=[{"dish": '"Pilaf"', "minutes": "60", "portions": "8"},
                {"dish": '"Salad"', "minutes": "15", "portions": "3"},
                {"dish": '"Tea"', "minutes": "5", "portions": "1"}],
        intro="На сайте рецептов под каждым блюдом печатается маленькая карточка. В заготовке уже есть название блюда "
              "`dish = {dish}`, время готовки в минутах `minutes = {minutes}` и число порций `portions = {portions}`.",
        steps=["Первой строкой выведи название блюда.",
               "Второй строкой выведи `Time:`, число минут и слово `min`. Например, для 30 минут: `Time: 30 min`.",
               "Третьей строкой выведи `Portions:` и число порций.",
               "Последней строкой выведи `Enjoy!`."],
        hint='Одним `print` можно вывести и текст, и число, и снова текст: `print("Time:", minutes, "min")`. '
             "Между значениями Python сам поставит пробелы.",
        solution='print(dish)\nprint("Time:", minutes, "min")\nprint("Portions:", portions)\nprint("Enjoy!")',
        wrong=[("забывает слово min после минут",
                'print(dish)\nprint("Time:", minutes)\nprint("Portions:", portions)\nprint("Enjoy!")'),
               ("печатает слово dish вместо названия блюда",
                'print("dish")\nprint("Time:", minutes, "min")\nprint("Portions:", portions)\nprint("Enjoy!")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-pr-shopping-list", title="Список покупок",
        given=["item1", "item2", "item3"],
        variants=[{"item1": '"milk"', "item2": '"bread"', "item3": '"eggs"'},
                  {"item1": '"apples"', "item2": '"cheese"', "item3": '"rice"'},
                  {"item1": '"tea"', "item2": '"sugar"', "item3": '"lemons"'}],
        hidden=[{"item1": '"butter"', "item2": '"fish"', "item3": '"salt"'},
                {"item1": '"juice"', "item2": '"pasta"', "item3": '"onions"'},
                {"item1": '"soap"', "item2": '"coffee"', "item3": '"honey"'}],
        intro="Мама попросила распечатать список покупок. Три товара уже записаны в заготовке: "
              "`item1 = {item1}`, `item2 = {item2}` и `item3 = {item3}`.",
        steps=["Первой строкой выведи заголовок `Shopping list`.",
               "Второй строкой выведи пустую строку — вызови `print()` без аргументов.",
               "Дальше выведи три пронумерованные строки: `1.` и первый товар, `2.` и второй, `3.` и третий. "
               "Например, если первый товар `\"salt\"`, строка будет `1. salt`."],
        hint='`print()` без аргументов выводит пустую строку. Номер и товар выводи одним `print` через запятую: '
             '`print("1.", item1)`. Если написать `"item1"` в кавычках, выведется само слово `item1`.',
        solution='print("Shopping list")\nprint()\nprint("1.", item1)\nprint("2.", item2)\nprint("3.", item3)',
        wrong=[("берёт имя переменной в кавычки",
                'print("Shopping list")\nprint()\nprint("1.", item1)\nprint("2.", "item2")\nprint("3.", item3)'),
               ("забывает пустую строку после заголовка",
                'print("Shopping list")\nprint("1.", item1)\nprint("2.", item2)\nprint("3.", item3)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-pr-train-board", title="Табло на вокзале",
        given=["city", "hours", "minutes", "platform"],
        variants=[{"city": '"Kazan"', "hours": '"09"', "minutes": '"45"', "platform": "3"},
                  {"city": '"Sochi"', "hours": '"17"', "minutes": '"05"', "platform": "1"},
                  {"city": '"Samara"', "hours": '"22"', "minutes": '"30"', "platform": "7"}],
        hidden=[{"city": '"Omsk"', "hours": '"06"', "minutes": '"10"', "platform": "2"},
                {"city": '"Tver"', "hours": '"13"', "minutes": '"55"', "platform": "5"},
                {"city": '"Perm"', "hours": '"00"', "minutes": '"20"', "platform": "4"}],
        intro="На табло вокзала показывают ближайший поезд. В заготовке уже есть город `city = {city}`, "
              "время отправления — часы `hours = {hours}` и минуты `minutes = {minutes}`, и номер платформы `platform = {platform}`.",
        steps=["Первой строкой выведи `Train to` и город.",
               "Второй строкой выведи `Departs at`, пробел и время в виде часов и минут через двоеточие без пробелов. "
               "Сделай это двумя вызовами `print`: первый выводит `Departs at` и заканчивается пробелом вместо перевода "
               "строки (`end=\" \"`), второй выводит часы и минуты с разделителем `sep=\":\"`. "
               "Например, для `\"08\"` и `\"15\"` строка будет `Departs at 08:15`.",
               "Третьей строкой выведи `Platform` и номер платформы."],
        hint='`sep` задаёт, что `print` ставит между значениями (по умолчанию пробел): `print("a", "b", sep="-")` выводит `a-b`. '
             '`end` задаёт, чем `print` заканчивает строку (по умолчанию переводом строки): после `print("Hi", end=" ")` '
             "следующий `print` продолжит ту же строку.",
        solution='print("Train to", city)\nprint("Departs at", end=" ")\nprint(hours, minutes, sep=":")\n'
                 'print("Platform", platform)',
        wrong=[("забывает sep — между часами и минутами пробел вместо двоеточия",
                'print("Train to", city)\nprint("Departs at", end=" ")\nprint(hours, minutes)\nprint("Platform", platform)'),
               ("забывает end — время уходит на следующую строку",
                'print("Train to", city)\nprint("Departs at")\nprint(hours, minutes, sep=":")\nprint("Platform", platform)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-pr-file-path", title="Путь к файлу",
        given=["folder", "name", "ext"],
        variants=[{"folder": '"docs"', "name": '"report"', "ext": '"txt"'},
                  {"folder": '"photos"', "name": '"sea"', "ext": '"jpg"'},
                  {"folder": '"music"', "name": '"song"', "ext": '"mp3"'}],
        hidden=[{"folder": '"games"', "name": '"save"', "ext": '"dat"'},
                {"folder": '"work"', "name": '"plan"', "ext": '"pdf"'},
                {"folder": '"home"', "name": '"notes"', "ext": '"md"'}],
        intro="Текстовый редактор сохраняет файл и сообщает, куда. В заготовке уже есть папка `folder = {folder}`, "
              "имя файла `name = {name}` и расширение `ext = {ext}`.",
        steps=["Первой строкой выведи `Saving file...`.",
               "Второй строкой выведи полный путь: папку, `/`, имя, точку и расширение — без пробелов. "
               "Сделай это двумя вызовами `print`: первый выводит папку и имя с разделителем `sep=\"/\"` "
               "и заканчивает строку точкой (`end=\".\"`), второй выводит расширение. "
               "Например, для `\"a\"`, `\"b\"` и `\"c\"` строка будет `a/b.c`.",
               "Третьей строкой выведи `Folder:` и папку.",
               "Четвёртой строкой выведи `Type:` и расширение."],
        hint='В одном `print` можно указать и `sep`, и `end`: `print("x", "y", sep="+", end="!")` выведет `x+y!` '
             "и не перейдёт на новую строку — следующий `print` продолжит её.",
        solution='print("Saving file...")\nprint(folder, name, sep="/", end=".")\nprint(ext)\n'
                 'print("Folder:", folder)\nprint("Type:", ext)',
        wrong=[("забывает sep — между папкой и именем пробел вместо /",
                'print("Saving file...")\nprint(folder, name, end=".")\nprint(ext)\nprint("Folder:", folder)\nprint("Type:", ext)'),
               ("забывает end — расширение уходит на следующую строку без точки",
                'print("Saving file...")\nprint(folder, name, sep="/")\nprint(ext)\nprint("Folder:", folder)\nprint("Type:", ext)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-pr-cafe-receipt", title="Чек в кофейне",
        given=["drink", "drink_price", "snack", "snack_price"],
        variants=[{"drink": '"Coffee"', "drink_price": "150", "snack": '"Bun"', "snack_price": "60"},
                  {"drink": '"Tea"', "drink_price": "90", "snack": '"Cookie"', "snack_price": "45"},
                  {"drink": '"Cocoa"', "drink_price": "130", "snack": '"Croissant"', "snack_price": "110"}],
        hidden=[{"drink": '"Latte"', "drink_price": "210", "snack": '"Muffin"', "snack_price": "95"},
                {"drink": '"Juice"', "drink_price": "120", "snack": '"Donut"', "snack_price": "70"},
                {"drink": '"Water"', "drink_price": "50", "snack": '"Cake"', "snack_price": "180"}],
        intro="Кофейня печатает чек. В заготовке уже есть напиток `drink = {drink}` и его цена `drink_price = {drink_price}`, "
              "а также выпечка `snack = {snack}` и её цена `snack_price = {snack_price}`.",
        steps=["Первой строкой выведи `RECEIPT`.",
               "Второй строкой выведи напиток, двоеточие с пробелом, цену и ` rub`. Сделай это одним `print`: "
               "напиток и цену раздели через `sep=\": \"`, а строку закончи через `end=\" rub\\n\"` "
               "(`\\n` — это перевод строки). Например, для `\"Milk\"` за 40 строка будет `Milk: 40 rub`.",
               "Третьей строкой точно так же выведи выпечку и её цену.",
               "Затем выведи пустую строку.",
               "Последней строкой выведи `Thank you!`."],
        hint='`sep` ставится только между значениями, а `end` — один раз в конце: `print("Milk", 40, sep=": ", end=" rub\\n")` '
             "выводит `Milk: 40 rub` и переходит на новую строку. Если забыть `\\n` в `end`, следующий `print` продолжит ту же строку.",
        solution='print("RECEIPT")\nprint(drink, drink_price, sep=": ", end=" rub\\n")\n'
                 'print(snack, snack_price, sep=": ", end=" rub\\n")\nprint()\nprint("Thank you!")',
        wrong=[("забывает sep — вместо двоеточия пробел",
                'print("RECEIPT")\nprint(drink, drink_price, sep=": ", end=" rub\\n")\n'
                'print(snack, snack_price, end=" rub\\n")\nprint()\nprint("Thank you!")'),
               ("забывает \\n в end — следующая строка приклеивается",
                'print("RECEIPT")\nprint(drink, drink_price, sep=": ", end=" rub")\n'
                'print(snack, snack_price, sep=": ", end=" rub\\n")\nprint()\nprint("Thank you!")')],
    ),
]
