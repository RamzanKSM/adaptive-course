"""PY_CLASS_BASIC — «Классы». Taught before: everything up to functions (def, return, parameters, default values),
conditions, loops, lists, slices, string methods. Here: a class as a template — `class`, `__init__` that stores the
parameters in `self.` attributes, one simple method; one object made from the class. Not yet: several objects working
together (next topic), inheritance, tuples, dicts."""
from build import OutputTask

SKILL = "PY_CLASS_BASIC"

NEED_CLASS = ("ClassDef", "Опиши данные в собственном классе: создай его через class — он будет шаблоном для объекта.")
NEED_INIT = ("re:def __init__\\(", "Сохрани данные в объекте через метод __init__ — он сам вызывается, когда создаётся объект.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-class-pet-card", title="Карточка питомца",
        given=["name", "kind", "age"],
        variants=[{"name": '"Barsik"', "kind": '"cat"', "age": "3"},
                  {"name": '"Sharik"', "kind": '"dog"', "age": "5"},
                  {"name": '"Kesha"', "kind": '"parrot"', "age": "2"}],
        hidden=[{"name": '"Murka"', "kind": '"cat"', "age": "7"},
                {"name": '"Rex"', "kind": '"sheepdog"', "age": "1"},
                {"name": '"Pushok"', "kind": '"hamster"', "age": "2"}],
        intro="В ветеринарной клинике на каждого питомца заводят карточку. Все карточки устроены одинаково — "
              "кличка, вид животного и возраст, — поэтому их удобно один раз описать классом, "
              "а потом создавать карточки по этому шаблону.",
        steps=["Создай класс `Pet`. В его методе `__init__(self, name, kind, age)` сохрани параметры в атрибуты объекта: "
               "`self.name`, `self.kind` и `self.age`.",
               "Создай по классу объект из переменных заготовки: `pet = Pet(name, kind, age)`.",
               "Выведи три строки: `Name: …`, `Kind: …` и `Age: …`. Вместо многоточий подставь атрибуты объекта "
               "`pet.name`, `pet.kind` и `pet.age`. После двоеточия — пробел, потом значение."],
        hint="Класс — это только шаблон: сам по себе он ничего не хранит. Запись `Pet(name, kind, age)` создаёт объект "
             "и сама вызывает `__init__`, а строки вида `self.name = name` кладут значения внутрь этого объекта. "
             "Достать их обратно можно через точку: `pet.name`.",
        solution='class Pet:\n    def __init__(self, name, kind, age):\n        self.name = name\n        self.kind = kind\n'
                 '        self.age = age\n\n\npet = Pet(name, kind, age)\nprint(f"Name: {pet.name}")\n'
                 'print(f"Kind: {pet.kind}")\nprint(f"Age: {pet.age}")',
        wrong=[("перепутал порядок аргументов при создании объекта — кличка и вид меняются местами",
                'class Pet:\n    def __init__(self, name, kind, age):\n        self.name = name\n        self.kind = kind\n'
                '        self.age = age\n\n\npet = Pet(kind, name, age)\nprint(f"Name: {pet.name}")\n'
                'print(f"Kind: {pet.kind}")\nprint(f"Age: {pet.age}")'),
               ("записал кличку, вид и возраст прямо в __init__ вместо параметров — карточка всегда одна и та же",
                'class Pet:\n    def __init__(self):\n        self.name = "Barsik"\n        self.kind = "cat"\n'
                '        self.age = 3\n\n\npet = Pet()\nprint(f"Name: {pet.name}")\n'
                'print(f"Kind: {pet.kind}")\nprint(f"Age: {pet.age}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-class-room-floor", title="Ламинат для комнаты",
        given=["length", "width", "price"],
        variants=[{"length": "5", "width": "4", "price": "900"},
                  {"length": "6", "width": "3", "price": "750"},
                  {"length": "4", "width": "4", "price": "1200"}],
        hidden=[{"length": "3", "width": "2", "price": "1000"},
                {"length": "7", "width": "5", "price": "600"},
                {"length": "10", "width": "1", "price": "850"}],
        intro="Ты помогаешь родителям с ремонтом: нужно понять, сколько квадратных метров ламината купить для комнаты "
              "и во сколько это обойдётся. Длина и ширина комнаты в метрах — `length` и `width`, "
              "цена одного квадратного метра ламината — `price`.",
        steps=["Создай класс `Room`. В методе `__init__(self, length, width)` сохрани длину и ширину в атрибуты "
               "`self.length` и `self.width`.",
               "Добавь классу метод `area(self)`, который возвращает площадь комнаты: длину, умноженную на ширину. "
               "Внутри метода бери размеры из атрибутов объекта — через `self.`.",
               "Создай объект `room = Room(length, width)` и выведи строку вида `Room area: 20 sq m`, "
               "получив площадь вызовом `room.area()`.",
               "Ниже выведи строку вида `Floor cost: 18000 rub` — со стоимостью: площадью, умноженной на `price`."],
        hint="Метод — это функция внутри класса. Первым параметром у него всегда идёт `self` — сам объект, "
             "поэтому внутри метода размеры комнаты доступны как `self.length` и `self.width`. "
             "Вызывая метод, не забудь скобки: `room.area()`.",
        solution='class Room:\n    def __init__(self, length, width):\n        self.length = length\n        self.width = width\n\n'
                 '    def area(self):\n        return self.length * self.width\n\n\nroom = Room(length, width)\n'
                 'print(f"Room area: {room.area()} sq m")\nprint(f"Floor cost: {room.area() * price} rub")',
        wrong=[("вызывает метод без скобок — вместо площади печатается описание метода",
                'class Room:\n    def __init__(self, length, width):\n        self.length = length\n        self.width = width\n\n'
                '    def area(self):\n        return self.length * self.width\n\n\nroom = Room(length, width)\n'
                'print(f"Room area: {room.area} sq m")\nprint(f"Floor cost: {room.area() * price} rub")'),
               ("опечатка в __init__: в ширину записана длина — комната считается квадратной",
                'class Room:\n    def __init__(self, length, width):\n        self.length = length\n        self.width = length\n\n'
                '    def area(self):\n        return self.length * self.width\n\n\nroom = Room(length, width)\n'
                'print(f"Room area: {room.area()} sq m")\nprint(f"Floor cost: {room.area() * price} rub")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:def area\\(\\s*self", "Посчитай площадь в методе area(self) внутри класса Room.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-class-book-days", title="Сколько дней читать книгу",
        given=["title", "pages", "per_day"],
        variants=[{"title": '"The Little Prince"', "pages": "96", "per_day": "25"},
                  {"title": '"Dubrovsky"', "pages": "160", "per_day": "40"},
                  {"title": '"Treasure Island"', "pages": "288", "per_day": "30"}],
        hidden=[{"title": '"Kashtanka"', "pages": "48", "per_day": "10"},
                {"title": '"Robinson Crusoe"', "pages": "320", "per_day": "32"},
                {"title": '"Mumu"', "pages": "30", "per_day": "50"},
                {"title": '"The Hobbit"', "pages": "310", "per_day": "20"}],
        intro="Ты составляешь план чтения на каникулы. Для книги известны название `title` и число страниц `pages`, "
              "а `per_day` — сколько страниц ты успеваешь прочитать за день. Нужно узнать, сколько дней уйдёт на книгу.",
        steps=["Создай класс `Book`. В методе `__init__(self, title, pages)` сохрани название и число страниц "
               "в атрибуты `self.title` и `self.pages`.",
               "Добавь метод `days_to_read(self, per_day)`, который возвращает число дней на чтение. "
               "Если последний день получается неполным, он всё равно считается целым днём: "
               "100 страниц по 30 в день — это 4 дня.",
               "Создай объект `book = Book(title, pages)`.",
               "Выведи строку вида `Book: The Little Prince, 96 pages` — с атрибутами `book.title` и `book.pages`, "
               "а второй строкой — `Days to read: …` с результатом метода `days_to_read(per_day)`."],
        hint="`//` даёт число полных дней, а `%` — сколько страниц осталось на последний, неполный день. "
             "Если остаток не равен нулю, к полным дням нужно прибавить ещё один. И печатай атрибуты объекта, "
             "а не сам объект: `book.title`, а не `book`.",
        solution='class Book:\n    def __init__(self, title, pages):\n        self.title = title\n        self.pages = pages\n\n'
                 '    def days_to_read(self, per_day):\n        days = self.pages // per_day\n'
                 '        if self.pages % per_day != 0:\n            days += 1\n        return days\n\n\n'
                 'book = Book(title, pages)\nprint(f"Book: {book.title}, {book.pages} pages")\n'
                 'print(f"Days to read: {book.days_to_read(per_day)}")',
        wrong=[("считает только полные дни — последние страницы не учитываются",
                'class Book:\n    def __init__(self, title, pages):\n        self.title = title\n        self.pages = pages\n\n'
                '    def days_to_read(self, per_day):\n        return self.pages // per_day\n\n\n'
                'book = Book(title, pages)\nprint(f"Book: {book.title}, {book.pages} pages")\n'
                'print(f"Days to read: {book.days_to_read(per_day)}")'),
               ("печатает сам объект вместо его названия",
                'class Book:\n    def __init__(self, title, pages):\n        self.title = title\n        self.pages = pages\n\n'
                '    def days_to_read(self, per_day):\n        days = self.pages // per_day\n'
                '        if self.pages % per_day != 0:\n            days += 1\n        return days\n\n\n'
                'book = Book(title, pages)\nprint(f"Book: {book}, {book.pages} pages")\n'
                'print(f"Days to read: {book.days_to_read(per_day)}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:def days_to_read\\(\\s*self", "Посчитай дни в методе days_to_read(self, per_day) внутри класса Book.")],
    ),
]
