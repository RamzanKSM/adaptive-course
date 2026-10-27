"""PY_WHILE_LOOP_BASIC — «Цикл while». Taught before: print, variables, assignment, arithmetic, int/float, strings,
type conversion, // and %, += -=, f-strings, if/else, comparisons, and/or/not, elif, truthiness, for + range,
accumulator. Here: a while loop that repeats while a condition holds, when the number of steps is not known in advance.
Not yet: break/continue, lists, string slicing and methods, functions."""
from build import OutputTask

SKILL = "PY_WHILE_LOOP_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-wh-rt-oven", title="Разогрев духовки",
        given=["temp", "rise"],
        variants=[{"temp": "20", "rise": "45"}, {"temp": "25", "rise": "30"}, {"temp": "60", "rise": "50"}],
        hidden=[{"temp": "180", "rise": "40"}, {"temp": "140", "rise": "40"}, {"temp": "22", "rise": "35"}],
        intro="Духовку включили, когда в ней было `temp = {temp}` градусов. Каждую минуту она нагревается ещё на "
              "`rise = {rise}` градусов. Ставить пирог можно, когда в духовке 180 градусов или больше.",
        steps=["Заведи счётчик минут `minute` со значением 0.",
               "Напиши цикл `while`, который повторяется, пока `temp` меньше 180.",
               "В цикле увеличь `minute` на 1, прибавь к `temp` значение `rise` и выведи строку вида `Minute 1: 65 C`",
               "После цикла выведи строку вида `Heating time: 4 min`"],
        hint="Цикл `while` проверяет условие перед каждым повтором. При ровно 180 градусах духовка уже готова, "
             "поэтому условие продолжения строгое: `temp < 180`. Если духовка уже горячая, цикл не выполнится ни разу.",
        solution='minute = 0\nwhile temp < 180:\n    minute += 1\n    temp += rise\n'
                 '    print(f"Minute {minute}: {temp} C")\nprint(f"Heating time: {minute} min")',
        wrong=[("нестрогое сравнение: при ровно 180 градусах греет ещё минуту",
                'minute = 0\nwhile temp <= 180:\n    minute += 1\n    temp += rise\n'
                '    print(f"Minute {minute}: {temp} C")\nprint(f"Heating time: {minute} min")'),
               ("печатает температуру до нагрева, а не после",
                'minute = 0\nwhile temp < 180:\n    minute += 1\n    print(f"Minute {minute}: {temp} C")\n'
                '    temp += rise\nprint(f"Heating time: {minute} min")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-wh-rt-candy-box", title="Коробка конфет на двоих",
        given=["candies", "a", "b"],
        variants=[{"candies": "20", "a": "3", "b": "4"}, {"candies": "15", "a": "2", "b": "5"},
                  {"candies": "10", "a": "4", "b": "4"}],
        hidden=[{"candies": "7", "a": "7", "b": "1"}, {"candies": "8", "a": "3", "b": "5"},
                {"candies": "9", "a": "3", "b": "5"}, {"candies": "12", "a": "1", "b": "2"}],
        intro="Аня и Борис едят конфеты из коробки, где лежит `candies = {candies}` штук. Они берут по очереди, "
              "первой — Аня: она за раз съедает `a = {a}` конфет, а Борис — `b = {b}`. Если в коробке осталось меньше, "
              "чем обычно берёт ребёнок, он съедает все оставшиеся. Узнаем, кому достанется последняя конфета.",
        steps=["Заведи счётчик ходов `turn = 0`.",
               "Пока в коробке есть конфеты (`candies` больше 0), повторяй в цикле `while`: увеличь `turn` на 1. "
               "Если `turn` нечётный, ходит Аня: запиши в `name` строку `\"Anya\"`, а в `take` — число `a`. "
               "Иначе ходит Борис: `name = \"Boris\"`, `take = b`.",
               "Там же, в цикле: если `take` больше `candies`, сделай `take` равным `candies`. Отними `take` от `candies` "
               "и выведи строку вида `Anya eats 3, left 17`",
               "После цикла в `name` осталось имя того, кто ходил последним. Выведи строку вида `Last candy: Boris`"],
        hint="Ход нечётный, когда `turn % 2 == 1`. Ребёнок не может съесть больше, чем лежит в коробке, — иначе "
             "конфет станет меньше нуля. Цикл остановится, когда `candies` станет ровно 0.",
        solution='turn = 0\nwhile candies > 0:\n    turn += 1\n    if turn % 2 == 1:\n'
                 '        name = "Anya"\n        take = a\n    else:\n        name = "Boris"\n        take = b\n'
                 '    if take > candies:\n        take = candies\n'
                 '    candies -= take\n    print(f"{name} eats {take}, left {candies}")\n'
                 'print(f"Last candy: {name}")',
        wrong=[("не ограничивает take: в коробке становится меньше нуля конфет",
                'turn = 0\nwhile candies > 0:\n    turn += 1\n    if turn % 2 == 1:\n'
                '        name = "Anya"\n        take = a\n    else:\n        name = "Boris"\n        take = b\n'
                '    candies -= take\n    print(f"{name} eats {take}, left {candies}")\n'
                'print(f"Last candy: {name}")'),
               ("первым ходит Борис",
                'turn = 0\nwhile candies > 0:\n    turn += 1\n    if turn % 2 == 0:\n'
                '        name = "Anya"\n        take = a\n    else:\n        name = "Boris"\n        take = b\n'
                '    if take > candies:\n        take = candies\n'
                '    candies -= take\n    print(f"{name} eats {take}, left {candies}")\n'
                'print(f"Last candy: {name}")'),
               ("печатает остаток до того, как отнять съеденное",
                'turn = 0\nwhile candies > 0:\n    turn += 1\n    if turn % 2 == 1:\n'
                '        name = "Anya"\n        take = a\n    else:\n        name = "Boris"\n        take = b\n'
                '    if take > candies:\n        take = candies\n'
                '    print(f"{name} eats {take}, left {candies}")\n    candies -= take\n'
                'print(f"Last candy: {name}")')],
        constructs=["while", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-wh-rt-hailstone", title="Числа-градины",
        given=["n"],
        variants=[{"n": "6"}, {"n": "7"}, {"n": "12"}],
        hidden=[{"n": "1"}, {"n": "16"}, {"n": "3"}, {"n": "9"}],
        intro="Есть забавная игра с числом `n = {n}`. Если число чётное, его делят пополам, а если нечётное — "
              "умножают на 3 и прибавляют 1. С новым числом делают то же самое, пока не получится 1. "
              "Число то растёт, то падает, как градина в туче. Узнаем, сколько шагов нужно и до какого "
              "наибольшего числа оно поднимется.",
        steps=["Заведи счётчик шагов `steps = 0` и переменную `top` — наибольшее число; сначала это само `n`.",
               "Пока `n` не равно 1, повторяй в цикле `while`: если `n` чётное, раздели его нацело на 2, "
               "иначе замени на `n * 3 + 1`. Затем увеличь `steps` на 1.",
               "Там же, в цикле: если новое `n` больше `top`, запиши его в `top`.",
               "После цикла выведи `Steps: 8` и следующей строкой `Top: 16`"],
        hint="Число чётное, когда `n % 2 == 0`. Делить нужно нацело, через `//`, иначе получится дробное число "
             "вроде `8.0`. Если `n` сразу равно 1, цикл не выполнится ни разу: шагов 0, а наибольшее число — 1.",
        solution='steps = 0\ntop = n\nwhile n != 1:\n    if n % 2 == 0:\n        n = n // 2\n    else:\n'
                 '        n = n * 3 + 1\n    steps += 1\n    if n > top:\n        top = n\n'
                 'print(f"Steps: {steps}")\nprint(f"Top: {top}")',
        wrong=[("делит через /: числа становятся дробными",
                'steps = 0\ntop = n\nwhile n != 1:\n    if n % 2 == 0:\n        n = n / 2\n    else:\n'
                '        n = n * 3 + 1\n    steps += 1\n    if n > top:\n        top = n\n'
                'print(f"Steps: {steps}")\nprint(f"Top: {top}")'),
               ("наибольшее начинается с 0: само n не учитывается",
                'steps = 0\ntop = 0\nwhile n != 1:\n    if n % 2 == 0:\n        n = n // 2\n    else:\n'
                '        n = n * 3 + 1\n    steps += 1\n    if n > top:\n        top = n\n'
                'print(f"Steps: {steps}")\nprint(f"Top: {top}")'),
               ("ветки перепутаны: чётное умножается, нечётное делится",
                'steps = 0\ntop = n\nwhile n > 1 and steps < 50:\n    if n % 2 == 1:\n        n = n // 2\n    else:\n'
                '        n = n * 3 + 1\n    steps += 1\n    if n > top:\n        top = n\n'
                'print(f"Steps: {steps}")\nprint(f"Top: {top}")')],
        constructs=["while", "if"],
    ),
]
