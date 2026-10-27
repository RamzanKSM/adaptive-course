"""LOGICAL_OR — «Логическое ИЛИ (||)» and ! (Java). Taught before: println, variables, assignment, arithmetic, primitive
types (boolean), String, / and %, += -= ++, if/else, comparison operators, &&. The syntax tree has no construct for
|| or !, so the hidden value sets cover every combination and boundary: `&&` instead of `||`, a lost `!` or a lost
part of the condition gives a wrong answer somewhere. Not yet: switch, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "LOGICAL_OR"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-or-rt-ski-lift", title="Горнолыжный подъёмник",
        given=[("int", "wind"), ("int", "frost")],
        variants=[{"wind": "8", "frost": "12"}, {"wind": "18", "frost": "5"}, {"wind": "10", "frost": "28"}],
        hidden=[{"wind": "15", "frost": "25"}, {"wind": "16", "frost": "0"}, {"wind": "0", "frost": "26"},
                {"wind": "20", "frost": "30"}, {"wind": "3", "frost": "10"}],
        intro="Кресельный подъёмник на горнолыжном курорте останавливают, если ветер сильнее 15 м/с или мороз сильнее "
              "25 градусов. Скорость ветра записана в поле `wind`, сила мороза в градусах — в поле `frost`.",
        steps=["Если `wind` больше 15 **или** `frost` больше 25, выведи `Lift is closed`.",
               "Иначе выведи `Lift is open`.",
               "Запиши обе проверки в одном условии через `||`."],
        hint="Условие с `||` истинно, если верна хотя бы одна его часть: для остановки хватит одного сильного ветра. "
             "При ветре ровно 15 м/с и морозе ровно 25 градусов подъёмник ещё работает.",
        solution='if (wind > 15 || frost > 25) {\n    System.out.println("Lift is closed");\n} else {\n'
                 '    System.out.println("Lift is open");\n}',
        wrong=[("&& вместо ||: закрывает подъёмник, только когда и ветер, и мороз сильные сразу",
                'if (wind > 15 && frost > 25) {\n    System.out.println("Lift is closed");\n} else {\n'
                '    System.out.println("Lift is open");\n}'),
               ("проверяет только ветер: при сильном морозе подъёмник работает",
                'if (wind > 15) {\n    System.out.println("Lift is closed");\n} else {\n'
                '    System.out.println("Lift is open");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-or-not-rt-laptop-update", title="Обновление ноутбука",
        given=[("boolean", "charging"), ("boolean", "presenting")],
        variants=[{"charging": "true", "presenting": "false"}, {"charging": "false", "presenting": "false"},
                  {"charging": "true", "presenting": "true"}],
        hidden=[{"charging": "false", "presenting": "true"}, {"charging": "true", "presenting": "false"},
                {"charging": "false", "presenting": "false"}, {"charging": "true", "presenting": "true"}],
        intro="Ноутбук Ани откладывает установку обновления, если он не подключён к зарядке или на нём сейчас идёт "
              "презентация. Подключён ли он к зарядке, записано в поле `charging`, идёт ли презентация — в поле "
              "`presenting` (оба поля — `true` или `false`).",
        steps=["Если ноутбук **не** заряжается **или** идёт презентация, выведи `Update postponed`.",
               "Иначе выведи `Installing update`.",
               "Запиши обе проверки в одном условии с помощью `!` и `||`."],
        hint="`!` переворачивает логическое значение: `!charging` читается как «ноутбук не заряжается».",
        solution='if (!charging || presenting) {\n    System.out.println("Update postponed");\n} else {\n'
                 '    System.out.println("Installing update");\n}',
        wrong=[("забыт !: откладывает обновление как раз на зарядке",
                'if (charging || presenting) {\n    System.out.println("Update postponed");\n} else {\n'
                '    System.out.println("Installing update");\n}'),
               ("&& вместо ||: откладывает, только когда и нет зарядки, и идёт презентация",
                'if (!charging && presenting) {\n    System.out.println("Update postponed");\n} else {\n'
                '    System.out.println("Installing update");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-or-rt-triangle-sticks", title="Треугольник из палочек",
        given=[("int", "a"), ("int", "b"), ("int", "c")],
        variants=[{"a": "3", "b": "4", "c": "5"}, {"a": "2", "b": "9", "c": "4"}, {"a": "6", "b": "6", "c": "11"}],
        hidden=[{"a": "1", "b": "2", "c": "3"}, {"a": "5", "b": "2", "c": "3"}, {"a": "2", "b": "7", "c": "5"},
                {"a": "10", "b": "1", "c": "1"}, {"a": "1", "b": "1", "c": "10"}, {"a": "7", "b": "7", "c": "7"}],
        intro="Боря хочет сложить треугольник из трёх палочек длиной `a`, `b` и `c` см. Ничего не выйдет, если какие-то "
              "две палочки вместе не длиннее третьей: например, из палочек 1, 2 и 3 см получится только плоская линия.",
        steps=["Выведи строку `Sticks: 3, 4, 5`, подставив `a`, `b` и `c` через запятую и пробел.",
               "Составь одно условие через `||`: `a + b` не больше `c`, **или** `a + c` не больше `b`, **или** "
               "`b + c` не больше `a`.",
               "Если условие верно, выведи следующей строкой `No triangle`.",
               "Иначе выведи следующей строкой `Perimeter: N cm`, где N — сумма длин трёх палочек."],
        hint="«Не больше» — это `<=`. Проверить нужно все три пары палочек: длинной может оказаться любая из трёх.",
        solution='System.out.println("Sticks: " + a + ", " + b + ", " + c);\n'
                 'if (a + b <= c || a + c <= b || b + c <= a) {\n    System.out.println("No triangle");\n} else {\n'
                 '    System.out.println("Perimeter: " + (a + b + c) + " cm");\n}',
        wrong=[("проверяет только одну пару: палочки, где длинная не последняя, «складываются»",
                'System.out.println("Sticks: " + a + ", " + b + ", " + c);\n'
                'if (a + b <= c) {\n    System.out.println("No triangle");\n} else {\n'
                '    System.out.println("Perimeter: " + (a + b + c) + " cm");\n}'),
               ("< вместо <=: из палочек 1, 2 и 3 см «получается» треугольник",
                'System.out.println("Sticks: " + a + ", " + b + ", " + c);\n'
                'if (a + b < c || a + c < b || b + c < a) {\n    System.out.println("No triangle");\n} else {\n'
                '    System.out.println("Perimeter: " + (a + b + c) + " cm");\n}')],
        constructs=["if"],
    ),
]
