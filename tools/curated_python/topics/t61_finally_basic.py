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
        variants=[{"copies": '"3"', "price": "50"}, {"copies": '"три"', "price": "40"}, {"copies": '"10"', "price": "35"}],
        hidden=[{"copies": '"1"', "price": "60"}, {"copies": '"x"', "price": "50"}, {"copies": '"5"', "price": "45"},
                {"copies": '""', "price": "50"}],
        intro="Фотобудка печатает снимки по {price} руб. за штуку. Сколько копий нужно, посетитель набирает на экране, "
              "поэтому число приходит строкой: `copies`, а цена одной копии лежит в `price`. "
              "Что бы ни случилось, в конце будка должна попрощаться.",
        steps=["В блоке `try` преврати `copies` в целое число, умножь на `price` и выведи сумму в виде "
               "`К оплате: 100 руб.`",
               "Если `int()` вызовет `ValueError`, выведи `Количество фото нужно ввести цифрами`.",
               "В блоке `finally` выведи `Спасибо, что зашли!` — эта строка должна появляться всегда: "
               "и после оплаты, и после ошибки."],
        hint="Блок `finally` пишется после `except` и выполняется в любом случае — была ошибка или нет. "
             "Туда кладут то, что нужно сделать обязательно.",
        solution='try:\n    print(f"К оплате: {int(copies) * price} руб.")\nexcept ValueError:\n'
                 '    print("Количество фото нужно ввести цифрами")\nfinally:\n    print("Спасибо, что зашли!")',
        wrong=[("прощается в конце try — после ошибки прощания нет",
                'try:\n    print(f"К оплате: {int(copies) * price} руб.")\n    print("Спасибо, что зашли!")\n'
                'except ValueError:\n    print("Количество фото нужно ввести цифрами")'),
               ("прощается только в except — после удачной оплаты прощания нет",
                'try:\n    print(f"К оплате: {int(copies) * price} руб.")\nexcept ValueError:\n'
                '    print("Количество фото нужно ввести цифрами")\n    print("Спасибо, что зашли!")')],
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
                  {"age_text": '"пятнадцать"', "rating": "12"}],
        hidden=[{"age_text": '"16"', "rating": "16"}, {"age_text": '"abc"', "rating": "18"},
                {"age_text": '"6"', "rating": "0"}, {"age_text": '"11"', "rating": "12"}],
        intro="Перед фильмом с ограничением {rating}+ онлайн-кинотеатр спрашивает возраст зрителя. Возраст приходит "
              "из формы строкой: `age_text`, а ограничение фильма лежит в `rating`.",
        steps=["В блоке `try` только преврати `age_text` в целое число.",
               "В блоке `except ValueError` выведи `Возраст нужно указать числом`.",
               "В блоке `else` (он выполняется, только если в `try` не было ошибки) сравни возраст с `rating`: "
               "если возраст не меньше `rating`, выведи `Приятного просмотра!`, иначе выведи "
               "`Фильм доступен с {rating} лет` (число возьми из `rating`).",
               "В блоке `finally` выведи `Проверка окончена` — эта строка нужна в любом случае."],
        hint="Блоки идут в таком порядке: `try`, `except`, `else`, `finally`. В `try` оставляй только то, что может "
             "сломаться, а то, что нужно сделать после удачи, переноси в `else`.",
        solution='try:\n    age = int(age_text)\nexcept ValueError:\n    print("Возраст нужно указать числом")\n'
                 'else:\n    if age >= rating:\n        print("Приятного просмотра!")\n    else:\n'
                 '        print(f"Фильм доступен с {rating} лет")\nfinally:\n    print("Проверка окончена")',
        wrong=[("сравнивает возраст после try/except, а не в else — после ошибки печатается лишняя строка",
                'age = 0\ntry:\n    age = int(age_text)\nexcept ValueError:\n    print("Возраст нужно указать числом")\n'
                'if age >= rating:\n    print("Приятного просмотра!")\nelse:\n    print(f"Фильм доступен с {rating} лет")\n'
                'print("Проверка окончена")'),
               ("«Проверка окончена» стоит в else, а не в finally — после ошибки этой строки нет",
                'try:\n    age = int(age_text)\nexcept ValueError:\n    print("Возраст нужно указать числом")\n'
                'else:\n    if age >= rating:\n        print("Приятного просмотра!")\n    else:\n'
                '        print(f"Фильм доступен с {rating} лет")\n    print("Проверка окончена")')],
        constructs=["try", "if"],
        must_use=[(TRY_ELSE, "Добавь блок `else:` сразу после `except` — на том же уровне отступа. Туда переносят "
                             "действия, которые нужны только тогда, когда в `try` не было ошибки."),
                  ("re:finally\\s*:", "Строку `Проверка окончена` выведи в блоке `finally:` — "
                                      "он выполняется в любом случае.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fin-turnstile-log", title="Журнал турникета",
        given=["allowed", "passes"],
        variants=[{"allowed": "[1042, 1077, 1100]", "passes": '["1042", "abc", "2000"]'},
                  {"allowed": "[5, 17, 23]", "passes": '["17", "23", "1 7", "6"]'},
                  {"allowed": "[300, 301]", "passes": '["301", "три сотни", "299", "300"]'}],
        hidden=[{"passes": '["1042", "17", "300"]'},
                {"passes": '["x"]'},
                {"passes": '["5", "1100", "301", "?"]'},
                {"passes": '["23", "-", "1077"]'}],
        intro="Турникет в офисе считывает код с карты сотрудника. Коды, с которыми можно пройти, лежат в списке "
              "`allowed`, а коды карт, приложенных сегодня, — в списке `passes` строками, как их прочитал считыватель. "
              "Служба охраны требует, чтобы каждая попытка прохода попадала в журнал — и удачная, и с ошибкой.",
        steps=["Напиши функцию `check_pass(code)`. В блоке `try` преврати `code` в целое число: если это число есть "
               "в списке `allowed`, верни строку `проходите`, иначе верни `доступа нет`.",
               "Если `int()` вызвал `ValueError`, верни строку `карта не читается`.",
               "Добавь блок `finally` и выведи в нём запись для журнала: `Запись в журнал: ` и код карты, "
               "например `Запись в журнал: 1234`.",
               "Для каждого кода из `passes` вызови функцию и выведи код и полученный ответ через двоеточие "
               "и пробел — например, `1234: проходите`."],
        hint="`return` внутри `try` или `except` сразу завершает функцию — но перед выходом Python всё равно выполнит "
             "блок `finally`. Поэтому запись в журнал, сделанная там, появится при любом исходе — "
             "и раньше, чем ответ функции будет напечатан.",
        solution='def check_pass(code):\n    try:\n        if int(code) in allowed:\n            return "проходите"\n'
                 '        return "доступа нет"\n    except ValueError:\n        return "карта не читается"\n'
                 '    finally:\n        print(f"Запись в журнал: {code}")\n\n\n'
                 'for code in passes:\n    result = check_pass(code)\n    print(f"{code}: {result}")',
        wrong=[("пишет в журнал внутри try перед return — когда карта не читается, записи в журнале нет",
                'def check_pass(code):\n    try:\n        number = int(code)\n        print(f"Запись в журнал: {code}")\n'
                '        if number in allowed:\n            return "проходите"\n        return "доступа нет"\n'
                '    except ValueError:\n        return "карта не читается"\n\n\n'
                'for code in passes:\n    result = check_pass(code)\n    print(f"{code}: {result}")'),
               ("пишет в журнал в цикле после ответа — строки выходят в другом порядке",
                'def check_pass(code):\n    try:\n        if int(code) in allowed:\n            return "проходите"\n'
                '        return "доступа нет"\n    except ValueError:\n        return "карта не читается"\n\n\n'
                'for code in passes:\n    result = check_pass(code)\n    print(f"{code}: {result}")\n'
                '    print(f"Запись в журнал: {code}")')],
        constructs=["function", "try", "for"],
        must_use=[("re:finally\\s*:", "Запись в журнал сделай в блоке `finally:` внутри функции — он выполняется "
                                      "даже после `return`, поэтому ни одна попытка не потеряется."),
                  ("re:except\\s+ValueError", "Нечитаемую карту поймай блоком `except ValueError:`.")],
    ),
]
