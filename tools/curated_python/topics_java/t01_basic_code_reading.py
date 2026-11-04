"""BASIC_CODE_READING — «Вывод в консоль» (Java). Taught before: nothing — this is the first topic: System.out.println
and System.out.print (the difference: println ends the line), text in quotes is printed as is, a name without quotes
prints the value of a field of the starter. Not yet: declaring own variables, assignment, arithmetic, string operations
(no `+` between strings — a line is assembled from several print calls), conditions, loops."""
from java_tasks import JavaOutputTask

SKILL = "BASIC_CODE_READING"


def _code(*lines: str) -> str:
    return "\n".join(lines)


def _change(code: str, old: str, new: str, nth: int = 1) -> str:
    """The code with the nth line equal to `old` replaced by `new` (a one-line mistake)."""
    lines = code.split("\n")
    found = [i for i, line in enumerate(lines) if line == old]
    assert len(found) >= nth, f"no line {old!r}"
    lines[found[nth - 1]] = new
    return "\n".join(lines)


TICKET = _code(
    'System.out.println("TRAIN TICKET");',
    'System.out.print("From: ");',
    'System.out.println(fromCity);',
    'System.out.print("To: ");',
    'System.out.println(toCity);',
    'System.out.print("Seat: ");',
    'System.out.println(seat);',
)

CARD = _code(
    'System.out.print("Dear ");',
    'System.out.print(to);',
    'System.out.println(",");',
    'System.out.println();',
    'System.out.println("Happy birthday!");',
    'System.out.print("From ");',
    'System.out.println(from);',
)

ROUTE = _code(
    'System.out.print("Route ");',
    'System.out.println(route);',
    'System.out.print(first);',
    'System.out.print(" -> ");',
    'System.out.print(middle);',
    'System.out.print(" -> ");',
    'System.out.println(last);',
    'System.out.println("Have a good trip");',
)

SCORE = _code(
    'System.out.println("FINAL SCORE");',
    'System.out.print(home);',
    'System.out.print(" ");',
    'System.out.print(homeGoals);',
    'System.out.print(":");',
    'System.out.print(guestGoals);',
    'System.out.print(" ");',
    'System.out.println(guest);',
)

RECEIPT = _code(
    'System.out.println(shop);',
    'System.out.println("==========");',
    'System.out.print(item1);',
    'System.out.print(": ");',
    'System.out.print(price1);',
    'System.out.println(" rub");',
    'System.out.print(item2);',
    'System.out.print(": ");',
    'System.out.print(price2);',
    'System.out.println(" rub");',
    'System.out.println("==========");',
)

