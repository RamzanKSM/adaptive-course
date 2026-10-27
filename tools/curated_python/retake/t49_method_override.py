"""PY_METHOD_OVERRIDE — «Переопределение методов». Taught before: everything up to classes, __init__, self and methods,
«private» attributes, @property, class attributes, inheritance. Here: a child writes its own method with the same name
as the parent's; the child's version runs for child objects, the parent's for parent objects; a parent method that
calls self.method() uses the child's version. Not yet: super() (later topic), tuples, dicts."""
from build import OutputTask

SKILL = "PY_METHOD_OVERRIDE"

NEED_CLASS = ("ClassDef", "Опиши объекты в собственных классах через class.")


def child_of(child: str, parent: str) -> tuple[str, str]:
    return (f"re:class\\s+{child}\\s*\\(\\s*{parent}\\s*\\)",
            f"Сделай класс `{child}` наследником `{parent}`: напиши `class {child}({parent}):`.")


def overridden(method: str, child: str) -> tuple[str, str]:
    return (f"re:def\\s+{method}\\s*\\([\\s\\S]*def\\s+{method}\\s*\\(",
            f"Переопредели метод: напиши в классе `{child}` свой метод `{method}` — с тем же именем и теми же "
            f"параметрами, что у родителя. Тогда для объектов `{child}` будет работать новая версия.")


GREETER = """\
class Greeter:
    def greet(self, name):
        return f"Hi, {name}!"


class FormalGreeter(Greeter):
    def greet(self, name):
        return f"Good afternoon, {name}."


friend = Greeter()
office = FormalGreeter()
print(friend.greet(name))
print(office.greet(name))
"""

CART = """\
class Cart:
    def __init__(self, prices):
        self.prices = prices

    def discount(self, total):
        return 0

    def pay(self):
        total = 0
        for price in self.prices:
            total += price
        return total - self.discount(total)


class ClubCart(Cart):
    def discount(self, total):
        if total >= 1000:
            return total // 10
        return 0


usual = Cart(prices)
club = ClubCart(prices)
print(f"Regular: {usual.pay()} rub")
print(f"Club card: {club.pay()} rub")
"""

