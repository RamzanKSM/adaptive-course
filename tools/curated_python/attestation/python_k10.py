"""Attestation, Python, tier up to topic 10 PY_ASSIGNMENT_OPERATORS — «Составное присваивание += -=».
Each task touches every topic 1–10: print (several values, commas), variables, assignment (a new value, a copy),
arithmetic + - * / and parentheses, order of execution, int and float (`/` gives a float), strings (gluing with `+`,
repeating with `*`, `len()`), type conversion int()/float()/str(), // and %, += -= (and %=).
Theme: games, hobbies and weather; every story is different.
Not yet: f-strings, conditions and comparisons, loops, lists, functions, round(), string methods and slices."""
from build import OutputTask

SKILL = "PY_ASSIGNMENT_OPERATORS"
AUG = [("AugAssign", "Используй составное присваивание (+=, -=), чтобы изменить переменную")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att10-board-game", title="Настольная игра",
        given=["player", "points", "bonus", "rounds"],
        variants=[{"player": '"Anya"', "points": '"38"', "bonus": "6", "rounds": "4"}],
        hidden=[{"player": '"Lena"', "points": '"29"', "bonus": "3", "rounds": "2"},
                {"player": '"Ivan"', "points": '"7"', "bonus": "4", "rounds": "8"},
                {"player": '"Mira"', "points": '"99"', "bonus": "0", "rounds": "4"},
                {"player": '"Boris"', "points": '"3"', "bonus": "1", "rounds": "5"}],
        intro="Игрок `player = {player}` играет в настольную игру. Табло хранит его очки строкой: `points = {points}`. "
              "В конце партии он вытянул две бонусные карты, каждая даёт `bonus = {bonus}` очков, а потом попал "
              "в ловушку и потерял 5 очков. Всего в партии было `rounds = {rounds}` раундов.",
        steps=["Заведи переменную `score` и положи в неё очки с табло, превратив строку в число с помощью `int()`.",
               "Две бонусные карты: два раза прибавь `bonus` к `score` с помощью `+=`.",
               "Ловушка: вычти из `score` 5 очков с помощью `-=`.",
               "Выведи одной строкой, склеив части через `+`: имя игрока, `\": \"`, очки (через `str()`) и "
               "`\" points\"` — получится, например, `Anya: 45 points`.",
               "Посчитай среднее число очков за раунд: `score`, делённое на `rounds` (обычным делением `/`). "
               "Выведи `Per round:` и это число через `print` с запятой.",
               "За каждые полные 10 очков игрок получает фишку. Посчитай число фишек (`//`) и сколько очков "
               "осталось сверх них (`%`), выведи `Chips:`, фишки, `left:` и остаток через `print` с запятыми."],
        hint="`int(\"38\")` превращает строку в число `38` — со строкой `+=` с числом не сработает. "
             "Деление `/` всегда даёт дробное число (`30 / 2` — это `15.0`). `45 // 10` даёт `4`, а `45 % 10` даёт `5`.",
        solution='score = int(points)\nscore += bonus\nscore += bonus\nscore -= 5\n'
                 'print(player + ": " + str(score) + " points")\n'
                 'average = score / rounds\nprint("Per round:", average)\n'
                 'chips = score // 10\nleft = score % 10\nprint("Chips:", chips, "left:", left)',
        wrong=[("вторую бонусную карту кладёт через = вместо += — очки с табло теряются",
                'score = int(points)\nscore += bonus\nscore = bonus\nscore -= 5\n'
                'print(player + ": " + str(score) + " points")\n'
                'average = score / rounds\nprint("Per round:", average)\n'
                'chips = score // 10\nleft = score % 10\nprint("Chips:", chips, "left:", left)'),
               ("путает // и %: фишки и остаток меняются местами",
                'score = int(points)\nscore += bonus\nscore += bonus\nscore -= 5\n'
                'print(player + ": " + str(score) + " points")\n'
                'average = score / rounds\nprint("Per round:", average)\n'
                'chips = score % 10\nleft = score // 10\nprint("Chips:", chips, "left:", left)'),
               ("среднее считает делением нацело // — теряется дробная часть",
                'score = int(points)\nscore += bonus\nscore += bonus\nscore -= 5\n'
                'print(player + ": " + str(score) + " points")\n'
                'average = score // rounds\nprint("Per round:", average)\n'
                'chips = score // 10\nleft = score % 10\nprint("Chips:", chips, "left:", left)')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att10-weather-report", title="Сводка погоды",
        given=["city", "temp", "rain"],
        variants=[{"city": '"Sochi"', "temp": '"12.5"', "rain": '"135"'}],
        hidden=[{"city": '"Kazan"', "temp": '"-4.0"', "rain": '"60"'},
                {"city": '"Murmansk"', "temp": '"0.5"', "rain": '"45"'},
                {"city": '"Omsk"', "temp": '"20"', "rain": '"0"'},
                {"city": '"Ufa"', "temp": '"7.5"', "rain": '"200"'}],
        intro="Метеостанция города `city = {city}` присылает данные строками: утреннюю температуру `temp = {temp}` "
              "в градусах и длительность дождя `rain = {rain}` в минутах. К обеду потеплело на 3 градуса, "
              "а к вечеру похолодало на 5.5 градуса. Составь сводку погоды за день.",
        steps=["Склей заголовок `title` из `\"Weather in \"` и `city` и выведи его. Следующей строкой выведи черту "
               "из знаков `-` той же длины, что заголовок: `\"-\" * len(title)`.",
               "Заведи `morning` — утреннюю температуру, превращённую в дробное число с помощью `float()`. "
               "Скопируй её в переменную `t`.",
               "Обед: прибавь к `t` 3 с помощью `+=` и выведи `Day:` и `t` через `print` с запятой.",
               "Вечер: вычти из `t` 5.5 с помощью `-=` и выведи `Evening:` и `t`.",
               "Посчитай среднюю температуру — среднее утренней и вечерней: их сумма, делённая на 2 "
               "(не забудь скобки). Выведи `Average:` и её.",
               "Преврати `rain` в целое число и раздели на часы (`// 60`) и оставшиеся минуты (`% 60`). "
               "Выведи склейкой через `+` строку вида `Rain: 2 h 15 min` (числа — через `str()`)."],
        hint="`morning` остаётся утренней температурой, даже когда `t` меняется: `t = morning` только копирует "
             "значение. `(a + b) / 2` — сначала сумма, потом деление; без скобок разделится только `b`.",
        solution='title = "Weather in " + city\nprint(title)\nprint("-" * len(title))\n'
                 'morning = float(temp)\nt = morning\nt += 3\nprint("Day:", t)\nt -= 5.5\nprint("Evening:", t)\n'
                 'average = (morning + t) / 2\nprint("Average:", average)\n'
                 'hours = int(rain) // 60\nrest = int(rain) % 60\nprint("Rain: " + str(hours) + " h " + str(rest) + " min")',
        wrong=[("забывает скобки: делит на 2 только вечернюю температуру",
                'title = "Weather in " + city\nprint(title)\nprint("-" * len(title))\n'
                'morning = float(temp)\nt = morning\nt += 3\nprint("Day:", t)\nt -= 5.5\nprint("Evening:", t)\n'
                'average = morning + t / 2\nprint("Average:", average)\n'
                'hours = int(rain) // 60\nrest = int(rain) % 60\nprint("Rain: " + str(hours) + " h " + str(rest) + " min")'),
               ("черту делает длиной в название города, а не в весь заголовок",
                'title = "Weather in " + city\nprint(title)\nprint("-" * len(city))\n'
                'morning = float(temp)\nt = morning\nt += 3\nprint("Day:", t)\nt -= 5.5\nprint("Evening:", t)\n'
                'average = (morning + t) / 2\nprint("Average:", average)\n'
                'hours = int(rain) // 60\nrest = int(rain) % 60\nprint("Rain: " + str(hours) + " h " + str(rest) + " min")'),
               ("минуты считает через // вместо остатка %",
                'title = "Weather in " + city\nprint(title)\nprint("-" * len(title))\n'
                'morning = float(temp)\nt = morning\nt += 3\nprint("Day:", t)\nt -= 5.5\nprint("Evening:", t)\n'
                'average = (morning + t) / 2\nprint("Average:", average)\n'
                'hours = int(rain) // 60\nrest = int(rain) // 60\nprint("Rain: " + str(hours) + " h " + str(rest) + " min")')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att10-photo-album", title="Фотоальбом",
        given=["photographer", "photos", "deleted", "per_page"],
        variants=[{"photographer": '"Boris"', "photos": '"250"', "deleted": "37", "per_page": "24"}],
        hidden=[{"photographer": '"Anya"', "photos": '"100"', "deleted": "4", "per_page": "12"},
                {"photographer": '"Lena"', "photos": '"50"', "deleted": "12", "per_page": "8"},
                {"photographer": '"Ivan"', "photos": '"30"', "deleted": "25", "per_page": "20"},
                {"photographer": '"Timur"', "photos": '"500"', "deleted": "0", "per_page": "30"}],
        intro="Фотограф `photographer = {photographer}` вернулся из похода. Камера показывает число снимков строкой: "
              "`photos = {photos}`. Неудачные `deleted = {deleted}` снимков он удаляет, а потом добавляет ещё 10 "
              "снимков заката с телефона. Каждый снимок весит 2.5 MB. Из снимков он печатает альбом, на страницу "
              "помещается `per_page = {per_page}` фото.",
        steps=["Заведи переменную `total` — число снимков из `photos`, превращённое в целое число с помощью `int()`.",
               "Вычти удалённые снимки с помощью `-=`, затем прибавь 10 снимков заката с помощью `+=`.",
               "Выведи `Photos:` и `total` через `print` с запятой.",
               "Посчитай объём всех снимков: `total`, умноженное на 2.5. Выведи `Size:`, объём и `MB` через `print` с запятыми.",
               "Посчитай число полных страниц альбома (`//`) и сколько снимков останется без страницы (`%`).",
               "Выведи одной строкой, склеив части через `+`: `\"Album of \"`, имя фотографа, `\": \"`, страницы, "
               "`\" pages + \"`, оставшиеся снимки и `\" photos\"` — например, `Album of Boris: 9 pages + 7 photos`."],
        hint="Порядок важен: объём и страницы считай уже после удаления и добавления снимков. "
             "Числа перед склейкой со строкой превращай через `str()`: `\"x\" + str(9)` даёт `\"x9\"`.",
        solution='total = int(photos)\ntotal -= deleted\ntotal += 10\nprint("Photos:", total)\n'
                 'size = total * 2.5\nprint("Size:", size, "MB")\n'
                 'pages = total // per_page\nloose = total % per_page\n'
                 'print("Album of " + photographer + ": " + str(pages) + " pages + " + str(loose) + " photos")',
        wrong=[("прибавляет удалённые снимки вместо того, чтобы вычесть",
                'total = int(photos)\ntotal += deleted\ntotal += 10\nprint("Photos:", total)\n'
                'size = total * 2.5\nprint("Size:", size, "MB")\n'
                'pages = total // per_page\nloose = total % per_page\n'
                'print("Album of " + photographer + ": " + str(pages) + " pages + " + str(loose) + " photos")'),
               ("страницы считает обычным делением / — получается дробное число",
                'total = int(photos)\ntotal -= deleted\ntotal += 10\nprint("Photos:", total)\n'
                'size = total * 2.5\nprint("Size:", size, "MB")\n'
                'pages = total / per_page\nloose = total % per_page\n'
                'print("Album of " + photographer + ": " + str(pages) + " pages + " + str(loose) + " photos")'),
               ("объём считает до того, как добавил снимки заката",
                'total = int(photos)\ntotal -= deleted\nsize = total * 2.5\ntotal += 10\nprint("Photos:", total)\n'
                'print("Size:", size, "MB")\n'
                'pages = total // per_page\nloose = total % per_page\n'
                'print("Album of " + photographer + ": " + str(pages) + " pages + " + str(loose) + " photos")')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att10-hero-shop", title="Лавка героя",
        given=["hero", "gold", "price", "potions"],
        variants=[{"hero": '"Knight"', "gold": '"1250"', "price": "85", "potions": "3"}],
        hidden=[{"hero": '"Mage"', "gold": '"400"', "price": "100", "potions": "4"},
                {"hero": '"Archer"', "gold": '"1000"', "price": "45", "potions": "2"},
                {"hero": '"Elf"', "gold": '"55"', "price": "10", "potions": "1"},
                {"hero": '"Dwarf"', "gold": '"2000"', "price": "250", "potions": "0"}],
        intro="В компьютерной игре герой `hero = {hero}` заходит в лавку. Игра хранит его золото строкой: "
              "`gold = {gold}`. Он покупает `potions = {potions}` зелий по `price = {price}` золотых, потом выполняет "
              "квест и получает 300 золотых. В обменнике за каждые полные 100 золотых дают 1 кристалл, остаток "
              "остаётся золотом. Каждое зелье восстанавливает 12.5 очков здоровья.",
        steps=["Заведи переменную `coins` — золото из `gold`, превращённое в целое число с помощью `int()`.",
               "Покупка: вычти из `coins` стоимость всех зелий (`price * potions`) с помощью `-=`. Выведи склейкой "
               "через `+` строку вида `Knight: 995 gold after shop` (имя героя, `\": \"`, золото через `str()` и "
               "`\" gold after shop\"`).",
               "Квест: прибавь к `coins` 300 с помощью `+=`.",
               "Обмен: сохрани в `gems` число кристаллов (`coins // 100`), а потом оставь в `coins` только "
               "остаток с помощью `coins %= 100`.",
               "Выведи `Gems:`, кристаллы, `gold:` и оставшееся золото через `print` с запятыми.",
               "Посчитай лечение: `potions`, умноженное на 12.5, и выведи `Healing:`, лечение и `HP`."],
        hint="Порядок важен: кристаллы считай до `coins %= 100`, иначе в `coins` будет уже только остаток. "
             "`x %= 100` — то же, что `x = x % 100`. Умножение на 12.5 даёт дробное число, даже `0 * 12.5` — это `0.0`.",
        solution='coins = int(gold)\ncoins -= price * potions\nprint(hero + ": " + str(coins) + " gold after shop")\n'
                 'coins += 300\ngems = coins // 100\ncoins %= 100\nprint("Gems:", gems, "gold:", coins)\n'
                 'heal = potions * 12.5\nprint("Healing:", heal, "HP")',
        wrong=[("оставляет остаток раньше, чем считает кристаллы",
                'coins = int(gold)\ncoins -= price * potions\nprint(hero + ": " + str(coins) + " gold after shop")\n'
                'coins += 300\ncoins %= 100\ngems = coins // 100\nprint("Gems:", gems, "gold:", coins)\n'
                'heal = potions * 12.5\nprint("Healing:", heal, "HP")'),
               ("вычитает цену одного зелья, а не всех",
                'coins = int(gold)\ncoins -= price\nprint(hero + ": " + str(coins) + " gold after shop")\n'
                'coins += 300\ngems = coins // 100\ncoins %= 100\nprint("Gems:", gems, "gold:", coins)\n'
                'heal = potions * 12.5\nprint("Healing:", heal, "HP")'),
               ("забывает награду за квест",
                'coins = int(gold)\ncoins -= price * potions\nprint(hero + ": " + str(coins) + " gold after shop")\n'
                'gems = coins // 100\ncoins %= 100\nprint("Gems:", gems, "gold:", coins)\n'
                'heal = potions * 12.5\nprint("Healing:", heal, "HP")')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att10-rain-gauge", title="Осадкомер",
        given=["station", "mon", "tue", "wed", "thu"],
        variants=[{"station": '"Omsk"', "mon": '"3"', "tue": '"12"', "wed": '"0"', "thu": '"9"'}],
        hidden=[{"station": '"Kazan"', "mon": '"0"', "tue": '"0"', "wed": '"0"', "thu": '"0"'},
                {"station": '"Sochi"', "mon": '"25"', "tue": '"14"', "wed": '"1"', "thu": '"30"'},
                {"station": '"Perm"', "mon": '"5"', "tue": '"2"', "wed": '"1"', "thu": '"3"'},
                {"station": '"Tver"', "mon": '"7"', "tue": '"7"', "wed": '"7"', "thu": '"9"'}],
        intro="Метеостанция `station = {station}` четыре дня мерила дождь. Датчик присылает миллиметры осадков "
              "строками: `mon = {mon}`, `tue = {tue}`, `wed = {wed}`, `thu = {thu}`. Стакан осадкомера вмещает "
              "10 мм: когда он полный, его выливают.",
        steps=["Заведи переменную `total = 0`.",
               "Прибавь к `total` осадки каждого дня — четыре строки с `+=`, каждый день превращай в число с помощью `int()`.",
               "Выведи склейкой через `+` строку вида `Station Omsk: 24 mm` (`\"Station \"`, название, `\": \"`, "
               "сумма через `str()` и `\" mm\"`).",
               "Посчитай среднее за день: `total`, делённое на 4 (обычным делением `/`). Выведи `Per day:`, среднее и "
               "`mm` через `print` с запятыми.",
               "Посчитай, сколько раз стакан наполнился целиком (`total // 10`) и сколько мм осталось в нём (`total % 10`). "
               "Выведи `Full:`, первое число, `rest:` и второе через `print` с запятыми.",
               "Нарисуй полоску: склей `\"|\"`, знак `#`, повторённый столько раз, сколько было полных стаканов, и ещё `\"|\"` "
               "— например, `|##|`."],
        hint="`\"#\" * 3` даёт `\"###\"`, а `\"#\" * 0` — пустую строку, тогда полоска будет `||`. "
             "Если написать `total = int(tue)`, осадки понедельника пропадут — нужно именно `+=`.",
        solution='total = 0\ntotal += int(mon)\ntotal += int(tue)\ntotal += int(wed)\ntotal += int(thu)\n'
                 'print("Station " + station + ": " + str(total) + " mm")\n'
                 'average = total / 4\nprint("Per day:", average, "mm")\n'
                 'full = total // 10\nrest = total % 10\nprint("Full:", full, "rest:", rest)\n'
                 'print("|" + "#" * full + "|")',
        wrong=[("второй день кладёт через = вместо += — понедельник теряется",
                'total = 0\ntotal += int(mon)\ntotal = int(tue)\ntotal += int(wed)\ntotal += int(thu)\n'
                'print("Station " + station + ": " + str(total) + " mm")\n'
                'average = total / 4\nprint("Per day:", average, "mm")\n'
                'full = total // 10\nrest = total % 10\nprint("Full:", full, "rest:", rest)\n'
                'print("|" + "#" * full + "|")'),
               ("рисует полоску по остатку, а не по полным стаканам",
                'total = 0\ntotal += int(mon)\ntotal += int(tue)\ntotal += int(wed)\ntotal += int(thu)\n'
                'print("Station " + station + ": " + str(total) + " mm")\n'
                'average = total / 4\nprint("Per day:", average, "mm")\n'
                'full = total // 10\nrest = total % 10\nprint("Full:", full, "rest:", rest)\n'
                'print("|" + "#" * rest + "|")'),
               ("среднее считает делением нацело // — теряется дробная часть",
                'total = 0\ntotal += int(mon)\ntotal += int(tue)\ntotal += int(wed)\ntotal += int(thu)\n'
                'print("Station " + station + ": " + str(total) + " mm")\n'
                'average = total // 4\nprint("Per day:", average, "mm")\n'
                'full = total // 10\nrest = total % 10\nprint("Full:", full, "rest:", rest)\n'
                'print("|" + "#" * full + "|")')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-att10-puzzle", title="Пазл",
        given=["name", "pieces", "per_evening", "lost"],
        variants=[{"name": '"Lena"', "pieces": '"1000"', "per_evening": "120", "lost": "15"}],
        hidden=[{"name": '"Anya"', "pieces": '"500"', "per_evening": "100", "lost": "0"},
                {"name": '"Boris"', "pieces": '"2000"', "per_evening": "150", "lost": "50"},
                {"name": '"Mira"', "pieces": '"250"', "per_evening": "30", "lost": "6"},
                {"name": '"Oleg"', "pieces": '"1000"', "per_evening": "200", "lost": "1"}],
        intro="`name = {name}` собирает пазл. На коробке написано число деталей — в программе это строка "
              "`pieces = {pieces}`. Три вечера подряд удавалось собрать по `per_evening = {per_evening}` деталей, "
              "но потом кот смахнул со стола `lost = {lost}` уже собранных деталей.",
        steps=["Заведи `total` — число деталей из `pieces`, превращённое в целое число с помощью `int()`.",
               "Заведи `done` — сколько деталей собрано за три вечера (`per_evening * 3`). "
               "Вычти смахнутые котом детали с помощью `-=`.",
               "Выведи склейкой через `+` строку вида `Lena has 345 of 1000 pieces`: имя, `\" has \"`, `done` "
               "через `str()`, `\" of \"`, строку `pieces` (она уже строка) и `\" pieces\"`.",
               "Посчитай процент готовности: `done * 100 / total`. Выведи склейкой `\"Done: \"`, процент через "
               "`str()` и `\"%\"` — например, `Done: 34.5%`.",
               "Заведи `left = total` и вычти из неё собранное с помощью `-=` — это детали, которые ещё не собраны.",
               "Посчитай, сколько полных вечеров ещё нужно (`left // per_evening`) и сколько деталей останется "
               "на последний неполный вечер (`left % per_evening`). Выведи `Evenings left:`, первое число, `+`, "
               "второе и `pieces` через `print` с запятыми."],
        hint="`pieces` — строка: склеивать её можно сразу, а считать — только после `int()`. "
             "Сначала умножай на 100, потом дели — так процент получается точным. `655 // 120` даёт `5`, `655 % 120` — `55`.",
        solution='total = int(pieces)\ndone = per_evening * 3\ndone -= lost\n'
                 'print(name + " has " + str(done) + " of " + pieces + " pieces")\n'
                 'percent = done * 100 / total\nprint("Done: " + str(percent) + "%")\n'
                 'left = total\nleft -= done\n'
                 'print("Evenings left:", left // per_evening, "+", left % per_evening, "pieces")',
        wrong=[("забывает про детали, которые смахнул кот",
                'total = int(pieces)\ndone = per_evening * 3\n'
                'print(name + " has " + str(done) + " of " + pieces + " pieces")\n'
                'percent = done * 100 / total\nprint("Done: " + str(percent) + "%")\n'
                'left = total\nleft -= done\n'
                'print("Evenings left:", left // per_evening, "+", left % per_evening, "pieces")'),
               ("вечера считает обычным делением / — получается дробное число",
                'total = int(pieces)\ndone = per_evening * 3\ndone -= lost\n'
                'print(name + " has " + str(done) + " of " + pieces + " pieces")\n'
                'percent = done * 100 / total\nprint("Done: " + str(percent) + "%")\n'
                'left = total\nleft -= done\n'
                'print("Evenings left:", left / per_evening, "+", left % per_evening, "pieces")'),
               ("считает собранное за один вечер, а не за три",
                'total = int(pieces)\ndone = per_evening\ndone -= lost\n'
                'print(name + " has " + str(done) + " of " + pieces + " pieces")\n'
                'percent = done * 100 / total\nprint("Done: " + str(percent) + "%")\n'
                'left = total\nleft -= done\n'
                'print("Evenings left:", left // per_evening, "+", left % per_evening, "pieces")')],
        must_use=AUG,
    ),
]
