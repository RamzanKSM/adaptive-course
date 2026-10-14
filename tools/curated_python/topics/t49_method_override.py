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


SUBSCRIPTION = """\
class Subscription:
    def price(self, months):
        return 299 * months


class StudentSubscription(Subscription):
    def price(self, months):
        return 149 * months


usual = Subscription()
student = StudentSubscription()
print(f"Regular plan for {months} months: {usual.price(months)} rub")
print(f"Student plan for {months} months: {student.price(months)} rub")
"""

BONUS = """\
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def bonus(self):
        return self.salary // 10

    def total(self):
        return self.salary + self.bonus()


class Manager(Employee):
    def bonus(self):
        return self.salary // 4


worker = Employee(worker_name, worker_salary)
boss = Manager(manager_name, manager_salary)
print(f"{worker.name}: bonus {worker.bonus()}, total {worker.total()} rub")
print(f"{boss.name}: bonus {boss.bonus()}, total {boss.total()} rub")
"""

KNIGHT = """\
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0


class Knight(Character):
    def take_damage(self, amount):
        self.health -= amount // 2
        if self.health < 0:
            self.health = 0


archer = Character("Archer", health)
knight = Knight("Knight", health)
for hit in hits:
    archer.take_damage(hit)
    knight.take_damage(hit)
    print(f"{archer.name}: {archer.health}, {knight.name}: {knight.health}")
"""


DELIVERY = """\
class Delivery:
    def days(self, km):
        return km // 300 + 2


class ExpressDelivery(Delivery):
    def days(self, km):
        return km // 1000 + 1


usual = Delivery()
express = ExpressDelivery()
print(f"Regular delivery for {km} km, days: {usual.days(km)}")
print(f"Express delivery for {km} km, days: {express.days(km)}")
"""

SENSORS = """\
class Sensor:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def unit(self):
        return "C"

    def report(self):
        return f"{self.name}: {self.value} {self.unit()}"


class HumiditySensor(Sensor):
    def unit(self):
        return "%"


class WindSensor(Sensor):
    def unit(self):
        return "m/s"


print(Sensor("Temperature", temp).report())
print(HumiditySensor("Humidity", humidity).report())
print(WindSensor("Wind", wind).report())
"""

