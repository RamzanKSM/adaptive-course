"""PY_ENCAPSULATION_BASIC — «Инкапсуляция». Taught before: everything up to functions, classes, creating objects,
__init__, methods and self. Here: an «internal» attribute `_x` / `__x` that code outside the class does not touch;
it changes only through methods that check the new value, and is read through a method. Not yet: @property (next
topic), inheritance, try/except and raise, tuples, dicts."""
from build import OutputTask

SKILL = "PY_ENCAPSULATION_BASIC"

NEED_CLASS = ("ClassDef", "Опиши объект в собственном классе через class.")
NEED_PRIVATE = ("re:self\\._\\w+\\s*=",
                "Храни значение во внутреннем атрибуте, имя которого начинается с подчёркивания, например self._best. "
                "Так видно, что снаружи класса его напрямую не меняют — только через методы.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-enc-rt-high-score", title="Рекорд в игре",
        given=["scores"],
        variants=[{"scores": "[350, 900, 420, 950, 100]"}, {"scores": "[1200, 800, 1100]"}, {"scores": "[40, 75, 75, 60]"}],
        hidden=[{"scores": "[]"}, {"scores": "[5]"}, {"scores": "[10, 20, 30, 40]"}, {"scores": "[999, 1000, 3]"}],
        intro="Игра хранит рекорд — лучший результат за все партии. После каждой партии результат отправляют в таблицу "
              "рекордов, но записывается он туда, только если он больше прежнего рекорда. Поэтому рекорд лежит "
              "во внутреннем атрибуте, а меняется только через метод с проверкой. В списке `scores` — результаты партий по порядку.",
        steps=["Создай класс `HighScore`. В `__init__(self)` заведи внутренний атрибут `self._best = 0`. "
               "Подчёркивание в начале имени означает: это внутренняя деталь класса, снаружи её напрямую не меняют.",
               "Добавь метод `submit(self, score)`: он записывает `score` в `self._best`, только если `score` больше "
               "текущего рекорда. Иначе рекорд не меняется.",
               "Добавь метод `get_best(self)`, который возвращает рекорд.",
               "Создай таблицу рекордов, отправь в неё по очереди все результаты из `scores` через метод `submit` "
               "и выведи строку вида `Best score: 950` — с рекордом, который вернул `get_best()`."],
        hint="Вся проверка живёт внутри метода `submit`, поэтому результаты нужно отправлять только через него. "
             "Если написать снаружи `table._best = score`, проверка не сработает и рекорд затрётся худшим результатом.",
        solution='class HighScore:\n    def __init__(self):\n        self._best = 0\n\n    def submit(self, score):\n'
                 '        if score > self._best:\n            self._best = score\n\n    def get_best(self):\n        return self._best\n\n\n'
                 'table = HighScore()\nfor score in scores:\n    table.submit(score)\nprint(f"Best score: {table.get_best()}")',
        wrong=[("метод submit не сравнивает с рекордом — в таблице остаётся последний результат",
                'class HighScore:\n    def __init__(self):\n        self._best = 0\n\n    def submit(self, score):\n'
                '        self._best = score\n\n    def get_best(self):\n        return self._best\n\n\n'
                'table = HighScore()\nfor score in scores:\n    table.submit(score)\nprint(f"Best score: {table.get_best()}")'),
               ("записывает результаты в обход метода, меняя table._best напрямую, — проверка не срабатывает",
                'class HighScore:\n    def __init__(self):\n        self._best = 0\n\n    def submit(self, score):\n'
                '        if score > self._best:\n            self._best = score\n\n    def get_best(self):\n        return self._best\n\n\n'
                'table = HighScore()\nfor score in scores:\n    table._best = score\nprint(f"Best score: {table.get_best()}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PRIVATE],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-enc-rt-chat-nick", title="Ник в чате",
        given=["start", "requests"],
        variants=[{"start": '"guest"', "requests": '["Ann", "Al", "Super Cat", "Ninja"]'},
                  {"start": '"newbie"', "requests": '["MaxPower2026xx", "Max"]'},
                  {"start": '"user"', "requests": '["Bob", "Bobby", "Bo b", "abcdefghijkl"]'}],
        hidden=[{"start": '"guest"', "requests": "[]"},
                {"start": '"player"', "requests": '["ab", "abcdefghijklm"]'},
                {"start": '"x1"', "requests": '["abc", "Tom Ford", "Kazan_Fox"]'}],
        intro="В школьном чате у каждого ученика есть ник. Ник должен быть длиной от 3 до 12 символов включительно "
              "и без пробелов — иначе его не примут. Ученик зашёл в чат с ником `start` и по очереди пробовал "
              "поменять его на ники из списка `requests`.",
        steps=["Создай класс `ChatUser`. В `__init__(self, nick)` сохрани ник во внутренний атрибут `self._nick`.",
               "Добавь метод `set_nick(self, nick)`. Если в `nick` от 3 до 12 символов включительно и в нём нет пробела, "
               "он сохраняет его в `self._nick` и выводит строку вида `Nick changed to Ann`. Иначе он выводит строку "
               "вида `Bad nick: Al` и ник не меняет.",
               "Добавь метод `get_nick(self)`, который возвращает текущий ник.",
               "Создай пользователя с ником `start` и передай в `set_nick` по очереди каждый ник из `requests`.",
               "В конце выведи строку вида `Current nick: Ninja` — с ником, который вернул `get_nick()`."],
        hint="Длину строки даёт `len(nick)`, а проверить, что пробела нет, можно так: `\" \" not in nick`. "
             "Оба условия нужны сразу — соедини их через `and`. Границы 3 и 12 тоже разрешены.",
        solution='class ChatUser:\n    def __init__(self, nick):\n        self._nick = nick\n\n    def set_nick(self, nick):\n'
                 '        if 3 <= len(nick) <= 12 and " " not in nick:\n            self._nick = nick\n'
                 '            print(f"Nick changed to {nick}")\n        else:\n            print(f"Bad nick: {nick}")\n\n'
                 '    def get_nick(self):\n        return self._nick\n\n\nuser = ChatUser(start)\nfor nick in requests:\n'
                 '    user.set_nick(nick)\nprint(f"Current nick: {user.get_nick()}")',
        wrong=[("не проверяет пробелы — принимает ник из двух слов",
                'class ChatUser:\n    def __init__(self, nick):\n        self._nick = nick\n\n    def set_nick(self, nick):\n'
                '        if 3 <= len(nick) <= 12:\n            self._nick = nick\n'
                '            print(f"Nick changed to {nick}")\n        else:\n            print(f"Bad nick: {nick}")\n\n'
                '    def get_nick(self):\n        return self._nick\n\n\nuser = ChatUser(start)\nfor nick in requests:\n'
                '    user.set_nick(nick)\nprint(f"Current nick: {user.get_nick()}")'),
               ("строгие сравнения — не принимает ники ровно из 3 и из 12 символов",
                'class ChatUser:\n    def __init__(self, nick):\n        self._nick = nick\n\n    def set_nick(self, nick):\n'
                '        if 3 < len(nick) < 12 and " " not in nick:\n            self._nick = nick\n'
                '            print(f"Nick changed to {nick}")\n        else:\n            print(f"Bad nick: {nick}")\n\n'
                '    def get_nick(self):\n        return self._nick\n\n\nuser = ChatUser(start)\nfor nick in requests:\n'
                '    user.set_nick(nick)\nprint(f"Current nick: {user.get_nick()}")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_PRIVATE],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-enc-rt-cinema-seats", title="Билеты на сеанс",
        given=["seats", "events"],
        variants=[{"seats": "30", "events": "[4, 10, -3, 25, 19]"},
                  {"seats": "10", "events": "[-2, 6, 5, -6, 5]"},
                  {"seats": "50", "events": "[20, -25, 30, 1, -50]"}],
        hidden=[{"seats": "5", "events": "[5, 1]"},
                {"seats": "8", "events": "[]"},
                {"seats": "12", "events": "[3, -3, -1, 12]"},
                {"seats": "20", "events": "[7, 7, 7, -14, 6]"}],
        intro="Касса кинотеатра продаёт билеты на сеанс, в зале `seats` мест. Нельзя продать больше билетов, чем "
              "осталось свободных мест, и нельзя вернуть больше билетов, чем было продано. В списке `events` по порядку "
              "записано, что происходило: положительное число — покупку стольких билетов, отрицательное — возврат.",
        steps=["Создай класс `Show`. В `__init__(self, seats)` заведи внутренние атрибуты с двумя подчёркиваниями: "
               "`self.__free = seats` (свободные места) и `self.__sold = 0` (продано билетов).",
               "Добавь метод `buy(self, count)`. Если `count` не больше свободных мест, он переносит `count` мест "
               "из свободных в проданные и выводит строку вида `Sold 4, free 26`. Иначе выводит строку вида "
               "`Only 7 seats left` с числом свободных мест и ничего не меняет.",
               "Добавь метод `refund(self, count)`. Если `count` не больше проданных билетов, он возвращает их "
               "в свободные места и выводит строку вида `Refund 3, free 19`. Иначе выводит строку вида "
               "`Cannot refund 2` и ничего не меняет.",
               "Добавь метод `get_sold(self)`, который возвращает число проданных билетов. Создай сеанс на `seats` мест "
               "и пройди циклом по `events`: положительное число передай в `buy`, отрицательное — в `refund`, "
               "но уже без минуса.",
               "Последней строкой выведи строку вида `Total sold: 14` — с числом, которое вернул `get_sold()`."],
        hint="Каждая проверка живёт в своём методе: `buy` смотрит на `self.__free`, `refund` — на `self.__sold`. "
             "Продать ровно все свободные места можно. Чтобы превратить отрицательное событие в положительное число, "
             "поставь перед ним минус: `-event`.",
        solution='class Show:\n    def __init__(self, seats):\n        self.__free = seats\n        self.__sold = 0\n\n'
                 '    def buy(self, count):\n        if count <= self.__free:\n            self.__free -= count\n'
                 '            self.__sold += count\n            print(f"Sold {count}, free {self.__free}")\n        else:\n'
                 '            print(f"Only {self.__free} seats left")\n\n    def refund(self, count):\n'
                 '        if count <= self.__sold:\n            self.__sold -= count\n            self.__free += count\n'
                 '            print(f"Refund {count}, free {self.__free}")\n        else:\n            print(f"Cannot refund {count}")\n\n'
                 '    def get_sold(self):\n        return self.__sold\n\n\nshow = Show(seats)\nfor event in events:\n'
                 '    if event > 0:\n        show.buy(event)\n    else:\n        show.refund(-event)\n'
                 'print(f"Total sold: {show.get_sold()}")',
        wrong=[("при возврате не проверяет, сколько продано, — проданных билетов становится меньше нуля",
                'class Show:\n    def __init__(self, seats):\n        self.__free = seats\n        self.__sold = 0\n\n'
                '    def buy(self, count):\n        if count <= self.__free:\n            self.__free -= count\n'
                '            self.__sold += count\n            print(f"Sold {count}, free {self.__free}")\n        else:\n'
                '            print(f"Only {self.__free} seats left")\n\n    def refund(self, count):\n'
                '        self.__sold -= count\n        self.__free += count\n'
                '        print(f"Refund {count}, free {self.__free}")\n\n'
                '    def get_sold(self):\n        return self.__sold\n\n\nshow = Show(seats)\nfor event in events:\n'
                '    if event > 0:\n        show.buy(event)\n    else:\n        show.refund(-event)\n'
                'print(f"Total sold: {show.get_sold()}")'),
               ("строгое сравнение при покупке — нельзя купить ровно все оставшиеся места",
                'class Show:\n    def __init__(self, seats):\n        self.__free = seats\n        self.__sold = 0\n\n'
                '    def buy(self, count):\n        if count < self.__free:\n            self.__free -= count\n'
                '            self.__sold += count\n            print(f"Sold {count}, free {self.__free}")\n        else:\n'
                '            print(f"Only {self.__free} seats left")\n\n    def refund(self, count):\n'
                '        if count <= self.__sold:\n            self.__sold -= count\n            self.__free += count\n'
                '            print(f"Refund {count}, free {self.__free}")\n        else:\n            print(f"Cannot refund {count}")\n\n'
                '    def get_sold(self):\n        return self.__sold\n\n\nshow = Show(seats)\nfor event in events:\n'
                '    if event > 0:\n        show.buy(event)\n    else:\n        show.refund(-event)\n'
                'print(f"Total sold: {show.get_sold()}")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_PRIVATE],
    ),
]
