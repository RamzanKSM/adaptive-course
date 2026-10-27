"""PY_FUNCTION_BASIC — «Функции». Taught before: everything up to string methods (conditions, loops, lists, iterating a
list, slices). Here: def, parameters, calling a function; the function prints. Not yet: return (next topic), default
values and keyword arguments."""
from build import OutputTask

SKILL = "PY_FUNCTION_BASIC"

NEED_DEF = ("FunctionDef", "Оформи решение в виде своей функции: создай её через def и вызови.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-fn-rt-order-ready", title="Заказ готов",
        given=["number"],
        variants=[{"number": "42"}, {"number": "7"}, {"number": "115"}],
        hidden=[{"number": "1"}, {"number": "300"}, {"number": "58"}],
        intro="В кафе на экране над стойкой показывают, чей заказ уже готов. "
              "Номер готового заказа записан в переменной `number`.",
        steps=["Создай функцию `call_order` с одним параметром `number`. Она печатает строку вида "
               "`Order #42 is ready` — только вместо 42 номер из параметра `number`. "
               "Между `#` и номером пробела нет.",
               "После функции вызови её один раз и передай ей переменную `number` из заготовки."],
        hint="Сама запись `def` ничего не печатает — код внутри функции выполнится, только когда ты её вызовешь. "
             "Чтобы между `#` и номером не появился пробел, удобно собрать строку через f-строку: `f\"Order #{{number}} ...\"`.",
        solution='def call_order(number):\n    print(f"Order #{number} is ready")\n\n\ncall_order(number)',
        wrong=[("забыл вызвать функцию — ничего не печатается",
                'def call_order(number):\n    print(f"Order #{number} is ready")'),
               ("печатает через запятую — после «#» появляется пробел",
                'def call_order(number):\n    print("Order #", number, "is ready")\n\n\ncall_order(number)')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fn-rt-name-frame", title="Рамка для надписи",
        given=["word"],
        variants=[{"word": '"Kazan"'}, {"word": '"Hello"'}, {"word": '"Python"'}],
        hidden=[{"word": '"Hi"'}, {"word": '"A"'}, {"word": '"Programming"'}],
        intro="Ты оформляешь надпись на табличке: слово `word` обводят рамкой из символов. "
              "Верхняя и нижняя линии рамки одинаковые, поэтому их удобно описать один раз в функции.",
        steps=["Создай функцию `border` с параметром `length`. Она печатает одну строку: знак `+`, "
               "затем `length` дефисов `-` и снова знак `+`. Например, `border(3)` печатает `+---+`",
               "Вызови `border`, передав ей длину слова `word`.",
               "Затем выведи слово между двумя вертикальными чертами без пробелов, например `|Kazan|`",
               "Снова вызови `border` с длиной слова — это нижняя линия рамки."],
        hint="Длину слова даёт `len(word)`, а строку можно повторить, умножив её на число: `\"-\" * 3` даёт `\"---\"`. "
             "Одну и ту же функцию можно вызывать сколько угодно раз.",
        solution='def border(length):\n    print("+" + "-" * length + "+")\n\n\n'
                 'border(len(word))\nprint("|" + word + "|")\nborder(len(word))',
        wrong=[("добавляет к длине два лишних дефиса — рамка шире слова",
                'def border(length):\n    print("+" + "-" * (length + 2) + "+")\n\n\n'
                'border(len(word))\nprint("|" + word + "|")\nborder(len(word))'),
               ("забыл нижнюю линию — вызывает функцию только один раз",
                'def border(length):\n    print("+" + "-" * length + "+")\n\n\n'
                'border(len(word))\nprint("|" + word + "|")')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fn-rt-conference-badges", title="Бейджи участников",
        given=["names"],
        variants=[{"names": '["anna", "Konstantin", "Boris"]'},
                  {"names": '["Svetlana", "oleg", "Marina", "Ilya"]'},
                  {"names": '["timur", "Valentina"]'}],
        hidden=[{"names": '["Sergei"]'},
                {"names": '["Yan", "Nikolai", "Albina", "Rostislav", "eva"]'},
                {"names": '["Kirill", "Lev", "Margarita"]'}],
        intro="На конференцию печатают бейджи. Имена участников записаны в список `names` — кто-то ввёл имя "
              "с большой буквы, кто-то с маленькой. На бейдже имя пишут заглавными буквами, а длинное имя сокращают, "
              "чтобы оно поместилось.",
        steps=["Создай функцию `print_badge` с двумя параметрами: `number` и `name`. Она печатает номер, точку, "
               "пробел и имя заглавными буквами. Если в имени больше 6 букв, печатаются только первые 6 букв "
               "и после них точка. Например, `print_badge(1, \"anna\")` печатает `1. ANNA`, "
               "а `print_badge(2, \"Konstantin\")` печатает `2. KONSTA.`",
               "Заведи переменную-счётчик со значением 1. Пройди циклом `for` по списку `names` и для каждого имени "
               "вызови функцию с текущим номером и именем, а потом увеличь счётчик на 1.",
               "Каждый бейдж — на своей строке, в том же порядке, что и в списке."],
        hint="Заглавные буквы даёт метод `upper()`, первые 6 символов — срез `name[:6]`, длину — `len(name)`. "
             "Имя ровно из 6 букв помещается целиком и сокращать его не нужно.",
        solution='def print_badge(number, name):\n    if len(name) > 6:\n'
                 '        print(f"{number}. {name[:6].upper()}.")\n    else:\n        print(f"{number}. {name.upper()}")\n\n\n'
                 'number = 1\nfor name in names:\n    print_badge(number, name)\n    number += 1',
        wrong=[("сокращает и имя ровно из 6 букв",
                'def print_badge(number, name):\n    if len(name) >= 6:\n'
                '        print(f"{number}. {name[:6].upper()}.")\n    else:\n        print(f"{number}. {name.upper()}")\n\n\n'
                'number = 1\nfor name in names:\n    print_badge(number, name)\n    number += 1'),
               ("счётчик начинается с 0 — нумерация сдвинута",
                'def print_badge(number, name):\n    if len(name) > 6:\n'
                '        print(f"{number}. {name[:6].upper()}.")\n    else:\n        print(f"{number}. {name.upper()}")\n\n\n'
                'number = 0\nfor name in names:\n    print_badge(number, name)\n    number += 1')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
]
