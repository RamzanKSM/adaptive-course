"""PY_FUNCTION_BASIC — «Функции». Taught before: everything up to string methods (conditions, loops, lists, iterating a
list, slices). Here: def, parameters, calling a function; the function prints. Not yet: return (next topic), default
values and keyword arguments."""
from build import OutputTask

SKILL = "PY_FUNCTION_BASIC"

NEED_DEF = ("FunctionDef", "Оформи решение в виде своей функции: создай её через def и вызови.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-fn-birthday", title="Поздравление с днём рождения",
        given=["name"],
        variants=[{"name": '"Анна"'}, {"name": '"Тимур"'}, {"name": '"Вера"'}],
        hidden=[{"name": '"Олег"'}, {"name": '"Зарина"'}, {"name": '"Ян"'}],
        intro="Ты пишешь бота для школьного чата, который поздравляет ребят с днём рождения. "
              "Имя именинника хранится в переменной `name`.",
        steps=["Создай функцию `congratulate` с одним параметром `name`. Она печатает поздравление вида "
               "`С днём рождения, Олег!` — только вместо «Олег» имя из параметра `name`. "
               "Перед восклицательным знаком пробела нет.",
               "После функции вызови её один раз и передай ей переменную `name` из заготовки."],
        hint="Сама по себе запись `def` ничего не печатает: она только объясняет Python, что делать. "
             "Код внутри функции выполнится, только когда ты её вызовешь — напишешь имя функции и в скобках аргумент.",
        solution='def congratulate(name):\n    print("С днём рождения, " + name + "!")\n\n\ncongratulate(name)',
        wrong=[("забыл вызвать функцию — ничего не печатается",
                'def congratulate(name):\n    print("С днём рождения, " + name + "!")'),
               ("печатает через запятую — перед восклицательным знаком появляется пробел",
                'def congratulate(name):\n    print("С днём рождения,", name, "!")\n\n\ncongratulate(name)')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fn-scoreboard", title="Счёт двух игроков",
        given=["name1", "points1", "name2", "points2"],
        variants=[{"name1": '"Аня"', "points1": "120", "name2": '"Олег"', "points2": "95"},
                  {"name1": '"Маша"', "points1": "48", "name2": '"Дима"', "points2": "300"},
                  {"name1": '"Лиза"', "points1": "77", "name2": '"Рома"', "points2": "77"}],
        hidden=[{"name1": '"Ваня"', "points1": "10", "name2": '"Нина"', "points2": "250"},
                {"name1": '"Кира"', "points1": "0", "name2": '"Стас"', "points2": "64"},
                {"name1": '"Гена"', "points1": "512", "name2": '"Оля"', "points2": "333"}],
        intro="В игре после раунда на экране показывают счёт каждого игрока. Строка для обоих игроков одинаковая, "
              "меняются только имя и очки, — поэтому удобно один раз описать её в функции и вызвать функцию дважды.",
        steps=["Создай функцию `show_player` с двумя параметрами: `name` (имя игрока) и `points` (его очки). "
               "Функция печатает строку вида `Счёт игрока Аня: 120`",
               "Вызови функцию два раза: сначала для первого игрока (`name1` и `points1`), "
               "потом для второго (`name2` и `points2`)."],
        hint="Аргументы попадают в параметры по порядку: первый аргумент при вызове становится первым параметром, "
             "второй — вторым. Одну и ту же функцию можно вызывать сколько угодно раз с разными значениями.",
        solution='def show_player(name, points):\n    print(f"Счёт игрока {name}: {points}")\n\n\n'
                 'show_player(name1, points1)\nshow_player(name2, points2)',
        wrong=[("передаёт аргументы не в том порядке — имя и очки меняются местами",
                'def show_player(name, points):\n    print(f"Счёт игрока {name}: {points}")\n\n\n'
                'show_player(points1, name1)\nshow_player(points2, name2)'),
               ("дважды вызывает функцию для первого игрока",
                'def show_player(name, points):\n    print(f"Счёт игрока {name}: {points}")\n\n\n'
                'show_player(name1, points1)\nshow_player(name1, points1)')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fn-pass-fail", title="Зачёт или незачёт",
        given=["scores"],
        variants=[{"scores": "[72, 38, 50, 91]"},
                  {"scores": "[50, 64, 12, 49]"},
                  {"scores": "[85, 47, 100, 50]"}],
        hidden=[{"scores": "[30, 50]"},
                {"scores": "[99, 49, 50, 51, 0, 75]"},
                {"scores": "[60]"}],
        intro="Учитель проверил контрольную и записал баллы учеников в список `scores`. "
              "Зачёт ставят, если ученик набрал 50 баллов или больше. Нужно вывести результат по каждому ученику.",
        steps=["Создай функцию `show_result` с параметром `score`. Она печатает число баллов, пробел и слово `зачёт`, "
               "если баллов 50 или больше, а иначе — число баллов, пробел и слово `незачёт`. "
               "Например, `show_result(64)` печатает `64 зачёт`, а `show_result(20)` печатает `20 незачёт`",
               "Пройди циклом `for` по списку `scores` и вызови функцию для каждого числа из списка — "
               "каждый результат на своей строке, в том же порядке, что и в списке."],
        hint="Внутри функции можно писать `if` и `else`, как в обычной программе. Обрати внимание на границу: "
             "ровно 50 баллов — это уже зачёт. А вызывать функцию нужно внутри цикла, а не после него.",
        solution='def show_result(score):\n    if score >= 50:\n        print(score, "зачёт")\n    else:\n'
                 '        print(score, "незачёт")\n\n\nfor score in scores:\n    show_result(score)',
        wrong=[("ставит зачёт только за баллы больше 50 — ровно 50 становится незачётом",
                'def show_result(score):\n    if score > 50:\n        print(score, "зачёт")\n    else:\n'
                '        print(score, "незачёт")\n\n\nfor score in scores:\n    show_result(score)'),
               ("вызывает функцию только для первого ученика",
                'def show_result(score):\n    if score >= 50:\n        print(score, "зачёт")\n    else:\n'
                '        print(score, "незачёт")\n\n\nshow_result(scores[0])')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
]
