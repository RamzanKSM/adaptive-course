"""LIST_BASIC — «Список List» (Java). Taught before: everything up to interfaces and super (conditions, loops, arrays,
static methods, classes). Here: List<…> and ArrayList, add, get, size, a for-each over a list, a new list built in a
loop, printing a list with println. Not yet: Set, Map, remove/indexOf/sort/subList (topic 50)."""
from java_tasks import JavaOutputTask

SKILL = "LIST_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-list-todo-day", title="Список дел на день",
        given=[("List<String>", "tasks"), ("String", "extra")],
        variants=[{"tasks": 'new ArrayList<>(List.of("exercise", "homework", "training"))', "extra": '"water the flowers"'},
                  {"tasks": 'new ArrayList<>(List.of("buy bread", "call grandma"))', "extra": '"walk the dog"'},
                  {"tasks": 'new ArrayList<>(List.of("do math", "read a book", "clean the desk", "pack the bag"))',
                   "extra": '"check the bike"'}],
        hidden=[{"tasks": "new ArrayList<>()", "extra": '"rest"'},
                {"tasks": 'new ArrayList<>(List.of("laundry"))', "extra": '"ironing"'},
                {"tasks": 'new ArrayList<>(List.of("morning run", "breakfast", "school", "art club", "dinner"))', "extra": '"bedtime story"'}],
        intro="Утром ты записываешь дела на день в список `tasks` — в том порядке, в котором будешь их делать. "
              "Днём появилось ещё одно дело — `extra`, и его нужно сделать последним.",
        steps=["Добавь дело `extra` в конец списка `tasks` методом `add`.",
               "Выведи строку вида `Tasks for today: 6` — сколько дел теперь в списке. Размер списка возвращает метод `size()`.",
               "Выведи строку вида `First: wash the dishes` с первым делом из списка, а затем строку вида "
               "`Last: take out the trash` с последним делом. Элемент по номеру достаёт метод `get`."],
        hint="Номера элементов в списке начинаются с 0, поэтому у последнего элемента номер на единицу меньше размера "
             "списка: `tasks.size() - 1`.",
        solution='tasks.add(extra);\nSystem.out.println("Tasks for today: " + tasks.size());\n'
                 'System.out.println("First: " + tasks.get(0));\nSystem.out.println("Last: " + tasks.get(tasks.size() - 1));',
        wrong=[("нумерует элементы с единицы — первым выводит второе дело",
                'tasks.add(extra);\nSystem.out.println("Tasks for today: " + tasks.size());\n'
                'System.out.println("First: " + tasks.get(1));\nSystem.out.println("Last: " + tasks.get(tasks.size() - 1));'),
               ("не добавил новое дело в список — и число дел, и последнее дело старые",
                'System.out.println("Tasks for today: " + tasks.size());\n'
                'System.out.println("First: " + tasks.get(0));\nSystem.out.println("Last: " + tasks.get(tasks.size() - 1));')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-list-sale-prices", title="Цены на распродаже",
        given=[("List<Integer>", "prices"), ("int", "percent")],
        variants=[{"prices": "new ArrayList<>(List.of(1200, 500, 3000))", "percent": "10"},
                  {"prices": "new ArrayList<>(List.of(800, 2500, 400, 1500))", "percent": "20"},
                  {"prices": "new ArrayList<>(List.of(4000, 600))", "percent": "25"}],
        hidden=[{"prices": "new ArrayList<>(List.of(700, 300, 100, 900, 200))", "percent": "0"},
                {"prices": "new ArrayList<>(List.of(5000, 5000))", "percent": "50"},
                {"prices": "new ArrayList<>(List.of(900))", "percent": "30"},
                {"prices": "new ArrayList<>()", "percent": "15"}],
        intro="В магазине распродажа: на все товары скидка {percent}%. Цены товаров из твоей корзины (в рублях) записаны "
              "в список `prices`, а размер скидки в процентах — в поле `percent`. Нужно узнать новые цены и сколько "
              "придётся заплатить.",
        steps=["Создай новый пустой список для цен со скидкой: `List<Integer> sale = new ArrayList<>();`.",
               "Пройди по списку `prices` циклом for-each и для каждой цены добавь в `sale` цену со скидкой: "
               "`price - price * percent / 100`.",
               "Выведи список `sale` командой `System.out.println(sale);`.",
               "Последней строкой выведи сумму всех цен из `sale` в виде `Total: 3150 rub`"],
        hint="Переменная цикла for-each — это копия элемента: если присвоить ей новое значение, список `prices` "
             "не изменится. Поэтому новые цены складывай в отдельный список методом `add`.",
        solution="List<Integer> sale = new ArrayList<>();\nfor (int price : prices) {\n    sale.add(price - price * percent / 100);\n}\n"
                 "System.out.println(sale);\nint total = 0;\nfor (int price : sale) {\n    total += price;\n}\n"
                 'System.out.println("Total: " + total + " rub");',
        wrong=[("меняет переменную цикла — в списке остаются старые цены",
                "for (int price : prices) {\n    price = price - price * percent / 100;\n}\nSystem.out.println(prices);\n"
                "int total = 0;\nfor (int price : prices) {\n    total += price;\n}\n"
                'System.out.println("Total: " + total + " rub");'),
               ("добавляет в список размер скидки, а не новую цену",
                "List<Integer> sale = new ArrayList<>();\nfor (int price : prices) {\n    sale.add(price * percent / 100);\n}\n"
                "System.out.println(sale);\nint total = 0;\nfor (int price : sale) {\n    total += price;\n}\n"
                'System.out.println("Total: " + total + " rub");')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-list-merge-playlist", title="Общий плейлист",
        given=[("List<String>", "mine"), ("List<String>", "friend")],
        variants=[{"mine": 'new ArrayList<>(List.of("Summer", "Night City", "Shore"))',
                   "friend": 'new ArrayList<>(List.of("Blue Tram", "Lights"))'},
                  {"mine": 'new ArrayList<>(List.of("Wind", "Road"))',
                   "friend": 'new ArrayList<>(List.of("Sun", "Lighthouse", "Flight", "Fog"))'},
                  {"mine": 'new ArrayList<>(List.of("Stars", "River", "Snowstorm", "Station", "April"))',
                   "friend": 'new ArrayList<>(List.of("Comets", "Bridges"))'}],
        hidden=[{"mine": "new ArrayList<>()", "friend": 'new ArrayList<>(List.of("One", "Two"))'},
                {"mine": 'new ArrayList<>(List.of("Dawn"))', "friend": "new ArrayList<>()"},
                {"mine": 'new ArrayList<>(List.of("Storm", "Rain", "Rainbow"))', "friend": 'new ArrayList<>(List.of("Snow", "Frost", "Ice"))'},
                {"mine": 'new ArrayList<>(List.of("Dream"))', "friend": 'new ArrayList<>(List.of("Tea", "Coffee", "Cocoa", "Juice"))'}],
        intro="Вы с другом собираете общий плейлист для поездки. Твои песни записаны в список `mine`, песни друга — "
              "в список `friend`. Песни должны идти по очереди: твоя, его, твоя, его… Когда в одном списке песни "
              "закончатся, оставшиеся песни другого идут подряд.",
        steps=["Создай пустой список `List<String> playlist = new ArrayList<>();`.",
               "Сделай цикл по номерам `i` от 0, который продолжается, пока `i` меньше размера хотя бы одного из списков. "
               "На каждом шаге добавь в `playlist` песню `mine.get(i)`, если в `mine` есть элемент с номером `i`, "
               "а затем песню `friend.get(i)`, если такой элемент есть в `friend`.",
               "Выведи `playlist` командой `System.out.println(playlist);`.",
               "Последней строкой выведи строку вида `Total songs: 7` — размер плейлиста."],
        hint="Элемент с номером `i` есть в списке, только если `i < list.size()`. Проверяй это перед каждым `get`, "
             "иначе программа остановится с ошибкой `IndexOutOfBoundsException`.",
        solution="List<String> playlist = new ArrayList<>();\nfor (int i = 0; i < mine.size() || i < friend.size(); i++) {\n"
                 "    if (i < mine.size()) {\n        playlist.add(mine.get(i));\n    }\n"
                 "    if (i < friend.size()) {\n        playlist.add(friend.get(i));\n    }\n}\n"
                 'System.out.println(playlist);\nSystem.out.println("Total songs: " + playlist.size());',
        wrong=[("цикл идёт только до конца короткого списка — песни из длинного теряются",
                "List<String> playlist = new ArrayList<>();\nfor (int i = 0; i < Math.min(mine.size(), friend.size()); i++) {\n"
                "    playlist.add(mine.get(i));\n    playlist.add(friend.get(i));\n}\n"
                'System.out.println(playlist);\nSystem.out.println("Total songs: " + playlist.size());'),
               ("сначала все свои песни, потом все песни друга — без чередования",
                "List<String> playlist = new ArrayList<>();\nfor (String song : mine) {\n    playlist.add(song);\n}\n"
                "for (String song : friend) {\n    playlist.add(song);\n}\n"
                'System.out.println(playlist);\nSystem.out.println("Total songs: " + playlist.size());')],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-list-weather-diary", title="Дневник погоды",
        given=[("List<Integer>", "temps"), ("int", "today"), ("int", "day")],
        variants=[{"temps": "new ArrayList<>(List.of(12, 15, 9, 14))", "today": "17", "day": "2"},
                  {"temps": "new ArrayList<>(List.of(-3, -5, 0))", "today": "2", "day": "1"},
                  {"temps": "new ArrayList<>(List.of(20, 22, 25, 24, 19, 18))", "today": "21", "day": "4"}],
        hidden=[{"temps": "new ArrayList<>()", "today": "5", "day": "1"},
                {"temps": "new ArrayList<>(List.of(7))", "today": "8", "day": "2"},
                {"temps": "new ArrayList<>(List.of(1, 2, 3))", "today": "4", "day": "3"},
                {"temps": "new ArrayList<>(List.of(30, 31, 29, 28, 27))", "today": "26", "day": "1"}],
        intro="Ты ведёшь дневник погоды: каждый день записываешь температуру в список `temps`. Сегодня на улице "
              "`today` градусов. А ещё друг спрашивает, какая температура была в день номер `day` (дни считаются с 1).",
        steps=["Добавь сегодняшнюю температуру `today` в конец списка `temps` методом `add`.",
               "Выведи строку вида `Days: 5` — сколько дней теперь записано в дневнике (метод `size()`).",
               "Выведи строку вида `Day 2: 15` — номер дня `day` и температуру в этот день. Достань её методом `get`; "
               "помни, что день номер 1 лежит в списке под номером 0.",
               "Последней строкой выведи весь список командой `System.out.println(temps);`."],
        hint="Номер элемента в списке на единицу меньше номера дня: день `day` достаётся как `temps.get(day - 1)`.",
        solution='temps.add(today);\nSystem.out.println("Days: " + temps.size());\n'
                 'System.out.println("Day " + day + ": " + temps.get(day - 1));\nSystem.out.println(temps);',
        wrong=[("берёт элемент с номером day — это следующий день",
                'temps.add(today);\nSystem.out.println("Days: " + temps.size());\n'
                'System.out.println("Day " + day + ": " + temps.get(day));\nSystem.out.println(temps);'),
               ("выводит число дней до того, как добавил сегодняшний",
                'System.out.println("Days: " + temps.size());\ntemps.add(today);\n'
                'System.out.println("Day " + day + ": " + temps.get(day - 1));\nSystem.out.println(temps);')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-list-step-goal", title="Цель по шагам",
        given=[("List<Integer>", "steps"), ("int", "goal")],
        variants=[{"steps": "new ArrayList<>(List.of(8000, 12000, 10000, 6500, 10000, 15000, 3000))", "goal": "10000"},
                  {"steps": "new ArrayList<>(List.of(4200, 5100, 4999, 7000))", "goal": "5000"},
                  {"steps": "new ArrayList<>(List.of(9000, 11000, 8000, 7999, 12500))", "goal": "8000"}],
        hidden=[{"steps": "new ArrayList<>(List.of(100, 200))", "goal": "1000"},
                {"steps": "new ArrayList<>(List.of(6000))", "goal": "6000"},
                {"steps": "new ArrayList<>(List.of(3000, 3001, 2999, 3000, 5000, 1))", "goal": "3000"},
                {"steps": "new ArrayList<>()", "goal": "5000"}],
        intro="Фитнес-браслет записывает, сколько шагов ты прошёл за каждый день, — по порядку, в список `steps`. "
              "Твоя цель — не меньше `goal` шагов в день. Нужно найти номера дней, когда цель выполнена.",
        steps=["Создай пустой список `List<Integer> goodDays = new ArrayList<>();` для номеров удачных дней.",
               "Пройди по списку `steps` циклом по номерам `i` от 0 до `steps.size() - 1`. Если в день с номером `i` "
               "шагов не меньше `goal`, добавь в `goodDays` номер этого дня для людей — `i + 1` (дни считаются с 1).",
               "Выведи `Good days: ` и сразу за этим список `goodDays`, например `Good days: [2, 3, 5]`.",
               "Последней строкой выведи строку вида `Goal reached: 3 of 7 days` — сколько дней в `goodDays` "
               "и сколько всего дней в `steps`."],
        hint="Цикл for-each даёт сами числа шагов, но не номер дня. Здесь нужен номер, поэтому иди по индексам и "
             "доставай шаги через `steps.get(i)`.",
        solution="List<Integer> goodDays = new ArrayList<>();\nfor (int i = 0; i < steps.size(); i++) {\n"
                 "    if (steps.get(i) >= goal) {\n        goodDays.add(i + 1);\n    }\n}\n"
                 'System.out.println("Good days: " + goodDays);\n'
                 'System.out.println("Goal reached: " + goodDays.size() + " of " + steps.size() + " days");',
        wrong=[("сравнивает строго больше — день ровно с goal шагами не засчитан",
                "List<Integer> goodDays = new ArrayList<>();\nfor (int i = 0; i < steps.size(); i++) {\n"
                "    if (steps.get(i) > goal) {\n        goodDays.add(i + 1);\n    }\n}\n"
                'System.out.println("Good days: " + goodDays);\n'
                'System.out.println("Goal reached: " + goodDays.size() + " of " + steps.size() + " days");'),
               ("добавляет индекс i — дни получаются пронумерованы с нуля",
                "List<Integer> goodDays = new ArrayList<>();\nfor (int i = 0; i < steps.size(); i++) {\n"
                "    if (steps.get(i) >= goal) {\n        goodDays.add(i);\n    }\n}\n"
                'System.out.println("Good days: " + goodDays);\n'
                'System.out.println("Goal reached: " + goodDays.size() + " of " + steps.size() + " days");')],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-list-price-changes", title="Цена на рынке",
        given=[("List<Integer>", "prices")],
        variants=[{"prices": "new ArrayList<>(List.of(120, 150, 140, 140, 170))"},
                  {"prices": "new ArrayList<>(List.of(300, 280, 250, 260))"},
                  {"prices": "new ArrayList<>(List.of(90, 80, 70))"}],
        hidden=[{"prices": "new ArrayList<>(List.of(100))"},
                {"prices": "new ArrayList<>(List.of(50, 50, 50))"},
                {"prices": "new ArrayList<>(List.of(10, 40, 20, 50, 45, 80))"},
                {"prices": "new ArrayList<>(List.of(200, 200, 230))"}],
        intro="Бабушка каждый день записывает цену килограмма огурцов на рынке в список `prices` — по порядку дней. "
              "Она хочет понять, как цена менялась от дня к дню и на сколько она подскакивала сильнее всего.",
        steps=["Создай пустой список `List<Integer> changes = new ArrayList<>();`. Пройди по номерам `i` начиная "
               "с 1 и для каждого дня добавь в `changes` изменение цены: `prices.get(i) - prices.get(i - 1)` "
               "(рост — положительное число, падение — отрицательное).",
               "Выведи `Changes: ` и сразу за этим список `changes`, например `Changes: [30, -10]`.",
               "Посчитай, сколько изменений больше нуля, и выведи строку вида `Days of growth: 2`.",
               "Если таких изменений нет, последней строкой выведи `No growth`, иначе — строку вида "
               "`Biggest rise: 30 rub` с самым большим изменением."],
        hint="У первого дня нет предыдущего, поэтому цикл начинается с `i = 1`, и изменений на одно меньше, чем "
             "дней. Если цена не изменилась, изменение равно 0 — это не рост.",
        solution="List<Integer> changes = new ArrayList<>();\nfor (int i = 1; i < prices.size(); i++) {\n"
                 "    changes.add(prices.get(i) - prices.get(i - 1));\n}\n"
                 'System.out.println("Changes: " + changes);\nint growth = 0;\nint biggest = 0;\n'
                 "for (int change : changes) {\n    if (change > 0) {\n        growth++;\n"
                 "        if (change > biggest) {\n            biggest = change;\n        }\n    }\n}\n"
                 'System.out.println("Days of growth: " + growth);\nif (growth == 0) {\n'
                 '    System.out.println("No growth");\n} else {\n'
                 '    System.out.println("Biggest rise: " + biggest + " rub");\n}',
        wrong=[("вычитает в обратном порядке — рост и падение меняются местами",
                "List<Integer> changes = new ArrayList<>();\nfor (int i = 1; i < prices.size(); i++) {\n"
                "    changes.add(prices.get(i - 1) - prices.get(i));\n}\n"
                'System.out.println("Changes: " + changes);\nint growth = 0;\nint biggest = 0;\n'
                "for (int change : changes) {\n    if (change > 0) {\n        growth++;\n"
                "        if (change > biggest) {\n            biggest = change;\n        }\n    }\n}\n"
                'System.out.println("Days of growth: " + growth);\nif (growth == 0) {\n'
                '    System.out.println("No growth");\n} else {\n'
                '    System.out.println("Biggest rise: " + biggest + " rub");\n}'),
               ("считает ростом и дни без изменений (change >= 0)",
                "List<Integer> changes = new ArrayList<>();\nfor (int i = 1; i < prices.size(); i++) {\n"
                "    changes.add(prices.get(i) - prices.get(i - 1));\n}\n"
                'System.out.println("Changes: " + changes);\nint growth = 0;\nint biggest = 0;\n'
                "for (int change : changes) {\n    if (change >= 0) {\n        growth++;\n"
                "        if (change > biggest) {\n            biggest = change;\n        }\n    }\n}\n"
                'System.out.println("Days of growth: " + growth);\nif (growth == 0) {\n'
                '    System.out.println("No growth");\n} else {\n'
                '    System.out.println("Biggest rise: " + biggest + " rub");\n}')],
        constructs=["for", "if"],
    ),
]
