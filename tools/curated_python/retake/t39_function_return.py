"""PY_FUNCTION_RETURN — «return и print». Taught before: everything up to functions that print (conditions, loops,
lists, slices, string methods, def with parameters). Here: return a value instead of printing it. Not yet: default
values and keyword arguments."""
from build import FunctionTask

SKILL = "PY_FUNCTION_RETURN"

TASKS = [
    FunctionTask(
        skill=SKILL, difficulty=1, slug="py-ret-rt-bonus-points", title="Бонусные баллы за покупку",
        function="bonus",
        variants=[{"step": 100}, {"step": 50}, {"step": 30}],
        intro="Магазин начисляет 1 бонусный балл за каждые полные {step} руб. в чеке. Касса вызывает функцию, "
              "чтобы узнать, сколько баллов добавить на карту покупателя, — поэтому функция должна вернуть число, "
              "а не напечатать его.",
        steps=["Допиши функцию `bonus(amount)`: параметр `amount` — сумма покупки в рублях (целое число).",
               "Функция должна вернуть через `return` число баллов целым числом: сколько раз {step} помещается "
               "в `amount` целиком. Неполные {step} руб. баллов не дают."],
        hint="Сколько раз число помещается целиком, считает деление нацело `//`. Обычное деление `/` даст дробное "
             "число. А `print` только показывает число на экране — тому, кто вызвал функцию, его отдаёт `return`.",
        starter="def bonus(amount):\n    # Напиши решение здесь\n    pass\n",
        solution="def bonus(amount):\n    return amount // {step}\n",
        inputs=["250", "1000", "29", "0", "470", "1234"],
        wrong=[("печатает баллы вместо return", "def bonus(amount):\n    print(amount // {step})\n"),
               ("делит через / — получается дробное число", "def bonus(amount):\n    return amount / {step}\n")],
    ),
    FunctionTask(
        skill=SKILL, difficulty=2, slug="py-ret-rt-movie-length", title="Длительность сеанса",
        function="show_length",
        variants=[{"ads": 15}, {"ads": 10}, {"ads": 20}],
        intro="В кинотеатре перед каждым фильмом {ads} минут показывают рекламу. На сайте у сеанса пишут, сколько он "
              "длится вместе с рекламой, в часах и минутах. Строку для сайта собирает функция, а показывает её "
              "другая часть программы — поэтому строку нужно вернуть.",
        steps=["Допиши функцию `show_length(minutes)`: `minutes` — длина фильма в минутах (целое число).",
               "Прибавь к длине фильма {ads} минут рекламы и раздели результат на полные часы и оставшиеся минуты.",
               "Верни строку вида `2 h 5 min`: число часов, пробел, `h`, пробел, число минут, пробел, `min`. "
               "Посмотри на примеры ниже."],
        hint="Полные часы — это `total // 60`, а оставшиеся минуты — остаток `total % 60`. "
             "Удобно собрать строку в f-строке и вернуть её через `return`.",
        starter="def show_length(minutes):\n    # Напиши решение здесь\n    pass\n",
        solution='def show_length(minutes):\n    total = minutes + {ads}\n    return f"{{total // 60}} h {{total % 60}} min"\n',
        inputs=["120", "95", "40", "165", "45", "200"],
        wrong=[("печатает строку вместо return",
                'def show_length(minutes):\n    total = minutes + {ads}\n    print(f"{{total // 60}} h {{total % 60}} min")\n'),
               ("забыл прибавить рекламу",
                'def show_length(minutes):\n    return f"{{minutes // 60}} h {{minutes % 60}} min"\n')],
    ),
    FunctionTask(
        skill=SKILL, difficulty=3, slug="py-ret-rt-password-points", title="Насколько надёжен пароль",
        function="password_points",
        variants=[{"length": 8}, {"length": 10}, {"length": 6}],
        intro="Сайт при регистрации оценивает пароль баллами от 0 до 3 и по ним рисует полоску надёжности. "
              "Баллы считает твоя функция и возвращает их сайту.",
        steps=["Допиши функцию `password_points(password)`: `password` — пароль (строка из английских букв и цифр). "
               "Функция возвращает число баллов.",
               "1 балл, если в пароле {length} символов или больше.",
               "Ещё 1 балл, если в пароле есть хотя бы одна цифра — сколько бы цифр ни было, балл за них один.",
               "Ещё 1 балл, если в пароле есть хотя бы одна заглавная буква. Верни сумму баллов через `return`."],
        hint="Цифру удобно искать циклом по символам: `ch in \"0123456789\"`. Запомни в переменной, что цифра нашлась, "
             "а балл прибавь уже после цикла. Заглавная буква есть, если `password.lower()` не равно `password`.",
        starter="def password_points(password):\n    # Напиши решение здесь\n    pass\n",
        solution='def password_points(password):\n    points = 0\n    if len(password) >= {length}:\n        points += 1\n'
                 '    has_digit = False\n    for ch in password:\n        if ch in "0123456789":\n            has_digit = True\n'
                 '    if has_digit:\n        points += 1\n    if password.lower() != password:\n        points += 1\n'
                 '    return points\n',
        inputs=['"cat"', '"Secret2026"', '"abcdefghij"', '"Abc1"', '"PASSWORD"', '"qwerty12345"', '"22"', '"Kazan"'],
        wrong=[("печатает баллы вместо return",
                'def password_points(password):\n    points = 0\n    if len(password) >= {length}:\n        points += 1\n'
                '    has_digit = False\n    for ch in password:\n        if ch in "0123456789":\n            has_digit = True\n'
                '    if has_digit:\n        points += 1\n    if password.lower() != password:\n        points += 1\n'
                '    print(points)\n'),
               ("прибавляет балл за каждую цифру, а не один раз",
                'def password_points(password):\n    points = 0\n    if len(password) >= {length}:\n        points += 1\n'
                '    for ch in password:\n        if ch in "0123456789":\n            points += 1\n'
                '    if password.lower() != password:\n        points += 1\n    return points\n')],
    ),
]
