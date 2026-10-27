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


# ───────── Apple baskets ─────────

BASKET = '''class Basket {
    String color;
    int apples;
}'''

BASKET_MAIN = '''Basket first = new Basket();
first.color = color1;
first.apples = apples1;
Basket second = new Basket();
second.color = color2;
second.apples = apples2;
first.apples -= move;
second.apples += move;
System.out.println(first.color + " basket: " + first.apples + " apples");
System.out.println(second.color + " basket: " + second.apples + " apples");'''

# ───────── Test results ─────────

STUDENT = '''class Student {
    String name;
    int score;
}'''

STUDENT_MAIN = '''Student[] students = new Student[names.length];
for (int i = 0; i < names.length; i++) {
    Student student = new Student();
    student.name = names[i];
    student.score = scores[i];
    students[i] = student;
}
int passed = 0;
for (int i = 0; i < students.length; i++) {
    if (students[i].score >= 60) {
        System.out.println("Passed: " + students[i].name + " (" + students[i].score + ")");
        passed++;
    }
}
System.out.println("Passed " + passed + " of " + students.length);'''

STUDENT_ONE_OBJECT = '''Student[] students = new Student[names.length];
Student student = new Student();
for (int i = 0; i < names.length; i++) {
    student.name = names[i];
    student.score = scores[i];
    students[i] = student;
}
int passed = 0;
for (int i = 0; i < students.length; i++) {
    if (students[i].score >= 60) {
        System.out.println("Passed: " + students[i].name + " (" + students[i].score + ")");
        passed++;
    }
}
System.out.println("Passed " + passed + " of " + students.length);'''

# ───────── Two cash desks ─────────

DESK = '''class Desk {
    String name;
    int customers;
    int items;
}'''

