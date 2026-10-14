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
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-or-aquarium", title="Вода в аквариуме",
        given=["temp"],
        variants=[{"temp": "25"}, {"temp": "19"}, {"temp": "31"}],
        hidden=[{"temp": "22"}, {"temp": "28"}, {"temp": "21"}, {"temp": "29"}],
        intro="Рыбкам в аквариуме хорошо, когда вода от 22 до 28 градусов. Датчик показывает температуру воды: `temp = {temp}`.",
        steps=["Если `temp` меньше 22 **или** `temp` больше 28, выведи `Check the heater`.",
               "Иначе выведи `Water OK`.",
               "Объедини обе проверки в одном условии с помощью `or`."],
        hint="Вода плохая, если она слишком холодная или слишком горячая — хватает одного из двух. "
             "Ровно 22 и ровно 28 градусов — ещё нормально, поэтому сравнения здесь строгие: `<` и `>`.",
        solution='if temp < 22 or temp > 28:\n    print("Check the heater")\nelse:\n    print("Water OK")',
        wrong=[("and вместо or: вода не бывает сразу холоднее 22 и горячее 28",
                'if temp < 22 and temp > 28:\n    print("Check the heater")\nelse:\n    print("Water OK")'),
               ("нестрогие сравнения: ровно 22 и 28 градусов считаются плохими",
                'if temp <= 22 or temp >= 28:\n    print("Check the heater")\nelse:\n    print("Water OK")')],
        constructs=["if"],
        must_use=[("Or", "Используй or, чтобы объединить обе проверки в одном условии")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-or-not-update", title="Обновление телефона",
        given=["on_wifi", "battery"],
        variants=[{"on_wifi": "True", "battery": "80"}, {"on_wifi": "False", "battery": "90"},
                  {"on_wifi": "True", "battery": "12"}],
        hidden=[{"on_wifi": "True", "battery": "30"}, {"on_wifi": "True", "battery": "29"},
                {"on_wifi": "False", "battery": "10"}, {"on_wifi": "False", "battery": "50"}],
        intro="Телефон ставит обновление, только когда он подключён к Wi-Fi и заряжен хотя бы на 30 процентов. "
              "Подключён ли он к Wi-Fi, записано в `on_wifi = {on_wifi}`, а заряд в процентах — в `battery = {battery}`.",
        steps=["Если телефон **не** подключён к Wi-Fi **или** заряд меньше 30, выведи `Update later`.",
               "Иначе выведи `Updating`.",
               "Запиши условие с помощью `not` и `or`."],
        hint="«Не подключён к Wi-Fi» — это `not on_wifi`. Отложить обновление можно из-за любой из двух причин, "
             "поэтому части условия соединяет `or`. При заряде ровно 30 обновление уже можно ставить.",
        solution='if not on_wifi or battery < 30:\n    print("Update later")\nelse:\n    print("Updating")',
        wrong=[("забыт not: обновляется без Wi-Fi и откладывает с Wi-Fi",
                'if on_wifi or battery < 30:\n    print("Update later")\nelse:\n    print("Updating")'),
               ("and вместо or: откладывает, только когда нет ни Wi-Fi, ни заряда",
                'if not on_wifi and battery < 30:\n    print("Update later")\nelse:\n    print("Updating")')],
        constructs=["if"],
        must_use=[("Not", "Используй not, чтобы проверить, что телефон не подключён к Wi-Fi"),
                  ("Or", "Используй or: чтобы отложить обновление, достаточно одной из двух причин")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-or-night-taxi", title="Ночной тариф такси",
        given=["hour", "km"],
        variants=[{"hour": "23", "km": "12"}, {"hour": "14", "km": "8"}, {"hour": "3", "km": "20"}],
        hidden=[{"hour": "6", "km": "10"}, {"hour": "5", "km": "4"}, {"hour": "22", "km": "15"},
                {"hour": "0", "km": "7"}, {"hour": "23", "km": "5"}],
        intro="Такси берёт 30 руб. за километр, а ночью — вдвое больше, 60 руб. Ночью считается время с 23 часов "
              "и до 6 часов утра. Поездка началась в `hour = {hour}` часов (от 0 до 23), её длина — `km = {km}` км.",
        steps=["Если `hour` меньше 6 **или** `hour` равен 23 или больше, цена за километр — 60 руб. Иначе — 30 руб.",
               "Выведи первой строкой цену за километр в формате `Rate: 30 rub/km`",
               "Второй строкой выведи стоимость поездки (километры, умноженные на цену) в формате `Total: 300 rub`"],
        hint="Ночь переходит через полночь, поэтому одним сравнением её не описать: это «поздний вечер» или «раннее утро». "
             "В 6 часов уже дневной тариф, а в 23 — уже ночной. Сохрани цену за километр в переменную в обеих ветках.",
        solution='if hour < 6 or hour >= 23:\n    rate = 60\nelse:\n    rate = 30\n'
                 'print(f"Rate: {rate} rub/km")\nprint(f"Total: {km * rate} rub")',
        wrong=[("and вместо or: ночного тарифа не бывает никогда",
                'if hour < 6 and hour >= 23:\n    rate = 60\nelse:\n    rate = 30\n'
                'print(f"Rate: {rate} rub/km")\nprint(f"Total: {km * rate} rub")'),
               ("строгое сравнение: в 23 часа ещё дневной тариф",
                'if hour < 6 or hour > 23:\n    rate = 60\nelse:\n    rate = 30\n'
                'print(f"Rate: {rate} rub/km")\nprint(f"Total: {km * rate} rub")')],
        constructs=["if"],
        must_use=[("Or", "Используй or: ночь — это или поздний вечер, или раннее утро")],
    ),
]
