"""LIST_OPERATIONS — «Операции со списком» (Java). Taught before: everything up to List, Set and Map. Here: remove by
index vs remove by value (the List<Integer> trap), add(index, e), set, contains, indexOf, Collections.sort on a copy,
subList, Collections.swap — and that indexes shift after an insertion or a removal."""
from java_tasks import JavaFunctionTask, JavaOutputTask

SKILL = "LIST_OPERATIONS"

PARKING = ('free.remove(Integer.valueOf(spot));\nSystem.out.println(free);\nSystem.out.println("Free spots: " + free.size());\n'
           'if (free.contains(1)) {\n    System.out.println("Spot 1 is free");\n} else {\n'
           '    System.out.println("Nearest free: " + free.get(0));\n}')

RACE = ('List<Integer> sorted = new ArrayList<>(times);\nCollections.sort(sorted);\n'
        'System.out.println("Podium: " + sorted.subList(0, 3));\nint best = sorted.get(0);\n'
        'System.out.println("Winner: runner " + (times.indexOf(best) + 1) + ", " + best + " sec");\n'
        'System.out.println("Start order: " + times);')

ROSTER_HEAD = "import java.util.*;\n\npublic class Solution {{\n    static List<String> nextWeek(List<String> duty) {{\n"
ROSTER_TAIL = "        return duty;\n    }}\n}}\n"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-listops-rt-parking-spot", title="Свободные места на парковке",
        given=[("List<Integer>", "free"), ("int", "spot")],
        variants=[{"free": "new ArrayList<>(List.of(2, 3, 5, 6, 8, 9))", "spot": "3"},
                  {"free": "new ArrayList<>(List.of(1, 2, 4, 5, 7))", "spot": "1"},
                  {"free": "new ArrayList<>(List.of(1, 3, 4, 6, 7, 8, 10))", "spot": "4"}],
        hidden=[{"free": "new ArrayList<>(List.of(4, 5, 6, 7, 8))", "spot": "2"},
                {"free": "new ArrayList<>(List.of(1, 2))", "spot": "2"},
                {"free": "new ArrayList<>(List.of(2, 3, 4, 5, 6))", "spot": "5"},
                {"free": "new ArrayList<>(List.of(1, 2, 3, 4, 5, 6, 7))", "spot": "6"}],
        intro="Список `free` хранит номера свободных мест на парковке по возрастанию. На место номер `spot` только что "
              "встала машина, и это место нужно убрать из списка свободных. Может быть и так, что охранник ошибся и "
              "такого номера среди свободных нет — тогда список не меняется.",
        steps=["Убери из списка `free` число `spot` — именно номер места, а не элемент с номером `spot`.",
               "Выведи список `free` командой `System.out.println(free);`.",
               "Выведи строку вида `Free spots: 5` — сколько мест осталось свободными.",
               "Если среди свободных есть место 1 (метод `contains`), выведи `Spot 1 is free`, иначе выведи строку вида "
               "`Nearest free: 2` — первый номер из списка."],
        hint="У списка чисел `free.remove(3)` убирает элемент с НОМЕРОМ 3. Чтобы убрать само число, передай объект: "
             "`free.remove(Integer.valueOf(spot))`.",
        solution=PARKING,
        wrong=[("удаляет по номеру элемента, а не по значению — со стоянки «уходит» другое место",
                PARKING.replace("free.remove(Integer.valueOf(spot));", "free.remove(spot);")),
               ("забыл убрать занятое место — список не изменился",
                PARKING.replace("free.remove(Integer.valueOf(spot));\n", ""))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-listops-rt-race-podium", title="Пьедестал забега",
        given=[("List<Integer>", "times")],
        variants=[{"times": "new ArrayList<>(List.of(65, 58, 71, 60, 62))"},
                  {"times": "new ArrayList<>(List.of(80, 77, 90))"},
                  {"times": "new ArrayList<>(List.of(55, 61, 49, 53, 70, 58))"}],
        hidden=[{"times": "new ArrayList<>(List.of(40, 41, 42))"},
                {"times": "new ArrayList<>(List.of(99, 88, 77, 66))"},
                {"times": "new ArrayList<>(List.of(70, 52, 64, 59, 51, 68, 75))"},
                {"times": "new ArrayList<>(List.of(63, 60, 61, 62))"}],
        intro="На школьном забеге на 400 метров записали время каждого бегуна в секундах. Список `times` идёт "
              "в порядке стартовых номеров: время бегуна номер 1 стоит первым, номер 2 — вторым и так далее. "
              "Все времена разные. Нужно узнать тройку лучших результатов и номер победителя.",
        steps=["Сделай копию списка `List<Integer> sorted = new ArrayList<>(times);` и отсортируй копию по возрастанию: "
               "`Collections.sort(sorted);`. Сам список `times` не сортируй — он ещё понадобится.",
               "Методом `subList` возьми из `sorted` первые три времени и выведи их в строке вида "
               "`Podium: [58, 60, 62]`.",
               "Лучшее время — первое в `sorted`. Найди его место в исходном списке `times` методом `indexOf` и выведи "
               "строку вида `Winner: runner 2, 58 sec` — стартовый номер (место в списке, считая с 1) и время.",
               "Последней строкой выведи `Start order: ` и сразу за этим список `times`."],
        hint="`subList(from, to)` берёт элементы с номера `from` включительно до `to` НЕ включительно. Если "
             "отсортировать сам `times`, исходный порядок пропадёт, и `indexOf` найдёт уже не стартовый номер.",
        solution=RACE,
        wrong=[("сортирует сам список times — номер победителя всегда 1",
                RACE.replace("List<Integer> sorted = new ArrayList<>(times);\nCollections.sort(sorted);",
                             "List<Integer> sorted = times;\nCollections.sort(sorted);")),
               ("пишет subList(0, 2), считая, что конец включается, — на пьедестале двое",
                RACE.replace("sorted.subList(0, 3)", "sorted.subList(0, 2)"))],
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=3, slug="java-listops-rt-duty-roster", title="Дежурство: {k} в конец списка",
        function="nextWeek",
        variants=[{"k": 2, "times": "2 раза", "people": "первые 2 человека переходят"},
                  {"k": 3, "times": "3 раза", "people": "первые 3 человека переходят"},
                  {"k": 4, "times": "4 раза", "people": "первые 4 человека переходят"}],
        intro="В классе дежурят по списку: дежурят те, кто стоит в начале. Каждую неделю {people} в конец списка — "
              "в том же порядке, в котором стояли, — а остальные сдвигаются к началу.",
        steps=["Напиши метод `static List<String> nextWeek(List<String> duty)`, который меняет сам список `duty` "
               "так, как он будет выглядеть на следующей неделе, и возвращает этот же список.",
               "Если список пустой, верни его без изменений.",
               "Иначе {times} повтори одно действие: убери из списка первый элемент методом `remove(0)` — он вернёт "
               "убранное имя — и добавь это имя в конец списка методом `add`.",
               "Если людей в списке меньше {k}, всё равно повтори действие {times}: список просто прокручивается по кругу."],
        hint="После `remove(0)` все остальные сдвигаются на одно место к началу, поэтому следующий, кого надо "
             "переставить, снова стоит под номером 0.",
        starter=ROSTER_HEAD + "        // Напиши решение здесь\n" + ROSTER_TAIL,
        solution=ROSTER_HEAD + "        if (duty.isEmpty()) {{\n            return duty;\n        }}\n"
                 "        for (int i = 0; i < {k}; i++) {{\n            String first = duty.remove(0);\n"
                 "            duty.add(first);\n        }}\n" + ROSTER_TAIL,
        inputs=['new ArrayList<>(List.of("Anya", "Boris", "Vika", "Gleb", "Dasha"))',
                'new ArrayList<>(List.of("Egor", "Zhenya", "Zina", "Ira", "Kirill", "Lena"))',
                'new ArrayList<>(List.of("Mark", "Nina"))',
                'new ArrayList<>(List.of("Oleg"))',
                'new ArrayList<>(List.of("Petya", "Rita", "Sasha", "Tanya"))',
                "new ArrayList<>()",
                'new ArrayList<>(List.of("Ulyana", "Fedor", "Yura", "Yana", "Arseny", "Bella", "Vlad"))'],
        wrong=[("переставляет с конца в начало — список крутится в другую сторону",
                ROSTER_HEAD + "        if (duty.isEmpty()) {{\n            return duty;\n        }}\n"
                "        for (int i = 0; i < {k}; i++) {{\n            String last = duty.remove(duty.size() - 1);\n"
                "            duty.add(0, last);\n        }}\n" + ROSTER_TAIL),
               ("добавляет имя в конец, но не убирает его из начала — люди в списке повторяются",
                ROSTER_HEAD + "        if (duty.isEmpty()) {{\n            return duty;\n        }}\n"
                "        for (int i = 0; i < {k}; i++) {{\n            duty.add(duty.get(i));\n        }}\n" + ROSTER_TAIL)],
    ),
]
