"""PY_POLYMORPHISM_BASIC — «Полиморфизм». Taught before: everything up to classes, __init__, self and methods,
«private» attributes, @property, class attributes, inheritance, overriding methods. Here: objects of different child
classes in one list; one loop calls the same method on each and every object answers in its own way — no checks of
«who is who». Not yet: super() (next topic), duck typing without a common parent, tuples, dicts, comprehensions."""
from build import OutputTask

SKILL = "PY_POLYMORPHISM_BASIC"

NEED_CLASS = ("ClassDef", "Опиши объекты в собственных классах через class.")
NEED_LOOP = ("For", "Обойди все объекты одним циклом for по списку.")


def child_of(child: str, parent: str) -> tuple[str, str]:
    return (f"re:class\\s+{child}\\s*\\(\\s*{parent}\\s*\\)",
            f"Сделай класс `{child}` наследником `{parent}`: напиши `class {child}({parent}):`.")


def no_title_check(what: str, method: str) -> tuple[str, str]:
    return ("re:\\A(?![\\s\\S]*\\.title\\s*[!=]=)",
            f"Не проверяй через if, какой это {what}: просто вызови `{method}`. "
            f"Каждый объект сам знает, как ответить, — в этом и смысл полиморфизма.")


NOTICES = """\
class Notice:
    def __init__(self, text):
        self.text = text

    def show(self):
        return self.text


class Info(Notice):
    def show(self):
        return "[i] " + self.text


class Alert(Notice):
    def show(self):
        return "[!] " + self.text


class Error(Notice):
    def show(self):
        return "[x] " + self.text


notices = [Info(text1), Alert(text2), Error(text3)]
for notice in notices:
    print(notice.show())
"""

SHAPES = """\
class Shape:
    title = "Shape"

    def __init__(self, size):
        self.size = size

    def area(self):
        return self.size * self.size


class Square(Shape):
    title = "Square"


class Triangle(Shape):
    title = "Triangle"

    def area(self):
        return self.size * self.size // 2


class Circle(Shape):
    title = "Circle"

    def area(self):
        return 3 * self.size * self.size


shapes = [Square(size), Triangle(size), Circle(size)]
total = 0
for shape in shapes:
    area = shape.area()
    print(f"{shape.title}: {area} sq cm")
    total += area
print(f"Total: {total} sq cm")
"""

