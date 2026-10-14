"""PY_EXCEPTION_TYPES — «Типы исключений». Taught before: everything up to comprehensions, then try/except.
Here: tell errors apart — ValueError, ZeroDivisionError, KeyError, IndexError, TypeError — with a separate except
block for each and a different reaction. Not yet: finally, raise."""
from build import OutputTask

SKILL = "PY_EXCEPTION_TYPES"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-exc-calculator", title="Калькулятор деления",
        given=["a", "b"],
        variants=[{"a": '"12"', "b": '"4"'}, {"a": '"15"', "b": '"0"'}, {"a": '"hundred"', "b": '"5"'}],
        hidden=[{"a": '"9"', "b": '"x"'}, {"a": '"7"', "b": '"0"'}, {"a": '"20"', "b": '"3"'},
                {"a": '"-8"', "b": '"2"'}],
        intro="Калькулятор получает два числа из полей ввода — строками `a` и `b` — и делит первое на второе нацело. "
              "Пользователь может ошибиться двумя разными способами, и на каждую ошибку калькулятор должен "
              "отвечать по-своему.",
        steps=["В блоке `try` преврати `a` и `b` в целые числа, раздели первое на второе через `//` "
               "и выведи результат в виде `Result: 6`.",
               "Если в строке не число, `int()` вызовет `ValueError` — перехвати её отдельным блоком `except` "
               "и выведи `Enter numbers only`.",
               "Если второе число — ноль, возникнет `ZeroDivisionError` — перехвати её своим блоком `except` "
               "и выведи `Cannot divide by zero`."],
        hint="После одного `try` можно написать несколько блоков `except` подряд — каждый для своего типа ошибки. "
             "Python выполнит тот блок, тип которого совпал с возникшей ошибкой.",
        solution='try:\n    print(f"Result: {int(a) // int(b)}")\nexcept ValueError:\n'
                 '    print("Enter numbers only")\nexcept ZeroDivisionError:\n    print("Cannot divide by zero")',
        wrong=[("один общий except на все ошибки — при делении на ноль выводит сообщение про числа",
                'try:\n    print(f"Result: {int(a) // int(b)}")\nexcept:\n    print("Enter numbers only")'),
               ("считает, что при делении на ноль получается 0",
                'try:\n    print(f"Result: {int(a) // int(b)}")\nexcept ValueError:\n'
                '    print("Enter numbers only")\nexcept ZeroDivisionError:\n    print("Result: 0")')],
        constructs=["try"],
        must_use=[("re:except\\s+ValueError",
                   "Для строки, которая не похожа на число, нужен свой блок `except ValueError:`."),
                  ("re:except\\s+ZeroDivisionError",
                   "Для деления на ноль нужен отдельный блок `except ZeroDivisionError:` — "
                   "тогда на каждую ошибку программа ответит по-своему.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-exc-cafe-order", title="Заказ в кафе",
        given=["menu", "dish", "count"],
        variants=[{"menu": '{"coffee": 150, "tea": 90, "juice": 120, "pancakes": 210}', "dish": '"tea"', "count": '"2"'},
                  {"menu": '{"coffee": 150, "tea": 90, "juice": 120, "pancakes": 210}', "dish": '"pizza"', "count": '"1"'},
                  {"menu": '{"coffee": 150, "tea": 90, "juice": 120, "pancakes": 210}', "dish": '"coffee"', "count": '"two"'}],
        hidden=[{"dish": '"juice"', "count": '"3"'}, {"dish": '"soup"', "count": '"2"'},
                {"dish": '"pancakes"', "count": '"many"'}, {"dish": '"Tea"', "count": '"1"'},
                {"dish": '"pancakes"', "count": '"4"'}],
        intro="Официант принимает заказы через планшет. Цены хранятся в словаре `menu`, название блюда — в `dish`, "
              "а количество гость вводит сам, поэтому оно записано строкой: `count`. Ошибиться можно и в названии "
              "блюда, и в количестве — и подсказка гостю в этих случаях должна быть разной.",
        steps=["В блоке `try` возьми цену блюда из словаря: `menu[dish]`, преврати `count` в целое число "
               "и выведи стоимость заказа (цена × количество) в виде `To pay: 300 rub`",
               "Если такого блюда в меню нет, обращение `menu[dish]` вызовет `KeyError` — тогда выведи "
               "`This dish is not on the menu`.",
               "Если количество записано не цифрами, `int()` вызовет `ValueError` — тогда выведи "
               "`Write the amount in digits`."],
        hint="`KeyError` возникает, когда в словаре нет такого ключа, а `ValueError` — когда `int()` получает строку, "
             "не похожую на число. Для каждой ошибки напиши свой блок `except`.",
        solution='try:\n    print(f"To pay: {menu[dish] * int(count)} rub")\nexcept KeyError:\n'
                 '    print("This dish is not on the menu")\nexcept ValueError:\n    print("Write the amount in digits")',
        wrong=[("перепутал ошибки: на KeyError отвечает про количество, а на ValueError — про блюдо",
                'try:\n    print(f"To pay: {menu[dish] * int(count)} rub")\nexcept KeyError:\n'
                '    print("Write the amount in digits")\nexcept ValueError:\n    print("This dish is not on the menu")'),
               ("один общий except — на любую ошибку отвечает, что блюда нет",
                'try:\n    print(f"To pay: {menu[dish] * int(count)} rub")\nexcept:\n'
                '    print("This dish is not on the menu")')],
        constructs=["try"],
        must_use=[("re:except\\s+KeyError",
                   "Блюдо, которого нет в меню, поймай отдельным блоком `except KeyError:` — "
                   "именно эту ошибку вызывает обращение к словарю по несуществующему ключу."),
                  ("re:except\\s+ValueError",
                   "Неправильное количество поймай своим блоком `except ValueError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-exc-tournament-board", title="Табло турнира",
        given=["results", "queries"],
        variants=[{"results": '{"Anya": [12, 15, 9], "Boris": [7, 20], "Vika": [11]}',
                   "queries": '[("Anya", 2), ("Boris", 3), ("Gosha", 1), ("Vika", "1")]'},
                  {"results": '{"Anya": [12, 15, 9], "Boris": [7, 20], "Vika": [11]}',
                   "queries": '[("Vika", 1), ("Boris", "2"), ("Anya", 3), ("Denis", 2)]'},
                  {"results": '{"Anya": [12, 15, 9], "Boris": [7, 20], "Vika": [11]}',
                   "queries": '[("Boris", 2), ("Eva", 1), ("Anya", 4), ("Anya", 1)]'}],
        hidden=[{"queries": '[("Anya", 1), ("Anya", 2), ("Anya", 3)]'},
                {"queries": '[("Vika", 2), ("Boris", "1"), ("Zina", 1), ("Anya", 3)]'},
                {"queries": '[("Gosha", 3)]'},
                {"queries": '[("Vika", "one"), ("Boris", 2), ("Boris", 5)]'}],
        intro="На табло школьного турнира показывают очки игроков по раундам. Результаты лежат в словаре `results`: "
              "ключ — имя игрока, значение — список его очков за раунды по порядку. Зрители присылают запросы — "
              "пары «имя, номер раунда» в списке `queries`, и в запросах бывают ошибки трёх разных видов.",
        steps=["Перебери пары `name, number` из `queries`. Для каждой в блоке `try` возьми из `results` список очков "
               "игрока и достань из него очки за раунд `number`. Раунды нумеруются с 1, а индексы списка — с 0, "
               "поэтому индекс равен `number - 1`.",
               "Если всё получилось, выведи строку вида `Anya, round 2: 15`.",
               "Если игрока нет в словаре (`KeyError`), выведи имя и `no such player` — например, "
               "`Gosha: no such player`.",
               "Если такого раунда в списке нет (`IndexError`), выведи имя, номер раунда и `not played yet` — например, "
               "`Boris, round 3: not played yet`.",
               "Если номер раунда записан строкой, вычитание `number - 1` вызовет `TypeError` — выведи имя и "
               "`round must be a number`, например `Vika: round must be a number`."],
        hint="Каждый запрос обрабатывай в своём `try` внутри цикла — тогда ошибка в одном запросе не помешает ответить "
             "на следующие. А отдельные блоки `except` для `KeyError`, `IndexError` и `TypeError` позволят ответить "
             "на каждую ошибку по-своему.",
        solution='for name, number in queries:\n    try:\n        print(f"{name}, round {number}: {results[name][number - 1]}")\n'
                 '    except KeyError:\n        print(f"{name}: no such player")\n'
                 '    except IndexError:\n        print(f"{name}, round {number}: not played yet")\n'
                 '    except TypeError:\n        print(f"{name}: round must be a number")',
        wrong=[("try вокруг всего цикла — после первой ошибки остальные запросы не обрабатываются",
                'try:\n    for name, number in queries:\n        print(f"{name}, round {number}: {results[name][number - 1]}")\n'
                'except KeyError:\n    print(f"{name}: no such player")\n'
                'except IndexError:\n    print(f"{name}, round {number}: not played yet")\n'
                'except TypeError:\n    print(f"{name}: round must be a number")'),
               ("путает KeyError и IndexError — на неизвестного игрока отвечает про раунд, и наоборот",
                'for name, number in queries:\n    try:\n        print(f"{name}, round {number}: {results[name][number - 1]}")\n'
                '    except IndexError:\n        print(f"{name}: no such player")\n'
                '    except KeyError:\n        print(f"{name}, round {number}: not played yet")\n'
                '    except TypeError:\n        print(f"{name}: round must be a number")')],
        constructs=["try", "for"],
        must_use=[("re:except\\s+KeyError", "Неизвестного игрока поймай отдельным блоком `except KeyError:`."),
                  ("re:except\\s+IndexError", "Несыгранный раунд поймай отдельным блоком `except IndexError:` — "
                                              "эту ошибку вызывает слишком большой индекс списка."),
                  ("re:except\\s+TypeError", "Номер раунда, записанный строкой, поймай отдельным блоком "
                                             "`except TypeError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-exc-prize-pick", title="Выбери приз",
        given=["prizes", "choice"],
        variants=[{"prizes": '["ball", "kite", "puzzle"]', "choice": '"2"'},
                  {"prizes": '["book", "cap"]', "choice": '"5"'},
                  {"prizes": '["yo-yo", "robot", "paints", "dominoes"]', "choice": '"third"'}],
        hidden=[{"prizes": '["car"]', "choice": '"1"'},
                {"prizes": '["pen", "mug", "toy"]', "choice": '"4"'},
                {"prizes": '["bag", "game"]', "choice": '"x"'},
                {"prizes": '["cube", "doll", "ship", "lamp", "drum"]', "choice": '"5"'}],
        intro="Победитель конкурса выбирает приз, вводя его номер в поле на экране. Призы лежат в списке `prizes` "
              "и нумеруются с 1, а введённый номер приходит строкой `choice`. Ошибиться можно двумя способами, "
              "и подсказки для них разные.",
        steps=["В блоке `try` преврати `choice` в целое число, достань из списка приз с этим номером (индекс на 1 меньше "
               "номера) и выведи строку вида `Your prize: kite`.",
               "Если введено не число, `int()` вызовет `ValueError` — перехвати её своим блоком `except` и выведи "
               "`Type the number of the prize`.",
               "Если приза с таким номером нет, обращение к списку вызовет `IndexError` — перехвати её отдельным блоком "
               "`except` и выведи `There is no such prize`."],
        hint="Слишком большой индекс списка вызывает `IndexError`. Не забудь вычесть 1: приз номер 1 лежит под индексом 0.",
        solution='try:\n    print(f"Your prize: {prizes[int(choice) - 1]}")\nexcept ValueError:\n'
                 '    print("Type the number of the prize")\nexcept IndexError:\n    print("There is no such prize")',
        wrong=[("не вычитает 1 — выдаёт следующий приз, а последний считает несуществующим",
                'try:\n    print(f"Your prize: {prizes[int(choice)]}")\nexcept ValueError:\n'
                '    print("Type the number of the prize")\nexcept IndexError:\n    print("There is no such prize")'),
               ("один общий except — на любую ошибку просит ввести число",
                'try:\n    print(f"Your prize: {prizes[int(choice) - 1]}")\nexcept:\n'
                '    print("Type the number of the prize")')],
        constructs=["try"],
        must_use=[("re:except\\s+ValueError", "Для строки, которая не похожа на число, нужен свой блок `except ValueError:`."),
                  ("re:except\\s+IndexError", "Для несуществующего номера приза нужен отдельный блок `except IndexError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-exc-stock-add", title="Приёмка товара",
        given=["stock", "item", "amount"],
        variants=[{"stock": '{"pens": 40, "pencils": 25, "erasers": 10}', "item": '"pencils"', "amount": "15"},
                  {"stock": '{"pens": 40, "pencils": 25, "erasers": 10}', "item": '"markers"', "amount": "5"},
                  {"stock": '{"pens": 40, "pencils": 25, "erasers": 10}', "item": '"pens"', "amount": '"20"'}],
        hidden=[{"item": '"erasers"', "amount": "1"}, {"item": '"glue"', "amount": "3"},
                {"item": '"erasers"', "amount": '"ten"'}, {"item": '"Pens"', "amount": "2"},
                {"item": '"pens"', "amount": "60"}],
        intro="Кладовщик принимает товар. Остатки хранятся в словаре `stock`, принятый товар — в `item`, а количество — "
              "в `amount`. Количество иногда попадает в программу строкой в кавычках вместо числа, а товара может не быть "
              "в списке склада. На эти две ошибки нужно отвечать по-разному.",
        steps=["В блоке `try` прибавь `amount` к остатку товара: `stock[item] + amount` — запиши результат обратно "
               "в `stock[item]` и выведи строку вида `pens: 60 now`.",
               "Если товара нет на складе, `stock[item]` вызовет `KeyError` — тогда выведи `Unknown item, ask the manager`.",
               "Если количество — строка, сложение числа со строкой вызовет `TypeError` — тогда выведи "
               "`Amount must be a number`."],
        hint="`10 + \"5\"` вызывает `TypeError`: Python не складывает числа со строками. Для каждой ошибки напиши свой "
             "блок `except` — их можно ставить один за другим после одного `try`.",
        solution='try:\n    stock[item] = stock[item] + amount\n    print(f"{item}: {stock[item]} now")\nexcept KeyError:\n'
                 '    print("Unknown item, ask the manager")\nexcept TypeError:\n    print("Amount must be a number")',
        wrong=[("перепутал ошибки местами — на неизвестный товар отвечает про количество",
                'try:\n    stock[item] = stock[item] + amount\n    print(f"{item}: {stock[item]} now")\nexcept TypeError:\n'
                '    print("Unknown item, ask the manager")\nexcept KeyError:\n    print("Amount must be a number")'),
               ("печатает только принятое количество, а не новый остаток",
                'try:\n    stock[item] = stock[item] + amount\n    print(f"{item}: {amount} now")\nexcept KeyError:\n'
                '    print("Unknown item, ask the manager")\nexcept TypeError:\n    print("Amount must be a number")')],
        constructs=["try"],
        must_use=[("re:except\\s+KeyError", "Неизвестный товар поймай отдельным блоком `except KeyError:`."),
                  ("re:except\\s+TypeError", "Количество-строку поймай своим блоком `except TypeError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-exc-command-calc", title="Пакет команд деления",
        given=["commands"],
        variants=[{"commands": '["10 / 2", "7 / 0", "abc / 3", "5", "9 / 4"]'},
                  {"commands": '["100 / 10", "8 / x", "6 / 3", "12"]'},
                  {"commands": '["1 / 0", "0 / 1", "3 / three", "20 / 6"]'}],
        hidden=[{"commands": '["4 / 2"]'},
                {"commands": '["3 / 0", "5 / 0"]'},
                {"commands": '["seven / 7", "14 / 7", "21", "28 / 0", "35 / 5"]'},
                {"commands": '["2 / two"]'}],
        intro="Калькулятор получает пачку команд — строк вида `\"10 / 2\"` — в списке `commands` и делит числа нацело. "
              "Команды набирают люди, поэтому в них бывают ошибки трёх видов: не число, деление на ноль "
              "и команда без второго числа.",
        steps=["Пройди по `commands`. Для каждой команды в блоке `try` разрежь строку методом `.split(\" / \")`, "
               "преврати части с индексами 0 и 1 в целые числа и выведи строку вида `10 / 2 = 5`.",
               "Если часть — не число (`ValueError`), выведи команду в кавычках и `has a bad number`, например "
               "`\"abc / 3\" has a bad number`.",
               "Если делитель равен нулю (`ZeroDivisionError`), выведи строку вида `\"7 / 0\" divides by zero`.",
               "Если после разрезания второй части нет (`IndexError`), выведи строку вида `\"5\" is not complete`.",
               "После цикла выведи строку вида `Done: 2, errors: 3` — сколько команд выполнено и сколько с ошибками."],
        hint="Чтобы напечатать команду в двойных кавычках, возьми f-строку в одинарные кавычки: `f'\"{{command}}\" divides by zero'`. "
             "Счётчик ошибок можно увеличивать в каждом блоке `except`.",
        solution='done = 0\nerrors = 0\nfor command in commands:\n    try:\n        parts = command.split(" / ")\n'
                 '        print(f"{command} = {int(parts[0]) // int(parts[1])}")\n        done += 1\n'
                 '    except ValueError:\n        print(f\'"{command}" has a bad number\')\n        errors += 1\n'
                 '    except ZeroDivisionError:\n        print(f\'"{command}" divides by zero\')\n        errors += 1\n'
                 '    except IndexError:\n        print(f\'"{command}" is not complete\')\n        errors += 1\n'
                 'print(f"Done: {done}, errors: {errors}")',
        wrong=[("увеличивает счётчик выполненных до деления — ошибки тоже считаются выполненными",
                'done = 0\nerrors = 0\nfor command in commands:\n    try:\n        done += 1\n        parts = command.split(" / ")\n'
                '        print(f"{command} = {int(parts[0]) // int(parts[1])}")\n'
                '    except ValueError:\n        print(f\'"{command}" has a bad number\')\n        errors += 1\n'
                '    except ZeroDivisionError:\n        print(f\'"{command}" divides by zero\')\n        errors += 1\n'
                '    except IndexError:\n        print(f\'"{command}" is not complete\')\n        errors += 1\n'
                'print(f"Done: {done}, errors: {errors}")'),
               ("путает ValueError и IndexError в ответах",
                'done = 0\nerrors = 0\nfor command in commands:\n    try:\n        parts = command.split(" / ")\n'
                '        print(f"{command} = {int(parts[0]) // int(parts[1])}")\n        done += 1\n'
                '    except IndexError:\n        print(f\'"{command}" has a bad number\')\n        errors += 1\n'
                '    except ZeroDivisionError:\n        print(f\'"{command}" divides by zero\')\n        errors += 1\n'
                '    except ValueError:\n        print(f\'"{command}" is not complete\')\n        errors += 1\n'
                'print(f"Done: {done}, errors: {errors}")')],
        constructs=["try", "for"],
        must_use=[("re:except\\s+ValueError", "Не число поймай отдельным блоком `except ValueError:`."),
                  ("re:except\\s+ZeroDivisionError", "Деление на ноль поймай отдельным блоком `except ZeroDivisionError:`."),
                  ("re:except\\s+IndexError", "Команду без второго числа поймай отдельным блоком `except IndexError:`.")],
    ),
]
