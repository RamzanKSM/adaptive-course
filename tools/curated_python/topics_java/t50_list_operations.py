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
               "Проверь методом `contains`, остались ли в списке двойки, и выведи `Двойки ещё есть` или `Двоек больше нет`."],
        hint="У списка два метода `remove`: по номеру — `remove(int index)` и по значению — `remove(Object o)`. "
             "Для `List<Integer>` вызов `marks.remove(2)` удалит элемент с номером 2. Чтобы Java выбрала удаление "
             "по значению, передай ей не число `int`, а объект `Integer`.",
        solution='marks.remove(Integer.valueOf(2));\nmarks.add(retake);\nSystem.out.println(marks);\nif (marks.contains(2)) {\n'
                 '    System.out.println("Двойки ещё есть");\n} else {\n    System.out.println("Двоек больше нет");\n}',
        wrong=[("marks.remove(2) удаляет элемент с номером 2, а не оценку 2",
                'marks.remove(2);\nmarks.add(retake);\nSystem.out.println(marks);\nif (marks.contains(2)) {\n'
                '    System.out.println("Двойки ещё есть");\n} else {\n    System.out.println("Двоек больше нет");\n}'),
               ("записывает новую оценку на место двойки, а не в конец списка",
                'marks.set(marks.indexOf(2), retake);\nSystem.out.println(marks);\nif (marks.contains(2)) {\n'
                '    System.out.println("Двойки ещё есть");\n} else {\n    System.out.println("Двоек больше нет");\n}')],
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
               "Выведи строку вида `Итог: 25` — сумму оценок из этой части."],
        hint="`subList(from, to)` берёт элементы с номерами от `from` включительно до `to` НЕ включительно. "
             "У последнего элемента номер `sorted.size() - 1` — его и нужно не включить.",
        solution="List<Integer> sorted = new ArrayList<>(scores);\nCollections.sort(sorted);\nSystem.out.println(sorted);\n"
                 "List<Integer> middle = sorted.subList(1, sorted.size() - 1);\nSystem.out.println(middle);\n"
                 'int total = 0;\nfor (int s : middle) {\n    total += s;\n}\nSystem.out.println("Итог: " + total);',
        wrong=[("берёт subList из исходного списка — отбрасывает первого и последнего судью, а не крайние оценки",
                "List<Integer> sorted = new ArrayList<>(scores);\nCollections.sort(sorted);\nSystem.out.println(sorted);\n"
                "List<Integer> middle = scores.subList(1, scores.size() - 1);\nSystem.out.println(middle);\n"
                'int total = 0;\nfor (int s : middle) {\n    total += s;\n}\nSystem.out.println("Итог: " + total);'),
               ("считает конец subList включительно — отбрасывает ещё и предпоследнюю оценку",
                "List<Integer> sorted = new ArrayList<>(scores);\nCollections.sort(sorted);\nSystem.out.println(sorted);\n"
                "List<Integer> middle = sorted.subList(1, sorted.size() - 2);\nSystem.out.println(middle);\n"
                'int total = 0;\nfor (int s : middle) {\n    total += s;\n}\nSystem.out.println("Итог: " + total);')],
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
               "Убери покупателя с его места и вставь на {k} позиции ближе к началу методом `add(номер, name)`. "
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
        inputs=['new ArrayList<>(List.of("Аня", "Борис", "Вика", "Гоша", "Даша")), "Гоша"',
                'new ArrayList<>(List.of("Ульяна", "Фёдор", "Чулпан", "Шамиль", "Эля", "Юра", "Яна")), "Юра"',
                'new ArrayList<>(List.of("Егор", "Женя", "Зина")), "Зина"',
                'new ArrayList<>(List.of("Ира", "Кирилл", "Лена", "Марк")), "Кирилл"',
                'new ArrayList<>(List.of("Нина", "Олег")), "Нина"',
                'new ArrayList<>(List.of("Петя", "Рита", "Саша")), "Таня"',
                'new ArrayList<>(List.of("Вера")), "Вера"',
                'new ArrayList<>(List.of("Арсений", "Белла", "Влад", "Галя", "Дан", "Ева")), "Ева"'],
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
]
