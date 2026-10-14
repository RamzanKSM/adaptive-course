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
]
