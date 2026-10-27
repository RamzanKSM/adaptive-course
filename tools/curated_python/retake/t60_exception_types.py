"""PY_EXCEPTION_TYPES — «Типы исключений». Taught before: everything up to comprehensions, then try/except.
Here: tell errors apart — ValueError, ZeroDivisionError, KeyError, IndexError, TypeError — with a separate except
block for each and a different reaction. Not yet: finally, raise."""
from build import OutputTask

SKILL = "PY_EXCEPTION_TYPES"

QUARTERS = """\
try:
    marks = quarters[number - 1]
    print(f"Quarter {number}: {len(marks)} marks")
    print(f"Average: {round(sum(marks) / len(marks), 1)}")
except IndexError:
    print(f"There is no quarter {number}")
except ZeroDivisionError:
    print("No marks yet")
"""

EXCHANGE = """\
bought = 0
for currency, rubles in requests:
    try:
        units = rubles // rates[currency]
        print(f"{rubles} rub -> {units} {currency}")
        bought += 1
    except KeyError:
        print(f"{currency}: unknown currency")
    except ZeroDivisionError:
        print(f"{currency}: not sold today")
    except TypeError:
        print(f"{currency}: amount must be a number")
print(f"Successful: {bought}")
"""

RATES = '{"USD": 90, "EUR": 100, "CNY": 0, "TRY": 3}'

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-exc-rt-points-per-game", title="Очки за игру",
        given=["points", "player", "games"],
        variants=[{"points": '{"Anya": 120, "Boris": 75, "Vera": 0}', "player": '"Anya"', "games": "10"},
                  {"points": '{"Anya": 120, "Boris": 75, "Vera": 0}', "player": '"Gleb"', "games": "4"},
                  {"points": '{"Anya": 120, "Boris": 75, "Vera": 0}', "player": '"Boris"', "games": "0"}],
        hidden=[{"player": '"Vera"', "games": "3"}, {"player": '"Dina"', "games": "0"},
                {"player": '"Boris"', "games": "5"}, {"player": '"anya"', "games": "2"},
                {"player": '"Anya"', "games": "0"}],
        intro="В школьной лиге настольных игр очки игроков хранятся в словаре `points`: ключ — имя, значение — "
              "сумма очков. Нужно узнать, сколько очков в среднем приносила игроку `player` одна игра, если он "
              "сыграл `games` игр. Ошибиться можно двумя способами, и ответы на них разные.",
        steps=["В блоке `try` возьми очки игрока из словаря: `points[player]`, раздели их на `games` нацело "
               "и выведи строку вида `Points per game: 12`.",
               "Если такого игрока нет в словаре, возникнет `KeyError` — перехвати её своим блоком `except` и выведи "
               "`No such player`.",
               "Если игрок ещё не сыграл ни одной игры, деление вызовет `ZeroDivisionError` — перехвати её отдельным "
               "блоком `except` и выведи `No games played yet`."],
        hint="После одного `try` можно поставить несколько блоков `except` подряд — каждый для своего типа ошибки. "
             "Python выполнит тот, тип которого совпал с ошибкой. Имена в словаре различают большие и маленькие буквы.",
        solution='try:\n    print(f"Points per game: {points[player] // games}")\nexcept KeyError:\n'
                 '    print("No such player")\nexcept ZeroDivisionError:\n    print("No games played yet")',
        wrong=[("один общий except — на любую ошибку отвечает, что игрока нет",
                'try:\n    print(f"Points per game: {points[player] // games}")\nexcept:\n    print("No such player")'),
               ("перепутал ответы: на KeyError говорит про игры, на ZeroDivisionError — про игрока",
                'try:\n    print(f"Points per game: {points[player] // games}")\nexcept KeyError:\n'
                '    print("No games played yet")\nexcept ZeroDivisionError:\n    print("No such player")')],
        constructs=["try"],
        must_use=[("re:except\\s+KeyError", "Неизвестного игрока поймай отдельным блоком `except KeyError:`."),
                  ("re:except\\s+ZeroDivisionError",
                   "Ноль сыгранных игр поймай своим блоком `except ZeroDivisionError:` — тогда на каждую ошибку "
                   "программа ответит по-своему.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-exc-rt-quarter-marks", title="Оценки за четверть",
        given=["quarters", "number"],
        variants=[{"quarters": "[[5, 4, 4, 5, 3], [4, 4, 5], []]", "number": "1"},
                  {"quarters": "[[5, 4, 4, 5, 3], [4, 4, 5], []]", "number": "3"},
                  {"quarters": "[[5, 4, 4, 5, 3], [4, 4, 5], []]", "number": "5"}],
        hidden=[{"number": "2"}, {"number": "4"}, {"quarters": "[[3]]", "number": "1"},
                {"quarters": "[[2, 3], [5, 5, 5, 4]]", "number": "2"}, {"quarters": "[[2, 3]]", "number": "2"}],
        intro="В электронном дневнике оценки ученика хранятся по четвертям: `quarters` — список, в котором для каждой "
              "четверти лежит свой список оценок. Если четверть только началась, её список пустой, а будущих четвертей "
              "в `quarters` ещё нет. Родители хотят посмотреть четверть с номером `number` — нумерация с 1.",
        steps=["В блоке `try` возьми список оценок четверти: индекс на 1 меньше номера. Выведи строку вида "
               "`Quarter 1: 5 marks` — номер четверти и сколько в ней оценок.",
               "Следующей строкой там же выведи средний балл, округлённый до одного знака через `round(..., 1)`, "
               "в виде `Average: 4.2`. Сумму оценок даёт `sum()`, их количество — `len()`.",
               "Если такой четверти в списке нет, возникнет `IndexError` — перехвати её своим блоком `except` и выведи "
               "строку вида `There is no quarter 5`.",
               "Если оценок в четверти пока нет, деление на их количество вызовет `ZeroDivisionError` — перехвати её "
               "отдельным блоком и выведи `No marks yet`."],
        hint="Слишком большой индекс списка вызывает `IndexError`, а деление на 0 — `ZeroDivisionError`. "
             "Для пустой четверти первая строка с числом оценок успеет напечататься до ошибки — так и задумано.",
        solution=QUARTERS,
        wrong=[("не вычитает 1 из номера — показывает следующую четверть",
                QUARTERS.replace("quarters[number - 1]", "quarters[number]")),
               ("перепутал ответы для IndexError и ZeroDivisionError",
                QUARTERS.replace('    print(f"There is no quarter {number}")\n', '    print("No marks yet!")\n')
                        .replace('    print("No marks yet")\n', '    print(f"There is no quarter {number}")\n')
                        .replace('    print("No marks yet!")\n', '    print("No marks yet")\n'))],
        constructs=["try"],
        must_use=[("re:except\\s+IndexError", "Несуществующую четверть поймай отдельным блоком `except IndexError:`."),
                  ("re:except\\s+ZeroDivisionError",
                   "Четверть без оценок поймай своим блоком `except ZeroDivisionError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-exc-rt-currency-exchange", title="Обмен валюты",
        given=["rates", "requests"],
        variants=[{"rates": RATES, "requests": '[("USD", 900), ("GBP", 500), ("CNY", 300), ("EUR", "1000"), ("TRY", 100)]'},
                  {"rates": RATES, "requests": '[("EUR", 2500), ("USD", "90"), ("JPY", 1000)]'},
                  {"rates": RATES, "requests": '[("CNY", 700), ("TRY", 31), ("USD", 89), ("EUR", 100)]'}],
        hidden=[{"requests": '[("USD", 180)]'},
                {"requests": '[("CHF", 100), ("CNY", 1), ("EUR", "5")]'},
                {"requests": '[("TRY", "300"), ("TRY", 300), ("KZT", 10), ("EUR", 999)]'},
                {"rates": '{"USD": 0}', "requests": '[("USD", 100), ("EUR", 100)]'}],
        intro="Обменник продаёт валюту за рубли. Курсы лежат в словаре `rates`: ключ — код валюты, значение — сколько "
              "рублей стоит одна её единица; если курс 0, эту валюту сегодня не продают. Покупатели по очереди присылают "
              "заявки в список `requests`: кортеж из кода валюты и суммы в рублях. Иногда сумма по ошибке приходит "
              "строкой.",
        steps=["Пройди по `requests`, распаковывая каждую заявку в две переменные. Для каждой в блоке `try` посчитай, "
               "сколько целых единиц валюты выйдет: рубли, делённые нацело на курс из `rates`. Выведи строку вида "
               "`900 rub -> 10 USD` и увеличь счётчик удачных обменов.",
               "Если такой валюты нет в словаре (`KeyError`), выведи строку вида `GBP: unknown currency`.",
               "Если курс равен 0 (`ZeroDivisionError`), выведи строку вида `CNY: not sold today`.",
               "Если сумма пришла строкой, деление строки на число вызовет `TypeError` — выведи строку вида "
               "`EUR: amount must be a number`.",
               "После цикла выведи строку вида `Successful: 2`."],
        hint="Каждую заявку обрабатывай в своём `try` внутри цикла, а для каждой ошибки поставь отдельный `except`. "
             "Счётчик увеличивай после деления и печати: если деление сломалось, эта строка не выполнится.",
        solution=EXCHANGE,
        wrong=[("try вокруг всего цикла — после первой ошибки остальные заявки не обрабатываются",
                'bought = 0\ntry:\n    for currency, rubles in requests:\n        units = rubles // rates[currency]\n'
                '        print(f"{rubles} rub -> {units} {currency}")\n        bought += 1\nexcept KeyError:\n'
                '    print(f"{currency}: unknown currency")\nexcept ZeroDivisionError:\n'
                '    print(f"{currency}: not sold today")\nexcept TypeError:\n'
                '    print(f"{currency}: amount must be a number")\nprint(f"Successful: {bought}")'),
               ("увеличивает счётчик до деления — неудачные заявки тоже считаются",
                EXCHANGE.replace("    try:\n        units = rubles // rates[currency]\n",
                                 "    try:\n        bought += 1\n        units = rubles // rates[currency]\n")
                        .replace('        print(f"{rubles} rub -> {units} {currency}")\n        bought += 1\n',
                                 '        print(f"{rubles} rub -> {units} {currency}")\n')),
               ("перепутал ответы для KeyError и ZeroDivisionError",
                EXCHANGE.replace("    except KeyError:\n", "    except ZeroDivisionError!\n")
                        .replace("    except ZeroDivisionError:\n", "    except KeyError:\n")
                        .replace("    except ZeroDivisionError!\n", "    except ZeroDivisionError:\n"))],
        constructs=["try", "for"],
        must_use=[("re:except\\s+KeyError", "Неизвестную валюту поймай отдельным блоком `except KeyError:`."),
                  ("re:except\\s+ZeroDivisionError", "Нулевой курс поймай отдельным блоком `except ZeroDivisionError:`."),
                  ("re:except\\s+TypeError", "Сумму-строку поймай отдельным блоком `except TypeError:`.")],
    ),
]
