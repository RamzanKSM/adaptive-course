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

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-select-trip-cities", title="Города путешественника",
        given=[("List<String>", "trips")],
        variants=[{"trips": 'new ArrayList<>(List.of("Kazan", "Sochi", "Kazan", "Vladimir", "Sochi", "Perm", "Kazan"))'},
                  {"trips": 'new ArrayList<>(List.of("Tver", "Omsk", "Tver", "Tver", "Kaluga"))'},
                  {"trips": 'new ArrayList<>(List.of("Murmansk", "Samara", "Astrakhan", "Samara", "Murmansk", "Yaroslavl"))'}],
        hidden=[{"trips": 'new ArrayList<>(List.of("Pskov"))'},
                {"trips": 'new ArrayList<>(List.of("Ufa", "Ufa", "Ufa"))'},
                {"trips": 'new ArrayList<>(List.of("Ryazan", "Bryansk", "Lipetsk", "Bryansk"))'},
                {"trips": 'new ArrayList<>(List.of("Abakan", "Biysk", "Chita"))'}],
        intro="Путешественник ведёт дневник: после каждой поездки он записывает город в список `trips`. В некоторых "
              "городах он побывал несколько раз. Для блога ему нужен список городов без повторов — в том порядке, "
              "в котором он побывал в них впервые.",
        steps=["Выведи строку вида `Trips: 8` — сколько всего записей в `trips`.",
               "Выбери коллекцию, которая сама не хранит повторов и при этом помнит порядок, в котором в неё добавляли "
               "элементы. Сложи в неё все города из `trips`.",
               "Выведи эту коллекцию через `System.out.println` — получится строка вида `[Tula, Oryol, Kursk]`.",
               "Последней строкой выведи строку вида `Different cities: 3` — сколько городов в этой коллекции."],
        hint="Повторы убирает множество. Но `HashSet` хранит элементы в непредсказуемом порядке, а `TreeSet` сортирует "
             "их по алфавиту — тебе нужен третий вид множества.",
        solution='System.out.println("Trips: " + trips.size());\nSet<String> cities = new LinkedHashSet<>(trips);\n'
                 'System.out.println(cities);\nSystem.out.println("Different cities: " + cities.size());',
        wrong=[("выбрал TreeSet — города идут по алфавиту, а не в порядке первой поездки",
                'System.out.println("Trips: " + trips.size());\nSet<String> cities = new TreeSet<>(trips);\n'
                'System.out.println(cities);\nSystem.out.println("Different cities: " + cities.size());'),
               ("оставил города в списке — повторы никуда не делись",
                'System.out.println("Trips: " + trips.size());\nList<String> cities = new ArrayList<>(trips);\n'
                'System.out.println(cities);\nSystem.out.println("Different cities: " + cities.size());'),
               ("убирает повторы вручную в списке через contains — вывод тот же, но коллекция не выбрана",
                'System.out.println("Trips: " + trips.size());\nList<String> cities = new ArrayList<>();\n'
                "for (String city : trips) {\n    if (!cities.contains(city)) {\n        cities.add(city);\n    }\n}\n"
                'System.out.println(cities);\nSystem.out.println("Different cities: " + cities.size());')],
        checks=uses_collections((("java/util/LinkedHashSet",),
                                 "Сложи города в коллекцию, которая сама не хранит повторов и помнит порядок добавления, — "
                                 "тогда убирать повторы вручную не придётся")),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-select-cloakroom", title="Гардероб в театре",
        given=[("List<Integer>", "tags"), ("List<String>", "coats"), ("List<Integer>", "returned")],
        variants=[{"tags": "new ArrayList<>(List.of(12, 5, 31, 8))",
                   "coats": 'new ArrayList<>(List.of("blue jacket", "gray coat", "red scarf", "black raincoat"))',
                   "returned": "new ArrayList<>(List.of(31, 12, 8))"},
                  {"tags": "new ArrayList<>(List.of(101, 102, 103))",
                   "coats": 'new ArrayList<>(List.of("fur coat", "windbreaker", "down jacket"))',
                   "returned": "new ArrayList<>(List.of(103, 101))"},
                  {"tags": "new ArrayList<>(List.of(7, 44, 19, 2, 60))",
                   "coats": 'new ArrayList<>(List.of("green raincoat", "yellow jacket", "white fur coat", "leather jacket", "beige coat"))',
                   "returned": "new ArrayList<>(List.of(2, 77, 44))"}],
        hidden=[{"tags": "new ArrayList<>(List.of(1))", "coats": 'new ArrayList<>(List.of("umbrella"))',
                 "returned": "new ArrayList<>(List.of(1))"},
                {"tags": "new ArrayList<>(List.of(10, 20))", "coats": 'new ArrayList<>(List.of("hat", "jacket"))',
                 "returned": "new ArrayList<>(List.of(30, 20, 10))"},
                {"tags": "new ArrayList<>(List.of(15, 16, 17))", "coats": 'new ArrayList<>(List.of("coat", "raincoat", "fur coat"))',
                 "returned": "new ArrayList<>(List.of(17, 15, 16))"},
                {"tags": "new ArrayList<>(List.of(3, 9, 4, 8))", "coats": 'new ArrayList<>(List.of("cap", "blazer", "sweater", "jacket"))',
                 "returned": "new ArrayList<>(List.of(5))"}],
        intro="В гардеробе театра каждому зрителю дают номерок. Номерки записаны в список `tags`, а вещи — в список "
              "`coats`: вещь `coats.get(i)` висит под номерком `tags.get(i)`. После спектакля зрители по очереди "
              "отдают номерки — они записаны в список `returned`.",
        steps=["Выбери коллекцию, в которой по номерку можно сразу найти вещь, не перебирая списки каждый раз, "
               "и заполни её из `tags` и `coats`.",
               "Для каждого номерка из `returned` по порядку выведи строку вида `Tag 50: green umbrella`.",
               "Если такого номерка в гардеробе нет, выведи строку вида `Tag 50: not found`."],
        hint="Нужна коллекция пар «ключ — значение»: ключ — номерок, значение — вещь. Заполнить её удобно циклом "
             "по номерам `i`, ведь `tags.get(i)` и `coats.get(i)` — одна пара.",
        solution="Map<Integer, String> cloakroom = new HashMap<>();\nfor (int i = 0; i < tags.size(); i++) {\n"
                 "    cloakroom.put(tags.get(i), coats.get(i));\n}\nfor (int tag : returned) {\n"
                 "    if (cloakroom.containsKey(tag)) {\n"
                 '        System.out.println("Tag " + tag + ": " + cloakroom.get(tag));\n    } else {\n'
                 '        System.out.println("Tag " + tag + ": not found");\n    }\n}',
        wrong=[("берёт вещи по порядку сдачи номерков, а не по самому номерку",
                "for (int i = 0; i < returned.size(); i++) {\n"
                '    System.out.println("Tag " + returned.get(i) + ": " + coats.get(i));\n}'),
               ("не проверяет, есть ли номерок в словаре, — для чужого номерка печатает null",
                "Map<Integer, String> cloakroom = new HashMap<>();\nfor (int i = 0; i < tags.size(); i++) {\n"
                "    cloakroom.put(tags.get(i), coats.get(i));\n}\nfor (int tag : returned) {\n"
                '    System.out.println("Tag " + tag + ": " + cloakroom.get(tag));\n}'),
               ("ищет номерок в списке через indexOf — вывод тот же, но без коллекции «ключ — значение»",
                "for (int tag : returned) {\n    int i = tags.indexOf(tag);\n    if (i >= 0) {\n"
                '        System.out.println("Tag " + tag + ": " + coats.get(i));\n    } else {\n'
                '        System.out.println("Tag " + tag + ": not found");\n    }\n}')],
        constructs=["for"],
        checks=uses_collections((("java/util/Map", "java/util/HashMap", "java/util/TreeMap", "java/util/LinkedHashMap"),
                                 "Сложи вещи в коллекцию пар «ключ — значение», где ключ — номерок: тогда вещь находится "
                                 "сразу, без перебора списков")),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-select-library-log", title="Журнал библиотеки",
        given=[("List<String>", "visits")],
        variants=[{"visits": 'new ArrayList<>(List.of("Petya", "Olya", "Vasya", "Olya", "Petya", "Olya"))'},
                  {"visits": 'new ArrayList<>(List.of("Seva", "Alina", "Seva", "Denis", "Seva"))'},
                  {"visits": 'new ArrayList<>(List.of("Yulya", "Timofey", "Kira", "Yulya", "Kira", "Vanya", "Yulya"))'}],
        hidden=[{"visits": 'new ArrayList<>(List.of("Roma"))'},
                {"visits": 'new ArrayList<>(List.of("Gena", "Arina"))'},
                {"visits": 'new ArrayList<>(List.of("Lena", "Lena", "Lena", "Lena"))'},
                {"visits": 'new ArrayList<>(List.of("Zoya", "Boris", "Emil", "Boris", "Nelli"))'}],
        intro="В школьной библиотеке записывают каждого, кто пришёл: имена в списке `visits` идут в порядке посещений, "
              "и один читатель может прийти много раз. Библиотекарю нужны три разных отчёта — для каждого подбери "
              "подходящую коллекцию.",
        steps=["Выведи `Last: ` и сразу за этим три последних посещения в том же порядке, например "
               "`Last: [Liza, Gosha, Liza]`. Если посещений меньше трёх, выведи все.",
               "Выведи `Readers: ` и коллекцию, которая сама убирает повторы и хранит читателей по алфавиту, например "
               "`Readers: [Gosha, Liza, Misha]`.",
               "Выведи `Visits: ` и словарь, который сам хранит ключи по алфавиту: для каждого читателя — сколько раз "
               "он приходил, например `Visits: {{Gosha=1, Liza=2, Misha=1}}`."],
        hint="Квадратные скобки при выводе дают списки и множества, а фигурные скобки со знаком `=` — словари. "
             "Подумай, какая коллекция сама убирает повторы и сортирует, а какая хранит пары и сортирует их по ключу.",
        solution="int from = Math.max(0, visits.size() - 3);\nList<String> last = visits.subList(from, visits.size());\n"
                 'System.out.println("Last: " + last);\nSet<String> readers = new TreeSet<>(visits);\n'
                 'System.out.println("Readers: " + readers);\nMap<String, Integer> counts = new TreeMap<>();\n'
                 "for (String name : visits) {\n    counts.put(name, counts.getOrDefault(name, 0) + 1);\n}\n"
                 'System.out.println("Visits: " + counts);',
        wrong=[("берёт три первых посещения вместо трёх последних",
                "List<String> last = visits.subList(0, Math.min(3, visits.size()));\n"
                'System.out.println("Last: " + last);\nSet<String> readers = new TreeSet<>(visits);\n'
                'System.out.println("Readers: " + readers);\nMap<String, Integer> counts = new TreeMap<>();\n'
                "for (String name : visits) {\n    counts.put(name, counts.getOrDefault(name, 0) + 1);\n}\n"
                'System.out.println("Visits: " + counts);'),
               ("выбрал LinkedHashSet и LinkedHashMap — читатели идут в порядке первого прихода, а не по алфавиту",
                "int from = Math.max(0, visits.size() - 3);\nList<String> last = visits.subList(from, visits.size());\n"
                'System.out.println("Last: " + last);\nSet<String> readers = new LinkedHashSet<>(visits);\n'
                'System.out.println("Readers: " + readers);\nMap<String, Integer> counts = new LinkedHashMap<>();\n'
                "for (String name : visits) {\n    counts.put(name, counts.getOrDefault(name, 0) + 1);\n}\n"
                'System.out.println("Visits: " + counts);'),
               ("сортирует список без повторов вручную — вывод тот же, но коллекция не выбрана",
                "int from = Math.max(0, visits.size() - 3);\nList<String> last = visits.subList(from, visits.size());\n"
                'System.out.println("Last: " + last);\nList<String> readers = new ArrayList<>(new HashSet<>(visits));\n'
                'Collections.sort(readers);\nSystem.out.println("Readers: " + readers);\n'
                "Map<String, Integer> counts = new TreeMap<>();\n"
                "for (String name : visits) {\n    counts.put(name, counts.getOrDefault(name, 0) + 1);\n}\n"
                'System.out.println("Visits: " + counts);')],
        constructs=["for"],
        checks=uses_collections((("java/util/TreeSet", "keySet"),
                                 "Для читателей выбери коллекцию, которая сама убирает повторы и хранит элементы по алфавиту"),
                                (("java/util/TreeMap",),
                                 "Для посещений выбери словарь, который сам хранит ключи по алфавиту, — тогда ничего не "
                                 "придётся сортировать вручную")),
    ),
]