CREDIT = """\
class Account:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount


class CreditAccount(Account):
    def withdraw(self, amount):
        if self.balance - amount >= -1000:
            self.balance -= amount


debit = Account(start)
credit = CreditAccount(start)
for amount in amounts:
    debit.withdraw(amount)
    credit.withdraw(amount)
    print(f"Debit: {debit.balance}, credit: {credit.balance}")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ovr-music-subscription", title="Студенческая подписка",
        given=["months"],
        variants=[{"months": "3"}, {"months": "12"}, {"months": "6"}],
        hidden=[{"months": "1"}, {"months": "24"}, {"months": "2"}],
        intro="Музыкальный сервис продаёт подписку по 299 руб. в месяц, а для студентов — по 149 руб. "
              "Студенческая подписка — это та же подписка, только цена считается по-другому. "
              "Покупатель хочет сравнить цены на `months` месяцев.",
        steps=["Создай класс `Subscription` с методом `price(self, months)`, который возвращает цену подписки "
               "на `months` месяцев: 299 руб. за каждый месяц.",
               "Создай класс `StudentSubscription` — наследник `Subscription`. Переопредели в нём метод "
               "`price(self, months)`: студенческая подписка стоит 149 руб. за месяц.",
               "Создай объекты `usual = Subscription()` и `student = StudentSubscription()`.",
               "Выведи две строки вида `Regular plan for 3 months: 897 rub` и "
               "`Student plan for 3 months: 447 rub` — цены возьми из методов `price` этих объектов."],
        hint="Переопределить метод — значит написать в наследнике метод с точно таким же именем. "
             "Когда ты вызываешь `student.price(...)`, Python сначала ищет `price` в классе `StudentSubscription` "
             "и, найдя его там, до версии родителя уже не доходит.",
        solution=SUBSCRIPTION,
        wrong=[("опечатка в имени метода наследника — срабатывает цена родителя",
                SUBSCRIPTION.replace("class StudentSubscription(Subscription):\n    def price(",
                                     "class StudentSubscription(Subscription):\n    def prise(")),
               ("создаёт студенческую подписку из класса-родителя — новая цена не работает",
                SUBSCRIPTION.replace("student = StudentSubscription()", "student = Subscription()"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("StudentSubscription", "Subscription"),
                  overridden("price", "StudentSubscription")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ovr-manager-bonus", title="Премия менеджера",
        given=["worker_name", "worker_salary", "manager_name", "manager_salary"],
        variants=[{"worker_name": '"Olga"', "worker_salary": "40000", "manager_name": '"Pavel"', "manager_salary": "60000"},
                  {"worker_name": '"Dima"', "worker_salary": "35000", "manager_name": '"Irina"', "manager_salary": "80000"},
                  {"worker_name": '"Katya"', "worker_salary": "52000", "manager_name": '"Sergey"', "manager_salary": "70000"}],
        hidden=[{"worker_name": '"Nina"', "worker_salary": "10000", "manager_name": '"Oleg"', "manager_salary": "10000"},
                {"worker_name": '"Timur"', "worker_salary": "45500", "manager_name": '"Alla"', "manager_salary": "99999"},
                {"worker_name": '"Yan"', "worker_salary": "0", "manager_name": '"Eva"', "manager_salary": "1000"}],
        intro="В конце года каждый сотрудник получает премию: обычный сотрудник — десятую часть зарплаты, "
              "а менеджер — четверть. Выплата считается одинаково для всех: зарплата плюс премия. "
              "Значит, в классе менеджера нужно поменять только расчёт премии.",
        steps=["Создай класс `Employee`. В `__init__(self, name, salary)` сохрани имя и зарплату "
               "в атрибуты `self.name` и `self.salary`.",
               "Добавь в `Employee` метод `bonus(self)`, который возвращает премию — зарплату, целочисленно "
               "делённую на 10, и метод `total(self)`, который возвращает зарплату плюс премию. Премию в `total` "
               "получай вызовом `self.bonus()`.",
               "Создай класс `Manager` — наследник `Employee` — и переопредели в нём только метод `bonus(self)`: "
               "премия менеджера — зарплата, целочисленно делённая на 4. Метод `total` в `Manager` не пиши.",
               "Создай `worker = Employee(worker_name, worker_salary)` и `boss = Manager(manager_name, manager_salary)`. "
               "Для каждого выведи строку вида `Olga: bonus 4000, total 44000 rub`"],
        hint="Метод `total` написан один раз в `Employee`, но вызывает `self.bonus()`. Когда `total` работает "
             "для менеджера, `self` — это менеджер, и Python возьмёт его версию `bonus`. Поэтому важно не "
             "считать премию в `total` вручную, а вызывать метод.",
        solution=BONUS,
        wrong=[("опечатка в имени переопределённого метода — менеджер получает премию как обычный сотрудник",
                BONUS.replace("class Manager(Employee):\n    def bonus(", "class Manager(Employee):\n    def bonuss(")),
               ("в total премия посчитана вручную, а не через self.bonus() — итог менеджера считается по старой формуле",
                BONUS.replace("return self.salary + self.bonus()", "return self.salary + self.salary // 10"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("Manager", "Employee"), overridden("bonus", "Manager"),
                  ("re:self\\.bonus\\(\\)",
                   "В методе `total` получай премию вызовом `self.bonus()`: тогда у менеджера сработает "
                   "его собственная версия премии.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ovr-knight-armor", title="Броня рыцаря",
        given=["health", "hits"],
        variants=[{"health": "100", "hits": "[30, 25, 60]"},
                  {"health": "60", "hits": "[50, 70, 40]"},
                  {"health": "120", "hits": "[40, 15, 90, 20]"}],
        hidden=[{"health": "50", "hits": "[60, 60, 20]"},
                {"health": "200", "hits": "[10]"},
                {"health": "30", "hits": "[7, 7, 7, 7]"}],
        intro="В игре лучник и рыцарь вместе отбиваются от дракона. У обоих в начале `health` очков здоровья, "
              "и удары дракона из списка `hits` достаются обоим. Но рыцарь в броне: она забирает себе половину удара.",
        steps=["Создай класс `Character`. В `__init__(self, name, health)` сохрани имя и здоровье. Добавь метод "
               "`take_damage(self, amount)`: он уменьшает здоровье на `amount`, но так, чтобы оно не стало меньше 0 — "
               "если получилось отрицательное число, здоровье становится 0.",
               "Создай класс `Knight` — наследник `Character` — и переопредели в нём `take_damage(self, amount)`: "
               "рыцарь теряет только `amount // 2` здоровья, и его здоровье тоже не бывает меньше 0.",
               "Создай `archer = Character(\"Archer\", health)` и `knight = Knight(\"Knight\", health)`.",
               "Пройди циклом по списку `hits`: каждый удар получают и лучник, и рыцарь. После каждого удара "
               "выведи строку вида `Archer: 70, Knight: 85`."],
        hint="Переопределённый метод полностью заменяет метод родителя, поэтому в версии `Knight` проверку "
             "«не меньше нуля» нужно написать заново — сама она из `Character` не перейдёт.",
        solution=KNIGHT,
        wrong=[("опечатка в имени метода рыцаря — броня не работает, рыцарь получает полный урон",
                KNIGHT.replace("class Knight(Character):\n    def take_damage(", "class Knight(Character):\n    def take_damag(")),
               ("в методе рыцаря забыта проверка — здоровье рыцаря уходит в минус",
                KNIGHT.replace("        self.health -= amount // 2\n        if self.health < 0:\n            self.health = 0\n",
                               "        self.health -= amount // 2\n"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("Knight", "Character"), overridden("take_damage", "Knight")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ovr-express-delivery", title="Экспресс-доставка",
        given=["km"],
        variants=[{"km": "900"}, {"km": "2500"}, {"km": "450"}],
        hidden=[{"km": "100"}, {"km": "1000"}, {"km": "6100"}],
        intro="Интернет-магазин отправляет заказы обычной и экспресс-доставкой. Обычная доставка идёт "
              "`km // 300 + 2` дней, экспресс-доставка — `km // 1000 + 1` дней. Экспресс — это та же доставка, "
              "только срок считается по-другому. Покупатель живёт в `km` километрах от склада.",
        steps=["Создай класс `Delivery` с методом `days(self, km)`, который возвращает срок обычной доставки: "
               "`km // 300 + 2` дней.",
               "Создай класс `ExpressDelivery` — наследник `Delivery`. Переопредели в нём метод `days(self, km)`: "
               "срок экспресс-доставки — `km // 1000 + 1` дней.",
               "Создай объекты `usual = Delivery()` и `express = ExpressDelivery()`.",
               "Выведи две строки вида `Regular delivery for 900 km, days: 5` и "
               "`Express delivery for 900 km, days: 1` — сроки возьми из методов `days` этих объектов."],
        hint="Переопределить метод — значит написать в наследнике метод с точно таким же именем. "
             "Вызов `express.days(km)` найдёт `days` в классе `ExpressDelivery` и до версии родителя не дойдёт.",
        solution=DELIVERY,
        wrong=[("опечатка в имени метода наследника — экспресс считается как обычная доставка",
                DELIVERY.replace("class ExpressDelivery(Delivery):\n    def days(",
                                 "class ExpressDelivery(Delivery):\n    def day(")),
               ("создаёт экспресс-доставку из класса-родителя — новый срок не работает",
                DELIVERY.replace("express = ExpressDelivery()", "express = Delivery()"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("ExpressDelivery", "Delivery"), overridden("days", "ExpressDelivery")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ovr-weather-sensors", title="Датчики метеостанции",
        given=["temp", "humidity", "wind"],
        variants=[{"temp": "18", "humidity": "65", "wind": "4"},
                  {"temp": "-7", "humidity": "80", "wind": "12"},
                  {"temp": "25", "humidity": "40", "wind": "1"}],
        hidden=[{"temp": "0", "humidity": "100", "wind": "0"},
                {"temp": "31", "humidity": "22", "wind": "9"},
                {"temp": "-25", "humidity": "55", "wind": "17"}],
        intro="На метеостанции три датчика: температуры, влажности и ветра. Каждый датчик выдаёт отчёт одинакового "
              "вида — название, значение и единица измерения. Отличается только единица: градусы `C`, проценты `%` "
              "или метры в секунду `m/s`. Показания датчиков — `temp`, `humidity` и `wind`.",
        steps=["Создай класс `Sensor`. В `__init__(self, name, value)` сохрани название и значение "
               "в атрибуты `self.name` и `self.value`.",
               "Добавь в `Sensor` метод `unit(self)`, который возвращает строку `C`, и метод `report(self)`, который "
               "возвращает строку вида `Temperature: 18 C`. Единицу измерения в `report` получай вызовом `self.unit()`.",
               "Создай наследников `Sensor`: `HumiditySensor`, где `unit` переопределён и возвращает `%`, и `WindSensor`, "
               "где `unit` возвращает `m/s`. Метод `report` в наследниках не пиши.",
               "Выведи три строки — результат `report()` для `Sensor(\"Temperature\", temp)`, "
               "`HumiditySensor(\"Humidity\", humidity)` и `WindSensor(\"Wind\", wind)`, например "
               "`Temperature: 18 C`, `Humidity: 65 %` и `Wind: 4 m/s`."],
        hint="Метод `report` написан один раз в `Sensor`, но вызывает `self.unit()`. Когда `report` работает для "
             "датчика ветра, `self` — это `WindSensor`, и Python возьмёт его версию `unit`. Если вписать `C` "
             "в `report` прямо в строку, переопределение не сработает.",
        solution=SENSORS,
        wrong=[("в report единица вписана прямо в строку, а не через self.unit() — у всех датчиков градусы",
                SENSORS.replace('{self.value} {self.unit()}', '{self.value} C')),
               ("опечатка в имени метода датчика ветра — ветер измеряется в градусах",
                SENSORS.replace("class WindSensor(Sensor):\n    def unit(", "class WindSensor(Sensor):\n    def units("))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("HumiditySensor", "Sensor"), child_of("WindSensor", "Sensor"),
                  overridden("unit", "HumiditySensor"),
                  ("re:self\\.unit\\(\\)",
                   "В методе `report` получай единицу вызовом `self.unit()`: тогда у каждого датчика сработает "
                   "его собственная версия.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ovr-credit-account", title="Дебетовая и кредитная карта",
        given=["start", "amounts"],
        variants=[{"start": "1000", "amounts": "[400, 900, 500]"},
                  {"start": "300", "amounts": "[300, 1000, 1]"},
                  {"start": "2000", "amounts": "[1500, 700, 800, 100]"}],
        hidden=[{"start": "0", "amounts": "[1000, 1]"},
                {"start": "500", "amounts": "[1501, 1500]"},
                {"start": "100", "amounts": "[50, 50, 50]"},
                {"start": "5000", "amounts": "[10]"}],
        intro="У клиента банка две карты, и на каждой лежит по `start` рублей. С дебетовой карты нельзя снять больше, "
              "чем на ней есть. Кредитная карта — та же карта, но банк разрешает уходить в минус до 1000 руб. "
              "Клиент по очереди пытается снять с обеих карт суммы из списка `amounts`; если снять нельзя, "
              "операция не проходит и баланс не меняется.",
        steps=["Создай класс `Account`. В `__init__(self, balance)` сохрани баланс в `self.balance`. Добавь метод "
               "`withdraw(self, amount)`: если `amount` не больше баланса, он уменьшает баланс на `amount`, "
               "иначе ничего не делает.",
               "Создай класс `CreditAccount` — наследник `Account` — и переопредели в нём `withdraw(self, amount)`: "
               "снятие проходит, если после него баланс будет не меньше -1000.",
               "Создай `debit = Account(start)` и `credit = CreditAccount(start)`.",
               "Пройди циклом по списку `amounts`: каждую сумму пытайся снять и с дебетовой, и с кредитной карты. "
               "После каждой суммы выведи строку вида `Debit: 600, credit: 600`."],
        hint="Переопределённый метод полностью заменяет метод родителя, поэтому проверку в `CreditAccount` пиши "
             "свою: `self.balance - amount >= -1000`. Уйти ровно в -1000 можно, а дальше — уже нет. "
             "Снять с дебетовой карты ровно весь баланс тоже можно.",
        solution=CREDIT,
        wrong=[("опечатка в имени метода кредитной карты — она ведёт себя как дебетовая",
                CREDIT.replace("class CreditAccount(Account):\n    def withdraw(", "class CreditAccount(Account):\n    def withdrow(")),
               ("строгое сравнение у кредитной карты — уйти ровно в -1000 нельзя",
                CREDIT.replace("self.balance - amount >= -1000", "self.balance - amount > -1000")),
               ("у дебетовой карты строгое сравнение — снять ровно весь баланс нельзя",
                CREDIT.replace("if amount <= self.balance:", "if amount < self.balance:"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("CreditAccount", "Account"), overridden("withdraw", "CreditAccount")],
    ),
]
