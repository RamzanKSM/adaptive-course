"""Integrative tasks (the task of a topic's 3rd iteration), Python, topics 12–14: if/else (PY_IF_ELSE_BASIC),
comparison operators (PY_COMPARISON_OPERATORS), and (PY_LOGICAL_AND). The topic of the family does the main work, and
1–2 earlier topics join it: arithmetic, order of execution, int/float, strings with `+`, int(), // and %, += -=,
f-strings (and, for comparisons and `and`, if/else and comparisons themselves).
Theme domains: museum tickets, fitness tracker, water meters, clothing sizes; the 3 stories of a topic are in 3 domains.
Not yet: elif, or/not, truthiness of non-bool values, loops, lists, string methods and slices, functions, :.2f, round();
in the if/else families also no printing of True/False, no !=, < or <= (they come with the comparison operators), and
no `and` before PY_LOGICAL_AND."""
from build import OutputTask

CMP = [("Compare", "Используй операторы сравнения: ==, !=, <, >, <=, >=")]
AND = [("And", "Используй and, чтобы объединить проверки в одном условии")]

TASKS = [
    # ───────── 12. Условия if / else ─────────
    OutputTask(
        skill="PY_IF_ELSE_BASIC", difficulty=3, slug="py-int-if-ticket-office", title="Касса музея перед закрытием",
        given=["hour", "minute", "close"],
        variants=[{"hour": "16", "minute": "25", "close": "18"}],
        hidden=[{"hour": "17", "minute": "0", "close": "18"}, {"hour": "17", "minute": "1", "close": "18"},
                {"hour": "19", "minute": "0", "close": "19"}, {"hour": "10", "minute": "0", "close": "20"},
                {"hour": "12", "minute": "45", "close": "17"}, {"hour": "20", "minute": "30", "close": "21"}],
        intro="Касса музея продаёт билеты, только пока до закрытия остаётся 60 минут или больше: за меньшее время "
              "выставку не посмотреть. Посетитель подошёл к кассе в `hour = {hour}` ч `minute = {minute}` мин, "
              "а музей закрывается ровно в `close = {close}` ч того же дня.",
        steps=["Переведи время прихода в минуты от полуночи: `hour * 60 + minute` — и сохрани в `now`. "
               "Время закрытия в минутах — `close * 60`. Посчитай, сколько минут осталось до закрытия, и сохрани в `left`.",
               "Выведи f-строкой `Until closing: <left // 60> h <left % 60> min`: часы — это `left`, делённое нацело "
               "на 60, а минуты — остаток от деления `left` на 60.",
               "Если `left` равно 60 или больше, выведи `Ticket sold`. Иначе выведи "
               "`Ticket office closed <60 - left> min ago`.",
               "Например, для прихода в 17 ч 20 мин и закрытия в 18 ч программа выводит `Until closing: 0 h 40 min` "
               "и `Ticket office closed 20 min ago`."],
        hint="17 ч 20 мин — это `17 * 60 + 20`, то есть 1040 минут от полуночи. `100 // 60` даёт `1`, а `100 % 60` — `40`. "
             "Если до закрытия ровно 60 минут, билет ещё продают, поэтому в условии нужен `>=`.",
        solution='now = hour * 60 + minute\nleft = close * 60 - now\nprint(f"Until closing: {left // 60} h {left % 60} min")\n'
                 'if left >= 60:\n    print("Ticket sold")\nelse:\n    print(f"Ticket office closed {60 - left} min ago")',
        wrong=[("строгое сравнение: ровно за 60 минут до закрытия билет не продают",
                'now = hour * 60 + minute\nleft = close * 60 - now\nprint(f"Until closing: {left // 60} h {left % 60} min")\n'
                'if left > 60:\n    print("Ticket sold")\nelse:\n    print(f"Ticket office closed {60 - left} min ago")'),
               ("часы прихода не переведены в минуты",
                'now = hour + minute\nleft = close * 60 - now\nprint(f"Until closing: {left // 60} h {left % 60} min")\n'
                'if left >= 60:\n    print("Ticket sold")\nelse:\n    print(f"Ticket office closed {60 - left} min ago")'),
               ("часы до закрытия посчитаны через / — получается дробь",
                'now = hour * 60 + minute\nleft = close * 60 - now\nprint(f"Until closing: {left / 60} h {left % 60} min")\n'
                'if left >= 60:\n    print("Ticket sold")\nelse:\n    print(f"Ticket office closed {60 - left} min ago")'),
               ("в else вычитание в обратном порядке — минуты отрицательные",
                'now = hour * 60 + minute\nleft = close * 60 - now\nprint(f"Until closing: {left // 60} h {left % 60} min")\n'
                'if left >= 60:\n    print("Ticket sold")\nelse:\n    print(f"Ticket office closed {left - 60} min ago")')],
        constructs=["if"],
    ),
    OutputTask(
        skill="PY_IF_ELSE_BASIC", difficulty=3, slug="py-int-if-meter-rollover", title="Старый счётчик воды",
        given=["before", "now", "price"],
        variants=[{"before": '"9987"', "now": '"0012"', "price": "45"}],
        hidden=[{"before": '"0450"', "now": '"0462"', "price": "45"}, {"before": '"1234"', "now": '"1234"', "price": "50"},
                {"before": '"9999"', "now": '"0000"', "price": "40"}, {"before": '"9950"', "now": '"0015"', "price": "52"},
                {"before": '"0000"', "now": '"0009"', "price": "48"}],
        intro="В квартире стоит старый счётчик холодной воды с четырьмя цифрами: после `9999` он показывает `0000` "
              "и считает дальше. Показания переписали с циферблата строками, вместе с нулями впереди: в прошлом месяце "
              "было `before = {before}`, в этом — `now = {now}` кубометров. Кубометр воды стоит `price = {price}` руб.",
        steps=["Склей через `+` строку `Meter: `, `before`, строку ` -> ` и `now` и выведи, например `Meter: 0450 -> 0462`.",
               "Преврати оба показания в целые числа с помощью `int()` и сохрани в `old` и `new`.",
               "Если `new` больше или равно `old`, расход `used` — это `new - old`. Иначе счётчик прошёл через `0000`: "
               "расход `used` равен `new + 10000 - old`, и в этой ветке выведи ещё `Meter passed 9999`.",
               "С помощью f-строк выведи `Used: <used> m3` и `To pay: <used * price> rub`. Например, для `\"9999\"`, "
               "`\"0000\"` и цены 40 руб. программа выводит `Meter: 9999 -> 0000`, `Meter passed 9999`, `Used: 1 m3`, "
               "`To pay: 40 rub`."],
        hint="`int(\"0012\")` даёт число `12`. В первой строке склеивай исходные строки — так нули впереди сохранятся. "
             "Если показания не изменились, расход 0 — это ветка `if`, а не `else`.",
        solution='print("Meter: " + before + " -> " + now)\nold = int(before)\nnew = int(now)\nif new >= old:\n'
                 '    used = new - old\nelse:\n    used = new + 10000 - old\n    print("Meter passed 9999")\n'
                 'print(f"Used: {used} m3")\nprint(f"To pay: {used * price} rub")',
        wrong=[("нет else: при переходе через 0000 расход отрицательный",
                'print("Meter: " + before + " -> " + now)\nold = int(before)\nnew = int(now)\nused = new - old\n'
                'print(f"Used: {used} m3")\nprint(f"To pay: {used * price} rub")'),
               ("строгое сравнение: при одинаковых показаниях насчитывает 10000 кубометров",
                'print("Meter: " + before + " -> " + now)\nold = int(before)\nnew = int(now)\nif new > old:\n'
                '    used = new - old\nelse:\n    used = new + 10000 - old\n    print("Meter passed 9999")\n'
                'print(f"Used: {used} m3")\nprint(f"To pay: {used * price} rub")'),
               ("в else показания вычтены в обратном порядке",
                'print("Meter: " + before + " -> " + now)\nold = int(before)\nnew = int(now)\nif new >= old:\n'
                '    used = new - old\nelse:\n    used = old - new\n    print("Meter passed 9999")\n'
                'print(f"Used: {used} m3")\nprint(f"To pay: {used * price} rub")'),
               ("первая строка выведена из чисел — нули впереди пропали",
                'old = int(before)\nnew = int(now)\nprint(f"Meter: {old} -> {new}")\nif new >= old:\n'
                '    used = new - old\nelse:\n    used = new + 10000 - old\n    print("Meter passed 9999")\n'
                'print(f"Used: {used} m3")\nprint(f"To pay: {used * price} rub")')],
        constructs=["if"],
    ),
    OutputTask(
        skill="PY_IF_ELSE_BASIC", difficulty=3, slug="py-int-if-run-points", title="Баллы за пробежку",
        given=["meters", "total"],
        variants=[{"meters": "5320", "total": "340"}],
        hidden=[{"meters": "5000", "total": "0"}, {"meters": "4999", "total": "120"}, {"meters": "4870", "total": "100"},
                {"meters": "12345", "total": "1000"}, {"meters": "950", "total": "5"}],
        intro="Фитнес-трекер начисляет баллы за пробежку: 1 балл за каждые полные 100 м, а за пробежку от 5000 м "
              "(5 км) — ещё 20 баллов бонусом. Сегодня ты пробежал `meters = {meters}` м, а на счету в приложении "
              "уже `total = {total}` баллов.",
        steps=["Выведи f-строкой `Distance: <meters / 1000> km`.",
               "Посчитай баллы за пробежку: `meters`, делённое нацело на 100, — и сохрани в `points`.",
               "Если `meters` равно 5000 или больше, прибавь к `points` бонус 20 с помощью `+=` и выведи `Bonus: 5K`. "
               "Иначе выведи `To 5K: <5000 - meters> m`.",
               "После условия прибавь `points` к `total` с помощью `+=` и выведи `Points: +<points>, total: <total>`. "
               "Например, для 4870 м и 100 баллов на счету программа выводит `Distance: 4.87 km`, `To 5K: 130 m`, "
               "`Points: +48, total: 148`."],
        hint="`4870 // 100` даёт `48`: неполная сотня метров балла не приносит. Бонус прибавляй к `points` внутри `if`, "
             "а `points` к `total` — уже после условия, тогда бонус попадёт и в общий счёт.",
        solution='print(f"Distance: {meters / 1000} km")\npoints = meters // 100\nif meters >= 5000:\n    points += 20\n'
                 '    print("Bonus: 5K")\nelse:\n    print(f"To 5K: {5000 - meters} m")\ntotal += points\n'
                 'print(f"Points: +{points}, total: {total}")',
        wrong=[("строгое сравнение: за ровно 5 км бонуса нет",
                'print(f"Distance: {meters / 1000} km")\npoints = meters // 100\nif meters > 5000:\n    points += 20\n'
                '    print("Bonus: 5K")\nelse:\n    print(f"To 5K: {5000 - meters} m")\ntotal += points\n'
                'print(f"Points: +{points}, total: {total}")'),
               ("баллы посчитаны через / — получается дробь",
                'print(f"Distance: {meters / 1000} km")\npoints = meters / 100\nif meters >= 5000:\n    points += 20\n'
                '    print("Bonus: 5K")\nelse:\n    print(f"To 5K: {5000 - meters} m")\ntotal += points\n'
                'print(f"Points: +{points}, total: {total}")'),
               ("баллы добавлены к общему счёту до бонуса — бонус в total не попал",
                'print(f"Distance: {meters / 1000} km")\npoints = meters // 100\ntotal += points\nif meters >= 5000:\n'
                '    points += 20\n    print("Bonus: 5K")\nelse:\n    print(f"To 5K: {5000 - meters} m")\n'
                'print(f"Points: +{points}, total: {total}")')],
        constructs=["if"],
    ),

    # ───────── 13. Операторы сравнения ─────────
    OutputTask(
        skill="PY_COMPARISON_OPERATORS", difficulty=3, slug="py-int-cmp-jacket-size", title="Размер пиджака",
        given=["chest", "hanger"],
        variants=[{"chest": "103", "hanger": "54"}],
        hidden=[{"chest": "98", "hanger": "48"}, {"chest": "96", "hanger": "48"}, {"chest": "99", "hanger": "50"},
                {"chest": "88", "hanger": "46"}, {"chest": "110", "hanger": "54"}],
        intro="Российский размер одежды — это половина обхвата груди: при обхвате 96 см нужен размер 48. Размеры бывают "
              "только чётными, поэтому если половина получилась нечётной, берут следующий, больший размер. "
              "Обхват груди покупателя — `chest = {chest}` см, а на вешалке висит пиджак размера `hanger = {hanger}`.",
        steps=["Посчитай половину обхвата нацело: `chest // 2` — и сохрани в `size`. Если `size` нечётный (остаток "
               "от деления на 2 не равен 0 — оператор `!=`), прибавь к `size` 1 с помощью `+=`. "
               "Выведи f-строкой `Your size: <size>`.",
               "С помощью f-строк выведи `Fits: <True/False>` — равен ли `hanger` размеру `size` — "
               "и `Too small: <True/False>` — меньше ли `hanger`, чем `size`.",
               "Если `hanger` не равен `size`, выведи `Ask for size <size>`, иначе выведи `Go to the fitting room`.",
               "Например, для обхвата 98 см и пиджака размера 48 программа выводит `Your size: 50`, `Fits: False`, "
               "`Too small: True`, `Ask for size 50`."],
        hint="`98 // 2` даёт `49`, а `49 % 2` — `1`: размер нечётный, значит, нужен 50. Результат сравнения можно "
             "вставить прямо в f-строку: `f\"Fits: {{hanger == size}}\"`. «Не равно» — это `!=`.",
        solution='size = chest // 2\nif size % 2 != 0:\n    size += 1\nprint(f"Your size: {size}")\n'
                 'print(f"Fits: {hanger == size}")\nprint(f"Too small: {hanger < size}")\nif hanger != size:\n'
                 '    print(f"Ask for size {size}")\nelse:\n    print("Go to the fitting room")',
        wrong=[("нет поправки на чётность — получается нечётный размер",
                'size = chest // 2\nprint(f"Your size: {size}")\n'
                'print(f"Fits: {hanger == size}")\nprint(f"Too small: {hanger < size}")\nif hanger != size:\n'
                '    print(f"Ask for size {size}")\nelse:\n    print("Go to the fitting room")'),
               ("== вместо != в проверке чётности: к чётному размеру прибавляется 1",
                'size = chest // 2\nif size % 2 == 0:\n    size += 1\nprint(f"Your size: {size}")\n'
                'print(f"Fits: {hanger == size}")\nprint(f"Too small: {hanger < size}")\nif hanger != size:\n'
                '    print(f"Ask for size {size}")\nelse:\n    print("Go to the fitting room")'),
               ("знак перевёрнут: Too small показывает, что пиджак больше",
                'size = chest // 2\nif size % 2 != 0:\n    size += 1\nprint(f"Your size: {size}")\n'
                'print(f"Fits: {hanger == size}")\nprint(f"Too small: {hanger > size}")\nif hanger != size:\n'
                '    print(f"Ask for size {size}")\nelse:\n    print("Go to the fitting room")'),
               ("в последнем условии == вместо != — ветки срабатывают наоборот",
                'size = chest // 2\nif size % 2 != 0:\n    size += 1\nprint(f"Your size: {size}")\n'
                'print(f"Fits: {hanger == size}")\nprint(f"Too small: {hanger < size}")\nif hanger == size:\n'
                '    print(f"Ask for size {size}")\nelse:\n    print("Go to the fitting room")')],
        constructs=["if"],
        must_use=CMP,
    ),
    OutputTask(
        skill="PY_COMPARISON_OPERATORS", difficulty=3, slug="py-int-cmp-ticket-machine", title="Билетный автомат в музее",
        given=["price", "count", "paid"],
        variants=[{"price": "450", "count": "3", "paid": "1500"}],
        hidden=[{"price": "375", "count": "2", "paid": "2000"}, {"price": "500", "count": "2", "paid": "1000"},
                {"price": "350", "count": "3", "paid": "1000"}, {"price": "299", "count": "1", "paid": "298"},
                {"price": "420", "count": "4", "paid": "5000"}],
        intro="Билетный автомат в музее продаёт билеты по `price = {price}` руб. Посетитель покупает `count = {count}` "
              "билета и вставляет в автомат `paid = {paid}` руб. Сдачу автомат выдаёт купюрами по 100 руб. и монетами.",
        steps=["Посчитай стоимость билетов: `price * count` — сохрани в `total` и выведи f-строкой `Total: <total> rub`.",
               "С помощью f-строк выведи `Enough: <True/False>` — больше ли `paid`, чем `total`, или равно ему — "
               "и `Exact: <True/False>` — равно ли `paid` ровно `total`.",
               "Если `paid` меньше `total`, выведи `Add <total - paid> rub`. Иначе посчитай сдачу `change` "
               "(`paid - total`) и выведи `Change: <change // 100> x 100 rub + <change % 100> rub`.",
               "Например, для двух билетов по 375 руб. и 2000 руб. программа выводит `Total: 750 rub`, `Enough: True`, "
               "`Exact: False`, `Change: 12 x 100 rub + 50 rub`."],
        hint="«Больше или равно» — это `>=`: если денег ровно столько, сколько стоят билеты, их хватает, а сдача 0. "
             "`1250 // 100` даёт `12` купюр, а `1250 % 100` — `50` руб. монетами.",
        solution='total = price * count\nprint(f"Total: {total} rub")\nprint(f"Enough: {paid >= total}")\n'
                 'print(f"Exact: {paid == total}")\nif paid < total:\n    print(f"Add {total - paid} rub")\nelse:\n'
                 '    change = paid - total\n    print(f"Change: {change // 100} x 100 rub + {change % 100} rub")',
        wrong=[("строгое сравнение: при оплате без сдачи денег будто не хватает",
                'total = price * count\nprint(f"Total: {total} rub")\nprint(f"Enough: {paid > total}")\n'
                'print(f"Exact: {paid == total}")\nif paid < total:\n    print(f"Add {total - paid} rub")\nelse:\n'
                '    change = paid - total\n    print(f"Change: {change // 100} x 100 rub + {change % 100} rub")'),
               ("<= вместо <: при точной оплате просит добавить 0 руб.",
                'total = price * count\nprint(f"Total: {total} rub")\nprint(f"Enough: {paid >= total}")\n'
                'print(f"Exact: {paid == total}")\nif paid <= total:\n    print(f"Add {total - paid} rub")\nelse:\n'
                '    change = paid - total\n    print(f"Change: {change // 100} x 100 rub + {change % 100} rub")'),
               ("монеты посчитаны через // — то же число, что и купюры",
                'total = price * count\nprint(f"Total: {total} rub")\nprint(f"Enough: {paid >= total}")\n'
                'print(f"Exact: {paid == total}")\nif paid < total:\n    print(f"Add {total - paid} rub")\nelse:\n'
                '    change = paid - total\n    print(f"Change: {change // 100} x 100 rub + {change // 100} rub")'),
               ("забыто число билетов",
                'total = price\nprint(f"Total: {total} rub")\nprint(f"Enough: {paid >= total}")\n'
                'print(f"Exact: {paid == total}")\nif paid < total:\n    print(f"Add {total - paid} rub")\nelse:\n'
                '    change = paid - total\n    print(f"Change: {change // 100} x 100 rub + {change % 100} rub")')],
        constructs=["if"],
        must_use=CMP,
    ),
    OutputTask(
        skill="PY_COMPARISON_OPERATORS", difficulty=3, slug="py-int-cmp-night-leak", title="Утечка воды ночью",
        given=["at1", "at5"],
        variants=[{"at1": "38215", "at5": "38227"}],
        hidden=[{"at1": "12450", "at5": "12470"}, {"at1": "5000", "at5": "5000"}, {"at1": "777", "at5": "796"},
                {"at1": "100", "at5": "101"}, {"at1": "64010", "at5": "64060"}],
        intro="Умный счётчик воды показывает расход в литрах. С 1:00 до 5:00 в квартире все спят и краны закрыты, "
              "поэтому показания за это время не должны меняться. В 1:00 счётчик показывал `at1 = {at1}` л, "
              "а в 5:00 — `at5 = {at5}` л.",
        steps=["Посчитай, сколько литров ушло за ночь: `at5 - at1` — и сохрани в `lost`. Выведи f-строкой "
               "`Night: <lost> l, <lost / 4> l/h` — ночь длится 4 часа.",
               "С помощью f-строк выведи `Leak: <True/False>` — отличается ли `at5` от `at1` (оператор `!=`) — "
               "и `Serious: <True/False>` — уходит ли 5 литров в час или больше (`lost / 4` сравни с 5).",
               "Если `at5` равно `at1`, выведи `All taps closed`. Иначе выведи "
               "`Check the pipes: <lost * 30> l in 30 nights`.",
               "Например, для 12450 и 12470 программа выводит `Night: 20 l, 5.0 l/h`, `Leak: True`, `Serious: True`, "
               "`Check the pipes: 600 l in 30 nights`."],
        hint="Деление `/` всегда даёт дробное число: `12 / 4` — это `3.0`. «Не равно» — это `!=`, "
             "а «5 или больше» — `>=`: ровно 5 литров в час — уже серьёзная утечка.",
        solution='lost = at5 - at1\nprint(f"Night: {lost} l, {lost / 4} l/h")\nprint(f"Leak: {at5 != at1}")\n'
                 'print(f"Serious: {lost / 4 >= 5}")\nif at5 == at1:\n    print("All taps closed")\nelse:\n'
                 '    print(f"Check the pipes: {lost * 30} l in 30 nights")',
        wrong=[("== вместо != : Leak показывает, что утечки нет",
                'lost = at5 - at1\nprint(f"Night: {lost} l, {lost / 4} l/h")\nprint(f"Leak: {at5 == at1}")\n'
                'print(f"Serious: {lost / 4 >= 5}")\nif at5 == at1:\n    print("All taps closed")\nelse:\n'
                '    print(f"Check the pipes: {lost * 30} l in 30 nights")'),
               ("строгое сравнение: ровно 5 л в час не считается серьёзной утечкой",
                'lost = at5 - at1\nprint(f"Night: {lost} l, {lost / 4} l/h")\nprint(f"Leak: {at5 != at1}")\n'
                'print(f"Serious: {lost / 4 > 5}")\nif at5 == at1:\n    print("All taps closed")\nelse:\n'
                '    print(f"Check the pipes: {lost * 30} l in 30 nights")'),
               ("литры в час посчитаны через // — дробная часть теряется",
                'lost = at5 - at1\nprint(f"Night: {lost} l, {lost // 4} l/h")\nprint(f"Leak: {at5 != at1}")\n'
                'print(f"Serious: {lost // 4 >= 5}")\nif at5 == at1:\n    print("All taps closed")\nelse:\n'
                '    print(f"Check the pipes: {lost * 30} l in 30 nights")'),
               ("в условии != вместо == — ветки срабатывают наоборот",
                'lost = at5 - at1\nprint(f"Night: {lost} l, {lost / 4} l/h")\nprint(f"Leak: {at5 != at1}")\n'
                'print(f"Serious: {lost / 4 >= 5}")\nif at5 != at1:\n    print("All taps closed")\nelse:\n'
                '    print(f"Check the pipes: {lost * 30} l in 30 nights")')],
        constructs=["if"],
        must_use=CMP,
    ),

    # ───────── 14. Логическое and ─────────
    OutputTask(
        skill="PY_LOGICAL_AND", difficulty=3, slug="py-int-and-day-streak", title="Серия дней на браслете",
        given=["steps", "active", "streak"],
        variants=[{"steps": "8640", "active": "22", "streak": "6"}],
        hidden=[{"steps": "7500", "active": "10", "streak": "4"}, {"steps": "7499", "active": "45", "streak": "9"},
                {"steps": "12000", "active": "9", "streak": "3"}, {"steps": "0", "active": "0", "streak": "0"},
                {"steps": "9100", "active": "15", "streak": "0"}],
        intro="Фитнес-браслет засчитывает день, если за день набрано не меньше 10000 шагов **и** не меньше 30 активных "
              "минут. К вечеру браслет насчитал `steps = {steps}` шагов и `active = {active}` активных минут, "
              "а засчитанных дней подряд сейчас `streak = {streak}`. Вечером ты ещё гуляешь 20 минут "
              "и проходишь за это время 2500 шагов.",
        steps=["Добавь вечернюю прогулку: увеличь `steps` на 2500, а `active` — на 20 с помощью `+=`. "
               "Выведи f-строкой `Today: <steps> steps, <active> min`.",
               "Если `steps` не меньше 10000 **и** `active` не меньше 30, увеличь `streak` на 1 и выведи `Day counted`.",
               "Иначе серия обрывается: запиши в `streak` значение 0 и выведи `Streak lost`.",
               "В конце (в любом случае) выведи `Days in a row: <streak>`. Например, для 7500 шагов, 10 минут и серии 4 "
               "программа выводит `Today: 10000 steps, 30 min`, `Day counted`, `Days in a row: 5`."],
        hint="«Не меньше» — это `>=`: ровно 10000 шагов и ровно 30 минут день засчитывают. Обе проверки пишутся "
             "полностью: `steps >= 10000 and active >= 30`.",
        solution='steps += 2500\nactive += 20\nprint(f"Today: {steps} steps, {active} min")\n'
                 'if steps >= 10000 and active >= 30:\n    streak += 1\n    print("Day counted")\nelse:\n    streak = 0\n'
                 '    print("Streak lost")\nprint(f"Days in a row: {streak}")',
        wrong=[("строгое сравнение: ровно 10000 шагов не засчитываются",
                'steps += 2500\nactive += 20\nprint(f"Today: {steps} steps, {active} min")\n'
                'if steps > 10000 and active >= 30:\n    streak += 1\n    print("Day counted")\nelse:\n    streak = 0\n'
                '    print("Streak lost")\nprint(f"Days in a row: {streak}")'),
               ("проверяются только шаги, про минуты забыли",
                'steps += 2500\nactive += 20\nprint(f"Today: {steps} steps, {active} min")\n'
                'if steps >= 10000:\n    streak += 1\n    print("Day counted")\nelse:\n    streak = 0\n'
                '    print("Streak lost")\nprint(f"Days in a row: {streak}")'),
               ("минуты прогулки не добавлены",
                'steps += 2500\nprint(f"Today: {steps} steps, {active} min")\n'
                'if steps >= 10000 and active >= 30:\n    streak += 1\n    print("Day counted")\nelse:\n    streak = 0\n'
                '    print("Streak lost")\nprint(f"Days in a row: {streak}")'),
               ("серия не обнуляется, когда день не засчитан",
                'steps += 2500\nactive += 20\nprint(f"Today: {steps} steps, {active} min")\n'
                'if steps >= 10000 and active >= 30:\n    streak += 1\n    print("Day counted")\nelse:\n'
                '    print("Streak lost")\nprint(f"Days in a row: {streak}")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill="PY_LOGICAL_AND", difficulty=3, slug="py-int-and-jacket-growth", title="Куртка на вырост",
        given=["height", "grow", "low", "high"],
        variants=[{"height": "118", "grow": "6", "low": "116", "high": "128"}],
        hidden=[{"height": "125", "grow": "6", "low": "116", "high": "128"},
                {"height": "116", "grow": "12", "low": "116", "high": "128"},
                {"height": "122", "grow": "7", "low": "116", "high": "128"},
                {"height": "110", "grow": "5", "low": "116", "high": "128"},
                {"height": "112", "grow": "6", "low": "116", "high": "128"},
                {"height": "141", "grow": "5", "low": "134", "high": "140"}],
        intro="Мама выбирает сыну куртку. На этикетке написано, на какой рост она сшита: от `low = {low}` "
              "до `high = {high}` см включительно. Сейчас рост сына — `height = {height}` см, а за год он вырастает "
              "на `grow = {grow}` см. Куртку стоит брать, только если она подходит и сейчас, и через год.",
        steps=["Проверь, подходит ли куртка сейчас: `height` не меньше `low` **и** не больше `high`. Сохрани результат "
               "этой проверки в переменную `now_ok` и выведи f-строкой `Fits now: <now_ok>`.",
               "Увеличь `height` на `grow` с помощью `+=` — это рост через год — и выведи `Next year: <height> cm`.",
               "Сделай ту же проверку для нового роста, сохрани результат в `later_ok` и выведи "
               "`Fits next year: <later_ok>`.",
               "Если истинны и `now_ok`, и `later_ok` (соедини их через `and`), выведи `Buy it`, иначе — "
               "`Look for another size`. Например, для роста 125, прироста 6 и этикетки от 116 до 128 программа "
               "выводит `Fits now: True`, `Next year: 131 cm`, `Fits next year: False`, `Look for another size`."],
        hint="Результат проверки можно сохранить в переменную, как число: `ok = x >= 1 and x <= 9` — в ней будет "
             "`True` или `False`. Проверку «сейчас» делай до `+=`: после него в `height` уже рост через год.",
        solution='now_ok = height >= low and height <= high\nprint(f"Fits now: {now_ok}")\nheight += grow\n'
                 'print(f"Next year: {height} cm")\nlater_ok = height >= low and height <= high\n'
                 'print(f"Fits next year: {later_ok}")\nif now_ok and later_ok:\n    print("Buy it")\nelse:\n'
                 '    print("Look for another size")',
        wrong=[("строгое сравнение: рост ровно на границе этикетки не подходит",
                'now_ok = height > low and height < high\nprint(f"Fits now: {now_ok}")\nheight += grow\n'
                'print(f"Next year: {height} cm")\nlater_ok = height > low and height < high\n'
                'print(f"Fits next year: {later_ok}")\nif now_ok and later_ok:\n    print("Buy it")\nelse:\n'
                '    print("Look for another size")'),
               ("проверка «сейчас» сделана после += — оба раза проверяется рост через год",
                'height += grow\nnow_ok = height >= low and height <= high\nprint(f"Fits now: {now_ok}")\n'
                'print(f"Next year: {height} cm")\nlater_ok = height >= low and height <= high\n'
                'print(f"Fits next year: {later_ok}")\nif now_ok and later_ok:\n    print("Buy it")\nelse:\n'
                '    print("Look for another size")'),
               ("забыта нижняя граница этикетки",
                'now_ok = height <= high\nprint(f"Fits now: {now_ok}")\nheight += grow\n'
                'print(f"Next year: {height} cm")\nlater_ok = height <= high\n'
                'print(f"Fits next year: {later_ok}")\nif now_ok and later_ok:\n    print("Buy it")\nelse:\n'
                '    print("Look for another size")'),
               ("покупает, если куртка подойдёт хотя бы через год",
                'now_ok = height >= low and height <= high\nprint(f"Fits now: {now_ok}")\nheight += grow\n'
                'print(f"Next year: {height} cm")\nlater_ok = height >= low and height <= high\n'
                'print(f"Fits next year: {later_ok}")\nif later_ok:\n    print("Buy it")\nelse:\n'
                '    print("Look for another size")')],
        constructs=["if"],
        must_use=AND,
    ),
    OutputTask(
        skill="PY_LOGICAL_AND", difficulty=3, slug="py-int-and-e-ticket", title="Электронный билет в музей",
        given=["code", "check", "date", "today"],
        variants=[{"code": '"48213"', "check": "4", "date": '"28.10"', "today": '"28.10"'}],
        hidden=[{"code": '"00707"', "check": "0", "date": '"28.10"', "today": '"28.10"'},
                {"code": '"48213"', "check": "4", "date": '"27.10"', "today": '"28.10"'},
                {"code": '"51630"', "check": "2", "date": '"01.11"', "today": '"01.11"'},
                {"code": '"12345"', "check": "3", "date": '"05.12"', "today": '"06.12"'},
                {"code": '"09995"', "check": "6", "date": '"31.12"', "today": '"31.12"'}],
        intro="На входе в музей турникет проверяет электронный билет. Из QR-кода он считывает номер билета строкой "
              "`code = {code}` и контрольную цифру `check = {check}`. Билет настоящий, если остаток от деления номера "
              "на 7 равен контрольной цифре. Ещё билет действует только в свой день: дата на билете — `date = {date}`, "
              "а сегодня — `today = {today}`.",
        steps=["Склей через `+` строку `Ticket #` и `code` и выведи, например `Ticket #00707`.",
               "Преврати `code` в целое число с помощью `int()`, найди остаток от его деления на 7 и сохрани в `rest`.",
               "С помощью f-строк выведи `Checksum OK: <True/False>` — равен ли `rest` значению `check` — "
               "и `Date OK: <True/False>` — равна ли `date` строке `today`.",
               "Если `rest` равен `check` **и** `date` равна `today`, выведи `Welcome to the museum`, иначе — "
               "`Ticket is not valid`. Например, для `code = \"00707\"`, `check = 0` и одинаковых дат программа выводит "
               "`Ticket #00707`, `Checksum OK: True`, `Date OK: True`, `Welcome to the museum`."],
        hint="`int(\"00707\")` даёт `707`, а `707 % 7` — `0`. Номер в первой строке склеивай как строку — так нули "
             "впереди сохранятся. В условии обе проверки пишутся полностью: `rest == check and date == today`.",
        solution='print("Ticket #" + code)\nrest = int(code) % 7\nprint(f"Checksum OK: {rest == check}")\n'
                 'print(f"Date OK: {date == today}")\nif rest == check and date == today:\n'
                 '    print("Welcome to the museum")\nelse:\n    print("Ticket is not valid")',
        wrong=[("проверяется только контрольная цифра, дата забыта",
                'print("Ticket #" + code)\nrest = int(code) % 7\nprint(f"Checksum OK: {rest == check}")\n'
                'print(f"Date OK: {date == today}")\nif rest == check:\n'
                '    print("Welcome to the museum")\nelse:\n    print("Ticket is not valid")'),
               ("вместо остатка взято деление нацело //",
                'print("Ticket #" + code)\nrest = int(code) // 7\nprint(f"Checksum OK: {rest == check}")\n'
                'print(f"Date OK: {date == today}")\nif rest == check and date == today:\n'
                '    print("Welcome to the museum")\nelse:\n    print("Ticket is not valid")'),
               ("проверяется только дата",
                'print("Ticket #" + code)\nrest = int(code) % 7\nprint(f"Checksum OK: {rest == check}")\n'
                'print(f"Date OK: {date == today}")\nif date == today:\n'
                '    print("Welcome to the museum")\nelse:\n    print("Ticket is not valid")'),
               ("номер выведен из числа — нули впереди пропали",
                'rest = int(code) % 7\nprint(f"Ticket #{int(code)}")\nprint(f"Checksum OK: {rest == check}")\n'
                'print(f"Date OK: {date == today}")\nif rest == check and date == today:\n'
                '    print("Welcome to the museum")\nelse:\n    print("Ticket is not valid")')],
        constructs=["if"],
        must_use=AND,
    ),
]
