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
        skill=SKILL, difficulty=1, slug="py-prop-rt-price-tax", title="Цена с налогом",
        given=["name", "price"],
        variants=[{"name": '"kettle"', "price": "1000"}, {"name": '"lamp"', "price": "450"},
                  {"name": '"chair"', "price": "2500"}],
        hidden=[{"name": '"pen"', "price": "50"}, {"name": '"sofa"', "price": "30000"}, {"name": '"mug"', "price": "135"}],
        intro="В интернет-магазине цена товара хранится без налога, а на странице нужно показать ещё налог 20 % "
              "и итоговую цену. Их удобно сделать свойствами: они читаются как атрибуты, а вычисляются из цены.",
        steps=["Создай класс `Product`. В `__init__(self, name, price)` сохрани название и цену в атрибуты "
               "`self.name` и `self.price`.",
               "Добавь свойство `tax` — метод с `@property` над ним. Оно возвращает налог: цену, умноженную на 20 "
               "и делённую нацело на 100.",
               "Добавь свойство `total`, которое возвращает цену плюс налог. Налог в нём возьми из свойства `self.tax`.",
               "Создай объект `product = Product(name, price)` и выведи две строки вида `kettle: 1000 + tax 200` "
               "и `Total: 1200 rub` — со значениями `product.name`, `product.price`, `product.tax` и `product.total`. "
               "Свойства читай без скобок."],
        hint="`@property` пишется на отдельной строке прямо над `def`. После этого `product.tax` вызывает метод сам, "
             "без скобок, — и внутри класса тоже: `self.tax`. Без `@property` запись без скобок вернула бы сам метод, а не число.",
        solution='class Product:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\n'
                 '    @property\n    def tax(self):\n        return self.price * 20 // 100\n\n'
                 '    @property\n    def total(self):\n        return self.price + self.tax\n\n\n'
                 'product = Product(name, price)\nprint(f"{product.name}: {product.price} + tax {product.tax}")\n'
                 'print(f"Total: {product.total} rub")',
        wrong=[("забыл @property у total — без скобок печатается описание метода",
                'class Product:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\n'
                '    @property\n    def tax(self):\n        return self.price * 20 // 100\n\n'
                '    def total(self):\n        return self.price + self.tax\n\n\n'
                'product = Product(name, price)\nprint(f"{product.name}: {product.price} + tax {product.tax}")\n'
                'print(f"Total: {product.total} rub")'),
               ("забыл разделить на 100 — налог в 20 раз больше цены",
                'class Product:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\n'
                '    @property\n    def tax(self):\n        return self.price * 20\n\n'
                '    @property\n    def total(self):\n        return self.price + self.tax\n\n\n'
                'product = Product(name, price)\nprint(f"{product.name}: {product.price} + tax {product.tax}")\n'
                'print(f"Total: {product.total} rub")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PROPERTY],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-prop-rt-backpack", title="Рюкзак в поход",
        given=["limit", "item1", "item2"],
        variants=[{"limit": "15", "item1": "9", "item2": "4"}, {"limit": "12", "item1": "7", "item2": "8"},
                  {"limit": "10", "item1": "10", "item2": "3"}],
        hidden=[{"limit": "20", "item1": "0", "item2": "20"}, {"limit": "8", "item1": "3", "item2": "6"},
                {"limit": "25", "item1": "5", "item2": "5"}, {"limit": "5", "item1": "6", "item2": "1"}],
        intro="Ты собираешься в поход: рюкзак выдерживает `limit` кг. Сначала ты положил в него вещи весом `item1` кг, "
              "потом ещё `item2` кг. После каждого раза хочется видеть, сколько места по весу осталось "
              "и не перегружен ли рюкзак.",
        steps=["Создай класс `Backpack`. В `__init__(self, limit)` сохрани предел в `self.limit` и задай `self.weight = 0`.",
               "Добавь свойство `free` (метод с `@property`), которое возвращает, сколько килограммов ещё можно положить: "
               "предел минус вес, а если вес уже не меньше предела — `0`.",
               "Добавь свойство `status`, которое возвращает `too heavy`, если вес больше предела, и `ok` в остальных случаях.",
               "Создай рюкзак `bag = Backpack(limit)`. Увеличь `bag.weight` на `item1` и выведи строку вида "
               "`Weight: 9 kg, free: 6 kg, ok`. Потом увеличь `bag.weight` на `item2` и выведи строку того же вида. "
               "Свойства читай без скобок."],
        hint="Свойство вычисляется заново при каждом чтении, поэтому после изменения `bag.weight` и `free`, и `status` "
             "сами станут новыми. Если посчитать их один раз в `__init__`, они останутся такими, как у пустого рюкзака. "
             "Ровно `limit` кг — ещё `ok`.",
        solution='class Backpack:\n    def __init__(self, limit):\n        self.limit = limit\n        self.weight = 0\n\n'
                 '    @property\n    def free(self):\n        if self.weight >= self.limit:\n            return 0\n'
                 '        return self.limit - self.weight\n\n    @property\n    def status(self):\n'
                 '        if self.weight > self.limit:\n            return "too heavy"\n        return "ok"\n\n\n'
                 'bag = Backpack(limit)\nbag.weight += item1\nprint(f"Weight: {bag.weight} kg, free: {bag.free} kg, {bag.status}")\n'
                 'bag.weight += item2\nprint(f"Weight: {bag.weight} kg, free: {bag.free} kg, {bag.status}")',
        wrong=[("считает свободное место один раз в __init__ — после вещей оно не меняется",
                'class Backpack:\n    def __init__(self, limit):\n        self.limit = limit\n        self.weight = 0\n'
                '        self.free = limit\n\n    @property\n    def status(self):\n'
                '        if self.weight > self.limit:\n            return "too heavy"\n        return "ok"\n\n\n'
                'bag = Backpack(limit)\nbag.weight += item1\nprint(f"Weight: {bag.weight} kg, free: {bag.free} kg, {bag.status}")\n'
                'bag.weight += item2\nprint(f"Weight: {bag.weight} kg, free: {bag.free} kg, {bag.status}")'),
               ("не ограничивает свободное место нулём — у перегруженного рюкзака оно отрицательное",
                'class Backpack:\n    def __init__(self, limit):\n        self.limit = limit\n        self.weight = 0\n\n'
                '    @property\n    def free(self):\n        return self.limit - self.weight\n\n    @property\n    def status(self):\n'
                '        if self.weight > self.limit:\n            return "too heavy"\n        return "ok"\n\n\n'
                'bag = Backpack(limit)\nbag.weight += item1\nprint(f"Weight: {bag.weight} kg, free: {bag.free} kg, {bag.status}")\n'
                'bag.weight += item2\nprint(f"Weight: {bag.weight} kg, free: {bag.free} kg, {bag.status}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PROPERTY],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prop-rt-class-poll", title="Голосование в классе",
        given=["votes"],
        variants=[{"votes": '["yes", "no", "yes", "maybe", "yes", "no"]'},
                  {"votes": '["no", "yes", "no", "no"]'},
                  {"votes": '["yes", "yes", "Yes", "no"]'}],
        hidden=[{"votes": "[]"},
                {"votes": '["yes", "no"]'},
                {"votes": '["yes"]'},
                {"votes": '["maybe", "no", "yes", "yes", "yes", "skip", "no"]'}],
        intro="Класс голосует, ехать ли на экскурсию. Каждый пишет `yes` или `no`, но кто-то пишет что-то другое — "
              "такие голоса не считаются. Решение принято, если голосов `yes` больше половины всех засчитанных голосов. "
              "В списке `votes` — голоса по порядку.",
        steps=["Создай класс `Poll`. В `__init__(self)` заведи внутренние атрибуты `self._yes = 0` и `self._no = 0`.",
               "Добавь метод `vote(self, answer)`: для `yes` он прибавляет 1 к `self._yes`, для `no` — к `self._no`, "
               "а любой другой ответ пропускает. Большие и маленькие буквы различаются: `Yes` не засчитывается.",
               "Добавь три свойства с `@property`: `total` — сколько голосов засчитано; `yes_percent` — процент голосов "
               "`yes` от засчитанных (умножь на 100 и раздели нацело), а если засчитанных нет — `0`; `result` — строку "
               "`accepted`, если `yes_percent` больше 50, иначе `rejected`. В `result` используй свойство `self.yes_percent`.",
               "Создай голосование, передай в `vote` по очереди все ответы из `votes` и выведи три строки вида "
               "`Votes: 5`, `Yes: 60%` и `Result: accepted` со значениями `poll.total`, `poll.yes_percent` и "
               "`poll.result` — без скобок."],
        hint="Свойство можно читать и внутри класса: в `result` пиши `self.yes_percent` без скобок, как атрибут. "
             "Ровно 50 % — это ещё не больше половины. А если голосов нет совсем, делить на ноль нельзя — "
             "сначала проверь `self.total == 0`.",
        solution='class Poll:\n    def __init__(self):\n        self._yes = 0\n        self._no = 0\n\n'
                 '    def vote(self, answer):\n        if answer == "yes":\n            self._yes += 1\n'
                 '        elif answer == "no":\n            self._no += 1\n\n    @property\n    def total(self):\n'
                 '        return self._yes + self._no\n\n    @property\n    def yes_percent(self):\n'
                 '        if self.total == 0:\n            return 0\n        return self._yes * 100 // self.total\n\n'
                 '    @property\n    def result(self):\n        if self.yes_percent > 50:\n            return "accepted"\n'
                 '        return "rejected"\n\n\npoll = Poll()\nfor answer in votes:\n    poll.vote(answer)\n'
                 'print(f"Votes: {poll.total}")\nprint(f"Yes: {poll.yes_percent}%")\nprint(f"Result: {poll.result}")',
        wrong=[("засчитывает любой другой ответ как no",
                'class Poll:\n    def __init__(self):\n        self._yes = 0\n        self._no = 0\n\n'
                '    def vote(self, answer):\n        if answer == "yes":\n            self._yes += 1\n'
                '        else:\n            self._no += 1\n\n    @property\n    def total(self):\n'
                '        return self._yes + self._no\n\n    @property\n    def yes_percent(self):\n'
                '        if self.total == 0:\n            return 0\n        return self._yes * 100 // self.total\n\n'
                '    @property\n    def result(self):\n        if self.yes_percent > 50:\n            return "accepted"\n'
                '        return "rejected"\n\n\npoll = Poll()\nfor answer in votes:\n    poll.vote(answer)\n'
                'print(f"Votes: {poll.total}")\nprint(f"Yes: {poll.yes_percent}%")\nprint(f"Result: {poll.result}")'),
               ("принимает решение и при ровно 50 % голосов yes",
                'class Poll:\n    def __init__(self):\n        self._yes = 0\n        self._no = 0\n\n'
                '    def vote(self, answer):\n        if answer == "yes":\n            self._yes += 1\n'
                '        elif answer == "no":\n            self._no += 1\n\n    @property\n    def total(self):\n'
                '        return self._yes + self._no\n\n    @property\n    def yes_percent(self):\n'
                '        if self.total == 0:\n            return 0\n        return self._yes * 100 // self.total\n\n'
                '    @property\n    def result(self):\n        if self.yes_percent >= 50:\n            return "accepted"\n'
                '        return "rejected"\n\n\npoll = Poll()\nfor answer in votes:\n    poll.vote(answer)\n'
                'print(f"Votes: {poll.total}")\nprint(f"Yes: {poll.yes_percent}%")\nprint(f"Result: {poll.result}")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_PROPERTY],
    ),
]
