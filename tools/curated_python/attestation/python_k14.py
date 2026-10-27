"""Attestation, Python, topics 1–14 (up to PY_LOGICAL_AND) — theme: school, exams and the library.
Each task touches every topic of the tier: print with several values, own variables, assignment, arithmetic, order of
execution, int/float (`/` gives a float, a float price), strings glued with `+`, int()/str(), // and %, += -=,
f-strings, if/else, comparison operators, and.
Not yet: or/not, elif, truthiness of non-bool values, loops, lists, string methods and slices, functions, :.2f."""
from build import OutputTask

SKILL = "PY_LOGICAL_AND"
AND = [("And", "Используй and, чтобы объединить проверки в одном условии")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att14-fine", title="Штраф за просроченную книгу",
        given=["book", "pages", "days", "warned"],
        variants=[{"book": '"Dune"', "pages": "412", "days": '"17"', "warned": "True"}],
        hidden=[{"book": '"Emma"', "pages": "380", "days": '"19"', "warned": "True"},
                {"book": '"Ulysses"', "pages": "730", "days": '"20"', "warned": "False"},
                {"book": '"Matilda"', "pages": "240", "days": '"14"', "warned": "True"},
                {"book": '"Holes"', "pages": "233", "days": '"0"', "warned": "False"},
                {"book": '"Beowulf"', "pages": "120", "days": '"30"', "warned": "True"}],
        intro="Ученик вернул в школьную библиотеку книгу `book = {book}` объёмом `pages = {pages}` страниц с опозданием. "
              "Терминал библиотеки передаёт число дней просрочки строкой: `days = {days}`. За каждую полную неделю "
              "просрочки штраф 50 руб., за каждый оставшийся день — 10 руб. Предупреждали ли читателя раньше, "
              "записано в `warned = {warned}`.",
        steps=["Выведи склейкой строк через `+` строку `Book: <book> (<pages> pages)`; число `pages` перед склейкой "
               "преврати в строку через `str()`. Например: `Book: Emma (380 pages)`.",
               "Преврати `days` в целое число через `int()` и сохрани в переменную `late`.",
               "Посчитай число полных недель `weeks` (деление `//` на 7) и оставшихся дней `rest` (остаток `%` от деления на 7).",
               "Выведи через `print` с запятыми: `Late:`, `weeks`, `weeks`, `rest`, `days` — например `Late: 2 weeks 5 days`.",
               "Сохрани в `fine` штраф за недели (`weeks * 50`), а затем добавь к нему штраф за дни через `+=`.",
               "Если штраф не меньше 150 руб. **и** читателя уже предупреждали (`warned`), выведи f-строкой "
               "`Fine: <fine> rub, card blocked`.",
               "Иначе выведи f-строкой `Fine: <fine> rub, with student card <fine / 2> rub` — по студенческому билету "
               "штраф вдвое меньше. Например, для штрафа 110 руб.: `Fine: 110 rub, with student card 55.0 rub`."],
        hint="`19 // 7` — это 2 полные недели, `19 % 7` — 5 оставшихся дней. Деление `/` всегда даёт дробное число: "
             "`110 / 2` — это `55.0`. Штраф ровно 150 руб. уже блокирует карточку, если читателя предупреждали.",
        solution='print("Book: " + book + " (" + str(pages) + " pages)")\nlate = int(days)\nweeks = late // 7\n'
                 'rest = late % 7\nprint("Late:", weeks, "weeks", rest, "days")\nfine = weeks * 50\nfine += rest * 10\n'
                 'if fine >= 150 and warned:\n    print(f"Fine: {fine} rub, card blocked")\nelse:\n'
                 '    print(f"Fine: {fine} rub, with student card {fine / 2} rub")',
        wrong=[("строгое сравнение: штраф ровно 150 руб. карточку не блокирует",
                'print("Book: " + book + " (" + str(pages) + " pages)")\nlate = int(days)\nweeks = late // 7\n'
                'rest = late % 7\nprint("Late:", weeks, "weeks", rest, "days")\nfine = weeks * 50\nfine += rest * 10\n'
                'if fine > 150 and warned:\n    print(f"Fine: {fine} rub, card blocked")\nelse:\n'
                '    print(f"Fine: {fine} rub, with student card {fine / 2} rub")'),
               ("забыта проверка предупреждения: блокирует карточку и тем, кого не предупреждали",
                'print("Book: " + book + " (" + str(pages) + " pages)")\nlate = int(days)\nweeks = late // 7\n'
                'rest = late % 7\nprint("Late:", weeks, "weeks", rest, "days")\nfine = weeks * 50\nfine += rest * 10\n'
                'if fine >= 150:\n    print(f"Fine: {fine} rub, card blocked")\nelse:\n'
                '    print(f"Fine: {fine} rub, with student card {fine / 2} rub")'),
               ("штраф за дни не добавлен к штрафу за недели",
                'print("Book: " + book + " (" + str(pages) + " pages)")\nlate = int(days)\nweeks = late // 7\n'
                'rest = late % 7\nprint("Late:", weeks, "weeks", rest, "days")\nfine = weeks * 50\nfine = rest * 10\n'
                'if fine >= 150 and warned:\n    print(f"Fine: {fine} rub, card blocked")\nelse:\n'
                '    print(f"Fine: {fine} rub, with student card {fine / 2} rub")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att14-seating", title="Рассадка на экзамене",
        given=["room", "students", "minutes", "questions"],
        variants=[{"room": '"A12"', "students": '"27"', "minutes": "90", "questions": "12"}],
        hidden=[{"room": '"B3"', "students": '"30"', "minutes": "60", "questions": "8"},
                {"room": '"C7"', "students": '"36"', "minutes": "80", "questions": "16"},
                {"room": '"D1"', "students": '"29"', "minutes": "100", "questions": "8"},
                {"room": '"E5"', "students": '"12"', "minutes": "45", "questions": "6"},
                {"room": '"F2"', "students": '"5"', "minutes": "90", "questions": "10"}],
        intro="Перед экзаменом в аудитории `room = {room}` рассаживают студентов: в каждом ряду 6 мест. Число студентов "
              "пришло из списка строкой: `students = {students}`. Экзамен идёт `minutes = {minutes}` минут, "
              "в билете `questions = {questions}` вопросов.",
        steps=["Преврати `students` в целое число через `int()` и сохрани в `n`.",
               "Посчитай число полностью занятых рядов `rows` (деление `//` на 6) и число студентов в последнем, "
               "неполном ряду `last` (остаток `%` от деления на 6).",
               "Выведи склейкой строк через `+` строку `Room <room>: <rows> full rows`; число `rows` перед склейкой "
               "преврати в строку через `str()`. Например: `Room B3: 5 full rows`.",
               "Выведи через `print` с запятыми: `Last row:`, `last`, `students` — например `Last row: 3 students`.",
               "Каждому студенту выдают 3 листа, сохрани их число в `sheets`; затем добавь 10 запасных листов через `+=`. "
               "Выведи f-строкой `Sheets: <sheets>`.",
               "Выведи f-строкой `Minutes per question: <minutes / questions>`, например `Minutes per question: 7.5`.",
               "Если неполного ряда нет (`last` равно 0) **и** студентов не больше 30, выведи `Perfect seating`, "
               "иначе — `Seating with gaps`."],
        hint="`27 // 6` — это 4 полных ряда, `27 % 6` — 3 студента в последнем ряду. Деление `/` даёт дробное число: "
             "`60 / 8` — это `7.5`, а `80 / 16` — `5.0`. Ровно 30 студентов ещё помещаются.",
        solution='n = int(students)\nrows = n // 6\nlast = n % 6\nprint("Room " + room + ": " + str(rows) + " full rows")\n'
                 'print("Last row:", last, "students")\nsheets = n * 3\nsheets += 10\nprint(f"Sheets: {sheets}")\n'
                 'print(f"Minutes per question: {minutes / questions}")\nif last == 0 and n <= 30:\n'
                 '    print("Perfect seating")\nelse:\n    print("Seating with gaps")',
        wrong=[("строгое сравнение: ровно 30 студентов считаются лишними",
                'n = int(students)\nrows = n // 6\nlast = n % 6\nprint("Room " + room + ": " + str(rows) + " full rows")\n'
                'print("Last row:", last, "students")\nsheets = n * 3\nsheets += 10\nprint(f"Sheets: {sheets}")\n'
                'print(f"Minutes per question: {minutes / questions}")\nif last == 0 and n < 30:\n'
                '    print("Perfect seating")\nelse:\n    print("Seating with gaps")'),
               ("забыты запасные листы",
                'n = int(students)\nrows = n // 6\nlast = n % 6\nprint("Room " + room + ": " + str(rows) + " full rows")\n'
                'print("Last row:", last, "students")\nsheets = n * 3\nprint(f"Sheets: {sheets}")\n'
                'print(f"Minutes per question: {minutes / questions}")\nif last == 0 and n <= 30:\n'
                '    print("Perfect seating")\nelse:\n    print("Seating with gaps")'),
               ("проверяет только заполненность рядов, а не вместимость",
                'n = int(students)\nrows = n // 6\nlast = n % 6\nprint("Room " + room + ": " + str(rows) + " full rows")\n'
                'print("Last row:", last, "students")\nsheets = n * 3\nsheets += 10\nprint(f"Sheets: {sheets}")\n'
                'print(f"Minutes per question: {minutes / questions}")\nif last == 0:\n'
                '    print("Perfect seating")\nelse:\n    print("Seating with gaps")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att14-reading", title="План чтения к сроку",
        given=["reader", "pages", "days", "read"],
        variants=[{"reader": '"Boris"', "pages": "320", "days": "8", "read": '"105"'}],
        hidden=[{"reader": '"Anya"', "pages": "275", "days": "5", "read": '"105"'},
                {"reader": '"Dina"', "pages": "300", "days": "2", "read": '"104"'},
                {"reader": '"Egor"', "pages": "400", "days": "4", "read": '"180"'},
                {"reader": '"Lena"', "pages": "270", "days": "5", "read": '"130"'},
                {"reader": '"Oleg"', "pages": "150", "days": "10", "read": '"0"'}],
        intro="Читательский клуб школьной библиотеки следит, успевает ли ученик `reader = {reader}` дочитать книгу "
              "в `pages = {pages}` страниц за оставшиеся `days = {days}` дней. Электронный дневник передаёт, сколько "
              "страниц уже прочитано, строкой: `read = {read}`. В книге главы по 25 страниц.",
        steps=["Преврати `read` в целое число через `int()` и сохрани в `done`.",
               "Сегодня прочитано ещё 20 страниц: увеличь `done` на 20 через `+=`.",
               "Выведи склейкой строк через `+` строку `<reader>: <done> pages read`; число `done` преврати в строку "
               "через `str()`. Например: `Anya: 125 pages read`.",
               "Посчитай число полных прочитанных глав `chapters` (деление `//` на 25) и страниц сверх них `extra` "
               "(остаток `%` от деления на 25). Выведи через `print` с запятыми: `Chapters:`, `chapters`, `and`, "
               "`extra`, `pages` — например `Chapters: 5 and 0 pages`.",
               "Посчитай, сколько страниц осталось (`left`), и сколько нужно читать в день: `per_day = left / days`. "
               "Выведи f-строкой `Left: <left>, per day: <per_day>` — например `Left: 150, per day: 30.0`.",
               "Если прочитано не меньше 5 глав **и** в день нужно читать не больше 30 страниц, выведи `On track`, "
               "иначе — `Read faster`."],
        hint="`125 // 25` — это 5 глав, `125 % 25` — 0 страниц сверх них. Деление `/` даёт дробное число: `150 / 5` — "
             "это `30.0`. Ровно 30 страниц в день — ещё нормальный темп.",
        solution='done = int(read)\ndone += 20\nprint(reader + ": " + str(done) + " pages read")\nchapters = done // 25\n'
                 'extra = done % 25\nprint("Chapters:", chapters, "and", extra, "pages")\nleft = pages - done\n'
                 'per_day = left / days\nprint(f"Left: {left}, per day: {per_day}")\n'
                 'if chapters >= 5 and per_day <= 30:\n    print("On track")\nelse:\n    print("Read faster")',
        wrong=[("строгое сравнение: ровно 30 страниц в день считается слишком много",
                'done = int(read)\ndone += 20\nprint(reader + ": " + str(done) + " pages read")\nchapters = done // 25\n'
                'extra = done % 25\nprint("Chapters:", chapters, "and", extra, "pages")\nleft = pages - done\n'
                'per_day = left / days\nprint(f"Left: {left}, per day: {per_day}")\n'
                'if chapters >= 5 and per_day < 30:\n    print("On track")\nelse:\n    print("Read faster")'),
               ("забыты сегодняшние 20 страниц",
                'done = int(read)\nprint(reader + ": " + str(done) + " pages read")\nchapters = done // 25\n'
                'extra = done % 25\nprint("Chapters:", chapters, "and", extra, "pages")\nleft = pages - done\n'
                'per_day = left / days\nprint(f"Left: {left}, per day: {per_day}")\n'
                'if chapters >= 5 and per_day <= 30:\n    print("On track")\nelse:\n    print("Read faster")'),
               ("проверяет только темп, а не число глав",
                'done = int(read)\ndone += 20\nprint(reader + ": " + str(done) + " pages read")\nchapters = done // 25\n'
                'extra = done % 25\nprint("Chapters:", chapters, "and", extra, "pages")\nleft = pages - done\n'
                'per_day = left / days\nprint(f"Left: {left}, per day: {per_day}")\n'
                'if per_day <= 30:\n    print("On track")\nelse:\n    print("Read faster")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att14-timetable", title="Успею ли в кружок",
        given=["start", "lessons", "club"],
        variants=[{"start": "510", "lessons": '"6"', "club": '"chess"'}],
        hidden=[{"start": "520", "lessons": '"6"', "club": '"chess"'},
                {"start": "480", "lessons": '"7"', "club": '"art"'},
                {"start": "480", "lessons": '"4"', "club": '"none"'},
                {"start": "510", "lessons": '"5"', "club": '"music"'},
                {"start": "530", "lessons": '"6"', "club": '"robotics"'}],
        intro="Уроки начинаются в `start = {start}` минут от полуночи (510 — это 8:30). Каждый урок длится 45 минут, "
              "между уроками перемены по 10 минут. Число уроков сегодня электронный дневник передаёт строкой: "
              "`lessons = {lessons}`. Ученик ходит в кружок `club = {club}` (`\"none\"` — если кружка нет), "
              "кружок начинается в 14:00, то есть в 840 минут.",
        steps=["Преврати `lessons` в целое число через `int()` и сохрани в `n`.",
               "Сохрани в `total` время всех уроков (`n * 45`), затем добавь к нему перемены через `+=`: "
               "перемен на одну меньше, чем уроков, то есть `(n - 1) * 10`.",
               "Посчитай `end = start + total` и выведи f-строкой `School day: <total> min`.",
               "Выведи через `print` с запятыми: `Ends at`, часы (`end // 60`), `h`, минуты (`end % 60`), `min` — "
               "например `Ends at 13 h 50 min`.",
               "Посчитай длину уроков в обычных часах: `n * 45 / 60`. Выведи склейкой строк через `+` строку "
               "`Study hours: <hours>`, превратив число в строку через `str()`, например `Study hours: 4.5`.",
               "Если уроки заканчиваются не позже 840 минут **и** `club` не равен `\"none\"`, выведи склейкой строк "
               "`Time for the <club> club`, иначе — `No club today`."],
        hint="`830 // 60` — это 13 часов, `830 % 60` — 50 минут. `6 * 45 / 60` — это `4.5`: деление `/` даёт дробное "
             "число. Если уроки кончаются ровно в 840 минут, в кружок ещё успеваешь. Не равно — это `!=`.",
        solution='n = int(lessons)\ntotal = n * 45\ntotal += (n - 1) * 10\nend = start + total\n'
                 'print(f"School day: {total} min")\nprint("Ends at", end // 60, "h", end % 60, "min")\n'
                 'print("Study hours: " + str(n * 45 / 60))\nif end <= 840 and club != "none":\n'
                 '    print("Time for the " + club + " club")\nelse:\n    print("No club today")',
        wrong=[("строгое сравнение: конец уроков ровно в 14:00 не оставляет времени на кружок",
                'n = int(lessons)\ntotal = n * 45\ntotal += (n - 1) * 10\nend = start + total\n'
                'print(f"School day: {total} min")\nprint("Ends at", end // 60, "h", end % 60, "min")\n'
                'print("Study hours: " + str(n * 45 / 60))\nif end < 840 and club != "none":\n'
                '    print("Time for the " + club + " club")\nelse:\n    print("No club today")'),
               ("перемен столько же, сколько уроков",
                'n = int(lessons)\ntotal = n * 45\ntotal += n * 10\nend = start + total\n'
                'print(f"School day: {total} min")\nprint("Ends at", end // 60, "h", end % 60, "min")\n'
                'print("Study hours: " + str(n * 45 / 60))\nif end <= 840 and club != "none":\n'
                '    print("Time for the " + club + " club")\nelse:\n    print("No club today")'),
               ("забыта проверка, есть ли кружок",
                'n = int(lessons)\ntotal = n * 45\ntotal += (n - 1) * 10\nend = start + total\n'
                'print(f"School day: {total} min")\nprint("Ends at", end // 60, "h", end % 60, "min")\n'
                'print("Study hours: " + str(n * 45 / 60))\nif end <= 840:\n'
                '    print("Time for the " + club + " club")\nelse:\n    print("No club today")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att14-ticket", title="Билет на экзамене",
        given=["name", "ticket", "correct", "time"],
        variants=[{"name": '"Gleb"', "ticket": '"17"', "correct": "14", "time": "75"}],
        hidden=[{"name": '"Ira"', "ticket": '"10"', "correct": "13", "time": "90"},
                {"name": '"Kirill"', "ticket": '"21"', "correct": "12", "time": "60"},
                {"name": '"Masha"', "ticket": '"1"', "correct": "20", "time": "95"},
                {"name": '"Nikita"', "ticket": '"30"', "correct": "15", "time": "40"},
                {"name": '"Polina"', "ticket": '"11"', "correct": "8", "time": "91"}],
        intro="На письменном экзамене 20 вопросов. Студент `name = {name}` вытянул билет с номером, который система "
              "передаёт строкой: `ticket = {ticket}`. Он ответил верно на `correct = {correct}` вопросов и потратил "
              "`time = {time}` минут.",
        steps=["Преврати `ticket` в целое число через `int()` и сохрани в `t`.",
               "Студенты сидят по 10 человек в аудитории: билеты 1–10 — аудитория 1, 11–20 — аудитория 2 и так далее. "
               "Посчитай `room = (t - 1) // 10 + 1`. Выведи склейкой строк через `+` строку `<name>, room <room>`, "
               "превратив `room` в строку через `str()`. Например: `Ira, room 1`.",
               "Нечётные билеты — вариант 2, чётные — вариант 1: `variant = t % 2 + 1`. Выведи через `print` "
               "с запятой `Variant:` и `variant`.",
               "Сохрани в `points` 5 баллов за каждый верный ответ, затем вычти через `-=` по 2 балла за каждый "
               "неверный (`20 - correct`).",
               "Выведи f-строкой `Points: <points>, share: <correct / 20>` — например `Points: 51, share: 0.65`.",
               "Если баллов не меньше 50 **и** студент уложился в 90 минут (не больше 90), выведи `Exam passed`, "
               "иначе — `Retake`."],
        hint="`(10 - 1) // 10 + 1` — это аудитория 1, а `(11 - 1) // 10 + 1` — аудитория 2. `17 % 2` — это 1, "
             "значит вариант 2. Деление `/` даёт дробное число: `13 / 20` — это `0.65`. Ровно 90 минут — ещё вовремя.",
        solution='t = int(ticket)\nroom = (t - 1) // 10 + 1\nprint(name + ", room " + str(room))\nvariant = t % 2 + 1\n'
                 'print("Variant:", variant)\npoints = correct * 5\npoints -= (20 - correct) * 2\n'
                 'print(f"Points: {points}, share: {correct / 20}")\nif points >= 50 and time <= 90:\n'
                 '    print("Exam passed")\nelse:\n    print("Retake")',
        wrong=[("строгое сравнение: ровно 90 минут — уже пересдача",
                't = int(ticket)\nroom = (t - 1) // 10 + 1\nprint(name + ", room " + str(room))\nvariant = t % 2 + 1\n'
                'print("Variant:", variant)\npoints = correct * 5\npoints -= (20 - correct) * 2\n'
                'print(f"Points: {points}, share: {correct / 20}")\nif points >= 50 and time < 90:\n'
                '    print("Exam passed")\nelse:\n    print("Retake")'),
               ("аудитория без «- 1»: билет 10 попадает во вторую аудиторию",
                't = int(ticket)\nroom = t // 10 + 1\nprint(name + ", room " + str(room))\nvariant = t % 2 + 1\n'
                'print("Variant:", variant)\npoints = correct * 5\npoints -= (20 - correct) * 2\n'
                'print(f"Points: {points}, share: {correct / 20}")\nif points >= 50 and time <= 90:\n'
                '    print("Exam passed")\nelse:\n    print("Retake")'),
               ("забыт штраф за неверные ответы",
                't = int(ticket)\nroom = (t - 1) // 10 + 1\nprint(name + ", room " + str(room))\nvariant = t % 2 + 1\n'
                'print("Variant:", variant)\npoints = correct * 5\n'
                'print(f"Points: {points}, share: {correct / 20}")\nif points >= 50 and time <= 90:\n'
                '    print("Exam passed")\nelse:\n    print("Retake")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att14-purchase", title="Закупка книг для библиотеки",
        given=["budget", "price", "genre"],
        variants=[{"budget": '"5000"', "price": "380", "genre": '"science"'}],
        hidden=[{"budget": '"4560"', "price": "380", "genre": '"science"'},
                {"budget": '"4000"', "price": "380", "genre": '"science"'},
                {"budget": '"6000"', "price": "450", "genre": '"poetry"'},
                {"budget": '"3000"', "price": "250", "genre": '"history"'},
                {"budget": '"900"', "price": "300", "genre": '"science"'}],
        intro="Школьная библиотека закупает книги жанра `genre = {genre}` по цене `price = {price}` руб. за штуку. "
              "Бюджет бухгалтерия передала строкой: `budget = {budget}`. Доставка стоит 250 руб., но бесплатна, "
              "если куплено не меньше 12 книг и это научные книги (`\"science\"`). Расходы делят поровну 4 класса.",
        steps=["Выведи склейкой строк через `+` строку `Genre: <genre>`.",
               "Преврати `budget` в целое число через `int()` и сохрани в `money`.",
               "Посчитай, сколько книг можно купить на весь бюджет (`count`, деление `//` на `price`), и сколько денег "
               "останется (`change`, остаток `%`). Выведи через `print` с запятыми `Books:`, `count`, `change:`, "
               "`change`, `rub` — например `Books: 13 change: 60 rub`.",
               "Сохрани стоимость книг (`count * price`) в `total`.",
               "Если книг не меньше 12 **и** жанр равен `\"science\"`, выведи `Free delivery`. Иначе добавь к `total` "
               "стоимость доставки 250 руб. через `+=` и выведи `Delivery: 250 rub`.",
               "В конце (в любом случае) выведи f-строкой `Total: <total> rub, per class: <total / 4>` — например "
               "`Total: 4940 rub, per class: 1235.0`."],
        hint="`5000 // 380` — это 13 книг, `5000 % 380` — 60 руб. сдачи. Деление `/` даёт дробное число: `4050 / 4` — "
             "это `1012.5`. Ровно 12 книг уже дают бесплатную доставку.",
        solution='print("Genre: " + genre)\nmoney = int(budget)\ncount = money // price\nchange = money % price\n'
                 'print("Books:", count, "change:", change, "rub")\ntotal = count * price\n'
                 'if count >= 12 and genre == "science":\n    print("Free delivery")\nelse:\n    total += 250\n'
                 '    print("Delivery: 250 rub")\nprint(f"Total: {total} rub, per class: {total / 4}")',
        wrong=[("строгое сравнение: за ровно 12 книг доставка платная",
                'print("Genre: " + genre)\nmoney = int(budget)\ncount = money // price\nchange = money % price\n'
                'print("Books:", count, "change:", change, "rub")\ntotal = count * price\n'
                'if count > 12 and genre == "science":\n    print("Free delivery")\nelse:\n    total += 250\n'
                '    print("Delivery: 250 rub")\nprint(f"Total: {total} rub, per class: {total / 4}")'),
               ("печатает строку о доставке, но не прибавляет её к сумме",
                'print("Genre: " + genre)\nmoney = int(budget)\ncount = money // price\nchange = money % price\n'
                'print("Books:", count, "change:", change, "rub")\ntotal = count * price\n'
                'if count >= 12 and genre == "science":\n    print("Free delivery")\nelse:\n'
                '    print("Delivery: 250 rub")\nprint(f"Total: {total} rub, per class: {total / 4}")'),
               ("забыта проверка жанра",
                'print("Genre: " + genre)\nmoney = int(budget)\ncount = money // price\nchange = money % price\n'
                'print("Books:", count, "change:", change, "rub")\ntotal = count * price\n'
                'if count >= 12:\n    print("Free delivery")\nelse:\n    total += 250\n'
                '    print("Delivery: 250 rub")\nprint(f"Total: {total} rub, per class: {total / 4}")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att14-quarter", title="Оценка за четверть",
        given=["name", "m1", "m2", "m3", "m4", "absences"],
        variants=[{"name": '"Vera"', "m1": "5", "m2": "4", "m3": "4", "m4": "5", "absences": '"3"'}],
        hidden=[{"name": '"Artem"', "m1": "5", "m2": "5", "m3": "5", "m4": "5", "absences": '"0"'},
                {"name": '"Sonya"', "m1": "4", "m2": "3", "m3": "4", "m4": "3", "absences": '"5"'},
                {"name": '"Timur"', "m1": "4", "m2": "4", "m3": "5", "m4": "4", "absences": '"2"'},
                {"name": '"Yulia"', "m1": "5", "m2": "4", "m3": "5", "m4": "4", "absences": '"8"'},
                {"name": '"Denis"', "m1": "3", "m2": "3", "m3": "2", "m4": "3", "absences": '"6"'},
                {"name": '"Kira"', "m1": "3", "m2": "3", "m3": "2", "m4": "3", "absences": '"1"'}],
        intro="Учитель выставляет ученику `name = {name}` оценку за четверть по четырём оценкам `m1 = {m1}`, "
              "`m2 = {m2}`, `m3 = {m3}`, `m4 = {m4}`. Число пропусков журнал передаёт строкой: `absences = {absences}`. "
              "Оценку округляют вверх, только если до следующей не хватает немного и пропусков мало.",
        steps=["Выведи склейкой строк через `+` строку `Report for <name>`.",
               "Сохрани сумму четырёх оценок в `total` и выведи через `print` с запятой `Average:` и `total / 4` — "
               "например `Average: 4.5`.",
               "Сохрани в `grade` целую часть среднего: `total // 4`.",
               "Преврати `absences` в целое число через `int()` и сохрани в `missed`.",
               "Если остаток `total % 4` не меньше 2 **и** пропусков не больше 5, увеличь `grade` на 1 через `+=` "
               "и выведи `Rounded up`. Иначе выведи `No rounding up`.",
               "В конце (в любом случае) выведи f-строкой `Quarter grade: <grade>`."],
        hint="Для оценок 5, 4, 4, 5 сумма 18: `18 / 4` — это `4.5`, `18 // 4` — это 4, `18 % 4` — это 2, "
             "значит при малом числе пропусков оценка станет 5. Ровно 5 пропусков ещё позволяют округлить вверх.",
        solution='print("Report for " + name)\ntotal = m1 + m2 + m3 + m4\nprint("Average:", total / 4)\ngrade = total // 4\n'
                 'missed = int(absences)\nif total % 4 >= 2 and missed <= 5:\n    grade += 1\n    print("Rounded up")\n'
                 'else:\n    print("No rounding up")\nprint(f"Quarter grade: {grade}")',
        wrong=[("строгое сравнение: при 5 пропусках оценку уже не округляют",
                'print("Report for " + name)\ntotal = m1 + m2 + m3 + m4\nprint("Average:", total / 4)\ngrade = total // 4\n'
                'missed = int(absences)\nif total % 4 >= 2 and missed < 5:\n    grade += 1\n    print("Rounded up")\n'
                'else:\n    print("No rounding up")\nprint(f"Quarter grade: {grade}")'),
               ("округляет при любом остатке, кроме нуля",
                'print("Report for " + name)\ntotal = m1 + m2 + m3 + m4\nprint("Average:", total / 4)\ngrade = total // 4\n'
                'missed = int(absences)\nif total % 4 >= 1 and missed <= 5:\n    grade += 1\n    print("Rounded up")\n'
                'else:\n    print("No rounding up")\nprint(f"Quarter grade: {grade}")'),
               ("забыта проверка пропусков",
                'print("Report for " + name)\ntotal = m1 + m2 + m3 + m4\nprint("Average:", total / 4)\ngrade = total // 4\n'
                'missed = int(absences)\nif total % 4 >= 2:\n    grade += 1\n    print("Rounded up")\n'
                'else:\n    print("No rounding up")\nprint(f"Quarter grade: {grade}")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att14-printer", title="Принтер в читальном зале",
        given=["doc", "pages", "copies", "paper"],
        variants=[{"doc": '"Essay"', "pages": "7", "copies": '"3"', "paper": "40"}],
        hidden=[{"doc": '"Report"', "pages": "10", "copies": '"4"', "paper": "20"},
                {"doc": '"Notes"', "pages": "9", "copies": '"5"', "paper": "100"},
                {"doc": '"Thesis"', "pages": "30", "copies": '"3"', "paper": "100"},
                {"doc": '"Poster"', "pages": "15", "copies": '"2"', "paper": "10"},
                {"doc": '"Quiz"', "pages": "1", "copies": '"6"', "paper": "5"}],
        intro="В читальном зале библиотеки печатают с двух сторон листа. Ученик печатает документ `doc = {doc}` "
              "на `pages = {pages}` страниц, число копий приходит из формы строкой: `copies = {copies}`. Лист стоит "
              "3.5 руб., в лотке принтера `paper = {paper}` листов.",
        steps=["Преврати `copies` в целое число через `int()` и сохрани в `n`.",
               "На лист помещаются 2 страницы, последняя нечётная страница занимает отдельный лист: "
               "`sheets = pages // 2 + pages % 2`. Сохрани в `total` число листов на все копии (`sheets * n`).",
               "Посчитай стоимость `cost = total * 3.5`.",
               "Выведи склейкой строк через `+` строку `Document: <doc>, <pages> pages`, превратив `pages` в строку "
               "через `str()`. Например: `Document: Report, 10 pages`.",
               "Выведи через `print` с запятыми: `Sheets:`, `total`, `cost:`, `cost`, `rub` — например "
               "`Sheets: 20 cost: 70.0 rub`.",
               "Если листов в лотке хватает (`total` не больше `paper`) **и** стоимость не больше 150 руб., уменьши "
               "`paper` на `total` через `-=` и выведи f-строкой `Printing, paper left: <paper>`. "
               "Иначе выведи `Ask the librarian`."],
        hint="Для 7 страниц: `7 // 2` — это 3 полных листа, `7 % 2` — ещё 1 лист для последней страницы, всего 4. "
             "Цена дробная, поэтому и стоимость дробная: `12 * 3.5` — это `42.0`. Если листов в лотке ровно столько, "
             "сколько нужно, печатать можно.",
        solution='n = int(copies)\nsheets = pages // 2 + pages % 2\ntotal = sheets * n\ncost = total * 3.5\n'
                 'print("Document: " + doc + ", " + str(pages) + " pages")\nprint("Sheets:", total, "cost:", cost, "rub")\n'
                 'if total <= paper and cost <= 150:\n    paper -= total\n    print(f"Printing, paper left: {paper}")\n'
                 'else:\n    print("Ask the librarian")',
        wrong=[("теряет последнюю нечётную страницу",
                'n = int(copies)\nsheets = pages // 2\ntotal = sheets * n\ncost = total * 3.5\n'
                'print("Document: " + doc + ", " + str(pages) + " pages")\nprint("Sheets:", total, "cost:", cost, "rub")\n'
                'if total <= paper and cost <= 150:\n    paper -= total\n    print(f"Printing, paper left: {paper}")\n'
                'else:\n    print("Ask the librarian")'),
               ("строгое сравнение: когда листов ровно хватает, печатать нельзя",
                'n = int(copies)\nsheets = pages // 2 + pages % 2\ntotal = sheets * n\ncost = total * 3.5\n'
                'print("Document: " + doc + ", " + str(pages) + " pages")\nprint("Sheets:", total, "cost:", cost, "rub")\n'
                'if total < paper and cost <= 150:\n    paper -= total\n    print(f"Printing, paper left: {paper}")\n'
                'else:\n    print("Ask the librarian")'),
               ("забыта проверка стоимости",
                'n = int(copies)\nsheets = pages // 2 + pages % 2\ntotal = sheets * n\ncost = total * 3.5\n'
                'print("Document: " + doc + ", " + str(pages) + " pages")\nprint("Sheets:", total, "cost:", cost, "rub")\n'
                'if total <= paper:\n    paper -= total\n    print(f"Printing, paper left: {paper}")\n'
                'else:\n    print("Ask the librarian")')],
        constructs=["if"],
        must_use=AND,
    ),
]
