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
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-try-candy-bag", title="Конфеты поровну",
        given=[("int", "candies"), ("int", "kids")],
        variants=[{"candies": "26", "kids": "4"}, {"candies": "15", "kids": "0"}, {"candies": "40", "kids": "6"}],
        hidden=[{"candies": "30", "kids": "0"}, {"candies": "12", "kids": "3"}, {"candies": "5", "kids": "7"},
                {"candies": "0", "kids": "2"}],
        intro="Мама принесла пакет с `candies` конфетами и делит их поровну между `kids` детьми, а то, что не "
              "делится, остаётся в пакете. Если детей нет, деление на ноль выбрасывает `ArithmeticException` — "
              "программа должна не падать, а сказать об этом.",
        steps=["В блоке `try` выведи строку вида `Each kid gets: 6 candies` — сколько конфет достанется каждому "
               "(целое деление `/`).",
               "Там же, следующей строкой, выведи строку вида `Left in the bag: 2` — остаток от деления `%`.",
               "Добавь блок `catch (ArithmeticException e)` и выведи в нём `No kids, the candies stay in the bag`."],
        hint="И `/`, и `%` на ноль выбрасывают одно и то же исключение. Если обе строки стоят внутри `try`, при нуле "
             "детей не напечатается ни одна из них — только сообщение из `catch`.",
        solution='try {\n    System.out.println("Each kid gets: " + candies / kids + " candies");\n'
                 '    System.out.println("Left in the bag: " + candies % kids);\n} catch (ArithmeticException e) {\n'
                 '    System.out.println("No kids, the candies stay in the bag");\n}',
        wrong=[("печатает остаток после try/catch — когда детей нет, появляется лишняя строка",
                'int left = candies;\ntry {\n    System.out.println("Each kid gets: " + candies / kids + " candies");\n'
                '    left = candies % kids;\n} catch (ArithmeticException e) {\n'
                '    System.out.println("No kids, the candies stay in the bag");\n}\n'
                'System.out.println("Left in the bag: " + left);'),
               ("перепутал / и % — каждому достаётся остаток, а в пакете остаётся частное",
                'try {\n    System.out.println("Each kid gets: " + candies % kids + " candies");\n'
                '    System.out.println("Left in the bag: " + candies / kids);\n} catch (ArithmeticException e) {\n'
                '    System.out.println("No kids, the candies stay in the bag");\n}')],
        constructs=["try"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-try-split-bill", title="Счёт в ресторане",
        given=[("int", "bill"), ("String", "people")],
        variants=[{"bill": "2400", "people": '"4"'}, {"bill": "1800", "people": '"0"'}, {"bill": "999", "people": '"three"'}],
        hidden=[{"bill": "500", "people": '"1"'}, {"bill": "3000", "people": '""'}, {"bill": "1000", "people": '"0"'},
                {"bill": "7700", "people": '"12"'}, {"bill": "600", "people": '"2 people"'}],
        intro="Компания делит счёт `bill` руб. поровну. Сколько человек платит, официант вводит в планшет, и эта строка "
              "попадает в `people`. Тут может пойти не так две вещи: в строке не число — или число 0.",
        steps=["В блоке `try` преврати `people` в целое число через `Integer.parseInt` и выведи строку вида "
               "`Each pays: 600 rub` — `bill`, делённый нацело на число людей.",
               "Добавь `catch (NumberFormatException e)` — строка не число — и выведи в нём "
               "`Enter the number of people in digits`.",
               "Добавь второй блок `catch (ArithmeticException e)` — людей 0 — и выведи в нём "
               "`Nobody to split the bill with`."],
        hint="К одному `try` можно приписать несколько `catch` подряд: Java выберет тот, чей тип совпадает с "
             "выброшенным исключением. Так каждая ошибка получает своё сообщение.",
        solution='try {\n    int n = Integer.parseInt(people);\n    System.out.println("Each pays: " + bill / n + " rub");\n'
                 '} catch (NumberFormatException e) {\n    System.out.println("Enter the number of people in digits");\n'
                 '} catch (ArithmeticException e) {\n    System.out.println("Nobody to split the bill with");\n}',
        wrong=[("перепутал сообщения в двух catch",
                'try {\n    int n = Integer.parseInt(people);\n    System.out.println("Each pays: " + bill / n + " rub");\n'
                '} catch (NumberFormatException e) {\n    System.out.println("Nobody to split the bill with");\n'
                '} catch (ArithmeticException e) {\n    System.out.println("Enter the number of people in digits");\n}'),
               ("один общий catch (Exception e) — на ноль людей печатает не ту причину",
                'try {\n    int n = Integer.parseInt(people);\n    System.out.println("Each pays: " + bill / n + " rub");\n'
                '} catch (Exception e) {\n    System.out.println("Enter the number of people in digits");\n}')],
        constructs=["try"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-try-sleep-survey", title="Опрос про сон",
        given=[("String[]", "answers")],
        variants=[{"answers": '{"8", "7", "nine", "6", "?"}'}, {"answers": '{"ten", "lots"}'},
                  {"answers": '{"9", "8", "10", "7"}'}],
        hidden=[{"answers": "{}"}, {"answers": '{"6"}'}, {"answers": '{"x", "5", "y", "9"}'},
                {"answers": '{"7", "7", "", "8", "8 h"}'}],
        intro="Школьный психолог провёл опрос: сколько часов ты спишь. Ответы пришли строками в массив `answers`, "
              "и кое-кто написал словами или поставил знак вопроса. Такие ответы нужно пропустить, а по остальным "
              "посчитать средний сон.",
        steps=["Заведи три счётчика: сумму часов, число принятых ответов и число пропущенных.",
               "Пройди по массиву `answers`. Для каждого ответа в блоке `try` преврати его в число через "
               "`Integer.parseInt`, прибавь к сумме и только потом увеличь число принятых. В "
               "`catch (NumberFormatException e)` увеличь число пропущенных.",
               "После цикла выведи строку вида `Skipped: 2`.",
               "Затем во втором блоке `try` выведи строку вида `Average: 7 h` — сумму, делённую нацело на число "
               "принятых ответов. Если принятых ответов нет, деление на ноль попадёт в `catch (ArithmeticException e)` — "
               "выведи там `No valid answers`."],
        hint="Если поставить увеличение счётчика перед `Integer.parseInt`, он увеличится и для плохого ответа: "
             "исключение случится уже после него. Всё, что должно сработать только для удачного числа, ставь после "
             "превращения.",
        solution='int total = 0;\nint count = 0;\nint skipped = 0;\nfor (String answer : answers) {\n    try {\n'
                 '        total += Integer.parseInt(answer);\n        count++;\n    } catch (NumberFormatException e) {\n'
                 '        skipped++;\n    }\n}\nSystem.out.println("Skipped: " + skipped);\ntry {\n'
                 '    System.out.println("Average: " + total / count + " h");\n} catch (ArithmeticException e) {\n'
                 '    System.out.println("No valid answers");\n}',
        wrong=[("увеличивает число принятых до parseInt — плохие ответы тоже попадают в среднее",
                'int total = 0;\nint count = 0;\nint skipped = 0;\nfor (String answer : answers) {\n    try {\n'
                '        count++;\n        total += Integer.parseInt(answer);\n    } catch (NumberFormatException e) {\n'
                '        skipped++;\n    }\n}\nSystem.out.println("Skipped: " + skipped);\ntry {\n'
                '    System.out.println("Average: " + total / count + " h");\n} catch (ArithmeticException e) {\n'
                '    System.out.println("No valid answers");\n}'),
               ("try вокруг всего цикла — после первого плохого ответа остальные не читаются",
                'int total = 0;\nint count = 0;\nint skipped = 0;\ntry {\n    for (String answer : answers) {\n'
                '        total += Integer.parseInt(answer);\n        count++;\n    }\n} catch (NumberFormatException e) {\n'
                '    skipped++;\n}\nSystem.out.println("Skipped: " + skipped);\ntry {\n'
                '    System.out.println("Average: " + total / count + " h");\n} catch (ArithmeticException e) {\n'
                '    System.out.println("No valid answers");\n}')],
        constructs=["try", "for"],
    ),
]
