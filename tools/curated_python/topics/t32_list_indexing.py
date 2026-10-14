"""PY_LIST_INDEXING — «Индексы списка». Taught before: print, variables, arithmetic, int/float, strings, type conversion,
// and %, +=, f-strings, conditions, for/while loops. Here: indexes from 0, negative indexes, len, changing an element
by index. Not yet: append, in, iterating a list, slices, string methods, functions."""
from build import OutputTask

SKILL = "PY_LIST_INDEXING"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-li-first-last", title="Первый и последний на финише",
        given=["runners"],
        variants=[{"runners": '["Anya", "Boris", "Vika", "Gosha", "Dasha"]'},
                  {"runners": '["Oleg", "Mila", "Timur", "Sonya", "Egor"]'},
                  {"runners": '["Katya", "Lyova", "Nina", "Petya", "Rita"]'}],
        hidden=[{"runners": '["Ira", "Gleb", "Zoya"]'},
                {"runners": '["Max", "Eva", "Yana", "Lev", "Osya", "Fil", "Yulya"]'},
                {"runners": '["Dina", "Artyom"]'}],
        intro="Забег закончился. В списке `runners` записаны имена бегунов в том порядке, в котором они пересекли финиш: "
              "первый в списке — победитель, последний — тот, кто прибежал позже всех.",
        steps=["Выведи через `print` первый элемент списка `runners` — имя победителя.",
               "Следующей строкой выведи последний элемент списка — имя того, кто финишировал последним. "
               "Бегунов может быть больше или меньше, чем в заготовке, поэтому не считай номер последнего вручную — "
               "используй отрицательный индекс."],
        hint='Нумерация элементов списка начинается с нуля, а отрицательные индексы считают с конца. '
             'Например, в списке `colors = ["red", "green", "blue"]` элемент `colors[0]` — это `"red"`, '
             'а `colors[-1]` — `"blue"`.',
        solution="print(runners[0])\nprint(runners[-1])",
        wrong=[("считает с единицы: печатает второго бегуна вместо первого", "print(runners[1])\nprint(runners[-1])"),
               ("берёт последний элемент по номеру из примера — для списка другой длины ответ неверный",
                "print(runners[0])\nprint(runners[4])")],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-li-fix-grade", title="Исправленная оценка",
        given=["grades", "number", "new_grade"],
        variants=[{"grades": "[4, 3, 5, 2, 4]", "number": "2", "new_grade": "5"},
                  {"grades": "[5, 2, 4, 3, 5]", "number": "4", "new_grade": "4"},
                  {"grades": "[3, 4, 2, 5, 4]", "number": "3", "new_grade": "3"}],
        hidden=[{"grades": "[2, 4, 5]", "number": "1", "new_grade": "3"},
                {"grades": "[5, 4, 4, 3, 5, 2, 4]", "number": "7", "new_grade": "3"},
                {"grades": "[3, 3, 4, 5]", "number": "3", "new_grade": "5"}],
        intro="Учитель ведёт журнал. Оценки за контрольную записаны в список `grades` в порядке журнала. "
              "Ученик с номером `number` пересдал контрольную и получил новую оценку `new_grade`. "
              "Номера в журнале, как и в жизни, начинаются с 1.",
        steps=["Замени в списке `grades` оценку ученика с номером `number` на `new_grade`. "
               "Помни: номера в журнале начинаются с 1, а индексы списка — с 0.",
               "Выведи весь список после замены командой `print(grades)`."],
        hint="Ученик с номером 1 стоит в списке под индексом 0, ученик с номером 2 — под индексом 1. "
             "Подумай, как получить индекс из номера. Элемент списка меняют так же, как переменную: "
             "`my_list[index] = new_value`.",
        solution="grades[number - 1] = new_grade\nprint(grades)",
        wrong=[("путает номер в журнале с индексом: меняет оценку следующего ученика", "grades[number] = new_grade\nprint(grades)"),
               ("печатает список до замены", "print(grades)\ngrades[number - 1] = new_grade")],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-li-swap-ends", title="Первая песня станет последней",
        given=["playlist"],
        variants=[{"playlist": '["Morning", "Road", "Sea", "City", "Night"]'},
                  {"playlist": '["Start", "Rhythm", "Wind", "Lights", "Final"]'},
                  {"playlist": '["Sunrise", "Summer", "Dance", "Rain", "Sunset"]'}],
        hidden=[{"playlist": '["Alpha", "Beta", "Gamma"]'},
                {"playlist": '["One", "Two", "Three", "Four", "Five", "Six", "Seven"]'},
                {"playlist": '["First", "Second"]'}],
        intro="Ты собираешь плейлист для вечеринки и хочешь, чтобы последняя песня заиграла первой, а первая — последней. "
              "Песни записаны в списке `playlist`. Остальные песни должны остаться на своих местах.",
        steps=["Поменяй местами первый и последний элементы списка `playlist`. Песен может быть больше или меньше, "
               "чем в заготовке, поэтому для последнего элемента используй отрицательный индекс.",
               "Выведи весь список после обмена командой `print(playlist)`."],
        hint="Если сразу написать `playlist[0] = playlist[-1]`, первая песня потеряется: на её место запишется последняя. "
             "Сначала сохрани первую песню в отдельную переменную, а уже потом меняй элементы.",
        solution="first = playlist[0]\nplaylist[0] = playlist[-1]\nplaylist[-1] = first\nprint(playlist)",
        wrong=[("теряет первую песню: в начале и в конце оказывается последняя",
                "playlist[0] = playlist[-1]\nplaylist[-1] = playlist[0]\nprint(playlist)"),
               ("берёт последний элемент по номеру из примера — для списка другой длины ответ неверный",
                "first = playlist[0]\nplaylist[0] = playlist[4]\nplaylist[4] = first\nprint(playlist)")],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-li-doctor-queue", title="Очередь к врачу",
        given=["queue"],
        variants=[{"queue": '["Anya", "Boris", "Vika", "Gosha"]'},
                  {"queue": '["Timur", "Nina", "Egor", "Sonya", "Lev", "Mila"]'},
                  {"queue": '["Rita", "Oleg", "Dasha"]'}],
        hidden=[{"queue": '["Ira"]'},
                {"queue": '["Max", "Eva", "Yana", "Fil", "Zoya"]'},
                {"queue": '["Dina", "Artyom"]'}],
        intro="Медсестра смотрит на электронное табло очереди к врачу. В списке `queue` записаны имена пациентов "
              "по порядку: первый в списке зайдёт в кабинет следующим.",
        steps=["Выведи, сколько человек в очереди, в формате `In queue: 3`. Людей может быть больше или меньше, "
               "чем в заготовке, поэтому не считай их вручную — используй `len`.",
               "Следующей строкой выведи, кто зайдёт к врачу, в формате `Next: Anya`"],
        hint="`len(queue)` даёт число элементов списка. Первый элемент списка — это `queue[0]`, "
             "потому что индексы начинаются с нуля.",
        solution='print(f"In queue: {len(queue)}")\nprint(f"Next: {queue[0]}")',
        wrong=[("считает с единицы: называет второго в очереди",
                'print(f"In queue: {len(queue)}")\nprint(f"Next: {queue[1]}")'),
               ("называет последнего в очереди вместо первого",
                'print(f"In queue: {len(queue)}")\nprint(f"Next: {queue[-1]}")')],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-li-weather-change", title="Теплее или холоднее",
        given=["temps"],
        variants=[{"temps": "[12, 15, 9, 11, 14]"}, {"temps": "[-3, -1, 2, 0]"}, {"temps": "[20, 23, 25, 21, 18, 16]"}],
        hidden=[{"temps": "[5, 5]"}, {"temps": "[0, 4, 7, -2, 1, 3, 10]"}, {"temps": "[8, 6, 2]"}],
        intro="Дневник погоды хранит дневную температуру в списке `temps`: первый элемент — самый ранний день, "
              "последний — сегодня, предпоследний — вчера. Дней в дневнике может быть сколько угодно, но не меньше двух.",
        steps=["Выведи сегодняшнюю температуру в формате `Today: 14`",
               "Следующей строкой выведи, на сколько градусов сегодня теплее, чем вчера: сегодняшняя температура минус "
               "вчерашняя, в формате `Change: 3`. Если похолодало, число получится отрицательным, например `Change: -4`"],
        hint="Отрицательные индексы считают с конца: `temps[-1]` — последний элемент, `temps[-2]` — предпоследний. "
             "Так не нужно знать, сколько всего дней в списке.",
        solution='print(f"Today: {temps[-1]}")\nprint(f"Change: {temps[-1] - temps[-2]}")',
        wrong=[("вычитает в обратном порядке: вчера минус сегодня",
                'print(f"Today: {temps[-1]}")\nprint(f"Change: {temps[-2] - temps[-1]}")'),
               ("берёт первый день вместо сегодняшнего",
                'print(f"Today: {temps[0]}")\nprint(f"Change: {temps[0] - temps[1]}")')],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-li-median-height", title="Средний рост в строю",
        given=["heights"],
        variants=[{"heights": "[138, 142, 145, 150, 153]"}, {"heights": "[131, 136, 141, 147]"},
                  {"heights": "[145, 148, 150, 152, 156, 160]"}],
        hidden=[{"heights": "[150]"}, {"heights": "[120, 125]"}, {"heights": "[133, 135, 141, 144, 146, 151, 158]"},
                {"heights": "[140, 141, 150, 152]"}],
        intro="Класс выстроился по росту, от самого низкого к самому высокому, и рост каждого ученика в сантиметрах "
              "записан в список `heights`. Физрук хочет узнать медиану — рост ученика, который стоит ровно посередине строя.",
        steps=["Найди длину списка через `len`.",
               "Если учеников нечётное число, медиана — это элемент посередине, его индекс — длина, делённая нацело на 2. "
               "Выведи его в формате `Median: 145`",
               "Если учеников чётное число, посередине стоят двое: элементы с индексами «длина // 2 - 1» и «длина // 2». "
               "Медиана — их среднее: сумма, делённая через `/` на 2. Выведи её в формате `Median: 143.5`"],
        hint="В списке из 5 элементов индексы от 0 до 4, и середина — индекс `5 // 2`, то есть 2. "
             "В списке из 4 элементов посередине стоят индексы 1 и 2. Чётность длины проверяют через `% 2`.",
        solution='n = len(heights)\nif n % 2 == 1:\n    print(f"Median: {heights[n // 2]}")\n'
                 'else:\n    print(f"Median: {(heights[n // 2 - 1] + heights[n // 2]) / 2}")',
        wrong=[("для чётной длины берёт только один элемент вместо среднего двух",
                'n = len(heights)\nprint(f"Median: {heights[n // 2]}")'),
               ("для чётной длины берёт не те два элемента",
                'n = len(heights)\nif n % 2 == 1:\n    print(f"Median: {heights[n // 2]}")\n'
                'else:\n    print(f"Median: {(heights[n // 2] + heights[n // 2 + 1]) / 2}")')],
        constructs=["list"],
    ),
]
