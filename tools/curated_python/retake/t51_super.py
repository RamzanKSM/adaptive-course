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


AUDIOBOOK = """\
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def info(self):
        return f"{self.title} by {self.author}"


class AudioBook(Book):
    def __init__(self, title, author, hours):
        super().__init__(title, author)
        self.hours = hours


book = AudioBook(title, author, hours)
print(book.info())
print(f"Listening time: {book.hours} h")
"""

GYM = """\
class Membership:
    def __init__(self, owner, months):
        self.owner = owner
        self.months = months
        self.price = months * 2000
        if months >= 6:
            self.price = self.price * 9 // 10


class FamilyMembership(Membership):
    def __init__(self, owner, months, people):
        super().__init__(owner, months)
        self.people = people
        self.price = self.price * people


single = Membership(name, months)
family = FamilyMembership(family_name, family_months, people)
print(f"{single.owner}: {single.months} months, {single.price} rub")
print(f"{family.owner}: {family.months} months, {family.people} people, {family.price} rub")
"""

TAXI = """\
class Ride:
    name = "Day"

    def __init__(self, km):
        self.km = km

    def cost(self):
        fare = 60 + self.km * 20
        if fare < 150:
            fare = 150
        return fare


class NightRide(Ride):
    name = "Night"

    def __init__(self, km, percent):
        super().__init__(km)
        self.percent = percent

    def cost(self):
        return super().cost() * (100 + self.percent) // 100


rides = [Ride(day_km), NightRide(night_km, percent)]
total = 0
for ride in rides:
    print(f"{ride.name}, {ride.km} km: {ride.cost()} rub")
    total += ride.cost()
print(f"Total: {total} rub")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-super-rt-audiobook", title="Аудиокнига",
        given=["title", "author", "hours"],
        variants=[{"title": '"Dune"', "author": '"Herbert"', "hours": "21"},
                  {"title": '"Emma"', "author": '"Austen"', "hours": "16"},
                  {"title": '"Ulysses"', "author": '"Joyce"', "hours": "27"}],
        hidden=[{"title": '"Hamlet"', "author": '"Shakespeare"', "hours": "4"},
                {"title": '"Solaris"', "author": '"Lem"', "hours": "9"},
                {"title": '"Lolita"', "author": '"Nabokov"', "hours": "11"}],
        intro="В приложении книжного магазина у каждой книги есть название и автор. Аудиокнига — тоже книга, "
              "только у неё есть ещё длительность в часах. Название и автора пусть сохраняет класс-родитель, "
              "а аудиокнига добавит только длительность.",
        steps=["Создай класс `Book`. В `__init__(self, title, author)` сохрани название и автора в `self.title` "
               "и `self.author`. Добавь метод `info(self)`, который возвращает строку вида `Dune by Herbert`.",
               "Создай класс `AudioBook` — наследник `Book` — со своим `__init__(self, title, author, hours)`. "
               "Первой строкой в нём вызови `super().__init__(title, author)`, а потом сохрани `self.hours`.",
               "Создай `book = AudioBook(title, author, hours)`.",
               "Выведи две строки: результат `book.info()` и строку вида `Listening time: 21 h`."],
        hint="Своего метода `info` у аудиокниги нет — она получает его от `Book`. А чтобы `info` нашёл "
             "`self.title` и `self.author`, их должен сохранить родитель: для этого и нужен `super().__init__(...)`. "
             "Передай ему название и автора в том порядке, в каком их ждёт `Book`.",
        solution=AUDIOBOOK,
        wrong=[("передаёт родителю аргументы в другом порядке — название и автор меняются местами",
                AUDIOBOOK.replace("super().__init__(title, author)", "super().__init__(author, title)")),
               ("передаёт родителю название дважды — вместо автора снова название",
                AUDIOBOOK.replace("super().__init__(title, author)", "super().__init__(title, title)"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("AudioBook", "Book"), NEED_SUPER_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-super-rt-gym-family", title="Семейный абонемент",
        given=["name", "months", "family_name", "family_months", "people"],
        variants=[{"name": '"Anya"', "months": "3", "family_name": '"Ivanovs"', "family_months": "12", "people": "3"},
                  {"name": '"Boris"', "months": "6", "family_name": '"Petrovs"', "family_months": "2", "people": "4"},
                  {"name": '"Vera"', "months": "4", "family_name": '"Smirnovs"', "family_months": "6", "people": "2"}],
        hidden=[{"name": '"Gleb"', "months": "6", "family_name": '"Orlovs"', "family_months": "5", "people": "2"},
                {"name": '"Dina"', "months": "12", "family_name": '"Popovs"', "family_months": "3", "people": "5"},
                {"name": '"Egor"', "months": "2", "family_name": '"Volkovs"', "family_months": "9", "people": "3"}],
        intro="Фитнес-клуб продаёт абонементы: месяц стоит 2000 руб., а если взять 6 месяцев и больше, на весь "
              "абонемент даётся скидка 10%. Семейный абонемент — тот же абонемент, его цена со скидкой считается "
              "так же, но потом умножается на число членов семьи.",
        steps=["Создай класс `Membership`. В `__init__(self, owner, months)` сохрани владельца и число месяцев "
               "в `self.owner` и `self.months`, а цену посчитай в `self.price`: `months * 2000`, а если "
               "месяцев 6 или больше — эта сумма, умноженная на 9 и делённая на 10 нацело.",
               "Создай класс `FamilyMembership` — наследник `Membership` — со своим "
               "`__init__(self, owner, months, people)`. Сначала вызови `super().__init__(owner, months)` — пусть "
               "родитель сохранит владельца и посчитает цену со скидкой. Потом сохрани `self.people` и умножь "
               "`self.price` на число людей.",
               "Создай `single = Membership(name, months)` и "
               "`family = FamilyMembership(family_name, family_months, people)`.",
               "Выведи строки вида `Anya: 3 months, 6000 rub` и `Ivanovs: 12 months, 3 people, 64800 rub`."],
        hint="Правило скидки записано только в `Membership.__init__`. Если наследник посчитает цену сам, без "
             "`super().__init__`, скидку легко потерять. И порядок важен: умножать `self.price` можно только после "
             "вызова родителя — до него цены ещё нет.",
        solution=GYM,
        wrong=[("не вызывает super().__init__ и считает цену сам — семья не получает скидку",
                GYM.replace("        super().__init__(owner, months)\n        self.people = people\n"
                            "        self.price = self.price * people\n",
                            "        self.owner = owner\n        self.months = months\n        self.people = people\n"
                            "        self.price = months * 2000 * people\n")),
               ("скидка только для абонементов длиннее 6 месяцев — ровно 6 месяцев без скидки",
                GYM.replace("        if months >= 6:", "        if months > 6:"))],
        constructs=["class"],
        must_use=[NEED_CLASS, child_of("FamilyMembership", "Membership"), NEED_SUPER_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-super-rt-night-taxi", title="Ночное такси",
        given=["day_km", "night_km", "percent"],
        variants=[{"day_km": "8", "night_km": "5", "percent": "30"},
                  {"day_km": "3", "night_km": "2", "percent": "50"},
                  {"day_km": "12", "night_km": "1", "percent": "20"}],
        hidden=[{"day_km": "4", "night_km": "4", "percent": "25"},
                {"day_km": "5", "night_km": "5", "percent": "0"},
                {"day_km": "20", "night_km": "10", "percent": "100"},
                {"day_km": "0", "night_km": "7", "percent": "10"}],
        intro="Такси считает цену поездки так: 60 руб. за посадку плюс 20 руб. за километр, но не меньше "
              "150 руб. за поездку. Ночная поездка — та же поездка, только к её цене (уже с учётом минимума) "
              "добавляется ночная надбавка `percent` процентов. Днём ты проехал `day_km` км, ночью — `night_km` км.",
        steps=["Создай класс `Ride` с атрибутом класса `name = \"Day\"`. В `__init__(self, km)` сохрани расстояние "
               "в `self.km`. Метод `cost(self)` возвращает `60 + km * 20`, а если это меньше 150 — ровно 150.",
               "Создай класс `NightRide` — наследник `Ride` — с атрибутом класса `name = \"Night\"` и своим "
               "`__init__(self, km, percent)`: вызови `super().__init__(km)` и сохрани `self.percent`.",
               "Переопредели в `NightRide` метод `cost(self)`: возьми цену родителя через `super().cost()`, умножь "
               "на `100 + self.percent` и раздели на 100 нацело.",
               "Создай список `rides = [Ride(day_km), NightRide(night_km, percent)]`. Одним циклом выведи для каждой "
               "поездки строку вида `Day, 8 km: 220 rub` и сложи цены.",
               "Последней строкой выведи общую сумму в виде `Total: 428 rub`."],
        hint="Внутри `NightRide.cost` не повторяй формулу родителя: `super().cost()` уже вернёт цену с посадкой "
             "и минимумом в 150 руб., осталось добавить надбавку. А `self.cost()` там вызвал бы сам себя. "
             "Делить нужно через `//`, иначе получится дробное число вроде `208.0`.",
        solution=TAXI,
        wrong=[("ночная цена считается заново по формуле без минимума в 150 руб.",
                TAXI.replace("        return super().cost() * (100 + self.percent) // 100",
                             "        return (60 + self.km * 20) * (100 + self.percent) // 100")),
               ("делит через / — ночная цена получается дробной",
                TAXI.replace("        return super().cost() * (100 + self.percent) // 100",
                             "        return super().cost() * (100 + self.percent) / 100"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, child_of("NightRide", "Ride"), NEED_SUPER_INIT,
                  ("re:super\\(\\)\\.cost\\(\\)",
                   "В `cost` ночной поездки возьми цену родителя через `super().cost()` и добавь к ней надбавку — "
                   "так формула и минимум останутся в одном месте.")],
    ),
]
