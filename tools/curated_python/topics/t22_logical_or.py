"""PY_LOGICAL_OR — «Логическое or и not». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, f-strings, if/else, comparison operators, and.
Not yet: elif, truthiness of non-bool values, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_LOGICAL_OR"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-or-weekend", title="Выходной или рабочий день",
        given=["day"],
        variants=[{"day": '"saturday"'}, {"day": '"wednesday"'}, {"day": '"sunday"'}],
        hidden=[{"day": '"monday"'}, {"day": '"sunday"'}, {"day": '"friday"'}, {"day": '"saturday"'}],
        intro="Умный будильник решает, можно ли сегодня поспать подольше. "
              "День недели записан строкой с маленькой буквы: `day = {day}`.",
        steps=['Если `day` равен `"saturday"` **или** `day` равен `"sunday"`, выведи `Day off`.',
               "Иначе выведи `Work day`.",
               "Объедини обе проверки в одном условии с помощью `or`."],
        hint="Каждая часть условия с `or` — это отдельное полное сравнение. "
             "Например, «x равно 1 или 2» записывается как `x == 1 or x == 2`, а не `x == 1 or 2`.",
        solution='if day == "saturday" or day == "sunday":\n    print("Day off")\nelse:\n    print("Work day")',
        wrong=[("сравнение только слева от or: условие всегда истинно",
                'if day == "saturday" or "sunday":\n    print("Day off")\nelse:\n    print("Work day")'),
               ("and вместо or: день не бывает сразу субботой и воскресеньем",
                'if day == "saturday" and day == "sunday":\n    print("Day off")\nelse:\n    print("Work day")')],
        constructs=["if"],
        must_use=[("Or", "Используй or, чтобы объединить обе проверки в одном условии")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-or-not-pool", title="Вход в бассейн",
        given=["has_cap", "has_note"],
        variants=[{"has_cap": "True", "has_note": "True"}, {"has_cap": "False", "has_note": "True"},
                  {"has_cap": "True", "has_note": "False"}],
        hidden=[{"has_cap": "False", "has_note": "False"}, {"has_cap": "True", "has_note": "True"},
                {"has_cap": "False", "has_note": "True"}, {"has_cap": "True", "has_note": "False"}],
        intro="В бассейн не пускают без шапочки или без справки от врача. "
              "Есть ли у посетителя шапочка, записано в `has_cap = {has_cap}`, а есть ли справка — в `has_note = {has_note}`.",
        steps=["Если шапочки нет **или** справки нет, выведи `No entry`.",
               "Иначе выведи `Come in`.",
               "Запиши условие с помощью `not` и `or`."],
        hint="`not` переворачивает значение: `not True` даёт `False`, а `not False` даёт `True`. "
             "Поэтому «шапочки нет» можно записать как `not has_cap`. Подумай, как так же записать «справки нет».",
        solution='if not has_cap or not has_note:\n    print("No entry")\nelse:\n    print("Come in")',
        wrong=[("and вместо or: не пускает, только когда нет ни шапочки, ни справки",
                'if not has_cap and not has_note:\n    print("No entry")\nelse:\n    print("Come in")'),
               ("not стоит только перед первой переменной",
                'if not has_cap or has_note:\n    print("No entry")\nelse:\n    print("Come in")')],
        constructs=["if"],
        must_use=[("Not", "Используй not, чтобы проверить, что шапочки или справки нет"),
                  ("Or", "Используй or: чтобы не пустить, достаточно, чтобы не хватало чего-то одного")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-or-cinema-discount", title="Билет в кино со скидкой",
        given=["age", "price"],
        variants=[{"age": "6", "price": "400"}, {"age": "35", "price": "350"}, {"age": "70", "price": "500"}],
        hidden=[{"age": "7", "price": "400"}, {"age": "65", "price": "300"}, {"age": "64", "price": "600"},
                {"age": "3", "price": "250"}],
        intro="В кинотеатре дети младше 7 лет и зрители от 65 лет и старше платят половину цены билета. "
              "Возраст зрителя — `age = {age}`, полная цена билета — `price = {price}` руб.",
        steps=["Если `age` меньше 7 **или** `age` равен 65 или больше, цена билета — половина `price`. "
               "Дели нацело через `//`, чтобы цена осталась целым числом.",
               "Иначе цена билета — полная `price`.",
               "Выведи цену одной строкой в формате `Ticket: 180 rub`"],
        hint="Проверь обе границы: зрителю ровно 7 лет скидка уже не положена, а зрителю ровно 65 лет — уже положена. "
             "Сначала сохрани цену в переменную в обеих ветках, а потом выведи её один раз через f-строку.",
        solution='if age < 7 or age >= 65:\n    cost = price // 2\nelse:\n    cost = price\nprint(f"Ticket: {cost} rub")',
        wrong=[("строгое сравнение: зрителю ровно 65 лет скидки нет",
                'if age < 7 or age > 65:\n    cost = price // 2\nelse:\n    cost = price\nprint(f"Ticket: {cost} rub")'),
               ("and вместо or: скидки нет ни у кого",
                'if age < 7 and age >= 65:\n    cost = price // 2\nelse:\n    cost = price\nprint(f"Ticket: {cost} rub")')],
        constructs=["if"],
        must_use=[("Or", "Используй or: скидка положена, если выполняется хотя бы одно из двух условий")],
    ),
]
