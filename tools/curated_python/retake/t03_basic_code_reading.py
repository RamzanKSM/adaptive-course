"""PY_BASIC_CODE_READING — «Вывод с print». Taught before: nothing, this is the first topic. The starter already holds the
given values in variables; the student only passes them to print (several arguments, an empty print(), sep= and end=).
Not yet: creating own variables, assignment, arithmetic, string concatenation, f-strings, conditions, loops."""
from build import OutputTask

SKILL = "PY_BASIC_CODE_READING"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-pr-rt-hotel-card", title="Карточка гостя в отеле",
        given=["guest", "room", "nights"],
        variants=[{"guest": '"Marat Galiev"', "room": "305", "nights": "3"},
                  {"guest": '"Vera Lebedeva"', "room": "112", "nights": "7"},
                  {"guest": '"Egor Smirnov"', "room": "48", "nights": "1"}],
        hidden=[{"guest": '"Alina Kuznetsova"', "room": "501", "nights": "2"},
                {"guest": '"Roman Fedorov"', "room": "9", "nights": "14"},
                {"guest": '"Liya Sharipova"', "room": "220", "nights": "5"}],
        intro="Отель при заселении печатает гостю карточку. Данные уже лежат в заготовке: имя гостя `guest = {guest}`, "
              "номер комнаты `room = {room}` и число ночей `nights = {nights}`.",
        steps=["Первой строкой выведи `WELCOME`.",
               "Второй строкой выведи `Guest:` и имя гостя.",
               "Третьей строкой выведи `Room:` и номер комнаты.",
               "Четвёртой строкой выведи `Nights:` и число ночей. Например, для 4 ночей строка будет `Nights: 4`."],
        hint='Текст и значение переменной выводятся одним `print` через запятую: `print("Room:", room)` — Python сам '
             'поставит между ними пробел. Имя переменной пиши без кавычек: `print("Room:", "room")` выведет слово `room`.',
        solution='print("WELCOME")\nprint("Guest:", guest)\nprint("Room:", room)\nprint("Nights:", nights)',
        wrong=[("берёт имя переменной в кавычки и печатает слово nights",
                'print("WELCOME")\nprint("Guest:", guest)\nprint("Room:", room)\nprint("Nights:", "nights")'),
               ("путает переменные: в строке комнаты печатает число ночей",
                'print("WELCOME")\nprint("Guest:", guest)\nprint("Room:", nights)\nprint("Nights:", nights)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-pr-rt-match-score", title="Итог матча",
        given=["home", "away", "home_goals", "away_goals"],
        variants=[{"home": '"Rubin"', "away": '"Zenit"', "home_goals": "2", "away_goals": "1"},
                  {"home": '"Spartak"', "away": '"Akhmat"', "home_goals": "0", "away_goals": "3"},
                  {"home": '"Krylia"', "away": '"Orenburg"', "home_goals": "4", "away_goals": "4"}],
        hidden=[{"home": '"Rostov"', "away": '"Sochi"', "home_goals": "1", "away_goals": "0"},
                {"home": '"Ural"', "away": '"Fakel"', "home_goals": "5", "away_goals": "2"},
                {"home": '"Dynamo"', "away": '"Lokomotiv"', "home_goals": "0", "away_goals": "0"}],
        intro="Спортивный сайт публикует итог футбольного матча. В заготовке уже есть хозяева `home = {home}`, "
              "гости `away = {away}` и сколько голов забила каждая команда: `home_goals = {home_goals}` и "
              "`away_goals = {away_goals}`.",
        steps=["Первой строкой выведи `FULL TIME`.",
               "Второй строкой выведи пустую строку — вызови `print()` без аргументов.",
               "Третьей строкой выведи обе команды с разделителем `sep=\" vs \"`. "
               "Например, для `\"Ufa\"` и `\"Tver\"` строка будет `Ufa vs Tver`.",
               "Четвёртой строкой выведи голы хозяев и голы гостей с разделителем `sep=\":\"` — без пробелов, "
               "например `3:0`."],
        hint='`sep` задаёт, что `print` ставит между значениями вместо пробела: `print("a", "b", sep=" vs ")` '
             "выводит `a vs b`. Пробелы вокруг `vs` должны быть внутри строки `sep`. Пустую строку выводит `print()`.",
        solution='print("FULL TIME")\nprint()\nprint(home, away, sep=" vs ")\nprint(home_goals, away_goals, sep=":")',
        wrong=[("забывает sep у счёта — между голами пробел вместо двоеточия",
                'print("FULL TIME")\nprint()\nprint(home, away, sep=" vs ")\nprint(home_goals, away_goals)'),
               ("забывает пустую строку после заголовка",
                'print("FULL TIME")\nprint(home, away, sep=" vs ")\nprint(home_goals, away_goals, sep=":")')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-pr-rt-chat-message", title="Уведомление о сообщении",
        given=["author", "text", "day", "month", "hours", "minutes"],
        variants=[{"author": '"Anya"', "text": '"See you tomorrow"', "day": '"12"', "month": '"05"',
                   "hours": '"18"', "minutes": '"30"'},
                  {"author": '"Kirill"', "text": '"Where are you?"', "day": '"03"', "month": '"11"',
                   "hours": '"09"', "minutes": '"05"'},
                  {"author": '"Zlata"', "text": '"Happy birthday!"', "day": '"28"', "month": '"02"',
                   "hours": '"23"', "minutes": '"59"'}],
        hidden=[{"author": '"Denis"', "text": '"Call me"', "day": '"01"', "month": '"01"',
                 "hours": '"00"', "minutes": '"15"'},
                {"author": '"Mila"', "text": '"OK"', "day": '"17"', "month": '"07"',
                 "hours": '"12"', "minutes": '"40"'},
                {"author": '"Ruslan"', "text": '"The bus is late"', "day": '"30"', "month": '"09"',
                 "hours": '"07"', "minutes": '"50"'}],
        intro="Мессенджер показывает уведомление о новом сообщении. В заготовке уже есть автор `author = {author}`, "
              "текст `text = {text}`, дата — день `day = {day}` и месяц `month = {month}`, и время — часы `hours = {hours}` "
              "и минуты `minutes = {minutes}`.",
        steps=["Первой строкой выведи `New message`.",
               "Второй строкой выведи дату и время в виде `12.05 at 18:30`. Сделай это двумя вызовами `print`: "
               "первый выводит день и месяц с разделителем `sep=\".\"` и заканчивает строку не переводом строки, "
               "а текстом ` at ` (`end=\" at \"`, с пробелами по краям); второй выводит часы и минуты с разделителем "
               "`sep=\":\"`.",
               "Третьей строкой выведи автора, двоеточие с пробелом и текст — одним `print` с `sep=\": \"`. "
               "Например, для `\"Oleg\"` и `\"Hi\"` строка будет `Oleg: Hi`."],
        hint='В одном `print` можно указать и `sep`, и `end`: `print("a", "b", sep=".", end=" at ")` выведет `a.b at ` '
             "и не перейдёт на новую строку — следующий `print` продолжит её. `sep` ставится только между значениями, "
             "`end` — один раз в конце.",
        solution='print("New message")\nprint(day, month, sep=".", end=" at ")\nprint(hours, minutes, sep=":")\n'
                 'print(author, text, sep=": ")',
        wrong=[("забывает end — время уходит на следующую строку, а at пропадает",
                'print("New message")\nprint(day, month, sep=".")\nprint(hours, minutes, sep=":")\n'
                'print(author, text, sep=": ")'),
               ("забывает sep у даты — между днём и месяцем пробел вместо точки",
                'print("New message")\nprint(day, month, end=" at ")\nprint(hours, minutes, sep=":")\n'
                'print(author, text, sep=": ")'),
               ("ставит end без пробелов — время прилипает к слову at",
                'print("New message")\nprint(day, month, sep=".", end="at")\nprint(hours, minutes, sep=":")\n'
                'print(author, text, sep=": ")')],
    ),
]
