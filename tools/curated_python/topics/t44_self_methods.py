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
               "`Шагов после утренней прогулки: 3000` — со значением из `counter.steps`.",
               "Потом вызови `counter.walk(evening)` и выведи строку вида `Шагов за день: 7500` — снова со значением из `counter.steps`."],
        hint="`self` — это тот самый объект, у которого вызвали метод. Запись `self.steps += count` "
             "меняет атрибут объекта, и новое значение сохраняется до следующего вызова метода.",
        solution='class StepCounter:\n    def __init__(self):\n        self.steps = 0\n\n    def walk(self, count):\n'
                 '        self.steps += count\n\n\ncounter = StepCounter()\ncounter.walk(morning)\n'
                 'print(f"Шагов после утренней прогулки: {counter.steps}")\ncounter.walk(evening)\n'
                 'print(f"Шагов за день: {counter.steps}")',
        wrong=[("присваивает вместо прибавления — браслет помнит только последнюю прогулку",
                'class StepCounter:\n    def __init__(self):\n        self.steps = 0\n\n    def walk(self, count):\n'
                '        self.steps = count\n\n\ncounter = StepCounter()\ncounter.walk(morning)\n'
                'print(f"Шагов после утренней прогулки: {counter.steps}")\ncounter.walk(evening)\n'
                'print(f"Шагов за день: {counter.steps}")'),
               ("пишет self.steps + count, но не сохраняет результат — шагов всегда 0",
                'class StepCounter:\n    def __init__(self):\n        self.steps = 0\n\n    def walk(self, count):\n'
                '        self.steps + count\n\n\ncounter = StepCounter()\ncounter.walk(morning)\n'
                'print(f"Шагов после утренней прогулки: {counter.steps}")\ncounter.walk(evening)\n'
                'print(f"Шагов за день: {counter.steps}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_METHOD],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-self-match-score", title="Счёт футбольного матча",
        given=["team1", "team2", "goals"],
        variants=[{"team1": '"Спартак"', "team2": '"Зенит"', "goals": '["Спартак", "Зенит", "Спартак"]'},
                  {"team1": '"Ракета"', "team2": '"Комета"', "goals": '["Комета", "Комета", "Ракета", "Комета"]'},
                  {"team1": '"Орлы"', "team2": '"Волки"', "goals": '["Волки", "Орлы"]'}],
        hidden=[{"team1": '"Альфа"', "team2": '"Бета"', "goals": "[]"},
                {"team1": '"Север"', "team2": '"Юг"', "goals": '["Юг"]'},
                {"team1": '"Синие"', "team2": '"Красные"', "goals": '["Синие", "Синие", "Красные", "Синие", "Синие"]'}],
        intro="Ты ведёшь табло школьного футбольного матча. Команды — `team1` и `team2`, а в списке `goals` по порядку "
              "записано, какая команда забивала каждый гол. У каждой команды свой счёт, и менять его должна сама команда.",
        steps=["Создай класс `Team`. В `__init__(self, name)` сохрани название в `self.name` и задай `self.score = 0`.",
               "Добавь метод `add_goal(self)`, который увеличивает счёт этой команды на 1.",
               "Создай два объекта: `home = Team(team1)` и `away = Team(team2)`. Пройди циклом по списку `goals`: "
               "если гол забила первая команда, вызови `home.add_goal()`, иначе — `away.add_goal()`.",
               "Выведи счёт строкой вида `Спартак 2:1 Зенит` — названия и голы бери из атрибутов объектов.",
               "Второй строкой выведи `Победа: …` с названием команды, забившей больше голов, а при равном счёте — `Ничья`."],
        hint="Метод один на весь класс, но `self` в нём каждый раз — та команда, у которой метод вызвали: "
             "`home.add_goal()` меняет счёт `home`, а `away.add_goal()` — счёт `away`. "
             "И не забывай скобки: без них метод не вызывается.",
        solution='class Team:\n    def __init__(self, name):\n        self.name = name\n        self.score = 0\n\n'
                 '    def add_goal(self):\n        self.score += 1\n\n\nhome = Team(team1)\naway = Team(team2)\n'
                 'for goal in goals:\n    if goal == home.name:\n        home.add_goal()\n    else:\n        away.add_goal()\n\n'
                 'print(f"{home.name} {home.score}:{away.score} {away.name}")\nif home.score > away.score:\n'
                 '    print(f"Победа: {home.name}")\nelif away.score > home.score:\n    print(f"Победа: {away.name}")\n'
                 'else:\n    print("Ничья")',
        wrong=[("вызывает метод без скобок — он не срабатывает, счёт остаётся 0:0",
                'class Team:\n    def __init__(self, name):\n        self.name = name\n        self.score = 0\n\n'
                '    def add_goal(self):\n        self.score += 1\n\n\nhome = Team(team1)\naway = Team(team2)\n'
                'for goal in goals:\n    if goal == home.name:\n        home.add_goal\n    else:\n        away.add_goal\n\n'
                'print(f"{home.name} {home.score}:{away.score} {away.name}")\nif home.score > away.score:\n'
                '    print(f"Победа: {home.name}")\nelif away.score > home.score:\n    print(f"Победа: {away.name}")\n'
                'else:\n    print("Ничья")'),
               ("в методе присваивает счёту 1 вместо прибавления — больше одного гола не бывает",
                'class Team:\n    def __init__(self, name):\n        self.name = name\n        self.score = 0\n\n'
                '    def add_goal(self):\n        self.score = 1\n\n\nhome = Team(team1)\naway = Team(team2)\n'
                'for goal in goals:\n    if goal == home.name:\n        home.add_goal()\n    else:\n        away.add_goal()\n\n'
                'print(f"{home.name} {home.score}:{away.score} {away.name}")\nif home.score > away.score:\n'
                '    print(f"Победа: {home.name}")\nelif away.score > home.score:\n    print(f"Победа: {away.name}")\n'
                'else:\n    print("Ничья")')],
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
               "Создай корзину и добавь в неё по очереди все цены из `prices`. Выведи строку `Сумма: …` с результатом `total()`.",
               "Если `fits(budget)` вернул `True`, выведи второй строкой `В бюджет укладываемся`, а иначе — "
               "строку вида `Не хватает: 65 руб.` с разницей между суммой и бюджетом."],
        hint="Внутри класса методы вызывают друг друга через `self`: `self.total()` — это метод `total` того же объекта. "
             "Сумму в `total` считай как обычно: заведи переменную с нулём и в цикле по `self.prices` прибавляй каждую цену. "
             "Ровно столько денег, сколько стоит корзина, — уже достаточно.",
        solution='class Cart:\n    def __init__(self):\n        self.prices = []\n\n    def add(self, price):\n'
                 '        self.prices.append(price)\n\n    def total(self):\n        result = 0\n        for price in self.prices:\n'
                 '            result += price\n        return result\n\n    def fits(self, budget):\n'
                 '        return self.total() <= budget\n\n\ncart = Cart()\nfor price in prices:\n    cart.add(price)\n\n'
                 'print(f"Сумма: {cart.total()}")\nif cart.fits(budget):\n    print("В бюджет укладываемся")\nelse:\n'
                 '    print(f"Не хватает: {cart.total() - budget} руб.")',
        wrong=[("метод add записывает новый список вместо добавления — в корзине остаётся только последний товар",
                'class Cart:\n    def __init__(self):\n        self.prices = []\n\n    def add(self, price):\n'
                '        self.prices = [price]\n\n    def total(self):\n        result = 0\n        for price in self.prices:\n'
                '            result += price\n        return result\n\n    def fits(self, budget):\n'
                '        return self.total() <= budget\n\n\ncart = Cart()\nfor price in prices:\n    cart.add(price)\n\n'
                'print(f"Сумма: {cart.total()}")\nif cart.fits(budget):\n    print("В бюджет укладываемся")\nelse:\n'
                '    print(f"Не хватает: {cart.total() - budget} руб.")'),
               ("строгое сравнение — когда сумма ровно равна бюджету, пишет, что денег не хватает",
                'class Cart:\n    def __init__(self):\n        self.prices = []\n\n    def add(self, price):\n'
                '        self.prices.append(price)\n\n    def total(self):\n        result = 0\n        for price in self.prices:\n'
                '            result += price\n        return result\n\n    def fits(self, budget):\n'
                '        return self.total() < budget\n\n\ncart = Cart()\nfor price in prices:\n    cart.add(price)\n\n'
                'print(f"Сумма: {cart.total()}")\nif cart.fits(budget):\n    print("В бюджет укладываемся")\nelse:\n'
                '    print(f"Не хватает: {cart.total() - budget} руб.")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_METHOD,
                  ("re:self\\.total\\(\\s*\\)", "В методе fits вызови метод total того же объекта через self.total() — "
                                               "так сумма считается в одном месте.")],
    ),
]
