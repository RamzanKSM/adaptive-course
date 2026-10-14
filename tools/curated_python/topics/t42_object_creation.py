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
        variants=[{"city1": '"Kazan"', "weight1": "3", "city2": '"Omsk"', "weight2": "5"},
                  {"city1": '"Tula"', "weight1": "12", "city2": '"Sochi"', "weight2": "1"},
                  {"city1": '"Perm"', "weight1": "7", "city2": '"Ufa"', "weight2": "4"}],
        hidden=[{"city1": '"Pskov"', "weight1": "2", "city2": '"Chita"', "weight2": "10"},
                {"city1": '"Yaroslavl"', "weight1": "15", "city2": '"Kursk"', "weight2": "4"},
                {"city1": '"Tomsk"', "weight1": "9", "city2": '"Oryol"', "weight2": "9"}],
        intro="Курьерская служба отправляет сегодня две посылки. У каждой посылки свой город назначения и свой вес "
              "в килограммах, но устроены они одинаково — значит, хватит одного класса и двух объектов.",
        steps=["Создай класс `Parcel`. В `__init__(self, city, weight)` сохрани город и вес в атрибуты "
               "`self.city` и `self.weight`.",
               "Создай два разных объекта: `parcel1` — из `city1` и `weight1`, `parcel2` — из `city2` и `weight2`.",
               "Для каждой посылки выведи строку вида `Parcel to Kazan: 3 kg` — сначала для первой, потом для второй.",
               "В конце выведи строку вида `Total weight: 8 kg` — с суммой весов двух посылок, взятых из их атрибутов."],
        hint="Каждый вызов `Parcel(...)` создаёт новый, отдельный объект со своими данными. "
             "Если записать второй объект в ту же переменную, что и первый, первый потеряется — "
             "поэтому у каждой посылки своя переменная.",
        solution='class Parcel:\n    def __init__(self, city, weight):\n        self.city = city\n        self.weight = weight\n\n\n'
                 'parcel1 = Parcel(city1, weight1)\nparcel2 = Parcel(city2, weight2)\n'
                 'print(f"Parcel to {parcel1.city}: {parcel1.weight} kg")\nprint(f"Parcel to {parcel2.city}: {parcel2.weight} kg")\n'
                 'print(f"Total weight: {parcel1.weight + parcel2.weight} kg")',
        wrong=[("записывает обе посылки в одну переменную — первая теряется, вторая печатается дважды",
                'class Parcel:\n    def __init__(self, city, weight):\n        self.city = city\n        self.weight = weight\n\n\n'
                'parcel = Parcel(city1, weight1)\nparcel = Parcel(city2, weight2)\n'
                'print(f"Parcel to {parcel.city}: {parcel.weight} kg")\nprint(f"Parcel to {parcel.city}: {parcel.weight} kg")\n'
                'print(f"Total weight: {parcel.weight + parcel.weight} kg")'),
               ("создаёт только первую посылку и печатает её два раза",
                'class Parcel:\n    def __init__(self, city, weight):\n        self.city = city\n        self.weight = weight\n\n\n'
                'parcel1 = Parcel(city1, weight1)\n'
                'print(f"Parcel to {parcel1.city}: {parcel1.weight} kg")\nprint(f"Parcel to {parcel1.city}: {parcel1.weight} kg")\n'
                'print(f"Total weight: {parcel1.weight + parcel1.weight} kg")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-obj-queue-tickets", title="Талоны электронной очереди",
        given=["names", "first"],
        variants=[{"names": '["Anya", "Boris", "Vika"]', "first": "15"},
                  {"names": '["Dima", "Eva"]', "first": "101"},
                  {"names": '["Zoya", "Igor", "Katya", "Lyova"]', "first": "7"}],
        hidden=[{"names": '["Masha"]', "first": "1"},
                {"names": '["Nina", "Oleg", "Petya"]', "first": "40"},
                {"names": '["Rita", "Sasha", "Tanya", "Ulyana", "Fedya"]', "first": "230"}],
        intro="В поликлинике работает электронная очередь: каждый, кто пришёл, получает талон со своим номером. "
              "Список `names` — люди в порядке прихода, а `first` — номер, с которого сегодня начинаются талоны.",
        steps=["Создай класс `Ticket`. В `__init__(self, number, owner)` сохрани номер талона и имя владельца "
               "в атрибуты `self.number` и `self.owner`.",
               "Создай пустой список `tickets`. Пройди циклом по списку `names` и для каждого человека создай объект "
               "`Ticket` и добавь его в `tickets`. Первый человек получает номер `first`, каждый следующий — на 1 больше.",
               "Вторым циклом пройди по списку `tickets` и для каждого талона выведи строку вида `Ticket 15: Anya`.",
               "В конце выведи строку вида `Total tickets: 3` — с длиной списка `tickets`."],
        hint="Объекты можно хранить в списке, как числа и строки: `tickets.append(Ticket(...))`. "
             "Номер удобно держать в отдельной переменной: перед циклом она равна `first`, "
             "а после создания каждого талона увеличивается на 1.",
        solution='class Ticket:\n    def __init__(self, number, owner):\n        self.number = number\n        self.owner = owner\n\n\n'
                 'tickets = []\nnumber = first\nfor name in names:\n    tickets.append(Ticket(number, name))\n    number += 1\n\n'
                 'for ticket in tickets:\n    print(f"Ticket {ticket.number}: {ticket.owner}")\n'
                 'print(f"Total tickets: {len(tickets)}")',
        wrong=[("не увеличивает номер — у всех талонов один и тот же номер",
                'class Ticket:\n    def __init__(self, number, owner):\n        self.number = number\n        self.owner = owner\n\n\n'
                'tickets = []\nfor name in names:\n    tickets.append(Ticket(first, name))\n\n'
                'for ticket in tickets:\n    print(f"Ticket {ticket.number}: {ticket.owner}")\n'
                'print(f"Total tickets: {len(tickets)}")'),
               ("добавляет талон в список после цикла — в списке оказывается только последний",
                'class Ticket:\n    def __init__(self, number, owner):\n        self.number = number\n        self.owner = owner\n\n\n'
                'tickets = []\nnumber = first\nfor name in names:\n    ticket = Ticket(number, name)\n    number += 1\n'
                'tickets.append(ticket)\n\n'
                'for ticket in tickets:\n    print(f"Ticket {ticket.number}: {ticket.owner}")\n'
                'print(f"Total tickets: {len(tickets)}")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-obj-fastest-runner", title="Самый быстрый бегун",
        given=["names", "times"],
        variants=[{"names": '["Olya", "Kirill", "Zhenya", "Tanya"]', "times": "[58, 52, 61, 66]"},
                  {"names": '["Misha", "Lena", "Artyom"]', "times": "[74, 69, 81]"},
                  {"names": '["Sonya", "Gleb", "Vera", "Pasha", "Nika"]', "times": "[63, 70, 55, 59, 64]"}],
        hidden=[{"names": '["Yura", "Alya", "Borya"]', "times": "[90, 85, 47]"},
                {"names": '["Dasha"]', "times": "[71]"},
                {"names": '["Ira", "Kostya", "Mitya", "Liza"]', "times": "[49, 56, 60, 52]"}],
        intro="На школьных соревнованиях бегуны пробежали 400 метров. В списке `names` — имена участников, "
              "а в списке `times` на тех же местах — их время в секундах. Все времена разные. Нужно найти победителя.",
        steps=["Создай класс `Runner`. В `__init__(self, name, time)` сохрани имя и время в атрибуты "
               "`self.name` и `self.time`.",
               "Создай список `runners`: пройди циклом по номерам позиций `range(len(names))` и для каждой позиции "
               "добавь в список объект `Runner` с именем и временем с этой позиции.",
               "Найди в списке `runners` объект с самым маленьким временем — запомни в переменной сам объект, "
               "а не только его время.",
               "Выведи две строки вида `Runners: 4` (сколько объектов в списке) и `Winner: Kirill, 52 sec` — "
               "с именем и временем победителя из атрибутов найденного объекта."],
        hint="Начни с того, что победитель — первый бегун в списке: `best = runners[0]`. Потом сравнивай каждого бегуна "
             "с ним: если `runner.time < best.time`, то `best = runner`. Так в `best` всегда лежит весь объект — "
             "и имя, и время.",
        solution='class Runner:\n    def __init__(self, name, time):\n        self.name = name\n        self.time = time\n\n\n'
                 'runners = []\nfor i in range(len(names)):\n    runners.append(Runner(names[i], times[i]))\n\n'
                 'best = runners[0]\nfor runner in runners:\n    if runner.time < best.time:\n        best = runner\n\n'
                 'print(f"Runners: {len(runners)}")\nprint(f"Winner: {best.name}, {best.time} sec")',
        wrong=[("ищет самое большое время — побеждает самый медленный",
                'class Runner:\n    def __init__(self, name, time):\n        self.name = name\n        self.time = time\n\n\n'
                'runners = []\nfor i in range(len(names)):\n    runners.append(Runner(names[i], times[i]))\n\n'
                'best = runners[0]\nfor runner in runners:\n    if runner.time > best.time:\n        best = runner\n\n'
                'print(f"Runners: {len(runners)}")\nprint(f"Winner: {best.name}, {best.time} sec")'),
               ("запоминает только лучшее время, а имя берёт у последнего бегуна из цикла",
                'class Runner:\n    def __init__(self, name, time):\n        self.name = name\n        self.time = time\n\n\n'
                'runners = []\nfor i in range(len(names)):\n    runners.append(Runner(names[i], times[i]))\n\n'
                'best_time = runners[0].time\nfor runner in runners:\n    if runner.time < best_time:\n        best_time = runner.time\n\n'
                'print(f"Runners: {len(runners)}")\nprint(f"Winner: {runner.name}, {best_time} sec")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-obj-two-mugs", title="Две кружки чая",
        given=["owner1", "owner2", "volume", "drunk"],
        variants=[{"owner1": '"Anya"', "owner2": '"Boris"', "volume": "250", "drunk": "100"},
                  {"owner1": '"Vika"', "owner2": '"Gleb"', "volume": "300", "drunk": "180"},
                  {"owner1": '"Dima"', "owner2": '"Eva"', "volume": "200", "drunk": "50"}],
        hidden=[{"owner1": '"Zoya"', "owner2": '"Igor"', "volume": "350", "drunk": "0"},
                {"owner1": '"Katya"', "owner2": '"Lev"', "volume": "220", "drunk": "220"},
                {"owner1": '"Masha"', "owner2": '"Nikita"', "volume": "400", "drunk": "125"}],
        intro="Двое друзей налили себе чай в одинаковые кружки — по `volume` миллилитров в каждую. "
              "Потом первый из них, `owner1`, отпил `drunk` миллилитров. Чай во второй кружке от этого не убавился: "
              "кружки разные, хоть и одинаковые на вид. Так же ведут себя и объекты одного класса.",
        steps=["Создай класс `Mug`. В `__init__(self, owner, volume)` сохрани владельца и объём чая в атрибуты "
               "`self.owner` и `self.volume`.",
               "Создай две отдельные кружки двумя вызовами класса: `mug1 = Mug(owner1, volume)` и "
               "`mug2 = Mug(owner2, volume)`.",
               "Уменьши чай только в первой кружке: `mug1.volume -= drunk`.",
               "Выведи для каждой кружки строку вида `Anya: 150 ml` — имя владельца и сколько чая осталось, "
               "сначала для первой кружки, потом для второй."],
        hint="Каждый вызов `Mug(...)` создаёт новый объект со своими атрибутами. Если вместо второго вызова написать "
             "`mug2 = mug1`, новой кружки не появится: обе переменные будут указывать на одну и ту же кружку, "
             "и глоток из «первой» убавит чай и во «второй».",
        solution='class Mug:\n    def __init__(self, owner, volume):\n        self.owner = owner\n        self.volume = volume\n\n\n'
                 'mug1 = Mug(owner1, volume)\nmug2 = Mug(owner2, volume)\nmug1.volume -= drunk\n'
                 'print(f"{mug1.owner}: {mug1.volume} ml")\nprint(f"{mug2.owner}: {mug2.volume} ml")',
        wrong=[("не создаёт вторую кружку, а пишет mug2 = mug1 — глоток убавляет чай в обеих",
                'class Mug:\n    def __init__(self, owner, volume):\n        self.owner = owner\n        self.volume = volume\n\n\n'
                'mug1 = Mug(owner1, volume)\nmug2 = mug1\nmug2.owner = owner2\nmug1.volume -= drunk\n'
                'print(f"{owner1}: {mug1.volume} ml")\nprint(f"{mug2.owner}: {mug2.volume} ml")'),
               ("отпивает не из той кружки — уменьшает чай у второго владельца",
                'class Mug:\n    def __init__(self, owner, volume):\n        self.owner = owner\n        self.volume = volume\n\n\n'
                'mug1 = Mug(owner1, volume)\nmug2 = Mug(owner2, volume)\nmug2.volume -= drunk\n'
                'print(f"{mug1.owner}: {mug1.volume} ml")\nprint(f"{mug2.owner}: {mug2.volume} ml")')],
        constructs=["class"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-obj-frosty-days", title="Морозные дни",
        given=["temps"],
        variants=[{"temps": "[2, -3, 0, -7, 4]"},
                  {"temps": "[-1, -5, 3]"},
                  {"temps": "[5, 8, -2, 1, -4, -6]"}],
        hidden=[{"temps": "[0, 1, 2]"},
                {"temps": "[-10]"},
                {"temps": "[3, -1, 0, 0, -1, 7, -15]"}],
        intro="Школьная метеостанция записала температуру за несколько дней подряд — список `temps`, "
              "по одному числу на день, начиная с первого дня. Нужно отметить морозные дни — те, "
              "когда температура была ниже нуля.",
        steps=["Создай класс `Day`. В `__init__(self, number, temp)` сохрани номер дня и температуру в атрибуты "
               "`self.number` и `self.temp`.",
               "Создай пустой список `days`. Пройди циклом по `temps` и для каждой температуры создай объект `Day` "
               "и добавь его в `days`. Первый день имеет номер 1, каждый следующий — на 1 больше.",
               "Вторым циклом пройди по списку `days` и для каждого дня с температурой ниже нуля выведи строку вида "
               "`Day 2: -3 C`. Попутно посчитай, сколько таких дней.",
               "В конце выведи строку вида `Frosty days: 2`. Ноль градусов морозом не считается."],
        hint="Номер дня удобно держать в отдельной переменной: перед циклом она равна 1, а после создания каждого "
             "объекта увеличивается на 1. Во втором цикле переменная цикла — уже объект `Day`, поэтому температура "
             "у него берётся через точку: `day.temp`.",
        solution='class Day:\n    def __init__(self, number, temp):\n        self.number = number\n        self.temp = temp\n\n\n'
                 'days = []\nnumber = 1\nfor temp in temps:\n    days.append(Day(number, temp))\n    number += 1\n\n'
                 'frosty = 0\nfor day in days:\n    if day.temp < 0:\n        print(f"Day {day.number}: {day.temp} C")\n'
                 '        frosty += 1\nprint(f"Frosty days: {frosty}")',
        wrong=[("считает ноль градусов морозом",
                'class Day:\n    def __init__(self, number, temp):\n        self.number = number\n        self.temp = temp\n\n\n'
                'days = []\nnumber = 1\nfor temp in temps:\n    days.append(Day(number, temp))\n    number += 1\n\n'
                'frosty = 0\nfor day in days:\n    if day.temp <= 0:\n        print(f"Day {day.number}: {day.temp} C")\n'
                '        frosty += 1\nprint(f"Frosty days: {frosty}")'),
               ("нумерует дни с нуля",
                'class Day:\n    def __init__(self, number, temp):\n        self.number = number\n        self.temp = temp\n\n\n'
                'days = []\nnumber = 0\nfor temp in temps:\n    days.append(Day(number, temp))\n    number += 1\n\n'
                'frosty = 0\nfor day in days:\n    if day.temp < 0:\n        print(f"Day {day.number}: {day.temp} C")\n'
                '        frosty += 1\nprint(f"Frosty days: {frosty}")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-obj-above-average", title="Выше среднего",
        given=["names", "scores"],
        variants=[{"names": '["Anya", "Boris", "Vika", "Gleb"]', "scores": "[80, 65, 90, 61]"},
                  {"names": '["Dasha", "Egor", "Zhenya"]', "scores": "[70, 85, 55]"},
                  {"names": '["Ira", "Kostya", "Lena", "Misha", "Nina"]', "scores": "[45, 92, 78, 60, 75]"}],
        hidden=[{"names": '["Oleg", "Polina"]', "scores": "[50, 50]"},
                {"names": '["Rita"]', "scores": "[99]"},
                {"names": '["Sasha", "Tanya", "Uma"]', "scores": "[70, 71, 72]"},
                {"names": '["Fedya", "Khristina", "Yasha", "Kira"]', "scores": "[100, 0, 40, 41]"}],
        intro="После контрольной учитель хочет похвалить тех, кто написал её лучше среднего по классу. "
              "В списке `names` — имена учеников, а в списке `scores` на тех же местах — их баллы.",
        steps=["Создай класс `Student`. В `__init__(self, name, score)` сохрани имя и баллы в атрибуты "
               "`self.name` и `self.score`.",
               "Создай список `students`: пройди циклом по позициям `range(len(names))` и для каждой позиции добавь "
               "объект `Student` с именем и баллами с этой позиции.",
               "Пройди по списку `students`, сложи баллы всех учеников и найди средний балл как целую часть от деления "
               "суммы на число учеников (`//`). Выведи строку вида `Average: 74`.",
               "Ещё одним циклом по `students` собери в список имена тех, у кого баллов строго больше среднего. "
               "Выведи строку вида `Above average: Anya, Vika` — имена через запятую и пробел в порядке списка. "
               "Если таких нет, выведи `Above average: none`."],
        hint="Средний балл можно найти, только когда пройдены все ученики, поэтому понадобятся два прохода по списку "
             "объектов: первый — для суммы, второй — для отбора. Имена из списка склеивает `\", \".join(...)`. "
             "Ученик, у которого баллов ровно столько, сколько среднее, выше среднего не считается.",
        solution='class Student:\n    def __init__(self, name, score):\n        self.name = name\n        self.score = score\n\n\n'
                 'students = []\nfor i in range(len(names)):\n    students.append(Student(names[i], scores[i]))\n\n'
                 'total = 0\nfor student in students:\n    total += student.score\naverage = total // len(students)\n'
                 'print(f"Average: {average}")\n\nbest = []\nfor student in students:\n    if student.score > average:\n'
                 '        best.append(student.name)\nif best:\n    print(f"Above average: {\', \'.join(best)}")\nelse:\n'
                 '    print("Above average: none")',
        wrong=[("отбирает тех, у кого баллов не меньше среднего — ученик ровно со средним баллом тоже попадает в список",
                'class Student:\n    def __init__(self, name, score):\n        self.name = name\n        self.score = score\n\n\n'
                'students = []\nfor i in range(len(names)):\n    students.append(Student(names[i], scores[i]))\n\n'
                'total = 0\nfor student in students:\n    total += student.score\naverage = total // len(students)\n'
                'print(f"Average: {average}")\n\nbest = []\nfor student in students:\n    if student.score >= average:\n'
                '        best.append(student.name)\nif best:\n    print(f"Above average: {\', \'.join(best)}")\nelse:\n'
                '    print("Above average: none")'),
               ("забыл случай, когда никто не выше среднего — печатает пустую строку после двоеточия",
                'class Student:\n    def __init__(self, name, score):\n        self.name = name\n        self.score = score\n\n\n'
                'students = []\nfor i in range(len(names)):\n    students.append(Student(names[i], scores[i]))\n\n'
                'total = 0\nfor student in students:\n    total += student.score\naverage = total // len(students)\n'
                'print(f"Average: {average}")\n\nbest = []\nfor student in students:\n    if student.score > average:\n'
                '        best.append(student.name)\nprint(f"Above average: {\', \'.join(best)}")')],
        constructs=["class", "for"],
        must_use=[NEED_CLASS, NEED_INIT],
    ),
]
