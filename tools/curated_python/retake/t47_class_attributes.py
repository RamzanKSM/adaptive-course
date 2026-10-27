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


EXAM = """\
class Exam:
    max_points = 40

    def __init__(self, student, points):
        self.student = student
        self.points = points

    def percent(self):
        return self.points * 100 // Exam.max_points


first = Exam(student1, points1)
second = Exam(student2, points2)
print(f"Max points: {Exam.max_points}")
print(f"{first.student}: {first.points} of {Exam.max_points}, {first.percent()}%")
print(f"{second.student}: {second.points} of {Exam.max_points}, {second.percent()}%")
"""

BOX = """\
class Box:
    limit = 100
    loaded = 0

    def __init__(self, weight):
        self.weight = weight
        if Box.loaded + weight <= Box.limit:
            Box.loaded += weight
            self.status = "loaded"
        else:
            self.status = "does not fit"


number = 1
for weight in weights:
    box = Box(weight)
    print(f"Box {number}: {box.weight} kg, {box.status}")
    number += 1
print(f"Truck load: {Box.loaded} of {Box.limit} kg")
"""

SENSOR = """\
class Sensor:
    level = 50
    sensors = []

    def __init__(self, room, value):
        self.room = room
        self.value = value
        Sensor.sensors.append(self)

    def alarm(self):
        return self.value > Sensor.level


def show_alarms():
    rooms_on = []
    for sensor in Sensor.sensors:
        if sensor.alarm():
            rooms_on.append(sensor.room)
    if rooms_on:
        print(f"Level {Sensor.level}: {', '.join(rooms_on)}")
    else:
        print(f"Level {Sensor.level}: none")


for i in range(len(rooms)):
    Sensor(rooms[i], values[i])
print(f"Sensors: {len(Sensor.sensors)}")
show_alarms()
Sensor.level = new_level
show_alarms()
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-clsattr-rt-exam-max", title="Баллы за экзамен",
        given=["student1", "points1", "student2", "points2"],
        variants=[{"student1": '"Anya"', "points1": "30", "student2": '"Boris"', "points2": "36"},
                  {"student1": '"Vika"', "points1": "12", "student2": '"Gleb"', "points2": "40"},
                  {"student1": '"Dina"', "points1": "25", "student2": '"Egor"', "points2": "18"}],
        hidden=[{"student1": '"Ira"', "points1": "0", "student2": '"Kostya"', "points2": "20"},
                {"student1": '"Lena"', "points1": "33", "student2": '"Misha"', "points2": "33"},
                {"student1": '"Nina"', "points1": "39", "student2": '"Oleg"', "points2": "4"}],
        intro="На экзамене по информатике у всех один и тот же максимум — 40 баллов. Это общее правило для всех "
              "работ, поэтому его удобно записать один раз — в самом классе. А имя ученика и его баллы у каждой "
              "работы свои. Сегодня `student1` набрал `points1` баллов, а `student2` — `points2`.",
        steps=["Создай класс `Exam`. Прямо в теле класса, а не в `__init__`, запиши атрибут класса `max_points = 40`.",
               "В `__init__(self, student, points)` сохрани имя и баллы в атрибуты `self.student` и `self.points`.",
               "Добавь метод `percent(self)`, который возвращает процент: баллы, умноженные на 100 и делённые нацело "
               "на `Exam.max_points`.",
               "Создай две работы: `first = Exam(student1, points1)` и `second = Exam(student2, points2)`.",
               "Выведи строку `Max points: 40` — число возьми из `Exam.max_points`. Потом по строке для каждой работы "
               "в виде `Anya: 30 of 40, 75%`"],
        hint="Атрибут класса записывается в теле класса без `self` и читается через имя класса: `Exam.max_points`. "
             "Он один на все работы, а вот баллы у каждой работы свои — их бери из `self.points`. "
             "Умножай на 100 до деления, иначе получится 0.",
        solution=EXAM,
        wrong=[("берёт в методе переменную points1 из заготовки вместо self.points — у обеих работ одинаковый процент",
                EXAM.replace("self.points * 100", "points1 * 100")),
               ("сначала делит, потом умножает на 100 — процент почти всегда 0",
                EXAM.replace("self.points * 100 // Exam.max_points", "self.points // Exam.max_points * 100"))],
        constructs=["class"],
        must_use=[NEED_CLASS, class_level("max_points", "max_points = 40", "Exam",
                                          "Тогда максимум будет один на все работы.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-clsattr-rt-truck-load", title="Погрузка в грузовик",
        given=["weights"],
        variants=[{"weights": "[30, 50, 40, 20]"}, {"weights": "[60, 45, 30]"}, {"weights": "[10, 95, 25, 50, 20]"}],
        hidden=[{"weights": "[100]"}, {"weights": "[101, 99, 1]"}, {"weights": "[]"}, {"weights": "[20, 20, 20, 20, 20, 20]"}],
        intro="На склад привезли коробки, и их по очереди грузят в один грузовик, который выдерживает 100 кг. "
              "Если очередная коробка уже не помещается по весу, её откладывают. Предел и общий вес груза — "
              "общие для всех коробок, поэтому это атрибуты класса. Веса коробок по порядку — в списке `weights`.",
        steps=["Создай класс `Box` с двумя атрибутами класса: `limit = 100` и `loaded = 0` — сколько килограммов "
               "уже в грузовике.",
               "В `__init__(self, weight)` сохрани вес в `self.weight`. Если `Box.loaded` вместе с этим весом не больше "
               "`Box.limit`, прибавь вес к `Box.loaded` и запиши в `self.status` строку `loaded`, а иначе — строку "
               "`does not fit`.",
               "Пройди циклом по `weights` и для каждого веса создай коробку. Сразу после создания выведи строку вида "
               "`Box 1: 30 kg, loaded` — номер коробки по порядку (с 1), вес и статус из атрибутов объекта.",
               "После цикла выведи строку вида `Truck load: 90 of 100 kg` — числа возьми из `Box.loaded` и `Box.limit`."],
        hint="Общий вес меняй через имя класса: `Box.loaded += weight`. Запись `self.loaded += weight` создаст у коробки "
             "её собственную копию, а общий вес класса так и останется нулём. Ровно 100 кг в грузовике — ещё можно.",
        solution=BOX,
        wrong=[("прибавляет вес через self — у класса общий вес так и остаётся нулём",
                BOX.replace("            Box.loaded += weight", "            self.loaded += weight")),
               ("строгое сравнение — не грузит коробку, после которой вес ровно 100 кг",
                BOX.replace("Box.loaded + weight <= Box.limit", "Box.loaded + weight < Box.limit"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, class_level("loaded", "loaded = 0", "Box", "Тогда вес груза будет общим для всех коробок."),
                  ("re:Box\\.loaded\\s*\\+=",
                   "Прибавляй вес через имя класса: `Box.loaded += weight`. Так растёт общий вес, "
                   "а не копия у одной коробки.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-clsattr-rt-smoke-sensors", title="Датчики дыма",
        given=["rooms", "values", "new_level"],
        variants=[{"rooms": '["kitchen", "hall", "garage"]', "values": "[70, 35, 55]", "new_level": "60"},
                  {"rooms": '["office", "lab"]', "values": "[20, 45]", "new_level": "30"},
                  {"rooms": '["attic", "bath", "porch", "shed"]', "values": "[50, 90, 10, 65]", "new_level": "40"}],
        hidden=[{"rooms": '["roof"]', "values": "[50]", "new_level": "49"},
                {"rooms": '["a1", "a2", "a3"]', "values": "[51, 80, 20]", "new_level": "90"},
                {"rooms": '["west", "east"]', "values": "[5, 6]", "new_level": "50"}],
        intro="В здании стоят датчики дыма — в комнатах из списка `rooms`, а в списке `values` на тех же местах — "
              "что показывает каждый датчик. Датчик поднимает тревогу, если его показание больше общего порога "
              "тревоги. Порог один на все датчики, и система помнит все созданные датчики — это атрибуты класса. "
              "Потом инженер меняет порог на `new_level`.",
        steps=["Создай класс `Sensor` с двумя атрибутами класса: `level = 50` — порог тревоги и `sensors = []` — "
               "список всех созданных датчиков.",
               "В `__init__(self, room, value)` сохрани комнату и показание в `self.room` и `self.value` "
               "и добавь сам объект в общий список: `Sensor.sensors.append(self)`. Добавь метод `alarm(self)`, "
               "который возвращает `True`, если показание больше `Sensor.level`.",
               "Создай по датчику на каждую позицию `range(len(rooms))` и выведи строку вида `Sensors: 3` — длину "
               "списка `Sensor.sensors`.",
               "Выведи строку вида `Level 50: kitchen, garage` — порог и комнаты датчиков с тревогой через запятую "
               "и пробел в порядке списка, а если тревоги нет нигде — `Level 50: none`. Перебирай датчики "
               "из `Sensor.sensors`.",
               "Поменяй порог сразу для всех датчиков через класс: `Sensor.level = new_level` — и снова выведи строку "
               "того же вида. Новые датчики не создавай."],
        hint="Строку с тревогами нужно вывести дважды, поэтому удобно написать для неё свою функцию. Если у объекта "
             "нет своего атрибута `level`, Python берёт его у класса — поэтому одной записи `Sensor.level = new_level` "
             "хватает для всех датчиков. Показание, равное порогу, тревогу ещё не поднимает. "
             "Имена из списка склеивает `\", \".join(...)`.",
        solution=SENSOR,
        wrong=[("меняет порог через первый датчик — у остальных и у класса порог старый",
                SENSOR.replace("Sensor.level = new_level", "Sensor.sensors[0].level = new_level")
                      .replace("return self.value > Sensor.level", "return self.value > self.level")),
               ("поднимает тревогу и при показании, равном порогу",
                SENSOR.replace("self.value > Sensor.level", "self.value >= Sensor.level"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS,
                  class_level("level", "level = 50", "Sensor", "Тогда порог будет общим для всех датчиков."),
                  ("re:Sensor\\.level\\s*=(?!=)",
                   "Поменяй порог через сам класс: `Sensor.level = new_level`. Тогда новый порог сразу "
                   "подействует на все датчики.")],
    ),
]
