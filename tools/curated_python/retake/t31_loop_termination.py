"""PY_LOOP_TERMINATION — «Завершение цикла»: while-циклы, которые обязаны остановиться. Taught before: print,
variables, arithmetic, strings, type conversion, // and %, += -=, f-strings, if/elif/else, comparisons, and/or/not,
truthiness, for + range, accumulator, while, break/continue.
Not yet: lists, string slicing and methods, functions."""
from build import OutputTask

SKILL = "PY_LOOP_TERMINATION"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lt-rt-candle", title="Догорающая свеча",
        given=["length", "burn"],
        variants=[{"length": "12", "burn": "4"}, {"length": "10", "burn": "3"}, {"length": "15", "burn": "6"}],
        hidden=[{"length": "8", "burn": "2"}, {"length": "5", "burn": "5"}, {"length": "7", "burn": "3"},
                {"length": "3", "burn": "4"}],
        intro="Свеча длиной `length = {length}` см горит, и за каждый час становится короче на `burn = {burn}` см. "
              "Нужно записывать её длину, пока свеча ещё не догорела.",
        steps=["Напиши цикл `while`, который работает, пока `length` больше 0.",
               "В цикле сначала выведи строку вида `Candle: 12 cm`, а потом уменьши `length` на `burn`.",
               "После цикла выведи `Burned out`"],
        hint="Цикл `while` останавливается, только когда его условие становится ложным. "
             "Если `length` внутри цикла не уменьшается, условие никогда не изменится и цикл будет крутиться бесконечно. "
             "Свеча длиной 0 см уже догорела — её длину не выводят.",
        solution='while length > 0:\n    print(f"Candle: {length} cm")\n    length -= burn\nprint("Burned out")',
        wrong=[("условие >= 0: когда свеча сгорела ровно до нуля, выводится «Candle: 0 cm»",
                'while length >= 0:\n    print(f"Candle: {length} cm")\n    length -= burn\nprint("Burned out")'),
               ("уменьшает длину до вывода: первая строка теряется, а в конце бывает минус",
                'while length > 0:\n    length -= burn\n    print(f"Candle: {length} cm")\nprint("Burned out")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lt-rt-two-trains", title="Встреча двух поездов",
        given=["dist", "speed1", "speed2"],
        variants=[{"dist": "300", "speed1": "60", "speed2": "40"}, {"dist": "450", "speed1": "80", "speed2": "70"},
                  {"dist": "200", "speed1": "50", "speed2": "30"}],
        hidden=[{"dist": "100", "speed1": "50", "speed2": "50"}, {"dist": "101", "speed1": "50", "speed2": "50"},
                {"dist": "90", "speed1": "70", "speed2": "60"}, {"dist": "500", "speed1": "45", "speed2": "55"}],
        intro="Два поезда выехали навстречу друг другу из городов, между которыми `dist = {dist}` км. Первый проезжает "
              "`speed1 = {speed1}` км в час, второй — `speed2 = {speed2}` км в час. Диспетчер каждый час записывает, "
              "сколько километров осталось между поездами, пока они не встретятся.",
        steps=["Заведи счётчик часов `hours`, который сначала равен 0.",
               "Пока `dist` больше 0, повторяй: увеличь `hours` на 1 и уменьши `dist` на сумму скоростей. "
               "Если `dist` стало меньше 0, сделай его равным 0 — поезда уже встретились.",
               "В конце каждого часа выведи строку вида `Hour 1: 200 km`",
               "После цикла выведи строку вида `Met after: 3 h`"],
        hint="За час поезда сближаются на `speed1 + speed2` км. Обнулять отрицательное расстояние нужно до вывода, "
             "иначе в последней строке появится минус. Цикл остановится, когда `dist` станет 0.",
        solution='hours = 0\nwhile dist > 0:\n    hours += 1\n    dist -= speed1 + speed2\n    if dist < 0:\n        dist = 0\n'
                 '    print(f"Hour {hours}: {dist} km")\nprint(f"Met after: {hours} h")',
        wrong=[("не обнуляет расстояние: в последней строке бывает минус",
                'hours = 0\nwhile dist > 0:\n    hours += 1\n    dist -= speed1 + speed2\n'
                '    print(f"Hour {hours}: {dist} km")\nprint(f"Met after: {hours} h")'),
               ("вычитает только скорость первого поезда",
                'hours = 0\nwhile dist > 0:\n    hours += 1\n    dist -= speed1\n    if dist < 0:\n        dist = 0\n'
                '    print(f"Hour {hours}: {dist} km")\nprint(f"Met after: {hours} h")'),
               ("печатает расстояние до того, как поезда проехали час",
                'hours = 0\nwhile dist > 0:\n    hours += 1\n    print(f"Hour {hours}: {dist} km")\n'
                '    dist -= speed1 + speed2\n    if dist < 0:\n        dist = 0\n'
                'print(f"Met after: {hours} h")')],
        constructs=["while", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lt-rt-guess-number", title="Угадай число",
        given=["secret", "top"],
        variants=[{"secret": "37", "top": "100"}, {"secret": "80", "top": "100"}, {"secret": "5", "top": "20"}],
        hidden=[{"secret": "1", "top": "100"}, {"secret": "100", "top": "100"}, {"secret": "50", "top": "100"},
                {"secret": "13", "top": "16"}],
        intro="Компьютер угадывает задуманное число от 1 до `top = {top}`. Задумано `secret = {secret}`. Компьютер каждый "
              "раз называет середину отрезка, где ещё может быть число, и по ответу «больше» или «меньше» "
              "отбрасывает половину. Так отрезок всё время сужается, и цикл обязательно закончится.",
        steps=["Заведи переменные `low = 1` и `high = top` — границы отрезка — и счётчик попыток `tries = 0`.",
               "Пока `low` не больше `high`, повторяй: увеличь `tries` на 1 и посчитай середину `guess` — "
               "`low` плюс `high`, делённое нацело на 2.",
               "Если `guess` равно `secret`, выведи строку вида `Try 3: 37 - correct` и выйди из цикла через `break`.",
               "Иначе, если `guess` меньше `secret`, выведи строку вида `Try 2: 25 - too small` и сдвинь `low` на `guess + 1`. "
               "Иначе выведи строку вида `Try 1: 50 - too big` и сдвинь `high` на `guess - 1`.",
               "После цикла выведи строку вида `Tries: 3`"],
        hint="Сдвигать границу нужно за `guess`, а не на сам `guess`: иначе отрезок может перестать сужаться, "
             "и цикл станет бесконечным. Делить нужно нацело, через `//`, — середина отрезка должна быть целым числом.",
        solution='low = 1\nhigh = top\ntries = 0\nwhile low <= high:\n    tries += 1\n    guess = (low + high) // 2\n'
                 '    if guess == secret:\n        print(f"Try {tries}: {guess} - correct")\n        break\n'
                 '    elif guess < secret:\n        print(f"Try {tries}: {guess} - too small")\n        low = guess + 1\n'
                 '    else:\n        print(f"Try {tries}: {guess} - too big")\n        high = guess - 1\n'
                 'print(f"Tries: {tries}")',
        wrong=[("границы сдвигаются не в ту сторону",
                'low = 1\nhigh = top\ntries = 0\nwhile low <= high:\n    tries += 1\n    guess = (low + high) // 2\n'
                '    if guess == secret:\n        print(f"Try {tries}: {guess} - correct")\n        break\n'
                '    elif guess < secret:\n        print(f"Try {tries}: {guess} - too small")\n        high = guess - 1\n'
                '    else:\n        print(f"Try {tries}: {guess} - too big")\n        low = guess + 1\n'
                'print(f"Tries: {tries}")'),
               ("делит через /: середина получается дробной",
                'low = 1\nhigh = top\ntries = 0\nwhile low <= high:\n    tries += 1\n    guess = (low + high) / 2\n'
                '    if guess == secret:\n        print(f"Try {tries}: {guess} - correct")\n        break\n'
                '    elif guess < secret:\n        print(f"Try {tries}: {guess} - too small")\n        low = guess + 1\n'
                '    else:\n        print(f"Try {tries}: {guess} - too big")\n        high = guess - 1\n'
                'print(f"Tries: {tries}")'),
               ("нет break: после угадывания цикл продолжается",
                'low = 1\nhigh = top\ntries = 0\nwhile low <= high and tries < 20:\n    tries += 1\n    guess = (low + high) // 2\n'
                '    if guess == secret:\n        print(f"Try {tries}: {guess} - correct")\n'
                '    elif guess < secret:\n        print(f"Try {tries}: {guess} - too small")\n        low = guess + 1\n'
                '    else:\n        print(f"Try {tries}: {guess} - too big")\n        high = guess - 1\n'
                'print(f"Tries: {tries}")')],
        constructs=["while", "if"],
    ),
]
