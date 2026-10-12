"""PY_RAISE_BASIC — «Выброс исключения raise». Taught before: everything up to comprehensions, then try/except,
separate except blocks for error types, else and finally. Here: a function checks its data and raises ValueError with
its own message; the caller catches it with `except ValueError as error` and shows that message."""
from build import OutputTask

SKILL = "PY_RAISE_BASIC"

RAISE = ("re:raise\\s+ValueError",
         "Сообщи о плохих данных из функции сам: `raise ValueError(\"текст\")`. Так функция останавливается "
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
               "`Возраст не может быть отрицательным`. Иначе верни `age`.",
               "Вызови функцию для `age` в блоке `try` и, если ошибки не было, выведи ответ функции в виде "
               "`Возраст принят: 30`.",
               "Перехвати ошибку блоком `except ValueError as error:` и выведи `Ошибка: ` и текст ошибки — "
               "например, `Ошибка: Возраст не может быть отрицательным`."],
        hint="Ошибку выбрасывают так: `raise ValueError(\"текст\")`. Функция на этом сразу останавливается, а ошибка "
             "переходит туда, где функцию вызвали, — там её и ловит `except`. После `as error` в переменной `error` "
             "лежит ошибка, и `print(error)` выводит её текст.",
        solution='def check_age(age):\n    if age < 0:\n        raise ValueError("Возраст не может быть отрицательным")\n'
                 '    return age\n\n\ntry:\n    result = check_age(age)\n    print(f"Возраст принят: {result}")\n'
                 'except ValueError as error:\n    print(f"Ошибка: {error}")',
        wrong=[("печатает сообщение вместо raise — анкета всё равно принимает отрицательный возраст",
                'def check_age(age):\n    if age < 0:\n        print("Возраст не может быть отрицательным")\n'
                '    return age\n\n\ntry:\n    result = check_age(age)\n    print(f"Возраст принят: {result}")\n'
                'except ValueError as error:\n    print(f"Ошибка: {error}")'),
               ("выбрасывает ValueError без сообщения — после «Ошибка:» пусто",
                'def check_age(age):\n    if age < 0:\n        raise ValueError\n'
                '    return age\n\n\ntry:\n    result = check_age(age)\n    print(f"Возраст принят: {result}")\n'
                'except ValueError as error:\n    print(f"Ошибка: {error}")')],
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
               "`Нужно забронировать хотя бы одно место`.",
               "Если `seats` больше `free`, функция выбрасывает `ValueError` с сообщением `Столько свободных мест нет`. "
               "Иначе она возвращает, сколько мест останется свободными.",
               "Вызови `book(seats, free)` в блоке `try` и выведи ответ в виде `Готово! Свободных мест осталось: 8`.",
               "Перехвати `ValueError` через `except ValueError as error:` и выведи `Бронь не создана: ` и текст "
               "ошибки — например, `Бронь не создана: Столько свободных мест нет`."],
        hint="У одной функции может быть несколько `raise` с разными сообщениями — для каждой проблемы своё. "
             "Тот, кто вызвал функцию, получит именно то сообщение, которое ты передал в `ValueError(...)`.",
        solution='def book(seats, free):\n    if seats < 1:\n        raise ValueError("Нужно забронировать хотя бы одно место")\n'
                 '    if seats > free:\n        raise ValueError("Столько свободных мест нет")\n    return free - seats\n\n\n'
                 'try:\n    left = book(seats, free)\n    print(f"Готово! Свободных мест осталось: {left}")\n'
                 'except ValueError as error:\n    print(f"Бронь не создана: {error}")',
        wrong=[("возвращает текст ошибки через return вместо raise — бронь считается созданной",
                'def book(seats, free):\n    if seats < 1:\n        return "Нужно забронировать хотя бы одно место"\n'
                '    if seats > free:\n        return "Столько свободных мест нет"\n    return free - seats\n\n\n'
                'try:\n    left = book(seats, free)\n    print(f"Готово! Свободных мест осталось: {left}")\n'
                'except ValueError as error:\n    print(f"Бронь не создана: {error}")'),
               ("не показывает текст ошибки — гость не узнаёт, почему бронь не создана",
                'def book(seats, free):\n    if seats < 1:\n        raise ValueError("Нужно забронировать хотя бы одно место")\n'
                '    if seats > free:\n        raise ValueError("Столько свободных мест нет")\n    return free - seats\n\n\n'
                'try:\n    left = book(seats, free)\n    print(f"Готово! Свободных мест осталось: {left}")\n'
                'except ValueError:\n    print("Бронь не создана")')],
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
               "с сообщением `Вес должен быть больше нуля`. Если вес больше `max_weight` — `ValueError` с сообщением "
               "`Слишком тяжёлая посылка`.",
               "Иначе функция возвращает стоимость: 150 руб. плюс 20 руб. за каждый килограмм.",
               "Перебери веса из `weights`. Для каждого вызови функцию в блоке `try`, прибавь стоимость к общей сумме "
               "и выведи вес и стоимость в виде `5 кг: 250 руб.`",
               "Если функция выбросила `ValueError`, выведи вес и текст ошибки — например, "
               "`0 кг: Вес должен быть больше нуля`. Такая посылка в сумму не входит, а следующие обрабатываются дальше.",
               "После цикла выведи общую сумму в виде `Итого: 1000 руб.`"],
        hint="Функция не решает, что печатать при плохом весе: она выбрасывает ошибку, а цикл ловит её и переходит "
             "к следующей посылке. Поэтому `try` нужен внутри цикла, а текст ошибки достаётся через `as error`.",
        solution='def parcel_cost(weight):\n    if weight <= 0:\n        raise ValueError("Вес должен быть больше нуля")\n'
                 '    if weight > max_weight:\n        raise ValueError("Слишком тяжёлая посылка")\n'
                 '    return 150 + 20 * weight\n\n\ntotal = 0\nfor weight in weights:\n    try:\n'
                 '        cost = parcel_cost(weight)\n        total += cost\n        print(f"{weight} кг: {cost} руб.")\n'
                 '    except ValueError as error:\n        print(f"{weight} кг: {error}")\nprint(f"Итого: {total} руб.")',
        wrong=[("try вокруг всего цикла — после первой плохой посылки остальные не считаются",
                'def parcel_cost(weight):\n    if weight <= 0:\n        raise ValueError("Вес должен быть больше нуля")\n'
                '    if weight > max_weight:\n        raise ValueError("Слишком тяжёлая посылка")\n'
                '    return 150 + 20 * weight\n\n\ntotal = 0\ntry:\n    for weight in weights:\n'
                '        cost = parcel_cost(weight)\n        total += cost\n        print(f"{weight} кг: {cost} руб.")\n'
                'except ValueError as error:\n    print(f"{weight} кг: {error}")\nprint(f"Итого: {total} руб.")'),
               ("печатает сообщение и возвращает 0 вместо raise — плохая посылка выглядит как бесплатная",
                'def parcel_cost(weight):\n    if weight <= 0:\n        print("Вес должен быть больше нуля")\n        return 0\n'
                '    if weight > max_weight:\n        print("Слишком тяжёлая посылка")\n        return 0\n'
                '    return 150 + 20 * weight\n\n\ntotal = 0\nfor weight in weights:\n    try:\n'
                '        cost = parcel_cost(weight)\n        total += cost\n        print(f"{weight} кг: {cost} руб.")\n'
                '    except ValueError as error:\n        print(f"{weight} кг: {error}")\nprint(f"Итого: {total} руб.")')],
        constructs=["function", "try", "for"],
        must_use=[RAISE],
    ),
]
