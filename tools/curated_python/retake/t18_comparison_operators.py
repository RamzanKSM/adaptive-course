"""PY_COMPARISON_OPERATORS — «Операторы сравнения». Taught before: print, variables, arithmetic, int/float, strings,
type conversion, // and %, += -=, f-strings, if/else.
Not yet: and/or/not, elif, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_COMPARISON_OPERATORS"
CMP = [("Compare", "Используй операторы сравнения: ==, !=, <, >, <=, >=")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-cmp-rt-ride-height", title="Ростомер у аттракциона",
        given=["height", "record"],
        variants=[{"height": "132", "record": "150"}, {"height": "118", "record": "118"}, {"height": "155", "record": "149"}],
        hidden=[{"height": "120", "record": "130"}, {"height": "140", "record": "140"}, {"height": "119", "record": "100"},
                {"height": "139", "record": "141"}],
        intro="У входа на американские горки стоит ростомер. Рост ребёнка — `height = {height}` см. Кататься можно "
              "с роста 120 см, а детям ниже 140 см нужен взрослый рядом. Ещё ростомер помнит самый большой рост за день: "
              "`record = {record}` см.",
        steps=["Выведи через `print` с запятой `Can ride:` и результат сравнения: рост 120 или больше.",
               "Выведи `With adult:` и результат сравнения: рост меньше 140.",
               "Выведи `New record:` и результат сравнения: рост больше, чем `record`.",
               "Выведи `Same as record:` и результат сравнения: рост равен `record`.",
               "Например, для роста 140 и рекорда 140 программа выводит `Can ride: True`, `With adult: False`, "
               "`New record: False`, `Same as record: True`."],
        hint="Сравнение — это значение `True` или `False`, его можно сразу напечатать: `print(\"Tall:\", height > 150)`. "
             "«120 или больше» — это `>=`, а «меньше 140» — строгое `<`: ровно 140 см — уже без взрослого. "
             "Равенство проверяют двойным `==`.",
        solution='print("Can ride:", height >= 120)\nprint("With adult:", height < 140)\nprint("New record:", height > record)\n'
                 'print("Same as record:", height == record)',
        wrong=[("строгое сравнение: ровно 120 см не пускают",
                'print("Can ride:", height > 120)\nprint("With adult:", height < 140)\nprint("New record:", height > record)\n'
                'print("Same as record:", height == record)'),
               ("<= вместо <: ребёнку ростом ровно 140 см будто нужен взрослый",
                'print("Can ride:", height >= 120)\nprint("With adult:", height <= 140)\nprint("New record:", height > record)\n'
                'print("Same as record:", height == record)'),
               (">= вместо >: повтор рекорда считается новым рекордом",
                'print("Can ride:", height >= 120)\nprint("With adult:", height < 140)\nprint("New record:", height >= record)\n'
                'print("Same as record:", height == record)')],
        must_use=CMP,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-cmp-rt-door-code", title="Кодовый замок",
        given=["code", "entered"],
        variants=[{"code": "4719", "entered": "4719"}, {"code": "2580", "entered": "2850"}, {"code": "1306", "entered": "1036"}],
        hidden=[{"code": "1111", "entered": "1112"}, {"code": "9000", "entered": "9000"}, {"code": "5005", "entered": "5004"},
                {"code": "123", "entered": "1230"}],
        intro="Кодовый замок на двери подъезда хранит код `code = {code}`. Житель набрал `entered = {entered}`. "
              "Для мастера, который настраивает замок, табло показывает ещё и подсказку: набранное число больше кода или нет.",
        steps=["Выведи через `print` с запятой `Correct:` и результат сравнения: равен ли `entered` коду.",
               "Выведи `Bigger:` и результат сравнения: больше ли `entered`, чем `code`.",
               "Если `entered` не равен `code` (оператор `!=`), выведи `Wrong code`, иначе выведи `Door is open`.",
               "Например, для кода 1111 и набранного 1112 программа выводит `Correct: False`, `Bigger: True`, `Wrong code`."],
        hint="Оператор `!=` значит «не равно»: `5 != 3` даёт `True`, а `5 != 5` — `False`. "
             "В условии `if entered != code:` первая ветка срабатывает, когда код набран неверно.",
        solution='print("Correct:", entered == code)\nprint("Bigger:", entered > code)\nif entered != code:\n'
                 '    print("Wrong code")\nelse:\n    print("Door is open")',
        wrong=[("ветки перепутаны: дверь открывается при неверном коде",
                'print("Correct:", entered == code)\nprint("Bigger:", entered > code)\nif entered != code:\n'
                '    print("Door is open")\nelse:\n    print("Wrong code")'),
               ("знак перевёрнут: Bigger показывает, что набранное меньше кода",
                'print("Correct:", entered == code)\nprint("Bigger:", entered < code)\nif entered != code:\n'
                '    print("Wrong code")\nelse:\n    print("Door is open")'),
               ("!= вместо == в первой строке",
                'print("Correct:", entered != code)\nprint("Bigger:", entered > code)\nif entered != code:\n'
                '    print("Wrong code")\nelse:\n    print("Door is open")')],
        constructs=["if"],
        must_use=CMP,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-cmp-rt-phone-plan", title="Минуты сверх тарифа",
        given=["used", "limit", "fee", "extra_price"],
        variants=[{"used": "640", "limit": "500", "fee": "450", "extra_price": "3"},
                  {"used": "320", "limit": "400", "fee": "390", "extra_price": "2"},
                  {"used": "1000", "limit": "1000", "fee": "700", "extra_price": "4"}],
        hidden=[{"used": "501", "limit": "500", "fee": "450", "extra_price": "3"},
                {"used": "0", "limit": "300", "fee": "250", "extra_price": "5"},
                {"used": "900", "limit": "600", "fee": "500", "extra_price": "1"},
                {"used": "300", "limit": "300", "fee": "100", "extra_price": "9"}],
        intro="Мобильный тариф стоит `fee = {fee}` руб. в месяц и включает `limit = {limit}` минут. Каждая минута "
              "сверх пакета стоит `extra_price = {extra_price}` руб. В этом месяце Тимур проговорил `used = {used}` минут.",
        steps=["С помощью f-строк выведи `Minutes: <used> of <limit>` и `Over limit: <True/False>` — результат сравнения "
               "«`used` больше, чем `limit`».",
               "Если `used` больше `limit`: посчитай лишние минуты `extra` (`used - limit`) и их стоимость `extra_cost` "
               "(`extra * extra_price`) и выведи `Extra: <extra> min, <extra_cost> rub` и `To pay: <fee + extra_cost> rub`.",
               "Иначе выведи `Minutes left: <limit - used>` и `To pay: <fee> rub`.",
               "Например, для 501 минуты при пакете 500, тарифе 450 руб. и цене минуты 3 руб. программа выводит "
               "`Minutes: 501 of 500`, `Over limit: True`, `Extra: 1 min, 3 rub` и `To pay: 453 rub`."],
        hint="Ровно `limit` минут — это ещё не перерасход: «больше» — это `>`, а не `>=`. Сравнение можно вставить "
             "прямо в f-строку: `f\"Over limit: {{used > limit}}\"`. Лишние минуты — это `used - limit`, а не все минуты.",
        solution='print(f"Minutes: {used} of {limit}")\nprint(f"Over limit: {used > limit}")\nif used > limit:\n'
                 '    extra = used - limit\n    extra_cost = extra * extra_price\n'
                 '    print(f"Extra: {extra} min, {extra_cost} rub")\n    print(f"To pay: {fee + extra_cost} rub")\n'
                 'else:\n    print(f"Minutes left: {limit - used}")\n    print(f"To pay: {fee} rub")',
        wrong=[(">= вместо >: при ровно исчерпанном пакете считает перерасход 0 минут",
                'print(f"Minutes: {used} of {limit}")\nprint(f"Over limit: {used > limit}")\nif used >= limit:\n'
                '    extra = used - limit\n    extra_cost = extra * extra_price\n'
                '    print(f"Extra: {extra} min, {extra_cost} rub")\n    print(f"To pay: {fee + extra_cost} rub")\n'
                'else:\n    print(f"Minutes left: {limit - used}")\n    print(f"To pay: {fee} rub")'),
               ("берёт за лишние все минуты, а не только сверх пакета",
                'print(f"Minutes: {used} of {limit}")\nprint(f"Over limit: {used > limit}")\nif used > limit:\n'
                '    extra = used\n    extra_cost = extra * extra_price\n'
                '    print(f"Extra: {extra} min, {extra_cost} rub")\n    print(f"To pay: {fee + extra_cost} rub")\n'
                'else:\n    print(f"Minutes left: {limit - used}")\n    print(f"To pay: {fee} rub")'),
               ("знак перевёрнут в условии",
                'print(f"Minutes: {used} of {limit}")\nprint(f"Over limit: {used > limit}")\nif used < limit:\n'
                '    extra = used - limit\n    extra_cost = extra * extra_price\n'
                '    print(f"Extra: {extra} min, {extra_cost} rub")\n    print(f"To pay: {fee + extra_cost} rub")\n'
                'else:\n    print(f"Minutes left: {limit - used}")\n    print(f"To pay: {fee} rub")')],
        constructs=["if"],
        must_use=CMP,
    ),
]
