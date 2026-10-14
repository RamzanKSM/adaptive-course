"""PY_COMPREHENSIONS — «Генераторы списков». Taught before: lists and their methods, tuples, sets, dicts, loops,
conditions, string methods, functions, classes. Here: list comprehensions — a new list from an expression over
the elements, with and without a condition. Not yet: try/except, lambda."""
from build import OutputTask

SKILL = "PY_COMPREHENSIONS"

NEED_LISTCOMP = ("ListComp", "Собери новый список генератором списка — одной строкой вида [выражение for элемент in список], "
                             "без цикла с append.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-comp-bonus-points", title="Бонусные баллы",
        given=["scores", "bonus"],
        variants=[{"scores": "[72, 85, 64, 90]", "bonus": "5"},
                  {"scores": "[50, 47, 66, 81, 73]", "bonus": "10"},
                  {"scores": "[12, 18, 9]", "bonus": "3"}],
        hidden=[{"scores": "[1, 2]", "bonus": "1"},
                {"scores": "[40, 55, 70, 85, 100, 15]", "bonus": "7"},
                {"scores": "[0]", "bonus": "20"}],
        intro="Контрольная оказалась сложной, и учитель решил добавить каждому ученику одинаковое число бонусных баллов — "
              "`bonus`. Баллы учеников записаны в список `scores`.",
        steps=["Создай новый список, в котором каждый балл из `scores` увеличен на `bonus`. Сделай это одной строкой — "
               "генератором списка, без цикла с `append`.",
               "Выведи новый список через `print`."],
        hint="Генератор списка читается почти как фраза: `[x * 2 for x in numbers]` — «x, умноженное на 2, для каждого x "
             "из numbers». Слева от `for` пишут, что положить в новый список, справа — откуда брать элементы.",
        solution="new_scores = [score + bonus for score in scores]\nprint(new_scores)",
        wrong=[("собирает новый список, но печатает старый — исходный список от этого не меняется",
                "new_scores = [score + bonus for score in scores]\nprint(scores)"),
               ("перебирает индексы вместо самих баллов — бонус прибавляется к номерам 0, 1, 2…",
                "new_scores = [i + bonus for i in range(len(scores))]\nprint(new_scores)")],
        constructs=["list"],
        must_use=[NEED_LISTCOMP],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-comp-big-purchases", title="Крупные покупки",
        given=["purchases", "limit"],
        variants=[{"purchases": "[350, 1200, 89, 4500, 700, 1500]", "limit": "1000"},
                  {"purchases": "[99, 250, 600, 249, 1000]", "limit": "250"},
                  {"purchases": "[5000, 120, 3000, 3000, 80]", "limit": "3000"}],
        hidden=[{"purchases": "[10, 20]", "limit": "100"},
                {"purchases": "[150, 300, 450, 600, 750, 900, 1050]", "limit": "450"},
                {"purchases": "[1, 2, 3]", "limit": "0"}],
        intro="Банковское приложение следит за тратами. Суммы покупок за неделю записаны в список `purchases`, "
              "а крупной считается покупка дороже `limit` рублей. Нужно отобрать крупные покупки.",
        steps=["Генератором списка с условием `if` собери новый список только из тех покупок, которые **больше** `limit`. "
               "Покупка, которая стоит ровно `limit`, крупной не считается. Порядок покупок сохрани.",
               "Выведи этот список через `print`.",
               "Следующей строкой выведи строку вида `Big purchases: 7` — сколько элементов в новом списке."],
        hint="Условие в генераторе списка пишут в конце: `[x for x in numbers if x % 2 == 0]` оставит только чётные числа. "
             "Элементы, для которых условие ложно, в новый список не попадут.",
        solution='big = [price for price in purchases if price > limit]\nprint(big)\nprint(f"Big purchases: {len(big)}")',
        wrong=[("забыл условие — в список попадают все покупки",
                'big = [price for price in purchases]\nprint(big)\nprint(f"Big purchases: {len(big)}")'),
               ("нестрогое сравнение — покупка ровно на limit тоже считается крупной",
                'big = [price for price in purchases if price >= limit]\nprint(big)\nprint(f"Big purchases: {len(big)}")')],
        constructs=["list"],
        must_use=[NEED_LISTCOMP],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-comp-clean-tags", title="Интересы из анкеты",
        given=["tags"],
        variants=[{"tags": '["  Python ", "", "GAMES", "   ", "Music  "]'},
                  {"tags": '["Sport", "  ", " Movies", "BOOKS ", ""]'},
                  {"tags": '["", " Drawing ", "  ", "Chess", "  Dance"]'}],
        hidden=[{"tags": '["Code"]'},
                {"tags": '["   ", ""]'},
                {"tags": '[" A ", "B", "  C  ", "", "d", " "]'},
                {"tags": '["Football", "  HOCKEY  ", "", "Tennis", "    ", "Running"]'}],
        intro="Пользователи заполняют в анкете поле «Интересы». Теги приходят неаккуратными: с лишними пробелами по краям, "
              "с большими буквами, а иногда пустыми или из одних пробелов. Все теги лежат в списке `tags`.",
        steps=["Генератором списка собери новый список аккуратных тегов: у каждого тега убери пробелы по краям методом "
               "`.strip()` и сделай все буквы маленькими методом `.lower()`.",
               "В новый список не должны попасть пустые теги — ни пустые строки, ни строки из одних пробелов. "
               "Порядок остальных тегов сохрани.",
               "Выведи новый список через `print`."],
        hint='Строка из одних пробелов не пустая, но после `.strip()` от неё остаётся пустая строка `""`. '
             'Поэтому в условии генератора проверяй тег уже после `.strip()`.',
        solution='clean = [tag.strip().lower() for tag in tags if tag.strip() != ""]\nprint(clean)',
        wrong=[("проверяет тег до .strip() — строки из пробелов превращаются в пустые теги",
                'clean = [tag.strip().lower() for tag in tags if tag != ""]\nprint(clean)'),
               ("забыл .strip() в выражении — пробелы по краям остаются",
                'clean = [tag.lower() for tag in tags if tag.strip() != ""]\nprint(clean)')],
        constructs=["list"],
        must_use=[NEED_LISTCOMP],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-comp-city-lengths", title="Длины названий городов",
        given=["cities"],
        variants=[{"cities": '["Kazan", "Sochi", "Moscow", "Omsk"]'},
                  {"cities": '["Vladivostok", "Tver", "Murmansk"]'},
                  {"cities": '["Ufa", "Perm", "Samara", "Saint Petersburg", "Kaluga"]'}],
        hidden=[{"cities": '["Orel"]'},
                {"cities": '["Tula", "Yekaterinburg", "Pskov", "Kirov", "Chita", "Tomsk"]'},
                {"cities": '["Ivanovo", "Ivanovo"]'}],
        intro="Для табло на вокзале нужно знать, сколько места займёт каждое название города. Названия лежат "
              "в списке `cities`.",
        steps=["Генератором списка собери новый список, в котором вместо каждого названия стоит его длина — "
               "число символов, которое возвращает `len()`. Порядок сохрани.",
               "Выведи этот список через `print`.",
               "Следующей строкой выведи строку вида `Longest: 11` — самую большую длину из нового списка. "
               "Её вернёт функция `max()`."],
        hint="В генераторе списка слева от `for` может стоять любое выражение с элементом: `[len(w) for w in words]` "
             "кладёт в новый список длину каждого слова. Пробел внутри названия — тоже символ.",
        solution='lengths = [len(city) for city in cities]\nprint(lengths)\nprint(f"Longest: {max(lengths)}")',
        wrong=[("печатает длину самого списка вместо длин названий",
                'lengths = [len(cities) for city in cities]\nprint(lengths)\nprint(f"Longest: {max(lengths)}")'),
               ("берёт длину первого названия вместо самой большой",
                'lengths = [len(city) for city in cities]\nprint(lengths)\nprint(f"Longest: {lengths[0]}")')],
        constructs=["list"],
        must_use=[NEED_LISTCOMP],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-comp-names-by-letter", title="Гости на одну букву",
        given=["guests", "letter"],
        variants=[{"guests": '["Anya", "Boris", "Alla", "Vika", "Artem"]', "letter": '"A"'},
                  {"guests": '["Mila", "Oleg", "Masha", "Max", "Nina", "Mark"]', "letter": '"M"'},
                  {"guests": '["Sonya", "Timur", "Semyon", "Liza"]', "letter": '"T"'}],
        hidden=[{"guests": '["Kira"]', "letter": '"K"'},
                {"guests": '["Dima", "Egor", "Fedya"]', "letter": '"Z"'},
                {"guests": '["Gleb", "Galya", "Gosha", "Ilya", "Gena"]', "letter": '"G"'}],
        intro="На празднике гостей рассаживают по столам по первой букве имени. Имена гостей записаны в список `guests`, "
              "за этот стол садятся гости, чьё имя начинается с буквы `letter`. Таблички для стола печатают большими буквами.",
        steps=["Генератором списка с условием `if` собери список табличек: имена гостей, которые начинаются с `letter`, "
               "написанные целиком большими буквами (метод `.upper()`). Порядок гостей сохрани.",
               "Выведи этот список через `print`.",
               "Следующей строкой выведи строку вида `At this table: 3` — сколько гостей сядет за стол."],
        hint="Проверить первую букву можно методом `.startswith(letter)` или сравнением `name[0] == letter`. "
             "Слева от `for` пишут, что положить в список (имя большими буквами), справа после `if` — кого брать.",
        solution='signs = [name.upper() for name in guests if name.startswith(letter)]\nprint(signs)\n'
                 'print(f"At this table: {len(signs)}")',
        wrong=[("забыл условие — таблички печатаются для всех гостей",
                'signs = [name.upper() for name in guests]\nprint(signs)\nprint(f"At this table: {len(signs)}")'),
               ("не переводит имена в большие буквы",
                'signs = [name for name in guests if name.startswith(letter)]\nprint(signs)\n'
                'print(f"At this table: {len(signs)}")')],
        constructs=["list"],
        must_use=[NEED_LISTCOMP],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-comp-exam-results", title="Кто сдал экзамен",
        given=["results", "pass_mark"],
        variants=[{"results": '["Anya:72", "Boris:45", "Vika:100", "Gleb:60"]', "pass_mark": "60"},
                  {"results": '["Oleg:9", "Mila:85", "Timur:50", "Sonya:51"]', "pass_mark": "51"},
                  {"results": '["Kira:30", "Lev:100", "Nina:99", "Petr:7", "Rita:64"]', "pass_mark": "65"}],
        hidden=[{"results": '["Ada:5"]', "pass_mark": "10"},
                {"results": '["Ben:100", "Cid:20", "Dan:3"]', "pass_mark": "4"},
                {"results": '["Eva:70", "Fil:70", "Gosha:69"]', "pass_mark": "70"},
                {"results": '["Ira:8", "Yan:80", "Zoya:100"]', "pass_mark": "9"}],
        intro="Результаты экзамена пришли из системы строками вида `\"Anya:72\"`: имя, двоеточие и баллы. Все строки "
              "лежат в списке `results`. Экзамен сдан, если баллов не меньше `pass_mark`.",
        steps=["Первым генератором списка собери список баллов всех учеников — целыми числами. Строку можно разрезать "
               "по двоеточию методом `.split(\":\")`: вторая часть — баллы, преврати её в число через `int()`.",
               "Вторым генератором списка с условием собери имена тех, у кого баллов не меньше `pass_mark`. Порядок сохрани.",
               "Выведи список имён сдавших через `print`.",
               "Следующей строкой выведи строку вида `Best score: 95` — самый большой балл из первого списка (функция `max()`)."],
        hint="`\"Anya:72\".split(\":\")` даёт список `[\"Anya\", \"72\"]`: имя — элемент с индексом 0, баллы — с индексом 1. "
             "Баллы обязательно переводи в числа: строки сравниваются по буквам, и `\"100\"` для них меньше, чем `\"45\"`.",
        solution='scores = [int(line.split(":")[1]) for line in results]\n'
                 'passed = [line.split(":")[0] for line in results if int(line.split(":")[1]) >= pass_mark]\n'
                 'print(passed)\nprint(f"Best score: {max(scores)}")',
        wrong=[("сравнивает баллы строками — «100» оказывается меньше «45», а «9» больше «51»",
                'scores = [line.split(":")[1] for line in results]\n'
                'passed = [line.split(":")[0] for line in results if line.split(":")[1] >= str(pass_mark)]\n'
                'print(passed)\nprint(f"Best score: {max(scores)}")'),
               ("строгое сравнение — ровно pass_mark баллов не считается сдачей",
                'scores = [int(line.split(":")[1]) for line in results]\n'
                'passed = [line.split(":")[0] for line in results if int(line.split(":")[1]) > pass_mark]\n'
                'print(passed)\nprint(f"Best score: {max(scores)}")')],
        constructs=["list"],
        must_use=[NEED_LISTCOMP],
    ),
]
