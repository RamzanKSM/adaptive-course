"""ARITHMETIC_BASIC — «Арифметика» (Java). Taught before: System.out.println / print, variables (`int`, `String`),
assignment. This topic: `+`, `-`, `*` on `int` values, the order of operations (multiplication first) and parentheses,
storing an intermediate result in a variable.
Not yet: division `/` and remainder `%` (topic «Целочисленное деление»), `+=`, double, string concatenation (a line is
assembled from several print calls), conditions, loops."""
from java_tasks import JavaOutputTask

SKILL = "ARITHMETIC_BASIC"


def _code(*lines: str) -> str:
    return "\n".join(lines)


def _change(code: str, old: str, new: str, nth: int = 1) -> str:
    """The code with the nth line equal to `old` replaced by `new` (a one-line mistake)."""
    lines = code.split("\n")
    found = [i for i, line in enumerate(lines) if line == old]
    assert len(found) >= nth, f"no line {old!r}"
    lines[found[nth - 1]] = new
    return "\n".join(lines)


CAFE = _code(
    'int juiceCost = juicePrice * juices;',
    'int total = pizza + juiceCost;',
    'System.out.print("Juice: ");',
    'System.out.print(juiceCost);',
    'System.out.println(" rub");',
    'System.out.print("Total: ");',
    'System.out.print(total);',
    'System.out.println(" rub");',
)

PARKING = _code(
    'int cost = hours * rate;',
    'int change = paid - cost;',
    'System.out.print("Cost: ");',
    'System.out.println(cost);',
    'System.out.print("Change: ");',
    'System.out.println(change);',
)

FENCE = _code(
    'int perimeter = 2 * (length + width);',
    'int cost = perimeter * price;',
    'System.out.print("Fence: ");',
    'System.out.print(perimeter);',
    'System.out.println(" m");',
    'System.out.print("Cost: ");',
    'System.out.print(cost);',
    'System.out.println(" rub");',
)

TAXI = _code(
    'int distanceCost = km * 25;',
    'int waitCost = minutes * 5;',
    'int total = 99 + distanceCost + waitCost;',
    'System.out.print("Distance: ");',
    'System.out.println(distanceCost);',
    'System.out.print("Waiting: ");',
    'System.out.println(waitCost);',
    'System.out.print("Total: ");',
    'System.out.println(total);',
)

PAINT = _code(
    'int walls = 2 * (length + width) * height;',
    'int paintArea = walls - door;',
    'int cost = paintArea * price;',
    'System.out.print("Walls, m2: ");',
    'System.out.println(walls);',
    'System.out.print("To paint, m2: ");',
    'System.out.println(paintArea);',
    'System.out.print("Cost, rub: ");',
    'System.out.println(cost);',
)

