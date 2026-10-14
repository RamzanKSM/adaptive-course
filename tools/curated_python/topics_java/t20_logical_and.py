"""LOGICAL_AND — «Логическое И (&&)» (Java). Taught before: println, variables, assignment, arithmetic, primitive types
(boolean), String, / and %, += -= ++, if/else, comparison operators. The syntax tree has no construct for &&, so every
hidden value set is chosen to need both parts of the condition (and its boundaries): `||`, a lost part or a strict
comparison gives a wrong answer somewhere. Not yet: || and !, switch, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "LOGICAL_AND"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-and-aquarium", title="Температура в аквариуме",
        given=[("int", "temp")],
        variants=[{"temp": "26"}, {"temp": "22"}, {"temp": "30"}],
        hidden=[{"temp": "24"}, {"temp": "28"}, {"temp": "23"}, {"temp": "29"}, {"temp": "25"}, {"temp": "15"}],
        intro="Рыбкам в аквариуме хорошо, когда вода не холоднее 24 °C и не теплее 28 °C. "
              "Датчик записал температуру воды в поле `temp`.",
        steps=["Если `temp` не меньше 24 **и** не больше 28, выведи `The fish are fine`.",
               "Иначе выведи `Fix the temperature`.",
               "Запиши обе проверки в одном условии через `&&`."],
        hint="Условие с `&&` истинно, только когда истинны обе его части. Каждая часть — полное сравнение с `temp`: "
             "запись вида `24 <= temp <= 28` в Java не скомпилируется.",
        solution='if (temp >= 24 && temp <= 28) {\n    System.out.println("The fish are fine");\n} else {\n'
                 '    System.out.println("Fix the temperature");\n}',
        wrong=[("строгие сравнения: ровно 24 и ровно 28 °C считаются неподходящими",
                'if (temp > 24 && temp < 28) {\n    System.out.println("The fish are fine");\n} else {\n'
                '    System.out.println("Fix the temperature");\n}'),
               ("|| вместо &&: условие верно при любой температуре",
                'if (temp >= 24 || temp <= 28) {\n    System.out.println("The fish are fine");\n} else {\n'
                '    System.out.println("Fix the temperature");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-and-exam-entry", title="Пропуск на экзамен",
        given=[("boolean", "hasPassport"), ("int", "minutesLate")],
        variants=[{"hasPassport": "true", "minutesLate": "5"}, {"hasPassport": "false", "minutesLate": "0"},
                  {"hasPassport": "true", "minutesLate": "20"}],
        hidden=[{"hasPassport": "true", "minutesLate": "15"}, {"hasPassport": "true", "minutesLate": "16"},
                {"hasPassport": "false", "minutesLate": "10"}, {"hasPassport": "true", "minutesLate": "0"},
                {"hasPassport": "false", "minutesLate": "40"}],
        intro="На экзамен пускают, только если у ученика с собой паспорт и он опоздал не больше чем на 15 минут. "
              "Есть ли паспорт, записано в поле `hasPassport` (`true` или `false`), на сколько минут ученик опоздал — "
              "в поле `minutesLate` (0 — пришёл вовремя).",
        steps=["Если паспорт есть **и** опоздание не больше 15 минут, выведи `Come in, please`.",
               "Иначе выведи `Entry is closed`.",
               "Объедини обе проверки в одном условии через `&&`."],
        hint="Переменная типа `boolean` сама уже является условием: `hasPassport && …` читается как «паспорт есть и …». "
             "Ученика, опоздавшего ровно на 15 минут, ещё пускают.",
        solution='if (hasPassport && minutesLate <= 15) {\n    System.out.println("Come in, please");\n} else {\n'
                 '    System.out.println("Entry is closed");\n}',
        wrong=[("|| вместо &&: пускает без паспорта или с большим опозданием",
                'if (hasPassport || minutesLate <= 15) {\n    System.out.println("Come in, please");\n} else {\n'
                '    System.out.println("Entry is closed");\n}'),
               ("строгое < 15: опоздавшего ровно на 15 минут не пускает",
                'if (hasPassport && minutesLate < 15) {\n    System.out.println("Come in, please");\n} else {\n'
                '    System.out.println("Entry is closed");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-and-triangle-sticks", title="Треугольник из палочек",
        given=[("int", "a"), ("int", "b"), ("int", "c")],
        variants=[{"a": "3", "b": "4", "c": "5"}, {"a": "2", "b": "3", "c": "7"}, {"a": "7", "b": "10", "c": "5"}],
        hidden=[{"a": "1", "b": "2", "c": "3"}, {"a": "10", "b": "3", "c": "4"}, {"a": "3", "b": "10", "c": "4"},
                {"a": "6", "b": "6", "c": "6"}, {"a": "5", "b": "9", "c": "5"}, {"a": "4", "b": "8", "c": "4"}],
        intro="У Димы три палочки длиной `a`, `b` и `c` сантиметров. Треугольник из них сложится, только если каждая "
              "палочка короче, чем две другие вместе.",
        steps=["Составь одно условие из трёх сравнений, соединённых `&&`: `a` меньше `b + c`, `b` меньше `a + c` "
               "и `c` меньше `a + b`.",
               "Если условие верно, выведи `Triangle: yes`, а следующей строкой — `Perimeter: … cm` "
               "(сумма длин трёх палочек).",
               "Иначе выведи одну строку `Triangle: no`."],
        hint="Если одна палочка ровно равна сумме двух других, треугольник «сплющится» в отрезок, поэтому сравнения "
             "строгие. Длинное условие можно перенести на новую строку сразу после `&&`.",
        solution='if (a < b + c && b < a + c && c < a + b) {\n    System.out.println("Triangle: yes");\n'
                 '    System.out.println("Perimeter: " + (a + b + c) + " cm");\n} else {\n'
                 '    System.out.println("Triangle: no");\n}',
        wrong=[("проверяет только c < a + b: не замечает, что слишком длинной может оказаться a или b",
                'if (c < a + b) {\n    System.out.println("Triangle: yes");\n'
                '    System.out.println("Perimeter: " + (a + b + c) + " cm");\n} else {\n'
                '    System.out.println("Triangle: no");\n}'),
               ("<= вместо <: «сплющенный» треугольник считается настоящим",
                'if (a <= b + c && b <= a + c && c <= a + b) {\n    System.out.println("Triangle: yes");\n'
                '    System.out.println("Perimeter: " + (a + b + c) + " cm");\n} else {\n'
                '    System.out.println("Triangle: no");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-and-bakery-hours", title="Открыта ли пекарня",
        given=[("int", "hour")],
        variants=[{"hour": "14"}, {"hour": "7"}, {"hour": "21"}],
        hidden=[{"hour": "8"}, {"hour": "9"}, {"hour": "20"}, {"hour": "22"}, {"hour": "0"}, {"hour": "12"}],
        intro="Пекарня у дома работает с 8 утра до 9 вечера: покупателей обслуживают, если сейчас не раньше 8 часов "
              "и не позже 20 часов. Который сейчас час (от 0 до 23), записано в поле `hour`.",
        steps=["Если `hour` не меньше 8 **и** не больше 20, выведи `The bakery is open`.",
               "Иначе выведи `Come back later`.",
               "Запиши обе проверки в одном условии через `&&`."],
        hint="Каждая часть условия с `&&` — отдельное полное сравнение с `hour`. В 8 и в 20 часов пекарня ещё работает.",
        solution='if (hour >= 8 && hour <= 20) {\n    System.out.println("The bakery is open");\n} else {\n'
                 '    System.out.println("Come back later");\n}',
        wrong=[("строгие сравнения: в 8 и в 20 часов пекарня считается закрытой",
                'if (hour > 8 && hour < 20) {\n    System.out.println("The bakery is open");\n} else {\n'
                '    System.out.println("Come back later");\n}'),
               ("проверяет только начало работы: поздно вечером тоже пишет, что открыто",
                'if (hour >= 8) {\n    System.out.println("The bakery is open");\n} else {\n'
                '    System.out.println("Come back later");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-and-card-discount", title="Скидка по карте",
        given=[("boolean", "hasCard"), ("int", "total")],
        variants=[{"hasCard": "true", "total": "1800"}, {"hasCard": "false", "total": "2500"},
                  {"hasCard": "true", "total": "600"}],
        hidden=[{"hasCard": "true", "total": "1000"}, {"hasCard": "true", "total": "990"},
                {"hasCard": "false", "total": "1000"}, {"hasCard": "true", "total": "4500"},
                {"hasCard": "false", "total": "300"}],
        intro="В книжном магазине скидка 10 процентов положена тем, у кого есть карта покупателя и покупка на 1000 руб. или больше. "
              "Есть ли у покупателя карта, записано в поле `hasCard` (`true` или `false`), сумма покупки в рублях — в поле `total`.",
        steps=["Если карта есть **и** `total` не меньше 1000, скидка равна `total / 10`, иначе скидка 0. Объедини обе проверки в одном условии через `&&`.",
               "Выведи две строки: `Discount: … rub` и `To pay: … rub` (сумма покупки минус скидка)."],
        hint="Переменная типа `boolean` сама является условием: `hasCard && …`. Заведи переменную для скидки до `if`, "
             "а в ветках только присвой ей значение. Покупка ровно на 1000 руб. уже со скидкой.",
        solution='int discount;\nif (hasCard && total >= 1000) {\n    discount = total / 10;\n} else {\n    discount = 0;\n}\n'
                 'System.out.println("Discount: " + discount + " rub");\nSystem.out.println("To pay: " + (total - discount) + " rub");',
        wrong=[("|| вместо &&: скидка даже без карты или на маленькую покупку",
                'int discount;\nif (hasCard || total >= 1000) {\n    discount = total / 10;\n} else {\n    discount = 0;\n}\n'
                'System.out.println("Discount: " + discount + " rub");\nSystem.out.println("To pay: " + (total - discount) + " rub");'),
               ("строгое > 1000: покупка ровно на 1000 руб. остаётся без скидки",
                'int discount;\nif (hasCard && total > 1000) {\n    discount = total / 10;\n} else {\n    discount = 0;\n}\n'
                'System.out.println("Discount: " + discount + " rub");\nSystem.out.println("To pay: " + (total - discount) + " rub");')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-and-cabin-bag", title="Ручная кладь в самолёт",
        given=[("int", "length"), ("int", "width"), ("int", "depth")],
        variants=[{"length": "50", "width": "35", "depth": "20"}, {"length": "60", "width": "40", "depth": "20"},
                  {"length": "55", "width": "30", "depth": "25"}],
        hidden=[{"length": "55", "width": "40", "depth": "20"}, {"length": "56", "width": "30", "depth": "15"},
                {"length": "40", "width": "41", "depth": "15"}, {"length": "40", "width": "30", "depth": "21"},
                {"length": "30", "width": "20", "depth": "10"}, {"length": "45", "width": "40", "depth": "20"}],
        intro="В салон самолёта можно взять сумку не больше 55 × 40 × 20 см. Размеры сумки Ани записаны в полях "
              "`length`, `width` и `depth` (в сантиметрах).",
        steps=["Составь одно условие из трёх сравнений, соединённых `&&`: `length` не больше 55, `width` не больше 40 "
               "и `depth` не больше 20.",
               "Если условие верно, выведи `Cabin bag: OK`, а следующей строкой — `Volume: … l`: объём сумки в литрах, "
               "то есть произведение трёх размеров, делённое на 1000 нацело.",
               "Иначе выведи одну строку `Cabin bag: too big`."],
        hint="Сумка ровно 55 × 40 × 20 см ещё проходит, поэтому нужны `<=`. Длинное условие можно перенести на новую строку сразу после `&&`.",
        solution='if (length <= 55 && width <= 40 && depth <= 20) {\n    System.out.println("Cabin bag: OK");\n'
                 '    System.out.println("Volume: " + length * width * depth / 1000 + " l");\n} else {\n'
                 '    System.out.println("Cabin bag: too big");\n}',
        wrong=[("проверяет только длину и ширину, забывает про глубину",
                'if (length <= 55 && width <= 40) {\n    System.out.println("Cabin bag: OK");\n'
                '    System.out.println("Volume: " + length * width * depth / 1000 + " l");\n} else {\n'
                '    System.out.println("Cabin bag: too big");\n}'),
               ("строгие сравнения: сумка ровно по размерам считается слишком большой",
                'if (length < 55 && width < 40 && depth < 20) {\n    System.out.println("Cabin bag: OK");\n'
                '    System.out.println("Volume: " + length * width * depth / 1000 + " l");\n} else {\n'
                '    System.out.println("Cabin bag: too big");\n}')],
        constructs=["if"],
    ),
]
