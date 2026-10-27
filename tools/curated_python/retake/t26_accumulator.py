"""PY_ACCUMULATOR_PATTERN — «Накопление результата в цикле». Taught before: print, variables, assignment, arithmetic,
int/float, strings, type conversion, // and %, += -=, f-strings, if/else, comparisons, and/or/not, elif, truthiness,
for + range. Here: a sum, a counter or a product started before the loop and updated on every step.
Not yet: while, break/continue, lists, string slicing and methods, functions."""
from build import OutputTask

SKILL = "PY_ACCUMULATOR_PATTERN"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-acc-rt-paper-fold", title="Складываем лист бумаги",
        given=["thick", "folds"],
        variants=[{"thick": "100", "folds": "4"}, {"thick": "80", "folds": "3"}, {"thick": "50", "folds": "6"}],
        hidden=[{"thick": "10", "folds": "1"}, {"thick": "200", "folds": "2"}, {"thick": "90", "folds": "5"}],
        intro="Лист бумаги толщиной `thick = {thick}` мкм складывают пополам `folds = {folds}` раз подряд. "
              "При каждом сгибе число слоёв бумаги удваивается.",
        steps=["Заведи переменную `layers` — сколько слоёв в пачке. Пока лист не сложен, слой один.",
               "Напиши цикл `for` с `range`, который перебирает номера сгибов от 1 до `folds` включительно.",
               "На каждом шаге умножь `layers` на 2 через `*=` и выведи строку вида `Fold 1: 2 layers` — "
               "номер сгиба и число слоёв после него.",
               "После цикла выведи толщину пачки (слои, умноженные на `thick`) в виде `Thickness: 1600 um`"],
        hint="Накопитель заводят до цикла, а внутри цикла только меняют. Для произведения начальное значение — 1, "
             "а не 0: умножение на 0 всегда даёт 0. `layers *= 2` — то же, что `layers = layers * 2`.",
        solution='layers = 1\nfor fold in range(1, folds + 1):\n    layers *= 2\n'
                 '    print(f"Fold {fold}: {layers} layers")\nprint(f"Thickness: {layers * thick} um")',
        wrong=[("начинает с 0 слоёв: всё время получается 0",
                'layers = 0\nfor fold in range(1, folds + 1):\n    layers *= 2\n'
                '    print(f"Fold {fold}: {layers} layers")\nprint(f"Thickness: {layers * thick} um")'),
               ("прибавляет 2 вместо удвоения",
                'layers = 1\nfor fold in range(1, folds + 1):\n    layers += 2\n'
                '    print(f"Fold {fold}: {layers} layers")\nprint(f"Thickness: {layers * thick} um")'),
               ("печатает число слоёв до сгиба, а не после",
                'layers = 1\nfor fold in range(1, folds + 1):\n    print(f"Fold {fold}: {layers} layers")\n'
                '    layers *= 2\nprint(f"Thickness: {layers * thick} um")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-acc-rt-clock-chime", title="Часы с боем",
        given=["start", "end"],
        variants=[{"start": "10", "end": "14"}, {"start": "8", "end": "11"}, {"start": "11", "end": "16"}],
        hidden=[{"start": "12", "end": "13"}, {"start": "1", "end": "3"}, {"start": "13", "end": "13"},
                {"start": "9", "end": "23"}],
        intro="Старинные часы на башне каждый час бьют столько раз, сколько показывает стрелка на циферблате "
              "из 12 часов: в 10:00 — 10 ударов, в 12:00 — 12, а в 14:00 — 2 удара, потому что стрелка стоит на 2. "
              "Турист слушал часы с `start = {start}`:00 до `end = {end}`:00 включительно (часы от 1 до 23).",
        steps=["Заведи накопитель `total` со значением 0.",
               "Циклом `for` перебери часы от `start` до `end` включительно.",
               "На каждом шаге найди число ударов: если час больше 12, это час минус 12, иначе сам час. "
               "Прибавь его к `total` и выведи строку вида `14:00 bongs: 2`.",
               "После цикла выведи `Total bongs: 36`"],
        hint="Число ударов удобно сохранить в переменную в обеих ветках `if` / `else`, а потом один раз прибавить "
             "и напечатать. В 12:00 часы бьют 12 раз, а не 0: 12 не больше 12.",
        solution='total = 0\nfor hour in range(start, end + 1):\n    if hour > 12:\n        bongs = hour - 12\n'
                 '    else:\n        bongs = hour\n    total += bongs\n    print(f"{hour}:00 bongs: {bongs}")\n'
                 'print(f"Total bongs: {total}")',
        wrong=[("правая граница не входит в range: последний час не учтён",
                'total = 0\nfor hour in range(start, end):\n    if hour > 12:\n        bongs = hour - 12\n'
                '    else:\n        bongs = hour\n    total += bongs\n    print(f"{hour}:00 bongs: {bongs}")\n'
                'print(f"Total bongs: {total}")'),
               ("нестрогое сравнение: в 12:00 часы молчат",
                'total = 0\nfor hour in range(start, end + 1):\n    if hour >= 12:\n        bongs = hour - 12\n'
                '    else:\n        bongs = hour\n    total += bongs\n    print(f"{hour}:00 bongs: {bongs}")\n'
                'print(f"Total bongs: {total}")'),
               ("перезаписывает total вместо накопления",
                'total = 0\nfor hour in range(start, end + 1):\n    if hour > 12:\n        bongs = hour - 12\n'
                '    else:\n        bongs = hour\n    total = bongs\n    print(f"{hour}:00 bongs: {bongs}")\n'
                'print(f"Total bongs: {total}")')],
        constructs=["for", "if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-acc-rt-taxi-meter", title="Счётчик такси по километрам",
        given=["km"],
        variants=[{"km": "15"}, {"km": "8"}, {"km": "2"}],
        hidden=[{"km": "1"}, {"km": "3"}, {"km": "4"}, {"km": "10"}, {"km": "11"}, {"km": "25"}],
        intro="Счётчик такси берёт за каждый километр по-разному: километры с 1-го по 3-й стоят по 40 руб., "
              "с 4-го по 10-й — по 25 руб., а все следующие — по 15 руб. Поездка длилась `km = {km}` км.",
        steps=["Заведи два накопителя со значением 0: `cost` — стоимость поездки и `cheap` — сколько было "
               "километров по 15 руб.",
               "Циклом `for` перебери номера километров от 1 до `km` включительно.",
               "Если номер не больше 3, прибавь к `cost` 40. Иначе, если номер не больше 10, прибавь 25. "
               "Иначе прибавь 15 и увеличь `cheap` на 1.",
               "После цикла выведи три строки: `Cost: 370 rub`, `Cheap km: 5` и среднюю цену километра "
               "(деление нацело `//`) в виде `Average: 24 rub/km`"],
        hint="Внутри цикла нужна цепочка `if` / `elif` / `else`. Проверяй пороги от меньшего к большему: если "
             "первым проверить «не больше 10», первые три километра тоже окажутся по 25 руб. "
             "Километр номер 3 ещё стоит 40, а номер 10 — ещё 25.",
        solution='cost = 0\ncheap = 0\nfor i in range(1, km + 1):\n    if i <= 3:\n        cost += 40\n'
                 '    elif i <= 10:\n        cost += 25\n    else:\n        cost += 15\n        cheap += 1\n'
                 'print(f"Cost: {cost} rub")\nprint(f"Cheap km: {cheap}")\nprint(f"Average: {cost // km} rub/km")',
        wrong=[("строгие сравнения: 3-й и 10-й километры считаются по следующей цене",
                'cost = 0\ncheap = 0\nfor i in range(1, km + 1):\n    if i < 3:\n        cost += 40\n'
                '    elif i < 10:\n        cost += 25\n    else:\n        cost += 15\n        cheap += 1\n'
                'print(f"Cost: {cost} rub")\nprint(f"Cheap km: {cheap}")\nprint(f"Average: {cost // km} rub/km")'),
               ("пороги в обратном порядке: первые три километра стоят 25 руб.",
                'cost = 0\ncheap = 0\nfor i in range(1, km + 1):\n    if i <= 10:\n        cost += 25\n'
                '    elif i <= 3:\n        cost += 40\n    else:\n        cost += 15\n        cheap += 1\n'
                'print(f"Cost: {cost} rub")\nprint(f"Cheap km: {cheap}")\nprint(f"Average: {cost // km} rub/km")'),
               ("range(km) начинает с 0: лишний километр в начале и нет последнего",
                'cost = 0\ncheap = 0\nfor i in range(km):\n    if i <= 3:\n        cost += 40\n'
                '    elif i <= 10:\n        cost += 25\n    else:\n        cost += 15\n        cheap += 1\n'
                'print(f"Cost: {cost} rub")\nprint(f"Cheap km: {cheap}")\nprint(f"Average: {cost // km} rub/km")')],
        constructs=["for", "if"],
    ),
]
