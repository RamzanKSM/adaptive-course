"""PY_STRING_METHODS — «Методы строк». Taught before: print, variables, arithmetic, int/float, strings, type conversion,
// and %, += -=, f-strings, conditions, for/while loops, break/continue, lists (indexes, append, len, in, iterating),
string slicing. Here: strip, lower, upper, title, capitalize, replace, count, find, split; a method returns a new
string and does not change the old one. Not yet: functions, join, list methods beyond append, list slices."""
from build import OutputTask

SKILL = "PY_STRING_METHODS"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-sm-rt-song-search", title="Поиск по названию песни",
        given=["title", "word"],
        variants=[{"title": '"The Road to Kazan"', "word": '"road"'},
                  {"title": '"Summer Rain"', "word": '"rain"'},
                  {"title": '"Night City Lights"', "word": '"moon"'}],
        hidden=[{"title": '"Rain"', "word": '"rain"'}, {"title": '"Blue Sky"', "word": '"sea"'},
                {"title": '"Dance All Night"', "word": '"night"'}],
        intro="Музыкальное приложение ищет слово в названии песни без учёта регистра: `Road` и `road` считаются одинаково. "
              "Название песни — `title = {title}`, слово для поиска записано маленькими буквами: `word = {word}`.",
        steps=["Методом `lower` переведи название в маленькие буквы и сохрани в `low`.",
               "Методом `find` найди, с какого индекса `word` начинается в `low`, и сохрани в `pos`. "
               "Если слова нет, `find` вернёт -1.",
               "Выведи три строки: название крупными буквами `Upper: THE ROAD TO KAZAN` (метод `upper`), "
               "`Position: 4` и `Found: True` или `Found: False` — найдено ли слово (`pos` не равно -1)."],
        hint="Методы не меняют строку, а возвращают новую — её нужно сохранить: `low = title.lower()`. "
             "Искать надо в `low`: в исходном названии `Road` с большой буквы, и `find` его не найдёт.",
        solution='low = title.lower()\npos = low.find(word)\nprint(f"Upper: {title.upper()}")\nprint(f"Position: {pos}")\n'
                 'print(f"Found: {pos != -1}")',
        wrong=[("ищет в исходном названии: слово с большой буквы не находится",
                'low = title.lower()\npos = title.find(word)\nprint(f"Upper: {title.upper()}")\nprint(f"Position: {pos}")\n'
                'print(f"Found: {pos != -1}")'),
               ("считает найденным только слово в самом начале",
                'low = title.lower()\npos = low.find(word)\nprint(f"Upper: {title.upper()}")\nprint(f"Position: {pos}")\n'
                'print(f"Found: {pos == 0}")')],
        must_use=[("re:\\.find\\(", "Найди позицию слова методом find.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-sm-rt-initials", title="Инициалы для подписи",
        given=["full_name"],
        variants=[{"full_name": '"anna maria petrova"'}, {"full_name": '"  boris ivanov "'},
                  {"full_name": '"vika  sofia   sokolova"'}],
        hidden=[{"full_name": '"lev"'}, {"full_name": '"timur rustam ali kozlov"'}, {"full_name": '" Mila Orlova"'}],
        intro="Программа для писем ставит в подписи инициалы. Полное имя ввели как попало: `full_name = {full_name}` — "
              "маленькими буквами и, может быть, с лишними пробелами. Слов в имени может быть сколько угодно.",
        steps=["Разбей имя на слова методом `split()` без аргументов и сохрани список в `words`.",
               "Заведи пустую строку `initials`. Циклом `for` перебери слова и для каждого прибавь к `initials` "
               "его первую букву, сделанную заглавной методом `upper`.",
               "Выведи `Words: 3`, затем `Initials: AMP` и последней строкой имя с заглавных букв без лишних пробелов "
               "по краям — `Name: Anna Maria Petrova` (методы `strip` и `title`)."],
        hint="`split()` без аргументов режет по любому количеству пробелов и сам не оставляет пустых слов. "
             "Первая буква слова — `word[0]`; к строке можно прибавлять через `+=`. "
             "`strip` убирает пробелы только по краям, а не внутри строки.",
        solution='words = full_name.split()\ninitials = ""\nfor word in words:\n    initials += word[0].upper()\n'
                 'print(f"Words: {len(words)}")\nprint(f"Initials: {initials}")\nprint(f"Name: {full_name.strip().title()}")',
        wrong=[("split(\" \") вместо split(): лишние пробелы дают пустые слова",
                'words = full_name.split(" ")\ninitials = ""\nfor word in words:\n    initials += word[:1].upper()\n'
                'print(f"Words: {len(words)}")\nprint(f"Initials: {initials}")\nprint(f"Name: {full_name.strip().title()}")'),
               ("забыт upper: инициалы маленькими буквами",
                'words = full_name.split()\ninitials = ""\nfor word in words:\n    initials += word[0]\n'
                'print(f"Words: {len(words)}")\nprint(f"Initials: {initials}")\nprint(f"Name: {full_name.strip().title()}")'),
               ("capitalize вместо title: только первое слово с большой буквы",
                'words = full_name.split()\ninitials = ""\nfor word in words:\n    initials += word[0].upper()\n'
                'print(f"Words: {len(words)}")\nprint(f"Initials: {initials}")\nprint(f"Name: {full_name.strip().capitalize()}")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-sm-rt-shopping-note", title="Заметка со списком покупок",
        given=["note"],
        variants=[{"note": '"milk, bread , eggs,tea "'}, {"note": '" apples,ORANGE juice, cheese"'},
                  {"note": '"rice ,  chicken,soup, cake, lemons"'}],
        hidden=[{"note": '"salt"'}, {"note": '"ab, cd ,ef"'}, {"note": '" fish , green tea,coffee beans , jam"'}],
        intro="Мама написала в заметке список покупок `note = {note}` — через запятую, но с лишними пробелами и "
              "буквами разного размера. Приложение показывает аккуратный список и подсказывает самый длинный пункт.",
        steps=["Разбей заметку методом `split` по запятой и сохрани список в `items`.",
               "Заведи счётчик `number = 0` и строку `longest = \"\"`. Перебери `items` циклом `for`: каждый пункт очисти "
               "от пробелов по краям (`strip`) и сделай с большой буквы только первое слово (`capitalize`).",
               "В цикле увеличь `number` на 1 и выведи строку вида `1. Milk`. Если очищенный пункт длиннее `longest`, "
               "запомни его в `longest`.",
               "После цикла выведи `Items: 4` и `Longest: Bread`"],
        hint="`capitalize` делает первую букву заглавной, а все остальные — маленькими: `\"ORANGE juice\"` станет "
             "`\"Orange juice\"`. Сравнивай длины уже очищенных пунктов — иначе пробелы по краям тоже посчитаются. "
             "Сравнение строгое: из пунктов одинаковой длины остаётся первый.",
        solution='items = note.split(",")\nnumber = 0\nlongest = ""\nfor item in items:\n    clean = item.strip().capitalize()\n'
                 '    number += 1\n    print(f"{number}. {clean}")\n    if len(clean) > len(longest):\n        longest = clean\n'
                 'print(f"Items: {number}")\nprint(f"Longest: {longest}")',
        wrong=[("сравнивает длины до strip: пункт с пробелами кажется длиннее",
                'items = note.split(",")\nnumber = 0\nlongest = ""\nfor item in items:\n    clean = item.strip().capitalize()\n'
                '    number += 1\n    print(f"{number}. {clean}")\n    if len(item) > len(longest):\n        longest = clean\n'
                'print(f"Items: {number}")\nprint(f"Longest: {longest}")'),
               ("title вместо capitalize: каждое слово пункта с большой буквы",
                'items = note.split(",")\nnumber = 0\nlongest = ""\nfor item in items:\n    clean = item.strip().title()\n'
                '    number += 1\n    print(f"{number}. {clean}")\n    if len(clean) > len(longest):\n        longest = clean\n'
                'print(f"Items: {number}")\nprint(f"Longest: {longest}")'),
               ("нестрогое сравнение: из одинаковых по длине остаётся последний",
                'items = note.split(",")\nnumber = 0\nlongest = ""\nfor item in items:\n    clean = item.strip().capitalize()\n'
                '    number += 1\n    print(f"{number}. {clean}")\n    if len(clean) >= len(longest):\n        longest = clean\n'
                'print(f"Items: {number}")\nprint(f"Longest: {longest}")')],
        constructs=["for", "if"],
    ),
]
