"""PY_DICT_BASIC — «Словари dict». Taught before: everything up to sets (conditions, loops, lists and their methods,
slices, string methods, functions, classes, tuples, sets). Here: d[key], .get(key, default), keys/values/items,
counting with a dict, adding and updating values. Dict order is insertion order, so printing in dict order is stable.
Not yet: comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_DICT_BASIC"

CIPHER = """\
result = ""
replaced = 0
for ch in message:
    result += code.get(ch, ch)
    if ch in code:
        replaced += 1
print(result)
print(f"Replaced: {replaced}")
"""

SQUADS = """\
squads = {}
for name, squad in kids:
    if squad not in squads:
        squads[squad] = []
    squads[squad].append(name)
biggest = ""
for squad, names in squads.items():
    print(f"{squad}: {', '.join(names)}")
    if biggest == "" or len(names) > len(squads[biggest]):
        biggest = squad
print(f"Biggest: {biggest} ({len(squads[biggest])})")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-dict-rt-pet-ages", title="Возраст питомцев",
        given=["pets", "name", "new_pet"],
        variants=[{"pets": '{"Rex": 3, "Murka": 5, "Kesha": 1}', "name": '"Murka"', "new_pet": '"Barsik"'},
                  {"pets": '{"Sharik": 7, "Polly": 2}', "name": '"Sharik"', "new_pet": '"Tuzik"'},
                  {"pets": '{"Luna": 4, "Tom": 9, "Bobik": 2, "Goldie": 1}', "name": '"Goldie"', "new_pet": '"Pushok"'}],
        hidden=[{"pets": '{"Kuzya": 0}', "name": '"Kuzya"', "new_pet": '"Ryzhik"'},
                {"pets": '{"Grom": 12, "Belka": 6, "Strelka": 6}', "name": '"Belka"', "new_pet": '"Zvezdochka"'},
                {"pets": '{"Snow": 3, "Leo": 8}', "name": '"Leo"', "new_pet": '"Mia"'}],
        intro="В ветеринарной клинике возраст питомцев хранится в словаре `pets`: ключ — кличка, значение — возраст "
              "в годах. У питомца `name` сегодня день рождения, а ещё в клинику впервые принесли котёнка `new_pet` — "
              "ему пока 0 лет.",
        steps=["Увеличь возраст питомца `name` в словаре на 1.",
               "Добавь в словарь новый ключ `new_pet` со значением 0.",
               "Выведи весь словарь командой `print(pets)`, а следующей строкой — строку вида `Pets: 4` с числом "
               "питомцев в словаре."],
        hint="К значению по ключу можно прибавить, как к обычной переменной: `d[key] += 1`. А запись `d[key] = value` "
             "с новым ключом добавляет в словарь новую пару — в конец. Число пар в словаре даёт `len()`.",
        solution='pets[name] += 1\npets[new_pet] = 0\nprint(pets)\nprint(f"Pets: {len(pets)}")',
        wrong=[("записывает возраст 1 вместо того, чтобы прибавить год",
                'pets[name] = 1\npets[new_pet] = 0\nprint(pets)\nprint(f"Pets: {len(pets)}")'),
               ("добавляет котёнку возраст 1 год вместо 0",
                'pets[name] += 1\npets[new_pet] = 1\nprint(pets)\nprint(f"Pets: {len(pets)}")')],
        constructs=["dict"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-dict-rt-secret-cipher", title="Секретный шифр",
        given=["code", "message"],
        variants=[{"code": '{"a": "o", "o": "a", "t": "d"}', "message": '"toast at noon"'},
                  {"code": '{"e": "3", "o": "0", "s": "5", "i": "1"}', "message": '"secret mission"'},
                  {"code": '{"m": "n", "n": "m"}', "message": '"meet me at nine"'}],
        hidden=[{"code": '{"x": "y"}', "message": '"hello"'},
                {"code": '{"a": "b", "b": "a"}', "message": '"abba"'},
                {"code": '{"l": "1", "o": "0", " ": "_"}', "message": '"look out"'},
                {"code": '{"c": "k", "k": "c", "s": "z"}', "message": '"kiss the cat"'}],
        intro="Друзья переписываются шифром замены. Шифр хранится в словаре `code`: ключ — символ исходного текста, "
              "значение — символ, на который его надо заменить. Символы, которых в словаре нет (например, пробелы), "
              "остаются как есть. Нужно зашифровать сообщение `message`.",
        steps=["Создай пустую строку для результата и счётчик заменённых символов, равный 0.",
               "Пройди циклом по символам `message`. Возьми замену символа методом `.get()`: если символа нет в словаре, "
               "вторым аргументом передай сам этот символ — тогда он останется без изменений. Допиши полученный символ "
               "в конец результата.",
               "Если символ есть среди ключей словаря `code`, увеличь счётчик на 1.",
               "Выведи зашифрованное сообщение, а следующей строкой — строку вида `Replaced: 7`."],
        hint="`code.get(ch, ch)` вернёт замену, если ключ `ch` есть в словаре, и сам `ch`, если его нет. "
             "Проверка `ch in code` ищет среди ключей словаря, а не среди значений.",
        solution=CIPHER,
        wrong=[("вызывает .get() с пустой строкой по умолчанию — символы без замены пропадают",
                CIPHER.replace("    result += code.get(ch, ch)\n", '    result += code.get(ch, "")\n')),
               ("ищет символ среди значений словаря, а не среди ключей",
                CIPHER.replace("    if ch in code:\n", "    if ch in code.values():\n"))],
        constructs=["dict", "for"],
        must_use=[("re:\\.get\\(", "Бери замену через .get() с запасным значением — тогда символы, которых нет в шифре, "
                                   "останутся как есть.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-dict-rt-camp-squads", title="Отряды в лагере",
        given=["kids"],
        variants=[{"kids": '[("Anya", "Eagles"), ("Boris", "Wolves"), ("Vera", "Eagles"), ("Gleb", "Bears"), '
                           '("Dina", "Wolves"), ("Egor", "Eagles")]'},
                  {"kids": '[("Ilya", "Foxes"), ("Kira", "Owls"), ("Lev", "Owls"), ("Mila", "Foxes")]'},
                  {"kids": '[("Nina", "Hawks"), ("Oleg", "Lynx"), ("Pasha", "Lynx"), ("Rita", "Hawks"), '
                           '("Sava", "Lynx"), ("Tanya", "Seals"), ("Uma", "Hawks"), ("Vlad", "Hawks")]'}],
        hidden=[{"kids": '[("Yana", "Dolphins")]'},
                {"kids": '[("Zhenya", "Tigers"), ("Ada", "Lions"), ("Bella", "Lions")]'},
                {"kids": '[("Fedya", "Ants"), ("Gosha", "Bees"), ("Ira", "Bees"), ("Kolya", "Ants"), ("Lida", "Ants"), '
                         '("Mark", "Bees")]'},
                {"kids": '[("Olya", "Cats"), ("Petya", "Cats"), ("Roma", "Dogs")]'}],
        intro="В летнем лагере детей распределили по отрядам. Список `kids` состоит из кортежей: имя ребёнка и название "
              "его отряда. Вожатым нужен список каждого отряда и самый большой отряд.",
        steps=["Создай пустой словарь `squads`: ключом будет название отряда, значением — список имён его детей.",
               "Пройди по `kids`, распаковывая каждый кортеж в имя и отряд. Если отряда ещё нет в словаре, сначала "
               "положи по этому ключу пустой список. Потом добавь имя в список отряда методом `.append()`.",
               "Пройди по словарю методом `.items()` и для каждого отряда выведи строку вида `Eagles: Anya, Vera, Egor` — "
               "имена через запятую и пробел в том порядке, в котором дети встречаются в `kids`.",
               "В том же цикле найди самый большой отряд; если таких несколько, нужен тот, что встретился раньше. "
               "Последней строкой выведи строку вида `Biggest: Eagles (3)`."],
        hint="Значением словаря может быть список, и его можно менять прямо в словаре: `squads[squad].append(name)`. "
             "Пустой список кладётся только для нового отряда — иначе каждый раз список отряда будет начинаться заново. "
             "Отряды словарь хранит в порядке добавления.",
        solution=SQUADS,
        wrong=[("кладёт пустой список при каждом ребёнке — в отряде остаётся только последний",
                SQUADS.replace("    if squad not in squads:\n        squads[squad] = []\n", "    squads[squad] = []\n")),
               ("при равном размере выбирает отряд, который встретился позже",
                SQUADS.replace("len(names) > len(squads[biggest])", "len(names) >= len(squads[biggest])"))],
        constructs=["dict", "for"],
        must_use=[("re:\\.items\\(", "Пройди по словарю методом .items(): так на каждом шаге у тебя будут и отряд, "
                                     "и список его детей."),
                  ("re:\\.append\\(", "Добавляй имя в список отряда методом .append().")],
    ),
]
