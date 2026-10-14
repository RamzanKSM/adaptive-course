"""PY_PROPERTY_BASIC — «Свойства @property». Taught before: everything up to functions, classes, creating objects,
__init__, methods and self, internal `_x` attributes changed through checking methods. Here: @property — a method
read like an attribute, without parentheses; it is computed anew on every read, so it follows changes of the
attributes; a read-only view of an internal attribute. Not yet: @x.setter, inheritance, tuples, dicts."""
from build import OutputTask

SKILL = "PY_PROPERTY_BASIC"

NEED_CLASS = ("ClassDef", "Опиши объект в собственном классе через class.")
NEED_PROPERTY = ("re:@property", "Сделай вычисляемое значение свойством: поставь над методом @property, "
                                  "и его можно будет читать как атрибут, без скобок.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-prop-name-badge", title="Бейдж участника",
        given=["first_name", "last_name"],
        variants=[{"first_name": '"Anna"', "last_name": '"Petrova"'},
                  {"first_name": '"Timur"', "last_name": '"Aliev"'},
                  {"first_name": '"Vera"', "last_name": '"Smirnova"'}],
        hidden=[{"first_name": '"Oleg"', "last_name": '"Kim"'},
                {"first_name": '"Zarina"', "last_name": '"Yusupova"'},
                {"first_name": '"Yan"', "last_name": '"Orlov"'}],
        intro="На олимпиаде каждому участнику печатают бейдж. Имя и фамилия хранятся отдельно, а на бейдже нужны "
              "полное имя и короткая подпись. Их удобно сделать свойствами: читаются как обычные атрибуты, "
              "а вычисляются из имени и фамилии.",
        steps=["Создай класс `Person`. В `__init__(self, first_name, last_name)` сохрани имя и фамилию в атрибуты "
               "`self.first_name` и `self.last_name`.",
               "Добавь свойство `full_name` — метод с `@property` над ним, который возвращает имя и фамилию через пробел.",
               "Добавь свойство `short_name`, которое возвращает первую букву имени, точку, пробел и фамилию: "
               "для Anna Petrova это `A. Petrova`.",
               "Создай объект `person = Person(first_name, last_name)` и выведи две строки: `Full name: …` "
               "со значением `person.full_name` и `Short: …` со значением `person.short_name`. Свойства читай без скобок."],
        hint="`@property` пишется на отдельной строке прямо над `def`. После этого `person.full_name` вызывает метод сам, "
             "без скобок. Без `@property` запись без скобок вернула бы сам метод, а не строку. "
             "Первая буква строки — `self.first_name[0]`.",
        solution='class Person:\n    def __init__(self, first_name, last_name):\n        self.first_name = first_name\n'
                 '        self.last_name = last_name\n\n    @property\n    def full_name(self):\n'
                 '        return self.first_name + " " + self.last_name\n\n    @property\n    def short_name(self):\n'
                 '        return self.first_name[0] + ". " + self.last_name\n\n\nperson = Person(first_name, last_name)\n'
                 'print(f"Full name: {person.full_name}")\nprint(f"Short: {person.short_name}")',
        wrong=[("забыл @property у short_name — без скобок печатается описание метода, а не подпись",
                'class Person:\n    def __init__(self, first_name, last_name):\n        self.first_name = first_name\n'
                '        self.last_name = last_name\n\n    @property\n    def full_name(self):\n'
                '        return self.first_name + " " + self.last_name\n\n    def short_name(self):\n'
                '        return self.first_name[0] + ". " + self.last_name\n\n\nperson = Person(first_name, last_name)\n'
                'print(f"Full name: {person.full_name}")\nprint(f"Short: {person.short_name}")'),
               ("берёт первую букву фамилии вместо имени",
                'class Person:\n    def __init__(self, first_name, last_name):\n        self.first_name = first_name\n'
                '        self.last_name = last_name\n\n    @property\n    def full_name(self):\n'
                '        return self.first_name + " " + self.last_name\n\n    @property\n    def short_name(self):\n'
                '        return self.last_name[0] + ". " + self.last_name\n\n\nperson = Person(first_name, last_name)\n'
                'print(f"Full name: {person.full_name}")\nprint(f"Short: {person.short_name}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PROPERTY],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-prop-pizza-order", title="Заказ пиццы",
        given=["pizzas", "drinks", "extra"],
        variants=[{"pizzas": "2", "drinks": "2", "extra": "1"},
                  {"pizzas": "1", "drinks": "3", "extra": "2"},
                  {"pizzas": "3", "drinks": "0", "extra": "4"}],
        hidden=[{"pizzas": "0", "drinks": "5", "extra": "1"},
                {"pizzas": "4", "drinks": "4", "extra": "0"},
                {"pizzas": "10", "drinks": "1", "extra": "3"},
                {"pizzas": "1", "drinks": "1", "extra": "1"}],
        intro="Ты оформляешь заказ в пиццерии: пицца стоит 500 руб., напиток — 100 руб. Сначала заказали `pizzas` пицц "
              "и `drinks` напитков, а потом друзья попросили добавить ещё `extra` пицц. Сумма заказа должна "
              "сама пересчитываться после каждого изменения.",
        steps=["Создай класс `Order`. В `__init__(self, pizzas, drinks)` сохрани количества в атрибуты "
               "`self.pizzas` и `self.drinks`.",
               "Добавь свойство `total` (метод с `@property`), которое возвращает стоимость заказа: "
               "500 руб. за каждую пиццу и 100 руб. за каждый напиток.",
               "Создай заказ `order = Order(pizzas, drinks)` и выведи строку вида `Total: 1200 rub` — со значением `order.total`, "
               "прочитанным без скобок.",
               "Увеличь атрибут `order.pizzas` на `extra` и снова выведи строку того же вида с `order.total`."],
        hint="Свойство вычисляется заново при каждом чтении `order.total`, поэтому оно всегда учитывает текущие атрибуты. "
             "А если посчитать сумму один раз в `__init__` и сохранить в атрибут, она так и останется старой. "
             "И добавлять пиццы нужно в атрибут объекта `order.pizzas`, а не в переменную `pizzas`.",
        solution='class Order:\n    def __init__(self, pizzas, drinks):\n        self.pizzas = pizzas\n        self.drinks = drinks\n\n'
                 '    @property\n    def total(self):\n        return self.pizzas * 500 + self.drinks * 100\n\n\n'
                 'order = Order(pizzas, drinks)\nprint(f"Total: {order.total} rub")\norder.pizzas += extra\n'
                 'print(f"Total: {order.total} rub")',
        wrong=[("считает сумму один раз в __init__ — после добавления пицц она не меняется",
                'class Order:\n    def __init__(self, pizzas, drinks):\n        self.pizzas = pizzas\n        self.drinks = drinks\n'
                '        self.total = pizzas * 500 + drinks * 100\n\n\n'
                'order = Order(pizzas, drinks)\nprint(f"Total: {order.total} rub")\norder.pizzas += extra\n'
                'print(f"Total: {order.total} rub")'),
               ("добавляет пиццы в переменную pizzas, а не в атрибут заказа",
                'class Order:\n    def __init__(self, pizzas, drinks):\n        self.pizzas = pizzas\n        self.drinks = drinks\n\n'
                '    @property\n    def total(self):\n        return self.pizzas * 500 + self.drinks * 100\n\n\n'
                'order = Order(pizzas, drinks)\nprint(f"Total: {order.total} rub")\npizzas += extra\n'
                'print(f"Total: {order.total} rub")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PROPERTY],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prop-player-level", title="Опыт и уровень игрока",
        given=["rewards"],
        variants=[{"rewards": "[40, 75, -20, 130]"}, {"rewards": "[100, 50, 50]"}, {"rewards": "[-30, 90, 15, 300]"}],
        hidden=[{"rewards": "[10]"}, {"rewards": "[99, 1, -5, 250]"}, {"rewards": "[0, 500]"}, {"rewards": "[60, 60, 60]"}],
        intro="В игре за задания дают очки опыта — список `rewards`. Иногда в список по ошибке попадает "
              "отрицательное число или ноль: такие награды игра пропускает. Каждые полные 100 очков опыта "
              "поднимают уровень на 1, а начинает игрок с первого уровня.",
        steps=["Создай класс `Player`. В `__init__(self)` заведи внутренний атрибут `self._xp = 0`.",
               "Добавь метод `add_xp(self, amount)`: он прибавляет `amount` к опыту, только если это число больше нуля.",
               "Добавь три свойства с `@property`: `xp` возвращает опыт, `level` — уровень, а `to_next` — сколько очков "
               "осталось набрать до следующего уровня. Например, при 140 очках уровень 2 и до следующего 60.",
               "Создай игрока и пройди циклом по `rewards`: передай каждую награду в `add_xp`, а после неё выведи строку "
               "вида `XP: 140, level: 2, to next: 60` со значениями `player.xp`, `player.level` "
               "и `player.to_next` — без скобок."],
        hint="Уровень и остаток можно вычислять прямо в свойствах из `self._xp`: число полных сотен даёт `// 100`, "
             "а сколько очков набрано сверх них — `% 100`. Не забудь, что при 0 очках уровень уже первый.",
        solution='class Player:\n    def __init__(self):\n        self._xp = 0\n\n    def add_xp(self, amount):\n'
                 '        if amount > 0:\n            self._xp += amount\n\n    @property\n    def xp(self):\n        return self._xp\n\n'
                 '    @property\n    def level(self):\n        return self._xp // 100 + 1\n\n'
                 '    @property\n    def to_next(self):\n        return 100 - self._xp % 100\n\n\n'
                 'player = Player()\nfor reward in rewards:\n    player.add_xp(reward)\n'
                 '    print(f"XP: {player.xp}, level: {player.level}, to next: {player.to_next}")',
        wrong=[("считает уровень без +1 — новичок оказывается на нулевом уровне",
                'class Player:\n    def __init__(self):\n        self._xp = 0\n\n    def add_xp(self, amount):\n'
                '        if amount > 0:\n            self._xp += amount\n\n    @property\n    def xp(self):\n        return self._xp\n\n'
                '    @property\n    def level(self):\n        return self._xp // 100\n\n'
                '    @property\n    def to_next(self):\n        return 100 - self._xp % 100\n\n\n'
                'player = Player()\nfor reward in rewards:\n    player.add_xp(reward)\n'
                '    print(f"XP: {player.xp}, level: {player.level}, to next: {player.to_next}")'),
               ("забыл @property у to_next — без скобок печатается описание метода, а не число",
                'class Player:\n    def __init__(self):\n        self._xp = 0\n\n    def add_xp(self, amount):\n'
                '        if amount > 0:\n            self._xp += amount\n\n    @property\n    def xp(self):\n        return self._xp\n\n'
                '    @property\n    def level(self):\n        return self._xp // 100 + 1\n\n'
                '    def to_next(self):\n        return 100 - self._xp % 100\n\n\n'
                'player = Player()\nfor reward in rewards:\n    player.add_xp(reward)\n'
                '    print(f"XP: {player.xp}, level: {player.level}, to next: {player.to_next}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PROPERTY],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-prop-temperature", title="Градусы в разных шкалах",
        given=["celsius"],
        variants=[{"celsius": "25"}, {"celsius": "-10"}, {"celsius": "35"}],
        hidden=[{"celsius": "0"}, {"celsius": "-40"}, {"celsius": "100"}],
        intro="Метеостанция хранит температуру в градусах Цельсия, а на табло для туристов нужно показать её ещё "
              "в градусах Фаренгейта и в кельвинах. Эти значения удобно сделать свойствами: они читаются как атрибуты, "
              "а вычисляются из градусов Цельсия.",
        steps=["Создай класс `Temperature`. В `__init__(self, celsius)` сохрани температуру в атрибут `self.celsius`.",
               "Добавь свойство `fahrenheit` — метод с `@property` над ним. Оно возвращает температуру по Фаренгейту: "
               "градусы Цельсия умножить на 9, разделить нацело на 5 и прибавить 32.",
               "Добавь свойство `kelvin`, которое возвращает градусы Цельсия плюс 273.",
               "Создай объект `temp = Temperature(celsius)` и выведи три строки: `Celsius: …`, `Fahrenheit: …` и "
               "`Kelvin: …` со значениями `temp.celsius`, `temp.fahrenheit` и `temp.kelvin`. Свойства читай без скобок."],
        hint="`@property` ставится на отдельной строке прямо над `def`, и тогда `temp.fahrenheit` работает без скобок. "
             "Порядок действий в формуле важен: сначала умножение и деление, потом прибавление 32. "
             "Деление нацело `//` даёт целое число, а обычное `/` — дробное вроде `77.0`.",
        solution='class Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n'
                 '    @property\n    def fahrenheit(self):\n        return self.celsius * 9 // 5 + 32\n\n'
                 '    @property\n    def kelvin(self):\n        return self.celsius + 273\n\n\n'
                 'temp = Temperature(celsius)\nprint(f"Celsius: {temp.celsius}")\n'
                 'print(f"Fahrenheit: {temp.fahrenheit}")\nprint(f"Kelvin: {temp.kelvin}")',
        wrong=[("сначала прибавляет 32, а потом умножает — формула перепутана",
                'class Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n'
                '    @property\n    def fahrenheit(self):\n        return (self.celsius + 32) * 9 // 5\n\n'
                '    @property\n    def kelvin(self):\n        return self.celsius + 273\n\n\n'
                'temp = Temperature(celsius)\nprint(f"Celsius: {temp.celsius}")\n'
                'print(f"Fahrenheit: {temp.fahrenheit}")\nprint(f"Kelvin: {temp.kelvin}")'),
               ("делит обычным делением — печатается дробное число вроде 77.0",
                'class Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n'
                '    @property\n    def fahrenheit(self):\n        return self.celsius * 9 / 5 + 32\n\n'
                '    @property\n    def kelvin(self):\n        return self.celsius + 273\n\n\n'
                'temp = Temperature(celsius)\nprint(f"Celsius: {temp.celsius}")\n'
                'print(f"Fahrenheit: {temp.fahrenheit}")\nprint(f"Kelvin: {temp.kelvin}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PROPERTY],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-prop-reading-progress", title="Прогресс чтения",
        given=["pages", "day1", "day2"],
        variants=[{"pages": "200", "day1": "40", "day2": "70"},
                  {"pages": "150", "day1": "15", "day2": "45"},
                  {"pages": "320", "day1": "100", "day2": "33"}],
        hidden=[{"pages": "100", "day1": "0", "day2": "100"},
                {"pages": "300", "day1": "1", "day2": "2"},
                {"pages": "90", "day1": "45", "day2": "44"},
                {"pages": "500", "day1": "250", "day2": "125"}],
        intro="Приложение для чтения показывает, какую часть книги ты уже прочитал. В книге `pages` страниц; "
              "в первый день ты прочитал `day1` страниц, во второй — ещё `day2`. После каждого дня приложение "
              "пересчитывает процент и число оставшихся страниц.",
        steps=["Создай класс `Reading`. В `__init__(self, pages)` сохрани число страниц в `self.pages` "
               "и задай `self.read = 0` — сколько страниц прочитано.",
               "Добавь свойство `percent` (метод с `@property`), которое возвращает, сколько процентов книги прочитано: "
               "прочитанные страницы умножить на 100 и разделить нацело на число страниц.",
               "Добавь свойство `left`, которое возвращает, сколько страниц осталось.",
               "Создай объект `reading = Reading(pages)`. Увеличь `reading.read` на `day1` и выведи строку вида "
               "`Read 40 of 200: 20%, 160 left`. Потом увеличь `reading.read` на `day2` и выведи строку того же вида. "
               "Значения бери из атрибутов и свойств объекта, свойства — без скобок."],
        hint="Свойство вычисляется заново при каждом чтении, поэтому после изменения `reading.read` процент сам "
             "станет новым. Если посчитать его один раз в `__init__`, он останется нулевым. Сначала умножай на 100, "
             "а потом дели: `40 // 200` уже даёт 0.",
        solution='class Reading:\n    def __init__(self, pages):\n        self.pages = pages\n        self.read = 0\n'
                 '\n    @property\n    def percent(self):\n        return self.read * 100 // self.pages\n\n'
                 '    @property\n    def left(self):\n        return self.pages - self.read\n\n\n'
                 'reading = Reading(pages)\nreading.read += day1\n'
                 'print(f"Read {reading.read} of {reading.pages}: {reading.percent}%, {reading.left} left")\n'
                 'reading.read += day2\n'
                 'print(f"Read {reading.read} of {reading.pages}: {reading.percent}%, {reading.left} left")',
        wrong=[("считает процент и остаток один раз в __init__ — после чтения они не меняются",
                'class Reading:\n    def __init__(self, pages):\n        self.pages = pages\n        self.read = 0\n'
                '        self.percent = self.read * 100 // pages\n        self.left = pages - self.read\n\n\n'
                'reading = Reading(pages)\nreading.read += day1\n'
                'print(f"Read {reading.read} of {reading.pages}: {reading.percent}%, {reading.left} left")\n'
                'reading.read += day2\n'
                'print(f"Read {reading.read} of {reading.pages}: {reading.percent}%, {reading.left} left")'),
               ("сначала делит, потом умножает на 100 — процент почти всегда 0",
                'class Reading:\n    def __init__(self, pages):\n        self.pages = pages\n        self.read = 0\n'
                '\n    @property\n    def percent(self):\n        return self.read // self.pages * 100\n\n'
                '    @property\n    def left(self):\n        return self.pages - self.read\n\n\n'
                'reading = Reading(pages)\nreading.read += day1\n'
                'print(f"Read {reading.read} of {reading.pages}: {reading.percent}%, {reading.left} left")\n'
                'reading.read += day2\n'
                'print(f"Read {reading.read} of {reading.pages}: {reading.percent}%, {reading.left} left")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PROPERTY],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prop-loyalty-card", title="Карта постоянного покупателя",
        given=["purchases"],
        variants=[{"purchases": "[3000, 2500, -400, 16000]"},
                  {"purchases": "[1200, 0, 3800, 900]"},
                  {"purchases": "[20000, 150, -20000]"}],
        hidden=[{"purchases": "[4999, 1]"},
                {"purchases": "[19999, 1, 5]"},
                {"purchases": "[-5000, 100]"},
                {"purchases": "[5000, 14999, 2]"}],
        intro="В магазине есть карта постоянного покупателя. Чем больше потрачено по карте, тем выше статус: "
              "до 5000 руб. — `bronze` без скидки, от 5000 руб. — `silver` со скидкой 5 %, от 20000 руб. — `gold` "
              "со скидкой 10 %. В списке `purchases` — суммы покупок по порядку. Иногда кассир ошибается и вводит "
              "ноль или отрицательное число — такие суммы карта пропускает.",
        steps=["Создай класс `LoyaltyCard`. В `__init__(self)` заведи внутренний атрибут `self._spent = 0`.",
               "Добавь метод `buy(self, amount)`: он прибавляет `amount` к потраченному, только если это число больше нуля.",
               "Добавь три свойства с `@property`: `spent` возвращает потраченную сумму; `status` — строку `bronze`, "
               "`silver` или `gold` по правилам выше; `discount` — скидку в процентах (0, 5 или 10). Скидку определяй "
               "по свойству `self.status`, а не повторяй сравнения с суммами.",
               "Создай карту и пройди циклом по `purchases`: передай каждую сумму в `buy`, а после неё выведи строку "
               "вида `Spent: 3000, status: bronze, discount: 0%` со значениями `card.spent`, `card.status` и "
               "`card.discount` — без скобок."],
        hint="Свойство можно читать и внутри класса: в `discount` пиши `self.status` без скобок, как атрибут. "
             "Ровно 5000 руб. — это уже `silver`, а ровно 20000 руб. — уже `gold`: проверяй сначала "
             "`self._spent < 5000`, потом `self._spent < 20000`.",
        solution='class LoyaltyCard:\n    def __init__(self):\n        self._spent = 0\n\n    def buy(self, amount):\n'
                 '        if amount > 0:\n            self._spent += amount\n\n    @property\n    def spent(self):\n'
                 '        return self._spent\n\n    @property\n    def status(self):\n        if self._spent < 5000:\n'
                 '            return "bronze"\n        if self._spent < 20000:\n            return "silver"\n'
                 '        return "gold"\n\n    @property\n    def discount(self):\n        if self.status == "gold":\n'
                 '            return 10\n        if self.status == "silver":\n            return 5\n'
                 '        return 0\n\n\ncard = LoyaltyCard()\nfor amount in purchases:\n    card.buy(amount)\n'
                 '    print(f"Spent: {card.spent}, status: {card.status}, discount: {card.discount}%")',
        wrong=[("сравнивает через <= — ровно 5000 и ровно 20000 руб. дают статус на ступень ниже",
                'class LoyaltyCard:\n    def __init__(self):\n        self._spent = 0\n\n    def buy(self, amount):\n'
                '        if amount > 0:\n            self._spent += amount\n\n    @property\n    def spent(self):\n'
                '        return self._spent\n\n    @property\n    def status(self):\n'
                '        if self._spent <= 5000:\n            return "bronze"\n        if self._spent <= 20000:\n'
                '            return "silver"\n        return "gold"\n\n    @property\n    def discount(self):\n'
                '        if self.status == "gold":\n            return 10\n        if self.status == "silver":\n'
                '            return 5\n        return 0\n\n\ncard = LoyaltyCard()\nfor amount in purchases:\n'
                '    card.buy(amount)\n'
                '    print(f"Spent: {card.spent}, status: {card.status}, discount: {card.discount}%")'),
               ("buy не проверяет сумму — отрицательные покупки уменьшают потраченное",
                'class LoyaltyCard:\n    def __init__(self):\n        self._spent = 0\n\n    def buy(self, amount):\n'
                '        self._spent += amount\n\n    @property\n    def spent(self):\n        return self._spent\n\n'
                '    @property\n    def status(self):\n        if self._spent < 5000:\n            return "bronze"\n'
                '        if self._spent < 20000:\n            return "silver"\n        return "gold"\n\n'
                '    @property\n    def discount(self):\n        if self.status == "gold":\n            return 10\n'
                '        if self.status == "silver":\n            return 5\n        return 0\n\n\n'
                'card = LoyaltyCard()\nfor amount in purchases:\n    card.buy(amount)\n'
                '    print(f"Spent: {card.spent}, status: {card.status}, discount: {card.discount}%")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PROPERTY],
    ),
]
