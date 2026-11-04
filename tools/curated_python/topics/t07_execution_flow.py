"""PY_EXECUTION_FLOW_BASIC — «Порядок выполнения». Taught before: print (several values separated by commas), variables,
assignment, arithmetic (+ - *). Commands run from top to bottom; a variable holds the value of its last assignment and does
not recalculate by itself. Not yet: int/float details, strings beyond literals, type conversion, // and %, += -=,
f-strings, conditions, loops, functions."""
from build import OutputTask

SKILL = "PY_EXECUTION_FLOW_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ef-piggy-bank", title="Копилка за неделю",
        given=["start", "gift", "spent"],
        variants=[{"start": "300", "gift": "500", "spent": "250"}, {"start": "120", "gift": "200", "spent": "90"},
                  {"start": "450", "gift": "150", "spent": "380"}],
        hidden=[{"start": "0", "gift": "100", "spent": "40"}, {"start": "700", "gift": "300", "spent": "1000"},
                {"start": "55", "gift": "45", "spent": "0"}],
        intro="В копилке у Ани лежит `start = {start}` руб. Бабушка подарила ей ещё `gift = {gift}` руб., "
              "а потом Аня потратила в магазине `spent = {spent}` руб. Программа должна показать, сколько денег было "
              "в копилке после каждого шага.",
        steps=["Выведи строку `Start:` и значение `start` через запятую в `print` — например, `Start: 100`.",
               "Заведи переменную `money`: это `start` плюс `gift`. Выведи `After gift:` и `money`.",
               "Уменьши `money`: присвой ей старое значение `money` минус `spent`. Выведи `After shop:` и `money`."],
        hint="Команды выполняются сверху вниз. В строке `money = money - spent` справа берётся то значение `money`, "
             "которое уже лежит в переменной после подарка. Если написать `start - spent`, подарок потеряется.",
        solution='print("Start:", start)\nmoney = start + gift\nprint("After gift:", money)\n'
                 'money = money - spent\nprint("After shop:", money)',
        wrong=[("вычитает траты из начальной суммы — подарок теряется",
                'print("Start:", start)\nmoney = start + gift\nprint("After gift:", money)\n'
                'money = start - spent\nprint("After shop:", money)'),
               ("печатает остаток до того, как вычел траты",
                'print("Start:", start)\nmoney = start + gift\nprint("After gift:", money)\n'
                'print("After shop:", money)\nmoney = money - spent')],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ef-coffee-price", title="Кофе подорожал",
        given=["price", "raise_by"],
        variants=[{"price": "180", "raise_by": "20"}, {"price": "150", "raise_by": "35"}, {"price": "210", "raise_by": "15"}],
        hidden=[{"price": "100", "raise_by": "0"}, {"price": "95", "raise_by": "50"}, {"price": "300", "raise_by": "1"}],
        intro="В кофейне чашка капучино стоила `price = {price}` руб. С понедельника цену подняли на `raise_by = {raise_by}` руб. "
              "Хозяин хочет табличку, где видны старая цена, новая цена и разница между ними.",
        steps=["Сохрани текущую цену в переменную `old_price` — это нужно сделать до того, как цена изменится.",
               "Увеличь `price`: присвой ей `price` плюс `raise_by`.",
               "Выведи три строки: `Old price:` и `old_price`, затем `New price:` и `price`, затем `Difference:` и "
               "`price` минус `old_price`. Например, для цены 100 и подорожания на 10 это `Old price: 100`, "
               "`New price: 110`, `Difference: 10`."],
        hint="После строки `price = price + raise_by` старой цены в `price` уже нет. Поэтому её надо запомнить "
             "в другой переменной заранее, а печатать старую цену из `old_price`, а не из `price`.",
        solution='old_price = price\nprice = price + raise_by\nprint("Old price:", old_price)\n'
                 'print("New price:", price)\nprint("Difference:", price - old_price)',
        wrong=[("печатает как старую цену уже изменённую `price`",
                'old_price = price\nprice = price + raise_by\nprint("Old price:", price)\n'
                'print("New price:", price)\nprint("Difference:", price - old_price)'),
               ("запоминает цену уже после подорожания",
                'price = price + raise_by\nold_price = price\nprint("Old price:", old_price)\n'
                'print("New price:", price)\nprint("Difference:", price - old_price)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ef-phone-balance", title="Баланс телефона",
        given=["balance", "top_up", "minutes"],
        variants=[{"balance": "40", "top_up": "300", "minutes": "25"}, {"balance": "15", "top_up": "200", "minutes": "40"},
                  {"balance": "120", "top_up": "100", "minutes": "60"}],
        hidden=[{"balance": "0", "top_up": "500", "minutes": "1"}, {"balance": "75", "top_up": "0", "minutes": "20"},
                {"balance": "10", "top_up": "150", "minutes": "0"}],
        intro="На счету телефона Бориса `balance = {balance}` руб. Он пополнил счёт на `top_up = {top_up}` руб., "
              "а потом проговорил `minutes = {minutes}` минут. Минута разговора стоит 3 руб.",
        steps=["Выведи `Balance:` и `balance` — баланс до пополнения.",
               "Пополни счёт: присвой `balance` старое значение плюс `top_up`. Выведи `After top-up:` и `balance`.",
               "Посчитай стоимость звонка в переменную `cost`: `minutes`, умноженные на 3. Выведи `Call cost:` и `cost`.",
               "Спиши стоимость звонка: присвой `balance` старое значение минус `cost`. Выведи `After call:` и `balance`."],
        hint="Выражение `balance + top_up` само по себе ничего не меняет: результат нужно присвоить переменной — "
             "`balance = balance + top_up`. Иначе в `balance` останется старое число.",
        solution='print("Balance:", balance)\nbalance = balance + top_up\nprint("After top-up:", balance)\n'
                 'cost = minutes * 3\nprint("Call cost:", cost)\nbalance = balance - cost\nprint("After call:", balance)',
        wrong=[("считает сумму пополнения, но не сохраняет её в `balance`",
                'print("Balance:", balance)\nbalance + top_up\nprint("After top-up:", balance)\n'
                'cost = minutes * 3\nprint("Call cost:", cost)\nbalance = balance - cost\nprint("After call:", balance)'),
               ("списывает минуты, а не их стоимость",
                'print("Balance:", balance)\nbalance = balance + top_up\nprint("After top-up:", balance)\n'
                'cost = minutes * 3\nprint("Call cost:", cost)\nbalance = balance - minutes\nprint("After call:", balance)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ef-pizza-order", title="К заказу присоединились друзья",
        given=["price", "count", "extra"],
        variants=[{"price": "550", "count": "2", "extra": "3"}, {"price": "490", "count": "3", "extra": "1"},
                  {"price": "620", "count": "1", "extra": "2"}],
        hidden=[{"price": "500", "count": "4", "extra": "0"}, {"price": "399", "count": "1", "extra": "5"},
                {"price": "700", "count": "2", "extra": "2"}],
        intro="Аня заказывает пиццу: одна стоит `price = {price}` руб., сначала она берёт `count = {count}` шт. "
              "Потом пришли друзья и попросили добавить ещё `extra = {extra}` шт. Важно понять: переменная, посчитанная "
              "раньше, сама не пересчитывается, когда меняются числа, из которых её посчитали.",
        steps=["Посчитай `total` — `price`, умноженная на `count`. Выведи `Total:` и `total`.",
               "Увеличь `count`: присвой ей `count` плюс `extra`. Выведи `Count:` и `count`.",
               "Выведи `Old total:` и `total` — ещё раз, ничего не пересчитывая: в `total` по-прежнему старая сумма.",
               "Пересчитай `total` по той же формуле (теперь с новым `count`) и выведи `New total:` и `total`."],
        hint="`total = price * count` вычисляется один раз — в тот момент, когда Python доходит до этой строки. "
             "Когда `count` потом меняется, `total` остаётся прежним, пока ты сам не напишешь формулу ещё раз.",
        solution='total = price * count\nprint("Total:", total)\ncount = count + extra\nprint("Count:", count)\n'
                 'print("Old total:", total)\ntotal = price * count\nprint("New total:", total)',
        wrong=[("считает новое количество, но не сохраняет его в `count`",
                'total = price * count\nprint("Total:", total)\ncount + extra\nprint("Count:", count)\n'
                'print("Old total:", total)\ntotal = price * count\nprint("New total:", total)'),
               ("не пересчитывает сумму — думает, что `total` обновится сам",
                'total = price * count\nprint("Total:", total)\ncount = count + extra\nprint("Count:", count)\n'
                'print("Old total:", total)\nprint("New total:", total)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ef-shop-cash", title="Касса магазина за день",
        given=["start", "morning", "evening"],
        variants=[{"start": "800", "morning": "2600", "evening": "1900"}, {"start": "500", "morning": "3100", "evening": "1200"},
                  {"start": "1000", "morning": "1500", "evening": "2400"}],
        hidden=[{"start": "200", "morning": "800", "evening": "0"}, {"start": "1000", "morning": "0", "evening": "700"},
                {"start": "650", "morning": "4350", "evening": "3300"}],
        intro="Утром в кассе магазина лежит `start = {start}` руб. До обеда покупатели заплатили `morning = {morning}` руб. "
              "В обед хозяйка забирает из кассы всё, кроме 1000 руб. размена. Вечером покупатели заплатили ещё "
              "`evening = {evening}` руб.",
        steps=["Заведи `cash` — `start` плюс `morning`. Выведи `Noon:` и `cash`.",
               "Посчитай, сколько забирает хозяйка: `taken` — это то, что сейчас в `cash`, минус 1000.",
               "Убери эти деньги из кассы: присвой `cash` значение `cash` минус `taken`. Выведи `Taken:` и `taken`.",
               "Добавь вечернюю выручку: `cash` становится `cash` плюс `evening`. Выведи `Close:` и `cash`.",
               "Последней строкой выведи `All money:` и сумму `taken` и `cash` — все деньги, которые есть у магазина к вечеру."],
        hint="Каждая строка берёт значения переменных такими, какие они в этот момент. `taken` надо считать из `cash` "
             "после утренней выручки, а не из `start`. После вычитания в кассе должно остаться ровно 1000.",
        solution='cash = start + morning\nprint("Noon:", cash)\ntaken = cash - 1000\ncash = cash - taken\n'
                 'print("Taken:", taken)\ncash = cash + evening\nprint("Close:", cash)\nprint("All money:", taken + cash)',
        wrong=[("считает, сколько забрать, из утренней суммы `start`, а не из текущей кассы",
                'cash = start + morning\nprint("Noon:", cash)\ntaken = start - 1000\ncash = cash - taken\n'
                'print("Taken:", taken)\ncash = cash + evening\nprint("Close:", cash)\nprint("All money:", taken + cash)'),
               ("печатает закрытие кассы до того, как добавил вечернюю выручку",
                'cash = start + morning\nprint("Noon:", cash)\ntaken = cash - 1000\ncash = cash - taken\n'
                'print("Taken:", taken)\nprint("Close:", cash)\ncash = cash + evening\nprint("All money:", taken + cash)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ef-library-shelf", title="Книги в школьной библиотеке",
        given=["books", "taken", "returned", "bought"],
        variants=[{"books": "120", "taken": "35", "returned": "20", "bought": "10"},
                  {"books": "86", "taken": "14", "returned": "9", "bought": "25"},
                  {"books": "240", "taken": "60", "returned": "45", "bought": "5"}],
        hidden=[{"books": "50", "taken": "0", "returned": "0", "bought": "7"}, {"books": "30", "taken": "30", "returned": "30", "bought": "0"},
                {"books": "75", "taken": "12", "returned": "3", "bought": "40"}],
        intro="На полках школьной библиотеки `books = {books}` книг. В понедельник ученики взяли домой `taken = {taken}` книг, "
              "во вторник вернули `returned = {returned}`, а в среду библиотека купила `bought = {bought}` новых книг. "
              "Библиотекарь следит за двумя числами: сколько книг на полках и сколько на руках у читателей.",
        steps=["Понедельник: уменьши `books` на `taken`, а в новую переменную `out` (книги на руках) запиши `taken`. "
               "Выведи `Monday:` и `books`.",
               "Вторник: увеличь `books` на `returned`, а `out` уменьши на `returned`. Выведи `Tuesday:` и `books`.",
               "Среда: увеличь `books` на `bought`.",
               "Выведи три строки: `On shelves:` и `books`, `With readers:` и `out`, `Total:` и сумму `books` и `out`."],
        hint="Каждое изменение записывай присваиванием, например `books = books - taken`. В последней строке нужна сумма "
             "текущих `books` и `out`: число `taken` осталось от понедельника и уже не показывает, сколько книг на руках.",
        solution='books = books - taken\nout = taken\nprint("Monday:", books)\nbooks = books + returned\n'
                 'out = out - returned\nprint("Tuesday:", books)\nbooks = books + bought\nprint("On shelves:", books)\n'
                 'print("With readers:", out)\nprint("Total:", books + out)',
        wrong=[("в итоге берёт устаревшее число `taken` вместо текущего `out`",
                'books = books - taken\nout = taken\nprint("Monday:", books)\nbooks = books + returned\n'
                'out = out - returned\nprint("Tuesday:", books)\nbooks = books + bought\nprint("On shelves:", books)\n'
                'print("With readers:", out)\nprint("Total:", books + taken)'),
               ("не уменьшает число книг на руках после возврата",
                'books = books - taken\nout = taken\nprint("Monday:", books)\nbooks = books + returned\n'
                'print("Tuesday:", books)\nbooks = books + bought\nprint("On shelves:", books)\n'
                'print("With readers:", out)\nprint("Total:", books + out)')],
    ),
]
