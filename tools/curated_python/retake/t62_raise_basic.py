"""PY_RAISE_BASIC — «Выброс исключения raise». Taught before: everything up to comprehensions, then try/except,
separate except blocks for error types, else and finally. Here: a function checks its data and raises ValueError with
its own message; the caller catches it with `except ValueError as error` and shows that message."""
from build import OutputTask

SKILL = "PY_RAISE_BASIC"

RAISE = ("re:raise\\s+ValueError",
         "Сообщи о плохих данных из функции сам: `raise ValueError(\"text\")`. Так функция останавливается "
         "и передаёт ошибку тому, кто её вызвал.")

EMAIL = """\
def check_email(email):
    if "@" not in email:
        raise ValueError("Email must contain @")
    return email


try:
    address = check_email(email)
    print(f"Welcome letter sent to {address}")
except ValueError as error:
    print(f"Error: {error}")
"""

LOGIN = """\
def check_login(login, taken):
    if len(login) < 4:
        raise ValueError("Login is too short")
    if " " in login:
        raise ValueError("Login must not contain spaces")
    if login in taken:
        raise ValueError("Login is already taken")
    return login


try:
    name = check_login(login, taken)
    print(f"Registered: {name}")
except ValueError as error:
    print(f"Try again: {error}")
"""

