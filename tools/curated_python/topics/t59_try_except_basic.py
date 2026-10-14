"""PY_TRY_EXCEPT_BASIC — «Обработка ошибок try / except». Taught before: everything up to comprehensions (conditions,
loops, lists, dicts, string methods, functions, classes, f-strings; int("abc") raises ValueError). Here: put risky code
into try and react to an error in except instead of crashing. Not yet: several except blocks on purpose, finally, raise."""
from build import OutputTask

SKILL = "PY_TRY_EXCEPT_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-try-candy-share", title="Конфеты поровну",
        given=["candies", "kids"],
        variants=[{"candies": "20", "kids": "4"}, {"candies": "17", "kids": "0"}, {"candies": "30", "kids": "7"}],
        hidden=[{"candies": "9", "kids": "0"}, {"candies": "12", "kids": "5"}, {"candies": "100", "kids": "10"},
                {"candies": "0", "kids": "3"}],
        intro="После праздника конфеты из переменной `candies` хотят поровну раздать детям, а сколько детей пришло, "
              "записано в `kids`. Если детей нет, деление на ноль вызывает ошибку `ZeroDivisionError`, "
              "и программа останавливается. Нужно, чтобы вместо этого она спокойно сообщила, в чём дело.",
        steps=["В блоке `try` раздели `candies` на `kids` нацело (через `//`) и выведи результат в виде "
               "`Each gets: 3 pcs` — после двоеточия пробел, число, пробел и `pcs`.",
               "Добавь блок `except ZeroDivisionError:` и выведи в нём `No kids to share with`."],
        hint="Код, который может сломаться, ставь внутрь `try`. Если там случится деление на ноль, Python не остановит "
             "программу, а сразу перейдёт в блок `except` — и строки, стоящие в `try` после ошибки, уже не выполнятся.",
        solution='try:\n    print(f"Each gets: {candies // kids} pcs")\n'
                 'except ZeroDivisionError:\n    print("No kids to share with")',
        wrong=[("печатает результат после try/except — когда детей нет, появляется лишняя строка «Each gets: 0 pcs»",
                'share = 0\ntry:\n    share = candies // kids\nexcept ZeroDivisionError:\n'
                '    print("No kids to share with")\nprint(f"Each gets: {share} pcs")'),
               ("делит через / вместо // — получается дробное число",
                'try:\n    print(f"Each gets: {candies / kids} pcs")\n'
                'except ZeroDivisionError:\n    print("No kids to share with")')],
        constructs=["try"],
        must_use=[("re:except\\s+ZeroDivisionError",
                   "Перехвати именно ошибку деления на ноль: напиши `except ZeroDivisionError:`. "
                   "Так программа обработает эту ошибку и не спрячет другие, о которых тебе стоит знать.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-try-double-bonus", title="Двойные бонусы",
        given=["bonuses"],
        variants=[{"bonuses": '{"Anya": "120", "Boris": "no card", "Vika": "75"}'},
                  {"bonuses": '{"Gosha": "40", "Dina": "300", "Egor": "15", "Zhanna": "?"}'},
                  {"bonuses": '{"Zoya": "50", "Ilya": "", "Katya": "error", "Lyova": "210"}'}],
        hidden=[{"bonuses": '{"Misha": "error", "Nina": "10"}'},
                {"bonuses": '{"Oleg": "5", "Petya": "0", "Rita": "x", "Sasha": "1000"}'},
                {"bonuses": '{"Timur": "77"}'},
                {"bonuses": '{"Ulya": "-", "Fedor": "none"}'}],
        intro="В пятницу магазин удваивает бонусы на картах покупателей. Бонусы выгрузили из старой базы в словарь "
              "`bonuses` (имя покупателя → бонусы строкой), и у некоторых покупателей там вместо числа оказалась ерунда.",
        steps=["Перебери пары «имя — бонусы» из словаря `bonuses` через `.items()`.",
               "Для каждого покупателя в блоке `try` преврати бонусы в целое число, удвой их и выведи имя, "
               "двоеточие, пробел и удвоенное число — например, `Olya: 80`.",
               "Если бонусы записаны не числом, `int()` вызовет `ValueError`. Перехвати её и выведи имя и слова "
               "`bad data` — например, `Olya: bad data`.",
               "Покупатели после испорченной записи тоже должны получить свои бонусы."],
        hint="Поставь `try` внутрь цикла, а не вокруг него: тогда ошибка у одного покупателя прервёт только его шаг, "
             "и цикл спокойно перейдёт к следующему.",
        solution='for name, text in bonuses.items():\n    try:\n        print(f"{name}: {int(text) * 2}")\n'
                 '    except ValueError:\n        print(f"{name}: bad data")',
        wrong=[("try вокруг всего цикла — после первой испорченной записи остальные покупатели не обрабатываются",
                'try:\n    for name, text in bonuses.items():\n        print(f"{name}: {int(text) * 2}")\n'
                'except ValueError:\n    print(f"{name}: bad data")'),
               ("печатает бонусы после try/except — у испорченной записи выводится ещё и старое число",
                'for name, text in bonuses.items():\n    try:\n        points = int(text)\n'
                '    except ValueError:\n        print(f"{name}: bad data")\n'
                '    print(f"{name}: {points * 2}")')],
        constructs=["try", "for"],
        must_use=[("re:except\\s+ValueError",
                   "Перехвати именно ошибку превращения строки в число: напиши `except ValueError:`. "
                   "Так ты обработаешь только испорченные бонусы и не спрячешь другие ошибки.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-try-average-mark", title="Средний балл в журнале",
        given=["marks"],
        variants=[{"marks": '["5", "4", "abs", "3", "5", "4"]'},
                  {"marks": '["abs", "abs"]'},
                  {"marks": '["3", "5", "sick", "5"]'}],
        hidden=[{"marks": '["4", "4", "4"]'},
                {"marks": '["2", "x", "5", ""]'},
                {"marks": '[]'},
                {"marks": '["5", "abs", "5", "4", "abs"]'}],
        intro="В электронном журнале оценки ученика хранятся строками в списке `marks`. Если ученик пропустил урок, "
              "вместо оценки стоит `abs` или другая пометка. Нужно посчитать средний балл только по настоящим оценкам.",
        steps=["Заведи две переменные — для суммы и для количества оценок — и присвой обеим `0`. Перебери строки "
               "из `marks` и в блоке `try` преврати каждую в целое число.",
               "Если превращение удалось, прибавь оценку к сумме и увеличь количество на 1. Если возникла "
               "`ValueError`, пропусти эту запись (в блоке `except` можно написать `pass`).",
               "После цикла выведи `Marks counted: 3` — со своим количеством.",
               "Затем во втором блоке `try` раздели сумму на количество, округли через `round(..., 1)` "
               "и выведи в виде `Average mark: 4.5`.",
               "Если настоящих оценок нет, деление на ноль вызовет `ZeroDivisionError` — перехвати её и выведи "
               "`No marks yet` вместо среднего балла."],
        hint="Порядок строк внутри `try` важен: как только `int()` вызвал ошибку, остальные строки блока `try` "
             "не выполняются. Поэтому увеличивай счётчик после успешного превращения, а не до него.",
        solution='total = 0\ncount = 0\nfor mark in marks:\n    try:\n        total += int(mark)\n        count += 1\n'
                 '    except ValueError:\n        pass\nprint(f"Marks counted: {count}")\n'
                 'try:\n    print(f"Average mark: {round(total / count, 1)}")\n'
                 'except ZeroDivisionError:\n    print("No marks yet")',
        wrong=[("увеличивает счётчик до int() — пропуски тоже считаются оценками",
                'total = 0\ncount = 0\nfor mark in marks:\n    try:\n        count += 1\n        total += int(mark)\n'
                '    except ValueError:\n        pass\nprint(f"Marks counted: {count}")\n'
                'try:\n    print(f"Average mark: {round(total / count, 1)}")\n'
                'except ZeroDivisionError:\n    print("No marks yet")'),
               ("try вокруг всего цикла — оценки после первого пропуска не учитываются",
                'total = 0\ncount = 0\ntry:\n    for mark in marks:\n        total += int(mark)\n        count += 1\n'
                'except ValueError:\n    pass\nprint(f"Marks counted: {count}")\n'
                'try:\n    print(f"Average mark: {round(total / count, 1)}")\n'
                'except ZeroDivisionError:\n    print("No marks yet")')],
        constructs=["try", "for"],
        must_use=[("re:except\\s+ValueError",
                   "Пропуски вроде «abs» нужно отсеять, перехватив ошибку превращения в число: `except ValueError:`."),
                  ("re:except\\s+ZeroDivisionError",
                   "Случай, когда оценок нет, обработай вторым блоком `try` с `except ZeroDivisionError:` — "
                   "так ты потренируешься ловить и эту ошибку.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-try-age-field", title="Возраст из анкеты",
        given=["age_text"],
        variants=[{"age_text": '"14"'}, {"age_text": '"fourteen"'}, {"age_text": '"9"'}],
        hidden=[{"age_text": '"12 years"'}, {"age_text": '"30"'}, {"age_text": '""'}, {"age_text": '"0"'}],
        intro="На сайте кружка ребёнок вводит свой возраст в поле анкеты, и программа получает его строкой `age_text`. "
              "Если ввести не число, `int()` вызывает ошибку `ValueError`, и программа останавливается. "
              "Нужно, чтобы вместо этого она вежливо попросила ввести число.",
        steps=["В блоке `try` преврати `age_text` в целое число и выведи строку вида `Next year you will be 15` — "
               "возраст, увеличенный на 1.",
               "Добавь блок `except ValueError:` и выведи в нём `Please type your age in digits`."],
        hint="Если `int()` не смог превратить строку в число, Python сразу перейдёт в `except`, и печать внутри `try` "
             "уже не выполнится. Поэтому печатай результат внутри `try`, сразу после превращения.",
        solution='try:\n    age = int(age_text)\n    print(f"Next year you will be {age + 1}")\n'
                 'except ValueError:\n    print("Please type your age in digits")',
        wrong=[("забывает прибавить год — печатает текущий возраст",
                'try:\n    age = int(age_text)\n    print(f"Next year you will be {age}")\n'
                'except ValueError:\n    print("Please type your age in digits")'),
               ("приклеивает 1 к строке вместо сложения чисел — из 14 получается 141",
                'try:\n    age = int(age_text)\n    print(f"Next year you will be {age_text + \'1\'}")\n'
                'except ValueError:\n    print("Please type your age in digits")')],
        constructs=["try"],
        must_use=[("re:except\\s+ValueError",
                   "Перехвати именно ошибку превращения строки в число: напиши `except ValueError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-try-bike-segments", title="Скорость на участках",
        given=["segments"],
        variants=[{"segments": "[(3, 15), (2, 0), (5, 20)]"},
                  {"segments": "[(4, 12), (6, 30), (1, 0), (2, 0)]"},
                  {"segments": "[(0, 0), (10, 40)]"}],
        hidden=[{"segments": "[(6, 20)]"},
                {"segments": "[(1, 0)]"},
                {"segments": "[(9, 27), (0, 5), (3, 0), (8, 16)]"}],
        intro="Велокомпьютер разбил поездку на участки. Каждый участок в списке `segments` — кортеж из длины в километрах "
              "и времени в минутах. Иногда таймер сбоит и записывает 0 минут — тогда при делении на время "
              "возникает `ZeroDivisionError`.",
        steps=["Пройди по `segments` циклом с номером участка: номера начинаются с 1. Удобно так: "
               "`for i in range(len(segments)):`, а участок — `segments[i]`.",
               "Для каждого участка в блоке `try` посчитай скорость в км/ч нацело: `km * 60 // minutes` — и выведи "
               "строку вида `Segment 1: 12 km/h`.",
               "Если время равно нулю, перехвати `ZeroDivisionError` и выведи строку вида `Segment 2: timer error`.",
               "После цикла выведи строку вида `Errors: 1` — сколько участков оказались со сбоем."],
        hint="Поставь `try` внутрь цикла: тогда сбой на одном участке не помешает посчитать остальные. "
             "Счётчик сбоев увеличивай в блоке `except`.",
        solution='errors = 0\nfor i in range(len(segments)):\n    km, minutes = segments[i]\n    try:\n'
                 '        print(f"Segment {i + 1}: {km * 60 // minutes} km/h")\n    except ZeroDivisionError:\n'
                 '        print(f"Segment {i + 1}: timer error")\n        errors += 1\nprint(f"Errors: {errors}")',
        wrong=[("try вокруг всего цикла — после первого сбоя остальные участки не считаются",
                'errors = 0\ntry:\n    for i in range(len(segments)):\n        km, minutes = segments[i]\n'
                '        print(f"Segment {i + 1}: {km * 60 // minutes} km/h")\nexcept ZeroDivisionError:\n'
                '    print(f"Segment {i + 1}: timer error")\n    errors += 1\nprint(f"Errors: {errors}")'),
               ("нумерует участки с нуля",
                'errors = 0\nfor i in range(len(segments)):\n    km, minutes = segments[i]\n    try:\n'
                '        print(f"Segment {i}: {km * 60 // minutes} km/h")\n    except ZeroDivisionError:\n'
                '        print(f"Segment {i}: timer error")\n        errors += 1\nprint(f"Errors: {errors}")')],
        constructs=["try", "for"],
        must_use=[("re:except\\s+ZeroDivisionError",
                   "Сбой таймера поймай именно как ошибку деления на ноль: `except ZeroDivisionError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-try-ticket-sales", title="Продажа билетов",
        given=["left", "requests"],
        variants=[{"left": "10", "requests": '["3", "two", "8", "7"]'},
                  {"left": "5", "requests": '["many", "6", "?"]'},
                  {"left": "20", "requests": '["4", "4", "lots", "15", "5"]'}],
        hidden=[{"left": "1", "requests": '["1"]'},
                {"left": "3", "requests": '["x", "y"]'},
                {"left": "12", "requests": '["2", "12", "3", "a", "7"]'},
                {"left": "8", "requests": '["9", "8", "1"]'}],
        intro="В кассе кинотеатра осталось `left` билетов на вечерний сеанс. Покупатели по очереди вводят в автомате, "
              "сколько билетов им нужно, — запросы строками лежат в списке `requests`. Некоторые вводят не число.",
        steps=["Заведи счётчики проданных билетов и удачных продаж, обоим присвой `0`. Пройди по `requests` и в блоке `try` "
               "преврати запрос в целое число.",
               "Если билетов хватает (запрошено не больше, чем осталось), продай их: уменьши `left`, увеличь оба счётчика "
               "и выведи строку вида `3: sold, 7 left`. Иначе выведи строку вида `8: only 7 left` и ничего не продавай.",
               "Если запрос не число, перехвати `ValueError` и выведи запрос и слова `not a number` — например, "
               "`two: not a number`.",
               "После цикла во втором блоке `try` выведи строку вида `Average sale: 5` — сколько билетов в среднем "
               "покупали за одну удачную продажу, нацело через `//`. Если продаж не было, перехвати "
               "`ZeroDivisionError` и выведи `No sales`."],
        hint="Всё, что зависит от числа, ставь внутрь `try` после `int()`: если превращение не удалось, эти строки "
             "не выполнятся. Последние билеты продать можно — запрос, равный остатку, удачный.",
        solution='sold = 0\nsales = 0\nfor text in requests:\n    try:\n        wanted = int(text)\n'
                 '        if wanted <= left:\n            left -= wanted\n            sold += wanted\n            sales += 1\n'
                 '            print(f"{wanted}: sold, {left} left")\n        else:\n            print(f"{wanted}: only {left} left")\n'
                 '    except ValueError:\n        print(f"{text}: not a number")\ntry:\n'
                 '    print(f"Average sale: {sold // sales}")\nexcept ZeroDivisionError:\n    print("No sales")',
        wrong=[("не продаёт последние билеты — запрос, равный остатку, отклоняется",
                'sold = 0\nsales = 0\nfor text in requests:\n    try:\n        wanted = int(text)\n'
                '        if wanted < left:\n            left -= wanted\n            sold += wanted\n            sales += 1\n'
                '            print(f"{wanted}: sold, {left} left")\n        else:\n            print(f"{wanted}: only {left} left")\n'
                '    except ValueError:\n        print(f"{text}: not a number")\ntry:\n'
                '    print(f"Average sale: {sold // sales}")\nexcept ZeroDivisionError:\n    print("No sales")'),
               ("try вокруг всего цикла — после первого неправильного запроса продажи прекращаются",
                'sold = 0\nsales = 0\ntry:\n    for text in requests:\n        wanted = int(text)\n'
                '        if wanted <= left:\n            left -= wanted\n            sold += wanted\n            sales += 1\n'
                '            print(f"{wanted}: sold, {left} left")\n        else:\n            print(f"{wanted}: only {left} left")\n'
                'except ValueError:\n    print(f"{text}: not a number")\ntry:\n'
                '    print(f"Average sale: {sold // sales}")\nexcept ZeroDivisionError:\n    print("No sales")'),
               ("считает удачной продажей и отказ — среднее занижено",
                'sold = 0\nsales = 0\nfor text in requests:\n    try:\n        wanted = int(text)\n        sales += 1\n'
                '        if wanted <= left:\n            left -= wanted\n            sold += wanted\n'
                '            print(f"{wanted}: sold, {left} left")\n        else:\n            print(f"{wanted}: only {left} left")\n'
                '    except ValueError:\n        print(f"{text}: not a number")\ntry:\n'
                '    print(f"Average sale: {sold // sales}")\nexcept ZeroDivisionError:\n    print("No sales")')],
        constructs=["try", "for"],
        must_use=[("re:except\\s+ValueError", "Запрос, который не число, отсей, перехватив `except ValueError:`."),
                  ("re:except\\s+ZeroDivisionError",
                   "Случай без продаж обработай вторым блоком `try` с `except ZeroDivisionError:`.")],
    ),
]
