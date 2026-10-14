"""ARRAY_ITERATION — «Перебор массива» (Java): цикл for-each и цикл по индексам, сумма, подсчёт по условию, поиск
минимума. Taught before: everything up to arrays (indexes, .length, new int[n], filling in a loop), conditions,
loops, break. Not yet: own methods."""
from java_tasks import JavaOutputTask

SKILL = "ARRAY_ITERATION"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-it-receipt", title="Чек из магазина",
        given=[("int[]", "prices")],
        variants=[{"prices": "{120, 450, 89, 300}"}, {"prices": "{75, 75, 210, 64, 990}"}, {"prices": "{1500, 349, 20}"}],
        hidden=[{"prices": "{99}"}, {"prices": "{10, 20, 30, 40, 50, 60, 70}"}, {"prices": "{500, 1}"},
                {"prices": "{250, 0, 125}"}],
        intro="Ты купил в магазине несколько товаров, и их цены в рублях записаны в массиве `prices`. "
              "Нужно посчитать, сколько всего придётся заплатить.",
        steps=["Заведи переменную для суммы, сначала она равна 0.",
               "Пройди по массиву `prices` циклом `for (int price : prices)` и прибавь к сумме каждую цену.",
               "После цикла выведи две строки: `Items: …` — сколько цен в массиве — и `Total: … rub` — общую сумму."],
        hint="В цикле `for (int price : prices)` переменная `price` по очереди принимает каждое значение из массива. "
             "Сумму объяви до цикла: если объявить её внутри, она будет заново становиться нулём на каждом шаге.",
        solution='int sum = 0;\nfor (int price : prices) {\n    sum += price;\n}\n'
                 'System.out.println("Items: " + prices.length);\nSystem.out.println("Total: " + sum + " rub");',
        wrong=[("присваивает вместо прибавления: в сумме оказывается только последняя цена",
                'int sum = 0;\nfor (int price : prices) {\n    sum = price;\n}\n'
                'System.out.println("Items: " + prices.length);\nSystem.out.println("Total: " + sum + " rub");'),
               ("начинает цикл с индекса 1: первая цена не попадает в сумму",
                'int sum = 0;\nfor (int i = 1; i < prices.length; i++) {\n    sum += prices[i];\n}\n'
                'System.out.println("Items: " + prices.length);\nSystem.out.println("Total: " + sum + " rub");')],
        constructs=["list", "for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-it-step-goal", title="Шагомер",
        given=[("int[]", "steps"), ("int", "goal")],
        variants=[{"steps": "{8200, 10450, 12000, 6100, 9990}", "goal": "10000"},
                  {"steps": "{5000, 7300, 6999, 4200, 8800, 7000}", "goal": "7000"},
                  {"steps": "{12500, 3000, 15000, 9000}", "goal": "9000"}],
        hidden=[{"steps": "{10000, 9999, 10001}", "goal": "10000"},
                {"steps": "{3000, 2500}", "goal": "5000"},
                {"steps": "{6000, 6000, 6000, 6000, 6000, 6000, 6000}", "goal": "6000"},
                {"steps": "{11000}", "goal": "8000"}],
        intro="Шагомер записал, сколько шагов ты проходил каждый день: массив `steps`, по одному числу на день. "
              "Твоя цель — не меньше {goal} шагов в день (поле `goal`).",
        steps=["Пройди по массиву циклом с индексом. Для каждого дня, когда цель выполнена (шагов `goal` или больше), "
               "выведи строку вида `Day 2: 10450` — номер дня и число шагов. Дни нумеруются с 1.",
               "Заодно посчитай такие дни. После цикла выведи строку вида `Goal reached on 2 of 5 days`, "
               "где второе число — сколько всего дней в массиве.",
               "Если цель не выполнена ни разу, программа выводит только последнюю строку."],
        hint="Номер дня нужен в выводе, поэтому здесь удобен цикл с индексом: `for (int i = 0; i < steps.length; i++)`. "
             "Номер дня на 1 больше индекса.",
        solution='int count = 0;\nfor (int i = 0; i < steps.length; i++) {\n    if (steps[i] >= goal) {\n'
                 '        System.out.println("Day " + (i + 1) + ": " + steps[i]);\n        count++;\n    }\n}\n'
                 'System.out.println("Goal reached on " + count + " of " + steps.length + " days");',
        wrong=[("строгое сравнение: день ровно с goal шагов не засчитывается",
                'int count = 0;\nfor (int i = 0; i < steps.length; i++) {\n    if (steps[i] > goal) {\n'
                '        System.out.println("Day " + (i + 1) + ": " + steps[i]);\n        count++;\n    }\n}\n'
                'System.out.println("Goal reached on " + count + " of " + steps.length + " days");'),
               ("нумерует дни с нуля",
                'int count = 0;\nfor (int i = 0; i < steps.length; i++) {\n    if (steps[i] >= goal) {\n'
                '        System.out.println("Day " + i + ": " + steps[i]);\n        count++;\n    }\n}\n'
                'System.out.println("Goal reached on " + count + " of " + steps.length + " days");')],
        constructs=["list", "for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-it-coldest-day", title="Самый холодный день",
        given=[("int[]", "temps")],
        variants=[{"temps": "{-3, 2, -12, 0, -5}"}, {"temps": "{4, 1, 7, 1, 3, 9}"}, {"temps": "{-8, -15, -2, -15}"}],
        hidden=[{"temps": "{5, 8, 3}"}, {"temps": "{-20}"}, {"temps": "{2, 2, 2, 2}"},
                {"temps": "{0, -1, 6, -7, -7, 10, -2}"}],
        intro="Метеостанция каждый день в полдень записывала температуру воздуха — значения лежат в массиве `temps` "
              "по порядку дней. Нужно найти самый холодный день.",
        steps=["Заведи переменную для самой низкой температуры и сначала запиши в неё первый элемент массива, "
               "а в переменную для номера дня — 1.",
               "Пройди циклом по остальным дням. Если в какой-то день температура ниже найденной, запомни её и номер "
               "этого дня (дни нумеруются с 1). Если самых холодных дней несколько, нужен самый первый из них.",
               "После цикла выведи две строки: `Coldest day: …` с номером дня и `Temperature: …` "
               "с температурой в этот день."],
        hint="Не начинай поиск с нуля: если все дни тёплые, ноль окажется ниже любой температуры из массива, "
             "и ответ будет неверным. Первый элемент массива — надёжное начальное значение.",
        solution='int min = temps[0];\nint day = 1;\nfor (int i = 1; i < temps.length; i++) {\n    if (temps[i] < min) {\n'
                 '        min = temps[i];\n        day = i + 1;\n    }\n}\n'
                 'System.out.println("Coldest day: " + day);\nSystem.out.println("Temperature: " + min);',
        wrong=[("начинает поиск с нуля: если все дни тёплые, находит несуществующие 0 градусов",
                'int min = 0;\nint day = 1;\nfor (int i = 0; i < temps.length; i++) {\n    if (temps[i] < min) {\n'
                '        min = temps[i];\n        day = i + 1;\n    }\n}\n'
                'System.out.println("Coldest day: " + day);\nSystem.out.println("Temperature: " + min);'),
               ("сравнивает через <=: из одинаково холодных дней выбирает последний",
                'int min = temps[0];\nint day = 1;\nfor (int i = 1; i < temps.length; i++) {\n    if (temps[i] <= min) {\n'
                '        min = temps[i];\n        day = i + 1;\n    }\n}\n'
                'System.out.println("Coldest day: " + day);\nSystem.out.println("Temperature: " + min);')],
        constructs=["list", "for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-it-shopping-list", title="Список покупок",
        given=[("String[]", "items")],
        variants=[{"items": '{"milk", "bread", "apples", "cheese"}'}, {"items": '{"rice", "tea", "eggs"}'},
                  {"items": '{"pasta", "tomatoes", "onion", "butter", "honey"}'}],
        hidden=[{"items": '{"water"}'}, {"items": '{"salt", "sugar"}'},
                {"items": '{"carrots", "fish", "juice", "yogurt", "oats", "pears", "nuts"}'}],
        intro="Мама написала список покупок — он лежит в массиве `items`. Аня хочет переписать его в заметку на телефоне "
              "аккуратным столбиком.",
        steps=["Выведи первой строкой `Shopping list:`.",
               "Пройди по массиву `items` циклом `for (String item : items)` и для каждой покупки выведи строку: "
               "дефис, пробел и название, например `- milk`.",
               "После цикла выведи `Total items: …` — сколько покупок в списке."],
        hint="В цикле `for (String item : items)` переменная `item` по очереди становится каждым элементом массива — "
             "индексы здесь не нужны. Количество покупок даёт `items.length`.",
        solution='System.out.println("Shopping list:");\nfor (String item : items) {\n    System.out.println("- " + item);\n}\n'
                 'System.out.println("Total items: " + items.length);',
        wrong=[("цикл с индекса 1: первая покупка пропадает",
                'System.out.println("Shopping list:");\nfor (int i = 1; i < items.length; i++) {\n    System.out.println("- " + items[i]);\n}\n'
                'System.out.println("Total items: " + items.length);'),
               ("итог печатается внутри цикла после каждой покупки",
                'System.out.println("Shopping list:");\nfor (String item : items) {\n    System.out.println("- " + item);\n'
                '    System.out.println("Total items: " + items.length);\n}')],
        constructs=["list", "for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-it-rainy-days", title="Дождливые дни",
        given=[("int[]", "rain")],
        variants=[{"rain": "{0, 5, 12, 0, 0, 3, 8}"}, {"rain": "{2, 0, 0, 0, 14}"}, {"rain": "{7, 1, 0, 9, 4, 0}"}],
        hidden=[{"rain": "{0, 0, 0}"}, {"rain": "{1}"}, {"rain": "{10, 20, 30, 40}"}, {"rain": "{0, 1, 0, 1, 0, 25, 0, 2}"}],
        intro="Метеостанция записала, сколько миллиметров дождя выпало в каждый день, — массив `rain`. "
              "Если в какой-то день дождя не было, там стоит 0.",
        steps=["Заведи до цикла две переменные со значением 0: число дождливых дней и всего миллиметров дождя.",
               "Пройди по массиву `rain` циклом `for-each`. Если в этот день выпало больше 0 мм, увеличь число дождливых "
               "дней на 1 и прибавь эти миллиметры к общему количеству.",
               "После цикла выведи три строки: `Days: …` (сколько дней в массиве), `Rainy days: …` и `Total rain: … mm`."],
        hint="Счётчик растёт на 1 только когда выполнено условие, а сумма копит сами значения. День с 0 мм — сухой.",
        solution='int rainy = 0;\nint total = 0;\nfor (int mm : rain) {\n    if (mm > 0) {\n        rainy++;\n        total += mm;\n    }\n}\n'
                 'System.out.println("Days: " + rain.length);\nSystem.out.println("Rainy days: " + rainy);\n'
                 'System.out.println("Total rain: " + total + " mm");',
        wrong=[(">= 0 вместо > 0: сухие дни тоже считаются дождливыми",
                'int rainy = 0;\nint total = 0;\nfor (int mm : rain) {\n    if (mm >= 0) {\n        rainy++;\n        total += mm;\n    }\n}\n'
                'System.out.println("Days: " + rain.length);\nSystem.out.println("Rainy days: " + rainy);\n'
                'System.out.println("Total rain: " + total + " mm");'),
               ("прибавляет к сумме 1 вместо миллиметров",
                'int rainy = 0;\nint total = 0;\nfor (int mm : rain) {\n    if (mm > 0) {\n        rainy++;\n        total += 1;\n    }\n}\n'
                'System.out.println("Days: " + rain.length);\nSystem.out.println("Rainy days: " + rainy);\n'
                'System.out.println("Total rain: " + total + " mm");')],
        constructs=["list", "for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-it-practice-streak", title="Серия занятий на гитаре",
        given=[("int[]", "minutes"), ("int", "goal")],
        variants=[{"minutes": "{30, 45, 10, 35, 40, 50, 0, 30}", "goal": "30"},
                  {"minutes": "{20, 25, 5, 20, 30, 15}", "goal": "20"},
                  {"minutes": "{60, 0, 45, 45, 50, 10, 60}", "goal": "45"}],
        hidden=[{"minutes": "{10, 5, 0}", "goal": "15"}, {"minutes": "{30, 30, 30, 30}", "goal": "30"},
                {"minutes": "{29, 30, 31, 0, 30}", "goal": "30"}, {"minutes": "{40}", "goal": "40"},
                {"minutes": "{50, 50, 0, 50, 0, 50, 50, 50}", "goal": "50"}],
        intro="Дима учится играть на гитаре. Сколько минут он занимался в каждый день, записано в массив `minutes`. "
              "День считается удачным, если Дима занимался не меньше {goal} минут (поле `goal`).",
        steps=["Заведи до цикла три переменные со значением 0: длина текущей серии удачных дней подряд, самая длинная "
               "серия и всего удачных дней.",
               "Пройди по массиву циклом. В удачный день увеличь текущую серию и число удачных дней на 1, и если текущая "
               "серия стала длиннее самой длинной, запомни её. В неудачный день текущая серия обнуляется.",
               "После цикла выведи две строки: `Good days: …` и `Longest streak: … days`."],
        hint="Самую длинную серию обновляй сразу, как только текущая её обогнала, — а не в момент, когда серия "
             "прерывается: иначе серия, которая идёт до самого конца массива, не будет учтена.",
        solution='int current = 0;\nint best = 0;\nint good = 0;\nfor (int m : minutes) {\n    if (m >= goal) {\n        current++;\n'
                 '        good++;\n        if (current > best) {\n            best = current;\n        }\n    } else {\n'
                 '        current = 0;\n    }\n}\nSystem.out.println("Good days: " + good);\n'
                 'System.out.println("Longest streak: " + best + " days");',
        wrong=[("обновляет самую длинную серию только при её обрыве: серия в конце массива теряется",
                'int current = 0;\nint best = 0;\nint good = 0;\nfor (int m : minutes) {\n    if (m >= goal) {\n        current++;\n'
                '        good++;\n    } else {\n        if (current > best) {\n            best = current;\n        }\n'
                '        current = 0;\n    }\n}\nSystem.out.println("Good days: " + good);\n'
                'System.out.println("Longest streak: " + best + " days");'),
               ("не обнуляет серию в неудачный день: считает все удачные дни одной серией",
                'int current = 0;\nint best = 0;\nint good = 0;\nfor (int m : minutes) {\n    if (m >= goal) {\n        current++;\n'
                '        good++;\n        if (current > best) {\n            best = current;\n        }\n    }\n}\n'
                'System.out.println("Good days: " + good);\n'
                'System.out.println("Longest streak: " + best + " days");')],
        constructs=["list", "for", "if"],
    ),
]
