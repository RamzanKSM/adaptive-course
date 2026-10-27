"""IF_ELSE_BASIC — «Условия if / else» (Java). Taught before: println, variables, assignment, arithmetic, primitive
types, strings, / and %, += -=. Comparisons in a condition are part of this topic (the course's diagnostic uses them)."""
from java_tasks import JavaOutputTask

SKILL = "IF_ELSE_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-if-rt-library-book", title="Книга из библиотеки",
        given=[("int", "days")],
        variants=[{"days": "10"}, {"days": "21"}, {"days": "3"}],
        hidden=[{"days": "14"}, {"days": "15"}, {"days": "1"}, {"days": "30"}],
        intro="Книгу из школьной библиотеки можно держать дома не больше 14 дней. Сколько дней книга уже у читателя, "
              "записано в поле `days`.",
        steps=["Если `days` больше `14`, выведи `Return the book`.",
               "Иначе выведи `Keep reading`."],
        hint="«Больше» в Java — это `>`. На 14-й день книгу ещё можно читать, возвращать пора только с 15-го.",
        solution='if (days > 14) {\n    System.out.println("Return the book");\n} else {\n    System.out.println("Keep reading");\n}',
        wrong=[("нестрогое сравнение: на 14-й день уже требует вернуть",
                'if (days >= 14) {\n    System.out.println("Return the book");\n} else {\n    System.out.println("Keep reading");\n}'),
               ("ветки перепутаны",
                'if (days > 14) {\n    System.out.println("Keep reading");\n} else {\n    System.out.println("Return the book");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-if-rt-digital-clock", title="Электронные часы",
        given=[("int", "minutes")],
        variants=[{"minutes": "545"}, {"minutes": "754"}, {"minutes": "1263"}],
        hidden=[{"minutes": "0"}, {"minutes": "600"}, {"minutes": "609"}, {"minutes": "610"}, {"minutes": "1439"}],
        intro="Электронные часы хранят время как число минут, прошедших с полуночи, — оно записано в поле `minutes`. "
              "На экране время нужно показать в привычном виде: часы, двоеточие и всегда две цифры минут.",
        steps=["Часы — это `minutes / 60`, а минуты на экране — остаток `minutes % 60`.",
               "Если минут на экране меньше `10`, выведи `Time: `, часы, двоеточие, `0` и минуты, например `Time: 9:05`.",
               "Иначе выведи `Time: `, часы, двоеточие и минуты, например `Time: 12:34`."],
        hint="Без лишнего нуля время 9 часов 5 минут выглядит как `9:5`. Поэтому в одной ветке после двоеточия "
             "допиши строку `\"0\"`, а в другой — нет.",
        solution='int h = minutes / 60;\nint m = minutes % 60;\nif (m < 10) {\n    System.out.println("Time: " + h + ":0" + m);\n} else {\n'
                 '    System.out.println("Time: " + h + ":" + m);\n}',
        wrong=[("не дописывает ноль: 9 часов 5 минут печатает как 9:5",
                'int h = minutes / 60;\nint m = minutes % 60;\nSystem.out.println("Time: " + h + ":" + m);'),
               ("нестрогое сравнение: 10 минут печатает как 010",
                'int h = minutes / 60;\nint m = minutes % 60;\nif (m <= 10) {\n    System.out.println("Time: " + h + ":0" + m);\n} else {\n'
                '    System.out.println("Time: " + h + ":" + m);\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-if-rt-elevator-load", title="Перегруз в лифте",
        given=[("int", "people"), ("int", "weight")],
        variants=[{"people": "4", "weight": "85"}, {"people": "6", "weight": "80"}, {"people": "5", "weight": "70"}],
        hidden=[{"people": "5", "weight": "80"}, {"people": "1", "weight": "401"}, {"people": "0", "weight": "75"},
                {"people": "10", "weight": "75"}],
        intro="Лифт поднимает не больше 400 кг. В кабину зашли `people` человек, каждый весит примерно `weight` кг — "
              "оба числа записаны в поля.",
        steps=["Посчитай общий вес: `people`, умноженное на `weight`, и выведи его в формате `Load: 340 kg`.",
               "Если общий вес меньше или равен `400`, выведи `Going up`, а следующей строкой — `Reserve: N kg`, "
               "где N — сколько килограммов ещё можно добавить до 400.",
               "Иначе выведи `Overload`, а следующей строкой — `Remove: N kg`, где N — на сколько общий вес больше 400."],
        hint="Сохрани общий вес в переменную `int` до `if`. Запас — это 400 минус вес, а лишнее — вес минус 400. "
             "При весе ровно 400 кг лифт едет, и запас равен 0.",
        solution='int load = people * weight;\nSystem.out.println("Load: " + load + " kg");\nif (load <= 400) {\n'
                 '    System.out.println("Going up");\n    System.out.println("Reserve: " + (400 - load) + " kg");\n} else {\n'
                 '    System.out.println("Overload");\n    System.out.println("Remove: " + (load - 400) + " kg");\n}',
        wrong=[("строгое сравнение: при ровно 400 кг пишет про перегруз",
                'int load = people * weight;\nSystem.out.println("Load: " + load + " kg");\nif (load < 400) {\n'
                '    System.out.println("Going up");\n    System.out.println("Reserve: " + (400 - load) + " kg");\n} else {\n'
                '    System.out.println("Overload");\n    System.out.println("Remove: " + (load - 400) + " kg");\n}'),
               ("при перегрузе вычитает в обратном порядке: лишний вес выходит отрицательным",
                'int load = people * weight;\nSystem.out.println("Load: " + load + " kg");\nif (load <= 400) {\n'
                '    System.out.println("Going up");\n    System.out.println("Reserve: " + (400 - load) + " kg");\n} else {\n'
                '    System.out.println("Overload");\n    System.out.println("Remove: " + (400 - load) + " kg");\n}')],
        constructs=["if"],
    ),
]
