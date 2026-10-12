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
        steps=["Если `temp` не меньше 24 **и** не больше 28, выведи `Рыбкам комфортно`.",
               "Иначе выведи `Температуру нужно поправить`.",
               "Запиши обе проверки в одном условии через `&&`."],
        hint="Условие с `&&` истинно, только когда истинны обе его части. Каждая часть — полное сравнение с `temp`: "
             "запись вида `24 <= temp <= 28` в Java не скомпилируется.",
        solution='if (temp >= 24 && temp <= 28) {\n    System.out.println("Рыбкам комфортно");\n} else {\n'
                 '    System.out.println("Температуру нужно поправить");\n}',
        wrong=[("строгие сравнения: ровно 24 и ровно 28 °C считаются неподходящими",
                'if (temp > 24 && temp < 28) {\n    System.out.println("Рыбкам комфортно");\n} else {\n'
                '    System.out.println("Температуру нужно поправить");\n}'),
               ("|| вместо &&: условие верно при любой температуре",
                'if (temp >= 24 || temp <= 28) {\n    System.out.println("Рыбкам комфортно");\n} else {\n'
                '    System.out.println("Температуру нужно поправить");\n}')],
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
        steps=["Если паспорт есть **и** опоздание не больше 15 минут, выведи `Проходите в аудиторию`.",
               "Иначе выведи `Вход на экзамен закрыт`.",
               "Объедини обе проверки в одном условии через `&&`."],
        hint="Переменная типа `boolean` сама уже является условием: `hasPassport && …` читается как «паспорт есть и …». "
             "Ученика, опоздавшего ровно на 15 минут, ещё пускают.",
        solution='if (hasPassport && minutesLate <= 15) {\n    System.out.println("Проходите в аудиторию");\n} else {\n'
                 '    System.out.println("Вход на экзамен закрыт");\n}',
        wrong=[("|| вместо &&: пускает без паспорта или с большим опозданием",
                'if (hasPassport || minutesLate <= 15) {\n    System.out.println("Проходите в аудиторию");\n} else {\n'
                '    System.out.println("Вход на экзамен закрыт");\n}'),
               ("строгое < 15: опоздавшего ровно на 15 минут не пускает",
                'if (hasPassport && minutesLate < 15) {\n    System.out.println("Проходите в аудиторию");\n} else {\n'
                '    System.out.println("Вход на экзамен закрыт");\n}')],
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
               "Если условие верно, выведи `Треугольник получится`, а следующей строкой — `Периметр: … см` "
               "(сумма длин трёх палочек).",
               "Иначе выведи одну строку `Треугольник не сложить`."],
        hint="Если одна палочка ровно равна сумме двух других, треугольник «сплющится» в отрезок, поэтому сравнения "
             "строгие. Длинное условие можно перенести на новую строку сразу после `&&`.",
        solution='if (a < b + c && b < a + c && c < a + b) {\n    System.out.println("Треугольник получится");\n'
                 '    System.out.println("Периметр: " + (a + b + c) + " см");\n} else {\n'
                 '    System.out.println("Треугольник не сложить");\n}',
        wrong=[("проверяет только c < a + b: не замечает, что слишком длинной может оказаться a или b",
                'if (c < a + b) {\n    System.out.println("Треугольник получится");\n'
                '    System.out.println("Периметр: " + (a + b + c) + " см");\n} else {\n'
                '    System.out.println("Треугольник не сложить");\n}'),
               ("<= вместо <: «сплющенный» треугольник считается настоящим",
                'if (a <= b + c && b <= a + c && c <= a + b) {\n    System.out.println("Треугольник получится");\n'
                '    System.out.println("Периметр: " + (a + b + c) + " см");\n} else {\n'
                '    System.out.println("Треугольник не сложить");\n}')],
        constructs=["if"],
    ),
]
