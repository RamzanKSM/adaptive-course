"""PY_INHERITANCE_BASIC — «Наследование». Taught before: everything up to functions, classes, __init__, self and
methods, «private» attributes, @property, class attributes. Here: `class Child(Parent)`; the child gets the parent's
__init__ and methods without writing them again and adds its own new methods, which may use the inherited attributes
and call inherited methods through self. Not yet: overriding methods, polymorphism, super() (next topics), tuples,
dicts."""
from build import OutputTask

SKILL = "PY_INHERITANCE_BASIC"

NEED_CLASS = ("ClassDef", "Опиши объекты в собственных классах через class.")


def child_of(child: str, parent: str) -> tuple[str, str]:
    return (f"re:class\\s+{child}\\s*\\(\\s*{parent}\\s*\\)",
            f"Сделай класс `{child}` наследником `{parent}`: напиши `class {child}({parent}):`. "
            f"Тогда всё, что умеет `{parent}`, `{child}` получит без повторения кода.")


def written_once(method: str, parent: str) -> tuple[str, str]:
    return (f"re:\\A(?![\\s\\S]*def\\s+{method}\\b[\\s\\S]*def\\s+{method}\\b)",
            f"Напиши метод `{method}` один раз — только в классе `{parent}`. "
            f"Наследники получат его сами, копировать его в них не нужно.")


PETS = """\
class Pet:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def daily_food(self):
        return self.weight * 30


class Cat(Pet):
    pass


class Dog(Pet):
    def walk_minutes(self):
        return self.weight * 5


cat = Cat(cat_name, cat_weight)
dog = Dog(dog_name, dog_weight)
print(f"{cat.name}: {cat.daily_food()} g of food a day")
print(f"{dog.name}: {dog.daily_food()} g of food a day")
print(f"{dog.name} walks {dog.walk_minutes()} minutes")
"""

ACCOUNT = """\
class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def show(self):
        print(f"{self.owner}: {self.balance} rub")


class SavingsAccount(Account):
    def add_interest(self, percent):
        self.deposit(self.balance * percent // 100)


account = SavingsAccount(owner, start)
account.show()
account.add_interest(percent)
account.show()
account.deposit(extra)
account.show()
account.add_interest(percent)
account.show()
"""

PARCELS = """\
class Parcel:
    def __init__(self, weight):
        self.weight = weight

    def price(self):
        return 100 + 20 * self.weight


class FragileParcel(Parcel):
    def safe_price(self):
        return self.price() + 150


total = 0
for weight in regular:
    parcel = Parcel(weight)
    print(f"Regular parcel {parcel.weight} kg: {parcel.price()} rub")
    total += parcel.price()
for weight in fragile:
    parcel = FragileParcel(weight)
    print(f"Fragile parcel {parcel.weight} kg: {parcel.safe_price()} rub")
    total += parcel.safe_price()
print(f"Total: {total} rub")
"""


STAFF = """\
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def year_salary(self):
        return self.salary * 12


class Worker(Employee):
    pass


class Chief(Employee):
    def bonus(self):
        return self.salary * 2


worker = Worker(worker_name, worker_salary)
chief = Chief(chief_name, chief_salary)
print(f"{worker.name} earns {worker.year_salary()} rub a year")
print(f"{chief.name} earns {chief.year_salary()} rub a year")
print(f"{chief.name} gets a bonus of {chief.bonus()} rub")
"""

PLAYLIST = """\
class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add(self, song):
        self.songs.append(song)

    def show(self):
        print(f"{self.name} ({len(self.songs)}): {', '.join(self.songs)}")


class SmartPlaylist(Playlist):
    def add_many(self, songs):
        for song in songs:
            if song not in self.songs:
                self.add(song)


playlist = SmartPlaylist(name)
playlist.add_many(first)
playlist.show()
playlist.add_many(second)
playlist.show()
"""

