"""Training attestation («Тренировочная аттестация»), Java, topics 1–9 (up to ASSIGNMENT_OPERATORS): println, variables,
assignment, arithmetic, execution order, primitive types (double, an (int) cast), String (+, substring, indexOf,
toUpperCase), / and %, += -= %= ++. One integrative story per family, theme: home, household and chores; the stories are
new, not those of the real attestation pool (attestation/java_k09.py).
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


PLANTS = _code(
    'neighbour = neighbour.substring(0, neighbour.indexOf(" "));',
    'int visits = days / every;',
    'visits++;',
    'int water = visits * plants * portion;',
    'double liters = water / 1000.0;',
    'int cans = water / 2000;',
    'int rest = water % 2000;',
    'System.out.println("Dear " + neighbour + ", please water " + plants + " plants " + visits + " times");',
    'System.out.println("Total water: " + liters + " l");',
    'System.out.println("Full cans: " + cans + ", plus " + rest + " ml");')

POWER = _code(
    'String code = month.substring(0, 3).toUpperCase();',
    'int used = current - previous;',
    'used += 15;',
    'previous = current;',
    'int kopecks = used * tariff;',
    'int rub = kopecks / 100;',
    'kopecks %= 100;',
    'double price = tariff / 100.0;',
    'System.out.println("Bill for " + code + ": " + used + " kWh");',
    'System.out.println("Price: " + price + " rub per kWh");',
    'System.out.println("To pay: " + rub + " rub " + kopecks + " kop");',
    'System.out.println("Saved reading: " + previous);')

CHORES = _code(
    'String name = kid.substring(0, 1).toUpperCase() + kid.substring(1);',
    'int points = dishes * 4 + trash * 3;',
    'points -= reminders * 2;',
    'points = (int) (points * 1.5);',
    'System.out.println(name + ": " + points + " points for the week");',
    'points += saved;',
    'int hours = points / 20;',
    'points %= 20;',
    'System.out.println("Games: " + hours + " h, points left: " + points);')

LAUNDRY = _code(
    'String fabric = tag.substring(0, tag.indexOf("-")).toUpperCase();',
    'String degrees = tag.substring(tag.indexOf("-") + 1);',
    'int loads = kg / drum;',
    'int rest = kg % drum;',
    'loads++;',
    'int minutes = loads * (cycle + 10);',
    'int hours = minutes / 60;',
    'minutes %= 60;',
    'double caps = loads * 1.5;',
    'System.out.println(fabric + ", " + degrees + " C");',
    'System.out.println("Loads: " + loads + ", waiting: " + rest + " kg");',
    'System.out.println("Time: " + hours + " h " + minutes + " min");',
    'System.out.println("Powder: " + caps + " caps");')

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac9-plants", title="Цветы на время отпуска",
        given=[("String", "neighbour"), ("int", "days"), ("int", "every"), ("int", "plants"), ("int", "portion")],
        variants=[{"neighbour": '"Olga Ivanova"', "days": "14", "every": "3", "plants": "7", "portion": "250"}],
        hidden=[{"neighbour": '"Boris Petrov"', "days": "10", "every": "2", "plants": "4", "portion": "500"},
                {"neighbour": '"Lena Smirnova"', "days": "2", "every": "3", "plants": "2", "portion": "300"},
                {"neighbour": '"Maxim Orlov"', "days": "21", "every": "1", "plants": "12", "portion": "150"},
                {"neighbour": '"Vera Kim"', "days": "30", "every": "7", "plants": "9", "portion": "200"}],
        intro="Семья уезжает в отпуск на `days` дней, а `plants` цветов в квартире будет поливать соседка — в телефоне "
              "она записана именем и фамилией: `neighbour`. Соседка придёт в первый же день, а потом будет приходить "
              "раз в `every` дней. За один приход каждый цветок получает `portion` мл воды, а лейка у соседки на "
              "2 литра (2000 мл). Оставь ей записку.",
        steps=["В записке нужно только имя: запиши в `neighbour` часть строки до пробела — "
               "`neighbour.substring(0, neighbour.indexOf(\" \"))`.",
               "Заведи `int visits = days / every;` — сколько раз соседка придёт после первого дня, и добавь к `visits` "
               "первый приход операцией `++`.",
               "Только после этого заведи `int water` — сколько всего миллилитров воды уйдёт: приходы, умноженные на "
               "число цветов и на порцию. И `double liters = water / 1000.0;` — то же в литрах.",
               "Заведи `int cans = water / 2000;` — сколько полных леек и `int rest = water % 2000;` — сколько "
               "миллилитров ещё останется налить сверх них.",
               "Выведи три строки: `Dear `, имя, `, please water `, число цветов, ` plants `, число приходов и ` times`; "
               "`Total water: `, литры и ` l`; `Full cans: `, полные лейки, `, plus `, остаток и ` ml`."],
        hint="Конец в `substring` не включается, поэтому пробел в имя не попадёт. Первый приход нужно добавить до "
             "подсчёта воды — иначе вода на него не будет учтена.",
        solution=PLANTS,
        wrong=[("первый приход добавлен после подсчёта воды: вода на него не учтена",
                _change(_change(PLANTS, 'visits++;', ''), 'double liters = water / 1000.0;',
                        'visits++;\ndouble liters = water / 1000.0;')),
               ("литры посчитаны делением нацело: дробная часть пропала",
                _change(PLANTS, 'double liters = water / 1000.0;', 'double liters = water / 1000;')),
               ("от имени отрезана последняя буква: конец substring и так не включается",
                _change(PLANTS, 'neighbour = neighbour.substring(0, neighbour.indexOf(" "));',
                        'neighbour = neighbour.substring(0, neighbour.indexOf(" ") - 1);'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac9-power-bill", title="Счёт за электричество",
        given=[("String", "month"), ("int", "previous"), ("int", "current"), ("int", "tariff")],
        variants=[{"month": '"October"', "previous": "18452", "current": "18671", "tariff": "625"}],
        hidden=[{"month": '"March"', "previous": "5000", "current": "5000", "tariff": "600"},
                {"month": '"January"', "previous": "12034", "current": "12485", "tariff": "548"},
                {"month": '"July"', "previous": "30990", "current": "31075", "tariff": "703"},
                {"month": '"May"', "previous": "999", "current": "1350", "tariff": "597"}],
        intro="В конце месяца `month` мама снимает показания счётчика электричества: в прошлый раз он показывал "
              "`previous` кВт·ч, а сейчас — `current`. К расходу квартиры добавляются ещё 15 кВт·ч на общие нужды дома "
              "(лифт и свет в подъезде). Один кВт·ч стоит `tariff` копеек. В квитанции месяц пишется тремя заглавными "
              "буквами, а сумма — рублями и копейками.",
        steps=["Заведи `String code` — первые три буквы месяца заглавными (`substring` и `toUpperCase()`).",
               "Заведи `int used` — расход квартиры (новые показания минус прошлые) и прибавь к нему 15 кВт·ч на "
               "общие нужды операцией `+=`.",
               "Запомни показания для следующего месяца: запиши `current` в `previous`. Сделай это только после "
               "подсчёта расхода.",
               "Заведи `int kopecks = used * tariff;` — сумма в копейках, и `int rub = kopecks / 100;` — целые рубли. "
               "Потом оставь в `kopecks` только копейки операцией `%=`.",
               "Заведи `double price = tariff / 100.0;` — цена одного кВт·ч в рублях.",
               "Выведи четыре строки: `Bill for `, код месяца, `: `, расход и ` kWh`; `Price: `, цена и ` rub per kWh`; "
               "`To pay: `, рубли, ` rub `, копейки и ` kop`; `Saved reading: ` и `previous`."],
        hint="В рубле 100 копеек: `kopecks / 100` — целые рубли, а `kopecks % 100` — оставшиеся копейки. Рубли нужно "
             "посчитать до `%=`, пока в `kopecks` ещё вся сумма.",
        solution=POWER,
        wrong=[("показания перезаписаны до подсчёта расхода: остаются только 15 кВт·ч на общие нужды",
                _change(_change(POWER, 'previous = current;', ''), 'int used = current - previous;',
                        'previous = current;\nint used = current - previous;')),
               ("копейки оставлены раньше, чем посчитаны рубли: рублей получается 0",
                POWER.replace('int rub = kopecks / 100;\nkopecks %= 100;', 'kopecks %= 100;\nint rub = kopecks / 100;')),
               ("цена кВт·ч посчитана делением нацело: копейки в цене пропали",
                _change(POWER, 'double price = tariff / 100.0;', 'double price = tariff / 100;'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac9-chores", title="Баллы за домашние дела",
        given=[("String", "kid"), ("int", "dishes"), ("int", "trash"), ("int", "reminders"), ("int", "saved")],
        variants=[{"kid": '"dasha"', "dishes": "7", "trash": "5", "reminders": "3", "saved": "13"}],
        hidden=[{"kid": '"misha"', "dishes": "0", "trash": "0", "reminders": "0", "saved": "0"},
                {"kid": '"anya"', "dishes": "5", "trash": "0", "reminders": "0", "saved": "10"},
                {"kid": '"lev"', "dishes": "3", "trash": "2", "reminders": "1", "saved": "19"},
                {"kid": '"sonya"', "dishes": "10", "trash": "7", "reminders": "4", "saved": "5"},
                {"kid": '"timur"', "dishes": "2", "trash": "1", "reminders": "0", "saved": "0"}],
        intro="Мама ведёт таблицу домашних дел. За каждое мытьё посуды ребёнок получает 4 балла, за каждый вынос "
              "мусора — 3 балла, а за каждое напоминание «ты опять забыл» снимается 2 балла. В воскресенье бабушка "
              "увеличивает баллы за неделю в полтора раза (дробную часть отбрасывает), и только потом к ним "
              "добавляются `saved` баллов, оставшихся с прошлой недели. Каждые полные 20 баллов — час игр на "
              "приставке, а остаток переходит на следующую неделю. На этой неделе ребёнок по имени `kid` (в "
              "приложении имя записано маленькими буквами) мыл посуду `dishes` раз, выносил мусор `trash` раз, "
              "а напоминать ему пришлось `reminders` раз.",
        steps=["Заведи `String name` — имя с заглавной буквы: первую букву `kid.substring(0, 1)` сделай заглавной "
               "через `toUpperCase()` и приклей к ней остаток имени `kid.substring(1)`.",
               "Заведи `int points` — баллы за посуду и мусор (`dishes * 4 + trash * 3`) и отними штраф за "
               "напоминания (`reminders * 2`) операцией `-=`.",
               "Бонус бабушки: запиши в `points` значение `(int) (points * 1.5)` — приведение к `int` отбрасывает "
               "дробную часть. Выведи имя, `: `, баллы и ` points for the week`.",
               "Только теперь прибавь старые баллы `saved` операцией `+=` — бабушкин бонус на них не действует.",
               "Заведи `int hours = points / 20;` — часы игр, а в `points` оставь остаток для следующей недели "
               "операцией `%=`. Выведи `Games: `, часы, ` h, points left: ` и остаток."],
        hint="В `(int) (points * 1.5)` умножение даёт `double`, например 55.5, а `(int)` отбрасывает дробную часть — "
             "получается 55. Скобки вокруг `points * 1.5` нужны, чтобы `(int)` применился к результату умножения.",
        solution=CHORES,
        wrong=[("старые баллы прибавлены до бонуса: бабушка увеличила и их",
                _change(_change(CHORES, 'points += saved;', ''), 'points = (int) (points * 1.5);',
                        'points += saved;\npoints = (int) (points * 1.5);')),
               ("+= вместо -=: штраф за напоминания прибавляется к баллам",
                _change(CHORES, 'points -= reminders * 2;', 'points += reminders * 2;')),
               ("/= вместо %=: в points осталось число часов, а не остаток баллов",
                _change(CHORES, 'points %= 20;', 'points /= 20;'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-prac9-laundry", title="Большая стирка",
        given=[("String", "tag"), ("int", "kg"), ("int", "drum"), ("int", "cycle")],
        variants=[{"tag": '"cotton-60"', "kg": "12", "drum": "5", "cycle": "85"}],
        hidden=[{"tag": '"wool-30"', "kg": "4", "drum": "6", "cycle": "50"},
                {"tag": '"synthetic-40"', "kg": "21", "drum": "7", "cycle": "70"},
                {"tag": '"linen-90"', "kg": "0", "drum": "5", "cycle": "120"},
                {"tag": '"silk-20"', "kg": "9", "drum": "8", "cycle": "35"},
                {"tag": '"denim-40"', "kg": "25", "drum": "6", "cycle": "100"}],
        intro="В субботу у семьи большая стирка: `kg` кг белья, а на ярлыке написано `tag` — ткань и температура "
              "стирки через дефис. В барабан помещается `drum` кг. Машинку запускают только полной, а то, что не "
              "набрало целую загрузку, ждёт следующей субботы. Кроме того, отдельной загрузкой всегда стирается "
              "постельное бельё. Одна стирка длится `cycle` минут, и после каждой ещё 10 минут уходит, чтобы "
              "развесить бельё. Порошка нужно полтора мерных колпачка на загрузку.",
        steps=["Заведи `String fabric` — часть ярлыка до дефиса заглавными буквами (номер дефиса в строке даёт "
               "`tag.indexOf(\"-\")`), и `String degrees` — всё, что после дефиса.",
               "Заведи `int loads = kg / drum;` — полные загрузки и `int rest = kg % drum;` — сколько килограммов ждёт "
               "следующей субботы. Потом добавь к `loads` загрузку постельного белья операцией `++`.",
               "Заведи `int minutes = loads * (cycle + 10);` — стирка и развешивание всех загрузок. Переведи это в "
               "часы: `int hours = minutes / 60;`, а в `minutes` оставь остаток операцией `%=`.",
               "Заведи `double caps = loads * 1.5;` — сколько колпачков порошка.",
               "Выведи четыре строки: ткань, `, `, температура и ` C`; `Loads: `, загрузки, `, waiting: `, остаток "
               "и ` kg`; `Time: `, часы, ` h `, минуты и ` min`; `Powder: `, колпачки и ` caps`."],
        hint="`tag.substring(tag.indexOf(\"-\") + 1)` начинается со следующего символа после дефиса, так что сам дефис "
             "в температуру не попадёт. Загрузку белья добавь до подсчёта времени и порошка, а часы посчитай до `%=`.",
        solution=LAUNDRY,
        wrong=[("загрузка постельного белья добавлена после подсчёта времени: её стирка не учтена",
                _change(_change(LAUNDRY, 'loads++;', ''), 'int hours = minutes / 60;',
                        'loads++;\nint hours = minutes / 60;')),
               ("температура взята вместе с дефисом",
                _change(LAUNDRY, 'String degrees = tag.substring(tag.indexOf("-") + 1);',
                        'String degrees = tag.substring(tag.indexOf("-"));')),
               ("минуты оставлены раньше, чем посчитаны часы: часов получается 0",
                LAUNDRY.replace('int hours = minutes / 60;\nminutes %= 60;', 'minutes %= 60;\nint hours = minutes / 60;'))],
        constructs=["augmented_assignment"],
    ),
]
