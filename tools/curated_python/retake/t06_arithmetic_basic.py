"""PY_ARITHMETIC_BASIC — «Арифметика». Taught before: print (several values, sep=, end=), variables, assignment.
Here: + - * /, the order of operations and parentheses, a result kept in a variable and used further.
Not yet: int/float in detail, // and %, += -=, type conversion, string concatenation, f-strings, conditions, loops."""
from build import OutputTask

SKILL = "PY_ARITHMETIC_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ar-rt-bike-trip", title="Велопрогулка",
        given=["speed", "hours", "done"],
        variants=[{"speed": "15", "hours": "2", "done": "12"}, {"speed": "12", "hours": "3", "done": "40"},
                  {"speed": "20", "hours": "1", "done": "5"}],
        hidden=[{"speed": "18", "hours": "2", "done": "30"}, {"speed": "10", "hours": "4", "done": "0"},
                {"speed": "25", "hours": "3", "done": "100"}],
        intro="Ребята катаются на велосипедах до озера и обратно. Едут они со скоростью `speed = {speed}` км/ч, "
              "дорога до озера занимает `hours = {hours}` ч, а `done = {done}` км уже проехали.",
        steps=["Посчитай `distance` — расстояние до озера: скорость, умноженная на часы.",
               "Посчитай `round_trip` — путь туда и обратно: `distance`, умноженное на 2.",
               "Посчитай `left` — сколько километров ещё осталось: `round_trip` минус `done`.",
               "Выведи три строки: `To the lake:`, `distance` и `km`; `Round trip:`, `round_trip` и `km`; "
               "`Left:`, `left` и `km`. Например: `Left: 7 km`."],
        hint="Результат вычисления сохраняй в переменную и используй дальше: `round_trip = distance * 2`. "
             "При вычитании важен порядок: из всего пути вычитай уже проеханное, а не наоборот.",
        solution='distance = speed * hours\nround_trip = distance * 2\nleft = round_trip - done\n'
                 'print("To the lake:", distance, "km")\nprint("Round trip:", round_trip, "km")\nprint("Left:", left, "km")',
        wrong=[("вычитает в обратном порядке — остаток отрицательный",
                'distance = speed * hours\nround_trip = distance * 2\nleft = done - round_trip\n'
                'print("To the lake:", distance, "km")\nprint("Round trip:", round_trip, "km")\nprint("Left:", left, "km")'),
               ("считает остаток от пути в одну сторону",
                'distance = speed * hours\nround_trip = distance * 2\nleft = distance - done\n'
                'print("To the lake:", distance, "km")\nprint("Round trip:", round_trip, "km")\nprint("Left:", left, "km")'),
               ("складывает скорость и часы вместо умножения",
                'distance = speed + hours\nround_trip = distance * 2\nleft = round_trip - done\n'
                'print("To the lake:", distance, "km")\nprint("Round trip:", round_trip, "km")\nprint("Left:", left, "km")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ar-rt-lemonade-stand", title="Лимонадный киоск",
        given=["buy", "sell", "sold"],
        variants=[{"buy": "30", "sell": "50", "sold": "40"}, {"buy": "45", "sell": "60", "sold": "25"},
                  {"buy": "20", "sell": "35", "sold": "70"}],
        hidden=[{"buy": "10", "sell": "40", "sold": "12"}, {"buy": "55", "sell": "55", "sold": "30"},
                {"buy": "25", "sell": "80", "sold": "3"}],
        intro="Летом школьники держат лимонадный киоск. Стакан лимонада обходится им в `buy = {buy}` руб., "
              "продают они его за `sell = {sell}` руб., за день продали `sold = {sold}` стаканов.",
        steps=["Посчитай `revenue` — выручку: цена продажи, умноженная на число стаканов.",
               "Посчитай `costs` — затраты: себестоимость стакана, умноженная на число стаканов.",
               "Посчитай `profit` одной формулой, не используя `revenue` и `costs`: разница цены продажи и "
               "себестоимости (её возьми в скобки), умноженная на число стаканов.",
               "Выведи три строки: `Revenue:` и `revenue`, `Costs:` и `costs`, `Profit:` и `profit`."],
        hint="Умножение выполняется раньше вычитания: `sell - buy * sold` умножит на число стаканов только себестоимость. "
             "Чтобы сначала посчитать разницу, возьми её в скобки: `(sell - buy) * sold`.",
        solution='revenue = sell * sold\ncosts = buy * sold\nprofit = (sell - buy) * sold\n'
                 'print("Revenue:", revenue)\nprint("Costs:", costs)\nprint("Profit:", profit)',
        wrong=[("забывает скобки — на число стаканов умножается только себестоимость",
                'revenue = sell * sold\ncosts = buy * sold\nprofit = sell - buy * sold\n'
                'print("Revenue:", revenue)\nprint("Costs:", costs)\nprint("Profit:", profit)'),
               ("прибыль — это прибыль с одного стакана, без умножения",
                'revenue = sell * sold\ncosts = buy * sold\nprofit = sell - buy\n'
                'print("Revenue:", revenue)\nprint("Costs:", costs)\nprint("Profit:", profit)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ar-rt-average-speed", title="Средняя скорость в дороге",
        given=["road1", "time1", "road2", "time2"],
        variants=[{"road1": "120", "time1": "2", "road2": "90", "time2": "1"},
                  {"road1": "200", "time1": "4", "road2": "60", "time2": "1"},
                  {"road1": "90", "time1": "1", "road2": "180", "time2": "4"}],
        hidden=[{"road1": "60", "time1": "1", "road2": "60", "time2": "2"},
                {"road1": "80", "time1": "2", "road2": "40", "time2": "2"},
                {"road1": "300", "time1": "5", "road2": "100", "time2": "5"}],
        intro="Семья едет на машине на дачу в два этапа. Первый этап — `road1 = {road1}` км по трассе за `time1 = {time1}` ч, "
              "второй — `road2 = {road2}` км по просёлку за `time2 = {time2}` ч. Навигатор показывает скорость на каждом "
              "этапе и среднюю скорость за всю поездку.",
        steps=["Посчитай `speed1` — скорость на первом этапе: расстояние, делённое на время.",
               "Посчитай `speed2` — скорость на втором этапе.",
               "Посчитай `average` — среднюю скорость: весь путь, делённый на всё время. И сумму расстояний, и сумму "
               "времени возьми в скобки.",
               "Выведи три строки: `Stage 1:`, `speed1` и `km/h`; `Stage 2:`, `speed2` и `km/h`; "
               "`Average:`, `average` и `km/h`. Деление через `/` даёт дробное число, например `Average: 70.0 km/h`."],
        hint="Средняя скорость — это не среднее двух скоростей: на медленном этапе машина едет дольше. "
             "Пиши `(road1 + road2) / (time1 + time2)`: без скобок деление выполнится раньше сложения.",
        solution='speed1 = road1 / time1\nspeed2 = road2 / time2\naverage = (road1 + road2) / (time1 + time2)\n'
                 'print("Stage 1:", speed1, "km/h")\nprint("Stage 2:", speed2, "km/h")\nprint("Average:", average, "km/h")',
        wrong=[("берёт среднее двух скоростей",
                'speed1 = road1 / time1\nspeed2 = road2 / time2\naverage = (speed1 + speed2) / 2\n'
                'print("Stage 1:", speed1, "km/h")\nprint("Stage 2:", speed2, "km/h")\nprint("Average:", average, "km/h")'),
               ("забывает скобки у времени — делит только на первое время",
                'speed1 = road1 / time1\nspeed2 = road2 / time2\naverage = (road1 + road2) / time1 + time2\n'
                'print("Stage 1:", speed1, "km/h")\nprint("Stage 2:", speed2, "km/h")\nprint("Average:", average, "km/h")')],
    ),
]