TRAINS = """\
class Train:
    def __init__(self, wagons):
        self.wagons = wagons

    def seats(self):
        return self.wagons * 50


class SleeperTrain(Train):
    def beds(self):
        return self.seats() - 20 * self.wagons


number = 1
total = 0
for record in trains:
    parts = record.split(":")
    wagons = int(parts[1])
    if parts[0] == "day":
        train = Train(wagons)
        print(f"Train {number}: {train.wagons} wagons, {train.seats()} seats")
        total += train.seats()
    else:
        train = SleeperTrain(wagons)
        print(f"Train {number}: {train.wagons} wagons, {train.beds()} beds")
        total += train.beds()
    number += 1
print(f"Passengers: {total}")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-inh-pet-food", title="Корм для питомцев",
        given=["cat_name", "cat_weight", "dog_name", "dog_weight"],
        variants=[{"cat_name": '"Murka"', "cat_weight": "4", "dog_name": '"Rex"', "dog_weight": "12"},
                  {"cat_name": '"Barsik"', "cat_weight": "6", "dog_name": '"Sharik"', "dog_weight": "20"},
                  {"cat_name": '"Snezhok"', "cat_weight": "3", "dog_name": '"Bim"', "dog_weight": "8"}],
        hidden=[{"cat_name": '"Pushok"', "cat_weight": "5", "dog_name": '"Tuzik"', "dog_weight": "5"},
                {"cat_name": '"Luna"', "cat_weight": "2", "dog_name": '"Jack"', "dog_weight": "31"},
                {"cat_name": '"Sonya"', "cat_weight": "7", "dog_name": '"Graf"', "dog_weight": "15"}],
        intro="Ветеринар составляет памятку для хозяев кошки и собаки. И кошка, и собака — питомцы: у каждого есть "
              "имя и вес, и корм для обоих считают одинаково. А вот гулять нужно только с собакой.",
        steps=["Создай класс `Pet`. В `__init__(self, name, weight)` сохрани имя и вес питомца в килограммах "
               "в атрибуты `self.name` и `self.weight`.",
               "Добавь в `Pet` метод `daily_food(self)`, который возвращает, сколько граммов корма нужно в день: "
               "по 30 граммов на каждый килограмм веса.",
               "Создай класс `Cat` — наследник `Pet`. Внутри напиши только `pass`: всё нужное кошка получит от родителя.",
               "Создай класс `Dog` — тоже наследник `Pet`. Добавь в него один новый метод `walk_minutes(self)`: "
               "сколько минут гулять с собакой — по 5 минут на каждый килограмм веса.",
               "Создай `cat = Cat(cat_name, cat_weight)` и `dog = Dog(dog_name, dog_weight)`. Выведи три строки: "
               "корм кошки, корм собаки и прогулку собаки — в виде `Murka: 120 g of food a day`, "
               "`Rex: 360 g of food a day` и `Rex walks 60 minutes`."],
        hint="Запись `class Cat(Pet):` значит «кошка — это питомец»: объект `Cat` сразу получает `__init__` "
             "и `daily_food` из класса `Pet`, хотя в самом `Cat` их нет. В наследнике пишут только то, "
             "чего нет у родителя.",
        solution=PETS,
        wrong=[("создаёт собаку с весом кошки — скопировал строку и не поправил",
                PETS.replace("Dog(dog_name, dog_weight)", "Dog(dog_name, cat_weight)")),
               ("прибавляет 30 граммов к весу вместо умножения",
                PETS.replace("return self.weight * 30", "return self.weight + 30"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("Cat", "Pet"), child_of("Dog", "Pet"), written_once("daily_food", "Pet")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-inh-savings-account", title="Накопительный счёт",
        given=["owner", "start", "percent", "extra"],
        variants=[{"owner": '"Anna"', "start": "1000", "percent": "5", "extra": "500"},
                  {"owner": '"Igor"', "start": "2000", "percent": "10", "extra": "300"},
                  {"owner": '"Sveta"', "start": "800", "percent": "3", "extra": "1200"}],
        hidden=[{"owner": '"Pyotr"', "start": "100", "percent": "50", "extra": "0"},
                {"owner": '"Olya"', "start": "5000", "percent": "1", "extra": "250"},
                {"owner": '"Misha"', "start": "0", "percent": "7", "extra": "1000"}],
        intro="Банк открыл клиенту накопительный счёт. Это обычный счёт, на который можно класть деньги, "
              "но банк ещё и начисляет на него проценты. Всё, что умеет обычный счёт, накопительный получает "
              "по наследству — дописать нужно только новое умение.",
        steps=["Создай класс `Account`. В `__init__(self, owner, balance)` сохрани владельца и сумму на счёте "
               "в атрибуты `self.owner` и `self.balance`.",
               "Добавь в `Account` метод `deposit(self, amount)`, который прибавляет `amount` к балансу, "
               "и метод `show(self)`, который печатает строку вида `Anna: 1000 rub`",
               "Создай класс `SavingsAccount` — наследник `Account`. Напиши в нём только один новый метод "
               "`add_interest(self, percent)`: он считает проценты — баланс, умноженный на `percent` "
               "и целочисленно делённый на 100 через `//`, — и зачисляет их на счёт через унаследованный метод `self.deposit(...)`.",
               "Создай `account = SavingsAccount(owner, start)`. Затем по очереди: выведи счёт через `show()`, "
               "начисли проценты `percent`, снова выведи счёт, положи на счёт `extra` рублей через `deposit`, "
               "снова выведи счёт, ещё раз начисли проценты и выведи счёт в последний раз."],
        hint="Внутри метода наследника можно вызывать методы родителя через `self` — так же, как свои: "
             "`self.deposit(...)`. А проценты каждый раз считай от текущего `self.balance`: "
             "после пополнения баланс уже другой.",
        solution=ACCOUNT,
        wrong=[("записывает проценты вместо баланса — деньги на счёте пропадают",
                ACCOUNT.replace("        self.deposit(self.balance * percent // 100)",
                                "        self.balance = self.balance * percent // 100")),
               ("считает проценты от стартовой суммы start, а не от текущего баланса",
                ACCOUNT.replace("self.deposit(self.balance * percent // 100)", "self.deposit(start * percent // 100)"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("SavingsAccount", "Account"), written_once("deposit", "Account"),
                  ("re:self\\.deposit\\(",
                   "Зачисли проценты через унаследованный метод `self.deposit(...)`: наследник может вызывать "
                   "методы родителя так же, как свои.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-inh-fragile-parcel", title="Хрупкие посылки",
        given=["regular", "fragile"],
        variants=[{"regular": "[2, 5]", "fragile": "[3]"},
                  {"regular": "[1]", "fragile": "[4, 2]"},
                  {"regular": "[10, 3, 6]", "fragile": "[1]"}],
        hidden=[{"regular": "[]", "fragile": "[5]"},
                {"regular": "[7, 7]", "fragile": "[]"},
                {"regular": "[1, 2]", "fragile": "[3, 4]"}],
        intro="Служба доставки везёт обычные и хрупкие посылки. Доставку любой посылки считают одинаково, "
              "но хрупкую ещё и кладут в защитную упаковку за отдельные деньги. Вес обычных посылок "
              "в килограммах записан в списке `regular`, хрупких — в списке `fragile`.",
        steps=["Создай класс `Parcel`. В `__init__(self, weight)` сохрани вес в `self.weight`. Добавь метод "
               "`price(self)`: доставка стоит 100 руб. плюс 20 руб. за каждый килограмм.",
               "Создай класс `FragileParcel` — наследник `Parcel`. Свой `__init__` ему не нужен. Добавь только "
               "новый метод `safe_price(self)`: цена доставки из унаследованного `self.price()` плюс 150 руб. за упаковку.",
               "Для каждого веса из `regular` создай `Parcel` и выведи строку вида `Regular parcel 2 kg: 140 rub`",
               "Для каждого веса из `fragile` создай `FragileParcel` и выведи строку вида "
               "`Fragile parcel 3 kg: 310 rub` — с ценой из `safe_price()`.",
               "Последней строкой выведи строку вида `Total: 650 rub` — сумму за все посылки (за хрупкие — вместе с упаковкой)."],
        hint="Не считай цену доставки в `safe_price` заново — вызови `self.price()`: хрупкая посылка тоже посылка, "
             "и этот метод у неё уже есть от родителя. Если потом тариф доставки изменится, править его придётся "
             "только в одном месте.",
        solution=PARCELS,
        wrong=[("считает в safe_price цену заново и забывает базовые 100 руб.",
                PARCELS.replace("        return self.price() + 150", "        return 20 * self.weight + 150")),
               ("добавляет в итог цену хрупкой посылки без упаковки",
                PARCELS.replace("    total += parcel.safe_price()", "    total += parcel.price()"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("FragileParcel", "Parcel"),
                  ("re:self\\.price\\(\\)",
                   "Внутри `safe_price` вызови унаследованный метод `self.price()`, а не считай цену доставки заново: "
                   "так формула живёт в одном месте.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-inh-staff-salary", title="Зарплата сотрудников",
        given=["worker_name", "worker_salary", "chief_name", "chief_salary"],
        variants=[{"worker_name": '"Anya"', "worker_salary": "50000", "chief_name": '"Boris"', "chief_salary": "90000"},
                  {"worker_name": '"Vika"', "worker_salary": "42000", "chief_name": '"Gleb"', "chief_salary": "75000"},
                  {"worker_name": '"Dasha"', "worker_salary": "38000", "chief_name": '"Egor"', "chief_salary": "120000"}],
        hidden=[{"worker_name": '"Zoya"', "worker_salary": "60000", "chief_name": '"Igor"', "chief_salary": "60000"},
                {"worker_name": '"Katya"', "worker_salary": "30500", "chief_name": '"Lev"', "chief_salary": "81000"},
                {"worker_name": '"Masha"', "worker_salary": "55000", "chief_name": '"Nikita"', "chief_salary": "100000"}],
        intro="Бухгалтер небольшой фирмы считает годовые зарплаты. И рабочий, и начальник — сотрудники: у каждого "
              "есть имя и зарплата за месяц, и годовую зарплату обоим считают одинаково. А вот премию в конце года "
              "получает только начальник.",
        steps=["Создай класс `Employee`. В `__init__(self, name, salary)` сохрани имя и месячную зарплату "
               "в атрибуты `self.name` и `self.salary`.",
               "Добавь в `Employee` метод `year_salary(self)`, который возвращает зарплату за год — за 12 месяцев.",
               "Создай класс `Worker` — наследник `Employee`. Внутри напиши только `pass`.",
               "Создай класс `Chief` — тоже наследник `Employee`. Добавь в него один новый метод `bonus(self)`: "
               "премия равна двум месячным зарплатам.",
               "Создай `worker = Worker(worker_name, worker_salary)` и `chief = Chief(chief_name, chief_salary)`. "
               "Выведи три строки: годовую зарплату рабочего, годовую зарплату начальника и премию начальника — "
               "в виде `Anya earns 600000 rub a year`, `Boris earns 1080000 rub a year` и `Boris gets a bonus of 180000 rub`."],
        hint="Запись `class Chief(Employee):` значит «начальник — это сотрудник»: объект `Chief` получает `__init__` "
             "и `year_salary` от `Employee`, хотя в самом `Chief` их нет. В наследнике пишут только новое — `bonus`.",
        solution=STAFF,
        wrong=[("создаёт начальника с зарплатой рабочего — скопировал строку и не поправил",
                STAFF.replace("Chief(chief_name, chief_salary)", "Chief(chief_name, worker_salary)")),
               ("считает премию как одну месячную зарплату",
                STAFF.replace("return self.salary * 2", "return self.salary"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("Worker", "Employee"), child_of("Chief", "Employee"),
                  written_once("year_salary", "Employee")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-inh-smart-playlist", title="Умный плейлист",
        given=["name", "first", "second"],
        variants=[{"name": '"Road"', "first": '["Sun", "Rain", "Wind"]', "second": '["Rain", "Snow"]'},
                  {"name": '"Gym"', "first": '["Run", "Jump"]', "second": '["Swim", "Run", "Jump", "Lift"]'},
                  {"name": '"Sleep"', "first": '["Moon", "Stars", "Moon"]', "second": '["Night"]'}],
        hidden=[{"name": '"Party"', "first": '["Dance"]', "second": '["Dance"]'},
                {"name": '"Study"', "first": '["Focus", "Calm"]', "second": '["Calm", "Calm", "Ocean", "Focus"]'},
                {"name": '"Trip"', "first": '["Hills", "River", "Forest"]', "second": '["Sea", "Sky"]'}],
        intro="В музыкальном приложении есть обычные плейлисты, куда песни добавляют по одной. Ты делаешь умный "
              "плейлист: он умеет всё то же самое, но ещё может добавить сразу целый список песен и при этом пропускает "
              "песни, которые в нём уже есть. Плейлист называется `name`; сначала в него добавляют список `first`, "
              "потом — список `second`.",
        steps=["Создай класс `Playlist`. В `__init__(self, name)` сохрани название в `self.name` и создай пустой "
               "список `self.songs`.",
               "Добавь в `Playlist` метод `add(self, song)`, который добавляет песню в конец списка, и метод `show(self)`, "
               "который печатает строку вида `Road (3): Sun, Rain, Wind` — название, число песен в скобках и песни "
               "через запятую и пробел.",
               "Создай класс `SmartPlaylist` — наследник `Playlist`. Напиши в нём только один новый метод "
               "`add_many(self, songs)`: он проходит по списку `songs` и каждую песню, которой ещё нет в `self.songs`, "
               "добавляет через унаследованный метод `self.add(...)`.",
               "Создай `playlist = SmartPlaylist(name)`. Вызови `add_many(first)` и `show()`, потом `add_many(second)` "
               "и снова `show()`."],
        hint="Проверить, есть ли песня в списке, можно так: `if song not in self.songs`. Добавлять песню внутри "
             "`add_many` нужно через `self.add(song)` — метод родителя вызывается через `self`, как свой. "
             "Песни в строку склеивает `\", \".join(self.songs)`.",
        solution=PLAYLIST,
        wrong=[("не проверяет повторы — одна и та же песня попадает в плейлист дважды",
                PLAYLIST.replace("            if song not in self.songs:\n                self.add(song)",
                                 "            self.add(song)")),
               ("add_many заменяет весь список новым — старые песни пропадают",
                PLAYLIST.replace("        for song in songs:\n            if song not in self.songs:\n                self.add(song)",
                                 "        self.songs = []\n        for song in songs:\n            if song not in self.songs:\n"
                                 "                self.add(song)"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("SmartPlaylist", "Playlist"), written_once("add", "Playlist"),
                  ("re:self\\.add\\(",
                   "Добавляй песни через унаследованный метод `self.add(...)`: наследник может вызывать "
                   "методы родителя так же, как свои.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-inh-sleeper-train", title="Дневные и спальные поезда",
        given=["trains"],
        variants=[{"trains": '["day:10", "sleeper:8", "day:4"]'},
                  {"trains": '["sleeper:12", "sleeper:5"]'},
                  {"trains": '["day:7", "day:3", "sleeper:15", "day:1"]'}],
        hidden=[{"trains": '["day:20"]'},
                {"trains": '["sleeper:1"]'},
                {"trains": '["sleeper:6", "day:6", "sleeper:2"]'}],
        intro="Вокзал отправляет за день несколько поездов. В дневном поезде в каждом вагоне 50 сидячих мест. "
              "Спальный поезд — тоже поезд, но в его вагонах полки вместо кресел, и в каждом вагоне на 20 мест меньше. "
              "В списке `trains` по порядку записаны поезда: тип (`day` или `sleeper`), двоеточие и число вагонов.",
        steps=["Создай класс `Train`. В `__init__(self, wagons)` сохрани число вагонов в `self.wagons`. "
               "Добавь метод `seats(self)`, который возвращает число мест: по 50 на каждый вагон.",
               "Создай класс `SleeperTrain` — наследник `Train`. Свой `__init__` ему не нужен. Добавь только новый метод "
               "`beds(self)`: число мест из унаследованного `self.seats()` минус по 20 мест за каждый вагон.",
               "Пройди по списку `trains`. Каждую запись раздели по двоеточию на тип и число вагонов "
               "(не забудь превратить число в `int`).",
               "Для дневного поезда создай `Train` и выведи строку вида `Train 1: 10 wagons, 500 seats`, "
               "для спального — `SleeperTrain` и строку вида `Train 2: 8 wagons, 240 beds`. Поезда нумеруй по порядку с 1.",
               "Последней строкой выведи `Passengers: …` — сколько всего пассажиров увезут все поезда, если все места "
               "и полки будут заняты."],
        hint="Внутри `beds` не считай места заново — вызови `self.seats()`: спальный поезд тоже поезд, и этот метод "
             "у него уже есть от родителя. Разделить строку `\"day:10\"` по двоеточию можно методом `.split(\":\")`.",
        solution=TRAINS,
        wrong=[("вычитает 20 мест на весь поезд, а не на каждый вагон",
                TRAINS.replace("return self.seats() - 20 * self.wagons", "return self.seats() - 20")),
               ("добавляет в итог для спального поезда сидячие места, а не полки",
                TRAINS.replace("        total += train.beds()", "        total += train.seats()"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("SleeperTrain", "Train"),
                  ("re:self\\.seats\\(\\)",
                   "Внутри `beds` вызови унаследованный метод `self.seats()`, а не считай места заново: "
                   "так формула живёт в одном месте.")],
    ),
]
