"""PY_POLYMORPHISM_BASIC — «Полиморфизм». Taught before: everything up to classes, __init__, self and methods,
«private» attributes, @property, class attributes, inheritance, overriding methods. Here: objects of different child
classes in one list; one loop calls the same method on each and every object answers in its own way — no checks of
«who is who». Not yet: super() (next topic), duck typing without a common parent, tuples, dicts, comprehensions."""
from build import OutputTask

SKILL = "PY_POLYMORPHISM_BASIC"

NEED_CLASS = ("ClassDef", "Опиши объекты в собственных классах через class.")
NEED_LOOP = ("For", "Обойди все объекты одним циклом for по списку.")


def child_of(child: str, parent: str) -> tuple[str, str]:
    return (f"re:class\\s+{child}\\s*\\(\\s*{parent}\\s*\\)",
            f"Сделай класс `{child}` наследником `{parent}`: напиши `class {child}({parent}):`.")


def no_title_check(what: str, method: str) -> tuple[str, str]:
    return ("re:\\A(?![\\s\\S]*\\.title\\s*[!=]=)",
            f"Не проверяй через if, какой это {what}: просто вызови `{method}`. "
            f"Каждый объект сам знает, как ответить, — в этом и смысл полиморфизма.")


FARM = """\
class Animal:
    def __init__(self, name):
        self.name = name

    def sound(self):
        return "..."


class Dog(Animal):
    def sound(self):
        return "Woof"


class Cat(Animal):
    def sound(self):
        return "Meow"


class Duck(Animal):
    def sound(self):
        return "Quack"


animals = [Dog(dog_name), Cat(cat_name), Duck(duck_name)]
for animal in animals:
    print(f"{animal.name}: {animal.sound()}")
"""

PAYMENTS = """\
class Payment:
    title = "Payment"

    def fee(self, amount):
        return 0


class Cash(Payment):
    title = "Cash"


class Card(Payment):
    title = "Card"

    def fee(self, amount):
        return amount // 100


class Transfer(Payment):
    title = "Transfer"

    def fee(self, amount):
        result = amount * 2 // 100
        if result < 30:
            result = 30
        return result


payments = [Cash(), Card(), Transfer()]
for payment in payments:
    fee = payment.fee(amount)
    print(f"{payment.title}: fee {fee} rub, to pay {amount + fee} rub")
"""

HEROES = """\
class Hero:
    title = "Hero"

    def __init__(self, level):
        self.level = level

    def damage(self):
        return 0


class Warrior(Hero):
    title = "Warrior"

    def damage(self):
        return 10 * self.level


class Mage(Hero):
    title = "Mage"

    def damage(self):
        return 25 + 5 * self.level


class Archer(Hero):
    title = "Archer"

    def damage(self):
        return 15 * self.level


heroes = []
for kind in team:
    if kind == "warrior":
        heroes.append(Warrior(level))
    elif kind == "mage":
        heroes.append(Mage(level))
    elif kind == "archer":
        heroes.append(Archer(level))

total = 0
for hero in heroes:
    hit = hero.damage()
    print(f"{hero.title}: damage {hit}")
    total += hit
print(f"Team damage: {total}")
"""


GUESTS = """\
class Guest:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"I am {self.name}"


class EnglishGuest(Guest):
    def greet(self):
        return f"Hello, I am {self.name}"


class FrenchGuest(Guest):
    def greet(self):
        return f"Bonjour, je suis {self.name}"


class GermanGuest(Guest):
    def greet(self):
        return f"Hallo, ich bin {self.name}"


guests = [EnglishGuest(english_name), FrenchGuest(french_name), GermanGuest(german_name)]
for guest in guests:
    print(guest.greet())
"""

TARIFFS = """\
class Tariff:
    title = "Tariff"

    def cost(self, minutes):
        return 0


class PerMinute(Tariff):
    title = "PerMinute"

    def cost(self, minutes):
        return 2 * minutes


class Package(Tariff):
    title = "Package"

    def cost(self, minutes):
        if minutes > 200:
            return 300 + 3 * (minutes - 200)
        return 300


class Unlimited(Tariff):
    title = "Unlimited"

    def cost(self, minutes):
        return 600


tariffs = [PerMinute(), Package(), Unlimited()]
best = tariffs[0]
for tariff in tariffs:
    print(f"{tariff.title}: {tariff.cost(minutes)} rub")
    if tariff.cost(minutes) < best.cost(minutes):
        best = tariff
print(f"Best: {best.title}")
"""

