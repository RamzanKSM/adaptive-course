"""OBJECT_CREATION — «Создание объектов» (Java). Taught before: everything up to static methods of Solution, and
classes (fields, simple methods). Here: `new` makes a new, separate object every time; several objects of one class
keep their own field values; objects created in a loop and kept in an array; a variable holds a reference, so
`second = first` is the same object, not a copy. Not yet: constructors (topic 37), this, private, static fields."""
from java_tasks import JavaOutputTask

SKILL = "OBJECT_CREATION"


def find_class(name: str) -> str:
    return (f'Class<?> c = cls("{name}");\n'
            f'need(c != null, "Создай класс {name} ниже класса Solution (после его закрывающей скобки) и без слова public");\n')


def need_field(cls: str, name: str, java_type: str, why: str) -> str:
    """An instance (non-static) field of the class with this name and type."""
    return (f'{{ Field f = null; try {{ f = c.getDeclaredField("{name}"); }} catch (NoSuchFieldException e) {{ }}\n'
            f'  need(f != null && f.getType() == {java_type}.class, "Объяви в классе {cls} поле {java_type} {name} — {why}");\n'
            f'  need(!Modifier.isStatic(f.getModifiers()), "Объяви поле {name} в классе {cls} без слова static — тогда у каждого объекта будет своё значение"); }}\n')


# ───────── Suitcases ─────────

SUITCASE = '''class Suitcase {
    String owner;
    int kg;
}'''

SUITCASE_MAIN = '''Suitcase first = new Suitcase();
first.owner = owner1;
first.kg = kg1;
Suitcase second = new Suitcase();
second.owner = owner2;
second.kg = kg2;
System.out.println(first.owner + ": " + first.kg + " kg");
System.out.println(second.owner + ": " + second.kg + " kg");
System.out.println("Together: " + (first.kg + second.kg) + " kg");'''

# ───────── Cafe orders ─────────

ORDER = '''class Order {
    int number;
    String dish;
    int price;
}'''

ORDER_MAIN = '''Order[] orders = new Order[dishes.length];
for (int i = 0; i < dishes.length; i++) {
    Order order = new Order();
    order.number = i + 1;
    order.dish = dishes[i];
    order.price = prices[i];
    orders[i] = order;
}
int total = 0;
for (int i = 0; i < orders.length; i++) {
    System.out.println("Order #" + orders[i].number + ": " + orders[i].dish + ", " + orders[i].price + " rub");
    total += orders[i].price;
}
System.out.println("Total: " + total + " rub");'''

ORDER_ONE_OBJECT = '''Order[] orders = new Order[dishes.length];
Order order = new Order();
for (int i = 0; i < dishes.length; i++) {
    order.number = i + 1;
    order.dish = dishes[i];
    order.price = prices[i];
    orders[i] = order;
}
int total = 0;
for (int i = 0; i < orders.length; i++) {
    System.out.println("Order #" + orders[i].number + ": " + orders[i].dish + ", " + orders[i].price + " rub");
    total += orders[i].price;
}
System.out.println("Total: " + total + " rub");'''

# ───────── Elections ─────────

CANDIDATE = '''class Candidate {
    String name;
    int votes;
}'''

ELECTION_MAIN = '''Candidate first = new Candidate();
first.name = name1;
Candidate second = new Candidate();
second.name = name2;
for (int i = 0; i < ballots.length; i++) {
    if (ballots[i].equals(first.name)) {
        first.votes++;
    } else {
        second.votes++;
    }
}
System.out.println(first.name + ", votes: " + first.votes);
System.out.println(second.name + ", votes: " + second.votes);
if (first.votes > second.votes) {
    System.out.println("Leader: " + first.name);
} else if (second.votes > first.votes) {
    System.out.println("Leader: " + second.name);
} else {
    System.out.println("Draw");
}'''

# ───────── Plants ─────────

PLANT = """class Plant {
    String name;
    int height;
}"""

PLANT_MAIN = """Plant first = new Plant();
first.name = plant1;
first.height = height1;
Plant second = new Plant();
second.name = plant2;
second.height = height2;
second.height += growth;
System.out.println(first.name + ": " + first.height + " cm");
System.out.println(second.name + ": " + second.height + " cm");"""

# ───────── Race ─────────

RUNNER = """class Runner {
    String name;
    int seconds;
}"""

