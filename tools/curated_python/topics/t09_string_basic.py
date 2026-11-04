"""PY_STRING_BASIC — «Строки». Taught before: print (several values separated by commas), variables, assignment,
arithmetic, order of execution, int/float. Here: string literals, gluing with `+`, repeating with `*`, `len()`.
Not yet: int()/float()/str(), indexing and slices, string methods, // and %, += -=, f-strings, conditions, loops,
functions."""
from build import OutputTask

SKILL = "PY_STRING_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-sb-badge", title="Бейдж участника",
        given=["first", "last", "company"],
        variants=[{"first": '"Anya"', "last": '"Petrova"', "company": '"Volga Soft"'},
                  {"first": '"Boris"', "last": '"Ivanov"', "company": '"Kazan Bank"'},
                  {"first": '"Mila"', "last": '"Sokolova"', "company": '"Sochi Tours"'}],
        hidden=[{"first": '"Ivan"', "last": '"Li"', "company": '"IT"'},
                {"first": '"Daria"', "last": '"Kuznetsova"', "company": '"North Star Logistics"'},
                {"first": '"Oleg"', "last": '"Orlov"', "company": '"Ural Steel"'}],
        intro="Для конференции печатают бейджи. Имя участника — `first = {first}`, фамилия — `last = {last}`, "
              "компания — `company = {company}`. Бейдж — это четыре строки с рамкой сверху и снизу.",
        steps=["Склей через `+` имя, пробел и фамилию в переменную `full`.",
               "Выведи верхнюю рамку — 20 знаков `=` (повтори строку `\"=\"` 20 раз с помощью `*`).",
               "Выведи `Name: ` и `full`, склеив их через `+`.",
               "Выведи `Company: ` и `company`, тоже через `+`.",
               "Выведи нижнюю рамку — 20 знаков `-`."],
        hint="`+` склеивает строки как есть, пробелы сам не добавляет: `\"Anya\" + \"Li\"` даёт `AnyaLi`. "
             "Пробел надо приклеить отдельной строкой `\" \"`. Имя переменной в кавычках — это уже просто текст: "
             "`\"company\"` напечатает слово `company`, а не название компании.",
        solution='full = first + " " + last\nprint("=" * 20)\nprint("Name: " + full)\nprint("Company: " + company)\n'
                 'print("-" * 20)',
        wrong=[("склеивает имя и фамилию без пробела",
                'full = first + last\nprint("=" * 20)\nprint("Name: " + full)\nprint("Company: " + company)\n'
                'print("-" * 20)'),
               ("берёт имя переменной в кавычки — печатается слово company",
                'full = first + " " + last\nprint("=" * 20)\nprint("Name: " + full)\nprint("Company: " + "company")\n'
                'print("-" * 20)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-sb-chant", title="Кричалка болельщиков",
        given=["team", "shout"],
        variants=[{"team": '"Rubin"', "shout": '"Ole-"'}, {"team": '"Spartak"', "shout": '"Hey-"'},
                  {"team": '"Zenit"', "shout": '"Go-"'}],
        hidden=[{"team": '"Ural"', "shout": '"La-"'}, {"team": '"Lokomotiv"', "shout": '"Ole-"'},
                {"team": '"Sochi"', "shout": '"Yo-"'}],
        intro="Болельщики придумывают кричалку для команды `team = {team}`. Повторяющийся возглас — `shout = {shout}`. "
              "Программа должна напечатать четыре строки кричалки.",
        steps=["Выведи `shout`, повторённый 3 раза, и сразу за ним название команды — склей через `+`, без пробелов. "
               "Например, для `\"La-\"` и `\"Ural\"` это `La-La-La-Ural`.",
               "Выведи название команды и ` is the best!` (с пробелом в начале), склеив их через `+`.",
               "Выведи `We love ` и название команды.",
               "Выведи `shout`, повторённый 2 раза, и сразу за ним `go!`."],
        hint="Строку можно повторить умножением на целое число: `\"ab\" * 3` даёт `ababab`. "
             "Если печатать через запятую — `print(shout * 3, team)`, — Python вставит между частями пробел, а здесь он не нужен.",
        solution='print(shout * 3 + team)\nprint(team + " is the best!")\nprint("We love " + team)\nprint(shout * 2 + "go!")',
        wrong=[("печатает через запятую — между возгласом и названием появляется пробел",
                'print(shout * 3, team)\nprint(team + " is the best!")\nprint("We love " + team)\nprint(shout * 2 + "go!")'),
               ("теряет пробел после слова love",
                'print(shout * 3 + team)\nprint(team + " is the best!")\nprint("We love" + team)\nprint(shout * 2 + "go!")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-sb-school-email", title="Школьная почта",
        given=["name", "surname", "domain"],
        variants=[{"name": '"anya"', "surname": '"petrova"', "domain": '"school5.ru"'},
                  {"name": '"boris"', "surname": '"ivanov"', "domain": '"lyceum.org"'},
                  {"name": '"timur"', "surname": '"safin"', "domain": '"kazan-school.ru"'}],
        hidden=[{"name": '"li"', "surname": '"wu"', "domain": '"a.ru"'},
                {"name": '"ekaterina"', "surname": '"vasilyeva"', "domain": '"gymnasium12.ru"'},
                {"name": '"oleg"', "surname": '"orlov"', "domain": '"mail.com"'}],
        intro="Каждому ученику выдают школьную почту. Логин — это имя, точка и фамилия, а адрес — логин, знак `@` и домен. "
              "Имя — `name = {name}`, фамилия — `surname = {surname}`, домен школы — `domain = {domain}`.",
        steps=["Склей логин `login`: `name`, `\".\"` и `surname`.",
               "Склей адрес `email`: `login`, `\"@\"` и `domain`.",
               "Выведи `Login: ` и `login`, склеив через `+`, затем `Email: ` и `email`.",
               "Последней строкой выведи через запятую `Length:` и длину адреса — `len(email)`. "
               "Например, для `\"a\"`, `\"b\"` и `\"c.ru\"` программа выводит `Login: a.b`, `Email: a.b@c.ru` и `Length: 8`."],
        hint="`len()` считает все символы строки, включая точки и `@`: `len(\"a.b@c.ru\")` — это `8`. "
             "Длина — число, поэтому её печатаем через запятую, а не приклеиваем к строке через `+`.",
        solution='login = name + "." + surname\nemail = login + "@" + domain\nprint("Login: " + login)\n'
                 'print("Email: " + email)\nprint("Length:", len(email))',
        wrong=[("забывает знак @ между логином и доменом",
                'login = name + "." + surname\nemail = login + domain\nprint("Login: " + login)\n'
                'print("Email: " + email)\nprint("Length:", len(email))'),
               ("считает длину логина вместо длины адреса",
                'login = name + "." + surname\nemail = login + "@" + domain\nprint("Login: " + login)\n'
                'print("Email: " + email)\nprint("Length:", len(login))')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-sb-sms", title="Длина SMS",
        given=["greeting", "name", "text"],
        variants=[{"greeting": '"Hi"', "name": '"Anya"', "text": '"See you at 5 near the park."'},
                  {"greeting": '"Hello"', "name": '"Boris"', "text": '"The match starts at 7."'},
                  {"greeting": '"Good morning"', "name": '"Mom"', "text": '"I am already at school."'}],
        hidden=[{"greeting": '"Hey"', "name": '"Li"', "text": '"Ok."'},
                {"greeting": '"Dear"', "name": '"Grandma"', "text": '"Happy birthday! We will come on Sunday with a cake."'},
                {"greeting": '"Hi"', "name": '"Oleg"', "text": '"Call me back."'}],
        intro="В одну SMS помещается 70 символов. Программа собирает сообщение из приветствия `greeting = {greeting}`, "
              "имени `name = {name}` и текста `text = {text}` и показывает, сколько символов ещё можно дописать.",
        steps=["Склей сообщение `message`: `greeting`, `\", \"`, `name`, `\"! \"` и `text` — именно в таком порядке.",
               "Выведи `message`.",
               "Выведи через запятую `Characters:` и длину сообщения `len(message)`.",
               "Выведи через запятую `Left:` и сколько символов осталось: 70 минус длина сообщения. "
               "Например, для `\"Hi\"`, `\"Li\"` и `\"Ok.\"` сообщение — `Hi, Li! Ok.`, в нём 11 символов, осталось 59."],
        hint="Запятая и восклицательный знак с пробелами — это тоже строки, их приклеивают через `+`: `\", \"` и `\"! \"`. "
             "`len()` считает и пробелы, и знаки препинания. Осталось — от длины всего сообщения, а не только текста.",
        solution='message = greeting + ", " + name + "! " + text\nprint(message)\nprint("Characters:", len(message))\n'
                 'print("Left:", 70 - len(message))',
        wrong=[("считает остаток только по тексту, без приветствия и имени",
                'message = greeting + ", " + name + "! " + text\nprint(message)\nprint("Characters:", len(message))\n'
                'print("Left:", 70 - len(text))'),
               ("склеивает части без запятой и пробелов",
                'message = greeting + name + text\nprint(message)\nprint("Characters:", len(message))\n'
                'print("Left:", 70 - len(message))')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-sb-menu-dots", title="Строки меню с точками",
        given=["dish1", "price1", "dish2", "price2", "width"],
        variants=[{"dish1": '"Borscht"', "price1": '"250 rub"', "dish2": '"Pancakes"', "price2": '"180 rub"', "width": "24"},
                  {"dish1": '"Soup"', "price1": '"90 rub"', "dish2": '"Chicken pie"', "price2": '"310 rub"', "width": "22"},
                  {"dish1": '"Tea"', "price1": '"50 rub"', "dish2": '"Cheesecake"', "price2": '"420 rub"', "width": "26"}],
        hidden=[{"dish1": '"Pizza"', "price1": '"500 rub"', "dish2": '"Juice"', "price2": '"70 rub"', "width": "20"},
                {"dish1": '"Salad"', "price1": '"1 rub"', "dish2": '"Fish and chips"', "price2": '"650 rub"', "width": "30"},
                {"dish1": '"Ice cream"', "price1": '"120 rub"', "dish2": '"Cola"', "price2": '"99 rub"', "width": "18"}],
        intro="В кафе печатают меню: название блюда слева, цена справа, а между ними — точки, чтобы каждая строка была "
              "ровно `width = {width}` символов. Блюда: `dish1 = {dish1}` за `price1 = {price1}` и `dish2 = {dish2}` "
              "за `price2 = {price2}`.",
        steps=["Посчитай точки для первой строки: `dots1` — это `\".\"`, повторённая столько раз, сколько символов "
               "остаётся от `width` после названия и цены: `width - len(dish1) - len(price1)`.",
               "Так же посчитай `dots2` для второго блюда.",
               "Выведи верхнюю рамку — `\"=\"`, повторённую `width` раз.",
               "Выведи строку первого блюда: `dish1`, `dots1` и `price1`, склеенные через `+`.",
               "Выведи строку второго блюда так же.",
               "Выведи нижнюю рамку — `\"-\"`, повторённую `width` раз. Например, для `\"Tea\"` за `\"5 rub\"` "
               "при ширине 12 строка блюда — `Tea....5 rub`."],
        hint="Длина строки блюда = длина названия + число точек + длина цены, и она должна равняться `width`. "
             "Значит, точек `width - len(dish1) - len(price1)`. Не забудь вычесть длину цены: в ней есть цифры, пробел и `rub`.",
        solution='dots1 = "." * (width - len(dish1) - len(price1))\ndots2 = "." * (width - len(dish2) - len(price2))\n'
                 'print("=" * width)\nprint(dish1 + dots1 + price1)\nprint(dish2 + dots2 + price2)\nprint("-" * width)',
        wrong=[("не вычитает длину цены — строка первого блюда получается длиннее рамки",
                'dots1 = "." * (width - len(dish1))\ndots2 = "." * (width - len(dish2) - len(price2))\n'
                'print("=" * width)\nprint(dish1 + dots1 + price1)\nprint(dish2 + dots2 + price2)\nprint("-" * width)'),
               ("делает рамку фиксированной длины 24, а не `width`",
                'dots1 = "." * (width - len(dish1) - len(price1))\ndots2 = "." * (width - len(dish2) - len(price2))\n'
                'print("=" * 24)\nprint(dish1 + dots1 + price1)\nprint(dish2 + dots2 + price2)\nprint("-" * 24)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-sb-progress-bar", title="Полоска прогресса",
        given=["name", "done", "total", "width"],
        variants=[{"name": '"Reading"', "done": "3", "total": "10", "width": "10"},
                  {"name": '"Running"', "done": "7", "total": "8", "width": "9"},
                  {"name": '"Piano"', "done": "5", "total": "12", "width": "8"}],
        hidden=[{"name": '"Yoga"', "done": "0", "total": "5", "width": "6"},
                {"name": '"English words"', "done": "15", "total": "15", "width": "14"},
                {"name": '"Swim"', "done": "2", "total": "6", "width": "4"}],
        intro="В приложении для привычек каждая привычка показана полоской прогресса. Привычка — `name = {name}`, "
              "выполнено `done = {done}` дней из `total = {total}`. Подпись дополняется пробелами до ширины "
              "`width = {width}`, чтобы полоски разных привычек стояли ровно друг под другом.",
        steps=["Склей подпись `label`: `name`, `\":\"` и пробел `\" \"`, повторённый `width - len(name)` раз.",
               "Склей полоску `bar`: `\"#\"`, повторённый `done` раз, и `\".\"`, повторённая `total - done` раз.",
               "Выведи одной строкой `label`, `\"[\"`, `bar` и `\"]\"`, склеенные через `+`.",
               "Выведи через запятую `Done:`, `done`, `of` и `total`.",
               "Выведи через запятую `Left:` и сколько дней осталось. Например, для `\"Gym\"`, 2 из 5 и ширины 5 "
               "программа выводит `Gym:  [##...]`, `Done: 2 of 5` и `Left: 3`."],
        hint="Строку можно умножить на число, в том числе на результат вычисления: `\".\" * (5 - 2)` даёт `...`. "
             "Скобки обязательны, иначе Python сначала умножит строку на 5, а потом попробует вычесть из строки число и остановится с ошибкой. А `\" \" * 0` — это пустая строка, так что "
             "подпись длиной ровно `width` тоже работает.",
        solution='label = name + ":" + " " * (width - len(name))\nbar = "#" * done + "." * (total - done)\n'
                 'print(label + "[" + bar + "]")\nprint("Done:", done, "of", total)\nprint("Left:", total - done)',
        wrong=[("повторяет точки `total` раз — полоска выходит слишком длинной",
                'label = name + ":" + " " * (width - len(name))\nbar = "#" * done + "." * total\n'
                'print(label + "[" + bar + "]")\nprint("Done:", done, "of", total)\nprint("Left:", total - done)'),
               ("добавляет `width` пробелов, не вычитая длину названия",
                'label = name + ":" + " " * width\nbar = "#" * done + "." * (total - done)\n'
                'print(label + "[" + bar + "]")\nprint("Done:", done, "of", total)\nprint("Left:", total - done)')],
    ),
]
