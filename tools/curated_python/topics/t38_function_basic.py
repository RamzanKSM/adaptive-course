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
        variants=[{"name": '"Anna"'}, {"name": '"Timur"'}, {"name": '"Vera"'}],
        hidden=[{"name": '"Oleg"'}, {"name": '"Zarina"'}, {"name": '"Yan"'}],
        intro="Ты пишешь бота для школьного чата, который поздравляет ребят с днём рождения. "
              "Имя именинника хранится в переменной `name`.",
        steps=["Создай функцию `congratulate` с одним параметром `name`. Она печатает поздравление вида "
               "`Happy birthday, Oleg!` — только вместо «Oleg» имя из параметра `name`. "
               "Перед восклицательным знаком пробела нет.",
               "После функции вызови её один раз и передай ей переменную `name` из заготовки."],
        hint="Сама по себе запись `def` ничего не печатает: она только объясняет Python, что делать. "
             "Код внутри функции выполнится, только когда ты её вызовешь — напишешь имя функции и в скобках аргумент.",
        solution='def congratulate(name):\n    print("Happy birthday, " + name + "!")\n\n\ncongratulate(name)',
        wrong=[("забыл вызвать функцию — ничего не печатается",
                'def congratulate(name):\n    print("Happy birthday, " + name + "!")'),
               ("печатает через запятую — перед восклицательным знаком появляется пробел",
                'def congratulate(name):\n    print("Happy birthday,", name, "!")\n\n\ncongratulate(name)')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fn-scoreboard", title="Счёт двух игроков",
        given=["name1", "points1", "name2", "points2"],
        variants=[{"name1": '"Anya"', "points1": "120", "name2": '"Oleg"', "points2": "95"},
                  {"name1": '"Masha"', "points1": "48", "name2": '"Dima"', "points2": "300"},
                  {"name1": '"Liza"', "points1": "77", "name2": '"Roma"', "points2": "77"}],
        hidden=[{"name1": '"Vanya"', "points1": "10", "name2": '"Nina"', "points2": "250"},
                {"name1": '"Kira"', "points1": "0", "name2": '"Stas"', "points2": "64"},
                {"name1": '"Gena"', "points1": "512", "name2": '"Olya"', "points2": "333"}],
        intro="В игре после раунда на экране показывают счёт каждого игрока. Строка для обоих игроков одинаковая, "
              "меняются только имя и очки, — поэтому удобно один раз описать её в функции и вызвать функцию дважды.",
        steps=["Создай функцию `show_player` с двумя параметрами: `name` (имя игрока) и `points` (его очки). "
               "Функция печатает строку вида `Player Anya: 120`",
               "Вызови функцию два раза: сначала для первого игрока (`name1` и `points1`), "
               "потом для второго (`name2` и `points2`)."],
        hint="Аргументы попадают в параметры по порядку: первый аргумент при вызове становится первым параметром, "
             "второй — вторым. Одну и ту же функцию можно вызывать сколько угодно раз с разными значениями.",
        solution='def show_player(name, points):\n    print(f"Player {name}: {points}")\n\n\n'
                 'show_player(name1, points1)\nshow_player(name2, points2)',
        wrong=[("передаёт аргументы не в том порядке — имя и очки меняются местами",
                'def show_player(name, points):\n    print(f"Player {name}: {points}")\n\n\n'
                'show_player(points1, name1)\nshow_player(points2, name2)'),
               ("дважды вызывает функцию для первого игрока",
                'def show_player(name, points):\n    print(f"Player {name}: {points}")\n\n\n'
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
        steps=["Создай функцию `show_result` с параметром `score`. Она печатает число баллов, пробел и слово `pass`, "
               "если баллов 50 или больше, а иначе — число баллов, пробел и слово `fail`. "
               "Например, `show_result(64)` печатает `64 pass`, а `show_result(20)` печатает `20 fail`",
               "Пройди циклом `for` по списку `scores` и вызови функцию для каждого числа из списка — "
               "каждый результат на своей строке, в том же порядке, что и в списке."],
        hint="Внутри функции можно писать `if` и `else`, как в обычной программе. Обрати внимание на границу: "
             "ровно 50 баллов — это уже зачёт. А вызывать функцию нужно внутри цикла, а не после него.",
        solution='def show_result(score):\n    if score >= 50:\n        print(score, "pass")\n    else:\n'
                 '        print(score, "fail")\n\n\nfor score in scores:\n    show_result(score)',
        wrong=[("ставит зачёт только за баллы больше 50 — ровно 50 становится незачётом",
                'def show_result(score):\n    if score > 50:\n        print(score, "pass")\n    else:\n'
                '        print(score, "fail")\n\n\nfor score in scores:\n    show_result(score)'),
               ("вызывает функцию только для первого ученика",
                'def show_result(score):\n    if score >= 50:\n        print(score, "pass")\n    else:\n'
                '        print(score, "fail")\n\n\nshow_result(scores[0])')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-fn-tile-area", title="Плитка для пола",
        given=["side"],
        variants=[{"side": "5"}, {"side": "3"}, {"side": "8"}],
        hidden=[{"side": "1"}, {"side": "4"}, {"side": "12"}],
        intro="Мастер кладёт плитку в квадратных комнатах и каждый раз считает площадь пола. "
              "Длина стороны комнаты в метрах записана в переменной `side`.",
        steps=["Создай функцию `show_area` с одним параметром `side`. Она печатает площадь квадратной комнаты "
               "(сторона, умноженная на саму себя) в виде `Area: 16 sq m`",
               "После функции вызови её один раз и передай ей переменную `side` из заготовки."],
        hint="Запись `def` только описывает функцию — сама по себе она ничего не печатает. "
             "Чтобы код внутри выполнился, функцию нужно вызвать: написать её имя и в скобках аргумент.",
        solution='def show_area(side):\n    print(f"Area: {side * side} sq m")\n\n\nshow_area(side)',
        wrong=[("забыл вызвать функцию — ничего не печатается",
                'def show_area(side):\n    print(f"Area: {side * side} sq m")'),
               ("считает периметр вместо площади",
                'def show_area(side):\n    print(f"Area: {side * 4} sq m")\n\n\nshow_area(side)')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fn-two-races", title="Старт двух заездов",
        given=["first", "second"],
        variants=[{"first": "3", "second": "5"}, {"first": "4", "second": "2"}, {"first": "5", "second": "3"}],
        hidden=[{"first": "1", "second": "2"}, {"first": "6", "second": "1"}, {"first": "2", "second": "4"}],
        intro="На картинге два заезда. Перед каждым судья ведёт обратный отсчёт, но с разного числа: "
              "перед первым заездом — с `first`, перед вторым — с `second`. Отсчёт устроен одинаково, "
              "поэтому его удобно описать один раз в функции.",
        steps=["Создай функцию `countdown` с параметром `n`. Она печатает числа от `n` до 1 по убыванию, "
               "каждое на отдельной строке, а потом строку `Go!`",
               "Вызови функцию два раза: сначала с `first`, потом с `second`."],
        hint="Внутри функции можно писать цикл, как в обычной программе: `range(n, 0, -1)` даёт числа от `n` до 1. "
             "Следи за отступами: `print(\"Go!\")` должен быть внутри функции, но после цикла.",
        solution='def countdown(n):\n    for i in range(n, 0, -1):\n        print(i)\n    print("Go!")\n\n\n'
                 'countdown(first)\ncountdown(second)',
        wrong=[("«Go!» внутри цикла — печатается после каждого числа",
                'def countdown(n):\n    for i in range(n, 0, -1):\n        print(i)\n        print("Go!")\n\n\n'
                'countdown(first)\ncountdown(second)'),
               ("вызывает функцию только для первого заезда",
                'def countdown(n):\n    for i in range(n, 0, -1):\n        print(i)\n    print("Go!")\n\n\n'
                'countdown(first)')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fn-movie-stars", title="Оценки фильмов звёздочками",
        given=["titles", "stars"],
        variants=[{"titles": '["Up", "Cars", "Coco"]', "stars": "[5, 3, 4]"},
                  {"titles": '["Shrek", "Frozen", "Moana", "Soul"]', "stars": "[4, 2, 5, 3]"},
                  {"titles": '["Bolt", "Rio"]', "stars": "[1, 4]"}],
        hidden=[{"titles": '["Dumbo"]', "stars": "[0]"},
                {"titles": '["Wall-E", "Brave", "Luca", "Onward", "Elio"]', "stars": "[5, 2, 3, 1, 4]"},
                {"titles": '["Mulan", "Tarzan"]', "stars": "[3, 5]"}],
        intro="Ты делаешь страничку с оценками мультфильмов. Названия записаны в список `titles`, а оценки от 0 до 5 — "
              "в список `stars` в том же порядке: `stars[0]` — оценка фильма `titles[0]` и так далее.",
        steps=["Создай функцию `show_rating` с двумя параметрами: `title` и `count`. Она печатает название, двоеточие, "
               "пробел, затем `count` звёздочек `*` и точки `.` до пяти знаков. Например, `show_rating(\"Up\", 3)` "
               "печатает `Up: ***..`",
               "Пройди циклом `for` по всем индексам списка `titles` (от 0 до последнего) и вызови функцию для каждого фильма "
               "с его названием и оценкой — каждую строку в том же порядке, что и в списке."],
        hint="Строку можно умножить на число: `\"*\" * 3` даёт `\"***\"`. Точек нужно `5 - count`. "
             "Индексы перебирает `range(len(titles))`, а название и оценку одного фильма берёшь по одному и тому же индексу.",
        solution='def show_rating(title, count):\n    print(title + ": " + "*" * count + "." * (5 - count))\n\n\n'
                 'for i in range(len(titles)):\n    show_rating(titles[i], stars[i])',
        wrong=[("не дописывает точки до пяти знаков",
                'def show_rating(title, count):\n    print(title + ": " + "*" * count)\n\n\n'
                'for i in range(len(titles)):\n    show_rating(titles[i], stars[i])'),
               ("печатает через запятую — между звёздочками и точками появляется пробел",
                'def show_rating(title, count):\n    print(title + ":", "*" * count, "." * (5 - count))\n\n\n'
                'for i in range(len(titles)):\n    show_rating(titles[i], stars[i])')],
        constructs=["function"],
        must_use=[NEED_DEF],
    ),
]
