"""PY_STRING_SLICING — «Срезы строк». Taught before: print, variables, arithmetic, int/float, strings, type conversion,
// and %, += -=, f-strings, conditions, for/while loops, break/continue, lists (indexes, append, len, in, iterating).
Here: s[a:b], s[:n], s[n:], negative bounds, a step: s[::2], s[1::2], s[::-1].
Not yet: string methods (upper, strip, split, replace, find, …), functions."""
from build import OutputTask

SKILL = "PY_STRING_SLICING"

NEED_SLICE = ("Slice", "Реши задачу срезами строки: вида `text[a:b]`, `text[:n]`, `text[::-1]`.")

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ss-rt-file-name", title="Имя и расширение файла",
        given=["file"],
        variants=[{"file": '"report_2026.pdf"'}, {"file": '"cat.png"'}, {"file": '"homework_final.txt"'}],
        hidden=[{"file": '"a.doc"'}, {"file": '"summer_photos_sochi.jpg"'}, {"file": '"notes.csv"'}],
        intro="Программа для фотографий и документов показывает файл в две строки: отдельно имя и отдельно расширение. "
              "Имя файла записано строкой `file = {file}`. У всех файлов расширение из 3 букв, а перед ним стоит точка.",
        steps=["Срезом с отрицательной границей вырежи последние 3 символа — расширение — в переменную `ext`.",
               "Срезом вырежи всё, кроме последних 4 символов (точки и расширения), в переменную `name`.",
               "Выведи две строки: `Name: report_2026` и `Extension: pdf`"],
        hint="Срез `text[-3:]` — последние 3 символа строки, а `text[:-4]` — вся строка без последних 4 символов. "
             "Отрицательные границы считают с конца, поэтому длину имени знать не нужно.",
        solution='ext = file[-3:]\nname = file[:-4]\nprint(f"Name: {name}")\nprint(f"Extension: {ext}")',
        wrong=[("отрезает только 3 символа: точка осталась в имени",
                'ext = file[-3:]\nname = file[:-3]\nprint(f"Name: {name}")\nprint(f"Extension: {ext}")'),
               ("берёт расширение вместе с точкой",
                'ext = file[-4:]\nname = file[:-4]\nprint(f"Name: {name}")\nprint(f"Extension: {ext}")')],
        must_use=[NEED_SLICE],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ss-rt-running-line", title="Бегущая строка",
        given=["text", "k"],
        variants=[{"text": '"WELCOME"', "k": "3"}, {"text": '"SALE50"', "k": "2"}, {"text": '"OPENNOW"', "k": "4"}],
        hidden=[{"text": '"ABC"', "k": "1"}, {"text": '"HELLO"', "k": "5"}, {"text": '"TICKETS"', "k": "6"},
                {"text": '"NEWS"', "k": "0"}],
        intro="Табло над входом в магазин показывает бегущую строку `text = {text}`. За каждый такт первая буква "
              "убегает с левого края и появляется справа. Прошло `k = {k}` тактов (`k` не больше длины строки).",
        steps=["Срезами раздели строку на две части: первые `k` символов — в переменную `head`, остальные — в `tail`.",
               "Склей части в обратном порядке: сначала `tail`, потом `head`, — это то, что сейчас на табло. "
               "Сохрани в `shown`.",
               "Выведи `Board: COMEWEL`",
               "Если `shown` совпадает с исходной строкой, выведи `Same as start`, иначе выведи `Moved by 3`"],
        hint="`text[:k]` — первые `k` символов, `text[k:]` — всё, начиная с индекса `k`. Строки склеивают через `+`. "
             "Если `k` равно 0 или длине строки, табло показывает исходный текст.",
        solution='head = text[:k]\ntail = text[k:]\nshown = tail + head\nprint(f"Board: {shown}")\n'
                 'if shown == text:\n    print("Same as start")\nelse:\n    print(f"Moved by {k}")',
        wrong=[("склеивает части в прежнем порядке",
                'head = text[:k]\ntail = text[k:]\nshown = head + tail\nprint(f"Board: {shown}")\n'
                'if shown == text:\n    print("Same as start")\nelse:\n    print(f"Moved by {k}")'),
               ("ошибка на единицу: хвост начинается с индекса k + 1, одна буква теряется",
                'head = text[:k]\ntail = text[k + 1:]\nshown = tail + head\nprint(f"Board: {shown}")\n'
                'if shown == text:\n    print("Same as start")\nelse:\n    print(f"Moved by {k}")')],
        constructs=["if"],
        must_use=[NEED_SLICE],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ss-rt-dna-codons", title="Кодоны ДНК",
        given=["dna"],
        variants=[{"dna": '"ATGGCCTTAGC"'}, {"dna": '"TTACGGATC"'}, {"dna": '"GGCATGCA"'}],
        hidden=[{"dna": '"AT"'}, {"dna": '"ATG"'}, {"dna": '"CCCAAAGGGTTTA"'}, {"dna": '"ACGTACGTACGT"'}],
        intro="Биолог читает цепочку ДНК `dna = {dna}` тройками букв — кодонами: первые три буквы, следующие три и так "
              "далее. Если длина цепочки не делится на 3, в конце остаются лишние буквы, которые в кодон не вошли.",
        steps=["Посчитай `full` — сколько букв входит в целые кодоны: длина цепочки, делённая нацело на 3 и умноженная на 3.",
               "Циклом `for` с `range` от 0 до `full` с шагом 3 перебери начала кодонов. Для каждого вырежи срезом "
               "три буквы и выведи строку вида `Codon 1: ATG` — номер кодона считай отдельным счётчиком.",
               "После цикла, если `full` меньше длины цепочки, выведи лишние буквы (срез с индекса `full` до конца) "
               "в виде `Extra: GC`, иначе выведи `No extra letters`"],
        hint="Если кодон начинается с индекса `i`, то это срез `dna[i:i + 3]`: символ с индексом `i + 3` уже не входит. "
             "Цикл до `full`, а не до длины строки, — иначе неполный хвост напечатается как кодон.",
        solution='full = len(dna) // 3 * 3\nnumber = 0\nfor i in range(0, full, 3):\n    number += 1\n'
                 '    print(f"Codon {number}: {dna[i:i + 3]}")\nif full < len(dna):\n    print(f"Extra: {dna[full:]}")\n'
                 'else:\n    print("No extra letters")',
        wrong=[("цикл до длины строки: неполный хвост печатается как кодон",
                'full = len(dna) // 3 * 3\nnumber = 0\nfor i in range(0, len(dna), 3):\n    number += 1\n'
                '    print(f"Codon {number}: {dna[i:i + 3]}")\nif full < len(dna):\n    print(f"Extra: {dna[full:]}")\n'
                'else:\n    print("No extra letters")'),
               ("срез dna[i:i + 2]: в кодоне две буквы вместо трёх",
                'full = len(dna) // 3 * 3\nnumber = 0\nfor i in range(0, full, 3):\n    number += 1\n'
                '    print(f"Codon {number}: {dna[i:i + 2]}")\nif full < len(dna):\n    print(f"Extra: {dna[full:]}")\n'
                'else:\n    print("No extra letters")'),
               ("лишними считает начало цепочки, а не конец",
                'full = len(dna) // 3 * 3\nnumber = 0\nfor i in range(0, full, 3):\n    number += 1\n'
                '    print(f"Codon {number}: {dna[i:i + 3]}")\nif full < len(dna):\n    print(f"Extra: {dna[:len(dna) - full]}")\n'
                'else:\n    print("No extra letters")')],
        constructs=["for"],
        must_use=[NEED_SLICE],
    ),
]
