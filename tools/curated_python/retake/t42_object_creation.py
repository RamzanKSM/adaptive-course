"""PY_OBJECT_CREATION — «Создание объектов». Taught before: everything up to functions, and classes (class, __init__,
self. attributes, a simple method). Here: calling the class to make objects; several independent objects from one
class; objects made in a loop and kept in a list. Not yet: inheritance, tuples, dicts, comprehensions."""
from build import OutputTask

SKILL = "PY_OBJECT_CREATION"

NEED_CLASS = ("ClassDef", "Опиши данные в собственном классе через class и создавай объекты по нему.")
NEED_INIT = ("re:def __init__\\(", "Передавай данные в объект через метод __init__ — он сам вызывается при создании объекта.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-obj-rt-two-buses", title="Пересадка между автобусами",
        given=["people1", "people2", "moved"],
        variants=[{"people1": "30", "people2": "12", "moved": "8"},
                  {"people1": "25", "people2": "25", "moved": "10"},
                  {"people1": "40", "people2": "5", "moved": "15"}],
        hidden=[{"people1": "10", "people2": "0", "moved": "10"},
                {"people1": "18", "people2": "33", "moved": "1"},
                {"people1": "50", "people2": "20", "moved": "0"}],
        intro="На конечной остановке стоят два автобуса: в автобусе `A` сидят `people1` пассажиров, в автобусе `B` — "
              "`people2`. Потом `moved` человек пересели из автобуса `A` в автобус `B`. Автобусы устроены одинаково, "
              "так что хватит одного класса и двух объектов.",
        steps=["Создай класс `Bus`. В `__init__(self, name, passengers)` сохрани название и число пассажиров в атрибуты "
               "`self.name` и `self.passengers`.",
               "Создай два разных объекта: `bus1 = Bus(\"A\", people1)` и `bus2 = Bus(\"B\", people2)`.",
               "Перенеси пассажиров: у `bus1` уменьши `passengers` на `moved`, а у `bus2` увеличь на `moved`.",
               "Выведи для каждого автобуса строку вида `Bus A: 22 passengers` — сначала для `bus1`, потом для `bus2`."],
        hint="Каждый объект хранит своё число пассажиров: `bus1.passengers` и `bus2.passengers` — разные атрибуты. "
             "Пересадка меняет оба автобуса: из одного люди выходят, в другой входят.",
        solution='class Bus:\n    def __init__(self, name, passengers):\n        self.name = name\n        self.passengers = passengers\n\n\n'
                 'bus1 = Bus("A", people1)\nbus2 = Bus("B", people2)\nbus1.passengers -= moved\nbus2.passengers += moved\n'
                 'print(f"Bus {bus1.name}: {bus1.passengers} passengers")\nprint(f"Bus {bus2.name}: {bus2.passengers} passengers")',
        wrong=[("забыл добавить пассажиров во второй автобус — люди пропали по дороге",
                'class Bus:\n    def __init__(self, name, passengers):\n        self.name = name\n        self.passengers = passengers\n\n\n'
                'bus1 = Bus("A", people1)\nbus2 = Bus("B", people2)\nbus1.passengers -= moved\n'
                'print(f"Bus {bus1.name}: {bus1.passengers} passengers")\nprint(f"Bus {bus2.name}: {bus2.passengers} passengers")'),
               ("перепутал автобусы — пассажиры пересаживаются из B в A",
                'class Bus:\n    def __init__(self, name, passengers):\n        self.name = name\n        self.passengers = passengers\n\n\n'
                'bus1 = Bus("A", people1)\nbus2 = Bus("B", people2)\nbus2.passengers -= moved\nbus1.passengers += moved\n'
                'print(f"Bus {bus1.name}: {bus1.passengers} passengers")\nprint(f"Bus {bus2.name}: {bus2.passengers} passengers")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-obj-rt-shop-receipt", title="Чек из магазина",
        given=["items", "prices"],
        variants=[{"items": '["milk", "bread", "cheese"]', "prices": "[89, 45, 320]"},
                  {"items": '["tea", "honey"]', "prices": "[150, 410]"},
                  {"items": '["apples", "rice", "eggs", "butter"]', "prices": "[120, 95, 110, 230]"}],
        hidden=[{"items": '["water"]', "prices": "[40]"},
                {"items": '["pasta", "salt", "sugar"]', "prices": "[70, 25, 85]"},
                {"items": '["juice", "nuts", "cocoa", "jam", "oats"]', "prices": "[130, 260, 300, 180, 75]"}],
        intro="Касса печатает чек: каждую покупку с номером и ценой, а внизу — итог. Названия покупок записаны "
              "в список `items`, а их цены в рублях — в список `prices` на тех же местах.",
        steps=["Создай класс `Item`. В `__init__(self, name, price)` сохрани название и цену в атрибуты "
               "`self.name` и `self.price`.",
               "Создай пустой список `receipt`. Пройди циклом по позициям `range(len(items))` и для каждой позиции "
               "добавь в `receipt` объект `Item` с названием и ценой с этой позиции.",
               "Вторым циклом пройди по списку `receipt` и выведи каждую покупку строкой вида `1. milk - 89 rub`: "
               "номер (с 1), точка, пробел, название, пробел, дефис, пробел, цена и `rub`. "
               "Попутно сложи цены всех покупок.",
               "В конце выведи строку вида `Total: 454 rub`."],
        hint="Номер покупки держи в отдельной переменной: перед вторым циклом она равна 1, а после каждой строки "
             "увеличивается на 1. Сумму копи так же: перед циклом `total = 0`, а в цикле `total += item.price`.",
        solution='class Item:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\n\n'
                 'receipt = []\nfor i in range(len(items)):\n    receipt.append(Item(items[i], prices[i]))\n\n'
                 'number = 1\ntotal = 0\nfor item in receipt:\n    print(f"{number}. {item.name} - {item.price} rub")\n'
                 '    total += item.price\n    number += 1\nprint(f"Total: {total} rub")',
        wrong=[("в итог записывает цену последней покупки вместо суммы",
                'class Item:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\n\n'
                'receipt = []\nfor i in range(len(items)):\n    receipt.append(Item(items[i], prices[i]))\n\n'
                'number = 1\ntotal = 0\nfor item in receipt:\n    print(f"{number}. {item.name} - {item.price} rub")\n'
                '    total = item.price\n    number += 1\nprint(f"Total: {total} rub")'),
               ("нумерует покупки с нуля",
                'class Item:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\n\n'
                'receipt = []\nfor i in range(len(items)):\n    receipt.append(Item(items[i], prices[i]))\n\n'
                'number = 0\ntotal = 0\nfor item in receipt:\n    print(f"{number}. {item.name} - {item.price} rub")\n'
                '    total += item.price\n    number += 1\nprint(f"Total: {total} rub")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-obj-rt-library-fines", title="Просроченные книги",
        given=["titles", "days"],
        variants=[{"titles": '["Mumu", "Dune", "Emma", "Ivanhoe"]', "days": "[10, 19, 14, 30]"},
                  {"titles": '["Matilda", "Heidi", "Peter Pan"]', "days": "[15, 3, 21]"},
                  {"titles": '["Dracula", "Bambi"]', "days": "[7, 16]"}],
        hidden=[{"titles": '["Pinocchio", "Lolita"]', "days": "[14, 2]"},
                {"titles": '["Oliver Twist"]', "days": "[15]"},
                {"titles": '["Frankenstein", "Rebecca", "Ulysses", "Beowulf", "Kim"]', "days": "[40, 14, 1, 18, 25]"}],
        intro="Книгу из школьной библиотеки можно держать 14 дней. За каждый день сверх этого начисляется штраф "
              "10 руб. В списке `titles` — книги, которые сейчас на руках, а в списке `days` на тех же местах — "
              "сколько дней каждая из них уже не в библиотеке.",
        steps=["Создай класс `Loan`. В `__init__(self, title, days)` сохрани название и число дней в атрибуты "
               "`self.title` и `self.days`.",
               "Создай список `loans`: пройди циклом по позициям `range(len(titles))` и для каждой позиции добавь "
               "объект `Loan` с названием и числом дней с этой позиции.",
               "Пройди по списку `loans`. Для каждой книги, которая на руках больше 14 дней, выведи строку вида "
               "`Dune: overdue 5, fine 50 rub` — после слова `overdue` число дней просрочки (дни минус 14), потом штраф за них. "
               "Попутно сложи все штрафы.",
               "В конце выведи строку вида `Total fine: 210 rub`. Если просроченных книг нет совсем, "
               "вместо неё выведи `No late books`."],
        hint="Ровно 14 дней — ещё не просрочка. Удобно перед циклом завести `total = 0` и прибавлять к нему штраф "
             "каждой просроченной книги, а после цикла проверить: если `total` так и остался 0, просроченных книг не было.",
        solution='class Loan:\n    def __init__(self, title, days):\n        self.title = title\n        self.days = days\n\n\n'
                 'loans = []\nfor i in range(len(titles)):\n    loans.append(Loan(titles[i], days[i]))\n\n'
                 'total = 0\nfor loan in loans:\n    if loan.days > 14:\n        late = loan.days - 14\n'
                 '        print(f"{loan.title}: overdue {late}, fine {late * 10} rub")\n        total += late * 10\n'
                 'if total > 0:\n    print(f"Total fine: {total} rub")\nelse:\n    print("No late books")',
        wrong=[("штрафует за все дни, а не только за дни просрочки",
                'class Loan:\n    def __init__(self, title, days):\n        self.title = title\n        self.days = days\n\n\n'
                'loans = []\nfor i in range(len(titles)):\n    loans.append(Loan(titles[i], days[i]))\n\n'
                'total = 0\nfor loan in loans:\n    if loan.days > 14:\n        late = loan.days\n'
                '        print(f"{loan.title}: overdue {late}, fine {late * 10} rub")\n        total += late * 10\n'
                'if total > 0:\n    print(f"Total fine: {total} rub")\nelse:\n    print("No late books")'),
               ("забыл случай без просрочек — печатает нулевой штраф",
                'class Loan:\n    def __init__(self, title, days):\n        self.title = title\n        self.days = days\n\n\n'
                'loans = []\nfor i in range(len(titles)):\n    loans.append(Loan(titles[i], days[i]))\n\n'
                'total = 0\nfor loan in loans:\n    if loan.days > 14:\n        late = loan.days - 14\n'
                '        print(f"{loan.title}: overdue {late}, fine {late * 10} rub")\n        total += late * 10\n'
                'print(f"Total fine: {total} rub")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
]
