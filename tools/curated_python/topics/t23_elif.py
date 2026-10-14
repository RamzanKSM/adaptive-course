"""PY_ELIF — «Цепочки elif». Taught before: if/else, comparisons, and, or/not, f-strings, arithmetic, strings.
Not yet: loops, lists, functions."""
from build import OutputTask

SKILL = "PY_ELIF"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-elif-test-grade", title="Оценка за тест",
        given=["score"],
        variants=[{"score": "87"}, {"score": "93"}, {"score": "61"}],
        hidden=[{"score": "90"}, {"score": "75"}, {"score": "50"}, {"score": "49"}, {"score": "100"}],
        intro="За тест можно набрать от 0 до 100 баллов. Результат ученика записан в переменной `score = {score}`. Программа должна сказать, какая это оценка.",
        steps=["Если баллов `90` или больше, выведи `excellent`.",
               "Иначе, если баллов `75` или больше, выведи `good`.",
               "Иначе, если баллов `50` или больше, выведи `pass`.",
               "Во всех остальных случаях выведи `fail`."],
        hint="Проверяй пороги сверху вниз: от самого высокого к самому низкому. Как только одно условие сработало, "
             "остальные ветки `elif` и `else` уже не проверяются.",
        solution='if score >= 90:\n    print("excellent")\nelif score >= 75:\n    print("good")\n'
                 'elif score >= 50:\n    print("pass")\nelse:\n    print("fail")',
        wrong=[("строгие сравнения: ровно 90 баллов уже не «excellent»",
                'if score > 90:\n    print("excellent")\nelif score > 75:\n    print("good")\n'
                'elif score > 50:\n    print("pass")\nelse:\n    print("fail")'),
               ("пороги снизу вверх: всё от 50 и выше становится «pass»",
                'if score >= 50:\n    print("pass")\nelif score >= 75:\n    print("good")\n'
                'elif score >= 90:\n    print("excellent")\nelse:\n    print("fail")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-elif-clothes", title="Что надеть на улицу",
        given=["temperature"],
        variants=[{"temperature": "-5"}, {"temperature": "10"}, {"temperature": "28"}],
        hidden=[{"temperature": "0"}, {"temperature": "15"}, {"temperature": "25"}, {"temperature": "-20"}, {"temperature": "19"}],
        intro="Утром программа смотрит на температуру за окном — `temperature = {temperature}` градусов — и подсказывает, как одеться.",
        steps=["Если температура ниже `0`, выведи `Wear a warm coat`.",
               "Иначе, если ниже `15`, выведи `Wear a jacket`.",
               "Иначе, если ниже `25`, выведи `A sweater is fine`.",
               "Иначе выведи `T-shirt weather`."],
        hint="«Ниже 15» — это `temperature < 15`. Ровно 15 градусов уже не ниже 15, поэтому при 15 программа "
             "должна перейти к следующей проверке.",
        solution='if temperature < 0:\n    print("Wear a warm coat")\nelif temperature < 15:\n    print("Wear a jacket")\n'
                 'elif temperature < 25:\n    print("A sweater is fine")\nelse:\n    print("T-shirt weather")',
        wrong=[("нестрогие сравнения: при 0 градусов советует пуховик",
                'if temperature <= 0:\n    print("Wear a warm coat")\nelif temperature <= 15:\n    print("Wear a jacket")\n'
                'elif temperature <= 25:\n    print("A sweater is fine")\nelse:\n    print("T-shirt weather")'),
               ("отдельные if вместо цепочки: при морозе печатает несколько советов",
                'if temperature < 0:\n    print("Wear a warm coat")\nif temperature < 15:\n    print("Wear a jacket")\n'
                'if temperature < 25:\n    print("A sweater is fine")\nelse:\n    print("T-shirt weather")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-elif-ticket-price", title="Цена билета в музей",
        given=["age", "is_student"],
        variants=[{"age": "5", "is_student": "False"}, {"age": "20", "is_student": "True"}, {"age": "70", "is_student": "False"}],
        hidden=[{"age": "30", "is_student": "False"}, {"age": "16", "is_student": "False"}, {"age": "7", "is_student": "False"},
                {"age": "65", "is_student": "True"}, {"age": "18", "is_student": "False"}, {"age": "3", "is_student": "False"}],
        intro="В музее цена билета зависит от возраста посетителя и от того, учится ли он: `age = {age}`, `is_student = {is_student}`.",
        steps=["Если посетителю меньше `7` лет, билет стоит `0` рублей.",
               "Иначе, если ему меньше `18` лет **или** он студент, билет стоит `150` рублей.",
               "Иначе, если ему `65` лет или больше, билет стоит `100` рублей.",
               "Во всех остальных случаях билет стоит `300` рублей. Выведи цену в виде `Ticket price: 150` — "
               "после двоеточия пробел, потом число."],
        hint="Условия проверяются по порядку, и срабатывает первое подходящее. Поэтому студенту 65 лет "
             "достанется цена из второго правила, а не из третьего.",
        solution='if age < 7:\n    price = 0\nelif age < 18 or is_student:\n    price = 150\n'
                 'elif age >= 65:\n    price = 100\nelse:\n    price = 300\nprint(f"Ticket price: {price}")',
        wrong=[("and вместо or: школьник без студенческого платит как взрослый",
                'if age < 7:\n    price = 0\nelif age < 18 and is_student:\n    price = 150\n'
                'elif age >= 65:\n    price = 100\nelse:\n    price = 300\nprint(f"Ticket price: {price}")'),
               ("забыт порог для детей до 7 лет",
                'if age < 18 or is_student:\n    price = 150\n'
                'elif age >= 65:\n    price = 100\nelse:\n    price = 300\nprint(f"Ticket price: {price}")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-elif-greeting", title="Приветствие по времени суток",
        given=["hour"],
        variants=[{"hour": "9"}, {"hour": "15"}, {"hour": "21"}],
        hidden=[{"hour": "5"}, {"hour": "6"}, {"hour": "12"}, {"hour": "18"}, {"hour": "0"}],
        intro="Умная колонка здоровается по-разному в зависимости от времени суток. Сейчас `hour = {hour}` часов (от 0 до 23).",
        steps=["Если `hour` меньше `6`, выведи `Good night`.",
               "Иначе, если меньше `12`, выведи `Good morning`.",
               "Иначе, если меньше `18`, выведи `Good afternoon`.",
               "Во всех остальных случаях выведи `Good evening`."],
        hint="Проверяй пороги по порядку, от раннего к позднему. Ровно в 12 часов уже не «меньше 12», "
             "поэтому сработает следующая ветка — `Good afternoon`.",
        solution='if hour < 6:\n    print("Good night")\nelif hour < 12:\n    print("Good morning")\n'
                 'elif hour < 18:\n    print("Good afternoon")\nelse:\n    print("Good evening")',
        wrong=[("нестрогие сравнения: в 12 часов всё ещё «утро»",
                'if hour <= 6:\n    print("Good night")\nelif hour <= 12:\n    print("Good morning")\n'
                'elif hour <= 18:\n    print("Good afternoon")\nelse:\n    print("Good evening")'),
               ("отдельные if вместо цепочки: печатает несколько приветствий",
                'if hour < 6:\n    print("Good night")\nif hour < 12:\n    print("Good morning")\n'
                'if hour < 18:\n    print("Good afternoon")\nelse:\n    print("Good evening")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-elif-luggage", title="Багаж в самолёте",
        given=["weight"],
        variants=[{"weight": "14"}, {"weight": "8"}, {"weight": "26"}],
        hidden=[{"weight": "10"}, {"weight": "11"}, {"weight": "20"}, {"weight": "30"}, {"weight": "31"}],
        intro="Авиакомпания берёт плату за чемодан в зависимости от его веса. Чемодан пассажира весит `weight = {weight}` кг.",
        steps=["Если вес больше `30` кг, выведи `Too heavy` — такой чемодан не примут.",
               "Иначе, если больше `20` кг, выведи `Fee: 1500 rub`.",
               "Иначе, если больше `10` кг, выведи `Fee: 500 rub`.",
               "Иначе выведи `Free`."],
        hint="Здесь пороги идут сверху вниз: сначала самый тяжёлый случай. Чемодан ровно 20 кг не «больше 20», "
             "поэтому он попадает в ветку с платой 500 руб.",
        solution='if weight > 30:\n    print("Too heavy")\nelif weight > 20:\n    print("Fee: 1500 rub")\n'
                 'elif weight > 10:\n    print("Fee: 500 rub")\nelse:\n    print("Free")',
        wrong=[("пороги снизу вверх: всё тяжелее 10 кг стоит 500 руб.",
                'if weight > 10:\n    print("Fee: 500 rub")\nelif weight > 20:\n    print("Fee: 1500 rub")\n'
                'elif weight > 30:\n    print("Too heavy")\nelse:\n    print("Free")'),
               ("нестрогие сравнения: чемодан ровно 10 кг платный",
                'if weight >= 30:\n    print("Too heavy")\nelif weight >= 20:\n    print("Fee: 1500 rub")\n'
                'elif weight >= 10:\n    print("Fee: 500 rub")\nelse:\n    print("Free")')],
        constructs=["if"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-elif-shop-discount", title="Скидка в магазине",
        given=["total", "has_card"],
        variants=[{"total": "2400", "has_card": "True"}, {"total": "6000", "has_card": "False"},
                  {"total": "1500", "has_card": "True"}],
        hidden=[{"total": "5000", "has_card": "True"}, {"total": "2000", "has_card": "True"},
                {"total": "3000", "has_card": "False"}, {"total": "800", "has_card": "False"},
                {"total": "1999", "has_card": "True"}],
        intro="Магазин даёт скидку в процентах. Покупка стоит `total = {total}` руб., а есть ли у покупателя "
              "карта магазина, записано в `has_card = {has_card}`.",
        steps=["Если `total` не меньше `5000`, скидка `15` процентов — с картой или без.",
               "Иначе, если `total` не меньше `2000` **и** есть карта, скидка `10` процентов.",
               "Иначе, если есть карта, скидка `5` процентов. Во всех остальных случаях скидки нет — `0` процентов.",
               "Посчитай сумму скидки в рублях: `total * percent // 100`, где `percent` — процент скидки. Выведи две строки: процент в формате "
               "`Discount: 10%` и сумму к оплате (покупка минус скидка) в формате `To pay: 900 rub`"],
        hint="Сохрани процент в переменную `percent` в каждой ветке, а считай и печатай уже после цепочки. "
             "Условия проверяются по порядку, поэтому покупатель с картой на 6000 руб. получит 15%, а не 10%.",
        solution='if total >= 5000:\n    percent = 15\nelif total >= 2000 and has_card:\n    percent = 10\n'
                 'elif has_card:\n    percent = 5\nelse:\n    percent = 0\n'
                 'discount = total * percent // 100\nprint(f"Discount: {percent}%")\nprint(f"To pay: {total - discount} rub")',
        wrong=[("or вместо and: 10% получает любой, кто купил на 2000 руб.",
                'if total >= 5000:\n    percent = 15\nelif total >= 2000 or has_card:\n    percent = 10\n'
                'elif has_card:\n    percent = 5\nelse:\n    percent = 0\n'
                'discount = total * percent // 100\nprint(f"Discount: {percent}%")\nprint(f"To pay: {total - discount} rub")'),
               ("печатает скидку вместо суммы к оплате",
                'if total >= 5000:\n    percent = 15\nelif total >= 2000 and has_card:\n    percent = 10\n'
                'elif has_card:\n    percent = 5\nelse:\n    percent = 0\n'
                'discount = total * percent // 100\nprint(f"Discount: {percent}%")\nprint(f"To pay: {discount} rub")')],
        constructs=["if"],
    ),
]
