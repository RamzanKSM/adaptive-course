"""PY_DUCK_TYPING — «Утиная типизация». Taught before: everything up to classes, __init__, self and methods,
«private» attributes, @property, class attributes, inheritance, overriding, polymorphism, super(). Here: unrelated
classes (no common parent) that have a method with the same name; a function works with any object that has this
method and never checks what the object is. Not yet: tuples, sets, dicts, comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_DUCK_TYPING"

NEED_CLASS = ("ClassDef", "Опиши предметы в собственных классах через class.")
NO_PARENT = ("re:\\A(?![\\s\\S]*class\\s+\\w+\\s*\\(\\s*\\w)",
             "Здесь классы не связаны наследованием: не указывай родителя в скобках после имени класса. "
             "Функции достаточно, что у каждого объекта есть метод с нужным именем.")


def need_function(name: str, params: str) -> tuple[str, str]:
    return (f"re:(?m)^def\\s+{name}\\s*\\(",
            f"Напиши отдельную функцию `{name}({params})` — не внутри класса, а после классов. "
            f"Она должна работать с любым объектом, у которого есть нужный метод.")


BACKPACK = """\
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def describe(self):
        return f"книга «{self.title}», {self.pages} стр."


class Phone:
    def __init__(self, model, battery):
        self.model = model
        self.battery = battery

    def describe(self):
        return f"телефон {self.model}, заряд {self.battery}%"


def show(item):
    print(f"В рюкзаке: {item.describe()}")


book = Book(title, pages)
phone = Phone(model, battery)
show(book)
show(phone)
"""

HIKE = """\
class Tent:
    name = "Палатка"

    def __init__(self, grams):
        self.grams = grams

    def weight(self):
        return self.grams


class Food:
    name = "Еда"

    def __init__(self, portions):
        self.portions = portions

    def weight(self):
        return self.portions * 300


class Water:
    name = "Вода"

    def __init__(self, liters):
        self.liters = liters

    def weight(self):
        return self.liters * 1000


def pack(items, limit):
    total = 0
    for item in items:
        print(f"{item.name}: {item.weight()} г")
        total += item.weight()
    print(f"Итого: {total} г")
    if total > limit:
        print("Слишком тяжело")
    else:
        print("Можно идти в поход")


pack([Tent(tent), Food(portions), Water(liters)], limit)
"""

CHECKOUT = """\
class Card:
    way = "картой"

    def __init__(self, balance):
        self.balance = balance

    def pay(self, price):
        if price <= self.balance:
            self.balance -= price
            return True
        return False


class Coupon:
    way = "купоном"

    def __init__(self, value):
        self.value = value

    def pay(self, price):
        if price <= self.value:
            self.value = 0
            return True
        return False


def pay_for(price, payers):
    for payer in payers:
        if payer.pay(price):
            print(f"{price} руб.: оплачено {payer.way}")
            return
    print(f"{price} руб.: не хватает денег")


card = Card(balance)
coupon = Coupon(coupon_value)
for price in prices:
    pay_for(price, [coupon, card])
