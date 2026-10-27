"""Attestation, Java, topics 1–9 (up to ASSIGNMENT_OPERATORS): println, variables, assignment, arithmetic, execution order,
primitive types (double, char), String (+, length, charAt, substring, indexOf, toUpperCase), / and %, += -= *= /= ++ --.
One integrative story per family, theme: transport, travel and city life.
Not yet: if/else, comparisons, logical operators, switch, loops, arrays, own methods and classes."""
from java_tasks import JavaOutputTask

SKILL = "ASSIGNMENT_OPERATORS"


def _code(*lines: str) -> str:
    return "\n".join(lines)


def _change(code: str, old: str, new: str) -> str:
    """The code with the line equal to `old` replaced by `new` (a one-line mistake)."""
    lines = code.split("\n")
    assert old in lines, old
    lines[lines.index(old)] = new
    return "\n".join(lines)


TAXI = _code(
    'int price = 150;',
    'price += km * 32;',
    'price += waiting * 9;',
    'price -= price % 10;',
    'int points = price / 100;',
    'double share = price;',
    'share /= people;',
    'System.out.println("Taxi to " + street.toUpperCase());',
    'System.out.println("Price: " + price + " rub");',
    'System.out.println("Each pays: " + share + " rub");',
    'System.out.println("Points: " + points);')

METRO = _code(
    'char badge = line.toUpperCase().charAt(0);',
    'int travel = stations * 2;',
    'travel += transfers * 5;',
    'travel++;',
    'System.out.println("Line " + badge + ", travel: " + travel + " min");',
    'int clock = hour * 60 + minute + travel;',
    'hour = (clock / 60) % 24;',
    'minute = clock % 60;',
    'System.out.println("Arrival: " + hour + " h " + minute + " min");')

TRAIN = _code(
    'seat--;',
    'int car = seat / seatsPerCar + 1;',
    'int place = seat % seatsPerCar + 1;',
    'String code = city.substring(0, 3).toUpperCase() + "-" + car + "-" + place;',
    'double price = km * 1.5;',
    'price += 150;',
    'price /= 2;',
    'System.out.println("Car: " + car + ", seat: " + place);',
    'System.out.println("Ticket: " + code);',
    'System.out.println("Price: " + price + " rub");')

PARKING = _code(
    'String number = plate.substring(0, 6);',
    'String region = plate.substring(6);',
    'int hours = minutes / 60;',
    'int rest = minutes % 60;',
    'int cost = hours * hourPrice;',
    'cost += rest * minutePrice;',
    'double total = cost * 0.75;',
    'System.out.println("Car: " + number + ", region " + region);',
    'System.out.println("Parked: " + hours + " h " + rest + " min");',
    'System.out.println("Cost: " + cost + " rub, to pay: " + total + " rub");')

SCOOTER = _code(
    'String name = login.substring(0, login.indexOf("."));',
    'int cost = 50;',
    'cost += minutes * 7;',
    'balance -= cost;',
    'double km = meters / 1000.0;',
    'int points = meters / 500;',
    'int toNext = 500 - meters % 500;',
    'System.out.println("Hi, " + name + "!");',
    'System.out.println("Distance: " + km + " km, cost: " + cost + " rub");',
    'System.out.println("Balance: " + balance + " rub");',
    'System.out.println("Points: " + points + ", next in " + toNext + " m");')

