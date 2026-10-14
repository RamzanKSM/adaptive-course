"""PY_SUPER_BASIC — «super()». Taught before: everything up to classes, __init__, self and methods, «private»
attributes, @property, class attributes, inheritance, overriding, polymorphism. Here: a child's own __init__ calls
super().__init__(...) so the parent sets up its part (attributes, a shared counter), then adds its own attributes;
an overridden method extends the parent's result through super().method(). Not yet: duck typing (next topic),
tuples, dicts, comprehensions, try/except."""
from build import OutputTask

SKILL = "PY_SUPER_BASIC"

NEED_CLASS = ("ClassDef", "Опиши объекты в собственных классах через class.")
NEED_SUPER_INIT = ("re:super\\(\\)\\.__init__\\(",
                   "В `__init__` наследника вызови конструктор родителя через `super().__init__(...)`: "
                   "пусть родитель сам заполнит свою часть объекта, а наследник добавит только новое.")


def child_of(child: str, parent: str) -> tuple[str, str]:
    return (f"re:class\\s+{child}\\s*\\(\\s*{parent}\\s*\\)",
            f"Сделай класс `{child}` наследником `{parent}`: напиши `class {child}({parent}):`.")


COURIER = """\
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def info(self):
        return f"{self.name}: {self.salary} rub"


class Courier(Employee):
    def __init__(self, name, salary, transport):
        super().__init__(name, salary)
        self.transport = transport


courier = Courier(name, salary, transport)
print(courier.info())
print(f"Transport: {courier.transport}")
"""

CAPTAIN = """\
class Player:
    count = 0

    def __init__(self, name):
        self.name = name
        Player.count += 1


class Captain(Player):
    def __init__(self, name, number):
        super().__init__(name)
        self.number = number


for name in players:
    player = Player(name)
cap = Captain(captain, number)
print(f"Captain: {cap.name}, number {cap.number}")
print(f"Total players: {Player.count}")
"""

GARAGE = """\
class Vehicle:
    def __init__(self, name):
        self.name = name
        self.wheels = 4

    def info(self):
        return f"{self.name}, wheels: {self.wheels}"


class Motorbike(Vehicle):
    def __init__(self, name, speed):
        super().__init__(name)
        self.wheels = 2
        self.speed = speed

    def info(self):
        return super().info() + f", top speed {self.speed} km/h"


garage = [Vehicle(car), Motorbike(bike, speed)]
for vehicle in garage:
    print(vehicle.info())
"""


LESSON = """\
class Lesson:
    def __init__(self, subject, minutes):
        self.subject = subject
        self.minutes = minutes

    def info(self):
        return f"{self.subject}: {self.minutes} min"


class OnlineLesson(Lesson):
    def __init__(self, subject, minutes, link):
        super().__init__(subject, minutes)
        self.link = link


lesson = OnlineLesson(subject, minutes, link)
print(lesson.info())
print(f"Link: {lesson.link}")
"""

BOSS = """\
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        if self.health > 100:
            self.health = 100


class Boss(Character):
    def __init__(self, name, health, armor):
        super().__init__(name, health)
        self.armor = armor
        self.health += armor


hero = Character(hero_name, hero_health)
boss = Boss(boss_name, boss_health, armor)
print(f"{hero.name}: health {hero.health}")
print(f"{boss.name}: health {boss.health}, armor {boss.armor}")
"""

