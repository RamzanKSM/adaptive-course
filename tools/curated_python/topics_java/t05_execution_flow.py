"""EXECUTION_FLOW_BASIC — «Порядок выполнения» (Java). Taught before: System.out.println / print, variables (`int`,
`String`), assignment, arithmetic `+ - *` with parentheses. This topic: statements run top to bottom one after another;
a variable changes step by step (`money = money - spent;` uses the value from the line above), a print shows the value
at that moment, a value must be saved before it changes, and the order of two changes matters.
Not yet: `+=` and `++`, division `/` and `%`, string concatenation (a line is assembled from several print calls),
conditions, loops."""
from java_tasks import JavaOutputTask

SKILL = "EXECUTION_FLOW_BASIC"


def _code(*lines: str) -> str:
    return "\n".join(lines)


def _change(code: str, old: str, new: str, nth: int = 1) -> str:
    """The code with the nth line equal to `old` replaced by `new` (a one-line mistake)."""
    lines = code.split("\n")
    found = [i for i, line in enumerate(lines) if line == old]
    assert len(found) >= nth, f"no line {old!r}"
    lines[found[nth - 1]] = new
    return "\n".join(lines)


def _swap(code: str, a: str, b: str) -> str:
    """The code with lines `a` and `b` exchanged (statements in the wrong order)."""
    lines = code.split("\n")
    i, j = lines.index(a), lines.index(b)
    lines[i], lines[j] = lines[j], lines[i]
    return "\n".join(lines)


PIGGY = _code(
    'int money = start;',
    'System.out.print("Start: ");',
    'System.out.println(money);',
    'money = money + gift;',
    'System.out.print("After gift: ");',
    'System.out.println(money);',
    'money = money - spent;',
    'System.out.print("After shop: ");',
    'System.out.println(money);',
)

SHELF = _code(
    'int shelf = books;',
    'System.out.print("Morning: ");',
    'System.out.println(shelf);',
    'shelf = shelf - lent;',
    'shelf = shelf + bought;',
    'System.out.print("Evening: ");',
    'System.out.println(shelf);',
)

COINS = _code(
    'int coins = start;',
    'coins = coins + quest;',
    'System.out.print("After quest: ");',
    'System.out.println(coins);',
    'coins = coins * 2;',
    'System.out.print("Weekend x2: ");',
    'System.out.println(coins);',
    'coins = coins - shop;',
    'System.out.print("After shop: ");',
    'System.out.println(coins);',
)

PRICE = _code(
    'int oldPrice = price;',
    'price = price + raise;',
    'price = price - discount;',
    'int total = price * count;',
    'System.out.print("Old price: ");',
    'System.out.println(oldPrice);',
    'System.out.print("New price: ");',
    'System.out.println(price);',
    'System.out.print("Total: ");',
    'System.out.println(total);',
)

CARD = _code(
    'int start = balance;',
    'balance = balance + salary;',
    'balance = balance - rent;',
    'balance = balance - food;',
    'balance = balance + 50;',
    'int change = balance - start;',
    'System.out.print("Balance: ");',
    'System.out.println(balance);',
    'System.out.print("Change: ");',
    'System.out.println(change);',
)

