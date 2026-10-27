"""PY_COMPREHENSIONS — «Генераторы списков». Taught before: lists and their methods, tuples, sets, dicts, loops,
conditions, string methods, functions, classes. Here: list comprehensions — a new list from an expression over
the elements, with and without a condition. Not yet: try/except, lambda."""
from build import OutputTask

SKILL = "PY_COMPREHENSIONS"

NEED_LISTCOMP = ("ListComp", "Собери новый список генератором списка — одной строкой вида [выражение for элемент in список], "
                             "без цикла с append.")

WEATHER = """\
changes = [temps[i + 1] - temps[i] for i in range(len(temps) - 1)]
print(changes)
warmer = [i + 2 for i in range(len(changes)) if changes[i] > 0]
print(f"Warmer days: {warmer}")
print(f"Biggest rise: {max(changes)}")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-comp-rt-initials", title="Сокращение из первых букв",
        given=["words"],
        variants=[{"words": '["Moscow", "State", "University"]'},
                  {"words": '["Very", "Important", "Person"]'},
                  {"words": '["Do", "It", "Yourself"]'}],
        hidden=[{"words": '["Okay"]'},
                {"words": '["Frequently", "Asked", "Questions"]'},
                {"words": '["As", "Soon", "As", "Possible"]'}],
        intro="Длинные названия часто сокращают по первым буквам слов: Moscow State University — MSU. Слова названия "
              "записаны в список `words`.",
        steps=["Генератором списка собери новый список из первых букв всех слов — у каждого слова возьми символ "
               "с индексом 0. Порядок сохрани.",
               "Выведи этот список через `print`.",
               "Следующей строкой выведи само сокращение — буквы из нового списка, склеенные без пробелов: "
               "`\"\".join(...)`."],
        hint="Слева от `for` в генераторе пишут, что положить в новый список: `[w[0] for w in words]` — первую букву "
             "каждого слова. Первая буква — индекс 0, а индекс -1 дал бы последнюю.",
        solution='letters = [word[0] for word in words]\nprint(letters)\nprint("".join(letters))',
        wrong=[("берёт последние буквы слов вместо первых",
                'letters = [word[-1] for word in words]\nprint(letters)\nprint("".join(letters))'),
               ("склеивает целые слова, а не первые буквы",
                'letters = [word[0] for word in words]\nprint(letters)\nprint("".join(words))')],
        constructs=["list"],
        must_use=[NEED_LISTCOMP],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-comp-rt-long-words", title="Длинные слова",
        given=["text", "size"],
        variants=[{"text": '"the quick brown fox jumps over the lazy dog"', "size": "5"},
                  {"text": '"reading books every evening makes life better"', "size": "6"},
                  {"text": '"a cat sat on a mat"', "size": "3"}],
        hidden=[{"text": '"hello"', "size": "5"},
                {"text": '"hello"', "size": "6"},
                {"text": '"one three five seven eleven"', "size": "4"},
                {"text": '"to be or not to be"', "size": "2"}],
        intro="Учитель английского хочет выписать для словарика длинные слова из предложения `text`: слова в нём "
              "написаны маленькими буквами через пробел. Длинным считается слово, в котором не меньше `size` букв.",
        steps=["Разбей `text` на слова методом `.split()`.",
               "Генератором списка с условием `if` собери слова, длина которых не меньше `size`. Порядок слов сохрани.",
               "Выведи этот список через `print`, а следующей строкой — строку вида `Long words: 3` с числом слов в нём."],
        hint="Условие в генераторе списка пишут в конце: `[w for w in words if len(w) > 2]`. «Не меньше» — это `>=`: "
             "слово ровно из `size` букв тоже подходит.",
        solution='words = text.split()\nlong_words = [word for word in words if len(word) >= size]\nprint(long_words)\n'
                 'print(f"Long words: {len(long_words)}")',
        wrong=[("строгое сравнение — слова ровно из size букв не попадают",
                'words = text.split()\nlong_words = [word for word in words if len(word) > size]\nprint(long_words)\n'
                'print(f"Long words: {len(long_words)}")'),
               ("забыл условие — в список попадают все слова",
                'words = text.split()\nlong_words = [word for word in words]\nprint(long_words)\n'
                'print(f"Long words: {len(long_words)}")')],
        constructs=["list"],
        must_use=[NEED_LISTCOMP],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-comp-rt-warm-days", title="Когда потеплело",
        given=["temps"],
        variants=[{"temps": "[3, 5, 4, 8, 8, 6]"},
                  {"temps": "[-2, -5, -1, 0, 3]"},
                  {"temps": "[15, 12, 12, 10]"}],
        hidden=[{"temps": "[1, 2]"},
                {"temps": "[7, 7, 7]"},
                {"temps": "[0, 10, 5, 6, 6, 9, 2]"},
                {"temps": "[20, 18, 21, 25, 24]"}],
        intro="Дневные температуры за несколько дней подряд записаны в список `temps`: первый элемент — день 1, второй — "
              "день 2 и так далее. Синоптику нужно знать, на сколько градусов менялась температура от каждого дня "
              "к следующему и в какие дни становилось теплее.",
        steps=["Первым генератором списка собери изменения: для каждого индекса `i` от 0 до `len(temps) - 2` — "
               "`temps[i + 1] - temps[i]`. Выведи этот список через `print`.",
               "Изменение с индексом `i` показывает, как отличается день с номером `i + 2` от предыдущего. Вторым "
               "генератором с условием собери номера дней, когда стало строго теплее, чем накануне. "
               "Выведи строку вида `Warmer days: [2, 4]`.",
               "Последней строкой выведи строку вида `Biggest rise: 4` — самое большое значение из списка изменений "
               "(функция `max()`)."],
        hint="Перебирать можно не только элементы, но и индексы: `[... for i in range(len(temps) - 1)]` — "
             "`range(len(temps) - 1)` не даст выйти за конец списка, когда берёшь `temps[i + 1]`. Изменение 0 — "
             "это не потепление.",
        solution=WEATHER,
        wrong=[("нумерует дни с ошибкой на один — номер дня равен i + 1",
                WEATHER.replace("warmer = [i + 2 for i", "warmer = [i + 1 for i")),
               ("вычитает в обратном порядке — потепление и похолодание меняются местами",
                WEATHER.replace("temps[i + 1] - temps[i]", "temps[i] - temps[i + 1]")),
               ("считает потеплением и день без изменений",
                WEATHER.replace("if changes[i] > 0]", "if changes[i] >= 0]"))],
        constructs=["list"],
        must_use=[NEED_LISTCOMP],
    ),
]
