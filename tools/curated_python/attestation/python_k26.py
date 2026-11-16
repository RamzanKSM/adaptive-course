"""Задания аттестации Python."""
from build import OutputTask

TASKS = [
    OutputTask(**{'skill': 'PY_STRING_SLICING',
 'difficulty': 3,
 'slug': 'py-att26-locker-code',
 'title': 'Код шкафчика',
 'given': ['code'],
 'variants': [{'code': '"AB-0123"'}],
 'hidden': [{'code': '"ZX-9001"'}, {'code': '"QW-0000"'}, {'code': '"MN-1234"'}],
 'intro': 'Код шкафчика `code = {code}` состоит из двух букв, дефиса и четырёх цифр.',
 'steps': ['Срезом сохрани буквы в `zone`.',
           'Срезом сохрани четыре цифры в `number`.',
           'Выведи `Zone:`, пробел и `zone`; затем `Number:`, пробел и `number`.',
           'Выведи `Reverse:` и цифры в обратном порядке. Если номер начинается с `0`, выведи `Special`, '
           'иначе `Regular`.'],
 'hint': 'Проверь порядок действий и границы: последний индекс среза не включается.',
 'solution': 'zone = code[:2]\n'
             'number = code[3:]\n'
             'print("Zone:", zone)\n'
             'print("Number:", number)\n'
             'print("Reverse:", number[::-1])\n'
             'if number[:1] == "0":\n'
             '    print("Special")\n'
             'else:\n'
             '    print("Regular")',
 'wrong': [('теряет последнюю цифру',
            'zone = code[:2]\n'
            'number = code[3:-1]\n'
            'print("Zone:", zone)\n'
            'print("Number:", number)\n'
            'print("Reverse:", number[::-1])\n'
            'if number[:1] == "0":\n'
            '    print("Special")\n'
            'else:\n'
            '    print("Regular")'),
           ('не переворачивает цифры',
            'zone = code[:2]\n'
            'number = code[3:]\n'
            'print("Zone:", zone)\n'
            'print("Number:", number)\n'
            'print("Reverse:", number)\n'
            'if number[:1] == "0":\n'
            '    print("Special")\n'
            'else:\n'
            '    print("Regular")')],
 'constructs': [],
 'must_use': [('Slice', 'Используй срезы строки.')]}),
    OutputTask(**{'skill': 'PY_STRING_SLICING',
 'difficulty': 3,
 'slug': 'py-att26-train-number',
 'title': 'Номер поезда',
 'given': ['train'],
 'variants': [{'train': '"R-0527"'}],
 'hidden': [{'train': '"K-0001"'}, {'train': '"S-9876"'}, {'train': '"A-1000"'}, {'train': '"E-1212"'}],
 'intro': 'Номер поезда `train = {train}`: буква маршрута, дефис и четыре цифры.',
 'steps': ['Срезом сохрани букву маршрута в `route`.',
           'Срезом сохрани первые две цифры номера в `first`.',
           'Срезом сохрани последние две цифры в `last`.',
           'Выведи `Route: <route>`, `First: <first>`, `Last: <last>`. Затем сравни числовые значения двух '
           'половин и выведи `Equal` или `Different`.'],
 'hint': 'Проверь порядок действий и границы: последний индекс среза не включается.',
 'solution': 'route = train[:1]\n'
             'first = train[2:4]\n'
             'last = train[-2:]\n'
             'print("Route:", route)\n'
             'print("First:", first)\n'
             'print("Last:", last)\n'
             'if int(first) == int(last):\n'
             '    print("Equal")\n'
             'else:\n'
             '    print("Different")',
 'wrong': [('пропускает первую цифру',
            'route = train[:1]\n'
            'first = train[3:5]\n'
            'last = train[-2:]\n'
            'print("Route:", route)\n'
            'print("First:", first)\n'
            'print("Last:", last)\n'
            'if int(first) == int(last):\n'
            '    print("Equal")\n'
            'else:\n'
            '    print("Different")'),
           ('берёт только последнюю цифру',
            'route = train[:1]\n'
            'first = train[2:4]\n'
            'last = train[-1:]\n'
            'print("Route:", route)\n'
            'print("First:", first)\n'
            'print("Last:", last)\n'
            'if int(first) == int(last):\n'
            '    print("Equal")\n'
            'else:\n'
            '    print("Different")')],
 'constructs': [],
 'must_use': [('Slice', 'Используй срезы строки.')]}),
    OutputTask(**{'skill': 'PY_STRING_SLICING',
 'difficulty': 3,
 'slug': 'py-att26-flight-date',
 'title': 'Дата вылета',
 'given': ['date'],
 'variants': [{'date': '"2027-05-09"'}],
 'hidden': [{'date': '"2030-01-01"'}, {'date': '"1999-12-31"'}, {'date': '"2028-10-02"'}],
 'intro': 'Дата вылета `date = {date}` записана как `YYYY-MM-DD`, все части фиксированной длины.',
 'steps': ['Срезом сохрани год в `year`.',
           'Срезом сохрани месяц в `month`.',
           'Срезом сохрани день в `day`.',
           'Выведи дату `DD/MM/YYYY`. Если месяц равен `01`, `02` или `12`, выведи `Winter`, иначе `Other '
           'season`.'],
 'hint': 'Проверь порядок действий и границы: последний индекс среза не включается.',
 'solution': 'year = date[:4]\n'
             'month = date[5:7]\n'
             'day = date[8:]\n'
             'print(day + "/" + month + "/" + year)\n'
             'if month == "01" or month == "02" or month == "12":\n'
             '    print("Winter")\n'
             'else:\n'
             '    print("Other season")',
 'wrong': [('теряет последнюю цифру месяца',
            'year = date[:4]\n'
            'month = date[5:6]\n'
            'day = date[8:]\n'
            'print(day + "/" + month + "/" + year)\n'
            'if month == "01" or month == "02" or month == "12":\n'
            '    print("Winter")\n'
            'else:\n'
            '    print("Other season")'),
           ('меняет день и месяц',
            'year = date[:4]\n'
            'month = date[5:7]\n'
            'day = date[8:]\n'
            'print(month + "/" + day + "/" + year)\n'
            'if month == "01" or month == "02" or month == "12":\n'
            '    print("Winter")\n'
            'else:\n'
            '    print("Other season")')],
 'constructs': [],
 'must_use': [('Slice', 'Используй срезы строки.')]}),
    OutputTask(**{'skill': 'PY_STRING_SLICING',
 'difficulty': 3,
 'slug': 'py-att26-inventory-label',
 'title': 'Складская этикетка',
 'given': ['label'],
 'variants': [{'label': '"BOX-4812"'}],
 'hidden': [{'label': '"BAG-0007"'}, {'label': '"KIT-9531"'}, {'label': '"BOX-1200"'}],
 'intro': 'Этикетка `label = {label}` содержит три буквы типа, дефис и четыре цифры партии.',
 'steps': ['Срезом выдели тип в `kind`.',
           'Срезом выдели цифры партии в `batch`.',
           'Выведи `Type: <kind>` и `Batch: <batch>` на отдельных строках.',
           'Выведи `Check: <digits>`: цифры партии на позициях 0 и 2 срезом с шагом 2. Затем циклом посчитай '
           'и выведи `Sum: <sum>` — сумму всех четырёх цифр партии.'],
 'hint': 'Проверь порядок действий и границы: последний индекс среза не включается.',
 'solution': 'kind = label[:3]\n'
             'batch = label[4:]\n'
             'print("Type:", kind)\n'
             'print("Batch:", batch)\n'
             'print("Check:", batch[::2])\n'
             'total = 0\n'
             'for digit in batch:\n'
             '    total += int(digit)\n'
             'print("Sum:", total)',
 'wrong': [('берёт нечётные позиции',
            'kind = label[:3]\n'
            'batch = label[4:]\n'
            'print("Type:", kind)\n'
            'print("Batch:", batch)\n'
            'print("Check:", batch[1::2])\n'
            'total = 0\n'
            'for digit in batch:\n'
            '    total += int(digit)\n'
            'print("Sum:", total)'),
           ('считает только первые три цифры',
            'kind = label[:3]\n'
            'batch = label[4:]\n'
            'print("Type:", kind)\n'
            'print("Batch:", batch)\n'
            'print("Check:", batch[::2])\n'
            'total = 0\n'
            'for digit in batch[:3]:\n'
            '    total += int(digit)\n'
            'print("Sum:", total)')],
 'constructs': [],
 'must_use': [('Slice', 'Используй срезы строки.')]}),
]
