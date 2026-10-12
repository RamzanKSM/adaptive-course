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
        steps=["Выведи `В интернете дешевле: ` и результат сравнения: цена в интернете меньше цены в магазине.",
               "Выведи `Цены равны: ` и результат сравнения: цены одинаковые.",
               "Выведи `Цены разные: ` и результат сравнения: цены не равны.",
               "Результат каждого сравнения Java напечатает сама — словом `true` или `false`."],
        hint="Сравнение само является значением `true` или `false`, его можно сразу прибавить к строке. "
             "Только возьми его в скобки: `\"Больше: \" + (a > b)`. Без скобок Java попробует сравнить строку с числом.",
        solution='System.out.println("В интернете дешевле: " + (online < store));\n'
                 'System.out.println("Цены равны: " + (online == store));\n'
                 'System.out.println("Цены разные: " + (online != store));',
        wrong=[("<= вместо <: при равных ценах пишет, что в интернете дешевле",
                'System.out.println("В интернете дешевле: " + (online <= store));\n'
                'System.out.println("Цены равны: " + (online == store));\n'
                'System.out.println("Цены разные: " + (online != store));'),
               ("сравнение в обратную сторону: > вместо <",
                'System.out.println("В интернете дешевле: " + (online > store));\n'
                'System.out.println("Цены равны: " + (online == store));\n'
                'System.out.println("Цены разные: " + (online != store));')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-compare-match-result", title="Итог футбольного матча",
        given=[("int", "home"), ("int", "away")],
        variants=[{"home": "2", "away": "1"}, {"home": "0", "away": "3"}, {"home": "1", "away": "1"}],
        hidden=[{"home": "0", "away": "0"}, {"home": "5", "away": "4"}, {"home": "4", "away": "5"}, {"home": "3", "away": "3"},
                {"home": "1", "away": "0"}],
        intro="Табло на стадионе после матча показывает счёт и итог игры. Сколько голов забили хозяева поля, записано "
              "в поле `home`, сколько забили гости — в поле `away`.",
        steps=["Выведи счёт: слово `Счёт`, пробел, голы хозяев, двоеточие и голы гостей, например `Счёт 3:0`.",
               "Следующей строкой: если хозяева забили больше, чем гости, выведи `Победа хозяев`.",
               "Если гости забили больше, чем хозяева, выведи `Победа гостей`.",
               "Если голов поровну, выведи `Ничья`."],
        hint="Исходов три, поэтому удобно написать `if`, затем `else if` и в конце `else`. Проверки идут сверху вниз, "
             "и выполняется только первая подходящая ветка — ничья останется для последнего `else`.",
        solution='System.out.println("Счёт " + home + ":" + away);\nif (home > away) {\n    System.out.println("Победа хозяев");\n'
                 '} else if (home < away) {\n    System.out.println("Победа гостей");\n} else {\n    System.out.println("Ничья");\n}',
        wrong=[(">= вместо >: при ничьей объявляет победу хозяев",
                'System.out.println("Счёт " + home + ":" + away);\nif (home >= away) {\n    System.out.println("Победа хозяев");\n'
                '} else if (home < away) {\n    System.out.println("Победа гостей");\n} else {\n    System.out.println("Ничья");\n}'),
               ("только две ветки: ничья считается победой гостей",
                'System.out.println("Счёт " + home + ":" + away);\nif (home > away) {\n    System.out.println("Победа хозяев");\n'
                '} else {\n    System.out.println("Победа гостей");\n}')],
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
        steps=["Если `speed` не больше `limit`, выведи одну строку `Скорость в норме`.",
               "Иначе посчитай превышение (`speed` минус `limit`) и выведи его строкой `Превышение: … км/ч`.",
               "Затем следующей строкой выведи штраф: если превышение не больше 20 км/ч — `Штрафа нет`, "
               "если от 21 до 40 км/ч включительно — `Штраф 500 руб.`, если больше 40 км/ч — `Штраф 1000 руб.`"],
        hint="Внутри ветки `else` можно написать ещё один `if`. Проверь границы: превышение ровно на 20 км/ч ещё без штрафа, "
             "а ровно на 40 км/ч — штраф 500 руб. Подумай, где нужен `<`, а где `<=`.",
        solution='if (speed <= limit) {\n    System.out.println("Скорость в норме");\n} else {\n    int excess = speed - limit;\n'
                 '    System.out.println("Превышение: " + excess + " км/ч");\n    if (excess <= 20) {\n        System.out.println("Штрафа нет");\n'
                 '    } else if (excess <= 40) {\n        System.out.println("Штраф 500 руб.");\n    } else {\n'
                 '        System.out.println("Штраф 1000 руб.");\n    }\n}',
        wrong=[("строгие сравнения: превышение ровно на 20 или 40 км/ч попадает в следующий штраф",
                'if (speed <= limit) {\n    System.out.println("Скорость в норме");\n} else {\n    int excess = speed - limit;\n'
                '    System.out.println("Превышение: " + excess + " км/ч");\n    if (excess < 20) {\n        System.out.println("Штрафа нет");\n'
                '    } else if (excess < 40) {\n        System.out.println("Штраф 500 руб.");\n    } else {\n'
                '        System.out.println("Штраф 1000 руб.");\n    }\n}'),
               ("< вместо <= в первой проверке: ровно разрешённая скорость считается превышением",
                'if (speed < limit) {\n    System.out.println("Скорость в норме");\n} else {\n    int excess = speed - limit;\n'
                '    System.out.println("Превышение: " + excess + " км/ч");\n    if (excess <= 20) {\n        System.out.println("Штрафа нет");\n'
                '    } else if (excess <= 40) {\n        System.out.println("Штраф 500 руб.");\n    } else {\n'
                '        System.out.println("Штраф 1000 руб.");\n    }\n}')],
        constructs=["if"],
    ),
]
