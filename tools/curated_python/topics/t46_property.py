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
]
