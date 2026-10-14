"""PY_ENCAPSULATION_BASIC — «Инкапсуляция». Taught before: everything up to functions, classes, creating objects,
__init__, methods and self. Here: an «internal» attribute `_x` / `__x` that code outside the class does not touch;
it changes only through methods that check the new value, and is read through a method. Not yet: @property (next
topic), inheritance, try/except and raise, tuples, dicts."""
from build import OutputTask

SKILL = "PY_ENCAPSULATION_BASIC"

NEED_CLASS = ("ClassDef", "Опиши объект в собственном классе через class.")
NEED_PRIVATE = ("re:self\\._\\w+\\s*=",
                "Храни значение во внутреннем атрибуте, имя которого начинается с подчёркивания, например self._money. "
                "Так видно, что снаружи класса его напрямую не меняют — только через методы.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-enc-piggy-bank", title="Электронная копилка",
        given=["coins"],
        variants=[{"coins": "[10, -5, 50, 0, 20]"}, {"coins": "[100, 200, -50]"}, {"coins": "[-10, 5, 5, 0, 30]"}],
        hidden=[{"coins": "[]"}, {"coins": "[1, 2, 3]"}, {"coins": "[-100, -1]"}, {"coins": "[500, -500, 500]"}],
        intro="Младший брат складывает деньги в электронную копилку, но иногда по ошибке вводит ноль "
              "или отрицательную сумму. Копилка должна сама пропускать такие суммы — поэтому деньги лежат "
              "во внутреннем атрибуте, а менять их можно только через метод с проверкой.",
        steps=["Создай класс `PiggyBank`. В `__init__(self)` заведи внутренний атрибут `self._money = 0`. "
               "Подчёркивание в начале имени означает: это внутренняя деталь класса, снаружи её напрямую не меняют.",
               "Добавь метод `put(self, amount)`: он прибавляет `amount` к `self._money`, только если сумма больше нуля. "
               "Ноль и отрицательные суммы метод пропускает.",
               "Добавь метод `get_money(self)`, который возвращает, сколько денег в копилке.",
               "Создай копилку, положи в неё по очереди все суммы из списка `coins` через метод `put` "
               "и выведи строку вида `Piggy bank: 80 rub` — с суммой, которую вернул `get_money()`."],
        hint="Вся проверка живёт внутри метода `put`, поэтому деньги нужно класть только через него. "
             "Если написать снаружи `bank._money += coin`, проверка не сработает и копилка примет даже отрицательную сумму.",
        solution='class PiggyBank:\n    def __init__(self):\n        self._money = 0\n\n    def put(self, amount):\n'
                 '        if amount > 0:\n            self._money += amount\n\n    def get_money(self):\n        return self._money\n\n\n'
                 'bank = PiggyBank()\nfor coin in coins:\n    bank.put(coin)\nprint(f"Piggy bank: {bank.get_money()} rub")',
        wrong=[("метод put не проверяет сумму — отрицательные числа уменьшают копилку",
                'class PiggyBank:\n    def __init__(self):\n        self._money = 0\n\n    def put(self, amount):\n'
                '        self._money += amount\n\n    def get_money(self):\n        return self._money\n\n\n'
                'bank = PiggyBank()\nfor coin in coins:\n    bank.put(coin)\nprint(f"Piggy bank: {bank.get_money()} rub")'),
               ("кладёт деньги в обход метода, меняя bank._money напрямую, — проверка не срабатывает",
                'class PiggyBank:\n    def __init__(self):\n        self._money = 0\n\n    def put(self, amount):\n'
                '        if amount > 0:\n            self._money += amount\n\n    def get_money(self):\n        return self._money\n\n\n'
                'bank = PiggyBank()\nfor coin in coins:\n    bank._money += coin\nprint(f"Piggy bank: {bank.get_money()} rub")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PRIVATE],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-enc-thermostat", title="Термостат",
        given=["start", "requests"],
        variants=[{"start": "20", "requests": "[22, 35, 18]"},
                  {"start": "21", "requests": "[30, 25, 10]"},
                  {"start": "18", "requests": "[16, 28, 29, 15]"}],
        hidden=[{"start": "22", "requests": "[40]"},
                {"start": "19", "requests": "[17, 27, 5]"},
                {"start": "25", "requests": "[]"},
                {"start": "20", "requests": "[16, 50, 0]"}],
        intro="В квартире стоит умный термостат. Его температуру можно менять только от 16 до 28 градусов включительно — "
              "иначе батареи могут испортиться. Термостат включили на `start` градусов, а потом жильцы по очереди "
              "просили поставить температуры из списка `requests`.",
        steps=["Создай класс `Thermostat`. В `__init__(self, temp)` сохрани температуру во внутренний атрибут `self._temp`.",
               "Добавь метод `set_temp(self, value)`. Если `value` от 16 до 28 включительно, он сохраняет её в `self._temp` "
               "и выводит строку вида `Set: 22`. Иначе он выводит строку вида `Not allowed: 35` и температуру не меняет.",
               "Добавь метод `get_temp(self)`, который возвращает текущую температуру.",
               "Создай термостат с температурой `start` и передай в `set_temp` по очереди каждое значение из `requests`.",
               "В конце выведи строку вида `Temperature: 18` — со значением, которое вернул `get_temp()`."],
        hint="Сохранять новое значение нужно только внутри ветки `if`, где проверка прошла. Проверку диапазона "
             "удобно записать двойным сравнением: `16 <= value <= 28` — так границы 16 и 28 тоже разрешены.",
        solution='class Thermostat:\n    def __init__(self, temp):\n        self._temp = temp\n\n    def set_temp(self, value):\n'
                 '        if 16 <= value <= 28:\n            self._temp = value\n            print(f"Set: {value}")\n'
                 '        else:\n            print(f"Not allowed: {value}")\n\n    def get_temp(self):\n        return self._temp\n\n\n'
                 'thermostat = Thermostat(start)\nfor value in requests:\n    thermostat.set_temp(value)\n'
                 'print(f"Temperature: {thermostat.get_temp()}")',
        wrong=[("строгие сравнения — границы 16 и 28 отклоняются",
                'class Thermostat:\n    def __init__(self, temp):\n        self._temp = temp\n\n    def set_temp(self, value):\n'
                '        if 16 < value < 28:\n            self._temp = value\n            print(f"Set: {value}")\n'
                '        else:\n            print(f"Not allowed: {value}")\n\n    def get_temp(self):\n        return self._temp\n\n\n'
                'thermostat = Thermostat(start)\nfor value in requests:\n    thermostat.set_temp(value)\n'
                'print(f"Temperature: {thermostat.get_temp()}")'),
               ("сохраняет значение после проверки, вне if, — запрещённая температура всё равно ставится",
                'class Thermostat:\n    def __init__(self, temp):\n        self._temp = temp\n\n    def set_temp(self, value):\n'
                '        if 16 <= value <= 28:\n            print(f"Set: {value}")\n'
                '        else:\n            print(f"Not allowed: {value}")\n        self._temp = value\n\n'
                '    def get_temp(self):\n        return self._temp\n\n\n'
                'thermostat = Thermostat(start)\nfor value in requests:\n    thermostat.set_temp(value)\n'
                'print(f"Temperature: {thermostat.get_temp()}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PRIVATE],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-enc-phone-battery", title="Батарея телефона",
        given=["start", "events"],
        variants=[{"start": "50", "events": "[30, 45, -40, -20]"},
                  {"start": "90", "events": "[25, -60, -50]"},
                  {"start": "15", "events": "[-5, 70, 30, -35]"}],
        hidden=[{"start": "100", "events": "[-1]"},
                {"start": "40", "events": "[-40, 10]"},
                {"start": "60", "events": "[50, 50, -30]"},
                {"start": "5", "events": "[-20]"}],
        intro="Ты пишешь программу для батареи телефона. Заряд измеряется в процентах и всегда лежит от 0 до 100: "
              "зарядить больше 100 % нельзя, и разрядиться ниже нуля тоже. В начале заряд равен `start`, "
              "а в списке `events` по порядку записано, что происходило: положительное число — зарядку на столько "
              "процентов, отрицательное — расход.",
        steps=["Создай класс `Battery`. В `__init__(self, level)` сохрани заряд во внутренний атрибут `self.__level` — "
               "с двумя подчёркиваниями: тогда Python ещё и прячет его от кода снаружи класса.",
               "Добавь метод `charge(self, amount)`: он прибавляет `amount` к заряду, но если получилось больше 100, "
               "заряд становится ровно 100.",
               "Добавь метод `use(self, amount)`: он отнимает `amount` от заряда, но если получилось меньше 0, "
               "заряд становится ровно 0. И метод `get_level(self)`, который возвращает заряд.",
               "Создай батарею с зарядом `start` и пройди циклом по `events`: положительное число передай в `charge`, "
               "отрицательное — в `use`, но уже без минуса. После каждого события выведи строку вида `Battery: 80%`.",
               "Последней строкой выведи `Phone is off`, если заряд равен 0, а иначе — `Phone is on`."],
        hint="Сначала измени заряд, а потом поправь его, если он вышел за границы: например, после прибавления проверь "
             "`if self.__level > 100` и поставь ровно 100. Чтобы превратить отрицательное событие в положительное "
             "число, поставь перед ним минус: `-event`.",
        solution='class Battery:\n    def __init__(self, level):\n        self.__level = level\n\n    def charge(self, amount):\n'
                 '        self.__level += amount\n        if self.__level > 100:\n            self.__level = 100\n\n'
                 '    def use(self, amount):\n        self.__level -= amount\n        if self.__level < 0:\n            self.__level = 0\n\n'
                 '    def get_level(self):\n        return self.__level\n\n\nbattery = Battery(start)\nfor event in events:\n'
                 '    if event > 0:\n        battery.charge(event)\n    else:\n        battery.use(-event)\n'
                 '    print(f"Battery: {battery.get_level()}%")\n\nif battery.get_level() == 0:\n    print("Phone is off")\n'
                 'else:\n    print("Phone is on")',
        wrong=[("charge не ограничивает заряд сверху — получается больше 100 %",
                'class Battery:\n    def __init__(self, level):\n        self.__level = level\n\n    def charge(self, amount):\n'
                '        self.__level += amount\n\n'
                '    def use(self, amount):\n        self.__level -= amount\n        if self.__level < 0:\n            self.__level = 0\n\n'
                '    def get_level(self):\n        return self.__level\n\n\nbattery = Battery(start)\nfor event in events:\n'
                '    if event > 0:\n        battery.charge(event)\n    else:\n        battery.use(-event)\n'
                '    print(f"Battery: {battery.get_level()}%")\n\nif battery.get_level() == 0:\n    print("Phone is off")\n'
                'else:\n    print("Phone is on")'),
               ("use не ограничивает заряд снизу — заряд уходит в минус, и телефон «работает»",
                'class Battery:\n    def __init__(self, level):\n        self.__level = level\n\n    def charge(self, amount):\n'
                '        self.__level += amount\n        if self.__level > 100:\n            self.__level = 100\n\n'
                '    def use(self, amount):\n        self.__level -= amount\n\n'
                '    def get_level(self):\n        return self.__level\n\n\nbattery = Battery(start)\nfor event in events:\n'
                '    if event > 0:\n        battery.charge(event)\n    else:\n        battery.use(-event)\n'
                '    print(f"Battery: {battery.get_level()}%")\n\nif battery.get_level() == 0:\n    print("Phone is off")\n'
                'else:\n    print("Phone is on")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PRIVATE],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-enc-locker-code", title="Код камеры хранения",
        given=["codes"],
        variants=[{"codes": '["12a4", "2580", "123"]'}, {"codes": '["7777", "99999", "4x21"]'},
                  {"codes": '["abcd", "0451", "31", "8642"]'}],
        hidden=[{"codes": "[]"}, {"codes": '["1234"]'}, {"codes": '["12345", "12 4", "one"]'},
                {"codes": '["1111", "2222", "33a3"]'}],
        intro="В камере хранения на вокзале каждая ячейка закрывается кодом. Новая ячейка открывается кодом `0000`, "
              "а пассажир может поставить свой код — ровно из четырёх цифр. Пассажиры часто ошибаются при вводе, "
              "поэтому ячейка сама проверяет новый код. В списке `codes` — коды, которые по очереди вводил пассажир.",
        steps=["Создай класс `Locker`. В `__init__(self)` заведи внутренний атрибут `self._code = \"0000\"`. "
               "Подчёркивание в начале имени означает, что снаружи класса этот атрибут напрямую не меняют.",
               "Добавь метод `set_code(self, code)`: он сохраняет `code` в `self._code`, только если в строке ровно "
               "4 символа и все они — цифры. Неподходящий код метод пропускает, и старый код остаётся.",
               "Добавь метод `get_code(self)`, который возвращает текущий код.",
               "Создай ячейку, передай в `set_code` по очереди все коды из `codes` и выведи строку вида "
               "`Locker code: 2580` — с кодом, который вернул `get_code()`."],
        hint="Проверить, что строка состоит только из цифр, можно методом `code.isdigit()`, а длину строки даёт `len(code)`. "
             "Нужны оба условия сразу — соедини их через `and`. Код меняй только через `set_code`, иначе проверка не сработает.",
        solution='class Locker:\n    def __init__(self):\n        self._code = "0000"\n\n'
                 '    def set_code(self, code):\n        if len(code) == 4 and code.isdigit():\n'
                 '            self._code = code\n\n    def get_code(self):\n        return self._code\n\n\n'
                 'locker = Locker()\nfor code in codes:\n    locker.set_code(code)\n'
                 'print(f"Locker code: {locker.get_code()}")',
        wrong=[("проверяет только длину кода — код с буквами тоже принимается",
                'class Locker:\n    def __init__(self):\n        self._code = "0000"\n\n'
                '    def set_code(self, code):\n        if len(code) == 4:\n            self._code = code\n\n'
                '    def get_code(self):\n        return self._code\n\n\nlocker = Locker()\nfor code in codes:\n'
                '    locker.set_code(code)\nprint(f"Locker code: {locker.get_code()}")'),
               ("ставит код в обход метода, меняя locker._code напрямую, — проверка не срабатывает",
                'class Locker:\n    def __init__(self):\n        self._code = "0000"\n\n'
                '    def set_code(self, code):\n        if len(code) == 4 and code.isdigit():\n'
                '            self._code = code\n\n    def get_code(self):\n        return self._code\n\n\n'
                'locker = Locker()\nfor code in codes:\n    locker._code = code\n'
                'print(f"Locker code: {locker.get_code()}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PRIVATE],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-enc-library-book", title="Книга в школьной библиотеке",
        given=["title", "actions"],
        variants=[{"title": '"Dubrovsky"', "actions": '["Anya", "Boris", "back", "Boris"]'},
                  {"title": '"Mumu"', "actions": '["back", "Vika", "back", "Gleb", "back"]'},
                  {"title": '"The Hobbit"', "actions": '["Dasha", "back", "back", "Egor", "Zoya"]'}],
        hidden=[{"title": '"Kashtanka"', "actions": "[]"},
                {"title": '"Treasure Island"', "actions": '["Igor"]'},
                {"title": '"Robinson Crusoe"', "actions": '["Katya", "Lev", "Masha", "back", "back"]'}],
        intro="В школьной библиотеке есть один экземпляр книги `title`. Пока книга у читателя, взять её другому нельзя, "
              "а вернуть можно только книгу, которую кто-то брал. В списке `actions` по порядку записано, что происходило: "
              "имя ученика означает, что он пришёл взять книгу, а слово `back` — что книгу принесли обратно.",
        steps=["Создай класс `LibraryBook`. В `__init__(self, title)` сохрани название во внутренний атрибут `self._title`, "
               "а во внутренний атрибут `self._reader` — пустую строку: книга на полке, ни у кого её нет.",
               "Добавь метод `take(self, reader)`. Если книга на полке, он записывает читателя в `self._reader` и выводит "
               "строку вида `Anya took Dubrovsky`. Иначе выводит строку вида `Boris has to wait, the book is with Anya` "
               "и ничего не меняет.",
               "Добавь метод `give_back(self)`. Если книга у читателя, он выводит строку вида `Returned by Anya` и снова "
               "делает `self._reader` пустой строкой. Если книга и так на полке, он выводит `Nothing to return`.",
               "Добавь метод `is_on_shelf(self)`, который возвращает `True`, если книга на полке.",
               "Создай книгу и пройди циклом по `actions`: для `back` вызывай `give_back()`, для имени — `take(...)`. "
               "Последней строкой выведи `On the shelf: yes` или `On the shelf: no` по результату `is_on_shelf()`."],
        hint="Пустая строка в `self._reader` и означает «книга на полке», поэтому проверка — `self._reader == \"\"`. "
             "В `give_back` сначала выведи имя читателя и только потом очищай атрибут, иначе имя уже потеряется.",
        solution='class LibraryBook:\n    def __init__(self, title):\n        self._title = title\n'
                 '        self._reader = ""\n\n    def take(self, reader):\n        if self._reader == "":\n'
                 '            self._reader = reader\n            print(f"{reader} took {self._title}")\n'
                 '        else:\n            print(f"{reader} has to wait, the book is with {self._reader}")\n\n'
                 '    def give_back(self):\n        if self._reader != "":\n'
                 '            print(f"Returned by {self._reader}")\n            self._reader = ""\n        else:\n'
                 '            print("Nothing to return")\n\n    def is_on_shelf(self):\n'
                 '        return self._reader == ""\n\n\nbook = LibraryBook(title)\nfor action in actions:\n'
                 '    if action == "back":\n        book.give_back()\n    else:\n        book.take(action)\n\n'
                 'if book.is_on_shelf():\n    print("On the shelf: yes")\nelse:\n    print("On the shelf: no")',
        wrong=[("не проверяет, свободна ли книга, — её забирают прямо у другого читателя",
                'class LibraryBook:\n    def __init__(self, title):\n        self._title = title\n'
                '        self._reader = ""\n\n    def take(self, reader):\n        if True:\n'
                '            self._reader = reader\n            print(f"{reader} took {self._title}")\n'
                '        else:\n            print(f"{reader} has to wait, the book is with {self._reader}")\n\n'
                '    def give_back(self):\n        if self._reader != "":\n'
                '            print(f"Returned by {self._reader}")\n            self._reader = ""\n        else:\n'
                '            print("Nothing to return")\n\n    def is_on_shelf(self):\n'
                '        return self._reader == ""\n\n\nbook = LibraryBook(title)\nfor action in actions:\n'
                '    if action == "back":\n        book.give_back()\n    else:\n        book.take(action)\n\n'
                'if book.is_on_shelf():\n    print("On the shelf: yes")\nelse:\n    print("On the shelf: no")'),
               ("при возврате не очищает читателя — книга так и числится выданной",
                'class LibraryBook:\n    def __init__(self, title):\n        self._title = title\n'
                '        self._reader = ""\n\n    def take(self, reader):\n        if self._reader == "":\n'
                '            self._reader = reader\n            print(f"{reader} took {self._title}")\n'
                '        else:\n            print(f"{reader} has to wait, the book is with {self._reader}")\n\n'
                '    def give_back(self):\n        if self._reader != "":\n'
                '            print(f"Returned by {self._reader}")\n            pass\n        else:\n'
                '            print("Nothing to return")\n\n    def is_on_shelf(self):\n'
                '        return self._reader == ""\n\n\nbook = LibraryBook(title)\nfor action in actions:\n'
                '    if action == "back":\n        book.give_back()\n    else:\n        book.take(action)\n\n'
                'if book.is_on_shelf():\n    print("On the shelf: yes")\nelse:\n    print("On the shelf: no")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PRIVATE],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-enc-bank-card", title="Банковская карта и PIN-код",
        given=["pin", "balance", "pins", "amounts"],
        variants=[{"pin": '"1234"', "balance": "2000", "pins": '["1234", "1111", "1234", "1234"]',
                   "amounts": "[500, 300, 2000, 1500]"},
                  {"pin": '"0707"', "balance": "5000", "pins": '["7070", "0000", "7777", "0707"]',
                   "amounts": "[100, 100, 100, 100]"},
                  {"pin": '"4321"', "balance": "800", "pins": '["1111", "2222", "4321", "3333", "4321"]',
                   "amounts": "[50, 50, 300, 50, 500]"}],
        hidden=[{"pin": '"9999"', "balance": "1000", "pins": '["9999"]', "amounts": "[1000]"},
                {"pin": '"5555"', "balance": "300", "pins": '["1", "2", "5555", "3", "4", "5555"]',
                 "amounts": "[10, 10, 10, 10, 10, 10]"},
                {"pin": '"2468"', "balance": "700", "pins": '["0000", "1111", "2222", "2468"]',
                 "amounts": "[100, 100, 100, 100]"},
                {"pin": '"1357"', "balance": "400", "pins": '["1357", "1357", "1357"]', "amounts": "[401, 150, 250]"}],
        intro="Ты пишешь программу банкомата. У карты есть PIN-код `pin` и баланс `balance` рублей. Владелец по очереди "
              "пытается снять деньги: в списке `pins` — введённые PIN-коды, а в списке `amounts` на тех же местах — "
              "суммы. Если ввести неверный PIN три раза подряд, карта блокируется навсегда.",
        steps=["Создай класс `Card`. В `__init__(self, pin, balance)` сохрани PIN-код и баланс во внутренние атрибуты "
               "`self.__pin` и `self.__balance` (с двумя подчёркиваниями), а ещё заведи `self.__wrong = 0` — "
               "сколько неверных PIN-кодов введено подряд — и `self.__blocked = False`.",
               "Добавь метод `withdraw(self, pin, amount)`. Если карта заблокирована, он выводит `Card blocked` и больше "
               "ничего не делает.",
               "Если PIN неверный, метод увеличивает `self.__wrong` на 1. Если это третья ошибка подряд, он блокирует "
               "карту и выводит `Wrong PIN, card blocked`, иначе выводит `Wrong PIN`. Деньги при этом не снимаются.",
               "Если PIN верный, метод обнуляет `self.__wrong`. Если `amount` больше баланса, выводит `Not enough money`, "
               "иначе уменьшает баланс и выводит строку вида `Withdrawn: 500, left: 1500`.",
               "Добавь метод `get_balance(self)`. Создай карту, вызови `withdraw` для каждой пары из `pins` и `amounts` "
               "(цикл по `range(len(pins))`) и в конце выведи строку вида `Balance: 1500 rub`."],
        hint="Внутри метода удобно проверять случаи по очереди и выходить из метода через `return`, как только случай "
             "обработан: сначала блокировка, потом PIN, потом деньги. Снять ровно весь баланс можно — "
             "не хватает денег, только если сумма больше баланса.",
        solution='class Card:\n    def __init__(self, pin, balance):\n        self.__pin = pin\n'
                 '        self.__balance = balance\n        self.__wrong = 0\n        self.__blocked = False\n\n'
                 '    def withdraw(self, pin, amount):\n        if self.__blocked:\n'
                 '            print("Card blocked")\n            return\n        if pin != self.__pin:\n'
                 '            self.__wrong += 1\n            if self.__wrong == 3:\n'
                 '                self.__blocked = True\n                print("Wrong PIN, card blocked")\n'
                 '            else:\n                print("Wrong PIN")\n            return\n'
                 '        self.__wrong = 0\n        if amount > self.__balance:\n'
                 '            print("Not enough money")\n            return\n        self.__balance -= amount\n'
                 '        print(f"Withdrawn: {amount}, left: {self.__balance}")\n\n    def get_balance(self):\n'
                 '        return self.__balance\n\n\ncard = Card(pin, balance)\nfor i in range(len(pins)):\n'
                 '    card.withdraw(pins[i], amounts[i])\nprint(f"Balance: {card.get_balance()} rub")',
        wrong=[("не обнуляет счётчик ошибок после верного PIN — карта блокируется после трёх ошибок не подряд",
                'class Card:\n    def __init__(self, pin, balance):\n        self.__pin = pin\n'
                '        self.__balance = balance\n        self.__wrong = 0\n        self.__blocked = False\n\n'
                '    def withdraw(self, pin, amount):\n        if self.__blocked:\n'
                '            print("Card blocked")\n            return\n        if pin != self.__pin:\n'
                '            self.__wrong += 1\n            if self.__wrong == 3:\n'
                '                self.__blocked = True\n                print("Wrong PIN, card blocked")\n'
                '            else:\n                print("Wrong PIN")\n            return\n'
                '        if amount > self.__balance:\n            print("Not enough money")\n            return\n'
                '        self.__balance -= amount\n        print(f"Withdrawn: {amount}, left: {self.__balance}")\n'
                '\n    def get_balance(self):\n        return self.__balance\n\n\ncard = Card(pin, balance)\n'
                'for i in range(len(pins)):\n    card.withdraw(pins[i], amounts[i])\n'
                'print(f"Balance: {card.get_balance()} rub")'),
               ("не проверяет блокировку — после трёх ошибок с картой всё равно можно работать",
                'class Card:\n    def __init__(self, pin, balance):\n        self.__pin = pin\n'
                '        self.__balance = balance\n        self.__wrong = 0\n        self.__blocked = False\n\n'
                '    def withdraw(self, pin, amount):\n        if pin != self.__pin:\n'
                '            self.__wrong += 1\n            if self.__wrong == 3:\n'
                '                self.__blocked = True\n                print("Wrong PIN, card blocked")\n'
                '            else:\n                print("Wrong PIN")\n            return\n'
                '        self.__wrong = 0\n        if amount > self.__balance:\n'
                '            print("Not enough money")\n            return\n        self.__balance -= amount\n'
                '        print(f"Withdrawn: {amount}, left: {self.__balance}")\n\n    def get_balance(self):\n'
                '        return self.__balance\n\n\ncard = Card(pin, balance)\nfor i in range(len(pins)):\n'
                '    card.withdraw(pins[i], amounts[i])\nprint(f"Balance: {card.get_balance()} rub")'),
               ("не даёт снять весь баланс целиком — сравнивает через >=",
                'class Card:\n    def __init__(self, pin, balance):\n        self.__pin = pin\n'
                '        self.__balance = balance\n        self.__wrong = 0\n        self.__blocked = False\n\n'
                '    def withdraw(self, pin, amount):\n        if self.__blocked:\n'
                '            print("Card blocked")\n            return\n        if pin != self.__pin:\n'
                '            self.__wrong += 1\n            if self.__wrong == 3:\n'
                '                self.__blocked = True\n                print("Wrong PIN, card blocked")\n'
                '            else:\n                print("Wrong PIN")\n            return\n'
                '        self.__wrong = 0\n        if amount >= self.__balance:\n'
                '            print("Not enough money")\n            return\n        self.__balance -= amount\n'
                '        print(f"Withdrawn: {amount}, left: {self.__balance}")\n\n    def get_balance(self):\n'
                '        return self.__balance\n\n\ncard = Card(pin, balance)\nfor i in range(len(pins)):\n'
                '    card.withdraw(pins[i], amounts[i])\nprint(f"Balance: {card.get_balance()} rub")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_PRIVATE],
    ),
]
