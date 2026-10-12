"""PY_LIST_INDEXING — «Индексы списка». Taught before: print, variables, arithmetic, int/float, strings, type conversion,
// and %, +=, f-strings, conditions, for/while loops. Here: indexes from 0, negative indexes, len, changing an element
by index. Not yet: append, in, iterating a list, slices, string methods, functions."""
from build import OutputTask

SKILL = "PY_LIST_INDEXING"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-li-first-last", title="Первый и последний на финише",
        given=["runners"],
        variants=[{"runners": '["Аня", "Борис", "Вика", "Гоша", "Даша"]'},
                  {"runners": '["Олег", "Мила", "Тимур", "Соня", "Егор"]'},
                  {"runners": '["Катя", "Лёва", "Нина", "Петя", "Рита"]'}],
        hidden=[{"runners": '["Ира", "Глеб", "Зоя"]'},
                {"runners": '["Макс", "Ева", "Яна", "Лев", "Ося", "Фил", "Юля"]'},
                {"runners": '["Дина", "Артём"]'}],
        intro="Забег закончился. В списке `runners` записаны имена бегунов в том порядке, в котором они пересекли финиш: "
              "первый в списке — победитель, последний — тот, кто прибежал позже всех.",
        steps=["Выведи через `print` первый элемент списка `runners` — имя победителя.",
               "Следующей строкой выведи последний элемент списка — имя того, кто финишировал последним. "
               "Бегунов может быть больше или меньше, чем в заготовке, поэтому не считай номер последнего вручную — "
               "используй отрицательный индекс."],
        hint='Нумерация элементов списка начинается с нуля, а отрицательные индексы считают с конца. '
             'Например, в списке `colors = ["красный", "зелёный", "синий"]` элемент `colors[0]` — это `"красный"`, '
             'а `colors[-1]` — `"синий"`.',
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
             "`список[индекс] = новое_значение`.",
        solution="grades[number - 1] = new_grade\nprint(grades)",
        wrong=[("путает номер в журнале с индексом: меняет оценку следующего ученика", "grades[number] = new_grade\nprint(grades)"),
               ("печатает список до замены", "print(grades)\ngrades[number - 1] = new_grade")],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-li-swap-ends", title="Первая песня станет последней",
        given=["playlist"],
        variants=[{"playlist": '["Утро", "Дорога", "Море", "Город", "Ночь"]'},
                  {"playlist": '["Старт", "Ритм", "Ветер", "Огни", "Финал"]'},
                  {"playlist": '["Рассвет", "Лето", "Танец", "Дождь", "Закат"]'}],
        hidden=[{"playlist": '["Альфа", "Бета", "Гамма"]'},
                {"playlist": '["Раз", "Два", "Три", "Четыре", "Пять", "Шесть", "Семь"]'},
                {"playlist": '["Первая", "Вторая"]'}],
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
]
