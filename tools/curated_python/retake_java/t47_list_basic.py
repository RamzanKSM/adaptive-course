"""LIST_BASIC — «Список List» (Java). Taught before: everything up to interfaces and super (conditions, loops, arrays,
static methods, classes). Here: List<…> and ArrayList, add, get, size, a for-each over a list, a new list built in a
loop, printing a list with println. Not yet: Set, Map, remove/indexOf/sort/subList (topic 50)."""
from java_tasks import JavaOutputTask

SKILL = "LIST_BASIC"

FARES = ("List<Integer> fares = new ArrayList<>();\nfor (int age : ages) {\n    if (age < 7) {\n        fares.add(0);\n"
         "    } else if (age >= 65) {\n        fares.add(fare / 2);\n    } else {\n        fares.add(fare);\n    }\n}\n"
         "System.out.println(fares);\nint total = 0;\nfor (int price : fares) {\n    total += price;\n}\n"
         'System.out.println("Total: " + total + " rub");')

PIGGY = ("List<Integer> balance = new ArrayList<>();\nint sum = 0;\nfor (int money : deposits) {\n    sum += money;\n"
         "    balance.add(sum);\n}\n"
         'System.out.println("Balance: " + balance);\nint week = 0;\nfor (int i = 0; i < balance.size(); i++) {\n'
         "    if (week == 0 && balance.get(i) >= target) {\n        week = i + 1;\n    }\n}\n"
         'if (week > 0) {\n    System.out.println("Target reached in week " + week);\n} else {\n'
         '    System.out.println("Not yet, " + (target - sum) + " rub to go");\n}')

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-list-rt-ticket-queue", title="Очередь в кассу",
        given=[("List<String>", "queue"), ("String", "me")],
        variants=[{"queue": 'new ArrayList<>(List.of("Anya", "Boris", "Vika"))', "me": '"Gleb"'},
                  {"queue": 'new ArrayList<>(List.of("Oleg", "Dima"))', "me": '"Zhenya"'},
                  {"queue": 'new ArrayList<>(List.of("Ira", "Kostya", "Nina", "Pavel", "Rita"))', "me": '"Sonya"'}],
        hidden=[{"queue": 'new ArrayList<>(List.of("Lev"))', "me": '"Mila"'},
                {"queue": 'new ArrayList<>(List.of("Yura", "Marat", "Alina", "Egor"))', "me": '"Fedya"'},
                {"queue": 'new ArrayList<>(List.of("Tanya", "Sasha"))', "me": '"Artem"'}],
        intro="В кинотеатре очередь в кассу. Кто в ней стоит, записано по порядку в список `queue`: первым в списке "
              "стоит тот, кто подойдёт к кассе следующим. Ты приходишь последним, твоё имя — в поле `me`.",
        steps=["Встань в конец очереди: добавь `me` в конец списка `queue` методом `add`.",
               "Выведи строку вида `In queue: 4` — сколько человек теперь в очереди (метод `size()`).",
               "Выведи строку вида `Next: Anya` — кто стоит первым. Элемент по номеру достаёт метод `get`.",
               "Выведи строку вида `Before me: Vika` — кто стоит прямо перед тобой, то есть предпоследним.",
               "Последней строкой выведи всю очередь командой `System.out.println(queue);`."],
        hint="Номера в списке начинаются с 0. Ты теперь последний, твой номер — `queue.size() - 1`, а тот, кто перед "
             "тобой, на единицу ближе к началу.",
        solution='queue.add(me);\nSystem.out.println("In queue: " + queue.size());\nSystem.out.println("Next: " + queue.get(0));\n'
                 'System.out.println("Before me: " + queue.get(queue.size() - 2));\nSystem.out.println(queue);',
        wrong=[("берёт последний элемент — перед тобой оказываешься ты сам",
                'queue.add(me);\nSystem.out.println("In queue: " + queue.size());\nSystem.out.println("Next: " + queue.get(0));\n'
                'System.out.println("Before me: " + queue.get(queue.size() - 1));\nSystem.out.println(queue);'),
               ("нумерует с единицы — следующим считает второго в очереди",
                'queue.add(me);\nSystem.out.println("In queue: " + queue.size());\nSystem.out.println("Next: " + queue.get(1));\n'
                'System.out.println("Before me: " + queue.get(queue.size() - 2));\nSystem.out.println(queue);')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-list-rt-bus-fares", title="Билеты на автобус",
        given=[("List<Integer>", "ages"), ("int", "fare")],
        variants=[{"ages": "new ArrayList<>(List.of(35, 5, 70, 12))", "fare": "60"},
                  {"ages": "new ArrayList<>(List.of(40, 38, 3))", "fare": "50"},
                  {"ages": "new ArrayList<>(List.of(66, 64, 7, 6, 19))", "fare": "80"}],
        hidden=[{"ages": "new ArrayList<>()", "fare": "60"},
                {"ages": "new ArrayList<>(List.of(65))", "fare": "90"},
                {"ages": "new ArrayList<>(List.of(7, 6, 64, 65, 30))", "fare": "40"},
                {"ages": "new ArrayList<>(List.of(1, 2))", "fare": "70"}],
        intro="Семья едет на автобусе. Возраст каждого записан в список `ages`, а обычный билет стоит `fare` руб. "
              "Дети младше 7 лет едут бесплатно, а пассажиры от 65 лет платят половину (целое деление).",
        steps=["Создай новый пустой список для цен билетов: `List<Integer> fares = new ArrayList<>();`.",
               "Пройди по списку `ages` циклом for-each. Для возраста меньше `7` добавь в `fares` число `0`, для возраста "
               "`65` и больше — `fare / 2`, для всех остальных — `fare`.",
               "Выведи список `fares` командой `System.out.println(fares);`.",
               "Последней строкой выведи сумму всех цен из `fares` в виде `Total: 150 rub`."],
        hint="Цены добавляй в `fares` в том же порядке, в котором идут пассажиры в `ages`, — тогда цена каждого стоит "
             "на том же месте, что и его возраст. Границы: семилетний платит полную цену, а 65-летний — половину.",
        solution=FARES,
        wrong=[("строгое сравнение с 65 — пассажир ровно 65 лет платит полную цену",
                FARES.replace("age >= 65", "age > 65")),
               ("детям до 7 лет тоже ставит полцены вместо бесплатного проезда",
                FARES.replace("fares.add(0);", "fares.add(fare / 2);"))],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-list-rt-piggy-bank", title="Копилка на велосипед",
        given=[("List<Integer>", "deposits"), ("int", "target")],
        variants=[{"deposits": "new ArrayList<>(List.of(500, 300, 700, 200))", "target": "1500"},
                  {"deposits": "new ArrayList<>(List.of(100, 250, 150))", "target": "1000"},
                  {"deposits": "new ArrayList<>(List.of(400, 400, 400, 400, 400))", "target": "1600"}],
        hidden=[{"deposits": "new ArrayList<>()", "target": "300"},
                {"deposits": "new ArrayList<>(List.of(1000))", "target": "1000"},
                {"deposits": "new ArrayList<>(List.of(200, 0, 300, 999))", "target": "500"},
                {"deposits": "new ArrayList<>(List.of(50, 60))", "target": "111"}],
        intro="Ты копишь на велосипед, который стоит `target` руб. Каждую неделю ты кладёшь в копилку какую-то сумму — "
              "суммы по порядку недель записаны в список `deposits`. Нужно узнать, сколько было в копилке после каждой "
              "недели и когда набралась нужная сумма.",
        steps=["Создай пустой список `List<Integer> balance = new ArrayList<>();` и переменную для суммы в копилке, "
               "равную 0. Пройди по `deposits` циклом for-each: прибавь очередной взнос к сумме и добавь новую сумму "
               "в `balance`.",
               "Выведи `Balance: ` и сразу за этим список `balance`, например `Balance: [500, 800, 1500, 1700]`.",
               "Найди первую неделю, после которой в копилке стало не меньше `target`. Недели считаются с 1: неделя "
               "элемента `balance.get(i)` — это `i + 1`.",
               "Если такая неделя есть, выведи строку вида `Target reached in week 3`, иначе — строку вида "
               "`Not yet, 200 rub to go`, где число — сколько ещё не хватает до `target`."],
        hint="В `balance` кладётся не сам взнос, а сумма всех взносов до этой недели включительно. Ищи первую подходящую "
             "неделю: когда она найдена, следующие недели её не заменяют.",
        solution=PIGGY,
        wrong=[("строгое сравнение — неделя, когда набралось ровно target, не засчитана",
                PIGGY.replace("balance.get(i) >= target", "balance.get(i) > target")),
               ("кладёт в balance сам взнос, а не накопленную сумму",
                PIGGY.replace("    balance.add(sum);\n", "    balance.add(money);\n")),
               ("запоминает последнюю подходящую неделю вместо первой",
                PIGGY.replace("week == 0 && balance.get(i) >= target", "balance.get(i) >= target"))],
        constructs=["for", "if"],
    ),
]
