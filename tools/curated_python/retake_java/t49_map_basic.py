"""MAP_BASIC — «Словарь Map» (Java). Taught before: everything up to List and Set. Here: Map, HashMap / LinkedHashMap /
TreeMap, put, get, getOrDefault, containsKey, size, keySet, a counter per key, a list as a value. Output never iterates
or prints a HashMap: a HashMap is only asked by key; iteration uses LinkedHashMap or TreeMap."""
from java_tasks import JavaOutputTask

SKILL = "MAP_BASIC"

RETRY = ('System.out.println("Students: " + marks.size());\nif (!marks.containsKey(name)) {\n'
         '    System.out.println(name + ": not in the journal");\n} else if (mark > marks.get(name)) {\n'
         '    int old = marks.get(name);\n    marks.put(name, mark);\n'
         '    System.out.println(name + ": " + old + " -> " + marks.get(name));\n} else {\n'
         '    System.out.println(name + ": stays " + marks.get(name));\n}')

LETTERS = ('Map<Character, Integer> counts = new LinkedHashMap<>();\nfor (int i = 0; i < word.length(); i++) {\n'
           '    char c = word.charAt(i);\n    counts.put(c, counts.getOrDefault(c, 0) + 1);\n}\nint repeated = 0;\n'
           'for (char c : counts.keySet()) {\n    System.out.println(c + ": " + counts.get(c));\n'
           '    if (counts.get(c) > 1) {\n        repeated++;\n    }\n}\n'
           'System.out.println("Repeated letters: " + repeated);')

