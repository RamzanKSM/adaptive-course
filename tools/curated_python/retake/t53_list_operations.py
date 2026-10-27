"""PY_LIST_OPERATIONS — «Операции со списком». Taught before: everything up to classes (conditions, loops, lists with
indexing, append, len, in, iterating, string slicing and methods, functions). Here: insert, remove, pop, index, count,
sort/sorted, reverse, slicing a list. Not yet: tuples, sets, dicts, comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_LIST_OPERATIONS"

EDITOR = """\
words = []
undone = []
for action in actions:
    if action == "undo":
        if len(words) > 0:
            word = words.pop()
            undone.append(word)
            print(f"Undo: {word}")
        else:
            print("Nothing to undo")
    elif action == "redo":
        if len(undone) > 0:
            word = undone.pop()
            words.append(word)
            print(f"Redo: {word}")
        else:
            print("Nothing to redo")
    else:
        words.append(action)
        undone = []
print(words)
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lo-rt-shopping-list", title="Список покупок",
        given=["shopping", "bought"],
        variants=[{"shopping": '["Milk", "Eggs", "Bread", "Cheese", "Apples"]', "bought": '"Bread"'},
                  {"shopping": '["Tea", "Sugar", "Rice", "Butter"]', "bought": '"Tea"'},
                  {"shopping": '["Soap", "Pasta", "Onions", "Juice", "Yogurt", "Fish"]', "bought": '"Fish"'}],
        hidden=[{"shopping": '["Salt", "Honey"]', "bought": '"Honey"'},
                {"shopping": '["Kefir", "Beans", "Corn", "Plums", "Nuts"]', "bought": '"Corn"'},
                {"shopping": '["Water", "Lemons", "Cookies"]', "bought": '"Water"'}],
        intro="Мама составила список покупок `shopping` и пронумеровала пункты по порядку, начиная с 1. "
              "Ты уже купил `bought` — этот пункт нужно вычеркнуть, а оставшиеся покупки расставить по алфавиту, "
              "чтобы их было удобнее искать.",
        steps=["Найди место `bought` в списке методом `.index()` и выведи строку вида `Bread was item 3` — "
               "с номером пункта так, как его считает мама, с 1.",
               "Убери `bought` из списка `shopping` методом `.remove()`.",
               "Отсортируй список `shopping` по алфавиту методом `.sort()` и выведи его командой `print(shopping)`."],
        hint="`.index()` возвращает индекс, а индексы считаются с 0 — к нему нужно прибавить 1. "
             "Номер ищи до сортировки: после `.sort()` элементы переставятся, и номер получится другим.",
        solution='print(f"{bought} was item {shopping.index(bought) + 1}")\nshopping.remove(bought)\n'
                 'shopping.sort()\nprint(shopping)',
        wrong=[("выводит индекс без +1 — номера сдвинуты на один",
                'print(f"{bought} was item {shopping.index(bought)}")\nshopping.remove(bought)\n'
                'shopping.sort()\nprint(shopping)'),
               ("сортирует до поиска номера — номер берётся из уже переставленного списка",
                'shopping.sort()\nprint(f"{bought} was item {shopping.index(bought) + 1}")\nshopping.remove(bought)\n'
                'print(shopping)')],
        constructs=["list"],
        must_use=[("re:\\.index\\(", "Найди номер пункта методом .index()."),
                  ("re:\\.remove\\(", "Вычеркни покупку методом .remove(): он ищет элемент по значению."),
                  ("re:\\.sort\\(", "Расставь покупки по алфавиту методом .sort().")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lo-rt-lap-median", title="Средний круг",
        given=["laps"],
        variants=[{"laps": "[66, 61, 70, 64, 63]"},
                  {"laps": "[58, 60, 60, 57, 62, 60, 59]"},
                  {"laps": "[75, 72, 79]"}],
        hidden=[{"laps": "[60, 64, 64, 64, 70]"},
                {"laps": "[90]"},
                {"laps": "[55, 50, 65, 45, 70, 40, 60]"},
                {"laps": "[81, 80, 82, 83, 84]"}],
        intro="Бегун пробежал нечётное число кругов по стадиону, время каждого круга в секундах записано в список `laps` "
              "по порядку. Тренер хочет знать медиану — время, которое оказывается ровно посередине, если "
              "расставить круги от быстрого к медленному, — и сколько кругов были быстрее медианы.",
        steps=["Получи новый список, отсортированный по возрастанию, функцией `sorted()` и выведи его через `print`.",
               "Медиана — элемент отсортированного списка с индексом `len(laps) // 2`. Выведи её в виде `Median: 64 s`.",
               "Найди в отсортированном списке методом `.index()`, где впервые встречается медиана. Все элементы перед "
               "этим местом меньше медианы, поэтому найденный индекс — это и есть число кругов быстрее медианы. "
               "Выведи его в виде `Faster laps: 2`."],
        hint="Брать средний элемент из несортированного `laps` нельзя — посередине окажется просто третий по счёту круг. "
             "А число быстрых кругов не всегда равно `len(laps) // 2`: если несколько кругов пробежаны ровно "
             "за время медианы, `.index()` найдёт первый из них.",
        solution='ranked = sorted(laps)\nprint(ranked)\nmedian = ranked[len(laps) // 2]\nprint(f"Median: {median} s")\n'
                 'print(f"Faster laps: {ranked.index(median)}")',
        wrong=[("берёт средний элемент несортированного списка",
                'ranked = sorted(laps)\nprint(ranked)\nmedian = laps[len(laps) // 2]\nprint(f"Median: {median} s")\n'
                'print(f"Faster laps: {ranked.index(median)}")'),
               ("считает быстрые круги как len(laps) // 2 — ошибается, когда несколько кругов равны медиане",
                'ranked = sorted(laps)\nprint(ranked)\nmedian = ranked[len(laps) // 2]\nprint(f"Median: {median} s")\n'
                'print(f"Faster laps: {len(laps) // 2}")')],
        constructs=["list"],
        must_use=[("re:\\bsorted\\(", "Получи отсортированный список функцией sorted()."),
                  ("re:\\.index\\(", "Найди место медианы в отсортированном списке методом .index().")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lo-rt-undo-redo", title="Отмена и повтор",
        given=["actions"],
        variants=[{"actions": '["I", "like", "cats", "undo", "undo", "redo", "dogs", "redo"]'},
                  {"actions": '["undo", "Hello", "big", "world", "undo", "redo", "redo"]'},
                  {"actions": '["one", "two", "three", "undo", "undo", "undo", "undo", "redo", "four"]'}],
        hidden=[{"actions": '["undo", "a", "redo"]'},
                {"actions": '["x", "y", "undo", "undo", "redo", "redo", "redo"]'},
                {"actions": '["go", "undo", "home", "undo", "redo"]'},
                {"actions": '["red", "green", "undo", "blue", "redo", "undo", "redo"]'}],
        intro="Ты пишешь простой текстовый редактор с кнопками «Отменить» и «Повторить». Пользователь по очереди "
              "делает действия из списка `actions`: `\"undo\"` — отменить, `\"redo\"` — повторить отменённое, а любая "
              "другая строка — напечатать это слово. Набранные слова хранятся в списке `words`, отменённые — "
              "в списке `undone`. Вначале оба списка пустые.",
        steps=["Пройди циклом по `actions`. Если действие — обычное слово, добавь его в конец `words`. После набора "
               "нового слова повторять старое уже нельзя: сделай `undone` снова пустым списком.",
               "Действие `\"undo\"`: если в `words` есть слова, вынь последнее методом `.pop()`, положи его в конец "
               "`undone` и выведи строку вида `Undo: cats`. Если `words` пуст, выведи `Nothing to undo`.",
               "Действие `\"redo\"`: если в `undone` есть слова, вынь последнее отменённое методом `.pop()`, верни его "
               "в конец `words` и выведи строку вида `Redo: like`. Если `undone` пуст, выведи `Nothing to redo`.",
               "После цикла выведи итоговый список слов командой `print(words)`."],
        hint="`.pop()` без аргумента вынимает последний элемент и возвращает его — именно так работает «Отменить»: "
             "отменяется последнее действие. Повторять нужно тоже то, что отменили последним, поэтому из `undone` "
             "тоже бери `.pop()` без индекса. Проверяй длину списка до `.pop()`: из пустого списка вынуть нечего.",
        solution=EDITOR,
        wrong=[("повторяет самое раннее отменённое слово — pop(0) вместо pop()",
                EDITOR.replace("            word = undone.pop()\n", "            word = undone.pop(0)\n")),
               ("не очищает отменённые слова после набора нового — повтор возвращает старые слова",
                EDITOR.replace("        words.append(action)\n        undone = []\n", "        words.append(action)\n")),
               ("отменяет первое слово текста, а не последнее",
                EDITOR.replace("            word = words.pop()\n", "            word = words.pop(0)\n"))],
        constructs=["list", "for", "if"],
        must_use=[("re:\\.pop\\(", "Вынимай слова методом .pop(): он убирает элемент из списка и сразу возвращает его.")],
    ),
]
