"""PY_DUCK_TYPING — «Утиная типизация». Taught before: everything up to classes, __init__, self and methods,
«private» attributes, @property, class attributes, inheritance, overriding, polymorphism, super(). Here: unrelated
classes (no common parent) that have a method with the same name; a function works with any object that has this
method and never checks what the object is. Not yet: tuples, sets, dicts, comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_DUCK_TYPING"

NEED_CLASS = ("ClassDef", "Опиши предметы в собственных классах через class.")
NO_PARENT = ("re:\\A(?![\\s\\S]*class\\s+\\w+\\s*\\(\\s*\\w)",
             "Здесь классы не связаны наследованием: не указывай родителя в скобках после имени класса. "
             "Функции достаточно, что у каждого объекта есть метод с нужным именем.")


def need_function(name: str, params: str) -> tuple[str, str]:
    return (f"re:(?m)^def\\s+{name}\\s*\\(",
            f"Напиши отдельную функцию `{name}({params})` — не внутри класса, а после классов. "
            f"Она должна работать с любым объектом, у которого есть нужный метод.")


NOTIFY = """\
class Email:
    def __init__(self, address):
        self.address = address

    def send(self, text):
        return f"email to {self.address}: {text}"


class Sms:
    def __init__(self, phone):
        self.phone = phone

    def send(self, text):
        return f"sms to {self.phone}: {text}"


def notify(channel, text):
    print(f"Sent {channel.send(text)}")


email = Email(address)
sms = Sms(phone)
notify(email, text)
notify(sms, text)
"""

POWER_BANK = """\
class Phone:
    name = "Phone"

    def __init__(self, percent):
        self.percent = percent

    def need(self):
        return (100 - self.percent) * 40


class Lamp:
    name = "Lamp"

    def __init__(self, hours):
        self.hours = hours

    def need(self):
        return self.hours * 100


class Speaker:
    name = "Speaker"

    def __init__(self, songs):
        self.songs = songs

    def need(self):
        return self.songs * 15


def charge(devices, bank):
    for device in devices:
        if device.need() <= bank:
            bank -= device.need()
            print(f"{device.name}: charged")
        else:
            print(f"{device.name}: skipped")
    print(f"Power bank left: {bank} mAh")


charge([Phone(percent), Lamp(hours), Speaker(songs)], bank)
"""

RACE = """\
class Rabbit:
    name = "Rabbit"

    def __init__(self, sleep_after):
        self.sleep_after = sleep_after
        self.moves = 0
        self.position = 0

    def move(self):
        self.moves += 1
        if self.moves <= self.sleep_after:
            self.position += 3


class Turtle:
    name = "Turtle"

    def __init__(self):
        self.position = 0

    def move(self):
        self.position += 1


class Frog:
    name = "Frog"

    def __init__(self, jump):
        self.jump = jump
        self.resting = False
        self.position = 0

    def move(self):
        if not self.resting:
            self.position += self.jump
        self.resting = not self.resting


def race(racers, finish):
    round_number = 0
    while True:
        round_number += 1
        for racer in racers:
            racer.move()
            if racer.position >= finish:
                print(f"Round {round_number}: {racer.name} wins")
                return


