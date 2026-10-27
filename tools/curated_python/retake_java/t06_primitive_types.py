"""PRIMITIVE_TYPES — «Примитивные типы» (Java). Taught before: println, variables, assignment, arithmetic, execution order.
The point: int for whole numbers, double for fractions, long when int is too small, char for one symbol; an (int) cast
drops the fraction, and an int expression overflows before it is stored in a long. Not yet: String variables and their
methods, integer division and %, += -= ++, if/else, comparisons, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "PRIMITIVE_TYPES"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-types-rt-laminate-floor", title="Ламинат на пол",
        given=[("double", "length"), ("double", "width"), ("int", "price")],
        variants=[{"length": "3.5", "width": "2.5", "price": "900"}, {"length": "4.5", "width": "3.5", "price": "1200"},
                  {"length": "5.5", "width": "2.5", "price": "760"}],
        hidden=[{"length": "2.0", "width": "2.0", "price": "1000"}, {"length": "6.5", "width": "3.25", "price": "1000"},
                {"length": "2.75", "width": "1.5", "price": "800"}],
        intro="Семья кладёт ламинат в прямоугольной спальне. Длина и ширина пола в метрах записаны в полях `length` и "
              "`width` (дробные числа), цена квадратного метра ламината в рублях — в поле `price`.",
        steps=["Заведи переменную `area` типа `double` — площадь пола: `length` умножить на `width`.",
               "Заведи переменную `cost` типа `double` — стоимость ламината: `area` умножить на `price`.",
               "Выведи `Area: `, площадь и ` m2`, например `Area: 8.75 m2`.",
               "Следующей строкой выведи `Cost: `, стоимость и ` rub`, например `Cost: 7875.0 rub`."],
        hint="Площадь из дробных сторон тоже дробная, а `int` хранит только целые числа, — поэтому обе переменные `double`. "
             "Число типа `double` Java печатает с точкой: `7875.0`.",
        solution='double area = length * width;\n'
                 'double cost = area * price;\n'
                 'System.out.println("Area: " + area + " m2");\n'
                 'System.out.println("Cost: " + cost + " rub");',
        wrong=[("площадь сохранена в int через (int): дробная часть теряется",
                'int area = (int) (length * width);\n'
                'double cost = area * price;\n'
                'System.out.println("Area: " + area + " m2");\n'
                'System.out.println("Cost: " + cost + " rub");'),
               ("(int) применён к длине до умножения: 3.5 м превращаются в 3 м",
                'double area = (int) length * width;\n'
                'double cost = area * price;\n'
                'System.out.println("Area: " + area + " m2");\n'
                'System.out.println("Cost: " + cost + " rub");')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-types-rt-ribbon-bows", title="Банты из ленты",
        given=[("double", "ribbon"), ("double", "bow")],
        variants=[{"ribbon": "5.0", "bow": "0.75"}, {"ribbon": "7.25", "bow": "1.5"}, {"ribbon": "3.0", "bow": "1.25"}],
        hidden=[{"ribbon": "3.5", "bow": "0.5"}, {"ribbon": "2.0", "bow": "0.75"}, {"ribbon": "0.5", "bow": "0.75"},
                {"ribbon": "9.0", "bow": "0.25"}],
        intro="Для украшения подарков из ленты длиной `ribbon` метров делают банты, на один бант уходит `bow` метра. "
              "Оба числа дробные. Бант можно сделать только из целого куска.",
        steps=["Заведи `int bows` — сколько целых бантов получится: `(int) (ribbon / bow)`.",
               "Заведи `double used` — сколько ленты уйдёт на банты: `bows` умножить на `bow`.",
               "Заведи `double left` — сколько ленты останется: `ribbon` минус `used`.",
               "Выведи три строки: `Bows: ` и число бантов, `Used: `, `used` и ` m`, `Left: `, `left` и ` m` — например `Left: 0.5 m`."],
        hint="`ribbon / bow` даёт дробное число, например `6.666…`. Приведение `(int)` отбрасывает дробную часть, и остаётся 6 — "
             "ровно столько целых бантов. А метры ленты остаются дробными, поэтому `used` и `left` — `double`.",
        solution='int bows = (int) (ribbon / bow);\n'
                 'double used = bows * bow;\n'
                 'double left = ribbon - used;\n'
                 'System.out.println("Bows: " + bows);\n'
                 'System.out.println("Used: " + used + " m");\n'
                 'System.out.println("Left: " + left + " m");',
        wrong=[("израсходованная лента сохранена в int: дробная часть метров теряется",
                'int bows = (int) (ribbon / bow);\n'
                'int used = (int) (bows * bow);\n'
                'double left = ribbon - used;\n'
                'System.out.println("Bows: " + bows);\n'
                'System.out.println("Used: " + used + " m");\n'
                'System.out.println("Left: " + left + " m");'),
               ("остаток считает как длину ленты минус один бант",
                'int bows = (int) (ribbon / bow);\n'
                'double used = bows * bow;\n'
                'double left = ribbon - bow;\n'
                'System.out.println("Bows: " + bows);\n'
                'System.out.println("Used: " + used + " m");\n'
                'System.out.println("Left: " + left + " m");')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-types-rt-heart-beats", title="Удары сердца за жизнь",
        given=[("int", "bpm"), ("int", "years")],
        variants=[{"bpm": "70", "years": "80"}, {"bpm": "60", "years": "75"}, {"bpm": "80", "years": "60"}],
        hidden=[{"bpm": "60", "years": "1"}, {"bpm": "90", "years": "50"}, {"bpm": "75", "years": "100"},
                {"bpm": "65", "years": "20"}],
        intro="На уроке биологии считают, сколько раз сердце ударит за жизнь. Пульс — ударов в минуту — записан в поле "
              "`bpm`, число лет — в поле `years`. Считай, что в году 365 дней. Самое большое число типа `int` — 2147483647, "
              "а ударов за жизнь получается больше.",
        steps=["Заведи `int perHour` — ударов за час: `bpm` умножить на `60`; затем `int perDay` — за сутки: `perHour` умножить на `24`.",
               "Заведи `long perYear` — ударов за год: `(long) perDay * 365`.",
               "Заведи `long total` — ударов за все годы: `perYear` умножить на `years`.",
               "Выведи четыре строки: `Per hour: `, `Per day: `, `Per year: `, `Total: ` — после каждой надписи её число."],
        hint="Произведение двух `int` Java считает в `int`, и если оно не помещается, число «переполняется» — молча становится "
             "неверным. `(long)` перед умножением заставляет считать сразу в `long`, а `long`, умноженный на `int`, остаётся `long`.",
        solution='int perHour = bpm * 60;\n'
                 'int perDay = perHour * 24;\n'
                 'long perYear = (long) perDay * 365;\n'
                 'long total = perYear * years;\n'
                 'System.out.println("Per hour: " + perHour);\n'
                 'System.out.println("Per day: " + perDay);\n'
                 'System.out.println("Per year: " + perYear);\n'
                 'System.out.println("Total: " + total);',
        wrong=[("всё считает в int и только потом кладёт в long: произведение уже переполнилось",
                'int perHour = bpm * 60;\n'
                'int perDay = perHour * 24;\n'
                'long perYear = perDay * 365;\n'
                'long total = perDay * 365 * years;\n'
                'System.out.println("Per hour: " + perHour);\n'
                'System.out.println("Per day: " + perDay);\n'
                'System.out.println("Per year: " + perYear);\n'
                'System.out.println("Total: " + total);'),
               ("(long) применён к уже переполненному произведению",
                'int perHour = bpm * 60;\n'
                'int perDay = perHour * 24;\n'
                'long perYear = (long) perDay * 365;\n'
                'long total = (long) (perDay * 365 * years);\n'
                'System.out.println("Per hour: " + perHour);\n'
                'System.out.println("Per day: " + perDay);\n'
                'System.out.println("Per year: " + perYear);\n'
                'System.out.println("Total: " + total);')],
        constructs=["assignment"],
    ),
]
