"""PY_FINALLY_BASIC — «Блок finally». Taught before: everything up to comprehensions, then try/except and separate
except blocks for different error types. Here: finally (runs always — after success, after an error, even after
return) and else (runs only when try had no error). Not yet: raise."""
from build import OutputTask

SKILL = "PY_FINALLY_BASIC"

# A try statement that has an else block: «else:» at the same indentation as an «except» line, right after its body.
TRY_ELSE = r"re:(?m)^([ \t]*)except\b[^\n]*\n(?:\1[ \t]+[^\n]*\n|[ \t]*\n)*\1else\s*:"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-fin-photo-booth", title="Фотобудка",
        given=["copies", "price"],
        variants=[{"copies": '"3"', "price": "50"}, {"copies": '"three"', "price": "40"}, {"copies": '"10"', "price": "35"}],
        hidden=[{"copies": '"1"', "price": "60"}, {"copies": '"x"', "price": "50"}, {"copies": '"5"', "price": "45"},
                {"copies": '""', "price": "50"}],
        intro="Фотобудка печатает снимки по {price} руб. за штуку. Сколько копий нужно, посетитель набирает на экране, "
              "поэтому число приходит строкой: `copies`, а цена одной копии лежит в `price`. "
              "Что бы ни случилось, в конце будка должна попрощаться.",
        steps=["В блоке `try` преврати `copies` в целое число, умножь на `price` и выведи сумму в виде "
               "`To pay: 100 rub`",
               "Если `int()` вызовет `ValueError`, выведи `Enter the number of photos in digits`.",
               "В блоке `finally` выведи `Thanks for coming!` — эта строка должна появляться всегда: "
               "и после оплаты, и после ошибки."],
        hint="Блок `finally` пишется после `except` и выполняется в любом случае — была ошибка или нет. "
             "Туда кладут то, что нужно сделать обязательно.",
        solution='try:\n    print(f"To pay: {int(copies) * price} rub")\nexcept ValueError:\n'
                 '    print("Enter the number of photos in digits")\nfinally:\n    print("Thanks for coming!")',
        wrong=[("прощается в конце try — после ошибки прощания нет",
                'try:\n    print(f"To pay: {int(copies) * price} rub")\n    print("Thanks for coming!")\n'
                'except ValueError:\n    print("Enter the number of photos in digits")'),
               ("прощается только в except — после удачной оплаты прощания нет",
                'try:\n    print(f"To pay: {int(copies) * price} rub")\nexcept ValueError:\n'
                '    print("Enter the number of photos in digits")\n    print("Thanks for coming!")')],
        constructs=["try"],
        must_use=[("re:finally\\s*:",
                   "Прощание выведи в блоке `finally:` — он выполняется в любом случае, была ошибка или нет."),
                  ("re:except\\s+ValueError",
                   "Неправильное количество поймай блоком `except ValueError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fin-age-rating", title="Возрастное ограничение фильма",
        given=["age_text", "rating"],
        variants=[{"age_text": '"15"', "rating": "16"}, {"age_text": '"21"', "rating": "18"},
                  {"age_text": '"fifteen"', "rating": "12"}],
        hidden=[{"age_text": '"16"', "rating": "16"}, {"age_text": '"abc"', "rating": "18"},
                {"age_text": '"6"', "rating": "0"}, {"age_text": '"11"', "rating": "12"}],
        intro="Перед фильмом с ограничением {rating}+ онлайн-кинотеатр спрашивает возраст зрителя. Возраст приходит "
              "из формы строкой: `age_text`, а ограничение фильма лежит в `rating`.",
        steps=["В блоке `try` только преврати `age_text` в целое число.",
               "В блоке `except ValueError` выведи `Age must be a number`.",
               "В блоке `else` (он выполняется, только если в `try` не было ошибки) сравни возраст с `rating`: "
               "если возраст не меньше `rating`, выведи `Enjoy the movie!`, иначе выведи "
               "`This movie is for ages {rating}+` (число возьми из `rating`).",
               "В блоке `finally` выведи `Check done` — эта строка нужна в любом случае."],
        hint="Блоки идут в таком порядке: `try`, `except`, `else`, `finally`. В `try` оставляй только то, что может "
             "сломаться, а то, что нужно сделать после удачи, переноси в `else`.",
        solution='try:\n    age = int(age_text)\nexcept ValueError:\n    print("Age must be a number")\n'
                 'else:\n    if age >= rating:\n        print("Enjoy the movie!")\n    else:\n'
                 '        print(f"This movie is for ages {rating}+")\nfinally:\n    print("Check done")',
        wrong=[("сравнивает возраст после try/except, а не в else — после ошибки печатается лишняя строка",
                'age = 0\ntry:\n    age = int(age_text)\nexcept ValueError:\n    print("Age must be a number")\n'
                'if age >= rating:\n    print("Enjoy the movie!")\nelse:\n    print(f"This movie is for ages {rating}+")\n'
                'print("Check done")'),
               ("«Check done» стоит в else, а не в finally — после ошибки этой строки нет",
                'try:\n    age = int(age_text)\nexcept ValueError:\n    print("Age must be a number")\n'
                'else:\n    if age >= rating:\n        print("Enjoy the movie!")\n    else:\n'
                '        print(f"This movie is for ages {rating}+")\n    print("Check done")')],
        constructs=["try", "if"],
        must_use=[(TRY_ELSE, "Добавь блок `else:` сразу после `except` — на том же уровне отступа. Туда переносят "
                             "действия, которые нужны только тогда, когда в `try` не было ошибки."),
                  ("re:finally\\s*:", "Строку `Check done` выведи в блоке `finally:` — "
                                      "он выполняется в любом случае.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fin-turnstile-log", title="Журнал турникета",
        given=["allowed", "passes"],
        variants=[{"allowed": "[1042, 1077, 1100]", "passes": '["1042", "abc", "2000"]'},
                  {"allowed": "[5, 17, 23]", "passes": '["17", "23", "1 7", "6"]'},
                  {"allowed": "[300, 301]", "passes": '["301", "three hundred", "299", "300"]'}],
        hidden=[{"passes": '["1042", "17", "300"]'},
                {"passes": '["x"]'},
                {"passes": '["5", "1100", "301", "?"]'},
                {"passes": '["23", "-", "1077"]'}],
        intro="Турникет в офисе считывает код с карты сотрудника. Коды, с которыми можно пройти, лежат в списке "
              "`allowed`, а коды карт, приложенных сегодня, — в списке `passes` строками, как их прочитал считыватель. "
              "Служба охраны требует, чтобы каждая попытка прохода попадала в журнал — и удачная, и с ошибкой.",
        steps=["Напиши функцию `check_pass(code)`. В блоке `try` преврати `code` в целое число: если это число есть "
               "в списке `allowed`, верни строку `come in`, иначе верни `no access`.",
               "Если `int()` вызвал `ValueError`, верни строку `card error`.",
               "Добавь блок `finally` и выведи в нём запись для журнала: `Log: ` и код карты, "
               "например `Log: 1234`.",
               "Для каждого кода из `passes` вызови функцию и выведи код и полученный ответ через двоеточие "
               "и пробел — например, `1234: come in`."],
        hint="`return` внутри `try` или `except` сразу завершает функцию — но перед выходом Python всё равно выполнит "
             "блок `finally`. Поэтому запись в журнал, сделанная там, появится при любом исходе — "
             "и раньше, чем ответ функции будет напечатан.",
        solution='def check_pass(code):\n    try:\n        if int(code) in allowed:\n            return "come in"\n'
                 '        return "no access"\n    except ValueError:\n        return "card error"\n'
                 '    finally:\n        print(f"Log: {code}")\n\n\n'
                 'for code in passes:\n    result = check_pass(code)\n    print(f"{code}: {result}")',
        wrong=[("пишет в журнал внутри try перед return — когда card error, записи в журнале нет",
                'def check_pass(code):\n    try:\n        number = int(code)\n        print(f"Log: {code}")\n'
                '        if number in allowed:\n            return "come in"\n        return "no access"\n'
                '    except ValueError:\n        return "card error"\n\n\n'
                'for code in passes:\n    result = check_pass(code)\n    print(f"{code}: {result}")'),
               ("пишет в журнал в цикле после ответа — строки выходят в другом порядке",
                'def check_pass(code):\n    try:\n        if int(code) in allowed:\n            return "come in"\n'
                '        return "no access"\n    except ValueError:\n        return "card error"\n\n\n'
                'for code in passes:\n    result = check_pass(code)\n    print(f"{code}: {result}")\n'
                '    print(f"Log: {code}")')],
        constructs=["function", "try", "for"],
        must_use=[("re:finally\\s*:", "Запись в журнал сделай в блоке `finally:` внутри функции — он выполняется "
                                      "даже после `return`, поэтому ни одна попытка не потеряется."),
                  ("re:except\\s+ValueError", "Нечитаемую карту поймай блоком `except ValueError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-fin-pizza-party", title="Пицца на всех",
        given=["slices", "friends"],
        variants=[{"slices": "12", "friends": "4"}, {"slices": "8", "friends": "0"}, {"slices": "10", "friends": "2"}],
        hidden=[{"slices": "6", "friends": "0"}, {"slices": "16", "friends": "5"}, {"slices": "8", "friends": "8"},
                {"slices": "2", "friends": "7"}],
        intro="На вечеринке пиццу из `slices` кусков делят поровну между `friends` друзьями. Иногда никто не пришёл, "
              "и тогда деление на ноль вызывает `ZeroDivisionError`. А пустую коробку в конце нужно выбросить в любом случае.",
        steps=["В блоке `try` раздели `slices` на `friends` нацело (через `//`) и выведи результат в виде "
               "`Each friend gets 3 slices`.",
               "Если возникла `ZeroDivisionError`, выведи `Nobody came, more pizza for me`.",
               "В блоке `finally` выведи `Box goes to recycling` — эта строка должна появляться всегда."],
        hint="`finally` пишется последним, после `except`, и выполняется и после удачи, и после ошибки. "
             "Если поставить строку в конец `try`, после ошибки до неё дело не дойдёт.",
        solution='try:\n    print(f"Each friend gets {slices // friends} slices")\nexcept ZeroDivisionError:\n'
                 '    print("Nobody came, more pizza for me")\nfinally:\n    print("Box goes to recycling")',
        wrong=[("выбрасывает коробку в конце try — после ошибки строки нет",
                'try:\n    print(f"Each friend gets {slices // friends} slices")\n    print("Box goes to recycling")\n'
                'except ZeroDivisionError:\n    print("Nobody came, more pizza for me")'),
               ("делит через / вместо // — получается дробное число",
                'try:\n    print(f"Each friend gets {slices / friends} slices")\nexcept ZeroDivisionError:\n'
                '    print("Nobody came, more pizza for me")\nfinally:\n    print("Box goes to recycling")')],
        constructs=["try"],
        must_use=[("re:finally\\s*:", "Строку про коробку выведи в блоке `finally:` — он выполняется в любом случае."),
                  ("re:except\\s+ZeroDivisionError", "Деление на ноль поймай блоком `except ZeroDivisionError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fin-phone-topup", title="Пополнение телефона",
        given=["amount_text", "balance"],
        variants=[{"amount_text": '"200"', "balance": "35"}, {"amount_text": '"5"', "balance": "120"},
                  {"amount_text": '"two hundred"', "balance": "0"}],
        hidden=[{"amount_text": '"10"', "balance": "1"}, {"amount_text": '"9"', "balance": "50"},
                {"amount_text": '"100 rub"', "balance": "40"}, {"amount_text": '"500"', "balance": "250"}],
        intro="Терминал пополняет баланс телефона. Сумму покупатель набирает на экране, и она приходит строкой "
              "`amount_text`, а текущий баланс лежит в `balance`. Меньше 10 руб. терминал не принимает. "
              "Чек терминал печатает всегда — даже если пополнить не получилось.",
        steps=["В блоке `try` только преврати `amount_text` в целое число.",
               "В блоке `except ValueError` выведи `Amount must be a number`.",
               "В блоке `else`: если сумма меньше 10, выведи `Minimum top-up is 10 rub`, иначе прибавь её к балансу "
               "и выведи строку вида `Balance: 235 rub`.",
               "В блоке `finally` выведи `Receipt printed`."],
        hint="Порядок блоков: `try`, `except`, `else`, `finally`. `else` выполняется только когда в `try` не было ошибки, "
             "а `finally` — всегда. Ровно 10 руб. терминал принимает.",
        solution='try:\n    amount = int(amount_text)\nexcept ValueError:\n    print("Amount must be a number")\n'
                 'else:\n    if amount < 10:\n        print("Minimum top-up is 10 rub")\n    else:\n'
                 '        balance += amount\n        print(f"Balance: {balance} rub")\nfinally:\n    print("Receipt printed")',
        wrong=[("не принимает ровно 10 рублей",
                'try:\n    amount = int(amount_text)\nexcept ValueError:\n    print("Amount must be a number")\n'
                'else:\n    if amount <= 10:\n        print("Minimum top-up is 10 rub")\n    else:\n'
                '        balance += amount\n        print(f"Balance: {balance} rub")\nfinally:\n    print("Receipt printed")'),
               ("печатает чек в else, а не в finally — после ошибки чека нет",
                'try:\n    amount = int(amount_text)\nexcept ValueError:\n    print("Amount must be a number")\n'
                'else:\n    if amount < 10:\n        print("Minimum top-up is 10 rub")\n    else:\n'
                '        balance += amount\n        print(f"Balance: {balance} rub")\n    print("Receipt printed")')],
        constructs=["try", "if"],
        must_use=[(TRY_ELSE, "Добавь блок `else:` сразу после `except` — на том же уровне отступа. Туда переносят "
                             "действия, которые нужны только тогда, когда в `try` не было ошибки."),
                  ("re:finally\\s*:", "Чек выведи в блоке `finally:` — он выполняется в любом случае.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fin-coffee-machine", title="Кофейный автомат",
        given=["menu", "orders"],
        variants=[{"menu": '{"latte": 180, "tea": 90, "cocoa": 150}', "orders": '[("tea", 100), ("mocha", 200), ("latte", 150)]'},
                  {"menu": '{"latte": 180, "tea": 90, "cocoa": 150}', "orders": '[("cocoa", 150), ("latte", 200)]'},
                  {"menu": '{"latte": 180, "tea": 90, "cocoa": 150}', "orders": '[("juice", 50), ("tea", 50), ("tea", 90)]'}],
        hidden=[{"orders": '[("latte", 180)]'},
                {"orders": '[("water", 10)]'},
                {"orders": '[("cocoa", 149), ("tea", 500), ("milk", 0), ("latte", 0)]'}],
        intro="Кофейный автомат готовит напитки по меню `menu` (напиток → цена в рублях). Заказы лежат в списке `orders`: "
              "каждый — кортеж из названия напитка и внесённой суммы. После каждого заказа — удачного или нет — "
              "автомат обязательно промывает трубки.",
        steps=["Напиши функцию `make(drink, paid)`. В блоке `try` возьми цену из `menu[drink]`. Если внесено меньше цены, "
               "верни строку вида `latte: need 30 rub more`, иначе верни строку вида `tea: ready, change 10 rub`.",
               "Если напитка нет в меню, `menu[drink]` вызовет `KeyError` — тогда верни строку вида `mocha: not on the menu`.",
               "Добавь в функцию блок `finally` и выведи в нём `Rinsing the tubes`.",
               "Для каждого заказа из `orders` вызови функцию и выведи то, что она вернула."],
        hint="`finally` выполняется даже после `return` — перед тем как функция отдаст ответ. Поэтому строка про промывку "
             "появится раньше, чем программа напечатает ответ функции.",
        solution='def make(drink, paid):\n    try:\n        price = menu[drink]\n        if paid < price:\n'
                 '            return f"{drink}: need {price - paid} rub more"\n        return f"{drink}: ready, change {paid - price} rub"\n'
                 '    except KeyError:\n        return f"{drink}: not on the menu"\n    finally:\n        print("Rinsing the tubes")\n\n\n'
                 'for drink, paid in orders:\n    print(make(drink, paid))',
        wrong=[("промывает трубки внутри try после взятия цены — после неизвестного напитка промывки нет",
                'def make(drink, paid):\n    try:\n        price = menu[drink]\n        print("Rinsing the tubes")\n'
                '        if paid < price:\n            return f"{drink}: need {price - paid} rub more"\n'
                '        return f"{drink}: ready, change {paid - price} rub"\n'
                '    except KeyError:\n        return f"{drink}: not on the menu"\n\n\n'
                'for drink, paid in orders:\n    print(make(drink, paid))'),
               ("промывает трубки в цикле после ответа — строки выходят в другом порядке",
                'def make(drink, paid):\n    try:\n        price = menu[drink]\n        if paid < price:\n'
                '            return f"{drink}: need {price - paid} rub more"\n        return f"{drink}: ready, change {paid - price} rub"\n'
                '    except KeyError:\n        return f"{drink}: not on the menu"\n\n\n'
                'for drink, paid in orders:\n    print(make(drink, paid))\n    print("Rinsing the tubes")'),
               ("отказывает, когда внесено ровно столько, сколько стоит напиток",
                'def make(drink, paid):\n    try:\n        price = menu[drink]\n        if paid <= price:\n'
                '            return f"{drink}: need {price - paid} rub more"\n        return f"{drink}: ready, change {paid - price} rub"\n'
                '    except KeyError:\n        return f"{drink}: not on the menu"\n    finally:\n        print("Rinsing the tubes")\n\n\n'
                'for drink, paid in orders:\n    print(make(drink, paid))')],
        constructs=["function", "try", "for"],
        must_use=[("re:finally\\s*:", "Промывку сделай в блоке `finally:` внутри функции — он выполняется даже после `return`."),
                  ("re:except\\s+KeyError", "Напиток не из меню поймай блоком `except KeyError:`.")],
    ),
]
