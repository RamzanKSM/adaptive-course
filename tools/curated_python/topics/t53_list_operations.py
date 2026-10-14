"""PY_LIST_OPERATIONS — «Операции со списком». Taught before: everything up to classes (conditions, loops, lists with
indexing, append, len, in, iterating, string slicing and methods, functions). Here: insert, remove, pop, index, count,
sort/sorted, reverse, slicing a list. Not yet: tuples, sets, dicts, comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_LIST_OPERATIONS"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lo-doctor-queue", title="Очередь к врачу",
        given=["queue", "urgent"],
        variants=[{"queue": '["Ivanov", "Petrova", "Sidorov", "Kozlova"]', "urgent": '"Morozov"'},
                  {"queue": '["Smirnova", "Orlov", "Belova", "Zaitsev", "Kim"]', "urgent": '"Lebedeva"'},
                  {"queue": '["Volkov", "Novikova", "Popov"]', "urgent": '"Egorova"'}],
        hidden=[{"queue": '["Sokolov", "Fedorova"]', "urgent": '"Pavlov"'},
                {"queue": '["Titov", "Medvedeva", "Zhukov", "Ershova", "Gusev", "Kuzmina"]', "urgent": '"Nosov"'},
                {"queue": '["Belkin", "Yakovleva", "Losev"]', "urgent": '"Sorokina"'}],
        intro="В поликлинике пациенты ждут приёма. Их фамилии записаны в список `queue` в порядке очереди: "
              "первым в списке стоит тот, кто зайдёт к врачу следующим. А ещё пришёл пациент `urgent` с сильной болью — "
              "его пропустят без очереди.",
        steps=["Врач приглашает первого пациента: убери его из списка `queue` методом `.pop(0)` и сохрани в переменную. "
               "Выведи строку вида `Next patient: Orekhov` — с фамилией этого пациента.",
               "Поставь пациента `urgent` в самое начало списка `queue` методом `.insert()`.",
               "Выведи очередь после этих изменений командой `print(queue)`."],
        hint="`.pop()` без аргумента убирает последний элемент списка, а с индексом — элемент на этом месте, и при этом "
             "возвращает его, так что его можно сохранить в переменную. `.append()` всегда добавляет в конец, "
             "а `.insert()` ставит элемент на место с нужным индексом и сдвигает остальные вправо.",
        solution='first = queue.pop(0)\nprint(f"Next patient: {first}")\nqueue.insert(0, urgent)\nprint(queue)',
        wrong=[("pop() без индекса — к врачу заходит последний в очереди",
                'first = queue.pop()\nprint(f"Next patient: {first}")\nqueue.insert(0, urgent)\nprint(queue)'),
               ("append вместо insert — срочный пациент оказывается в конце очереди",
                'first = queue.pop(0)\nprint(f"Next patient: {first}")\nqueue.append(urgent)\nprint(queue)')],
        constructs=["list"],
        must_use=[("re:\\.pop\\(", "Достань первого пациента методом .pop(0): он убирает элемент из списка и сразу возвращает его."),
                  ("re:\\.insert\\(", "Поставь срочного пациента в начало методом .insert(): append умеет добавлять только в конец.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lo-long-jump", title="Три лучших прыжка",
        given=["jumps"],
        variants=[{"jumps": "[412, 455, 498, 430, 471]"},
                  {"jumps": "[380, 402, 395, 417, 366, 410]"},
                  {"jumps": "[470, 455, 462, 449, 481]"}],
        hidden=[{"jumps": "[300, 350, 320, 310]"},
                {"jumps": "[520, 410, 430, 405, 415, 440, 425]"},
                {"jumps": "[390, 400, 410, 420, 430]"}],
        intro="Спортсмен сделал несколько попыток в прыжках в длину. Результаты в сантиметрах записаны в список `jumps` "
              "по порядку: первая попытка, вторая и так далее. Тренеру нужны три лучших результата и номер самой удачной попытки.",
        steps=["Получи новый список результатов, отсортированный от большего к меньшему: функция `sorted()` с аргументом "
               "`reverse=True`. Сам список `jumps` не меняй — исходный порядок попыток ещё понадобится.",
               "Возьми срезом первые три элемента отсортированного списка — три лучших результата — и выведи этот срез через `print`.",
               "Следующей строкой выведи номер попытки с лучшим прыжком в виде `Best try: 2`. Найди место лучшего "
               "результата в исходном списке `jumps` методом `.index()`. Помни, что попытки нумеруются с 1, а индексы — с 0."],
        hint="Метод `.sort()` переставляет элементы в самом списке, и прежний порядок теряется. А функция `sorted()` "
             "возвращает новый отсортированный список и не трогает старый. Срез `[:3]` берёт элементы с индексами 0, 1 и 2.",
        solution='ranked = sorted(jumps, reverse=True)\nprint(ranked[:3])\nbest = ranked[0]\n'
                 'print(f"Best try: {jumps.index(best) + 1}")',
        wrong=[("сортирует сам список через .sort() — исходный порядок теряется, и лучшей всегда оказывается первая попытка",
                'jumps.sort(reverse=True)\nprint(jumps[:3])\nbest = jumps[0]\nprint(f"Best try: {jumps.index(best) + 1}")'),
               ("забыл reverse=True — сортирует по возрастанию и выводит три худших прыжка",
                'ranked = sorted(jumps)\nprint(ranked[:3])\nbest = ranked[0]\nprint(f"Best try: {jumps.index(best) + 1}")')],
        constructs=["list"],
        must_use=[("re:\\bsorted\\(", "Получи отсортированную копию через sorted(): метод .sort() переставил бы сам список jumps, "
                                      "и номер лучшей попытки потерялся бы."),
                  ("re:\\.index\\(", "Найди место лучшего результата в списке jumps методом .index().")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lo-guest-duplicates", title="Лишние записи в списке гостей",
        given=["guests", "name"],
        variants=[{"guests": '["Anya", "Oleg", "Oleg", "Vika", "Dima", "Oleg"]', "name": '"Oleg"'},
                  {"guests": '["Lena", "Lena", "Petya", "Sonya", "Lena", "Roma"]', "name": '"Lena"'},
                  {"guests": '["Misha", "Katya", "Tanya", "Tanya", "Grisha"]', "name": '"Tanya"'}],
        hidden=[{"guests": '["Ira", "Gleb", "Zoya"]', "name": '"Gleb"'},
                {"guests": '["Yura", "Yura", "Yura", "Yura", "Elya"]', "name": '"Yura"'},
                {"guests": '["Asya", "Vova", "Nina"]', "name": '"Petya"'},
                {"guests": '["Kira", "Lev", "Kira", "Lev", "Kira"]', "name": '"Lev"'}],
        intro="Организатор праздника собирал список гостей из нескольких чатов, поэтому некоторые имена попали в список "
              "`guests` по несколько раз. Гость `name` написал, что прийти не сможет, — все его записи нужно убрать.",
        steps=["Посчитай методом `.count()`, сколько раз `name` встречается в списке `guests`, и выведи строку вида `Entries: 5`.",
               "Убери из списка `guests` все записи `name`. Помни: метод `.remove()` за один вызов убирает только первое "
               "совпадение. Если `name` в списке нет, ничего удалять не нужно. Остальные гости должны остаться в прежнем порядке.",
               "Выведи список после удаления командой `print(guests)`."],
        hint="Ты уже знаешь, сколько раз имя встречается в списке, — значит, знаешь, сколько раз нужно вызвать `.remove()`. "
             "А вот удалять элементы прямо внутри `for` по этому же списку опасно: элементы сдвигаются, "
             "и цикл перескакивает через соседний.",
        solution='times = guests.count(name)\nprint(f"Entries: {times}")\nfor i in range(times):\n    guests.remove(name)\nprint(guests)',
        wrong=[("вызывает .remove() один раз — убирается только первая запись",
                'print(f"Entries: {guests.count(name)}")\nguests.remove(name)\nprint(guests)'),
               ("удаляет элементы внутри for по тому же списку — соседняя запись пропускается",
                'print(f"Entries: {guests.count(name)}")\nfor guest in guests:\n    if guest == name:\n'
                '        guests.remove(guest)\nprint(guests)')],
        constructs=["list"],
        must_use=[("re:\\.count\\(", "Посчитай записи методом .count() — он сразу говорит, сколько раз элемент встречается в списке."),
                  ("re:\\.remove\\(", "Убирай записи методом .remove(): он ищет элемент по значению, а не по индексу.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lo-playlist-skip", title="Плейлист задом наперёд",
        given=["songs", "skip"],
        variants=[{"songs": '["Yesterday", "Imagine", "Hello", "Believer", "Faded"]', "skip": '"Hello"'},
                  {"songs": '["Thunder", "Radioactive", "Demons", "Natural"]', "skip": '"Thunder"'},
                  {"songs": '["Shape of You", "Perfect", "Photograph", "Castle on the Hill", "Galway Girl", "Happier"]',
                   "skip": '"Happier"'}],
        hidden=[{"songs": '["Alone", "Lily"]', "skip": '"Alone"'},
                {"songs": '["Sunrise", "Rain", "Wind", "Snow", "Fog"]', "skip": '"Wind"'},
                {"songs": '["One", "Two", "Three"]', "skip": '"Three"'}],
        intro="Перед дальней поездкой ты собрал плейлист `songs`. Песня `skip` надоела — её нужно убрать. "
              "А оставшиеся песни хочется послушать в обратном порядке: с последней до первой.",
        steps=["Убери песню `skip` из списка `songs` методом `.remove()` — он ищет элемент по значению.",
               "Выведи строку вида `Songs left: 4` с числом песен, которые остались в списке.",
               "Разверни список `songs` методом `.reverse()` и выведи его командой `print(songs)`."],
        hint="`.remove(x)` убирает элемент, равный `x`, где бы он ни стоял, а `.pop()` без аргумента убирает последний. "
             "`.reverse()` переставляет элементы в самом списке и ничего не возвращает, поэтому печатай сам список "
             "после вызова, а не результат `songs.reverse()`.",
        solution='songs.remove(skip)\nprint(f"Songs left: {len(songs)}")\nsongs.reverse()\nprint(songs)',
        wrong=[("pop() вместо remove — убирается последняя песня, а не надоевшая",
                'songs.pop()\nprint(f"Songs left: {len(songs)}")\nsongs.reverse()\nprint(songs)'),
               ("печатает результат songs.reverse() — выводится None",
                'songs.remove(skip)\nprint(f"Songs left: {len(songs)}")\nprint(songs.reverse())')],
        constructs=["list"],
        must_use=[("re:\\.remove\\(", "Убери песню методом .remove(): он находит элемент по значению."),
                  ("re:\\.reverse\\(", "Разверни список методом .reverse().")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lo-judges-scores", title="Оценки судей",
        given=["scores"],
        variants=[{"scores": "[7, 9, 8, 10, 6]"},
                  {"scores": "[5, 8, 8, 9, 7, 4]"},
                  {"scores": "[10, 9, 9, 8, 10]"}],
        hidden=[{"scores": "[3, 6, 9]"},
                {"scores": "[8, 2, 7, 7, 9, 10, 6]"},
                {"scores": "[5, 5, 5, 5]"},
                {"scores": "[4, 10, 1, 6, 8]"}],
        intro="Фигуристку оценивают несколько судей, их оценки записаны в список `scores` в порядке, в котором сидят судьи. "
              "Чтобы один слишком строгий или слишком добрый судья не испортил результат, самую низкую и самую высокую "
              "оценку отбрасывают, а остальные складывают.",
        steps=["Получи новый список оценок, отсортированный по возрастанию, функцией `sorted()`.",
               "Срезом возьми из отсортированного списка все оценки, кроме первой и последней, — то есть без самой низкой "
               "и самой высокой. Выведи этот срез через `print`.",
               "Сложи оценки из среза в цикле и выведи строку вида `Final score: 24`."],
        hint="В срезе можно использовать отрицательный индекс: `[1:-1]` начинает со второго элемента и останавливается "
             "перед последним. Если резать исходный список без сортировки, отбросятся оценки крайних судей, "
             "а не самая низкая и самая высокая.",
        solution='ranked = sorted(scores)\nkept = ranked[1:-1]\nprint(kept)\ntotal = 0\nfor score in kept:\n'
                 '    total += score\nprint(f"Final score: {total}")',
        wrong=[("режет исходный список без сортировки — отбрасываются первый и последний судья",
                'kept = scores[1:-1]\nprint(kept)\ntotal = 0\nfor score in kept:\n    total += score\nprint(f"Final score: {total}")'),
               ("срез [1:] — отбрасывается только самая низкая оценка",
                'ranked = sorted(scores)\nkept = ranked[1:]\nprint(kept)\ntotal = 0\nfor score in kept:\n'
                '    total += score\nprint(f"Final score: {total}")')],
        constructs=["list", "for"],
        must_use=[("re:\\bsorted\\(", "Получи отсортированную копию оценок через sorted()."),
                  ("re:\\[[^\\]]*:[^\\]]*\\]", "Отбрось крайние оценки срезом списка.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lo-let-ahead", title="Пропусти вперёд",
        given=["line", "passes"],
        variants=[{"line": '["Anya", "Boris", "Vera", "Gleb", "Dina"]', "passes": '["Boris", "Zoya", "Anya"]'},
                  {"line": '["Oleg", "Pasha", "Rita", "Sveta"]', "passes": '["Rita", "Oleg", "Oleg"]'},
                  {"line": '["Ilya", "Kira", "Lena", "Mark", "Nina", "Olya"]', "passes": '["Nina", "Ilya", "Petr", "Kira"]'}],
        hidden=[{"line": '["Tim", "Uma"]', "passes": '["Uma"]'},
                {"line": '["Ada", "Ben", "Cid"]', "passes": '["Max", "Ada", "Ada", "Ada"]'},
                {"line": '["Fil", "Gosha", "Hana", "Igor"]', "passes": '["Gosha", "Hana", "Fil"]'}],
        intro="В очереди к кассе стоят люди из списка `line`, первым в списке стоит тот, кто ближе всех к кассе. "
              "Люди из списка `passes` по очереди пропускают вперёд того, кто стоит сразу за ними, — то есть меняются "
              "с ним местами. Некоторых из `passes` в очереди вообще нет.",
        steps=["Пройди циклом по списку `passes`. Если очередного человека нет в `line`, выведи строку вида "
               "`Zoya is not in line` и переходи к следующему.",
               "Если человек есть в очереди, найди его место методом `.index()`, вынь его из списка методом `.pop()` "
               "с этим индексом и вставь методом `.insert()` на одно место дальше от кассы, чем он стоял. "
               "Если он стоял последним, он так и остаётся последним.",
               "После цикла выведи итоговую очередь командой `print(line)`."],
        hint="Проверь человека через `in` до вызова `.index()`: если элемента нет в списке, `.index()` остановит программу "
             "с ошибкой. После `.pop(i)` все, кто стоял дальше, сдвигаются на одно место ближе, поэтому вставлять "
             "нужно на индекс `i + 1`. А `.insert()` с индексом, равным длине списка, просто добавляет в конец.",
        solution='for name in passes:\n    if name in line:\n        i = line.index(name)\n        line.pop(i)\n'
                 '        line.insert(i + 1, name)\n    else:\n        print(f"{name} is not in line")\nprint(line)',
        wrong=[("вставляет обратно на тот же индекс — никто не меняется местами",
                'for name in passes:\n    if name in line:\n        i = line.index(name)\n        line.pop(i)\n'
                '        line.insert(i, name)\n    else:\n        print(f"{name} is not in line")\nprint(line)'),
               ("убирает человека и ставит в конец очереди через append",
                'for name in passes:\n    if name in line:\n        line.remove(name)\n        line.append(name)\n'
                '    else:\n        print(f"{name} is not in line")\nprint(line)'),
               ("сдвигает на два места — вставляет на индекс i + 2",
                'for name in passes:\n    if name in line:\n        i = line.index(name)\n        line.pop(i)\n'
                '        line.insert(i + 2, name)\n    else:\n        print(f"{name} is not in line")\nprint(line)')],
        constructs=["list", "for"],
        must_use=[("re:\\.index\\(", "Найди место человека в очереди методом .index()."),
                  ("re:\\.insert\\(", "Поставь человека на новое место методом .insert().")],
    ),
]
