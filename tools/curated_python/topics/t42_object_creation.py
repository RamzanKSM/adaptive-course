"""PY_OBJECT_CREATION — «Создание объектов». Taught before: everything up to functions, and classes (class, __init__,
self. attributes, a simple method). Here: calling the class to make objects; several independent objects from one
class; objects made in a loop and kept in a list. Not yet: inheritance, tuples, dicts, comprehensions."""
from build import OutputTask

SKILL = "PY_OBJECT_CREATION"

NEED_CLASS = ("ClassDef", "Опиши данные в собственном классе через class и создавай объекты по нему.")
NEED_INIT = ("re:def __init__\\(", "Передавай данные в объект через метод __init__ — он сам вызывается при создании объекта.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-obj-two-parcels", title="Две посылки",
        given=["city1", "weight1", "city2", "weight2"],
        variants=[{"city1": '"Казань"', "weight1": "3", "city2": '"Омск"', "weight2": "5"},
                  {"city1": '"Тула"', "weight1": "12", "city2": '"Сочи"', "weight2": "1"},
                  {"city1": '"Пермь"', "weight1": "7", "city2": '"Уфа"', "weight2": "4"}],
        hidden=[{"city1": '"Псков"', "weight1": "2", "city2": '"Чита"', "weight2": "10"},
                {"city1": '"Ярославль"', "weight1": "15", "city2": '"Курск"', "weight2": "4"},
                {"city1": '"Томск"', "weight1": "9", "city2": '"Орёл"', "weight2": "9"}],
        intro="Курьерская служба отправляет сегодня две посылки. У каждой посылки свой город назначения и свой вес "
              "в килограммах, но устроены они одинаково — значит, хватит одного класса и двух объектов.",
        steps=["Создай класс `Parcel`. В `__init__(self, city, weight)` сохрани город и вес в атрибуты "
               "`self.city` и `self.weight`.",
               "Создай два разных объекта: `parcel1` — из `city1` и `weight1`, `parcel2` — из `city2` и `weight2`.",
               "Для каждой посылки выведи строку вида `Посылка в Казань: 3 кг` — сначала для первой, потом для второй.",
               "В конце выведи строку вида `Общий вес: 8 кг` — с суммой весов двух посылок, взятых из их атрибутов."],
        hint="Каждый вызов `Parcel(...)` создаёт новый, отдельный объект со своими данными. "
             "Если записать второй объект в ту же переменную, что и первый, первый потеряется — "
             "поэтому у каждой посылки своя переменная.",
        solution='class Parcel:\n    def __init__(self, city, weight):\n        self.city = city\n        self.weight = weight\n\n\n'
                 'parcel1 = Parcel(city1, weight1)\nparcel2 = Parcel(city2, weight2)\n'
                 'print(f"Посылка в {parcel1.city}: {parcel1.weight} кг")\nprint(f"Посылка в {parcel2.city}: {parcel2.weight} кг")\n'
                 'print(f"Общий вес: {parcel1.weight + parcel2.weight} кг")',
        wrong=[("записывает обе посылки в одну переменную — первая теряется, вторая печатается дважды",
                'class Parcel:\n    def __init__(self, city, weight):\n        self.city = city\n        self.weight = weight\n\n\n'
                'parcel = Parcel(city1, weight1)\nparcel = Parcel(city2, weight2)\n'
                'print(f"Посылка в {parcel.city}: {parcel.weight} кг")\nprint(f"Посылка в {parcel.city}: {parcel.weight} кг")\n'
                'print(f"Общий вес: {parcel.weight + parcel.weight} кг")'),
               ("создаёт только первую посылку и печатает её два раза",
                'class Parcel:\n    def __init__(self, city, weight):\n        self.city = city\n        self.weight = weight\n\n\n'
                'parcel1 = Parcel(city1, weight1)\n'
                'print(f"Посылка в {parcel1.city}: {parcel1.weight} кг")\nprint(f"Посылка в {parcel1.city}: {parcel1.weight} кг")\n'
                'print(f"Общий вес: {parcel1.weight + parcel1.weight} кг")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-obj-queue-tickets", title="Талоны электронной очереди",
        given=["names", "first"],
        variants=[{"names": '["Аня", "Борис", "Вика"]', "first": "15"},
                  {"names": '["Дима", "Ева"]', "first": "101"},
                  {"names": '["Зоя", "Игорь", "Катя", "Лёва"]', "first": "7"}],
        hidden=[{"names": '["Маша"]', "first": "1"},
                {"names": '["Нина", "Олег", "Петя"]', "first": "40"},
                {"names": '["Рита", "Саша", "Таня", "Ульяна", "Федя"]', "first": "230"}],
        intro="В поликлинике работает электронная очередь: каждый, кто пришёл, получает талон со своим номером. "
              "Список `names` — люди в порядке прихода, а `first` — номер, с которого сегодня начинаются талоны.",
        steps=["Создай класс `Ticket`. В `__init__(self, number, owner)` сохрани номер талона и имя владельца "
               "в атрибуты `self.number` и `self.owner`.",
               "Создай пустой список `tickets`. Пройди циклом по списку `names` и для каждого человека создай объект "
               "`Ticket` и добавь его в `tickets`. Первый человек получает номер `first`, каждый следующий — на 1 больше.",
               "Вторым циклом пройди по списку `tickets` и для каждого талона выведи строку вида `Талон 15: Аня`.",
               "В конце выведи строку вида `Всего талонов: 3` — с длиной списка `tickets`."],
        hint="Объекты можно хранить в списке, как числа и строки: `tickets.append(Ticket(...))`. "
             "Номер удобно держать в отдельной переменной: перед циклом она равна `first`, "
             "а после создания каждого талона увеличивается на 1.",
        solution='class Ticket:\n    def __init__(self, number, owner):\n        self.number = number\n        self.owner = owner\n\n\n'
                 'tickets = []\nnumber = first\nfor name in names:\n    tickets.append(Ticket(number, name))\n    number += 1\n\n'
                 'for ticket in tickets:\n    print(f"Талон {ticket.number}: {ticket.owner}")\n'
                 'print(f"Всего талонов: {len(tickets)}")',
        wrong=[("не увеличивает номер — у всех талонов один и тот же номер",
                'class Ticket:\n    def __init__(self, number, owner):\n        self.number = number\n        self.owner = owner\n\n\n'
                'tickets = []\nfor name in names:\n    tickets.append(Ticket(first, name))\n\n'
                'for ticket in tickets:\n    print(f"Талон {ticket.number}: {ticket.owner}")\n'
                'print(f"Всего талонов: {len(tickets)}")'),
               ("добавляет талон в список после цикла — в списке оказывается только последний",
                'class Ticket:\n    def __init__(self, number, owner):\n        self.number = number\n        self.owner = owner\n\n\n'
                'tickets = []\nnumber = first\nfor name in names:\n    ticket = Ticket(number, name)\n    number += 1\n'
                'tickets.append(ticket)\n\n'
                'for ticket in tickets:\n    print(f"Талон {ticket.number}: {ticket.owner}")\n'
                'print(f"Всего талонов: {len(tickets)}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-obj-fastest-runner", title="Самый быстрый бегун",
        given=["names", "times"],
        variants=[{"names": '["Оля", "Кирилл", "Женя", "Таня"]', "times": "[58, 52, 61, 66]"},
                  {"names": '["Миша", "Лена", "Артём"]', "times": "[74, 69, 81]"},
                  {"names": '["Соня", "Глеб", "Вера", "Паша", "Ника"]', "times": "[63, 70, 55, 59, 64]"}],
        hidden=[{"names": '["Юра", "Аля", "Боря"]', "times": "[90, 85, 47]"},
                {"names": '["Даша"]', "times": "[71]"},
                {"names": '["Ира", "Костя", "Митя", "Лиза"]', "times": "[49, 56, 60, 52]"}],
        intro="На школьных соревнованиях бегуны пробежали 400 метров. В списке `names` — имена участников, "
              "а в списке `times` на тех же местах — их время в секундах. Все времена разные. Нужно найти победителя.",
        steps=["Создай класс `Runner`. В `__init__(self, name, time)` сохрани имя и время в атрибуты "
               "`self.name` и `self.time`.",
               "Создай список `runners`: пройди циклом по номерам позиций `range(len(names))` и для каждой позиции "
               "добавь в список объект `Runner` с именем и временем с этой позиции.",
               "Найди в списке `runners` объект с самым маленьким временем — запомни в переменной сам объект, "
               "а не только его время.",
               "Выведи две строки вида `Участников: 4` (сколько объектов в списке) и `Победитель: Кирилл, 52 сек` — "
               "с именем и временем победителя из атрибутов найденного объекта."],
        hint="Начни с того, что победитель — первый бегун в списке: `best = runners[0]`. Потом сравнивай каждого бегуна "
             "с ним: если `runner.time < best.time`, то `best = runner`. Так в `best` всегда лежит весь объект — "
             "и имя, и время.",
        solution='class Runner:\n    def __init__(self, name, time):\n        self.name = name\n        self.time = time\n\n\n'
                 'runners = []\nfor i in range(len(names)):\n    runners.append(Runner(names[i], times[i]))\n\n'
                 'best = runners[0]\nfor runner in runners:\n    if runner.time < best.time:\n        best = runner\n\n'
                 'print(f"Участников: {len(runners)}")\nprint(f"Победитель: {best.name}, {best.time} сек")',
        wrong=[("ищет самое большое время — побеждает самый медленный",
                'class Runner:\n    def __init__(self, name, time):\n        self.name = name\n        self.time = time\n\n\n'
                'runners = []\nfor i in range(len(names)):\n    runners.append(Runner(names[i], times[i]))\n\n'
                'best = runners[0]\nfor runner in runners:\n    if runner.time > best.time:\n        best = runner\n\n'
                'print(f"Участников: {len(runners)}")\nprint(f"Победитель: {best.name}, {best.time} сек")'),
               ("запоминает только лучшее время, а имя берёт у последнего бегуна из цикла",
                'class Runner:\n    def __init__(self, name, time):\n        self.name = name\n        self.time = time\n\n\n'
                'runners = []\nfor i in range(len(names)):\n    runners.append(Runner(names[i], times[i]))\n\n'
                'best_time = runners[0].time\nfor runner in runners:\n    if runner.time < best_time:\n        best_time = runner.time\n\n'
                'print(f"Участников: {len(runners)}")\nprint(f"Победитель: {runner.name}, {best_time} сек")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
]
