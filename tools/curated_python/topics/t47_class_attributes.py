"""PY_CLASS_ATTRIBUTES — «Атрибуты класса». Taught before: everything up to functions, classes, creating objects,
__init__, self and methods, «private» attributes, @property. Here: an attribute written in the class body is one for
all objects; it is read through the class or through any object; a counter of created objects changes through the
class name; changing the attribute through the class reaches every object, assigning it through an object makes a
separate copy. Not yet: inheritance (next topics), tuples, dicts, comprehensions, try/except."""
from build import OutputTask

SKILL = "PY_CLASS_ATTRIBUTES"

NEED_CLASS = ("ClassDef", "Опиши объект в собственном классе через class.")


def class_level(name: str, example: str, cls: str, why: str) -> tuple[str, str]:
    """The attribute is assigned right in the class body (one indentation level), not in __init__."""
    return (f"re:(?m)^( {{1,4}}|\\t){name}\\s*=(?!=)",
            f"Сделай `{name}` атрибутом класса: запиши `{example}` прямо в теле класса `{cls}`, а не в `__init__`. {why}")


SHELF = """\
class Shelf:
    capacity = 30

    def __init__(self, topic, books):
        self.topic = topic
        self.books = books

    def free_places(self):
        return Shelf.capacity - self.books


first = Shelf(topic1, books1)
second = Shelf(topic2, books2)
print(f"Each shelf holds: {Shelf.capacity}")
print(f"{first.topic}: {first.free_places()} free places")
print(f"{second.topic}: {second.free_places()} free places")
"""

MONSTER = """\
class Monster:
    count = 0

    def __init__(self, name):
        self.name = name
        Monster.count += 1
        self.number = Monster.count


for name in names:
    monster = Monster(name)
    print(f"Monster {monster.number}: {monster.name}")
print(f"Total monsters: {Monster.count}")
"""

