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
        return f'book "{self.title}", {self.pages} pages'


class Phone:
    def __init__(self, model, battery):
        self.model = model
        self.battery = battery

    def describe(self):
        return f"phone {self.model}, battery {self.battery}%"


def show(item):
    print(f"In the backpack: {item.describe()}")


book = Book(title, pages)
phone = Phone(model, battery)
show(book)
show(phone)
"""

HIKE = """\
class Tent:
    name = "Tent"

    def __init__(self, grams):
        self.grams = grams

    def weight(self):
        return self.grams


class Food:
    name = "Food"

    def __init__(self, portions):
        self.portions = portions

    def weight(self):
        return self.portions * 300


class Water:
    name = "Water"

    def __init__(self, liters):
        self.liters = liters

    def weight(self):
        return self.liters * 1000


def pack(items, limit):
    total = 0
    for item in items:
        print(f"{item.name}: {item.weight()} g")
        total += item.weight()
    print(f"Total: {total} g")
    if total > limit:
        print("Too heavy")
    else:
        print("Ready for the hike")


pack([Tent(tent), Food(portions), Water(liters)], limit)
"""

CHECKOUT = """\
class Card:
    way = "by card"

    def __init__(self, balance):
        self.balance = balance

    def pay(self, price):
        if price <= self.balance:
            self.balance -= price
            return True
        return False


class Coupon:
    way = "by coupon"

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
            print(f"{price} rub: paid {payer.way}")
            return
    print(f"{price} rub: not enough money")


card = Card(balance)
coupon = Coupon(coupon_value)
for price in prices:
    pay_for(price, [coupon, card])
print(f"Left on card: {card.balance} rub")
"""

PAINT = """\
class Square:
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


def paint(shape, price):
    print(f"Area {shape.area()} m2, cost {shape.area() * price} rub")


floor = Square(side)
wall = Rectangle(width, height)
paint(floor, price)
paint(wall, price)
"""

COMMUTE = """\
class Walk:
    name = "Walk"

    def minutes(self, km):
        return km * 12


class Bike:
    name = "Bike"

    def __init__(self, speed):
        self.speed = speed

    def minutes(self, km):
        return km * 60 // self.speed


class Bus:
    name = "Bus"

    def __init__(self, wait):
        self.wait = wait

    def minutes(self, km):
        return self.wait + km * 2


def choose(options, km):
    best = options[0]
    for option in options:
        time = option.minutes(km)
        print(f"{option.name}: {time} min")
        if time < best.minutes(km):
            best = option
    print(f"Best: {best.name}")


choose([Walk(), Bike(speed), Bus(wait)], km)
"""

BATTLE = """\
class Knight:
    name = "Knight"

    def __init__(self, hp, armor):
        self.hp = hp
        self.armor = armor

    def take_hit(self, damage):
        if damage > self.armor:
            self.hp -= damage - self.armor
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0


class Ghost:
    name = "Ghost"

    def __init__(self, hp):
        self.hp = hp

    def take_hit(self, damage):
        self.hp -= damage // 2
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0


def attack(targets, damage):
    for target in targets:
        if target.is_alive():
            target.take_hit(damage)
            print(f"{target.name}: {target.hp} hp")
        else:
            print(f"{target.name} is out")


