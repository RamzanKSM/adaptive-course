"""LOGICAL_AND — «Логическое И (&&)» (Java). Taught before: println, variables, assignment, arithmetic, primitive types
(boolean), String, / and %, += -= ++, if/else, comparison operators. The syntax tree has no construct for &&, so every
hidden value set is chosen to need both parts of the condition (and its boundaries): `||`, a lost part or a strict
comparison gives a wrong answer somewhere. Not yet: || and !, switch, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "LOGICAL_AND"


def _pulse(condition: str) -> str:
    return (f'if ({condition}) {{\n    System.out.println("Keep this pace");\n}} else {{\n'
            '    System.out.println("Change the pace");\n}')


def _garden(condition: str) -> str:
    return (f'if ({condition}) {{\n    System.out.println("Water the garden");\n'
            '    System.out.println("Water needed: " + beds * 10 + " l");\n} else {\n'
            '    System.out.println("No watering today");\n}')


def _sport(condition: str) -> str:
    return ('int total = run + jump + swim;\nSystem.out.println("Total: " + total);\n'
            f'if ({condition}) {{\n    System.out.println("Qualified");\n}} else {{\n    System.out.println("Not qualified");\n}}')


TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-and-rt-pulse-zone", title="Пульс на пробежке",
        given=[("int", "pulse")],
        variants=[{"pulse": "135"}, {"pulse": "110"}, {"pulse": "162"}],
        hidden=[{"pulse": "120"}, {"pulse": "150"}, {"pulse": "119"}, {"pulse": "151"}, {"pulse": "140"}, {"pulse": "70"}],
        intro="Тренер советует бегать так, чтобы пульс был не ниже 120 и не выше 150 ударов в минуту. "
              "Фитнес-браслет записал текущий пульс в поле `pulse`.",
        steps=["Если `pulse` не меньше 120 **и** не больше 150, выведи `Keep this pace`.",
               "Иначе выведи `Change the pace`.",
               "Запиши обе проверки в одном условии через `&&`."],
        hint="Условие с `&&` истинно, только когда истинны обе его части. Каждая часть — полное сравнение с `pulse`: "
             "запись вида `120 <= pulse <= 150` в Java не скомпилируется. Пульс ровно 120 или ровно 150 подходит.",
        solution=_pulse('pulse >= 120 && pulse <= 150'),
        wrong=[("строгие сравнения: пульс ровно 120 и ровно 150 считается неподходящим",
                _pulse('pulse > 120 && pulse < 150')),
               ("проверяет только нижнюю границу: слишком частый пульс тоже одобряет",
                _pulse('pulse >= 120'))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-and-rt-garden-watering", title="Полив огорода",
        given=[("int", "rain"), ("int", "temp"), ("int", "beds")],
        variants=[{"rain": "0", "temp": "28", "beds": "6"}, {"rain": "12", "temp": "30", "beds": "4"},
                  {"rain": "3", "temp": "17", "beds": "8"}],
        hidden=[{"rain": "4", "temp": "20", "beds": "5"}, {"rain": "5", "temp": "25", "beds": "5"},
                {"rain": "0", "temp": "19", "beds": "3"}, {"rain": "2", "temp": "35", "beds": "10"},
                {"rain": "20", "temp": "10", "beds": "2"}],
        intro="Автоматический полив включается, если за ночь выпало меньше 5 мм дождя и днём не холоднее 20 °C. "
              "Сколько миллиметров дождя выпало, записано в поле `rain`, температура — в поле `temp`, число грядок — "
              "в поле `beds`. Каждой грядке нужно 10 литров воды.",
        steps=["Если `rain` меньше 5 **и** `temp` не меньше 20, выведи `Water the garden`, а следующей строкой — "
               "`Water needed: … l` (сколько литров нужно на все грядки).",
               "Иначе выведи одну строку `No watering today`.",
               "Объедини обе проверки в одном условии через `&&`."],
        hint="Полив нужен, только когда выполнены оба условия сразу. Обрати внимание на границы: при ровно 5 мм дождя "
             "поливать уже не надо, а при ровно 20 °C — надо.",
        solution=_garden('rain < 5 && temp >= 20'),
        wrong=[("|| вместо &&: поливает и после дождя, и в холод",
                _garden('rain < 5 || temp >= 20')),
               ("<= 5 вместо < 5: поливает после ровно 5 мм дождя",
                _garden('rain <= 5 && temp >= 20'))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-and-rt-sport-qualification", title="Отбор на соревнования",
        given=[("int", "run"), ("int", "jump"), ("int", "swim")],
        variants=[{"run": "75", "jump": "68", "swim": "80"}, {"run": "90", "jump": "55", "swim": "85"},
                  {"run": "62", "jump": "65", "swim": "61"}],
        hidden=[{"run": "60", "jump": "70", "swim": "70"}, {"run": "60", "jump": "60", "swim": "79"},
                {"run": "59", "jump": "80", "swim": "80"}, {"run": "80", "jump": "80", "swim": "59"},
                {"run": "100", "jump": "100", "swim": "100"}, {"run": "70", "jump": "59", "swim": "90"}],
        intro="Чтобы попасть в сборную школы по троеборью, нужно в каждом виде — беге, прыжках и плавании — набрать "
              "не меньше 60 баллов, а в сумме — не меньше 200. Баллы спортсмена записаны в полях `run`, `jump` и `swim`.",
        steps=["Заведи `int total` — сумму трёх баллов — и выведи `Total: ` и `total`.",
               "Составь одно условие из четырёх сравнений, соединённых `&&`: каждый из трёх баллов не меньше 60 "
               "и `total` не меньше 200.",
               "Если условие верно, выведи `Qualified`, иначе — `Not qualified`."],
        hint="Хорошая сумма не спасает провал в одном виде, а проходные баллы во всех видах не спасают маленькую сумму, — "
             "поэтому нужны все четыре проверки. Длинное условие можно перенести на новую строку сразу после `&&`.",
        solution=_sport('run >= 60 && jump >= 60 && swim >= 60 && total >= 200'),
        wrong=[("забывает проверить сумму: 60 + 60 + 79 проходит отбор",
                _sport('run >= 60 && jump >= 60 && swim >= 60')),
               ("забывает проверить плавание",
                _sport('run >= 60 && jump >= 60 && total >= 200'))],
        constructs=["if"],
    ),
]
