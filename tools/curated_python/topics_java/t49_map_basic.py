"""MAP_BASIC — «Словарь Map» (Java). Taught before: everything up to List and Set. Here: Map, HashMap / LinkedHashMap /
TreeMap, put, get, getOrDefault, containsKey, size, keySet, a counter per key, a list as a value. Output never iterates
or prints a HashMap: a HashMap is only asked by key; iteration uses LinkedHashMap or TreeMap."""
from java_tasks import JavaOutputTask

SKILL = "MAP_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-map-gym-lockers", title="Шкафчики в раздевалке",
        given=[("Map<String, Integer>", "lockers"), ("String", "name")],
        variants=[{"lockers": 'new HashMap<>(Map.of("Anya", 12, "Boris", 7, "Vika", 3, "Grisha", 15))', "name": '"Vika"'},
                  {"lockers": 'new HashMap<>(Map.of("Dina", 21, "Egor", 4, "Zhenya", 9))', "name": '"Zoya"'},
                  {"lockers": 'new HashMap<>(Map.of("Igor", 30, "Kira", 18, "Lyova", 2, "Marat", 25, "Nina", 11))', "name": '"Marat"'}],
        hidden=[{"lockers": 'new HashMap<>(Map.of("Oskar", 1))', "name": '"Oskar"'},
                {"lockers": 'new HashMap<>(Map.of("Polina", 8, "Ruslan", 16))', "name": '"Stas"'},
                {"lockers": 'new HashMap<>(Map.of("Taya", 5, "Ulyana", 6, "Fedya", 13))', "name": '"Fedya"'},
                {"lockers": "new HashMap<>()", "name": '"Yasha"'}],
        intro="В спортзале у каждого ученика свой шкафчик. Словарь `lockers` хранит, у кого какой шкафчик: ключ — имя, "
              "значение — номер шкафчика. К тренеру подошёл ученик `name` и спрашивает, какой у него номер.",
        steps=["Выведи строку вида `Lockers in use: 6` — сколько пар хранится в словаре (метод `size()`).",
               "Если в словаре есть ключ `name` (проверь методом `containsKey`), выведи имя, двоеточие и номер шкафчика, "
               "например `Petya: locker 14`. Номер достань из словаря методом `get`.",
               "Иначе выведи имя и слова `no locker`, например `Petya: no locker`."],
        hint="Если ключа в словаре нет, `get` вернёт не ошибку, а `null`. Поэтому сначала спроси словарь, знает ли он такое имя.",
        solution='System.out.println("Lockers in use: " + lockers.size());\nif (lockers.containsKey(name)) {\n'
                 '    System.out.println(name + ": locker " + lockers.get(name));\n} else {\n'
                 '    System.out.println(name + ": no locker");\n}',
        wrong=[("не проверяет, есть ли имя в словаре, — для незнакомого имени печатает null",
                'System.out.println("Lockers in use: " + lockers.size());\n'
                'System.out.println(name + ": locker " + lockers.get(name));'),
               ("ищет имя среди значений, а не среди ключей",
                'System.out.println("Lockers in use: " + lockers.size());\nif (lockers.containsValue(name)) {\n'
                '    System.out.println(name + ": locker " + lockers.get(name));\n} else {\n'
                '    System.out.println(name + ": no locker");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-map-pizza-orders", title="Сколько пицц продали",
        given=[("List<String>", "orders")],
        variants=[{"orders": 'new ArrayList<>(List.of("Margherita", "Pepperoni", "Margherita", "Hawaiian", "Pepperoni", "Margherita"))'},
                  {"orders": 'new ArrayList<>(List.of("Four Cheese", "BBQ", "BBQ", "Four Cheese", "BBQ"))'},
                  {"orders": 'new ArrayList<>(List.of("Veggie", "Mushroom", "Meat", "Mushroom", "Veggie", "Mushroom", "Seafood"))'}],
        hidden=[{"orders": 'new ArrayList<>(List.of("Cheese"))'},
                {"orders": 'new ArrayList<>(List.of("Kids", "Kids", "Kids"))'},
                {"orders": 'new ArrayList<>(List.of("Ranch", "Arriba", "Ranch", "Caesar"))'},
                {"orders": 'new ArrayList<>(List.of("Alfredo", "Bianca", "Alfredo"))'}],
        intro="Пиццерия записывает каждую проданную пиццу в список `orders` — по одному названию на каждую пиццу. "
              "Вечером повар хочет узнать, сколько пицц каждого вида продали.",
        steps=["Создай словарь `Map<String, Integer> counts = new LinkedHashMap<>();` — он помнит, в каком порядке "
               "в него добавляли ключи.",
               "Пройди по `orders` и для каждой пиццы увеличь её счётчик в словаре на 1. Если пиццы в словаре ещё нет, "
               "её счётчик должен стать 1 — текущее значение удобно брать через `counts.getOrDefault(name, 0)`.",
               "Пройди по ключам словаря (`counts.keySet()`) и для каждой пиццы выведи строку вида `Carbonara: 2`. "
               "Пиццы идут в том порядке, в котором впервые встретились в `orders`.",
               "Последней строкой выведи строку вида `Pizza kinds: 5` — сколько ключей в словаре."],
        hint="`put` с уже существующим ключом не добавляет новую пару, а заменяет значение. Значит, новое значение "
             "счётчика — это старое плюс один.",
        solution='Map<String, Integer> counts = new LinkedHashMap<>();\nfor (String p : orders) {\n'
                 '    counts.put(p, counts.getOrDefault(p, 0) + 1);\n}\nfor (String p : counts.keySet()) {\n'
                 '    System.out.println(p + ": " + counts.get(p));\n}\nSystem.out.println("Pizza kinds: " + counts.size());',
        wrong=[("каждый раз записывает 1 — счётчик не растёт",
                'Map<String, Integer> counts = new LinkedHashMap<>();\nfor (String p : orders) {\n'
                '    counts.put(p, 1);\n}\nfor (String p : counts.keySet()) {\n'
                '    System.out.println(p + ": " + counts.get(p));\n}\nSystem.out.println("Pizza kinds: " + counts.size());'),
               ("взял TreeMap — пиццы выводятся по алфавиту, а не в порядке первого заказа",
                'Map<String, Integer> counts = new TreeMap<>();\nfor (String p : orders) {\n'
                '    counts.put(p, counts.getOrDefault(p, 0) + 1);\n}\nfor (String p : counts.keySet()) {\n'
                '    System.out.println(p + ": " + counts.get(p));\n}\nSystem.out.println("Pizza kinds: " + counts.size());')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-map-notebook-piles", title="Тетради по стопкам",
        given=[("List<String>", "surnames")],
        variants=[{"surnames": 'new ArrayList<>(List.of("Kozlov", "Andreeva", "Kotova", "Belov", "Abramov", "Kuznetsova"))'},
                  {"surnames": 'new ArrayList<>(List.of("Smirnova", "Petrov", "Sokolov", "Pavlova", "Morozov"))'},
                  {"surnames": 'new ArrayList<>(List.of("Ivanov", "Lebedeva", "Ivanova", "Novikov", "Laptev", "Isaeva", "Galkin"))'}],
        hidden=[{"surnames": 'new ArrayList<>(List.of("Orlov"))'},
                {"surnames": 'new ArrayList<>(List.of("Shishkin", "Shilova", "Shubin"))'},
                {"surnames": 'new ArrayList<>(List.of("Yakovlev", "Volkova", "Egorov", "Tikhonova", "Volkov"))'},
                {"surnames": "new ArrayList<>()"}],
        intro="Учительница раскладывает проверенные тетради по стопкам: в каждой стопке — тетради учеников, чьи фамилии "
              "начинаются на одну и ту же букву. Фамилии в списке `surnames` идут в том порядке, в котором ученики сдавали тетради.",
        steps=["Создай словарь `Map<Character, List<String>> piles = new TreeMap<>();`: ключ — первая буква фамилии, "
               "значение — список фамилий на эту букву. `TreeMap` хранит ключи по алфавиту.",
               "Пройди по `surnames`. Первую букву фамилии `s` даёт `s.charAt(0)`. Если такой буквы ещё нет в словаре, "
               "положи под неё новый пустой список. Затем добавь фамилию в список этой буквы.",
               "Для каждой буквы словаря выведи строку вида `D: [Dmitriev, Denisova]` — букву, двоеточие, пробел и список "
               "фамилий. Внутри стопки фамилии идут в том порядке, в котором сдавали тетради.",
               "Последней строкой выведи строку вида `Piles: 4` — сколько разных букв получилось."],
        hint="Значение в словаре — сам список, поэтому `piles.get(letter).add(surname)` добавляет фамилию прямо в него, "
             "и класть список в словарь заново не нужно.",
        solution='Map<Character, List<String>> piles = new TreeMap<>();\nfor (String s : surnames) {\n    char letter = s.charAt(0);\n'
                 '    if (!piles.containsKey(letter)) {\n        piles.put(letter, new ArrayList<>());\n    }\n'
                 '    piles.get(letter).add(s);\n}\nfor (char letter : piles.keySet()) {\n'
                 '    System.out.println(letter + ": " + piles.get(letter));\n}\nSystem.out.println("Piles: " + piles.size());',
        wrong=[("каждый раз кладёт под букву новый список — в стопке остаётся только последняя фамилия",
                'Map<Character, List<String>> piles = new TreeMap<>();\nfor (String s : surnames) {\n    char letter = s.charAt(0);\n'
                '    List<String> pile = new ArrayList<>();\n    pile.add(s);\n    piles.put(letter, pile);\n}\n'
                'for (char letter : piles.keySet()) {\n    System.out.println(letter + ": " + piles.get(letter));\n}\n'
                'System.out.println("Piles: " + piles.size());'),
               ("берёт символ с номером 1 — это вторая буква фамилии",
                'Map<Character, List<String>> piles = new TreeMap<>();\nfor (String s : surnames) {\n    char letter = s.charAt(1);\n'
                '    if (!piles.containsKey(letter)) {\n        piles.put(letter, new ArrayList<>());\n    }\n'
                '    piles.get(letter).add(s);\n}\nfor (char letter : piles.keySet()) {\n'
                '    System.out.println(letter + ": " + piles.get(letter));\n}\nSystem.out.println("Piles: " + piles.size());')],
        constructs=["for", "if"],
    ),
]
