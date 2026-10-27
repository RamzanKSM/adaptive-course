"""Attestation, Java, topics 1–12 (up to LOGICAL_AND): println, variables, assignment, arithmetic, execution order,
primitive types (double, char, boolean, an (int) cast), String (+, toUpperCase/toLowerCase, charAt, substring),
/ and %, += -= *= /= ++, if/else, comparison operators, &&. Theme: sports and fitness — every story is different.
Each reference solution uses every topic once in a natural way; hidden value sets hit both sides of every part of
the && condition and its boundaries. Not yet: || and !, switch, loops, arrays, own methods and classes, equals."""
import textwrap

from java_tasks import JavaOutputTask

SKILL = "LOGICAL_AND"


def code(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


def swap(text: str, old: str, new: str) -> str:
    assert old in text, old
    return text.replace(old, new)


RUN = code("""
    String name = runner.toUpperCase();
    int minutes = seconds / 60;
    int rest = seconds % 60;
    double km = meters / 1000.0;
    int fullKm = (int) km;
    int points = fullKm * 10;
    String badge = "";
    if (fullKm >= 5 && minutes < 30) {
        badge = "fast five";
        points += 50;
    } else {
        badge = "keep training";
    }
    System.out.println("Runner: " + name);
    System.out.println("Time: " + minutes + " min " + rest + " sec");
    System.out.println("Full km: " + fullKm);
    System.out.println("Badge: " + badge);
    System.out.println("Points: " + points);
""")

POOL = code("""
    int distance = laps * poolLength;
    int km = distance / 1000;
    int m = distance % 1000;
    char letter = swimmer.charAt(0);
    int tokens = laps / 4;
    String challenge = "";
    if (distance >= 1000 && poolLength == 50) {
        challenge = "done";
        tokens += 5;
    } else {
        challenge = "open";
    }
    System.out.println("Card: " + letter + "-" + laps);
    System.out.println("Distance: " + km + " km " + m + " m");
    System.out.println("Challenge: " + challenge);
    System.out.println("Tokens: " + tokens);
""")

GYM = code("""
    int perSide = (target - 20) / 2;
    int plates = perSide / 10;
    int extra = perSide % 10;
    int percent = (int) (target * 100 / bodyWeight);
    int volume = target;
    volume *= reps;
    String level = "";
    if (percent >= 100 && reps >= 5) {
        level = "strong";
    } else {
        level = "growing";
    }
    System.out.println("Lifter: " + lifter.toUpperCase());
    System.out.println("Each side: " + plates + " x 10 kg + " + extra + " kg");
    System.out.println("Of body weight: " + percent + "%");
    System.out.println("Volume: " + volume + " kg");
    System.out.println("Level: " + level);
""")

BAND = code("""
    int percent = steps * 100 / goal;
    int toNext = 1000 - steps % 1000;
    char grade = 'B';
    if (steps >= goal && activeMinutes >= 30) {
        grade = 'A';
        streak++;
    } else {
        streak = 0;
    }
    System.out.println("Band: " + owner.toLowerCase());
    System.out.println("Goal: " + percent + "%");
    System.out.println("Next thousand in: " + toNext + " steps");
    System.out.println("Grade: " + grade);
    System.out.println("Streak: " + streak + " days");
""")

BIKE = code("""
    String tag = rider.substring(0, 3).toUpperCase();
    int hours = minutes / 60;
    int rest = minutes % 60;
    int speed = km * 60 / minutes;
    double kcal = minutes * 8.5;
    int badges = km / 10;
    String zone = "";
    if (pulse >= 120 && pulse <= 150) {
        zone = "fat burning";
        badges += 2;
    } else {
        zone = "out of zone";
    }
    System.out.println(tag + ": " + km + " km in " + hours + " h " + rest + " min");
    System.out.println("Speed: " + speed + " km/h");
    System.out.println("Calories: " + kcal);
    System.out.println("Zone: " + zone);
    System.out.println("Badges: " + badges);
""")

KEEPER = code("""
    int percent = saves * 100 / shots;
    double rating = percent / 10.0;
    int missed = shots - saves;
    int pushUps = missed * 10;
    String status = "";
    if (percent >= 80 && shots >= 20) {
        status = "ready for the match";
        pushUps /= 2;
    } else {
        status = "more practice";
    }
    System.out.println("Shirt: " + keeper.toUpperCase());
    System.out.println("Saves: " + saves + " of " + shots + " (" + percent + "%)");
    System.out.println("Rating: " + rating);
    System.out.println("Push-ups: " + pushUps);
    System.out.println("Status: " + status);
""")

BASKET = code("""
    int points = twos * 2;
    points += threes * 3;
    double perQuarter = points / 4.0;
    int made = twos + threes;
    int accuracy = made * 100 / attempts;
    String result = "";
    if (points >= 10 && rebounds >= 10) {
        result = "double-double";
    } else {
        result = "regular game";
    }
    System.out.println("Player: " + player + " (" + player.charAt(0) + ")");
    System.out.println("Points: " + points);
    System.out.println("Per quarter: " + perQuarter);
    System.out.println("Accuracy: " + accuracy + "%");
    System.out.println("Result: " + result);
""")

CLUB = code("""
    String card = member.substring(0, 2).toUpperCase() + "-" + months;
    int price = months * 2500;
    int discount;
    if (student && age <= 23) {
        discount = price / 5;
    } else {
        discount = 0;
    }
    int pay = price;
    pay -= discount;
    int perMonth = pay / months;
    int sessions = months * 12;
    System.out.println("Card: " + card);
    System.out.println("Price: " + price + " rub");
    System.out.println("Discount: " + discount + " rub");
    System.out.println("To pay: " + pay + " rub");
    System.out.println("Per month: " + perMonth + " rub, per session: " + pay / sessions + " rub");
""")

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att12-run", title="Утренняя пробежка",
        given=[("String", "runner"), ("int", "meters"), ("int", "seconds")],
        variants=[{"runner": '"Anya"', "meters": "5400", "seconds": "1625"}],
        hidden=[{"runner": '"Boris"', "meters": "4999", "seconds": "1500"},
                {"runner": '"Dima"', "meters": "5000", "seconds": "1799"},
                {"runner": '"Lena"', "meters": "5000", "seconds": "1800"},
                {"runner": '"Oleg"', "meters": "10250", "seconds": "3000"},
                {"runner": '"Kira"', "meters": "7300", "seconds": "1740"}],
        intro="Беговое приложение подводит итог пробежки. Имя бегуна записано в поле `runner`, дистанция в метрах — "
              "в поле `meters`, время пробежки в секундах — в поле `seconds`.",
        steps=["Сохрани имя бегуна большими буквами: `runner.toUpperCase()`.",
               "Посчитай полные минуты (`seconds / 60`) и оставшиеся секунды (`seconds % 60`).",
               "Запиши дистанцию в километрах в переменную типа `double`: `meters / 1000.0`. Число полных "
               "километров получи из неё приведением `(int)`.",
               "Очки: по 10 за каждый полный километр.",
               "Если полных километров не меньше 5 **и** полных минут меньше 30, значок — `fast five`, и к очкам "
               "прибавь 50 через `+=`. Иначе значок — `keep training`. Обе проверки — в одном условии через `&&`.",
               "Выведи пять строк: `Runner: …` (имя большими буквами), `Time: … min … sec`, `Full km: …`, "
               "`Badge: …`, `Points: …`."],
        hint="`meters / 1000.0` даёт дробное число, а `(int)` отбрасывает дробную часть: из 5.4 получится 5. "
             "Ровно 30 минут — это уже не быстрее 30.",
        solution=RUN,
        wrong=[("<= 30 вместо < 30: ровно 30 минут засчитывается как быстрый забег",
                swap(RUN, "minutes < 30", "minutes <= 30")),
               ("|| вместо &&: значок дают за любую быструю или любую длинную пробежку",
                swap(RUN, "fullKm >= 5 && minutes < 30", "fullKm >= 5 || minutes < 30")),
               ("минуты и секунды перепутаны местами", swap(RUN, "int minutes = seconds / 60;\nint rest = seconds % 60;",
                                                           "int minutes = seconds % 60;\nint rest = seconds / 60;"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att12-pool", title="Километр в бассейне",
        given=[("String", "swimmer"), ("int", "laps"), ("int", "poolLength")],
        variants=[{"swimmer": '"Marat"', "laps": "26", "poolLength": "50"}],
        hidden=[{"swimmer": '"Vera"', "laps": "20", "poolLength": "50"},
                {"swimmer": '"Ilya"', "laps": "40", "poolLength": "25"},
                {"swimmer": '"Zoya"', "laps": "19", "poolLength": "50"},
                {"swimmer": '"Timur"', "laps": "80", "poolLength": "25"},
                {"swimmer": '"Nina"', "laps": "61", "poolLength": "50"}],
        intro="В клубе плавания идёт челлендж «километр в большом бассейне». Имя пловца записано в поле `swimmer`, "
              "сколько бассейнов он проплыл — в поле `laps`, длина бассейна в метрах (25 или 50) — в поле `poolLength`.",
        steps=["Посчитай всю дистанцию в метрах: `laps * poolLength`.",
               "Раздели её на полные километры (`/ 1000`) и оставшиеся метры (`% 1000`).",
               "Сохрани первую букву имени в переменную типа `char`: `swimmer.charAt(0)`.",
               "Жетоны: по одному за каждые 4 полных бассейна (`laps / 4`).",
               "Если дистанция не меньше 1000 м **и** бассейн 50-метровый, челлендж — `done`, и к жетонам прибавь "
               "5 через `+=`. Иначе челлендж — `open`. Обе проверки — в одном условии через `&&`.",
               "Выведи четыре строки: `Card: …-…` (буква и число бассейнов через дефис), `Distance: … km … m`, "
               "`Challenge: …`, `Tokens: …`."],
        hint="Равенство в Java проверяется двумя знаками: `poolLength == 50`. Ровно 1000 м челлендж уже засчитывает.",
        solution=POOL,
        wrong=[("> 1000 вместо >= 1000: ровно километр не засчитывается",
                swap(POOL, "distance >= 1000", "distance > 1000")),
               ("|| вместо &&: челлендж засчитан и в 25-метровом бассейне",
                swap(POOL, "distance >= 1000 && poolLength == 50", "distance >= 1000 || poolLength == 50")),
               ("километры через / 100: получаются сотни метров",
                swap(POOL, "int km = distance / 1000;", "int km = distance / 100;"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att12-gym", title="Штанга в зале",
        given=[("String", "lifter"), ("int", "target"), ("int", "reps"), ("double", "bodyWeight")],
        variants=[{"lifter": '"Boris"', "target": "90", "reps": "5", "bodyWeight": "80.0"}],
        hidden=[{"lifter": '"Anya"', "target": "60", "reps": "8", "bodyWeight": "62.5"},
                {"lifter": '"Gleb"', "target": "80", "reps": "5", "bodyWeight": "80.0"},
                {"lifter": '"Petr"', "target": "100", "reps": "4", "bodyWeight": "75.5"},
                {"lifter": '"Sasha"', "target": "70", "reps": "6", "bodyWeight": "70.5"},
                {"lifter": '"Ivan"', "target": "120", "reps": "10", "bodyWeight": "90.0"}],
        intro="Тренер собирает штангу и записывает подход в дневник. Имя спортсмена — в поле `lifter`, вес штанги "
              "в килограммах — в поле `target`, сколько раз он её поднял — в поле `reps`, вес самого спортсмена — "
              "в дробном поле `bodyWeight`. Гриф весит 20 кг, блины по 10 кг.",
        steps=["Посчитай, сколько килограммов вешать на каждую сторону грифа: `(target - 20) / 2`.",
               "Раздели это на блины по 10 кг (`/ 10`) и остаток в килограммах (`% 10`).",
               "Посчитай, сколько процентов от веса спортсмена составляет штанга: `target * 100 / bodyWeight` — это "
               "дробное число, приведи его к `int` через `(int)` (скобки вокруг всего выражения).",
               "Объём подхода: заведи переменную `volume`, равную `target`, и умножь её на `reps` через `*=`.",
               "Если процент не меньше 100 **и** повторов не меньше 5, уровень — `strong`, иначе — `growing`. "
               "Обе проверки — в одном условии через `&&`.",
               "Выведи пять строк: `Lifter: …` (имя большими буквами), `Each side: … x 10 kg + … kg`, "
               "`Of body weight: …%`, `Volume: … kg`, `Level: …`."],
        hint="Приведение `(int)` отбрасывает дробную часть, не округляя: 99.9 станет 99. Штанга ровно в свой вес — "
             "это уже 100 процентов.",
        solution=GYM,
        wrong=[("> 100 вместо >= 100: штанга ровно в свой вес не считается",
                swap(GYM, "percent >= 100", "percent > 100")),
               ("> 5 вместо >= 5: пять повторов не засчитываются", swap(GYM, "reps >= 5", "reps > 5")),
               ("блины и остаток перепутаны", swap(GYM, "int plates = perSide / 10;\nint extra = perSide % 10;",
                                                   "int plates = perSide % 10;\nint extra = perSide / 10;"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att12-band", title="Фитнес-браслет",
        given=[("String", "owner"), ("int", "steps"), ("int", "goal"), ("int", "activeMinutes"), ("int", "streak")],
        variants=[{"owner": '"Lena"', "steps": "10450", "goal": "10000", "activeMinutes": "42", "streak": "4"}],
        hidden=[{"owner": '"Max"', "steps": "10000", "goal": "10000", "activeMinutes": "30", "streak": "0"},
                {"owner": '"Ira"', "steps": "9999", "goal": "10000", "activeMinutes": "60", "streak": "7"},
                {"owner": '"Egor"', "steps": "15000", "goal": "12000", "activeMinutes": "29", "streak": "3"},
                {"owner": '"Ulyana"', "steps": "12500", "goal": "8000", "activeMinutes": "31", "streak": "10"}],
        intro="Вечером фитнес-браслет подводит итог дня. Имя владельца записано в поле `owner`, шаги за день — в поле "
              "`steps`, дневная цель по шагам — в поле `goal`, минуты активной нагрузки — в поле `activeMinutes`, "
              "сколько дней подряд цель уже выполнена — в поле `streak`.",
        steps=["Посчитай, сколько процентов цели пройдено: `steps * 100 / goal`.",
               "Посчитай, сколько шагов осталось до следующей тысячи: 1000 минус остаток от деления `steps` на 1000.",
               "Заведи переменную типа `char` для оценки дня со значением `'B'`.",
               "Если шагов не меньше цели **и** активных минут не меньше 30, оценка становится `'A'`, а `streak` "
               "увеличь на 1 через `++`. Иначе серия обрывается: присвой `streak` значение 0. Обе проверки — "
               "в одном условии через `&&`.",
               "Выведи пять строк: `Band: …` (имя маленькими буквами), `Goal: …%`, `Next thousand in: … steps`, "
               "`Grade: …`, `Streak: … days`."],
        hint="Символ типа `char` пишется в одинарных кавычках: `'A'`. Поле `streak` можно менять, как обычную "
             "переменную. Если шагов ровно 10000, до следующей тысячи остаётся 1000.",
        solution=BAND,
        wrong=[("> 30 вместо >= 30: ровно 30 активных минут не засчитываются",
                swap(BAND, "activeMinutes >= 30", "activeMinutes > 30")),
               ("серия не обрывается: нет streak = 0 в ветке else",
                swap(BAND, "} else {\n    streak = 0;\n}", "}")),
               ("|| вместо &&: оценка A и за одни только шаги",
                swap(BAND, "steps >= goal && activeMinutes", "steps >= goal || activeMinutes"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att12-bike", title="Велотренировка",
        given=[("String", "rider"), ("int", "km"), ("int", "minutes"), ("int", "pulse")],
        variants=[{"rider": '"Nikita"', "km": "38", "minutes": "95", "pulse": "135"}],
        hidden=[{"rider": '"Alina"', "km": "20", "minutes": "60", "pulse": "120"},
                {"rider": '"Roman"', "km": "45", "minutes": "120", "pulse": "150"},
                {"rider": '"Sofia"', "km": "31", "minutes": "70", "pulse": "151"},
                {"rider": '"Daniil"', "km": "12", "minutes": "45", "pulse": "119"}],
        intro="Велокомпьютер показывает итог тренировки. Имя велосипедиста записано в поле `rider`, проехано "
              "километров — в поле `km`, время в минутах — в поле `minutes`, средний пульс — в поле `pulse`.",
        steps=["Сделай метку для таблицы: первые три буквы имени большими буквами — `rider.substring(0, 3)`, "
               "а затем `toUpperCase()`.",
               "Раздели время на полные часы (`/ 60`) и оставшиеся минуты (`% 60`).",
               "Средняя скорость в км/ч — целое число: `km * 60 / minutes`.",
               "Калории — дробное число типа `double`: по 8.5 ккал за минуту.",
               "Значки: по одному за каждые 10 полных километров. Если пульс не меньше 120 **и** не больше 150, "
               "зона — `fat burning`, и к значкам прибавь 2 через `+=`. Иначе зона — `out of zone`. Обе проверки — "
               "в одном условии через `&&`.",
               "Выведи пять строк: `…: … km in … h … min` (в начале метка), `Speed: … km/h`, `Calories: …`, "
               "`Zone: …`, `Badges: …`."],
        hint="Число типа `double` печатается с точкой, даже если оно целое: `510.0`. Пульс ровно 120 и ровно 150 "
             "ещё в зоне.",
        solution=BIKE,
        wrong=[("строгие сравнения: пульс ровно 120 или 150 вне зоны",
                swap(BIKE, "pulse >= 120 && pulse <= 150", "pulse > 120 && pulse < 150")),
               ("|| вместо &&: в зоне оказывается любой пульс",
                swap(BIKE, "pulse >= 120 && pulse <= 150", "pulse >= 120 || pulse <= 150")),
               ("скорость km / minutes * 60: целое деление до умножения даёт 0",
                swap(BIKE, "km * 60 / minutes", "km / minutes * 60"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att12-keeper", title="Тренировка вратаря",
        given=[("String", "keeper"), ("int", "shots"), ("int", "saves")],
        variants=[{"keeper": '"Sergey"', "shots": "20", "saves": "17"}],
        hidden=[{"keeper": '"Artem"', "shots": "19", "saves": "18"},
                {"keeper": '"Kolya"', "shots": "25", "saves": "20"},
                {"keeper": '"Pasha"', "shots": "30", "saves": "23"},
                {"keeper": '"Gosha"', "shots": "40", "saves": "40"},
                {"keeper": '"Mira"', "shots": "20", "saves": "15"}],
        intro="На тренировке по вратарю футбольной команды бьют пенальти. Имя вратаря записано в поле `keeper`, "
              "сколько было ударов — в поле `shots`, сколько из них он отбил — в поле `saves`.",
        steps=["Посчитай процент отбитых ударов целым числом: `saves * 100 / shots`.",
               "Рейтинг — дробное число типа `double`: процент, делённый на `10.0`.",
               "Посчитай пропущенные мячи (удары минус отбитые); за каждый пропущенный — 10 отжиманий.",
               "Если процент не меньше 80 **и** ударов было не меньше 20, статус — `ready for the match`, а отжиманий "
               "становится вдвое меньше: раздели их на 2 через `/=`. Иначе статус — `more practice`. Обе проверки — "
               "в одном условии через `&&`.",
               "Выведи пять строк: `Shirt: …` (имя большими буквами), `Saves: … of … (…%)`, `Rating: …`, "
               "`Push-ups: …`, `Status: …`."],
        hint="Порядок важен: `saves / shots * 100` при делении целых сначала даст 0. Ровно 80 процентов уже хватает.",
        solution=KEEPER,
        wrong=[("> 80 вместо >= 80: ровно 80 процентов не хватает",
                swap(KEEPER, "percent >= 80", "percent > 80")),
               ("> 20 вместо >= 20: ровно 20 ударов не хватает", swap(KEEPER, "shots >= 20", "shots > 20")),
               ("saves / shots * 100: целое деление сначала даёт 0",
                swap(KEEPER, "saves * 100 / shots", "saves / shots * 100"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att12-basket", title="Статистика баскетболистки",
        given=[("String", "player"), ("int", "twos"), ("int", "threes"), ("int", "attempts"), ("int", "rebounds")],
        variants=[{"player": '"Kira"', "twos": "7", "threes": "3", "attempts": "18", "rebounds": "11"}],
        hidden=[{"player": '"Liza"', "twos": "5", "threes": "0", "attempts": "12", "rebounds": "10"},
                {"player": '"Vika"', "twos": "3", "threes": "1", "attempts": "9", "rebounds": "15"},
                {"player": '"Olya"', "twos": "8", "threes": "4", "attempts": "20", "rebounds": "9"},
                {"player": '"Dasha"', "twos": "0", "threes": "0", "attempts": "4", "rebounds": "2"},
                {"player": '"Masha"', "twos": "10", "threes": "2", "attempts": "15", "rebounds": "12"}],
        intro="После матча тренер заполняет карточку баскетболистки. Её имя записано в поле `player`, попадания "
              "за 2 очка — в поле `twos`, за 3 очка — в поле `threes`, все броски с игры — в поле `attempts`, "
              "подборы — в поле `rebounds`.",
        steps=["Заведи `points`, равную очкам за двухочковые (`twos * 2`), затем прибавь очки за трёхочковые через `+=`.",
               "Очки за четверть — дробное число типа `double`: `points / 4.0` (в матче 4 четверти).",
               "Точность бросков в процентах — целое число: попадания (`twos + threes`) умножь на 100 и раздели "
               "на `attempts`.",
               "Если очков не меньше 10 **и** подборов не меньше 10, результат — `double-double`, иначе — "
               "`regular game`. Обе проверки — в одном условии через `&&`.",
               "Выведи пять строк: `Player: … (…)` (имя и в скобках его первая буква), `Points: …`, "
               "`Per quarter: …`, `Accuracy: …%`, `Result: …`."],
        hint="`points / 4` делит целые числа и теряет дробную часть, а `points / 4.0` даёт `5.75`. Первая буква — "
             "`player.charAt(0)`.",
        solution=BASKET,
        wrong=[("> 10 вместо >= 10: ровно 10 очков не засчитываются",
                swap(BASKET, "points >= 10", "points > 10")),
               ("points / 4: целое деление теряет дробную часть",
                swap(BASKET, "points / 4.0", "points / 4")),
               ("|| вместо &&: хватает одних очков или одних подборов",
                swap(BASKET, "points >= 10 && rebounds", "points >= 10 || rebounds"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-att12-club", title="Абонемент в фитнес-клуб",
        given=[("String", "member"), ("int", "months"), ("boolean", "student"), ("int", "age")],
        variants=[{"member": '"Anton"', "months": "6", "student": "true", "age": "19"}],
        hidden=[{"member": '"Ksenia"', "months": "3", "student": "true", "age": "23"},
                {"member": '"Lev"', "months": "12", "student": "true", "age": "24"},
                {"member": '"Polina"', "months": "1", "student": "false", "age": "18"},
                {"member": '"Denis"', "months": "7", "student": "true", "age": "20"},
                {"member": '"Rita"', "months": "5", "student": "false", "age": "30"}],
        intro="Администратор фитнес-клуба оформляет абонемент. Имя клиента записано в поле `member`, на сколько "
              "месяцев абонемент — в поле `months`, студент ли клиент — в поле `student` (`true` или `false`), "
              "возраст — в поле `age`. Месяц стоит 2500 руб., в месяц 12 тренировок.",
        steps=["Номер карты: первые две буквы имени большими буквами, дефис и число месяцев — например, `AN-6`.",
               "Посчитай цену: месяцы умножь на 2500.",
               "Скидка: если клиент студент **и** ему не больше 23 лет, она равна пятой части цены "
               "(`price / 5`), иначе 0. Обе проверки — в одном условии через `&&`.",
               "К оплате: заведи `pay`, равную цене, и вычти из неё скидку через `-=`.",
               "Посчитай, сколько это в месяц (`pay / months`) и за одну тренировку (`pay` делить на число всех "
               "тренировок, целым делением).",
               "Выведи пять строк: `Card: …`, `Price: … rub`, `Discount: … rub`, `To pay: … rub`, "
               "`Per month: … rub, per session: … rub`."],
        hint="Поле типа `boolean` само является условием: `student && …`. В 23 года скидка ещё положена. "
             "Первые две буквы — `member.substring(0, 2)`.",
        solution=CLUB,
        wrong=[("< 23 вместо <= 23: в 23 года скидку не дают", swap(CLUB, "age <= 23", "age < 23")),
               ("не проверяет, студент ли клиент: скидка всем молодым",
                swap(CLUB, "student && age <= 23", "age <= 23")),
               ("скидка вычтена из самой цены: в строке Price уже сумма со скидкой",
                swap(CLUB, "int pay = price;", "price -= discount;\nint pay = price;"))],
        constructs=["if"],
    ),
]
