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
]
