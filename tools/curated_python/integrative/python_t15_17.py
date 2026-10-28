"""Integrative tasks of the 3rd iteration, Python, topics 15–17: PY_LOGICAL_OR («Логическое or и not»), PY_ELIF
(«Цепочки elif»), PY_TRUTHINESS («Истинность значений»). One small story each (about 4–5 minutes): the topic at the core
plus 1–2 earlier topics — int()/float(), // and %, += -=, strings (+, *, len), `/` giving a float, f-strings; the elif
stories also use or. Theme domains: online games, delivery service, clinic appointments, library loans (the 3 stories
of a topic are in 3 different domains).
Not yet: loops, lists, string methods and slices, functions, format specifiers like :.2f, round(); the or/not stories
use no elif and no truthiness of non-bool values, the elif stories no truthiness of non-bool values."""
from build import OutputTask

OR = ("Or", "Используй or, чтобы объединить проверки в одном условии")
NOT = ("Not", "Используй not, чтобы проверить, что условие не выполнено")
ELIF = (r"re:\belif\b", "Используй цепочку if / elif / else: случаи проверяются по порядку, срабатывает первый подходящий")

TASKS = [
    # ───────── 15. Логическое or и not ─────────
    OutputTask(
        skill="PY_LOGICAL_OR", difficulty=3, slug="py-int-or-dungeon", title="Вход в подземелье",
        given=["nick", "xp", "has_key"],
        variants=[{"nick": '"Ranger"', "xp": '"12450"', "has_key": "True"}],
        hidden=[{"nick": '"Mira"', "xp": '"9080"', "has_key": "False"},
                {"nick": '"Odin"', "xp": '"15000"', "has_key": "False"},
                {"nick": '"Kai"', "xp": '"14999"', "has_key": "False"},
                {"nick": '"Zed"', "xp": '"700"', "has_key": "True"},
                {"nick": '"Bold"', "xp": '"21300"', "has_key": "True"}],
        intro="Игрок `nick = {nick}` в онлайн-игре подошёл ко входу в подземелье. Сервер передаёт его опыт строкой: "
              "`xp = {xp}`. Каждая полная тысяча очков опыта — это один уровень. Есть ли у игрока ключ от подземелья, "
              "записано в `has_key = {has_key}`.",
        steps=["Преврати `xp` в целое число. Посчитай уровень `level` — опыт, делённый нацело (`//`) на 1000, — "
               "и очки к следующему уровню `rest` — остаток от деления опыта на 1000.",
               "Выведи f-строкой `<nick>: level <level>, <rest>/1000 xp`.",
               "В подземелье пускают игрока с уровнем 15 или выше **или** игрока с ключом. Если пускают, выведи "
               "`Dungeon is open`.",
               "Иначе выведи f-строкой `Dungeon is closed, levels left: <15 - level>`. Например, игрок `Mira` "
               "с опытом `\"9080\"` и без ключа получит `Mira: level 9, 80/1000 xp` и "
               "`Dungeon is closed, levels left: 6`."],
        hint="`12450 // 1000` — это 12, а `12450 % 1000` — 450. `has_key` уже равно `True` или `False`, его можно "
             "ставить в условие как есть: `... or has_key`. Уровень ровно 15 уже подходит.",
        solution='points = int(xp)\nlevel = points // 1000\nrest = points % 1000\n'
                 'print(f"{nick}: level {level}, {rest}/1000 xp")\nif level >= 15 or has_key:\n'
                 '    print("Dungeon is open")\nelse:\n    print(f"Dungeon is closed, levels left: {15 - level}")',
        wrong=[("and вместо or: без ключа не пускает даже игрока 15 уровня",
                'points = int(xp)\nlevel = points // 1000\nrest = points % 1000\n'
                'print(f"{nick}: level {level}, {rest}/1000 xp")\nif level >= 15 and has_key:\n'
                '    print("Dungeon is open")\nelse:\n    print(f"Dungeon is closed, levels left: {15 - level}")'),
               ("строгое сравнение: игрок ровно 15 уровня не проходит",
                'points = int(xp)\nlevel = points // 1000\nrest = points % 1000\n'
                'print(f"{nick}: level {level}, {rest}/1000 xp")\nif level > 15 or has_key:\n'
                '    print("Dungeon is open")\nelse:\n    print(f"Dungeon is closed, levels left: {15 - level}")'),
               ("уровень посчитан через / — получается дробный уровень",
                'points = int(xp)\nlevel = points / 1000\nrest = points % 1000\n'
                'print(f"{nick}: level {level}, {rest}/1000 xp")\nif level >= 15 or has_key:\n'
                '    print("Dungeon is open")\nelse:\n    print(f"Dungeon is closed, levels left: {15 - level}")')],
        constructs=["if"],
        must_use=[("Or", "Используй or: в подземелье пускают по уровню или по ключу")],
    ),
    OutputTask(
        skill="PY_LOGICAL_OR", difficulty=3, slug="py-int-or-water", title="Вода с доставкой на этаж",
        given=["bottles", "has_lift"],
        variants=[{"bottles": '"4"', "has_lift": "True"}],
        hidden=[{"bottles": '"2"', "has_lift": "False"},
                {"bottles": '"3"', "has_lift": "True"},
                {"bottles": '"1"', "has_lift": "True"},
                {"bottles": '"6"', "has_lift": "False"},
                {"bottles": '"3"', "has_lift": "False"}],
        intro="Служба доставки привозит питьевую воду в больших бутылях, бутыль стоит 250 руб. Число бутылей пришло "
              "из формы заказа строкой: `bottles = {bottles}`. Есть ли в доме лифт, записано в `has_lift = {has_lift}`. "
              "Курьер поднимает воду в квартиру бесплатно, только если в доме есть лифт и бутылей не больше 3, "
              "а иначе берёт за подъём 40 руб. за каждую бутыль.",
        steps=["Преврати `bottles` в целое число `n` и посчитай стоимость воды: `total = n * 250`.",
               "Если в доме **нет** лифта (`not has_lift`) **или** бутылей больше 3, подъём платный: посчитай "
               "`carry = n * 40`, прибавь `carry` к `total` с помощью `+=` и выведи f-строкой `Carrying: <carry> rub`.",
               "Иначе выведи `Carrying: free`.",
               "В конце (в любом случае) выведи f-строкой `Total: <total> rub`. Например, для `\"2\"` бутылей в доме "
               "без лифта программа выводит `Carrying: 80 rub` и `Total: 580 rub`."],
        hint="«Лифта нет» — это `not has_lift`. Для платного подъёма хватает одной из двух причин, поэтому части "
             "условия соединяет `or`. За ровно 3 бутыли в доме с лифтом платить не нужно.",
        solution='n = int(bottles)\ntotal = n * 250\nif not has_lift or n > 3:\n    carry = n * 40\n    total += carry\n'
                 '    print(f"Carrying: {carry} rub")\nelse:\n    print("Carrying: free")\nprint(f"Total: {total} rub")',
        wrong=[("and вместо or: платит только тот, у кого нет лифта и больше 3 бутылей",
                'n = int(bottles)\ntotal = n * 250\nif not has_lift and n > 3:\n    carry = n * 40\n    total += carry\n'
                '    print(f"Carrying: {carry} rub")\nelse:\n    print("Carrying: free")\nprint(f"Total: {total} rub")'),
               ("забыт not: за подъём платят жильцы домов с лифтом",
                'n = int(bottles)\ntotal = n * 250\nif has_lift or n > 3:\n    carry = n * 40\n    total += carry\n'
                '    print(f"Carrying: {carry} rub")\nelse:\n    print("Carrying: free")\nprint(f"Total: {total} rub")'),
               ("плата за подъём выведена, но не прибавлена к сумме",
                'n = int(bottles)\ntotal = n * 250\nif not has_lift or n > 3:\n    carry = n * 40\n'
                '    print(f"Carrying: {carry} rub")\nelse:\n    print("Carrying: free")\nprint(f"Total: {total} rub")'),
               ("нестрогое сравнение: за 3 бутыли в доме с лифтом тоже берут плату",
                'n = int(bottles)\ntotal = n * 250\nif not has_lift or n >= 3:\n    carry = n * 40\n    total += carry\n'
                '    print(f"Carrying: {carry} rub")\nelse:\n    print("Carrying: free")\nprint(f"Total: {total} rub")')],
        constructs=["if"],
        must_use=[("Not", "Используй not, чтобы проверить, что лифта нет"),
                  ("Or", "Используй or: для платного подъёма хватает одной из двух причин")],
    ),
    OutputTask(
        skill="PY_LOGICAL_OR", difficulty=3, slug="py-int-or-blood-test", title="Анализ крови натощак",
        given=["name", "arrived", "fasting"],
        variants=[{"name": '"Anya"', "arrived": "545", "fasting": "True"}],
        hidden=[{"name": '"Boris"', "arrived": "659", "fasting": "True"},
                {"name": '"Vera"', "arrived": "660", "fasting": "True"},
                {"name": '"Gleb"', "arrived": "480", "fasting": "False"},
                {"name": '"Dina"', "arrived": "700", "fasting": "False"},
                {"name": '"Ilya"', "arrived": "600", "fasting": "True"}],
        intro="Пациент `name = {name}` записан в поликлинику на анализ крови. Время, когда он пришёл, записано "
              "в минутах от полуночи: `arrived = {arrived}` (например, 545 — это 9:05). Пришёл ли он натощак, "
              "записано в `fasting = {fasting}`. Кровь берут только натощак и только до 11:00, то есть до 660 минут.",
        steps=["Выведи f-строкой `<name> arrived at <hours> h <minutes> min`, где `hours` — `arrived`, делённое нацело "
               "на 60, а `minutes` — остаток от деления `arrived` на 60.",
               "Если пациент пришёл **не** натощак (`not fasting`) **или** пришёл в 660 минут или позже, выведи "
               "`Blood test: come tomorrow`.",
               "Иначе кровь берут сейчас, а результат будет готов через 3 часа: посчитай `ready = arrived + 180` "
               "и выведи f-строкой `Results at <hours> h <minutes> min` — часы и минуты из `ready` считаются так же, "
               "как в шаге 1. Например, для прихода натощак в 600 минут — `Results at 13 h 0 min`."],
        hint="`545 // 60` — это 9 часов, `545 % 60` — 5 минут. «Не натощак» — это `not fasting`. "
             "Пришедший ровно в 660 минут (11:00) уже опоздал.",
        solution='print(f"{name} arrived at {arrived // 60} h {arrived % 60} min")\n'
                 'if not fasting or arrived >= 660:\n    print("Blood test: come tomorrow")\nelse:\n'
                 '    ready = arrived + 180\n    print(f"Results at {ready // 60} h {ready % 60} min")',
        wrong=[("and вместо or: домой отправляет, только если пациент и поел, и опоздал",
                'print(f"{name} arrived at {arrived // 60} h {arrived % 60} min")\n'
                'if not fasting and arrived >= 660:\n    print("Blood test: come tomorrow")\nelse:\n'
                '    ready = arrived + 180\n    print(f"Results at {ready // 60} h {ready % 60} min")'),
               ("забыт not: домой отправляет тех, кто пришёл натощак",
                'print(f"{name} arrived at {arrived // 60} h {arrived % 60} min")\n'
                'if fasting or arrived >= 660:\n    print("Blood test: come tomorrow")\nelse:\n'
                '    ready = arrived + 180\n    print(f"Results at {ready // 60} h {ready % 60} min")'),
               ("строгое сравнение: пришедший ровно в 11:00 ещё сдаёт анализ",
                'print(f"{name} arrived at {arrived // 60} h {arrived % 60} min")\n'
                'if not fasting or arrived > 660:\n    print("Blood test: come tomorrow")\nelse:\n'
                '    ready = arrived + 180\n    print(f"Results at {ready // 60} h {ready % 60} min")')],
        constructs=["if"],
        must_use=[("Not", "Используй not, чтобы проверить, что пациент пришёл не натощак"),
                  ("Or", "Используй or: чтобы перенести анализ, хватает одной из двух причин")],
    ),

    # ───────── 16. Цепочки elif ─────────
    OutputTask(
        skill="PY_ELIF", difficulty=3, slug="py-int-elif-book-queue", title="Очередь на книгу",
        given=["title", "place", "days"],
        variants=[{"title": '"Dune"', "place": "3", "days": "20"}],
        hidden=[{"title": '"Emma"', "place": "1", "days": "14"},
                {"title": '"Holes"', "place": "3", "days": "15"},
                {"title": '"Matilda"', "place": "2", "days": "31"},
                {"title": '"Beowulf"', "place": "2", "days": "10"},
                {"title": '"Ulysses"', "place": "4", "days": "21"}],
        intro="На популярную книгу `title = {title}` в библиотеке записываются в очередь. Читатель стоит в ней "
              "на месте `place = {place}` (место 1 значит, что книга уже вернулась и ждёт его). Каждый читатель "
              "перед ним держит книгу `days = {days}` дней.",
        steps=["Посчитай, сколько дней ждать: перед читателем стоят `place - 1` человек, и каждый держит книгу "
               "`days` дней. Сохрани результат в `wait`.",
               "Если `wait` равно 0, выведи f-строкой `<title>: ready to pick up`.",
               "Иначе, если `wait` не больше 30, выведи f-строкой `<title>: wait <wait> days`.",
               "Иначе выведи f-строкой `<title>: wait <weeks> weeks <rest> days`, где `weeks` — `wait`, делённое "
               "нацело на 7, а `rest` — остаток от деления `wait` на 7. Например, для книги `\"Emma\"` и 45 дней "
               "ожидания — `Emma: wait 6 weeks 3 days`."],
        hint="Цепочка проверяет условия по порядку, поэтому случай «0 дней» должен стоять первым: 0 тоже не больше 30. "
             "Ровно 30 дней ещё пишут в днях. `45 // 7` — это 6, `45 % 7` — 3.",
        solution='wait = (place - 1) * days\nif wait == 0:\n    print(f"{title}: ready to pick up")\n'
                 'elif wait <= 30:\n    print(f"{title}: wait {wait} days")\nelse:\n'
                 '    print(f"{title}: wait {wait // 7} weeks {wait % 7} days")',
        wrong=[("забыто «- 1»: первый в очереди тоже ждёт",
                'wait = place * days\nif wait == 0:\n    print(f"{title}: ready to pick up")\n'
                'elif wait <= 30:\n    print(f"{title}: wait {wait} days")\nelse:\n'
                '    print(f"{title}: wait {wait // 7} weeks {wait % 7} days")'),
               ("условия в другом порядке: при 0 дней печатает wait 0 days",
                'wait = (place - 1) * days\nif wait <= 30:\n    print(f"{title}: wait {wait} days")\n'
                'elif wait == 0:\n    print(f"{title}: ready to pick up")\nelse:\n'
                '    print(f"{title}: wait {wait // 7} weeks {wait % 7} days")'),
               ("отдельные if вместо цепочки: при 0 дней печатает две строки",
                'wait = (place - 1) * days\nif wait == 0:\n    print(f"{title}: ready to pick up")\n'
                'if wait <= 30:\n    print(f"{title}: wait {wait} days")\nelse:\n'
                '    print(f"{title}: wait {wait // 7} weeks {wait % 7} days")'),
               ("строгое сравнение: ровно 30 дней уже пишет в неделях",
                'wait = (place - 1) * days\nif wait == 0:\n    print(f"{title}: ready to pick up")\n'
                'elif wait < 30:\n    print(f"{title}: wait {wait} days")\nelse:\n'
                '    print(f"{title}: wait {wait // 7} weeks {wait % 7} days")')],
        constructs=["if"],
        must_use=[ELIF],
    ),
    OutputTask(
        skill="PY_ELIF", difficulty=3, slug="py-int-elif-league", title="Лига после матча",
        given=["rating", "delta"],
        variants=[{"rating": '"1480"', "delta": "-25"}],
        hidden=[{"rating": '"1020"', "delta": "-40"},
                {"rating": '"1470"', "delta": "30"},
                {"rating": '"990"', "delta": "10"},
                {"rating": '"1600"', "delta": "-15"},
                {"rating": '"500"', "delta": "25"}],
        intro="В онлайн-игре после каждого матча меняется рейтинг игрока. Сервер передаёт рейтинг до матча строкой: "
              "`rating = {rating}`. За матч игрок получил `delta = {delta}` очков (за поражение это число "
              "отрицательное). По новому рейтингу игрок попадает в лигу: 1500 и больше — `Gold`, 1000 и больше — "
              "`Silver`, меньше 1000 — `Bronze`.",
        steps=["Преврати `rating` в целое число `points` и прибавь к нему `delta` с помощью `+=`. "
               "Выведи f-строкой `Rating: <points>`.",
               "Если `points` не меньше 1500, выведи `League: Gold`.",
               "Иначе, если `points` не меньше 1000, выведи f-строкой `League: Silver, to Gold: <1500 - points>`.",
               "Иначе выведи f-строкой `League: Bronze, to Silver: <1000 - points>`. Например, для рейтинга "
               "`\"1020\"` и `delta = -40` программа выводит `Rating: 980` и `League: Bronze, to Silver: 20`."],
        hint="Лигу выбирают по рейтингу уже после матча, поэтому `+=` стоит до цепочки. Пороги проверяй сверху вниз: "
             "сначала 1500, потом 1000. Ровно 1500 — это уже `Gold`.",
        solution='points = int(rating)\npoints += delta\nprint(f"Rating: {points}")\nif points >= 1500:\n'
                 '    print("League: Gold")\nelif points >= 1000:\n    print(f"League: Silver, to Gold: {1500 - points}")\n'
                 'else:\n    print(f"League: Bronze, to Silver: {1000 - points}")',
        wrong=[("забыт += delta: лига по рейтингу до матча",
                'points = int(rating)\nprint(f"Rating: {points}")\nif points >= 1500:\n'
                '    print("League: Gold")\nelif points >= 1000:\n    print(f"League: Silver, to Gold: {1500 - points}")\n'
                'else:\n    print(f"League: Bronze, to Silver: {1000 - points}")'),
               ("пороги снизу вверх: всё от 1000 становится Silver",
                'points = int(rating)\npoints += delta\nprint(f"Rating: {points}")\nif points >= 1000:\n'
                '    print(f"League: Silver, to Gold: {1500 - points}")\nelif points >= 1500:\n    print("League: Gold")\n'
                'else:\n    print(f"League: Bronze, to Silver: {1000 - points}")'),
               ("отдельные if вместо цепочки: игрок Gold печатает ещё и Silver",
                'points = int(rating)\npoints += delta\nprint(f"Rating: {points}")\nif points >= 1500:\n'
                '    print("League: Gold")\nif points >= 1000:\n    print(f"League: Silver, to Gold: {1500 - points}")\n'
                'else:\n    print(f"League: Bronze, to Silver: {1000 - points}")'),
               ("строгие сравнения: ровно 1500 — ещё Silver",
                'points = int(rating)\npoints += delta\nprint(f"Rating: {points}")\nif points > 1500:\n'
                '    print("League: Gold")\nelif points > 1000:\n    print(f"League: Silver, to Gold: {1500 - points}")\n'
                'else:\n    print(f"League: Bronze, to Silver: {1000 - points}")')],
        constructs=["if"],
        must_use=[ELIF],
    ),
    OutputTask(
        skill="PY_ELIF", difficulty=3, slug="py-int-elif-fever-bot", title="Чат-бот записи к врачу",
        given=["temp", "age"],
        variants=[{"temp": '"37.4"', "age": "30"}],
        hidden=[{"temp": '"36.6"', "age": "70"},
                {"temp": '"38.5"', "age": "20"},
                {"temp": '"37.2"', "age": "30"},
                {"temp": '"37.1"', "age": "64"},
                {"temp": '"39.0"', "age": "80"},
                {"temp": '"36.6"', "age": "65"}],
        intro="Чат-бот поликлиники помогает записаться к терапевту. Пациент написал в чат свою температуру, поэтому "
              "она пришла строкой: `temp = {temp}`. Возраст пациента — `age = {age}`.",
        steps=["Преврати `temp` в дробное число с помощью `float()`, сохрани в `t` и выведи f-строкой "
               "`Temperature: <t>`.",
               "Если `t` не меньше 38.5, выведи `A doctor will come to your home`.",
               "Иначе, если `t` не меньше 37.2 **или** пациенту 65 лет или больше, выведи `Visit today, room 14`.",
               "Во всех остальных случаях выведи `Book any free day`. Например, для `\"36.6\"` и 70 лет программа "
               "выводит `Temperature: 36.6` и `Visit today, room 14`."],
        hint="Сравнивать можно только число с числом, поэтому сначала `float(temp)`. Условия проверяются по порядку: "
             "пациенту 80 лет с температурой 39.0 врач придёт домой — сработает первая ветка, а не вторая.",
        solution='t = float(temp)\nprint(f"Temperature: {t}")\nif t >= 38.5:\n    print("A doctor will come to your home")\n'
                 'elif t >= 37.2 or age >= 65:\n    print("Visit today, room 14")\nelse:\n    print("Book any free day")',
        wrong=[("условия в другом порядке: при высокой температуре зовёт в поликлинику",
                't = float(temp)\nprint(f"Temperature: {t}")\nif t >= 37.2 or age >= 65:\n    print("Visit today, room 14")\n'
                'elif t >= 38.5:\n    print("A doctor will come to your home")\nelse:\n    print("Book any free day")'),
               ("and вместо or: пациента до 65 лет с температурой не зовут сегодня",
                't = float(temp)\nprint(f"Temperature: {t}")\nif t >= 38.5:\n    print("A doctor will come to your home")\n'
                'elif t >= 37.2 and age >= 65:\n    print("Visit today, room 14")\nelse:\n    print("Book any free day")'),
               ("строгое сравнение: при 38.5 врач домой не придёт",
                't = float(temp)\nprint(f"Temperature: {t}")\nif t > 38.5:\n    print("A doctor will come to your home")\n'
                'elif t >= 37.2 or age >= 65:\n    print("Visit today, room 14")\nelse:\n    print("Book any free day")')],
        constructs=["if"],
        must_use=[ELIF],
    ),

    # ───────── 17. Истинность значений ─────────
    OutputTask(
        skill="PY_TRUTHINESS", difficulty=3, slug="py-int-truth-courier", title="Карточка заказа для курьера",
        given=["code", "tip"],
        variants=[{"code": '"4512"', "tip": '"100"'}],
        hidden=[{"code": '""', "tip": '""'},
                {"code": '"1234"', "tip": '""'},
                {"code": '""', "tip": '"50"'},
                {"code": '"0007"', "tip": '"0"'},
                {"code": '"88"', "tip": '"300"'}],
        intro="Курьер службы доставки открывает карточку заказа. Код домофона — `code = {code}` (если клиент его "
              "не указал, там пустая строка `\"\"`). Чаевые клиент вписал в поле формы, поэтому они записаны строкой: "
              "`tip = {tip}`; если поле не заполнено, там тоже пустая строка. За доставку курьер получает 150 руб. "
              "плюс чаевые.",
        steps=["Если код домофона указан (проверь просто `if code:`), выведи f-строкой `Intercom: <code>`, "
               "иначе выведи `Intercom: call the client`.",
               "Заведи `pay = 150`. Если поле чаевых заполнено (`if tip:`), преврати `tip` в целое число "
               "и прибавь его к `pay` с помощью `+=`.",
               "Выведи f-строкой `Courier gets <pay> rub`. Например, без кода и без чаевых программа выводит "
               "`Intercom: call the client` и `Courier gets 150 rub`."],
        hint="Пустая строка в условии ложна, а любая непустая — истинна, даже `\"0\"`. `int(\"\")` завершится "
             "ошибкой, поэтому превращай `tip` в число только внутри `if tip:`.",
        solution='if code:\n    print(f"Intercom: {code}")\nelse:\n    print("Intercom: call the client")\n'
                 'pay = 150\nif tip:\n    pay += int(tip)\nprint(f"Courier gets {pay} rub")',
        wrong=[("лишний not: ветки домофона срабатывают наоборот",
                'if not code:\n    print(f"Intercom: {code}")\nelse:\n    print("Intercom: call the client")\n'
                'pay = 150\nif tip:\n    pay += int(tip)\nprint(f"Courier gets {pay} rub")'),
               ("чаевые затирают оплату: = вместо +=",
                'if code:\n    print(f"Intercom: {code}")\nelse:\n    print("Intercom: call the client")\n'
                'pay = 150\nif tip:\n    pay = int(tip)\nprint(f"Courier gets {pay} rub")')],
        constructs=["if"],
        must_use=[(r"re:if\s+(not\s+)?tip\s*:", "Проверь поле чаевых через истинность строки: `if tip:` — "
                                                "пустая строка ложна, и тогда `int()` не нужен")],
    ),
    OutputTask(
        skill="PY_TRUTHINESS", difficulty=3, slug="py-int-truth-catalog", title="Книга в каталоге библиотеки",
        given=["title", "author", "copies"],
        variants=[{"title": '"Dune"', "author": '"Frank Herbert"', "copies": "2"}],
        hidden=[{"title": '"Beowulf"', "author": '""', "copies": "0"},
                {"title": '"Emma"', "author": '"Jane Austen"', "copies": "0"},
                {"title": '"Sagas"', "author": '""', "copies": "3"},
                {"title": '"Holes"', "author": '"Louis Sachar"', "copies": "1"}],
        intro="Электронный каталог библиотеки показывает карточку книги `title = {title}`. Автор — `author = {author}` "
              "(у старых книг автор бывает неизвестен, тогда там пустая строка `\"\"`). Сколько экземпляров сейчас "
              "можно взять домой, записано в `copies = {copies}`.",
        steps=["Сохрани в `who` автора, а если строка `author` пустая — строку `\"unknown author\"`. "
               "Запиши это одной строкой через `or`: `who = author or \"unknown author\"`.",
               "Склей через `+` строку `line` из названия, строки ` by ` и `who` и выведи её. Под ней выведи строку "
               "из знаков `=` такой же длины, как `line` (длину даёт `len()`).",
               "Если свободные экземпляры есть (проверь просто `if copies:`), выведи f-строкой `Available: <copies>`, "
               "иначе выведи `All copies are on loan`. Например, для книги `\"Beowulf\"` без автора и 0 экземпляров программа выводит "
               "`Beowulf by unknown author`, под ней 25 знаков `=` и `All copies are on loan`."],
        hint="`a or b` даёт `a`, если `a` истинно, а иначе — `b`; пустая строка и число 0 ложны. Порядок важен: "
             "сначала то, что хотим показать. `\"=\" * 4` даёт `====`.",
        solution='who = author or "unknown author"\nline = title + " by " + who\nprint(line)\nprint("=" * len(line))\n'
                 'if copies:\n    print(f"Available: {copies}")\nelse:\n    print("All copies are on loan")',
        wrong=[("части or переставлены: всегда unknown author",
                'who = "unknown author" or author\nline = title + " by " + who\nprint(line)\nprint("=" * len(line))\n'
                'if copies:\n    print(f"Available: {copies}")\nelse:\n    print("All copies are on loan")'),
               ("черта длиной в название, а не во всю строку",
                'who = author or "unknown author"\nline = title + " by " + who\nprint(line)\nprint("=" * len(title))\n'
                'if copies:\n    print(f"Available: {copies}")\nelse:\n    print("All copies are on loan")'),
               ("лишний not: свободные экземпляры считаются выданными",
                'who = author or "unknown author"\nline = title + " by " + who\nprint(line)\nprint("=" * len(line))\n'
                'if not copies:\n    print(f"Available: {copies}")\nelse:\n    print("All copies are on loan")')],
        constructs=["if"],
        must_use=[("BoolOp", "Используй or, чтобы подставить автора по умолчанию: `author or \"unknown author\"`")],
    ),
    OutputTask(
        skill="PY_TRUTHINESS", difficulty=3, slug="py-int-truth-duels", title="Таблица дуэлей",
        given=["nick", "clan", "wins", "losses"],
        variants=[{"nick": '"Ranger"', "clan": '"Wolves"', "wins": "9", "losses": "4"}],
        hidden=[{"nick": '"Fox"', "clan": '""', "wins": "5", "losses": "0"},
                {"nick": '"Kai"', "clan": '"Owls"', "wins": "6", "losses": "4"},
                {"nick": '"Zed"', "clan": '""', "wins": "3", "losses": "6"},
                {"nick": '"Mira"', "clan": '"Bears"', "wins": "0", "losses": "0"},
                {"nick": '"Odin"', "clan": '"Elk"', "wins": "8", "losses": "8"}],
        intro="Онлайн-игра показывает таблицу дуэлей за день. Ник игрока — `nick = {nick}`, его клан — "
              "`clan = {clan}` (если игрок не в клане, там пустая строка `\"\"`). За день он выиграл `wins = {wins}` "
              "дуэлей и проиграл `losses = {losses}`.",
        steps=["Сохрани в `name` ник. Если клан указан (проверь просто `if clan:`), имя в таблице другое: склей через "
               "`+` строку `\"[\"`, клан, строку `\"] \"` (скобка и пробел) и ник — получится `[<clan>] <nick>`.",
               "Посчитай отношение побед к поражениям: `ratio = wins / losses`. Но делить на 0 нельзя: если "
               "поражений не было (проверь через истинность: `if losses:`), `ratio` равно просто `wins`.",
               "Выведи f-строкой `<name>: ratio <ratio>`. Например, игрок `Fox` без клана с 5 победами и без "
               "поражений получит `Fox: ratio 5`, а игрок `Kai` из клана `\"Owls\"` с 6 победами и 4 поражениями — "
               "`[Owls] Kai: ratio 1.5`."],
        hint="Число 0 в условии ложно, любое другое — истинно, поэтому `if losses:` значит «если поражения были». "
             "Деление `/` даёт дробное число: `8 / 8` — это `1.0`.",
        solution='name = nick\nif clan:\n    name = "[" + clan + "] " + nick\nif losses:\n    ratio = wins / losses\n'
                 'else:\n    ratio = wins\nprint(f"{name}: ratio {ratio}")',
        wrong=[("деление нацело //: дробная часть теряется",
                'name = nick\nif clan:\n    name = "[" + clan + "] " + nick\nif losses:\n    ratio = wins // losses\n'
                'else:\n    ratio = wins\nprint(f"{name}: ratio {ratio}")'),
               ("лишний not: скобки с кланом достаются игроку без клана",
                'name = nick\nif not clan:\n    name = "[" + clan + "] " + nick\nif losses:\n    ratio = wins / losses\n'
                'else:\n    ratio = wins\nprint(f"{name}: ratio {ratio}")'),
               ("без поражений отношение считается нулём",
                'name = nick\nif clan:\n    name = "[" + clan + "] " + nick\nif losses:\n    ratio = wins / losses\n'
                'else:\n    ratio = 0\nprint(f"{name}: ratio {ratio}")')],
        constructs=["if"],
        must_use=[(r"re:if\s+(not\s+)?losses\s*:", "Проверь поражения через истинность числа: `if losses:` — "
                                                   "0 ложен, и тогда делить нельзя")],
    ),
]
