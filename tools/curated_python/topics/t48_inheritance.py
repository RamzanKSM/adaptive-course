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
]
