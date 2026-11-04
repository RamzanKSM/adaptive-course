"""INTEGER_DIVISION — «Целочисленное деление и остаток» (Java). Taught before: println, variables, assignment, arithmetic,
execution order, primitive types, String. The point: int / int drops the fraction, % gives the remainder; together
they split a number into units (hours and minutes, hundreds and tens, rows and seats). Not yet: += -= ++, if/else,
comparisons, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "INTEGER_DIVISION"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-div-pizza-slices", title="Пицца на компанию",
        given=[("int", "slices"), ("int", "friends")],
        variants=[{"slices": "10", "friends": "3"}, {"slices": "12", "friends": "5"}, {"slices": "16", "friends": "6"}],
        hidden=[{"slices": "10", "friends": "5"}, {"slices": "7", "friends": "10"}, {"slices": "9", "friends": "2"},
                {"slices": "24", "friends": "7"}],
        intro="Друзья заказали пиццу и делят куски поровну, целыми кусками. Сколько всего кусков, записано в поле "
              "`slices`, сколько друзей — в поле `friends`. Лишние куски, которые не делятся поровну, остаются в коробке.",
        steps=["Заведи `int each` — сколько целых кусков достанется каждому.",
               "Заведи `int left` — сколько кусков останется в коробке.",
               "Выведи три строки: `Friends: ` и число друзей, `Each gets: ` и `each`, `Left in box: ` и `left`."],
        hint="При делении двух `int` Java отбрасывает дробную часть: `8 / 3` — это `2`. "
             "Остаток от деления даёт оператор `%`: `8 % 3` — это `2`.",
        solution='int each = slices / friends;\n'
                 'int left = slices % friends;\n'
                 'System.out.println("Friends: " + friends);\n'
                 'System.out.println("Each gets: " + each);\n'
                 'System.out.println("Left in box: " + left);',
        wrong=[("операнды остатка перепутаны: друзья % куски",
                'int each = slices / friends;\n'
                'int left = friends % slices;\n'
                'System.out.println("Friends: " + friends);\n'
                'System.out.println("Each gets: " + each);\n'
                'System.out.println("Left in box: " + left);'),
               ("перепутаны / и %: каждому — остаток",
                'int each = slices % friends;\n'
                'int left = slices % friends;\n'
                'System.out.println("Friends: " + friends);\n'
                'System.out.println("Each gets: " + each);\n'
                'System.out.println("Left in box: " + left);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-div-film-duration", title="Длительность фильма",
        given=[("String", "title"), ("int", "minutes")],
        variants=[{"title": '"Interstellar"', "minutes": "169"}, {"title": '"Up"', "minutes": "96"},
                  {"title": '"Titanic"', "minutes": "194"}],
        hidden=[{"title": '"Short"', "minutes": "60"}, {"title": '"Cartoon"', "minutes": "59"},
                {"title": '"Avatar"', "minutes": "162"}, {"title": '"Shrek"', "minutes": "90"}],
        intro="Сайт кинотеатра показывает длительность фильма в часах и минутах. Название фильма записано в поле "
              "`title`, длительность в минутах — в поле `minutes`.",
        steps=["Заведи `int hours` — сколько полных часов в фильме, и `int rest` — сколько минут остаётся сверх полных часов.",
               "Заведи `int seconds` — длительность фильма в секундах.",
               "Выведи `Film: ` и название.",
               "Выведи `Duration: `, часы, ` h `, минуты и ` min` — например `Duration: 2 h 49 min`.",
               "Последней строкой выведи `In seconds: ` и `seconds`."],
        hint="В часе 60 минут. Полные часы — это `minutes / 60` (дробная часть отбрасывается), "
             "а оставшиеся минуты — остаток `minutes % 60`.",
        solution='int hours = minutes / 60;\n'
                 'int rest = minutes % 60;\n'
                 'int seconds = minutes * 60;\n'
                 'System.out.println("Film: " + title);\n'
                 'System.out.println("Duration: " + hours + " h " + rest + " min");\n'
                 'System.out.println("In seconds: " + seconds);',
        wrong=[("минуты сверх часов посчитаны как minutes - 60: верно только для фильмов от часа до двух",
                'int hours = minutes / 60;\n'
                'int rest = minutes - 60;\n'
                'int seconds = minutes * 60;\n'
                'System.out.println("Film: " + title);\n'
                'System.out.println("Duration: " + hours + " h " + rest + " min");\n'
                'System.out.println("In seconds: " + seconds);'),
               ("перепутаны / и %: часы — остаток",
                'int hours = minutes % 60;\n'
                'int rest = minutes % 60;\n'
                'int seconds = minutes * 60;\n'
                'System.out.println("Film: " + title);\n'
                'System.out.println("Duration: " + hours + " h " + rest + " min");\n'
                'System.out.println("In seconds: " + seconds);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-div-lock-digits", title="Цифры кодового замка",
        given=[("int", "code")],
        variants=[{"code": "472"}, {"code": "905"}, {"code": "318"}],
        hidden=[{"code": "100"}, {"code": "999"}, {"code": "560"}, {"code": "101"}],
        intro="У чемодана кодовый замок с тремя колёсиками. Код — трёхзначное число — записан в поле `code`. "
              "Чтобы выставить код, нужно знать каждую цифру отдельно.",
        steps=["Заведи `int hundreds` — первую цифру (сотни), `int tens` — вторую (десятки), `int ones` — третью (единицы).",
               "Заведи `int sum` — сумму трёх цифр.",
               "Выведи четыре строки: `First wheel: ` и сотни, `Second wheel: ` и десятки, `Third wheel: ` и единицы, "
               "`Digit sum: ` и сумму."],
        hint="Последняя цифра числа — остаток от деления на 10: `472 % 10` — это `2`. Деление на 10 «отрезает» "
             "последнюю цифру: `472 / 10` — это `47`. Комбинируя `/` и `%`, достань среднюю цифру.",
        solution='int hundreds = code / 100;\n'
                 'int tens = code / 10 % 10;\n'
                 'int ones = code % 10;\n'
                 'int sum = hundreds + tens + ones;\n'
                 'System.out.println("First wheel: " + hundreds);\n'
                 'System.out.println("Second wheel: " + tens);\n'
                 'System.out.println("Third wheel: " + ones);\n'
                 'System.out.println("Digit sum: " + sum);',
        wrong=[("десятки как code % 100: получаются две последние цифры",
                'int hundreds = code / 100;\n'
                'int tens = code % 100;\n'
                'int ones = code % 10;\n'
                'int sum = hundreds + tens + ones;\n'
                'System.out.println("First wheel: " + hundreds);\n'
                'System.out.println("Second wheel: " + tens);\n'
                'System.out.println("Third wheel: " + ones);\n'
                'System.out.println("Digit sum: " + sum);'),
               ("десятки как code / 10: получаются две первые цифры",
                'int hundreds = code / 100;\n'
                'int tens = code / 10;\n'
                'int ones = code % 10;\n'
                'int sum = hundreds + tens + ones;\n'
                'System.out.println("First wheel: " + hundreds);\n'
                'System.out.println("Second wheel: " + tens);\n'
                'System.out.println("Third wheel: " + ones);\n'
                'System.out.println("Digit sum: " + sum);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-div-atm-notes", title="Банкомат выдаёт купюры",
        given=[("int", "amount")],
        variants=[{"amount": "3750"}, {"amount": "12480"}, {"amount": "905"}],
        hidden=[{"amount": "1000"}, {"amount": "99"}, {"amount": "2001"}, {"amount": "15999"}],
        intro="Банкомат выдаёт сумму `amount` рублей: сначала как можно больше купюр по 1000, из того, что осталось, — "
              "как можно больше купюр по 100, а остаток — монетами.",
        steps=["Заведи `int thousands` — сколько купюр по 1000, и `int rest` — сколько рублей останется после них.",
               "Заведи `int hundreds` — сколько купюр по 100 можно выдать из `rest`.",
               "Заведи `int coins` — сколько рублей останется на монеты.",
               "Выведи три строки: `1000 rub notes: ` и число тысячных купюр, `100 rub notes: ` и число сотенных, "
               "`Coins: `, сумму монетами и ` rub`."],
        hint="Каждый следующий шаг работает с остатком предыдущего: сотенные купюры считаются не из всей суммы, а из "
             "того, что осталось после тысячных, — то есть из `amount % 1000`.",
        solution='int thousands = amount / 1000;\n'
                 'int rest = amount % 1000;\n'
                 'int hundreds = rest / 100;\n'
                 'int coins = rest % 100;\n'
                 'System.out.println("1000 rub notes: " + thousands);\n'
                 'System.out.println("100 rub notes: " + hundreds);\n'
                 'System.out.println("Coins: " + coins + " rub");',
        wrong=[("сотенные считаются из всей суммы, а не из остатка",
                'int thousands = amount / 1000;\n'
                'int rest = amount % 1000;\n'
                'int hundreds = amount / 100;\n'
                'int coins = rest % 100;\n'
                'System.out.println("1000 rub notes: " + thousands);\n'
                'System.out.println("100 rub notes: " + hundreds);\n'
                'System.out.println("Coins: " + coins + " rub");'),
               ("остаток после тысячных как amount - thousands: забыто умножение на 1000",
                'int thousands = amount / 1000;\n'
                'int rest = amount - thousands;\n'
                'int hundreds = rest / 100;\n'
                'int coins = rest % 100;\n'
                'System.out.println("1000 rub notes: " + thousands);\n'
                'System.out.println("100 rub notes: " + hundreds);\n'
                'System.out.println("Coins: " + coins + " rub");')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-div-cinema-seat", title="Ряд и место по номеру билета",
        given=[("int", "ticket"), ("int", "seatsInRow")],
        variants=[{"ticket": "27", "seatsInRow": "10"}, {"ticket": "40", "seatsInRow": "8"}, {"ticket": "13", "seatsInRow": "12"}],
        hidden=[{"ticket": "1", "seatsInRow": "10"}, {"ticket": "10", "seatsInRow": "10"}, {"ticket": "11", "seatsInRow": "10"},
                {"ticket": "100", "seatsInRow": "20"}, {"ticket": "5", "seatsInRow": "6"}],
        intro="В зале кинотеатра в каждом ряду `seatsInRow` мест. Билеты пронумерованы подряд с 1: первые `seatsInRow` "
              "билетов — это первый ряд (места с 1 по `seatsInRow`), следующие — второй ряд и так далее. "
              "Номер билета записан в поле `ticket`.",
        steps=["Заведи `int index` — номер билета, если считать с нуля: `ticket` минус `1`.",
               "Заведи `int row` — номер ряда: `index`, делённый нацело на `seatsInRow`, плюс `1`.",
               "Заведи `int seat` — номер места в ряду: остаток от деления `index` на `seatsInRow`, плюс `1`.",
               "Заведи `int before` — сколько мест во всех рядах перед твоим: (`row` минус 1), умноженное на `seatsInRow`.",
               "Выведи четыре строки: `Ticket: `, `Row: `, `Seat: `, `Seats in front rows: ` — после каждой надписи её число."],
        hint="Деление и остаток удобно считать от нуля: при 10 местах в ряду билеты 1–10 дают `index` от 0 до 9, и "
             "`index / 10` у всех них равно `0`. Проверь себя на последнем месте ряда: билет 10 — это ряд 1, место 10.",
        solution='int index = ticket - 1;\n'
                 'int row = index / seatsInRow + 1;\n'
                 'int seat = index % seatsInRow + 1;\n'
                 'int before = (row - 1) * seatsInRow;\n'
                 'System.out.println("Ticket: " + ticket);\n'
                 'System.out.println("Row: " + row);\n'
                 'System.out.println("Seat: " + seat);\n'
                 'System.out.println("Seats in front rows: " + before);',
        wrong=[("ряд считается от номера билета, а не от index: последнее место ряда уходит в следующий ряд",
                'int index = ticket - 1;\n'
                'int row = ticket / seatsInRow + 1;\n'
                'int seat = index % seatsInRow + 1;\n'
                'int before = (row - 1) * seatsInRow;\n'
                'System.out.println("Ticket: " + ticket);\n'
                'System.out.println("Row: " + row);\n'
                'System.out.println("Seat: " + seat);\n'
                'System.out.println("Seats in front rows: " + before);'),
               ("место как ticket % seatsInRow: последнее место ряда получается нулевым",
                'int index = ticket - 1;\n'
                'int row = index / seatsInRow + 1;\n'
                'int seat = ticket % seatsInRow;\n'
                'int before = (row - 1) * seatsInRow;\n'
                'System.out.println("Ticket: " + ticket);\n'
                'System.out.println("Row: " + row);\n'
                'System.out.println("Seat: " + seat);\n'
                'System.out.println("Seats in front rows: " + before);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-div-race-pace", title="Время и темп забега",
        given=[("int", "time"), ("int", "km")],
        variants=[{"time": "7384", "km": "21"}, {"time": "15125", "km": "42"}, {"time": "3005", "km": "10"}],
        hidden=[{"time": "3599", "km": "10"}, {"time": "3600", "km": "12"}, {"time": "59", "km": "1"},
                {"time": "10000", "km": "7"}, {"time": "4321", "km": "5"}],
        intro="Спортивные часы записали время забега в секундах — поле `time` — и длину дистанции в километрах — поле "
              "`km`. Нужно показать время в часах, минутах и секундах и темп — сколько в среднем занял один километр.",
        steps=["Заведи `int hours` — полные часы, `int minutes` — полные минуты сверх часов, `int seconds` — секунды сверх минут.",
               "Заведи `int pace` — секунд на один километр: `time`, делённое нацело на `km`.",
               "Заведи `int paceMin` и `int paceSec` — сколько в `pace` полных минут и секунд сверх них.",
               "Выведи `Time: `, часы, ` h `, минуты, ` min `, секунды и ` s` — например `Time: 2 h 3 min 4 s`.",
               "Следующей строкой выведи `Pace: `, минуты темпа, ` min `, секунды темпа и ` s per km`."],
        hint="В часе 3600 секунд. Минуты сверх часов — это сначала остаток после часов (`time % 3600`), а потом "
             "деление этого остатка на 60. Секунды сверх минут — просто `time % 60`.",
        solution='int hours = time / 3600;\n'
                 'int minutes = time % 3600 / 60;\n'
                 'int seconds = time % 60;\n'
                 'int pace = time / km;\n'
                 'int paceMin = pace / 60;\n'
                 'int paceSec = pace % 60;\n'
                 'System.out.println("Time: " + hours + " h " + minutes + " min " + seconds + " s");\n'
                 'System.out.println("Pace: " + paceMin + " min " + paceSec + " s per km");',
        wrong=[("минуты как time / 60: получаются все минуты забега, а не сверх часов",
                'int hours = time / 3600;\n'
                'int minutes = time / 60;\n'
                'int seconds = time % 60;\n'
                'int pace = time / km;\n'
                'int paceMin = pace / 60;\n'
                'int paceSec = pace % 60;\n'
                'System.out.println("Time: " + hours + " h " + minutes + " min " + seconds + " s");\n'
                'System.out.println("Pace: " + paceMin + " min " + paceSec + " s per km");'),
               ("секунды как time % 3600: получается остаток после часов целиком",
                'int hours = time / 3600;\n'
                'int minutes = time % 3600 / 60;\n'
                'int seconds = time % 3600;\n'
                'int pace = time / km;\n'
                'int paceMin = pace / 60;\n'
                'int paceSec = pace % 60;\n'
                'System.out.println("Time: " + hours + " h " + minutes + " min " + seconds + " s");\n'
                'System.out.println("Pace: " + paceMin + " min " + paceSec + " s per km");')],
        constructs=["assignment"],
    ),
]
