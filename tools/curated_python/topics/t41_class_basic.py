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
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-class-train-ticket", title="Билет на поезд",
        given=["train", "origin", "destination"],
        variants=[{"train": "102", "origin": '"Kazan"', "destination": '"Moscow"'},
                  {"train": "35", "origin": '"Sochi"', "destination": '"Rostov"'},
                  {"train": "418", "origin": '"Perm"', "destination": '"Ufa"'}],
        hidden=[{"train": "7", "origin": '"Tula"', "destination": '"Oryol"'},
                {"train": "250", "origin": '"Omsk"', "destination": '"Tomsk"'},
                {"train": "64", "origin": '"Samara"', "destination": '"Saratov"'}],
        intro="На вокзале печатают билеты на поезда. В каждом билете есть номер поезда, станция отправления и станция "
              "прибытия. Все билеты устроены одинаково, поэтому билет удобно описать классом и создавать по нему объекты.",
        steps=["Создай класс `Ticket`. В его методе `__init__(self, train, origin, destination)` сохрани параметры "
               "в атрибуты объекта: `self.train`, `self.origin` и `self.destination`.",
               "Создай по классу объект из переменных заготовки: `ticket = Ticket(train, origin, destination)`.",
               "Выведи две строки: `Train: …` с атрибутом `ticket.train` и `Route: … - …` — сначала `ticket.origin`, "
               "потом пробел, дефис, пробел и `ticket.destination`. Например, `Route: Kazan - Moscow`."],
        hint="Внутри `__init__` строка `self.origin = origin` кладёт значение параметра в сам объект. "
             "После создания объекта значения достаются через точку: `ticket.origin`. "
             "Следи за порядком аргументов — он должен совпадать с порядком параметров в `__init__`.",
        solution='class Ticket:\n    def __init__(self, train, origin, destination):\n        self.train = train\n'
                 '        self.origin = origin\n        self.destination = destination\n\n\n'
                 'ticket = Ticket(train, origin, destination)\nprint(f"Train: {ticket.train}")\n'
                 'print(f"Route: {ticket.origin} - {ticket.destination}")',
        wrong=[("перепутал станции при создании объекта — маршрут печатается задом наперёд",
                'class Ticket:\n    def __init__(self, train, origin, destination):\n        self.train = train\n'
                '        self.origin = origin\n        self.destination = destination\n\n\n'
                'ticket = Ticket(train, destination, origin)\nprint(f"Train: {ticket.train}")\n'
                'print(f"Route: {ticket.origin} - {ticket.destination}")'),
               ("записал данные билета прямо в __init__ вместо параметров — билет всегда один и тот же",
                'class Ticket:\n    def __init__(self):\n        self.train = 102\n'
                '        self.origin = "Kazan"\n        self.destination = "Moscow"\n\n\n'
                'ticket = Ticket()\nprint(f"Train: {ticket.train}")\n'
                'print(f"Route: {ticket.origin} - {ticket.destination}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-class-cafe-order", title="Заказ в кафе",
        given=["price", "quantity", "paid"],
        variants=[{"price": "80", "quantity": "5", "paid": "500"},
                  {"price": "120", "quantity": "3", "paid": "400"},
                  {"price": "65", "quantity": "6", "paid": "1000"}],
        hidden=[{"price": "100", "quantity": "2", "paid": "200"},
                {"price": "45", "quantity": "7", "paid": "500"},
                {"price": "250", "quantity": "1", "paid": "300"}],
        intro="В кафе покупатель берёт несколько одинаковых пирожков. Цена одного пирожка — `price` рублей, "
              "количество — `quantity`, а `paid` — сколько денег покупатель дал кассиру. "
              "Нужно посчитать сумму заказа и сдачу.",
        steps=["Создай класс `Order`. В методе `__init__(self, price, quantity)` сохрани цену и количество в атрибуты "
               "`self.price` и `self.quantity`.",
               "Добавь классу метод `total(self)`, который возвращает сумму заказа: цену, умноженную на количество. "
               "Внутри метода бери данные из атрибутов объекта — через `self.`.",
               "Создай объект `order = Order(price, quantity)` и выведи строку вида `Order total: 400 rub`, "
               "получив сумму вызовом `order.total()`.",
               "Ниже выведи строку вида `Change: 100 rub` — сдачу: `paid` минус сумма заказа."],
        hint="Метод — это функция внутри класса, и первым параметром у неё идёт `self` — сам объект. "
             "Поэтому в методе цена доступна как `self.price`. Сдача — это то, что дали, минус то, что стоит заказ, "
             "а не наоборот.",
        solution='class Order:\n    def __init__(self, price, quantity):\n        self.price = price\n        self.quantity = quantity\n\n'
                 '    def total(self):\n        return self.price * self.quantity\n\n\norder = Order(price, quantity)\n'
                 'print(f"Order total: {order.total()} rub")\nprint(f"Change: {paid - order.total()} rub")',
        wrong=[("в методе складывает цену и количество вместо умножения",
                'class Order:\n    def __init__(self, price, quantity):\n        self.price = price\n        self.quantity = quantity\n\n'
                '    def total(self):\n        return self.price + self.quantity\n\n\norder = Order(price, quantity)\n'
                'print(f"Order total: {order.total()} rub")\nprint(f"Change: {paid - order.total()} rub")'),
               ("считает сдачу наоборот — из суммы заказа вычитает деньги покупателя",
                'class Order:\n    def __init__(self, price, quantity):\n        self.price = price\n        self.quantity = quantity\n\n'
                '    def total(self):\n        return self.price * self.quantity\n\n\norder = Order(price, quantity)\n'
                'print(f"Order total: {order.total()} rub")\nprint(f"Change: {order.total() - paid} rub")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:def total\\(\\s*self", "Посчитай сумму заказа в методе total(self) внутри класса Order.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-class-phone-minutes", title="Минуты сверх тарифа",
        given=["owner", "minutes", "limit", "price"],
        variants=[{"owner": '"Anya"', "minutes": "420", "limit": "400", "price": "3"},
                  {"owner": '"Boris"', "minutes": "150", "limit": "300", "price": "2"},
                  {"owner": '"Vika"', "minutes": "655", "limit": "500", "price": "4"}],
        hidden=[{"owner": '"Gleb"', "minutes": "300", "limit": "300", "price": "5"},
                {"owner": '"Dasha"', "minutes": "301", "limit": "300", "price": "5"},
                {"owner": '"Egor"', "minutes": "0", "limit": "200", "price": "3"},
                {"owner": '"Zhenya"', "minutes": "1000", "limit": "600", "price": "2"}],
        intro="Мобильный оператор считает, сколько абонент должен доплатить за месяц. В тариф входит `limit` минут "
              "разговоров. Если абонент `owner` проговорил `minutes` минут и это больше, чем входит в тариф, "
              "каждая лишняя минута стоит `price` рублей. Если не больше — доплачивать ничего не нужно.",
        steps=["Создай класс `Phone`. В методе `__init__(self, owner, minutes)` сохрани имя абонента и число минут "
               "в атрибуты `self.owner` и `self.minutes`.",
               "Добавь метод `extra_cost(self, limit, price)`, который возвращает доплату. Если `self.minutes` больше "
               "`limit`, доплата — число лишних минут (`self.minutes - limit`), умноженное на `price`. Иначе метод "
               "возвращает 0.",
               "Создай объект `phone = Phone(owner, minutes)`.",
               "Выведи строку вида `Owner: Anya, 420 min` — с атрибутами `phone.owner` и `phone.minutes`, "
               "а второй строкой — `Extra cost: …` с результатом `phone.extra_cost(limit, price)` и словом `rub` "
               "через пробел, например `Extra cost: 60 rub`."],
        hint="Платить нужно только за минуты сверх тарифа, а не за все: из 420 минут при тарифе на 400 "
             "лишних всего 20. Если минут меньше лимита, разность получится отрицательной — поэтому сначала "
             "проверь условие через `if`.",
        solution='class Phone:\n    def __init__(self, owner, minutes):\n        self.owner = owner\n        self.minutes = minutes\n\n'
                 '    def extra_cost(self, limit, price):\n        if self.minutes > limit:\n'
                 '            return (self.minutes - limit) * price\n        return 0\n\n\n'
                 'phone = Phone(owner, minutes)\nprint(f"Owner: {phone.owner}, {phone.minutes} min")\n'
                 'print(f"Extra cost: {phone.extra_cost(limit, price)} rub")',
        wrong=[("при превышении берёт плату за все минуты, а не только за лишние",
                'class Phone:\n    def __init__(self, owner, minutes):\n        self.owner = owner\n        self.minutes = minutes\n\n'
                '    def extra_cost(self, limit, price):\n        if self.minutes > limit:\n'
                '            return self.minutes * price\n        return 0\n\n\n'
                'phone = Phone(owner, minutes)\nprint(f"Owner: {phone.owner}, {phone.minutes} min")\n'
                'print(f"Extra cost: {phone.extra_cost(limit, price)} rub")'),
               ("не проверяет лимит — при малом числе минут доплата получается отрицательной",
                'class Phone:\n    def __init__(self, owner, minutes):\n        self.owner = owner\n        self.minutes = minutes\n\n'
                '    def extra_cost(self, limit, price):\n        return (self.minutes - limit) * price\n\n\n'
                'phone = Phone(owner, minutes)\nprint(f"Owner: {phone.owner}, {phone.minutes} min")\n'
                'print(f"Extra cost: {phone.extra_cost(limit, price)} rub")')],
        constructs=["class", "if"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:def extra_cost\\(\\s*self", "Посчитай доплату в методе extra_cost(self, limit, price) внутри класса Phone.")],
    ),
]
