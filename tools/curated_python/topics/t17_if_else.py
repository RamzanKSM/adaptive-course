"""PY_IF_ELSE_BASIC — «Условия if / else». Taught before: print, variables, arithmetic, int/float, strings, type
conversion, // and %, += -=, f-strings. Simple comparisons (>, >=, ==) come together with the condition itself.
Not yet: elif, and/or/not, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_IF_ELSE_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-if-ride-height", title="Пропуск на горки",
        given=["height"],
        variants=[{"height": "135"}, {"height": "110"}, {"height": "152"}],
        hidden=[{"height": "120"}, {"height": "119"}, {"height": "98"}, {"height": "171"}],
        intro="На американские горки пускают детей ростом от 120 см и выше. "
              "Рост посетителя в сантиметрах записан в переменной: `height = {height}`.",
        steps=["Если `height` равен 120 или больше, выведи `You can ride`.",
               "Иначе выведи `Not yet`.",
               "Программа должна вывести ровно одну строку."],
        hint="«120 или больше» — это сравнение `>=`, а не `>`: с `>` ребёнка ростом ровно 120 см не пустят. "
             "Не забудь двоеточие после условия и после `else`, а команды внутри веток пиши с отступом.",
        solution='if height >= 120:\n    print("You can ride")\nelse:\n    print("Not yet")',
        wrong=[("строгое сравнение: ребёнка ростом ровно 120 см не пускают",
                'if height > 120:\n    print("You can ride")\nelse:\n    print("Not yet")'),
               ("нет else: вторая надпись печатается всегда",
                'if height >= 120:\n    print("You can ride")\nprint("Not yet")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-if-pairs", title="Разбиваемся на пары",
        given=["students"],
        variants=[{"students": "24"}, {"students": "17"}, {"students": "30"}],
        hidden=[{"students": "2"}, {"students": "1"}, {"students": "15"}, {"students": "28"}],
        intro="На физкультуре класс встаёт в пары. Сколько учеников сегодня пришло, записано в переменной `students = {students}`. "
              "Нужно узнать, хватит ли каждому пары, и сколько получится пар.",
        steps=["Проверь, делится ли `students` на 2 без остатка — для этого есть оператор `%`.",
               "Если делится, выведи `Everyone has a pair`, иначе выведи `One has no pair`.",
               "После условия (в любом случае) выведи второй строкой число полных пар в формате `Pairs: 5`. "
               "Число пар — это `students`, делённое на 2 нацело."],
        hint="У чётного числа остаток от деления на 2 равен 0: `8 % 2` даёт `0`, а `9 % 2` даёт `1`. "
             "Деление нацело делает оператор `//`: `9 // 2` даёт `4`, без дробной части.",
        solution='if students % 2 == 0:\n    print("Everyone has a pair")\nelse:\n    print("One has no pair")\n'
                 'print(f"Pairs: {students // 2}")',
        wrong=[("путает // и %: проверяет частное вместо остатка",
                'if students // 2 == 0:\n    print("Everyone has a pair")\nelse:\n    print("One has no pair")\n'
                'print(f"Pairs: {students // 2}")'),
               ("делит через / — число пар получается дробным",
                'if students % 2 == 0:\n    print("Everyone has a pair")\nelse:\n    print("One has no pair")\n'
                'print(f"Pairs: {students / 2}")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-if-free-delivery", title="Бесплатная доставка",
        given=["price", "count"],
        variants=[{"price": "450", "count": "3"}, {"price": "700", "count": "4"}, {"price": "390", "count": "5"}],
        hidden=[{"price": "500", "count": "4"}, {"price": "999", "count": "2"}, {"price": "120", "count": "1"},
                {"price": "1200", "count": "3"}],
        intro="Интернет-магазин привозит заказ бесплатно, если товары в нём стоят 2000 руб. или больше, "
              "а иначе доставка стоит 300 руб. Покупатель берёт несколько одинаковых товаров: их количество — `count = {count}`, "
              "а цена одной штуки — `price = {price}` руб.",
        steps=["Посчитай стоимость товаров: `price`, умноженная на `count`.",
               "Если стоимость товаров 2000 или больше, доставка стоит 0 руб., иначе — 300 руб.",
               "Выведи три строки: стоимость товаров, стоимость доставки и сумму к оплате (товары плюс доставка). "
               "Например, для товаров на 1500 руб. это `Goods: 1500 rub`, `Delivery: 300 rub` и `To pay: 1800 rub`"],
        hint="Сначала сохрани стоимость товаров в переменную, затем в `if` и в `else` запиши в другую переменную "
             "цену доставки. Тогда после условия останется только вывести три строки через f-строки.",
        solution='total = price * count\nif total >= 2000:\n    delivery = 0\nelse:\n    delivery = 300\n'
                 'print(f"Goods: {total} rub")\nprint(f"Delivery: {delivery} rub")\n'
                 'print(f"To pay: {total + delivery} rub")',
        wrong=[("строгое сравнение: заказ ровно на 2000 руб. платит за доставку",
                'total = price * count\nif total > 2000:\n    delivery = 0\nelse:\n    delivery = 300\n'
                'print(f"Goods: {total} rub")\nprint(f"Delivery: {delivery} rub")\n'
                'print(f"To pay: {total + delivery} rub")'),
               ("забывает прибавить доставку к сумме к оплате",
                'total = price * count\nif total >= 2000:\n    delivery = 0\nelse:\n    delivery = 300\n'
                'print(f"Goods: {total} rub")\nprint(f"Delivery: {delivery} rub")\n'
                'print(f"To pay: {total} rub")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-if-phone-battery", title="Заряд телефона",
        given=["charge"],
        variants=[{"charge": "15"}, {"charge": "64"}, {"charge": "8"}],
        hidden=[{"charge": "20"}, {"charge": "19"}, {"charge": "100"}, {"charge": "3"}],
        intro="Телефон напоминает поставить его на зарядку, когда заряда осталось меньше 20 процентов. "
              "Сколько процентов заряда сейчас, записано в переменной: `charge = {charge}`.",
        steps=["Если `charge` равен 20 или больше, выведи `Battery OK`.",
               "Иначе выведи `Please charge`.",
               "Программа должна вывести ровно одну строку."],
        hint="«20 или больше» записывается как `charge >= 20`. При ровно 20 процентах напоминания ещё нет. "
             "После условия и после `else` нужно двоеточие, а `print` внутри веток пишется с отступом.",
        solution='if charge >= 20:\n    print("Battery OK")\nelse:\n    print("Please charge")',
        wrong=[("строгое сравнение: при ровно 20 процентах просит зарядить",
                'if charge > 20:\n    print("Battery OK")\nelse:\n    print("Please charge")'),
               ("ветки перепутаны местами",
                'if charge >= 20:\n    print("Please charge")\nelse:\n    print("Battery OK")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-if-phone-minutes", title="Минуты по тарифу",
        given=["minutes"],
        variants=[{"minutes": "340"}, {"minutes": "125"}, {"minutes": "410"}],
        hidden=[{"minutes": "300"}, {"minutes": "301"}, {"minutes": "0"}, {"minutes": "299"}],
        intro="В тариф мобильной связи входит 300 минут разговоров в месяц. Каждая минута сверх них стоит 2 руб. "
              "Сколько минут абонент проговорил за месяц, записано в `minutes = {minutes}`.",
        steps=["Сначала выведи строку с потраченными минутами в формате `Used: 120 min`.",
               "Если `minutes` больше 300, выведи второй строкой доплату: лишние минуты (сверх 300), умноженные на 2, "
               "в формате `Extra: 20 rub`.",
               "Иначе выведи второй строкой, сколько минут ещё осталось из 300, в формате `Left: 180 min`."],
        hint="Ровно 300 минут — это ещё не «больше 300»: доплаты нет, осталось `0` минут. "
             "Лишние минуты — это `minutes - 300`, оставшиеся — `300 - minutes`.",
        solution='print(f"Used: {minutes} min")\nif minutes > 300:\n    print(f"Extra: {(minutes - 300) * 2} rub")\n'
                 'else:\n    print(f"Left: {300 - minutes} min")',
        wrong=[("забывает умножить лишние минуты на цену",
                'print(f"Used: {minutes} min")\nif minutes > 300:\n    print(f"Extra: {minutes - 300} rub")\n'
                'else:\n    print(f"Left: {300 - minutes} min")'),
               ("берёт за все минуты, а не только за лишние",
                'print(f"Used: {minutes} min")\nif minutes > 300:\n    print(f"Extra: {minutes * 2} rub")\n'
                'else:\n    print(f"Left: {300 - minutes} min")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-if-parking", title="Оплата парковки",
        given=["start", "end"],
        variants=[{"start": "9", "end": "14"}, {"start": "10", "end": "11"}, {"start": "8", "end": "17"}],
        hidden=[{"start": "12", "end": "14"}, {"start": "13", "end": "16"}, {"start": "7", "end": "7"},
                {"start": "6", "end": "22"}],
        intro="На парковке у торгового центра первые 2 часа бесплатные, а каждый следующий час стоит 60 руб. "
              "Машина заехала в `start = {start}` часов, а уехала в `end = {end}` часов того же дня.",
        steps=["Посчитай, сколько часов машина стояла: `end` минус `start`.",
               "Если она стояла больше 2 часов, платных часов столько, сколько получилось сверх двух. Иначе платных часов 0.",
               "Выведи три строки: сколько часов машина стояла, сколько из них платных и сколько нужно заплатить "
               "(платные часы, умноженные на 60). Например, для 4 часов это `Time: 4 h`, `Paid: 2 h` и `Cost: 120 rub`"],
        hint="Сохрани время стоянки в одну переменную, а в `if` и в `else` запиши в другую переменную число платных часов. "
             "После условия останется вывести три строки через f-строки.",
        solution='hours = end - start\nif hours > 2:\n    paid = hours - 2\nelse:\n    paid = 0\n'
                 'print(f"Time: {hours} h")\nprint(f"Paid: {paid} h")\nprint(f"Cost: {paid * 60} rub")',
        wrong=[("не вычитает бесплатные часы",
                'hours = end - start\nif hours > 2:\n    paid = hours\nelse:\n    paid = 0\n'
                'print(f"Time: {hours} h")\nprint(f"Paid: {paid} h")\nprint(f"Cost: {paid * 60} rub")'),
               ("нет else: при короткой стоянке платные часы уходят в минус",
                'hours = end - start\npaid = hours - 2\n'
                'print(f"Time: {hours} h")\nprint(f"Paid: {paid} h")\nprint(f"Cost: {paid * 60} rub")')],
        constructs=["if"],
    ),
]
