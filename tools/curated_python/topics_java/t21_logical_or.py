"""LOGICAL_OR — «Логическое ИЛИ (||)» and ! (Java). Taught before: println, variables, assignment, arithmetic, primitive
types (boolean), String, / and %, += -= ++, if/else, comparison operators, &&. The syntax tree has no construct for
|| or !, so the hidden value sets cover every combination and boundary: `&&` instead of `||`, a lost `!` or a lost
part of the condition gives a wrong answer somewhere. Not yet: switch, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "LOGICAL_OR"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-or-greenhouse-alarm", title="Датчик в теплице",
        given=[("int", "temp")],
        variants=[{"temp": "5"}, {"temp": "22"}, {"temp": "35"}],
        hidden=[{"temp": "10"}, {"temp": "30"}, {"temp": "9"}, {"temp": "31"}, {"temp": "20"}, {"temp": "-3"}],
        intro="В теплице с помидорами стоит датчик. Он поднимает тревогу, если там холоднее 10 °C или жарче 30 °C. "
              "Текущая температура записана в поле `temp`.",
        steps=["Если `temp` меньше 10 **или** больше 30, выведи `Alarm: check the greenhouse`.",
               "Иначе выведи `All is OK`.",
               "Запиши обе проверки в одном условии через `||`."],
        hint="Условие с `||` истинно, если верна хотя бы одна его часть. Ровно 10 °C и ровно 30 °C — ещё нормальная "
             "температура, тревога не нужна.",
        solution='if (temp < 10 || temp > 30) {\n    System.out.println("Alarm: check the greenhouse");\n} else {\n'
                 '    System.out.println("All is OK");\n}',
        wrong=[("&& вместо ||: температура не бывает сразу ниже 10 и выше 30, тревоги нет никогда",
                'if (temp < 10 && temp > 30) {\n    System.out.println("Alarm: check the greenhouse");\n} else {\n'
                '    System.out.println("All is OK");\n}'),
               ("<= и >=: ровно 10 и ровно 30 °C вызывают тревогу",
                'if (temp <= 10 || temp >= 30) {\n    System.out.println("Alarm: check the greenhouse");\n} else {\n'
                '    System.out.println("All is OK");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-or-not-flight-delay", title="Задержка рейса",
        given=[("boolean", "storm"), ("boolean", "fueled")],
        variants=[{"storm": "false", "fueled": "true"}, {"storm": "true", "fueled": "true"}, {"storm": "false", "fueled": "false"}],
        hidden=[{"storm": "false", "fueled": "true"}, {"storm": "true", "fueled": "true"},
                {"storm": "false", "fueled": "false"}, {"storm": "true", "fueled": "false"}],
        intro="Диспетчер в аэропорту решает, можно ли начинать посадку. Идёт ли над аэропортом гроза, записано в поле "
              "`storm`, заправлен ли самолёт — в поле `fueled` (оба поля — `true` или `false`).",
        steps=["Если идёт гроза **или** самолёт **не** заправлен, выведи `The flight is delayed`.",
               "Иначе выведи `Boarding is open`.",
               "Запиши обе проверки в одном условии с помощью `||` и `!`."],
        hint="`!` переворачивает логическое значение: `!true` — это `false`, а `!false` — это `true`. "
             "Подумай, как с его помощью записать «самолёт не заправлен».",
        solution='if (storm || !fueled) {\n    System.out.println("The flight is delayed");\n} else {\n'
                 '    System.out.println("Boarding is open");\n}',
        wrong=[("забыт !: задерживает как раз заправленный самолёт",
                'if (storm || fueled) {\n    System.out.println("The flight is delayed");\n} else {\n'
                '    System.out.println("Boarding is open");\n}'),
               ("&& вместо ||: задерживает рейс, только когда и гроза, и самолёт не заправлен",
                'if (storm && !fueled) {\n    System.out.println("The flight is delayed");\n} else {\n'
                '    System.out.println("Boarding is open");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-or-leap-year", title="Високосный год",
        given=[("int", "year")],
        variants=[{"year": "2024"}, {"year": "1900"}, {"year": "2000"}],
        hidden=[{"year": "2023"}, {"year": "2100"}, {"year": "2400"}, {"year": "1996"}, {"year": "2000"}, {"year": "1900"}],
        intro="Год високосный, если он делится на 4, но не делится на 100. Исключение — годы, которые делятся на 400: "
              "они тоже високосные. Поэтому 2000 год был високосным, а 1900 — нет. Год записан в поле `year`.",
        steps=["Составь одно условие: год делится на 4 **и** не делится на 100, **или** год делится на 400.",
               "Если условие верно, выведи строку `Year … is a leap year: 366 days`, подставив значение `year`.",
               "Иначе выведи `Year … is a common year: 365 days`."],
        hint="«Делится на 100» — это `year % 100 == 0`, а «не делится» — `year % 100 != 0`. "
             "Возьми часть с `&&` в скобки: так сразу видно, какие проверки связаны между собой.",
        solution='if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {\n'
                 '    System.out.println("Year " + year + " is a leap year: 366 days");\n} else {\n'
                 '    System.out.println("Year " + year + " is a common year: 365 days");\n}',
        wrong=[("проверяет только деление на 4: 1900 и 2100 становятся високосными",
                'if (year % 4 == 0) {\n'
                '    System.out.println("Year " + year + " is a leap year: 366 days");\n} else {\n'
                '    System.out.println("Year " + year + " is a common year: 365 days");\n}'),
               ("забыто исключение для 400: 2000 год получается обычным",
                'if (year % 4 == 0 && year % 100 != 0) {\n'
                '    System.out.println("Year " + year + " is a leap year: 366 days");\n} else {\n'
                '    System.out.println("Year " + year + " is a common year: 365 days");\n}')],
        constructs=["if"],
    ),
]