PIECES = """\
class Piece:
    title = "Piece"

    def __init__(self):
        self.position = 0

    def step(self, roll):
        return 0

    def move(self, roll):
        self.position += self.step(roll)


class Walker(Piece):
    title = "Walker"

    def step(self, roll):
        return roll


class Jumper(Piece):
    title = "Jumper"

    def step(self, roll):
        if roll % 2 == 0:
            return roll * 2
        return 0


class Snail(Piece):
    title = "Snail"

    def step(self, roll):
        return 1


pieces = [Walker(), Jumper(), Snail()]
for roll in rolls:
    for piece in pieces:
        piece.move(roll)

leader = pieces[0]
for piece in pieces:
    print(f"{piece.title}: {piece.position}")
    if piece.position > leader.position:
        leader = piece
print(f"Leader: {leader.title}")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-poly-rt-notices", title="Сообщения в журнале",
        given=["text1", "text2", "text3"],
        variants=[{"text1": '"Backup done"', "text2": '"Disk almost full"', "text3": '"Printer offline"'},
                  {"text1": '"Lesson starts"', "text2": '"Low battery"', "text3": '"No internet"'},
                  {"text1": '"New message"', "text2": '"Password expires"', "text3": '"Login failed"'}],
        hidden=[{"text1": '"Hello"', "text2": '"Slow network"', "text3": '"File not found"'},
                {"text1": '"Update ready"', "text2": '"Too many tabs"', "text3": '"Server down"'},
                {"text1": '"OK"', "text2": '"Check it"', "text3": '"Stop"'}],
        intro="Программа ведёт журнал событий. Сообщения бывают трёх видов: информация, предупреждение и ошибка, "
              "и каждое показывается со своим значком в начале. Журнал должен вывести все сообщения одним циклом. "
              "Тексты сообщений — `text1`, `text2` и `text3`.",
        steps=["Создай класс `Notice`. В `__init__(self, text)` сохрани текст в `self.text`. Добавь метод `show(self)`, "
               "который возвращает сам текст.",
               "Создай три наследника `Notice` и переопредели в каждом `show(self)`: `Info` возвращает текст "
               "со значком `[i]` и пробелом в начале, `Alert` — со значком `[!]`, `Error` — со значком `[x]`. "
               "Например, `[!] Disk almost full`.",
               "Создай список `notices = [Info(text1), Alert(text2), Error(text3)]`.",
               "Одним циклом `for` пройди по списку и выведи результат `show()` каждого сообщения. Метод `show()` "
               "в программе вызывай только в одном месте — внутри этого цикла."],
        hint="В цикле переменная по очереди указывает на каждое сообщение, а строка `notice.show()` одна и та же. "
             "Python сам смотрит, какого класса текущий объект, и вызывает его версию метода.",
        solution=NOTICES,
        wrong=[("опечатка в имени метода у ошибки — значок не появляется: срабатывает метод родителя",
                NOTICES.replace("class Error(Notice):\n    def show(", "class Error(Notice):\n    def shov(")),
               ("создаёт все сообщения из класса Notice — значков нет",
                NOTICES.replace("[Info(text1), Alert(text2), Error(text3)]",
                                "[Notice(text1), Notice(text2), Notice(text3)]"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_LOOP, child_of("Info", "Notice"), child_of("Alert", "Notice"),
                  child_of("Error", "Notice"),
                  ("re:\\A(?![\\s\\S]*\\.show\\(\\)[\\s\\S]*\\.show\\(\\))[\\s\\S]*\\.show\\(\\)",
                   "Вызывай `show()` только в одном месте — внутри цикла по списку `notices`. Каждое сообщение "
                   "само знает, как себя показать, поэтому одна строка кода подходит для всех.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-poly-rt-shape-areas", title="Площади фигур",
        given=["size"],
        variants=[{"size": "4"}, {"size": "10"}, {"size": "7"}],
        hidden=[{"size": "1"}, {"size": "3"}, {"size": "20"}],
        intro="Для школьной стенгазеты вырезают из цветной бумаги квадрат, треугольник и круг одного размера `size` см. "
              "Площадь у каждой фигуры считается по-своему, а вывести площади и общую площадь бумаги нужно одинаково — "
              "одним циклом.",
        steps=["Создай класс `Shape` с атрибутом класса `title = \"Shape\"`. В `__init__(self, size)` сохрани размер "
               "в `self.size`. Добавь метод `area(self)`, который возвращает `size`, умноженный на себя.",
               "Создай класс `Square` — наследник `Shape` — с `title = \"Square\"`. Метод `area` в нём не пиши: "
               "площадь квадрата считается так же, как у родителя.",
               "Создай класс `Triangle` — наследник `Shape` — с `title = \"Triangle\"` и переопредели `area`: "
               "половина квадрата — `size * size // 2`.",
               "Создай класс `Circle` — наследник `Shape` — с `title = \"Circle\"` и переопредели `area`: круг радиусом "
               "`size`, число пи округли до 3 — `3 * size * size`.",
               "Создай список `shapes = [Square(size), Triangle(size), Circle(size)]`. Одним циклом по нему выведи "
               "для каждой фигуры строку вида `Triangle: 8 sq cm` и попутно сложи площади. Внутри цикла не проверяй, "
               "какая это фигура, — просто вызывай `area()`. Последней строкой выведи строку вида `Total: 72 sq cm`."],
        hint="У `Square` нет своего `area`, поэтому для него сработает версия из `Shape`, а у `Triangle` и `Circle` — "
             "их собственные. Чтобы не вызывать метод дважды, сохрани площадь в переменную и используй её и для "
             "строки, и для суммы.",
        solution=SHAPES,
        wrong=[("проверяет фигуру через if и считает по-особому только круг — треугольник получается как квадрат",
                SHAPES.replace("    area = shape.area()\n",
                               "    if shape.title == \"Circle\":\n        area = shape.area()\n"
                               "    else:\n        area = shape.size * shape.size\n")),
               ("в треугольнике делит обычным делением — площадь дробная",
                SHAPES.replace("return self.size * self.size // 2", "return self.size * self.size / 2"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_LOOP, child_of("Square", "Shape"), child_of("Triangle", "Shape"),
                  child_of("Circle", "Shape"), no_title_check("фигура", "area()")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-poly-rt-board-game", title="Фишки настольной игры",
        given=["rolls"],
        variants=[{"rolls": "[3, 4, 6, 1]"}, {"rolls": "[2, 5, 5, 2, 1]"}, {"rolls": "[1, 1, 1]"}],
        hidden=[{"rolls": "[]"}, {"rolls": "[6]"}, {"rolls": "[1, 3, 5, 6, 2]"}, {"rolls": "[4, 4]"}],
        intro="В настольной игре три фишки, и каждая ходит по-своему. Пешеход проходит столько клеток, сколько выпало "
              "на кубике. Прыгун прыгает на удвоенное число, но только если выпало чётное число, а иначе стоит на месте. "
              "Улитка всегда ползёт на 1 клетку. В списке `rolls` по порядку записано, что выпадало на кубике; "
              "после каждого броска ходят все три фишки.",
        steps=["Создай класс `Piece` с атрибутом класса `title = \"Piece\"`. В `__init__(self)` задай `self.position = 0`. "
               "Добавь метод `step(self, roll)`, который возвращает `0`, и метод `move(self, roll)`, который прибавляет "
               "к `self.position` результат `self.step(roll)`.",
               "Создай трёх наследников `Piece`, в каждом задай свой `title` и переопредели только `step(self, roll)`: "
               "`Walker` — `\"Walker\"`, ход — `roll`; `Jumper` — `\"Jumper\"`, ход — `roll * 2` при чётном `roll`, "
               "иначе `0`; `Snail` — `\"Snail\"`, ход — всегда `1`.",
               "Создай список `pieces = [Walker(), Jumper(), Snail()]`. Пройди циклом по `rolls` и для каждого броска "
               "вложенным циклом вызови `move(roll)` у каждой фишки.",
               "Потом пройди по `pieces`: выведи для каждой фишки строку вида `Walker: 14` и попутно найди лидера — "
               "фишку, которая дальше всех. Если таких несколько, лидер — та, что раньше в списке. "
               "Последней строкой выведи `Leader: …` с её названием. Не проверяй в циклах, какая это фишка."],
        hint="Метод `move` написан один раз, в родителе, но вызывает `self.step(roll)` — и для каждой фишки сработает "
             "её версия `step`. Чётность проверяют остатком: `roll % 2 == 0`. Лидера ищи, как наибольшее число: "
             "начни с `leader = pieces[0]` и заменяй его, только если позиция строго больше.",
        solution=PIECES,
        wrong=[("прыгун прыгает при любом броске — забыл проверку на чётность",
                PIECES.replace("        if roll % 2 == 0:\n            return roll * 2\n        return 0\n",
                               "        return roll * 2\n")),
               ("при равенстве лидером становится фишка, которая позже в списке",
                PIECES.replace("if piece.position > leader.position:", "if piece.position >= leader.position:"))],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_LOOP, child_of("Walker", "Piece"), child_of("Jumper", "Piece"),
                  child_of("Snail", "Piece"), no_title_check("фишка", "move(roll)"),
                  ("re:self\\.step\\(",
                   "В методе `move` вызывай `self.step(roll)`: тогда у каждой фишки сработает её собственная версия хода.")],
    ),
]
