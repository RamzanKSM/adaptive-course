"""PY_SELF_BASIC — «self и методы». Taught before: everything up to functions, classes, creating objects, __init__.
Here: methods that read and change the object's own attributes through self; each object keeps its own state;
calling a method with parentheses; one method calling another through self. Not yet: _private attributes and
@property (next topics), inheritance, tuples, dicts."""
from build import OutputTask

SKILL = "PY_SELF_BASIC"

NEED_CLASS = ("ClassDef", "Опиши объект в собственном классе через class.")
NEED_METHOD = ("re:def (?!__init__)\\w+\\(\\s*self",
               "Опиши действие методом класса — функцией внутри класса, у которой первый параметр self. "
               "Через self метод меняет данные именно этого объекта.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-self-rt-scooter-battery", title="Заряд самоката",
        given=["battery", "km1", "km2"],
        variants=[{"battery": "100", "km1": "8", "km2": "15"}, {"battery": "75", "km1": "12", "km2": "3"},
                  {"battery": "90", "km1": "5", "km2": "20"}],
        hidden=[{"battery": "100", "km1": "0", "km2": "50"}, {"battery": "60", "km1": "10", "km2": "10"},
                {"battery": "44", "km1": "1", "km2": "21"}],
        intro="Электросамокат тратит 2% заряда на каждый километр поездки. Утром заряд был `battery` процентов, "
              "потом ты проехал `km1` км, а позже ещё `km2` км. Самокат должен помнить свой заряд между поездками.",
        steps=["Создай класс `Scooter`. В `__init__(self, battery)` сохрани заряд в атрибут `self.battery`.",
               "Добавь метод `ride(self, km)`, который уменьшает `self.battery` на `km`, умноженное на 2.",
               "Создай объект `scooter = Scooter(battery)`. Вызови `scooter.ride(km1)` и выведи строку вида "
               "`Battery: 84%` — со значением из `scooter.battery`.",
               "Потом вызови `scooter.ride(km2)` и снова выведи строку того же вида."],
        hint="`self` — это тот самый самокат, у которого вызвали метод. Запись `self.battery -= km * 2` меняет атрибут "
             "объекта, и новое значение сохраняется до следующей поездки.",
        solution='class Scooter:\n    def __init__(self, battery):\n        self.battery = battery\n\n'
                 '    def ride(self, km):\n        self.battery -= km * 2\n\n\nscooter = Scooter(battery)\n'
                 'scooter.ride(km1)\nprint(f"Battery: {scooter.battery}%")\nscooter.ride(km2)\nprint(f"Battery: {scooter.battery}%")',
        wrong=[("присваивает вместо вычитания — в заряд записывается расход",
                'class Scooter:\n    def __init__(self, battery):\n        self.battery = battery\n\n'
                '    def ride(self, km):\n        self.battery = km * 2\n\n\nscooter = Scooter(battery)\n'
                'scooter.ride(km1)\nprint(f"Battery: {scooter.battery}%")\nscooter.ride(km2)\nprint(f"Battery: {scooter.battery}%")'),
               ("забыл умножить на 2 — тратит 1% на километр",
                'class Scooter:\n    def __init__(self, battery):\n        self.battery = battery\n\n'
                '    def ride(self, km):\n        self.battery -= km\n\n\nscooter = Scooter(battery)\n'
                'scooter.ride(km1)\nprint(f"Battery: {scooter.battery}%")\nscooter.ride(km2)\nprint(f"Battery: {scooter.battery}%")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_METHOD],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-self-rt-elevator", title="Лифт",
        given=["requests"],
        variants=[{"requests": "[5, 2, 2, 9]"}, {"requests": "[1, 7, 3]"}, {"requests": "[4, 4, 1, 6, 6]"}],
        hidden=[{"requests": "[]"}, {"requests": "[1, 1]"}, {"requests": "[12, 3, 12, 1, 8, 8, 2]"}],
        intro="Лифт стоит на первом этаже. Жильцы по очереди нажимают кнопки — в списке `requests` записано, на какой "
              "этаж просили поехать. Если лифт уже на нужном этаже, он никуда не едет. Лифт должен сам помнить, "
              "где он стоит и сколько раз ездил.",
        steps=["Создай класс `Elevator`. В `__init__(self)` задай `self.floor = 1` и счётчик поездок `self.trips = 0`.",
               "Добавь метод `go_to(self, floor)`. Если `floor` не равен текущему этажу `self.floor`, метод печатает "
               "строку вида `Floor 1 -> 5` (откуда и куда), потом записывает новый этаж в `self.floor` и увеличивает "
               "`self.trips` на 1. Если равен — ничего не делает.",
               "Создай объект `lift = Elevator()` и пройди циклом по `requests`, вызывая `lift.go_to(...)` для каждого этажа.",
               "В конце выведи строку вида `Now at floor 9, trips 3` — со значениями из атрибутов лифта."],
        hint="Порядок важен: сначала напечатай строку со старым этажом `self.floor`, и только потом запиши в `self.floor` "
             "новый. Через `self` метод помнит этаж между вызовами.",
        solution='class Elevator:\n    def __init__(self):\n        self.floor = 1\n        self.trips = 0\n\n'
                 '    def go_to(self, floor):\n        if floor != self.floor:\n            print(f"Floor {self.floor} -> {floor}")\n'
                 '            self.floor = floor\n            self.trips += 1\n\n\nlift = Elevator()\nfor floor in requests:\n'
                 '    lift.go_to(floor)\nprint(f"Now at floor {lift.floor}, trips {lift.trips}")',
        wrong=[("сначала меняет этаж, а потом печатает — в строке оба этажа одинаковые",
                'class Elevator:\n    def __init__(self):\n        self.floor = 1\n        self.trips = 0\n\n'
                '    def go_to(self, floor):\n        if floor != self.floor:\n            self.floor = floor\n'
                '            print(f"Floor {self.floor} -> {floor}")\n            self.trips += 1\n\n\nlift = Elevator()\n'
                'for floor in requests:\n    lift.go_to(floor)\nprint(f"Now at floor {lift.floor}, trips {lift.trips}")'),
               ("не проверяет текущий этаж — считает поездку, даже когда лифт никуда не едет",
                'class Elevator:\n    def __init__(self):\n        self.floor = 1\n        self.trips = 0\n\n'
                '    def go_to(self, floor):\n        print(f"Floor {self.floor} -> {floor}")\n'
                '        self.floor = floor\n        self.trips += 1\n\n\nlift = Elevator()\nfor floor in requests:\n'
                '    lift.go_to(floor)\nprint(f"Now at floor {lift.floor}, trips {lift.trips}")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_METHOD],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-self-rt-card-payments", title="Оплата картой",
        given=["balance", "purchases"],
        variants=[{"balance": "1000", "purchases": "[300, 900, 450]"},
                  {"balance": "500", "purchases": "[120, 80, 400, 300]"},
                  {"balance": "2000", "purchases": "[2500, 1999, 5]"}],
        hidden=[{"balance": "100", "purchases": "[100]"},
                {"balance": "50", "purchases": "[60, 70]"},
                {"balance": "0", "purchases": "[]"},
                {"balance": "700", "purchases": "[200, 200, 200, 101, 100]"}],
        intro="Банковская карта проводит покупки по очереди. Если денег на карте хватает, покупка проходит и сумма "
              "списывается, а если не хватает — покупку отклоняют. На карте `balance` рублей, в списке `purchases` — "
              "суммы покупок в том порядке, в каком их пытались оплатить.",
        steps=["Создай класс `Card`. В `__init__(self, balance)` сохрани баланс в `self.balance` и задай два счётчика: "
               "`self.paid = 0` и `self.declined = 0`.",
               "Добавь метод `can_pay(self, amount)`: он возвращает `True`, если `amount` не больше баланса, иначе `False`.",
               "Добавь метод `pay(self, amount)`. Проверку в нём не пиши заново — вызови свой же метод `self.can_pay(amount)`. "
               "Если можно, спиши сумму, увеличь `self.paid` на 1 и выведи строку вида `Paid 300, left 700`. "
               "Иначе увеличь `self.declined` на 1 и выведи строку вида `Declined 900`.",
               "Создай карту, пройди циклом по `purchases` и вызови `pay` для каждой суммы. В конце выведи строку вида "
               "`Payments: 2, declined: 1`."],
        hint="Внутри класса методы вызывают друг друга через `self`: `self.can_pay(amount)` — это метод того же объекта. "
             "Если денег ровно столько, сколько стоит покупка, — их хватает.",
        solution='class Card:\n    def __init__(self, balance):\n        self.balance = balance\n        self.paid = 0\n'
                 '        self.declined = 0\n\n    def can_pay(self, amount):\n        return amount <= self.balance\n\n'
                 '    def pay(self, amount):\n        if self.can_pay(amount):\n            self.balance -= amount\n'
                 '            self.paid += 1\n            print(f"Paid {amount}, left {self.balance}")\n        else:\n'
                 '            self.declined += 1\n            print(f"Declined {amount}")\n\n\ncard = Card(balance)\n'
                 'for amount in purchases:\n    card.pay(amount)\nprint(f"Payments: {card.paid}, declined: {card.declined}")',
        wrong=[("строгое сравнение — отклоняет покупку, когда денег ровно столько, сколько нужно",
                'class Card:\n    def __init__(self, balance):\n        self.balance = balance\n        self.paid = 0\n'
                '        self.declined = 0\n\n    def can_pay(self, amount):\n        return amount < self.balance\n\n'
                '    def pay(self, amount):\n        if self.can_pay(amount):\n            self.balance -= amount\n'
                '            self.paid += 1\n            print(f"Paid {amount}, left {self.balance}")\n        else:\n'
                '            self.declined += 1\n            print(f"Declined {amount}")\n\n\ncard = Card(balance)\n'
                'for amount in purchases:\n    card.pay(amount)\nprint(f"Payments: {card.paid}, declined: {card.declined}")'),
               ("проверяет по стартовому балансу, а не по текущему — пропускает покупки, на которые денег уже нет",
                'class Card:\n    def __init__(self, balance):\n        self.balance = balance\n        self.paid = 0\n'
                '        self.declined = 0\n\n    def can_pay(self, amount):\n        return amount <= balance\n\n'
                '    def pay(self, amount):\n        if self.can_pay(amount):\n            self.balance -= amount\n'
                '            self.paid += 1\n            print(f"Paid {amount}, left {self.balance}")\n        else:\n'
                '            self.declined += 1\n            print(f"Declined {amount}")\n\n\ncard = Card(balance)\n'
                'for amount in purchases:\n    card.pay(amount)\nprint(f"Payments: {card.paid}, declined: {card.declined}")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_METHOD,
                  ("re:self\\.can_pay\\(", "В методе pay вызови метод can_pay того же объекта через self.can_pay(amount) — "
                                          "так проверка написана в одном месте.")],
    ),
]
