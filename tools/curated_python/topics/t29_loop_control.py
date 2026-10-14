"""PY_LOOP_CONTROL — «break и continue». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, += -=, f-strings, if/elif/else, comparisons, and/or/not, truthiness, for + range, accumulator, while.
Not yet: lists, string slicing and methods, functions."""
from build import OutputTask

SKILL = "PY_LOOP_CONTROL"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lc-skip-floor", title="Лифт без одного этажа",
        given=["floors", "skip"],
        variants=[{"floors": "7", "skip": "4"}, {"floors": "9", "skip": "6"}, {"floors": "8", "skip": "3"}],
        hidden=[{"floors": "5", "skip": "2"}, {"floors": "6", "skip": "6"}, {"floors": "10", "skip": "4"}],
        intro="В некоторых домах нет этажа с «несчастливым» номером. Кнопки в лифте нашего дома пронумерованы "
              "от 1 до `floors = {floors}`, но кнопки с номером `skip = {skip}` нет.",
        steps=["Перебери циклом `for` номера от 1 до `floors` включительно.",
               "Если номер равен `skip`, пропусти его с помощью `continue`.",
               "Каждый остальной номер выведи на отдельной строке."],
        hint="`continue` сразу переходит к следующему шагу цикла: команды, которые стоят в цикле ниже него, "
             "на этом шаге не выполняются. Поэтому проверка должна стоять перед `print`.",
        solution="for floor in range(1, floors + 1):\n    if floor == skip:\n        continue\n    print(floor)",
        wrong=[("break вместо continue: цикл обрывается на пропущенном этаже",
                "for floor in range(1, floors + 1):\n    if floor == skip:\n        break\n    print(floor)"),
               ("print стоит перед проверкой: пропущенный номер всё равно выводится",
                "for floor in range(1, floors + 1):\n    print(floor)\n    if floor == skip:\n        continue")],
        constructs=["for"],
        must_use=[("Continue", "Используй continue, чтобы пропустить этаж")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lc-team-size", title="Равные команды",
        given=["n"],
        variants=[{"n": "15"}, {"n": "12"}, {"n": "49"}],
        hidden=[{"n": "7"}, {"n": "9"}, {"n": "10"}, {"n": "35"}],
        intro="Тренер делит `n = {n}` ребят на одинаковые команды так, чтобы никто не остался лишним. "
              "Команды должны быть как можно меньше, но в каждой — хотя бы 2 человека.",
        steps=["Перебирай размер команды циклом `for` от 2 до `n` включительно "
               "(размер `n` тоже подходит: тогда все будут в одной команде).",
               "Как только нашёлся размер, на который `n` делится без остатка, выведи его в формате `Team size: 4` "
               "и сразу останови цикл командой `break`.",
               "Программа должна вывести ровно одну строку."],
        hint="Без `break` цикл продолжит перебор и выведет все подходящие размеры. "
             "`break` выходит из цикла сразу, поэтому выведется только первый найденный — самый маленький — размер.",
        solution='for size in range(2, n + 1):\n    if n % size == 0:\n        print(f"Team size: {size}")\n        break',
        wrong=[("нет break: выводятся все подходящие размеры",
                'for size in range(2, n + 1):\n    if n % size == 0:\n        print(f"Team size: {size}")'),
               ("перебор с 1: на 1 делится любое число",
                'for size in range(1, n + 1):\n    if n % size == 0:\n        print(f"Team size: {size}")\n        break')],
        constructs=["for"],
        must_use=[("Break", "Используй break, чтобы остановить перебор, когда размер найден")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lc-piggy-bank", title="Копилка до цели",
        given=["weekly", "goal"],
        variants=[{"weekly": "150", "goal": "500"}, {"weekly": "200", "goal": "600"}, {"weekly": "350", "goal": "1000"}],
        hidden=[{"weekly": "100", "goal": "300"}, {"weekly": "250", "goal": "1000"}, {"weekly": "400", "goal": "500"},
                {"weekly": "500", "goal": "400"}],
        intro="Маша копит на наушники за `goal = {goal}` руб. Копилка сначала пустая, "
              "а каждую неделю Маша кладёт в неё `weekly = {weekly}` руб.",
        steps=["Заведи две переменные: номер недели и сумму в копилке. Обе сначала равны 0.",
               "Запусти цикл `while True:`. В нём увеличь номер недели на 1, добавь к сумме `weekly` "
               "и выведи строку вида `Week 5: 900 rub`",
               "Сразу после этого, если сумма стала не меньше `goal`, останови цикл командой `break`.",
               "После цикла выведи `Enough money!`"],
        hint="`while True` сам по себе никогда не закончится — выйти из него можно только через `break`. "
             "«Не меньше» значит «больше или равно»: если сумма ровно равна цене, денег уже хватает.",
        solution='week = 0\ntotal = 0\nwhile True:\n    week += 1\n    total += weekly\n'
                 '    print(f"Week {week}: {total} rub")\n    if total >= goal:\n        break\n'
                 'print("Enough money!")',
        wrong=[("строгое сравнение: при сумме ровно goal копит лишнюю неделю",
                'week = 0\ntotal = 0\nwhile True:\n    week += 1\n    total += weekly\n'
                '    print(f"Week {week}: {total} rub")\n    if total > goal:\n        break\n'
                'print("Enough money!")'),
               ("проверка стоит перед print: последняя неделя не выводится",
                'week = 0\ntotal = 0\nwhile True:\n    week += 1\n    total += weekly\n'
                '    if total >= goal:\n        break\n    print(f"Week {week}: {total} rub")\n'
                'print("Enough money!")')],
        constructs=["while"],
        must_use=[("Break", "Используй break, чтобы выйти из цикла while True")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lc-rest-days", title="Дни отдыха в тренировках",
        given=["days", "rest"],
        variants=[{"days": "8", "rest": "3"}, {"days": "10", "rest": "4"}, {"days": "7", "rest": "5"}],
        hidden=[{"days": "6", "rest": "2"}, {"days": "4", "rest": "4"}, {"days": "9", "rest": "3"}],
        intro="Лена готовится к забегу и составляет план тренировок на `days = {days}` дней. "
              "Каждый `rest = {rest}`-й день (день, номер которого делится на `rest` без остатка) — день отдыха, "
              "его в плане нет.",
        steps=["Перебери циклом `for` номера дней от 1 до `days` включительно.",
               "Если номер дня делится на `rest` без остатка, пропусти этот день с помощью `continue`.",
               "Для каждого остального дня выведи отдельной строкой надпись вида `Day 2: training`"],
        hint="Число делится на `rest` без остатка, когда остаток `%` равен 0. "
             "`continue` пропускает всё, что стоит в цикле ниже, поэтому проверку пиши перед `print`.",
        solution='for day in range(1, days + 1):\n    if day % rest == 0:\n        continue\n    print(f"Day {day}: training")',
        wrong=[("break вместо continue: план обрывается на первом дне отдыха",
                'for day in range(1, days + 1):\n    if day % rest == 0:\n        break\n    print(f"Day {day}: training")'),
               ("пропускает только сам день rest, а не все кратные ему",
                'for day in range(1, days + 1):\n    if day == rest:\n        continue\n    print(f"Day {day}: training")')],
        constructs=["for"],
        must_use=[("Continue", "Используй continue, чтобы пропустить день отдыха")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lc-next-bus", title="Ближайший автобус",
        given=["interval", "arrive"],
        variants=[{"interval": "15", "arrive": "20"}, {"interval": "10", "arrive": "43"}, {"interval": "20", "arrive": "5"}],
        hidden=[{"interval": "15", "arrive": "30"}, {"interval": "12", "arrive": "0"}, {"interval": "5", "arrive": "58"},
                {"interval": "20", "arrive": "41"}],
        intro="Автобус отходит от остановки в начале часа (на минуте 0) и потом каждые `interval = {interval}` минут, "
              "последний раз — на минуте 60. Аня пришла на остановку на минуте `arrive = {arrive}`.",
        steps=["Перебирай минуты отправления циклом `for` с `range` от 0 до 60 включительно с шагом `interval`.",
               "Как только нашлось отправление, которое не раньше `arrive`, выведи его в формате `Bus at minute 30` "
               "и сразу останови цикл командой `break`.",
               "Программа должна вывести ровно одну строку."],
        hint="Если Аня пришла ровно в минуту отправления, она успевает на этот автобус: сравнение здесь `>=`. "
             "Без `break` цикл продолжит перебор и выведет все следующие автобусы.",
        solution='for minute in range(0, 61, interval):\n    if minute >= arrive:\n        print(f"Bus at minute {minute}")\n        break',
        wrong=[("нет break: выводятся все автобусы после прихода",
                'for minute in range(0, 61, interval):\n    if minute >= arrive:\n        print(f"Bus at minute {minute}")'),
               ("строгое сравнение: Аня не успевает на автобус, который отходит ровно при ней",
                'for minute in range(0, 61, interval):\n    if minute > arrive:\n        print(f"Bus at minute {minute}")\n        break')],
        constructs=["for"],
        must_use=[("Break", "Используй break, чтобы остановить перебор, когда автобус найден")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lc-harvest", title="Сбор яблок",
        given=["per_day", "rain", "goal"],
        variants=[{"per_day": "40", "rain": "3", "goal": "150"}, {"per_day": "60", "rain": "4", "goal": "200"},
                  {"per_day": "25", "rain": "2", "goal": "75"}],
        hidden=[{"per_day": "50", "rain": "3", "goal": "100"}, {"per_day": "30", "rain": "5", "goal": "120"},
                {"per_day": "100", "rain": "2", "goal": "90"}, {"per_day": "20", "rain": "4", "goal": "130"}],
        intro="Фермер собирает яблоки, пока не наберёт `goal = {goal}` кг. В хороший день он собирает `per_day = {per_day}` кг, "
              "а каждый `rain = {rain}`-й день (номер дня делится на `rain` без остатка) идёт дождь, и сбора нет.",
        steps=["Заведи две переменные: номер дня и собранные килограммы. Обе сначала равны 0.",
               "Запусти цикл `while True:`. В начале каждого шага увеличь номер дня на 1.",
               "Если в этот день дождь, выведи строку вида `Day 3: rain` и перейди к следующему дню командой `continue`.",
               "Иначе добавь `per_day` к собранному и выведи строку вида `Day 2: 80 kg` (сколько собрано всего). "
               "Если собрано не меньше `goal`, останови цикл командой `break`.",
               "После цикла выведи строку вида `Done on day 5`"],
        hint="`continue` в `while` сразу возвращает к началу цикла, поэтому номер дня нужно увеличивать в самом начале шага — "
             "иначе после дождливого дня цикл никогда не сдвинется дальше. Выйти из `while True` можно только через `break`.",
        solution='day = 0\ntotal = 0\nwhile True:\n    day += 1\n    if day % rain == 0:\n        print(f"Day {day}: rain")\n'
                 '        continue\n    total += per_day\n    print(f"Day {day}: {total} kg")\n    if total >= goal:\n        break\n'
                 'print(f"Done on day {day}")',
        wrong=[("нет continue: в дождливый день тоже собирает яблоки",
                'day = 0\ntotal = 0\nwhile True:\n    day += 1\n    if day % rain == 0:\n        print(f"Day {day}: rain")\n'
                '    total += per_day\n    print(f"Day {day}: {total} kg")\n    if total >= goal:\n        break\n'
                'print(f"Done on day {day}")'),
               ("строгое сравнение: собрав ровно goal, работает лишний день",
                'day = 0\ntotal = 0\nwhile True:\n    day += 1\n    if day % rain == 0:\n        print(f"Day {day}: rain")\n'
                '        continue\n    total += per_day\n    print(f"Day {day}: {total} kg")\n    if total > goal:\n        break\n'
                'print(f"Done on day {day}")')],
        constructs=["while"],
        must_use=[("Break", "Используй break, чтобы выйти из цикла while True"),
                  ("Continue", "Используй continue, чтобы пропустить дождливый день")],
    ),
]
