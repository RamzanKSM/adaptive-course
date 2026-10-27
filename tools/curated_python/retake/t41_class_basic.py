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
        skill=SKILL, difficulty=1, slug="py-class-rt-game-player", title="Профиль игрока",
        given=["nick", "team", "level"],
        variants=[{"nick": '"Ghost"', "team": '"Wolves"', "level": "12"},
                  {"nick": '"Rocket"', "team": '"Tigers"', "level": "3"},
                  {"nick": '"Luna"', "team": '"Owls"', "level": "27"}],
        hidden=[{"nick": '"Blaze"', "team": '"Sharks"', "level": "1"},
                {"nick": '"Pixel"', "team": '"Bears"', "level": "50"},
                {"nick": '"Storm"', "team": '"Foxes"', "level": "8"}],
        intro="В онлайн-игре у каждого игрока есть профиль: ник, команда и уровень. Все профили устроены одинаково, "
              "поэтому профиль удобно один раз описать классом и создавать по нему объекты.",
        steps=["Создай класс `Player`. В его методе `__init__(self, nick, team, level)` сохрани параметры в атрибуты "
               "объекта: `self.nick`, `self.team` и `self.level`.",
               "Создай по классу объект из переменных заготовки: `player = Player(nick, team, level)`.",
               "Выведи две строки: `Nick: …` с атрибутом `player.nick` и `Team: …, level …` — сначала `player.team`, "
               "потом запятая, пробел, слово `level`, пробел и `player.level`. Например, `Team: Wolves, level 12`."],
        hint="Запись `Player(nick, team, level)` создаёт объект и сама вызывает `__init__`, а строки вида "
             "`self.team = team` кладут значения внутрь объекта. Достать их можно через точку: `player.team`. "
             "Порядок аргументов при создании должен совпадать с порядком параметров в `__init__`.",
        solution='class Player:\n    def __init__(self, nick, team, level):\n        self.nick = nick\n        self.team = team\n'
                 '        self.level = level\n\n\nplayer = Player(nick, team, level)\nprint(f"Nick: {player.nick}")\n'
                 'print(f"Team: {player.team}, level {player.level}")',
        wrong=[("перепутал порядок аргументов при создании объекта — ник и команда меняются местами",
                'class Player:\n    def __init__(self, nick, team, level):\n        self.nick = nick\n        self.team = team\n'
                '        self.level = level\n\n\nplayer = Player(team, nick, level)\nprint(f"Nick: {player.nick}")\n'
                'print(f"Team: {player.team}, level {player.level}")'),
               ("записал данные прямо в __init__ вместо параметров — профиль всегда один и тот же",
                'class Player:\n    def __init__(self):\n        self.nick = "Ghost"\n        self.team = "Wolves"\n'
                '        self.level = 12\n\n\nplayer = Player()\nprint(f"Nick: {player.nick}")\n'
                'print(f"Team: {player.team}, level {player.level}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-class-rt-dream-goal", title="Копим на мечту",
        given=["price", "saved"],
        variants=[{"price": "5000", "saved": "2500"},
                  {"price": "12000", "saved": "3000"},
                  {"price": "800", "saved": "600"}],
        hidden=[{"price": "1000", "saved": "0"},
                {"price": "4000", "saved": "4000"},
                {"price": "3000", "saved": "1000"}],
        intro="Ты копишь на новые наушники. Они стоят `price` рублей, а в копилке уже `saved` рублей. "
              "Нужно узнать, сколько ещё осталось накопить и какая часть цены уже собрана.",
        steps=["Создай класс `Goal`. В методе `__init__(self, price, saved)` сохрани цену и накопленную сумму в атрибуты "
               "`self.price` и `self.saved`.",
               "Добавь классу метод `left(self)`, который возвращает, сколько ещё осталось накопить: цену минус "
               "накопленное. Внутри метода бери данные из атрибутов объекта — через `self.`.",
               "Создай объект `goal = Goal(price, saved)` и выведи строку вида `Left: 2500 rub`, "
               "получив остаток вызовом `goal.left()`.",
               "Ниже выведи строку вида `Saved: 50%` — сколько процентов цены уже накоплено: `saved`, умноженное "
               "на 100 и делённое нацело на `price`."],
        hint="Метод — это функция внутри класса, и первым параметром у неё идёт `self` — сам объект. "
             "Поэтому в методе цена доступна как `self.price`. Вызывая метод, не забудь скобки: `goal.left()`.",
        solution='class Goal:\n    def __init__(self, price, saved):\n        self.price = price\n        self.saved = saved\n\n'
                 '    def left(self):\n        return self.price - self.saved\n\n\ngoal = Goal(price, saved)\n'
                 'print(f"Left: {goal.left()} rub")\nprint(f"Saved: {saved * 100 // price}%")',
        wrong=[("вызывает метод без скобок — вместо остатка печатается описание метода",
                'class Goal:\n    def __init__(self, price, saved):\n        self.price = price\n        self.saved = saved\n\n'
                '    def left(self):\n        return self.price - self.saved\n\n\ngoal = Goal(price, saved)\n'
                'print(f"Left: {goal.left} rub")\nprint(f"Saved: {saved * 100 // price}%")'),
               ("в проценты переводит остаток, а не накопленное",
                'class Goal:\n    def __init__(self, price, saved):\n        self.price = price\n        self.saved = saved\n\n'
                '    def left(self):\n        return self.price - self.saved\n\n\ngoal = Goal(price, saved)\n'
                'print(f"Left: {goal.left()} rub")\nprint(f"Saved: {goal.left() * 100 // price}%")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:def left\\(\\s*self", "Посчитай остаток в методе left(self) внутри класса Goal.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-class-rt-test-grade", title="Оценка за контрольную",
        given=["student", "points", "max_points"],
        variants=[{"student": '"Anya"', "points": "42", "max_points": "50"},
                  {"student": '"Timur"', "points": "18", "max_points": "40"},
                  {"student": '"Vera"', "points": "29", "max_points": "30"}],
        hidden=[{"student": '"Gleb"', "points": "45", "max_points": "50"},
                {"student": '"Dina"', "points": "35", "max_points": "50"},
                {"student": '"Egor"', "points": "25", "max_points": "50"},
                {"student": '"Lera"', "points": "24", "max_points": "50"},
                {"student": '"Oleg"', "points": "0", "max_points": "20"}],
        intro="Учитель переводит баллы за контрольную в оценку. Ученик `student` набрал `points` баллов из `max_points`. "
              "Оценка зависит от процента набранных баллов: от 90% — `5`, от 70% — `4`, от 50% — `3`, меньше 50% — `2`.",
        steps=["Создай класс `Test`. В методе `__init__(self, student, points)` сохрани имя и баллы "
               "в атрибуты `self.student` и `self.points`.",
               "Добавь метод `grade(self, max_points)`, который возвращает оценку числом. Сначала посчитай процент: "
               "`self.points`, умноженное на 100 и делённое нацело на `max_points`. Потом проверь границы: "
               "90 и больше — `5`, 70 и больше — `4`, 50 и больше — `3`, иначе `2`.",
               "Создай объект `test = Test(student, points)`.",
               "Выведи строку вида `Student: Anya, 42 of 50` — с атрибутами `test.student` и `test.points` и числом "
               "`max_points`, а второй строкой — `Grade: …` с результатом `test.grade(max_points)`."],
        hint="Умножай на 100 до деления: `42 // 50` даёт 0. Проверяй границы сверху вниз через `if`, `elif` и `else` "
             "и в каждой ветке возвращай свою оценку. Ровно 90% — это уже пятёрка.",
        solution='class Test:\n    def __init__(self, student, points):\n        self.student = student\n        self.points = points\n\n'
                 '    def grade(self, max_points):\n        percent = self.points * 100 // max_points\n'
                 '        if percent >= 90:\n            return 5\n        elif percent >= 70:\n            return 4\n'
                 '        elif percent >= 50:\n            return 3\n        else:\n            return 2\n\n\n'
                 'test = Test(student, points)\nprint(f"Student: {test.student}, {test.points} of {max_points}")\n'
                 'print(f"Grade: {test.grade(max_points)}")',
        wrong=[("строгие сравнения — на границе ставит оценку ниже",
                'class Test:\n    def __init__(self, student, points):\n        self.student = student\n        self.points = points\n\n'
                '    def grade(self, max_points):\n        percent = self.points * 100 // max_points\n'
                '        if percent > 90:\n            return 5\n        elif percent > 70:\n            return 4\n'
                '        elif percent > 50:\n            return 3\n        else:\n            return 2\n\n\n'
                'test = Test(student, points)\nprint(f"Student: {test.student}, {test.points} of {max_points}")\n'
                'print(f"Grade: {test.grade(max_points)}")'),
               ("сначала делит, потом умножает на 100 — процент почти всегда 0",
                'class Test:\n    def __init__(self, student, points):\n        self.student = student\n        self.points = points\n\n'
                '    def grade(self, max_points):\n        percent = self.points // max_points * 100\n'
                '        if percent >= 90:\n            return 5\n        elif percent >= 70:\n            return 4\n'
                '        elif percent >= 50:\n            return 3\n        else:\n            return 2\n\n\n'
                'test = Test(student, points)\nprint(f"Student: {test.student}, {test.points} of {max_points}")\n'
                'print(f"Grade: {test.grade(max_points)}")')],
        constructs=["class", "if"],
        must_use=[NEED_CLASS, NEED_INIT,
                  ("re:def grade\\(\\s*self", "Посчитай оценку в методе grade(self, max_points) внутри класса Test.")],
    ),
]