ACCOUNT = """\
class Account:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Not enough money")
        self.balance -= amount


account = Account(start)
for action, amount in operations:
    try:
        if action == "deposit":
            account.deposit(amount)
        else:
            account.withdraw(amount)
        print(f"{action} {amount}: ok, balance {account.balance}")
    except ValueError as error:
        print(f"{action} {amount}: {error}")
print(f"Final balance: {account.balance} rub")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-raise-rt-email-check", title="Проверка почты",
        given=["email"],
        variants=[{"email": '"anya@mail.ru"'}, {"email": '"boris.mail.ru"'}, {"email": '"vera@yandex.ru"'}],
        hidden=[{"email": '"gleb"'}, {"email": '"@"'}, {"email": '"dina@inbox.ru"'}, {"email": '""'}],
        intro="Сайт секции отправляет приветственное письмо на адрес `email`, который ввёл пользователь. В адресе "
              "почты обязательно есть символ `@`. Если его нет, функция проверки должна выбросить ошибку, а сайт — "
              "показать её текст.",
        steps=["Напиши функцию `check_email(email)`. Если символа `@` в `email` нет, выброси `ValueError` "
               "с сообщением `Email must contain @`. Иначе верни `email`.",
               "Вызови функцию для `email` в блоке `try` и, если ошибки не было, выведи строку вида "
               "`Welcome letter sent to anya@mail.ru` — с адресом, который вернула функция.",
               "Перехвати ошибку блоком `except ValueError as error:` и выведи `Error: ` и текст ошибки — "
               "например, `Error: Email must contain @`."],
        hint="Проверить, есть ли символ в строке, можно через `in`: `\"@\" not in email`. Ошибку выбрасывают так: "
             "`raise ValueError(\"text\")` — функция сразу останавливается, а ошибку ловит `except` там, где функцию "
             "вызвали. После `as error` в переменной `error` лежит ошибка, и её текст можно вывести в f-строке.",
        solution=EMAIL,
        wrong=[("печатает сообщение вместо raise — письмо всё равно отправляется на неверный адрес",
                EMAIL.replace('        raise ValueError("Email must contain @")\n', '        print("Email must contain @")\n')),
               ("выбрасывает ValueError без сообщения — после «Error:» пусто",
                EMAIL.replace('        raise ValueError("Email must contain @")\n', '        raise ValueError\n'))],
        constructs=["function", "try", "if"],
        must_use=[RAISE],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-raise-rt-login-check", title="Регистрация логина",
        given=["login", "taken"],
        variants=[{"login": '"anya_k"', "taken": '["boris", "vera_v", "admin"]'},
                  {"login": '"admin"', "taken": '["boris", "vera_v", "admin"]'},
                  {"login": '"big cat"', "taken": '["boris", "vera_v", "admin"]'}],
        hidden=[{"login": '"abc"'}, {"login": '"abcd"'}, {"login": '"a b"'}, {"login": '"vera_v"'},
                {"login": '"Admin"'}, {"login": '"my login"', "taken": '["my login"]'}],
        intro="Игровой сайт регистрирует новых игроков. Игрок придумал логин `login`, а логины, которые уже заняты, "
              "лежат в списке `taken`. Функция проверки должна отказывать при плохом логине и объяснять, что не так.",
        steps=["Напиши функцию `check_login(login, taken)`. Проверки делай по порядку: если в логине меньше 4 символов, "
               "выброси `ValueError` с сообщением `Login is too short`; если в нём есть пробел — "
               "`Login must not contain spaces`; если он есть в `taken` — `Login is already taken`.",
               "Если все проверки пройдены, функция возвращает логин.",
               "Вызови функцию в блоке `try` и выведи строку вида `Registered: anya_k`.",
               "Перехвати `ValueError` через `except ValueError as error:` и выведи `Try again: ` и текст ошибки — "
               "например, `Try again: Login is already taken`."],
        hint="У одной функции может быть несколько `raise` — для каждой проблемы своё сообщение. Первый сработавший "
             "`raise` останавливает функцию, поэтому порядок проверок важен. Логин ровно из 4 символов подходит.",
        solution=LOGIN,
        wrong=[("отклоняет и логин ровно из 4 символов",
                LOGIN.replace("    if len(login) < 4:", "    if len(login) <= 4:")),
               ("возвращает текст ошибки через return вместо raise — плохой логин регистрируется",
                LOGIN.replace('        raise ValueError("Login is already taken")\n',
                              '        return "Login is already taken"\n')),
               ("не показывает текст ошибки — игрок не узнаёт, что не так",
                LOGIN.replace('except ValueError as error:\n    print(f"Try again: {error}")\n',
                              'except ValueError:\n    print("Try again")\n'))],
        constructs=["function", "try", "if"],
        must_use=[RAISE],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-raise-rt-bank-account", title="Банковский счёт",
        given=["start", "operations"],
        variants=[{"start": "1000", "operations": '[("withdraw", 300), ("deposit", 0), ("withdraw", 900), ("deposit", 500)]'},
                  {"start": "0", "operations": '[("withdraw", 100), ("deposit", 250), ("withdraw", 250)]'},
                  {"start": "500", "operations": '[("deposit", -50), ("withdraw", -10), ("withdraw", 501), ("deposit", 1)]'}],
        hidden=[{"start": "100", "operations": '[("withdraw", 100)]'},
                {"start": "100", "operations": '[("withdraw", 101), ("withdraw", 50)]'},
                {"start": "0", "operations": '[("deposit", 0), ("withdraw", 0)]'},
                {"start": "2000", "operations": '[("deposit", 700), ("withdraw", 2700), ("deposit", 30), ("withdraw", 40)]'}],
        intro="Банк ведёт счёт клиента. На счёте сначала `start` рублей. Операции лежат в списке `operations`: каждая — "
              "кортеж из действия (`\"deposit\"` — положить деньги, `\"withdraw\"` — снять) и суммы. Проверять сумму "
              "должен сам счёт: при неверной операции его методы выбрасывают ошибку, а программа показывает её текст "
              "и переходит к следующей операции.",
        steps=["Создай класс `Account`. В `__init__(self, balance)` сохрани баланс в `self.balance`.",
               "Метод `deposit(self, amount)`: если сумма меньше или равна 0, выброси `ValueError` с сообщением "
               "`Amount must be positive`; иначе прибавь её к балансу.",
               "Метод `withdraw(self, amount)`: если сумма меньше или равна 0 — та же ошибка `Amount must be positive`; "
               "если она больше баланса — `ValueError` с сообщением `Not enough money`; иначе вычти её из баланса.",
               "Создай `account = Account(start)` и пройди по `operations`, распаковывая каждую операцию. В блоке `try` "
               "вызови нужный метод и выведи строку вида `withdraw 300: ok, balance 700`. Если метод выбросил "
               "`ValueError`, выведи действие, сумму и текст ошибки — например, `deposit 0: Amount must be positive`.",
               "После цикла выведи строку вида `Final balance: 1200 rub`."],
        hint="Метод, как и функция, может выбросить ошибку через `raise` — она долетит до `try` в цикле, и строка "
             "`ok` после вызова не выполнится. Снять ровно весь баланс можно: тогда на счёте останется 0.",
        solution=ACCOUNT,
        wrong=[("не даёт снять ровно весь баланс",
                ACCOUNT.replace("        if amount > self.balance:", "        if amount >= self.balance:")),
               ("печатает сообщение вместо raise — неудачное снятие отмечается как ok",
                ACCOUNT.replace('            raise ValueError("Not enough money")\n',
                                '            print("Not enough money")\n            return\n')),
               ("try вокруг всего цикла — после первой ошибки остальные операции не выполняются",
                ACCOUNT.replace('for action, amount in operations:\n    try:\n        if action == "deposit":\n'
                                '            account.deposit(amount)\n        else:\n            account.withdraw(amount)\n'
                                '        print(f"{action} {amount}: ok, balance {account.balance}")\n'
                                '    except ValueError as error:\n        print(f"{action} {amount}: {error}")\n',
                                'try:\n    for action, amount in operations:\n        if action == "deposit":\n'
                                '            account.deposit(amount)\n        else:\n            account.withdraw(amount)\n'
                                '        print(f"{action} {amount}: ok, balance {account.balance}")\n'
                                'except ValueError as error:\n    print(f"{action} {amount}: {error}")\n'))],
        constructs=["class", "try", "for"],
        must_use=[RAISE, ("ClassDef", "Опиши счёт собственным классом `Account`: пусть его методы сами проверяют суммы.")],
    ),
]
