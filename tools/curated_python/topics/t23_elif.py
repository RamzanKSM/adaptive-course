"""PY_ELIF — «Цепочки elif». Taught before: if/else, comparisons, and, or/not, f-strings, arithmetic, strings.
Not yet: loops, lists, functions."""
from build import OutputTask

SKILL = "PY_ELIF"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-elif-test-grade", title="Оценка за тест",
        given=["score"],
        variants=[{"score": "87"}, {"score": "93"}, {"score": "61"}],
        hidden=[{"score": "90"}, {"score": "75"}, {"score": "50"}, {"score": "49"}, {"score": "100"}],
        intro="За тест можно набрать от 0 до 100 баллов. Результат ученика записан в переменной `score = {score}`. Программа должна сказать, какая это оценка.",
        steps=["Если баллов `90` или больше, выведи `отлично`.",
               "Иначе, если баллов `75` или больше, выведи `хорошо`.",
               "Иначе, если баллов `50` или больше, выведи `удовлетворительно`.",
               "Во всех остальных случаях выведи `неудовлетворительно`."],
        hint="Проверяй пороги сверху вниз: от самого высокого к самому низкому. Как только одно условие сработало, "
             "остальные ветки `elif` и `else` уже не проверяются.",
        solution='if score >= 90:\n    print("отлично")\nelif score >= 75:\n    print("хорошо")\n'
                 'elif score >= 50:\n    print("удовлетворительно")\nelse:\n    print("неудовлетворительно")',
        wrong=[("строгие сравнения: ровно 90 баллов уже не «отлично»",
                'if score > 90:\n    print("отлично")\nelif score > 75:\n    print("хорошо")\n'
                'elif score > 50:\n    print("удовлетворительно")\nelse:\n    print("неудовлетворительно")'),
               ("пороги снизу вверх: всё от 50 и выше становится «удовлетворительно»",
                'if score >= 50:\n    print("удовлетворительно")\nelif score >= 75:\n    print("хорошо")\n'
                'elif score >= 90:\n    print("отлично")\nelse:\n    print("неудовлетворительно")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-elif-clothes", title="Что надеть на улицу",
        given=["temperature"],
        variants=[{"temperature": "-5"}, {"temperature": "10"}, {"temperature": "28"}],
        hidden=[{"temperature": "0"}, {"temperature": "15"}, {"temperature": "25"}, {"temperature": "-20"}, {"temperature": "19"}],
        intro="Утром программа смотрит на температуру за окном — `temperature = {temperature}` градусов — и подсказывает, как одеться.",
        steps=["Если температура ниже `0`, выведи `Надень пуховик`.",
               "Иначе, если ниже `15`, выведи `Надень куртку`.",
               "Иначе, если ниже `25`, выведи `Хватит свитера`.",
               "Иначе выведи `Можно в футболке`."],
        hint="«Ниже 15» — это `temperature < 15`. Ровно 15 градусов уже не ниже 15, поэтому при 15 программа "
             "должна перейти к следующей проверке.",
        solution='if temperature < 0:\n    print("Надень пуховик")\nelif temperature < 15:\n    print("Надень куртку")\n'
                 'elif temperature < 25:\n    print("Хватит свитера")\nelse:\n    print("Можно в футболке")',
        wrong=[("нестрогие сравнения: при 0 градусов советует пуховик",
                'if temperature <= 0:\n    print("Надень пуховик")\nelif temperature <= 15:\n    print("Надень куртку")\n'
                'elif temperature <= 25:\n    print("Хватит свитера")\nelse:\n    print("Можно в футболке")'),
               ("отдельные if вместо цепочки: при морозе печатает несколько советов",
                'if temperature < 0:\n    print("Надень пуховик")\nif temperature < 15:\n    print("Надень куртку")\n'
                'if temperature < 25:\n    print("Хватит свитера")\nelse:\n    print("Можно в футболке")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-elif-ticket-price", title="Цена билета в музей",
        given=["age", "is_student"],
        variants=[{"age": "5", "is_student": "False"}, {"age": "20", "is_student": "True"}, {"age": "70", "is_student": "False"}],
        hidden=[{"age": "30", "is_student": "False"}, {"age": "16", "is_student": "False"}, {"age": "7", "is_student": "False"},
                {"age": "65", "is_student": "True"}, {"age": "18", "is_student": "False"}, {"age": "3", "is_student": "False"}],
        intro="В музее цена билета зависит от возраста посетителя и от того, учится ли он: `age = {age}`, `is_student = {is_student}`.",
        steps=["Если посетителю меньше `7` лет, билет стоит `0` рублей.",
               "Иначе, если ему меньше `18` лет **или** он студент, билет стоит `150` рублей.",
               "Иначе, если ему `65` лет или больше, билет стоит `100` рублей.",
               "Во всех остальных случаях билет стоит `300` рублей. Выведи цену в виде `Цена билета: 150` — "
               "после двоеточия пробел, потом число."],
        hint="Условия проверяются по порядку, и срабатывает первое подходящее. Поэтому студенту 65 лет "
             "достанется цена из второго правила, а не из третьего.",
        solution='if age < 7:\n    price = 0\nelif age < 18 or is_student:\n    price = 150\n'
                 'elif age >= 65:\n    price = 100\nelse:\n    price = 300\nprint(f"Цена билета: {price}")',
        wrong=[("and вместо or: школьник без студенческого платит как взрослый",
                'if age < 7:\n    price = 0\nelif age < 18 and is_student:\n    price = 150\n'
                'elif age >= 65:\n    price = 100\nelse:\n    price = 300\nprint(f"Цена билета: {price}")'),
               ("забыт порог для детей до 7 лет",
                'if age < 18 or is_student:\n    price = 150\n'
                'elif age >= 65:\n    price = 100\nelse:\n    price = 300\nprint(f"Цена билета: {price}")')],
        constructs=["if"],
    ),
]
