"""PY_DICT_BASIC — «Словари dict». Taught before: everything up to sets (conditions, loops, lists and their methods,
slices, string methods, functions, classes, tuples, sets). Here: d[key], .get(key, default), keys/values/items,
counting with a dict, adding and updating values. Dict order is insertion order, so printing in dict order is stable.
Not yet: comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_DICT_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-dict-phone-book", title="Записная книжка",
        given=["phones", "name"],
        variants=[{"phones": '{"Anya": "+7 900 111-22-33", "Boris": "+7 911 222-33-44", "Vika": "+7 922 333-44-55"}',
                   "name": '"Boris"'},
                  {"phones": '{"Mom": "+7 903 555-12-34", "Dad": "+7 905 555-43-21", "Grandma": "+7 916 777-00-11", '
                             '"Coach": "+7 926 123-45-67"}',
                   "name": '"Coach"'},
                  {"phones": '{"Oleg": "+7 999 010-20-30", "Sonya": "+7 985 404-50-60"}', "name": '"Oleg"'}],
        hidden=[{"phones": '{"Anya": "+7 900 111-22-33", "Boris": "+7 911 222-33-44"}', "name": '"Grisha"'},
                {"phones": '{"Kira": "+7 901 000-00-01"}', "name": '"Kira"'},
                {"phones": '{"Dima": "+7 902 100-20-30", "Lena": "+7 903 200-30-40", "Max": "+7 904 300-40-50"}', "name": '"Lena"'},
                {"phones": '{"Dima": "+7 902 100-20-30", "Lena": "+7 903 200-30-40"}', "name": '"Misha"'}],
        intro="В телефоне есть записная книжка — словарь `phones`: ключ — имя, значение — номер телефона. "
              "Нужно найти номер человека по имени `name`. Иногда ищут того, кого в книжке нет, — "
              "тогда программа не должна падать с ошибкой.",
        steps=["Найди номер для `name` в словаре `phones` методом `.get()`. Если такого имени в книжке нет, "
               "вместо номера должна получиться строка `number not found` — передай её в `.get()` вторым аргументом.",
               "Выведи строку вида `Gena: +7 900 000-00-00` — имя, двоеточие, пробел и номер "
               "(или `number not found`, если имени в книжке нет)."],
        hint='Запись `phones["Gena"]` остановит программу с ошибкой `KeyError`, если такого ключа в словаре нет. '
             'А `.get()` в этом случае спокойно вернёт `None` — или то значение, которое ты передал ему вторым аргументом.',
        solution='phone = phones.get(name, "number not found")\nprint(f"{name}: {phone}")',
        wrong=[("берёт номер через квадратные скобки — для имени, которого нет в книжке, программа падает с KeyError",
                'print(f"{name}: {phones[name]}")'),
               ("вызывает .get() без второго аргумента — для отсутствующего имени печатается None",
                'print(f"{name}: {phones.get(name)}")')],
        constructs=["dict"],
        must_use=[("re:\\.get\\(", "Возьми номер через .get(): если имени нет в книжке, он не уронит программу, "
                                   "а вернёт запасное значение.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-dict-class-votes", title="Выборы старосты",
        given=["votes"],
        variants=[{"votes": '["Anya", "Boris", "Anya", "Vika", "Boris", "Anya"]'},
                  {"votes": '["Timur", "Sonya", "Sonya", "Timur", "Sonya", "Mila", "Sonya"]'},
                  {"votes": '["Gosha", "Dina", "Eva", "Dina", "Gosha"]'}],
        hidden=[{"votes": '["Ira"]'},
                {"votes": '["Lev", "Lev", "Lev", "Zoya"]'},
                {"votes": '["Yan", "Ada", "Yan", "Ada", "Kim", "Ada"]'}],
        intro="В классе выбирали старосту. Каждый ученик написал на листке одно имя, и все голоса по порядку "
              "записали в список `votes`. Нужно подсчитать, сколько голосов получил каждый кандидат.",
        steps=["Создай пустой словарь для подсчёта голосов: ключом в нём будет имя кандидата, значением — число его голосов. "
               "Пустой словарь — это пара фигурных скобок: `counts = {{}}`.",
               "Пройди циклом `for` по списку `votes` и для каждого имени увеличь его счётчик в словаре на 1. "
               "Если имени в словаре ещё нет, его счётчик должен стать равен 1.",
               "Пройди по словарю методом `.items()` и для каждого кандидата выведи строку вида `Gena: 7`. "
               "Кандидаты должны идти в том порядке, в котором они впервые встречаются в списке `votes`, — "
               "словарь как раз хранит ключи в порядке добавления."],
        hint="Метод `.get(key, 0)` возвращает значение по ключу, а если такого ключа ещё нет — `0`. "
             "Значит, новое значение счётчика — это то, что вернул `.get()`, плюс 1.",
        solution='counts = {}\nfor name in votes:\n    counts[name] = counts.get(name, 0) + 1\n'
                 'for name, number in counts.items():\n    print(f"{name}: {number}")',
        wrong=[("записывает 1 вместо того, чтобы прибавлять, — у каждого кандидата по одному голосу",
                'counts = {}\nfor name in votes:\n    counts[name] = 1\n'
                'for name, number in counts.items():\n    print(f"{name}: {number}")'),
               ("считает без словаря через .count() — один и тот же кандидат печатается несколько раз",
                'for name in votes:\n    print(f"{name}: {votes.count(name)}")')],
        constructs=["dict", "for"],
        must_use=[("Dict", "Считай голоса в словаре: создай пустой словарь фигурными скобками {} — ключом будет имя, "
                           "значением — число голосов."),
                  ("re:\\.items\\(", "Выведи результаты, пройдя по словарю методом .items(): он сразу даёт и имя, и число голосов.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-dict-warehouse", title="Привоз на склад",
        given=["stock", "delivery"],
        variants=[{"stock": '{"apples": 40, "pears": 25, "plums": 10}', "delivery": '{"pears": 15, "peaches": 20}'},
                  {"stock": '{"notebooks": 120, "pens": 300}', "delivery": '{"pens": 150, "rulers": 40, "notebooks": 30}'},
                  {"stock": '{"milk": 18, "kefir": 12, "cheese": 7, "butter": 9}', "delivery": '{"cheese": 10, "yogurt": 24}'}],
        hidden=[{"stock": '{"flour": 5}', "delivery": '{"flour": 5}'},
                {"stock": '{"nails": 100, "screws": 80}', "delivery": '{"dowels": 60, "bolts": 90}'},
                {"stock": '{"tea": 30, "coffee": 15, "cocoa": 8}', "delivery": '{"cocoa": 12, "coffee": 5, "tea": 1}'}],
        intro="На складе магазина остатки товаров хранятся в словаре `stock`: ключ — название товара, значение — "
              "сколько штук осталось. Приехала машина с товаром — что и сколько привезли, записано в словаре `delivery`. "
              "Нужно обновить склад.",
        steps=["Пройди по словарю `delivery` методом `.items()` — так на каждом шаге у тебя будут и название товара, "
               "и привезённое количество.",
               "Если товар уже есть в `stock`, прибавь привезённое количество к его остатку. Если такого товара "
               "на складе ещё не было, добавь его в `stock` с привезённым количеством.",
               "Выведи весь склад после привоза: для каждого товара из `stock` строку вида `bananas: 12` — в том порядке, "
               "в котором товары стоят в словаре (новые товары окажутся в конце).",
               "Последней строкой выведи строку вида `Total: 250` — сумму всех количеств на складе. "
               "Все значения словаря можно получить методом `.values()`."],
        hint="Если ключа в словаре ещё нет, запись `stock[item] = amount` просто создаст его, а `stock[item] += amount` "
             "упадёт с ошибкой `KeyError`: прибавлять не к чему. Поэтому новому товару нужна отдельная ветка `else` — "
             "или запасное значение из `.get(item, 0)`.",
        solution='for item, amount in delivery.items():\n    stock[item] = stock.get(item, 0) + amount\n'
                 'for item, amount in stock.items():\n    print(f"{item}: {amount}")\nprint(f"Total: {sum(stock.values())}")',
        wrong=[("перезаписывает остаток привезённым количеством вместо того, чтобы прибавить",
                'for item, amount in delivery.items():\n    stock[item] = amount\n'
                'for item, amount in stock.items():\n    print(f"{item}: {amount}")\nprint(f"Total: {sum(stock.values())}")'),
               ("обновляет только товары, которые уже были на складе, — новые не добавляются",
                'for item, amount in delivery.items():\n    if item in stock:\n        stock[item] += amount\n'
                'for item, amount in stock.items():\n    print(f"{item}: {amount}")\nprint(f"Total: {sum(stock.values())}")')],
        constructs=["dict", "for"],
        must_use=[("re:\\.items\\(", "Пройди по словарю delivery методом .items(): так на каждом шаге у тебя будут "
                                     "и товар, и количество.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-dict-fix-grade", title="Исправленная оценка",
        given=["grades", "subject", "new_grade"],
        variants=[{"grades": '{"math": 3, "history": 5, "biology": 4}', "subject": '"math"', "new_grade": "4"},
                  {"grades": '{"english": 4, "physics": 2}', "subject": '"physics"', "new_grade": "5"},
                  {"grades": '{"music": 5, "art": 5, "literature": 3, "chemistry": 4}', "subject": '"literature"',
                   "new_grade": "4"}],
        hidden=[{"grades": '{"pe": 2}', "subject": '"pe"', "new_grade": "3"},
                {"grades": '{"math": 5, "russian": 4, "geography": 3}', "subject": '"geography"', "new_grade": "5"},
                {"grades": '{"history": 4, "informatics": 3, "math": 4}', "subject": '"history"', "new_grade": "2"}],
        intro="В электронном дневнике четвертные оценки хранятся в словаре `grades`: ключ — предмет, значение — оценка. "
              "Ученик пересдал предмет `subject` и получил новую оценку `new_grade`.",
        steps=["Выведи строку вида `Old grade: 3` — оценку по предмету `subject` до пересдачи. Возьми её из словаря "
               "по ключу в квадратных скобках.",
               "Запиши в словарь по ключу `subject` новую оценку `new_grade`.",
               "Выведи весь словарь после изменения командой `print(grades)`."],
        hint="Запись `d[key] = value` меняет значение, если такой ключ уже есть, и не создаёт второй ключ — "
             "в словаре каждый ключ встречается только один раз. Старую оценку выведи до того, как перезапишешь её.",
        solution='print(f"Old grade: {grades[subject]}")\ngrades[subject] = new_grade\nprint(grades)',
        wrong=[("выводит старую оценку уже после изменения — печатается новая",
                'grades[subject] = new_grade\nprint(f"Old grade: {grades[subject]}")\nprint(grades)'),
               ("путает ключ и значение — в словаре появляется лишняя пара",
                'print(f"Old grade: {grades[subject]}")\ngrades[new_grade] = subject\nprint(grades)')],
        constructs=["dict"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-dict-screen-time", title="Время у экрана",
        given=["screen", "limit"],
        variants=[{"screen": '{"Mon": 2, "Tue": 3, "Wed": 1, "Thu": 4, "Fri": 3, "Sat": 6, "Sun": 5}', "limit": "3"},
                  {"screen": '{"Mon": 5, "Tue": 2, "Wed": 5, "Thu": 1, "Fri": 2}', "limit": "2"},
                  {"screen": '{"Sat": 4, "Sun": 7, "Mon": 1}', "limit": "4"}],
        hidden=[{"screen": '{"Mon": 1}', "limit": "1"},
                {"screen": '{"Mon": 3, "Tue": 3, "Wed": 3}', "limit": "5"},
                {"screen": '{"Mon": 0, "Tue": 8, "Wed": 2, "Thu": 9, "Fri": 9}', "limit": "1"}],
        intro="Телефон записывает, сколько часов в день ты провёл у экрана. Данные лежат в словаре `screen`: ключ — день "
              "недели, значение — число часов. Родители договорились с тобой, что больше `limit` часов в день — это перебор.",
        steps=["Сложи все значения словаря — их можно получить методом `.values()` — и выведи строку вида `Total: 20 h`.",
               "Пройди по словарю методом `.items()` и найди день с самым большим числом часов. Если таких дней несколько, "
               "нужен первый из них. Выведи строку вида `Most: Fri (6 h)`.",
               "Посчитай, в скольких днях часов было больше `limit`, и выведи строку вида `Days over limit: 2`."],
        hint="Самый большой день ищи так же, как самое большое число в списке: запомни первый день как лучший и заменяй "
             "его, только если часов строго больше. День, в котором ровно `limit` часов, перебором не считается.",
        solution='total = 0\nfor hours in screen.values():\n    total += hours\nprint(f"Total: {total} h")\n'
                 'best_day = ""\nbest_hours = -1\nover = 0\nfor day, hours in screen.items():\n'
                 '    if hours > best_hours:\n        best_day = day\n        best_hours = hours\n'
                 '    if hours > limit:\n        over += 1\nprint(f"Most: {best_day} ({best_hours} h)")\n'
                 'print(f"Days over limit: {over}")',
        wrong=[("при равенстве часов берёт последний день, а не первый",
                'total = 0\nfor hours in screen.values():\n    total += hours\nprint(f"Total: {total} h")\n'
                'best_day = ""\nbest_hours = -1\nover = 0\nfor day, hours in screen.items():\n'
                '    if hours >= best_hours:\n        best_day = day\n        best_hours = hours\n'
                '    if hours > limit:\n        over += 1\nprint(f"Most: {best_day} ({best_hours} h)")\n'
                'print(f"Days over limit: {over}")'),
               ("считает перебором и день ровно с limit часов",
                'total = 0\nfor hours in screen.values():\n    total += hours\nprint(f"Total: {total} h")\n'
                'best_day = ""\nbest_hours = -1\nover = 0\nfor day, hours in screen.items():\n'
                '    if hours > best_hours:\n        best_day = day\n        best_hours = hours\n'
                '    if hours >= limit:\n        over += 1\nprint(f"Most: {best_day} ({best_hours} h)")\n'
                'print(f"Days over limit: {over}")')],
        constructs=["dict", "for"],
        must_use=[("re:\\.items\\(", "Пройди по словарю методом .items(): так на каждом шаге у тебя будут и день, и часы.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-dict-game-inventory", title="Рюкзак героя",
        given=["inventory", "actions"],
        variants=[{"inventory": '{"apple": 2, "sword": 1}',
                   "actions": '[("take", "apple", 3), ("use", "potion", 1), ("use", "apple", 4), ("use", "sword", 1)]'},
                  {"inventory": '{"arrow": 10, "bread": 1}',
                   "actions": '[("use", "arrow", 4), ("use", "bread", 2), ("take", "potion", 2), ("use", "bread", 1)]'},
                  {"inventory": '{"gold": 50}',
                   "actions": '[("use", "gold", 50), ("take", "map", 1), ("take", "gold", 5), ("use", "gold", 6)]'}],
        hidden=[{"inventory": '{"key": 1}', "actions": '[("use", "key", 1)]'},
                {"inventory": '{"coin": 3, "rope": 1}', "actions": '[("take", "coin", 2), ("take", "torch", 4), ("use", "torch", 1)]'},
                {"inventory": '{"stone": 5}', "actions": '[("use", "stone", 6), ("use", "stone", 5), ("take", "stone", 1)]'}],
        intro="В игре рюкзак героя — словарь `inventory`: ключ — предмет, значение — сколько штук есть. Герой совершает "
              "действия из списка `actions`. Каждое действие — кортеж из трёх значений: `\"take\"` (взять) или "
              "`\"use\"` (использовать), название предмета и количество.",
        steps=["Пройди по списку `actions`, распаковывая каждый кортеж в три переменные.",
               "`take`: прибавь количество к запасу предмета; если предмета в рюкзаке ещё не было, он появляется "
               "с этим количеством.",
               "`use`: если предмета в рюкзаке меньше, чем нужно (или его нет совсем), выведи строку вида "
               "`Not enough potion` и ничего не меняй. Иначе уменьши запас; если он стал равен 0, удали предмет "
               "из словаря командой `del inventory[item]`.",
               "После всех действий выведи каждый предмет рюкзака строкой вида `apple: 5` в порядке словаря, "
               "а последней строкой — `Items: 2`, сколько разных предметов осталось."],
        hint="`inventory.get(item, 0)` вернёт 0 для предмета, которого нет в рюкзаке, — это удобно и при взятии, "
             "и при проверке запаса. Предмет, удалённый через `del` и потом взятый снова, встанет в конец словаря.",
        solution='for action, item, amount in actions:\n    if action == "take":\n'
                 '        inventory[item] = inventory.get(item, 0) + amount\n    else:\n'
                 '        have = inventory.get(item, 0)\n        if have < amount:\n            print(f"Not enough {item}")\n'
                 '        else:\n            inventory[item] = have - amount\n            if inventory[item] == 0:\n'
                 '                del inventory[item]\nfor item, count in inventory.items():\n    print(f"{item}: {count}")\n'
                 'print(f"Items: {len(inventory)}")',
        wrong=[("не удаляет закончившиеся предметы — в рюкзаке остаются предметы с нулём",
                'for action, item, amount in actions:\n    if action == "take":\n'
                '        inventory[item] = inventory.get(item, 0) + amount\n    else:\n'
                '        have = inventory.get(item, 0)\n        if have < amount:\n            print(f"Not enough {item}")\n'
                '        else:\n            inventory[item] = have - amount\nfor item, count in inventory.items():\n'
                '    print(f"{item}: {count}")\nprint(f"Items: {len(inventory)}")'),
               ("не проверяет запас — количество уходит в минус",
                'for action, item, amount in actions:\n    if action == "take":\n'
                '        inventory[item] = inventory.get(item, 0) + amount\n    else:\n'
                '        inventory[item] = inventory.get(item, 0) - amount\n        if inventory[item] == 0:\n'
                '            del inventory[item]\nfor item, count in inventory.items():\n    print(f"{item}: {count}")\n'
                'print(f"Items: {len(inventory)}")'),
               ("отказывает, даже когда предметов ровно столько, сколько нужно",
                'for action, item, amount in actions:\n    if action == "take":\n'
                '        inventory[item] = inventory.get(item, 0) + amount\n    else:\n'
                '        have = inventory.get(item, 0)\n        if have <= amount:\n            print(f"Not enough {item}")\n'
                '        else:\n            inventory[item] = have - amount\n            if inventory[item] == 0:\n'
                '                del inventory[item]\nfor item, count in inventory.items():\n    print(f"{item}: {count}")\n'
                'print(f"Items: {len(inventory)}")')],
        constructs=["dict", "for"],
        must_use=[("re:\\bdel\\s", "Убери закончившийся предмет из словаря командой del inventory[item].")],
    ),
]
