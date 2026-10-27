"""PY_FUNCTION_PARAMETERS — «Параметры функций». Taught before: everything up to return (conditions, loops, lists,
slices, string methods, def, return). Here: several parameters, default values, keyword arguments."""
from build import FunctionTask

SKILL = "PY_FUNCTION_PARAMETERS"

TASKS = [
    FunctionTask(
        skill=SKILL, difficulty=1, slug="py-par-rt-free-seats", title="Свободные места в автобусах",
        function="free_seats",
        variants=[{"capacity": 40}, {"capacity": 30}, {"capacity": 52}],
        intro="Турфирма везёт группу на экскурсию на одинаковых автобусах, в каждом по {capacity} мест. "
              "Нужна функция, которая считает, сколько мест останется свободными.",
        steps=["Допиши функцию `free_seats(passengers, buses)`: `passengers` — сколько человек едет, "
               "`buses` — сколько автобусов заказано.",
               "Верни целым числом, сколько мест свободно: все места во всех автобусах ({capacity} в каждом) "
               "минус число пассажиров.",
               "Функцию вызывают и с именованными аргументами, например `free_seats(buses=2, passengers=55)`, "
               "поэтому не меняй названия и порядок параметров."],
        hint="При вызове с именами Python кладёт значение в параметр с таким же именем, в каком бы порядке их ни написали. "
             "Сначала посчитай, сколько мест всего: число автобусов, умноженное на {capacity}.",
        starter="def free_seats(passengers, buses):\n    # Напиши решение здесь\n    pass\n",
        solution="def free_seats(passengers, buses):\n    return buses * {capacity} - passengers\n",
        inputs=["25, 1", "buses=2, passengers=55", "80, 3", "passengers=0, buses=1", "45, 2", "buses=4, passengers=100"],
        public=3,
        wrong=[("переставил параметры местами: пассажиры и автобусы путаются",
                "def free_seats(buses, passengers):\n    return buses * {capacity} - passengers\n"),
               ("забыл умножить на число автобусов — считает места только в одном",
                "def free_seats(passengers, buses):\n    return {capacity} - passengers\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=2, slug="py-par-rt-test-percent", title="Процент за контрольную",
        function="percent",
        variants=[{"total": 40}, {"total": 50}, {"total": 20}],
        intro="Учитель переводит баллы за контрольную в проценты. Обычно в контрольной {total} баллов, "
              "но бывают и другие — тогда максимум передают в функцию отдельно. За бонусные задачи ученик может "
              "набрать больше максимума, но процент всё равно не бывает больше 100.",
        steps=["Допиши функцию `percent(points, total={total})`: `points` — сколько баллов набрал ученик, "
               "`total` — максимум баллов. Значение по умолчанию {total} уже стоит в заготовке.",
               "Посчитай процент: `points`, умноженное на 100 и делённое нацело на `total`.",
               "Если получилось больше 100, верни `100`, иначе верни посчитанный процент. Функцию вызывают и так: "
               "`percent(30)`, и так: `percent(9, 12)` или `percent(points=9, total=12)`."],
        hint="Внутри функции используй параметр `total`, а не число {total}: если максимум передали при вызове, "
             "в `total` окажется он. Умножай на 100 до деления, иначе `//` округлит почти всё до нуля.",
        starter="def percent(points, total={total}):\n    # Напиши решение здесь\n    pass\n",
        solution="def percent(points, total={total}):\n    result = points * 100 // total\n    if result > 100:\n"
                 "        return 100\n    return result\n",
        inputs=["15", "9, 12", "total=10, points=13", "0", "points=18", "7, total=7", "33, 60"],
        public=3,
        wrong=[("использует число из условия вместо параметра total — переданный максимум не учитывается",
                "def percent(points, total={total}):\n    result = points * 100 // {total}\n    if result > 100:\n"
                "        return 100\n    return result\n"),
               ("не ограничивает процент сотней — с бонусными баллами выходит больше 100",
                "def percent(points, total={total}):\n    return points * 100 // total\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=3, slug="py-par-rt-letter-count", title="Сколько раз встречается буква",
        function="count_letter",
        variants=[{"letter": "a"}, {"letter": "o"}, {"letter": "e"}],
        intro="Ты пишешь помощника для игры в слова: он считает, сколько раз в тексте встречается буква. "
              "Чаще всего спрашивают про букву `{letter}`, а иногда нужно не различать большие и маленькие буквы.",
        steps=["Допиши функцию `count_letter(text, letter=\"{letter}\", ignore_case=False)`: `text` — текст, "
               "`letter` — какую букву искать (по умолчанию `{letter}`), `ignore_case` — не различать ли большие "
               "и маленькие буквы (по умолчанию различать).",
               "Обычно функция возвращает, сколько раз `letter` встречается в `text` ровно в таком виде: "
               "`A` и `a` — разные буквы.",
               "Если `ignore_case` равно `True`, большие и маленькие буквы считаются одинаковыми — и в тексте, "
               "и в самой букве `letter`.",
               "Функцию вызывают по-разному, например `count_letter(\"Kazan\", \"z\")` "
               "или `count_letter(\"Olga and Oleg\", letter=\"O\", ignore_case=True)`."],
        hint="Метод `text.count(letter)` считает, сколько раз `letter` встречается в `text`. Чтобы не различать "
             "большие и маленькие буквы, переведи в маленькие через `.lower()` и текст, и букву. "
             "Используй параметр `letter`, а не букву `{letter}` в кавычках.",
        starter="def count_letter(text, letter=\"{letter}\", ignore_case=False):\n    # Напиши решение здесь\n    pass\n",
        solution="def count_letter(text, letter=\"{letter}\", ignore_case=False):\n    if ignore_case:\n"
                 "        text = text.lower()\n        letter = letter.lower()\n    return text.count(letter)\n",
        inputs=['"an orange tree near the road"', '"Kazan", "z"', '"Olga and Oleg", letter="O", ignore_case=True',
                'text="Eva went to see Elena", ignore_case=True', '"AAA aa", "A"', '"too good to be true", "o", True',
                'letter="s", text="Sochi"'],
        public=3,
        wrong=[("всегда ищет букву по умолчанию — переданная буква не учитывается",
                "def count_letter(text, letter=\"{letter}\", ignore_case=False):\n    if ignore_case:\n"
                "        text = text.lower()\n    return text.count(\"{letter}\")\n"),
               ("переводит в маленькие только текст, а заглавную букву ищет как есть",
                "def count_letter(text, letter=\"{letter}\", ignore_case=False):\n    if ignore_case:\n"
                "        text = text.lower()\n    return text.count(letter)\n")],
    ),
]
