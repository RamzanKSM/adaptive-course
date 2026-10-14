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
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-map-cafe-menu", title="Новая цена в меню",
        given=[("Map<String, Integer>", "menu"), ("String", "dish"), ("int", "newPrice")],
        variants=[{"menu": 'new HashMap<>(Map.of("tea", 80, "coffee", 150, "cake", 220, "juice", 120))',
                   "dish": '"coffee"', "newPrice": "170"},
                  {"menu": 'new HashMap<>(Map.of("soup", 250, "salad", 190, "bread", 30))',
                   "dish": '"pie"', "newPrice": "140"},
                  {"menu": 'new HashMap<>(Map.of("pancakes", 210, "cocoa", 110, "omelet", 180, "toast", 90, "porridge", 130))',
                   "dish": '"toast"', "newPrice": "100"}],
        hidden=[{"menu": "new HashMap<>()", "dish": '"water"', "newPrice": "50"},
                {"menu": 'new HashMap<>(Map.of("milk", 70))', "dish": '"milk"', "newPrice": "75"},
                {"menu": 'new HashMap<>(Map.of("burger", 320, "fries", 150))', "dish": '"shake"', "newPrice": "200"},
                {"menu": 'new HashMap<>(Map.of("lemonade", 160, "pizza", 450, "pasta", 380))', "dish": '"pizza"', "newPrice": "500"}],
        intro="В кафе меню хранится в словаре `menu`: ключ — название блюда, значение — цена в рублях. Повар решил, "
              "что блюдо `dish` теперь стоит `newPrice` руб. Такого блюда в меню может ещё и не быть — тогда оно появится.",
        steps=["Выведи строку вида `Items before: 4` — сколько блюд в меню сейчас (метод `size()`).",
               "Запиши в словарь новую цену одной командой `menu.put(dish, newPrice);`.",
               "Выведи строку вида `Items after: 4` — сколько блюд в меню теперь.",
               "Последней строкой выведи название блюда и его цену из словаря (метод `get`), например `coffee: 170 rub`."],
        hint="`put` с ключом, который уже есть, не добавляет второе блюдо, а заменяет старую цену. Поэтому число блюд "
             "растёт, только если блюдо новое.",
        solution='System.out.println("Items before: " + menu.size());\nmenu.put(dish, newPrice);\n'
                 'System.out.println("Items after: " + menu.size());\nSystem.out.println(dish + ": " + menu.get(dish) + " rub");',
        wrong=[("выводит цену до того, как записал новую, — печатается старая цена или null",
                'System.out.println("Items before: " + menu.size());\nSystem.out.println(dish + ": " + menu.get(dish) + " rub");\n'
                'menu.put(dish, newPrice);\nSystem.out.println("Items after: " + menu.size());'),
               ("не записывает цену в словарь, а печатает newPrice — новое блюдо в меню не появилось",
                'System.out.println("Items before: " + menu.size());\n'
                'System.out.println("Items after: " + menu.size());\nSystem.out.println(dish + ": " + newPrice + " rub");')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-map-trip-expenses", title="Кто сколько заплатил в поездке",
        given=[("List<String>", "payers"), ("List<Integer>", "amounts")],
        variants=[{"payers": 'new ArrayList<>(List.of("Anya", "Boris", "Anya", "Vika", "Boris"))',
                   "amounts": "new ArrayList<>(List.of(1200, 800, 300, 950, 400))"},
                  {"payers": 'new ArrayList<>(List.of("Gleb", "Dina", "Dina"))',
                   "amounts": "new ArrayList<>(List.of(2000, 700, 600))"},
                  {"payers": 'new ArrayList<>(List.of("Egor", "Zhenya", "Egor", "Egor", "Inna", "Zhenya"))',
                   "amounts": "new ArrayList<>(List.of(150, 500, 250, 100, 640, 120))"}],
        hidden=[{"payers": 'new ArrayList<>(List.of("Kira"))', "amounts": "new ArrayList<>(List.of(300))"},
                {"payers": 'new ArrayList<>(List.of("Lev", "Mila", "Lev"))', "amounts": "new ArrayList<>(List.of(100, 300, 200))"},
                {"payers": 'new ArrayList<>(List.of("Nika", "Oleg", "Pavel"))', "amounts": "new ArrayList<>(List.of(500, 900, 400))"},
                {"payers": 'new ArrayList<>(List.of("Rita", "Rita", "Rita"))', "amounts": "new ArrayList<>(List.of(10, 20, 30))"}],
        intro="Друзья съездили в поход и записывали каждую покупку: кто платил — в список `payers`, сколько рублей — "
              "в список `amounts` (покупка номер `i` — это `payers.get(i)` и `amounts.get(i)`). Теперь нужно "
              "понять, сколько всего потратил каждый.",
        steps=["Создай словарь `Map<String, Integer> totals = new LinkedHashMap<>();` — он помнит порядок, в котором "
               "в него добавляли ключи.",
               "Пройди по номерам покупок `i` и прибавь сумму `amounts.get(i)` к тому, что уже набралось у "
               "`payers.get(i)`. Если человека в словаре ещё нет, считай, что у него было 0 — удобно взять "
               "`totals.getOrDefault(name, 0)`.",
               "Пройди по ключам словаря и для каждого выведи строку вида `Anya: 1500 rub` — в порядке, в котором "
               "люди впервые встретились в `payers`.",
               "Последней строкой выведи строку вида `Paid the most: Anya` — у кого самая большая сумма. Если у "
               "нескольких суммы равны, назови того, кто раньше встретился в `payers`."],
        hint="Чтобы найти самого щедрого, заведи `String best = payers.get(0);` и в цикле по ключам заменяй его, "
             "только если сумма текущего строго больше суммы `best`.",
        solution='Map<String, Integer> totals = new LinkedHashMap<>();\nfor (int i = 0; i < payers.size(); i++) {\n'
                 '    String name = payers.get(i);\n    totals.put(name, totals.getOrDefault(name, 0) + amounts.get(i));\n}\n'
                 'String best = payers.get(0);\nfor (String name : totals.keySet()) {\n'
                 '    System.out.println(name + ": " + totals.get(name) + " rub");\n'
                 '    if (totals.get(name) > totals.get(best)) {\n        best = name;\n    }\n}\n'
                 'System.out.println("Paid the most: " + best);',
        wrong=[("записывает в словарь только последнюю покупку человека, а не сумму",
                'Map<String, Integer> totals = new LinkedHashMap<>();\nfor (int i = 0; i < payers.size(); i++) {\n'
                '    String name = payers.get(i);\n    totals.put(name, amounts.get(i));\n}\n'
                'String best = payers.get(0);\nfor (String name : totals.keySet()) {\n'
                '    System.out.println(name + ": " + totals.get(name) + " rub");\n'
                '    if (totals.get(name) > totals.get(best)) {\n        best = name;\n    }\n}\n'
                'System.out.println("Paid the most: " + best);'),
               ("сравнивает через >= — при равных суммах называет того, кто встретился позже",
                'Map<String, Integer> totals = new LinkedHashMap<>();\nfor (int i = 0; i < payers.size(); i++) {\n'
                '    String name = payers.get(i);\n    totals.put(name, totals.getOrDefault(name, 0) + amounts.get(i));\n}\n'
                'String best = payers.get(0);\nfor (String name : totals.keySet()) {\n'
                '    System.out.println(name + ": " + totals.get(name) + " rub");\n'
                '    if (totals.get(name) >= totals.get(best)) {\n        best = name;\n    }\n}\n'
                'System.out.println("Paid the most: " + best);')],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-map-shop-stock", title="Остатки в магазине",
        given=[("Map<String, Integer>", "stock"), ("List<String>", "orders")],
        variants=[{"stock": 'new TreeMap<>(Map.of("milk", 2, "bread", 1, "eggs", 3))',
                   "orders": 'new ArrayList<>(List.of("bread", "milk", "bread", "cheese"))'},
                  {"stock": 'new TreeMap<>(Map.of("pen", 1, "notebook", 2))',
                   "orders": 'new ArrayList<>(List.of("pen", "pen", "ruler", "notebook"))'},
                  {"stock": 'new TreeMap<>(Map.of("apple", 4, "pear", 0, "plum", 2, "kiwi", 1))',
                   "orders": 'new ArrayList<>(List.of("pear", "kiwi", "apple", "kiwi", "plum"))'}],
        hidden=[{"stock": 'new TreeMap<>(Map.of("soap", 1))', "orders": "new ArrayList<>()"},
                {"stock": 'new TreeMap<>(Map.of("tea", 0))', "orders": 'new ArrayList<>(List.of("tea", "tea"))'},
                {"stock": 'new TreeMap<>(Map.of("salt", 3, "rice", 2))', "orders": 'new ArrayList<>(List.of("rice", "rice", "rice", "salt"))'},
                {"stock": 'new TreeMap<>(Map.of("cola", 5))', "orders": 'new ArrayList<>(List.of("juice", "cola"))'}],
        intro="В маленьком магазине остатки товаров хранятся в словаре `stock`: ключ — товар, значение — сколько "
              "штук осталось. Это `TreeMap`, поэтому ключи в нём идут по алфавиту. Покупатели по очереди просят "
              "товары из списка `orders`, по одной штуке.",
        steps=["Пройди по `orders`. Если товара нет среди ключей словаря, выведи строку вида `No such item: cheese`.",
               "Иначе, если товара осталось 0 штук, выведи строку вида `Out of stock: bread`.",
               "Иначе уменьши остаток товара в словаре на 1 (запиши новое значение через `put`) и выведи строку "
               "вида `Sold: milk`.",
               "После всех заказов пройди по ключам словаря и для каждого товара выведи строку вида `eggs: 3` — "
               "сколько его осталось."],
        hint="`stock.get(item) - 1` только считает новое число, а в словаре ничего не меняет. Чтобы остаток "
             "уменьшился, положи это число обратно под тем же ключом: `stock.put(item, ...)`.",
        solution='for (String item : orders) {\n    if (!stock.containsKey(item)) {\n'
                 '        System.out.println("No such item: " + item);\n    } else if (stock.get(item) == 0) {\n'
                 '        System.out.println("Out of stock: " + item);\n    } else {\n'
                 '        stock.put(item, stock.get(item) - 1);\n        System.out.println("Sold: " + item);\n    }\n}\n'
                 'for (String item : stock.keySet()) {\n    System.out.println(item + ": " + stock.get(item));\n}',
        wrong=[("не проверяет, остался ли товар, — остаток уходит в минус",
                'for (String item : orders) {\n    if (!stock.containsKey(item)) {\n'
                '        System.out.println("No such item: " + item);\n    } else {\n'
                '        stock.put(item, stock.get(item) - 1);\n        System.out.println("Sold: " + item);\n    }\n}\n'
                'for (String item : stock.keySet()) {\n    System.out.println(item + ": " + stock.get(item));\n}'),
               ("считает новый остаток, но не кладёт его обратно в словарь",
                'for (String item : orders) {\n    if (!stock.containsKey(item)) {\n'
                '        System.out.println("No such item: " + item);\n    } else if (stock.get(item) == 0) {\n'
                '        System.out.println("Out of stock: " + item);\n    } else {\n'
                '        int left = stock.get(item) - 1;\n        System.out.println("Sold: " + item);\n    }\n}\n'
                'for (String item : stock.keySet()) {\n    System.out.println(item + ": " + stock.get(item));\n}')],
        constructs=["for", "if"],
    ),
]
