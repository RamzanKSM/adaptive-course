"""PY_COLLECTION_SELECTION — «Выбор коллекции». Taught before: lists and their methods, tuples, sets, dicts, loops,
conditions, functions, classes. Here: the statement describes what the data must do (no repeats and fast `in` →
set; lookup by key → dict; keep order and repeats → list; fixed records → tuple) and the student picks the
collection; the structure check names the right one and says why. Not yet: comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_COLLECTION_SELECTION"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-sel-free-login", title="Свободен ли логин",
        given=["attempts", "login"],
        variants=[{"attempts": '["anna", "max", "anna", "kit", "max", "anna", "zoe"]', "login": '"kit"'},
                  {"attempts": '["sun", "moon", "star", "sun"]', "login": '"sky"'},
                  {"attempts": '["dima", "dima", "lena", "olga", "lena", "ivan"]', "login": '"olga"'}],
        hidden=[{"attempts": '["a1"]', "login": '"a1"'},
                {"attempts": '["x", "y", "z", "x", "y", "z", "x", "y"]', "login": '"w"'},
                {"attempts": '["neo", "trinity", "neo"]', "login": '"neo"'}],
        intro="Сайт игрового клуба регистрирует новых игроков. В список `attempts` записаны логины из всех попыток "
              "регистрации — некоторые ребята нажимали кнопку по несколько раз, поэтому логины повторяются. "
              "Ещё один игрок хочет взять логин `login`.",
        steps=["Выведи строку вида `Total tries: 10` — сколько всего было попыток регистрации.",
               "Сложи логины в такую коллекцию, которая сама избавляется от повторов и быстро отвечает на вопрос "
               "«есть ли в ней такой элемент?». Выведи строку вида `Different logins: 5` — сколько в ней элементов.",
               "Проверь, есть ли `login` в этой коллекции, и выведи сам логин, двоеточие, пробел и слово `taken`, "
               "если такой логин уже есть, или `free`, если его нет. Например: `petya: taken`."],
        hint="Вспомни четыре коллекции. Список и кортеж хранят всё подряд, вместе с повторами; словарь хранит пары "
             "«ключ — значение»; а ещё одна коллекция хранит каждый элемент только один раз.",
        solution='print(f"Total tries: {len(attempts)}")\ntaken = set(attempts)\nprint(f"Different logins: {len(taken)}")\n'
                 'if login in taken:\n    print(f"{login}: taken")\nelse:\n    print(f"{login}: free")',
        wrong=[("оставляет логины в списке — повторы считаются несколько раз",
                'print(f"Total tries: {len(attempts)}")\nprint(f"Different logins: {len(attempts)}")\n'
                'if login in attempts:\n    print(f"{login}: taken")\nelse:\n    print(f"{login}: free")'),
               ("сразу превращает попытки в множество — и в числе попыток теряются повторы",
                'taken = set(attempts)\nprint(f"Total tries: {len(taken)}")\nprint(f"Different logins: {len(taken)}")\n'
                'if login in taken:\n    print(f"{login}: taken")\nelse:\n    print(f"{login}: free")')],
        constructs=["if"],
        must_use=[("re:\\bset\\(", "Для уникальных логинов выбери множество set: оно само убирает повторы "
                                   "и быстро проверяет, есть ли в нём элемент.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-sel-airport-codes", title="Коды аэропортов",
        given=["codes", "cities", "route"],
        variants=[{"codes": '["SVO", "LED", "KZN", "AER"]', "cities": '["Moscow", "Saint Petersburg", "Kazan", "Sochi"]',
                   "route": '["LED", "SVO", "AER", "SVO"]'},
                  {"codes": '["OVB", "KJA", "IKT"]', "cities": '["Novosibirsk", "Krasnoyarsk", "Irkutsk"]',
                   "route": '["IKT", "OVB", "KJA"]'},
                  {"codes": '["KGD", "MMK", "SVX", "LED", "UFA"]',
                   "cities": '["Kaliningrad", "Murmansk", "Yekaterinburg", "Saint Petersburg", "Ufa"]',
                   "route": '["SVX", "UFA", "SVX", "MMK", "KGD"]'}],
        hidden=[{"codes": '["AAA", "BBB"]', "cities": '["Alpha", "Beta"]', "route": '["BBB", "AAA", "BBB"]'},
                {"codes": '["KZN", "AER", "SVO"]', "cities": '["Kazan", "Sochi", "Moscow"]',
                 "route": '["SVO", "AER", "KZN", "SVO", "AER"]'},
                {"codes": '["MRV", "ROV", "KRR", "VOG"]', "cities": '["Mineralnye Vody", "Rostov", "Krasnodar", "Volgograd"]',
                 "route": '["VOG"]'}],
        intro="Авиакомпания хранит коды аэропортов и названия городов в двух списках: `codes` и `cities`. "
              "Код и его город стоят на одинаковых местах: `codes[0]` — это город `cities[0]` и так далее. "
              "Маршрут путешественника записан кодами в списке `route`, а на табло нужны названия городов.",
        steps=["Собери из `codes` и `cities` такую коллекцию, в которой по коду аэропорта можно сразу получить "
               "название города, не перебирая списки каждый раз.",
               "Пройди по списку `route` и для каждого кода выведи название города — каждое на отдельной строке, "
               "в порядке маршрута."],
        hint="Нужна коллекция, которая хранит пары «ключ — значение» и по ключу сразу отдаёт значение. "
             "Заполнить её удобно циклом по индексам `for i in range(len(codes)):` — на каждом шаге `codes[i]` "
             "и `cities[i]` образуют одну пару.",
        solution="city_of = {}\nfor i in range(len(codes)):\n    city_of[codes[i]] = cities[i]\nfor code in route:\n    print(city_of[code])",
        wrong=[("берёт города по номеру в маршруте, а не по коду",
                "for i in range(len(route)):\n    print(cities[i])"),
               ("перепутал ключи и значения — по коду ничего не находится",
                "city_of = {}\nfor i in range(len(codes)):\n    city_of[cities[i]] = codes[i]\nfor code in route:\n    print(city_of.get(code))")],
        constructs=["dict", "for"],
        must_use=[("Dict", "Для поиска города по коду выбери словарь: создай его фигурными скобками {} и заполни парами "
                           "«код — город». Тогда город находится по коду сразу, без перебора списка.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-sel-olympiad-schools", title="Участники по школам",
        given=["entries"],
        variants=[{"entries": '[("Ivanov", 57), ("Petrova", 1543), ("Sidorov", 57), ("Kozlova", 2), ("Morozov", 1543)]'},
                  {"entries": '[("Orlova", 12), ("Belov", 5), ("Zaitseva", 5), ("Kim", 30), ("Lebedev", 12), ("Nosova", 5)]'},
                  {"entries": '[("Volkov", 239), ("Egorova", 30), ("Popov", 239), ("Titova", 239)]'}],
        hidden=[{"entries": '[("Gusev", 1)]'},
                {"entries": '[("Zhukov", 3), ("Ershova", 2), ("Nosov", 1), ("Pavlov", 2)]'},
                {"entries": '[("Sokolov", 10), ("Fedorova", 10), ("Yakovleva", 10)]'}],
        intro="На олимпиаду записываются ученики из разных школ. Каждая запись в списке `entries` — кортеж "
              "из фамилии участника и номера его школы. Записи идут в порядке регистрации. "
              "Организаторам нужен список участников по каждой школе.",
        steps=["Выбери коллекцию, в которой по номеру школы можно хранить и сразу находить список её участников, "
               "и заполни её, пройдя по `entries`. Фамилии внутри каждой школы должны идти в порядке регистрации.",
               "Для каждой школы выведи строку вида `School 8: Smirnov, Kuznetsova` — слово `School`, номер, двоеточие "
               "и фамилии через запятую с пробелом. Школы выводи в том порядке, в котором они впервые встречаются в `entries`.",
               "Последней строкой выведи строку вида `Total schools: 6` — сколько разных школ участвует."],
        hint="Значением в паре «ключ — значение» может быть и список. Когда школа встречается впервые, заведи для неё "
             'пустой список, а дальше добавляй в него фамилии через `.append()`. Склеить фамилии поможет `", ".join(...)`.',
        solution='by_school = {}\nfor surname, school in entries:\n    if school not in by_school:\n        by_school[school] = []\n'
                 '    by_school[school].append(surname)\nfor school, surnames in by_school.items():\n'
                 '    names = ", ".join(surnames)\n    print(f"School {school}: {names}")\nprint(f"Total schools: {len(by_school)}")',
        wrong=[("перебирает школы через отсортированное множество — порядок первой регистрации теряется",
                'schools = []\nfor surname, school in entries:\n    schools.append(school)\nfor school in sorted(set(schools)):\n'
                '    found = []\n    for surname, number in entries:\n        if number == school:\n            found.append(surname)\n'
                '    names = ", ".join(found)\n    print(f"School {school}: {names}")\nprint(f"Total schools: {len(set(schools))}")'),
               ("каждый раз записывает в словарь новый список — у школы остаётся только последний участник",
                'by_school = {}\nfor surname, school in entries:\n    by_school[school] = [surname]\n'
                'for school, surnames in by_school.items():\n    names = ", ".join(surnames)\n    print(f"School {school}: {names}")\n'
                'print(f"Total schools: {len(by_school)}")')],
        constructs=["dict", "for"],
        must_use=[("Dict", "Сгруппируй участников в словаре: ключ — номер школы, значение — список фамилий. "
                           "Словарь помнит порядок, в котором добавлялись школы, и сразу находит нужную.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-sel-rgb-color", title="Цвет из трёх чисел",
        given=["red", "green", "blue"],
        variants=[{"red": "255", "green": "128", "blue": "0"},
                  {"red": "120", "green": "120", "blue": "120"},
                  {"red": "0", "green": "200", "blue": "255"}],
        hidden=[{"red": "0", "green": "0", "blue": "0"},
                {"red": "10", "green": "10", "blue": "11"},
                {"red": "77", "green": "50", "blue": "77"},
                {"red": "200", "green": "30", "blue": "60"}],
        intro="Графический редактор хранит цвет как три числа от 0 до 255: сколько в нём красного `red`, зелёного `green` "
              "и синего `blue`. Цвет — это одна запись: порядок чисел важен, их всегда ровно три, и после того как цвет "
              "выбран, менять его отдельные части программа не должна.",
        steps=["Сложи три числа в порядке красный, зелёный, синий в такую коллекцию, которая хранит порядок, "
               "а изменить её после создания нельзя. Сохрани её в переменную `color`.",
               "Выведи строку вида `Color: (10, 20, 30)` — после двоеточия и пробела сама коллекция `color`.",
               "Следующей строкой выведи `Shade of gray`, если все три числа в `color` равны, иначе `Colored`. "
               "Числа бери из `color` по индексам."],
        hint="Список тоже хранит порядок, но его можно случайно изменить: `color[0] = 0`. Вспомни коллекцию, которая "
             "пишется в круглых скобках и после создания не меняется.",
        solution='color = (red, green, blue)\nprint(f"Color: {color}")\nif color[0] == color[1] and color[1] == color[2]:\n'
                 '    print("Shade of gray")\nelse:\n    print("Colored")',
        wrong=[("складывает цвет в список — печатаются квадратные скобки",
                'color = [red, green, blue]\nprint(f"Color: {color}")\nif color[0] == color[1] and color[1] == color[2]:\n'
                '    print("Shade of gray")\nelse:\n    print("Colored")'),
               ("сравнивает только красный и зелёный — синий не проверяется",
                'color = (red, green, blue)\nprint(f"Color: {color}")\nif color[0] == color[1]:\n'
                '    print("Shade of gray")\nelse:\n    print("Colored")')],
        constructs=["if"],
        must_use=[("Tuple", "Для цвета выбери кортеж: (red, green, blue). Он хранит порядок трёх чисел, "
                            "а изменить его после создания нельзя.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-sel-chat-feed", title="Лента чата",
        given=["chat"],
        variants=[{"chat": '[("Anya", "hi"), ("Boris", "hello"), ("Anya", "who is coming?"), ("Vika", "me"), ("Boris", "me too")]'},
                  {"chat": '[("Oleg", "ready?"), ("Oleg", "start"), ("Mila", "go"), ("Oleg", "ok")]'},
                  {"chat": '[("Kira", "lunch?"), ("Lev", "yes"), ("Kira", "where"), ("Nina", "cafe"), ("Lev", "fine"), '
                           '("Kira", "at 2")]'}],
        hidden=[{"chat": '[("Zoya", "hey")]'},
                {"chat": '[("Ada", "a"), ("Ben", "b"), ("Cid", "c"), ("Dan", "d"), ("Eva", "e")]'},
                {"chat": '[("Max", "one"), ("Max", "two"), ("Max", "three"), ("Max", "four")]'}],
        intro="В групповом чате сообщения записаны в список `chat` в порядке отправки. Каждое сообщение — кортеж "
              "из имени автора и текста. Один человек может написать много сообщений. Под окном чата нужно показать "
              "три последних сообщения и сколько разных людей писало в чат.",
        steps=["Выведи три последних сообщения ленты в порядке отправки — каждое строкой вида `Anya: hi`. Если сообщений "
               "меньше трёх, выведи все. Порядок и повторы авторов здесь важны.",
               "Собери авторов всех сообщений в такую коллекцию, которая сама избавляется от повторов.",
               "Последней строкой выведи строку вида `Authors: 4` — сколько разных людей писало в чат."],
        hint="Лента уже хранится в списке — он помнит порядок, и срез `[-3:]` даёт последние три элемента (или все, если "
             "их меньше). А для подсчёта разных авторов подойдёт коллекция, в которой каждый элемент хранится один раз.",
        solution='for author, text in chat[-3:]:\n    print(f"{author}: {text}")\nauthors = set()\nfor author, text in chat:\n'
                 '    authors.add(author)\nprint(f"Authors: {len(authors)}")',
        wrong=[("считает авторов по числу сообщений — повторы учитываются",
                'for author, text in chat[-3:]:\n    print(f"{author}: {text}")\nprint(f"Authors: {len(chat)}")\nauthors = set()'),
               ("берёт три первых сообщения вместо трёх последних",
                'for author, text in chat[:3]:\n    print(f"{author}: {text}")\nauthors = set()\nfor author, text in chat:\n'
                '    authors.add(author)\nprint(f"Authors: {len(authors)}")')],
        constructs=["for"],
        must_use=[("re:\\bset\\(", "Для разных авторов выбери множество set: каждый автор попадёт в него только один раз.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-sel-office-pass", title="Пропуска в офис",
        given=["cards", "scans"],
        variants=[{"cards": '[(12, "Anya"), (34, "Boris"), (56, "Vika")]', "scans": "[12, 34, 77, 12, 56, 34, 12]"},
                  {"cards": '[(1, "Oleg"), (2, "Mila")]', "scans": "[2, 2, 2, 5, 1]"},
                  {"cards": '[(101, "Kira"), (202, "Lev"), (303, "Nina"), (404, "Petr")]', "scans": "[303, 404, 303, 999, 101]"}],
        hidden=[{"cards": '[(7, "Zoya")]', "scans": "[7]"},
                {"cards": '[(1, "Ada"), (2, "Ben")]', "scans": "[3, 4]"},
                {"cards": '[(5, "Max"), (6, "Eva")]', "scans": "[5, 6, 6, 5, 6, 5, 8]"}],
        intro="На входе в офис стоит турникет. Сотрудники записаны в список `cards`: каждая запись — кортеж из номера "
              "пропуска и имени. В списке `scans` — номера пропусков в том порядке, в котором их прикладывали к турникету. "
              "Первое прикладывание — человек входит, следующее — выходит, потом снова входит и так далее.",
        steps=["Собери из `cards` коллекцию, в которой по номеру пропуска сразу находится имя сотрудника.",
               "Заведи коллекцию для тех, кто сейчас в офисе: в ней нужно только быстро проверять, есть ли там человек, "
               "добавлять и убирать его; повторов в ней быть не может.",
               "Пройди по `scans`. Если такого пропуска нет среди сотрудников, выведи строку вида `Card 77: denied`. "
               "Если человек сейчас в офисе, выведи строку вида `Card 12: goodbye, Anya` и убери его из тех, кто внутри; "
               "иначе выведи `Card 12: welcome, Anya` и добавь его.",
               "Последней строкой выведи строку вида `Inside: 2` — сколько людей осталось в офисе."],
        hint="Имя по номеру удобно искать в словаре: ключ — номер пропуска, значение — имя. А тех, кто внутри, удобно "
             "хранить в множестве: `.add(x)` добавляет элемент, `.remove(x)` убирает его, `x in inside` проверяет.",
        solution='names = {}\nfor number, name in cards:\n    names[number] = name\ninside = set()\nfor card in scans:\n'
                 '    if card not in names:\n        print(f"Card {card}: denied")\n    elif card in inside:\n'
                 '        print(f"Card {card}: goodbye, {names[card]}")\n        inside.remove(card)\n    else:\n'
                 '        print(f"Card {card}: welcome, {names[card]}")\n        inside.add(card)\nprint(f"Inside: {len(inside)}")',
        wrong=[("не убирает вышедших — каждый следующий проход считается выходом",
                'names = {}\nfor number, name in cards:\n    names[number] = name\ninside = set()\nfor card in scans:\n'
                '    if card not in names:\n        print(f"Card {card}: denied")\n    elif card in inside:\n'
                '        print(f"Card {card}: goodbye, {names[card]}")\n    else:\n'
                '        print(f"Card {card}: welcome, {names[card]}")\n        inside.add(card)\nprint(f"Inside: {len(inside)}")'),
               ("впускает и незнакомые пропуска — проверка сотрудников пропущена",
                'names = {}\nfor number, name in cards:\n    names[number] = name\ninside = set()\nfor card in scans:\n'
                '    if card in inside:\n        print(f"Card {card}: goodbye, {names.get(card)}")\n        inside.remove(card)\n'
                '    else:\n        print(f"Card {card}: welcome, {names.get(card)}")\n        inside.add(card)\n'
                'print(f"Inside: {len(inside)}")')],
        constructs=["dict", "for"],
        must_use=[("Dict", "Для поиска имени по номеру пропуска выбери словарь: создай его фигурными скобками {} "
                           "и заполни парами «номер — имя»."),
                  ("re:\\bset\\(", "Для тех, кто в офисе, выбери множество set(): оно быстро проверяет, есть ли в нём "
                                       "человек, и не хранит повторов.")],
    ),
]
