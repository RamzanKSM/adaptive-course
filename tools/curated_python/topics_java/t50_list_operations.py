"""LIST_OPERATIONS — «Операции со списком» (Java). Taught before: everything up to List, Set and Map. Here: remove by
index vs remove by value (the List<Integer> trap), add(index, e), set, contains, indexOf, Collections.sort on a copy,
subList, Collections.swap — and that indexes shift after an insertion or a removal."""
from java_tasks import JavaFunctionTask, JavaOutputTask

SKILL = "LIST_OPERATIONS"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-listops-retake", title="Пересдача двойки",
        given=[("List<Integer>", "marks"), ("int", "retake")],
        variants=[{"marks": "new ArrayList<>(List.of(5, 2, 4, 3, 2, 5))", "retake": "4"},
                  {"marks": "new ArrayList<>(List.of(5, 3, 4, 2, 4))", "retake": "3"},
                  {"marks": "new ArrayList<>(List.of(2, 3, 5, 5, 2, 4, 3))", "retake": "5"}],
        hidden=[{"marks": "new ArrayList<>(List.of(2, 2, 2))", "retake": "3"},
                {"marks": "new ArrayList<>(List.of(5, 4, 5))", "retake": "4"},
                {"marks": "new ArrayList<>(List.of(3, 2))", "retake": "5"},
                {"marks": "new ArrayList<>(List.of(4, 3, 3, 2, 5, 4))", "retake": "4"}],
        intro="В электронном журнале оценки ученика за четверть записаны в список `marks` по порядку. Ученик пересдал "
              "одну двойку: учитель убирает из журнала первую двойку, а новую оценку `retake` записывает в конец списка.",
        steps=["Убери из списка `marks` первую оценку 2 — именно число 2, а не элемент с номером 2. Если двоек в списке нет, "
               "список не меняется.",
               "Добавь оценку `retake` в конец списка.",
               "Выведи список `marks` командой `System.out.println(marks);`.",
               "Проверь методом `contains`, остались ли в списке двойки, и выведи `Still has twos` или `No more twos`."],
        hint="У списка два метода `remove`: по номеру — `remove(int index)` и по значению — `remove(Object o)`. "
             "Для `List<Integer>` вызов `marks.remove(2)` удалит элемент с номером 2. Чтобы Java выбрала удаление "
             "по значению, передай ей не число `int`, а объект `Integer`.",
        solution='marks.remove(Integer.valueOf(2));\nmarks.add(retake);\nSystem.out.println(marks);\nif (marks.contains(2)) {\n'
                 '    System.out.println("Still has twos");\n} else {\n    System.out.println("No more twos");\n}',
        wrong=[("marks.remove(2) удаляет элемент с номером 2, а не оценку 2",
                'marks.remove(2);\nmarks.add(retake);\nSystem.out.println(marks);\nif (marks.contains(2)) {\n'
                '    System.out.println("Still has twos");\n} else {\n    System.out.println("No more twos");\n}'),
               ("записывает новую оценку на место двойки, а не в конец списка",
                'marks.set(marks.indexOf(2), retake);\nSystem.out.println(marks);\nif (marks.contains(2)) {\n'
                '    System.out.println("Still has twos");\n} else {\n    System.out.println("No more twos");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-listops-judges", title="Оценки судей",
        given=[("List<Integer>", "scores")],
        variants=[{"scores": "new ArrayList<>(List.of(8, 6, 9, 7, 10, 7))"},
                  {"scores": "new ArrayList<>(List.of(5, 9, 6, 6, 8))"},
                  {"scores": "new ArrayList<>(List.of(9, 9, 10, 8, 9, 7, 9))"}],
        hidden=[{"scores": "new ArrayList<>(List.of(4, 10, 7))"},
                {"scores": "new ArrayList<>(List.of(6, 6, 6, 6))"},
                {"scores": "new ArrayList<>(List.of(1, 10, 2, 9, 3, 8, 4, 7))"},
                {"scores": "new ArrayList<>(List.of(10, 3, 5, 3, 10))"}],
        intro="На соревнованиях по гимнастике судьи ставят баллы от 1 до 10. Чтобы слишком строгий или слишком добрый "
              "судья не решил исход, самую низкую и самую высокую оценку отбрасывают, а остальные складывают. "
              "Оценки судей записаны в список `scores`.",
        steps=["Сделай копию списка `List<Integer> sorted = new ArrayList<>(scores);` и отсортируй её по возрастанию: "
               "`Collections.sort(sorted);`. Выведи `sorted` через `System.out.println`.",
               "Методом `subList` возьми из `sorted` все оценки, кроме первой (самой низкой) и последней (самой высокой), "
               "и выведи эту часть списка.",
               "Выведи строку вида `Score: 25` — сумму оценок из этой части."],
        hint="`subList(from, to)` берёт элементы с номерами от `from` включительно до `to` НЕ включительно. "
             "У последнего элемента номер `sorted.size() - 1` — его и нужно не включить.",
        solution="List<Integer> sorted = new ArrayList<>(scores);\nCollections.sort(sorted);\nSystem.out.println(sorted);\n"
                 "List<Integer> middle = sorted.subList(1, sorted.size() - 1);\nSystem.out.println(middle);\n"
                 'int total = 0;\nfor (int s : middle) {\n    total += s;\n}\nSystem.out.println("Score: " + total);',
        wrong=[("берёт subList из исходного списка — отбрасывает первого и последнего судью, а не крайние оценки",
                "List<Integer> sorted = new ArrayList<>(scores);\nCollections.sort(sorted);\nSystem.out.println(sorted);\n"
                "List<Integer> middle = scores.subList(1, scores.size() - 1);\nSystem.out.println(middle);\n"
                'int total = 0;\nfor (int s : middle) {\n    total += s;\n}\nSystem.out.println("Score: " + total);'),
               ("считает конец subList включительно — отбрасывает ещё и предпоследнюю оценку",
                "List<Integer> sorted = new ArrayList<>(scores);\nCollections.sort(sorted);\nSystem.out.println(sorted);\n"
                "List<Integer> middle = sorted.subList(1, sorted.size() - 2);\nSystem.out.println(middle);\n"
                'int total = 0;\nfor (int s : middle) {\n    total += s;\n}\nSystem.out.println("Score: " + total);')],
        constructs=["for"],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=3, slug="java-listops-let-ahead", title="Пропустить вперёд на {k} места",
        function="letAhead",
        variants=[{"k": 2, "places": "2 места"}, {"k": 3, "places": "3 места"}, {"k": 4, "places": "4 места"}],
        intro="В очереди к кассе принято пропускать вперёд пожилых людей: такой покупатель переходит на {places} вперёд, "
              "а все, кого он обошёл, сдвигаются на одно место назад. Очередь — это список имён: первым в списке стоит тот, "
              "кто подойдёт к кассе следующим.",
        steps=["Напиши метод `static List<String> letAhead(List<String> queue, String name)`, который возвращает "
               "очередь после того, как покупатель `name` перешёл на {places} вперёд.",
               "Найди место покупателя методом `indexOf`. Если его нет в очереди, верни очередь без изменений.",
               "Убери покупателя с его места и вставь на {k} позиции ближе к началу методом `add(index, name)`. "
               "Если перед ним меньше {k} человек, он становится первым.",
               "Остальные люди сохраняют свой порядок друг относительно друга."],
        hint="После `remove` все, кто стоял за покупателем, сдвигаются на одно место к началу, а после `add` — на одно "
             "место назад. Поэтому важно, что делать раньше: убрать покупателя или вставить его на новое место.",
        starter="import java.util.*;\n\npublic class Solution {{\n"
                "    static List<String> letAhead(List<String> queue, String name) {{\n"
                "        // Напиши решение здесь\n        return queue;\n    }}\n}}\n",
        solution="import java.util.*;\n\npublic class Solution {{\n"
                 "    static List<String> letAhead(List<String> queue, String name) {{\n"
                 "        int i = queue.indexOf(name);\n        if (i == -1) {{\n            return queue;\n        }}\n"
                 "        queue.remove(i);\n        queue.add(Math.max(0, i - {k}), name);\n        return queue;\n    }}\n}}\n",
        inputs=['new ArrayList<>(List.of("Anya", "Boris", "Vika", "Gosha", "Dasha")), "Gosha"',
                'new ArrayList<>(List.of("Ulyana", "Fedor", "Chulpan", "Shamil", "Elya", "Yura", "Yana")), "Yura"',
                'new ArrayList<>(List.of("Egor", "Zhenya", "Zina")), "Zina"',
                'new ArrayList<>(List.of("Ira", "Kirill", "Lena", "Mark")), "Kirill"',
                'new ArrayList<>(List.of("Nina", "Oleg")), "Nina"',
                'new ArrayList<>(List.of("Petya", "Rita", "Sasha")), "Tanya"',
                'new ArrayList<>(List.of("Vera")), "Vera"',
                'new ArrayList<>(List.of("Arseny", "Bella", "Vlad", "Galya", "Dan", "Eva")), "Eva"'],
        wrong=[("сначала вставляет, потом удаляет по старому номеру — номера уже сдвинулись, и из очереди уходит другой человек",
                "import java.util.*;\n\npublic class Solution {{\n"
                "    static List<String> letAhead(List<String> queue, String name) {{\n"
                "        int i = queue.indexOf(name);\n        if (i == -1) {{\n            return queue;\n        }}\n"
                "        queue.add(Math.max(0, i - {k}), name);\n        queue.remove(i);\n        return queue;\n    }}\n}}\n"),
               ("меняет местами с тем, кто стоял на k мест впереди, — остальные не сдвигаются",
                "import java.util.*;\n\npublic class Solution {{\n"
                "    static List<String> letAhead(List<String> queue, String name) {{\n"
                "        int i = queue.indexOf(name);\n        if (i == -1) {{\n            return queue;\n        }}\n"
                "        Collections.swap(queue, i, Math.max(0, i - {k}));\n        return queue;\n    }}\n}}\n")],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-listops-fix-name", title="Опечатка в списке класса",
        given=[("List<String>", "pupils"), ("String", "typo"), ("String", "fixed")],
        variants=[{"pupils": 'new ArrayList<>(List.of("Anya", "Brois", "Vika", "Gleb"))', "typo": '"Brois"', "fixed": '"Boris"'},
                  {"pupils": 'new ArrayList<>(List.of("Dima", "Egor", "Zhenya"))', "typo": '"Ivna"', "fixed": '"Ivan"'},
                  {"pupils": 'new ArrayList<>(List.of("Kira", "Lena", "Mark", "Nnia", "Olya"))', "typo": '"Nnia"', "fixed": '"Nina"'}],
        hidden=[{"pupils": 'new ArrayList<>(List.of("Petay"))', "typo": '"Petay"', "fixed": '"Petya"'},
                {"pupils": 'new ArrayList<>(List.of("Rita", "Sasha"))', "typo": '"Tima"', "fixed": '"Tim"'},
                {"pupils": 'new ArrayList<>(List.of("Ulyana", "Fedya", "Yana", "Sasha", "Rma"))', "typo": '"Rma"', "fixed": '"Roma"'},
                {"pupils": 'new ArrayList<>(List.of("Zoya", "Gosha"))', "typo": '"Zoya"', "fixed": '"Zoe"'}],
        intro="Учительница заметила опечатку в списке класса `pupils`: имя `typo` написано неправильно, а должно быть "
              "`fixed`. Исправленное имя должно остаться на том же месте списка. Может оказаться и так, что такой "
              "опечатки в списке нет.",
        steps=["Найди место опечатки методом `indexOf(typo)` — он возвращает номер элемента или `-1`, если его нет.",
               "Если имя нашлось, замени его на `fixed` методом `set(index, fixed)` и выведи строку вида "
               "`Fixed at place 2` — место в списке, считая с 1.",
               "Если не нашлось, выведи строку вида `Ivna not found` — с именем `typo`.",
               "Последней строкой выведи список командой `System.out.println(pupils);`."],
        hint="`set` заменяет элемент на месте, и длина списка не меняется, а `add` вставил бы ещё один элемент. "
             "Место для людей на 1 больше номера в списке.",
        solution='int index = pupils.indexOf(typo);\nif (index >= 0) {\n    pupils.set(index, fixed);\n'
                 '    System.out.println("Fixed at place " + (index + 1));\n} else {\n'
                 '    System.out.println(typo + " not found");\n}\nSystem.out.println(pupils);',
        wrong=[("вставляет исправленное имя через add — опечатка остаётся в списке",
                'int index = pupils.indexOf(typo);\nif (index >= 0) {\n    pupils.add(index, fixed);\n'
                '    System.out.println("Fixed at place " + (index + 1));\n} else {\n'
                '    System.out.println(typo + " not found");\n}\nSystem.out.println(pupils);'),
               ("печатает номер в списке, а не место — считает с нуля",
                'int index = pupils.indexOf(typo);\nif (index >= 0) {\n    pupils.set(index, fixed);\n'
                '    System.out.println("Fixed at place " + index);\n} else {\n'
                '    System.out.println(typo + " not found");\n}\nSystem.out.println(pupils);')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-listops-height-line", title="Строимся по росту",
        given=[("List<Integer>", "heights"), ("int", "newcomer")],
        variants=[{"heights": "new ArrayList<>(List.of(128, 131, 135, 140, 142))", "newcomer": "137"},
                  {"heights": "new ArrayList<>(List.of(150, 152, 152, 158))", "newcomer": "152"},
                  {"heights": "new ArrayList<>(List.of(119, 124, 126))", "newcomer": "115"}],
        hidden=[{"heights": "new ArrayList<>()", "newcomer": "130"},
                {"heights": "new ArrayList<>(List.of(140, 145))", "newcomer": "150"},
                {"heights": "new ArrayList<>(List.of(133, 133, 133))", "newcomer": "133"},
                {"heights": "new ArrayList<>(List.of(120, 125, 130, 135, 140, 145))", "newcomer": "131"}],
        intro="На физкультуре класс стоит в шеренге по росту — от низкого к высокому, рост в сантиметрах записан в "
              "список `heights`. Пришёл новенький ростом `newcomer` см. Он встаёт сразу за последним, кто не выше "
              "его, — остальные сдвигаются на одно место.",
        steps=["Найди место для новенького: заведи `int place = 0;` и циклом `while` увеличивай `place`, пока "
               "`place` меньше размера списка и `heights.get(place)` не больше `newcomer`.",
               "Вставь новенького на это место методом `heights.add(place, newcomer);` — все, кто стоял с этого "
               "места и дальше, сдвинутся вправо.",
               "Выведи список командой `System.out.println(heights);`.",
               "Последней строкой выведи строку вида `Newcomer stands at place 4` — его место в шеренге, считая с 1."],
        hint="Условие `place < heights.size()` проверяй первым: если новенький выше всех, цикл дойдёт до конца "
             "списка, и `add(heights.size(), ...)` просто поставит его последним.",
        solution="int place = 0;\nwhile (place < heights.size() && heights.get(place) <= newcomer) {\n    place++;\n}\n"
                 'heights.add(place, newcomer);\nSystem.out.println(heights);\n'
                 'System.out.println("Newcomer stands at place " + (place + 1));',
        wrong=[("сравнивает строго меньше — новенький встаёт перед ребятами такого же роста",
                "int place = 0;\nwhile (place < heights.size() && heights.get(place) < newcomer) {\n    place++;\n}\n"
                'heights.add(place, newcomer);\nSystem.out.println(heights);\n'
                'System.out.println("Newcomer stands at place " + (place + 1));'),
               ("заменяет ученика на найденном месте через set — один ученик пропадает из шеренги",
                "int place = 0;\nwhile (place < heights.size() && heights.get(place) <= newcomer) {\n    place++;\n}\n"
                'if (place < heights.size()) {\n    heights.set(place, newcomer);\n} else {\n    heights.add(newcomer);\n}\n'
                'System.out.println(heights);\nSystem.out.println("Newcomer stands at place " + (place + 1));')],
        constructs=["while"],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=3, slug="java-listops-short-songs", title="Убрать песни короче {limit} секунд",
        function="removeShort",
        variants=[{"limit": 60}, {"limit": 90}, {"limit": 120}],
        intro="В плейлисте попались обрывки песен. Плейлист — список длительностей песен в секундах, и из него "
              "нужно убрать все песни короче {limit} секунд, не меняя порядок остальных.",
        steps=["Напиши метод `static List<Integer> removeShort(List<Integer> songs)`, который убирает из самого списка "
               "`songs` все длительности меньше {limit} и возвращает этот же список.",
               "Удаляй по номеру методом `songs.remove(i)`. Песня ровно {limit} секунд остаётся.",
               "После удаления все элементы правее сдвигаются на одно место влево — сделай так, чтобы ни одна "
               "песня не была пропущена."],
        hint="Если удалить элемент с номером `i` и сразу перейти к `i + 1`, то элемент, который сдвинулся на место "
             "`i`, никто не проверит. Можно идти по списку с конца к началу — тогда сдвиг не мешает.",
        starter="import java.util.*;\n\npublic class Solution {{\n"
                "    static List<Integer> removeShort(List<Integer> songs) {{\n"
                "        // Напиши решение здесь\n        return songs;\n    }}\n}}\n",
        solution="import java.util.*;\n\npublic class Solution {{\n"
                 "    static List<Integer> removeShort(List<Integer> songs) {{\n"
                 "        for (int i = songs.size() - 1; i >= 0; i--) {{\n"
                 "            if (songs.get(i) < {limit}) {{\n                songs.remove(i);\n            }}\n        }}\n"
                 "        return songs;\n    }}\n}}\n",
        inputs=["new ArrayList<>(List.of(200, 45, 30, 180, 59, 61))",
                "new ArrayList<>(List.of(10, 20, 240, 15))",
                "new ArrayList<>(List.of(60, 90, 120, 119, 89, 59))",
                "new ArrayList<>(List.of(300, 250))",
                "new ArrayList<>(List.of(5, 6, 7))",
                "new ArrayList<>(List.of(100, 30, 40, 50, 150, 20, 25))",
                "new ArrayList<>()"],
        wrong=[("удаляет и идёт вперёд с i++ — песня, сдвинувшаяся на место удалённой, пропускается",
                "import java.util.*;\n\npublic class Solution {{\n"
                "    static List<Integer> removeShort(List<Integer> songs) {{\n"
                "        for (int i = 0; i < songs.size(); i++) {{\n"
                "            if (songs.get(i) < {limit}) {{\n                songs.remove(i);\n            }}\n        }}\n"
                "        return songs;\n    }}\n}}\n"),
               ("сравнивает через <= — удаляет и песни ровно на границе",
                "import java.util.*;\n\npublic class Solution {{\n"
                "    static List<Integer> removeShort(List<Integer> songs) {{\n"
                "        for (int i = songs.size() - 1; i >= 0; i--) {{\n"
                "            if (songs.get(i) <= {limit}) {{\n                songs.remove(i);\n            }}\n        }}\n"
                "        return songs;\n    }}\n}}\n")],
    ),
]