print(f"На карте осталось: {card.balance} руб.")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-duck-backpack", title="Что лежит в рюкзаке",
        given=["title", "pages", "model", "battery"],
        variants=[{"title": '"Дюна"', "pages": "412", "model": '"Nokia"', "battery": "80"},
                  {"title": '"Гарри Поттер"', "pages": "320", "model": '"Pixel"', "battery": "15"},
                  {"title": '"Маленький принц"', "pages": "96", "model": '"iPhone"', "battery": "100"}],
        hidden=[{"title": '"Онегин"', "pages": "240", "model": '"Galaxy"', "battery": "5"},
                {"title": '"Хоббит"', "pages": "310", "model": '"Redmi"', "battery": "57"},
                {"title": '"Муму"', "pages": "48", "model": '"Xperia"', "battery": "99"}],
        intro="Ты собираешь рюкзак, и программа перечисляет, что в нём лежит. Книга и телефон — совсем разные "
              "классы без общего родителя, но оба умеют описать себя методом `describe()`. "
              "Функции, которая выводит содержимое рюкзака, этого достаточно.",
        steps=["Создай класс `Book`. В `__init__(self, title, pages)` сохрани название и число страниц. Добавь метод "
               "`describe(self)`, который возвращает строку вида `книга «Дюна», 412 стр.`",
               "Создай класс `Phone` — отдельный, без родителя. В `__init__(self, model, battery)` сохрани модель "
               "и заряд в процентах. Добавь метод `describe(self)`, который возвращает строку вида "
               "`телефон Nokia, заряд 80%`.",
               "Напиши функцию `show(item)`, которая печатает строку вида `В рюкзаке: книга «Дюна», 412 стр.` — "
               "после двоеточия и пробела идёт результат `item.describe()`. Проверять, книга это или телефон, не нужно.",
               "Создай `book = Book(title, pages)` и `phone = Phone(model, battery)` и вызови `show` сначала "
               "для книги, потом для телефона."],
        hint="Функции `show` всё равно, какого класса предмет: она просто вызывает у него `describe()`. "
             "Главное, чтобы `describe` **возвращал** строку через `return`, а не печатал её сам.",
        solution=BACKPACK,
        wrong=[("функция show берёт глобальную переменную book вместо параметра item — книга выводится дважды",
                BACKPACK.replace('    print(f"В рюкзаке: {item.describe()}")', '    print(f"В рюкзаке: {book.describe()}")')),
               ("describe печатает описание вместо return — show выводит None",
                BACKPACK.replace('        return f"книга «{self.title}», {self.pages} стр."',
                                 '        print(f"книга «{self.title}», {self.pages} стр.")')
                        .replace('        return f"телефон {self.model}, заряд {self.battery}%"',
                                 '        print(f"телефон {self.model}, заряд {self.battery}%")'))],
        constructs=["class", "function"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("show", "item")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-duck-hiking-gear", title="Сборы в поход",
        given=["tent", "portions", "liters", "limit"],
        variants=[{"tent": "2500", "portions": "4", "liters": "2", "limit": "6000"},
                  {"tent": "3000", "portions": "6", "liters": "1", "limit": "5000"},
                  {"tent": "1800", "portions": "2", "liters": "3", "limit": "5400"}],
        hidden=[{"tent": "2000", "portions": "1", "liters": "1", "limit": "3300"},
                {"tent": "4000", "portions": "10", "liters": "3", "limit": "8000"},
                {"tent": "1500", "portions": "0", "liters": "0", "limit": "2000"}],
        intro="Перед походом нужно взвесить снаряжение: палатка весит `tent` граммов, еды взято `portions` порций, "
              "воды — `liters` литров. Унести можно не больше `limit` граммов. Палатка, еда и вода — разные классы, "
              "и вес у каждого считается по-своему, но у всех есть метод `weight()`.",
        steps=["Создай три отдельных класса без общего родителя. У каждого — атрибут класса `name` "
               "и метод `weight(self)`, который возвращает вес в граммах.",
               "`Tent`: `name = \"Палатка\"`, в `__init__(self, grams)` сохраняет вес, `weight` возвращает его.",
               "`Food`: `name = \"Еда\"`, в `__init__(self, portions)` сохраняет число порций, `weight` возвращает "
               "по 300 граммов на порцию. `Water`: `name = \"Вода\"`, в `__init__(self, liters)` сохраняет литры, "
               "`weight` возвращает по 1000 граммов на литр.",
               "Напиши функцию `pack(items, limit)`. Для каждого предмета из списка `items` она печатает строку "
               "вида `Палатка: 2500 г`, потом строку вида `Итого: 5700 г` с общим весом. Если общий вес больше `limit`, "
               "последней строкой печатает `Слишком тяжело`, иначе — `Можно идти в поход`.",
               "Вызови `pack([Tent(tent), Food(portions), Water(liters)], limit)`."],
        hint="Внутри `pack` не нужно выяснять, палатка перед тобой или вода: у любого предмета есть `name` и `weight()`. "
             "Общий вес копи в переменной, которую создаёшь до цикла. И обрати внимание: ровно `limit` граммов "
             "унести ещё можно.",
        solution=HIKE,
        wrong=[("обнуляет общий вес внутри цикла — в итог попадает только последний предмет",
                HIKE.replace("    total = 0\n    for item in items:\n",
                             "    for item in items:\n        total = 0\n")),
               ("считает слишком тяжёлым даже вес, равный лимиту",
                HIKE.replace("    if total > limit:", "    if total >= limit:"))],
        constructs=["class", "function", "for"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("pack", "items, limit")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-duck-card-coupon", title="Карта или купон",
        given=["balance", "coupon_value", "prices"],
        variants=[{"balance": "1000", "coupon_value": "500", "prices": "[300, 400, 350]"},
                  {"balance": "500", "coupon_value": "1000", "prices": "[1200, 700, 300]"},
                  {"balance": "2000", "coupon_value": "300", "prices": "[250, 250, 1800, 100]"}],
        hidden=[{"balance": "100", "coupon_value": "50", "prices": "[80, 200]"},
                {"balance": "0", "coupon_value": "0", "prices": "[10]"},
                {"balance": "5000", "coupon_value": "700", "prices": "[700, 700, 700]"}],
        intro="На кассе покупатель может заплатить картой или подарочным купоном. Карта и купон — совсем разные вещи, "
              "но у обоих есть метод `pay`, и кассе этого достаточно: ей неважно, что ей дали, лишь бы оно умело платить. "
              "На карте `balance` рублей, купон на `coupon_value` рублей, а цены покупок — в списке `prices`.",
        steps=["Создай класс `Card` с атрибутом класса `way = \"картой\"`. В `__init__(self, balance)` сохрани баланс. "
               "Метод `pay(self, price)`: если цена не больше баланса, списывает её с баланса и возвращает `True`, "
               "иначе возвращает `False`.",
               "Создай отдельный класс `Coupon` (не наследник `Card`) с атрибутом класса `way = \"купоном\"`. "
               "В `__init__(self, value)` сохрани номинал купона. Метод `pay(self, price)`: если цена не больше номинала, "
               "купон сгорает целиком — номинал становится 0 — и метод возвращает `True`, иначе возвращает `False`.",
               "Напиши функцию `pay_for(price, payers)`. Она по очереди пробует заплатить `price` каждым способом "
               "из списка `payers`, вызывая у него `pay(price)`. При первой удачной оплате печатает строку вида "
               "`300 руб.: оплачено купоном` и сразу завершает работу через `return`. Если не подошёл ни один способ, "
               "печатает строку вида `1200 руб.: не хватает денег`.",
               "Создай `card = Card(balance)` и `coupon = Coupon(coupon_value)`. Для каждой цены из `prices` вызови "
               "`pay_for(price, [coupon, card])` — сначала пробуем купон, потом карту.",
               "Последней строкой выведи остаток на карте в виде `На карте осталось: 250 руб.`"],
        hint="Функции `pay_for` не нужно знать, карта перед ней или купон: она вызывает `payer.pay(price)` и смотрит, "
             "вернулось `True` или `False`. Это и есть утиная типизация: если объект умеет платить, им можно платить.",
        solution=CHECKOUT,
        wrong=[("купон не сгорает после оплаты — им платят снова и снова",
                CHECKOUT.replace("            self.value = 0\n", "")),
               ("после удачной оплаты не выходит из функции — покупку оплачивают и купоном, и картой",
                CHECKOUT.replace('            print(f"{price} руб.: оплачено {payer.way}")\n            return\n',
                                 '            print(f"{price} руб.: оплачено {payer.way}")\n'))],
        constructs=["class", "function", "for"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("pay_for", "price, payers")],
    ),
]