CHARITY = ('Map<String, Integer> total = new TreeMap<>(first);\nint both = 0;\nfor (String item : second.keySet()) {\n'
           '    if (total.containsKey(item)) {\n        both++;\n    }\n'
           '    total.put(item, total.getOrDefault(item, 0) + second.get(item));\n}\n'
           'for (String item : total.keySet()) {\n    System.out.println(item + ": " + total.get(item));\n}\n'
           'System.out.println("Brought by both: " + both);')

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-map-rt-mark-retry", title="Пересдача контрольной",
        given=[("Map<String, Integer>", "marks"), ("String", "name"), ("int", "mark")],
        variants=[{"marks": 'new HashMap<>(Map.of("Anya", 3, "Boris", 4, "Vika", 5))', "name": '"Anya"', "mark": "5"},
                  {"marks": 'new HashMap<>(Map.of("Gleb", 4, "Dasha", 2, "Egor", 3, "Zoya", 5))', "name": '"Gleb"', "mark": "3"},
                  {"marks": 'new HashMap<>(Map.of("Ira", 2, "Kostya", 3))', "name": '"Lena"', "mark": "4"}],
        hidden=[{"marks": 'new HashMap<>(Map.of("Misha", 4))', "name": '"Misha"', "mark": "4"},
                {"marks": 'new HashMap<>(Map.of("Nina", 2, "Oleg", 5))', "name": '"Nina"', "mark": "3"},
                {"marks": 'new HashMap<>(Map.of("Pavel", 3, "Rita", 3, "Sasha", 4))', "name": '"Tanya"', "mark": "5"},
                {"marks": "new HashMap<>()", "name": '"Ulyana"', "mark": "2"}],
        intro="Оценки за контрольную хранятся в словаре `marks`: ключ — имя ученика, значение — оценка. Ученик `name` "
              "пересдал контрольную и получил `mark`. В журнал идёт лучшая из двух оценок, а пересдавать могут только "
              "те, кто есть в журнале.",
        steps=["Выведи строку вида `Students: 3` — сколько учеников в словаре (метод `size()`).",
               "Если ключа `name` в словаре нет (метод `containsKey`), выведи строку вида `Lena: not in the journal`.",
               "Иначе если новая оценка `mark` больше старой (достань её методом `get`), запиши новую оценку в "
               "словарь методом `put` и выведи строку вида `Anya: 3 -> 5` — старая оценка, стрелка `->` и новая.",
               "Иначе выведи строку вида `Gleb: stays 4` — с оценкой, которая осталась в словаре."],
        hint="Старую оценку запомни в переменную до `put`: после `put` словарь хранит уже новую. При равных оценках "
             "в журнале ничего не меняется.",
        solution=RETRY,
        wrong=[("записывает оценку пересдачи всегда — даже если она хуже",
                'System.out.println("Students: " + marks.size());\nif (!marks.containsKey(name)) {\n'
                '    System.out.println(name + ": not in the journal");\n} else {\n'
                '    int old = marks.get(name);\n    marks.put(name, mark);\n'
                '    System.out.println(name + ": " + old + " -> " + marks.get(name));\n}'),
               ("сравнивает через >= — при равной оценке пишет, что она изменилась",
                RETRY.replace("mark > marks.get(name)", "mark >= marks.get(name)"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-map-rt-word-letters", title="Сколько раз встречается буква",
        given=[("String", "word")],
        variants=[{"word": '"banana"'}, {"word": '"letter"'}, {"word": '"java"'}],
        hidden=[{"word": '"a"'}, {"word": '"abc"'}, {"word": '"mississippi"'}, {"word": '"zzz"'}],
        intro="В игре со словами нужно посчитать, сколько раз в слове `word` встречается каждая буква. Слово "
              "записано маленькими английскими буквами.",
        steps=["Создай словарь `Map<Character, Integer> counts = new LinkedHashMap<>();` — он помнит, в каком порядке "
               "в него добавляли ключи.",
               "Пройди циклом по номерам букв слова (букву с номером `i` даёт `word.charAt(i)`) и увеличь счётчик этой "
               "буквы на 1. Текущее значение удобно брать через `counts.getOrDefault(c, 0)`.",
               "Пройди по ключам словаря (`counts.keySet()`) и для каждой буквы выведи строку вида `b: 1`. Буквы идут "
               "в том порядке, в котором впервые встретились в слове.",
               "Последней строкой выведи строку вида `Repeated letters: 2` — сколько букв встретилось больше одного раза."],
        hint="`put` с ключом, который уже есть в словаре, заменяет значение. Поэтому новое значение счётчика — это "
             "старое плюс один, а для новой буквы старым считается 0.",
        solution=LETTERS,
        wrong=[("каждый раз записывает 1 — счётчик не растёт",
                LETTERS.replace("counts.put(c, counts.getOrDefault(c, 0) + 1);", "counts.put(c, 1);")),
               ("считает повторившимися все буквы, а не только те, что встретились больше одного раза",
                LETTERS.replace("counts.get(c) > 1", "counts.get(c) >= 1"))],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-map-rt-charity-boxes", title="Сбор вещей для приюта",
        given=[("Map<String, Integer>", "first"), ("Map<String, Integer>", "second")],
        variants=[{"first": 'new TreeMap<>(Map.of("books", 12, "toys", 5, "scarves", 3))',
                   "second": 'new TreeMap<>(Map.of("toys", 7, "mittens", 4))'},
                  {"first": 'new TreeMap<>(Map.of("pencils", 30, "paper", 10))',
                   "second": 'new TreeMap<>(Map.of("paper", 15, "pencils", 20, "paints", 6))'},
                  {"first": 'new TreeMap<>(Map.of("socks", 8, "hats", 2, "blankets", 1, "food", 9))',
                   "second": 'new TreeMap<>(Map.of("games", 3, "puzzles", 2))'}],
        hidden=[{"first": 'new TreeMap<>(Map.of("balls", 2))', "second": 'new TreeMap<>(Map.of("balls", 3))'},
                {"first": "new TreeMap<>()", "second": 'new TreeMap<>(Map.of("cups", 4, "plates", 5))'},
                {"first": 'new TreeMap<>(Map.of("jars", 1, "bags", 2))', "second": "new TreeMap<>()"},
                {"first": 'new TreeMap<>(Map.of("a", 1, "b", 2, "c", 3))', "second": 'new TreeMap<>(Map.of("c", 10, "d", 20, "a", 30))'}],
        intro="Два класса собирали вещи для приюта. Что принёс каждый класс, записано в словари `first` и `second`: "
              "ключ — вещь, значение — сколько штук. Оба словаря — `TreeMap`, ключи в них идут по алфавиту. "
              "Теперь всё нужно сложить в одну общую опись.",
        steps=["Создай общий словарь — копию первого: `Map<String, Integer> total = new TreeMap<>(first);` — и счётчик "
               "вещей, которые принесли оба класса, равный 0.",
               "Пройди по ключам словаря `second`. Если такая вещь уже есть в `total` (метод `containsKey`), увеличь "
               "счётчик. Затем прибавь количество из `second` к тому, что уже есть в `total` — для новой вещи там 0, "
               "удобно взять `total.getOrDefault(item, 0)`.",
               "Пройди по ключам `total` и для каждой вещи выведи строку вида `toys: 12`.",
               "Последней строкой выведи строку вида `Brought by both: 1` — сколько вещей принесли оба класса."],
        hint="Проверяй `containsKey` до того, как положишь вещь в `total`: после `put` она там будет всегда. "
             "А `put` с существующим ключом заменяет значение, поэтому сначала сложи старое и новое количество.",
        solution=CHARITY,
        wrong=[("кладёт количество из second вместо суммы — вещи первого класса пропадают",
                CHARITY.replace("total.getOrDefault(item, 0) + second.get(item)", "second.get(item)")),
               ("проверяет containsKey после put — каждая вещь второго класса кажется общей",
                CHARITY.replace('    if (total.containsKey(item)) {\n        both++;\n    }\n'
                                '    total.put(item, total.getOrDefault(item, 0) + second.get(item));\n',
                                '    total.put(item, total.getOrDefault(item, 0) + second.get(item));\n'
                                '    if (total.containsKey(item)) {\n        both++;\n    }\n'))],
        constructs=["for", "if"],
    ),
]
