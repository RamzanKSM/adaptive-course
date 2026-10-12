"""LIST_BASIC — «Список List» (Java). Taught before: everything up to interfaces and super (conditions, loops, arrays,
static methods, classes). Here: List<…> and ArrayList, add, get, size, a for-each over a list, a new list built in a
loop, printing a list with println. Not yet: Set, Map, remove/indexOf/sort/subList (topic 50)."""
from java_tasks import JavaOutputTask

SKILL = "LIST_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-list-todo-day", title="Список дел на день",
        given=[("List<String>", "tasks"), ("String", "extra")],
        variants=[{"tasks": 'new ArrayList<>(List.of("зарядка", "уроки", "тренировка"))', "extra": '"полить цветы"'},
                  {"tasks": 'new ArrayList<>(List.of("купить хлеб", "позвонить бабушке"))', "extra": '"погулять с собакой"'},
                  {"tasks": 'new ArrayList<>(List.of("сделать математику", "почитать книгу", "убрать на столе", "собрать рюкзак"))',
                   "extra": '"проверить велосипед"'}],
        hidden=[{"tasks": "new ArrayList<>()", "extra": '"отдохнуть"'},
                {"tasks": 'new ArrayList<>(List.of("стирка"))', "extra": '"глажка"'},
                {"tasks": 'new ArrayList<>(List.of("пробежка", "завтрак", "школа", "кружок", "ужин"))', "extra": '"сказка"'}],
        intro="Утром ты записываешь дела на день в список `tasks` — в том порядке, в котором будешь их делать. "
              "Днём появилось ещё одно дело — `extra`, и его нужно сделать последним.",
        steps=["Добавь дело `extra` в конец списка `tasks` методом `add`.",
               "Выведи строку вида `Дел на сегодня: 6` — сколько дел теперь в списке. Размер списка возвращает метод `size()`.",
               "Выведи строку вида `Первое: помыть посуду` с первым делом из списка, а затем строку вида "
               "`Последнее: вынести мусор` с последним делом. Элемент по номеру достаёт метод `get`."],
        hint="Номера элементов в списке начинаются с 0, поэтому у последнего элемента номер на единицу меньше размера "
             "списка: `tasks.size() - 1`.",
        solution='tasks.add(extra);\nSystem.out.println("Дел на сегодня: " + tasks.size());\n'
                 'System.out.println("Первое: " + tasks.get(0));\nSystem.out.println("Последнее: " + tasks.get(tasks.size() - 1));',
        wrong=[("нумерует элементы с единицы — первым выводит второе дело",
                'tasks.add(extra);\nSystem.out.println("Дел на сегодня: " + tasks.size());\n'
                'System.out.println("Первое: " + tasks.get(1));\nSystem.out.println("Последнее: " + tasks.get(tasks.size() - 1));'),
               ("не добавил новое дело в список — и число дел, и последнее дело старые",
                'System.out.println("Дел на сегодня: " + tasks.size());\n'
                'System.out.println("Первое: " + tasks.get(0));\nSystem.out.println("Последнее: " + tasks.get(tasks.size() - 1));')],
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
               "`цена - цена * percent / 100`.",
               "Выведи список `sale` командой `System.out.println(sale);`.",
               "Последней строкой выведи сумму всех цен из `sale` в виде `Итого: 3150 руб.`"],
        hint="Переменная цикла for-each — это копия элемента: если присвоить ей новое значение, список `prices` "
             "не изменится. Поэтому новые цены складывай в отдельный список методом `add`.",
        solution="List<Integer> sale = new ArrayList<>();\nfor (int price : prices) {\n    sale.add(price - price * percent / 100);\n}\n"
                 "System.out.println(sale);\nint total = 0;\nfor (int price : sale) {\n    total += price;\n}\n"
                 'System.out.println("Итого: " + total + " руб.");',
        wrong=[("меняет переменную цикла — в списке остаются старые цены",
                "for (int price : prices) {\n    price = price - price * percent / 100;\n}\nSystem.out.println(prices);\n"
                "int total = 0;\nfor (int price : prices) {\n    total += price;\n}\n"
                'System.out.println("Итого: " + total + " руб.");'),
               ("добавляет в список размер скидки, а не новую цену",
                "List<Integer> sale = new ArrayList<>();\nfor (int price : prices) {\n    sale.add(price * percent / 100);\n}\n"
                "System.out.println(sale);\nint total = 0;\nfor (int price : sale) {\n    total += price;\n}\n"
                'System.out.println("Итого: " + total + " руб.");')],
        constructs=["for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-list-merge-playlist", title="Общий плейлист",
        given=[("List<String>", "mine"), ("List<String>", "friend")],
        variants=[{"mine": 'new ArrayList<>(List.of("Лето", "Ночной город", "Берег"))',
                   "friend": 'new ArrayList<>(List.of("Синий трамвай", "Огни"))'},
                  {"mine": 'new ArrayList<>(List.of("Ветер", "Дорога"))',
                   "friend": 'new ArrayList<>(List.of("Солнце", "Маяк", "Полёт", "Туман"))'},
                  {"mine": 'new ArrayList<>(List.of("Звёзды", "Река", "Метель", "Вокзал", "Апрель"))',
                   "friend": 'new ArrayList<>(List.of("Кометы", "Мосты"))'}],
        hidden=[{"mine": "new ArrayList<>()", "friend": 'new ArrayList<>(List.of("Один", "Два"))'},
                {"mine": 'new ArrayList<>(List.of("Рассвет"))', "friend": "new ArrayList<>()"},
                {"mine": 'new ArrayList<>(List.of("Гроза", "Ливень", "Радуга"))', "friend": 'new ArrayList<>(List.of("Снег", "Иней", "Лёд"))'},
                {"mine": 'new ArrayList<>(List.of("Сон"))', "friend": 'new ArrayList<>(List.of("Чай", "Кофе", "Какао", "Морс"))'}],
        intro="Вы с другом собираете общий плейлист для поездки. Твои песни записаны в список `mine`, песни друга — "
              "в список `friend`. Песни должны идти по очереди: твоя, его, твоя, его… Когда в одном списке песни "
              "закончатся, оставшиеся песни другого идут подряд.",
        steps=["Создай пустой список `List<String> playlist = new ArrayList<>();`.",
               "Сделай цикл по номерам `i` от 0, который продолжается, пока `i` меньше размера хотя бы одного из списков. "
               "На каждом шаге добавь в `playlist` песню `mine.get(i)`, если в `mine` есть элемент с номером `i`, "
               "а затем песню `friend.get(i)`, если такой элемент есть в `friend`.",
               "Выведи `playlist` командой `System.out.println(playlist);`.",
               "Последней строкой выведи строку вида `Всего песен: 7` — размер плейлиста."],
        hint="Элемент с номером `i` есть в списке, только если `i < список.size()`. Проверяй это перед каждым `get`, "
             "иначе программа остановится с ошибкой `IndexOutOfBoundsException`.",
        solution="List<String> playlist = new ArrayList<>();\nfor (int i = 0; i < mine.size() || i < friend.size(); i++) {\n"
                 "    if (i < mine.size()) {\n        playlist.add(mine.get(i));\n    }\n"
                 "    if (i < friend.size()) {\n        playlist.add(friend.get(i));\n    }\n}\n"
                 'System.out.println(playlist);\nSystem.out.println("Всего песен: " + playlist.size());',
        wrong=[("цикл идёт только до конца короткого списка — песни из длинного теряются",
                "List<String> playlist = new ArrayList<>();\nfor (int i = 0; i < Math.min(mine.size(), friend.size()); i++) {\n"
                "    playlist.add(mine.get(i));\n    playlist.add(friend.get(i));\n}\n"
                'System.out.println(playlist);\nSystem.out.println("Всего песен: " + playlist.size());'),
               ("сначала все свои песни, потом все песни друга — без чередования",
                "List<String> playlist = new ArrayList<>();\nfor (String song : mine) {\n    playlist.add(song);\n}\n"
                "for (String song : friend) {\n    playlist.add(song);\n}\n"
                'System.out.println(playlist);\nSystem.out.println("Всего песен: " + playlist.size());')],
        constructs=["for", "if"],
    ),
]