PARKING = """\
class Vehicle:
    title = "Vehicle"

    def __init__(self, hours):
        self.hours = hours

    def fee(self):
        return 0


class Car(Vehicle):
    title = "Car"

    def fee(self):
        return 50 * self.hours


class Bike(Vehicle):
    title = "Bike"

    def fee(self):
        return 20 * (self.hours - 1)


class Truck(Vehicle):
    title = "Truck"

    def fee(self):
        if self.hours < 2:
            return 150 * 2
        return 150 * self.hours


vehicles = []
for record in parking:
    parts = record.split(":")
    hours = int(parts[1])
    if parts[0] == "car":
        vehicles.append(Car(hours))
    elif parts[0] == "bike":
        vehicles.append(Bike(hours))
    elif parts[0] == "truck":
        vehicles.append(Truck(hours))

total = 0
for vehicle in vehicles:
    fee = vehicle.fee()
    print(f"{vehicle.title}, {vehicle.hours} h: {fee} rub")
    total += fee
print(f"Total: {total} rub")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-poly-farm-voices", title="Голоса на ферме",
        given=["dog_name", "cat_name", "duck_name"],
        variants=[{"dog_name": '"Sharik"', "cat_name": '"Murka"', "duck_name": '"Kryakva"'},
                  {"dog_name": '"Polkan"', "cat_name": '"Vaska"', "duck_name": '"Feather"'},
                  {"dog_name": '"Druzhok"', "cat_name": '"Simba"', "duck_name": '"Cloud"'}],
        hidden=[{"dog_name": '"Bobik"', "cat_name": '"Ginger"', "duck_name": '"Belka"'},
                {"dog_name": '"Laika"', "cat_name": '"Tom"', "duck_name": '"Donald"'},
                {"dog_name": '"Alma"', "cat_name": '"Peach"', "duck_name": '"Drop"'}],
        intro="На детской ферме живут собака, кошка и утка. Экскурсовод по очереди подходит к каждому животному, "
              "и оно подаёт голос — каждое по-своему. Программа должна обойти всех животных одним циклом.",
        steps=["Создай класс `Animal`. В `__init__(self, name)` сохрани имя в `self.name`. Добавь метод `sound(self)`, "
               "который возвращает строку `...`.",
               "Создай три наследника `Animal` и переопредели в каждом метод `sound(self)`: `Dog` возвращает `Woof`, "
               "`Cat` — `Meow`, `Duck` — `Quack`.",
               "Создай список `animals = [Dog(dog_name), Cat(cat_name), Duck(duck_name)]`.",
               "Одним циклом `for` пройди по списку и для каждого животного выведи строку вида `Sharik: Woof`. "
               "Метод `sound()` в программе вызывай только в одном месте — внутри этого цикла."],
        hint="В цикле переменная по очереди указывает на собаку, кошку и утку, а строка `animal.sound()` одна и та же. "
             "Python сам смотрит, какого класса текущий объект, и вызывает его версию метода.",
        solution=FARM,
        wrong=[("опечатка в имени метода у утки — утка молчит: срабатывает метод родителя",
                FARM.replace("class Duck(Animal):\n    def sound(", "class Duck(Animal):\n    def saund(")),
               ("создаёт всех животных из класса Animal — все печатают ...",
                FARM.replace("[Dog(dog_name), Cat(cat_name), Duck(duck_name)]",
                             "[Animal(dog_name), Animal(cat_name), Animal(duck_name)]"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_LOOP, child_of("Dog", "Animal"), child_of("Cat", "Animal"), child_of("Duck", "Animal"),
                  ("re:\\A(?![\\s\\S]*\\.sound\\(\\)[\\s\\S]*\\.sound\\(\\))[\\s\\S]*\\.sound\\(\\)",
                   "Вызывай `sound()` только в одном месте — внутри цикла по списку `animals`. Каждое животное "
                   "само знает, какой звук издавать, поэтому одна строка кода подходит для всех.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-poly-payment-fee", title="Комиссия за оплату",
        given=["amount"],
        variants=[{"amount": "2500"}, {"amount": "900"}, {"amount": "4000"}],
        hidden=[{"amount": "1000"}, {"amount": "15000"}, {"amount": "99"}, {"amount": "1500"}],
        intro="Интернет-магазин предлагает оплатить заказ на `amount` рублей тремя способами: наличными курьеру, "
              "картой или банковским переводом. Комиссия у каждого способа своя, а показать покупателю все варианты "
              "нужно одинаково — одним циклом.",
        steps=["Создай класс `Payment` с атрибутом класса `title = \"Payment\"` и методом `fee(self, amount)`, "
               "который возвращает комиссию `0`.",
               "Создай класс `Cash` — наследник `Payment` — с `title = \"Cash\"`. Метод `fee` в нём не пиши: наличными платят без комиссии.",
               "Создай класс `Card` — наследник `Payment` — с `title = \"Card\"` и переопредели `fee`: комиссия 1% — `amount // 100`.",
               "Создай класс `Transfer` — наследник `Payment` — с `title = \"Transfer\"` и переопредели `fee`: комиссия 2% — "
               "`amount * 2 // 100`, но не меньше 30 руб.",
               "Создай список `payments = [Cash(), Card(), Transfer()]`. Одним циклом по нему выведи для каждого "
               "способа строку вида `Card: fee 25 rub, to pay 2525 rub` Внутри цикла не проверяй, "
               "какой это способ, — просто вызывай `fee(amount)`."],
        hint="У `Cash` нет своего `fee`, поэтому для него сработает версия из `Payment`, а у `Card` и `Transfer` — "
             "их собственные. Чтобы не вызывать метод дважды, сохрани комиссию в переменную и используй её и для "
             "комиссии, и для суммы к оплате.",
        solution=PAYMENTS,
        wrong=[("проверяет способ оплаты через if и берёт комиссию только у карты — перевод получается бесплатным",
                PAYMENTS.replace("    fee = payment.fee(amount)\n",
                                 "    if payment.title == \"Card\":\n        fee = payment.fee(amount)\n"
                                 "    else:\n        fee = 0\n")),
               ("забыл про минимальную комиссию перевода — на маленьких суммах она меньше 30 руб.",
                PAYMENTS.replace("        if result < 30:\n            result = 30\n", ""))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_LOOP, child_of("Cash", "Payment"), child_of("Card", "Payment"),
                  child_of("Transfer", "Payment"), no_title_check("способ оплаты", "fee(amount)")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-poly-hero-squad", title="Отряд героев",
        given=["team", "level"],
        variants=[{"team": '["warrior", "mage", "archer"]', "level": "2"},
                  {"team": '["mage", "mage", "warrior"]', "level": "1"},
                  {"team": '["archer", "warrior", "archer", "mage"]', "level": "3"}],
        hidden=[{"team": '["warrior"]', "level": "5"},
                {"team": '["archer", "mage"]', "level": "1"},
                {"team": '["mage", "warrior", "archer", "warrior", "mage"]', "level": "4"}],
        intro="Ты собираешь отряд для похода. В списке `team` записано, кто идёт в отряд, а `level` — уровень "
              "всех героев. Каждый тип героя наносит урон по-своему, а программа должна посчитать урон всего отряда.",
        steps=["Создай класс `Hero` с атрибутом класса `title = \"Hero\"`. В `__init__(self, level)` сохрани уровень "
               "в `self.level`. Добавь метод `damage(self)`, который возвращает `0`.",
               "Создай трёх наследников `Hero`, в каждом задай свой `title` и переопредели `damage(self)`: "
               "`Warrior` — `\"Warrior\"`, урон — уровень, умноженный на 10; `Mage` — `\"Mage\"`, урон — 25 плюс уровень, "
               "умноженный на 5; `Archer` — `\"Archer\"`, урон — уровень, умноженный на 15.",
               "Собери список `heroes`: пройди по `team` и для строки `\"warrior\"` добавь `Warrior(level)`, "
               "для `\"mage\"` — `Mage(level)`, для `\"archer\"` — `Archer(level)`.",
               "Вторым циклом пройди по `heroes`: для каждого героя выведи строку вида `Warrior: damage 20` и прибавь его "
               "урон к общему. В этом цикле не проверяй, кто есть кто, — просто вызывай `damage()`.",
               "Последней строкой выведи общий урон в виде `Team damage: 85`."],
        hint="Выбирать класс через `if` нужно только один раз — когда создаёшь героев из строк. Дальше каждый объект "
             "сам знает свой урон и своё название, поэтому во втором цикле хватит `hero.damage()` и `hero.title`.",
        solution=HEROES,
        wrong=[("опечатка в имени метода у лучника — его урон считается как у Hero, то есть 0",
                HEROES.replace("class Archer(Hero):\n    title = \"Archer\"\n\n    def damage(",
                               "class Archer(Hero):\n    title = \"Archer\"\n\n    def damge(")),
               ("обнуляет общий урон внутри цикла — в итоге остаётся урон только последнего героя",
                HEROES.replace("total = 0\nfor hero in heroes:\n    hit = hero.damage()\n",
                               "for hero in heroes:\n    total = 0\n    hit = hero.damage()\n"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_LOOP, child_of("Warrior", "Hero"), child_of("Mage", "Hero"),
                  child_of("Archer", "Hero"), no_title_check("герой", "damage()")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-poly-foreign-guests", title="Гости из разных стран",
        given=["english_name", "french_name", "german_name"],
        variants=[{"english_name": '"John"', "french_name": '"Pierre"', "german_name": '"Hans"'},
                  {"english_name": '"Emma"', "french_name": '"Claire"', "german_name": '"Greta"'},
                  {"english_name": '"Oliver"', "french_name": '"Louis"', "german_name": '"Klaus"'}],
        hidden=[{"english_name": '"Lucy"', "french_name": '"Marie"', "german_name": '"Otto"'},
                {"english_name": '"Jack"', "french_name": '"Julien"', "german_name": '"Anna"'},
                {"english_name": '"Kate"', "french_name": '"Paul"', "german_name": '"Lena"'}],
        intro="В школу на фестиваль приехали гости из Англии, Франции и Германии. Ведущий по очереди даёт каждому "
              "микрофон, и каждый гость представляется на своём языке. Программа должна обойти всех гостей одним циклом.",
        steps=["Создай класс `Guest`. В `__init__(self, name)` сохрани имя в `self.name`. Добавь метод `greet(self)`, "
               "который возвращает строку вида `I am John`.",
               "Создай три наследника `Guest` и переопредели в каждом `greet(self)`: `EnglishGuest` возвращает строку "
               "вида `Hello, I am John`, `FrenchGuest` — `Bonjour, je suis Pierre`, `GermanGuest` — `Hallo, ich bin Hans`. "
               "Имя в каждой строке бери из `self.name`.",
               "Создай список `guests = [EnglishGuest(english_name), FrenchGuest(french_name), GermanGuest(german_name)]`.",
               "Одним циклом `for` пройди по списку и выведи результат `greet()` каждого гостя. Метод `greet()` "
               "в программе вызывай только в одном месте — внутри этого цикла."],
        hint="Переопределённый метод тоже может пользоваться атрибутами объекта: `self.name` у каждого гостя своё. "
             "А в цикле строка `guest.greet()` одна, но Python для каждого гостя вызывает версию его класса.",
        solution=GUESTS,
        wrong=[("опечатка в имени метода у немецкого гостя — он представляется по-нейтральному, методом родителя",
                GUESTS.replace("class GermanGuest(Guest):\n    def greet(", "class GermanGuest(Guest):\n    def great(")),
               ("создаёт всех гостей из класса Guest — никто не здоровается на своём языке",
                GUESTS.replace("[EnglishGuest(english_name), FrenchGuest(french_name), GermanGuest(german_name)]",
                               "[Guest(english_name), Guest(french_name), Guest(german_name)]"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_LOOP, child_of("EnglishGuest", "Guest"), child_of("FrenchGuest", "Guest"),
                  child_of("GermanGuest", "Guest"),
                  ("re:\\A(?![\\s\\S]*\\.greet\\(\\)[\\s\\S]*\\.greet\\(\\))[\\s\\S]*\\.greet\\(\\)",
                   "Вызывай `greet()` только в одном месте — внутри цикла по списку `guests`. Каждый гость "
                   "сам знает, как поздороваться, поэтому одна строка кода подходит для всех.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-poly-phone-tariffs", title="Выбор тарифа",
        given=["minutes"],
        variants=[{"minutes": "250"}, {"minutes": "120"}, {"minutes": "400"}],
        hidden=[{"minutes": "0"}, {"minutes": "200"}, {"minutes": "150"}, {"minutes": "1000"}],
        intro="Ты помогаешь бабушке выбрать тариф мобильной связи. Она говорит по телефону `minutes` минут в месяц. "
              "У оператора три тарифа, и каждый считает стоимость по-своему. Нужно показать цену каждого тарифа "
              "и выбрать самый дешёвый.",
        steps=["Создай класс `Tariff` с атрибутом класса `title = \"Tariff\"` и методом `cost(self, minutes)`, "
               "который возвращает `0`.",
               "Создай наследника `PerMinute` с `title = \"PerMinute\"`: `cost` возвращает 2 руб. за каждую минуту.",
               "Создай наследника `Package` с `title = \"Package\"`: 300 руб. в месяц, в них входит 200 минут, "
               "а каждая минута сверх 200 стоит 3 руб.",
               "Создай наследника `Unlimited` с `title = \"Unlimited\"`: `cost` всегда возвращает 600.",
               "Создай список `tariffs = [PerMinute(), Package(), Unlimited()]`. Одним циклом по нему выведи для каждого "
               "тарифа строку вида `Package: 450 rub` и попутно найди самый дешёвый тариф. Если цены равны, "
               "остаётся тот, что раньше в списке. Последней строкой выведи `Best: …` с его названием. "
               "Не проверяй в цикле, какой это тариф, — просто вызывай `cost(minutes)`."],
        hint="Самый дешёвый ищи так же, как минимум в списке чисел, только храни весь объект: начни с "
             "`best = tariffs[0]` и заменяй его, если `tariff.cost(minutes) < best.cost(minutes)`. "
             "Строгое сравнение и оставляет при равенстве более ранний тариф.",
        solution=TARIFFS,
        wrong=[("в пакете считает по 3 руб. за все минуты, а не только за минуты сверх 200",
                TARIFFS.replace("return 300 + 3 * (minutes - 200)", "return 300 + 3 * minutes")),
               ("ищет самый дорогой тариф вместо самого дешёвого",
                TARIFFS.replace("if tariff.cost(minutes) < best.cost(minutes):", "if tariff.cost(minutes) > best.cost(minutes):")),
               ("при равной цене выбирает более поздний тариф",
                TARIFFS.replace("if tariff.cost(minutes) < best.cost(minutes):", "if tariff.cost(minutes) <= best.cost(minutes):"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_LOOP, child_of("PerMinute", "Tariff"), child_of("Package", "Tariff"),
                  child_of("Unlimited", "Tariff"), no_title_check("тариф", "cost(minutes)")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-poly-parking-fees", title="Оплата парковки",
        given=["parking"],
        variants=[{"parking": '["car:3", "bike:4", "truck:5"]'},
                  {"parking": '["truck:1", "car:2", "car:1"]'},
                  {"parking": '["bike:1", "truck:2", "bike:6", "car:4"]'}],
        hidden=[{"parking": '["car:10"]'},
                {"parking": '["bike:2", "truck:3"]'},
                {"parking": '["truck:1", "bike:1", "truck:2", "car:1"]'}],
        intro="На платной парковке стоят машины, мотоциклы и грузовики, и для каждого вида транспорта свои правила "
              "оплаты. В списке `parking` по порядку записано, кто стоял: вид (`car`, `bike` или `truck`), двоеточие "
              "и число часов. Нужно выписать каждому счёт и посчитать выручку парковки.",
        steps=["Создай класс `Vehicle` с атрибутом класса `title = \"Vehicle\"`. В `__init__(self, hours)` сохрани часы "
               "в `self.hours`. Добавь метод `fee(self)`, который возвращает `0`.",
               "Создай трёх наследников `Vehicle`, в каждом задай свой `title` и переопредели `fee(self)`: "
               "`Car` — `\"Car\"`, 50 руб. за каждый час; `Bike` — `\"Bike\"`, 20 руб. за час, но первый час бесплатный; "
               "`Truck` — `\"Truck\"`, 150 руб. за час, но платят минимум за 2 часа.",
               "Собери список `vehicles`: раздели каждую запись из `parking` по двоеточию, преврати часы в `int` "
               "и создай объект нужного класса.",
               "Вторым циклом пройди по `vehicles`: для каждого выведи строку вида `Car, 3 h: 150 rub` и прибавь плату "
               "к выручке. В этом цикле не проверяй, кто есть кто, — просто вызывай `fee()`.",
               "Последней строкой выведи выручку в виде `Total: 960 rub`."],
        hint="Проверять вид транспорта через `if` нужно только один раз — когда создаёшь объекты из строк. "
             "Особые правила живут внутри методов `fee`: у мотоцикла оплачиваются часы без первого (`self.hours - 1`), "
             "а у грузовика, если он стоял меньше 2 часов, платят как за 2.",
        solution=PARKING,
        wrong=[("забыл про бесплатный первый час у мотоцикла",
                PARKING.replace("return 20 * (self.hours - 1)", "return 20 * self.hours")),
               ("не учитывает минимальную оплату грузовика — за 1 час берёт как за 1",
                PARKING.replace("        if self.hours < 2:\n            return 150 * 2\n", "")),
               ("опечатка в имени метода у машины — её плата считается как у Vehicle, то есть 0",
                PARKING.replace("class Car(Vehicle):\n    title = \"Car\"\n\n    def fee(",
                                "class Car(Vehicle):\n    title = \"Car\"\n\n    def fees("))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_LOOP, child_of("Car", "Vehicle"), child_of("Bike", "Vehicle"),
                  child_of("Truck", "Vehicle"), no_title_check("транспорт", "fee()")],
    ),
]
