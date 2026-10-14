"""LOOP_TERMINATION — «Завершение цикла» (Java): while-циклы, которые обязаны остановиться — условие зависит от
переменной, которая меняется в цикле, и выход через break. Taught before: println, variables, arithmetic, primitive
types, String, / and %, += ++, if/else, comparisons, &&, ||, switch, for, accumulator, while.
Not yet: arrays, own methods. Every loop here (references and wrong solutions) stops for every value set."""
from java_tasks import JavaOutputTask

SKILL = "LOOP_TERMINATION"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-lt-pushup-ladder", title="Отжимания лесенкой",
        given=[("int", "reps"), ("int", "less")],
        variants=[{"reps": "15", "less": "4"}, {"reps": "25", "less": "6"}, {"reps": "18", "less": "7"}],
        hidden=[{"reps": "12", "less": "4"}, {"reps": "3", "less": "5"}, {"reps": "30", "less": "6"},
                {"reps": "10", "less": "3"}],
        intro="Тренер придумал упражнение «лесенкой»: в первом подходе нужно отжаться {reps} раз (поле `reps`), "
              "а в каждом следующем — на {less} меньше (поле `less`). Подходы продолжаются, пока в подходе "
              "остаётся хотя бы одно отжимание.",
        steps=["Напиши цикл `while`, который работает, пока `reps` больше 0.",
               "В цикле сначала выведи строку с числом отжиманий в подходе — первая будет `Push-ups in this set: {reps}`, — "
               "а потом уменьши `reps` на `less`.",
               "Когда цикл закончится, выведи `Workout is over`."],
        hint="Цикл `while` останавливается, только когда его условие становится ложным. Если внутри цикла не менять "
             "`reps`, условие `reps > 0` будет верным всегда, и цикл никогда не закончится.",
        solution='while (reps > 0) {\n    System.out.println("Push-ups in this set: " + reps);\n    reps -= less;\n}\n'
                 'System.out.println("Workout is over");',
        wrong=[("условие >= 0: когда отжимания кончаются ровно на нуле, печатается лишний подход из 0 отжиманий",
                'while (reps >= 0) {\n    System.out.println("Push-ups in this set: " + reps);\n    reps -= less;\n}\n'
                'System.out.println("Workout is over");'),
               ("уменьшает число до вывода: первый подход теряется, а в конце бывает минус",
                'while (reps > 0) {\n    reps -= less;\n    System.out.println("Push-ups in this set: " + reps);\n}\n'
                'System.out.println("Workout is over");')],
        constructs=["while"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-lt-bus-wait", title="Ждём автобус",
        given=[("int", "interval"), ("int", "arrive")],
        variants=[{"interval": "15", "arrive": "26"}, {"interval": "20", "arrive": "47"}, {"interval": "12", "arrive": "50"}],
        hidden=[{"interval": "10", "arrive": "30"}, {"interval": "25", "arrive": "0"}, {"interval": "7", "arrive": "50"},
                {"interval": "30", "arrive": "31"}],
        intro="Первый автобус отходит от остановки ровно в 8:00, а дальше автобусы уходят каждые {interval} мин. "
              "Ты пришёл на остановку через {arrive} мин. после 8:00. Интервал записан в поле `interval`, "
              "а время твоего прихода — в поле `arrive`.",
        steps=["Заведи переменную `bus` — через сколько минут после 8:00 уходит автобус. Сначала она равна 0: это первый автобус.",
               "Напиши цикл `while`: пока `bus` меньше `arrive`, этот автобус уже ушёл — прибавляй к `bus` значение "
               "`interval`, чтобы перейти к следующему. Если ты пришёл ровно к отправлению, ты на этот автобус успеваешь.",
               "После цикла выведи две строки в формате `Your bus: 30 min after 8:00` и `Wait: 4 min` — "
               "во второй строке столько минут, сколько пройдёт от твоего прихода до отправления."],
        hint="Каждый повтор цикла увеличивает `bus`, поэтому рано или поздно `bus` догонит `arrive` и цикл закончится. "
             "Подумай о знаке сравнения: когда `bus` равно `arrive`, автобус ещё стоит на остановке.",
        solution='int bus = 0;\nwhile (bus < arrive) {\n    bus += interval;\n}\n'
                 'System.out.println("Your bus: " + bus + " min after 8:00");\n'
                 'System.out.println("Wait: " + (bus - arrive) + " min");',
        wrong=[("условие <=: если пришёл ровно к отправлению, ждёт следующий автобус",
                'int bus = 0;\nwhile (bus <= arrive) {\n    bus += interval;\n}\n'
                'System.out.println("Your bus: " + bus + " min after 8:00");\n'
                'System.out.println("Wait: " + (bus - arrive) + " min");'),
               ("вычитает в обратном порядке: время ожидания получается отрицательным",
                'int bus = 0;\nwhile (bus < arrive) {\n    bus += interval;\n}\n'
                'System.out.println("Your bus: " + bus + " min after 8:00");\n'
                'System.out.println("Wait: " + (arrive - bus) + " min");')],
        constructs=["while"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-lt-scooter", title="Электросамокат до школы",
        given=[("int", "distance"), ("int", "charge"), ("int", "perKm")],
        variants=[{"distance": "8", "charge": "50", "perKm": "7"}, {"distance": "5", "charge": "60", "perKm": "9"},
                  {"distance": "12", "charge": "80", "perKm": "8"}],
        hidden=[{"distance": "6", "charge": "42", "perKm": "7"}, {"distance": "10", "charge": "35", "perKm": "4"},
                {"distance": "3", "charge": "100", "perKm": "10"}, {"distance": "15", "charge": "64", "perKm": "5"}],
        intro="Ты едешь в школу на электросамокате. До школы {distance} км (поле `distance`), батарея заряжена на {charge}% "
              "(поле `charge`), а каждый километр тратит {perKm}% заряда (поле `perKm`). Если заряда не хватает на "
              "следующий километр, самокат останавливается, и дальше придётся идти пешком.",
        steps=["Заведи счётчик `km` — сколько километров ты уже проехал. Сначала он равен 0.",
               "Напиши цикл `while`, который работает, пока `km` меньше `distance`. В начале каждого повтора проверь: "
               "если `charge` меньше `perKm`, на следующий километр заряда не хватит — выйди из цикла командой `break`. "
               "Иначе уменьши `charge` на `perKm` и увеличь `km` на 1.",
               "После цикла: если `km` равно `distance`, выведи `Made it to school! Charge: 15%`. Иначе выведи "
               "`The scooter died after 7 km`, а следующей строкой — `Left to walk: 1 km`. "
               "Числа в этих строках подставь из своего расчёта."],
        hint="У этого цикла два выхода: условие `km < distance` становится ложным, когда ты доехал, а `break` срабатывает, "
             "когда кончился заряд. Поэтому после цикла по значению `km` можно понять, каким из выходов он закончился.",
        solution='int km = 0;\nwhile (km < distance) {\n    if (charge < perKm) {\n        break;\n    }\n'
                 '    charge -= perKm;\n    km++;\n}\nif (km == distance) {\n'
                 '    System.out.println("Made it to school! Charge: " + charge + "%");\n} else {\n'
                 '    System.out.println("The scooter died after " + km + " km");\n'
                 '    System.out.println("Left to walk: " + (distance - km) + " km");\n}',
        wrong=[("сравнивает через <=: останавливается, даже когда заряда ровно на один километр",
                'int km = 0;\nwhile (km < distance) {\n    if (charge <= perKm) {\n        break;\n    }\n'
                '    charge -= perKm;\n    km++;\n}\nif (km == distance) {\n'
                '    System.out.println("Made it to school! Charge: " + charge + "%");\n} else {\n'
                '    System.out.println("The scooter died after " + km + " km");\n'
                '    System.out.println("Left to walk: " + (distance - km) + " km");\n}'),
               ("после цикла решает по заряду (charge > 0), а не по пройденным километрам",
                'int km = 0;\nwhile (km < distance) {\n    if (charge < perKm) {\n        break;\n    }\n'
                '    charge -= perKm;\n    km++;\n}\nif (charge > 0) {\n'
                '    System.out.println("Made it to school! Charge: " + charge + "%");\n} else {\n'
                '    System.out.println("The scooter died after " + km + " km");\n'
                '    System.out.println("Left to walk: " + (distance - km) + " km");\n}')],
        constructs=["while", "if"],
    ),
]
