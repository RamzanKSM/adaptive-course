"""PY_TUPLE_BASIC — «Кортежи». Taught before: everything up to list operations (conditions, loops, lists and their
methods, slices, string methods, functions, classes). Here: creating a tuple, indexing, unpacking (also in a for header),
immutability and list()/tuple(). Not yet: sets, dicts, comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_TUPLE_BASIC"

ROBOT = """\
position = start
highest = start
for dx, dy in moves:
    x, y = position
    position = (x + dx, y + dy)
    print(position)
    if position[1] > highest[1]:
        highest = position
print(f"Highest point: {highest}")
if position == start:
    print("Back at start")
else:
    print("Not at start")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-tup-rt-alarm-time", title="Время будильника",
        given=["alarm"],
        variants=[{"alarm": "(7, 30)"}, {"alarm": "(12, 0)"}, {"alarm": "(9, 5)"}],
        hidden=[{"alarm": "(0, 0)"}, {"alarm": "(11, 59)"}, {"alarm": "(23, 45)"}, {"alarm": "(12, 1)"}],
        intro="Будильник хранит время звонка в кортеже `alarm` из двух чисел: сначала часы (от 0 до 23), потом минуты. "
              "Нужно вывести время звонка, посчитать, сколько минут прошло с полуночи, и понять, до полудня "
              "звонок или после.",
        steps=["Распакуй кортеж `alarm` одной строкой в две переменные: `hours` и `minutes` — именно в таком порядке "
               "числа стоят в кортеже.",
               "Выведи строку вида `Alarm: 7 h 30 min`.",
               "Следующей строкой выведи строку вида `Minutes since midnight: 450` — часы, умноженные на 60, плюс минуты.",
               "Последней строкой выведи `Before noon`, если часов меньше 12, иначе `After noon`."],
        hint="После `a, b = (5, 9)` в `a` окажется 5, а в `b` — 9: элементы раскладываются по порядку. "
             "Ровно в 12 часов полдень уже наступил, поэтому 12 h 0 min — это `After noon`.",
        solution='hours, minutes = alarm\nprint(f"Alarm: {hours} h {minutes} min")\n'
                 'print(f"Minutes since midnight: {hours * 60 + minutes}")\n'
                 'if hours < 12:\n    print("Before noon")\nelse:\n    print("After noon")',
        wrong=[("распаковывает в обратном порядке — часы и минуты меняются местами",
                'minutes, hours = alarm\nprint(f"Alarm: {hours} h {minutes} min")\n'
                'print(f"Minutes since midnight: {hours * 60 + minutes}")\n'
                'if hours < 12:\n    print("Before noon")\nelse:\n    print("After noon")'),
               ("считает 12 часов ещё утром",
                'hours, minutes = alarm\nprint(f"Alarm: {hours} h {minutes} min")\n'
                'print(f"Minutes since midnight: {hours * 60 + minutes}")\n'
                'if hours <= 12:\n    print("Before noon")\nelse:\n    print("After noon")')],
        must_use=[("re:(?m)^\\s*\\(?\\s*\\w+\\s*,\\s*\\w+\\s*\\)?\\s*=[^=]",
                   "Достань часы и минуты распаковкой кортежа — одной строкой вида a, b = кортеж.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-tup-rt-train-stops", title="Остановки электрички",
        given=["stops", "start", "end"],
        variants=[{"stops": '("Moscow", "Khimki", "Kryukovo", "Solnechnogorsk", "Klin", "Tver")',
                   "start": '"Khimki"', "end": '"Klin"'},
                  {"stops": '("Kazan", "Zelenodolsk", "Sviyazhsk", "Kanash")', "start": '"Kazan"', "end": '"Sviyazhsk"'},
                  {"stops": '("Sochi", "Khosta", "Adler", "Sirius", "Esto-Sadok")', "start": '"Adler"',
                   "end": '"Esto-Sadok"'}],
        hidden=[{"stops": '("Omsk", "Tara")', "start": '"Omsk"', "end": '"Tara"'},
                {"stops": '("Perm", "Kungur", "Chusovoy", "Lysva", "Gubakha", "Kizel", "Chernushka")',
                 "start": '"Chusovoy"', "end": '"Chernushka"'},
                {"stops": '("Tula", "Shchekino", "Plavsk", "Chern", "Mtsensk")', "start": '"Tula"', "end": '"Shchekino"'}],
        intro="Маршрут электрички записан в кортеже `stops` — станции стоят в порядке движения поезда, и в программе их "
              "никто не должен поменять. Пассажир садится на станции `start` и выходит на станции `end`, которая "
              "стоит дальше по маршруту.",
        steps=["Найди методом `.index()` место станции `start` и место станции `end` в кортеже `stops`.",
               "Возьми срезом кусок маршрута от `start` до `end` включительно — получится тоже кортеж — "
               "и выведи его через `print`.",
               "Выведи строку вида `Stations to ride: 4` — на сколько станций пассажир проедет вперёд: разницу "
               "между местами `end` и `start`."],
        hint="У кортежа, как и у списка, есть `.index()`, обращение по индексу и срезы — нельзя только менять элементы. "
             "Срез `[a:b]` не включает элемент с индексом `b`, поэтому, чтобы конечная станция попала в срез, "
             "правую границу нужно взять на 1 больше.",
        solution='first = stops.index(start)\nlast = stops.index(end)\nprint(stops[first:last + 1])\n'
                 'print(f"Stations to ride: {last - first}")',
        wrong=[("срез без +1 — конечная станция не попадает в маршрут",
                'first = stops.index(start)\nlast = stops.index(end)\nprint(stops[first:last])\n'
                'print(f"Stations to ride: {last - first}")'),
               ("считает станции вместе с начальной — ответ на одну больше",
                'first = stops.index(start)\nlast = stops.index(end)\nprint(stops[first:last + 1])\n'
                'print(f"Stations to ride: {last - first + 1}")')],
        must_use=[("re:\\.index\\(", "Найди места станций в кортеже методом .index()."),
                  ("re:\\[[^\\]]*:[^\\]]*\\]", "Возьми кусок маршрута срезом кортежа.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-tup-rt-robot-path", title="Путь робота",
        given=["start", "moves"],
        variants=[{"start": "(0, 0)", "moves": "[(1, 2), (2, 1), (0, -3), (-3, 0)]"},
                  {"start": "(2, -1)", "moves": "[(0, 3), (1, -1), (-1, 3), (2, 0)]"},
                  {"start": "(-1, 4)", "moves": "[(1, -2), (2, 0), (-3, -1)]"}],
        hidden=[{"start": "(0, 0)", "moves": "[(0, -1), (0, 1)]"},
                {"start": "(5, 5)", "moves": "[(1, 1), (1, -1), (-2, 0)]"},
                {"start": "(-2, -3)", "moves": "[(1, 1), (1, 1)]"},
                {"start": "(1, 1)", "moves": "[(2, 3), (1, 0), (-3, -4)]"}],
        intro="Робот-пылесос ездит по клетчатому полу. Его начальная клетка — кортеж `start` из двух чисел `(x, y)`. "
              "Ходы записаны в список `moves`: каждый ход — кортеж `(dx, dy)`, на сколько клеток робот сдвигается "
              "по x и по y. Нужно проследить путь робота, найти самую верхнюю клетку, где он побывал, и проверить, "
              "вернулся ли он туда, откуда начал.",
        steps=["Положение робота храни в кортеже `position`, вначале это `start`. Самой верхней клеткой `highest` "
               "вначале тоже считай `start`.",
               "Пройди циклом по `moves`, распаковывая каждый ход прямо в заголовке цикла в `dx, dy`. Кортеж изменить "
               "нельзя, поэтому на каждом ходе распакуй `position` в `x, y` и собери новый кортеж `(x + dx, y + dy)`. "
               "Выведи его через `print`.",
               "Если y новой клетки строго больше, чем y клетки `highest`, запомни новую клетку как `highest`. "
               "При равной высоте остаётся клетка, где робот был раньше.",
               "После цикла выведи строку вида `Highest point: (3, 3)`, а затем `Back at start`, если итоговая клетка "
               "совпадает со `start`, иначе `Not at start`."],
        hint="Кортежи сравниваются через `==` поэлементно: `(1, 2) == (1, 2)` — это `True`. Высота клетки — второй "
             "элемент кортежа, индекс 1. Начальная клетка тоже считается: робот мог только спускаться, и тогда "
             "самая верхняя клетка — стартовая.",
        solution=ROBOT,
        wrong=[("при равной высоте запоминает более позднюю клетку",
                ROBOT.replace("    if position[1] > highest[1]:", "    if position[1] >= highest[1]:")),
               ("начинает поиск самой верхней клетки с (0, 0), а не со стартовой",
                ROBOT.replace("highest = start\n", "highest = (0, 0)\n")),
               ("сравнивает клетки по x, а не по y",
                ROBOT.replace("    if position[1] > highest[1]:", "    if position[0] > highest[0]:"))],
        constructs=["for"],
        must_use=[("re:(?m)^\\s*for\\s+\\(?\\s*\\w+\\s*,\\s*\\w+\\s*\\)?\\s*in\\b",
                   "Распакуй каждый ход прямо в заголовке цикла: for dx, dy in moves.")],
    ),
]
