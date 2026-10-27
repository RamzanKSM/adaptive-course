"""PY_STRING_BASIC — «Строки». Taught before: print (several values separated by commas), variables, assignment,
arithmetic, order of execution, int/float. Here: string literals, gluing with `+`, repeating with `*`, `len()`.
Not yet: int()/float()/str(), indexing and slices, string methods, // and %, += -=, f-strings, conditions, loops,
functions."""
from build import OutputTask

SKILL = "PY_STRING_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-sb-rt-photo-caption", title="Подпись к фото",
        given=["place", "year", "friend"],
        variants=[{"place": '"Baikal"', "year": '"2025"', "friend": '"anya_k"'},
                  {"place": '"Elbrus"', "year": '"2026"', "friend": '"timur.climbs"'},
                  {"place": '"Altai"', "year": '"2024"', "friend": '"vera22"'}],
        hidden=[{"place": '"Kazan"', "year": '"2023"', "friend": '"li"'},
                {"place": '"Kamchatka"', "year": '"2030"', "friend": '"boris_on_tour"'},
                {"place": '"Sochi"', "year": '"1999"', "friend": '"mom"'}],
        intro="Ты выкладываешь фото из поездки. Место — `place = {place}`, год — `year = {year}` (это строка, а не число), "
              "друг на фото — `friend = {friend}`. Программа собирает подпись к фото.",
        steps=["Склей через `+` место, запятую с пробелом `\", \"` и год в переменную `caption`.",
               "Выведи `caption`.",
               "Выведи `With @` и друга, склеив через `+`, без пробела после `@`.",
               "Выведи хештег: `\"#\"`, место и год, склеенные через `+` без пробелов. Например, для `\"Ufa\"` и `\"2020\"` "
               "это `#Ufa2020`.",
               "Последней строкой выведи `Best trip` и сразу за ним `\"!\"`, повторённый 3 раза."],
        hint="`+` склеивает строки как есть и пробелов сам не добавляет: `\"Ufa\" + \"2020\"` даёт `Ufa2020`. "
             "Где пробел нужен, его приклеивают отдельной строкой. Строку можно повторить умножением на число: "
             "`\"!\" * 3` даёт `!!!`.",
        solution='caption = place + ", " + year\nprint(caption)\nprint("With @" + friend)\nprint("#" + place + year)\n'
                 'print("Best trip" + "!" * 3)',
        wrong=[("печатает хештег через запятую — между местом и годом появляются пробелы",
                'caption = place + ", " + year\nprint(caption)\nprint("With @" + friend)\nprint("#", place, year)\n'
                'print("Best trip" + "!" * 3)'),
               ("склеивает место и год без запятой",
                'caption = place + " " + year\nprint(caption)\nprint("With @" + friend)\nprint("#" + place + year)\n'
                'print("Best trip" + "!" * 3)'),
               ("берёт имя переменной в кавычки — печатается слово friend",
                'caption = place + ", " + year\nprint(caption)\nprint("With @" + "friend")\nprint("#" + place + year)\n'
                'print("Best trip" + "!" * 3)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-sb-rt-password-mask", title="Пароль звёздочками",
        given=["login", "password"],
        variants=[{"login": '"anya_p"', "password": '"sun2026"'}, {"login": '"boris"', "password": '"qwerty12"'},
                  {"login": '"kamila.r"', "password": '"MyCat!7"'}],
        hidden=[{"login": '"li"', "password": '"a1"'}, {"login": '"oleg_orlov"', "password": '"Very$ecret12"'},
                {"login": '"t"', "password": '"pass word"'}],
        intro="На экране входа пароль не показывают, а заменяют каждый его символ звёздочкой. Логин — `login = {login}`, "
              "пароль — `password = {password}`. Надёжным считается пароль из 12 символов.",
        steps=["Выведи `Login: ` и логин, склеив через `+`.",
               "Склей маску `mask`: строку `\"*\"`, повторённую столько раз, сколько символов в пароле (`len(password)`).",
               "Выведи `Password: ` и `mask`, склеив через `+`.",
               "Выведи через запятую `Length:` и длину пароля.",
               "Выведи через запятую `To 12:` и сколько символов не хватает до 12: 12 минус длина пароля. "
               "Например, для пароля `\"abc\"` это `Password: ***`, `Length: 3` и `To 12: 9`."],
        hint="`len()` считает все символы строки, включая цифры, знаки и пробелы, и возвращает число. "
             "Строку можно умножить на это число: `\"*\" * len(\"abc\")` даёт `***`. Само число к строке через `+` не "
             "приклеить, поэтому длину печатаем через запятую.",
        solution='print("Login: " + login)\nmask = "*" * len(password)\nprint("Password: " + mask)\n'
                 'print("Length:", len(password))\nprint("To 12:", 12 - len(password))',
        wrong=[("делает маску по длине логина",
                'print("Login: " + login)\nmask = "*" * len(login)\nprint("Password: " + mask)\n'
                'print("Length:", len(password))\nprint("To 12:", 12 - len(password))'),
               ("показывает пароль вместо звёздочек",
                'print("Login: " + login)\nmask = password\nprint("Password: " + mask)\n'
                'print("Length:", len(password))\nprint("To 12:", 12 - len(password))'),
               ("вычитает в обратном порядке",
                'print("Login: " + login)\nmask = "*" * len(password)\nprint("Password: " + mask)\n'
                'print("Length:", len(password))\nprint("To 12:", len(password) - 12)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-sb-rt-quote-frame", title="Цитата в рамке",
        given=["text", "author"],
        variants=[{"text": '"Practice makes perfect"', "author": '"Proverb"'},
                  {"text": '"Simple is better than complex"', "author": '"Tim Peters"'},
                  {"text": '"Code never lies"', "author": '"Ron Jeffries"'}],
        hidden=[{"text": '"Keep calm"', "author": '"Anon"'},
                {"text": '"Learning never exhausts the mind"', "author": '"Leonardo da Vinci"'},
                {"text": '"Hello, world"', "author": '"Kernighan"'}],
        intro="Для стенгазеты печатают цитату в рамке: текст `text = {text}` обведён рамкой из `+`, `-` и `|`, "
              "а под рамкой справа стоит подпись `author = {author}`. Ширина рамки зависит от длины цитаты.",
        steps=["Склей рамку `border`: `\"+\"`, затем `\"-\"`, повторённый `len(text) + 2` раз, и снова `\"+\"`.",
               "Выведи `border`, затем строку `\"| \"`, текст и `\" |\"`, склеенные через `+`, затем снова `border`.",
               "Склей подпись `sign`: `\"- \"` и автора.",
               "Выведи подпись, прижатую к правому краю рамки: перед ней столько пробелов, чтобы вся строка была такой же "
               "длины, как `border`. Пробелов нужно `len(border) - len(sign)`.",
               "Например, для текста `\"Hi\"` и автора `\"Li\"` программа выводит `+----+`, `| Hi |`, `+----+` и `  - Li`."],
        hint="В строке `| Hi |` по краям стоит по пробелу, поэтому чёрточек в рамке на 2 больше, чем символов в тексте: "
             "`\"-\" * (len(text) + 2)`. Скобки обязательны: без них строка повторится `len(text)` раз, а потом Python "
             "попробует прибавить к строке число и остановится с ошибкой.",
        solution='border = "+" + "-" * (len(text) + 2) + "+"\nprint(border)\nprint("| " + text + " |")\nprint(border)\n'
                 'sign = "- " + author\nprint(" " * (len(border) - len(sign)) + sign)',
        wrong=[("делает рамку на два символа короче — она не закрывает пробелы по краям",
                'border = "+" + "-" * len(text) + "+"\nprint(border)\nprint("| " + text + " |")\nprint(border)\n'
                'sign = "- " + author\nprint(" " * (len(border) - len(sign)) + sign)'),
               ("считает отступ подписи по длине автора, забыв про `- ` перед ним",
                'border = "+" + "-" * (len(text) + 2) + "+"\nprint(border)\nprint("| " + text + " |")\nprint(border)\n'
                'sign = "- " + author\nprint(" " * (len(border) - len(author)) + sign)'),
               ("забывает пробелы внутри рамки вокруг текста",
                'border = "+" + "-" * (len(text) + 2) + "+"\nprint(border)\nprint("|" + text + "|")\nprint(border)\n'
                'sign = "- " + author\nprint(" " * (len(border) - len(sign)) + sign)')],
    ),
]
