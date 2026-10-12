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
               "После цикла выведи две строки: `Дней копила: …` и `В копилке: … руб.`"],
        hint="Если создать `total` внутри цикла, она будет начинаться с нуля на каждом шаге. Сумма копится в переменной, "
             "созданной до цикла, а печатается после него — когда все дни уже добавлены.",
        solution='int total = 0;\nfor (int day = 1; day <= days; day++) {\n    total += day;\n}\n'
                 'System.out.println("Дней копила: " + days);\nSystem.out.println("В копилке: " + total + " руб.");',
        wrong=[("= вместо +=: в копилке оказывается только последний взнос",
                'int total = 0;\nfor (int day = 1; day <= days; day++) {\n    total = day;\n}\n'
                'System.out.println("Дней копила: " + days);\nSystem.out.println("В копилке: " + total + " руб.");'),
               ("< вместо <=: последний день не учтён",
                'int total = 0;\nfor (int day = 1; day < days; day++) {\n    total += day;\n}\n'
                'System.out.println("Дней копила: " + days);\nSystem.out.println("В копилке: " + total + " руб.");')],
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
               "После цикла выведи две строки: `Бесплатных чашек: …` и `К оплате: … руб.`"],
        hint="Счётчик — это тоже накопление: он растёт на 1 только тогда, когда выполнено условие. "
             "А в сумму попадают только те чашки, за которые платят.",
        solution='int free = 0;\nint total = 0;\nfor (int i = 1; i <= cups; i++) {\n    if (i % 5 == 0) {\n        free++;\n'
                 '    } else {\n        total += price;\n    }\n}\nSystem.out.println("Бесплатных чашек: " + free);\n'
                 'System.out.println("К оплате: " + total + " руб.");',
        wrong=[("цикл с нуля: чашка с номером 0 считается бесплатной, а последняя не учтена",
                'int free = 0;\nint total = 0;\nfor (int i = 0; i < cups; i++) {\n    if (i % 5 == 0) {\n        free++;\n'
                '    } else {\n        total += price;\n    }\n}\nSystem.out.println("Бесплатных чашек: " + free);\n'
                'System.out.println("К оплате: " + total + " руб.");'),
               ("цена добавляется за каждую чашку, в том числе за бесплатные",
                'int free = 0;\nint total = 0;\nfor (int i = 1; i <= cups; i++) {\n    if (i % 5 == 0) {\n        free++;\n'
                '    }\n    total += price;\n}\nSystem.out.println("Бесплатных чашек: " + free);\n'
                'System.out.println("К оплате: " + total + " руб.");')],
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
               "Каждый год после начисления выводи строку `Год …: … руб.` — номер года и сумму на вкладе.",
               "После цикла выведи `Прибыль: … руб.` — на сколько `balance` стал больше начальной суммы `money`."],
        hint="Проценты каждый год считаются от текущего `balance`, а не от начальной суммы `money`: "
             "поэтому с каждым годом прибавка становится чуть больше.",
        solution='int balance = money;\nfor (int year = 1; year <= years; year++) {\n    balance += balance * percent / 100;\n'
                 '    System.out.println("Год " + year + ": " + balance + " руб.");\n}\n'
                 'System.out.println("Прибыль: " + (balance - money) + " руб.");',
        wrong=[("проценты каждый год от начальной суммы, а не от текущей",
                'int balance = money;\nfor (int year = 1; year <= years; year++) {\n    balance += money * percent / 100;\n'
                '    System.out.println("Год " + year + ": " + balance + " руб.");\n}\n'
                'System.out.println("Прибыль: " + (balance - money) + " руб.");'),
               ("percent / 100 нацело даёт 0: вклад не растёт",
                'int balance = money;\nfor (int year = 1; year <= years; year++) {\n    balance += balance * (percent / 100);\n'
                '    System.out.println("Год " + year + ": " + balance + " руб.");\n}\n'
                'System.out.println("Прибыль: " + (balance - money) + " руб.");')],
        constructs=["for", "augmented_assignment"],
    ),
]
