"""ARRAY_BASIC — «Массивы» (Java): длина массива (.length), последний элемент через длину, создание массива
`new int[n]` и заполнение его в цикле. Taught before: everything up to array indexing (conditions, switch, for,
accumulator, while, break, elements by index). Not yet: own methods; the for-each loop is the next topic, so loops
here go over indexes."""
from java_tasks import JavaOutputTask

SKILL = "ARRAY_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ab-rt-train-cars", title="Вагоны поезда",
        given=[("int[]", "passengers")],
        variants=[{"passengers": "{34, 41, 28, 50, 37}"}, {"passengers": "{12, 30, 25}"},
                  {"passengers": "{45, 38, 52, 40, 36, 44, 29}"}],
        hidden=[{"passengers": "{20}"}, {"passengers": "{10, 15, 20, 25, 30, 35, 40, 45, 50}"},
                {"passengers": "{7, 8, 9}"}, {"passengers": "{60, 61, 62, 63, 64}"}],
        intro="Проводник записал, сколько пассажиров едет в каждом вагоне, в массив `passengers` — от головы поезда "
              "к хвосту. Вагонов всегда нечётное число, и начальник поезда хочет знать про первый, средний и последний.",
        steps=["Выведи строку `Cars: …` — сколько элементов в массиве.",
               "Выведи строку `First car: …` — первый элемент массива.",
               "Выведи строку `Middle car: …` — элемент с индексом `passengers.length / 2`.",
               "Выведи строку `Last car: …` — последний элемент массива.",
               "Вагонов может быть больше или меньше, чем в заготовке, поэтому индексы считай через длину массива."],
        hint="Длину массива даёт `passengers.length` (без скобок). Например, в поезде из 5 вагонов средний имеет "
             "индекс 5 / 2 = 2, а последний — индекс 4, на единицу меньше длины.",
        solution='System.out.println("Cars: " + passengers.length);\nSystem.out.println("First car: " + passengers[0]);\n'
                 'System.out.println("Middle car: " + passengers[passengers.length / 2]);\n'
                 'System.out.println("Last car: " + passengers[passengers.length - 1]);',
        wrong=[("для последнего вагона индекс length - 2: выводит предпоследний",
                'System.out.println("Cars: " + passengers.length);\nSystem.out.println("First car: " + passengers[0]);\n'
                'System.out.println("Middle car: " + passengers[passengers.length / 2]);\n'
                'System.out.println("Last car: " + passengers[passengers.length - 2]);'),
               ("средний вагон взят из примера по готовому индексу 2",
                'System.out.println("Cars: " + passengers.length);\nSystem.out.println("First car: " + passengers[0]);\n'
                'System.out.println("Middle car: " + passengers[2]);\n'
                'System.out.println("Last car: " + passengers[passengers.length - 1]);')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ab-rt-compartment-seats", title="Места в купе",
        given=[("int", "compartments")],
        variants=[{"compartments": "4"}, {"compartments": "6"}, {"compartments": "3"}],
        hidden=[{"compartments": "1"}, {"compartments": "2"}, {"compartments": "9"}, {"compartments": "5"}],
        intro="В купейном вагоне {compartments} купе (поле `compartments`), в каждом по 4 места. Места нумеруются "
              "подряд: в первом купе места 1–4, во втором 5–8 и так далее. Нужно напечатать табличку для проводника.",
        steps=["Создай массив `int[] firstSeat` длиной `compartments` — по одному элементу на купе.",
               "Заполни его циклом `for`: в элемент с индексом `i` запиши номер первого места в купе — `i * 4 + 1`.",
               "Вторым циклом `for` пройди по массиву и для каждого купе выведи строку вида `Compartment 1: seats 1-4` — "
               "номер купе (на 1 больше индекса), первое и последнее место (первое плюс 3).",
               "После цикла выведи `Seats in the car: …` — последнее место последнего купе."],
        hint="Новый массив создают так: `new int[compartments]`. Последний элемент массива — с индексом "
             "`firstSeat.length - 1`, а последнее место в купе на 3 больше первого.",
        solution='int[] firstSeat = new int[compartments];\nfor (int i = 0; i < firstSeat.length; i++) {\n    firstSeat[i] = i * 4 + 1;\n}\n'
                 'for (int i = 0; i < firstSeat.length; i++) {\n'
                 '    System.out.println("Compartment " + (i + 1) + ": seats " + firstSeat[i] + "-" + (firstSeat[i] + 3));\n}\n'
                 'System.out.println("Seats in the car: " + (firstSeat[firstSeat.length - 1] + 3));',
        wrong=[("забыл + 1: места начинаются с 0",
                'int[] firstSeat = new int[compartments];\nfor (int i = 0; i < firstSeat.length; i++) {\n    firstSeat[i] = i * 4;\n}\n'
                'for (int i = 0; i < firstSeat.length; i++) {\n'
                '    System.out.println("Compartment " + (i + 1) + ": seats " + firstSeat[i] + "-" + (firstSeat[i] + 3));\n}\n'
                'System.out.println("Seats in the car: " + (firstSeat[firstSeat.length - 1] + 3));'),
               ("последнее место купе считает как первое плюс 4: купе по 5 мест",
                'int[] firstSeat = new int[compartments];\nfor (int i = 0; i < firstSeat.length; i++) {\n    firstSeat[i] = i * 4 + 1;\n}\n'
                'for (int i = 0; i < firstSeat.length; i++) {\n'
                '    System.out.println("Compartment " + (i + 1) + ": seats " + firstSeat[i] + "-" + (firstSeat[i] + 4));\n}\n'
                'System.out.println("Seats in the car: " + (firstSeat[firstSeat.length - 1] + 4));')],
        constructs=["list", "for"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ab-rt-duty-rotation", title="Карусель дежурств",
        given=[("String[]", "duty")],
        variants=[{"duty": '{"Anya", "Boris", "Vika", "Gosha"}'},
                  {"duty": '{"Oleg", "Mila", "Timur", "Sonya", "Egor"}'},
                  {"duty": '{"Katya", "Lyova", "Nina"}'}],
        hidden=[{"duty": '{"Ira", "Gleb"}'}, {"duty": '{"Max"}'},
                {"duty": '{"Eva", "Yana", "Lev", "Osya", "Fil", "Yulya"}'}],
        intro="В массиве `duty` записан порядок дежурств по классу на эту неделю: первый элемент дежурит в понедельник, "
              "второй — во вторник и так далее. На следующей неделе порядок сдвигается: все поднимаются на одно место "
              "вверх, а тот, кто был первым, уходит в конец списка.",
        steps=["Создай новый массив `String[] next` такой же длины, как `duty`.",
               "Заполни его циклом `for`: в `next[i]` положи элемент `duty` со следующим индексом, `i + 1`, а в последний "
               "элемент `next` — первый элемент `duty`.",
               "Вторым циклом выведи элементы `next` по одному в строке: номер (начиная с 1), точка, пробел и имя, "
               "например `1. Boris`."],
        hint="Индекс `i + 1` существует для всех элементов, кроме последнего. Поэтому цикл заполнения можно вести до "
             "`duty.length - 1`, а последний элемент `next[next.length - 1]` заполнить отдельно, после цикла.",
        solution='String[] next = new String[duty.length];\nfor (int i = 0; i < duty.length - 1; i++) {\n    next[i] = duty[i + 1];\n}\n'
                 'next[next.length - 1] = duty[0];\nfor (int i = 0; i < next.length; i++) {\n'
                 '    System.out.println((i + 1) + ". " + next[i]);\n}',
        wrong=[("последний элемент заполнен последним, а не первым: первый дежурный пропадает",
                'String[] next = new String[duty.length];\nfor (int i = 0; i < duty.length - 1; i++) {\n    next[i] = duty[i + 1];\n}\n'
                'next[next.length - 1] = duty[duty.length - 1];\nfor (int i = 0; i < next.length; i++) {\n'
                '    System.out.println((i + 1) + ". " + next[i]);\n}'),
               ("сдвигает в другую сторону: последний дежурный становится первым",
                'String[] next = new String[duty.length];\nfor (int i = 1; i < duty.length; i++) {\n    next[i] = duty[i - 1];\n}\n'
                'next[0] = duty[duty.length - 1];\nfor (int i = 0; i < next.length; i++) {\n'
                '    System.out.println((i + 1) + ". " + next[i]);\n}')],
        constructs=["list", "for"],
    ),
]
