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
]
