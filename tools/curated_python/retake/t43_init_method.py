"""PY_INIT_METHOD — «Метод __init__». Taught before: everything up to functions (with default values), classes, creating
objects. Here: __init__ runs by itself when an object is created; its parameters are the arguments of the class call;
it sets starting values that are not passed, default parameter values, attributes computed from the parameters.
Not yet: inheritance, @property, tuples, dicts."""
from build import OutputTask

SKILL = "PY_INIT_METHOD"

NEED_CLASS = ("ClassDef", "Опиши объект в собственном классе через class.")
NEED_INIT = ("re:def __init__\\(", "Задай атрибуты в методе __init__ — Python сам вызывает его, когда создаёт объект. "
             "Имя пишется с двумя подчёркиваниями с каждой стороны.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-init-rt-club-member", title="Новичок в кружке",
        given=["name", "age", "visits"],
        variants=[{"name": '"Anya"', "age": "12", "visits": "4"},
                  {"name": '"Timur"', "age": "10", "visits": "1"},
                  {"name": '"Lera"', "age": "14", "visits": "7"}],
        hidden=[{"name": '"Gleb"', "age": "9", "visits": "0"},
                {"name": '"Sabina"', "age": "15", "visits": "12"},
                {"name": '"Kolya"', "age": "11", "visits": "3"}],
        intro="В кружок робототехники записался новый ученик: имя `name`, возраст `age`. У каждого новичка пока "
              "ноль посещённых занятий и значок `newbie`. Потом ученик сходил на `visits` занятий.",
        steps=["Создай класс `Member` с методом `__init__(self, name, age)`. Сохрани имя и возраст в атрибуты "
               "`self.name` и `self.age`, а ещё задай стартовые значения, которые при создании не передаются: "
               "`self.lessons = 0` и `self.badge = \"newbie\"`.",
               "Последней строкой внутри `__init__` выведи строку вида `Welcome, Anya!` — с именем из параметра `name`.",
               "Создай ученика: `member = Member(name, age)`. Отдельно вызывать `__init__` не нужно. "
               "Потом увеличь `member.lessons` на `visits`.",
               "Выведи строку вида `Anya (12): newbie, lessons 4` — все значения бери из атрибутов объекта `member`."],
        hint="`__init__` срабатывает сам в момент `Member(name, age)`. В нём задают не только атрибуты из параметров, "
             "но и такие, у которых у всех новых объектов одинаковое начальное значение — как `self.lessons = 0`. "
             "Потом атрибут можно менять снаружи: `member.lessons += visits`.",
        solution='class Member:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n'
                 '        self.lessons = 0\n        self.badge = "newbie"\n        print(f"Welcome, {name}!")\n\n\n'
                 'member = Member(name, age)\nmember.lessons += visits\n'
                 'print(f"{member.name} ({member.age}): {member.badge}, lessons {member.lessons}")',
        wrong=[("начинает счёт занятий с 1 вместо 0",
                'class Member:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n'
                '        self.lessons = 1\n        self.badge = "newbie"\n        print(f"Welcome, {name}!")\n\n\n'
                'member = Member(name, age)\nmember.lessons += visits\n'
                'print(f"{member.name} ({member.age}): {member.badge}, lessons {member.lessons}")'),
               ("записывает возраст числом 12 вместо параметра age — у всех один возраст",
                'class Member:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = 12\n'
                '        self.lessons = 0\n        self.badge = "newbie"\n        print(f"Welcome, {name}!")\n\n\n'
                'member = Member(name, age)\nmember.lessons += visits\n'
                'print(f"{member.name} ({member.age}): {member.badge}, lessons {member.lessons}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-init-rt-gym-membership", title="Абонемент в спортзал",
        given=["name1", "name2", "months2"],
        variants=[{"name1": '"Anna"', "name2": '"Igor"', "months2": "6"},
                  {"name1": '"Marat"', "name2": '"Olga"', "months2": "3"},
                  {"name1": '"Sveta"', "name2": '"Pyotr"', "months2": "12"}],
        hidden=[{"name1": '"Yulya"', "name2": '"Denis"', "months2": "2"},
                {"name1": '"Akhmed"', "name2": '"Nina"', "months2": "1"},
                {"name1": '"Lev"', "name2": '"Kira"', "months2": "9"}],
        intro="В спортзале месяц занятий стоит 2000 руб. Чаще всего берут абонемент на один месяц, поэтому срок "
              "можно не называть — тогда он равен 1. Сегодня купили два абонемента: `name1` не назвал срок, "
              "а `name2` взял абонемент на `months2` месяцев.",
        steps=["Создай класс `Membership`. Его метод `__init__` принимает имя `name` и число месяцев `months` "
               "со значением по умолчанию 1: `def __init__(self, name, months=1)`. Сохрани оба значения в атрибуты "
               "`self.name` и `self.months`, а ещё сразу посчитай атрибут `self.price` — `months`, умноженное на 2000.",
               "Создай первый абонемент, передав только имя: `card1 = Membership(name1)`. Второй — с именем и сроком: "
               "`card2 = Membership(name2, months2)`.",
               "Для каждого абонемента выведи строку вида `Anna: months 1, price 2000 rub` — сначала для первого, "
               "потом для второго."],
        hint="Значения по умолчанию у `__init__` работают так же, как у обычной функции: если аргумент не передали, "
             "параметр получает значение по умолчанию. Цену считай из параметра `months`, а не из числа 1.",
        solution='class Membership:\n    def __init__(self, name, months=1):\n        self.name = name\n        self.months = months\n'
                 '        self.price = months * 2000\n\n\ncard1 = Membership(name1)\ncard2 = Membership(name2, months2)\n'
                 'print(f"{card1.name}: months {card1.months}, price {card1.price} rub")\n'
                 'print(f"{card2.name}: months {card2.months}, price {card2.price} rub")',
        wrong=[("цену всегда ставит за один месяц, не глядя на срок",
                'class Membership:\n    def __init__(self, name, months=1):\n        self.name = name\n        self.months = months\n'
                '        self.price = 2000\n\n\ncard1 = Membership(name1)\ncard2 = Membership(name2, months2)\n'
                'print(f"{card1.name}: months {card1.months}, price {card1.price} rub")\n'
                'print(f"{card2.name}: months {card2.months}, price {card2.price} rub")'),
               ("поставил значением по умолчанию 12 месяцев вместо 1",
                'class Membership:\n    def __init__(self, name, months=12):\n        self.name = name\n        self.months = months\n'
                '        self.price = months * 2000\n\n\ncard1 = Membership(name1)\ncard2 = Membership(name2, months2)\n'
                'print(f"{card1.name}: months {card1.months}, price {card1.price} rub")\n'
                'print(f"{card2.name}: months {card2.months}, price {card2.price} rub")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:def __init__\\([^)]*months\\s*=\\s*1\\b",
                   "Сделай срок параметром __init__ со значением по умолчанию: def __init__(self, name, months=1).")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-init-rt-weather-log", title="Дневник погоды",
        given=["temps"],
        variants=[{"temps": "[-5, 12, 20]"}, {"temps": "[3, -12, 15, 0]"}, {"temps": "[25, 14, -1]"}],
        hidden=[{"temps": "[0]"}, {"temps": "[-1, 15, 14, -20, 30]"}, {"temps": "[18, 7]"}],
        intro="Метеостанция записывает температуру за несколько дней — список `temps` в градусах Цельсия. "
              "Для каждой записи нужно сразу знать температуру в кельвинах и оценку погоды, поэтому запись "
              "вычисляет их сама, как только её создают.",
        steps=["Создай класс `Reading`. Его метод `__init__(self, celsius)` сохраняет температуру в атрибут "
               "`self.celsius` и сразу вычисляет ещё два атрибута.",
               "`self.kelvin` — температура в кельвинах: `celsius` плюс 273.",
               "`self.state` — оценка погоды: `frost`, если температура ниже 0; `cold`, если от 0 до 14 включительно; "
               "`warm`, если 15 и выше.",
               "Пройди циклом по списку `temps` и для каждого числа создай объект `Reading`. Для каждой записи выведи "
               "строку вида `Day 1: -5 C (268 K), frost` — номер дня по порядку, начиная с 1, и значения "
               "из атрибутов объекта."],
        hint="В `__init__` можно писать `if`, `elif` и `else`, как в обычной функции, и в каждой ветке задавать "
             "`self.state` своё значение. Если написать три отдельных `if` без `elif`, следующая проверка может "
             "перезаписать уже найденную оценку.",
        solution='class Reading:\n    def __init__(self, celsius):\n        self.celsius = celsius\n        self.kelvin = celsius + 273\n'
                 '        if celsius < 0:\n            self.state = "frost"\n        elif celsius < 15:\n'
                 '            self.state = "cold"\n        else:\n            self.state = "warm"\n\n\n'
                 'number = 1\nfor temp in temps:\n    reading = Reading(temp)\n'
                 '    print(f"Day {number}: {reading.celsius} C ({reading.kelvin} K), {reading.state}")\n    number += 1',
        wrong=[("считает ноль градусов морозом",
                'class Reading:\n    def __init__(self, celsius):\n        self.celsius = celsius\n        self.kelvin = celsius + 273\n'
                '        if celsius <= 0:\n            self.state = "frost"\n        elif celsius < 15:\n'
                '            self.state = "cold"\n        else:\n            self.state = "warm"\n\n\n'
                'number = 1\nfor temp in temps:\n    reading = Reading(temp)\n'
                '    print(f"Day {number}: {reading.celsius} C ({reading.kelvin} K), {reading.state}")\n    number += 1'),
               ("проверяет отдельными if без elif — мороз перезаписывается на cold",
                'class Reading:\n    def __init__(self, celsius):\n        self.celsius = celsius\n        self.kelvin = celsius + 273\n'
                '        if celsius < 0:\n            self.state = "frost"\n        if celsius < 15:\n'
                '            self.state = "cold"\n        else:\n            self.state = "warm"\n\n\n'
                'number = 1\nfor temp in temps:\n    reading = Reading(temp)\n'
                '    print(f"Day {number}: {reading.celsius} C ({reading.kelvin} K), {reading.state}")\n    number += 1')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:self\\.state\\s*=", "Вычисли оценку погоды прямо в __init__ и сохрани её в атрибут self.state.")],
    ),
]
