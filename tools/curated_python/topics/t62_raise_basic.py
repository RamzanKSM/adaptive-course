"""PY_RAISE_BASIC — «Выброс исключения raise». Taught before: everything up to comprehensions, then try/except,
separate except blocks for error types, else and finally. Here: a function checks its data and raises ValueError with
its own message; the caller catches it with `except ValueError as error` and shows that message."""
from build import OutputTask

SKILL = "PY_RAISE_BASIC"

RAISE = ("re:raise\\s+ValueError",
         "Сообщи о плохих данных из функции сам: `raise ValueError(\"text\")`. Так функция останавливается "
         "и передаёт ошибку тому, кто её вызвал.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-raise-age-check", title="Проверка возраста в анкете",
        given=["age"],
        variants=[{"age": "25"}, {"age": "-3"}, {"age": "40"}],
        hidden=[{"age": "0"}, {"age": "-1"}, {"age": "17"}, {"age": "-100"}],
        intro="Анкета на сайте проверяет возраст пользователя — он записан в `age`. Отрицательного возраста "
              "не бывает: в таком случае функция проверки должна выбросить ошибку, а анкета — показать её текст.",
        steps=["Напиши функцию `check_age(age)`. Если `age` меньше нуля, выброси `ValueError` с сообщением "
               "`Age cannot be negative`. Иначе верни `age`.",
               "Вызови функцию для `age` в блоке `try` и, если ошибки не было, выведи ответ функции в виде "
               "`Age accepted: 30`.",
               "Перехвати ошибку блоком `except ValueError as error:` и выведи `Error: ` и текст ошибки — "
               "например, `Error: Age cannot be negative`."],
        hint="Ошибку выбрасывают так: `raise ValueError(\"text\")`. Функция на этом сразу останавливается, а ошибка "
             "переходит туда, где функцию вызвали, — там её и ловит `except`. После `as error` в переменной `error` "
             "лежит ошибка, и `print(error)` выводит её текст.",
        solution='def check_age(age):\n    if age < 0:\n        raise ValueError("Age cannot be negative")\n'
                 '    return age\n\n\ntry:\n    result = check_age(age)\n    print(f"Age accepted: {result}")\n'
                 'except ValueError as error:\n    print(f"Error: {error}")',
        wrong=[("печатает сообщение вместо raise — анкета всё равно принимает отрицательный возраст",
                'def check_age(age):\n    if age < 0:\n        print("Age cannot be negative")\n'
                '    return age\n\n\ntry:\n    result = check_age(age)\n    print(f"Age accepted: {result}")\n'
                'except ValueError as error:\n    print(f"Error: {error}")'),
               ("выбрасывает ValueError без сообщения — после «Error:» пусто",
                'def check_age(age):\n    if age < 0:\n        raise ValueError\n'
                '    return age\n\n\ntry:\n    result = check_age(age)\n    print(f"Age accepted: {result}")\n'
                'except ValueError as error:\n    print(f"Error: {error}")')],
        constructs=["function", "try", "if"],
        must_use=[RAISE],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-raise-theatre-booking", title="Бронирование мест в театре",
        given=["seats", "free"],
        variants=[{"seats": "2", "free": "10"}, {"seats": "0", "free": "5"}, {"seats": "7", "free": "4"}],
        hidden=[{"seats": "5", "free": "5"}, {"seats": "6", "free": "5"}, {"seats": "-1", "free": "3"},
                {"seats": "1", "free": "30"}],
        intro="Сайт театра бронирует места на спектакль. Сколько мест хочет взять гость, записано в `seats`, "
              "а сколько мест свободно сейчас — в `free`. "
              "Функция бронирования должна отказывать, если запрос невыполним, и объяснять почему.",
        steps=["Напиши функцию `book(seats, free)`. Если `seats` меньше 1, она выбрасывает `ValueError` с сообщением "
               "`Book at least one seat`.",
               "Если `seats` больше `free`, функция выбрасывает `ValueError` с сообщением `Not enough free seats`. "
               "Иначе она возвращает, сколько мест останется свободными.",
               "Вызови `book(seats, free)` в блоке `try` и выведи ответ в виде `Done! Free seats left: 8`.",
               "Перехвати `ValueError` через `except ValueError as error:` и выведи `Booking failed: ` и текст "
               "ошибки — например, `Booking failed: Not enough free seats`."],
        hint="У одной функции может быть несколько `raise` с разными сообщениями — для каждой проблемы своё. "
             "Тот, кто вызвал функцию, получит именно то сообщение, которое ты передал в `ValueError(...)`.",
        solution='def book(seats, free):\n    if seats < 1:\n        raise ValueError("Book at least one seat")\n'
                 '    if seats > free:\n        raise ValueError("Not enough free seats")\n    return free - seats\n\n\n'
                 'try:\n    left = book(seats, free)\n    print(f"Done! Free seats left: {left}")\n'
                 'except ValueError as error:\n    print(f"Booking failed: {error}")',
        wrong=[("возвращает текст ошибки через return вместо raise — бронь считается созданной",
                'def book(seats, free):\n    if seats < 1:\n        return "Book at least one seat"\n'
                '    if seats > free:\n        return "Not enough free seats"\n    return free - seats\n\n\n'
                'try:\n    left = book(seats, free)\n    print(f"Done! Free seats left: {left}")\n'
                'except ValueError as error:\n    print(f"Booking failed: {error}")'),
               ("не показывает текст ошибки — гость не узнаёт, почему бронь не создана",
                'def book(seats, free):\n    if seats < 1:\n        raise ValueError("Book at least one seat")\n'
                '    if seats > free:\n        raise ValueError("Not enough free seats")\n    return free - seats\n\n\n'
                'try:\n    left = book(seats, free)\n    print(f"Done! Free seats left: {left}")\n'
                'except ValueError:\n    print("Booking failed")')],
        constructs=["function", "try", "if"],
        must_use=[RAISE],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-raise-parcel-cost", title="Стоимость посылок",
        given=["weights", "max_weight"],
        variants=[{"weights": "[2, 0, 5, 40]", "max_weight": "30"},
                  {"weights": "[10, 25, -1]", "max_weight": "20"},
                  {"weights": "[1, 3, 12]", "max_weight": "15"}],
        hidden=[{"weights": "[30, 31, 1]"}, {"weights": "[0, 0]"}, {"weights": "[7, 100, 4, 15]"},
                {"weights": "[20, 21]"}],
        intro="Почта принимает посылки весом до {max_weight} кг включительно — это число лежит в `max_weight`. "
              "Веса посылок, которые принесли сегодня, записаны в список `weights` (в килограммах). Нужно посчитать "
              "стоимость отправки каждой посылки и общую сумму.",
        steps=["Напиши функцию `parcel_cost(weight)`. Если вес меньше или равен нулю, она выбрасывает `ValueError` "
               "с сообщением `Weight must be above zero`. Если вес больше `max_weight` — `ValueError` с сообщением "
               "`Parcel is too heavy`.",
               "Иначе функция возвращает стоимость: 150 руб. плюс 20 руб. за каждый килограмм.",
               "Перебери веса из `weights`. Для каждого вызови функцию в блоке `try`, прибавь стоимость к общей сумме "
               "и выведи вес и стоимость в виде `5 kg: 250 rub`",
               "Если функция выбросила `ValueError`, выведи вес и текст ошибки — например, "
               "`0 kg: Weight must be above zero`. Такая посылка в сумму не входит, а следующие обрабатываются дальше.",
               "После цикла выведи общую сумму в виде `Total: 1000 rub`"],
        hint="Функция не решает, что печатать при плохом весе: она выбрасывает ошибку, а цикл ловит её и переходит "
             "к следующей посылке. Поэтому `try` нужен внутри цикла, а текст ошибки достаётся через `as error`.",
        solution='def parcel_cost(weight):\n    if weight <= 0:\n        raise ValueError("Weight must be above zero")\n'
                 '    if weight > max_weight:\n        raise ValueError("Parcel is too heavy")\n'
                 '    return 150 + 20 * weight\n\n\ntotal = 0\nfor weight in weights:\n    try:\n'
                 '        cost = parcel_cost(weight)\n        total += cost\n        print(f"{weight} kg: {cost} rub")\n'
                 '    except ValueError as error:\n        print(f"{weight} kg: {error}")\nprint(f"Total: {total} rub")',
        wrong=[("try вокруг всего цикла — после первой плохой посылки остальные не считаются",
                'def parcel_cost(weight):\n    if weight <= 0:\n        raise ValueError("Weight must be above zero")\n'
                '    if weight > max_weight:\n        raise ValueError("Parcel is too heavy")\n'
                '    return 150 + 20 * weight\n\n\ntotal = 0\ntry:\n    for weight in weights:\n'
                '        cost = parcel_cost(weight)\n        total += cost\n        print(f"{weight} kg: {cost} rub")\n'
                'except ValueError as error:\n    print(f"{weight} kg: {error}")\nprint(f"Total: {total} rub")'),
               ("печатает сообщение и возвращает 0 вместо raise — плохая посылка выглядит как бесплатная",
                'def parcel_cost(weight):\n    if weight <= 0:\n        print("Weight must be above zero")\n        return 0\n'
                '    if weight > max_weight:\n        print("Parcel is too heavy")\n        return 0\n'
                '    return 150 + 20 * weight\n\n\ntotal = 0\nfor weight in weights:\n    try:\n'
                '        cost = parcel_cost(weight)\n        total += cost\n        print(f"{weight} kg: {cost} rub")\n'
                '    except ValueError as error:\n        print(f"{weight} kg: {error}")\nprint(f"Total: {total} rub")')],
        constructs=["function", "try", "for"],
        must_use=[RAISE],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-raise-password-length", title="Длина пароля",
        given=["password"],
        variants=[{"password": '"sunflower7"'}, {"password": '"cat12"'}, {"password": '"qwerty12"'}],
        hidden=[{"password": '"abcdefg"'}, {"password": '""'}, {"password": '"correct horse battery"'},
                {"password": '"12345678"'}],
        intro="При регистрации пользователь придумывает пароль — он записан в `password`. Пароль короче 8 символов "
              "слишком легко подобрать: функция проверки должна выбросить ошибку, а сайт — показать её текст.",
        steps=["Напиши функцию `check_password(password)`. Если в пароле меньше 8 символов, выброси `ValueError` "
               "с сообщением `Password is too short`. Иначе верни длину пароля.",
               "Вызови функцию для `password` в блоке `try` и, если ошибки не было, выведи строку вида "
               "`Password saved, 10 characters`.",
               "Перехвати ошибку блоком `except ValueError as error:` и выведи `Error: ` и текст ошибки — "
               "например, `Error: Password is too short`."],
        hint="`raise ValueError(\"text\")` сразу останавливает функцию и передаёт ошибку туда, где функцию вызвали. "
             "Пароль ровно из 8 символов подходит.",
        solution='def check_password(password):\n    if len(password) < 8:\n        raise ValueError("Password is too short")\n'
                 '    return len(password)\n\n\ntry:\n    length = check_password(password)\n'
                 '    print(f"Password saved, {length} characters")\nexcept ValueError as error:\n    print(f"Error: {error}")',
        wrong=[("печатает сообщение вместо raise — короткий пароль всё равно сохраняется",
                'def check_password(password):\n    if len(password) < 8:\n        print("Password is too short")\n'
                '    return len(password)\n\n\ntry:\n    length = check_password(password)\n'
                '    print(f"Password saved, {length} characters")\nexcept ValueError as error:\n    print(f"Error: {error}")'),
               ("отклоняет и пароль ровно из 8 символов",
                'def check_password(password):\n    if len(password) <= 8:\n        raise ValueError("Password is too short")\n'
                '    return len(password)\n\n\ntry:\n    length = check_password(password)\n'
                '    print(f"Password saved, {length} characters")\nexcept ValueError as error:\n    print(f"Error: {error}")')],
        constructs=["function", "try", "if"],
        must_use=[RAISE],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-raise-alarm-time", title="Будильник",
        given=["hours", "minutes"],
        variants=[{"hours": "7", "minutes": "30"}, {"hours": "25", "minutes": "10"}, {"hours": "6", "minutes": "75"}],
        hidden=[{"hours": "0", "minutes": "0"}, {"hours": "23", "minutes": "59"}, {"hours": "24", "minutes": "0"},
                {"hours": "12", "minutes": "60"}, {"hours": "-1", "minutes": "5"}, {"hours": "9", "minutes": "-5"}],
        intro="Приложение-будильник получает время подъёма: часы `hours` и минуты `minutes`. Часы бывают только "
              "от 0 до 23, минуты — от 0 до 59. Функция установки должна отказывать при неверном времени "
              "и объяснять, что не так.",
        steps=["Напиши функцию `set_alarm(hours, minutes)`. Если часы меньше 0 или больше 23, выброси `ValueError` "
               "с сообщением `Hours must be from 0 to 23`.",
               "Если минуты меньше 0 или больше 59, выброси `ValueError` с сообщением `Minutes must be from 0 to 59`. "
               "Иначе верни строку вида `7 h 30 min`.",
               "Вызови функцию в блоке `try` и выведи строку вида `Alarm set for 7 h 30 min`.",
               "Перехвати `ValueError` через `except ValueError as error:` и выведи `Cannot set alarm: ` и текст ошибки."],
        hint="Проверяй часы раньше минут: если неверно и то и другое, пользователь увидит сообщение про часы. "
             "Границы 0, 23 и 59 — правильные значения.",
        solution='def set_alarm(hours, minutes):\n    if hours < 0 or hours > 23:\n        raise ValueError("Hours must be from 0 to 23")\n'
                 '    if minutes < 0 or minutes > 59:\n        raise ValueError("Minutes must be from 0 to 59")\n'
                 '    return f"{hours} h {minutes} min"\n\n\ntry:\n    print(f"Alarm set for {set_alarm(hours, minutes)}")\n'
                 'except ValueError as error:\n    print(f"Cannot set alarm: {error}")',
        wrong=[("считает 24 часа и 60 минут правильным временем",
                'def set_alarm(hours, minutes):\n    if hours < 0 or hours > 24:\n        raise ValueError("Hours must be from 0 to 23")\n'
                '    if minutes < 0 or minutes > 60:\n        raise ValueError("Minutes must be from 0 to 59")\n'
                '    return f"{hours} h {minutes} min"\n\n\ntry:\n    print(f"Alarm set for {set_alarm(hours, minutes)}")\n'
                'except ValueError as error:\n    print(f"Cannot set alarm: {error}")'),
               ("не проверяет отрицательные значения",
                'def set_alarm(hours, minutes):\n    if hours > 23:\n        raise ValueError("Hours must be from 0 to 23")\n'
                '    if minutes > 59:\n        raise ValueError("Minutes must be from 0 to 59")\n'
                '    return f"{hours} h {minutes} min"\n\n\ntry:\n    print(f"Alarm set for {set_alarm(hours, minutes)}")\n'
                'except ValueError as error:\n    print(f"Cannot set alarm: {error}")')],
        constructs=["function", "try", "if"],
        must_use=[RAISE],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-raise-test-marks", title="Оценки за контрольную",
        given=["marks"],
        variants=[{"marks": '["5", "four", "3", "7", "4"]'},
                  {"marks": '["0", "x", "6"]'},
                  {"marks": '["2", "5", "5", "1", "-3"]'}],
        hidden=[{"marks": '["4"]'},
                {"marks": '["", "9"]'},
                {"marks": '["1", "5", "10", "3", "abc", "5"]'},
                {"marks": '["5", "5"]'}],
        intro="Учитель вносит оценки за контрольную в таблицу, и они попадают в программу строками — список `marks`. "
              "Иногда в таблицу попадает опечатка: слово вместо числа или число вне шкалы от 1 до 5. Такие записи "
              "нужно показать с объяснением, а средний балл посчитать только по правильным оценкам.",
        steps=["Напиши функцию `parse_mark(text)`. Если строка не состоит из одних цифр (метод `.isdigit()`), выброси "
               "`ValueError` с сообщением `not a number`. Преврати строку в число; если оно меньше 1 или больше 5, "
               "выброси `ValueError` с сообщением `must be from 1 to 5`. Иначе верни оценку.",
               "Заведи сумму и количество, обоим присвой 0. Для каждой строки из `marks` вызови функцию в блоке `try` "
               "и учти оценку в сумме и количестве.",
               "Если функция выбросила ошибку, выведи строку и текст ошибки через двоеточие — например, `four: not a number`.",
               "После цикла выведи строку вида `Average: 4.2` — среднее, округлённое через `round(..., 1)`. "
               "Если правильных оценок нет, выведи `No valid marks`."],
        hint="`\"-3\".isdigit()` возвращает `False`: минус — не цифра, поэтому для такой строки будет `not a number`. "
             "`try` ставь внутрь цикла, чтобы одна опечатка не мешала остальным оценкам.",
        solution='def parse_mark(text):\n    if not text.isdigit():\n        raise ValueError("not a number")\n'
                 '    mark = int(text)\n    if mark < 1 or mark > 5:\n        raise ValueError("must be from 1 to 5")\n'
                 '    return mark\n\n\ntotal = 0\ncount = 0\nfor text in marks:\n    try:\n        mark = parse_mark(text)\n'
                 '        total += mark\n        count += 1\n    except ValueError as error:\n        print(f"{text}: {error}")\n'
                 'if count == 0:\n    print("No valid marks")\nelse:\n    print(f"Average: {round(total / count, 1)}")',
        wrong=[("не проверяет шкалу — оценки 0, 6 и 7 входят в средний балл",
                'def parse_mark(text):\n    if not text.isdigit():\n        raise ValueError("not a number")\n'
                '    return int(text)\n\n\ntotal = 0\ncount = 0\nfor text in marks:\n    try:\n        mark = parse_mark(text)\n'
                '        total += mark\n        count += 1\n    except ValueError as error:\n        print(f"{text}: {error}")\n'
                'if count == 0:\n    print("No valid marks")\nelse:\n    print(f"Average: {round(total / count, 1)}")'),
               ("try вокруг всего цикла — оценки после первой опечатки не учитываются",
                'def parse_mark(text):\n    if not text.isdigit():\n        raise ValueError("not a number")\n'
                '    mark = int(text)\n    if mark < 1 or mark > 5:\n        raise ValueError("must be from 1 to 5")\n'
                '    return mark\n\n\ntotal = 0\ncount = 0\ntry:\n    for text in marks:\n        mark = parse_mark(text)\n'
                '        total += mark\n        count += 1\nexcept ValueError as error:\n    print(f"{text}: {error}")\n'
                'if count == 0:\n    print("No valid marks")\nelse:\n    print(f"Average: {round(total / count, 1)}")'),
               ("увеличивает количество до проверки — опечатки тоже попадают в делитель",
                'def parse_mark(text):\n    if not text.isdigit():\n        raise ValueError("not a number")\n'
                '    mark = int(text)\n    if mark < 1 or mark > 5:\n        raise ValueError("must be from 1 to 5")\n'
                '    return mark\n\n\ntotal = 0\ncount = 0\nfor text in marks:\n    try:\n        count += 1\n'
                '        mark = parse_mark(text)\n        total += mark\n    except ValueError as error:\n        print(f"{text}: {error}")\n'
                'if count == 0:\n    print("No valid marks")\nelse:\n    print(f"Average: {round(total / count, 1)}")')],
        constructs=["function", "try", "for"],
        must_use=[RAISE],
    ),
]
