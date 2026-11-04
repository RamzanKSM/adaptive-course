"""PY_TRUTHINESS — «Истинность значений». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, += -=, f-strings, if/else, comparison operators, and, or/not, elif.
Not yet: loops, lists, functions."""
from build import OutputTask

SKILL = "PY_TRUTHINESS"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-tr-greeting", title="Приветствие на сайте",
        given=["name", "phone"],
        variants=[{"name": '"Anya"', "phone": '""'}, {"name": '""', "phone": '"+79001234567"'},
                  {"name": '"Boris"', "phone": '"+79115550011"'}],
        hidden=[{"name": '""', "phone": '""'}, {"name": '"Vera"', "phone": '"123"'}, {"name": '"Oleg"', "phone": '""'}],
        intro="Сайт здоровается с посетителем. Имя посетителя записано в `name = {name}`, телефон — в `phone = {phone}`. "
              "Если посетитель что-то не заполнил, там пустая строка `\"\"`.",
        steps=["Если строка `name` не пустая, выведи f-строкой `Hello, <name>!`, иначе выведи `Hello, guest!`. "
               "Пиши условие просто `if name:` — без сравнений.",
               "Затем, если телефон пустой, выведи `Please add a phone`, а иначе выведи `Phone saved`. "
               "Для пустой строки используй `not`: `if not phone:`.",
               "Например, для `name = \"Vera\"` и `phone = \"\"` программа выводит `Hello, Vera!` и `Please add a phone`."],
        hint="В условии строка сама превращается в `True` или `False`: пустая строка `\"\"` ложна, "
             "любая непустая — истинна. `not` переворачивает значение: `not \"\"` — это `True`.",
        solution='if name:\n    print(f"Hello, {name}!")\nelse:\n    print("Hello, guest!")\nif not phone:\n'
                 '    print("Please add a phone")\nelse:\n    print("Phone saved")',
        wrong=[("забыт not: просит телефон, когда он уже есть",
                'if name:\n    print(f"Hello, {name}!")\nelse:\n    print("Hello, guest!")\nif phone:\n'
                '    print("Please add a phone")\nelse:\n    print("Phone saved")'),
               ("лишний not в первом условии: ветки срабатывают наоборот",
                'if not name:\n    print(f"Hello, {name}!")\nelse:\n    print("Hello, guest!")\nif not phone:\n'
                '    print("Please add a phone")\nelse:\n    print("Phone saved")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-tr-player-card", title="Карточка игрока",
        given=["nickname", "name", "city", "level"],
        variants=[{"nickname": '"Dragon"', "name": '"Ivan"', "city": '""', "level": "7"},
                  {"nickname": '""', "name": '"Masha"', "city": '"Kazan"', "level": "0"},
                  {"nickname": '""', "name": '"Petr"', "city": '""', "level": "12"}],
        hidden=[{"nickname": '"Fox"', "name": '"Lena"', "city": '"Omsk"', "level": "3"},
                {"nickname": '""', "name": '"Gleb"', "city": '"Tula"', "level": "0"},
                {"nickname": '"Owl"', "name": '"Nina"', "city": '""', "level": "0"}],
        intro="В игре на карточке игрока показывают его ник, город и уровень. Ник — `nickname = {nickname}`, "
              "настоящее имя — `name = {name}`, город — `city = {city}`, уровень — `level = {level}`. "
              "Незаполненные строки пустые, а у новичка уровень 0.",
        steps=["Сохрани в переменную `shown` ник, а если ник пустой — имя. Запиши это одной строкой: `shown = nickname or name`.",
               "Так же сохрани в `place` город, а если он пустой — строку `\"Unknown city\"`.",
               "Сохрани в `start` уровень, а если он равен 0 — число 1 (тоже через `or`).",
               "С помощью f-строк выведи `Player: <shown>`, `From: <place>` и `Level: <start>`.",
               "Например, для ника `\"Fox\"`, города `\"Omsk\"` и уровня 3 программа выводит `Player: Fox`, `From: Omsk`, "
               "`Level: 3`."],
        hint="`a or b` возвращает `a`, если `a` истинно, а иначе — `b`. Пустая строка и число 0 ложны, поэтому "
             "`\"\" or \"Guest\"` даёт `\"Guest\"`, а `0 or 1` даёт `1`. Порядок важен: сначала то, что хотим показать.",
        solution='shown = nickname or name\nplace = city or "Unknown city"\nstart = level or 1\nprint(f"Player: {shown}")\n'
                 'print(f"From: {place}")\nprint(f"Level: {start}")',
        wrong=[("части or переставлены: показывает имя даже при заполненном нике",
                'shown = name or nickname\nplace = city or "Unknown city"\nstart = level or 1\nprint(f"Player: {shown}")\n'
                'print(f"From: {place}")\nprint(f"Level: {start}")'),
               ("and вместо or: для уровня 0 печатается 0",
                'shown = nickname or name\nplace = city or "Unknown city"\nstart = level and 1\nprint(f"Player: {shown}")\n'
                'print(f"From: {place}")\nprint(f"Level: {start}")')],
        must_use=[("BoolOp", "Используй or, чтобы подставить значение по умолчанию")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-tr-order-form", title="Оформление заказа",
        given=["count", "address", "phone"],
        variants=[{"count": "3", "address": '"Lenina 5"', "phone": '"+79001112233"'},
                  {"count": "0", "address": '"Mira 12"', "phone": '"+79004445566"'},
                  {"count": "2", "address": '"Sadovaya 7"', "phone": '""'}],
        hidden=[{"count": "1", "address": '""', "phone": '"+7900"'}, {"count": "0", "address": '""', "phone": '""'},
                {"count": "5", "address": '"Gagarina 1"', "phone": '"8800"'}, {"count": "4", "address": '""', "phone": '""'}],
        intro="Интернет-магазин проверяет заказ перед отправкой. В корзине `count = {count}` товаров, адрес — "
              "`address = {address}`, телефон — `phone = {phone}`. Незаполненное поле — пустая строка.",
        steps=["Выведи f-строкой `Items: <count>`.",
               "Если корзина пуста (`count` равно 0), выведи `Cart is empty`. Проверь это через истинность: `if not count:`.",
               "Иначе, если заполнены **и** адрес, **и** телефон, выведи `Order of <count> items accepted`.",
               "Иначе выведи `Fill in address and phone`.",
               "Например, для 1 товара, пустого адреса и телефона `\"+7900\"` программа выводит `Items: 1` и "
               "`Fill in address and phone`."],
        hint="Число 0 ложно, любое другое — истинно; пустая строка ложна, непустая — истинна. "
             "Поэтому `address and phone` истинно, только когда обе строки не пустые.",
        solution='print(f"Items: {count}")\nif not count:\n    print("Cart is empty")\nelif address and phone:\n'
                 '    print(f"Order of {count} items accepted")\nelse:\n    print("Fill in address and phone")',
        wrong=[("or вместо and: хватает одного заполненного поля",
                'print(f"Items: {count}")\nif not count:\n    print("Cart is empty")\nelif address or phone:\n'
                '    print(f"Order of {count} items accepted")\nelse:\n    print("Fill in address and phone")'),
               ("забыт not: пустой считается полная корзина",
                'print(f"Items: {count}")\nif count:\n    print("Cart is empty")\nelif address and phone:\n'
                '    print(f"Order of {count} items accepted")\nelse:\n    print("Fill in address and phone")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-tr-promo-code", title="Промокод в корзине",
        given=["price", "count", "promo"],
        variants=[{"price": "450", "count": "2", "promo": '"SUMMER"'}, {"price": "120", "count": "5", "promo": '""'},
                  {"price": "990", "count": "1", "promo": '"HELLO"'}],
        hidden=[{"price": "300", "count": "3", "promo": '""'}, {"price": "75", "count": "4", "promo": '"A"'},
                {"price": "1000", "count": "2", "promo": '"VIP"'}, {"price": "50", "count": "1", "promo": '""'}],
        intro="В корзине `count = {count}` товаров по `price = {price}` руб. В поле промокода покупатель ввёл "
              "`promo = {promo}` — если поле не заполнено, там пустая строка. Любой непустой промокод даёт скидку 100 руб.",
        steps=["Посчитай стоимость покупки (`price` умножить на `count`) и сохрани в `total`.",
               "Если промокод введён (`if promo:`), уменьши `total` на 100 с помощью `-=` и выведи f-строкой "
               "`Promo <promo>: -100 rub`.",
               "Иначе выведи `No promo`.",
               "В конце (в любом случае) выведи `To pay: <total> rub`.",
               "Например, для 3 товаров по 300 руб. без промокода программа выводит `No promo` и `To pay: 900 rub`."],
        hint="Пустая строка `\"\"` в условии ложна, а строка из пробела `\" \"` — уже истинна. "
             "Поэтому проще всего писать `if promo:`, а не сравнивать с пустой строкой вручную.",
        solution='total = price * count\nif promo:\n    total -= 100\n    print(f"Promo {promo}: -100 rub")\nelse:\n'
                 '    print("No promo")\nprint(f"To pay: {total} rub")',
        wrong=[("сравнивает с пробелом вместо пустой строки — скидка даётся всегда",
                'total = price * count\nif promo != " ":\n    total -= 100\n    print(f"Promo {promo}: -100 rub")\nelse:\n'
                '    print("No promo")\nprint(f"To pay: {total} rub")'),
               ("not перед promo: скидка достаётся тем, кто промокод не ввёл",
                'total = price * count\nif not promo:\n    total -= 100\n    print(f"Promo {promo}: -100 rub")\nelse:\n'
                '    print("No promo")\nprint(f"To pay: {total} rub")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-tr-school-buses", title="Автобусы на экскурсию",
        given=["people", "seats"],
        variants=[{"people": "95", "seats": "40"}, {"people": "120", "seats": "30"}, {"people": "47", "seats": "45"}],
        hidden=[{"people": "80", "seats": "40"}, {"people": "81", "seats": "40"}, {"people": "10", "seats": "50"},
                {"people": "100", "seats": "33"}],
        intro="Школа везёт `people = {people}` учеников на экскурсию. В одном автобусе `seats = {seats}` мест. "
              "Нужно понять, сколько заказать автобусов и сколько человек поедет в неполном автобусе.",
        steps=["Посчитай, сколько автобусов заполнится целиком (`people // seats`), и сохрани в `buses`.",
               "Посчитай, сколько учеников осталось без места (`people % seats`), и сохрани в `rest`.",
               "Если `rest` не ноль (проверь просто `if rest:`), увеличь `buses` на 1 с помощью `+=`.",
               "Выведи f-строкой `Buses: <buses>`.",
               "Затем, если `rest` не ноль, выведи `Last bus: <rest> people`, иначе выведи `All buses are full`.",
               "Например, для 81 ученика и 40 мест программа выводит `Buses: 3` и `Last bus: 1 people`, "
               "а для 80 учеников — `Buses: 2` и `All buses are full`."],
        hint="Число 0 в условии ложно, а любое другое число — истинно. Поэтому `if rest:` значит «если остаток не ноль». "
             "Деление нацело `//` даёт число полных автобусов, остаток `%` — сколько учеников не поместилось.",
        solution='buses = people // seats\nrest = people % seats\nif rest:\n    buses += 1\nprint(f"Buses: {buses}")\n'
                 'if rest:\n    print(f"Last bus: {rest} people")\nelse:\n    print("All buses are full")',
        wrong=[("not перед rest: лишний автобус заказывается, когда все поместились",
                'buses = people // seats\nrest = people % seats\nif not rest:\n    buses += 1\nprint(f"Buses: {buses}")\n'
                'if rest:\n    print(f"Last bus: {rest} people")\nelse:\n    print("All buses are full")'),
               ("путает // и %: в rest попадает частное",
                'buses = people // seats\nrest = people // seats\nif rest:\n    buses += 1\nprint(f"Buses: {buses}")\n'
                'if rest:\n    print(f"Last bus: {rest} people")\nelse:\n    print("All buses are full")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-tr-profile-filled", title="Заполненность профиля",
        given=["name", "city", "age"],
        variants=[{"name": '"Anya"', "city": '""', "age": "16"}, {"name": '""', "city": '"Sochi"', "age": "0"},
                  {"name": '"Boris"', "city": '"Kazan"', "age": "19"}],
        hidden=[{"name": '""', "city": '""', "age": "0"}, {"name": '"Ira"', "city": '"Omsk"', "age": "0"},
                {"name": '""', "city": '""', "age": "20"}, {"name": '"Max"', "city": '"Tver"', "age": "33"}],
        intro="Соцсеть показывает, насколько заполнен профиль. Имя — `name = {name}`, город — `city = {city}`, "
              "возраст — `age = {age}`. Пустая строка или возраст 0 значат, что поле не заполнено. "
              "Имя даёт 40%, город — 30%, возраст — 30%.",
        steps=["Заведи переменную `score = 0`.",
               "Тремя отдельными `if` проверь поля через истинность (`if name:`, `if city:`, `if age:`) "
               "и для каждого заполненного прибавь к `score` его проценты с помощью `+=`.",
               "Выведи f-строкой `Profile: <score>%`.",
               "Если `score` равен 100, выведи `Profile complete`, иначе выведи `Missing: <100 - score>%`.",
               "Например, для заполненных имени и города и возраста 0 программа выводит `Profile: 70%` и `Missing: 30%`."],
        hint="Проверки идут отдельными `if`, а не через `elif`: каждое поле добавляет свои проценты независимо от других. "
             "Пустая строка и 0 в условии ложны.",
        solution='score = 0\nif name:\n    score += 40\nif city:\n    score += 30\nif age:\n    score += 30\n'
                 'print(f"Profile: {score}%")\nif score == 100:\n    print("Profile complete")\nelse:\n'
                 '    print(f"Missing: {100 - score}%")',
        wrong=[("not перед age: возраст засчитывается, когда он не заполнен",
                'score = 0\nif name:\n    score += 40\nif city:\n    score += 30\nif not age:\n    score += 30\n'
                'print(f"Profile: {score}%")\nif score == 100:\n    print("Profile complete")\nelse:\n'
                '    print(f"Missing: {100 - score}%")'),
               ("elif вместо if: после имени город уже не проверяется",
                'score = 0\nif name:\n    score += 40\nelif city:\n    score += 30\nif age:\n    score += 30\n'
                'print(f"Profile: {score}%")\nif score == 100:\n    print("Profile complete")\nelse:\n'
                '    print(f"Missing: {100 - score}%")')],
        constructs=["if"],
    ),
]
