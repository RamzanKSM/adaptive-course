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


TRANSPORT = """\
class Vehicle:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed

    def hours(self, km):
        return km // self.speed


class Bus(Vehicle):
    pass


class Plane(Vehicle):
    def minutes(self, km):
        return km * 60 // self.speed


bus = Bus("Bus", bus_speed)
plane = Plane("Plane", plane_speed)
print(f"{bus.name}: {bus.hours(km)} h")
print(f"{plane.name}: {plane.hours(km)} h")
print(f"{plane.name} in minutes: {plane.minutes(km)}")
"""

STOPWATCH = """\
class Stopwatch:
    def __init__(self):
        self.seconds = 0

    def add(self, seconds):
        self.seconds += seconds

    def show(self):
        print(f"Time: {self.seconds // 60} min {self.seconds % 60} sec")


class TrainerStopwatch(Stopwatch):
    def add_minutes(self, minutes):
        self.add(minutes * 60)


watch = TrainerStopwatch()
watch.add(first)
watch.show()
watch.add_minutes(minutes)
watch.show()
watch.add(second)
watch.show()
"""

PLANS = """\
class Plan:
    def __init__(self, minutes):
        self.minutes = minutes

    def cost(self):
        extra = 0
        if self.minutes > 500:
            extra = (self.minutes - 500) * 2
        return 300 + extra


class FamilyPlan(Plan):
    def per_person(self, people):
        return self.cost() // people


number = 1
total = 0
for line in lines:
    parts = line.split(":")
    if parts[0] == "solo":
        plan = Plan(int(parts[1]))
        print(f"Line {number}: {plan.cost()} rub")
    else:
        plan = FamilyPlan(int(parts[1]))
        print(f"Line {number}: {plan.cost()} rub, {plan.per_person(int(parts[2]))} rub each")
    total += plan.cost()
    number += 1
print(f"Total: {total} rub")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-inh-rt-bus-plane", title="Автобус или самолёт",
        given=["km", "bus_speed", "plane_speed"],
        variants=[{"km": "900", "bus_speed": "75", "plane_speed": "600"},
                  {"km": "1200", "bus_speed": "60", "plane_speed": "480"},
                  {"km": "1600", "bus_speed": "80", "plane_speed": "640"}],
        hidden=[{"km": "300", "bus_speed": "50", "plane_speed": "600"},
                {"km": "2000", "bus_speed": "100", "plane_speed": "500"},
                {"km": "720", "bus_speed": "90", "plane_speed": "720"}],
        intro="Ты выбираешь, как добраться до города в `km` км: на автобусе или на самолёте. И автобус, и самолёт — "
              "транспорт: у каждого есть название и скорость в км/ч, и время в пути в полных часах считают одинаково. "
              "А вот для самолёта хочется знать ещё и точное число минут.",
        steps=["Создай класс `Vehicle`. В `__init__(self, name, speed)` сохрани название и скорость в атрибуты "
               "`self.name` и `self.speed`.",
               "Добавь в `Vehicle` метод `hours(self, km)`, который возвращает полные часы в пути: `km`, делённое "
               "нацело на скорость.",
               "Создай класс `Bus` — наследник `Vehicle`. Внутри напиши только `pass`.",
               "Создай класс `Plane` — тоже наследник `Vehicle`. Добавь в него один новый метод `minutes(self, km)`: "
               "время в пути в минутах — `km`, умноженное на 60 и делённое нацело на скорость.",
               "Создай `bus = Bus(\"Bus\", bus_speed)` и `plane = Plane(\"Plane\", plane_speed)`. Выведи три строки "
               "вида `Bus: 12 h`, `Plane: 1 h` и `Plane in minutes: 90` — часы автобуса, часы самолёта и минуты самолёта."],
        hint="Запись `class Plane(Vehicle):` значит «самолёт — это транспорт»: объект `Plane` сразу получает `__init__` "
             "и `hours` из класса `Vehicle`, хотя в самом `Plane` их нет. В наследнике пишут только то, чего нет у родителя.",
        solution=TRANSPORT,
        wrong=[("создаёт самолёт со скоростью автобуса — скопировал строку и не поправил",
                TRANSPORT.replace('Plane("Plane", plane_speed)', 'Plane("Plane", bus_speed)')),
               ("в minutes сначала делит, потом умножает на 60 — минуты кратны часу",
                TRANSPORT.replace("return km * 60 // self.speed", "return km // self.speed * 60"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("Bus", "Vehicle"), child_of("Plane", "Vehicle"), written_once("hours", "Vehicle")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-inh-rt-trainer-stopwatch", title="Секундомер тренера",
        given=["first", "minutes", "second"],
        variants=[{"first": "45", "minutes": "2", "second": "80"},
                  {"first": "130", "minutes": "5", "second": "15"},
                  {"first": "59", "minutes": "1", "second": "1"}],
        hidden=[{"first": "0", "minutes": "0", "second": "0"},
                {"first": "600", "minutes": "10", "second": "61"},
                {"first": "12", "minutes": "3", "second": "48"}],
        intro="Обычный секундомер умеет добавлять секунды и показывать время. Тренеру нужен секундомер, "
              "который умеет всё то же самое, но ещё может добавить сразу целые минуты. Сначала тренер добавил `first` "
              "секунд, потом `minutes` минут, потом ещё `second` секунд.",
        steps=["Создай класс `Stopwatch`. В `__init__(self)` задай `self.seconds = 0`.",
               "Добавь в `Stopwatch` метод `add(self, seconds)`, который прибавляет секунды, и метод `show(self)`, "
               "который печатает строку вида `Time: 2 min 5 sec` — полные минуты и оставшиеся секунды.",
               "Создай класс `TrainerStopwatch` — наследник `Stopwatch`. Напиши в нём только один новый метод "
               "`add_minutes(self, minutes)`: он переводит минуты в секунды и добавляет их через унаследованный "
               "метод `self.add(...)`.",
               "Создай `watch = TrainerStopwatch()`. Затем по очереди: добавь `first` секунд через `add` и выведи время "
               "через `show()`, добавь `minutes` минут через `add_minutes` и выведи время, добавь `second` секунд "
               "и выведи время в последний раз."],
        hint="Внутри метода наследника можно вызывать методы родителя через `self` — так же, как свои: `self.add(...)`. "
             "В минуте 60 секунд. Полные минуты даёт `// 60`, а оставшиеся секунды — `% 60`.",
        solution=STOPWATCH,
        wrong=[("add_minutes записывает время заново вместо добавления — прежние секунды теряются",
                STOPWATCH.replace("        self.add(minutes * 60)", "        self.seconds = minutes * 60")),
               ("забыл перевести минуты в секунды",
                STOPWATCH.replace("self.add(minutes * 60)", "self.add(minutes)"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("TrainerStopwatch", "Stopwatch"), written_once("add", "Stopwatch"),
                  ("re:self\\.add\\(",
                   "Добавляй минуты через унаследованный метод `self.add(...)`: наследник может вызывать "
                   "методы родителя так же, как свои.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-inh-rt-phone-plans", title="Обычный и семейный тариф",
        given=["lines"],
        variants=[{"lines": '["solo:650", "family:900:3", "solo:200"]'},
                  {"lines": '["family:500:2", "solo:501"]'},
                  {"lines": '["solo:1000", "family:300:4", "family:750:5", "solo:500"]'}],
        hidden=[{"lines": '["solo:0"]'},
                {"lines": '["family:501:1", "family:1200:3"]'},
                {"lines": '["solo:499", "solo:500", "solo:501", "family:2000:7"]'}],
        intro="Оператор связи считает счета за месяц. Любой тариф стоит 300 руб., в него входит 500 минут, а каждая "
              "минута сверх них стоит 2 руб. Семейный тариф — тоже тариф и считается так же, но его делят на несколько "
              "человек. В списке `lines` — номера по порядку: `solo:` и число минут или `family:`, число минут, "
              "двоеточие и сколько человек делят счёт.",
        steps=["Создай класс `Plan`. В `__init__(self, minutes)` сохрани минуты в `self.minutes`. Добавь метод "
               "`cost(self)`: 300 руб. плюс по 2 руб. за каждую минуту сверх 500.",
               "Создай класс `FamilyPlan` — наследник `Plan`. Свой `__init__` ему не нужен. Добавь только новый метод "
               "`per_person(self, people)`: стоимость из унаследованного `self.cost()`, делённая нацело на `people`.",
               "Пройди по списку `lines` и раздели каждую запись по двоеточию (числа превращай в `int`). "
               "Для `solo` создай `Plan` и выведи строку вида `Line 1: 600 rub`, для `family` — `FamilyPlan` "
               "и строку вида `Line 2: 1100 rub, 366 rub each`. Номера нумеруй по порядку с 1.",
               "Последней строкой выведи строку вида `Total: 2000 rub` — сумму счетов всех номеров."],
        hint="Не считай стоимость в `per_person` заново — вызови `self.cost()`: семейный тариф тоже тариф, и этот метод "
             "у него уже есть от родителя. Минуты сверх пакета — это `self.minutes - 500`, но только если минут больше 500. "
             "Разделить строку `\"family:900:3\"` по двоеточию можно методом `.split(\":\")`.",
        solution=PLANS,
        wrong=[("делит обычным делением — доля получается дробной",
                PLANS.replace("return self.cost() // people", "return self.cost() / people")),
               ("при превышении берёт по 2 руб. за все минуты, а не только за лишние",
                PLANS.replace("extra = (self.minutes - 500) * 2", "extra = self.minutes * 2"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("FamilyPlan", "Plan"), written_once("cost", "Plan"),
                  ("re:self\\.cost\\(\\s*\\)",
                   "Внутри `per_person` вызови унаследованный метод `self.cost()`, а не считай стоимость заново: "
                   "так формула живёт в одном месте.")],
    ),
]
