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
]
