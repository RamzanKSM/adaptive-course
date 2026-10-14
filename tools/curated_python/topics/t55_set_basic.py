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
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-set-dice-faces", title="Все грани кубика",
        given=["rolls"],
        variants=[{"rolls": "[3, 5, 3, 1, 6, 5, 3]"}, {"rolls": "[2, 2, 4, 2]"}, {"rolls": "[6, 1, 2, 5, 3, 4, 6, 1]"}],
        hidden=[{"rolls": "[1]"}, {"rolls": "[1, 2, 3, 4, 5, 6]"}, {"rolls": "[4, 4, 4, 4, 4, 4, 4]"},
                {"rolls": "[5, 6, 5, 6, 1, 2, 1]"}],
        intro="Ты бросаешь игральный кубик, у которого шесть граней с числами от 1 до 6. Результаты всех бросков "
              "записаны в список `rolls`. Хочется узнать, сколько разных граней уже выпало и все ли грани ты успел увидеть.",
        steps=["Выведи строку вида `Rolls: 9` — сколько всего было бросков.",
               "Преврати список `rolls` в множество с помощью `set()` — повторы исчезнут — и выведи строку вида "
               "`Different faces: 4` с количеством его элементов.",
               "Последней строкой выведи `All faces seen`, если выпали все шесть граней, иначе строку вида "
               "`Not seen yet: 2` — сколько граней ещё ни разу не выпадало."],
        hint="Шесть бросков ещё не значат, что выпали все шесть граней: одна грань могла выпасть дважды. "
             "Считать нужно элементы множества, а не броски.",
        solution='print(f"Rolls: {len(rolls)}")\nfaces = set(rolls)\nprint(f"Different faces: {len(faces)}")\n'
                 'if len(faces) == 6:\n    print("All faces seen")\nelse:\n    print(f"Not seen yet: {6 - len(faces)}")',
        wrong=[("считает разными гранями все броски — повторы учитываются",
                'print(f"Rolls: {len(rolls)}")\nprint(f"Different faces: {len(rolls)}")\n'
                'if len(set(rolls)) == 6:\n    print("All faces seen")\nelse:\n    print(f"Not seen yet: {6 - len(set(rolls))}")'),
               ("решает, что все грани выпали, если бросков было не меньше шести",
                'print(f"Rolls: {len(rolls)}")\nfaces = set(rolls)\nprint(f"Different faces: {len(faces)}")\n'
                'if len(rolls) >= 6:\n    print("All faces seen")\nelse:\n    print(f"Not seen yet: {6 - len(faces)}")')],
        must_use=[("re:\\bset\\(", "Убери повторы с помощью множества: set(rolls) оставит каждую грань только один раз.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-set-new-words", title="Новые слова в тексте",
        given=["known", "text"],
        variants=[{"known": '{"the", "cat", "is", "on"}', "text": '"the cat is on the mat and the dog is on the mat"'},
                  {"known": '{"i", "like", "to"}', "text": '"i like to swim and i like to run and swim"'},
                  {"known": '{"we", "go", "to", "school"}', "text": '"we go to school by bus and go home by bus"'}],
        hidden=[{"known": '{"hello"}', "text": '"hello hello hello"'},
                {"known": '{"a"}', "text": '"red apple and green apple and a red pear"'},
                {"known": '{"one", "two"}', "text": '"three one four three two five four"'}],
        intro="Ты учишь английский. Слова, которые ты уже знаешь, лежат в множестве `known`. Тебе попался текст `text` — "
              "все слова в нём написаны маленькими буквами через пробел. Нужно выписать новые слова, каждое по одному разу.",
        steps=["Разбей текст на слова методом `.split()` и создай пустое множество для уже выписанных новых слов — "
               "`set()`.",
               "Пройди по словам текста. Если слова нет в `known` и его ещё нет среди выписанных, выведи это слово "
               "на отдельной строке и добавь его в множество выписанных методом `.add()`.",
               "После цикла выведи строку вида `New words: 3` — сколько разных новых слов нашлось."],
        hint="Пустое множество создают только через `set()`: пустые фигурные скобки `{{}}` — это пустой словарь. "
             "Слово выписывается, только если обе проверки `not in` верны, поэтому соедини их через `and`.",
        solution='words = text.split()\nwritten = set()\nfor word in words:\n'
                 '    if word not in known and word not in written:\n        print(word)\n        written.add(word)\n'
                 'print(f"New words: {len(written)}")',
        wrong=[("не проверяет, выписано ли слово, — новое слово печатается при каждой встрече",
                'words = text.split()\nwritten = set()\nfor word in words:\n'
                '    if word not in known:\n        print(word)\n        written.add(word)\n'
                'print(f"New words: {len(written)}")'),
               ("перебирает буквы текста вместо слов",
                'written = set()\nfor word in text:\n'
                '    if word not in known and word not in written and word != " ":\n        print(word)\n        written.add(word)\n'
                'print(f"New words: {len(written)}")')],
        constructs=["for", "if"],
        must_use=[("re:\\.add\\(", "Запоминай выписанные слова в множестве методом .add() — так одно слово не выпишется дважды.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-set-club-days", title="Дни для кружка",
        given=["anya_days", "boris_days", "club_days"],
        variants=[{"anya_days": "[1, 3, 4, 6]", "boris_days": "[2, 3, 6, 7]", "club_days": "[3, 5]"},
                  {"anya_days": "[2, 5]", "boris_days": "[5, 2, 1]", "club_days": "[1, 2, 5, 6]"},
                  {"anya_days": "[1, 2, 3, 4, 5, 6]", "boris_days": "[6, 7, 2]", "club_days": "[2, 4, 6]"}],
        hidden=[{"anya_days": "[1, 2, 3, 4, 5, 6, 7]", "boris_days": "[1, 2, 3, 4, 5, 6, 7]", "club_days": "[7]"},
                {"anya_days": "[4]", "boris_days": "[4]", "club_days": "[4, 1]"},
                {"anya_days": "[1, 7, 1]", "boris_days": "[3, 7, 5]", "club_days": "[5, 6]"}],
        intro="Аня и Борис хотят вместе ходить в шахматный кружок. Дни недели обозначены числами от 1 (понедельник) "
              "до 7 (воскресенье). В списке `anya_days` — дни, когда свободна Аня, в `boris_days` — когда свободен Борис, "
              "в `club_days` — дни занятий кружка. В списках дни могут повторяться.",
        steps=["Преврати все три списка в множества с помощью `set()`.",
               "Выведи через `print` слово `Both free:` и через пробел отсортированный функцией `sorted()` список дней, "
               "когда свободны и Аня, и Борис. Например: `Both free: [2, 7]`.",
               "Следующей строкой так же выведи `Club for both:` и отсортированный список дней кружка, когда свободны оба.",
               "Последней строкой выведи строку вида `Both busy: 3` — сколько дней недели не свободен ни один из них. "
               "Все дни недели — это `set(range(1, 8))`."],
        hint="`a & b` — элементы, которые есть в обоих множествах, `a | b` — все элементы из обоих без повторов, "
             "`a - b` — элементы `a`, которых нет в `b`. Дни, когда заняты оба, — это неделя без тех дней, "
             "когда свободен хоть кто-то.",
        solution='anya = set(anya_days)\nboris = set(boris_days)\nclub = set(club_days)\nboth = anya & boris\n'
                 'print("Both free:", sorted(both))\nprint("Club for both:", sorted(both & club))\n'
                 'busy = set(range(1, 8)) - (anya | boris)\nprint(f"Both busy: {len(busy)}")',
        wrong=[("объединяет дни вместо пересечения — считает днями «обоих» дни, когда свободен хотя бы один",
                'anya = set(anya_days)\nboris = set(boris_days)\nclub = set(club_days)\nboth = anya | boris\n'
                'print("Both free:", sorted(both))\nprint("Club for both:", sorted(both & club))\n'
                'busy = set(range(1, 8)) - (anya | boris)\nprint(f"Both busy: {len(busy)}")'),
               ("считает занятые дни вычитанием длин списков — повторы и общие дни учитываются неправильно",
                'anya = set(anya_days)\nboris = set(boris_days)\nclub = set(club_days)\nboth = anya & boris\n'
                'print("Both free:", sorted(both))\nprint("Club for both:", sorted(both & club))\n'
                'print(f"Both busy: {7 - len(anya_days) - len(boris_days)}")')],
        must_use=[("re:\\bset\\(", "Преврати списки дней в множества через set(): у множеств есть готовые операции "
                                       "пересечения, разности и объединения.")],
    ),
]
