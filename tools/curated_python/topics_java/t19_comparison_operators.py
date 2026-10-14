"""COMPARISON_OPERATORS — «Операторы сравнения» (Java). Taught before: println, variables, assignment, arithmetic,
primitive types, String, / and %, += -= ++, if/else. The point: ==, !=, <, >, <=, >= give a boolean, and the right
operator decides the boundary cases. Not yet: && || !, switch, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "COMPARISON_OPERATORS"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-compare-headphones-price", title="Где дешевле наушники",
        given=[("int", "online"), ("int", "store")],
        variants=[{"online": "2990", "store": "3490"}, {"online": "4200", "store": "3900"}, {"online": "1500", "store": "1500"}],
        hidden=[{"online": "3999", "store": "4000"}, {"online": "4000", "store": "3999"}, {"online": "2500", "store": "2500"},
                {"online": "100", "store": "9000"}],
        intro="Одни и те же наушники продаются в интернет-магазине и в обычном магазине у дома. "
              "Цена в интернете записана в поле `online`, цена в магазине — в поле `store` (в рублях).",
        steps=["Выведи `Cheaper online: ` и результат сравнения: цена в интернете меньше цены в магазине.",
               "Выведи `Same price: ` и результат сравнения: цены одинаковые.",
               "Выведи `Different prices: ` и результат сравнения: цены не равны.",
               "Результат каждого сравнения Java напечатает сама — словом `true` или `false`."],
        hint="Сравнение само является значением `true` или `false`, его можно сразу прибавить к строке. "
             "Только возьми его в скобки: `\"Bigger: \" + (a > b)`. Без скобок Java попробует сравнить строку с числом.",
        solution='System.out.println("Cheaper online: " + (online < store));\n'
                 'System.out.println("Same price: " + (online == store));\n'
                 'System.out.println("Different prices: " + (online != store));',
        wrong=[("<= вместо <: при равных ценах пишет, что в интернете дешевле",
                'System.out.println("Cheaper online: " + (online <= store));\n'
                'System.out.println("Same price: " + (online == store));\n'
                'System.out.println("Different prices: " + (online != store));'),
               ("сравнение в обратную сторону: > вместо <",
                'System.out.println("Cheaper online: " + (online > store));\n'
                'System.out.println("Same price: " + (online == store));\n'
                'System.out.println("Different prices: " + (online != store));')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-compare-match-result", title="Итог футбольного матча",
        given=[("int", "home"), ("int", "away")],
        variants=[{"home": "2", "away": "1"}, {"home": "0", "away": "3"}, {"home": "1", "away": "1"}],
        hidden=[{"home": "0", "away": "0"}, {"home": "5", "away": "4"}, {"home": "4", "away": "5"}, {"home": "3", "away": "3"},
                {"home": "1", "away": "0"}],
        intro="Табло на стадионе после матча показывает счёт и итог игры. Сколько голов забили хозяева поля, записано "
              "в поле `home`, сколько забили гости — в поле `away`.",
        steps=["Выведи счёт: слово `Score`, пробел, голы хозяев, двоеточие и голы гостей, например `Score 3:0`.",
               "Следующей строкой: если хозяева забили больше, чем гости, выведи `Home team wins`.",
               "Если гости забили больше, чем хозяева, выведи `Away team wins`.",
               "Если голов поровну, выведи `Draw`."],
        hint="Исходов три, поэтому удобно написать `if`, затем `else if` и в конце `else`. Проверки идут сверху вниз, "
             "и выполняется только первая подходящая ветка — ничья останется для последнего `else`.",
        solution='System.out.println("Score " + home + ":" + away);\nif (home > away) {\n    System.out.println("Home team wins");\n'
                 '} else if (home < away) {\n    System.out.println("Away team wins");\n} else {\n    System.out.println("Draw");\n}',
        wrong=[(">= вместо >: при ничьей объявляет победу хозяев",
                'System.out.println("Score " + home + ":" + away);\nif (home >= away) {\n    System.out.println("Home team wins");\n'
                '} else if (home < away) {\n    System.out.println("Away team wins");\n} else {\n    System.out.println("Draw");\n}'),
               ("только две ветки: ничья считается победой гостей",
                'System.out.println("Score " + home + ":" + away);\nif (home > away) {\n    System.out.println("Home team wins");\n'
                '} else {\n    System.out.println("Away team wins");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-compare-speed-camera", title="Камера контроля скорости",
        given=[("int", "speed"), ("int", "limit")],
        variants=[{"speed": "85", "limit": "60"}, {"speed": "100", "limit": "90"}, {"speed": "150", "limit": "90"}],
        hidden=[{"speed": "60", "limit": "60"}, {"speed": "40", "limit": "60"}, {"speed": "80", "limit": "60"},
                {"speed": "81", "limit": "60"}, {"speed": "100", "limit": "60"}, {"speed": "101", "limit": "60"}],
        intro="Камера на дороге измерила скорость машины — поле `speed`, в км/ч. На этом участке можно ехать не быстрее, "
              "чем указано в поле `limit`. Размер штрафа зависит от того, насколько превышена скорость.",
        steps=["Если `speed` не больше `limit`, выведи одну строку `Speed is OK`.",
               "Иначе посчитай превышение (`speed` минус `limit`) и выведи его строкой `Over by: … km/h`.",
               "Затем следующей строкой выведи штраф: если превышение не больше 20 км/ч — `No fine`, "
               "если от 21 до 40 км/ч включительно — `Fine: 500 rub`, если больше 40 км/ч — `Fine: 1000 rub`"],
        hint="Внутри ветки `else` можно написать ещё один `if`. Проверь границы: превышение ровно на 20 км/ч ещё без штрафа, "
             "а ровно на 40 км/ч — штраф 500 руб. Подумай, где нужен `<`, а где `<=`.",
        solution='if (speed <= limit) {\n    System.out.println("Speed is OK");\n} else {\n    int excess = speed - limit;\n'
                 '    System.out.println("Over by: " + excess + " km/h");\n    if (excess <= 20) {\n        System.out.println("No fine");\n'
                 '    } else if (excess <= 40) {\n        System.out.println("Fine: 500 rub");\n    } else {\n'
                 '        System.out.println("Fine: 1000 rub");\n    }\n}',
        wrong=[("строгие сравнения: превышение ровно на 20 или 40 км/ч попадает в следующий штраф",
                'if (speed <= limit) {\n    System.out.println("Speed is OK");\n} else {\n    int excess = speed - limit;\n'
                '    System.out.println("Over by: " + excess + " km/h");\n    if (excess < 20) {\n        System.out.println("No fine");\n'
                '    } else if (excess < 40) {\n        System.out.println("Fine: 500 rub");\n    } else {\n'
                '        System.out.println("Fine: 1000 rub");\n    }\n}'),
               ("< вместо <= в первой проверке: ровно разрешённая скорость считается превышением",
                'if (speed < limit) {\n    System.out.println("Speed is OK");\n} else {\n    int excess = speed - limit;\n'
                '    System.out.println("Over by: " + excess + " km/h");\n    if (excess <= 20) {\n        System.out.println("No fine");\n'
                '    } else if (excess <= 40) {\n        System.out.println("Fine: 500 rub");\n    } else {\n'
                '        System.out.println("Fine: 1000 rub");\n    }\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-compare-exam-mark", title="Проходной балл",
        given=[("int", "points"), ("int", "needed")],
        variants=[{"points": "72", "needed": "60"}, {"points": "45", "needed": "50"}, {"points": "65", "needed": "65"}],
        hidden=[{"points": "59", "needed": "60"}, {"points": "60", "needed": "60"}, {"points": "61", "needed": "60"},
                {"points": "0", "needed": "40"}, {"points": "100", "needed": "70"}],
        intro="После экзамена ученик смотрит, сколько баллов он набрал, — поле `points`. "
              "Чтобы сдать экзамен, нужно набрать не меньше проходного балла — поле `needed`.",
        steps=["Выведи `Passed: ` и результат сравнения: `points` больше или равно `needed`.",
               "Выведи `Exactly the mark: ` и результат сравнения: `points` равно `needed`.",
               "Выведи `Above the mark: ` и результат сравнения: `points` больше `needed`.",
               "Результат каждого сравнения Java напечатает сама — словом `true` или `false`."],
        hint="Сравнение можно сразу прибавить к строке, если взять его в скобки: `\"Bigger: \" + (a > b)`. "
             "Обрати внимание: ровно проходной балл — это уже сдал, но ещё не «выше».",
        solution='System.out.println("Passed: " + (points >= needed));\n'
                 'System.out.println("Exactly the mark: " + (points == needed));\n'
                 'System.out.println("Above the mark: " + (points > needed));',
        wrong=[("> вместо >=: ровно проходной балл считается несданным экзаменом",
                'System.out.println("Passed: " + (points > needed));\n'
                'System.out.println("Exactly the mark: " + (points == needed));\n'
                'System.out.println("Above the mark: " + (points > needed));'),
               (">= вместо > в последней строке",
                'System.out.println("Passed: " + (points >= needed));\n'
                'System.out.println("Exactly the mark: " + (points == needed));\n'
                'System.out.println("Above the mark: " + (points >= needed));')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-compare-guess-number", title="Угадай число",
        given=[("int", "secret"), ("int", "guess")],
        variants=[{"secret": "42", "guess": "30"}, {"secret": "17", "guess": "25"}, {"secret": "8", "guess": "8"}],
        hidden=[{"secret": "50", "guess": "49"}, {"secret": "50", "guess": "51"}, {"secret": "50", "guess": "50"},
                {"secret": "1", "guess": "100"}, {"secret": "99", "guess": "0"}],
        intro="Аня загадала число — поле `secret`, а Борис пытается его угадать и называет своё число — поле `guess`. "
              "Аня отвечает подсказкой.",
        steps=["Выведи `Guess: ` и число Бориса, например `Guess: 30`.",
               "Следующей строкой: если `guess` меньше `secret`, выведи `Too low`.",
               "Если `guess` больше `secret`, выведи `Too high`.",
               "Если числа равны, выведи `You got it`."],
        hint="Исходов три — подойдут `if`, `else if` и `else`. Выполняется только первая подходящая ветка, "
             "поэтому для угаданного числа останется последний `else`.",
        solution='System.out.println("Guess: " + guess);\nif (guess < secret) {\n    System.out.println("Too low");\n'
                 '} else if (guess > secret) {\n    System.out.println("Too high");\n} else {\n    System.out.println("You got it");\n}',
        wrong=[("<= вместо <: угаданное число называет слишком маленьким",
                'System.out.println("Guess: " + guess);\nif (guess <= secret) {\n    System.out.println("Too low");\n'
                '} else if (guess > secret) {\n    System.out.println("Too high");\n} else {\n    System.out.println("You got it");\n}'),
               ("сравнение в обратную сторону: подсказки перепутаны",
                'System.out.println("Guess: " + guess);\nif (guess > secret) {\n    System.out.println("Too low");\n'
                '} else if (guess < secret) {\n    System.out.println("Too high");\n} else {\n    System.out.println("You got it");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-compare-race-winner", title="Победитель забега",
        given=[("int", "anya"), ("int", "boris"), ("int", "vera")],
        variants=[{"anya": "64", "boris": "58", "vera": "61"}, {"anya": "55", "boris": "57", "vera": "55"},
                  {"anya": "70", "boris": "66", "vera": "62"}],
        hidden=[{"anya": "60", "boris": "60", "vera": "65"}, {"anya": "70", "boris": "60", "vera": "60"},
                {"anya": "50", "boris": "50", "vera": "50"}, {"anya": "49", "boris": "50", "vera": "51"},
                {"anya": "80", "boris": "75", "vera": "74"}, {"anya": "62", "boris": "61", "vera": "63"}],
        intro="Аня, Борис и Вера пробежали стометровку. Их время в секундах записано в полях `anya`, `boris` и `vera`. "
              "Побеждает тот, у кого время меньше.",
        steps=["Найди победителя. Если у нескольких бегунов одинаковое лучшее время, побеждает тот, кто стоит раньше "
               "в списке: сначала Аня, потом Борис, потом Вера.",
               "Выведи `Winner: ` и имя победителя латиницей: `Anya`, `Boris` или `Vera`.",
               "Следующей строкой выведи `Best time: … s` — время победителя."],
        hint="Сначала сравни Аню с Борисом, а потом того, кто быстрее, — с Верой: внутри ветки можно написать ещё один `if`. "
             "Подумай, где нужен `<=`, чтобы при равном времени выигрывал тот, кто раньше в списке.",
        solution='String winner;\nint best;\nif (anya <= boris) {\n    if (anya <= vera) {\n        winner = "Anya";\n        best = anya;\n'
                 '    } else {\n        winner = "Vera";\n        best = vera;\n    }\n} else {\n    if (boris <= vera) {\n'
                 '        winner = "Boris";\n        best = boris;\n    } else {\n        winner = "Vera";\n        best = vera;\n    }\n}\n'
                 'System.out.println("Winner: " + winner);\nSystem.out.println("Best time: " + best + " s");',
        wrong=[("строгие сравнения: при равном времени побеждает тот, кто позже в списке",
                'String winner;\nint best;\nif (anya < boris) {\n    if (anya < vera) {\n        winner = "Anya";\n        best = anya;\n'
                '    } else {\n        winner = "Vera";\n        best = vera;\n    }\n} else {\n    if (boris < vera) {\n'
                '        winner = "Boris";\n        best = boris;\n    } else {\n        winner = "Vera";\n        best = vera;\n    }\n}\n'
                'System.out.println("Winner: " + winner);\nSystem.out.println("Best time: " + best + " s");'),
               ("если Борис быстрее Ани, забывает сравнить его с Верой",
                'String winner;\nint best;\nif (anya <= boris) {\n    if (anya <= vera) {\n        winner = "Anya";\n        best = anya;\n'
                '    } else {\n        winner = "Vera";\n        best = vera;\n    }\n} else {\n    winner = "Boris";\n    best = boris;\n}\n'
                'System.out.println("Winner: " + winner);\nSystem.out.println("Best time: " + best + " s");')],
        constructs=["if"],
    ),
]
