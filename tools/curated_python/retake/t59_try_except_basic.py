"""PY_TRY_EXCEPT_BASIC — «Обработка ошибок try / except». Taught before: everything up to comprehensions (conditions,
loops, lists, dicts, string methods, functions, classes, f-strings; int("abc") raises ValueError). Here: put risky code
into try and react to an error in except instead of crashing. Not yet: several except blocks on purpose, finally, raise."""
from build import OutputTask

SKILL = "PY_TRY_EXCEPT_BASIC"

CART = """\
total = 0
for i in range(len(prices)):
    try:
        count = int(amounts[i])
        cost = prices[i] * count
        total += cost
        print(f"Line {i + 1}: {count} x {prices[i]} = {cost} rub")
    except ValueError:
        print(f"Line {i + 1}: skipped")
print(f"Total: {total} rub")
"""

BILLS = """\
done = 0
for bill in bills:
    parts = bill.split("/")
    try:
        total = int(parts[0])
        people = int(parts[1])
    except ValueError:
        print(f"{bill}: bad numbers")
        continue
    try:
        print(f"{bill}: {total // people} rub each")
        done += 1
    except ZeroDivisionError:
        print(f"{bill}: nobody to pay")
print(f"Bills split: {done}")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-try-rt-book-page", title="Перейти на страницу",
        given=["page_text", "total"],
        variants=[{"page_text": '"42"', "total": "300"}, {"page_text": '"forty"', "total": "120"},
                  {"page_text": '"7"', "total": "96"}],
        hidden=[{"page_text": '"1"', "total": "10"}, {"page_text": '"12a"', "total": "50"},
                {"page_text": '""', "total": "200"}, {"page_text": '"250"', "total": "250"}],
        intro="В приложении для чтения можно ввести номер страницы, на которую нужно перейти. Программа получает его "
              "строкой `page_text`, а всего в книге `total` страниц. Если ввести не число, `int()` вызывает ошибку "
              "`ValueError`, и программа останавливается. Нужно, чтобы вместо этого она подсказала, что вводить.",
        steps=["В блоке `try` преврати `page_text` в целое число и выведи строку вида `Opening page 42`.",
               "Там же, в `try`, следующей строкой выведи строку вида `Pages left: 258` — сколько страниц в книге "
               "после этой: `total` минус номер страницы.",
               "Добавь блок `except ValueError:` и выведи в нём `Page must be a number`."],
        hint="Обе строки с номером страницы должны стоять внутри `try`: если `int()` не справился, Python сразу перейдёт "
             "в `except`, и ни одна из них не выполнится. Тогда при ошибке программа выведет только подсказку.",
        solution='try:\n    page = int(page_text)\n    print(f"Opening page {page}")\n    print(f"Pages left: {total - page}")\n'
                 'except ValueError:\n    print("Page must be a number")',
        wrong=[("при ошибке ставит страницу 0 и печатает дальше — выводятся лишние строки",
                'try:\n    page = int(page_text)\nexcept ValueError:\n    print("Page must be a number")\n    page = 0\n'
                'print(f"Opening page {page}")\nprint(f"Pages left: {total - page}")'),
               ("забывает вычесть номер страницы — печатает, сколько страниц всего",
                'try:\n    page = int(page_text)\n    print(f"Opening page {page}")\n    print(f"Pages left: {total}")\n'
                'except ValueError:\n    print("Page must be a number")')],
        constructs=["try"],
        must_use=[("re:except\\s+ValueError",
                   "Перехвати именно ошибку превращения строки в число: напиши `except ValueError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-try-rt-cart-amounts", title="Количество в корзине",
        given=["prices", "amounts"],
        variants=[{"prices": "[50, 120, 35]", "amounts": '["3", "two", "4"]'},
                  {"prices": "[200, 80]", "amounts": '["1", "5"]'},
                  {"prices": "[15, 60, 90, 45]", "amounts": '["x", "2", "", "10"]'}],
        hidden=[{"prices": "[100]", "amounts": '["abc"]'},
                {"prices": "[10, 20, 30]", "amounts": '["0", "1", "2"]'},
                {"prices": "[70, 70, 70, 70]", "amounts": '["1", "?", "3", "many"]'}],
        intro="В корзине интернет-магазина у каждой строки есть цена товара — список `prices` — и количество, "
              "которое покупатель ввёл в поле, — список строк `amounts`. Цена и количество одной строки стоят "
              "на одинаковых местах. Иногда в поле количества оказывается не число.",
        steps=["Пройди по строкам корзины циклом `for i in range(len(prices)):` — номер строки для покупателя "
               "на 1 больше индекса.",
               "В блоке `try` преврати `amounts[i]` в целое число, посчитай стоимость строки (цена, умноженная "
               "на количество), прибавь её к общей сумме и выведи строку вида `Line 1: 3 x 50 = 150 rub`.",
               "Если количество не число, перехвати `ValueError` и выведи строку вида `Line 2: skipped`.",
               "После цикла выведи строку вида `Total: 290 rub` — сумму по всем строкам, которые удалось посчитать."],
        hint="Поставь `try` внутрь цикла: тогда ошибка в одной строке корзины прервёт только её шаг, а цикл перейдёт "
             "к следующей. Общую сумму заведи до цикла и прибавляй к ней только внутри `try`, после `int()`.",
        solution=CART,
        wrong=[("try вокруг всего цикла — после первой ошибки остальные строки не считаются",
                'total = 0\ntry:\n    for i in range(len(prices)):\n        count = int(amounts[i])\n'
                '        cost = prices[i] * count\n        total += cost\n'
                '        print(f"Line {i + 1}: {count} x {prices[i]} = {cost} rub")\n'
                'except ValueError:\n    print(f"Line {i + 1}: skipped")\nprint(f"Total: {total} rub")'),
               ("нумерует строки с нуля",
                CART.replace("Line {i + 1}", "Line {i}"))],
        constructs=["try", "for"],
        must_use=[("re:except\\s+ValueError",
                   "Перехвати именно ошибку превращения строки в число: напиши `except ValueError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-try-rt-split-bill", title="Разделить счёт",
        given=["bills"],
        variants=[{"bills": '["1200/3", "900/0", "abc/2", "1000/4"]'},
                  {"bills": '["500/2", "750/3"]'},
                  {"bills": '["2000/x", "0/5", "3100/0", "999/1"]'}],
        hidden=[{"bills": '["10/0"]'},
                {"bills": '["a/b", "7/q"]'},
                {"bills": '["100/3", "250/0", "1/1", "seven/7", "640/8"]'},
                {"bills": '["50/5"]'}],
        intro="В ресторане официант вводит в планшет, как разделить счёт: строка `\"1200/3\"` значит «счёт 1200 руб. "
              "на троих». Все такие строки лежат в списке `bills`. Иногда в строку попадает не число, а иногда "
              "по ошибке вводят 0 человек.",
        steps=["Заведи счётчик разделённых счетов, равный 0. Для каждой строки из `bills` разрежь её по `/` методом "
               "`.split(\"/\")`: первая часть — сумма, вторая — число людей.",
               "В первом блоке `try` преврати обе части в целые числа. Если возникла `ValueError`, выведи строку вида "
               "`abc/2: bad numbers` и переходи к следующему счёту командой `continue`.",
               "Во втором блоке `try` раздели сумму на число людей нацело, выведи строку вида `1200/3: 400 rub each` "
               "и увеличь счётчик на 1. Если людей 0, перехвати `ZeroDivisionError` и выведи строку вида "
               "`900/0: nobody to pay`.",
               "После цикла выведи строку вида `Bills split: 2`."],
        hint="Счётчик увеличивай после деления, внутри второго `try`: если деление сломалось, строки после него "
             "не выполнятся, и неудачный счёт не посчитается. `continue` сразу начинает следующий шаг цикла.",
        solution=BILLS,
        wrong=[("увеличивает счётчик до деления — счета на 0 человек тоже считаются разделёнными",
                BILLS.replace('        print(f"{bill}: {total // people} rub each")\n        done += 1\n',
                              '        done += 1\n        print(f"{bill}: {total // people} rub each")\n')),
               ("делит через / — сумма с каждого получается дробной",
                BILLS.replace("{total // people}", "{total / people}")),
               ("путает части строки — делит число людей на сумму",
                BILLS.replace("        total = int(parts[0])\n        people = int(parts[1])\n",
                              "        total = int(parts[1])\n        people = int(parts[0])\n"))],
        constructs=["try", "for"],
        must_use=[("re:except\\s+ValueError", "Строку, в которой не числа, отсей, перехватив `except ValueError:`."),
                  ("re:except\\s+ZeroDivisionError",
                   "Деление на 0 человек обработай вторым блоком `try` с `except ZeroDivisionError:`.")],
    ),
]
