"""PY_STRING_METHODS — «Методы строк». Taught before: print, variables, arithmetic, int/float, strings, type conversion,
// and %, += -=, f-strings, conditions, for/while loops, break/continue, lists (indexes, append, len, in, iterating),
string slicing. Here: strip, lower, upper, title, capitalize, replace, count, find, split; a method returns a new
string and does not change the old one. Not yet: functions, join, list methods beyond append, list slices."""
from build import OutputTask

SKILL = "PY_STRING_METHODS"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-sm-badge", title="Бейдж участника",
        given=["raw"],
        variants=[{"raw": '"  anna petrova  "'}, {"raw": '"boris ivanov   "'}, {"raw": '"   vika sokolova"'}],
        hidden=[{"raw": '"lev li"'}, {"raw": '"  timur kozlov "'}, {"raw": '"MILA ORLOVA  "'}],
        intro="Участник конференции ввёл имя и фамилию в анкету небрежно: `raw = {raw}` — с лишними пробелами по краям "
              "и маленькими буквами. Подготовь надписи для бейджа.",
        steps=["Убери пробелы по краям строки методом `strip` и сохрани результат в `clean`.",
               "Методом `title` сделай каждое слово с большой буквы и сохрани в `name`.",
               "Выведи три строки: `Name: Anna Petrova`, надпись крупными буквами `Badge: ANNA PETROVA` (метод `upper`) "
               "и длину очищенной строки `Length: 12`"],
        hint="Методы не меняют строку, а возвращают новую — её нужно сохранить: `clean = raw.strip()`. "
             "`title` делает заглавной первую букву каждого слова, а `capitalize` — только первую букву всей строки.",
        solution='clean = raw.strip()\nname = clean.title()\nprint(f"Name: {name}")\nprint(f"Badge: {name.upper()}")\n'
                 'print(f"Length: {len(clean)}")',
        wrong=[("не убраны пробелы по краям: имя и длина неверные",
                'clean = raw\nname = clean.title()\nprint(f"Name: {name}")\nprint(f"Badge: {name.upper()}")\n'
                'print(f"Length: {len(clean)}")'),
               ("capitalize вместо title: фамилия остаётся с маленькой буквы",
                'clean = raw.strip()\nname = clean.capitalize()\nprint(f"Name: {name}")\nprint(f"Badge: {name.upper()}")\n'
                'print(f"Length: {len(clean)}")')],
        must_use=[("re:\\.strip\\(", "Убери пробелы по краям методом strip.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-sm-typo", title="Опечатка в объявлении",
        given=["text", "wrong", "right"],
        variants=[{"text": '"Teh shop opens at 9. Teh cafe opens at 10."', "wrong": '"Teh"', "right": '"The"'},
                  {"text": '"Fresh brad and sweet brad rolls today. Brad is cheap."', "wrong": '"brad"', "right": '"bread"'},
                  {"text": '"Concert in the park on Satuday. Tickets for Satuday only."', "wrong": '"Satuday"', "right": '"Saturday"'}],
        hidden=[{"text": '"No mistakes here."', "wrong": '"teh"', "right": '"the"'},
                {"text": '"aaa"', "wrong": '"a"', "right": '"bb"'},
                {"text": '"Moscow is big. I love Moskow."', "wrong": '"Moskow"', "right": '"Moscow"'}],
        intro="В объявлении `text` слово с опечаткой `wrong = {wrong}` нужно заменить на правильное `right = {right}`. "
              "Регистр букв важен: `Brad` и `brad` — разные слова.",
        steps=["Методом `count` посчитай, сколько раз в `text` встречается `wrong`, и сохрани в `count`.",
               "Методом `replace` замени в `text` все `wrong` на `right` и сохрани результат в `fixed`.",
               "Выведи три строки: `Mistakes: 2`, исправленный текст и его длину в виде `Length: 42`"],
        hint="`text.replace(old, new)` возвращает новую строку, где все `old` заменены на `new`; сама `text` не меняется. "
             "Порядок аргументов важен: сначала что заменить, потом на что.",
        solution='count = text.count(wrong)\nfixed = text.replace(wrong, right)\nprint(f"Mistakes: {count}")\n'
                 'print(fixed)\nprint(f"Length: {len(fixed)}")',
        wrong=[("считает правильное слово вместо ошибочного",
                'count = text.count(right)\nfixed = text.replace(wrong, right)\nprint(f"Mistakes: {count}")\n'
                'print(fixed)\nprint(f"Length: {len(fixed)}")'),
               ("перепутаны аргументы replace: ничего не исправлено",
                'count = text.count(wrong)\nfixed = text.replace(right, wrong)\nprint(f"Mistakes: {count}")\n'
                'print(fixed)\nprint(f"Length: {len(fixed)}")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-sm-email", title="Проверка email",
        given=["raw"],
        variants=[{"raw": '" Anna.Petrova@Mail.ru "'}, {"raw": '"BORIS@Example.COM  "'}, {"raw": '"vika_s@school"'}],
        hidden=[{"raw": '"a@b.c"'}, {"raw": '"no-at-sign.ru"'}, {"raw": '"x@y@z.ru"'}, {"raw": '"  Lev@Kazan.Net"'}],
        intro="Пользователь ввёл адрес почты в форму регистрации: `raw = {raw}`. Сайт приводит адрес к единому виду "
              "и проверяет, похож ли он на настоящий.",
        steps=["Убери пробелы по краям и переведи все буквы в маленькие — сохрани результат в `email`.",
               "Разбей `email` методом `split` по символу `@` и сохрани список частей в `parts`. Выведи `Email: anna.petrova@mail.ru`",
               "Если частей ровно две и во второй части есть точка, выведи `User: anna.petrova` и следующей строкой "
               "`Domain: mail.ru`. Иначе выведи `Invalid email`"],
        hint="Методы можно вызывать цепочкой: `raw.strip().lower()`. "
             "`\"a@b\".split(\"@\")` даёт список `[\"a\", \"b\"]`: если `@` нет, частей будет одна, если два `@` — три.",
        solution='email = raw.strip().lower()\nparts = email.split("@")\nprint(f"Email: {email}")\n'
                 'if len(parts) == 2 and "." in parts[1]:\n    print(f"User: {parts[0]}")\n    print(f"Domain: {parts[1]}")\n'
                 'else:\n    print("Invalid email")',
        wrong=[("не убраны пробелы по краям адреса",
                'email = raw.lower()\nparts = email.split("@")\nprint(f"Email: {email}")\n'
                'if len(parts) == 2 and "." in parts[1]:\n    print(f"User: {parts[0]}")\n    print(f"Domain: {parts[1]}")\n'
                'else:\n    print("Invalid email")'),
               ("разбивает по точке вместо @",
                'email = raw.strip().lower()\nparts = email.split(".")\nprint(f"Email: {email}")\n'
                'if len(parts) == 2 and "." in parts[1]:\n    print(f"User: {parts[0]}")\n    print(f"Domain: {parts[1]}")\n'
                'else:\n    print("Invalid email")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-sm-review", title="Разбор отзыва",
        given=["review", "topic"],
        variants=[{"review": '"Great pizza. The pizza was hot and the Pizza box was nice."', "topic": '"pizza"'},
                  {"review": '"Fast delivery! Delivery guy was polite. delivery took 20 minutes."', "topic": '"delivery"'},
                  {"review": '"Nice hotel, nice view, but the Hotel bar was closed."', "topic": '"hotel"'}],
        hidden=[{"review": '"ok"', "topic": '"pizza"'}, {"review": '"Tea tea TEA"', "topic": '"tea"'},
                {"review": '"I like music"', "topic": '"music"'}],
        intro="Сервис отзывов анализирует текст `review`. Нужно узнать, сколько в отзыве слов, каким словом он начинается "
              "и сколько раз упомянута тема `topic = {topic}` — в любом регистре: `Pizza` и `pizza` считаются одинаково. "
              "Тема записана маленькими буквами.",
        steps=["Разбей отзыв на слова методом `split()` без аргументов и сохрани список в `words`.",
               "Переведи весь отзыв в маленькие буквы и сохрани в `lower`.",
               "Выведи три строки: `Words: 12`, первое слово `First word: Great` и число упоминаний темы в `lower` "
               "(метод `count`) в виде `Mentions of pizza: 3`"],
        hint="`split()` без аргументов режет строку по пробелам. Метод `count` различает регистр, поэтому "
             "считать нужно в строке, переведённой в маленькие буквы.",
        solution='words = review.split()\nlower = review.lower()\nprint(f"Words: {len(words)}")\n'
                 'print(f"First word: {words[0]}")\nprint(f"Mentions of {topic}: {lower.count(topic)}")',
        wrong=[("считает в исходном отзыве: упоминания с большой буквы пропущены",
                'words = review.split()\nlower = review.lower()\nprint(f"Words: {len(words)}")\n'
                'print(f"First word: {words[0]}")\nprint(f"Mentions of {topic}: {review.count(topic)}")'),
               ("режет по запятой вместо пробелов",
                'words = review.split(",")\nlower = review.lower()\nprint(f"Words: {len(words)}")\n'
                'print(f"First word: {words[0]}")\nprint(f"Mentions of {topic}: {lower.count(topic)}")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-sm-gradebook", title="Строка из электронного журнала",
        given=["line"],
        variants=[{"line": '"Anna:5,4,5,3"'}, {"line": '"Boris:3,4,4"'}, {"line": '"Vika:5,5,4,5,5"'}],
        hidden=[{"line": '"Lev:2"'}, {"line": '"Timur:4,3,5,5,2,4"'}, {"line": '"Mila:3,3"'}],
        intro="Электронный журнал выгружает оценки строкой `line = {line}`: имя ученика, двоеточие и оценки через запятую "
              "без пробелов.",
        steps=["Методом `find` найди, под каким индексом стоит двоеточие, и сохрани в `colon`.",
               "Срезом до двоеточия получи имя `name`, а часть после двоеточия разбей методом `split` по запятой "
               "в список `grades`.",
               "Заведи накопитель `total` со значением 0 и циклом `for` прибавь к нему каждую оценку, переведённую в число через `int`.",
               "Выведи три строки: `Student: Anna`, `Grades: 4` и `Sum: 17`"],
        hint="`\"Anna:5\".find(\":\")` даёт 4. Срез `line[:colon]` не включает само двоеточие, а оценки начинаются "
             "со следующего индекса — `colon + 1`. После `split` оценки — это строки, например `\"5\"`.",
        solution='colon = line.find(":")\nname = line[:colon]\ngrades = line[colon + 1:].split(",")\ntotal = 0\n'
                 'for grade in grades:\n    total += int(grade)\nprint(f"Student: {name}")\n'
                 'print(f"Grades: {len(grades)}")\nprint(f"Sum: {total}")',
        wrong=[("срез имени включает двоеточие",
                'colon = line.find(":")\nname = line[:colon + 1]\ngrades = line[colon + 1:].split(",")\ntotal = 0\n'
                'for grade in grades:\n    total += int(grade)\nprint(f"Student: {name}")\n'
                'print(f"Grades: {len(grades)}")\nprint(f"Sum: {total}")'),
               ("перезаписывает total вместо накопления: в сумме только последняя оценка",
                'colon = line.find(":")\nname = line[:colon]\ngrades = line[colon + 1:].split(",")\ntotal = 0\n'
                'for grade in grades:\n    total = int(grade)\nprint(f"Student: {name}")\n'
                'print(f"Grades: {len(grades)}")\nprint(f"Sum: {total}")')],
        constructs=["for"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-sm-hashtag", title="Хэштег для поста",
        given=["phrase", "limit"],
        variants=[{"phrase": '"  summer trip to kazan "', "limit": "20"},
                  {"phrase": '"best day ever"', "limit": "12"},
                  {"phrase": '"my first python program"', "limit": "15"}],
        hidden=[{"phrase": '"hi"', "limit": "5"}, {"phrase": '"  sochi   sea  "', "limit": "8"},
                {"phrase": '"a b c d e f"', "limit": "6"},
                {"phrase": '"go home"', "limit": "7"}],
        intro="Соцсеть превращает фразу `phrase = {phrase}` в хэштег: каждое слово с большой буквы, пробелы убраны, "
              "впереди знак `#`. Хэштег не должен быть длиннее `limit = {limit}` символов, считая `#`.",
        steps=["Убери пробелы по краям фразы и сохрани результат в `clean`. Разбей `clean` на слова методом `split()` в `words`.",
               "Собери хэштег `tag`: знак `#` плюс `clean`, в которой сначала каждое слово сделано с большой буквы "
               "(`title`), а потом все пробелы убраны (`replace`).",
               "Выведи `Words: 4` и следующей строкой `Tag: #SummerTripToKazan`",
               "Если хэштег длиннее `limit`, выведи, на сколько символов, в виде `Too long by 6`. Иначе выведи `OK`"],
        hint="Порядок методов важен: после удаления пробелов `title` увидит одно длинное слово и сделает заглавной "
             "только первую букву. Цепочка `clean.title().replace(\" \", \"\")` сначала делает заглавные буквы.",
        solution='clean = phrase.strip()\nwords = clean.split()\ntag = "#" + clean.title().replace(" ", "")\n'
                 'print(f"Words: {len(words)}")\nprint(f"Tag: {tag}")\nif len(tag) > limit:\n'
                 '    print(f"Too long by {len(tag) - limit}")\nelse:\n    print("OK")',
        wrong=[("сначала убирает пробелы, потом title: заглавная только первая буква",
                'clean = phrase.strip()\nwords = clean.split()\ntag = "#" + clean.replace(" ", "").title()\n'
                'print(f"Words: {len(words)}")\nprint(f"Tag: {tag}")\nif len(tag) > limit:\n'
                '    print(f"Too long by {len(tag) - limit}")\nelse:\n    print("OK")'),
               ("нестрогое сравнение: хэштег ровно в limit символов считается длинным",
                'clean = phrase.strip()\nwords = clean.split()\ntag = "#" + clean.title().replace(" ", "")\n'
                'print(f"Words: {len(words)}")\nprint(f"Tag: {tag}")\nif len(tag) >= limit:\n'
                '    print(f"Too long by {len(tag) - limit}")\nelse:\n    print("OK")')],
        constructs=["if"],
    ),
]