DESK_MAIN = '''Desk first = new Desk();
first.name = "Desk 1";
Desk second = new Desk();
second.name = "Desk 2";
for (int i = 0; i < items.length; i++) {
    Desk target;
    if (first.items <= second.items) {
        target = first;
    } else {
        target = second;
    }
    target.customers++;
    target.items += items[i];
}
System.out.println(first.name + ": customers " + first.customers + ", items " + first.items);
System.out.println(second.name + ": customers " + second.customers + ", items " + second.items);
if (first.items > second.items) {
    System.out.println("Busier: " + first.name);
} else if (second.items > first.items) {
    System.out.println("Busier: " + second.name);
} else {
    System.out.println("Equal");
}'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-obj-rt-apple-baskets", title="Яблоки в корзинах",
        given=[("String", "color1"), ("int", "apples1"), ("String", "color2"), ("int", "apples2"), ("int", "move")],
        variants=[{"color1": '"Red"', "apples1": "20", "color2": '"Green"', "apples2": "6", "move": "7"},
                  {"color1": '"Blue"', "apples1": "15", "color2": '"White"', "apples2": "15", "move": "4"},
                  {"color1": '"Yellow"', "apples1": "32", "color2": '"Brown"', "apples2": "0", "move": "12"}],
        hidden=[{"color1": '"Black"', "apples1": "10", "color2": '"Pink"', "apples2": "3", "move": "0"},
                {"color1": '"Orange"', "apples1": "9", "color2": '"Gray"', "apples2": "21", "move": "9"},
                {"color1": '"Purple"', "apples1": "14", "color2": '"Golden"', "apples2": "8", "move": "3"}],
        intro="В саду собрали яблоки в две корзины. Цвет корзин и число яблок в них записаны в полях `color1`, `apples1`, "
              "`color2` и `apples2`. Первая корзина слишком тяжёлая, поэтому из неё переложили `move` яблок во вторую.",
        steps=["Ниже класса `Solution` создай класс `Basket` (без `public`) с полями `String color` и `int apples`.",
               "В `main` создай два отдельных объекта: `Basket first = new Basket();` и `Basket second = new Basket();`. "
               "Заполни первый из `color1` и `apples1`, второй — из `color2` и `apples2`.",
               "Переложи яблоки: уменьши `first.apples` на `move` и увеличь `second.apples` на `move`.",
               "Выведи две строки вида `Red basket: 13 apples` — сначала для первой корзины, потом для второй. "
               "Значения бери из полей объектов."],
        hint="Две корзины — два вызова `new`, у каждой свои поля. Если написать `Basket second = first;`, вторая переменная "
             "будет указывать на ту же самую корзину, и яблоки просто никуда не переложатся.",
        solution=BASKET_MAIN,
        classes=BASKET,
        wrong=[("вторая корзина — не новый объект, а тот же самый: `Basket second = first;`",
                BASKET_MAIN.replace("Basket second = new Basket();", "Basket second = first;")),
               ("поля класса объявлены static — обе корзины делят один цвет и одно число яблок",
                BASKET_MAIN, BASKET.replace("    String color;", "    static String color;").replace("    int apples;", "    static int apples;"))],
        constructs=["class"],
        checks=find_class("Basket")
               + need_field("Basket", "color", "String", "цвет корзины")
               + need_field("Basket", "apples", "int", "сколько в корзине яблок"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-obj-rt-test-results", title="Итоги контрольной",
        given=[("String[]", "names"), ("int[]", "scores")],
        variants=[{"names": '{"Anya", "Boris", "Vika", "Gosha"}', "scores": "{82, 45, 60, 71}"},
                  {"names": '{"Dima", "Eva", "Fedya"}', "scores": "{59, 90, 33}"},
                  {"names": '{"Ilya", "Kira", "Lena", "Mark", "Nadya"}', "scores": "{100, 61, 58, 75, 60}"}],
        hidden=[{"names": '{"Oleg"}', "scores": "{60}"},
                {"names": '{"Polina", "Rustam"}', "scores": "{59, 12}"},
                {"names": '{"Semyon", "Tonya", "Ulyana"}', "scores": "{88, 95, 64}"},
                {"names": '{"Varya", "Yura", "Zakhar", "Alisa"}', "scores": "{61, 59, 60, 0}"}],
        intro="Учитель проверил контрольную. Имена учеников записаны в массиве `names`, а их баллы — в массиве `scores` "
              "под теми же номерами. Зачёт ставится, если набрано 60 баллов или больше. Каждый ученик — отдельный объект.",
        steps=["Ниже класса `Solution` создай класс `Student` (без `public`) с полями `String name` и `int score`.",
               "В `main` создай массив `Student[] students = new Student[names.length];`. В цикле для каждого ученика "
               "создай новый объект `new Student()`, заполни его поля и положи в массив.",
               "Вторым циклом пройди по массиву `students` и для каждого, у кого `score` не меньше 60, выведи строку вида "
               "`Passed: Anya (82)`. Порядок — как в массиве.",
               "Последней строкой выведи строку вида `Passed 3 of 4`: сколько учеников получили зачёт и сколько всего "
               "объектов в массиве `students`."],
        hint="Создавай объект внутри цикла: каждое `new Student()` — новый ученик. Если сделать один объект до цикла, все "
             "ячейки массива будут указывать на него, и в нём останется только последний ученик. Ровно 60 баллов — это уже зачёт.",
        solution=STUDENT_MAIN,
        classes=STUDENT,
        wrong=[("создаёт один объект до цикла — все ячейки массива указывают на последнего ученика", STUDENT_ONE_OBJECT),
               ("строгое сравнение: ученик с ровно 60 баллами не получает зачёт",
                STUDENT_MAIN.replace("students[i].score >= 60", "students[i].score > 60"))],
        constructs=["class", "for", "if"],
        checks=find_class("Student")
               + need_field("Student", "name", "String", "имя ученика")
               + need_field("Student", "score", "int", "баллы за контрольную"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-obj-rt-cash-desks", title="Две кассы",
        given=[("int[]", "items")],
        variants=[{"items": "{5, 3, 8, 2, 4}"},
                  {"items": "{10, 1, 1, 1, 6}"},
                  {"items": "{7, 7, 3, 9}"}],
        hidden=[{"items": "{4}"},
                {"items": "{}"},
                {"items": "{2, 2, 2, 2}"},
                {"items": "{12, 3, 4, 2, 6, 1, 5}"}],
        intro="В магазине работают две кассы. Покупатели подходят по очереди; сколько товаров у каждого, записано по "
              "порядку в массиве `items`. Каждый покупатель идёт на ту кассу, где сейчас меньше товаров, — а если товаров "
              "поровну, на первую.",
        steps=["Ниже класса `Solution` создай класс `Desk` (без `public`) с полями `String name`, `int customers` и `int items`.",
               "В `main` создай два объекта-кассы: `first` с именем `\"Desk 1\"` и `second` с именем `\"Desk 2\"`.",
               "Пройди по массиву `items`. Для каждого покупателя заведи переменную `Desk target`: если у `first` товаров "
               "меньше или столько же, сколько у `second`, присвой `target = first`, иначе `target = second`. Затем прибавь "
               "к `target.customers` единицу, а к `target.items` — товары покупателя.",
               "Выведи две строки вида `Desk 1: customers 3, items 11` — для первой кассы, потом для второй. Третьей строкой "
               "выведи `Busier: Desk 1` с именем кассы, где товаров больше, а если поровну — `Equal`."],
        hint="`target` — не третья касса, а ссылка на одну из двух. Поэтому `target.items += ...` меняет поля именно той "
             "кассы, на которую `target` сейчас указывает. Первый покупатель идёт на первую кассу: у обеих пока 0 товаров.",
        solution=DESK_MAIN,
        classes=DESK,
        wrong=[("при равном числе товаров отправляет покупателя на вторую кассу",
                DESK_MAIN.replace("first.items <= second.items", "first.items < second.items")),
               ("выбирает кассу по числу покупателей, а не по числу товаров",
                DESK_MAIN.replace("first.items <= second.items", "first.customers <= second.customers"))],
        constructs=["class", "for", "if"],
        checks=find_class("Desk")
               + need_field("Desk", "name", "String", "название кассы")
               + need_field("Desk", "customers", "int", "сколько покупателей обслужила касса")
               + need_field("Desk", "items", "int", "сколько товаров пробила касса"),
    ),
]
