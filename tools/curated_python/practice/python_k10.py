"""Training attestation («Тренировочная аттестация»), Python, tier up to topic 10 PY_ASSIGNMENT_OPERATORS — «Составное
присваивание += -=». Each task has the size and kind of the real attestation and touches every topic 1–10: print
(several values, commas), variables, assignment (a new variable from a value), arithmetic + - * / and parentheses, order
of execution (what is computed before a change keeps the old value), int and float (`/` gives a float), strings (gluing
with `+`, repeating with `*`, `len()`), type conversion int()/float()/str(), // and %, += -=.
Theme: music, concerts and cinema; every story is different (and different from the real attestation pool).
Not yet: f-strings, conditions and comparisons, loops, lists, functions, round(), string methods and slices."""
from build import OutputTask

SKILL = "PY_ASSIGNMENT_OPERATORS"
AUG = [("AugAssign", "Используй составное присваивание (+=, -=), чтобы изменить переменную")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac10-cartoon", title="Мультфильм",
        given=["title", "frames", "added", "cut"],
        variants=[{"title": '"Red Fox"', "frames": '"1240"', "added": "85", "cut": "40"}],
        hidden=[{"title": '"Owl"', "frames": '"500"', "added": "0", "cut": "0"},
                {"title": '"Blue Whale"', "frames": '"10"', "added": "3", "cut": "1"},
                {"title": '"Cat"', "frames": '"2999"', "added": "1", "cut": "25"},
                {"title": '"Hedgehog"', "frames": '"730"', "added": "120", "cut": "7"}],
        intro="Студия рисует короткий мультфильм `title = {title}`. Программа монтажа показывает, сколько в нём кадров, "
              "строкой: `frames = {frames}`. За день аниматор дорисовал ещё `added = {added}` кадров, а режиссёр "
              "вырезал `cut = {cut}` неудачных. Мультфильм показывают со скоростью 25 кадров в секунду.",
        steps=["Заведи переменную `total` — число кадров из `frames`, превращённое в целое число с помощью `int()`.",
               "Прибавь к `total` дорисованные кадры с помощью `+=`, затем вычти вырезанные с помощью `-=`.",
               "Выведи одной строкой, склеив части через `+`: название, `\": \"`, число кадров (через `str()`) и "
               "`\" frames\"` — получится, например, `Red Fox: 1285 frames`.",
               "Посчитай длину мультфильма в секундах: `total`, делённое на 25 (обычным делением `/`). "
               "Выведи `Length:`, длину и `s` через `print` с запятыми.",
               "Для монтажа длину записывают таймкодом: полные секунды (`total // 25`) и кадры, которые остались сверх "
               "них (`total % 25`). Выведи `Timecode:`, секунды, `s`, кадры и `fr` (от frames — кадры) через `print` "
               "с запятыми."],
        hint="Длину и таймкод считай уже после того, как добавил и вырезал кадры. Деление `/` всегда даёт дробное число: "
             "`500 / 25` — это `20.0`. А `1285 // 25` даёт `51`, `1285 % 25` — `10`: эти 10 кадров и есть 0.4 секунды.",
        solution='total = int(frames)\ntotal += added\ntotal -= cut\nprint(title + ": " + str(total) + " frames")\n'
                 'length = total / 25\nprint("Length:", length, "s")\n'
                 'secs = total // 25\nrest = total % 25\nprint("Timecode:", secs, "s", rest, "fr")',
        wrong=[("считает длину до того, как вырезал неудачные кадры",
                'total = int(frames)\ntotal += added\nlength = total / 25\ntotal -= cut\n'
                'print(title + ": " + str(total) + " frames")\nprint("Length:", length, "s")\n'
                'secs = total // 25\nrest = total % 25\nprint("Timecode:", secs, "s", rest, "fr")'),
               ("путает // и %: секунды и кадры в таймкоде меняются местами",
                'total = int(frames)\ntotal += added\ntotal -= cut\nprint(title + ": " + str(total) + " frames")\n'
                'length = total / 25\nprint("Length:", length, "s")\n'
                'secs = total % 25\nrest = total // 25\nprint("Timecode:", secs, "s", rest, "fr")'),
               ("длину считает делением нацело // — теряется дробная часть секунды",
                'total = int(frames)\ntotal += added\ntotal -= cut\nprint(title + ": " + str(total) + " frames")\n'
                'length = total // 25\nprint("Length:", length, "s")\n'
                'secs = total // 25\nrest = total % 25\nprint("Timecode:", secs, "s", rest, "fr")')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac10-band-fee", title="Гонорар группы",
        given=["band", "fee", "hours", "members"],
        variants=[{"band": '"Night Owls"', "fee": '"47350"', "hours": '"2.5"', "members": "4"}],
        hidden=[{"band": '"Echo"', "fee": '"30000"', "hours": '"2.0"', "members": "3"},
                {"band": '"Jazz Cats"', "fee": '"9999"', "hours": '"1.25"', "members": "7"},
                {"band": '"Duo"', "fee": '"12345"', "hours": '"2.5"', "members": "2"},
                {"band": '"Big Band"', "fee": '"100000"', "hours": '"4.0"', "members": "12"},
                {"band": '"Solo"', "fee": '"2005"', "hours": '"0.5"', "members": "1"}],
        intro="Группа `band = {band}` отыграла концерт. Организатор прислал гонорар и длительность концерта строками: "
              "`fee = {fee}` руб. и `hours = {hours}` ч. Из гонорара 10% получает звукорежиссёр (копейки "
              "отбрасываются), а 1500 руб. уходит на такси для инструментов. Остаток делят поровну между "
              "`members = {members}` музыкантами, а рубли, которые поровну не делятся, кладут в копилку группы.",
        steps=["Заведи переменную `money` — гонорар из `fee`, превращённый в целое число с помощью `int()`.",
               "Посчитай, сколько группа заработала за час концерта: `money`, делённое на длительность, превращённую "
               "в дробное число с помощью `float()`. Выведи `Per hour:`, это число и `rub` через `print` с запятыми.",
               "Посчитай долю звукорежиссёра `sound` — `money // 10`. Вычти её из `money` с помощью `-=`, а потом "
               "так же вычти 1500 руб. на такси.",
               "Выведи одной строкой, склеив части через `+`: название группы, `\" share \"`, `money` (через `str()`) "
               "и `\" rub\"` — получится, например, `Night Owls share 41115 rub`.",
               "Посчитай долю каждого музыканта `share` (`money // members`) и сколько рублей уйдёт в копилку `fund` "
               "(`money % members`). Выведи две строки через `print` с запятыми: `Each:`, доля и `rub`, затем "
               "`Fund:`, копилка и `rub`."],
        hint="Заработок за час считай по всему гонорару — до вычетов. `float(\"2.5\")` даёт число `2.5`, а деление `/` "
             "всегда даёт дробное число. `41115 // 4` даёт `10278`, а `41115 % 4` — `3`: столько рублей поровну не делится.",
        solution='money = int(fee)\nper_hour = money / float(hours)\nprint("Per hour:", per_hour, "rub")\n'
                 'sound = money // 10\nmoney -= sound\nmoney -= 1500\nprint(band + " share " + str(money) + " rub")\n'
                 'share = money // members\nfund = money % members\nprint("Each:", share, "rub")\nprint("Fund:", fund, "rub")',
        wrong=[("считает заработок за час уже после вычетов, а не по всему гонорару",
                'money = int(fee)\nsound = money // 10\nmoney -= sound\nmoney -= 1500\n'
                'per_hour = money / float(hours)\nprint("Per hour:", per_hour, "rub")\n'
                'print(band + " share " + str(money) + " rub")\n'
                'share = money // members\nfund = money % members\nprint("Each:", share, "rub")\nprint("Fund:", fund, "rub")'),
               ("долю звукорежиссёра считает остатком % вместо деления нацело //",
                'money = int(fee)\nper_hour = money / float(hours)\nprint("Per hour:", per_hour, "rub")\n'
                'sound = money % 10\nmoney -= sound\nmoney -= 1500\nprint(band + " share " + str(money) + " rub")\n'
                'share = money // members\nfund = money % members\nprint("Each:", share, "rub")\nprint("Fund:", fund, "rub")'),
               ("долю музыканта считает обычным делением / — получается дробное число",
                'money = int(fee)\nper_hour = money / float(hours)\nprint("Per hour:", per_hour, "rub")\n'
                'sound = money // 10\nmoney -= sound\nmoney -= 1500\nprint(band + " share " + str(money) + " rub")\n'
                'share = money / members\nfund = money % members\nprint("Each:", share, "rub")\nprint("Fund:", fund, "rub")')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac10-subtitles", title="Субтитры",
        given=["hero", "phrase", "start"],
        variants=[{"hero": '"Captain"', "phrase": '"We fly at dawn"', "start": '"754"'}],
        hidden=[{"hero": '"Ann"', "phrase": '"Run!"', "start": '"61"'},
                {"hero": '"Doctor"', "phrase": '"The ship is ready now"', "start": '"122"'},
                {"hero": '"Mila"', "phrase": '"I knew it!"', "start": '"3600"'},
                {"hero": '"Old man"', "phrase": '"The sea is calm today"', "start": '"2"'}],
        intro="Переводчик делает субтитры к фильму. Герой `hero = {hero}` говорит реплику `phrase = {phrase}`. "
              "В файле субтитров время, когда реплика появляется, записано строкой — секунд от начала фильма: "
              "`start = {start}`. Строка экрана вмещает 30 символов, субтитр ставят по центру, а края экрана "
              "отмечают знаком `|`.",
        steps=["Склей субтитр `line`: имя героя, `\": \"` и реплика.",
               "Посчитай отступ слева `left` — половина свободного места, деление нацело: `(30 - len(line)) // 2`. "
               "Отступ справа `right` — всё остальное свободное место: `30 - len(line) - left`.",
               "Выведи строку экрана, склеив через `+`: `\"|\"`, пробел `\" \"`, повторённый `left` раз, `line`, "
               "пробел, повторённый `right` раз, и `\"|\"`.",
               "Субтитр держат на экране по 1 секунде на каждые 10 символов. Посчитай время показа — длина `line`, "
               "делённая на 10 (обычным делением `/`). Выведи `Show:`, это время и `s` через `print` с запятыми.",
               "Заведи `t` — время появления из `start`, превращённое в целое число с помощью `int()`. Режиссёр "
               "попросил показывать субтитр на 2 секунды раньше: вычти 2 из `t` с помощью `-=`.",
               "Выведи время появления в минутах и секундах: `At`, `t // 60`, `min`, `t % 60` и `s` через `print` "
               "с запятыми — получится, например, `At 12 min 32 s`."],
        hint="`len(\"Bo: Hi!\")` — это 7: пробелы и знаки тоже считаются. Если свободных мест нечётное число, справа "
             "окажется на один пробел больше, чем слева, поэтому `right` не всегда равен `left`. "
             "`\" \" * 0` — пустая строка. Деление `/` всегда даёт дробное число: `30 / 10` — это `3.0`.",
        solution='line = hero + ": " + phrase\nleft = (30 - len(line)) // 2\nright = 30 - len(line) - left\n'
                 'print("|" + " " * left + line + " " * right + "|")\n'
                 'show = len(line) / 10\nprint("Show:", show, "s")\n'
                 't = int(start)\nt -= 2\nprint("At", t // 60, "min", t % 60, "s")',
        wrong=[("делает отступ справа таким же, как слева: при нечётном свободном месте строка экрана короче",
                'line = hero + ": " + phrase\nleft = (30 - len(line)) // 2\nright = left\n'
                'print("|" + " " * left + line + " " * right + "|")\n'
                'show = len(line) / 10\nprint("Show:", show, "s")\n'
                't = int(start)\nt -= 2\nprint("At", t // 60, "min", t % 60, "s")'),
               ("забывает показать субтитр на 2 секунды раньше",
                'line = hero + ": " + phrase\nleft = (30 - len(line)) // 2\nright = 30 - len(line) - left\n'
                'print("|" + " " * left + line + " " * right + "|")\n'
                'show = len(line) / 10\nprint("Show:", show, "s")\n'
                't = int(start)\nprint("At", t // 60, "min", t % 60, "s")'),
               ("время показа считает делением нацело // — теряется дробная часть",
                'line = hero + ": " + phrase\nleft = (30 - len(line)) // 2\nright = 30 - len(line) - left\n'
                'print("|" + " " * left + line + " " * right + "|")\n'
                'show = len(line) // 10\nprint("Show:", show, "s")\n'
                't = int(start)\nt -= 2\nprint("At", t // 60, "min", t % 60, "s")')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-prac10-metronome", title="Метроном",
        given=["piece", "bpm", "step", "beats"],
        variants=[{"piece": '"Blue Lake"', "bpm": '"80"', "step": "8", "beats": "320"}],
        hidden=[{"piece": '"Rain"', "bpm": '"60"', "step": "0", "beats": "120"},
                {"piece": '"Waltz"', "bpm": '"100"', "step": "10", "beats": "100"},
                {"piece": '"Old Clock"', "bpm": '"40"', "step": "20", "beats": "250"},
                {"piece": '"Spring"', "bpm": '"130"', "step": "10", "beats": "520"},
                {"piece": '"Fast Train"', "bpm": '"200"', "step": "20", "beats": "1000"}],
        intro="Ученица разучивает на пианино пьесу `piece = {piece}`. Метроном в телефоне показывает темп строкой: "
              "`bpm = {bpm}` — столько ударов в минуту было вчера. Сегодня она два раза ускорила метроном, каждый раз "
              "на `step = {step}` ударов в минуту. Во всей пьесе `beats = {beats}` ударов.",
        steps=["Заведи переменную `tempo` — темп из `bpm`, превращённый в целое число с помощью `int()`.",
               "Два раза прибавь к `tempo` ускорение `step` с помощью `+=`.",
               "Выведи одной строкой, склеив части через `+`: название пьесы, `\": \"`, вчерашний темп `bpm` (это уже "
               "строка), `\" -> \"`, новый темп (через `str()`) и `\" bpm\"` — получится, например, "
               "`Blue Lake: 80 -> 96 bpm`.",
               "В минуте 60 секунд, поэтому один удар длится `60 / tempo` секунды. Выведи `Beat:`, это число и `s` "
               "через `print` с запятыми.",
               "Посчитай, сколько целых секунд звучит вся пьеса в новом темпе: `beats * 60 // tempo`, и сохрани "
               "в переменную `seconds`.",
               "Выведи `Time:`, минуты (`seconds // 60`), `min`, оставшиеся секунды (`seconds % 60`) и `s` через "
               "`print` с запятыми."],
        hint="`bpm` так и остаётся строкой со вчерашним темпом: `+=` меняет только `tempo`. При темпе 96 метроном "
             "щёлкает 96 раз в минуту, и удар длится `60 / 96`, то есть `0.625` секунды. `200 // 60` даёт `3`, "
             "а `200 % 60` — `20`.",
        solution='tempo = int(bpm)\ntempo += step\ntempo += step\nprint(piece + ": " + bpm + " -> " + str(tempo) + " bpm")\n'
                 'beat = 60 / tempo\nprint("Beat:", beat, "s")\n'
                 'seconds = beats * 60 // tempo\nprint("Time:", seconds // 60, "min", seconds % 60, "s")',
        wrong=[("ускоряет метроном только один раз",
                'tempo = int(bpm)\ntempo += step\nprint(piece + ": " + bpm + " -> " + str(tempo) + " bpm")\n'
                'beat = 60 / tempo\nprint("Beat:", beat, "s")\n'
                'seconds = beats * 60 // tempo\nprint("Time:", seconds // 60, "min", seconds % 60, "s")'),
               ("длительность удара считает наоборот: tempo / 60",
                'tempo = int(bpm)\ntempo += step\ntempo += step\nprint(piece + ": " + bpm + " -> " + str(tempo) + " bpm")\n'
                'beat = tempo / 60\nprint("Beat:", beat, "s")\n'
                'seconds = beats * 60 // tempo\nprint("Time:", seconds // 60, "min", seconds % 60, "s")'),
               ("забывает умножить на 60 и получает минуты вместо секунд",
                'tempo = int(bpm)\ntempo += step\ntempo += step\nprint(piece + ": " + bpm + " -> " + str(tempo) + " bpm")\n'
                'beat = 60 / tempo\nprint("Beat:", beat, "s")\n'
                'seconds = beats // tempo\nprint("Time:", seconds // 60, "min", seconds % 60, "s")')],
        must_use=AUG,
    ),
]
