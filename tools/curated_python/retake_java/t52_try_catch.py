"""TRY_CATCH_BASIC — «Обработка исключений try / catch» (Java). Taught before: everything up to choosing a collection
(conditions, loops, arrays, methods, classes, collections). Here: put risky code into try and react in catch instead of
crashing — division by zero (ArithmeticException) and Integer.parseInt on a non-number (NumberFormatException).
Not yet: finally, throw, throws. Only our own texts are printed, never Java's exception messages."""
from java_tasks import JavaOutputTask

SKILL = "TRY_CATCH_BASIC"

TICKETS = ('try {\n    int n = Integer.parseInt(count);\n    System.out.println("To pay: " + n * price + " rub");\n'
           '} catch (NumberFormatException e) {\n    System.out.println("Type the number of tickets in digits");\n}')

COUPON = ('try {\n    int percent = Integer.parseInt(code.substring(4));\n    System.out.println("Discount: " + percent + "%");\n'
          '    System.out.println("To pay: " + (price - price * percent / 100) + " rub");\n'
          '} catch (NumberFormatException e) {\n    System.out.println("Unknown code, to pay: " + price + " rub");\n}')

FUEL = ('int valid = 0;\nfor (int i = 0; i < distances.length; i++) {\n    try {\n'
        '        int km = Integer.parseInt(distances[i]);\n        int per100 = liters[i] * 100 / km;\n'
        '        System.out.println("Trip " + (i + 1) + ": " + per100 + " l per 100 km");\n        valid++;\n'
        '    } catch (NumberFormatException e) {\n        System.out.println("Trip " + (i + 1) + ": bad distance");\n'
        '    } catch (ArithmeticException e) {\n        System.out.println("Trip " + (i + 1) + ": zero distance");\n    }\n}\n'
        'System.out.println("Valid trips: " + valid);')

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-try-rt-cinema-tickets", title="Сколько билетов в кино",
        given=[("String", "count"), ("int", "price")],
        variants=[{"count": '"3"', "price": "300"}, {"count": '"5"', "price": "250"}, {"count": '"2"', "price": "420"}],
        hidden=[{"count": '"two"', "price": "300"}, {"count": '"1"', "price": "500"}, {"count": '""', "price": "350"},
                {"count": '"4 tickets"', "price": "200"}, {"count": '"10"', "price": "150"}],
        intro="В кассе кинотеатра покупатель вводит на экране, сколько билетов ему нужно, и эта строка попадает в поле "
              "`count`. Билет стоит `price` руб. Но вместо цифр там может оказаться слово или пустая строка — "
              "тогда `Integer.parseInt` выбрасывает исключение `NumberFormatException`, и программа падает.",
        steps=["В блоке `try` преврати `count` в целое число методом `Integer.parseInt`.",
               "Там же выведи строку вида `To pay: 900 rub` — число билетов, умноженное на `price`.",
               "Добавь блок `catch (NumberFormatException e)` и выведи в нём `Type the number of tickets in digits`."],
        hint="Всё, что зависит от превращённого числа, держи внутри `try`: если `parseInt` выбросил исключение, "
             "остальные строки блока не выполняются, и программа сразу переходит в `catch`.",
        solution=TICKETS,
        wrong=[("печатает сумму после try/catch — при ошибке появляется лишняя строка с нулём",
                'int n = 0;\ntry {\n    n = Integer.parseInt(count);\n} catch (NumberFormatException e) {\n'
                '    System.out.println("Type the number of tickets in digits");\n}\n'
                'System.out.println("To pay: " + n * price + " rub");'),
               ("перехватывает ArithmeticException вместо NumberFormatException — на слове программа падает",
                TICKETS.replace("NumberFormatException", "ArithmeticException"))],
        constructs=["try"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-try-rt-promo-percent", title="Скидочный код",
        given=[("int", "price"), ("String", "code")],
        variants=[{"price": "1000", "code": '"SALE15"'},
                  {"price": "2400", "code": '"SALE25"'},
                  {"price": "780", "code": '"SALE10"'}],
        hidden=[{"price": "1000", "code": '"SALEX"'},
                {"price": "500", "code": '"SALE"'},
                {"price": "3000", "code": '"SALE50"'},
                {"price": "999", "code": '"SALE5o"'},
                {"price": "640", "code": '"SALE0"'}],
        intro="Интернет-магазин раздаёт скидочные коды: слово `SALE` и сразу за ним процент скидки, например `SALE15`. "
              "Покупатель ввёл код в поле `code`, а заказ стоит `price` руб. Иногда в коде опечатка, и после `SALE` "
              "стоит не число.",
        steps=["В блоке `try` возьми часть кода после первых четырёх букв — `code.substring(4)` — и преврати её в число "
               "методом `Integer.parseInt`. Это процент скидки.",
               "Там же выведи две строки: `Discount: 15%` — с процентом — и `To pay: 850 rub` — цену со скидкой, "
               "то есть `price - price * percent / 100`.",
               "Если после `SALE` не число, `parseInt` выбрасывает `NumberFormatException`. Перехвати его в `catch` и "
               "выведи строку вида `Unknown code, to pay: 1000 rub` — с полной ценой."],
        hint="Строку со скидкой печатай только после того, как `parseInt` успешно сработал: если код плохой, "
             "в выводе не должно быть ни одной строки про скидку. Пустая строка после `SALE` — тоже не число.",
        solution=COUPON,
        wrong=[("печатает строку со скидкой до parseInt — при плохом коде появляется лишняя строка",
                'try {\n    System.out.println("Discount: " + code.substring(4) + "%");\n'
                '    int percent = Integer.parseInt(code.substring(4));\n'
                '    System.out.println("To pay: " + (price - price * percent / 100) + " rub");\n'
                '} catch (NumberFormatException e) {\n    System.out.println("Unknown code, to pay: " + price + " rub");\n}'),
               ("превращает в число весь код вместе с SALE — любой код считается неизвестным",
                COUPON.replace("Integer.parseInt(code.substring(4))", "Integer.parseInt(code)"))],
        constructs=["try"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-try-rt-fuel-log", title="Журнал расхода бензина",
        given=[("String[]", "distances"), ("int[]", "liters")],
        variants=[{"distances": '{"400", "abc", "250"}', "liters": "{32, 20, 25}"},
                  {"distances": '{"0", "300", "120", "?"}', "liters": "{5, 21, 12, 9}"},
                  {"distances": '{"500", "200", "", "0", "100"}', "liters": "{40, 18, 10, 3, 7}"}],
        hidden=[{"distances": "{}", "liters": "{}"},
                {"distances": '{"100"}', "liters": "{6}"},
                {"distances": '{"x", "0", "y"}', "liters": "{1, 2, 3}"},
                {"distances": '{"50", "60", "70 km", "80"}', "liters": "{4, 6, 7, 8}"}],
        intro="Водитель записывает поездки: сколько километров проехал — строкой в массив `distances` (её вводят "
              "с телефона), сколько литров бензина потратил — числом в массив `liters` под тем же номером. Иногда "
              "расстояние записано с ошибкой, а иногда это 0 — машину только завели и заглушили.",
        steps=["Заведи счётчик удачных поездок и пройди по номерам `i` массива `distances` обычным циклом `for`.",
               "Для каждой поездки в блоке `try` преврати `distances[i]` в число через `Integer.parseInt`, посчитай "
               "расход на 100 км — `liters[i] * 100 / km` — и выведи строку вида `Trip 1: 8 l per 100 km` (поездки "
               "нумеруются с 1). Только после этого увеличь счётчик.",
               "Добавь `catch (NumberFormatException e)` с выводом строки вида `Trip 2: bad distance` и второй "
               "`catch (ArithmeticException e)` с выводом строки вида `Trip 2: zero distance`.",
               "После цикла выведи строку вида `Valid trips: 2`."],
        hint="`try` ставь внутри цикла, вокруг одной поездки: тогда ошибка в одной записи не мешает обработать "
             "следующие. Счётчик увеличивай последним — до него программа доходит, только если ошибок не было.",
        solution=FUEL,
        wrong=[("try вокруг всего цикла — после первой ошибочной поездки остальные не обрабатываются",
                'int valid = 0;\ntry {\n    for (int i = 0; i < distances.length; i++) {\n'
                '        int km = Integer.parseInt(distances[i]);\n        int per100 = liters[i] * 100 / km;\n'
                '        System.out.println("Trip " + (i + 1) + ": " + per100 + " l per 100 km");\n        valid++;\n    }\n'
                '} catch (NumberFormatException e) {\n    System.out.println("Trip ?: bad distance");\n'
                '} catch (ArithmeticException e) {\n    System.out.println("Trip ?: zero distance");\n}\n'
                'System.out.println("Valid trips: " + valid);'),
               ("увеличивает счётчик до вычислений — ошибочные поездки тоже засчитаны",
                FUEL.replace('    try {\n        int km', '    valid++;\n    try {\n        int km')
                    .replace(' l per 100 km");\n        valid++;\n', ' l per 100 km");\n')),
               ("перепутал сообщения в двух catch",
                FUEL.replace('": bad distance"', '": TMP"').replace('": zero distance"', '": bad distance"')
                    .replace('": TMP"', '": zero distance"'))],
        constructs=["try", "for"],
    ),
]
