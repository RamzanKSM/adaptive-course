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
]
