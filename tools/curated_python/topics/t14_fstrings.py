"""PY_FSTRINGS — «f-строки». Taught before: print, variables, assignment, arithmetic, order of execution, int/float,
strings, type conversion, // and %, += -=.
Not yet: format specifiers like :.2f, conditions, comparisons, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_FSTRINGS"
FSTR = [("JoinedStr", "Используй f-строку: f\"...{переменная}...\"")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-fs-train-ticket", title="Билет на поезд",
        given=["name", "city", "seat", "price"],
        variants=[{"name": '"Anya Petrova"', "city": '"Kazan"', "seat": "14", "price": "2300"},
                  {"name": '"Boris Ivanov"', "city": '"Sochi"', "seat": "3", "price": "4150"},
                  {"name": '"Dina Orlova"', "city": '"Tver"', "seat": "27", "price": "980"}],
        hidden=[{"name": '"Ilya"', "city": '"Omsk"', "seat": "1", "price": "5000"},
                {"name": '"Vera Lis"', "city": '"Perm"', "seat": "52", "price": "1"},
                {"name": '"Oleg"', "city": '"Kursk"', "seat": "9", "price": "760"}],
        intro="Касса печатает билет на поезд из Москвы. Данные пассажира записаны в переменных: имя `name = {name}`, "
              "город `city = {city}`, место `seat = {seat}` и цена билета `price = {price}` руб. "
              "Сервисный сбор кассы — 50 руб.",
        steps=["Каждую строку выводи через `print` с f-строкой.",
               "Выведи `Passenger: ` и имя, затем `From Moscow to ` и город, затем `Seat: ` и место.",
               "Выведи `Price: `, цену и ` rub`.",
               "Последней строкой выведи `With fee: `, цену плюс 50 и ` rub`. "
               "Например, для цены 1000 последние строки — `Price: 1000 rub` и `With fee: 1050 rub`."],
        hint="Не забудь букву `f` перед кавычкой: без неё Python напечатает фигурные скобки как есть. "
             "Вычисление тоже пиши внутри скобок: `f\"{{price + 50}}\"`, иначе `+ 50` попадёт в текст.",
        solution='print(f"Passenger: {name}")\nprint(f"From Moscow to {city}")\nprint(f"Seat: {seat}")\n'
                 'print(f"Price: {price} rub")\nprint(f"With fee: {price + 50} rub")',
        wrong=[("забыта буква f — печатается {seat}",
                'print(f"Passenger: {name}")\nprint(f"From Moscow to {city}")\nprint("Seat: {seat}")\n'
                'print(f"Price: {price} rub")\nprint(f"With fee: {price + 50} rub")'),
               ("сложение вынесено за фигурные скобки и попадает в текст",
                'print(f"Passenger: {name}")\nprint(f"From Moscow to {city}")\nprint(f"Seat: {seat}")\n'
                'print(f"Price: {price} rub")\nprint(f"With fee: {price} + 50 rub")')],
        must_use=FSTR,
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-fs-weather", title="Прогноз погоды",
        given=["city", "day", "night"],
        variants=[{"city": '"Kazan"', "day": "18", "night": "7"}, {"city": '"Sochi"', "day": "26", "night": "19"},
                  {"city": '"Murmansk"', "day": "4", "night": "-3"}],
        hidden=[{"city": '"Omsk"', "day": "0", "night": "-12"}, {"city": '"Perm"', "day": "21", "night": "20"},
                {"city": '"Yakutsk"', "day": "-25", "night": "-38"}],
        intro="Приложение погоды показывает прогноз на сегодня. Город записан в `city = {city}`, "
              "температура днём — `day = {day}`, ночью — `night = {night}` градусов.",
        steps=["Выведи `Weather in ` и город.",
               "Выведи `Day: `, дневную температуру и ` C`.",
               "Выведи `Night: `, ночную температуру и ` C`.",
               "Выведи `Difference: `, на сколько днём теплее, чем ночью, и ` C`. Каждую строку печатай через f-строку.",
               "Например, для Omsk, 10 и 4 градусов программа выводит `Weather in Omsk`, `Day: 10 C`, `Night: 4 C`, "
               "`Difference: 6 C`."],
        hint="Разницу посчитай прямо внутри фигурных скобок: `{{day - night}}`. "
             "Порядок важен: из дневной температуры вычитаем ночную.",
        solution='print(f"Weather in {city}")\nprint(f"Day: {day} C")\nprint(f"Night: {night} C")\n'
                 'print(f"Difference: {day - night} C")',
        wrong=[("вычитает в обратном порядке — разница выходит с минусом",
                'print(f"Weather in {city}")\nprint(f"Day: {day} C")\nprint(f"Night: {night} C")\n'
                'print(f"Difference: {night - day} C")'),
               ("забыта буква f в первой строке",
                'print("Weather in {city}")\nprint(f"Day: {day} C")\nprint(f"Night: {night} C")\n'
                'print(f"Difference: {day - night} C")')],
        must_use=FSTR,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fs-bill-split", title="Делим счёт в кафе",
        given=["bill", "friends"],
        variants=[{"bill": "2350", "friends": "4"}, {"bill": "1000", "friends": "3"}, {"bill": "4710", "friends": "6"}],
        hidden=[{"bill": "900", "friends": "3"}, {"bill": "1001", "friends": "2"}, {"bill": "777", "friends": "5"}],
        intro="Друзья поели в кафе на `bill = {bill}` руб. и делят счёт поровну на `friends = {friends}` человек. "
              "Каждый платит целое число рублей, а то, что не делится поровну, доплатит кто-то один.",
        steps=["Посчитай долю каждого — `bill`, делённый нацело на `friends`, — и сохрани в переменную `share`.",
               "Посчитай остаток от деления `bill` на `friends` и сохрани в переменную `rest`.",
               "С помощью f-строк выведи три строки: `Bill: <bill> rub, friends: <friends>`, "
               "`Each pays: <share> rub` и `Extra: <rest> rub`.",
               "Например, для счёта 1000 руб. на 3 человек программа выводит `Bill: 1000 rub, friends: 3`, "
               "`Each pays: 333 rub` и `Extra: 1 rub`."],
        hint="Деление нацело — `//`, остаток — `%`: `1000 // 3` даёт `333`, `1000 % 3` даёт `1`. "
             "Обычное деление `/` дало бы дробь `333.333...`.",
        solution='share = bill // friends\nrest = bill % friends\nprint(f"Bill: {bill} rub, friends: {friends}")\n'
                 'print(f"Each pays: {share} rub")\nprint(f"Extra: {rest} rub")',
        wrong=[("делит через / — доля получается дробной",
                'share = bill / friends\nrest = bill % friends\nprint(f"Bill: {bill} rub, friends: {friends}")\n'
                'print(f"Each pays: {share} rub")\nprint(f"Extra: {rest} rub")'),
               ("в остаток кладёт частное",
                'share = bill // friends\nrest = bill // friends\nprint(f"Bill: {bill} rub, friends: {friends}")\n'
                'print(f"Each pays: {share} rub")\nprint(f"Extra: {rest} rub")')],
        must_use=FSTR,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fs-price-tag", title="Ценник со скидкой",
        given=["brand", "model", "year", "price", "discount"],
        variants=[{"brand": '"Lumia"', "model": '"X5"', "year": "2024", "price": "18000", "discount": "15"},
                  {"brand": '"Nova"', "model": '"Air"', "year": "2023", "price": "9990", "discount": "10"},
                  {"brand": '"Orbit"', "model": '"Pro 2"', "year": "2025", "price": "42500", "discount": "20"}],
        hidden=[{"brand": '"Zet"', "model": '"Mini"', "year": "2020", "price": "1000", "discount": "50"},
                {"brand": '"Kite"', "model": '"S"', "year": "2022", "price": "3333", "discount": "3"},
                {"brand": '"Polar"', "model": '"One"', "year": "2021", "price": "500", "discount": "0"}],
        intro="Магазин электроники печатает ценники со скидкой. О телефоне известно: марка `brand = {brand}`, "
              "модель `model = {model}`, год выпуска `year = {year}`, цена `price = {price}` руб. и скидка "
              "`discount = {discount}` процентов. Копейки скидки отбрасываются.",
        steps=["Посчитай новую цену: из `price` вычти `price * discount // 100` — и сохрани её в переменную `new_price`.",
               "С помощью f-строк выведи первой строкой марку, пробел, модель и год в скобках, например `Zet Mini (2020)`.",
               "Затем выведи `Old price: <price> rub`, `Discount: <discount>%` и `New price: <new_price> rub`.",
               "Например, для цены 1000 и скидки 50 последние строки — `Old price: 1000 rub`, `Discount: 50%`, "
               "`New price: 500 rub`."],
        hint="Скидка в рублях — это `price * discount // 100`, а не `discount`: 15% от 18000 — это 2700 руб., а не 15. "
             "В одной f-строке может быть несколько фигурных скобок: `f\"{{brand}} {{model}}\"`.",
        solution='new_price = price - price * discount // 100\nprint(f"{brand} {model} ({year})")\n'
                 'print(f"Old price: {price} rub")\nprint(f"Discount: {discount}%")\nprint(f"New price: {new_price} rub")',
        wrong=[("вычитает проценты как рубли",
                'new_price = price - discount\nprint(f"{brand} {model} ({year})")\n'
                'print(f"Old price: {price} rub")\nprint(f"Discount: {discount}%")\nprint(f"New price: {new_price} rub")'),
               ("между маркой и моделью нет пробела",
                'new_price = price - price * discount // 100\nprint(f"{brand}{model} ({year})")\n'
                'print(f"Old price: {price} rub")\nprint(f"Discount: {discount}%")\nprint(f"New price: {new_price} rub")')],
        must_use=FSTR,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fs-course-progress", title="Прогресс по курсу",
        given=["done", "total"],
        variants=[{"done": "7", "total": "20"}, {"done": "3", "total": "12"}, {"done": "11", "total": "15"}],
        hidden=[{"done": "0", "total": "8"}, {"done": "10", "total": "10"}, {"done": "1", "total": "3"}],
        intro="Онлайн-курс показывает ученику его прогресс. Пройдено уроков: `done = {done}`, всего уроков в курсе: "
              "`total = {total}`. Нужно вывести карточку прогресса с полоской из символов.",
        steps=["Посчитай, сколько уроков осталось, и сохрани в переменную `left`.",
               "Посчитай процент пройденного: `done * 100 // total` — и сохрани в переменную `percent`.",
               "С помощью f-строк выведи `Lessons: <done> of <total>`, `Left: <left>` и `Progress: <percent>%`.",
               "Последней строкой выведи полоску в квадратных скобках: столько символов `#`, сколько уроков пройдено, "
               "и столько точек `.`, сколько осталось. Например, для 2 пройденных из 5 полоска — `[##...]`, "
               "а процент — `Progress: 40%`."],
        hint="Строку можно повторить умножением: `\"#\" * 3` даёт `###`. Такое выражение можно написать прямо в фигурных "
             "скобках, только кавычки внутри возьми одинарные: `f\"[{{'#' * done}}]\"`. Процент считай так: сначала "
             "умножь на 100, потом дели нацело — `done // total * 100` почти всегда даёт 0.",
        solution='left = total - done\npercent = done * 100 // total\nprint(f"Lessons: {done} of {total}")\n'
                 'print(f"Left: {left}")\nprint(f"Progress: {percent}%")\nprint(f"[{\'#\' * done}{\'.\' * left}]")',
        wrong=[("сначала делит нацело, потом умножает на 100 — процент обнуляется",
                'left = total - done\npercent = done // total * 100\nprint(f"Lessons: {done} of {total}")\n'
                'print(f"Left: {left}")\nprint(f"Progress: {percent}%")\nprint(f"[{\'#\' * done}{\'.\' * left}]")'),
               ("в полоске точек столько же, сколько всего уроков",
                'left = total - done\npercent = done * 100 // total\nprint(f"Lessons: {done} of {total}")\n'
                'print(f"Left: {left}")\nprint(f"Progress: {percent}%")\nprint(f"[{\'#\' * done}{\'.\' * total}]")')],
        must_use=FSTR,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fs-shop-receipt", title="Чек в магазине",
        given=["item", "price", "count", "cash"],
        variants=[{"item": '"Notebook"', "price": "65", "count": "4", "cash": "500"},
                  {"item": '"Pen"', "price": "35", "count": "7", "cash": "300"},
                  {"item": '"Juice"', "price": "119", "count": "3", "cash": "1000"}],
        hidden=[{"item": '"Apple"', "price": "20", "count": "5", "cash": "100"},
                {"item": '"Cake"', "price": "450", "count": "1", "cash": "2000"},
                {"item": '"Tea"', "price": "89", "count": "2", "cash": "200"}],
        intro="Касса печатает чек. Покупатель берёт товар `item = {item}` по цене `price = {price}` руб. "
              "в количестве `count = {count}` штук и даёт кассиру `cash = {cash}` руб.",
        steps=["Посчитай стоимость покупки (`price` умножить на `count`) и сохрани в `total`.",
               "Посчитай сдачу (`cash` минус `total`) и сохрани в `change`.",
               "С помощью f-строк выведи пять строк: `<item> x<count>`, `Price: <price> rub`, "
               "`Total: <total> rub`, `Cash: <cash> rub` и `Change: <change> rub`.",
               "Например, для 5 штук `\"Apple\"` по 20 руб. и 100 руб. от покупателя первая строка — `Apple x5`, "
               "а последняя — `Change: 0 rub`."],
        hint="В строке `Apple x5` между `x` и числом пробела нет: `f\"{{item}} x{{count}}\"`. "
             "Сдача — это деньги покупателя минус стоимость, а не наоборот.",
        solution='total = price * count\nchange = cash - total\nprint(f"{item} x{count}")\nprint(f"Price: {price} rub")\n'
                 'print(f"Total: {total} rub")\nprint(f"Cash: {cash} rub")\nprint(f"Change: {change} rub")',
        wrong=[("вычитает в обратном порядке — сдача выходит с минусом",
                'total = price * count\nchange = total - cash\nprint(f"{item} x{count}")\nprint(f"Price: {price} rub")\n'
                'print(f"Total: {total} rub")\nprint(f"Cash: {cash} rub")\nprint(f"Change: {change} rub")'),
               ("пишет умножение текстом вне фигурных скобок",
                'total = price * count\nchange = cash - total\nprint(f"{item} x{count}")\nprint(f"Price: {price} rub")\n'
                'print(f"Total: {price} * {count} rub")\nprint(f"Cash: {cash} rub")\nprint(f"Change: {change} rub")')],
        must_use=FSTR,
    ),
]
