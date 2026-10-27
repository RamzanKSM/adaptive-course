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


PURSE = _code(
    'int money = tens * 10 + fives * 5;',
    'int need = goal - money;',
    'System.out.print("Saved: ");',
    'System.out.print(money);',
    'System.out.println(" rub");',
    'System.out.print("Need: ");',
    'System.out.print(need);',
    'System.out.println(" rub");',
)

HIKE = _code(
    'int people = boys + girls + 2;',
    'int sandwiches = people * days * 3;',
    'int water = (people * 2 + 5) * days;',
    'System.out.print("People: ");',
    'System.out.println(people);',
    'System.out.print("Sandwiches: ");',
    'System.out.println(sandwiches);',
    'System.out.print("Water: ");',
    'System.out.print(water);',
    'System.out.println(" l");',
)

COTTAGE = _code(
    'int house = nights * price;',
    'int extra = (guests - 4) * 500 * nights;',
    'int total = house + extra + 1500;',
    'int left = budget - total;',
    'System.out.print("House: ");',
    'System.out.println(house);',
    'System.out.print("Extra guests: ");',
    'System.out.println(extra);',
    'System.out.print("Total: ");',
    'System.out.println(total);',
    'System.out.print("Left: ");',
    'System.out.println(left);',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ar-rt-coin-purse", title="Мелочь на наушники",
        given=[("int", "tens"), ("int", "fives"), ("int", "goal")],
        variants=[{"tens": "12", "fives": "7", "goal": "500"}, {"tens": "30", "fives": "4", "goal": "400"},
                  {"tens": "5", "fives": "20", "goal": "200"}],
        hidden=[{"tens": "0", "fives": "1", "goal": "100"}, {"tens": "40", "fives": "0", "goal": "400"},
                {"tens": "17", "fives": "9", "goal": "1000"}],
        intro="Маша копит на наушники стоимостью `goal` руб. В кошельке у неё `tens` монет по 10 руб. и `fives` монет по 5 руб.",
        steps=["Объяви переменную `int money` — сколько денег в кошельке: монеты по 10, умноженные на 10, плюс монеты по 5, умноженные на 5.",
               "Объяви переменную `int need` — сколько ещё не хватает до `goal`.",
               "Выведи две строки: `Saved: … rub` и `Need: … rub`, например `Saved: 155 rub`.",
               "Число в строке выводи отдельной командой `System.out.print`, а ` rub` — командой `System.out.println`."],
        hint="Умножение выполняется раньше сложения, поэтому `tens * 10 + fives * 5` считается правильно и без скобок.",
        solution=PURSE,
        wrong=[("забывает умножить пятирублёвые монеты на 5: считает их штуки, а не рубли",
                _change(PURSE, 'int money = tens * 10 + fives * 5;', 'int money = tens * 10 + fives;')),
               ("вычитает в обратном порядке: деньги в кошельке минус цель",
                _change(PURSE, 'int need = goal - money;', 'int need = money - goal;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ar-rt-hike-supplies", title="Запасы на поход",
        given=[("int", "boys"), ("int", "girls"), ("int", "days")],
        variants=[{"boys": "6", "girls": "5", "days": "3"}, {"boys": "4", "girls": "8", "days": "2"},
                  {"boys": "10", "girls": "7", "days": "4"}],
        hidden=[{"boys": "1", "girls": "1", "days": "1"}, {"boys": "9", "girls": "3", "days": "5"},
                {"boys": "0", "girls": "12", "days": "2"}],
        intro="В поход идут `boys` мальчиков, `girls` девочек и два вожатых, поход длится `days` дней. "
              "Каждый съедает 3 бутерброда в день. Воды в день нужно по 2 литра на человека и ещё 5 литров на готовку.",
        steps=["Объяви переменную `int people` — сколько всего людей в походе, вместе с двумя вожатыми.",
               "Объяви переменную `int sandwiches` — сколько бутербродов нужно на весь поход.",
               "Объяви переменную `int water` — сколько литров воды нужно на весь поход: воду за один день умножь на число дней.",
               "Выведи три строки: `People: ` и число людей, `Sandwiches: ` и число бутербродов, `Water: `, литры и ` l` — "
               "например `Water: 54 l`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть — через `System.out.println`."],
        hint="Вода за один день — это `people * 2 + 5`. Чтобы умножить на дни всю эту сумму, а не только пятёрку, возьми её в скобки.",
        solution=HIKE,
        wrong=[("без скобок: на число дней умножаются только 5 литров на готовку",
                _change(HIKE, 'int water = (people * 2 + 5) * days;', 'int water = people * 2 + 5 * days;')),
               ("забывает двух вожатых",
                _change(HIKE, 'int people = boys + girls + 2;', 'int people = boys + girls;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ar-rt-cottage-rent", title="Аренда дома на выходные",
        given=[("int", "nights"), ("int", "price"), ("int", "guests"), ("int", "budget")],
        variants=[{"nights": "2", "price": "4000", "guests": "6", "budget": "15000"},
                  {"nights": "3", "price": "3500", "guests": "5", "budget": "14000"},
                  {"nights": "4", "price": "5000", "guests": "8", "budget": "30000"}],
        hidden=[{"nights": "1", "price": "3000", "guests": "4", "budget": "5000"},
                {"nights": "5", "price": "2500", "guests": "7", "budget": "25000"},
                {"nights": "2", "price": "6000", "guests": "9", "budget": "20000"}],
        intro="Друзья снимают загородный дом на `nights` ночей по `price` руб. за ночь. В цену входят 4 гостя, за каждого "
              "следующего берут 500 руб. за каждую ночь. Уборка после отъезда — 1500 руб. Едут `guests` человек "
              "(не меньше четырёх), у них есть `budget` руб.",
        steps=["Объяви переменную `int house` — плата за ночи без доплат.",
               "Объяви переменную `int extra` — доплата за гостей сверх четырёх за все ночи.",
               "Объяви переменную `int total` — дом, доплата и уборка вместе, и переменную `int left` — сколько останется от `budget`.",
               "Выведи четыре строки: `House: `, `Extra guests: `, `Total: ` и `Left: `, после каждой подписи — своё число.",
               "Подписи выводи через `System.out.print`, числа — через `System.out.println`."],
        hint="Лишних гостей `guests - 4`. Эту разность возьми в скобки, прежде чем умножать на 500 и на число ночей.",
        solution=COTTAGE,
        wrong=[("без скобок: из числа гостей вычитает 4 * 500 * nights",
                _change(COTTAGE, 'int extra = (guests - 4) * 500 * nights;', 'int extra = guests - 4 * 500 * nights;')),
               ("доплату считает только за одну ночь",
                _change(COTTAGE, 'int extra = (guests - 4) * 500 * nights;', 'int extra = (guests - 4) * 500;'))],
        constructs=["assignment"],
    ),
]
