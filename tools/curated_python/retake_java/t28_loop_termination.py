"""LOOP_TERMINATION — «Завершение цикла» (Java): while-циклы, которые обязаны остановиться — условие зависит от
переменной, которая меняется в цикле, и выход через break. Taught before: println, variables, arithmetic, primitive
types, String, / and %, += ++, if/else, comparisons, &&, ||, switch, for, accumulator, while.
Not yet: arrays, own methods. Every loop here (references and wrong solutions) stops for every value set."""
from java_tasks import JavaOutputTask

SKILL = "LOOP_TERMINATION"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-lt-rt-pancake-flour", title="Блины, пока есть мука",
        given=[("int", "flour"), ("int", "per")],
        variants=[{"flour": "500", "per": "120"}, {"flour": "300", "per": "60"}, {"flour": "250", "per": "70"}],
        hidden=[{"flour": "240", "per": "80"}, {"flour": "50", "per": "80"}, {"flour": "80", "per": "80"},
                {"flour": "1000", "per": "150"}],
        intro="Бабушка печёт блины. Муки у неё {flour} г (поле `flour`), а на один блин уходит {per} г (поле `per`). "
              "Она печёт, пока муки хватает ещё на один блин.",
        steps=["Заведи счётчик блинов `count` со значением 0.",
               "Напиши цикл `while`, который работает, пока `flour` не меньше `per`. В цикле уменьши `flour` на `per`, "
               "увеличь `count` на 1 и выведи строку `Pancake …` с номером блина.",
               "Когда цикл закончится, выведи `Flour left: … g`."],
        hint="Цикл остановится, только если внутри него `flour` уменьшается: тогда условие рано или поздно станет "
             "ложным. Если муки осталось ровно на один блин, его ещё можно испечь.",
        solution='int count = 0;\nwhile (flour >= per) {\n    flour -= per;\n    count++;\n    System.out.println("Pancake " + count);\n}\n'
                 'System.out.println("Flour left: " + flour + " g");',
        wrong=[("> вместо >=: последний блин, на который муки ровно хватает, не испечён",
                'int count = 0;\nwhile (flour > per) {\n    flour -= per;\n    count++;\n    System.out.println("Pancake " + count);\n}\n'
                'System.out.println("Flour left: " + flour + " g");'),
               ("условие flour > 0: печёт, даже когда муки не хватает, и мука уходит в минус",
                'int count = 0;\nwhile (flour > 0) {\n    flour -= per;\n    count++;\n    System.out.println("Pancake " + count);\n}\n'
                'System.out.println("Flour left: " + flour + " g");')],
        constructs=["while"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-lt-rt-two-trams", title="Два трамвая из депо",
        given=[("int", "a"), ("int", "b")],
        variants=[{"a": "6", "b": "8"}, {"a": "10", "b": "15"}, {"a": "9", "b": "12"}],
        hidden=[{"a": "5", "b": "5"}, {"a": "4", "b": "12"}, {"a": "12", "b": "4"}, {"a": "7", "b": "3"}],
        intro="Ровно в 6:00 из депо одновременно выходят два трамвая. Дальше трамвай первого маршрута выходит каждые "
              "{a} мин. (поле `a`), а второго — каждые {b} мин. (поле `b`). Через сколько минут они снова выйдут вместе?",
        steps=["Заведи переменную `t` и положи в неё `a` — когда первый маршрут выходит во второй раз.",
               "Напиши цикл `while`: пока `t` не делится на `b` без остатка, второй трамвай в эту минуту не выходит — "
               "прибавь к `t` значение `a`, чтобы перейти к следующему выходу первого маршрута.",
               "После цикла выведи две строки: `Together again after … min` и `Trips: …, …` — сколько раз за это время "
               "вышел каждый маршрут (`t / a` и `t / b`), не считая выхода в 6:00."],
        hint="`t` растёт на каждом повторе, а среди чисел `a`, `2 * a`, `3 * a`… обязательно встретится число, которое "
             "делится на `b`, — поэтому цикл закончится. Не начинай с 0: ноль делится на что угодно, и цикл "
             "остановится сразу.",
        solution='int t = a;\nwhile (t % b != 0) {\n    t += a;\n}\nSystem.out.println("Together again after " + t + " min");\n'
                 'System.out.println("Trips: " + t / a + ", " + t / b);',
        wrong=[("начинает с 0: цикл не выполняется ни разу, ответ 0 минут",
                'int t = 0;\nwhile (t % b != 0) {\n    t += a;\n}\nSystem.out.println("Together again after " + t + " min");\n'
                'System.out.println("Trips: " + t / a + ", " + t / b);'),
               ("прибавляет по 1 минуте: находит выход второго маршрута, а не общий",
                'int t = a;\nwhile (t % b != 0) {\n    t++;\n}\nSystem.out.println("Together again after " + t + " min");\n'
                'System.out.println("Trips: " + t / a + ", " + t / b);')],
        constructs=["while"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-lt-rt-cookie-boxes", title="Коробки для печенья",
        given=[("int", "cookies")],
        variants=[{"cookies": "56"}, {"cookies": "45"}, {"cookies": "53"}],
        hidden=[{"cookies": "10"}, {"cookies": "20"}, {"cookies": "18"}, {"cookies": "11"}, {"cookies": "63"},
                {"cookies": "13"}],
        intro="Пекарня испекла {cookies} печений (поле `cookies`) и хочет разложить их в одинаковые коробки без остатка. "
              "Бывают коробки на 6, 7, 8, 9 и 10 печений. Нужна самая маленькая подходящая коробка.",
        steps=["Выведи строку `Cookies: …`.",
               "Заведи переменную `size` со значением 6. Напиши цикл `while`, который работает, пока `size` не больше 10. "
               "В цикле: если `cookies` делится на `size` без остатка, коробка подходит — выйди из цикла командой `break`. "
               "Иначе увеличь `size` на 1.",
               "После цикла: если `size` не больше 10, выведи `Box of …: … boxes` — размер коробки и сколько коробок нужно. "
               "Иначе выведи `No box from 6 to 10 fits`."],
        hint="У цикла два выхода: `break`, когда коробка нашлась, и условие `size <= 10`, когда все размеры перебраны. "
             "После цикла по значению `size` видно, каким выходом он закончился: если коробка не нашлась, `size` стало 11.",
        solution='System.out.println("Cookies: " + cookies);\nint size = 6;\nwhile (size <= 10) {\n    if (cookies % size == 0) {\n'
                 '        break;\n    }\n    size++;\n}\nif (size <= 10) {\n    System.out.println("Box of " + size + ": " + cookies / size + " boxes");\n'
                 '} else {\n    System.out.println("No box from 6 to 10 fits");\n}',
        wrong=[("< 10 вместо <= 10: коробка на 10 печений не проверяется",
                'System.out.println("Cookies: " + cookies);\nint size = 6;\nwhile (size < 10) {\n    if (cookies % size == 0) {\n'
                '        break;\n    }\n    size++;\n}\nif (size < 10) {\n    System.out.println("Box of " + size + ": " + cookies / size + " boxes");\n'
                '} else {\n    System.out.println("No box from 6 to 10 fits");\n}'),
               ("после цикла проверяет делимость, а не size: при 11 печеньях «находит» коробку на 11",
                'System.out.println("Cookies: " + cookies);\nint size = 6;\nwhile (size <= 10) {\n    if (cookies % size == 0) {\n'
                '        break;\n    }\n    size++;\n}\nif (cookies % size == 0) {\n    System.out.println("Box of " + size + ": " + cookies / size + " boxes");\n'
                '} else {\n    System.out.println("No box from 6 to 10 fits");\n}')],
        constructs=["while", "if"],
    ),
]