knight = Knight(knight_hp, armor)
ghost = Ghost(ghost_hp)
for damage in hits:
    attack([knight, ghost], damage)
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-duck-backpack", title="Что лежит в рюкзаке",
        given=["title", "pages", "model", "battery"],
        variants=[{"title": '"Dune"', "pages": "412", "model": '"Nokia"', "battery": "80"},
                  {"title": '"Harry Potter"', "pages": "320", "model": '"Pixel"', "battery": "15"},
                  {"title": '"The Little Prince"', "pages": "96", "model": '"iPhone"', "battery": "100"}],
        hidden=[{"title": '"Onegin"', "pages": "240", "model": '"Galaxy"', "battery": "5"},
                {"title": '"The Hobbit"', "pages": "310", "model": '"Redmi"', "battery": "57"},
                {"title": '"Mumu"', "pages": "48", "model": '"Xperia"', "battery": "99"}],
        intro="Ты собираешь рюкзак, и программа перечисляет, что в нём лежит. Книга и телефон — совсем разные "
              "классы без общего родителя, но оба умеют описать себя методом `describe()`. "
              "Функции, которая выводит содержимое рюкзака, этого достаточно.",
        steps=["Создай класс `Book`. В `__init__(self, title, pages)` сохрани название и число страниц. Добавь метод "
               "`describe(self)`, который возвращает строку вида `book \"Dune\", 412 pages`",
               "Создай класс `Phone` — отдельный, без родителя. В `__init__(self, model, battery)` сохрани модель "
               "и заряд в процентах. Добавь метод `describe(self)`, который возвращает строку вида "
               "`phone Nokia, battery 80%`.",
               "Напиши функцию `show(item)`, которая печатает строку вида `In the backpack: book \"Dune\", 412 pages` — "
               "после двоеточия и пробела идёт результат `item.describe()`. Проверять, книга это или телефон, не нужно.",
               "Создай `book = Book(title, pages)` и `phone = Phone(model, battery)` и вызови `show` сначала "
               "для книги, потом для телефона."],
        hint="Функции `show` всё равно, какого класса предмет: она просто вызывает у него `describe()`. "
             "Главное, чтобы `describe` **возвращал** строку через `return`, а не печатал её сам.",
        solution=BACKPACK,
        wrong=[("функция show берёт глобальную переменную book вместо параметра item — книга выводится дважды",
                BACKPACK.replace('    print(f"In the backpack: {item.describe()}")', '    print(f"In the backpack: {book.describe()}")')),
               ("describe печатает описание вместо return — show выводит None",
                BACKPACK.replace('        return f\'book "{self.title}", {self.pages} pages\'',
                                 '        print(f\'book "{self.title}", {self.pages} pages\')')
                        .replace('        return f"phone {self.model}, battery {self.battery}%"',
                                 '        print(f"phone {self.model}, battery {self.battery}%")'))],
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
               "`Tent`: `name = \"Tent\"`, в `__init__(self, grams)` сохраняет вес, `weight` возвращает его.",
               "`Food`: `name = \"Food\"`, в `__init__(self, portions)` сохраняет число порций, `weight` возвращает "
               "по 300 граммов на порцию. `Water`: `name = \"Water\"`, в `__init__(self, liters)` сохраняет литры, "
               "`weight` возвращает по 1000 граммов на литр.",
               "Напиши функцию `pack(items, limit)`. Для каждого предмета из списка `items` она печатает строку "
               "вида `Tent: 2500 g`, потом строку вида `Total: 5700 g` с общим весом. Если общий вес больше `limit`, "
               "последней строкой печатает `Too heavy`, иначе — `Ready for the hike`.",
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
        steps=["Создай класс `Card` с атрибутом класса `way = \"by card\"`. В `__init__(self, balance)` сохрани баланс. "
               "Метод `pay(self, price)`: если цена не больше баланса, списывает её с баланса и возвращает `True`, "
               "иначе возвращает `False`.",
               "Создай отдельный класс `Coupon` (не наследник `Card`) с атрибутом класса `way = \"by coupon\"`. "
               "В `__init__(self, value)` сохрани номинал купона. Метод `pay(self, price)`: если цена не больше номинала, "
               "купон сгорает целиком — номинал становится 0 — и метод возвращает `True`, иначе возвращает `False`.",
               "Напиши функцию `pay_for(price, payers)`. Она по очереди пробует заплатить `price` каждым способом "
               "из списка `payers`, вызывая у него `pay(price)`. При первой удачной оплате печатает строку вида "
               "`300 rub: paid by coupon` и сразу завершает работу через `return`. Если не подошёл ни один способ, "
               "печатает строку вида `1200 rub: not enough money`.",
               "Создай `card = Card(balance)` и `coupon = Coupon(coupon_value)`. Для каждой цены из `prices` вызови "
               "`pay_for(price, [coupon, card])` — сначала пробуем купон, потом карту.",
               "Последней строкой выведи остаток на карте в виде `Left on card: 250 rub`"],
        hint="Функции `pay_for` не нужно знать, карта перед ней или купон: она вызывает `payer.pay(price)` и смотрит, "
             "вернулось `True` или `False`. Это и есть утиная типизация: если объект умеет платить, им можно платить.",
        solution=CHECKOUT,
        wrong=[("купон не сгорает после оплаты — им платят снова и снова",
                CHECKOUT.replace("            self.value = 0\n", "")),
               ("после удачной оплаты не выходит из функции — покупку оплачивают и купоном, и картой",
                CHECKOUT.replace('            print(f"{price} rub: paid {payer.way}")\n            return\n',
                                 '            print(f"{price} rub: paid {payer.way}")\n'))],
        constructs=["class", "function", "for"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("pay_for", "price, payers")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-duck-paint-cost", title="Сколько стоит покраска",
        given=["side", "width", "height", "price"],
        variants=[{"side": "4", "width": "5", "height": "3", "price": "30"},
                  {"side": "6", "width": "8", "height": "2", "price": "25"},
                  {"side": "3", "width": "4", "height": "7", "price": "50"}],
        hidden=[{"side": "1", "width": "1", "height": "1", "price": "10"},
                {"side": "10", "width": "12", "height": "3", "price": "15"},
                {"side": "5", "width": "2", "height": "9", "price": "40"}],
        intro="На даче нужно покрасить квадратный пол веранды со стороной `side` метров и прямоугольную стену "
              "шириной `width` и высотой `height` метров. Краска на один квадратный метр стоит `price` рублей. "
              "Квадрат и прямоугольник — разные классы без общего родителя, но оба умеют считать свою площадь "
              "методом `area()`.",
        steps=["Создай класс `Square`. В `__init__(self, side)` сохрани длину стороны. Метод `area(self)` возвращает "
               "площадь квадрата — сторону, умноженную на саму себя.",
               "Создай отдельный класс `Rectangle`, без родителя. В `__init__(self, width, height)` сохрани ширину "
               "и высоту. Метод `area(self)` возвращает ширину, умноженную на высоту.",
               "Напиши функцию `paint(shape, price)`, которая печатает строку вида `Area 16 m2, cost 480 rub`: "
               "площадь фигуры из `shape.area()` и стоимость краски — площадь, умноженную на `price`. "
               "Проверять, квадрат это или прямоугольник, не нужно.",
               "Создай `floor = Square(side)` и `wall = Rectangle(width, height)` и вызови `paint` сначала для пола, "
               "потом для стены."],
        hint="Функция `paint` просто вызывает `area()` у того, что ей передали, — у квадрата и у прямоугольника этот метод "
             "считает по-разному, но называется одинаково. Метод должен **возвращать** площадь через `return`.",
        solution=PAINT,
        wrong=[("площадь квадрата считается как периметр — сторона умножается на 4",
                PAINT.replace("        return self.side * self.side", "        return self.side * 4")),
               ("функция paint берёт глобальную переменную floor вместо параметра shape — дважды выводится пол",
                PAINT.replace("    print(f\"Area {shape.area()} m2, cost {shape.area() * price} rub\")",
                              "    print(f\"Area {floor.area()} m2, cost {floor.area() * price} rub\")"))],
        constructs=["class", "function"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("paint", "shape, price")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-duck-commute", title="Как быстрее добраться",
        given=["km", "speed", "wait"],
        variants=[{"km": "3", "speed": "15", "wait": "10"},
                  {"km": "2", "speed": "10", "wait": "1"},
                  {"km": "1", "speed": "4", "wait": "20"}],
        hidden=[{"km": "2", "speed": "12", "wait": "6"},
                {"km": "1", "speed": "5", "wait": "15"},
                {"km": "5", "speed": "12", "wait": "3"},
                {"km": "4", "speed": "20", "wait": "30"}],
        intro="До школы `km` километров. Добраться можно пешком, на велосипеде со скоростью `speed` км/ч или на автобусе, "
              "которого приходится ждать `wait` минут. Это три разных класса, и время в пути каждый считает по-своему, "
              "но у всех есть метод `minutes(km)`.",
        steps=["Создай три отдельных класса без общего родителя. У каждого — атрибут класса `name` и метод "
               "`minutes(self, km)`, который возвращает время в пути в минутах.",
               "`Walk`: `name = \"Walk\"`, `__init__` не нужен, `minutes` возвращает по 12 минут на километр. "
               "`Bike`: `name = \"Bike\"`, в `__init__(self, speed)` сохраняет скорость, `minutes` возвращает "
               "`km * 60 // self.speed`.",
               "`Bus`: `name = \"Bus\"`, в `__init__(self, wait)` сохраняет время ожидания, `minutes` возвращает "
               "ожидание плюс по 2 минуты на километр.",
               "Напиши функцию `choose(options, km)`. Сначала лучшим считай первый способ из списка `options`. "
               "Для каждого способа печатай строку вида `Bike: 12 min`; если его время строго меньше времени лучшего, "
               "он становится лучшим. После цикла выведи строку вида `Best: Bike`.",
               "Вызови `choose([Walk(), Bike(speed), Bus(wait)], km)`."],
        hint="Функции `choose` не важно, что перед ней — велосипед или автобус: она вызывает `minutes(km)` у любого способа. "
             "Лучший способ можно хранить как сам объект и потом взять у него `name`. Если времена равны, "
             "лучшим остаётся тот, что стоит в списке раньше.",
        solution=COMMUTE,
        wrong=[("при равном времени выбирает способ, который стоит в списке позже",
                COMMUTE.replace("        if time < best.minutes(km):", "        if time <= best.minutes(km):")),
               ("выбирает самый долгий способ вместо самого быстрого",
                COMMUTE.replace("        if time < best.minutes(km):", "        if time > best.minutes(km):"))],
        constructs=["class", "function", "for"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("choose", "options, km")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-duck-knight-ghost", title="Рыцарь и призрак",
        given=["knight_hp", "armor", "ghost_hp", "hits"],
        variants=[{"knight_hp": "30", "armor": "5", "ghost_hp": "20", "hits": "[12, 3, 25, 10, 8]"},
                  {"knight_hp": "50", "armor": "10", "ghost_hp": "8", "hits": "[9, 20, 16, 40]"},
                  {"knight_hp": "12", "armor": "2", "ghost_hp": "30", "hits": "[15, 1, 6, 30]"}],
        hidden=[{"knight_hp": "10", "armor": "0", "ghost_hp": "10", "hits": "[10, 4]"},
                {"knight_hp": "100", "armor": "20", "ghost_hp": "5", "hits": "[20, 21, 9, 3]"},
                {"knight_hp": "5", "armor": "3", "ghost_hp": "3", "hits": "[2, 8, 7, 6]"}],
        intro="В игре по очереди наносятся удары с силой из списка `hits`, и каждый удар задевает и рыцаря, и призрака. "
              "У рыцаря `knight_hp` единиц здоровья и броня `armor`, у призрака — `ghost_hp` единиц здоровья. "
              "Урон они получают по-разному, но у обоих есть методы `take_hit(damage)` и `is_alive()`.",
        steps=["Создай класс `Knight` с атрибутом класса `name = \"Knight\"`. В `__init__(self, hp, armor)` сохрани здоровье "
               "и броню. Метод `take_hit(self, damage)`: если удар сильнее брони, здоровье уменьшается на разницу "
               "`damage - armor`, иначе не меняется; если здоровье стало меньше 0, оно становится 0. "
               "Метод `is_alive(self)` возвращает `True`, если здоровье больше 0.",
               "Создай отдельный класс `Ghost` (не наследник `Knight`) с атрибутом класса `name = \"Ghost\"`. "
               "В `__init__(self, hp)` сохрани здоровье. Метод `take_hit(self, damage)` уменьшает здоровье на "
               "`damage // 2` (призрак получает только половину урона), и здоровье тоже не опускается ниже 0. "
               "Метод `is_alive(self)` — такой же, как у рыцаря.",
               "Напиши функцию `attack(targets, damage)`. Для каждой цели из списка: если она жива, нанеси ей удар "
               "и выведи строку вида `Knight: 23 hp`, иначе выведи строку вида `Knight is out` и удар не наноси.",
               "Создай `knight = Knight(knight_hp, armor)` и `ghost = Ghost(ghost_hp)`. Для каждой силы удара из `hits` "
               "вызови `attack([knight, ghost], damage)`."],
        hint="Функция `attack` не выясняет, рыцарь перед ней или призрак: она спрашивает `is_alive()` и вызывает "
             "`take_hit(damage)`, а каждый класс сам решает, сколько здоровья потерять. Проверь удар, который слабее брони: "
             "здоровье рыцаря от него не должно расти.",
        solution=BATTLE,
        wrong=[("рыцарь вычитает броню из любого удара — слабый удар его лечит",
                BATTLE.replace("        if damage > self.armor:\n            self.hp -= damage - self.armor\n",
                               "        self.hp -= damage - self.armor\n")),
               ("бьёт и уже выбывшие цели — вместо «is out» печатается 0 hp",
                BATTLE.replace("        if target.is_alive():\n", "        if True:\n"))],
        constructs=["class", "function", "for"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("attack", "targets, damage")],
    ),
]
