"""PY_ELIF — «Цепочки elif». Taught before: if/else, comparisons, and, or/not, f-strings, arithmetic, strings.
Not yet: loops, lists, functions."""
from build import OutputTask

SKILL = "PY_ELIF"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-elif-rt-fuel-gauge", title="Датчик топлива",
        given=["fuel"],
        variants=[{"fuel": "64"}, {"fuel": "95"}, {"fuel": "7"}],
        hidden=[{"fuel": "80"}, {"fuel": "79"}, {"fuel": "30"}, {"fuel": "10"}, {"fuel": "9"}],
        intro="Датчик в машине показывает, насколько заполнен бензобак. Уровень топлива в процентах записан "
              "в переменной `fuel = {fuel}`.",
        steps=["Если `fuel` равен `80` или больше, выведи `Full`.",
               "Иначе, если `fuel` равен `30` или больше, выведи `Half`.",
               "Иначе, если `fuel` равен `10` или больше, выведи `Low`.",
               "Во всех остальных случаях выведи `Refuel now`."],
        hint="Проверяй пороги сверху вниз, от 80 к 10, и используй `>=`: при ровно 30 процентах датчик уже показывает `Half`. "
             "Как только одно условие сработало, остальные ветки цепочки не проверяются.",
        solution='if fuel >= 80:\n    print("Full")\nelif fuel >= 30:\n    print("Half")\n'
                 'elif fuel >= 10:\n    print("Low")\nelse:\n    print("Refuel now")',
        wrong=[("строгие сравнения: при ровно 80 процентах не «Full»",
                'if fuel > 80:\n    print("Full")\nelif fuel > 30:\n    print("Half")\n'
                'elif fuel > 10:\n    print("Low")\nelse:\n    print("Refuel now")'),
               ("пороги снизу вверх: всё от 10 процентов становится «Low»",
                'if fuel >= 10:\n    print("Low")\nelif fuel >= 30:\n    print("Half")\n'
                'elif fuel >= 80:\n    print("Full")\nelse:\n    print("Refuel now")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-elif-rt-coffee-size", title="Размер кофе",
        given=["size"],
        variants=[{"size": '"medium"'}, {"size": '"small"'}, {"size": '"huge"'}],
        hidden=[{"size": '"large"'}, {"size": '"small"'}, {"size": '"medium"'}, {"size": '"tiny"'}],
        intro="Кофейный автомат спрашивает размер стакана и показывает объём и цену. "
              "Выбранный размер записан строкой: `size = {size}`.",
        steps=['Если `size` равен `"small"`, выведи две строки: `Volume: 250 ml` и `Price: 120 rub`.',
               'Иначе, если `size` равен `"medium"`, выведи `Volume: 350 ml` и `Price: 160 rub`.',
               'Иначе, если `size` равен `"large"`, выведи `Volume: 450 ml` и `Price: 200 rub`.',
               "Во всех остальных случаях выведи одну строку `No such size`."],
        hint="Строки сравниваются через `==`, а значение пишется в кавычках: `size == \"small\"`. "
             "В каждой из трёх первых веток два `print` с одинаковым отступом.",
        solution='if size == "small":\n    print("Volume: 250 ml")\n    print("Price: 120 rub")\n'
                 'elif size == "medium":\n    print("Volume: 350 ml")\n    print("Price: 160 rub")\n'
                 'elif size == "large":\n    print("Volume: 450 ml")\n    print("Price: 200 rub")\n'
                 'else:\n    print("No such size")',
        wrong=[("цены у среднего и большого стакана перепутаны",
                'if size == "small":\n    print("Volume: 250 ml")\n    print("Price: 120 rub")\n'
                'elif size == "medium":\n    print("Volume: 350 ml")\n    print("Price: 200 rub")\n'
                'elif size == "large":\n    print("Volume: 450 ml")\n    print("Price: 160 rub")\n'
                'else:\n    print("No such size")'),
               ("нет ветки else: на неизвестный размер ничего не печатает",
                'if size == "small":\n    print("Volume: 250 ml")\n    print("Price: 120 rub")\n'
                'elif size == "medium":\n    print("Volume: 350 ml")\n    print("Price: 160 rub")\n'
                'elif size == "large":\n    print("Volume: 450 ml")\n    print("Price: 200 rub")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-elif-rt-late-lab", title="Лабораторная со штрафом",
        given=["score", "days_late"],
        variants=[{"score": "95", "days_late": "2"}, {"score": "92", "days_late": "0"},
                  {"score": "70", "days_late": "3"}],
        hidden=[{"score": "85", "days_late": "0"}, {"score": "84", "days_late": "0"}, {"score": "100", "days_late": "1"},
                {"score": "100", "days_late": "8"}, {"score": "60", "days_late": "2"}, {"score": "72", "days_late": "1"}, {"score": "40", "days_late": "0"}],
        intro="Преподаватель проверяет лабораторную работу. За неё набрано `score = {score}` баллов, "
              "а сдана она с опозданием на `days_late = {days_late}` дней. За каждый день опоздания снимают 5 баллов.",
        steps=["Посчитай итоговые баллы: `score` минус 5, умноженное на `days_late`.",
               "Выбери оценку цепочкой условий. Если опоздание больше `7` дней, оценка `2` — работу не принимают. "
               "Иначе, если итоговых баллов `85` или больше **и** опоздания нет совсем, оценка `5`.",
               "Иначе, если итоговых баллов `70` или больше, оценка `4`. Иначе, если `50` или больше, оценка `3`. "
               "Во всех остальных случаях оценка `2`.",
               "Выведи две строки: итоговые баллы в формате `Points: 85` и оценку в формате `Grade: 4`"],
        hint="Сначала сохрани итоговые баллы в переменную, потом в каждой ветке цепочки запиши оценку в другую переменную "
             "и выведи обе строки после цепочки. Опоздание «совсем нет» — это `days_late == 0`: "
             "работа на 95 баллов, сданная на 2 дня позже, получит только 4.",
        solution='points = score - days_late * 5\n'
                 'if days_late > 7:\n    grade = 2\nelif points >= 85 and days_late == 0:\n    grade = 5\n'
                 'elif points >= 70:\n    grade = 4\nelif points >= 50:\n    grade = 3\nelse:\n    grade = 2\n'
                 'print(f"Points: {points}")\nprint(f"Grade: {grade}")',
        wrong=[("не проверяет опоздание для пятёрки",
                'points = score - days_late * 5\n'
                'if days_late > 7:\n    grade = 2\nelif points >= 85:\n    grade = 5\n'
                'elif points >= 70:\n    grade = 4\nelif points >= 50:\n    grade = 3\nelse:\n    grade = 2\n'
                'print(f"Points: {points}")\nprint(f"Grade: {grade}")'),
               ("забыто правило про опоздание больше недели",
                'points = score - days_late * 5\n'
                'if points >= 85 and days_late == 0:\n    grade = 5\n'
                'elif points >= 70:\n    grade = 4\nelif points >= 50:\n    grade = 3\nelse:\n    grade = 2\n'
                'print(f"Points: {points}")\nprint(f"Grade: {grade}")'),
               ("оценку ставит по баллам без штрафа",
                'points = score - days_late * 5\n'
                'if days_late > 7:\n    grade = 2\nelif score >= 85 and days_late == 0:\n    grade = 5\n'
                'elif score >= 70:\n    grade = 4\nelif score >= 50:\n    grade = 3\nelse:\n    grade = 2\n'
                'print(f"Points: {points}")\nprint(f"Grade: {grade}")')],
        constructs=["if"],
    ),
]