STORE = _code(
    'int items = boxes * perBox;',
    'System.out.print("Start: ");',
    'System.out.println(items);',
    'items = items + arrived * perBox;',
    'System.out.print("After delivery: ");',
    'System.out.println(items);',
    'items = items - sold;',
    'System.out.print("After sales: ");',
    'System.out.println(items);',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-flow-piggy-bank", title="Копилка",
        given=[("int", "start"), ("int", "gift"), ("int", "spent")],
        variants=[{"start": "300", "gift": "500", "spent": "250"}, {"start": "1200", "gift": "1000", "spent": "700"},
                  {"start": "50", "gift": "200", "spent": "120"}],
        hidden=[{"start": "0", "gift": "100", "spent": "30"}, {"start": "800", "gift": "300", "spent": "1000"},
                {"start": "150", "gift": "0", "spent": "50"}],
        intro="В копилке у Миши лежало `start` руб. Бабушка подарила ему `gift` руб., а потом он потратил `spent` руб. в магазине.",
        steps=["Объяви переменную `int money` со значением `start` и выведи строку `Start: ` и значение `money`.",
               "Прибавь подарок: `money = money + gift;`. Выведи `After gift: ` и значение `money`.",
               "Вычти покупку из `money` так же и выведи `After shop: ` и значение `money`.",
               "Подписи выводи через `System.out.print`, значение — через `System.out.println`."],
        hint="Команды выполняются сверху вниз: каждая строка берёт значение `money`, которое получилось строкой выше.",
        solution=PIGGY,
        wrong=[("при покупке считает от начальной суммы и теряет подарок",
                _change(PIGGY, 'money = money - spent;', 'money = start - spent;')),
               ("печатает After gift до того, как прибавил подарок",
                PIGGY.replace('money = money + gift;\nSystem.out.print("After gift: ");\nSystem.out.println(money);',
                              'System.out.print("After gift: ");\nSystem.out.println(money);\nmoney = money + gift;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-flow-bookshelf", title="Книги на полке",
        given=[("int", "books"), ("int", "lent"), ("int", "bought")],
        variants=[{"books": "40", "lent": "3", "bought": "5"}, {"books": "12", "lent": "4", "bought": "1"},
                  {"books": "75", "lent": "10", "bought": "2"}],
        hidden=[{"books": "5", "lent": "5", "bought": "3"}, {"books": "20", "lent": "1", "bought": "7"},
                {"books": "33", "lent": "8", "bought": "0"}],
        intro="Утром на полке у Лены стояло `books` книг. Днём она дала подруге почитать `lent` книг, а вечером купила ещё `bought`.",
        steps=["Объяви переменную `int shelf` со значением `books` и выведи строку `Morning: ` и значение `shelf`.",
               "Вычти из `shelf` отданные книги, а следующей командой прибавь купленные — каждое изменение отдельной строкой вида `shelf = shelf ...;`.",
               "Выведи строку `Evening: ` и значение `shelf`.",
               "Подписи выводи через `System.out.print`, значение — через `System.out.println`."],
        hint="Вторая команда изменения должна начинать с того числа, которое осталось после первой, поэтому справа снова пишут `shelf`.",
        solution=SHELF,
        wrong=[("прибавляет купленные к утреннему числу и теряет отданные книги",
                _change(SHELF, 'shelf = shelf + bought;', 'shelf = books + bought;')),
               ("отданные книги прибавляет, а не вычитает",
                _change(SHELF, 'shelf = shelf - lent;', 'shelf = shelf + lent;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-flow-game-coins", title="Монеты в игре",
        given=[("int", "start"), ("int", "quest"), ("int", "shop")],
        variants=[{"start": "100", "quest": "50", "shop": "120"}, {"start": "40", "quest": "60", "shop": "35"},
                  {"start": "250", "quest": "150", "shop": "500"}],
        hidden=[{"start": "0", "quest": "10", "shop": "5"}, {"start": "75", "quest": "25", "shop": "200"},
                {"start": "300", "quest": "0", "shop": "100"}],
        intro="У игрока `start` монет. Он прошёл задание и получил `quest` монет, потом сработал бонус выходного дня — "
              "все монеты удвоились, а потом он купил в магазине меч за `shop` монет.",
        steps=["Объяви переменную `int coins` со значением `start` и прибавь к ней награду за задание. "
               "Выведи `After quest: ` и значение `coins`.",
               "Удвой монеты: `coins = coins * 2;`. Выведи `Weekend x2: ` и значение `coins`.",
               "Вычти цену меча и выведи `After shop: ` и значение `coins`.",
               "Подписи выводи через `System.out.print`, значение — через `System.out.println`."],
        hint="Порядок важен: бонус удваивает монеты вместе с наградой за задание, поэтому награду прибавляют раньше удвоения.",
        solution=COINS,
        wrong=[("удваивает начальные монеты и теряет награду за задание",
                _change(COINS, 'coins = coins * 2;', 'coins = start * 2;')),
               ("удваивает до того, как прибавить награду",
                _swap(COINS, 'coins = coins + quest;', 'coins = coins * 2;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-flow-price-change", title="Цена изменилась",
        given=[("int", "price"), ("int", "raise"), ("int", "discount"), ("int", "count")],
        variants=[{"price": "200", "raise": "50", "discount": "30", "count": "3"},
                  {"price": "990", "raise": "110", "discount": "200", "count": "2"},
                  {"price": "75", "raise": "25", "discount": "10", "count": "6"}],
        hidden=[{"price": "100", "raise": "20", "discount": "20", "count": "5"},
                {"price": "450", "raise": "0", "discount": "50", "count": "1"},
                {"price": "60", "raise": "40", "discount": "15", "count": "4"}],
        intro="Магазин поднял цену товара на `raise` руб., а на распродаже снизил её на `discount` руб. Сначала товар стоил "
              "`price` руб. Покупатель берёт `count` штук по новой цене.",
        steps=["Объяви переменную `int oldPrice` и сохрани в неё `price` — до любых изменений.",
               "Измени поле `price`: сначала прибавь `raise`, потом вычти `discount`.",
               "Объяви переменную `int total` — новая цена, умноженная на `count`.",
               "Выведи три строки: `Old price: `, `New price: ` и `Total: `, после каждой подписи — своё число.",
               "Подписи выводи через `System.out.print`, числа — через `System.out.println`."],
        hint="Старую цену надо сохранить первой командой: после изменений поле `price` её уже не помнит.",
        solution=PRICE,
        wrong=[("считает покупку по старой цене",
                _change(PRICE, 'int total = price * count;', 'int total = oldPrice * count;')),
               ("сохраняет старую цену после того, как цена уже выросла",
                _swap(PRICE, 'int oldPrice = price;', 'price = price + raise;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-flow-card-balance", title="Баланс карты за день",
        given=[("int", "balance"), ("int", "salary"), ("int", "rent"), ("int", "food")],
        variants=[{"balance": "3000", "salary": "40000", "rent": "25000", "food": "2500"},
                  {"balance": "15000", "salary": "30000", "rent": "18000", "food": "4000"},
                  {"balance": "500", "salary": "52000", "rent": "30000", "food": "1800"}],
        hidden=[{"balance": "0", "salary": "20000", "rent": "15000", "food": "1000"},
                {"balance": "10000", "salary": "35000", "rent": "40000", "food": "3000"},
                {"balance": "7000", "salary": "0", "rent": "0", "food": "650"}],
        intro="Утром на карте было `balance` руб. За день пришла зарплата `salary` руб., списалась аренда `rent` руб., "
              "оплачены продукты на `food` руб., и банк вернул кешбэк 50 руб.",
        steps=["Объяви переменную `int start` и сохрани в неё утренний `balance`.",
               "Измени поле `balance` четырьмя командами по порядку событий: зарплата, аренда, продукты, кешбэк 50 руб.",
               "Объяви переменную `int change` — насколько баланс изменился за день: вечерний минус утренний.",
               "Выведи две строки: `Balance: ` и вечерний баланс, затем `Change: ` и `change`.",
               "Подписи выводи через `System.out.print`, числа — через `System.out.println`."],
        hint="Каждая команда вида `balance = balance - rent;` берёт результат предыдущей. Утренний баланс нужен в конце, "
             "поэтому его сохраняют в `start` раньше всех изменений.",
        solution=CARD,
        wrong=[("вычитает в обратном порядке: утренний минус вечерний",
                _change(CARD, 'int change = balance - start;', 'int change = start - balance;')),
               ("продукты прибавляет к балансу, а не вычитает",
                _change(CARD, 'balance = balance - food;', 'balance = balance + food;')),
               ("сохраняет утренний баланс уже после зарплаты",
                _swap(CARD, 'int start = balance;', 'balance = balance + salary;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-flow-warehouse", title="Склад за день",
        given=[("int", "boxes"), ("int", "perBox"), ("int", "arrived"), ("int", "sold")],
        variants=[{"boxes": "10", "perBox": "12", "arrived": "5", "sold": "70"},
                  {"boxes": "4", "perBox": "24", "arrived": "3", "sold": "100"},
                  {"boxes": "20", "perBox": "6", "arrived": "10", "sold": "35"}],
        hidden=[{"boxes": "0", "perBox": "10", "arrived": "2", "sold": "15"},
                {"boxes": "7", "perBox": "8", "arrived": "0", "sold": "56"},
                {"boxes": "15", "perBox": "20", "arrived": "6", "sold": "1"}],
        intro="Утром на складе было `boxes` коробок с тетрадями, в каждой коробке `perBox` тетрадей. Днём привезли ещё "
              "`arrived` таких же коробок, а к вечеру продали `sold` тетрадей поштучно.",
        steps=["Объяви переменную `int items` — сколько тетрадей было утром, и выведи `Start: ` и `items`.",
               "Прибавь к `items` тетради из привезённых коробок и выведи `After delivery: ` и `items`.",
               "Вычти проданные тетради и выведи `After sales: ` и `items`.",
               "Подписи выводи через `System.out.print`, числа — через `System.out.println`."],
        hint="Привезли коробки, а считаем тетради: прибавлять нужно `arrived * perBox`. Умножение выполнится раньше сложения.",
        solution=STORE,
        wrong=[("прибавляет число коробок вместо числа тетрадей в них",
                _change(STORE, 'items = items + arrived * perBox;', 'items = items + arrived;')),
               ("после продаж считает от утреннего запаса и теряет поставку",
                _change(STORE, 'items = items - sold;', 'items = boxes * perBox - sold;'))],
        constructs=["assignment"],
    ),
]