TRIP = _code(
    'int children = students * ticket;',
    'int grownups = adults * (ticket + 200);',
    'int total = children + grownups + 3000;',
    'int left = budget - total;',
    'System.out.print("Total: ");',
    'System.out.println(total);',
    'System.out.print("Left: ");',
    'System.out.println(left);',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ar-pizza-bill", title="Пицца и сок",
        given=[("int", "pizza"), ("int", "juicePrice"), ("int", "juices")],
        variants=[{"pizza": "650", "juicePrice": "90", "juices": "3"}, {"pizza": "520", "juicePrice": "120", "juices": "2"},
                  {"pizza": "780", "juicePrice": "75", "juices": "4"}],
        hidden=[{"pizza": "600", "juicePrice": "100", "juices": "1"}, {"pizza": "450", "juicePrice": "80", "juices": "5"},
                {"pizza": "900", "juicePrice": "110", "juices": "0"}],
        intro="Друзья заказали одну пиццу и несколько стаканов сока. Пицца стоит `pizza` руб., стакан сока — `juicePrice` руб., "
              "стаканов заказали `juices`.",
        steps=["Объяви переменную `int juiceCost` — стоимость всего сока: цена стакана, умноженная на число стаканов.",
               "Объяви переменную `int total` — пицца плюс сок.",
               "Выведи две строки: `Juice: … rub` и `Total: … rub`, например `Juice: 270 rub`.",
               "Число в строке выводи отдельной командой `System.out.print`, а ` rub` — командой `System.out.println`."],
        hint="Умножение в Java пишется звёздочкой: `juicePrice * juices`. В `total` складывай пиццу с уже посчитанным `juiceCost`.",
        solution=CAFE,
        wrong=[("в сумме складывает пиццу с ценой одного стакана, а не всего сока",
                _change(CAFE, 'int total = pizza + juiceCost;', 'int total = pizza + juicePrice;')),
               ("складывает цену стакана с числом стаканов вместо умножения",
                _change(CAFE, 'int juiceCost = juicePrice * juices;', 'int juiceCost = juicePrice + juices;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ar-parking-change", title="Сдача на парковке",
        given=[("int", "hours"), ("int", "rate"), ("int", "paid")],
        variants=[{"hours": "3", "rate": "60", "paid": "200"}, {"hours": "5", "rate": "40", "paid": "500"},
                  {"hours": "2", "rate": "150", "paid": "1000"}],
        hidden=[{"hours": "1", "rate": "100", "paid": "100"}, {"hours": "4", "rate": "70", "paid": "300"},
                {"hours": "8", "rate": "50", "paid": "1000"}],
        intro="Паркомат берёт `rate` руб. за каждый час стоянки. Машина простояла `hours` часов, водитель внёс `paid` руб.",
        steps=["Объяви переменную `int cost` — плата за стоянку: часы, умноженные на цену часа.",
               "Объяви переменную `int change` — сдача: сколько внесено, минус плата.",
               "Выведи две строки: `Cost: ` и плата, затем `Change: ` и сдача, например `Cost: 180`.",
               "Подписи выводи через `System.out.print`, числа — через `System.out.println`."],
        hint="При вычитании важен порядок: из большего (внесённых денег) вычитают меньшее (плату).",
        solution=PARKING,
        wrong=[("вычитает в обратном порядке: плата минус внесённые деньги",
                _change(PARKING, 'int change = paid - cost;', 'int change = cost - paid;')),
               ("складывает часы с ценой часа вместо умножения",
                _change(PARKING, 'int cost = hours * rate;', 'int cost = hours + rate;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ar-garden-fence", title="Забор вокруг грядки",
        given=[("int", "length"), ("int", "width"), ("int", "price")],
        variants=[{"length": "6", "width": "4", "price": "350"}, {"length": "10", "width": "3", "price": "200"},
                  {"length": "8", "width": "8", "price": "500"}],
        hidden=[{"length": "5", "width": "2", "price": "100"}, {"length": "12", "width": "7", "price": "250"},
                {"length": "3", "width": "9", "price": "400"}],
        intro="Прямоугольную грядку длиной `length` м и шириной `width` м обносят забором по всему краю. "
              "Метр забора стоит `price` руб.",
        steps=["Объяви переменную `int perimeter` — длина забора: дважды сумма длины и ширины.",
               "Объяви переменную `int cost` — стоимость забора: длина забора, умноженная на цену метра.",
               "Выведи две строки: `Fence: … m` и `Cost: … rub`, например `Fence: 20 m`.",
               "Число выводи отдельной командой `System.out.print`, а ` m` или ` rub` — командой `System.out.println`."],
        hint="Умножение выполняется раньше сложения, поэтому сумму длины и ширины нужно взять в скобки: `2 * (length + width)`.",
        solution=FENCE,
        wrong=[("без скобок: удваивает только длину",
                _change(FENCE, 'int perimeter = 2 * (length + width);', 'int perimeter = 2 * length + width;')),
               ("считает площадь грядки вместо длины забора",
                _change(FENCE, 'int perimeter = 2 * (length + width);', 'int perimeter = length * width;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ar-taxi-fare", title="Поездка на такси",
        given=[("int", "km"), ("int", "minutes")],
        variants=[{"km": "12", "minutes": "4"}, {"km": "5", "minutes": "0"}, {"km": "30", "minutes": "10"}],
        hidden=[{"km": "1", "minutes": "1"}, {"km": "18", "minutes": "7"}, {"km": "45", "minutes": "3"}],
        intro="Такси берёт 99 руб. за посадку, 25 руб. за каждый километр и 5 руб. за каждую минуту ожидания. "
              "Поездка заняла `km` км, ждать пришлось `minutes` мин.",
        steps=["Объяви переменную `int distanceCost` — плата за километры, и переменную `int waitCost` — плата за ожидание.",
               "Объяви переменную `int total` — посадка плюс плата за километры плюс плата за ожидание.",
               "Выведи три строки: `Distance: ` и плата за километры, `Waiting: ` и плата за ожидание, `Total: ` и итог.",
               "Подписи выводи через `System.out.print`, числа — через `System.out.println`."],
        hint="Числа тарифа можно писать прямо в выражении: `km * 25`. Не забудь 99 руб. за посадку в итоге.",
        solution=TAXI,
        wrong=[("забывает плату за посадку",
                _change(TAXI, 'int total = 99 + distanceCost + waitCost;', 'int total = distanceCost + waitCost;')),
               ("плату за ожидание считает сложением, а не умножением",
                _change(TAXI, 'int waitCost = minutes * 5;', 'int waitCost = minutes + 5;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ar-wall-paint", title="Покраска стен",
        given=[("int", "length"), ("int", "width"), ("int", "height"), ("int", "door"), ("int", "price")],
        variants=[{"length": "5", "width": "4", "height": "3", "door": "2", "price": "120"},
                  {"length": "6", "width": "3", "height": "2", "door": "3", "price": "90"},
                  {"length": "4", "width": "4", "height": "3", "door": "4", "price": "150"}],
        hidden=[{"length": "3", "width": "2", "height": "2", "door": "2", "price": "100"},
                {"length": "7", "width": "5", "height": "3", "door": "5", "price": "80"},
                {"length": "2", "width": "6", "height": "4", "door": "3", "price": "110"}],
        intro="Стены комнаты-прямоугольника длиной `length` м, шириной `width` м и высотой `height` м красят краской. "
              "Дверь площадью `door` кв. м не красят. Работа стоит `price` руб. за квадратный метр.",
        steps=["Объяви переменную `int walls` — площадь всех четырёх стен: периметр пола `2 * (length + width)`, умноженный на высоту.",
               "Объяви переменную `int paintArea` — площадь стен без двери.",
               "Объяви переменную `int cost` — стоимость работы за `paintArea` квадратных метров.",
               "Выведи три строки: `Walls, m2: `, `To paint, m2: ` и `Cost, rub: `, после каждой подписи — своё число.",
               "Подписи выводи через `System.out.print`, числа — через `System.out.println`."],
        hint="Каждое следующее значение считается из предыдущего: сначала все стены, потом без двери, потом деньги.",
        solution=PAINT,
        wrong=[("без скобок: высота умножается только на ширину",
                _change(PAINT, 'int walls = 2 * (length + width) * height;', 'int walls = 2 * length + width * height;')),
               ("считает стоимость за все стены, забыв вычесть дверь",
                _change(PAINT, 'int cost = paintArea * price;', 'int cost = walls * price;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ar-class-trip", title="Экскурсия класса",
        given=[("int", "students"), ("int", "adults"), ("int", "ticket"), ("int", "budget")],
        variants=[{"students": "25", "adults": "2", "ticket": "300", "budget": "12000"},
                  {"students": "18", "adults": "3", "ticket": "450", "budget": "15000"},
                  {"students": "30", "adults": "4", "ticket": "200", "budget": "11000"}],
        hidden=[{"students": "10", "adults": "1", "ticket": "500", "budget": "9000"},
                {"students": "22", "adults": "2", "ticket": "350", "budget": "12000"},
                {"students": "15", "adults": "5", "ticket": "100", "budget": "6000"}],
        intro="Класс едет в музей. Детский билет стоит `ticket` руб., взрослый — на 200 руб. дороже. Едут `students` "
              "учеников и `adults` взрослых, автобус стоит 3000 руб. на всех. Родители собрали `budget` руб.",
        steps=["Объяви переменную `int children` — билеты учеников, и переменную `int grownups` — билеты взрослых "
               "(цена взрослого билета — `ticket + 200`).",
               "Объяви переменную `int total` — все билеты плюс автобус.",
               "Объяви переменную `int left` — сколько денег останется от `budget`.",
               "Выведи две строки: `Total: ` и `total`, затем `Left: ` и `left`.",
               "Подписи выводи через `System.out.print`, числа — через `System.out.println`."],
        hint="Цену взрослого билета возьми в скобки: `adults * (ticket + 200)`. Без скобок 200 прибавится один раз, а не за каждого взрослого.",
        solution=TRIP,
        wrong=[("без скобок: 200 руб. прибавляет один раз, а не за каждого взрослого",
                _change(TRIP, 'int grownups = adults * (ticket + 200);', 'int grownups = adults * ticket + 200;')),
               ("вычитает в обратном порядке: итог минус бюджет",
                _change(TRIP, 'int left = budget - total;', 'int left = total - budget;'))],
        constructs=["assignment"],
    ),
]
