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
               "После цикла выведи две строки: `Товаров: …` — сколько цен в массиве — и `Итого: … руб.` — общую сумму."],
        hint="В цикле `for (int price : prices)` переменная `price` по очереди принимает каждое значение из массива. "
             "Сумму объяви до цикла: если объявить её внутри, она будет заново становиться нулём на каждом шаге.",
        solution='int sum = 0;\nfor (int price : prices) {\n    sum += price;\n}\n'
                 'System.out.println("Товаров: " + prices.length);\nSystem.out.println("Итого: " + sum + " руб.");',
        wrong=[("присваивает вместо прибавления: в сумме оказывается только последняя цена",
                'int sum = 0;\nfor (int price : prices) {\n    sum = price;\n}\n'
                'System.out.println("Товаров: " + prices.length);\nSystem.out.println("Итого: " + sum + " руб.");'),
               ("начинает цикл с индекса 1: первая цена не попадает в сумму",
                'int sum = 0;\nfor (int i = 1; i < prices.length; i++) {\n    sum += prices[i];\n}\n'
                'System.out.println("Товаров: " + prices.length);\nSystem.out.println("Итого: " + sum + " руб.");')],
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
               "выведи строку вида `День 2: 10450` — номер дня и число шагов. Дни нумеруются с 1.",
               "Заодно посчитай такие дни. После цикла выведи строку вида `Цель выполнена в 2 дн. из 5`, "
               "где второе число — сколько всего дней в массиве.",
               "Если цель не выполнена ни разу, программа выводит только последнюю строку."],
        hint="Номер дня нужен в выводе, поэтому здесь удобен цикл с индексом: `for (int i = 0; i < steps.length; i++)`. "
             "Номер дня на 1 больше индекса.",
        solution='int count = 0;\nfor (int i = 0; i < steps.length; i++) {\n    if (steps[i] >= goal) {\n'
                 '        System.out.println("День " + (i + 1) + ": " + steps[i]);\n        count++;\n    }\n}\n'
                 'System.out.println("Цель выполнена в " + count + " дн. из " + steps.length);',
        wrong=[("строгое сравнение: день ровно с goal шагов не засчитывается",
                'int count = 0;\nfor (int i = 0; i < steps.length; i++) {\n    if (steps[i] > goal) {\n'
                '        System.out.println("День " + (i + 1) + ": " + steps[i]);\n        count++;\n    }\n}\n'
                'System.out.println("Цель выполнена в " + count + " дн. из " + steps.length);'),
               ("нумерует дни с нуля",
                'int count = 0;\nfor (int i = 0; i < steps.length; i++) {\n    if (steps[i] >= goal) {\n'
                '        System.out.println("День " + i + ": " + steps[i]);\n        count++;\n    }\n}\n'
                'System.out.println("Цель выполнена в " + count + " дн. из " + steps.length);')],
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
               "После цикла выведи две строки: `Самый холодный день: …` с номером дня и `Температура: …` "
               "с температурой в этот день."],
        hint="Не начинай поиск с нуля: если все дни тёплые, ноль окажется ниже любой температуры из массива, "
             "и ответ будет неверным. Первый элемент массива — надёжное начальное значение.",
        solution='int min = temps[0];\nint day = 1;\nfor (int i = 1; i < temps.length; i++) {\n    if (temps[i] < min) {\n'
                 '        min = temps[i];\n        day = i + 1;\n    }\n}\n'
                 'System.out.println("Самый холодный день: " + day);\nSystem.out.println("Температура: " + min);',
        wrong=[("начинает поиск с нуля: если все дни тёплые, находит несуществующие 0 градусов",
                'int min = 0;\nint day = 1;\nfor (int i = 0; i < temps.length; i++) {\n    if (temps[i] < min) {\n'
                '        min = temps[i];\n        day = i + 1;\n    }\n}\n'
                'System.out.println("Самый холодный день: " + day);\nSystem.out.println("Температура: " + min);'),
               ("сравнивает через <=: из одинаково холодных дней выбирает последний",
                'int min = temps[0];\nint day = 1;\nfor (int i = 1; i < temps.length; i++) {\n    if (temps[i] <= min) {\n'
                '        min = temps[i];\n        day = i + 1;\n    }\n}\n'
                'System.out.println("Самый холодный день: " + day);\nSystem.out.println("Температура: " + min);')],
        constructs=["list", "for", "if"],
    ),
]
