"""PY_SELF_BASIC — «self и методы». Taught before: everything up to functions, classes, creating objects, __init__.
Here: methods that read and change the object's own attributes through self; each object keeps its own state;
calling a method with parentheses; one method calling another through self. Not yet: _private attributes and
@property (next topics), inheritance, tuples, dicts."""
from build import OutputTask

SKILL = "PY_SELF_BASIC"

NEED_CLASS = ("ClassDef", "Опиши объект в собственном классе через class.")
NEED_METHOD = ("re:def (?!__init__)\\w+\\(\\s*self",
               "Опиши действие методом класса — функцией внутри класса, у которой первый параметр self. "
               "Через self метод меняет данные именно этого объекта.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-self-step-counter", title="Шагомер",
        given=["morning", "evening"],
        variants=[{"morning": "3000", "evening": "4500"}, {"morning": "1200", "evening": "6800"},
                  {"morning": "5400", "evening": "2100"}],
        hidden=[{"morning": "0", "evening": "100"}, {"morning": "8000", "evening": "8000"}, {"morning": "250", "evening": "9999"}],
        intro="Фитнес-браслет считает шаги за день. Утром ты прошёл `morning` шагов, вечером — ещё `evening`. "
              "Браслет должен копить шаги, а не забывать утреннюю прогулку.",
        steps=["Создай класс `StepCounter`. В `__init__(self)` задай начальное значение `self.steps = 0`.",
               "Добавь метод `walk(self, count)`, который прибавляет `count` к `self.steps`.",
               "Создай объект `counter = StepCounter()`. Вызови `counter.walk(morning)` и выведи строку вида "
               "`Steps after the morning walk: 3000` — со значением из `counter.steps`.",
               "Потом вызови `counter.walk(evening)` и выведи строку вида `Steps today: 7500` — снова со значением из `counter.steps`."],
        hint="`self` — это тот самый объект, у которого вызвали метод. Запись `self.steps += count` "
             "меняет атрибут объекта, и новое значение сохраняется до следующего вызова метода.",
        solution='class StepCounter:\n    def __init__(self):\n        self.steps = 0\n\n    def walk(self, count):\n'
                 '        self.steps += count\n\n\ncounter = StepCounter()\ncounter.walk(morning)\n'
                 'print(f"Steps after the morning walk: {counter.steps}")\ncounter.walk(evening)\n'
                 'print(f"Steps today: {counter.steps}")',
        wrong=[("присваивает вместо прибавления — браслет помнит только последнюю прогулку",
                'class StepCounter:\n    def __init__(self):\n        self.steps = 0\n\n    def walk(self, count):\n'
                '        self.steps = count\n\n\ncounter = StepCounter()\ncounter.walk(morning)\n'
                'print(f"Steps after the morning walk: {counter.steps}")\ncounter.walk(evening)\n'
                'print(f"Steps today: {counter.steps}")'),
               ("пишет self.steps + count, но не сохраняет результат — шагов всегда 0",
                'class StepCounter:\n    def __init__(self):\n        self.steps = 0\n\n    def walk(self, count):\n'
                '        self.steps + count\n\n\ncounter = StepCounter()\ncounter.walk(morning)\n'
                'print(f"Steps after the morning walk: {counter.steps}")\ncounter.walk(evening)\n'
                'print(f"Steps today: {counter.steps}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_METHOD],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-self-match-score", title="Счёт футбольного матча",
        given=["team1", "team2", "goals"],
        variants=[{"team1": '"Spartak"', "team2": '"Zenit"', "goals": '["Spartak", "Zenit", "Spartak"]'},
                  {"team1": '"Rockets"', "team2": '"Comets"', "goals": '["Comets", "Comets", "Rockets", "Comets"]'},
                  {"team1": '"Eagles"', "team2": '"Wolves"', "goals": '["Wolves", "Eagles"]'}],
        hidden=[{"team1": '"Alpha"', "team2": '"Beta"', "goals": "[]"},
                {"team1": '"North"', "team2": '"South"', "goals": '["South"]'},
                {"team1": '"Blue"', "team2": '"Red"', "goals": '["Blue", "Blue", "Red", "Blue", "Blue"]'}],
        intro="Ты ведёшь табло школьного футбольного матча. Команды — `team1` и `team2`, а в списке `goals` по порядку "
              "записано, какая команда забивала каждый гол. У каждой команды свой счёт, и менять его должна сама команда.",
        steps=["Создай класс `Team`. В `__init__(self, name)` сохрани название в `self.name` и задай `self.score = 0`.",
               "Добавь метод `add_goal(self)`, который увеличивает счёт этой команды на 1.",
               "Создай два объекта: `home = Team(team1)` и `away = Team(team2)`. Пройди циклом по списку `goals`: "
               "если гол забила первая команда, вызови `home.add_goal()`, иначе — `away.add_goal()`.",
               "Выведи счёт строкой вида `Spartak 2:1 Zenit` — названия и голы бери из атрибутов объектов.",
               "Второй строкой выведи `Winner: …` с названием команды, забившей больше голов, а при равном счёте — `Draw`."],
        hint="Метод один на весь класс, но `self` в нём каждый раз — та команда, у которой метод вызвали: "
             "`home.add_goal()` меняет счёт `home`, а `away.add_goal()` — счёт `away`. "
             "И не забывай скобки: без них метод не вызывается.",
        solution='class Team:\n    def __init__(self, name):\n        self.name = name\n        self.score = 0\n\n'
                 '    def add_goal(self):\n        self.score += 1\n\n\nhome = Team(team1)\naway = Team(team2)\n'
                 'for goal in goals:\n    if goal == home.name:\n        home.add_goal()\n    else:\n        away.add_goal()\n\n'
                 'print(f"{home.name} {home.score}:{away.score} {away.name}")\nif home.score > away.score:\n'
                 '    print(f"Winner: {home.name}")\nelif away.score > home.score:\n    print(f"Winner: {away.name}")\n'
                 'else:\n    print("Draw")',
        wrong=[("вызывает метод без скобок — он не срабатывает, счёт остаётся 0:0",
                'class Team:\n    def __init__(self, name):\n        self.name = name\n        self.score = 0\n\n'
                '    def add_goal(self):\n        self.score += 1\n\n\nhome = Team(team1)\naway = Team(team2)\n'
                'for goal in goals:\n    if goal == home.name:\n        home.add_goal\n    else:\n        away.add_goal\n\n'
                'print(f"{home.name} {home.score}:{away.score} {away.name}")\nif home.score > away.score:\n'
                '    print(f"Winner: {home.name}")\nelif away.score > home.score:\n    print(f"Winner: {away.name}")\n'
                'else:\n    print("Draw")'),
               ("в методе присваивает счёту 1 вместо прибавления — больше одного гола не бывает",
                'class Team:\n    def __init__(self, name):\n        self.name = name\n        self.score = 0\n\n'
                '    def add_goal(self):\n        self.score = 1\n\n\nhome = Team(team1)\naway = Team(team2)\n'
                'for goal in goals:\n    if goal == home.name:\n        home.add_goal()\n    else:\n        away.add_goal()\n\n'
                'print(f"{home.name} {home.score}:{away.score} {away.name}")\nif home.score > away.score:\n'
                '    print(f"Winner: {home.name}")\nelif away.score > home.score:\n    print(f"Winner: {away.name}")\n'
                'else:\n    print("Draw")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_METHOD],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-self-cart-budget", title="Корзина и бюджет",
        given=["prices", "budget"],
        variants=[{"prices": "[120, 45, 300]", "budget": "400"},
                  {"prices": "[250, 80, 99, 30]", "budget": "500"},
                  {"prices": "[1500, 700]", "budget": "2000"}],
        hidden=[{"prices": "[100, 200, 300]", "budget": "600"},
                {"prices": "[50]", "budget": "10"},
                {"prices": "[]", "budget": "100"},
                {"prices": "[999, 1, 500, 500]", "budget": "3000"}],
        intro="Интернет-магазин складывает товары в корзину и подсказывает, укладываешься ли ты в бюджет. "
              "В списке `prices` — цены товаров, которые ты добавляешь, а `budget` — сколько денег у тебя есть.",
        steps=["Создай класс `Cart`. В `__init__(self)` создай пустой список `self.prices`.",
               "Добавь метод `add(self, price)`, который добавляет цену в список `self.prices`, "
               "и метод `total(self)`, который возвращает сумму всех цен в корзине.",
               "Добавь метод `fits(self, budget)`: он возвращает `True`, если сумма корзины не больше `budget`, "
               "и `False`, если больше. Сумму в нём не считай заново — вызови свой же метод через `self.total()`.",
               "Создай корзину и добавь в неё по очереди все цены из `prices`. Выведи строку `Total: …` с результатом `total()`.",
               "Если `fits(budget)` вернул `True`, выведи второй строкой `Within budget`, а иначе — "
               "строку вида `Short by: 65 rub` с разницей между суммой и бюджетом."],
        hint="Внутри класса методы вызывают друг друга через `self`: `self.total()` — это метод `total` того же объекта. "
             "Сумму в `total` считай как обычно: заведи переменную с нулём и в цикле по `self.prices` прибавляй каждую цену. "
             "Ровно столько денег, сколько стоит корзина, — уже достаточно.",
        solution='class Cart:\n    def __init__(self):\n        self.prices = []\n\n    def add(self, price):\n'
                 '        self.prices.append(price)\n\n    def total(self):\n        result = 0\n        for price in self.prices:\n'
                 '            result += price\n        return result\n\n    def fits(self, budget):\n'
                 '        return self.total() <= budget\n\n\ncart = Cart()\nfor price in prices:\n    cart.add(price)\n\n'
                 'print(f"Total: {cart.total()}")\nif cart.fits(budget):\n    print("Within budget")\nelse:\n'
                 '    print(f"Short by: {cart.total() - budget} rub")',
        wrong=[("метод add записывает новый список вместо добавления — в корзине остаётся только последний товар",
                'class Cart:\n    def __init__(self):\n        self.prices = []\n\n    def add(self, price):\n'
                '        self.prices = [price]\n\n    def total(self):\n        result = 0\n        for price in self.prices:\n'
                '            result += price\n        return result\n\n    def fits(self, budget):\n'
                '        return self.total() <= budget\n\n\ncart = Cart()\nfor price in prices:\n    cart.add(price)\n\n'
                'print(f"Total: {cart.total()}")\nif cart.fits(budget):\n    print("Within budget")\nelse:\n'
                '    print(f"Short by: {cart.total() - budget} rub")'),
               ("строгое сравнение — когда сумма ровно равна бюджету, пишет, что денег не хватает",
                'class Cart:\n    def __init__(self):\n        self.prices = []\n\n    def add(self, price):\n'
                '        self.prices.append(price)\n\n    def total(self):\n        result = 0\n        for price in self.prices:\n'
                '            result += price\n        return result\n\n    def fits(self, budget):\n'
                '        return self.total() < budget\n\n\ncart = Cart()\nfor price in prices:\n    cart.add(price)\n\n'
                'print(f"Total: {cart.total()}")\nif cart.fits(budget):\n    print("Within budget")\nelse:\n'
                '    print(f"Short by: {cart.total() - budget} rub")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_METHOD,
                  ("re:self\\.total\\(\\s*\\)", "В методе fits вызови метод total того же объекта через self.total() — "
                                               "так сумма считается в одном месте.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-self-water-bottle", title="Бутылка воды",
        given=["volume", "sip1", "sip2"],
        variants=[{"volume": "500", "sip1": "150", "sip2": "100"}, {"volume": "750", "sip1": "200", "sip2": "320"},
                  {"volume": "330", "sip1": "30", "sip2": "90"}],
        hidden=[{"volume": "1000", "sip1": "0", "sip2": "1000"}, {"volume": "600", "sip1": "250", "sip2": "250"},
                {"volume": "450", "sip1": "45", "sip2": "5"}],
        intro="Умная бутылка для воды сама считает, сколько воды в ней осталось и сколько раз из неё пили. "
              "В бутылку налили `volume` миллилитров, потом из неё выпили сначала `sip1`, а позже ещё `sip2` миллилитров.",
        steps=["Создай класс `Bottle`. В `__init__(self, volume)` сохрани объём в `self.volume` и задай счётчик глотков "
               "`self.sips = 0`.",
               "Добавь метод `drink(self, amount)`, который за один вызов делает две вещи: уменьшает `self.volume` "
               "на `amount` и увеличивает `self.sips` на 1.",
               "Создай объект `bottle = Bottle(volume)`. Вызови `bottle.drink(sip1)` и выведи строку вида "
               "`Sips: 1, left: 350 ml` — со значениями из `bottle.sips` и `bottle.volume`.",
               "Потом вызови `bottle.drink(sip2)` и снова выведи строку того же вида."],
        hint="Через `self` метод меняет атрибуты именно той бутылки, у которой его вызвали, и изменения сохраняются "
             "между вызовами. Уменьшить атрибут можно записью `self.volume -= amount`.",
        solution='class Bottle:\n    def __init__(self, volume):\n        self.volume = volume\n        self.sips = 0\n\n'
                 '    def drink(self, amount):\n        self.volume -= amount\n        self.sips += 1\n\n\n'
                 'bottle = Bottle(volume)\nbottle.drink(sip1)\nprint(f"Sips: {bottle.sips}, left: {bottle.volume} ml")\n'
                 'bottle.drink(sip2)\nprint(f"Sips: {bottle.sips}, left: {bottle.volume} ml")',
        wrong=[("в методе пишет self.volume = amount — в бутылке оказывается ровно столько, сколько выпили",
                'class Bottle:\n    def __init__(self, volume):\n        self.volume = volume\n        self.sips = 0\n\n'
                '    def drink(self, amount):\n        self.volume = amount\n        self.sips += 1\n\n\n'
                'bottle = Bottle(volume)\nbottle.drink(sip1)\nprint(f"Sips: {bottle.sips}, left: {bottle.volume} ml")\n'
                'bottle.drink(sip2)\nprint(f"Sips: {bottle.sips}, left: {bottle.volume} ml")'),
               ("забыл увеличить счётчик глотков — он всегда 0",
                'class Bottle:\n    def __init__(self, volume):\n        self.volume = volume\n        self.sips = 0\n\n'
                '    def drink(self, amount):\n        self.volume -= amount\n\n\n'
                'bottle = Bottle(volume)\nbottle.drink(sip1)\nprint(f"Sips: {bottle.sips}, left: {bottle.volume} ml")\n'
                'bottle.drink(sip2)\nprint(f"Sips: {bottle.sips}, left: {bottle.volume} ml")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_METHOD],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-self-two-lamps", title="Две лампы",
        given=["room1", "room2", "presses"],
        variants=[{"room1": '"kitchen"', "room2": '"hall"', "presses": '["kitchen", "hall", "kitchen", "kitchen", "hall"]'},
                  {"room1": '"bedroom"', "room2": '"bath"', "presses": '["bath", "bedroom", "bath", "bath"]'},
                  {"room1": '"study"', "room2": '"garage"', "presses": '["study", "garage"]'}],
        hidden=[{"room1": '"attic"', "room2": '"porch"', "presses": "[]"},
                {"room1": '"left"', "room2": '"right"', "presses": '["right", "right"]'},
                {"room1": '"red"', "room2": '"blue"', "presses": '["red", "red", "red", "blue", "red", "blue", "blue"]'}],
        intro="В умном доме две лампы — в комнатах `room1` и `room2`, и сначала обе выключены. Каждое нажатие "
              "выключателя переключает лампу: выключенная загорается, горящая гаснет. В списке `presses` по порядку "
              "записано, в какой комнате нажимали выключатель.",
        steps=["Создай класс `Lamp`. В `__init__(self, room)` сохрани комнату в `self.room`, задай `self.on = False` "
               "и счётчик нажатий `self.clicks = 0`.",
               "Добавь метод `switch(self)`: он меняет `self.on` на противоположное значение и увеличивает "
               "`self.clicks` на 1. И метод `status(self)`, который возвращает строку `on`, если лампа горит, и `off`, если нет.",
               "Создай две лампы: `lamp1 = Lamp(room1)` и `lamp2 = Lamp(room2)`. Пройди циклом по `presses`: "
               "если нажали в комнате первой лампы, вызови `lamp1.switch()`, иначе — `lamp2.switch()`.",
               "Для каждой лампы выведи строку вида `kitchen: on, clicks 3` — комнату, результат `status()` и число нажатий.",
               "Последней строкой выведи `Lamps on: …` — сколько ламп горит в конце."],
        hint="Противоположное логическое значение даёт `not`: `self.on = not self.on`. Метод один на обе лампы, "
             "но `self` в нём — та лампа, у которой его вызвали, поэтому `lamp1.switch()` не трогает `lamp2`.",
        solution='class Lamp:\n    def __init__(self, room):\n        self.room = room\n        self.on = False\n        self.clicks = 0\n\n'
                 '    def switch(self):\n        self.on = not self.on\n        self.clicks += 1\n\n    def status(self):\n'
                 '        if self.on:\n            return "on"\n        return "off"\n\n\nlamp1 = Lamp(room1)\nlamp2 = Lamp(room2)\n'
                 'for room in presses:\n    if room == lamp1.room:\n        lamp1.switch()\n    else:\n        lamp2.switch()\n\n'
                 'print(f"{lamp1.room}: {lamp1.status()}, clicks {lamp1.clicks}")\n'
                 'print(f"{lamp2.room}: {lamp2.status()}, clicks {lamp2.clicks}")\ncount = 0\nif lamp1.on:\n    count += 1\n'
                 'if lamp2.on:\n    count += 1\nprint(f"Lamps on: {count}")',
        wrong=[("switch всегда включает лампу, а не переключает её",
                'class Lamp:\n    def __init__(self, room):\n        self.room = room\n        self.on = False\n        self.clicks = 0\n\n'
                '    def switch(self):\n        self.on = True\n        self.clicks += 1\n\n    def status(self):\n'
                '        if self.on:\n            return "on"\n        return "off"\n\n\nlamp1 = Lamp(room1)\nlamp2 = Lamp(room2)\n'
                'for room in presses:\n    if room == lamp1.room:\n        lamp1.switch()\n    else:\n        lamp2.switch()\n\n'
                'print(f"{lamp1.room}: {lamp1.status()}, clicks {lamp1.clicks}")\n'
                'print(f"{lamp2.room}: {lamp2.status()}, clicks {lamp2.clicks}")\ncount = 0\nif lamp1.on:\n    count += 1\n'
                'if lamp2.on:\n    count += 1\nprint(f"Lamps on: {count}")'),
               ("при каждом нажатии переключает первую лампу, в какой бы комнате ни нажали",
                'class Lamp:\n    def __init__(self, room):\n        self.room = room\n        self.on = False\n        self.clicks = 0\n\n'
                '    def switch(self):\n        self.on = not self.on\n        self.clicks += 1\n\n    def status(self):\n'
                '        if self.on:\n            return "on"\n        return "off"\n\n\nlamp1 = Lamp(room1)\nlamp2 = Lamp(room2)\n'
                'for room in presses:\n    lamp1.switch()\n\n'
                'print(f"{lamp1.room}: {lamp1.status()}, clicks {lamp1.clicks}")\n'
                'print(f"{lamp2.room}: {lamp2.status()}, clicks {lamp2.clicks}")\ncount = 0\nif lamp1.on:\n    count += 1\n'
                'if lamp2.on:\n    count += 1\nprint(f"Lamps on: {count}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_METHOD],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-self-bus-stops", title="Автобус на маршруте",
        given=["capacity", "entering", "leaving"],
        variants=[{"capacity": "30", "entering": "[20, 25, 10]", "leaving": "[0, 8, 12]"},
                  {"capacity": "40", "entering": "[35, 12, 6, 20]", "leaving": "[0, 3, 15, 5]"},
                  {"capacity": "20", "entering": "[25, 4, 9]", "leaving": "[0, 10, 2]"}],
        hidden=[{"capacity": "10", "entering": "[10]", "leaving": "[0]"},
                {"capacity": "10", "entering": "[11, 3]", "leaving": "[0, 0]"},
                {"capacity": "50", "entering": "[5, 0, 60]", "leaving": "[0, 5, 0]"},
                {"capacity": "15", "entering": "[15, 15]", "leaving": "[0, 15]"}],
        intro="Автобус вмещает `capacity` пассажиров и выезжает на маршрут пустым. На каждой остановке сначала выходят "
              "пассажиры, а потом заходят новые — сколько поместится; остальные остаются ждать следующий автобус. "
              "В списке `leaving` — сколько человек выходит на каждой остановке, в списке `entering` на тех же местах — "
              "сколько хочет зайти.",
        steps=["Создай класс `Bus`. В `__init__(self, capacity)` сохрани вместимость в `self.capacity` и задай "
               "`self.passengers = 0`.",
               "Добавь метод `free_seats(self)`, который возвращает число свободных мест, и метод `leave(self, count)`, "
               "который уменьшает число пассажиров на `count`.",
               "Добавь метод `board(self, count)`: он узнаёт число свободных мест, вызвав свой же метод "
               "`self.free_seats()`. Если все `count` человек помещаются, он сажает их всех и возвращает 0. "
               "Иначе сажает столько, сколько есть мест, и возвращает, сколько человек не поместилось.",
               "Создай автобус и пройди по остановкам циклом по `range(len(entering))`: на каждой сначала вызови `leave`, "
               "потом `board`. После каждой остановки выведи строку вида `Stop 1: 20 on board, 0 left behind` — "
               "номер остановки начиная с 1, число пассажиров и сколько человек не поместилось."],
        hint="Внутри класса методы вызывают друг друга через `self`: `free = self.free_seats()`. Свободных мест — это "
             "вместимость минус те, кто уже едет, а не вся вместимость. Порядок на остановке важен: сначала выход, "
             "потом посадка.",
        solution='class Bus:\n    def __init__(self, capacity):\n        self.capacity = capacity\n'
                 '        self.passengers = 0\n\n    def free_seats(self):\n'
                 '        return self.capacity - self.passengers\n\n    def leave(self, count):\n'
                 '        self.passengers -= count\n\n    def board(self, count):\n'
                 '        free = self.free_seats()\n        if count <= free:\n'
                 '            self.passengers += count\n            return 0\n        self.passengers += free\n'
                 '        return count - free\n\n\nbus = Bus(capacity)\nfor i in range(len(entering)):\n'
                 '    bus.leave(leaving[i])\n    behind = bus.board(entering[i])\n'
                 '    print(f"Stop {i + 1}: {bus.passengers} on board, {behind} left behind")',
        wrong=[("считает свободными все места автобуса, не вычитая тех, кто уже едет",
                'class Bus:\n    def __init__(self, capacity):\n        self.capacity = capacity\n'
                '        self.passengers = 0\n\n    def free_seats(self):\n        return self.capacity\n\n'
                '    def leave(self, count):\n        self.passengers -= count\n\n    def board(self, count):\n'
                '        free = self.free_seats()\n        if count <= free:\n'
                '            self.passengers += count\n            return 0\n        self.passengers += free\n'
                '        return count - free\n\n\nbus = Bus(capacity)\nfor i in range(len(entering)):\n'
                '    bus.leave(leaving[i])\n    behind = bus.board(entering[i])\n'
                '    print(f"Stop {i + 1}: {bus.passengers} on board, {behind} left behind")'),
               ("на остановке сначала сажает новых пассажиров, а потом выпускает выходящих",
                'class Bus:\n    def __init__(self, capacity):\n        self.capacity = capacity\n'
                '        self.passengers = 0\n\n    def free_seats(self):\n'
                '        return self.capacity - self.passengers\n\n    def leave(self, count):\n'
                '        self.passengers -= count\n\n    def board(self, count):\n'
                '        free = self.free_seats()\n        if count <= free:\n'
                '            self.passengers += count\n            return 0\n        self.passengers += free\n'
                '        return count - free\n\n\nbus = Bus(capacity)\nfor i in range(len(entering)):\n'
                '    behind = bus.board(entering[i])\n    bus.leave(leaving[i])\n'
                '    print(f"Stop {i + 1}: {bus.passengers} on board, {behind} left behind")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_METHOD,
                  ("re:self\\.free_seats\\(\\s*\\)", "В методе board узнай число мест вызовом своего же метода "
                                                    "self.free_seats() — так оно считается в одном месте.")],
    ),
]