RACE_MAIN = """Runner[] runners = new Runner[names.length];
for (int i = 0; i < names.length; i++) {
    Runner runner = new Runner();
    runner.name = names[i];
    runner.seconds = seconds[i];
    runners[i] = runner;
}
Runner best = runners[0];
for (int i = 1; i < runners.length; i++) {
    if (runners[i].seconds < best.seconds) {
        best = runners[i];
    }
}
System.out.println("Runners: " + runners.length);
System.out.println("Winner: " + best.name + ", " + best.seconds + " s");"""

RACE_ONE_OBJECT = """Runner[] runners = new Runner[names.length];
Runner runner = new Runner();
for (int i = 0; i < names.length; i++) {
    runner.name = names[i];
    runner.seconds = seconds[i];
    runners[i] = runner;
}
Runner best = runners[0];
for (int i = 1; i < runners.length; i++) {
    if (runners[i].seconds < best.seconds) {
        best = runners[i];
    }
}
System.out.println("Runners: " + runners.length);
System.out.println("Winner: " + best.name + ", " + best.seconds + " s");"""

# ───────── Dice game ─────────

PLAYER = """class Player {
    String name;
    int points;
}"""

DICE_MAIN = """Player first = new Player();
first.name = name1;
Player second = new Player();
second.name = name2;
Player current = first;
for (int i = 0; i < rolls.length; i++) {
    current.points += rolls[i];
    if (rolls[i] != 6) {
        if (current == first) {
            current = second;
        } else {
            current = first;
        }
    }
}
System.out.println(first.name + ": " + first.points + " points");
System.out.println(second.name + ": " + second.points + " points");
if (first.points > second.points) {
    System.out.println("Winner: " + first.name);
} else if (second.points > first.points) {
    System.out.println("Winner: " + second.name);
} else {
    System.out.println("Draw");
}"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-obj-two-suitcases", title="Два чемодана",
        given=[("String", "owner1"), ("int", "kg1"), ("String", "owner2"), ("int", "kg2")],
        variants=[{"owner1": '"Anya"', "kg1": "12", "owner2": '"Boris"', "kg2": "18"},
                  {"owner1": '"Oleg"', "kg1": "20", "owner2": '"Ira"', "kg2": "9"},
                  {"owner1": '"Masha"', "kg1": "15", "owner2": '"Dima"', "kg2": "16"}],
        hidden=[{"owner1": '"Katya"', "kg1": "7", "owner2": '"Misha"', "kg2": "23"},
                {"owner1": '"Pavel"', "kg1": "25", "owner2": '"Lena"', "kg2": "4"},
                {"owner1": '"Nik"', "kg1": "10", "owner2": '"Eva"', "kg2": "10"}],
        intro="Двое друзей летят в отпуск, и у каждого свой чемодан. Владельцы и вес чемоданов в килограммах записаны "
              "в полях `owner1`, `kg1`, `owner2` и `kg2`. Чемоданы устроены одинаково, но у каждого свой владелец и свой вес — "
              "это два разных объекта одного класса.",
        steps=["Ниже класса `Solution` создай класс `Suitcase` (без `public`) с полями `String owner` и `int kg`.",
               "В `main` создай два отдельных объекта: `Suitcase first = new Suitcase();` и `Suitcase second = new Suitcase();`. "
               "Заполни поля первого из `owner1` и `kg1`, а второго — из `owner2` и `kg2`.",
               "Выведи три строки: строку вида `Anya: 12 kg` для первого чемодана, такую же для второго и строку вида "
               "`Together: 30 kg` с суммой весов. Все значения бери из полей объектов `first` и `second`."],
        hint="Каждый вызов `new Suitcase()` создаёт новый, отдельный объект со своими полями. Поэтому `first.kg` и "
             "`second.kg` хранят разные значения, хотя класс у них один.",
        solution=SUITCASE_MAIN,
        classes=SUITCASE,
        wrong=[("второй чемодан — не новый объект, а тот же самый: `Suitcase second = first;`, и его данные затирают первый",
                SUITCASE_MAIN.replace("Suitcase second = new Suitcase();", "Suitcase second = first;")),
               ("поля класса объявлены static — оба объекта делят одни и те же значения",
                SUITCASE_MAIN, SUITCASE.replace("    String owner;", "    static String owner;").replace("    int kg;", "    static int kg;"))],
        constructs=["class"],
        checks=find_class("Suitcase")
               + need_field("Suitcase", "owner", "String", "владелец чемодана")
               + need_field("Suitcase", "kg", "int", "вес чемодана в килограммах"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-obj-cafe-orders", title="Заказы в кафе",
        given=[("String[]", "dishes"), ("int[]", "prices")],
        variants=[{"dishes": '{"Soup", "Pilaf", "Juice"}', "prices": "{250, 400, 90}"},
                  {"dishes": '{"Pancakes", "Tea"}', "prices": "{180, 60}"},
                  {"dishes": '{"Salad", "Borsch", "Cutlet", "Juice"}', "prices": "{220, 280, 310, 100}"}],
        hidden=[{"dishes": '{"Pizza"}', "prices": "{550}"},
                {"dishes": '{"Omelet", "Coffee", "Toast"}', "prices": "{200, 150, 260}"},
                {"dishes": '{"Pasta", "Lemonade", "Cake", "Tea", "Bread"}', "prices": "{390, 120, 210, 50, 30}"}],
        intro="Официант принимает заказ за столиком: блюда записаны по порядку в массиве `dishes`, а их цены — "
              "в массиве `prices` под теми же номерами. Для кухни каждое блюдо — отдельный заказ со своим номером.",
        steps=["Ниже класса `Solution` создай класс `Order` (без `public`) с полями `int number`, `String dish` и `int price`.",
               "В `main` создай массив `Order[] orders = new Order[dishes.length];`. В цикле для каждого блюда создай "
               "новый объект `new Order()`, запиши в него номер (первое блюдо — заказ №1, дальше по порядку), блюдо и цену "
               "и положи объект в массив.",
               "Вторым циклом пройди по массиву `orders` и для каждого заказа выведи строку вида `Order #1: Soup, 250 rub`.",
               "Последней строкой выведи строку вида `Total: 740 rub` — сумму цен всех заказов из массива `orders`."],
        hint="Объект нужно создавать внутри цикла: каждое `new Order()` — это новый заказ. Если создать один объект "
             "до цикла и класть в массив его, все ячейки массива будут указывать на один и тот же заказ — последний.",
        solution=ORDER_MAIN,
        classes=ORDER,
        wrong=[("создаёт один объект до цикла — все ячейки массива указывают на последний заказ", ORDER_ONE_OBJECT),
               ("номера заказов начинаются с 0, а не с 1", ORDER_MAIN.replace("order.number = i + 1;", "order.number = i;"))],
        constructs=["class"],
        checks=find_class("Order")
               + need_field("Order", "number", "int", "номер заказа")
               + need_field("Order", "dish", "String", "название блюда")
               + need_field("Order", "price", "int", "цена блюда"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-obj-class-election", title="Выборы старосты",
        given=[("String", "name1"), ("String", "name2"), ("String[]", "ballots")],
        variants=[{"name1": '"Anya"', "name2": '"Boris"', "ballots": '{"Anya", "Boris", "Anya", "Anya", "Boris"}'},
                  {"name1": '"Gleb"', "name2": '"Nina"', "ballots": '{"Nina", "Nina", "Gleb", "Nina"}'},
                  {"name1": '"Sveta"', "name2": '"Artem"', "ballots": '{"Artem", "Sveta", "Sveta", "Artem"}'}],
        hidden=[{"name1": '"Dasha"', "name2": '"Egor"', "ballots": '{"Egor"}'},
                {"name1": '"Kira"', "name2": '"Lesha"', "ballots": '{"Kira", "Kira", "Kira"}'},
                {"name1": '"Roma"', "name2": '"Yulya"', "ballots": "{}"},
                {"name1": '"Vanya"', "name2": '"Tanya"', "ballots": '{"Tanya", "Vanya", "Vanya", "Tanya", "Tanya", "Vanya", "Tanya"}'}],
        intro="В классе выбирают старосту из двух кандидатов — `name1` и `name2`. Каждый ученик написал на бюллетене "
              "имя одного из них; все бюллетени по порядку записаны в массиве `ballots`. У каждого кандидата свой "
              "счёт голосов, поэтому кандидаты — два отдельных объекта.",
        steps=["Ниже класса `Solution` создай класс `Candidate` (без `public`) с полями `String name` и `int votes`.",
               "В `main` создай два объекта-кандидата: `first` с именем из `name1` и `second` с именем из `name2`. "
               "Голосов у нового объекта сначала 0 — поле `int` само начинается с нуля.",
               "Пройди по массиву `ballots`: если в бюллетене имя первого кандидата, прибавь 1 к `first.votes`, иначе — "
               "к `second.votes`. Строки сравнивай методом `equals`.",
               "Выведи две строки вида `Anya, votes: 3` — сначала для первого кандидата, потом для второго. Третьей строкой "
               "выведи `Leader: Anya` с именем того, у кого голосов больше, а если голосов поровну — `Draw`."],
        hint="Голоса копятся в полях объектов: `first.votes++` меняет счёт только первого кандидата, потому что `first` и "
             "`second` — два разных объекта, созданных двумя вызовами `new`.",
        solution=ELECTION_MAIN,
        classes=CANDIDATE,
        wrong=[("второй кандидат — тот же объект, что и первый (`second = first`), и все голоса попадают в один счёт",
                ELECTION_MAIN.replace("Candidate second = new Candidate();", "Candidate second = first;")),
               ("забыл else — каждый бюллетень засчитывается второму кандидату",
                ELECTION_MAIN.replace("        first.votes++;\n    } else {\n        second.votes++;\n    }",
                                      "        first.votes++;\n    }\n    second.votes++;"))],
        constructs=["class"],
        checks=find_class("Candidate")
               + need_field("Candidate", "name", "String", "имя кандидата")
               + need_field("Candidate", "votes", "int", "сколько голосов набрал кандидат"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-obj-two-plants", title="Два цветка на подоконнике",
        given=[("String", "plant1"), ("int", "height1"), ("String", "plant2"), ("int", "height2"), ("int", "growth")],
        variants=[{"plant1": '"Ficus"', "height1": "40", "plant2": '"Cactus"', "height2": "15", "growth": "5"},
                  {"plant1": '"Aloe"', "height1": "25", "plant2": '"Violet"', "height2": "10", "growth": "3"},
                  {"plant1": '"Palm"', "height1": "90", "plant2": '"Mint"', "height2": "20", "growth": "8"}],
        hidden=[{"plant1": '"Fern"', "height1": "30", "plant2": '"Basil"', "height2": "12", "growth": "0"},
                {"plant1": '"Lemon"', "height1": "55", "plant2": '"Orchid"', "height2": "35", "growth": "11"},
                {"plant1": '"Ivy"', "height1": "18", "plant2": '"Rose"', "height2": "18", "growth": "2"}],
        intro="На подоконнике стоят два цветка. Их названия и высота в сантиметрах записаны в полях `plant1`, `height1`, "
              "`plant2` и `height2`. Подкормку получил только второй цветок, и он вырос ещё на `growth` см.",
        steps=["Ниже класса `Solution` создай класс `Plant` (без `public`) с полями `String name` и `int height`.",
               "В `main` создай два отдельных объекта: `Plant first = new Plant();` и `Plant second = new Plant();`. "
               "Заполни первый из `plant1` и `height1`, второй — из `plant2` и `height2`.",
               "Увеличь высоту только второго цветка: `second.height += growth;`.",
               "Выведи две строки вида `Ficus: 40 cm` — сначала для первого цветка, потом для второго, значения бери "
               "из полей объектов."],
        hint="У каждого объекта свои поля: изменение `second.height` никак не трогает `first.height`, потому что "
             "`new` создал два разных цветка.",
        solution=PLANT_MAIN,
        classes=PLANT,
        wrong=[("второй цветок — не новый объект, а тот же самый: `Plant second = first;`",
                PLANT_MAIN.replace("Plant second = new Plant();", "Plant second = first;")),
               ("поля класса объявлены static — оба цветка делят одну высоту и одно название",
                PLANT_MAIN, PLANT.replace("    String name;", "    static String name;").replace("    int height;", "    static int height;"))],
        constructs=["class"],
        checks=find_class("Plant")
               + need_field("Plant", "name", "String", "название цветка")
               + need_field("Plant", "height", "int", "высота в сантиметрах"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-obj-race-winner", title="Победитель забега",
        given=[("String[]", "names"), ("int[]", "seconds")],
        variants=[{"names": '{"Anya", "Boris", "Vika"}', "seconds": "{62, 58, 65}"},
                  {"names": '{"Gleb", "Dasha", "Egor", "Zoya"}', "seconds": "{71, 74, 69, 70}"},
                  {"names": '{"Ilya", "Kira"}', "seconds": "{55, 60}"}],
        hidden=[{"names": '{"Lev"}', "seconds": "{80}"},
                {"names": '{"Mila", "Nik", "Olya", "Petya", "Rita"}', "seconds": "{66, 64, 70, 63, 68}"},
                {"names": '{"Sasha", "Tanya", "Uma"}', "seconds": "{59, 61, 57}"},
                {"names": '{"Vera", "Yan"}', "seconds": "{75, 52}"}],
        intro="На школьной стометровке у каждого бегуна своё время. Имена записаны в массиве `names`, а время в секундах — "
              "в массиве `seconds` под теми же номерами. Каждый бегун — отдельный объект.",
        steps=["Ниже класса `Solution` создай класс `Runner` (без `public`) с полями `String name` и `int seconds`.",
               "В `main` создай массив `Runner[] runners = new Runner[names.length];` и в цикле для каждого бегуна создай "
               "новый объект `new Runner()`, заполни его поля и положи в массив.",
               "Найди самого быстрого: заведи переменную `Runner best = runners[0];` и пройди по остальным бегунам; "
               "если у бегуна время меньше, чем у `best`, запомни в `best` этого бегуна. Времена у всех разные.",
               "Выведи две строки вида `Runners: 3` и `Winner: Boris, 58 s`, значения бери из массива и из полей `best`."],
        hint="Переменная `best` не копирует бегуна, а просто указывает на один из объектов массива. Поэтому через "
             "`best.name` и `best.seconds` видны данные именно этого бегуна.",
        solution=RACE_MAIN,
        classes=RUNNER,
        wrong=[("создаёт один объект до цикла — все ячейки массива указывают на последнего бегуна", RACE_ONE_OBJECT),
               ("перепутал знак сравнения — побеждает самый медленный",
                RACE_MAIN.replace("runners[i].seconds < best.seconds", "runners[i].seconds > best.seconds"))],
        constructs=["class", "for"],
        checks=find_class("Runner")
               + need_field("Runner", "name", "String", "имя бегуна")
               + need_field("Runner", "seconds", "int", "время в секундах"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-obj-dice-turns", title="Игра в кости",
        given=[("String", "name1"), ("String", "name2"), ("int[]", "rolls")],
        variants=[{"name1": '"Anya"', "name2": '"Boris"', "rolls": "{3, 6, 2, 5, 4}"},
                  {"name1": '"Gleb"', "name2": '"Nina"', "rolls": "{6, 6, 1, 2, 6, 3}"},
                  {"name1": '"Sveta"', "name2": '"Artem"', "rolls": "{4, 2, 6, 5}"}],
        hidden=[{"name1": '"Dasha"', "name2": '"Egor"', "rolls": "{5}"},
                {"name1": '"Kira"', "name2": '"Lesha"', "rolls": "{2, 6, 4, 6}"},
                {"name1": '"Roma"', "name2": '"Yulya"', "rolls": "{}"},
                {"name1": '"Vanya"', "name2": '"Tanya"', "rolls": "{1, 3, 6, 1, 2, 5, 6, 6, 4}"}],
        intro="Двое игроков — `name1` и `name2` — по очереди бросают кубик, первым ходит `name1`. Выпавшие очки по порядку "
              "записаны в массиве `rolls`. Кто выбросил 6, бросает ещё раз, иначе ход переходит к сопернику.",
        steps=["Ниже класса `Solution` создай класс `Player` (без `public`) с полями `String name` и `int points`.",
               "В `main` создай два объекта-игрока `first` и `second` с именами из `name1` и `name2`. Заведи переменную "
               "`Player current = first;` — она указывает на того, чей сейчас ход.",
               "Пройди по массиву `rolls`: прибавь очки к `current.points`; если выпало не 6, переключи ход — если "
               "`current == first`, присвой `current = second`, иначе `current = first`.",
               "Выведи две строки вида `Anya: 7 points` — для первого игрока, потом для второго. Третьей строкой выведи "
               "`Winner: Anya` с именем того, у кого очков больше, а при равенстве — `Draw`."],
        hint="`current` — не третий игрок, а ссылка на одного из двух объектов. Поэтому `current.points += ...` меняет "
             "очки того игрока, на которого `current` сейчас указывает.",
        solution=DICE_MAIN,
        classes=PLAYER,
        wrong=[("переключает ход после каждого броска, даже после шестёрки",
                DICE_MAIN.replace("    if (rolls[i] != 6) {\n        if (current == first) {\n            current = second;\n"
                                  "        } else {\n            current = first;\n        }\n    }",
                                  "    if (current == first) {\n        current = second;\n    } else {\n        current = first;\n    }")),
               ("при равенстве очков объявляет победителем второго игрока вместо Draw",
                DICE_MAIN.replace('} else if (second.points > first.points) {\n    System.out.println("Winner: " + second.name);\n'
                                  '} else {\n    System.out.println("Draw");\n}',
                                  '} else {\n    System.out.println("Winner: " + second.name);\n}'))],
        constructs=["class", "for", "if"],
        checks=find_class("Player")
               + need_field("Player", "name", "String", "имя игрока")
               + need_field("Player", "points", "int", "сколько очков набрал игрок"),
    ),
]
