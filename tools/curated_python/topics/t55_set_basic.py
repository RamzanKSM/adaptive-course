"""PY_SET_BASIC — «Множества set». Taught before: everything up to tuples (conditions, loops, lists and their methods,
slices, string methods, functions, classes, tuples). Here: set() for removing repeats, `in`, add, union/intersection/
difference. Sets are never printed or iterated for output directly (their order is not fixed): sorted() or len().
Not yet: dicts, comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_SET_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-set-word-letters", title="Разные буквы в слове",
        given=["word"],
        variants=[{"word": '"banana"'}, {"word": '"letter"'}, {"word": '"coffee"'}],
        hidden=[{"word": '"cat"'}, {"word": '"mama"'}, {"word": '"program"'}, {"word": '"kayak"'}],
        intro="В игре «Угадай слово» загадано слово `word`. Ведущему нужно знать, сколько разных букв предстоит "
              "угадать игрокам: каждую букву называют один раз, даже если в слове она встречается несколько раз.",
        steps=["Преврати строку `word` в множество букв с помощью `set()` — повторы при этом исчезнут сами.",
               "Выведи строку вида `Different letters: 5` с количеством элементов этого множества.",
               'Следующей строкой выведи сами буквы в алфавитном порядке через пробел, например `a k t`. '
               'У множества нет порядка, поэтому сначала отсортируй его функцией `sorted()` — она вернёт список, — '
               'а потом склей буквы через `" ".join(...)`.'],
        hint='Множество хранит каждый элемент только один раз: `set("mama")` — это множество всего из двух букв, '
             '`m` и `a`. Длину множества, как и длину списка, узнают через `len()`.',
        solution='letters = set(word)\nprint(f"Different letters: {len(letters)}")\nprint(" ".join(sorted(letters)))',
        wrong=[("считает длину слова — повторяющиеся буквы учитываются несколько раз",
                'print(f"Different letters: {len(word)}")\nprint(" ".join(sorted(set(word))))'),
               ("сортирует само слово, а не множество — буквы повторяются",
                'print(f"Different letters: {len(set(word))}")\nprint(" ".join(sorted(word)))')],
        must_use=[("re:\\bset\\(", "Убери повторы с помощью множества: set(word) оставит каждую букву только один раз.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-set-sticker-album", title="Альбом с наклейками",
        given=["album", "pack"],
        variants=[{"album": "{3, 7, 12, 15, 20}", "pack": "[7, 21, 3, 30, 21]"},
                  {"album": "{1, 4, 9}", "pack": "[5, 4, 5, 10]"},
                  {"album": "{2, 6, 11, 18}", "pack": "[11, 2, 25, 6, 25, 8]"}],
        hidden=[{"album": "{1, 2}", "pack": "[3, 4]"},
                {"album": "{10, 20, 30}", "pack": "[10, 20, 30]"},
                {"album": "{5}", "pack": "[6, 6, 6, 5, 7]"},
                {"album": "{1, 2, 3, 4}", "pack": "[9, 1, 9, 2, 8, 8, 3]"}],
        intro="Ты собираешь альбом с наклейками. Номера наклеек, которые уже вклеены, хранятся в множестве `album`. "
              "Ты открыл новый пакетик — номера наклеек из него по порядку записаны в список `pack`. "
              "В одном пакетике могут попасться и одинаковые наклейки.",
        steps=["Пройди циклом `for` по списку `pack`.",
               "Если наклейка уже есть в множестве `album`, выведи строку вида `Repeat: 14` с её номером. "
               "Иначе выведи строку вида `New: 14` и сразу добавь эту наклейку в `album` методом `.add()` — "
               "тогда такая же наклейка дальше в пакетике окажется уже повтором.",
               "После цикла выведи строку вида `In album: 40` — сколько разных наклеек теперь в альбоме."],
        hint="Проверка `x in album` для множества пишется так же, как для списка. Главное — не забыть добавить новую "
             "наклейку в множество: иначе вторая такая же наклейка из того же пакетика тоже покажется новой.",
        solution='for sticker in pack:\n    if sticker in album:\n        print(f"Repeat: {sticker}")\n    else:\n'
                 '        print(f"New: {sticker}")\n        album.add(sticker)\nprint(f"In album: {len(album)}")',
        wrong=[("не добавляет новую наклейку в альбом — вторая такая же тоже считается новой",
                'for sticker in pack:\n    if sticker in album:\n        print(f"Repeat: {sticker}")\n    else:\n'
                '        print(f"New: {sticker}")\nprint(f"In album: {len(album)}")'),
               ("сначала добавляет наклейку, а потом проверяет — все наклейки оказываются повторами",
                'for sticker in pack:\n    album.add(sticker)\n    if sticker in album:\n        print(f"Repeat: {sticker}")\n'
                '    else:\n        print(f"New: {sticker}")\nprint(f"In album: {len(album)}")')],
        constructs=["for", "if"],
        must_use=[("re:\\.add\\(", "Вклей новую наклейку в альбом методом .add() — так множество запомнит, что она у тебя уже есть.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-set-common-friends", title="Общие друзья",
        given=["my_friends", "sasha_friends"],
        variants=[{"my_friends": '["Anya", "Boris", "Vika", "Gosha", "Dina"]', "sasha_friends": '["Vika", "Egor", "Anya", "Zhora"]'},
                  {"my_friends": '["Oleg", "Mila", "Timur"]', "sasha_friends": '["Timur", "Sonya", "Mila", "Liza", "Nika"]'},
                  {"my_friends": '["Katya", "Nina", "Petya", "Rita", "Semyon"]', "sasha_friends": '["Petya", "Katya", "Rita"]'}],
        hidden=[{"my_friends": '["Ira", "Gleb"]', "sasha_friends": '["Zoya", "Dan"]'},
                {"my_friends": '["Max", "Eva", "Yana"]', "sasha_friends": '["Eva", "Yana", "Max"]'},
                {"my_friends": '["Anya", "Vika", "Yulia", "Fil", "Osya", "Taya"]', "sasha_friends": '["Yulia", "Osya", "Kira"]'}],
        intro="У тебя и у твоего одноклассника Саши есть списки друзей в соцсети: `my_friends` — твои друзья, "
              "`sasha_friends` — друзья Саши. Хочется узнать, кто у вас общий, кто дружит только с тобой "
              "и сколько всего разных людей в двух списках.",
        steps=["Преврати оба списка в множества с помощью `set()`.",
               "Выведи через `print` слово `Common:` и через пробел список тех, кто есть в обоих множествах, "
               "отсортированный по алфавиту функцией `sorted()`. Например: `Common: ['Gena', 'Lida']`.",
               "Следующей строкой так же выведи `Only mine:` и отсортированный список тех, кто есть среди твоих друзей, "
               "но не среди друзей Саши.",
               "Последней строкой выведи строку вида `Total people: 9` — сколько разных людей есть хотя бы в одном из двух списков."],
        hint="У множеств есть готовые операции: `a & b` — элементы, которые есть в обоих множествах; `a - b` — те, что есть "
             "в `a`, но нет в `b`; `a | b` — все элементы из обоих множеств без повторов. Порядок в `a - b` важен.",
        solution='mine = set(my_friends)\nsasha = set(sasha_friends)\nprint("Common:", sorted(mine & sasha))\n'
                 'print("Only mine:", sorted(mine - sasha))\nprint(f"Total people: {len(mine | sasha)}")',
        wrong=[("вычитает множества в обратном порядке — получаются друзья только Саши",
                'mine = set(my_friends)\nsasha = set(sasha_friends)\nprint("Common:", sorted(mine & sasha))\n'
                'print("Only mine:", sorted(sasha - mine))\nprint(f"Total people: {len(mine | sasha)}")'),
               ("складывает длины списков — общие друзья посчитаны дважды",
                'mine = set(my_friends)\nsasha = set(sasha_friends)\nprint("Common:", sorted(mine & sasha))\n'
                'print("Only mine:", sorted(mine - sasha))\nprint(f"Total people: {len(my_friends) + len(sasha_friends)}")')],
        must_use=[("re:\\bset\\(", "Преврати списки в множества через set(): у множеств есть готовые операции "
                                   "пересечения, разности и объединения.")],
    ),
]
