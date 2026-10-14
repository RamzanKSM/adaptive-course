"""ACCUMULATOR_PATTERN — «Накопление результата в цикле» (Java). Taught before: println, variables, assignment,
arithmetic, primitive types, String, / and %, += -= ++, if/else, comparisons, && || !, switch, for. The point: a
variable created before the loop, changed with += on every step (or only when a condition holds) and printed after it.
Not yet: while, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "ACCUMULATOR_PATTERN"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-accum-piggy-bank", title="Копилка с растущими взносами",
        given=[("int", "days")],
        variants=[{"days": "5"}, {"days": "10"}, {"days": "7"}],
        hidden=[{"days": "1"}, {"days": "2"}, {"days": "30"}, {"days": "12"}],
        intro="Маша решила копить на подарок: в первый день положить в копилку 1 рубль, во второй — 2 рубля, в третий — "
              "3, и так каждый день на рубль больше. Копить она будет `days` дней.",
        steps=["До цикла заведи переменную `total` со значением 0.",
               "Циклом `for` перебери дни от 1 до `days` включительно и на каждом шаге добавляй к `total` номер дня "
               "с помощью `+=`.",
               "После цикла выведи две строки: `Days saved: …` и `In the piggy bank: … rub`"],
        hint="Если создать `total` внутри цикла, она будет начинаться с нуля на каждом шаге. Сумма копится в переменной, "
             "созданной до цикла, а печатается после него — когда все дни уже добавлены.",
        solution='int total = 0;\nfor (int day = 1; day <= days; day++) {\n    total += day;\n}\n'
                 'System.out.println("Days saved: " + days);\nSystem.out.println("In the piggy bank: " + total + " rub");',
        wrong=[("= вместо +=: в копилке оказывается только последний взнос",
                'int total = 0;\nfor (int day = 1; day <= days; day++) {\n    total = day;\n}\n'
                'System.out.println("Days saved: " + days);\nSystem.out.println("In the piggy bank: " + total + " rub");'),
               ("< вместо <=: последний день не учтён",
                'int total = 0;\nfor (int day = 1; day < days; day++) {\n    total += day;\n}\n'
                'System.out.println("Days saved: " + days);\nSystem.out.println("In the piggy bank: " + total + " rub");')],
        constructs=["for", "augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-accum-free-coffee", title="Каждый пятый кофе бесплатно",
        given=[("int", "cups"), ("int", "price")],
        variants=[{"cups": "12", "price": "180"}, {"cups": "4", "price": "150"}, {"cups": "15", "price": "200"}],
        hidden=[{"cups": "5", "price": "100"}, {"cups": "1", "price": "250"}, {"cups": "10", "price": "90"},
                {"cups": "9", "price": "120"}, {"cups": "20", "price": "50"}],
        intro="В кофейне акция: каждая пятая чашка кофе бесплатная — 5-я, 10-я, 15-я и так далее. "
              "Офис заказал `cups` чашек, обычная цена чашки — `price` руб.",
        steps=["До цикла заведи две переменные со значением 0: сколько чашек досталось бесплатно и сколько всего нужно заплатить.",
               "Перебери циклом `for` номера чашек от 1 до `cups` включительно.",
               "Если номер чашки делится на 5 без остатка, увеличь число бесплатных чашек на 1, "
               "иначе добавь к сумме `price`.",
               "После цикла выведи две строки: `Free cups: …` и `Total: … rub`"],
        hint="Счётчик — это тоже накопление: он растёт на 1 только тогда, когда выполнено условие. "
             "А в сумму попадают только те чашки, за которые платят.",
        solution='int free = 0;\nint total = 0;\nfor (int i = 1; i <= cups; i++) {\n    if (i % 5 == 0) {\n        free++;\n'
                 '    } else {\n        total += price;\n    }\n}\nSystem.out.println("Free cups: " + free);\n'
                 'System.out.println("Total: " + total + " rub");',
        wrong=[("цикл с нуля: чашка с номером 0 считается бесплатной, а последняя не учтена",
                'int free = 0;\nint total = 0;\nfor (int i = 0; i < cups; i++) {\n    if (i % 5 == 0) {\n        free++;\n'
                '    } else {\n        total += price;\n    }\n}\nSystem.out.println("Free cups: " + free);\n'
                'System.out.println("Total: " + total + " rub");'),
               ("цена добавляется за каждую чашку, в том числе за бесплатные",
                'int free = 0;\nint total = 0;\nfor (int i = 1; i <= cups; i++) {\n    if (i % 5 == 0) {\n        free++;\n'
                '    }\n    total += price;\n}\nSystem.out.println("Free cups: " + free);\n'
                'System.out.println("Total: " + total + " rub");')],
        constructs=["for", "if", "augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-accum-bank-deposit", title="Вклад с процентами на проценты",
        given=[("int", "money"), ("int", "percent"), ("int", "years")],
        variants=[{"money": "10000", "percent": "5", "years": "3"}, {"money": "2000", "percent": "10", "years": "4"},
                  {"money": "50000", "percent": "8", "years": "2"}],
        hidden=[{"money": "1000", "percent": "10", "years": "1"}, {"money": "100", "percent": "50", "years": "5"},
                {"money": "5000", "percent": "0", "years": "3"}, {"money": "999", "percent": "3", "years": "6"}],
        intro="Бабушка положила в банк `money` руб. на `years` лет под `percent`% годовых. Каждый год банк добавляет "
              "проценты к тому, что уже лежит на вкладе, — в том числе к процентам прошлых лет.",
        steps=["Заведи переменную `balance` и положи в неё начальную сумму `money`.",
               "Циклом `for` повтори расчёт для каждого года: посчитай проценты за год — `percent` процентов от "
               "`balance` нацело (сначала умножь на `percent`, потом раздели на 100) — и добавь их к `balance` через `+=`.",
               "Каждый год после начисления выводи строку `Year …: … rub` — номер года и сумму на вкладе.",
               "После цикла выведи `Profit: … rub` — на сколько `balance` стал больше начальной суммы `money`."],
        hint="Проценты каждый год считаются от текущего `balance`, а не от начальной суммы `money`: "
             "поэтому с каждым годом прибавка становится чуть больше.",
        solution='int balance = money;\nfor (int year = 1; year <= years; year++) {\n    balance += balance * percent / 100;\n'
                 '    System.out.println("Year " + year + ": " + balance + " rub");\n}\n'
                 'System.out.println("Profit: " + (balance - money) + " rub");',
        wrong=[("проценты каждый год от начальной суммы, а не от текущей",
                'int balance = money;\nfor (int year = 1; year <= years; year++) {\n    balance += money * percent / 100;\n'
                '    System.out.println("Year " + year + ": " + balance + " rub");\n}\n'
                'System.out.println("Profit: " + (balance - money) + " rub");'),
               ("percent / 100 нацело даёт 0: вклад не растёт",
                'int balance = money;\nfor (int year = 1; year <= years; year++) {\n    balance += balance * (percent / 100);\n'
                '    System.out.println("Year " + year + ": " + balance + " rub");\n}\n'
                'System.out.println("Profit: " + (balance - money) + " rub");')],
        constructs=["for", "augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-accum-bacteria", title="Бактерии в чашке",
        given=[("int", "hours")],
        variants=[{"hours": "5"}, {"hours": "8"}, {"hours": "3"}],
        hidden=[{"hours": "1"}, {"hours": "0"}, {"hours": "10"}, {"hours": "20"}],
        intro="В лаборатории в чашку посадили одну бактерию. Каждый час каждая бактерия делится надвое, то есть "
              "бактерий становится вдвое больше. Наблюдение длится `hours` часов.",
        steps=["До цикла заведи переменную `count` со значением 1.",
               "Циклом `for` повтори `hours` раз: на каждом шаге умножай `count` на 2 с помощью `*=`.",
               "После цикла выведи строку `After … hours: … bacteria` — число часов и число бактерий."],
        hint="`count *= 2` — то же, что `count = count * 2`. Начальное значение 1, а не 0: ноль сколько ни умножай, будет ноль.",
        solution='int count = 1;\nfor (int i = 1; i <= hours; i++) {\n    count *= 2;\n}\n'
                 'System.out.println("After " + hours + " hours: " + count + " bacteria");',
        wrong=[("+= вместо *=: бактерий каждый час прибавляется только по две",
                'int count = 1;\nfor (int i = 1; i <= hours; i++) {\n    count += 2;\n}\n'
                'System.out.println("After " + hours + " hours: " + count + " bacteria");'),
               ("цикл на один шаг длиннее: лишнее удвоение",
                'int count = 1;\nfor (int i = 0; i <= hours; i++) {\n    count *= 2;\n}\n'
                'System.out.println("After " + hours + " hours: " + count + " bacteria");')],
        constructs=["for", "augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-accum-lucky-tickets", title="Счастливые билеты",
        given=[("int", "first"), ("int", "last")],
        variants=[{"first": "1", "last": "30"}, {"first": "15", "last": "48"}, {"first": "100", "last": "160"}],
        hidden=[{"first": "7", "last": "7"}, {"first": "8", "last": "16"}, {"first": "17", "last": "27"},
                {"first": "1", "last": "6"}, {"first": "70", "last": "80"}],
        intro="На школьном празднике продали билеты с номерами от `first` до `last` включительно. Билет считается "
              "счастливым, если его номер заканчивается на цифру 7, — такие билеты получают приз.",
        steps=["До цикла заведи две переменные со значением 0: сколько билетов проверено и сколько из них счастливых.",
               "Перебери циклом `for` номера от `first` до `last` включительно. На каждом шаге увеличивай число "
               "проверенных билетов на 1, а если номер заканчивается на 7, увеличивай и число счастливых.",
               "После цикла выведи две строки: `Tickets checked: …` и `Lucky tickets: …`."],
        hint="Последнюю цифру числа даёт остаток от деления на 10: у номера 47 выражение `47 % 10` равно 7.",
        solution='int checked = 0;\nint lucky = 0;\nfor (int n = first; n <= last; n++) {\n    checked++;\n    if (n % 10 == 7) {\n'
                 '        lucky++;\n    }\n}\nSystem.out.println("Tickets checked: " + checked);\nSystem.out.println("Lucky tickets: " + lucky);',
        wrong=[("проверяет делимость на 7, а не последнюю цифру",
                'int checked = 0;\nint lucky = 0;\nfor (int n = first; n <= last; n++) {\n    checked++;\n    if (n % 7 == 0) {\n'
                '        lucky++;\n    }\n}\nSystem.out.println("Tickets checked: " + checked);\nSystem.out.println("Lucky tickets: " + lucky);'),
               ("< вместо <=: последний билет не проверен",
                'int checked = 0;\nint lucky = 0;\nfor (int n = first; n < last; n++) {\n    checked++;\n    if (n % 10 == 7) {\n'
                '        lucky++;\n    }\n}\nSystem.out.println("Tickets checked: " + checked);\nSystem.out.println("Lucky tickets: " + lucky);')],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-accum-pool-pass", title="Оплата бассейна",
        given=[("int", "days"), ("int", "trial"), ("int", "price")],
        variants=[{"days": "10", "trial": "3", "price": "200"}, {"days": "14", "trial": "2", "price": "300"},
                  {"days": "8", "trial": "5", "price": "160"}],
        hidden=[{"days": "7", "trial": "7", "price": "100"}, {"days": "9", "trial": "7", "price": "100"},
                {"days": "21", "trial": "0", "price": "200"}, {"days": "3", "trial": "1", "price": "400"},
                {"days": "15", "trial": "10", "price": "120"}],
        intro="Дима ходит в бассейн каждый день `days` дней подряд. Первые `trial` дней — пробные и бесплатные. "
              "Потом каждый день стоит `price` руб., но каждый седьмой день (7-й, 14-й, 21-й…) — за полцены.",
        steps=["До цикла заведи две переменные со значением 0: число оплаченных дней и сумму к оплате.",
               "Перебери циклом `for` номера дней от 1 до `days` включительно.",
               "Если номер дня не больше `trial`, день бесплатный — ничего не добавляй. Иначе увеличь число оплаченных "
               "дней на 1 и добавь к сумме `price / 2`, если номер дня делится на 7, или `price` — если не делится.",
               "После цикла выведи две строки: `Paid days: …` и `Total: … rub`."],
        hint="Порядок проверок важен: пробный день бесплатный, даже если это седьмой день. Поэтому сначала проверь "
             "пробный период, а проверку на 7 поставь внутрь ветки `else`.",
        solution='int paid = 0;\nint total = 0;\nfor (int day = 1; day <= days; day++) {\n    if (day > trial) {\n        paid++;\n'
                 '        if (day % 7 == 0) {\n            total += price / 2;\n        } else {\n            total += price;\n        }\n'
                 '    }\n}\nSystem.out.println("Paid days: " + paid);\nSystem.out.println("Total: " + total + " rub");',
        wrong=[("седьмой день проверяется раньше пробного: пробный 7-й день оплачивается за полцены",
                'int paid = 0;\nint total = 0;\nfor (int day = 1; day <= days; day++) {\n    if (day % 7 == 0) {\n        paid++;\n'
                '        total += price / 2;\n    } else if (day > trial) {\n        paid++;\n        total += price;\n'
                '    }\n}\nSystem.out.println("Paid days: " + paid);\nSystem.out.println("Total: " + total + " rub");'),
               ("пробные дни тоже считаются оплаченными",
                'int paid = 0;\nint total = 0;\nfor (int day = 1; day <= days; day++) {\n    paid++;\n    if (day > trial) {\n'
                '        if (day % 7 == 0) {\n            total += price / 2;\n        } else {\n            total += price;\n        }\n'
                '    }\n}\nSystem.out.println("Paid days: " + paid);\nSystem.out.println("Total: " + total + " rub");')],
        constructs=["for", "if", "augmented_assignment"],
    ),
]
