"""COLLECTION_SELECTION — «Выбор коллекции» (Java). Taught before: List and its operations, Set (HashSet, TreeSet,
LinkedHashSet), Map (HashMap, TreeMap, LinkedHashMap). Here: the statement says what the data must do (no repeats but
keep the order → LinkedHashSet; find a value by a key → Map; keep order and repeats → List; unique and sorted → TreeSet;
pairs sorted by key → TreeMap), and the student picks the collection. The syntax tree cannot tell which one was
picked, so the output is built so that the wrong choice prints something else."""
from java_tasks import JavaOutputTask

SKILL = "COLLECTION_SELECTION"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-select-trip-cities", title="Города путешественника",
        given=[("List<String>", "trips")],
        variants=[{"trips": 'new ArrayList<>(List.of("Казань", "Сочи", "Казань", "Владимир", "Сочи", "Пермь", "Казань"))'},
                  {"trips": 'new ArrayList<>(List.of("Тверь", "Омск", "Тверь", "Тверь", "Калуга"))'},
                  {"trips": 'new ArrayList<>(List.of("Мурманск", "Самара", "Астрахань", "Самара", "Мурманск", "Ярославль"))'}],
        hidden=[{"trips": 'new ArrayList<>(List.of("Псков"))'},
                {"trips": 'new ArrayList<>(List.of("Уфа", "Уфа", "Уфа"))'},
                {"trips": 'new ArrayList<>(List.of("Рязань", "Брянск", "Липецк", "Брянск"))'},
                {"trips": 'new ArrayList<>(List.of("Абакан", "Бийск", "Чита"))'}],
        intro="Путешественник ведёт дневник: после каждой поездки он записывает город в список `trips`. В некоторых "
              "городах он побывал несколько раз. Для блога ему нужен список городов без повторов — в том порядке, "
              "в котором он побывал в них впервые.",
        steps=["Выведи строку вида `Поездок: 8` — сколько всего записей в `trips`.",
               "Выбери коллекцию, которая сама не хранит повторов и при этом помнит порядок, в котором в неё добавляли "
               "элементы. Сложи в неё все города из `trips`.",
               "Выведи эту коллекцию через `System.out.println` — получится строка вида `[Тула, Орёл, Курск]`.",
               "Последней строкой выведи строку вида `Разных городов: 3` — сколько городов в этой коллекции."],
        hint="Повторы убирает множество. Но `HashSet` хранит элементы в непредсказуемом порядке, а `TreeSet` сортирует "
             "их по алфавиту — тебе нужен третий вид множества.",
        solution='System.out.println("Поездок: " + trips.size());\nSet<String> cities = new LinkedHashSet<>(trips);\n'
                 'System.out.println(cities);\nSystem.out.println("Разных городов: " + cities.size());',
        wrong=[("выбрал TreeSet — города идут по алфавиту, а не в порядке первой поездки",
                'System.out.println("Поездок: " + trips.size());\nSet<String> cities = new TreeSet<>(trips);\n'
                'System.out.println(cities);\nSystem.out.println("Разных городов: " + cities.size());'),
               ("оставил города в списке — повторы никуда не делись",
                'System.out.println("Поездок: " + trips.size());\nList<String> cities = new ArrayList<>(trips);\n'
                'System.out.println(cities);\nSystem.out.println("Разных городов: " + cities.size());')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-select-cloakroom", title="Гардероб в театре",
        given=[("List<Integer>", "tags"), ("List<String>", "coats"), ("List<Integer>", "returned")],
        variants=[{"tags": "new ArrayList<>(List.of(12, 5, 31, 8))",
                   "coats": 'new ArrayList<>(List.of("синяя куртка", "серое пальто", "красный шарф", "чёрный плащ"))',
                   "returned": "new ArrayList<>(List.of(31, 12, 8))"},
                  {"tags": "new ArrayList<>(List.of(101, 102, 103))",
                   "coats": 'new ArrayList<>(List.of("шуба", "ветровка", "пуховик"))',
                   "returned": "new ArrayList<>(List.of(103, 101))"},
                  {"tags": "new ArrayList<>(List.of(7, 44, 19, 2, 60))",
                   "coats": 'new ArrayList<>(List.of("зелёный плащ", "жёлтая куртка", "белая шуба", "кожаная куртка", "бежевое пальто"))',
                   "returned": "new ArrayList<>(List.of(2, 77, 44))"}],
        hidden=[{"tags": "new ArrayList<>(List.of(1))", "coats": 'new ArrayList<>(List.of("зонт"))',
                 "returned": "new ArrayList<>(List.of(1))"},
                {"tags": "new ArrayList<>(List.of(10, 20))", "coats": 'new ArrayList<>(List.of("шляпа", "куртка"))',
                 "returned": "new ArrayList<>(List.of(30, 20, 10))"},
                {"tags": "new ArrayList<>(List.of(15, 16, 17))", "coats": 'new ArrayList<>(List.of("пальто", "плащ", "шуба"))',
                 "returned": "new ArrayList<>(List.of(17, 15, 16))"},
                {"tags": "new ArrayList<>(List.of(3, 9, 4, 8))", "coats": 'new ArrayList<>(List.of("кепка", "пиджак", "свитер", "куртка"))',
                 "returned": "new ArrayList<>(List.of(5))"}],
        intro="В гардеробе театра каждому зрителю дают номерок. Номерки записаны в список `tags`, а вещи — в список "
              "`coats`: вещь `coats.get(i)` висит под номерком `tags.get(i)`. После спектакля зрители по очереди "
              "отдают номерки — они записаны в список `returned`.",
        steps=["Выбери коллекцию, в которой по номерку можно сразу найти вещь, не перебирая списки каждый раз, "
               "и заполни её из `tags` и `coats`.",
               "Для каждого номерка из `returned` по порядку выведи строку вида `Номерок 50: зелёный зонт`.",
               "Если такого номерка в гардеробе нет, выведи строку вида `Номерок 50: не найден`."],
        hint="Нужна коллекция пар «ключ — значение»: ключ — номерок, значение — вещь. Заполнить её удобно циклом "
             "по номерам `i`, ведь `tags.get(i)` и `coats.get(i)` — одна пара.",
        solution="Map<Integer, String> cloakroom = new HashMap<>();\nfor (int i = 0; i < tags.size(); i++) {\n"
                 "    cloakroom.put(tags.get(i), coats.get(i));\n}\nfor (int tag : returned) {\n"
                 "    if (cloakroom.containsKey(tag)) {\n"
                 '        System.out.println("Номерок " + tag + ": " + cloakroom.get(tag));\n    } else {\n'
                 '        System.out.println("Номерок " + tag + ": не найден");\n    }\n}',
        wrong=[("берёт вещи по порядку сдачи номерков, а не по самому номерку",
                "for (int i = 0; i < returned.size(); i++) {\n"
                '    System.out.println("Номерок " + returned.get(i) + ": " + coats.get(i));\n}'),
               ("не проверяет, есть ли номерок в словаре, — для чужого номерка печатает null",
                "Map<Integer, String> cloakroom = new HashMap<>();\nfor (int i = 0; i < tags.size(); i++) {\n"
                "    cloakroom.put(tags.get(i), coats.get(i));\n}\nfor (int tag : returned) {\n"
                '    System.out.println("Номерок " + tag + ": " + cloakroom.get(tag));\n}')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-select-library-log", title="Журнал библиотеки",
        given=[("List<String>", "visits")],
        variants=[{"visits": 'new ArrayList<>(List.of("Петя", "Оля", "Вася", "Оля", "Петя", "Оля"))'},
                  {"visits": 'new ArrayList<>(List.of("Сева", "Алина", "Сева", "Денис", "Сева"))'},
                  {"visits": 'new ArrayList<>(List.of("Юля", "Тимофей", "Кира", "Юля", "Кира", "Ваня", "Юля"))'}],
        hidden=[{"visits": 'new ArrayList<>(List.of("Рома"))'},
                {"visits": 'new ArrayList<>(List.of("Гена", "Арина"))'},
                {"visits": 'new ArrayList<>(List.of("Лена", "Лена", "Лена", "Лена"))'},
                {"visits": 'new ArrayList<>(List.of("Зоя", "Борис", "Эмиль", "Борис", "Нелли"))'}],
        intro="В школьной библиотеке записывают каждого, кто пришёл: имена в списке `visits` идут в порядке посещений, "
              "и один читатель может прийти много раз. Библиотекарю нужны три разных отчёта — для каждого подбери "
              "подходящую коллекцию.",
        steps=["Выведи `Последние: ` и сразу за этим три последних посещения в том же порядке, например "
               "`Последние: [Лиза, Гоша, Лиза]`. Если посещений меньше трёх, выведи все.",
               "Выведи `Читатели: ` и всех читателей без повторов по алфавиту, например `Читатели: [Гоша, Лиза, Миша]`.",
               "Выведи `Посещения: ` и коллекцию, в которой для каждого читателя по алфавиту записано, сколько раз он "
               "приходил, например `Посещения: {{Гоша=1, Лиза=2, Миша=1}}`."],
        hint="Квадратные скобки при выводе дают списки и множества, а фигурные скобки со знаком `=` — словари. "
             "Подумай, какая коллекция сама убирает повторы и сортирует, а какая хранит пары и сортирует их по ключу.",
        solution="int from = Math.max(0, visits.size() - 3);\nList<String> last = visits.subList(from, visits.size());\n"
                 'System.out.println("Последние: " + last);\nSet<String> readers = new TreeSet<>(visits);\n'
                 'System.out.println("Читатели: " + readers);\nMap<String, Integer> counts = new TreeMap<>();\n'
                 "for (String name : visits) {\n    counts.put(name, counts.getOrDefault(name, 0) + 1);\n}\n"
                 'System.out.println("Посещения: " + counts);',
        wrong=[("берёт три первых посещения вместо трёх последних",
                "List<String> last = visits.subList(0, Math.min(3, visits.size()));\n"
                'System.out.println("Последние: " + last);\nSet<String> readers = new TreeSet<>(visits);\n'
                'System.out.println("Читатели: " + readers);\nMap<String, Integer> counts = new TreeMap<>();\n'
                "for (String name : visits) {\n    counts.put(name, counts.getOrDefault(name, 0) + 1);\n}\n"
                'System.out.println("Посещения: " + counts);'),
               ("выбрал LinkedHashSet и LinkedHashMap — читатели идут в порядке первого прихода, а не по алфавиту",
                "int from = Math.max(0, visits.size() - 3);\nList<String> last = visits.subList(from, visits.size());\n"
                'System.out.println("Последние: " + last);\nSet<String> readers = new LinkedHashSet<>(visits);\n'
                'System.out.println("Читатели: " + readers);\nMap<String, Integer> counts = new LinkedHashMap<>();\n'
                "for (String name : visits) {\n    counts.put(name, counts.getOrDefault(name, 0) + 1);\n}\n"
                'System.out.println("Посещения: " + counts);')],
        constructs=["for"],
    ),
]