DELIVERY = """\
class Order:
    def __init__(self, prices):
        self.prices = prices

    def total(self):
        result = 0
        for price in self.prices:
            result += price
        return result

    def describe(self):
        return f"Items: {len(self.prices)}, total: {self.total()} rub"


class DeliveryOrder(Order):
    def __init__(self, prices, address):
        super().__init__(prices)
        self.address = address

    def total(self):
        base = super().total()
        if base < 1000:
            return base + 200
        return base

    def describe(self):
        return super().describe() + f", delivery to {self.address}"


orders = [Order(prices), DeliveryOrder(prices, address)]
for order in orders:
    print(order.describe())
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-super-courier", title="Курьер службы доставки",
        given=["name", "salary", "transport"],
        variants=[{"name": '"Oleg"', "salary": "45000", "transport": '"bike"'},
                  {"name": '"Marina"', "salary": "52000", "transport": '"scooter"'},
                  {"name": '"Artyom"', "salary": "61000", "transport": '"moped"'}],
        hidden=[{"name": '"Liza"', "salary": "38000", "transport": '"on foot"'},
                {"name": '"Rustam"', "salary": "70500", "transport": '"car"'},
                {"name": '"Ksyusha"', "salary": "40000", "transport": '"e-bike"'}],
        intro="В службе доставки работают сотрудники: у каждого есть имя и зарплата. Курьер — тоже сотрудник, "
              "только у него есть ещё и транспорт. Имя и зарплату курьера пусть сохраняет класс-родитель, "
              "а курьер добавит только своё.",
        steps=["Создай класс `Employee`. В `__init__(self, name, salary)` сохрани имя и зарплату в `self.name` "
               "и `self.salary`. Добавь метод `info(self)`, который возвращает строку вида `Oleg: 45000 rub`",
               "Создай класс `Courier` — наследник `Employee` — со своим `__init__(self, name, salary, transport)`. "
               "Первой строкой в нём вызови `super().__init__(name, salary)`, а потом сохрани `self.transport`.",
               "Создай `courier = Courier(name, salary, transport)`.",
               "Выведи две строки: результат `courier.info()` и строку вида `Transport: bike`."],
        hint="`super().__init__(...)` запускает `__init__` родителя для того же самого объекта. Аргументы передавай "
             "в том порядке, в каком их ждёт родитель: сначала имя, потом зарплата.",
        solution=COURIER,
        wrong=[("передаёт аргументы родителю в другом порядке — имя и зарплата меняются местами",
                COURIER.replace("super().__init__(name, salary)", "super().__init__(salary, name)")),
               ("параметры в __init__ курьера стоят не в том порядке, в каком передаются при создании",
                COURIER.replace("def __init__(self, name, salary, transport):",
                                "def __init__(self, transport, name, salary):"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("Courier", "Employee"), NEED_SUPER_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-super-team-captain", title="Капитан команды",
        given=["players", "captain", "number"],
        variants=[{"players": '["Anya", "Vika", "Sveta"]', "captain": '"Lena"', "number": "10"},
                  {"players": '["Petya", "Kolya"]', "captain": '"Sasha"', "number": "7"},
                  {"players": '["Dasha", "Masha", "Glasha", "Natasha", "Pasha"]', "captain": '"Misha"', "number": "1"}],
        hidden=[{"players": "[]", "captain": '"Gosha"', "number": "9"},
                {"players": '["Ira"]', "captain": '"Yulya"', "number": "23"},
                {"players": '["Lyova", "Tima", "Roma", "Zhenya"]', "captain": '"Fedya"', "number": "4"}],
        intro="Школьная футбольная команда записывает игроков. Класс игрока сам считает, сколько игроков создано. "
              "Капитан — тоже игрок, только у него есть ещё номер на капитанской повязке. "
              "Важно, чтобы капитан тоже попал в общий счёт.",
        steps=["Создай класс `Player` с атрибутом класса `count = 0`. В `__init__(self, name)` сохрани имя "
               "в `self.name` и увеличь `Player.count` на 1.",
               "Создай класс `Captain` — наследник `Player` — со своим `__init__(self, name, number)`. "
               "Вызови в нём `super().__init__(name)`, а потом сохрани `self.number`. Счётчик в `Captain` "
               "сам не трогай — это уже делает родитель.",
               "Создай объект `Player` для каждого имени из списка `players`, а потом капитана: "
               "`cap = Captain(captain, number)`.",
               "Выведи строку вида `Captain: Lena, number 10`, а затем строку вида `Total players: 4` — "
               "число возьми из `Player.count`."],
        hint="Если в `Captain` написать свой `__init__` и не вызвать родительский, код из `Player.__init__` "
             "для капитана не выполнится — и счётчик его не заметит. `super().__init__(name)` запускает "
             "этот код и для капитана.",
        solution=CAPTAIN,
        wrong=[("не вызывает super().__init__, а сохраняет имя сам — капитан не попадает в счётчик",
                CAPTAIN.replace("        super().__init__(name)\n", "        self.name = name\n")),
               ("вызывает super().__init__ и ещё раз сам увеличивает счётчик — капитан посчитан дважды",
                CAPTAIN.replace("        super().__init__(name)\n",
                                "        super().__init__(name)\n        Player.count += 1\n"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("Captain", "Player"), NEED_SUPER_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-super-motorbike", title="Мотоцикл в гараже",
        given=["car", "bike", "speed"],
        variants=[{"car": '"Lada"', "bike": '"Ural"', "speed": "180"},
                  {"car": '"Niva"', "bike": '"Jawa"', "speed": "120"},
                  {"car": '"Volga"', "bike": '"Minsk"', "speed": "95"}],
        hidden=[{"car": '"Moskvich"', "bike": '"Dnepr"', "speed": "150"},
                {"car": '"Gazel"', "bike": '"Sova"', "speed": "60"},
                {"car": '"Zhiguli"', "bike": '"Voskhod"', "speed": "110"}],
        intro="Программа описывает транспорт в гараже. У обычной машины 4 колеса. Мотоцикл — тоже транспорт, "
              "но колёс у него 2, а в описании нужна ещё и максимальная скорость. Описание мотоцикла должно "
              "продолжать описание родителя, а не повторять его код.",
        steps=["Создай класс `Vehicle`. В `__init__(self, name)` сохрани название в `self.name` и задай "
               "`self.wheels = 4`. Добавь метод `info(self)`, который возвращает строку вида `Lada, wheels: 4`.",
               "Создай класс `Motorbike` — наследник `Vehicle` — со своим `__init__(self, name, speed)`: вызови "
               "`super().__init__(name)`, после этого поставь `self.wheels = 2` и сохрани `self.speed`.",
               "Переопредели в `Motorbike` метод `info(self)`: пусть он берёт строку родителя через `super().info()` "
               "и дописывает к ней `, top speed 180 km/h` — со скоростью из `self.speed`.",
               "Создай список `garage = [Vehicle(car), Motorbike(bike, speed)]` и одним циклом выведи `info()` "
               "каждого транспорта."],
        hint="Порядок в `__init__` важен: `super().__init__(name)` ставит 4 колеса. Если задать `self.wheels = 2` "
             "до вызова родителя, родитель перезапишет это значение. А `super().info()` возвращает строку — "
             "к ней можно приклеить продолжение через `+`.",
        solution=GARAGE,
        wrong=[("задаёт 2 колеса до вызова super().__init__ — родитель перезаписывает их на 4",
                GARAGE.replace("        super().__init__(name)\n        self.wheels = 2\n",
                               "        self.wheels = 2\n        super().__init__(name)\n")),
               ("в info мотоцикла не вызывает super().info() — пропадают название и колёса",
                GARAGE.replace('        return super().info() + f", top speed {self.speed} km/h"',
                               '        return f"top speed {self.speed} km/h"'))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("Motorbike", "Vehicle"), NEED_SUPER_INIT,
                  ("re:super\\(\\)\\.info\\(\\)",
                   "В `info` мотоцикла возьми описание родителя через `super().info()` и допиши к нему скорость — "
                   "так не придётся повторять код родителя.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-super-online-lesson", title="Онлайн-урок",
        given=["subject", "minutes", "link"],
        variants=[{"subject": '"Math"', "minutes": "45", "link": '"meet.school.ru/math7"'},
                  {"subject": '"English"', "minutes": "40", "link": '"meet.school.ru/eng5"'},
                  {"subject": '"Physics"', "minutes": "90", "link": '"meet.school.ru/phys9"'}],
        hidden=[{"subject": '"History"', "minutes": "30", "link": '"meet.school.ru/hist"'},
                {"subject": '"Art"', "minutes": "60", "link": '"meet.school.ru/art2"'},
                {"subject": '"Biology"', "minutes": "35", "link": '"meet.school.ru/bio"'}],
        intro="В расписании школы у каждого урока есть предмет и длительность в минутах. Онлайн-урок — тоже урок, "
              "только у него есть ещё ссылка на видеовстречу. Предмет и длительность пусть сохраняет класс-родитель, "
              "а онлайн-урок добавит только ссылку.",
        steps=["Создай класс `Lesson`. В `__init__(self, subject, minutes)` сохрани предмет и длительность "
               "в `self.subject` и `self.minutes`. Добавь метод `info(self)`, который возвращает строку вида `Math: 45 min`.",
               "Создай класс `OnlineLesson` — наследник `Lesson` — со своим `__init__(self, subject, minutes, link)`. "
               "Первой строкой в нём вызови `super().__init__(subject, minutes)`, а потом сохрани `self.link`.",
               "Создай `lesson = OnlineLesson(subject, minutes, link)`.",
               "Выведи две строки: результат `lesson.info()` и строку вида `Link: meet.school.ru/math7`."],
        hint="`super().__init__(...)` запускает `__init__` родителя для того же самого объекта, поэтому после него "
             "у онлайн-урока уже есть `self.subject` и `self.minutes`. Передай родителю именно параметры, "
             "а не готовые числа.",
        solution=LESSON,
        wrong=[("передаёт родителю аргументы в другом порядке — предмет и минуты меняются местами",
                LESSON.replace("super().__init__(subject, minutes)", "super().__init__(minutes, subject)")),
               ("передаёт родителю число 45 вместо параметра minutes — все уроки по 45 минут",
                LESSON.replace("super().__init__(subject, minutes)", "super().__init__(subject, 45)"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("OnlineLesson", "Lesson"), NEED_SUPER_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-super-boss-armor", title="Броня босса",
        given=["hero_name", "hero_health", "boss_name", "boss_health", "armor"],
        variants=[{"hero_name": '"Knight"', "hero_health": "150", "boss_name": '"Dragon"', "boss_health": "200", "armor": "30"},
                  {"hero_name": '"Elf"', "hero_health": "80", "boss_name": '"Troll"', "boss_health": "90", "armor": "50"},
                  {"hero_name": '"Wizard"', "hero_health": "100", "boss_name": '"Golem"', "boss_health": "120", "armor": "75"}],
        hidden=[{"hero_name": '"Rogue"', "hero_health": "101", "boss_name": '"Hydra"', "boss_health": "100", "armor": "10"},
                {"hero_name": '"Monk"', "hero_health": "60", "boss_name": '"Ogre"', "boss_health": "40", "armor": "0"},
                {"hero_name": '"Bard"', "hero_health": "99", "boss_name": '"Lich"', "boss_health": "500", "armor": "100"}],
        intro="В игре у любого персонажа здоровье не может быть больше 100: если при создании передали больше, "
              "оно урезается до 100. Босс — тоже персонаж, к нему применяется то же правило, но у босса есть ещё броня, "
              "и она добавляется к здоровью уже после урезания. Создай героя и босса.",
        steps=["Создай класс `Character`. В `__init__(self, name, health)` сохрани имя в `self.name`, а здоровье — "
               "в `self.health`; если оно больше 100, сделай его ровно 100.",
               "Создай класс `Boss` — наследник `Character` — со своим `__init__(self, name, health, armor)`. "
               "Сначала вызови `super().__init__(name, health)` — пусть родитель сохранит имя и урежет здоровье. "
               "Потом сохрани `self.armor` и прибавь броню к `self.health`.",
               "Создай `hero = Character(hero_name, hero_health)` и `boss = Boss(boss_name, boss_health, armor)`.",
               "Выведи строки вида `Knight: health 100` и `Dragon: health 130, armor 30`."],
        hint="Правило про 100 написано только в `Character.__init__`. Если наследник не вызовет `super().__init__`, "
             "а сохранит здоровье сам, правило для босса не сработает. И порядок важен: броню прибавляй после "
             "вызова родителя, иначе родитель перезапишет здоровье.",
        solution=BOSS,
        wrong=[("не вызывает super().__init__, а сохраняет имя и здоровье сам — здоровье босса не урезается",
                BOSS.replace("        super().__init__(name, health)\n",
                             "        self.name = name\n        self.health = health\n")),
               ("прибавляет броню до вызова родителя — родитель перезаписывает здоровье, и брони в нём нет",
                BOSS.replace("        super().__init__(name, health)\n        self.armor = armor\n        self.health += armor\n",
                             "        self.health = health + armor\n        super().__init__(name, health)\n"
                             "        self.armor = armor\n"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("Boss", "Character"), NEED_SUPER_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-super-delivery-order", title="Заказ с доставкой",
        given=["prices", "address"],
        variants=[{"prices": "[350, 420, 80]", "address": '"Lenina 5"'},
                  {"prices": "[600, 750]", "address": '"Mira 12"'},
                  {"prices": "[120, 90, 45, 300]", "address": '"Sadovaya 3"'}],
        hidden=[{"prices": "[1000]", "address": '"Gagarina 1"'},
                {"prices": "[999]", "address": '"Pushkina 10"'},
                {"prices": "[500, 500, 500]", "address": '"Lesnaya 7"'},
                {"prices": "[10]", "address": '"Tsvetochnaya 2"'}],
        intro="Магазин принимает заказы на самовывоз и с доставкой. Заказ с доставкой — тот же заказ, но к сумме "
              "добавляется 200 руб. за доставку, если товаров меньше чем на 1000 руб., а в описании нужен адрес. "
              "Покупатель сравнивает два варианта для одних и тех же товаров с ценами `prices` и адреса `address`.",
        steps=["Создай класс `Order`. В `__init__(self, prices)` сохрани список цен в `self.prices`. Добавь метод "
               "`total(self)`, который возвращает сумму цен, и метод `describe(self)`, который возвращает строку вида "
               "`Items: 3, total: 850 rub` — число товаров и сумму, полученную вызовом `self.total()`.",
               "Создай класс `DeliveryOrder` — наследник `Order` — со своим `__init__(self, prices, address)`: вызови "
               "`super().__init__(prices)` и сохрани `self.address`.",
               "Переопредели в `DeliveryOrder` метод `total(self)`: возьми сумму родителя через `super().total()` и, "
               "если она меньше 1000, прибавь 200 руб. за доставку. От 1000 руб. доставка бесплатная.",
               "Переопредели в `DeliveryOrder` метод `describe(self)`: строка родителя из `super().describe()` плюс "
               "`, delivery to Lenina 5` — с адресом из `self.address`.",
               "Создай список `orders = [Order(prices), DeliveryOrder(prices, address)]` и одним циклом выведи "
               "`describe()` каждого заказа."],
        hint="`describe` родителя вызывает `self.total()`. Для заказа с доставкой `self` — это `DeliveryOrder`, "
             "поэтому сработает его `total` с доставкой, хотя сама строка собирается в родителе. А внутри "
             "`DeliveryOrder.total` сумму товаров бери через `super().total()` — `self.total()` вызвал бы сам себя.",
        solution=DELIVERY,
        wrong=[("доставка бесплатна только от суммы больше 1000 — при ровно 1000 руб. берёт 200 руб.",
                DELIVERY.replace("if base < 1000:", "if base <= 1000:")),
               ("в describe родителя считает сумму заново, а не через self.total() — доставка в сумму не попадает",
                DELIVERY.replace('total: {self.total()} rub', 'total: {Order.total(self)} rub')),
               ("describe заказа с доставкой не вызывает super().describe() — пропадают число товаров и сумма",
                DELIVERY.replace('        return super().describe() + f", delivery to {self.address}"',
                                 '        return f"delivery to {self.address}"'))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("DeliveryOrder", "Order"), NEED_SUPER_INIT,
                  ("re:super\\(\\)\\.total\\(\\)",
                   "В `total` заказа с доставкой возьми сумму товаров через `super().total()` — так формула "
                   "суммы остаётся в одном месте."),
                  ("re:super\\(\\)\\.describe\\(\\)",
                   "В `describe` заказа с доставкой возьми строку родителя через `super().describe()` и допиши "
                   "к ней адрес.")],
    ),
]
