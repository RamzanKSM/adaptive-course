"""PY_LOGICAL_OR — «Логическое or и not». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, f-strings, if/else, comparison operators, and.
Not yet: elif, truthiness of non-bool values, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_LOGICAL_OR"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-or-rt-traffic-light", title="Светофор",
        given=["light"],
        variants=[{"light": '"red"'}, {"light": '"green"'}, {"light": '"yellow"'}],
        hidden=[{"light": '"green"'}, {"light": '"yellow"'}, {"light": '"red"'}, {"light": '"green"'}],
        intro="Беспилотный автомобиль подъехал к перекрёстку и смотрит на светофор. "
              "Цвет сигнала записан строкой с маленькой буквы: `light = {light}`.",
        steps=['Если `light` равен `"red"` **или** `light` равен `"yellow"`, выведи `Stop`.',
               "Иначе выведи `Go`.",
               "Объедини обе проверки в одном условии с помощью `or`."],
        hint="Каждая часть условия с `or` — это отдельное полное сравнение: `light == ... or light == ...`. "
             "Запись `light == \"red\" or \"yellow\"` не работает так, как кажется: такое условие истинно всегда.",
        solution='if light == "red" or light == "yellow":\n    print("Stop")\nelse:\n    print("Go")',
        wrong=[("сравнение только слева от or: условие всегда истинно",
                'if light == "red" or "yellow":\n    print("Stop")\nelse:\n    print("Go")'),
               ("and вместо or: сигнал не бывает сразу красным и жёлтым",
                'if light == "red" and light == "yellow":\n    print("Stop")\nelse:\n    print("Go")')],
        constructs=["if"],
        must_use=[("Or", "Используй or, чтобы объединить обе проверки в одном условии")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-or-rt-car-start", title="Можно ли ехать",
        given=["belt_on", "door_open"],
        variants=[{"belt_on": "True", "door_open": "False"}, {"belt_on": "False", "door_open": "False"},
                  {"belt_on": "True", "door_open": "True"}],
        hidden=[{"belt_on": "False", "door_open": "True"}, {"belt_on": "True", "door_open": "False"},
                {"belt_on": "True", "door_open": "True"}, {"belt_on": "False", "door_open": "False"}],
        intro="Бортовой компьютер машины не даёт тронуться, пока не пристёгнут ремень или пока открыта дверь. "
              "Пристёгнут ли ремень, записано в `belt_on = {belt_on}`, а открыта ли дверь — в `door_open = {door_open}`.",
        steps=["Если ремень **не** пристёгнут **или** дверь открыта, выведи `Check the car`.",
               "Иначе выведи `Ready to drive`.",
               "Запиши условие с помощью `not` и `or`."],
        hint="«Ремень не пристёгнут» — это `not belt_on`. А вот про дверь переменная уже говорит «открыта», "
             "поэтому перед `door_open` слово `not` не нужно. Помешать поездке может любая из двух причин.",
        solution='if not belt_on or door_open:\n    print("Check the car")\nelse:\n    print("Ready to drive")',
        wrong=[("not и перед дверью: машина едет с открытой дверью",
                'if not belt_on or not door_open:\n    print("Check the car")\nelse:\n    print("Ready to drive")'),
               ("and вместо or: не пускает, только когда обе причины сразу",
                'if not belt_on and door_open:\n    print("Check the car")\nelse:\n    print("Ready to drive")')],
        constructs=["if"],
        must_use=[("Not", "Используй not, чтобы проверить, что ремень не пристёгнут"),
                  ("Or", "Используй or: чтобы не тронуться, достаточно одной из двух причин")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-or-rt-parcel-oversize", title="Негабаритная посылка",
        given=["weight", "length"],
        variants=[{"weight": "8", "length": "130"}, {"weight": "12", "length": "80"}, {"weight": "25", "length": "60"}],
        hidden=[{"weight": "20", "length": "100"}, {"weight": "21", "length": "50"}, {"weight": "5", "length": "101"},
                {"weight": "30", "length": "150"}, {"weight": "1", "length": "10"}],
        intro="Почта берёт за посылку 50 руб. за каждый килограмм. Если посылка тяжелее 20 кг или длиннее 100 см, "
              "она считается негабаритной, и к цене добавляют ещё 500 руб. "
              "Посылка весит `weight = {weight}` кг, её длина — `length = {length}` см.",
        steps=["Если `weight` больше 20 **или** `length` больше 100, доплата за негабарит — 500 руб. Иначе доплаты нет: 0 руб.",
               "Выведи первой строкой доплату в формате `Oversize fee: 500 rub`",
               "Второй строкой выведи полную цену — `weight`, умноженный на 50, плюс доплата — в формате `Total: 900 rub`"],
        hint="Для доплаты хватает одного из двух условий. Проверь границы: посылка ровно 20 кг и ровно 100 см ещё обычная, "
             "поэтому сравнения строгие. Сохрани доплату в переменную в обеих ветках, а потом выведи обе строки.",
        solution='if weight > 20 or length > 100:\n    fee = 500\nelse:\n    fee = 0\n'
                 'print(f"Oversize fee: {fee} rub")\nprint(f"Total: {weight * 50 + fee} rub")',
        wrong=[("нестрогие сравнения: посылка ровно 20 кг или ровно 100 см считается негабаритной",
                'if weight >= 20 or length >= 100:\n    fee = 500\nelse:\n    fee = 0\n'
                'print(f"Oversize fee: {fee} rub")\nprint(f"Total: {weight * 50 + fee} rub")'),
               ("and вместо or: доплата, только когда посылка и тяжёлая, и длинная",
                'if weight > 20 and length > 100:\n    fee = 500\nelse:\n    fee = 0\n'
                'print(f"Oversize fee: {fee} rub")\nprint(f"Total: {weight * 50 + fee} rub")')],
        constructs=["if"],
        must_use=[("Or", "Используй or: посылка негабаритная, если выполняется хотя бы одно из двух условий")],
    ),
]
