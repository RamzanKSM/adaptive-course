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
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-or-museum-free", title="Бесплатный вход в музей",
        given=[("int", "age")],
        variants=[{"age": "5"}, {"age": "34"}, {"age": "70"}],
        hidden=[{"age": "6"}, {"age": "7"}, {"age": "64"}, {"age": "65"}, {"age": "18"}, {"age": "90"}],
        intro="В краеведческий музей бесплатно пускают детей младше 7 лет и пенсионеров от 65 лет. Остальные покупают "
              "билет за 300 руб. Возраст посетителя записан в поле `age`.",
        steps=["Если `age` меньше 7 **или** не меньше 65, выведи `Free entry`.",
               "Иначе выведи `Ticket: 300 rub`.",
               "Запиши обе проверки в одном условии через `||`."],
        hint="Условие с `||` истинно, если верна хотя бы одна его часть. Семилетний уже платит, а 65-летний проходит бесплатно.",
        solution='if (age < 7 || age >= 65) {\n    System.out.println("Free entry");\n} else {\n'
                 '    System.out.println("Ticket: 300 rub");\n}',
        wrong=[("&& вместо ||: возраст не бывает сразу меньше 7 и больше 64, бесплатно не проходит никто",
                'if (age < 7 && age >= 65) {\n    System.out.println("Free entry");\n} else {\n'
                '    System.out.println("Ticket: 300 rub");\n}'),
               ("> 65 вместо >= 65: 65-летнему приходится платить",
                'if (age < 7 || age > 65) {\n    System.out.println("Free entry");\n} else {\n'
                '    System.out.println("Ticket: 300 rub");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-or-not-phone-ring", title="Беззвучный режим",
        given=[("boolean", "silent"), ("boolean", "favorite")],
        variants=[{"silent": "true", "favorite": "false"}, {"silent": "false", "favorite": "false"},
                  {"silent": "true", "favorite": "true"}],
        hidden=[{"silent": "false", "favorite": "true"}, {"silent": "true", "favorite": "false"},
                {"silent": "false", "favorite": "false"}, {"silent": "true", "favorite": "true"}],
        intro="Телефон Бориса звонит громко, если беззвучный режим выключен или звонит кто-то из избранных контактов. "
              "Включён ли беззвучный режим, записано в поле `silent`, звонит ли избранный контакт — в поле `favorite` "
              "(оба поля — `true` или `false`).",
        steps=["Если беззвучный режим **не** включён **или** звонит избранный контакт, выведи `Ring! Ring!`.",
               "Иначе выведи `Quiet call`.",
               "Запиши обе проверки в одном условии с помощью `!` и `||`."],
        hint="`!` переворачивает логическое значение: `!silent` читается как «беззвучный режим не включён».",
        solution='if (!silent || favorite) {\n    System.out.println("Ring! Ring!");\n} else {\n'
                 '    System.out.println("Quiet call");\n}',
        wrong=[("забыт !: звонит громко как раз в беззвучном режиме",
                'if (silent || favorite) {\n    System.out.println("Ring! Ring!");\n} else {\n'
                '    System.out.println("Quiet call");\n}'),
               ("&& вместо ||: громко звонят только избранные и только без беззвучного режима",
                'if (!silent && favorite) {\n    System.out.println("Ring! Ring!");\n} else {\n'
                '    System.out.println("Quiet call");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-or-weekend-gift", title="Подарок в выходные",
        given=[("int", "day"), ("int", "total")],
        variants=[{"day": "6", "total": "1500"}, {"day": "3", "total": "2000"}, {"day": "7", "total": "800"}],
        hidden=[{"day": "6", "total": "1000"}, {"day": "7", "total": "999"}, {"day": "6", "total": "200"},
                {"day": "5", "total": "5000"}, {"day": "7", "total": "3000"}, {"day": "1", "total": "100"}],
        intro="Магазин игрушек дарит подарок за покупку от 1000 руб., но только в выходные. День недели записан в поле `day` "
              "(1 — понедельник, …, 6 — суббота, 7 — воскресенье), сумма покупки в рублях — в поле `total`.",
        steps=["Выведи строку `Day …, total … rub`, подставив `day` и `total`.",
               "Составь одно условие: день — суббота **или** воскресенье, **и** при этом `total` не меньше 1000.",
               "Если условие верно, выведи следующей строкой `Gift: yes`, иначе — `Gift: no`."],
        hint="`&&` выполняется раньше, чем `||`, как умножение раньше сложения. Поэтому проверку дня "
             "(`day == 6 || day == 7`) нужно взять в скобки, иначе в субботу подарок получит любая покупка.",
        solution='System.out.println("Day " + day + ", total " + total + " rub");\n'
                 'if ((day == 6 || day == 7) && total >= 1000) {\n    System.out.println("Gift: yes");\n} else {\n'
                 '    System.out.println("Gift: no");\n}',
        wrong=[("без скобок: в субботу подарок получает даже маленькая покупка",
                'System.out.println("Day " + day + ", total " + total + " rub");\n'
                'if (day == 6 || day == 7 && total >= 1000) {\n    System.out.println("Gift: yes");\n} else {\n'
                '    System.out.println("Gift: no");\n}'),
               ("> 1000 вместо >= 1000: покупка ровно на 1000 руб. без подарка",
                'System.out.println("Day " + day + ", total " + total + " rub");\n'
                'if ((day == 6 || day == 7) && total > 1000) {\n    System.out.println("Gift: yes");\n} else {\n'
                '    System.out.println("Gift: no");\n}')],
        constructs=["if"],
    ),
]
