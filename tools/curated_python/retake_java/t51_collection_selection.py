"""COLLECTION_SELECTION — «Выбор коллекции» (Java). Taught before: List and its operations, Set (HashSet, TreeSet,
LinkedHashSet), Map (HashMap, TreeMap, LinkedHashMap). Here: the statement says what the data must do (no repeats but
keep the order → LinkedHashSet; find a value by a key → Map; keep order and repeats → List; unique and sorted → TreeSet;
pairs sorted by key → TreeMap), and the student picks the collection. The output is built so that a wrong collection
prints something else; a list with repeats removed by hand (or a lookup with indexOf) prints the same, so `checks` also
looks for the chosen collection in the compiled class, like the switch check: it reads Solution.class through
getResourceAsStream and collects the names in its constant pool — every class the code creates or calls a method of is
there (java/util/LinkedHashSet …). If the class bytes cannot be read, the check passes rather than reject a correct
solution."""
from java_tasks import JavaOutputTask

SKILL = "COLLECTION_SELECTION"


def uses_collections(*requirements: tuple[tuple[str, ...], str]) -> str:
    """Checks that need, for each (names, message), at least one of the names in Solution's constant pool."""
    reads = """Set<String> pool = new HashSet<>();
boolean readable = false;
try (InputStream in = Solution.class.getResourceAsStream("Solution.class")) {
    if (in != null) {
        DataInputStream d = new DataInputStream(new ByteArrayInputStream(in.readAllBytes()));
        d.skipBytes(8);
        int poolSize = d.readUnsignedShort();
        for (int i = 1; i < poolSize; i++) {
            int tag = d.readUnsignedByte();
            if (tag == 1) pool.add(d.readUTF());
            else if (tag == 5 || tag == 6) { d.skipBytes(8); i++; }
            else if (tag == 7 || tag == 8 || tag == 16 || tag == 19 || tag == 20) d.skipBytes(2);
            else if (tag == 15) d.skipBytes(3);
            else d.skipBytes(4);
        }
        readable = true;
    }
} catch (IOException e) { readable = false; }
final boolean known = readable;
java.util.function.Predicate<String> uses = name -> !known || pool.stream().anyMatch(entry -> entry.contains(name));
"""
    needs = "".join("need(" + " || ".join(f'uses.test("{name}")' for name in names) + f', "{message}");\n'
                    for names, message in requirements)
    return reads + needs

KITCHEN = ('System.out.println("Dishes ordered: " + dishes.length);\nList<String> ticket = new ArrayList<>();\n'
           'for (String dish : dishes) {\n    ticket.add(dish);\n}\nticket.add(extra);\nSystem.out.println(ticket);\n'
           'System.out.println("Portions: " + ticket.size());')

SHOP = ('Map<String, Integer> priceList = new TreeMap<>();\nfor (int i = 0; i < products.size(); i++) {\n'
        '    priceList.put(products.get(i), prices.get(i));\n}\nSystem.out.println("Price list: " + priceList);\nint total = 0;\n'
        'for (String item : cart) {\n    if (priceList.containsKey(item)) {\n        total += priceList.get(item);\n    } else {\n'
        '        System.out.println("No price: " + item);\n    }\n}\nSystem.out.println("Total: " + total + " rub");')

