"""PY_LOOP_TERMINATION — «Завершение цикла»: while-циклы, которые обязаны остановиться. Taught before: print,
variables, arithmetic, strings, type conversion, // and %, += -=, f-strings, if/elif/else, comparisons, and/or/not,
truthiness, for + range, accumulator, while, break/continue.
Not yet: lists, string slicing and methods, functions."""
from build import OutputTask

SKILL = "PY_LOOP_TERMINATION"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lt-water-tank", title="Бак с водой",
        given=["water", "leak"],
        variants=[{"water": "10", "leak": "3"}, {"water": "12", "leak": "4"}, {"water": "9", "leak": "2"}],
        hidden=[{"water": "6", "leak": "2"}, {"water": "5", "leak": "5"}, {"water": "7", "leak": "3"},
                {"water": "2", "leak": "4"}],
        intro="В баке `water = {water}` л воды, и каждую минуту из него вытекает `leak = {leak}` л. "
              "Нужно следить за баком, пока в нём есть вода.",
        steps=["Напиши цикл `while`, который работает, пока `water` больше 0.",
               "В цикле сначала выведи строку вида `Water left: 15 l`, а потом уменьши `water` на `leak`.",
               "После цикла выведи `Tank is empty`."],
        hint="Цикл `while` останавливается, только когда его условие становится ложным. "
             "Если `water` внутри цикла не уменьшается, условие никогда не изменится и цикл будет крутиться бесконечно.",
        solution='while water > 0:\n    print(f"Water left: {water} l")\n    water -= leak\nprint("Tank is empty")',
        wrong=[("условие >= 0: когда вода вытекла ровно до нуля, выводится «Water left: 0 l»",
                'while water >= 0:\n    print(f"Water left: {water} l")\n    water -= leak\nprint("Tank is empty")'),
               ("уменьшает воду до вывода: первая строка теряется, а в конце бывает минус",
                'while water > 0:\n    water -= leak\n    print(f"Water left: {water} l")\nprint("Tank is empty")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lt-bacteria", title="Колония бактерий",
        given=["count", "limit"],
        variants=[{"count": "3", "limit": "50"}, {"count": "5", "limit": "100"}, {"count": "7", "limit": "30"}],
        hidden=[{"count": "3", "limit": "48"}, {"count": "1", "limit": "10"}, {"count": "10", "limit": "20"},
                {"count": "6", "limit": "1000"}],
        intro="Сколько бактерий сейчас в пробирке, записано в `count = {count}`. Каждый час их становится в 2 раза больше. "
              "Учёному нужно знать, через сколько часов бактерий станет не меньше `limit = {limit}`.",
        steps=["Заведи счётчик часов, который сначала равен 0.",
               "Пока бактерий меньше `limit`, удваивай `count` и прибавляй к счётчику часов 1.",
               "После цикла выведи одной строкой число часов и итоговое число бактерий в формате "
               "`Hours: 2, bacteria: 40`"],
        hint="Условие `while` проверяется перед каждым повтором. Когда бактерий стало ровно `limit`, "
             "их уже достаточно — удваивать ещё раз не нужно. Выбери знак сравнения, который это учитывает.",
        solution='hours = 0\nwhile count < limit:\n    count = count * 2\n    hours += 1\n'
                 'print(f"Hours: {hours}, bacteria: {count}")',
        wrong=[("условие <=: когда бактерий ровно limit, удваивает лишний раз",
                'hours = 0\nwhile count <= limit:\n    count = count * 2\n    hours += 1\n'
                'print(f"Hours: {hours}, bacteria: {count}")'),
               ("счётчик часов начинается с 1",
                'hours = 1\nwhile count < limit:\n    count = count * 2\n    hours += 1\n'
                'print(f"Hours: {hours}, bacteria: {count}")')],
        constructs=["while"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lt-snail", title="Улитка на столбе",
        given=["height", "up", "down"],
        variants=[{"height": "10", "up": "4", "down": "1"}, {"height": "12", "up": "5", "down": "3"},
                  {"height": "20", "up": "7", "down": "4"}],
        hidden=[{"height": "9", "up": "3", "down": "1"}, {"height": "5", "up": "6", "down": "2"},
                {"height": "30", "up": "6", "down": "1"}, {"height": "16", "up": "4", "down": "2"}],
        intro="Улитка ползёт вверх по столбу высотой `height = {height}` м. За день она поднимается на `up = {up}` м, "
              "а за ночь сползает на `down = {down}` м. Если днём улитка добралась до верха, она уже наверху "
              "и ночью не сползает.",
        steps=["Заведи две переменные: номер дня и высоту, на которой сейчас улитка. Обе сначала равны 0.",
               "В цикле `while` повторяй сутки: номер дня увеличивается на 1, улитка поднимается на `up`. "
               "Если теперь она на высоте `height` или выше, цикл должен закончиться, "
               "а если нет — ночью она сползает на `down`.",
               "После цикла выведи номер дня, когда улитка добралась до верха, в формате "
               "`The snail gets out on day 9`"],
        hint="Проверять, добралась ли улитка до верха, нужно сразу после дневного подъёма — до того, как она сползёт ночью. "
             "Удобно написать `while True:` и выйти из цикла через `break`, когда высота стала не меньше `height`.",
        solution='day = 0\npos = 0\nwhile True:\n    day += 1\n    pos += up\n    if pos >= height:\n        break\n'
                 '    pos -= down\nprint(f"The snail gets out on day {day}")',
        wrong=[("сползание вычитается до проверки: улитка «сползает» даже с вершины",
                'day = 0\npos = 0\nwhile pos < height:\n    day += 1\n    pos = pos + up - down\n'
                'print(f"The snail gets out on day {day}")'),
               ("строгое сравнение: улитка ровно на вершине не считается выбравшейся",
                'day = 0\npos = 0\nwhile True:\n    day += 1\n    pos += up\n    if pos > height:\n        break\n'
                '    pos -= down\nprint(f"The snail gets out on day {day}")')],
        constructs=["while"],
    ),
]
