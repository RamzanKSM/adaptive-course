"""PY_FOR_RANGE — «Цикл for и range». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, += -=, f-strings, if/else, comparisons, and/or/not, elif, truthiness.
Not yet: accumulating a result in a loop, while, break/continue, lists, functions."""
from build import OutputTask

SKILL = "PY_FOR_RANGE"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-for-rt-push-ups", title="План отжиманий",
        given=["days"],
        variants=[{"days": "4"}, {"days": "6"}, {"days": "3"}],
        hidden=[{"days": "1"}, {"days": "5"}, {"days": "7"}],
        intro="Миша составляет план тренировок: в первый день 10 отжиманий, во второй 20, в третий 30 — "
              "каждый день на 10 больше. План нужен на `days = {days}` дней.",
        steps=["Напиши цикл `for` с `range`, который перебирает номера дней от 1 до `days` включительно.",
               "На каждом шаге выведи отдельной строкой надпись вида `Day 2: 20 push-ups`: номер дня и число отжиманий "
               "(номер дня, умноженный на 10)."],
        hint="`range(a, b)` выдаёт числа от `a` до `b - 1`: правая граница не входит. "
             "В f-строке в фигурных скобках можно сразу посчитать число отжиманий: `{{day * 10}}`.",
        solution='for day in range(1, days + 1):\n    print(f"Day {day}: {day * 10} push-ups")',
        wrong=[("range(days) начинает с 0: день 0 и нет последнего дня",
                'for day in range(days):\n    print(f"Day {day}: {day * 10} push-ups")'),
               ("правая граница не входит в range: последний день пропущен",
                'for day in range(1, days):\n    print(f"Day {day}: {day * 10} push-ups")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-for-rt-water-stations", title="Пункты с водой на забеге",
        given=["length", "step"],
        variants=[{"length": "21", "step": "5"}, {"length": "10", "step": "2"}, {"length": "15", "step": "4"}],
        hidden=[{"length": "20", "step": "5"}, {"length": "3", "step": "5"}, {"length": "12", "step": "3"},
                {"length": "7", "step": "7"}],
        intro="Трасса забега длиной `length = {length}` км. Пункты с водой ставят через каждые `step = {step}` км: "
              "первый — на отметке `step` км, следующий — ещё через `step` км, и так далее, пока не кончится трасса.",
        steps=["С помощью цикла `for` и `range` с шагом `step` перебери отметки `step`, `2 * step`, … — все, "
               "которые не больше `length`.",
               "Каждую отметку выведи на отдельной строке в виде `Water at 5 km`.",
               "После цикла выведи одной строкой `Finish at <length> km`, например `Finish at 21 km`."],
        hint="Третье число в `range` — шаг, и он может быть переменной: `range(step, ..., step)`. "
             "Правая граница не входит, поэтому, чтобы пункт ровно на финише попал в список, справа нужно `length + 1`. "
             "Если трасса короче шага, пунктов с водой нет совсем — выводится только финиш.",
        solution='for km in range(step, length + 1, step):\n    print(f"Water at {km} km")\nprint(f"Finish at {length} km")',
        wrong=[("правая граница length: пункт ровно на финише пропущен",
                'for km in range(step, length, step):\n    print(f"Water at {km} km")\nprint(f"Finish at {length} km")'),
               ("начинает с 0: появляется пункт на старте",
                'for km in range(0, length + 1, step):\n    print(f"Water at {km} km")\nprint(f"Finish at {length} km")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-for-rt-bike-rental", title="Прокат велосипеда по часам",
        given=["start", "end"],
        variants=[{"start": "7", "end": "11"}, {"start": "16", "end": "20"}, {"start": "10", "end": "13"}],
        hidden=[{"start": "8", "end": "10"}, {"start": "17", "end": "19"}, {"start": "12", "end": "13"},
                {"start": "6", "end": "21"}],
        intro="Велосипед взяли в прокате в `start = {start}` часов и вернули в `end = {end}` часов. Каждый час "
              "оплачивается отдельно: днём, в часы, которые начинаются с 9 до 17 включительно, — 100 руб., "
              "а утром и вечером — 50 руб.",
        steps=["Перебери циклом `for` часы от `start` до `end` — **не включая** `end`: в этот час велосипед уже вернули.",
               "Если час не меньше 9 **и** не больше 17, выведи строку вида `10:00 100 rub`.",
               "Иначе выведи строку вида `8:00 50 rub`."],
        hint="`range(start, end)` как раз не включает `end` — здесь правую границу менять не нужно. "
             "Проверь границы: час, начинающийся в 9, и час, начинающийся в 17, — дневные, а в 18 уже вечер.",
        solution='for hour in range(start, end):\n    if hour >= 9 and hour <= 17:\n        print(f"{hour}:00 100 rub")\n'
                 '    else:\n        print(f"{hour}:00 50 rub")',
        wrong=[("лишний час: перебирает до end включительно",
                'for hour in range(start, end + 1):\n    if hour >= 9 and hour <= 17:\n        print(f"{hour}:00 100 rub")\n'
                '    else:\n        print(f"{hour}:00 50 rub")'),
               ("строгое сравнение: час с 17 до 18 считается вечерним",
                'for hour in range(start, end):\n    if hour >= 9 and hour < 17:\n        print(f"{hour}:00 100 rub")\n'
                '    else:\n        print(f"{hour}:00 50 rub")'),
               ("or вместо and: все часы дневные",
                'for hour in range(start, end):\n    if hour >= 9 or hour <= 17:\n        print(f"{hour}:00 100 rub")\n'
                '    else:\n        print(f"{hour}:00 50 rub")')],
        constructs=["for"],
    ),
]
