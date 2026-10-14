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
]