PIGGY = """\
class PiggyBank:
    def __init__(self):
        self.total = 0

    def put(self, amount):
        if amount > 0:
            self.total += amount


class GoldPiggyBank(PiggyBank):
    def put(self, amount):
        if amount >= 50:
            self.total += amount + amount // 10


basic = PiggyBank()
gold = GoldPiggyBank()
for amount in amounts:
    basic.put(amount)
    gold.put(amount)
    print(f"Basic: {basic.total}, gold: {gold.total}")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ovr-rt-greeter", title="Приветствие от бота",
        given=["name"],
        variants=[{"name": '"Anna"'}, {"name": '"Timur"'}, {"name": '"Vera"'}],
        hidden=[{"name": '"Oleg"'}, {"name": '"Zarina"'}, {"name": '"Yan"'}],
        intro="Чат-бот здоровается с пользователями. В чате друзей он пишет просто, а в рабочем чате — вежливо. "
              "Вежливый бот — это тот же бот, только здоровается по-другому. Пользователя зовут `name`.",
        steps=["Создай класс `Greeter` с методом `greet(self, name)`, который возвращает строку вида `Hi, Anna!`",
               "Создай класс `FormalGreeter` — наследник `Greeter`. Переопредели в нём метод `greet(self, name)`: "
               "он возвращает строку вида `Good afternoon, Anna.` — с точкой в конце.",
               "Создай объекты `friend = Greeter()` и `office = FormalGreeter()`.",
               "Выведи две строки: результат `friend.greet(name)` и результат `office.greet(name)`."],
        hint="Переопределить метод — значит написать в наследнике метод с точно таким же именем. "
             "Когда ты вызываешь `office.greet(...)`, Python сначала ищет `greet` в классе `FormalGreeter` "
             "и, найдя его там, до версии родителя уже не доходит.",
        solution=GREETER,
        wrong=[("опечатка в имени метода наследника — срабатывает приветствие родителя",
                GREETER.replace("class FormalGreeter(Greeter):\n    def greet(", "class FormalGreeter(Greeter):\n    def great(")),
               ("создаёт вежливого бота из класса-родителя — новое приветствие не работает",
                GREETER.replace("office = FormalGreeter()", "office = Greeter()"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("FormalGreeter", "Greeter"), overridden("greet", "FormalGreeter")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ovr-rt-club-cart", title="Скидка по клубной карте",
        given=["prices"],
        variants=[{"prices": "[450, 300, 450]"}, {"prices": "[120, 80, 250]"}, {"prices": "[999, 1]"}],
        hidden=[{"prices": "[999]"}, {"prices": "[600, 400]"}, {"prices": "[2500, 700, 35]"}, {"prices": "[]"}, {"prices": "[500, 499]"}],
        intro="В магазине одни и те же покупки можно оплатить обычной картой или клубной. Итог считается одинаково: "
              "сумма покупок минус скидка. Обычная карта скидки не даёт, а клубная даёт 10 %, если покупок "
              "на 1000 руб. или больше. Значит, в клубной корзине нужно поменять только расчёт скидки. "
              "Цены покупок — в списке `prices`.",
        steps=["Создай класс `Cart`. В `__init__(self, prices)` сохрани список цен в `self.prices`.",
               "Добавь в `Cart` метод `discount(self, total)`, который возвращает скидку `0`, и метод `pay(self)`, "
               "который складывает все цены из `self.prices` и возвращает сумму минус скидку. Скидку в `pay` получай "
               "вызовом `self.discount(...)` с суммой покупок.",
               "Создай класс `ClubCart` — наследник `Cart` — и переопредели в нём только метод `discount(self, total)`: "
               "если `total` не меньше 1000, скидка — `total`, делённое нацело на 10, иначе `0`. Метод `pay` в `ClubCart` "
               "не пиши.",
               "Создай `usual = Cart(prices)` и `club = ClubCart(prices)` и выведи две строки вида "
               "`Regular: 1200 rub` и `Club card: 1080 rub` — с результатами `pay()`."],
        hint="Метод `pay` написан один раз, в родителе. Но когда его вызывают для клубной корзины, `self` — это "
             "`ClubCart`, и `self.discount(...)` найдёт её версию скидки. Ровно 1000 руб. — скидка уже есть.",
        solution=CART,
        wrong=[("считает скидку в pay вручную, без self.discount — у клубной карты скидки нет",
                CART.replace("        return total - self.discount(total)", "        return total - 0")),
               ("строгое сравнение — при покупках ровно на 1000 руб. скидки нет",
                CART.replace("if total >= 1000:", "if total > 1000:"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("ClubCart", "Cart"), overridden("discount", "ClubCart"),
                  ("re:self\\.discount\\(",
                   "В методе `pay` получай скидку вызовом `self.discount(...)`: тогда у клубной корзины сработает "
                   "её собственная версия.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ovr-rt-gold-piggy", title="Золотая копилка",
        given=["amounts"],
        variants=[{"amounts": "[100, 30, -20, 200]"}, {"amounts": "[50, 49, 500]"}, {"amounts": "[0, 70, 10, 150]"}],
        hidden=[{"amounts": "[]"}, {"amounts": "[49]"}, {"amounts": "[50, 50, -50, 1000]"}, {"amounts": "[5, 6, 7]"}],
        intro="У брата обычная копилка, у сестры — золотая. Они договорились класть в них одинаковые суммы из списка "
              "`amounts`. Обычная копилка принимает любую сумму больше нуля. Золотая — та же копилка, но принимает "
              "только суммы от 50 руб. и сверху добавляет к каждой бонус — её десятую часть.",
        steps=["Создай класс `PiggyBank`. В `__init__(self)` задай `self.total = 0`. Добавь метод `put(self, amount)`: "
               "если `amount` больше нуля, он прибавляет его к `self.total`, иначе ничего не делает.",
               "Создай класс `GoldPiggyBank` — наследник `PiggyBank` — и переопредели в нём `put(self, amount)`: "
               "если `amount` не меньше 50, к `self.total` прибавляется `amount` и ещё бонус `amount // 10`, "
               "иначе ничего не происходит.",
               "Создай `basic = PiggyBank()` и `gold = GoldPiggyBank()`.",
               "Пройди циклом по списку `amounts`: каждую сумму положи и в обычную, и в золотую копилку. После каждой "
               "суммы выведи строку вида `Basic: 130, gold: 110`."],
        hint="`__init__` золотой копилке писать не нужно — он достанется от родителя. А вот `put` пишется заново целиком: "
             "проверка у золотой копилки своя (`amount >= 50`), и бонус считается от самой суммы. Ровно 50 руб. "
             "золотая копилка уже принимает.",
        solution=PIGGY,
        wrong=[("в золотой копилке забыл бонус — она ничем не лучше обычной, только строже",
                PIGGY.replace("self.total += amount + amount // 10", "self.total += amount")),
               ("строгое сравнение — золотая копилка не принимает ровно 50 руб.",
                PIGGY.replace("if amount >= 50:", "if amount > 50:"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("GoldPiggyBank", "PiggyBank"), overridden("put", "GoldPiggyBank")],
    ),
]