racers = [Rabbit(sleep_after), Turtle(), Frog(jump)]
race(racers, finish)
for racer in racers:
    print(f"{racer.name}: {racer.position} m")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-duck-rt-email-sms", title="Письмо или СМС",
        given=["address", "phone", "text"],
        variants=[{"address": '"anya@mail.ru"', "phone": '"+79001234567"', "text": '"Lesson moved to 10:00"'},
                  {"address": '"boris@yandex.ru"', "phone": '"+79115550011"', "text": '"Exam on Monday"'},
                  {"address": '"vera@gmail.com"', "phone": '"+79263332211"', "text": '"Bring your laptop"'}],
        hidden=[{"address": '"gleb@inbox.ru"', "phone": '"+79990000000"', "text": '"No classes today"'},
                {"address": '"dina@list.ru"', "phone": '"+79031112233"', "text": '"Room 305"'},
                {"address": '"egor@bk.ru"', "phone": '"+79507778899"', "text": '"See you"'}],
        intro="Деканат рассылает студентам сообщения: одним по электронной почте, другим по СМС. Письмо и СМС — "
              "совсем разные классы без общего родителя, но оба умеют отправить текст методом `send(text)`. "
              "Функции рассылки этого достаточно.",
        steps=["Создай класс `Email`. В `__init__(self, address)` сохрани адрес. Добавь метод `send(self, text)`, "
               "который возвращает строку вида `email to anya@mail.ru: Lesson moved to 10:00`.",
               "Создай класс `Sms` — отдельный, без родителя. В `__init__(self, phone)` сохрани номер телефона. "
               "Метод `send(self, text)` возвращает строку вида `sms to +79001234567: Lesson moved to 10:00`.",
               "Напиши функцию `notify(channel, text)`, которая печатает `Sent` и через пробел результат "
               "`channel.send(text)`. Проверять, письмо это или СМС, не нужно.",
               "Создай `email = Email(address)` и `sms = Sms(phone)` и вызови `notify` с текстом `text` сначала "
               "для письма, потом для СМС."],
        hint="Внутри `notify` есть только параметр `channel` — с ним и работай: функции всё равно, какого он класса, "
             "лишь бы у него был метод `send`. Метод должен **возвращать** строку через `return`, а печатает её `notify`.",
        solution=NOTIFY,
        wrong=[("функция notify берёт глобальную переменную email вместо параметра channel — дважды уходит письмо",
                NOTIFY.replace('    print(f"Sent {channel.send(text)}")', '    print(f"Sent {email.send(text)}")')),
               ("СМС отправляется без текста сообщения",
                NOTIFY.replace('        return f"sms to {self.phone}: {text}"', '        return f"sms to {self.phone}"'))],
        constructs=["class", "function"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("notify", "channel, text")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-duck-rt-power-bank", title="Пауэрбанк в походе",
        given=["percent", "hours", "songs", "bank"],
        variants=[{"percent": "40", "hours": "5", "songs": "30", "bank": "3000"},
                  {"percent": "70", "hours": "8", "songs": "20", "bank": "2000"},
                  {"percent": "10", "hours": "3", "songs": "40", "bank": "2500"}],
        hidden=[{"percent": "100", "hours": "0", "songs": "0", "bank": "0"},
                {"percent": "50", "hours": "10", "songs": "10", "bank": "3150"},
                {"percent": "0", "hours": "20", "songs": "100", "bank": "1000"},
                {"percent": "90", "hours": "2", "songs": "5", "bank": "600"}],
        intro="В походе есть пауэрбанк, в котором `bank` мАч. От него по очереди заряжают телефон, фонарь и колонку. "
              "Телефон заряжен на `percent` процентов, фонарь должен светить `hours` часов, колонка — сыграть `songs` песен. "
              "Это три разных класса, и сколько энергии нужно, каждый считает по-своему, но у всех есть метод `need()`.",
        steps=["Создай три отдельных класса без общего родителя. У каждого — атрибут класса `name` и метод "
               "`need(self)`, который возвращает, сколько мАч нужно этому устройству.",
               "`Phone`: `name = \"Phone\"`, в `__init__(self, percent)` сохраняет заряд, `need` возвращает "
               "по 40 мАч на каждый недостающий до 100 процент. `Lamp`: `name = \"Lamp\"`, в `__init__(self, hours)` "
               "сохраняет часы, `need` возвращает по 100 мАч на час. `Speaker`: `name = \"Speaker\"`, "
               "в `__init__(self, songs)` сохраняет число песен, `need` возвращает по 15 мАч на песню.",
               "Напиши функцию `charge(devices, bank)`. Для каждого устройства из списка `devices`: если ему нужно "
               "не больше, чем осталось в пауэрбанке, вычти это из `bank` и выведи строку вида `Phone: charged`, "
               "иначе выведи строку вида `Speaker: skipped` и ничего не вычитай.",
               "После цикла функция выводит строку вида `Power bank left: 100 mAh`.",
               "Вызови `charge([Phone(percent), Lamp(hours), Speaker(songs)], bank)`."],
        hint="Функция `charge` не выясняет, телефон перед ней или колонка: она спрашивает у любого устройства `need()`. "
             "Если заряда осталось ровно столько, сколько нужно, устройство заряжается, и в пауэрбанке остаётся 0.",
        solution=POWER_BANK,
        wrong=[("строгое сравнение: устройство не заряжается, когда заряда осталось ровно столько, сколько нужно",
                POWER_BANK.replace("        if device.need() <= bank:", "        if device.need() < bank:")),
               ("не вычитает потраченный заряд — пауэрбанк никогда не разряжается",
                POWER_BANK.replace("            bank -= device.need()\n", ""))],
        constructs=["class", "function", "for"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("charge", "devices, bank")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-duck-rt-animal-race", title="Забег зверей",
        given=["sleep_after", "jump", "finish"],
        variants=[{"sleep_after": "2", "jump": "4", "finish": "8"},
                  {"sleep_after": "5", "jump": "3", "finish": "12"},
                  {"sleep_after": "1", "jump": "1", "finish": "4"}],
        hidden=[{"sleep_after": "1", "jump": "5", "finish": "3"},
                {"sleep_after": "0", "jump": "2", "finish": "5"},
                {"sleep_after": "4", "jump": "7", "finish": "30"},
                {"sleep_after": "3", "jump": "6", "finish": "12"}],
        intro="Заяц, черепаха и лягушка бегут до финиша на расстоянии `finish` метров. Забег идёт раундами: в каждом "
              "раунде звери ходят по очереди — заяц, черепаха, лягушка. Побеждает тот, кто первым дошёл до финиша "
              "или пробежал его. Двигается каждый по-своему, но у всех есть метод `move()` и атрибут `position`.",
        steps=["Создай класс `Rabbit` с атрибутом класса `name = \"Rabbit\"`. В `__init__(self, sleep_after)` сохрани "
               "`sleep_after`, а счётчик ходов и позицию `position` сделай равными 0. Метод `move(self)` увеличивает "
               "счётчик ходов на 1 и, если ходов пока не больше `sleep_after`, сдвигает зайца на 3 метра. "
               "Дальше заяц спит и стоит на месте.",
               "Создай отдельный класс `Turtle` с `name = \"Turtle\"`: в `__init__(self)` позиция 0, а `move(self)` "
               "каждый раз сдвигает её на 1 метр.",
               "Создай отдельный класс `Frog` с `name = \"Frog\"`. В `__init__(self, jump)` сохрани длину прыжка, "
               "позицию 0 и признак отдыха `resting = False`. Метод `move(self)`: если лягушка не отдыхает, она прыгает "
               "на `jump` метров; в любом случае после хода признак отдыха меняется на противоположный — "
               "так лягушка прыгает через раунд.",
               "Напиши функцию `race(racers, finish)`. Она считает раунды с 1 и в каждом раунде вызывает `move()` "
               "у каждого зверя из списка по порядку. Сразу после хода проверь: если `position` зверя не меньше `finish`, "
               "выведи строку вида `Round 3: Frog wins` и завершай функцию через `return` — остальные в этом раунде уже "
               "не ходят.",
               "Создай `racers = [Rabbit(sleep_after), Turtle(), Frog(jump)]`, вызови `race(racers, finish)`, "
               "а потом для каждого зверя выведи строку вида `Rabbit: 6 m` с его позицией."],
        hint="Функции `race` не важно, кто перед ней: она вызывает `move()` и смотрит на `position` у любого зверя. "
             "Раунды удобно крутить в `while True`, а выходить из функции — через `return` в момент победы. "
             "Проверяй финиш сразу после хода каждого зверя, а не в конце раунда.",
        solution=RACE,
        wrong=[("проверяет финиш только в конце раунда — звери после победителя успевают сделать ход",
                RACE.replace("        for racer in racers:\n            racer.move()\n            if racer.position >= finish:\n",
                             "        for racer in racers:\n            racer.move()\n        for racer in racers:\n"
                             "            if racer.position >= finish:\n")),
               ("лягушка никогда не отдыхает и прыгает каждый раунд",
                RACE.replace("        self.resting = not self.resting\n", "")),
               ("строгое сравнение: зверь, вставший ровно на финиш, ещё не победил",
                RACE.replace("            if racer.position >= finish:", "            if racer.position > finish:"))],
        constructs=["class", "function", "while"],
        must_use=[NEED_CLASS, NO_PARENT, need_function("race", "racers, finish")],
    ),
]
