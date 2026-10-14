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
]