WEATHER = _code(
    'System.out.print("Weather in ");',
    'System.out.println(city);',
    'System.out.print("Day ");',
    'System.out.print(day);',
    'System.out.print(" / Night ");',
    'System.out.println(night);',
    'System.out.print("Sky: ");',
    'System.out.println(sky);',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-out-train-ticket", title="Билет на поезд",
        given=[("String", "fromCity"), ("String", "toCity"), ("int", "seat")],
        variants=[{"fromCity": '"Kazan"', "toCity": '"Sochi"', "seat": "14"},
                  {"fromCity": '"Moscow"', "toCity": '"Samara"', "seat": "37"},
                  {"fromCity": '"Perm"', "toCity": '"Ufa"', "seat": "5"}],
        hidden=[{"fromCity": '"Omsk"', "toCity": '"Tomsk"', "seat": "21"},
                {"fromCity": '"Kirov"', "toCity": '"Kazan"', "seat": "1"},
                {"fromCity": '"Sochi"', "toCity": '"Moscow"', "seat": "54"}],
        intro="Касса вокзала печатает билет: город отправления, город прибытия и номер места. "
              "Они записаны в полях `fromCity`, `toCity` и `seat`.",
        steps=["Первой строкой выведи `TRAIN TICKET`.",
               "Второй строкой — `From: ` и значение `fromCity`, например `From: Kazan`.",
               "Третьей — `To: ` и значение `toCity`, четвёртой — `Seat: ` и значение `seat`.",
               "Подпись и значение стоят на одной строке: подпись выведи через `System.out.print`, а значение — через `System.out.println`."],
        hint="`System.out.print` не переходит на новую строку, а `System.out.println` переходит. "
             "Имя поля пиши без кавычек: `System.out.println(seat)` печатает число, а `System.out.println(\"seat\")` — слово seat.",
        solution=TICKET,
        wrong=[("имя поля в кавычках: печатает слово fromCity вместо города",
                _change(TICKET, 'System.out.println(fromCity);', 'System.out.println("fromCity");')),
               ("подпись выведена через println: значение уходит на следующую строку",
                _change(TICKET, 'System.out.print("To: ");', 'System.out.println("To: ");'))],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-out-birthday-card", title="Открытка ко дню рождения",
        given=[("String", "to"), ("String", "from")],
        variants=[{"to": '"Anya"', "from": '"Boris"'}, {"to": '"Grandma"', "from": '"Masha"'}, {"to": '"Timur"', "from": '"Dad"'}],
        hidden=[{"to": '"Vika"', "from": '"Oleg"'}, {"to": '"Mom"', "from": '"Kate"'}, {"to": '"Ilya"', "from": '"Team"'}],
        intro="Ты печатаешь открытку. Кому она, записано в поле `to`, от кого — в поле `from`.",
        steps=["Первая строка: `Dear `, имя из `to` и запятая, например `Dear Anya,`. Выведи её тремя командами: "
               "`Dear ` и имя — через `System.out.print`, запятую — через `System.out.println`.",
               "Вторая строка пустая: `System.out.println();` с пустыми скобками.",
               "Третья строка: `Happy birthday!`",
               "Четвёртая строка: `From ` и имя из `from`, например `From Boris`."],
        hint="Пока не вызван `println`, всё печатается на одной строке. Пустые скобки у `println` дают пустую строку.",
        solution=CARD,
        wrong=[("имя выведено через println: запятая уезжает на следующую строку",
                _change(CARD, 'System.out.print(to);', 'System.out.println(to);')),
               ("имя поля в кавычках: печатает слово from вместо имени",
                _change(CARD, 'System.out.println(from);', 'System.out.println("from");'))],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-out-bus-route", title="Табло автобуса",
        given=[("int", "route"), ("String", "first"), ("String", "middle"), ("String", "last")],
        variants=[{"route": "7", "first": '"Station"', "middle": '"Park"', "last": '"Airport"'},
                  {"route": "42", "first": '"Market"', "middle": '"School"', "last": '"Stadium"'},
                  {"route": "15", "first": '"Center"', "middle": '"Bridge"', "last": '"Zoo"'}],
        hidden=[{"route": "3", "first": '"Port"', "middle": '"Theatre"', "last": '"Hospital"'},
                {"route": "101", "first": '"Lake"', "middle": '"Mall"', "last": '"Library"'},
                {"route": "8", "first": '"Airport"', "middle": '"Station"', "last": '"Park"'}],
        intro="На табло автобуса показаны номер маршрута и три остановки по порядку. Номер записан в поле `route`, "
              "остановки — в полях `first`, `middle` и `last`.",
        steps=["Первая строка: `Route ` и номер маршрута, например `Route 7`.",
               "Вторая строка: три остановки через ` -> ` (пробел, стрелка из минуса и знака больше, пробел), например `Station -> Park -> Airport`.",
               "Третья строка: `Have a good trip`.",
               "Каждую часть строки выводи отдельной командой `System.out.print`, а последнюю часть строки — `System.out.println`."],
        hint="Вторая строка собирается из пяти частей: остановка, стрелка, остановка, стрелка, остановка. "
             "Перейти на новую строку нужно только после последней.",
        solution=ROUTE,
        wrong=[("средняя остановка выведена через println: строка рвётся посередине",
                _change(ROUTE, 'System.out.print(middle);', 'System.out.println(middle);')),
               ("последняя остановка выведена через print: следующая строка приклеивается к ней",
                _change(ROUTE, 'System.out.println(last);', 'System.out.print(last);'))],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-out-match-score", title="Счёт матча",
        given=[("String", "home"), ("String", "guest"), ("int", "homeGoals"), ("int", "guestGoals")],
        variants=[{"home": '"Rubin"', "guest": '"Zenit"', "homeGoals": "2", "guestGoals": "1"},
                  {"home": '"Spartak"', "guest": '"Dynamo"', "homeGoals": "0", "guestGoals": "3"},
                  {"home": '"Sochi"', "guest": '"Ural"', "homeGoals": "4", "guestGoals": "2"}],
        hidden=[{"home": '"Akron"', "guest": '"Krasnodar"', "homeGoals": "1", "guestGoals": "5"},
                {"home": '"Orenburg"', "guest": '"Rostov"', "homeGoals": "3", "guestGoals": "0"},
                {"home": '"Zenit"', "guest": '"Rubin"', "homeGoals": "2", "guestGoals": "2"}],
        intro="После матча на табло стадиона выводят итоговый счёт. Хозяева поля записаны в поле `home`, гости — в `guest`, "
              "их голы — в `homeGoals` и `guestGoals`.",
        steps=["Первая строка: `FINAL SCORE`.",
               "Вторая строка: хозяева, пробел, голы хозяев, двоеточие, голы гостей, пробел, гости — например `Rubin 2:1 Zenit`.",
               "Вторую строку выводи по частям командой `System.out.print`, а последнюю часть — `System.out.println`."],
        hint="Пробелы и двоеточие — это тоже части строки, их печатают в кавычках: `System.out.print(\" \");`. "
             "Сначала идут голы хозяев, потом гостей.",
        solution=SCORE,
        wrong=[("дважды выводит голы гостей вместо голов хозяев",
                _change(SCORE, 'System.out.print(homeGoals);', 'System.out.print(guestGoals);')),
               ("голы хозяев выведены через println: счёт разрывается на две строки",
                _change(SCORE, 'System.out.print(homeGoals);', 'System.out.println(homeGoals);'))],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-out-shop-receipt", title="Чек из магазина",
        given=[("String", "shop"), ("String", "item1"), ("int", "price1"), ("String", "item2"), ("int", "price2")],
        variants=[{"shop": '"Lenta"', "item1": '"bread"', "price1": "45", "item2": '"milk"', "price2": "89"},
                  {"shop": '"Magnit"', "item1": '"apples"', "price1": "120", "item2": '"tea"', "price2": "210"},
                  {"shop": '"Pyaterochka"', "item1": '"cheese"', "price1": "350", "item2": '"eggs"', "price2": "99"}],
        hidden=[{"shop": '"Perekrestok"', "item1": '"rice"', "price1": "80", "item2": '"juice"', "price2": "130"},
                {"shop": '"Dixy"', "item1": '"butter"', "price1": "190", "item2": '"bread"', "price2": "40"},
                {"shop": '"Lenta"', "item1": '"milk"', "price1": "89", "item2": '"bread"', "price2": "45"}],
        intro="Касса печатает короткий чек на две покупки. Название магазина записано в поле `shop`, покупки и их цены — "
              "в полях `item1`, `price1`, `item2`, `price2`.",
        steps=["Первая строка: название магазина.",
               "Вторая строка: десять знаков равенства `==========`.",
               "Третья строка: первая покупка, двоеточие с пробелом, её цена и ` rub` — например `bread: 45 rub`.",
               "Четвёртая строка: так же для второй покупки.",
               "Пятая строка: снова `==========`."],
        hint="Строку с покупкой выводи четырьмя командами: товар, `\": \"` и цена — через `System.out.print`, "
             "а `\" rub\"` (с пробелом впереди) — через `System.out.println`.",
        solution=RECEIPT,
        wrong=[("цена выведена через println: слово rub уезжает на следующую строку",
                _change(RECEIPT, 'System.out.print(price1);', 'System.out.println(price1);')),
               ("во второй строке покупки снова цена первой покупки",
                _change(RECEIPT, 'System.out.print(price2);', 'System.out.print(price1);'))],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-out-weather-card", title="Прогноз погоды",
        given=[("String", "city"), ("int", "day"), ("int", "night"), ("String", "sky")],
        variants=[{"city": '"Sochi"', "day": "24", "night": "17", "sky": '"sunny"'},
                  {"city": '"Kazan"', "day": "12", "night": "5", "sky": '"cloudy"'},
                  {"city": '"Murmansk"', "day": "3", "night": "0", "sky": '"snow"'}],
        hidden=[{"city": '"Omsk"', "day": "18", "night": "9", "sky": '"rain"'},
                {"city": '"Moscow"', "day": "7", "night": "2", "sky": '"windy"'},
                {"city": '"Sochi"', "day": "17", "night": "24", "sky": '"fog"'}],
        intro="Погодное приложение показывает карточку на сегодня. Город записан в поле `city`, температура днём и ночью — "
              "в полях `day` и `night`, состояние неба — в поле `sky`.",
        steps=["Первая строка: `Weather in ` и город, например `Weather in Sochi`.",
               "Вторая строка: `Day `, дневная температура, ` / Night ` и ночная температура, например `Day 24 / Night 17`.",
               "Третья строка: `Sky: ` и значение `sky`, например `Sky: sunny`.",
               "Части одной строки выводи через `System.out.print`, а последнюю часть каждой строки — через `System.out.println`."],
        hint="Во второй строке четыре части: `\"Day \"`, `day`, `\" / Night \"`, `night`. Следи за пробелами внутри кавычек.",
        solution=WEATHER,
        wrong=[("подпись ночи выведена через println: строка рвётся посередине",
                _change(WEATHER, 'System.out.print(" / Night ");', 'System.out.println(" / Night ");')),
               ("ночью выводит дневную температуру",
                _change(WEATHER, 'System.out.println(night);', 'System.out.println(day);'))],
    ),
]
