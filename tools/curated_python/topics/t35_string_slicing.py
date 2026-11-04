"""PY_STRING_SLICING — «Срезы строк». Taught before: print, variables, arithmetic, int/float, strings, type conversion,
// and %, += -=, f-strings, conditions, for/while loops, break/continue, lists (indexes, append, len, in, iterating).
Here: s[a:b], s[:n], s[n:], negative bounds, a step: s[::2], s[1::2], s[::-1].
Not yet: string methods (upper, strip, split, replace, find, …), functions."""
from build import OutputTask

SKILL = "PY_STRING_SLICING"

NEED_SLICE = ("Slice", "Реши задачу срезами строки: вида `text[a:b]`, `text[:n]`, `text[::-1]`.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ss-date", title="Дата в другом формате",
        given=["date"],
        variants=[{"date": '"2026-10-22"'}, {"date": '"2025-03-08"'}, {"date": '"2024-12-31"'}],
        hidden=[{"date": '"2027-01-05"'}, {"date": '"1999-07-14"'}, {"date": '"2030-11-30"'}],
        intro="Программа получает дату в виде строки `date = {date}`: год из 4 цифр, дефис, месяц из 2 цифр, дефис, "
              "день из 2 цифр. Нужно разобрать её на части и записать по-русски: день, месяц, год через точку.",
        steps=["Срезом вырежи из `date` год (символы с индексами 0–3) в переменную `year`.",
               "Так же вырежи месяц (индексы 5–6) в `month` и день (с индекса 8 до конца) в `day`.",
               "Выведи три строки: `Year: 2026`, `Month: 10` и дату в виде `22.10.2026`"],
        hint="В срезе `text[a:b]` символ с индексом `b` уже не входит: `\"2026-10-22\"[0:4]` — это `\"2026\"`. "
             "Если правую границу не писать, срез идёт до конца строки.",
        solution='year = date[:4]\nmonth = date[5:7]\nday = date[8:]\nprint(f"Year: {year}")\nprint(f"Month: {month}")\n'
                 'print(f"{day}.{month}.{year}")',
        wrong=[("правая граница среза не входит: от месяца осталась одна цифра",
                'year = date[:4]\nmonth = date[5:6]\nday = date[8:]\nprint(f"Year: {year}")\nprint(f"Month: {month}")\n'
                'print(f"{day}.{month}.{year}")'),
               ("срез [0:3]: от года осталось три цифры",
                'year = date[0:3]\nmonth = date[5:7]\nday = date[8:]\nprint(f"Year: {year}")\nprint(f"Month: {month}")\n'
                'print(f"{day}.{month}.{year}")')],
        must_use=[NEED_SLICE],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ss-phone", title="Скрытый номер телефона",
        given=["phone"],
        variants=[{"phone": '"+79161234567"'}, {"phone": '"+79035550192"'}, {"phone": '"+79876543210"'}],
        hidden=[{"phone": '"+79001112233"'}, {"phone": '"+79995554433"'}, {"phone": '"+79270000001"'}],
        intro="Интернет-магазин показывает номер телефона покупателя не полностью. Номер записан строкой `phone = {phone}`: "
              "`+7`, потом 3 цифры кода оператора, потом ещё 7 цифр.",
        steps=["Срезом вырежи код оператора — 3 цифры сразу после `+7` — в переменную `code`.",
               "Срезом с отрицательной границей вырежи последние 4 цифры номера в переменную `last`.",
               "Выведи три строки: `Operator code: 916`, `Last digits: 4567` и скрытый номер `Hidden: +7******4567` — "
               "первые два символа номера, шесть звёздочек и последние 4 цифры."],
        hint="Символы `+` и `7` стоят под индексами 0 и 1, поэтому код начинается с индекса 2. "
             "Срез `text[-4:]` — это последние 4 символа строки: правую границу не пишут, чтобы дойти до конца.",
        solution='code = phone[2:5]\nlast = phone[-4:]\nprint(f"Operator code: {code}")\nprint(f"Last digits: {last}")\n'
                 'print(f"Hidden: {phone[:2]}******{last}")',
        wrong=[("срез [-4:-1] не доходит до конца: последней цифры нет",
                'code = phone[2:5]\nlast = phone[-4:-1]\nprint(f"Operator code: {code}")\nprint(f"Last digits: {last}")\n'
                'print(f"Hidden: {phone[:2]}******{last}")'),
               ("код вырезан на один символ раньше: в него попала 7",
                'code = phone[1:4]\nlast = phone[-4:]\nprint(f"Operator code: {code}")\nprint(f"Last digits: {last}")\n'
                'print(f"Hidden: {phone[:2]}******{last}")')],
        must_use=[NEED_SLICE],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ss-palindrome", title="Слово-перевёртыш",
        given=["word"],
        variants=[{"word": '"level"'}, {"word": '"robot"'}, {"word": '"racecar"'}],
        hidden=[{"word": '"noon"'}, {"word": '"a"'}, {"word": '"python"'}],
        intro="Ребята играют в перевёртыши: слово записывают задом наперёд и смотрят, не получилось ли то же самое слово. "
              "Такие слова называют палиндромами. Слово записано в переменной `word = {word}`.",
        steps=["Срезом с шагом -1 получи слово задом наперёд и сохрани его в переменную `backwards`.",
               "Выведи `Word: robot` и следующей строкой `Backwards: tobor`",
               "Если слово совпадает со своим перевёртышем, выведи `Palindrome`, иначе выведи `Not a palindrome`"],
        hint="Третье число в срезе — шаг. Срез `text[::-1]` проходит всю строку с конца к началу. "
             "Не путай его со срезом `text[:-1]` — это строка без последнего символа.",
        solution='backwards = word[::-1]\nprint(f"Word: {word}")\nprint(f"Backwards: {backwards}")\nif word == backwards:\n'
                 '    print("Palindrome")\nelse:\n    print("Not a palindrome")',
        wrong=[("срез [:-1] вместо [::-1]: просто отрезает последнюю букву",
                'backwards = word[:-1]\nprint(f"Word: {word}")\nprint(f"Backwards: {backwards}")\nif word == backwards:\n'
                '    print("Palindrome")\nelse:\n    print("Not a palindrome")'),
               ("печатает исходное слово вместо перевёртыша",
                'backwards = word[::-1]\nprint(f"Word: {word}")\nprint(f"Backwards: {word}")\nif word == backwards:\n'
                '    print("Palindrome")\nelse:\n    print("Not a palindrome")')],
        constructs=["if"],
        must_use=[NEED_SLICE],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ss-login", title="Логин для школьного портала",
        given=["first", "last", "year"],
        variants=[{"first": '"Anna"', "last": '"Petrova"', "year": '"2011"'},
                  {"first": '"Boris"', "last": '"Ivanov"', "year": '"2010"'},
                  {"first": '"Vika"', "last": '"Sokolova"', "year": '"2012"'}],
        hidden=[{"first": '"Lev"', "last": '"Li"', "year": '"2009"'},
                {"first": '"Timur"', "last": '"Kozlov"', "year": '"2013"'},
                {"first": '"Mila"', "last": '"Orlova"', "year": '"2008"'}],
        intro="Школьный портал выдаёт ученикам логины. Логин — это первые 4 буквы фамилии, первая буква имени "
              "и две последние цифры года рождения. Имя, фамилия и год записаны строками: `first = {first}`, "
              "`last = {last}`, `year = {year}`.",
        steps=["Возьми первую букву имени в переменную `initial`, первые 4 буквы фамилии — в `part`, "
               "последние 2 цифры года — в `digits`. Используй срезы.",
               "Выведи строку для журнала: фамилию, пробел, первую букву имени и точку — `Student: Petrova A.`",
               "Следующей строкой выведи логин: `Login: PetrA11`"],
        hint="Срез `text[:4]` даёт первые 4 символа, а если строка короче, — всю строку, без ошибки. "
             "Последние 2 символа — `text[-2:]`; а `text[-2]` — это только один символ.",
        solution='initial = first[:1]\npart = last[:4]\ndigits = year[-2:]\nprint(f"Student: {last} {initial}.")\n'
                 'print(f"Login: {part}{initial}{digits}")',
        wrong=[("year[-2] — это одна цифра, а не две",
                'initial = first[:1]\npart = last[:4]\ndigits = year[-2]\nprint(f"Student: {last} {initial}.")\n'
                'print(f"Login: {part}{initial}{digits}")'),
               ("срез фамилии с индекса 1: пропущена первая буква",
                'initial = first[:1]\npart = last[1:5]\ndigits = year[-2:]\nprint(f"Student: {last} {initial}.")\n'
                'print(f"Login: {part}{initial}{digits}")')],
        must_use=[NEED_SLICE],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ss-spy", title="Шифровка разведчика",
        given=["code"],
        variants=[{"code": '"xOqLzLwEkH"'}, {"code": '"aYbPcS"'}, {"code": '"mTnNpEqGrA"'}],
        hidden=[{"code": '"zOzG"'}, {"code": '"aTbEcRdCeEfS"'}, {"code": '"xNyUzR"'}],
        intro="Разведчик прислал шифровку `code = {code}`. Настоящее сообщение спрятано в символах с нечётными "
              "индексами (1, 3, 5, …) и записано задом наперёд, а символы с чётными индексами (0, 2, 4, …) — "
              "просто шум.",
        steps=["Срезом с шагом 2, начиная с индекса 1, вырежи символы сообщения в переменную `letters`.",
               "Разверни `letters` срезом с шагом -1 и сохрани в `message`.",
               "Срезом с шагом 2 от начала строки вырежи шум в переменную `noise`.",
               "Выведи три строки: `Noise: xqzwk`, `Message: HELLO` и длину сообщения `Letters: 5`"],
        hint="В срезе `text[start::step]` первое число — откуда начать, последнее — шаг: `\"abcdef\"[1::2]` — это "
             "`\"bdf\"`. Развернуть строку можно срезом `[::-1]`.",
        solution='letters = code[1::2]\nmessage = letters[::-1]\nnoise = code[::2]\nprint(f"Noise: {noise}")\n'
                 'print(f"Message: {message}")\nprint(f"Letters: {len(message)}")',
        wrong=[("берёт символы с чётными индексами: вместо сообщения получается шум",
                'letters = code[::2]\nmessage = letters[::-1]\nnoise = code[::2]\nprint(f"Noise: {noise}")\n'
                'print(f"Message: {message}")\nprint(f"Letters: {len(message)}")'),
               ("забыл развернуть: сообщение остаётся задом наперёд",
                'letters = code[1::2]\nmessage = letters\nnoise = code[::2]\nprint(f"Noise: {noise}")\n'
                'print(f"Message: {message}")\nprint(f"Letters: {len(message)}")')],
        must_use=[NEED_SLICE],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ss-travel", title="Сколько ехать на поезде",
        given=["start", "end"],
        variants=[{"start": '"08:45"', "end": '"11:20"'}, {"start": '"09:10"', "end": '"13:05"'},
                  {"start": '"14:30"', "end": '"16:30"'}],
        hidden=[{"start": '"00:00"', "end": '"00:01"'}, {"start": '"07:55"', "end": '"22:10"'},
                {"start": '"12:00"', "end": '"12:59"'}],
        intro="Поезд отправляется в `start = {start}` и прибывает в `end = {end}` того же дня. Время записано строкой: "
              "две цифры часов, двоеточие, две цифры минут. Узнай, сколько длится поездка.",
        steps=["Срезами вырежи часы и минуты отправления и переведи их в числа через `int`: `h1` и `m1`. "
               "Так же получи `h2` и `m2` для прибытия.",
               "Переведи оба момента в минуты от полуночи (часы * 60 + минуты) и посчитай разницу `total`.",
               "Выведи `Minutes: 155` и следующей строкой `Travel time: 2 h 35 min` — целые часы (`//`) "
               "и оставшиеся минуты (`%`)."],
        hint="В строке `\"08:45\"` часы — символы с индексами 0 и 1, двоеточие — индекс 2, минуты — с индекса 3 до конца. "
             "`int(\"08\")` даёт 8.",
        solution='h1 = int(start[:2])\nm1 = int(start[3:])\nh2 = int(end[:2])\nm2 = int(end[3:])\n'
                 'total = (h2 * 60 + m2) - (h1 * 60 + m1)\nprint(f"Minutes: {total}")\n'
                 'print(f"Travel time: {total // 60} h {total % 60} min")',
        wrong=[("минуты отправления вырезаны с индекса 4: от них осталась одна цифра",
                'h1 = int(start[:2])\nm1 = int(start[4:])\nh2 = int(end[:2])\nm2 = int(end[3:])\n'
                'total = (h2 * 60 + m2) - (h1 * 60 + m1)\nprint(f"Minutes: {total}")\n'
                'print(f"Travel time: {total // 60} h {total % 60} min")'),
               ("часы отправления вырезаны срезом [:1]: осталась одна цифра",
                'h1 = int(start[:1])\nm1 = int(start[3:])\nh2 = int(end[:2])\nm2 = int(end[3:])\n'
                'total = (h2 * 60 + m2) - (h1 * 60 + m1)\nprint(f"Minutes: {total}")\n'
                'print(f"Travel time: {total // 60} h {total % 60} min")')],
        must_use=[NEED_SLICE],
    ),
]
