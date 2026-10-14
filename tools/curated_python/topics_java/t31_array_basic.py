"""ARRAY_BASIC — «Массивы» (Java): длина массива (.length), последний элемент через длину, создание массива
`new int[n]` и заполнение его в цикле. Taught before: everything up to array indexing (conditions, switch, for,
accumulator, while, break, elements by index). Not yet: own methods; the for-each loop is the next topic, so loops
here go over indexes."""
from java_tasks import JavaOutputTask

SKILL = "ARRAY_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ab-class-list", title="Список класса",
        given=[("String[]", "students")],
        variants=[{"students": '{"Aliev", "Belova", "Dyakov", "Galkina", "Voronin"}'},
                  {"students": '{"Andreeva", "Borisov", "Ershova", "Ilina", "Zaytsev", "Zhukov"}'},
                  {"students": '{"Karpov", "Lebedeva", "Morozov", "Nosova"}'}],
        hidden=[{"students": '{"Orlov", "Petrova", "Rudnev"}'},
                {"students": '{"Ageev", "Bykova", "Egorov", "Guseva", "Isaeva", "Vlasov", "Zharova", "Zotov"}'},
                {"students": '{"Yakovlev"}'},
                {"students": '{"Sidorova", "Titov"}'}],
        intro="Классный руководитель записал фамилии учеников по алфавиту в массив `students`. Ему нужно узнать, "
              "сколько в классе учеников и кто стоит в списке последним.",
        steps=["Выведи строку `Students on the list: …` — сколько элементов в массиве `students`.",
               "Следующей строкой выведи `Last on the list: …` — последний элемент массива.",
               "Учеников может быть больше или меньше, чем в заготовке, поэтому не считай их вручную: и количество, "
               "и индекс последнего элемента получи из длины массива."],
        hint="Длину массива даёт `students.length` (без скобок: это не метод). Индексы начинаются с 0, "
             "поэтому у последнего элемента индекс на единицу меньше длины.",
        solution='System.out.println("Students on the list: " + students.length);\n'
                 'System.out.println("Last on the list: " + students[students.length - 1]);',
        wrong=[("путает количество элементов с последним индексом: учеников получается на одного меньше",
                'System.out.println("Students on the list: " + (students.length - 1));\n'
                'System.out.println("Last on the list: " + students[students.length - 1]);'),
               ("посчитал учеников в примере вручную и вывел готовое число",
                'System.out.println("Students on the list: 5");\n'
                'System.out.println("Last on the list: " + students[students.length - 1]);')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ab-price-table", title="Табличка с ценами",
        given=[("int", "price"), ("int", "max")],
        variants=[{"price": "70", "max": "4"}, {"price": "85", "max": "5"}, {"price": "120", "max": "3"}],
        hidden=[{"price": "50", "max": "6"}, {"price": "99", "max": "1"}, {"price": "200", "max": "2"},
                {"price": "65", "max": "7"}],
        intro="Продавец мороженого хочет повесить табличку с ценами: сколько стоят одна порция, две и так далее — "
              "до {max} порций. Одна порция стоит {price} руб. Цена порции записана в поле `price`, а самое большое число порций — в поле `max`.",
        steps=["Создай массив `int[] totals` длиной `max` — по одному элементу на каждую строку таблички.",
               "Заполни его циклом `for`: в элемент с индексом `i` запиши, сколько стоят `i + 1` порций.",
               "Вторым циклом `for` пройди по массиву `totals` и для каждого элемента выведи строку вида "
               "`1 pcs: {price} rub` — сначала число порций, потом их цена."],
        hint="Новый массив создают так: `new int[max]` — сразу после создания все его элементы равны 0. "
             "В элементе с индексом 0 хранится цена одной порции, с индексом 1 — двух: число порций на 1 больше индекса.",
        solution='int[] totals = new int[max];\nfor (int i = 0; i < totals.length; i++) {\n    totals[i] = price * (i + 1);\n}\n'
                 'for (int i = 0; i < totals.length; i++) {\n    System.out.println((i + 1) + " pcs: " + totals[i] + " rub");\n}',
        wrong=[("забыл прибавить 1: в первой строке оказывается цена нуля порций",
                'int[] totals = new int[max];\nfor (int i = 0; i < totals.length; i++) {\n    totals[i] = price * i;\n}\n'
                'for (int i = 0; i < totals.length; i++) {\n    System.out.println((i + 1) + " pcs: " + totals[i] + " rub");\n}'),
               ("второй цикл идёт до length - 1: последняя строка таблички пропадает",
                'int[] totals = new int[max];\nfor (int i = 0; i < totals.length; i++) {\n    totals[i] = price * (i + 1);\n}\n'
                'for (int i = 0; i < totals.length - 1; i++) {\n    System.out.println((i + 1) + " pcs: " + totals[i] + " rub");\n}')],
        constructs=["list", "for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ab-book-stack", title="Стопка учебников",
        given=[("String[]", "books")],
        variants=[{"books": '{"Algebra", "Physics", "History", "Biology"}'},
                  {"books": '{"Literature", "Chemistry", "Geography", "English", "Geometry"}'},
                  {"books": '{"Russian", "Computer Science", "Social Studies"}'}],
        hidden=[{"books": '{"Music", "Art"}'},
                {"books": '{"Atlas", "Dictionary", "Problem Book", "Dictation Book", "Reader", "Handbook"}'},
                {"books": '{"Encyclopedia"}'}],
        intro="Ты складывал учебники в стопку по одному в том порядке, в каком они записаны в массиве `books`: "
              "первый оказался в самом низу. Снимать учебники будут сверху, то есть в обратном порядке.",
        steps=["Создай новый массив `String[] order` такой же длины, как `books`.",
               "Заполни его циклом `for`: в `order[0]` должен попасть последний учебник из `books`, в `order[1]` — "
               "предпоследний и так далее.",
               "Вторым циклом выведи элементы `order` по одному в строке: номер (начиная с 1), точка, пробел и название, "
               "например `1. Physics`"],
        hint="Посмотри на пары индексов: `order[0]` берёт учебник с индексом `books.length - 1`, `order[1]` — "
             "с индексом `books.length - 2`. Как индекс в `books` зависит от `i`?",
        solution='String[] order = new String[books.length];\nfor (int i = 0; i < books.length; i++) {\n'
                 '    order[i] = books[books.length - 1 - i];\n}\nfor (int i = 0; i < order.length; i++) {\n'
                 '    System.out.println((i + 1) + ". " + order[i]);\n}',
        wrong=[("копирует учебники в том же порядке, не переворачивая",
                'String[] order = new String[books.length];\nfor (int i = 0; i < books.length; i++) {\n'
                '    order[i] = books[i];\n}\nfor (int i = 0; i < order.length; i++) {\n'
                '    System.out.println((i + 1) + ". " + order[i]);\n}'),
               ("нумерует строки с нуля",
                'String[] order = new String[books.length];\nfor (int i = 0; i < books.length; i++) {\n'
                '    order[i] = books[books.length - 1 - i];\n}\nfor (int i = 0; i < order.length; i++) {\n'
                '    System.out.println(i + ". " + order[i]);\n}')],
        constructs=["list", "for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ab-game-levels", title="Очки за уровни игры",
        given=[("int[]", "scores")],
        variants=[{"scores": "{820, 1050, 640, 1200, 910}"}, {"scores": "{400, 750, 1100}"},
                  {"scores": "{990, 350, 1500, 800, 720, 1340}"}],
        hidden=[{"scores": "{100, 200}"}, {"scores": "{500, 600, 700, 800, 900, 1000, 1100, 1200}"},
                {"scores": "{300, 300, 250, 410}"}],
        intro="Игра записывает, сколько очков Борис набрал на каждом пройденном уровне, в массив `scores`: "
              "первый уровень — первый элемент, последний пройденный — последний. Пройдено всегда хотя бы два уровня.",
        steps=["Выведи строку `Levels played: …` — сколько элементов в массиве.",
               "Следующей строкой выведи `Last level: …` — последний элемент массива.",
               "Затем выведи `Level before: …` — предпоследний элемент.",
               "Уровней может быть больше или меньше, чем в заготовке, поэтому индексы вычисляй через длину массива."],
        hint="Длину массива даёт `scores.length`. У последнего элемента индекс `scores.length - 1`, а у предпоследнего — "
             "ещё на единицу меньше. Следи, чтобы `- 1` оказался внутри квадратных скобок.",
        solution='System.out.println("Levels played: " + scores.length);\nSystem.out.println("Last level: " + scores[scores.length - 1]);\n'
                 'System.out.println("Level before: " + scores[scores.length - 2]);',
        wrong=[("перепутал последний и предпоследний: индексы length - 2 и length - 1 поменялись местами",
                'System.out.println("Levels played: " + scores.length);\nSystem.out.println("Last level: " + scores[scores.length - 2]);\n'
                'System.out.println("Level before: " + scores[scores.length - 1]);'),
               ("- 1 вне скобок: вычитает единицу из очков, а не из индекса",
                'System.out.println("Levels played: " + scores.length);\nSystem.out.println("Last level: " + scores[scores.length - 1]);\n'
                'System.out.println("Level before: " + (scores[scores.length - 1] - 1));')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ab-garland", title="Гирлянда на ёлку",
        given=[("int", "bulbs")],
        variants=[{"bulbs": "5"}, {"bulbs": "4"}, {"bulbs": "7"}],
        hidden=[{"bulbs": "1"}, {"bulbs": "2"}, {"bulbs": "6"}, {"bulbs": "9"}],
        intro="Аня собирает гирлянду из {bulbs} лампочек (поле `bulbs`). Цвета чередуются: первая лампочка красная, "
              "вторая зелёная, третья снова красная и так далее.",
        steps=["Создай массив `String[] colors` длиной `bulbs`.",
               "Заполни его циклом `for` по индексам: если индекс чётный, запиши в элемент `red`, иначе — `green`.",
               "Вторым циклом выведи все лампочки по одной в строке: `Bulb 1: red`, `Bulb 2: green` и так далее "
               "(номер лампочки на 1 больше индекса).",
               "После цикла выведи `Last bulb: …` — цвет последнего элемента массива."],
        hint="Новый массив строк создают так: `new String[bulbs]`. Индекс 0 чётный — это первая, красная лампочка. "
             "Чётность проверяет `i % 2 == 0`.",
        solution='String[] colors = new String[bulbs];\nfor (int i = 0; i < colors.length; i++) {\n    if (i % 2 == 0) {\n'
                 '        colors[i] = "red";\n    } else {\n        colors[i] = "green";\n    }\n}\n'
                 'for (int i = 0; i < colors.length; i++) {\n    System.out.println("Bulb " + (i + 1) + ": " + colors[i]);\n}\n'
                 'System.out.println("Last bulb: " + colors[colors.length - 1]);',
        wrong=[("цвета перепутаны: первая лампочка получается зелёной",
                'String[] colors = new String[bulbs];\nfor (int i = 0; i < colors.length; i++) {\n    if (i % 2 == 1) {\n'
                '        colors[i] = "red";\n    } else {\n        colors[i] = "green";\n    }\n}\n'
                'for (int i = 0; i < colors.length; i++) {\n    System.out.println("Bulb " + (i + 1) + ": " + colors[i]);\n}\n'
                'System.out.println("Last bulb: " + colors[colors.length - 1]);'),
               ("в последней строке берёт первый элемент вместо последнего",
                'String[] colors = new String[bulbs];\nfor (int i = 0; i < colors.length; i++) {\n    if (i % 2 == 0) {\n'
                '        colors[i] = "red";\n    } else {\n        colors[i] = "green";\n    }\n}\n'
                'for (int i = 0; i < colors.length; i++) {\n    System.out.println("Bulb " + (i + 1) + ": " + colors[i]);\n}\n'
                'System.out.println("Last bulb: " + colors[0]);')],
        constructs=["list", "for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ab-bike-trip", title="Велопоход по дням",
        given=[("int[]", "km")],
        variants=[{"km": "{40, 55, 35, 60}"}, {"km": "{25, 30, 45}"}, {"km": "{50, 20, 70, 40, 30}"}],
        hidden=[{"km": "{12}"}, {"km": "{10, 10}"}, {"km": "{33, 41, 27, 50, 38, 61}"}, {"km": "{5, 100, 1}"}],
        intro="Вера ездила в велопоход. Сколько километров она проезжала в каждый день, записано в массив `km` "
              "по порядку дней. Вера хочет видеть, сколько всего проехано к концу каждого дня.",
        steps=["Создай массив `int[] passed` такой же длины, как `km`.",
               "Положи в `passed[0]` значение `km[0]`, а остальные элементы заполни циклом `for`, начиная с индекса 1: "
               "`passed[i]` — это всё, что проехано к концу прошлого дня, плюс `km[i]`.",
               "Вторым циклом выведи для каждого дня строку `After day …: … km` (номер дня на 1 больше индекса).",
               "После цикла выведи `Average: … km per day` — последний элемент `passed`, делённый нацело на число дней."],
        hint="Сколько проехано к концу прошлого дня, уже лежит в `passed[i - 1]`. А последний элемент `passed` — "
             "это весь путь за поход, его индекс `passed.length - 1`.",
        solution='int[] passed = new int[km.length];\npassed[0] = km[0];\nfor (int i = 1; i < km.length; i++) {\n'
                 '    passed[i] = passed[i - 1] + km[i];\n}\nfor (int i = 0; i < passed.length; i++) {\n'
                 '    System.out.println("After day " + (i + 1) + ": " + passed[i] + " km");\n}\n'
                 'System.out.println("Average: " + passed[passed.length - 1] / passed.length + " km per day");',
        wrong=[("складывает только два соседних дня, а не всё, что проехано раньше",
                'int[] passed = new int[km.length];\npassed[0] = km[0];\nfor (int i = 1; i < km.length; i++) {\n'
                '    passed[i] = km[i - 1] + km[i];\n}\nfor (int i = 0; i < passed.length; i++) {\n'
                '    System.out.println("After day " + (i + 1) + ": " + passed[i] + " km");\n}\n'
                'System.out.println("Average: " + passed[passed.length - 1] / passed.length + " km per day");'),
               ("забыл заполнить passed[0]: в первый день получается 0 км",
                'int[] passed = new int[km.length];\nfor (int i = 1; i < km.length; i++) {\n'
                '    passed[i] = passed[i - 1] + km[i];\n}\nfor (int i = 0; i < passed.length; i++) {\n'
                '    System.out.println("After day " + (i + 1) + ": " + passed[i] + " km");\n}\n'
                'System.out.println("Average: " + passed[passed.length - 1] / passed.length + " km per day");')],
        constructs=["list", "for"],
    ),
]
