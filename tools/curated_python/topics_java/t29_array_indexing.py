"""ARRAY_INDEXING — «Индексы массива» (Java). Taught before: println, variables, arithmetic, types, String, / and %,
+= ++, conditions, switch, for, accumulator, while, loop termination. Here: an element by index, indexes from 0,
a number counted from 1 turned into an index, changing an element. Not yet: .length (ARRAY_BASIC), iterating an
array, own methods — so the tasks only read elements at indexes known from the statement or from given numbers."""
from java_tasks import JavaOutputTask

SKILL = "ARRAY_INDEXING"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ai-podium", title="Пьедестал почёта",
        given=[("String[]", "finish")],
        variants=[{"finish": '{"Anya", "Boris", "Vika", "Gosha", "Dasha"}'},
                  {"finish": '{"Oleg", "Mila", "Timur", "Sonya"}'},
                  {"finish": '{"Katya", "Lyova", "Nina", "Petya", "Rita", "Stas"}'}],
        hidden=[{"finish": '{"Ira", "Gleb", "Zoya"}'},
                {"finish": '{"Max", "Eva", "Yana", "Lev", "Osya", "Fil", "Yulya"}'},
                {"finish": '{"Dina", "Artyom", "Vera", "Grisha"}'}],
        intro="Лыжная гонка закончилась. В массиве `finish` записаны имена лыжников в том порядке, в котором они "
              "пересекли финиш: самый первый элемент — победитель. Трёх лучших награждают на пьедестале.",
        steps=["Выведи три строки: `Gold: …`, `Silver: …` и `Bronze: …` — вместо многоточия имена тех, кто финишировал "
               "первым, вторым и третьим.",
               "Бери имена из массива `finish` по индексу. Участников гонки может быть больше или меньше, чем в заготовке, "
               "но всегда не меньше трёх."],
        hint="Индексы элементов массива начинаются с нуля. Например, в массиве `{{\"red\", \"green\", \"blue\"}}` "
             "элемент с индексом 1 — это `\"green\"`, а вовсе не `\"red\"`.",
        solution='System.out.println("Gold: " + finish[0]);\nSystem.out.println("Silver: " + finish[1]);\n'
                 'System.out.println("Bronze: " + finish[2]);',
        wrong=[("считает индексы с единицы: золото получает второй лыжник",
                'System.out.println("Gold: " + finish[1]);\nSystem.out.println("Silver: " + finish[2]);\n'
                'System.out.println("Bronze: " + finish[3]);'),
               ("скопировал строку и не поправил индекс: бронзу получает серебряный призёр",
                'System.out.println("Gold: " + finish[0]);\nSystem.out.println("Silver: " + finish[1]);\n'
                'System.out.println("Bronze: " + finish[1]);')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ai-lessons", title="Какой сейчас урок",
        given=[("String[]", "lessons"), ("int", "number")],
        variants=[{"lessons": '{"Math", "Russian", "Physics", "History", "Music"}', "number": "3"},
                  {"lessons": '{"Biology", "Literature", "Algebra", "Chemistry", "PE", "English"}', "number": "2"},
                  {"lessons": '{"Geography", "Geometry", "Computer Science", "Social Studies"}', "number": "1"}],
        hidden=[{"lessons": '{"Drawing", "Reading", "Crafts"}', "number": "2"},
                {"lessons": '{"Algebra", "Physics", "Chemistry", "Biology", "History", "Art", "Music"}', "number": "6"},
                {"lessons": '{"English", "Math"}', "number": "1"},
                {"lessons": '{"Crafts", "Literature", "PE", "Math"}', "number": "3"}],
        intro="В массиве `lessons` записано расписание уроков на сегодня по порядку. Сейчас идёт урок номер {number} "
              "(поле `number`) — в школе уроки нумеруют с 1.",
        steps=["Выведи строку `Now: …` — название урока с номером `number`. Помни: номера уроков начинаются с 1, "
               "а индексы массива — с 0.",
               "Следующей строкой выведи `Next: …` — название следующего урока. Урок номер `number` никогда не бывает "
               "последним, так что следующий урок есть всегда.",
               "Индекс вычисляй из `number`: при другом номере урока программа должна вывести другие уроки."],
        hint="Первый урок лежит в массиве под индексом 0, второй — под индексом 1: индекс всегда на единицу меньше номера. "
             "А следующий урок стоит сразу за текущим, и его индекс на единицу больше.",
        solution='System.out.println("Now: " + lessons[number - 1]);\nSystem.out.println("Next: " + lessons[number]);',
        wrong=[("путает номер урока с индексом: печатает следующий урок вместо текущего",
                'System.out.println("Now: " + lessons[number]);\nSystem.out.println("Next: " + lessons[number + 1]);'),
               ("берёт индексы из примера, а не вычисляет их из number",
                'System.out.println("Now: " + lessons[2]);\nSystem.out.println("Next: " + lessons[3]);')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ai-relay-swap", title="Замена в эстафете",
        given=[("String[]", "team"), ("int", "a"), ("int", "b")],
        variants=[{"team": '{"Anya", "Boris", "Vika", "Gosha", "Dasha"}', "a": "2", "b": "4"},
                  {"team": '{"Oleg", "Mila", "Timur", "Sonya", "Egor"}', "a": "1", "b": "3"},
                  {"team": '{"Katya", "Lyova", "Nina", "Petya", "Rita", "Stas"}', "a": "3", "b": "5"}],
        hidden=[{"team": '{"Ira", "Gleb", "Zoya"}', "a": "1", "b": "3"},
                {"team": '{"Max", "Eva", "Yana", "Lev", "Osya", "Fil", "Yulya"}', "a": "4", "b": "7"},
                {"team": '{"Dina", "Artyom"}', "a": "1", "b": "2"},
                {"team": '{"Vera", "Grisha", "Danya", "Ksyusha"}', "a": "2", "b": "3"}],
        intro="Бегуны эстафетной команды записаны в массив `team` по порядку этапов: кто бежит первый этап, кто второй "
              "и так далее. Перед стартом тренер решил поменять местами бегунов на этапах {a} и {b} (поля `a` и `b`). "
              "Этапы нумеруются с 1.",
        steps=["Поменяй местами элементы массива `team` для этапов `a` и `b`. Индекс элемента на 1 меньше номера этапа.",
               "Чтобы при обмене не потерять ни одного имени, сначала сохрани один из элементов во вспомогательную "
               "переменную типа `String`.",
               "После обмена выведи три строки: `Stage {a}: …` и `Stage {b}: …` — кто теперь бежит эти этапы, "
               "а потом `First stage: …` — кто теперь бежит первым. Номера этапов в строках бери из `a` и `b`."],
        hint="Если сразу записать в элемент для этапа `a` бегуна с этапа `b`, прежнее имя пропадёт: в массиве окажутся "
             "два одинаковых имени. Поэтому сначала скопируй его в отдельную переменную, а уже потом меняй элементы.",
        solution='String temp = team[a - 1];\nteam[a - 1] = team[b - 1];\nteam[b - 1] = temp;\n'
                 'System.out.println("Stage " + a + ": " + team[a - 1]);\nSystem.out.println("Stage " + b + ": " + team[b - 1]);\n'
                 'System.out.println("First stage: " + team[0]);',
        wrong=[("меняет без вспомогательной переменной: одно имя теряется, а другое оказывается на двух этапах",
                'team[a - 1] = team[b - 1];\nteam[b - 1] = team[a - 1];\n'
                'System.out.println("Stage " + a + ": " + team[a - 1]);\nSystem.out.println("Stage " + b + ": " + team[b - 1]);\n'
                'System.out.println("First stage: " + team[0]);'),
               ("использует номер этапа как индекс: меняет не тех бегунов",
                'String temp = team[a];\nteam[a] = team[b];\nteam[b] = temp;\n'
                'System.out.println("Stage " + a + ": " + team[a]);\nSystem.out.println("Stage " + b + ": " + team[b]);\n'
                'System.out.println("First stage: " + team[0]);')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ai-week-weather", title="Погода за неделю",
        given=[("int[]", "temps")],
        variants=[{"temps": "{12, 14, 9, 11, 15, 18, 17}"}, {"temps": "{-3, -5, -2, 0, 1, -1, -4}"},
                  {"temps": "{22, 25, 27, 24, 21, 19, 26}"}],
        hidden=[{"temps": "{1, 2, 3, 4, 5, 6, 7}"}, {"temps": "{30, 10, 20, 0, -10, 5, 15}"},
                {"temps": "{8, 8, 8, 9, 8, 8, 8}"}],
        intro="Метеостанция записала дневную температуру за неделю в массив `temps`: первый элемент — понедельник, "
              "второй — вторник, и так до воскресенья. В массиве всегда ровно 7 чисел.",
        steps=["Выведи три строки: `Monday: … C`, `Friday: … C` и `Sunday: … C` — температуру в понедельник, пятницу "
               "и воскресенье.",
               "Следующей строкой выведи `Change: …` — температура в воскресенье минус температура в понедельник.",
               "Бери числа из массива `temps` по индексу."],
        hint="Индексы начинаются с нуля: понедельник — `temps[0]`. Посчитай по пальцам, какой индекс у пятницы и у воскресенья.",
        solution='System.out.println("Monday: " + temps[0] + " C");\nSystem.out.println("Friday: " + temps[4] + " C");\n'
                 'System.out.println("Sunday: " + temps[6] + " C");\nSystem.out.println("Change: " + (temps[6] - temps[0]));',
        wrong=[("для пятницы индекс 5: выводит субботу",
                'System.out.println("Monday: " + temps[0] + " C");\nSystem.out.println("Friday: " + temps[5] + " C");\n'
                'System.out.println("Sunday: " + temps[6] + " C");\nSystem.out.println("Change: " + (temps[6] - temps[0]));'),
               ("для понедельника индекс 1: выводит вторник",
                'System.out.println("Monday: " + temps[1] + " C");\nSystem.out.println("Friday: " + temps[4] + " C");\n'
                'System.out.println("Sunday: " + temps[6] + " C");\nSystem.out.println("Change: " + (temps[6] - temps[1]));')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ai-cafe-order", title="Заказ по номерам меню",
        given=[("int[]", "prices"), ("int", "first"), ("int", "second")],
        variants=[{"prices": "{250, 180, 320, 90, 150}", "first": "3", "second": "1"},
                  {"prices": "{120, 450, 300, 200, 80, 60}", "first": "2", "second": "5"},
                  {"prices": "{99, 199, 299, 399}", "first": "1", "second": "3"}],
        hidden=[{"prices": "{10, 20, 30}", "first": "2", "second": "2"},
                {"prices": "{500, 100, 700, 300, 900, 50, 40}", "first": "5", "second": "4"},
                {"prices": "{70, 80}", "first": "1", "second": "1"},
                {"prices": "{15, 25, 35, 45, 55}", "first": "4", "second": "2"}],
        intro="В меню кафе блюда пронумерованы с 1, а их цены в рублях записаны в массив `prices` по порядку. "
              "Гость заказал блюдо номер {first} (поле `first`) и блюдо номер {second} (поле `second`).",
        steps=["Выведи строку `Dish {first}: … rub` — цену первого заказанного блюда, и строку `Dish {second}: … rub` — "
               "цену второго. Номера блюд в строках бери из `first` и `second`.",
               "Последней строкой выведи `Total: … rub` — сумму двух цен.",
               "Индексы вычисляй из `first` и `second`: при других номерах программа должна вывести другие цены."],
        hint="Блюдо номер 1 лежит в массиве под индексом 0, поэтому индекс блюда — его номер минус 1. "
             "Сумму двух чисел в строке возьми в скобки, иначе числа склеятся.",
        solution='System.out.println("Dish " + first + ": " + prices[first - 1] + " rub");\n'
                 'System.out.println("Dish " + second + ": " + prices[second - 1] + " rub");\n'
                 'System.out.println("Total: " + (prices[first - 1] + prices[second - 1]) + " rub");',
        wrong=[("использует номер блюда как индекс: берёт цену следующего блюда",
                'System.out.println("Dish " + first + ": " + prices[first] + " rub");\n'
                'System.out.println("Dish " + second + ": " + prices[second] + " rub");\n'
                'System.out.println("Total: " + (prices[first] + prices[second]) + " rub");'),
               ("сумма без скобок: цены склеиваются в одну строку",
                'System.out.println("Dish " + first + ": " + prices[first - 1] + " rub");\n'
                'System.out.println("Dish " + second + ": " + prices[second - 1] + " rub");\n'
                'System.out.println("Total: " + prices[first - 1] + prices[second - 1] + " rub");')],
        constructs=["list"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ai-shelf-stock", title="Товар на полке",
        given=[("int[]", "stock"), ("int", "shelf"), ("int", "want")],
        variants=[{"stock": "{12, 5, 8, 20}", "shelf": "3", "want": "6"},
                  {"stock": "{7, 3, 15, 0, 9}", "shelf": "2", "want": "5"},
                  {"stock": "{30, 14, 6}", "shelf": "1", "want": "10"}],
        hidden=[{"stock": "{4, 9}", "shelf": "1", "want": "9"}, {"stock": "{4, 9, 2}", "shelf": "2", "want": "9"},
                {"stock": "{10, 0, 5, 1}", "shelf": "4", "want": "3"}, {"stock": "{8, 8, 8}", "shelf": "1", "want": "8"},
                {"stock": "{2, 6, 11, 3, 7}", "shelf": "5", "want": "1"}],
        intro="На складе полки пронумерованы с 1, а сколько коробок стоит на каждой полке, записано в массив `stock`. "
              "Покупатель хочет забрать {want} коробок (поле `want`) с полки номер {shelf} (поле `shelf`). "
              "Если на полке меньше коробок, он забирает всё, что есть.",
        steps=["Посчитай, сколько коробок покупатель заберёт: `want`, если на полке их не меньше, иначе — всё, что на полке.",
               "Уменьши элемент массива для этой полки на это число — массив должен измениться.",
               "Выведи три строки: `Sold: …`, `Left on shelf {shelf}: …` (сколько коробок теперь на этой полке, номер "
               "полки бери из `shelf`) и `Shelf 1 now: …` — сколько коробок теперь на первой полке склада."],
        hint="Индекс полки на 1 меньше её номера. Элемент массива меняется так же, как переменная: `stock[i] -= 3;`. "
             "Если покупатель брал с первой полки, в последней строке должно быть уже новое число.",
        solution='int sold;\nif (stock[shelf - 1] >= want) {\n    sold = want;\n} else {\n    sold = stock[shelf - 1];\n}\n'
                 'stock[shelf - 1] -= sold;\nSystem.out.println("Sold: " + sold);\n'
                 'System.out.println("Left on shelf " + shelf + ": " + stock[shelf - 1]);\nSystem.out.println("Shelf 1 now: " + stock[0]);',
        wrong=[("не проверяет, хватает ли коробок: на полке получается минус",
                'int sold = want;\nstock[shelf - 1] -= sold;\nSystem.out.println("Sold: " + sold);\n'
                'System.out.println("Left on shelf " + shelf + ": " + stock[shelf - 1]);\nSystem.out.println("Shelf 1 now: " + stock[0]);'),
               ("считает остаток в отдельной переменной и не меняет массив: первая полка не уменьшается",
                'int sold;\nif (stock[shelf - 1] >= want) {\n    sold = want;\n} else {\n    sold = stock[shelf - 1];\n}\n'
                'int left = stock[shelf - 1] - sold;\nSystem.out.println("Sold: " + sold);\n'
                'System.out.println("Left on shelf " + shelf + ": " + left);\nSystem.out.println("Shelf 1 now: " + stock[0]);')],
        constructs=["list", "if"],
    ),
]
