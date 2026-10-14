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
        skill=SKILL, difficulty=1, slug="py-init-new-hero", title="Новый герой",
        given=["name", "health"],
        variants=[{"name": '"Lina"', "health": "80"}, {"name": '"Grom"', "health": "120"}, {"name": '"Iskra"', "health": "95"}],
        hidden=[{"name": '"Shadow"', "health": "60"}, {"name": '"Storm"', "health": "150"}, {"name": '"Hedgehog"', "health": "100"}],
        intro="В игре при создании персонажа игрок выбирает имя и здоровье, а уровень и золото у всех новичков одинаковые: "
              "первый уровень и пустой кошелёк. Всё это должен подготовить метод `__init__`.",
        steps=["Создай класс `Hero` с методом `__init__(self, name, health)`. Сохрани имя и здоровье в атрибуты "
               "`self.name` и `self.health`, а ещё задай стартовые значения, которые при создании не передаются: "
               "`self.level = 1` и `self.gold = 0`.",
               "Последней строкой внутри `__init__` выведи строку вида `Hero Lina is ready` — только вместо «Lina» "
               "имя из параметра `name`.",
               "Создай героя: `hero = Hero(name, health)`. Отдельно вызывать `__init__` не нужно.",
               "Выведи строку вида `Lina: level 1, health 80, gold 0` — все значения бери из атрибутов объекта `hero`."],
        hint="`__init__` срабатывает сам в момент `Hero(name, health)`: Python создаёт пустой объект, передаёт его "
             "в `__init__` как `self`, а остальные аргументы — по порядку в `name` и `health`. "
             "Если вызвать `__init__` ещё раз вручную, он выполнится второй раз.",
        solution='class Hero:\n    def __init__(self, name, health):\n        self.name = name\n        self.health = health\n'
                 '        self.level = 1\n        self.gold = 0\n        print(f"Hero {name} is ready")\n\n\n'
                 'hero = Hero(name, health)\n'
                 'print(f"{hero.name}: level {hero.level}, health {hero.health}, gold {hero.gold}")',
        wrong=[("вызывает __init__ ещё раз вручную — приветствие печатается дважды",
                'class Hero:\n    def __init__(self, name, health):\n        self.name = name\n        self.health = health\n'
                '        self.level = 1\n        self.gold = 0\n        print(f"Hero {name} is ready")\n\n\n'
                'hero = Hero(name, health)\nhero.__init__(name, health)\n'
                'print(f"{hero.name}: level {hero.level}, health {hero.health}, gold {hero.gold}")'),
               ("записывает здоровье числом 100 вместо параметра health — у всех героев одинаковое здоровье",
                'class Hero:\n    def __init__(self, name, health):\n        self.name = name\n        self.health = 100\n'
                '        self.level = 1\n        self.gold = 0\n        print(f"Hero {name} is ready")\n\n\n'
                'hero = Hero(name, health)\n'
                'print(f"{hero.name}: level {hero.level}, health {hero.health}, gold {hero.gold}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-init-table-booking", title="Бронь столика",
        given=["name1", "name2", "guests2"],
        variants=[{"name1": '"Anna"', "name2": '"Igor"', "guests2": "5"},
                  {"name1": '"Marat"', "name2": '"Olga"', "guests2": "4"},
                  {"name1": '"Sveta"', "name2": '"Pyotr"', "guests2": "8"}],
        hidden=[{"name1": '"Yulya"', "name2": '"Denis"', "guests2": "3"},
                {"name1": '"Akhmed"', "name2": '"Nina"', "guests2": "1"},
                {"name1": '"Lev"', "name2": '"Kira"', "guests2": "6"}],
        intro="В ресторане чаще всего бронируют столик на двоих, поэтому при брони число гостей можно не называть — "
              "тогда их считается 2. Сегодня позвонили два человека: `name1` не назвал число гостей, "
              "а `name2` сказал, что их будет `guests2`.",
        steps=["Создай класс `Booking`. Его метод `__init__` принимает имя `name` и число гостей `guests` "
               "со значением по умолчанию 2: `def __init__(self, name, guests=2)`. Сохрани оба значения "
               "в атрибуты `self.name` и `self.guests`.",
               "Создай первую бронь, передав только имя: `booking1 = Booking(name1)`. Вторую — с именем и числом гостей: "
               "`booking2 = Booking(name2, guests2)`.",
               "Для каждой брони выведи строку вида `Booking for Anna, guests: 2` — сначала для первой, потом для второй."],
        hint="Значения по умолчанию у `__init__` работают так же, как у обычной функции: если аргумент не передали, "
             "параметр получает значение по умолчанию, а если передали — то, что передали. Сохранять в атрибут "
             "нужно именно параметр `guests`, а не число 2.",
        solution='class Booking:\n    def __init__(self, name, guests=2):\n        self.name = name\n        self.guests = guests\n\n\n'
                 'booking1 = Booking(name1)\nbooking2 = Booking(name2, guests2)\n'
                 'print(f"Booking for {booking1.name}, guests: {booking1.guests}")\n'
                 'print(f"Booking for {booking2.name}, guests: {booking2.guests}")',
        wrong=[("в __init__ всегда записывает 2 гостя, не глядя на параметр",
                'class Booking:\n    def __init__(self, name, guests=2):\n        self.name = name\n        self.guests = 2\n\n\n'
                'booking1 = Booking(name1)\nbooking2 = Booking(name2, guests2)\n'
                'print(f"Booking for {booking1.name}, guests: {booking1.guests}")\n'
                'print(f"Booking for {booking2.name}, guests: {booking2.guests}")'),
               ("поставил значением по умолчанию 1 гостя вместо 2",
                'class Booking:\n    def __init__(self, name, guests=1):\n        self.name = name\n        self.guests = guests\n\n\n'
                'booking1 = Booking(name1)\nbooking2 = Booking(name2, guests2)\n'
                'print(f"Booking for {booking1.name}, guests: {booking1.guests}")\n'
                'print(f"Booking for {booking2.name}, guests: {booking2.guests}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:def __init__\\([^)]*guests\\s*=\\s*2",
                   "Сделай число гостей параметром __init__ со значением по умолчанию: def __init__(self, name, guests=2).")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-init-kitchen-timers", title="Кухонные таймеры",
        given=["durations"],
        variants=[{"durations": "[125, 60, 59]"}, {"durations": "[300, 95, 610]"}, {"durations": "[45, 3600, 181]"}],
        hidden=[{"durations": "[1]"}, {"durations": "[61, 600, 7, 1234]"}, {"durations": "[3599, 120]"}],
        intro="Умная кухня ставит несколько таймеров сразу и получает их длительности в секундах — список `durations`. "
              "Человеку удобнее видеть минуты и секунды, поэтому таймер сам раскладывает время, как только его создают.",
        steps=["Создай класс `Timer`. Его метод `__init__(self, total)` получает время в секундах и сразу "
               "раскладывает его на два атрибута: `self.minutes` — сколько полных минут, "
               "`self.seconds` — сколько секунд остаётся сверх полных минут.",
               "Пройди циклом по списку `durations` и для каждого числа создай объект `Timer`.",
               "Для каждого таймера выведи строку вида `Timer 1: 2 min 5 sec` — номер таймера по порядку, начиная с 1, "
               "а потом минуты и секунды из атрибутов объекта."],
        hint="В `__init__` можно не только сохранять параметры, но и вычислять из них новые атрибуты. "
             "Полные минуты даёт целочисленное деление `total // 60`, а остаток секунд — `total % 60`.",
        solution='class Timer:\n    def __init__(self, total):\n        self.minutes = total // 60\n        self.seconds = total % 60\n\n\n'
                 'number = 1\nfor total in durations:\n    timer = Timer(total)\n'
                 '    print(f"Timer {number}: {timer.minutes} min {timer.seconds} sec")\n    number += 1',
        wrong=[("сохраняет в seconds всё время целиком, а не остаток",
                'class Timer:\n    def __init__(self, total):\n        self.minutes = total // 60\n        self.seconds = total\n\n\n'
                'number = 1\nfor total in durations:\n    timer = Timer(total)\n'
                '    print(f"Timer {number}: {timer.minutes} min {timer.seconds} sec")\n    number += 1'),
               ("делит обычным делением — минуты получаются дробными",
                'class Timer:\n    def __init__(self, total):\n        self.minutes = total / 60\n        self.seconds = total % 60\n\n\n'
                'number = 1\nfor total in durations:\n    timer = Timer(total)\n'
                '    print(f"Timer {number}: {timer.minutes} min {timer.seconds} sec")\n    number += 1')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-init-bank-account", title="Новый банковский счёт",
        given=["owner", "deposit"],
        variants=[{"owner": '"Anya"', "deposit": "500"}, {"owner": '"Boris"', "deposit": "1200"},
                  {"owner": '"Vika"', "deposit": "75"}],
        hidden=[{"owner": '"Gleb"', "deposit": "0"}, {"owner": '"Dasha"', "deposit": "10000"},
                {"owner": '"Egor"', "deposit": "330"}],
        intro="Банк открывает новый счёт на имя клиента `owner`. На только что открытом счёте денег нет, "
              "но банк дарит каждому новому клиенту 100 бонусных рублей. Сразу после открытия клиент кладёт "
              "на счёт `deposit` рублей.",
        steps=["Создай класс `Account` с методом `__init__(self, owner)`. Сохрани имя в атрибут `self.owner`, "
               "а ещё задай стартовые значения, которые при создании не передаются: `self.balance = 0` "
               "и `self.bonus = 100`.",
               "Создай счёт: `account = Account(owner)`. Выведи строку вида `New account: Anya` и под ней строку "
               "вида `Balance: 0, bonus: 100` — значения бери из атрибутов объекта.",
               "Положи деньги на счёт: увеличь `account.balance` на `deposit`.",
               "Выведи строку вида `Available: 600 rub` — сумму баланса и бонуса из атрибутов объекта."],
        hint="`__init__` вызывается сам при `Account(owner)`. В нём можно задавать не только атрибуты из параметров, "
             "но и такие, у которых у всех новых объектов одно и то же начальное значение — как `self.balance = 0`. "
             "Потом атрибут можно менять снаружи: `account.balance += deposit`.",
        solution='class Account:\n    def __init__(self, owner):\n        self.owner = owner\n        self.balance = 0\n'
                 '        self.bonus = 100\n\n\naccount = Account(owner)\nprint(f"New account: {account.owner}")\n'
                 'print(f"Balance: {account.balance}, bonus: {account.bonus}")\naccount.balance += deposit\n'
                 'print(f"Available: {account.balance + account.bonus} rub")',
        wrong=[("перепутал стартовые значения — положил 100 на баланс, а бонус оставил нулевым",
                'class Account:\n    def __init__(self, owner):\n        self.owner = owner\n        self.balance = 100\n'
                '        self.bonus = 0\n\n\naccount = Account(owner)\nprint(f"New account: {account.owner}")\n'
                'print(f"Balance: {account.balance}, bonus: {account.bonus}")\naccount.balance += deposit\n'
                'print(f"Available: {account.balance + account.bonus} rub")'),
               ("заменяет баланс взносом, а не прибавляет к нему, и забывает про бонус в итоге",
                'class Account:\n    def __init__(self, owner):\n        self.owner = owner\n        self.balance = 0\n'
                '        self.bonus = 100\n\n\naccount = Account(owner)\nprint(f"New account: {account.owner}")\n'
                'print(f"Balance: {account.balance}, bonus: {account.bonus}")\naccount.balance = deposit\n'
                'print(f"Available: {account.balance} rub")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-init-coffee-order", title="Заказы в кофейне",
        given=["drink1", "drink2", "sugar2"],
        variants=[{"drink1": '"latte"', "drink2": '"cappuccino"', "sugar2": "2"},
                  {"drink1": '"americano"', "drink2": '"mocha"', "sugar2": "1"},
                  {"drink1": '"flat white"', "drink2": '"raf"', "sugar2": "3"}],
        hidden=[{"drink1": '"espresso"', "drink2": '"latte"', "sugar2": "0"},
                {"drink1": '"cocoa"', "drink2": '"americano"', "sugar2": "5"},
                {"drink1": '"mocha"', "drink2": '"tea"', "sugar2": "1"}],
        intro="В кофейне большинство гостей берут средний стакан без сахара, поэтому кассир указывает размер и сахар, "
              "только если гость попросил что-то другое. Сегодня первый гость заказал просто `drink1`, второй — "
              "`drink2` с `sugar2` ложками сахара, а третий — снова `drink1`, но в большом стакане.",
        steps=["Создай класс `Coffee`. Его метод `__init__` принимает напиток `drink`, размер `size` со значением "
               "по умолчанию `\"medium\"` и число ложек сахара `sugar` со значением по умолчанию 0: "
               "`def __init__(self, drink, size=\"medium\", sugar=0)`. Сохрани все три значения в атрибуты "
               "`self.drink`, `self.size` и `self.sugar`.",
               "Создай три заказа: `order1 = Coffee(drink1)`; `order2 = Coffee(drink2, sugar=sugar2)` — сахар "
               "передан по имени, а размер остаётся по умолчанию; `order3 = Coffee(drink1, \"large\")`.",
               "Для каждого заказа по порядку выведи строку вида `latte, medium, sugar 0` — напиток, размер и сахар "
               "из атрибутов объекта."],
        hint="Если записать второй заказ как `Coffee(drink2, sugar2)`, число сахара по порядку попадёт в параметр "
             "`size` — ведь он идёт вторым. Чтобы пропустить параметр и задать следующий, передай аргумент по имени: "
             "`sugar=sugar2`.",
        solution='class Coffee:\n    def __init__(self, drink, size="medium", sugar=0):\n        self.drink = drink\n'
                 '        self.size = size\n        self.sugar = sugar\n\n\norder1 = Coffee(drink1)\n'
                 'order2 = Coffee(drink2, sugar=sugar2)\norder3 = Coffee(drink1, "large")\n'
                 'print(f"{order1.drink}, {order1.size}, sugar {order1.sugar}")\n'
                 'print(f"{order2.drink}, {order2.size}, sugar {order2.sugar}")\n'
                 'print(f"{order3.drink}, {order3.size}, sugar {order3.sugar}")',
        wrong=[("передаёт сахар вторым аргументом без имени — число попадает в размер стакана",
                'class Coffee:\n    def __init__(self, drink, size="medium", sugar=0):\n        self.drink = drink\n'
                '        self.size = size\n        self.sugar = sugar\n\n\norder1 = Coffee(drink1)\n'
                'order2 = Coffee(drink2, sugar2)\norder3 = Coffee(drink1, "large")\n'
                'print(f"{order1.drink}, {order1.size}, sugar {order1.sugar}")\n'
                'print(f"{order2.drink}, {order2.size}, sugar {order2.sugar}")\n'
                'print(f"{order3.drink}, {order3.size}, sugar {order3.sugar}")'),
               ("в __init__ всегда записывает средний размер, не глядя на параметр size",
                'class Coffee:\n    def __init__(self, drink, size="medium", sugar=0):\n        self.drink = drink\n'
                '        self.size = "medium"\n        self.sugar = sugar\n\n\norder1 = Coffee(drink1)\n'
                'order2 = Coffee(drink2, sugar=sugar2)\norder3 = Coffee(drink1, "large")\n'
                'print(f"{order1.drink}, {order1.size}, sugar {order1.sugar}")\n'
                'print(f"{order2.drink}, {order2.size}, sugar {order2.sugar}")\n'
                'print(f"{order3.drink}, {order3.size}, sugar {order3.sugar}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:def __init__\\([^)]*size\\s*=\\s*[\"']medium[\"'][^)]*sugar\\s*=\\s*0",
                   "Сделай размер и сахар параметрами __init__ со значениями по умолчанию: "
                   "def __init__(self, drink, size=\"medium\", sugar=0).")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-init-school-email", title="Школьная почта",
        given=["people"],
        variants=[{"people": '["Anya Petrova", "Boris Li", "Vika Smirnova"]'},
                  {"people": '["Gleb Orlov", "Dasha Kuznetsova"]'},
                  {"people": '["Egor Ivanov", "Zoya Volkova", "Igor Sokolov", "Lena Kim"]'}],
        hidden=[{"people": '["Masha Popova"]'},
                {"people": '["Nikita Fedorov", "Olya Belova", "Pavel Wu"]'},
                {"people": '["Roma Zaitsev", "Sonya Lebedeva"]'}],
        intro="Школа заводит ученикам электронную почту. Адрес составляется из имени и фамилии: первая буква имени, "
              "точка и первые шесть букв фамилии, всё маленькими буквами, а после — `@school.ru`. "
              "В списке `people` — имена и фамилии учеников через пробел.",
        steps=["Создай класс `Pupil`. Его метод `__init__(self, first, last)` сохраняет имя и фамилию в атрибуты "
               "`self.first` и `self.last` и сразу вычисляет из них атрибут `self.email`.",
               "Адрес составь так: первая буква имени, точка, первые 6 букв фамилии (если фамилия короче — вся фамилия) "
               "и `@school.ru`, и всё это маленькими буквами. Для `Anya Petrova` получится `a.petrov@school.ru`.",
               "Пройди циклом по списку `people`, раздели каждую строку по пробелу на имя и фамилию и создай "
               "объект `Pupil`.",
               "Для каждого ученика выведи строку вида `Anya Petrova: a.petrov@school.ru` — имя и фамилию "
               "из атрибутов объекта и его адрес."],
        hint="В `__init__` можно вычислять новые атрибуты из параметров. Первые 6 букв даёт срез `last[:6]` — "
             "если в строке меньше 6 символов, срез просто вернёт её целиком. Маленькие буквы даёт метод `.lower()`, "
             "а разделить строку по пробелу — `.split()`.",
        solution='class Pupil:\n    def __init__(self, first, last):\n        self.first = first\n        self.last = last\n'
                 '        self.email = (first[0] + "." + last[:6]).lower() + "@school.ru"\n\n\n'
                 'for person in people:\n    parts = person.split()\n    pupil = Pupil(parts[0], parts[1])\n'
                 '    print(f"{pupil.first} {pupil.last}: {pupil.email}")',
        wrong=[("забыл перевести адрес в маленькие буквы",
                'class Pupil:\n    def __init__(self, first, last):\n        self.first = first\n        self.last = last\n'
                '        self.email = first[0] + "." + last[:6] + "@school.ru"\n\n\n'
                'for person in people:\n    parts = person.split()\n    pupil = Pupil(parts[0], parts[1])\n'
                '    print(f"{pupil.first} {pupil.last}: {pupil.email}")'),
               ("берёт в срез пять букв фамилии вместо шести",
                'class Pupil:\n    def __init__(self, first, last):\n        self.first = first\n        self.last = last\n'
                '        self.email = (first[0] + "." + last[:5]).lower() + "@school.ru"\n\n\n'
                'for person in people:\n    parts = person.split()\n    pupil = Pupil(parts[0], parts[1])\n'
                '    print(f"{pupil.first} {pupil.last}: {pupil.email}")'),
               ("берёт фамилию целиком, без среза",
                'class Pupil:\n    def __init__(self, first, last):\n        self.first = first\n        self.last = last\n'
                '        self.email = (first[0] + "." + last).lower() + "@school.ru"\n\n\n'
                'for person in people:\n    parts = person.split()\n    pupil = Pupil(parts[0], parts[1])\n'
                '    print(f"{pupil.first} {pupil.last}: {pupil.email}")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:self\\.email\\s*=", "Вычисли адрес прямо в __init__ и сохрани его в атрибут self.email.")],
    ),
]
