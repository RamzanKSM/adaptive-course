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
]