TOUR = _code(
    'int total = tourists * ticket;',
    'total += museum.length() * 30;',
    'tourists++;',
    'int buses = tourists / seats;',
    'int minivan = tourists % seats;',
    'double guide = total * 0.125;',
    'System.out.println("Tour to " + museum + ": " + tourists + " people");',
    'System.out.println("Buses: " + buses + ", minivan: " + minivan);',
    'System.out.println("Total: " + total + " rub, guide: " + guide + " rub");')

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att9-taxi", title="Такси на компанию",
        given=[("String", "street"), ("int", "km"), ("int", "waiting"), ("int", "people")],
        variants=[{"street": '"Lenina"', "km": "7", "waiting": "5", "people": "4"}],
        hidden=[{"street": '"Mira"', "km": "0", "waiting": "0", "people": "1"},
                {"street": '"Sadovaya"', "km": "25", "waiting": "11", "people": "2"},
                {"street": '"Arbat"', "km": "3", "waiting": "1", "people": "8"},
                {"street": '"Tverskaya"', "km": "12", "waiting": "0", "people": "5"}],
        intro="Друзья едут на такси на улицу `street`: `people` человек, `km` километров. Посадка стоит 150 рублей, "
              "каждый километр — 32 рубля, каждая минута ожидания — 9 рублей, а водитель ждал их `waiting` минут. "
              "Водитель округляет цену вниз до десятков рублей, а за каждые полные 100 рублей начисляет бонусный балл.",
        steps=["Заведи `int price = 150;`. Прибавь к `price` плату за километры (`km * 32`), потом плату за ожидание "
               "(`waiting * 9`) — каждую операцией `+=`.",
               "Округли цену вниз до десятков: отними от `price` остаток от деления `price` на `10` операцией `-=`.",
               "Заведи `int points = price / 100;` — число бонусных баллов.",
               "Заведи `double share = price;` и раздели `share` на `people` операцией `/=` — это доля каждого, "
               "в `double` деление не отбрасывает дробную часть.",
               "Выведи четыре строки: `Taxi to ` и название улицы заглавными буквами (`toUpperCase()`); `Price: `, цена "
               "и ` rub`; `Each pays: `, доля и ` rub`; `Points: ` и баллы."],
        hint="`price % 10` — это последняя цифра цены, без неё цена делится на 10 ровно. Делить долю нужно уже "
             "округлённую цену, поэтому округление идёт раньше, чем `share`.",
        solution=TAXI,
        wrong=[("%= вместо -= ... %: в price остаётся только последняя цифра",
                _change(TAXI, 'price -= price % 10;', 'price %= 10;')),
               ("доля посчитана в int: price / people отбрасывает дробную часть ещё до записи в double",
                _change(_change(TAXI, 'double share = price;', 'double share = price / people;'), 'share /= people;', '')),
               ("=+ вместо +=: плата за километры теряется",
                _change(TAXI, 'price += waiting * 9;', 'price =+ waiting * 9;'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att9-metro", title="Когда я доеду на метро",
        given=[("String", "line"), ("int", "hour"), ("int", "minute"), ("int", "stations"), ("int", "transfers")],
        variants=[{"line": '"green"', "hour": "8", "minute": "47", "stations": "9", "transfers": "2"}],
        hidden=[{"line": '"ring"', "hour": "23", "minute": "50", "stations": "10", "transfers": "1"},
                {"line": '"blue"', "hour": "10", "minute": "30", "stations": "12", "transfers": "1"},
                {"line": '"yellow"', "hour": "6", "minute": "0", "stations": "1", "transfers": "0"},
                {"line": '"red"', "hour": "17", "minute": "15", "stations": "20", "transfers": "3"}],
        intro="Аня входит в метро на линии `line` в `hour` часов `minute` минут. Ей нужно проехать `stations` перегонов "
              "(по 2 минуты каждый) и сделать `transfers` пересадок (по 5 минут каждая), а ещё одна минута уходит "
              "на турникет. Во сколько она доедет?",
        steps=["Заведи `char badge` — первую букву названия линии заглавной: `line.toUpperCase().charAt(0)`.",
               "Заведи `int travel = stations * 2;`, прибавь время пересадок (`transfers * 5`) операцией `+=` и добавь "
               "минуту на турникет операцией `++`.",
               "Выведи `Line `, букву, `, travel: `, время в пути и ` min`.",
               "Заведи `int clock = hour * 60 + minute + travel;` — сколько минут пройдёт с полуночи до прибытия.",
               "Запиши в `hour` час прибытия — `(clock / 60) % 24` (после 23 часов снова идёт 0), а в `minute` — "
               "минуты прибытия: `clock % 60`.",
               "Выведи `Arrival: `, час, ` h `, минуты и ` min`."],
        hint="Просто прибавить `travel` к `minute` нельзя: минут может стать больше 60. Поэтому время переводится в "
             "минуты с полуночи, а потом обратно — делением нацело и остатком.",
        solution=METRO,
        wrong=[("нет % 24: после полуночи получается 24 часа",
                _change(METRO, 'hour = (clock / 60) % 24;', 'hour = clock / 60;')),
               ("минуты просто сложены: может получиться больше 60 минут",
                _change(_change(METRO, 'hour = (clock / 60) % 24;', ''), 'minute = clock % 60;', 'minute += travel;')),
               ("-- вместо ++: минута на турникет отнимается",
                _change(METRO, 'travel++;', 'travel--;'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att9-train", title="Вагон и место в поезде",
        given=[("String", "city"), ("int", "km"), ("int", "seat"), ("int", "seatsPerCar")],
        variants=[{"city": '"Kazan"', "km": "815", "seat": "47", "seatsPerCar": "36"}],
        hidden=[{"city": '"Sochi"', "km": "1620", "seat": "36", "seatsPerCar": "36"},
                {"city": '"Omsk"', "km": "2700", "seat": "1", "seatsPerCar": "54"},
                {"city": '"Tula"', "km": "180", "seat": "109", "seatsPerCar": "54"},
                {"city": '"Perm"', "km": "1387", "seat": "73", "seatsPerCar": "36"}],
        intro="Борис покупает студенческий билет на поезд в город `city`, ехать `km` километров. В каждом вагоне "
              "`seatsPerCar` мест, а места пронумерованы подряд через весь поезд, начиная с 1: у Бориса общий номер "
              "места `seat`. Билет стоит 1.5 рубля за километр плюс 150 рублей за постельное бельё, а студент платит "
              "половину.",
        steps=["Считать удобнее с нуля: уменьши `seat` на один операцией `--`.",
               "Заведи `int car = seat / seatsPerCar + 1;` — номер вагона и `int place = seat % seatsPerCar + 1;` — "
               "номер места в вагоне.",
               "Заведи `String code` — код билета: первые три буквы города заглавными (`substring` и `toUpperCase()`), "
               "дефис, номер вагона, дефис, место. Например, для Kazan, вагона 2 и места 11 — `KAZ-2-11`.",
               "Заведи `double price = km * 1.5;`, прибавь 150 рублей за бельё операцией `+=`, а потом раздели цену "
               "на `2` операцией `/=`.",
               "Выведи три строки: `Car: `, вагон, `, seat: ` и место; `Ticket: ` и код; `Price: `, цена и ` rub`."],
        hint="Без `seat--` последнее место вагона (например, 36-е при 36 местах) попало бы в следующий вагон. "
             "Скидка студента считается от цены вместе с бельём, поэтому `/=` идёт после `+=`.",
        solution=TRAIN,
        wrong=[("забыт seat--: последнее место вагона уходит в следующий вагон",
                _change(TRAIN, 'seat--;', '')),
               ("скидка до белья: бельё оплачивается полностью",
                TRAIN.replace('price += 150;\nprice /= 2;', 'price /= 2;\nprice += 150;'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att9-parking", title="Оплата городской парковки",
        given=[("String", "plate"), ("int", "minutes"), ("int", "hourPrice"), ("int", "minutePrice")],
        variants=[{"plate": '"A123BC77"', "minutes": "135", "hourPrice": "200", "minutePrice": "4"}],
        hidden=[{"plate": '"K777OP177"', "minutes": "60", "hourPrice": "150", "minutePrice": "3"},
                {"plate": '"M001AA05"', "minutes": "59", "hourPrice": "300", "minutePrice": "5"},
                {"plate": '"E555KX99"', "minutes": "0", "hourPrice": "100", "minutePrice": "2"},
                {"plate": '"T808TT116"', "minutes": "241", "hourPrice": "100", "minutePrice": "2"}],
        intro="Машина с номером `plate` простояла на городской парковке `minutes` минут. Первые шесть символов номера — "
              "сам номер, остальные — код региона. Каждый полный час стоит `hourPrice` рублей, оставшиеся минуты — "
              "по `minutePrice` рублей за минуту. У водителя карта жителя, и он платит только 75 процентов стоимости.",
        steps=["Заведи `String number = plate.substring(0, 6);` и `String region = plate.substring(6);`.",
               "Заведи `int hours = minutes / 60;` — полные часы и `int rest = minutes % 60;` — оставшиеся минуты.",
               "Заведи `int cost = hours * hourPrice;` и прибавь оплату оставшихся минут (`rest * minutePrice`) "
               "операцией `+=`.",
               "Заведи `double total = cost * 0.75;` — сколько платит житель.",
               "Выведи три строки: `Car: `, номер, `, region ` и регион; `Parked: `, часы, ` h `, минуты и ` min`; "
               "`Cost: `, стоимость, ` rub, to pay: `, сумма к оплате и ` rub`."],
        hint="`plate.substring(6)` берёт всё с седьмого символа (номер 6) до конца строки — так регион из двух и из "
             "трёх цифр берётся одинаково. `minutes % 60` — минуты, которые не сложились в полный час.",
        solution=PARKING,
        wrong=[("житель платит 25 процентов вместо 75: скидка перепутана с оплатой",
                _change(PARKING, 'double total = cost * 0.75;', 'double total = cost * 0.25;')),
               ("=+ вместо +=: оплата полных часов теряется",
                _change(PARKING, 'cost += rest * minutePrice;', 'cost =+ rest * minutePrice;'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att9-scooter", title="Поездка на электросамокате",
        given=[("String", "login"), ("int", "minutes"), ("int", "meters"), ("int", "balance")],
        variants=[{"login": '"anna.petrova"', "minutes": "12", "meters": "2350", "balance": "500"}],
        hidden=[{"login": '"boris.ivanov"', "minutes": "0", "meters": "0", "balance": "50"},
                {"login": '"lena.k"', "minutes": "30", "meters": "5000", "balance": "1000"},
                {"login": '"max.orlov"', "minutes": "5", "meters": "499", "balance": "300"},
                {"login": '"oleg.smirnov"', "minutes": "45", "meters": "8125", "balance": "2000"}],
        intro="Пользователь с логином `login` взял электросамокат и проехал `meters` метров за `minutes` минут. Старт "
              "стоит 50 рублей, каждая минута — 7 рублей, деньги списываются с баланса `balance`. За каждые полные "
              "500 метров начисляется бонусный балл.",
        steps=["Имя пользователя — часть логина до точки: заведи `String name = login.substring(0, login.indexOf(\".\"));`.",
               "Заведи `int cost = 50;`, прибавь `minutes * 7` операцией `+=` и спиши `cost` с `balance` операцией `-=`.",
               "Заведи `double km = meters / 1000.0;` — расстояние в километрах с дробной частью.",
               "Заведи `int points = meters / 500;` — баллы и `int toNext = 500 - meters % 500;` — сколько метров "
               "осталось проехать до следующего балла.",
               "Выведи четыре строки: `Hi, `, имя и `!`; `Distance: `, километры, ` km, cost: `, стоимость и ` rub`; "
               "`Balance: `, баланс и ` rub`; `Points: `, баллы, `, next in `, остаток метров и ` m`."],
        hint="`meters / 1000` с двумя целыми числами отбросит дробную часть, а `meters / 1000.0` — нет: одно из чисел "
             "дробное, и деление тоже дробное.",
        solution=SCOOTER,
        wrong=[("деление на 1000 без .0: километры без дробной части",
                _change(SCOOTER, 'double km = meters / 1000.0;', 'double km = meters / 1000;')),
               ("+= вместо -=: стоимость прибавляется к балансу",
                _change(SCOOTER, 'balance -= cost;', 'balance += cost;')),
               ("до следующего балла выведен остаток, а не сколько осталось",
                _change(SCOOTER, 'int toNext = 500 - meters % 500;', 'int toNext = meters % 500;'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att9-museum-tour", title="Автобусы на экскурсию",
        given=[("String", "museum"), ("int", "tourists"), ("int", "seats"), ("int", "ticket")],
        variants=[{"museum": '"Hermitage"', "tourists": "60", "seats": "25", "ticket": "500"}],
        hidden=[{"museum": '"Kremlin"', "tourists": "49", "seats": "25", "ticket": "700"},
                {"museum": '"Planetarium"', "tourists": "12", "seats": "18", "ticket": "350"},
                {"museum": '"Zoo"', "tourists": "89", "seats": "45", "ticket": "400"},
                {"museum": '"Darwin"', "tourists": "100", "seats": "30", "ticket": "250"}],
        intro="Турагентство везёт `tourists` туристов в музей `museum`, билет стоит `ticket` рублей с человека. Для "
              "автобуса заказывают табличку с названием музея: каждая буква стоит 30 рублей. С группой едет гид: "
              "за билет он не платит, но место в транспорте занимает. В автобусе `seats` мест; полные автобусы "
              "заполняются целиком, а кто не поместился, едет на минивэне. Гиду агентство платит 12.5 процента выручки.",
        steps=["Заведи `int total = tourists * ticket;` — выручка за билеты, и прибавь стоимость таблички "
               "(`museum.length() * 30`) операцией `+=`.",
               "Только после этого добавь к `tourists` гида операцией `++`.",
               "Заведи `int buses = tourists / seats;` — полные автобусы и `int minivan = tourists % seats;` — сколько "
               "человек едет на минивэне.",
               "Заведи `double guide = total * 0.125;` — оплата гида.",
               "Выведи три строки: `Tour to `, название музея, `: `, число людей вместе с гидом и ` people`; `Buses: `, "
               "автобусы, `, minivan: ` и люди в минивэне; `Total: `, выручка, ` rub, guide: `, оплата гида и ` rub`."],
        hint="Порядок важен: выручка считается, пока гида ещё нет в `tourists`, а места в транспорте — когда он уже "
             "добавлен. `museum.length()` — число букв в названии.",
        solution=TOUR,
        wrong=[("гид добавлен до подсчёта выручки: он платит за билет",
                _change(_change(TOUR, 'tourists++;', ''), 'int total = tourists * ticket;', 'tourists++;\nint total = tourists * ticket;')),
               ("минивэн посчитан делением, а не остатком",
                _change(TOUR, 'int minivan = tourists % seats;', 'int minivan = tourists / seats;'))],
        constructs=["augmented_assignment"],
    ),
]
