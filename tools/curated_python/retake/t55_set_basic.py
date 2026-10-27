"""PY_SET_BASIC — «Множества set». Taught before: everything up to tuples (conditions, loops, lists and their methods,
slices, string methods, functions, classes, tuples). Here: set() for removing repeats, `in`, add, union/intersection/
difference. Sets are never printed or iterated for output directly (their order is not fixed): sorted() or len().
Not yet: dicts, comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_SET_BASIC"

TURNSTILE = """\
inside = set()
visitors = set()
for event in events:
    action, name = event.split()
    if action == "in":
        if name in inside:
            print(f"{name} is already inside")
        else:
            inside.add(name)
            visitors.add(name)
    else:
        if name in inside:
            inside = inside - {name}
        else:
            print(f"{name} was not inside")
print("Inside:", sorted(inside))
print(f"Visitors today: {len(visitors)}")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-set-rt-delivery-cities", title="Города доставки",
        given=["deliveries", "home"],
        variants=[{"deliveries": '["Kazan", "Sochi", "Kazan", "Omsk", "Sochi", "Kazan"]', "home": '"Omsk"'},
                  {"deliveries": '["Perm", "Tula", "Perm", "Perm"]', "home": '"Kazan"'},
                  {"deliveries": '["Ufa", "Tver", "Orel", "Ufa", "Kursk", "Tver", "Orel"]', "home": '"Tver"'}],
        hidden=[{"deliveries": '["Sochi"]', "home": '"Sochi"'},
                {"deliveries": '["Omsk", "Omsk", "Omsk"]', "home": '"Tomsk"'},
                {"deliveries": '["Penza", "Vologda", "Anapa", "Kirov"]', "home": '"Kirov"'}],
        intro="Интернет-магазин записывает в список `deliveries` город каждой доставки за неделю, поэтому один город "
              "встречается там много раз. Начальнику нужен список разных городов и ответ, возили ли что-нибудь "
              "в город `home`.",
        steps=["Преврати список `deliveries` в множество с помощью `set()` — повторы исчезнут.",
               "Выведи строку вида `Cities: 3` — сколько разных городов в множестве.",
               "Следующей строкой выведи эти города в алфавитном порядке через запятую и пробел, например "
               "`Kazan, Omsk, Sochi`. Множество сначала отсортируй функцией `sorted()`, а потом склей через "
               "`\", \".join(...)`.",
               "Последней строкой выведи `Delivered to Omsk: yes`, если город `home` есть в множестве, иначе "
               "строку вида `Delivered to Omsk: no` — с названием города `home`."],
        hint="Проверка `x in s` для множества пишется так же, как для списка. У множества нет порядка, поэтому печатать "
             "его нужно только после `sorted()`, а число элементов узнают через `len()`.",
        solution='cities = set(deliveries)\nprint(f"Cities: {len(cities)}")\nprint(", ".join(sorted(cities)))\n'
                 'if home in cities:\n    print(f"Delivered to {home}: yes")\nelse:\n    print(f"Delivered to {home}: no")',
        wrong=[("считает все доставки, а не разные города",
                'cities = set(deliveries)\nprint(f"Cities: {len(deliveries)}")\nprint(", ".join(sorted(cities)))\n'
                'if home in cities:\n    print(f"Delivered to {home}: yes")\nelse:\n    print(f"Delivered to {home}: no")'),
               ("сортирует исходный список — города повторяются",
                'cities = set(deliveries)\nprint(f"Cities: {len(cities)}")\nprint(", ".join(sorted(deliveries)))\n'
                'if home in cities:\n    print(f"Delivered to {home}: yes")\nelse:\n    print(f"Delivered to {home}: no")')],
        must_use=[("re:\\bset\\(", "Убери повторы с помощью множества: set(deliveries) оставит каждый город один раз.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-set-rt-password-check", title="Проверка пароля",
        given=["password"],
        variants=[{"password": '"abc12abc"'}, {"password": '"secret2026x"'}, {"password": '"qwertyuiop"'}],
        hidden=[{"password": '"aaaaaaa1"'}, {"password": '"abcdefg1"'}, {"password": '"abcdefgh"'},
                {"password": '"9876543210"'}, {"password": '"x7y7z7w7v7"'}],
        intro="Сайт проверяет пароль `password`. Надёжным он считает пароль, в котором не меньше 8 разных символов "
              "и есть хотя бы одна цифра. Повторы не помогают: в пароле `aaaaaaaa` всего один разный символ.",
        steps=["Преврати `password` в множество символов с помощью `set()` и выведи строку вида `Different symbols: 5`.",
               "Найди цифры, которые есть в пароле: пересечение множества символов пароля и множества "
               "`set(\"0123456789\")`. Выведи через `print` слово `Digits:` и через пробел этот набор цифр, "
               "отсортированный функцией `sorted()`, например `Digits: ['1', '2']`.",
               "Последней строкой выведи `Strong password`, если разных символов 8 или больше и в пароле есть хотя бы "
               "одна цифра, иначе `Weak password`."],
        hint="`a & b` — элементы, которые есть в обоих множествах. Если цифр в пароле нет, пересечение пустое, "
             "и его длина равна 0. Ровно 8 разных символов — это уже достаточно.",
        solution='symbols = set(password)\nprint(f"Different symbols: {len(symbols)}")\n'
                 'digits = symbols & set("0123456789")\nprint("Digits:", sorted(digits))\n'
                 'if len(symbols) >= 8 and len(digits) > 0:\n    print("Strong password")\nelse:\n'
                 '    print("Weak password")',
        wrong=[("считает длину пароля, а не число разных символов",
                'symbols = set(password)\nprint(f"Different symbols: {len(password)}")\n'
                'digits = symbols & set("0123456789")\nprint("Digits:", sorted(digits))\n'
                'if len(password) >= 8 and len(digits) > 0:\n    print("Strong password")\nelse:\n'
                '    print("Weak password")'),
               ("не проверяет, есть ли в пароле цифра",
                'symbols = set(password)\nprint(f"Different symbols: {len(symbols)}")\n'
                'digits = symbols & set("0123456789")\nprint("Digits:", sorted(digits))\n'
                'if len(symbols) >= 8:\n    print("Strong password")\nelse:\n'
                '    print("Weak password")'),
               ("требует больше 8 разных символов — ровно 8 считает слабым паролем",
                'symbols = set(password)\nprint(f"Different symbols: {len(symbols)}")\n'
                'digits = symbols & set("0123456789")\nprint("Digits:", sorted(digits))\n'
                'if len(symbols) > 8 and len(digits) > 0:\n    print("Strong password")\nelse:\n'
                '    print("Weak password")')],
        constructs=["if"],
        must_use=[("re:\\bset\\(", "Собери символы пароля в множество через set(): так повторы не посчитаются.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-set-rt-turnstile", title="Турникет в спортзале",
        given=["events"],
        variants=[{"events": '["in Anya", "in Boris", "out Anya", "in Vera", "in Boris", "out Gleb", "in Anya"]'},
                  {"events": '["out Dina", "in Egor", "in Dina", "out Egor", "out Egor"]'},
                  {"events": '["in Lev", "in Mila", "in Nik", "out Mila", "out Lev", "in Mila", "in Mila"]'}],
        hidden=[{"events": '["in Ira"]'},
                {"events": '["out Oleg"]'},
                {"events": '["in Pasha", "out Pasha", "in Pasha", "out Pasha"]'},
                {"events": '["in Rita", "in Sava", "in Rita", "out Tima", "out Sava", "in Uma"]'}],
        intro="Турникет спортзала записывает события в список `events`: строка `in Anya` значит, что Аня вошла, "
              "а `out Anya` — что вышла. Иногда турникет ошибается и записывает лишнее событие. Нужно понять, "
              "кто сейчас в зале и сколько разных людей сегодня приходило.",
        steps=["Создай два пустых множества: `inside` — кто сейчас в зале, и `visitors` — кто сегодня хоть раз входил.",
               "Пройди по `events`. Каждую строку разбей методом `.split()` и распакуй в две переменные: действие и имя.",
               "Если действие `in`: когда человек уже в `inside`, выведи строку вида `Boris is already inside`; иначе "
               "добавь его методом `.add()` и в `inside`, и в `visitors`.",
               "Если действие `out`: когда человек есть в `inside`, убери его оттуда разностью множеств — "
               "`inside = inside - {{name}}`; иначе выведи строку вида `Gleb was not inside`.",
               "После цикла выведи через `print` слово `Inside:` и через пробел отсортированный функцией `sorted()` "
               "список тех, кто в зале, например `Inside: ['Boris', 'Vera']`, а последней строкой — строку вида "
               "`Visitors today: 3`."],
        hint="`{{name}}` — это множество из одного элемента, и `inside - {{name}}` даёт новое множество без этого человека. "
             "`visitors` только растёт: тот, кто вошёл, вышел и вошёл снова, — всё равно один посетитель.",
        solution=TURNSTILE,
        wrong=[("не проверяет, в зале ли уже человек, — повторный вход не замечает",
                TURNSTILE.replace("        if name in inside:\n            print(f\"{name} is already inside\")\n"
                                  "        else:\n            inside.add(name)\n            visitors.add(name)\n",
                                  "        inside.add(name)\n        visitors.add(name)\n")),
               ("при выходе убирает человека и из посетителей — посетителей получается меньше",
                TURNSTILE.replace("            inside = inside - {name}\n",
                                  "            inside = inside - {name}\n            visitors = visitors - {name}\n")),
               ("при выходе не проверяет, был ли человек в зале, — ошибку турникета не замечает",
                TURNSTILE.replace("        if name in inside:\n            inside = inside - {name}\n"
                                  "        else:\n            print(f\"{name} was not inside\")\n",
                                  "        inside = inside - {name}\n"))],
        constructs=["for", "if"],
        must_use=[("re:\\bset\\(", "Создай пустые множества через set(): пустые фигурные скобки {} — это не множество."),
                  ("re:\\.add\\(", "Добавляй людей в множество методом .add().")],
    ),
]
