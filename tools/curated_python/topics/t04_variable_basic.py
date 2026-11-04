"""PY_VARIABLE_BASIC — «Переменные». Taught before: print (several values, empty print(), sep=, end=).
The student creates own variables with a value and uses variables (also one variable several times) in print.
Not yet: changing a variable (reassignment), arithmetic, string concatenation, f-strings, conditions, loops."""
from build import OutputTask

SKILL = "PY_VARIABLE_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-var-player-profile", title="Профиль игрока",
        given=["nick", "level"],
        variants=[{"nick": '"DragonSlayer"', "level": "12"}, {"nick": '"NightOwl"', "level": "3"},
                  {"nick": '"Rocket77"', "level": "40"}],
        hidden=[{"nick": '"Pixel"', "level": "1"}, {"nick": '"IceQueen"', "level": "25"}, {"nick": '"Bolt"', "level": "99"}],
        intro="Игра показывает профиль игрока. Ник и уровень уже есть в заготовке: `nick = {nick}` и `level = {level}`. "
              "Статус игрока программа хранит в своей переменной.",
        steps=["Создай переменную `status` со строкой `\"online\"`.",
               "Первой строкой выведи ник.",
               "Второй строкой выведи `Level:` и уровень.",
               "Третьей строкой выведи `Status:` и значение переменной `status`. Получится `Status: online`."],
        hint='Переменная создаётся так: `status = "online"` — слева имя, справа значение. Создай её до того, '
             'как печатаешь. В `print` имя переменной пиши без кавычек: `print("Status:", status)`.',
        solution='status = "online"\nprint(nick)\nprint("Level:", level)\nprint("Status:", status)',
        wrong=[("печатает слово level вместо уровня",
                'status = "online"\nprint(nick)\nprint("Level:", "level")\nprint("Status:", status)'),
               ("печатает уровень вместо ника",
                'status = "online"\nprint(level)\nprint("Level:", level)\nprint("Status:", status)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-var-weather", title="Прогноз погоды",
        given=["city", "temp", "wind"],
        variants=[{"city": '"Kazan"', "temp": "18", "wind": "4"}, {"city": '"Sochi"', "temp": "27", "wind": "2"},
                  {"city": '"Murmansk"', "temp": "-6", "wind": "11"}],
        hidden=[{"city": '"Tomsk"', "temp": "-20", "wind": "7"}, {"city": '"Ufa"', "temp": "9", "wind": "15"},
                {"city": '"Yalta"', "temp": "31", "wind": "1"}],
        intro="Приложение погоды показывает прогноз. Город, температура и скорость ветра уже есть в заготовке: "
              "`city = {city}`, `temp = {temp}`, `wind = {wind}`. Единицы измерения программа хранит в своих переменных.",
        steps=["Создай переменную `degrees` со строкой `\"C\"` и переменную `speed` со строкой `\"m/s\"`.",
               "Первой строкой выведи `Weather in` и город.",
               "Второй строкой выведи `Temperature:`, температуру и `degrees`. Например: `Temperature: 5 C`.",
               "Третьей строкой выведи `Wind:`, скорость ветра и `speed`. Например: `Wind: 3 m/s`."],
        hint='В одном `print` можно передать несколько переменных через запятую: `print("Wind:", wind, speed)`. '
             "Следи, чтобы в каждой строке стояла своя переменная: температура — `temp`, ветер — `wind`.",
        solution='degrees = "C"\nspeed = "m/s"\nprint("Weather in", city)\nprint("Temperature:", temp, degrees)\n'
                 'print("Wind:", wind, speed)',
        wrong=[("перепутал переменные: в строке температуры печатает ветер",
                'degrees = "C"\nspeed = "m/s"\nprint("Weather in", city)\nprint("Temperature:", wind, degrees)\n'
                'print("Wind:", wind, speed)'),
               ("забывает единицы у ветра",
                'degrees = "C"\nspeed = "m/s"\nprint("Weather in", city)\nprint("Temperature:", temp, degrees)\n'
                'print("Wind:", wind)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-var-invitation", title="Приглашение на праздник",
        given=["guest"],
        variants=[{"guest": '"Anya"'}, {"guest": '"Boris"'}, {"guest": '"Kamila"'}],
        hidden=[{"guest": '"Ilya"'}, {"guest": '"Zarina"'}, {"guest": '"Oleg"'}],
        intro="Ты печатаешь приглашения на день рождения. Имя гостя уже есть в заготовке: `guest = {guest}`. "
              "Название праздника и дату удобно хранить в переменных: если праздник перенесут, исправить нужно будет одну строку.",
        steps=["Создай переменную `party` со строкой `\"Birthday party\"` и переменную `date` со строкой `\"May 12\"`.",
               "Первой строкой выведи `Dear` и имя гостя.",
               "Второй строкой выведи `You are invited to` и `party`.",
               "Третьей строкой выведи `Date:` и `date`.",
               "Четвёртой строкой выведи `See you,` и снова имя гостя. Например, для гостя `\"Lena\"`: `See you, Lena`."],
        hint="Одну переменную можно использовать сколько угодно раз: имя гостя печатается и в первой, и в последней строке. "
             'Не бери имя переменной в кавычки: `print("See you,", "guest")` выведет само слово `guest`.',
        solution='party = "Birthday party"\ndate = "May 12"\nprint("Dear", guest)\nprint("You are invited to", party)\n'
                 'print("Date:", date)\nprint("See you,", guest)',
        wrong=[("берёт имя переменной в кавычки в последней строке",
                'party = "Birthday party"\ndate = "May 12"\nprint("Dear", guest)\nprint("You are invited to", party)\n'
                'print("Date:", date)\nprint("See you,", "guest")'),
               ("печатает название праздника вместо даты",
                'party = "Birthday party"\ndate = "May 12"\nprint("Dear", guest)\nprint("You are invited to", party)\n'
                'print("Date:", party)\nprint("See you,", guest)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-var-parcel-label", title="Наклейка на посылку",
        given=["receiver", "street", "city", "weight"],
        variants=[{"receiver": '"Boris Ivanov"', "street": '"Lenina 5"', "city": '"Sochi"', "weight": "3"},
                  {"receiver": '"Elena Kim"', "street": '"Mira 17"', "city": '"Kazan"', "weight": "12"},
                  {"receiver": '"Pavel Gromov"', "street": '"Sadovaya 2"', "city": '"Tula"', "weight": "1"}],
        hidden=[{"receiver": '"Maria Lis"', "street": '"Pushkina 10"', "city": '"Omsk"', "weight": "7"},
                {"receiver": '"Ruslan Aliev"', "street": '"Gagarina 41"', "city": '"Perm"', "weight": "20"},
                {"receiver": '"Nina Osipova"', "street": '"Polevaya 3"', "city": '"Kursk"', "weight": "2"}],
        intro="Интернет-магазин печатает наклейку на посылку. Данные получателя уже есть в заготовке: `receiver = {receiver}`, "
              "`street = {street}`, `city = {city}` и вес в килограммах `weight = {weight}`. Название магазина-отправителя "
              "программа хранит в своей переменной.",
        steps=["Создай переменную `shop` со строкой `\"Book Corner\"` и переменную `unit` со строкой `\"kg\"`.",
               "Первой строкой выведи `From:` и `shop`.",
               "Второй строкой выведи `To:` и получателя.",
               "Третьей строкой выведи улицу, четвёртой — город.",
               "Пятой строкой выведи `Weight:`, вес и `unit`. Например: `Weight: 4 kg`."],
        hint="Сначала создай переменные, потом печатай: Python выполняет строки сверху вниз, и переменную нельзя "
             "использовать до того, как ей дали значение. Улицу и город выводи каждую своим `print`.",
        solution='shop = "Book Corner"\nunit = "kg"\nprint("From:", shop)\nprint("To:", receiver)\nprint(street)\n'
                 'print(city)\nprint("Weight:", weight, unit)',
        wrong=[("перепутал переменные: в строке получателя печатает магазин",
                'shop = "Book Corner"\nunit = "kg"\nprint("From:", shop)\nprint("To:", shop)\nprint(street)\n'
                'print(city)\nprint("Weight:", weight, unit)'),
               ("путает порядок: город раньше улицы",
                'shop = "Book Corner"\nunit = "kg"\nprint("From:", shop)\nprint("To:", receiver)\nprint(city)\n'
                'print(street)\nprint("Weight:", weight, unit)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-var-club-meeting", title="Объявление о встрече клуба",
        given=["leader", "room", "time"],
        variants=[{"leader": '"Anya"', "room": "214", "time": '"18:00"'},
                  {"leader": '"Timur"', "room": "305", "time": '"16:30"'},
                  {"leader": '"Vera"', "room": "12", "time": '"19:15"'}],
        hidden=[{"leader": '"Gleb"', "room": "101", "time": '"15:00"'},
                {"leader": '"Alsu"', "room": "7", "time": '"20:45"'},
                {"leader": '"Mark"', "room": "420", "time": '"12:10"'}],
        intro="Школьный клуб программистов вешает объявление о встрече. Ведущий, кабинет и время уже есть в заготовке: "
              "`leader = {leader}`, `room = {room}`, `time = {time}`. Название клуба программа хранит в своей переменной "
              "и печатает его дважды.",
        steps=["Создай переменную `club` со строкой `\"Python club\"`.",
               "Первой строкой выведи название клуба.",
               "Второй строкой выведи `Leader:` и ведущего.",
               "Третьей строкой выведи `Room:` и кабинет, четвёртой — `Time:` и время.",
               "Пятой строкой выведи `Ask`, ведущего, `about` и название клуба. "
               "Например, для ведущего `\"Ivan\"`: `Ask Ivan about Python club`."],
        hint='В последней строке четыре значения в одном `print`: `print("Ask", leader, "about", club)`. '
             "Слова в кавычках печатаются как есть, а вместо переменных без кавычек подставляются их значения.",
        solution='club = "Python club"\nprint(club)\nprint("Leader:", leader)\nprint("Room:", room)\n'
                 'print("Time:", time)\nprint("Ask", leader, "about", club)',
        wrong=[("берёт имя переменной club в кавычки",
                'club = "Python club"\nprint(club)\nprint("Leader:", leader)\nprint("Room:", room)\n'
                'print("Time:", time)\nprint("Ask", leader, "about", "club")'),
               ("пишет имя ведущего прямо в тексте вместо переменной",
                'club = "Python club"\nprint(club)\nprint("Leader:", leader)\nprint("Room:", room)\n'
                'print("Time:", time)\nprint("Ask leader about", club)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-var-date-formats", title="Дата в двух форматах",
        given=["day", "month", "year"],
        variants=[{"day": '"12"', "month": '"05"', "year": '"2026"'},
                  {"day": '"01"', "month": '"09"', "year": '"2025"'},
                  {"day": '"31"', "month": '"12"', "year": '"2027"'}],
        hidden=[{"day": '"07"', "month": '"03"', "year": '"2024"'},
                {"day": '"25"', "month": '"11"', "year": '"2030"'},
                {"day": '"15"', "month": '"06"', "year": '"1999"'}],
        intro="В России дату пишут как день, месяц, год через точку, а в международном формате ISO — год, месяц, день "
              "через дефис. Части даты уже есть в заготовке: `day = {day}`, `month = {month}`, `year = {year}`. "
              "Разделители программа хранит в своих переменных.",
        steps=["Создай переменную `dot` со строкой `\".\"` и переменную `dash` со строкой `\"-\"`.",
               "Первой строкой выведи `Russian format:`.",
               "Второй строкой выведи день, месяц и год с разделителем `sep=dot`.",
               "Третьей строкой выведи `ISO format:`.",
               "Четвёртой строкой выведи год, месяц и день с разделителем `sep=dash`. "
               "Например, для 2 марта 2020 года строки будут `02.03.2020` и `2020-03-02`."],
        hint='Значение `sep` можно взять из переменной: `print("a", "b", sep=dot)` выведет `a.b`. '
             "Следи за порядком: в формате ISO год идёт первым, а день — последним.",
        solution='dot = "."\ndash = "-"\nprint("Russian format:")\nprint(day, month, year, sep=dot)\n'
                 'print("ISO format:")\nprint(year, month, day, sep=dash)',
        wrong=[("в формате ISO оставляет русский порядок день-месяц-год",
                'dot = "."\ndash = "-"\nprint("Russian format:")\nprint(day, month, year, sep=dot)\n'
                'print("ISO format:")\nprint(day, month, year, sep=dash)'),
               ("путает разделители",
                'dot = "."\ndash = "-"\nprint("Russian format:")\nprint(day, month, year, sep=dash)\n'
                'print("ISO format:")\nprint(year, month, day, sep=dot)')],
    ),
]