ELECTIVES = ('Set<String> all = new TreeSet<>(courses);\nSystem.out.println("Courses: " + all);\n'
             'Map<String, Set<String>> groups = new TreeMap<>();\nfor (int i = 0; i < courses.size(); i++) {\n'
             '    String course = courses.get(i);\n    if (!groups.containsKey(course)) {\n'
             '        groups.put(course, new LinkedHashSet<>());\n    }\n    groups.get(course).add(students.get(i));\n}\n'
             'System.out.println("Groups: " + groups);\nString busiest = "";\nint most = 0;\n'
             'for (String course : groups.keySet()) {\n    if (groups.get(course).size() > most) {\n'
             '        most = groups.get(course).size();\n        busiest = course;\n    }\n}\n'
             'System.out.println("Busiest: " + busiest + ", " + most + " students");')

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-select-rt-kitchen-ticket", title="Заказ на кухню",
        given=[("String[]", "dishes"), ("String", "extra")],
        variants=[{"dishes": '{"tea", "soup", "tea", "pie"}', "extra": '"tea"'},
                  {"dishes": '{"pizza", "salad", "pizza"}', "extra": '"juice"'},
                  {"dishes": '{"coffee", "cake", "coffee", "cake", "coffee"}', "extra": '"water"'}],
        hidden=[{"dishes": '{"soup"}', "extra": '"bread"'},
                {"dishes": '{"tea", "tea", "tea"}', "extra": '"tea"'},
                {"dishes": '{"omelet", "toast", "cocoa", "pancakes"}', "extra": '"jam"'},
                {"dishes": "{}", "extra": '"cola"'}],
        intro="Официант принял заказ: блюда записаны в массив `dishes` в том порядке, в котором гости их называли. "
              "Если два гостя заказали чай, на кухне должны приготовить две чашки. Потом гости попросили ещё одно "
              "блюдо — `extra`. Повар готовит строго по порядку, поэтому важны и порядок, и повторы.",
        steps=["Выведи строку вида `Dishes ordered: 4` — сколько блюд в массиве `dishes`.",
               "Выбери коллекцию, которая хранит элементы в порядке добавления и не теряет повторы. Сложи в неё все "
               "блюда из `dishes` по порядку, а последним добавь `extra`.",
               "Выведи эту коллекцию через `System.out.println` — получится строка вида `[tea, soup, tea, pie, tea]`.",
               "Последней строкой выведи строку вида `Portions: 5` — сколько элементов в этой коллекции."],
        hint="Множества здесь не подходят: они убирают повторы, и вторая чашка чая пропадёт. А `TreeSet` к тому же "
             "переставит блюда по алфавиту.",
        solution=KITCHEN,
        wrong=[("выбрал LinkedHashSet — повторные блюда пропали",
                KITCHEN.replace("List<String> ticket = new ArrayList<>();", "Set<String> ticket = new LinkedHashSet<>();")),
               ("выбрал TreeSet — блюда идут по алфавиту и без повторов",
                KITCHEN.replace("List<String> ticket = new ArrayList<>();", "Set<String> ticket = new TreeSet<>();"))],
        constructs=["for"],
        checks=uses_collections((("java/util/List", "java/util/ArrayList", "java/util/LinkedList"),
                                 "Сложи блюда в коллекцию, которая хранит порядок и повторы, — в список: так ей "
                                 "можно добавить блюдо в конец и узнать размер")),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-select-rt-price-list", title="Прайс-лист и корзина",
        given=[("List<String>", "products"), ("List<Integer>", "prices"), ("List<String>", "cart")],
        variants=[{"products": 'new ArrayList<>(List.of("milk", "bread", "apple"))',
                   "prices": "new ArrayList<>(List.of(90, 45, 20))",
                   "cart": 'new ArrayList<>(List.of("apple", "milk", "apple", "candy"))'},
                  {"products": 'new ArrayList<>(List.of("pen", "notebook", "glue", "eraser"))',
                   "prices": "new ArrayList<>(List.of(30, 70, 55, 15))",
                   "cart": 'new ArrayList<>(List.of("notebook", "notebook", "ruler", "pen"))'},
                  {"products": 'new ArrayList<>(List.of("tea", "sugar", "lemon"))',
                   "prices": "new ArrayList<>(List.of(150, 80, 25))",
                   "cart": 'new ArrayList<>(List.of("lemon", "lemon", "lemon", "tea", "honey", "jam"))'}],
        hidden=[{"products": 'new ArrayList<>(List.of("soap"))', "prices": "new ArrayList<>(List.of(60))",
                 "cart": "new ArrayList<>()"},
                {"products": 'new ArrayList<>(List.of("rice", "corn", "beans"))', "prices": "new ArrayList<>(List.of(100, 70, 90))",
                 "cart": 'new ArrayList<>(List.of("beans", "rice", "beans"))'},
                {"products": 'new ArrayList<>(List.of("kiwi", "fig"))', "prices": "new ArrayList<>(List.of(35, 40))",
                 "cart": 'new ArrayList<>(List.of("plum", "plum"))'},
                {"products": 'new ArrayList<>(List.of("cola", "chips", "nuts", "water"))', "prices": "new ArrayList<>(List.of(95, 120, 200, 40))",
                 "cart": 'new ArrayList<>(List.of("water", "nuts", "cola", "chips", "water"))'}],
        intro="В магазине есть прайс-лист: товары записаны в список `products`, а их цены — в список `prices` (цена "
              "товара `products.get(i)` — это `prices.get(i)`). Покупатель принёс на кассу корзину `cart`, и одинаковых "
              "товаров в ней может быть несколько. Иногда в корзине попадается товар без цены.",
        steps=["Выбери коллекцию пар «товар — цена», в которой цену можно сразу найти по названию и в которой товары "
               "сами хранятся по алфавиту. Заполни её из `products` и `prices`.",
               "Выведи `Price list: ` и сразу за этим эту коллекцию, например `Price list: {{apple=20, bread=45}}`.",
               "Пройди по `cart` по порядку. Цену каждого товара, который есть в прайс-листе, прибавь к сумме, а для "
               "товара без цены выведи строку вида `No price: candy`.",
               "Последней строкой выведи строку вида `Total: 130 rub` — сумму за все товары с ценой."],
        hint="Нужен словарь, где ключ — название товара. Из трёх видов словаря по алфавиту ключи хранит только один. "
             "Одинаковые товары в корзине оплачиваются каждый, поэтому корзину не превращай в множество.",
        solution=SHOP,
        wrong=[("выбрал LinkedHashMap — прайс-лист идёт в исходном порядке, а не по алфавиту",
                SHOP.replace("new TreeMap<>()", "new LinkedHashMap<>()")),
               ("сложил корзину в множество — одинаковые товары оплачены только один раз",
                SHOP.replace("for (String item : cart) {", "for (String item : new TreeSet<>(cart)) {"))],
        constructs=["for", "if"],
        checks=uses_collections((("java/util/TreeMap",),
                                 "Сложи цены в словарь, который сам хранит ключи по алфавиту: в нём цена находится "
                                 "по названию сразу, без перебора списков")),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-select-rt-electives", title="Запись на кружки",
        given=[("List<String>", "students"), ("List<String>", "courses")],
        variants=[{"students": 'new ArrayList<>(List.of("Anya", "Boris", "Anya", "Vika", "Boris", "Anya"))',
                   "courses": 'new ArrayList<>(List.of("chess", "robots", "art", "chess", "chess", "chess"))'},
                  {"students": 'new ArrayList<>(List.of("Gleb", "Dasha", "Egor", "Dasha", "Gleb"))',
                   "courses": 'new ArrayList<>(List.of("music", "dance", "dance", "music", "music"))'},
                  {"students": 'new ArrayList<>(List.of("Ira", "Kira", "Lev", "Mila", "Ira", "Lev", "Kira"))',
                   "courses": 'new ArrayList<>(List.of("theatre", "art", "theatre", "art", "art", "chess", "theatre"))'}],
        hidden=[{"students": 'new ArrayList<>(List.of("Nina"))', "courses": 'new ArrayList<>(List.of("yoga"))'},
                {"students": 'new ArrayList<>(List.of("Oleg", "Oleg", "Oleg"))', "courses": 'new ArrayList<>(List.of("judo", "judo", "judo"))'},
                {"students": 'new ArrayList<>(List.of("Rita", "Pavel", "Sasha", "Rita"))',
                 "courses": 'new ArrayList<>(List.of("swim", "chess", "swim", "chess"))'},
                {"students": 'new ArrayList<>(List.of("Tanya", "Uma", "Fedya", "Yura", "Zoya"))',
                 "courses": 'new ArrayList<>(List.of("math", "art", "math", "art", "drums"))'}],
        intro="Ученики записываются на кружки через школьный сайт. Каждая запись — это ученик `students.get(i)` "
              "и кружок `courses.get(i)`. Ученик может записаться на несколько кружков, а иногда по ошибке "
              "записывается на один кружок дважды. Для трёх отчётов подбери подходящие коллекции.",
        steps=["Выведи `Courses: ` и коллекцию кружков, которая сама убирает повторы и хранит их по алфавиту, например "
               "`Courses: [art, chess, robots]`.",
               "Собери словарь, который сам хранит ключи по алфавиту: ключ — кружок, значение — множество его учеников "
               "без повторов в том порядке, в котором они записывались. Выведи `Groups: ` и этот словарь, например "
               "`Groups: {{art=[Anya], chess=[Anya, Vika, Boris]}}`.",
               "Пройди по ключам словаря и найди кружок, в котором больше всего учеников. Если таких несколько, "
               "выбери первый по алфавиту. Выведи строку вида `Busiest: chess, 3 students`."],
        hint="Значение словаря — само множество: если кружка ещё нет в словаре, положи под него новое пустое "
             "множество, а потом добавь в него ученика. Подумай, какое множество помнит порядок добавления.",
        solution=ELECTIVES,
        wrong=[("взял для учеников кружка список — записавшийся дважды ученик повторяется",
                ELECTIVES.replace("Map<String, Set<String>> groups", "Map<String, List<String>> groups")
                         .replace("new LinkedHashSet<>()", "new ArrayList<>()")),
               ("взял для учеников кружка TreeSet — ученики идут по алфавиту, а не в порядке записи",
                ELECTIVES.replace("new LinkedHashSet<>()", "new TreeSet<>()")),
               ("выбрал LinkedHashMap для словаря — кружки идут в порядке записи, а не по алфавиту",
                ELECTIVES.replace("Map<String, Set<String>> groups = new TreeMap<>();",
                                  "Map<String, Set<String>> groups = new LinkedHashMap<>();"))],
        constructs=["for", "if"],
        checks=uses_collections((("java/util/TreeSet",),
                                 "Для списка кружков выбери множество, которое само убирает повторы и хранит элементы по алфавиту"),
                                (("java/util/TreeMap",),
                                 "Для групп выбери словарь, который сам хранит ключи по алфавиту"),
                                (("java/util/LinkedHashSet",),
                                 "Для учеников кружка выбери множество, которое убирает повторы и помнит порядок "
                                 "добавления, — тогда ничего не придётся проверять вручную")),
    ),
]
