"""PY_IF_ELSE_BASIC — «Условия if / else». Taught before: print, variables, arithmetic, int/float, strings, type
conversion, // and %, += -=, f-strings. Simple comparisons (>, >=, ==) come together with the condition itself.
Not yet: elif, and/or/not, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_IF_ELSE_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-if-rt-kettle", title="Закипел ли чайник",
        given=["temp"],
        variants=[{"temp": "72"}, {"temp": "100"}, {"temp": "45"}],
        hidden=[{"temp": "99"}, {"temp": "100"}, {"temp": "18"}, {"temp": "0"}],
        intro="Умный чайник показывает температуру воды. Вода кипит, когда нагрелась до 100 градусов. "
              "Текущая температура записана в переменной: `temp = {temp}`.",
        steps=["Если `temp` равна 100 или больше, выведи `Water is boiling`.",
               "Иначе выведи `Please wait`.",
               "Программа должна вывести ровно одну строку."],
        hint="«100 или больше» — это `temp >= 100`: при ровно 100 градусах вода уже кипит. "
             "После условия и после `else` ставится двоеточие, а `print` внутри веток пишется с отступом.",
        solution='if temp >= 100:\n    print("Water is boiling")\nelse:\n    print("Please wait")',
        wrong=[("строгое сравнение: при ровно 100 градусах всё ещё ждёт",
                'if temp > 100:\n    print("Water is boiling")\nelse:\n    print("Please wait")'),
               ("ветки перепутаны местами",
                'if temp >= 100:\n    print("Please wait")\nelse:\n    print("Water is boiling")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-if-rt-party-pizza", title="Пицца на праздник",
        given=["guests"],
        variants=[{"guests": "20"}, {"guests": "32"}, {"guests": "13"}],
        hidden=[{"guests": "8"}, {"guests": "7"}, {"guests": "1"}, {"guests": "100"}, {"guests": "41"}],
        intro="На праздник заказывают пиццу. Каждую пиццу режут на 8 кусков, и каждому гостю достаётся ровно один кусок. "
              "Сколько гостей придёт, записано в `guests = {guests}`.",
        steps=["Проверь, делится ли `guests` на 8 без остатка.",
               "Если делится, выведи число пицц (`guests`, делённое на 8 нацело) в формате `Pizzas: 3`, "
               "а второй строкой — `No slices left`.",
               "Иначе пицц нужно на одну больше, чем `guests // 8`, чтобы хватило всем. Выведи их число в том же "
               "формате, а второй строкой — сколько кусков останется лишними, в формате `Slices left: 4`."],
        hint="Остаток `guests % 8` — это гости, которым достались куски последней пиццы: при 20 гостях это `4`. "
             "Значит, в последней пицце лишних кусков `8 - guests % 8`.",
        solution='if guests % 8 == 0:\n    print(f"Pizzas: {guests // 8}")\n    print("No slices left")\n'
                 'else:\n    print(f"Pizzas: {guests // 8 + 1}")\n    print(f"Slices left: {8 - guests % 8}")',
        wrong=[("не добавляет последнюю неполную пиццу",
                'if guests % 8 == 0:\n    print(f"Pizzas: {guests // 8}")\n    print("No slices left")\n'
                'else:\n    print(f"Pizzas: {guests // 8}")\n    print(f"Slices left: {8 - guests % 8}")'),
               ("лишними считает куски, которые съедят, а не оставшиеся",
                'if guests % 8 == 0:\n    print(f"Pizzas: {guests // 8}")\n    print("No slices left")\n'
                'else:\n    print(f"Pizzas: {guests // 8 + 1}")\n    print(f"Slices left: {guests % 8}")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-if-rt-step-goal", title="Цель по шагам",
        given=["steps", "goal"],
        variants=[{"steps": "7500", "goal": "10000"}, {"steps": "9300", "goal": "8000"},
                  {"steps": "3600", "goal": "6000"}],
        hidden=[{"steps": "8000", "goal": "8000"}, {"steps": "7999", "goal": "8000"}, {"steps": "0", "goal": "5000"},
                {"steps": "15000", "goal": "12000"}],
        intro="Фитнес-браслет считает шаги за день и сравнивает их с целью. Сегодня пройдено `steps = {steps}` шагов, "
              "а цель на день — `goal = {goal}` шагов.",
        steps=["Если `steps` равно `goal` или больше, цель выполнена и до неё осталось 0 шагов. "
               "Иначе осталось `goal` минус `steps` шагов.",
               "Посчитай процент выполнения: `steps`, умноженное на 100 и делённое на `goal` нацело.",
               "Выведи три строки: шаги и цель, процент и сколько шагов осталось. "
               "Например, для 7500 шагов при цели 10000 это `Steps: 7500 of 10000`, `Done: 75%` и `Left: 2500 steps`"],
        hint="Сохрани оставшиеся шаги в переменную: в `if` запиши в неё 0, а в `else` — разницу. "
             "Процент считай через `//`, иначе получится дробное число вроде `75.0`.",
        solution='if steps >= goal:\n    left = 0\nelse:\n    left = goal - steps\n'
                 'print(f"Steps: {steps} of {goal}")\nprint(f"Done: {steps * 100 // goal}%")\n'
                 'print(f"Left: {left} steps")',
        wrong=[("при перевыполнении вычитает всё равно: остаток уходит в минус",
                'left = goal - steps\n'
                'print(f"Steps: {steps} of {goal}")\nprint(f"Done: {steps * 100 // goal}%")\n'
                'print(f"Left: {left} steps")'),
               ("делит через / — процент получается дробным",
                'if steps >= goal:\n    left = 0\nelse:\n    left = goal - steps\n'
                'print(f"Steps: {steps} of {goal}")\nprint(f"Done: {steps * 100 / goal}%")\n'
                'print(f"Left: {left} steps")')],
        constructs=["if"],
    ),
]
