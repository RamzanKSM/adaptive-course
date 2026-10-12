"""MAP_BASIC — «Словарь Map» (Java). Taught before: everything up to List and Set. Here: Map, HashMap / LinkedHashMap /
TreeMap, put, get, getOrDefault, containsKey, size, keySet, a counter per key, a list as a value. Output never iterates
or prints a HashMap: a HashMap is only asked by key; iteration uses LinkedHashMap or TreeMap."""
from java_tasks import JavaOutputTask

SKILL = "MAP_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-map-gym-lockers", title="Шкафчики в раздевалке",
        given=[("Map<String, Integer>", "lockers"), ("String", "name")],
        variants=[{"lockers": 'new HashMap<>(Map.of("Аня", 12, "Борис", 7, "Вика", 3, "Гриша", 15))', "name": '"Вика"'},
                  {"lockers": 'new HashMap<>(Map.of("Дина", 21, "Егор", 4, "Женя", 9))', "name": '"Зоя"'},
                  {"lockers": 'new HashMap<>(Map.of("Игорь", 30, "Кира", 18, "Лёва", 2, "Марат", 25, "Нина", 11))', "name": '"Марат"'}],
        hidden=[{"lockers": 'new HashMap<>(Map.of("Оскар", 1))', "name": '"Оскар"'},
                {"lockers": 'new HashMap<>(Map.of("Полина", 8, "Руслан", 16))', "name": '"Стас"'},
                {"lockers": 'new HashMap<>(Map.of("Тая", 5, "Ульяна", 6, "Федя", 13))', "name": '"Федя"'},
                {"lockers": "new HashMap<>()", "name": '"Яша"'}],
        intro="В спортзале у каждого ученика свой шкафчик. Словарь `lockers` хранит, у кого какой шкафчик: ключ — имя, "
              "значение — номер шкафчика. К тренеру подошёл ученик `name` и спрашивает, какой у него номер.",
        steps=["Выведи строку вида `Занято шкафчиков: 6` — сколько пар хранится в словаре (метод `size()`).",
               "Если в словаре есть ключ `name` (проверь методом `containsKey`), выведи имя, двоеточие и номер шкафчика, "
               "например `Петя: шкафчик 14`. Номер достань из словаря методом `get`.",
               "Иначе выведи имя и слова `шкафчика нет`, например `Петя: шкафчика нет`."],
        hint="Если ключа в словаре нет, `get` вернёт не ошибку, а `null`. Поэтому сначала спроси словарь, знает ли он такое имя.",
        solution='System.out.println("Занято шкафчиков: " + lockers.size());\nif (lockers.containsKey(name)) {\n'
                 '    System.out.println(name + ": шкафчик " + lockers.get(name));\n} else {\n'
                 '    System.out.println(name + ": шкафчика нет");\n}',
        wrong=[("не проверяет, есть ли имя в словаре, — для незнакомого имени печатает null",
                'System.out.println("Занято шкафчиков: " + lockers.size());\n'
                'System.out.println(name + ": шкафчик " + lockers.get(name));'),
               ("ищет имя среди значений, а не среди ключей",
                'System.out.println("Занято шкафчиков: " + lockers.size());\nif (lockers.containsValue(name)) {\n'
                '    System.out.println(name + ": шкафчик " + lockers.get(name));\n} else {\n'
                '    System.out.println(name + ": шкафчика нет");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-map-pizza-orders", title="Сколько пицц продали",
        given=[("List<String>", "orders")],
        variants=[{"orders": 'new ArrayList<>(List.of("Маргарита", "Пепперони", "Маргарита", "Гавайская", "Пепперони", "Маргарита"))'},
                  {"orders": 'new ArrayList<>(List.of("Четыре сыра", "Барбекю", "Барбекю", "Четыре сыра", "Барбекю"))'},
                  {"orders": 'new ArrayList<>(List.of("Овощная", "Грибная", "Мясная", "Грибная", "Овощная", "Грибная", "Морская"))'}],
        hidden=[{"orders": 'new ArrayList<>(List.of("Сырная"))'},
                {"orders": 'new ArrayList<>(List.of("Детская", "Детская", "Детская"))'},
                {"orders": 'new ArrayList<>(List.of("Ранч", "Арриба", "Ранч", "Цезарь"))'},
                {"orders": 'new ArrayList<>(List.of("Альфредо", "Бьянка", "Альфредо"))'}],
        intro="Пиццерия записывает каждую проданную пиццу в список `orders` — по одному названию на каждую пиццу. "
              "Вечером повар хочет узнать, сколько пицц каждого вида продали.",
        steps=["Создай словарь `Map<String, Integer> counts = new LinkedHashMap<>();` — он помнит, в каком порядке "
               "в него добавляли ключи.",
               "Пройди по `orders` и для каждой пиццы увеличь её счётчик в словаре на 1. Если пиццы в словаре ещё нет, "
               "её счётчик должен стать 1 — текущее значение удобно брать через `counts.getOrDefault(название, 0)`.",
               "Пройди по ключам словаря (`counts.keySet()`) и для каждой пиццы выведи строку вида `Карбонара: 2`. "
               "Пиццы идут в том порядке, в котором впервые встретились в `orders`.",
               "Последней строкой выведи строку вида `Видов пиццы: 5` — сколько ключей в словаре."],
        hint="`put` с уже существующим ключом не добавляет новую пару, а заменяет значение. Значит, новое значение "
             "счётчика — это старое плюс один.",
        solution='Map<String, Integer> counts = new LinkedHashMap<>();\nfor (String p : orders) {\n'
                 '    counts.put(p, counts.getOrDefault(p, 0) + 1);\n}\nfor (String p : counts.keySet()) {\n'
                 '    System.out.println(p + ": " + counts.get(p));\n}\nSystem.out.println("Видов пиццы: " + counts.size());',
        wrong=[("каждый раз записывает 1 — счётчик не растёт",
                'Map<String, Integer> counts = new LinkedHashMap<>();\nfor (String p : orders) {\n'
                '    counts.put(p, 1);\n}\nfor (String p : counts.keySet()) {\n'
                '    System.out.println(p + ": " + counts.get(p));\n}\nSystem.out.println("Видов пиццы: " + counts.size());'),
               ("взял TreeMap — пиццы выводятся по алфавиту, а не в порядке первого заказа",
                'Map<String, Integer> counts = new TreeMap<>();\nfor (String p : orders) {\n'
                '    counts.put(p, counts.getOrDefault(p, 0) + 1);\n}\nfor (String p : counts.keySet()) {\n'
                '    System.out.println(p + ": " + counts.get(p));\n}\nSystem.out.println("Видов пиццы: " + counts.size());')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-map-notebook-piles", title="Тетради по стопкам",
        given=[("List<String>", "surnames")],
        variants=[{"surnames": 'new ArrayList<>(List.of("Козлов", "Андреева", "Котова", "Белов", "Абрамов", "Кузнецова"))'},
                  {"surnames": 'new ArrayList<>(List.of("Смирнова", "Петров", "Соколов", "Павлова", "Морозов"))'},
                  {"surnames": 'new ArrayList<>(List.of("Иванов", "Лебедева", "Иванова", "Новиков", "Лаптев", "Исаева", "Галкин"))'}],
        hidden=[{"surnames": 'new ArrayList<>(List.of("Орлов"))'},
                {"surnames": 'new ArrayList<>(List.of("Шишкин", "Шилова", "Шубин"))'},
                {"surnames": 'new ArrayList<>(List.of("Яковлев", "Волкова", "Егоров", "Тихонова", "Волков"))'},
                {"surnames": "new ArrayList<>()"}],
        intro="Учительница раскладывает проверенные тетради по стопкам: в каждой стопке — тетради учеников, чьи фамилии "
              "начинаются на одну и ту же букву. Фамилии в списке `surnames` идут в том порядке, в котором ученики сдавали тетради.",
        steps=["Создай словарь `Map<Character, List<String>> piles = new TreeMap<>();`: ключ — первая буква фамилии, "
               "значение — список фамилий на эту букву. `TreeMap` хранит ключи по алфавиту.",
               "Пройди по `surnames`. Первую букву фамилии `s` даёт `s.charAt(0)`. Если такой буквы ещё нет в словаре, "
               "положи под неё новый пустой список. Затем добавь фамилию в список этой буквы.",
               "Для каждой буквы словаря выведи строку вида `Д: [Дмитриев, Денисова]` — букву, двоеточие, пробел и список "
               "фамилий. Внутри стопки фамилии идут в том порядке, в котором сдавали тетради.",
               "Последней строкой выведи строку вида `Стопок: 4` — сколько разных букв получилось."],
        hint="Значение в словаре — сам список, поэтому `piles.get(буква).add(фамилия)` добавляет фамилию прямо в него, "
             "и класть список в словарь заново не нужно.",
        solution='Map<Character, List<String>> piles = new TreeMap<>();\nfor (String s : surnames) {\n    char letter = s.charAt(0);\n'
                 '    if (!piles.containsKey(letter)) {\n        piles.put(letter, new ArrayList<>());\n    }\n'
                 '    piles.get(letter).add(s);\n}\nfor (char letter : piles.keySet()) {\n'
                 '    System.out.println(letter + ": " + piles.get(letter));\n}\nSystem.out.println("Стопок: " + piles.size());',
        wrong=[("каждый раз кладёт под букву новый список — в стопке остаётся только последняя фамилия",
                'Map<Character, List<String>> piles = new TreeMap<>();\nfor (String s : surnames) {\n    char letter = s.charAt(0);\n'
                '    List<String> pile = new ArrayList<>();\n    pile.add(s);\n    piles.put(letter, pile);\n}\n'
                'for (char letter : piles.keySet()) {\n    System.out.println(letter + ": " + piles.get(letter));\n}\n'
                'System.out.println("Стопок: " + piles.size());'),
               ("берёт символ с номером 1 — это вторая буква фамилии",
                'Map<Character, List<String>> piles = new TreeMap<>();\nfor (String s : surnames) {\n    char letter = s.charAt(1);\n'
                '    if (!piles.containsKey(letter)) {\n        piles.put(letter, new ArrayList<>());\n    }\n'
                '    piles.get(letter).add(s);\n}\nfor (char letter : piles.keySet()) {\n'
                '    System.out.println(letter + ": " + piles.get(letter));\n}\nSystem.out.println("Стопок: " + piles.size());')],
        constructs=["for", "if"],
    ),
]
