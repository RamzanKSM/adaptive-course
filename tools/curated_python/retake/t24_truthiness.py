"""PY_TRUTHINESS — «Истинность значений». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, += -=, f-strings, if/else, comparison operators, and, or/not, elif.
Not yet: loops, lists, functions."""
from build import OutputTask

SKILL = "PY_TRUTHINESS"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-tr-rt-alarm-clock", title="Будильник на телефоне",
        given=["label", "snooze"],
        variants=[{"label": '"Gym"', "snooze": "0"}, {"label": '""', "snooze": "10"},
                  {"label": '"School"', "snooze": "5"}],
        hidden=[{"label": '""', "snooze": "0"}, {"label": '"Work"', "snooze": "15"}, {"label": '"Pills"', "snooze": "0"}],
        intro="Телефон показывает карточку будильника. Подпись будильника — `label = {label}` (если её не задали, там "
              "пустая строка `\"\"`), а повтор через сколько минут — `snooze = {snooze}` (0 значит, что повтор выключен).",
        steps=["Если подпись не пустая, выведи f-строкой `Alarm: <label>`, иначе выведи `Alarm`. "
               "Пиши условие просто `if label:` — без сравнений.",
               "Затем, если повтор выключен, выведи `Snooze off`, а иначе выведи f-строкой `Snooze: <snooze> min`. "
               "Для числа 0 используй `not`: `if not snooze:`.",
               "Например, для `label = \"Work\"` и `snooze = 15` программа выводит `Alarm: Work` и `Snooze: 15 min`."],
        hint="В условии значение само превращается в `True` или `False`: пустая строка `\"\"` и число `0` ложны, "
             "любая непустая строка и любое другое число — истинны. `not 0` — это `True`.",
        solution='if label:\n    print(f"Alarm: {label}")\nelse:\n    print("Alarm")\nif not snooze:\n'
                 '    print("Snooze off")\nelse:\n    print(f"Snooze: {snooze} min")',
        wrong=[("забыт not: пишет «Snooze off», когда повтор включён",
                'if label:\n    print(f"Alarm: {label}")\nelse:\n    print("Alarm")\nif snooze:\n'
                '    print("Snooze off")\nelse:\n    print(f"Snooze: {snooze} min")'),
               ("лишний not в первом условии: ветки подписи срабатывают наоборот",
                'if not label:\n    print(f"Alarm: {label}")\nelse:\n    print("Alarm")\nif not snooze:\n'
                '    print("Snooze off")\nelse:\n    print(f"Snooze: {snooze} min")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-tr-rt-cinema-booking", title="Бронь билетов в кино",
        given=["seats_left", "tickets", "email"],
        variants=[{"seats_left": "40", "tickets": "3", "email": '"anya@mail.ru"'},
                  {"seats_left": "12", "tickets": "0", "email": '"boris@mail.ru"'},
                  {"seats_left": "5", "tickets": "2", "email": '""'}],
        hidden=[{"seats_left": "2", "tickets": "4", "email": '"vera@mail.ru"'},
                {"seats_left": "6", "tickets": "6", "email": '""'},
                {"seats_left": "30", "tickets": "0", "email": '""'},
                {"seats_left": "50", "tickets": "1", "email": '"oleg@mail.ru"'}],
        intro="Сайт кинотеатра бронирует билеты. В зале осталось `seats_left = {seats_left}` свободных мест. Покупатель "
              "выбрал `tickets = {tickets}` билетов (0 — ещё ничего не выбрал) и ввёл почту `email = {email}` "
              "(пустая строка — почту не ввёл, тогда билеты просто показывают на экране).",
        steps=["Если билеты не выбраны (проверь через истинность: `if not tickets:`), выведи `Choose your tickets`.",
               "Иначе, если `tickets` больше `seats_left`, выведи `Not enough seats`.",
               "Иначе уменьши `seats_left` на `tickets` с помощью `-=` и выведи f-строкой `Tickets booked: <tickets>`. "
               "Если при этом почта не пустая (`if email:`), выведи ещё строку `Sent to <email>`.",
               "В конце (в любом случае) выведи `Seats left: <seats_left>`.",
               "Например, для 2 свободных мест и 4 билетов программа выводит `Not enough seats` и `Seats left: 2`."],
        hint="Число 0 и пустая строка в условии ложны. Проверка почты стоит внутри ветки `else` — "
             "с отступом на уровень глубже. Забронировать ровно все оставшиеся места можно.",
        solution='if not tickets:\n    print("Choose your tickets")\nelif tickets > seats_left:\n    print("Not enough seats")\n'
                 'else:\n    seats_left -= tickets\n    print(f"Tickets booked: {tickets}")\n    if email:\n'
                 '        print(f"Sent to {email}")\nprint(f"Seats left: {seats_left}")',
        wrong=[("почта печатается всегда, даже пустая",
                'if not tickets:\n    print("Choose your tickets")\nelif tickets > seats_left:\n    print("Not enough seats")\n'
                'else:\n    seats_left -= tickets\n    print(f"Tickets booked: {tickets}")\n'
                '    print(f"Sent to {email}")\nprint(f"Seats left: {seats_left}")'),
               ("нестрогое сравнение: нельзя забронировать ровно все оставшиеся места",
                'if not tickets:\n    print("Choose your tickets")\nelif tickets >= seats_left:\n    print("Not enough seats")\n'
                'else:\n    seats_left -= tickets\n    print(f"Tickets booked: {tickets}")\n    if email:\n'
                '        print(f"Sent to {email}")\nprint(f"Seats left: {seats_left}")'),
               ("забыт not: просит выбрать билеты, когда они выбраны",
                'if tickets:\n    print("Choose your tickets")\nelif tickets > seats_left:\n    print("Not enough seats")\n'
                'else:\n    seats_left -= tickets\n    print(f"Tickets booked: {tickets}")\n    if email:\n'
                '        print(f"Sent to {email}")\nprint(f"Seats left: {seats_left}")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-tr-rt-microwave-timer", title="Таймер микроволновки",
        given=["seconds"],
        variants=[{"seconds": "125"}, {"seconds": "180"}, {"seconds": "45"}],
        hidden=[{"seconds": "60"}, {"seconds": "59"}, {"seconds": "0"}, {"seconds": "61"}, {"seconds": "600"}],
        intro="Микроволновка показывает на экране, сколько осталось греть. Время задано в секундах: `seconds = {seconds}`. "
              "Экран не показывает нулевые части: вместо `3 min 0 sec` пишет `3 min`.",
        steps=["Посчитай полные минуты (`seconds // 60`) и сохрани в `minutes`, а оставшиеся секунды (`seconds % 60`) — в `secs`.",
               "Если и `minutes`, и `secs` не нули (проверь через истинность: `if minutes and secs:`), "
               "выведи f-строкой `Timer: <minutes> min <secs> sec`.",
               "Иначе, если не ноль только `minutes`, выведи `Timer: <minutes> min`. "
               "Иначе, если не ноль только `secs`, выведи `Timer: <secs> sec`.",
               "Во всех остальных случаях (время 0) выведи `Timer is not set`.",
               "Например, для 61 секунды программа выводит `Timer: 1 min 1 sec`, а для 60 — `Timer: 1 min`."],
        hint="Число 0 в условии ложно, любое другое — истинно, поэтому `if minutes:` значит «если минут не ноль». "
             "Порядок веток важен: сначала проверь случай, когда обе части не нулевые, — иначе при 125 секундах "
             "сработает ветка только с минутами.",
        solution='minutes = seconds // 60\nsecs = seconds % 60\nif minutes and secs:\n'
                 '    print(f"Timer: {minutes} min {secs} sec")\nelif minutes:\n    print(f"Timer: {minutes} min")\n'
                 'elif secs:\n    print(f"Timer: {secs} sec")\nelse:\n    print("Timer is not set")',
        wrong=[("or вместо and: показывает «0 min» или «0 sec»",
                'minutes = seconds // 60\nsecs = seconds % 60\nif minutes or secs:\n'
                '    print(f"Timer: {minutes} min {secs} sec")\nelif minutes:\n    print(f"Timer: {minutes} min")\n'
                'elif secs:\n    print(f"Timer: {secs} sec")\nelse:\n    print("Timer is not set")'),
               ("ветка только с минутами стоит первой: секунды теряются",
                'minutes = seconds // 60\nsecs = seconds % 60\nif minutes:\n    print(f"Timer: {minutes} min")\n'
                'elif minutes and secs:\n    print(f"Timer: {minutes} min {secs} sec")\n'
                'elif secs:\n    print(f"Timer: {secs} sec")\nelse:\n    print("Timer is not set")'),
               ("путает // и %: минуты и секунды меняются местами",
                'minutes = seconds % 60\nsecs = seconds // 60\nif minutes and secs:\n'
                '    print(f"Timer: {minutes} min {secs} sec")\nelif minutes:\n    print(f"Timer: {minutes} min")\n'
                'elif secs:\n    print(f"Timer: {secs} sec")\nelse:\n    print("Timer is not set")')],
        constructs=["if"],
    ),
]
