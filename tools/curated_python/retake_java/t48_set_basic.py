"""SET_BASIC — «Множество Set» (Java). Taught before: everything up to List (add, get, size, for-each). Here: Set,
HashSet and TreeSet, add (and its boolean result), contains, size, a set built from a list, retainAll / removeAll /
addAll. Output never iterates or prints a HashSet: only sizes, booleans or a TreeSet. Not yet: Map."""
from java_tasks import JavaOutputTask

SKILL = "SET_BASIC"

DICE = ('Set<Integer> faces = new TreeSet<>(rolls);\nSystem.out.println("Rolls: " + rolls.size());\n'
        'System.out.println("Faces seen: " + faces);\nSystem.out.println("Never rolled: " + (6 - faces.size()));\n'
        'if (faces.contains(6)) {\n    System.out.println("Six: yes");\n} else {\n    System.out.println("Six: no");\n}')

HOMEWORK = ('Set<String> done = new HashSet<>();\nfor (String name : submissions) {\n    done.add(name);\n}\n'
            'for (String name : students) {\n    if (!done.contains(name)) {\n        System.out.println("No homework: " + name);\n    }\n}\n'
            'System.out.println("Submitted: " + done.size() + " of " + students.size());')

RECIPE = ('Set<String> have = new TreeSet<>(recipe);\nhave.retainAll(fridge);\nSystem.out.println("Have: " + have);\n'
          'Set<String> buy = new TreeSet<>(recipe);\nbuy.removeAll(fridge);\nSystem.out.println("To buy: " + buy);\n'
          'Set<String> extra = new TreeSet<>(fridge);\nextra.removeAll(recipe);\n'
          'System.out.println("Not needed: " + extra.size());\nif (buy.size() == 0) {\n    System.out.println("Ready to cook");\n'
          '} else {\n    System.out.println("Go shopping");\n}')

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-set-rt-dice-faces", title="Грани кубика",
        given=[("List<Integer>", "rolls")],
        variants=[{"rolls": "new ArrayList<>(List.of(3, 1, 3, 5, 1, 3))"},
                  {"rolls": "new ArrayList<>(List.of(6, 2, 6, 4, 2, 1, 5))"},
                  {"rolls": "new ArrayList<>(List.of(4, 4, 2, 4))"}],
        hidden=[{"rolls": "new ArrayList<>(List.of(6))"},
                {"rolls": "new ArrayList<>(List.of(1, 2, 3, 4, 5, 6, 6, 1))"},
                {"rolls": "new ArrayList<>(List.of(5, 5, 5, 5, 5))"},
                {"rolls": "new ArrayList<>(List.of(2, 1, 2, 3, 1))"}],
        intro="Вова бросает игральный кубик с гранями от 1 до 6 и записывает каждый результат в список `rolls`. "
              "Многие числа выпали несколько раз. Он хочет узнать, какие грани уже выпадали, а какие — ещё ни разу.",
        steps=["Создай множество `Set<Integer> faces = new TreeSet<>(rolls);` — оно само уберёт повторы и расставит "
               "числа по возрастанию.",
               "Выведи строку вида `Rolls: 6` — сколько всего бросков в списке `rolls`.",
               "Выведи `Faces seen: ` и сразу за этим множество `faces`, например `Faces seen: [1, 3, 5]`.",
               "Выведи строку вида `Never rolled: 3` — сколько из шести граней ещё ни разу не выпало.",
               "Последней строкой проверь методом `contains`, выпадала ли шестёрка: выведи `Six: yes` или `Six: no`."],
        hint="Ни разу не выпавших граней столько, сколько 6 минус число РАЗНЫХ выпавших чисел, то есть минус размер "
             "множества, а не списка.",
        solution=DICE,
        wrong=[("считает невыпавшие грани по числу бросков — повторы тоже вычитаются",
                DICE.replace("(6 - faces.size())", "(6 - rolls.size())")),
               ("сложил броски в список, а не в множество — повторы остались",
                DICE.replace("Set<Integer> faces = new TreeSet<>(rolls);", "List<Integer> faces = new ArrayList<>(rolls);"))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-set-rt-homework-check", title="Кто сдал домашку",
        given=[("List<String>", "students"), ("List<String>", "submissions")],
        variants=[{"students": 'new ArrayList<>(List.of("Anya", "Boris", "Vika", "Gleb", "Dasha"))',
                   "submissions": 'new ArrayList<>(List.of("Vika", "Anya", "Vika", "Dasha"))'},
                  {"students": 'new ArrayList<>(List.of("Oleg", "Pavel", "Rita"))',
                   "submissions": 'new ArrayList<>(List.of("Rita", "Rita", "Rita"))'},
                  {"students": 'new ArrayList<>(List.of("Ira", "Kostya", "Lena", "Misha", "Nina", "Sasha"))',
                   "submissions": 'new ArrayList<>(List.of("Misha", "Ira", "Sasha", "Misha", "Kostya", "Nina"))'}],
        hidden=[{"students": 'new ArrayList<>(List.of("Lev", "Mila"))', "submissions": "new ArrayList<>()"},
                {"students": 'new ArrayList<>(List.of("Yura", "Zoya"))', "submissions": 'new ArrayList<>(List.of("Zoya", "Yura", "Yura"))'},
                {"students": 'new ArrayList<>(List.of("Egor", "Fedya", "Inna", "Kira"))',
                 "submissions": 'new ArrayList<>(List.of("Kira", "Egor", "Kira", "Egor", "Kira"))'}],
        intro="Учительница собирает домашние работы через школьный сайт. Список класса — `students`. Каждый раз, когда "
              "кто-то отправляет работу, его имя записывается в список `submissions`; некоторые исправляли работу и "
              "отправляли её ещё раз. Нужно понять, кто домашку так и не сдал.",
        steps=["Создай пустое множество `Set<String> done = new HashSet<>();` и добавь в него методом `add` каждое имя "
               "из `submissions` (цикл for-each).",
               "Пройди по списку класса `students` по порядку. Для каждого, кого нет в `done` (метод `contains`), "
               "выведи строку вида `No homework: Boris`.",
               "Последней строкой выведи строку вида `Submitted: 3 of 5` — сколько разных учеников сдали работу "
               "и сколько всего учеников в классе."],
        hint="Сдавших учеников столько, сколько разных имён в `submissions`, — это размер множества `done`, а не "
             "размер списка: повторная отправка нового ученика не добавляет.",
        solution=HOMEWORK,
        wrong=[("считает сдавших по числу отправок — исправленные работы засчитываются дважды",
                HOMEWORK.replace('done.size() + " of "', 'submissions.size() + " of "')),
               ("перечисляет тех, кто сдал, а не тех, кто не сдал",
                HOMEWORK.replace("if (!done.contains(name))", "if (done.contains(name))"))],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-set-rt-recipe-fridge", title="Рецепт и холодильник",
        given=[("List<String>", "recipe"), ("List<String>", "fridge")],
        variants=[{"recipe": 'new ArrayList<>(List.of("eggs", "milk", "flour", "sugar"))',
                   "fridge": 'new ArrayList<>(List.of("milk", "cheese", "eggs", "milk", "butter"))'},
                  {"recipe": 'new ArrayList<>(List.of("potato", "onion", "carrot"))',
                   "fridge": 'new ArrayList<>(List.of("carrot", "onion", "potato", "potato"))'},
                  {"recipe": 'new ArrayList<>(List.of("rice", "fish", "cucumber", "rice"))',
                   "fridge": 'new ArrayList<>(List.of("apple", "cucumber", "yogurt"))'}],
        hidden=[{"recipe": 'new ArrayList<>(List.of("tea"))', "fridge": "new ArrayList<>()"},
                {"recipe": 'new ArrayList<>(List.of("bread", "ham"))', "fridge": 'new ArrayList<>(List.of("ham", "bread"))'},
                {"recipe": 'new ArrayList<>(List.of("tomato", "pepper", "salt"))',
                 "fridge": 'new ArrayList<>(List.of("salt", "jam", "salt", "kefir", "lemon"))'},
                {"recipe": 'new ArrayList<>(List.of("beet", "beet", "cabbage"))', "fridge": 'new ArrayList<>(List.of("cabbage"))'}],
        intro="Ты хочешь приготовить блюдо. Продукты для него записаны в список `recipe`, а то, что лежит в "
              "холодильнике, — в список `fridge` (одинаковые продукты могут повторяться). `TreeSet` — множество, "
              "которое хранит элементы по алфавиту, — поможет понять, что нужно докупить.",
        steps=["Создай множество `Set<String> have = new TreeSet<>(recipe);` и оставь в нём только продукты, которые "
               "есть в `fridge`, методом `retainAll`. Выведи `Have: ` и это множество, например `Have: [eggs, milk]`.",
               "Создай ещё одну копию `recipe` — тоже `TreeSet` — и убери из неё всё, что есть в `fridge`, методом "
               "`removeAll`. Выведи `To buy: ` и это множество.",
               "Сделай `TreeSet` из `fridge`, убери из него всё, что есть в `recipe`, и выведи строку вида "
               "`Not needed: 2` — сколько разных продуктов из холодильника для блюда не нужны.",
               "Если докупать ничего не нужно (множество из второго шага пустое), выведи `Ready to cook`, "
               "иначе — `Go shopping`."],
        hint="`retainAll` и `removeAll` меняют то множество, у которого их вызвали. Поэтому для каждого шага делай "
             "свою новую копию списка, а сами `recipe` и `fridge` не трогай.",
        solution=RECIPE,
        wrong=[("работает с одним и тем же множеством — после retainAll докупать как будто нечего",
                'Set<String> food = new TreeSet<>(recipe);\nfood.retainAll(fridge);\nSystem.out.println("Have: " + food);\n'
                'food.removeAll(fridge);\nSystem.out.println("To buy: " + food);\n'
                'Set<String> extra = new TreeSet<>(fridge);\nextra.removeAll(recipe);\n'
                'System.out.println("Not needed: " + extra.size());\nif (food.size() == 0) {\n    System.out.println("Ready to cook");\n'
                '} else {\n    System.out.println("Go shopping");\n}'),
               ("для ненужных продуктов вычитает в обратном порядке — получает то, что надо докупить",
                RECIPE.replace('Set<String> extra = new TreeSet<>(fridge);\nextra.removeAll(recipe);',
                               'Set<String> extra = new TreeSet<>(recipe);\nextra.removeAll(fridge);'))],
        constructs=["if"],
    ),
]
