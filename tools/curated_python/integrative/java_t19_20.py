"""Integrative tasks (the task of a topic's 3rd iteration), Java, topics 19–20: ARRAY_INDEXING «Индексы массива» and
ARRAY_BASIC «Массивы». Each family: the topic at the core plus 1–2 earlier topics doing real work, one value set,
about 4–5 minutes; hidden value sets hit every branch and boundary.

ARRAY_INDEXING (element by index, a number counted from 1 turned into an index, changing an element) is joined by
/ and if/else (humidity sensor), if/else with a comparison and a double average (re-taken test), switch with += -=
(warehouse operation). Not yet: .length, loops over an array, own methods — so the indexes come from the statement
or from given numbers.
ARRAY_BASIC (.length, new int[n] / new String[n] filled in a for loop over indexes, a second loop to print) is joined
by % and for (playlist queue on a circle), if/else with a comparison (temperature changes), / and % with if
(boxes on shelves). Not yet: for-each, a sum / count / minimum over an array (ARRAY_ITERATION), own methods.

Theme domains: weather station measurements, warehouse and inventory, music playlists, marks in a journal."""
import textwrap

from java_tasks import JavaOutputTask
from topics_java.t22_switch import uses_switch


def code(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


def swap(text: str, old: str, new: str) -> str:
    assert old in text, old
    return text.replace(old, new)


HUMIDITY = code("""
    int i = broken - 1;
    humidity[i] = (humidity[i - 1] + humidity[i + 1]) / 2;
    System.out.println("Fixed reading " + broken + ": " + humidity[i] + "%");
    System.out.println("Around: " + humidity[i - 1] + " " + humidity[i] + " " + humidity[i + 1]);
    if (humidity[i] >= 85) {
        System.out.println("Fog warning");
    } else {
        System.out.println("No fog");
    }
""")

RETAKE = code("""
    int i = work - 1;
    if (retake > marks[i]) {
        System.out.println("Work " + work + ": " + marks[i] + " -> " + retake);
        marks[i] = retake;
    } else {
        System.out.println("Work " + work + ": " + marks[i] + " stays");
    }
    double average = (marks[0] + marks[1] + marks[2] + marks[3]) / 4.0;
    System.out.println("Average: " + average);
""")

STOCK = code("""
    int i = item - 1;
    int before = boxes[i];
    switch (op) {
        case '+': boxes[i] += qty; break;
        case '-': boxes[i] -= qty; break;
        case '=': boxes[i] = qty; break;
    }
    System.out.println("Item " + item + ": " + before + " -> " + boxes[i]);
""")

QUEUE = code("""
    System.out.println("Now playing: " + songs[now - 1]);
    String[] queue = new String[count];
    for (int i = 0; i < queue.length; i++) {
        queue[i] = songs[(now + i) % songs.length];
    }
    for (int i = 0; i < queue.length; i++) {
        System.out.println((i + 1) + ". " + queue[i]);
    }
""")

TEMPS = code("""
    int[] change = new int[temps.length - 1];
    for (int i = 0; i < change.length; i++) {
        change[i] = temps[i + 1] - temps[i];
    }
    for (int i = 0; i < change.length; i++) {
        if (change[i] > 0) {
            System.out.println("Day " + (i + 2) + ": +" + change[i]);
        } else {
            System.out.println("Day " + (i + 2) + ": " + change[i]);
        }
    }
""")

SHELVES = code("""
    int[] onShelf = new int[shelves];
    for (int i = 0; i < onShelf.length; i++) {
        onShelf[i] = boxes / shelves;
        if (i < boxes % shelves) {
            onShelf[i]++;
        }
    }
    for (int i = 0; i < onShelf.length; i++) {
        System.out.println("Shelf " + (i + 1) + ": " + onShelf[i]);
    }
""")

TASKS = [
    # ───────── ARRAY_INDEXING ─────────
    JavaOutputTask(
        skill="ARRAY_INDEXING", difficulty=3, slug="java-int-index-humidity", title="Сбой датчика влажности",
        given=[("int[]", "humidity"), ("int", "broken")],
        variants=[{"humidity": "{78, 81, 0, 88, 92, 90}", "broken": "3"}],
        hidden=[{"humidity": "{90, 0, 80, 75}", "broken": "2"},
                {"humidity": "{60, 64, 70, 99, 74}", "broken": "4"},
                {"humidity": "{88, 91, 5, 96, 94, 89, 86}", "broken": "3"},
                {"humidity": "{70, 0, 73}", "broken": "2"},
                {"humidity": "{50, 55, 61, 66, 72, 100, 86, 80}", "broken": "6"},
                {"humidity": "{85, 86, 120, 87, 90}", "broken": "3"}],
        intro="Метеостанция каждый час записывает влажность воздуха в процентах — замеры лежат в массиве `humidity` "
              "по порядку. Замер номер {broken} (поле `broken`, замеры нумеруются с 1) датчик записал со сбоем, и его "
              "заменяют средним двух соседних замеров. Сбойный замер никогда не бывает первым или последним. "
              "Если влажность не меньше 85%, станция предупреждает о тумане.",
        steps=["Индекс сбойного замера на 1 меньше его номера `broken`. Запиши в этот элемент массива среднее двух "
               "соседних замеров — того, что перед ним, и того, что после: их сумму, делённую нацело на 2.",
               "Выведи строку `Fixed reading {broken}: …%` — новое значение этого элемента (номер замера бери из "
               "поля `broken`).",
               "Выведи строку `Around: … … …` — через пробел замер перед исправленным, сам исправленный и замер "
               "после него. Все три числа бери из массива.",
               "Последней строкой выведи `Fog warning`, если исправленная влажность не меньше 85, иначе — `No fog`."],
        hint="Соседи элемента с индексом `i` — это `humidity[i - 1]` и `humidity[i + 1]`. Сумму возьми в скобки, иначе "
             "на 2 разделится только второе число. Деление целого на целое отбрасывает дробную часть: `169 / 2` равно `84`.",
        solution=HUMIDITY,
        wrong=[("сумма без скобок: на 2 делится только второй сосед",
                swap(HUMIDITY, "(humidity[i - 1] + humidity[i + 1]) / 2", "humidity[i - 1] + humidity[i + 1] / 2")),
               ("> 85 вместо >= 85: при влажности ровно 85% предупреждения нет",
                swap(HUMIDITY, "humidity[i] >= 85", "humidity[i] > 85")),
               ("считает среднее в отдельной переменной и не меняет массив: в строке Around остаётся сбойный замер",
                code("""
                    int i = broken - 1;
                    int fixed = (humidity[i - 1] + humidity[i + 1]) / 2;
                    System.out.println("Fixed reading " + broken + ": " + fixed + "%");
                    System.out.println("Around: " + humidity[i - 1] + " " + humidity[i] + " " + humidity[i + 1]);
                    if (fixed >= 85) {
                        System.out.println("Fog warning");
                    } else {
                        System.out.println("No fog");
                    }
                """)),
               ("использует номер замера как индекс: исправляет следующий замер",
                swap(HUMIDITY, "int i = broken - 1;", "int i = broken;"))],
        constructs=["list", "if"],
    ),
    JavaOutputTask(
        skill="ARRAY_INDEXING", difficulty=3, slug="java-int-index-retake", title="Пересдача контрольной",
        given=[("int[]", "marks"), ("int", "work"), ("int", "retake")],
        variants=[{"marks": "{4, 3, 5, 4}", "work": "2", "retake": "5"}],
        hidden=[{"marks": "{5, 4, 4, 3}", "work": "4", "retake": "3"},
                {"marks": "{2, 4, 3, 4}", "work": "1", "retake": "4"},
                {"marks": "{5, 5, 4, 5}", "work": "3", "retake": "3"},
                {"marks": "{3, 3, 2, 3}", "work": "3", "retake": "3"},
                {"marks": "{4, 4, 4, 2}", "work": "4", "retake": "5"}],
        intro="В журнале записаны оценки Вики за четыре контрольные в этой четверти — массив `marks` по порядку "
              "контрольных, в нём всегда ровно 4 оценки. Контрольную номер {work} (поле `work`, контрольные "
              "нумеруются с 1) Вика пересдала и получила {retake} (поле `retake`). В журнале остаётся лучшая из "
              "двух оценок.",
        steps=["Найди индекс пересданной контрольной: он на 1 меньше номера `work`.",
               "Если `retake` больше старой оценки, выведи строку `Work {work}: … -> …` (сначала старая оценка, потом "
               "новая) и запиши `retake` в этот элемент массива. Иначе выведи `Work {work}: … stays` со старой "
               "оценкой, а массив не меняй.",
               "Посчитай средний балл за четверть уже после пересдачи: сумму четырёх элементов массива раздели на "
               "`4.0` и сохрани в переменную типа `double`.",
               "Последней строкой выведи `Average: …`."],
        hint="Старую оценку выведи до того, как запишешь в элемент новую: после присваивания её в массиве уже нет. "
             "Сумма целых чисел, делённая на `4`, остаётся целой — дробная часть пропадёт, а делённая на `4.0` даёт "
             "дробное число.",
        solution=RETAKE,
        wrong=[(">= вместо >: при той же оценке пишет, что она изменилась",
                swap(RETAKE, "retake > marks[i]", "retake >= marks[i]")),
               ("делит на 4, а не на 4.0: дробная часть среднего пропадает",
                swap(RETAKE, "/ 4.0;", "/ 4;")),
               ("считает средний балл до пересдачи, по старым оценкам",
                code("""
                    int i = work - 1;
                    double average = (marks[0] + marks[1] + marks[2] + marks[3]) / 4.0;
                    if (retake > marks[i]) {
                        System.out.println("Work " + work + ": " + marks[i] + " -> " + retake);
                        marks[i] = retake;
                    } else {
                        System.out.println("Work " + work + ": " + marks[i] + " stays");
                    }
                    System.out.println("Average: " + average);
                """)),
               ("использует номер контрольной как индекс: сравнивает со следующей оценкой",
                swap(RETAKE, "int i = work - 1;", "int i = work;"))],
        constructs=["list", "if"],
    ),
    JavaOutputTask(
        skill="ARRAY_INDEXING", difficulty=3, slug="java-int-index-stock", title="Операция на складе",
        given=[("int[]", "boxes"), ("int", "item"), ("char", "op"), ("int", "qty")],
        variants=[{"boxes": "{12, 30, 7, 25, 18}", "item": "3", "op": "'+'", "qty": "20"}],
        hidden=[{"boxes": "{40, 15, 22}", "item": "2", "op": "'-'", "qty": "6"},
                {"boxes": "{5, 8, 13, 0}", "item": "4", "op": "'='", "qty": "10"},
                {"boxes": "{14, 9, 3}", "item": "1", "op": "'-'", "qty": "4"},
                {"boxes": "{21, 33, 16, 2, 11, 6}", "item": "5", "op": "'='", "qty": "9"},
                {"boxes": "{3, 50}", "item": "1", "op": "'+'", "qty": "6"},
                {"boxes": "{6, 18, 27}", "item": "3", "op": "'-'", "qty": "27"}],
        intro="На складе товары пронумерованы с 1, а сколько коробок каждого товара лежит на складе, записано в массив "
              "`boxes`. Кладовщик провёл одну операцию с товаром номер {item} (поле `item`): её код записан в поле "
              "`op`, а число коробок — в поле `qty`. Код `'+'` значит «привезли `qty` коробок», `'-'` — «увезли "
              "`qty` коробок», `'='` — «пересчитали, и коробок оказалось ровно `qty`». Увозят никогда не больше, "
              "чем есть.",
        steps=["Индекс товара на 1 меньше его номера `item`. Сохрани в переменную, сколько коробок этого товара было "
               "до операции.",
               "С помощью `switch` по полю `op` измени элемент массива: для `'+'` прибавь к нему `qty` через `+=`, "
               "для `'-'` вычти `qty` через `-=`, для `'='` запиши в него `qty`.",
               "Выведи строку `Item {item}: … -> …` — сколько коробок было до операции и сколько стало (новое число "
               "бери из массива, номер товара — из поля `item`)."],
        hint="В `case` символ пишут в одинарных кавычках: `case '+':`. Без `break` в конце ветки выполнение "
             "«проваливается» в следующую ветку. А «было» сохрани до `switch`: после него в элементе уже новое число.",
        solution=STOCK,
        wrong=[("забыл break после ветки '+': сразу выполняется и ветка '-', число не меняется",
                swap(STOCK, "case '+': boxes[i] += qty; break;", "case '+': boxes[i] += qty;")),
               ("для '=' прибавляет qty, а не записывает его",
                swap(STOCK, "case '=': boxes[i] = qty; break;", "case '=': boxes[i] += qty; break;")),
               ("не сохранил, сколько было: обе части строки берёт из массива уже после изменения",
                swap(STOCK, '": " + before + " -> "', '": " + boxes[i] + " -> "')),
               ("использует номер товара как индекс: меняет следующий товар",
                swap(STOCK, "int i = item - 1;", "int i = item;"))],
        constructs=["list"],
        checks=uses_switch("op"),
    ),
    # ───────── ARRAY_BASIC ─────────
    JavaOutputTask(
        skill="ARRAY_BASIC", difficulty=3, slug="java-int-array-queue", title="Очередь песен по кругу",
        given=[("String[]", "songs"), ("int", "now"), ("int", "count")],
        variants=[{"songs": '{"Sunny Day", "Night Drive", "Old Bridge", "Green Hills", "Last Train"}', "now": "4", "count": "3"}],
        hidden=[{"songs": '{"Rain Song", "City Lights", "Snow Walk"}', "now": "1", "count": "2"},
                {"songs": '{"Blue River", "Silver Bell", "Ocean Wave", "Quiet Street"}', "now": "4", "count": "1"},
                {"songs": '{"Morning Run", "Red Kite", "Warm Wind"}', "now": "2", "count": "5"},
                {"songs": '{"Long Road", "Pine Forest", "Star Map", "Late Bus", "First Snow", "Open Sea"}', "now": "3", "count": "4"},
                {"songs": '{"Two Hearts", "Paper Boat"}', "now": "2", "count": "3"},
                {"songs": '{"Big City", "Small Town", "Grey Sky", "Gold Sand"}', "now": "2", "count": "4"}],
        intro="Песни плейлиста записаны в массив `songs` по порядку. Сейчас играет песня номер {now} (поле `now`, "
              "песни нумеруются с 1). Плейлист закольцован: после последней песни снова играет первая. Плеер "
              "показывает очередь следующих песен — столько, сколько записано в поле `count` (сейчас {count}); "
              "если очередь длиннее плейлиста, песни в ней идут по кругу ещё раз.",
        steps=["Выведи строку `Now playing: …` — песню номер `now`.",
               "Создай массив `String[] queue` длиной `count`.",
               "Заполни его циклом `for`: `queue[0]` — песня сразу после текущей, `queue[1]` — следующая за ней и так "
               "далее. У текущей песни индекс `now - 1`, значит, у следующей — `now`. Чтобы после последней песни "
               "снова шла первая, индекс в `songs` бери как остаток от деления на `songs.length`.",
               "Вторым циклом выведи элементы `queue` по одному в строке: номер в очереди (с 1), точка, пробел и "
               "название, например `1. Last Train`."],
        hint="Для `queue[i]` нужна песня, которая стоит на `i` позиций дальше, чем `songs[now]`. Остаток от деления на "
             "длину плейлиста возвращает слишком большой индекс в начало: в плейлисте из 5 песен `5 % 5` равно 0, "
             "а `6 % 5` — 1.",
        solution=QUEUE,
        wrong=[("очередь начинается с текущей песни: индекс now - 1 вместо now",
                swap(QUEUE, "songs[(now + i) % songs.length]", "songs[(now - 1 + i) % songs.length]")),
               ("остаток от деления на songs.length - 1: последняя песня плейлиста в очередь не попадает",
                swap(QUEUE, "% songs.length]", "% (songs.length - 1)]")),
               ("нумерует очередь с нуля",
                swap(QUEUE, "System.out.println((i + 1) + \". \" + queue[i]);", "System.out.println(i + \". \" + queue[i]);"))],
        constructs=["list", "for"],
    ),
    JavaOutputTask(
        skill="ARRAY_BASIC", difficulty=3, slug="java-int-array-temps", title="Перепады температуры",
        given=[("int[]", "temps")],
        variants=[{"temps": "{12, 15, 13, 13, 17, 9}"}],
        hidden=[{"temps": "{5, 3}"},
                {"temps": "{-4, -1, -1, 2}"},
                {"temps": "{20, 21, 23, 26, 30, 35, 41, 48}"},
                {"temps": "{0, -3, -7}"},
                {"temps": "{7, 7, 8}"}],
        intro="Метеостанция каждое утро в 9:00 записывала температуру воздуха — значения лежат в массиве `temps` по "
              "порядку дней, первый элемент — день 1. Синоптику нужно знать, на сколько градусов менялась "
              "температура от каждого дня к следующему.",
        steps=["Создай массив `int[] change` на один элемент короче, чем `temps`: перемен между днями на одну меньше, "
               "чем самих дней.",
               "Заполни его циклом `for`: `change[i]` — температура дня с индексом `i + 1` минус температура дня "
               "с индексом `i`.",
               "Вторым циклом выведи для каждого элемента `change` строку `Day …: …` — номер дня, в который "
               "температура стала такой (у `change[0]` это день 2), и само изменение.",
               "Если изменение больше нуля, поставь перед числом знак `+`, например `Day 2: +3`. Отрицательное число "
               "выведи как есть (минус у него уже есть), а ноль — без знака: `Day 4: 0`."],
        hint="Новый массив создают через `new int[temps.length - 1]`. Тогда цикл до `change.length` не выйдет за край "
             "массива `temps`, даже когда берёт `temps[i + 1]`. Знак `+` — обычный текст, его приклеивают к строке "
             "перед числом.",
        solution=TEMPS,
        wrong=[(">= 0 вместо > 0: у нуля появляется знак +0",
                swap(TEMPS, "change[i] > 0", "change[i] >= 0")),
               ("вычитает наоборот: из вчерашней температуры сегодняшнюю, знаки перепутаны",
                swap(TEMPS, "temps[i + 1] - temps[i]", "temps[i] - temps[i + 1]")),
               ("номер дня на 1 больше индекса, а не на 2: изменения сдвинуты на день раньше",
                swap(TEMPS, "(i + 2)", "(i + 1)"))],
        constructs=["list", "for", "if"],
    ),
    JavaOutputTask(
        skill="ARRAY_BASIC", difficulty=3, slug="java-int-array-shelves", title="Коробки поровну по полкам",
        given=[("int", "boxes"), ("int", "shelves")],
        variants=[{"boxes": "27", "shelves": "5"}],
        hidden=[{"boxes": "20", "shelves": "4"},
                {"boxes": "7", "shelves": "3"},
                {"boxes": "3", "shelves": "5"},
                {"boxes": "30", "shelves": "7"},
                {"boxes": "9", "shelves": "1"},
                {"boxes": "11", "shelves": "6"}],
        intro="На склад привезли {boxes} коробок (поле `boxes`), их раскладывают по {shelves} полкам (поле `shelves`, "
              "полки нумеруются с 1). Коробки делят поровну, а лишние — те, что поровну не делятся, — кладут по одной "
              "на первые полки.",
        steps=["Создай массив `int[] onShelf` длиной `shelves` — по элементу на каждую полку.",
               "Заполни его циклом `for`: в каждый элемент запиши `boxes / shelves` — сколько коробок достаётся "
               "каждой полке поровну.",
               "Лишних коробок `boxes % shelves`. В том же цикле, если индекс полки меньше этого числа, прибавь "
               "к элементу ещё одну коробку.",
               "Вторым циклом выведи для каждой полки строку `Shelf …: …` — номер полки (на 1 больше индекса) "
               "и сколько на ней коробок."],
        hint="Лишняя коробка достаётся ровно `boxes % shelves` первым полкам — с индексами 0, 1 и так далее, пока "
             "индекс меньше остатка. Добавить коробку к элементу массива можно так же, как к переменной: `onShelf[i]++`.",
        solution=SHELVES,
        wrong=[("<= вместо <: лишнюю коробку получает на одну полку больше",
                swap(SHELVES, "i < boxes % shelves", "i <= boxes % shelves")),
               ("кладёт все лишние коробки на первую полку",
                code("""
                    int[] onShelf = new int[shelves];
                    for (int i = 0; i < onShelf.length; i++) {
                        onShelf[i] = boxes / shelves;
                    }
                    onShelf[0] += boxes % shelves;
                    for (int i = 0; i < onShelf.length; i++) {
                        System.out.println("Shelf " + (i + 1) + ": " + onShelf[i]);
                    }
                """)),
               ("нумерует полки с нуля",
                swap(SHELVES, '"Shelf " + (i + 1)', '"Shelf " + i'))],
        constructs=["list", "for", "if"],
    ),
]
