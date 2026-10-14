"""TRY_CATCH_BASIC — «Обработка исключений try / catch» (Java). Taught before: everything up to choosing a collection
(conditions, loops, arrays, methods, classes, collections). Here: put risky code into try and react in catch instead of
crashing — division by zero (ArithmeticException) and Integer.parseInt on a non-number (NumberFormatException).
Not yet: finally, throw, throws. Only our own texts are printed, never Java's exception messages."""
from java_tasks import JavaOutputTask

SKILL = "TRY_CATCH_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-try-prize-fund", title="Призовой фонд олимпиады",
        given=[("int", "prize"), ("int", "winners")],
        variants=[{"prize": "9000", "winners": "3"}, {"prize": "5000", "winners": "0"}, {"prize": "12000", "winners": "5"}],
        hidden=[{"prize": "7000", "winners": "0"}, {"prize": "1000", "winners": "4"}, {"prize": "10000", "winners": "1"},
                {"prize": "0", "winners": "2"}],
        intro="Призовой фонд школьной олимпиады (поле `prize`, в рублях) делят поровну между победителями, а их число "
              "записано в `winners`. Если победителей нет, деление на ноль выбрасывает исключение `ArithmeticException`, "
              "и программа аварийно останавливается. Сделай так, чтобы вместо этого она выводила понятное сообщение.",
        steps=["В блоке `try` раздели `prize` на `winners` оператором `/` и сразу выведи результат в виде "
               "`Each winner gets: 3000 rub`",
               "Добавь блок `catch (ArithmeticException e)` и выведи в нём `No winners, the prize moves to next year`."],
        hint="Если в `try` случится деление на ноль, Java сразу перейдёт в `catch`, а остальные строки блока `try` "
             "пропустит. Поэтому печатай результат прямо в `try`, сразу после деления.",
        solution='try {\n    System.out.println("Each winner gets: " + prize / winners + " rub");\n'
                 '} catch (ArithmeticException e) {\n    System.out.println("No winners, the prize moves to next year");\n}',
        wrong=[("печатает результат после try/catch — когда победителей нет, появляется лишняя строка с нулём",
                'int share = 0;\ntry {\n    share = prize / winners;\n} catch (ArithmeticException e) {\n'
                '    System.out.println("No winners, the prize moves to next year");\n}\n'
                'System.out.println("Each winner gets: " + share + " rub");'),
               ("пустой catch, а сообщение стоит после него — оно печатается и тогда, когда победители есть",
                'try {\n    System.out.println("Each winner gets: " + prize / winners + " rub");\n'
                '} catch (ArithmeticException e) {\n}\nSystem.out.println("No winners, the prize moves to next year");')],
        constructs=["try"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-try-workout-minutes", title="Длительность тренировки",
        given=[("String", "minutes")],
        variants=[{"minutes": '"135"'}, {"minutes": '""'}, {"minutes": '"90"'}],
        hidden=[{"minutes": '"2 hours"'}, {"minutes": '"60"'}, {"minutes": '"45"'}, {"minutes": '"forty"'},
                {"minutes": '"600"'}],
        intro="Фитнес-приложение показывает длительность тренировки в часах и минутах. Пользователь вводит её "
              "в минутах, и строка из поля ввода попадает в `minutes` — но там может оказаться что угодно, "
              "даже пустая строка.",
        steps=["В блоке `try` преврати `minutes` в целое число методом `Integer.parseInt`.",
               "Там же выведи время в виде `2 h 15 min`: часы — это минуты, делённые на 60 нацело, а оставшиеся "
               "минуты — остаток от деления на 60.",
               "Если в строке не число, `Integer.parseInt` выбрасывает `NumberFormatException`. Перехвати его "
               "в `catch` и выведи `Enter the time in minutes`."],
        hint="Не пытайся заранее угадать все неправильные строки через `if` — их слишком много. Просто попробуй "
             "превратить строку в число внутри `try`: любая неудача сама приведёт в `catch`.",
        solution='try {\n    int total = Integer.parseInt(minutes);\n'
                 '    System.out.println(total / 60 + " h " + total % 60 + " min");\n'
                 '} catch (NumberFormatException e) {\n    System.out.println("Enter the time in minutes");\n}',
        wrong=[("печатает время после try/catch — при ошибке появляется лишняя строка «0 h 0 min»",
                'int total = 0;\ntry {\n    total = Integer.parseInt(minutes);\n} catch (NumberFormatException e) {\n'
                '    System.out.println("Enter the time in minutes");\n}\n'
                'System.out.println(total / 60 + " h " + total % 60 + " min");'),
               ("проверяет через if только пустую строку вместо try/catch — на «2 hours» программа падает",
                'if (minutes.equals("")) {\n    System.out.println("Enter the time in minutes");\n} else {\n'
                '    int total = Integer.parseInt(minutes);\n'
                '    System.out.println(total / 60 + " h " + total % 60 + " min");\n}')],
        constructs=["try"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-try-receipt-total", title="Сумма по чеку",
        given=[("String[]", "prices")],
        variants=[{"prices": '{"120", "4O0", "85", "300"}'}, {"prices": '{"99", "15", "##", "250", ""}'},
                  {"prices": '{"error", "450", "70"}'}],
        hidden=[{"prices": '{"10", "20", "30"}'}, {"prices": '{"?"}'}, {"prices": "{}"},
                {"prices": '{"5", "x", "y", "15", "z"}'}, {"prices": '{"1000", "2O0"}'}],
        intro="Кассовый аппарат выгрузил цены покупок строками в массив `prices`. Из-за сбоя печати некоторые "
              "позиции испорчены — вместо цены в них посторонние символы. Нужно посчитать сумму по всем целым ценам "
              "и сообщить, какие позиции прочитать не удалось.",
        steps=["Заведи переменную для суммы и перебери массив `prices` по индексам обычным циклом `for`.",
               "Для каждой позиции в блоке `try` преврати строку в целое число через `Integer.parseInt` и прибавь его к сумме.",
               "Если превратить не удалось (`NumberFormatException`), выведи `Item 2: cannot read price` — с номером "
               "позиции в чеке (нумерация с 1) — и переходи к следующей.",
               "После цикла выведи `Total: 505 rub` — сумму всех прочитанных цен."],
        hint="Поставь `try` внутрь цикла, а не вокруг него: тогда ошибка в одной позиции прервёт только её обработку, "
             "а цикл пойдёт дальше. Номер позиции в чеке на 1 больше индекса в массиве.",
        solution='int total = 0;\nfor (int i = 0; i < prices.length; i++) {\n    try {\n'
                 '        total += Integer.parseInt(prices[i]);\n    } catch (NumberFormatException e) {\n'
                 '        System.out.println("Item " + (i + 1) + ": cannot read price");\n    }\n}\n'
                 'System.out.println("Total: " + total + " rub");',
        wrong=[("try вокруг всего цикла — после первой испорченной позиции остальные не считаются",
                'int total = 0;\nint i = 0;\ntry {\n    for (i = 0; i < prices.length; i++) {\n'
                '        total += Integer.parseInt(prices[i]);\n    }\n} catch (NumberFormatException e) {\n'
                '    System.out.println("Item " + (i + 1) + ": cannot read price");\n}\n'
                'System.out.println("Total: " + total + " rub");'),
               ("нумерует позиции с нуля — печатает индекс массива вместо номера в чеке",
                'int total = 0;\nfor (int i = 0; i < prices.length; i++) {\n    try {\n'
                '        total += Integer.parseInt(prices[i]);\n    } catch (NumberFormatException e) {\n'
                '        System.out.println("Item " + i + ": cannot read price");\n    }\n}\n'
                'System.out.println("Total: " + total + " rub");')],
        constructs=["try", "for"],
    ),
]
