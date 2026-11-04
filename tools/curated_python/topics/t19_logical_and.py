"""PY_LOGICAL_AND — «Логическое and». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, += -=, f-strings, if/else, comparison operators.
Not yet: or/not, elif, truthiness of non-bool values, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_LOGICAL_AND"
AND = [("And", "Используй and, чтобы объединить проверки в одном условии")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-and-car-driver", title="Можно ли сесть за руль",
        given=["age", "has_license"],
        variants=[{"age": "19", "has_license": "True"}, {"age": "25", "has_license": "False"}, {"age": "17", "has_license": "True"}],
        hidden=[{"age": "18", "has_license": "True"}, {"age": "16", "has_license": "False"},
                {"age": "40", "has_license": "False"}, {"age": "30", "has_license": "True"}],
        intro="Прокат машин выдаёт автомобиль, только если клиенту 18 лет или больше **и** у него есть права. "
              "Возраст клиента — `age = {age}`, а есть ли права, записано в `has_license = {has_license}`.",
        steps=["Выведи через `print` с запятой `Age OK:` и результат сравнения: 18 лет или больше.",
               "Выведи `License:` и значение `has_license`.",
               "Если оба условия выполнены одновременно, выведи `You can drive`, иначе — `No car for you`. "
               "Объедини обе проверки в одном условии с помощью `and`.",
               "Например, для 18 лет и прав программа выводит `Age OK: True`, `License: True`, `You can drive`."],
        hint="`and` даёт `True`, только когда истинны обе части: `True and False` — это `False`. "
             "Переменную `has_license` уже не нужно сравнивать с `True` — она сама является `True` или `False`.",
        solution='print("Age OK:", age >= 18)\nprint("License:", has_license)\nif age >= 18 and has_license:\n'
                 '    print("You can drive")\nelse:\n    print("No car for you")',
        wrong=[("строгое сравнение в условии: в 18 лет машину не дают",
                'print("Age OK:", age >= 18)\nprint("License:", has_license)\nif age > 18 and has_license:\n'
                '    print("You can drive")\nelse:\n    print("No car for you")'),
               ("проверяет только возраст, про права забыли",
                'print("Age OK:", age >= 18)\nprint("License:", has_license)\nif age >= 18:\n'
                '    print("You can drive")\nelse:\n    print("No car for you")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-and-tea-temperature", title="Чай нужной температуры",
        given=["temp"],
        variants=[{"temp": "58"}, {"temp": "85"}, {"temp": "42"}],
        hidden=[{"temp": "50"}, {"temp": "65"}, {"temp": "49"}, {"temp": "66"}],
        intro="Умная кружка подсказывает, можно ли пить чай. Чай приятно пить, если его температура от 50 до 65 "
              "градусов включительно. Сейчас температура чая `temp = {temp}`.",
        steps=["Выведи `Tea:`, `temp` и `C` через `print` с запятыми.",
               "Если `temp` не меньше 50 **и** не больше 65, выведи `Just right`.",
               "Иначе выведи `Not now`.",
               "Последней строкой (в любом случае) выведи `Enjoy your tea`.",
               "Например, для 50 градусов программа выводит `Tea: 50 C`, `Just right`, `Enjoy your tea`."],
        hint="«От 50 до 65 включительно» — это две проверки: `temp >= 50` и `temp <= 65`. "
             "Соедини их через `and`. Граничные значения 50 и 65 тоже подходят.",
        solution='print("Tea:", temp, "C")\nif temp >= 50 and temp <= 65:\n    print("Just right")\nelse:\n'
                 '    print("Not now")\nprint("Enjoy your tea")',
        wrong=[("строгое сравнение: ровно 65 градусов не подходит",
                'print("Tea:", temp, "C")\nif temp >= 50 and temp < 65:\n    print("Just right")\nelse:\n'
                '    print("Not now")\nprint("Enjoy your tea")'),
               ("проверяет только нижнюю границу",
                'print("Tea:", temp, "C")\nif temp >= 50:\n    print("Just right")\nelse:\n'
                '    print("Not now")\nprint("Enjoy your tea")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-and-friday-coupon", title="Купон выходного дня",
        given=["price", "count", "day"],
        variants=[{"price": "350", "count": "4", "day": '"friday"'}, {"price": "290", "count": "3", "day": '"friday"'},
                  {"price": "520", "count": "2", "day": '"monday"'}],
        hidden=[{"price": "250", "count": "4", "day": '"friday"'}, {"price": "999", "count": "1", "day": '"friday"'},
                {"price": "600", "count": "5", "day": '"sunday"'}, {"price": "100", "count": "3", "day": '"monday"'}],
        intro="Магазин даёт скидку 200 руб., если покупка стоит 1000 руб. или больше **и** сегодня пятница. "
              "Покупатель берёт `count = {count}` товаров по `price = {price}` руб., сегодня `day = {day}`.",
        steps=["Посчитай стоимость покупки (`price` умножить на `count`), сохрани в `total` и выведи "
               "f-строкой `Total: <total> rub`.",
               "Если `total` не меньше 1000 **и** `day` равен `\"friday\"`, уменьши `total` на 200 с помощью `-=` "
               "и выведи `Coupon applied`.",
               "Иначе выведи `No coupon`.",
               "В конце (в любом случае) выведи `To pay: <total> rub`.",
               "Например, для 4 товаров по 250 руб. в пятницу программа выводит `Total: 1000 rub`, `Coupon applied`, "
               "`To pay: 800 rub`."],
        hint="Оба условия пишутся полностью: `total >= 1000 and day == \"friday\"`. "
             "Покупка ровно на 1000 руб. тоже получает скидку.",
        solution='total = price * count\nprint(f"Total: {total} rub")\nif total >= 1000 and day == "friday":\n'
                 '    total -= 200\n    print("Coupon applied")\nelse:\n    print("No coupon")\nprint(f"To pay: {total} rub")',
        wrong=[("строгое сравнение: покупка ровно на 1000 руб. без скидки",
                'total = price * count\nprint(f"Total: {total} rub")\nif total > 1000 and day == "friday":\n'
                '    total -= 200\n    print("Coupon applied")\nelse:\n    print("No coupon")\nprint(f"To pay: {total} rub")'),
               ("пишет =- вместо -=: сумма становится отрицательной",
                'total = price * count\nprint(f"Total: {total} rub")\nif total >= 1000 and day == "friday":\n'
                '    total =- 200\n    print("Coupon applied")\nelse:\n    print("No coupon")\nprint(f"To pay: {total} rub")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-and-exam-parts", title="Зачёт из двух частей",
        given=["theory", "practice"],
        variants=[{"theory": "55", "practice": "60"}, {"theory": "35", "practice": "80"}, {"theory": "48", "practice": "45"}],
        hidden=[{"theory": "40", "practice": "60"}, {"theory": "50", "practice": "39"}, {"theory": "45", "practice": "50"},
                {"theory": "90", "practice": "90"}],
        intro="Зачёт состоит из теории и практики, за каждую часть дают до 100 баллов. Зачёт сдан, если за теорию "
              "не меньше 40 баллов, **и** за практику не меньше 40, **и** в сумме не меньше 100. "
              "Ученик набрал `theory = {theory}` и `practice = {practice}`.",
        steps=["Посчитай сумму баллов, сохрани в `total` и выведи f-строкой `Total: <total>`.",
               "Выведи f-строкой `Both parts: <True/False>` — результат проверки, что обе части не меньше 40 "
               "(две проверки через `and`).",
               "Если выполнены все три условия, выведи `Passed`, иначе — `Failed`.",
               "Например, для 45 и 50 баллов программа выводит `Total: 95`, `Both parts: True`, `Failed`."],
        hint="Через `and` можно соединить больше двух проверок: `a >= 1 and b >= 1 and c >= 1`. "
             "Результат `and` тоже можно напечатать внутри f-строки.",
        solution='total = theory + practice\nprint(f"Total: {total}")\nprint(f"Both parts: {theory >= 40 and practice >= 40}")\n'
                 'if theory >= 40 and practice >= 40 and total >= 100:\n    print("Passed")\nelse:\n    print("Failed")',
        wrong=[("в условии забыта проверка суммы",
                'total = theory + practice\nprint(f"Total: {total}")\nprint(f"Both parts: {theory >= 40 and practice >= 40}")\n'
                'if theory >= 40 and practice >= 40:\n    print("Passed")\nelse:\n    print("Failed")'),
               ("строгое сравнение: ровно 40 баллов за теорию не засчитываются",
                'total = theory + practice\nprint(f"Total: {total}")\nprint(f"Both parts: {theory >= 40 and practice >= 40}")\n'
                'if theory > 40 and practice >= 40 and total >= 100:\n    print("Passed")\nelse:\n    print("Failed")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-and-triangle", title="Треугольник из палочек",
        given=["a", "b", "c"],
        variants=[{"a": "3", "b": "4", "c": "5"}, {"a": "2", "b": "9", "c": "4"}, {"a": "6", "b": "6", "c": "6"}],
        hidden=[{"a": "1", "b": "2", "c": "3"}, {"a": "10", "b": "3", "c": "4"}, {"a": "5", "b": "5", "c": "5"},
                {"a": "2", "b": "3", "c": "9"}, {"a": "7", "b": "7", "c": "3"}],
        intro="Петя хочет сложить треугольник из трёх палочек длиной `a = {a}`, `b = {b}` и `c = {c}` см. "
              "Треугольник получится, только если каждая палочка короче двух других вместе.",
        steps=["Если `a` меньше `b + c`, **и** `b` меньше `a + c`, **и** `c` меньше `a + b`, выведи `Triangle` "
               "и второй строкой f-строку `Perimeter: <a + b + c>`.",
               "Иначе выведи `No triangle`.",
               "После этого отдельным `if`/`else` проверь, равны ли все три палочки (`a` равна `b` **и** `b` равна `c`): "
               "если да, выведи `All equal`, иначе — `Not all equal`.",
               "Например, для палочек 5, 5 и 5 программа выводит `Triangle`, `Perimeter: 15`, `All equal`, "
               "а для 1, 2 и 3 — `No triangle`, `Not all equal`."],
        hint="Если одна палочка ровно равна сумме двух других, треугольник сплющится в отрезок — поэтому сравнение строгое `<`. "
             "Нужно проверить все три палочки, а не две.",
        solution='if a < b + c and b < a + c and c < a + b:\n    print("Triangle")\n    print(f"Perimeter: {a + b + c}")\n'
                 'else:\n    print("No triangle")\nif a == b and b == c:\n    print("All equal")\nelse:\n    print("Not all equal")',
        wrong=[("<= вместо <: сплющенный треугольник 1, 2, 3 считается настоящим",
                'if a <= b + c and b <= a + c and c <= a + b:\n    print("Triangle")\n    print(f"Perimeter: {a + b + c}")\n'
                'else:\n    print("No triangle")\nif a == b and b == c:\n    print("All equal")\nelse:\n    print("Not all equal")'),
               ("проверяет только две палочки из трёх",
                'if a < b + c and b < a + c:\n    print("Triangle")\n    print(f"Perimeter: {a + b + c}")\n'
                'else:\n    print("No triangle")\nif a == b and b == c:\n    print("All equal")\nelse:\n    print("Not all equal")'),
               ("для равенства проверяет только две палочки",
                'if a < b + c and b < a + c and c < a + b:\n    print("Triangle")\n    print(f"Perimeter: {a + b + c}")\n'
                'else:\n    print("No triangle")\nif a == b:\n    print("All equal")\nelse:\n    print("Not all equal")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-and-bank-transfer", title="Перевод с дневным лимитом",
        given=["balance", "sent", "amount"],
        variants=[{"balance": "12000", "sent": "30000", "amount": "8000"},
                  {"balance": "5000", "sent": "10000", "amount": "6500"},
                  {"balance": "40000", "sent": "45000", "amount": "7000"}],
        hidden=[{"balance": "3000", "sent": "0", "amount": "3000"}, {"balance": "9000", "sent": "42000", "amount": "8000"},
                {"balance": "100000", "sent": "49000", "amount": "1000"}, {"balance": "200", "sent": "500", "amount": "300"}],
        intro="Банк разрешает переводить не больше 50000 руб. в день. Сегодня клиент уже перевёл `sent = {sent}` руб., "
              "на счету у него `balance = {balance}` руб., и он хочет перевести ещё `amount = {amount}` руб. "
              "Перевод проходит, только если денег на счету хватает **и** дневной лимит не превышен.",
        steps=["Посчитай, сколько ещё можно перевести сегодня: 50000 минус `sent` — и сохрани в `left_today`.",
               "С помощью f-строк выведи `Balance: <balance> rub` и `Left today: <left_today> rub`.",
               "Если `amount` не больше `balance` **и** `amount` не больше `left_today`, уменьши `balance` на `amount` "
               "с помощью `-=` и выведи `Sent <amount> rub`. Иначе выведи `Refused`.",
               "В конце (в любом случае) выведи `New balance: <balance> rub`.",
               "Например, для баланса 3000, `sent = 0` и перевода 3000 руб. программа выводит `Balance: 3000 rub`, "
               "`Left today: 50000 rub`, `Sent 3000 rub`, `New balance: 0 rub`."],
        hint="«Не больше» — это `<=`: перевести ровно весь остаток на счету или ровно остаток лимита можно. "
             "Новый баланс печатается после `if`/`else`, без отступа.",
        solution='left_today = 50000 - sent\nprint(f"Balance: {balance} rub")\nprint(f"Left today: {left_today} rub")\n'
                 'if amount <= balance and amount <= left_today:\n    balance -= amount\n    print(f"Sent {amount} rub")\n'
                 'else:\n    print("Refused")\nprint(f"New balance: {balance} rub")',
        wrong=[("строгое сравнение: нельзя перевести ровно всё, что есть на счету",
                'left_today = 50000 - sent\nprint(f"Balance: {balance} rub")\nprint(f"Left today: {left_today} rub")\n'
                'if amount < balance and amount <= left_today:\n    balance -= amount\n    print(f"Sent {amount} rub")\n'
                'else:\n    print("Refused")\nprint(f"New balance: {balance} rub")'),
               ("прибавляет уже переведённое к лимиту вместо вычитания",
                'left_today = 50000 + sent\nprint(f"Balance: {balance} rub")\nprint(f"Left today: {left_today} rub")\n'
                'if amount <= balance and amount <= left_today:\n    balance -= amount\n    print(f"Sent {amount} rub")\n'
                'else:\n    print("Refused")\nprint(f"New balance: {balance} rub")')],
        constructs=["if"],
        must_use=AND,
    ),
]
