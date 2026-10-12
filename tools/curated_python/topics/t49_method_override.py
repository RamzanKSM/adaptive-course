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
print(f"Обычная подписка на {months} мес.: {usual.price(months)} руб.")
print(f"Студенческая подписка на {months} мес.: {student.price(months)} руб.")
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
print(f"{worker.name}: премия {worker.bonus()}, всего {worker.total()} руб.")
print(f"{boss.name}: премия {boss.bonus()}, всего {boss.total()} руб.")
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


archer = Character("Лучник", health)
knight = Knight("Рыцарь", health)
for hit in hits:
    archer.take_damage(hit)
    knight.take_damage(hit)
    print(f"{archer.name}: {archer.health}, {knight.name}: {knight.health}")
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
               "Выведи две строки вида `Обычная подписка на 3 мес.: 897 руб.` и "
               "`Студенческая подписка на 3 мес.: 447 руб.` — цены возьми из методов `price` этих объектов."],
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
        variants=[{"worker_name": '"Ольга"', "worker_salary": "40000", "manager_name": '"Павел"', "manager_salary": "60000"},
                  {"worker_name": '"Дима"', "worker_salary": "35000", "manager_name": '"Ирина"', "manager_salary": "80000"},
                  {"worker_name": '"Катя"', "worker_salary": "52000", "manager_name": '"Сергей"', "manager_salary": "70000"}],
        hidden=[{"worker_name": '"Нина"', "worker_salary": "10000", "manager_name": '"Олег"', "manager_salary": "10000"},
                {"worker_name": '"Тимур"', "worker_salary": "45500", "manager_name": '"Алла"', "manager_salary": "99999"},
                {"worker_name": '"Ян"', "worker_salary": "0", "manager_name": '"Ева"', "manager_salary": "1000"}],
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
               "Для каждого выведи строку вида `Ольга: премия 4000, всего 44000 руб.`"],
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
               "Создай `archer = Character(\"Лучник\", health)` и `knight = Knight(\"Рыцарь\", health)`.",
               "Пройди циклом по списку `hits`: каждый удар получают и лучник, и рыцарь. После каждого удара "
               "выведи строку вида `Лучник: 70, Рыцарь: 85`."],
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
]