TRIP = """\
class Trip:
    rate = 25

    def __init__(self, km):
        self.km = km

    def cost(self):
        return self.km * self.rate


trips = []
for km in distances:
    trips.append(Trip(km))
for trip in trips:
    print(f"{trip.km} km: {trip.cost()} rub")
Trip.rate = new_rate
print(f"New rate: {Trip.rate} rub per km")
for trip in trips:
    print(f"{trip.km} km: {trip.cost()} rub")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-clsattr-library-shelves", title="Полки в библиотеке",
        given=["topic1", "books1", "topic2", "books2"],
        variants=[{"topic1": '"Sci-fi"', "books1": "18", "topic2": '"Crime"', "books2": "25"},
                  {"topic1": '"Fairy tales"', "books1": "7", "topic2": '"Poems"', "books2": "30"},
                  {"topic1": '"History"', "books1": "29", "topic2": '"Science"', "books2": "11"}],
        hidden=[{"topic1": '"Comics"', "books1": "0", "topic2": '"Dictionaries"', "books2": "30"},
                {"topic1": '"Sport"', "books1": "15", "topic2": '"Music"', "books2": "15"},
                {"topic1": '"Cooking"', "books1": "3", "topic2": '"Travel"', "books2": "22"}],
        intro="В школьной библиотеке все полки одинаковые: на любую помещается 30 книг. Это общее свойство всех полок, "
              "поэтому его удобно записать один раз — в самом классе, а не в каждом объекте. "
              "А тема полки и число книг на ней у каждой полки свои.",
        steps=["Создай класс `Shelf`. Прямо в теле класса, а не в `__init__`, запиши атрибут класса `capacity = 30`.",
               "В `__init__(self, topic, books)` сохрани тему полки и количество книг на ней в атрибуты "
               "`self.topic` и `self.books`.",
               "Добавь метод `free_places(self)`, который возвращает, сколько ещё книг поместится на полку: "
               "вместимость минус количество книг.",
               "Создай две полки: `first = Shelf(topic1, books1)` и `second = Shelf(topic2, books2)`.",
               "Выведи строку `Each shelf holds: 30` — число возьми из `Shelf.capacity`. Потом выведи "
               "по строке для первой и для второй полки в виде `Sci-fi: 12 free places`."],
        hint="Атрибут класса записывают в теле класса без `self`. Прочитать его можно и через класс — `Shelf.capacity`, "
             "и через объект — `self.capacity`: если у объекта нет своего атрибута с таким именем, Python возьмёт его у класса. "
             "А вот количество книг у каждой полки своё — его бери из `self.books`.",
        solution=SHELF,
        wrong=[("уменьшает общую вместимость у класса — вторая полка считается от уже уменьшенного числа",
                SHELF.replace("        return Shelf.capacity - self.books",
                              "        Shelf.capacity -= self.books\n        return Shelf.capacity")),
               ("берёт в методе переменную books1 из заготовки вместо self.books — у обеих полок одинаковый ответ",
                SHELF.replace("Shelf.capacity - self.books", "Shelf.capacity - books1"))],
        constructs=["class"],
        must_use=[NEED_CLASS, class_level("capacity", "capacity = 30", "Shelf",
                                          "Тогда вместимость будет одна на все полки.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-clsattr-monster-counter", title="Счётчик монстров",
        given=["names"],
        variants=[{"names": '["Goblin", "Troll", "Orc"]'},
                  {"names": '["Dragon", "Skeleton"]'},
                  {"names": '["Slime", "Spider", "Wolf", "Ghost"]'}],
        hidden=[{"names": '["Zombie"]'},
                {"names": '["Minotaur", "Cyclops", "Harpy", "Hydra", "Centaur"]'},
                {"names": '["Troll", "Troll"]'}],
        intro="В игре на уровне по очереди появляются монстры из списка `names`. Игра даёт каждому монстру "
              "порядковый номер и помнит, сколько монстров создано всего. Счётчик один на всех монстров — "
              "значит, это атрибут класса.",
        steps=["Создай класс `Monster` с атрибутом класса `count = 0` — сколько монстров уже создано.",
               "В `__init__(self, name)` сохрани имя в `self.name`, затем увеличь общий счётчик `Monster.count` на 1 "
               "и сохрани его новое значение в `self.number` — это порядковый номер монстра.",
               "Пройди циклом по списку `names` и для каждого имени создай монстра. Сразу после создания выведи "
               "строку вида `Monster 1: Goblin` — номер и имя бери из атрибутов объекта.",
               "После цикла выведи строку вида `Total monsters: 3` — число возьми из `Monster.count`."],
        hint="Меняй общий счётчик через имя класса, а не через `self`. Запись `self.count += 1` создаст у объекта "
             "его собственную копию счётчика, а общий счётчик класса так и останется нулём.",
        solution=MONSTER,
        wrong=[("увеличивает self.count — у каждого монстра своя копия, номер всегда 1, а общий счётчик 0",
                MONSTER.replace("        Monster.count += 1\n        self.number = Monster.count",
                                "        self.count += 1\n        self.number = self.count")),
               ("запоминает номер до увеличения счётчика — нумерация начинается с нуля",
                MONSTER.replace("        Monster.count += 1\n        self.number = Monster.count",
                                "        self.number = Monster.count\n        Monster.count += 1"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS,
                  class_level("count", "count = 0", "Monster", "Тогда счётчик будет один на всех монстров."),
                  ("re:Monster\\.count\\s*(\\+=|=\\s*Monster\\.count\\s*\\+)",
                   "Увеличивай счётчик через имя класса: `Monster.count += 1`. Так меняется общий счётчик, "
                   "а не копия у одного монстра.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-clsattr-taxi-rate", title="Новый тариф такси",
        given=["distances", "new_rate"],
        variants=[{"distances": "[5, 12, 3]", "new_rate": "30"},
                  {"distances": "[8, 2]", "new_rate": "40"},
                  {"distances": "[10, 4, 7, 1]", "new_rate": "20"}],
        hidden=[{"distances": "[6]", "new_rate": "35"},
                {"distances": "[1, 2, 3]", "new_rate": "25"},
                {"distances": "[15, 9]", "new_rate": "50"}],
        intro="Диспетчер такси считает стоимость заказанных поездок. Цена за километр одинакова для всех поездок — "
              "это тариф, общий для всего таксопарка. Длины поездок в километрах записаны в списке `distances`. "
              "Вдруг тариф меняется на `new_rate` рублей за километр, и все поездки нужно пересчитать.",
        steps=["Создай класс `Trip` с атрибутом класса `rate = 25` — цена одного километра. "
               "В `__init__(self, km)` сохрани длину поездки в `self.km`.",
               "Добавь метод `cost(self)`, который возвращает стоимость поездки: километры, умноженные на тариф.",
               "Для каждого числа из `distances` создай объект `Trip` и сложи эти объекты в список `trips`. "
               "Выведи стоимость каждой поездки строкой вида `5 km: 125 rub`",
               "Поменяй тариф один раз сразу для всех поездок: `Trip.rate = new_rate`. Затем выведи строку вида "
               "`New rate: 30 rub per km` — число возьми из `Trip.rate`.",
               "Снова выведи стоимость каждой поездки в том же виде, уже по новому тарифу. "
               "Новые объекты не создавай — пройди по тому же списку `trips`."],
        hint="Если у объекта нет своего атрибута `rate`, Python берёт его у класса. Поэтому достаточно один раз "
             "поменять `Trip.rate`, и новый тариф сразу увидят все поездки — даже созданные раньше. "
             "А присваивание через объект (`trip.rate = ...`) создаст копию только у этого объекта.",
        solution=TRIP,
        wrong=[("меняет тариф через первую поездку — остальные поездки и сам класс остаются со старым тарифом",
                TRIP.replace("Trip.rate = new_rate", "trips[0].rate = new_rate")),
               ("записывает тариф в __init__ как атрибут объекта — смена тарифа у класса до поездок не доходит",
                TRIP.replace("        self.km = km", "        self.km = km\n        self.rate = 25"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS,
                  class_level("rate", "rate = 25", "Trip", "Тогда тариф будет общим для всех поездок."),
                  ("re:Trip\\.rate\\s*=(?!=)",
                   "Поменяй тариф через сам класс: `Trip.rate = new_rate`. Тогда новая цена сразу "
                   "подействует на все поездки.")],
    ),
]
