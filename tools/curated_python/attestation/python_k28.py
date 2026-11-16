"""Задания аттестации Python."""
from build import OutputTask

TASKS = [
    OutputTask(**{'skill': 'PY_FUNCTION_BASIC',
 'difficulty': 3,
 'slug': 'py-att28-kiosk-receipt',
 'title': 'Чек киоска',
 'given': ['item', 'price', 'count'],
 'variants': [{'item': '"Tea"', 'price': '25', 'count': '4'}],
 'hidden': [{'item': '"Juice"', 'price': '30', 'count': '3'},
            {'item': '"Cake"', 'price': '100', 'count': '1'},
            {'item': '"Water"', 'price': '50', 'count': '0'}],
 'intro': 'В киоске товар `item = {item}` стоит `price = {price}` руб., количество покупаемых товаров — `count = {count}`. При '
          'сумме от 100 руб. скидка 10 руб.',
 'steps': ['Создай функцию `receipt(name, price, count)`.',
           'Внутри вычисли стоимость всех товаров и при сумме не меньше 100 вычти скидку 10.',
           'Функция печатает строку `<name>: <total> rub`.',
           'После определения вызови функцию с данными покупки.'],
 'hint': 'Проверь порядок аргументов и используй значения параметров функции.',
 'solution': 'def receipt(name, price, count):\n'
             '    total = price * count\n'
             '    if total >= 100:\n'
             '        total -= 10\n'
             '    print(f"{name}: {total} rub")\n'
             '\n'
             'receipt(item, price, count)',
 'wrong': [('скидка только выше границы',
            'def receipt(name, price, count):\n'
            '    total = price * count\n'
            '    if total > 100:\n'
            '        total -= 10\n'
            '    print(f"{name}: {total} rub")\n'
            '\n'
            'receipt(item, price, count)'),
           ('стоимость без количества',
            'def receipt(name, price, count):\n'
            '    total = price + count\n'
            '    if total >= 100:\n'
            '        total -= 10\n'
            '    print(f"{name}: {total} rub")\n'
            '\n'
            'receipt(item, price, count)')],
 'constructs': ['function'],
 'must_use': [('FunctionDef', 'Создай и вызови свою функцию.')]}),
    OutputTask(**{'skill': 'PY_FUNCTION_BASIC',
 'difficulty': 3,
 'slug': 'py-att28-participant-cards',
 'title': 'Карточки участников',
 'given': ['participants', 'number'],
 'variants': [{'participants': '["Anna", "Oleg", "Li"]', 'number': '7'}],
 'hidden': [{'participants': '["A"]', 'number': '1'},
            {'participants': '[]', 'number': '5'},
            {'participants': '["Mira", "Tim"]', 'number': '10'}],
 'intro': 'Список имён участников `participants = {participants}`, первый номер карточки `number = '
          '{number}`.',
 'steps': ['Создай функцию `card(name, number)` с двумя параметрами.',
           'Функция выводит `Card <number>: <name>`, затем черту из дефисов длиной имени.',
           'Пройди по списку циклом `for`, вызывая функцию для каждого имени.',
           'После каждого вызова увеличивай номер на 1; пустой список ничего не выводит.'],
 'hint': 'Проверь порядок аргументов и используй значения параметров функции.',
 'solution': 'def card(name, number):\n'
             '    print(f"Card {number}: {name}")\n'
             '    print("-" * len(name))\n'
             '\n'
             'for name in participants:\n'
             '    card(name, number)\n'
             '    number += 1',
 'wrong': [('не увеличивает номер',
            'def card(name, number):\n'
            '    print(f"Card {number}: {name}")\n'
            '    print("-" * len(name))\n'
            '\n'
            'for name in participants:\n'
            '    card(name, number)\n'
            '    number += 0'),
           ('черта на один символ длиннее',
            'def card(name, number):\n'
            '    print(f"Card {number}: {name}")\n'
            '    print("-" * (len(name) + 1))\n'
            '\n'
            'for name in participants:\n'
            '    card(name, number)\n'
            '    number += 1')],
 'constructs': ['function'],
 'must_use': [('FunctionDef', 'Создай и вызови свою функцию.')]}),
    OutputTask(**{'skill': 'PY_FUNCTION_BASIC',
 'difficulty': 3,
 'slug': 'py-att28-match-scoreboard',
 'title': 'Табло матча',
 'given': ['home', 'away', 'goals1', 'goals2'],
 'variants': [{'home': '"Lions"', 'away': '"Bears"', 'goals1': '3', 'goals2': '1'}],
 'hidden': [{'home': '"A"', 'away': '"B"', 'goals1': '0', 'goals2': '0'},
            {'home': '"Red"', 'away': '"Blue"', 'goals1': '1', 'goals2': '2'},
            {'home': '"X"', 'away': '"Y"', 'goals1': '5', 'goals2': '0'}],
 'intro': 'Матч: хозяева `home = {home}` забили `goals1 = {goals1}`, гости `away = {away}` забили `goals2 = '
          '{goals2}`.',
 'steps': ['Создай функцию `scoreboard(home, away, a, b)`.',
           'Внутри выведи строку `<home> <a>:<b> <away>`.',
           'Следующей строкой выведи `Home wins`, `Away wins` или `Draw` по счёту.',
           'Вызови функцию после определения, передав команды и их голы по порядку.'],
 'hint': 'Проверь порядок аргументов и используй значения параметров функции.',
 'solution': 'def scoreboard(home, away, a, b):\n'
             '    print(f"{home} {a}:{b} {away}")\n'
             '    if a > b:\n'
             '        print("Home wins")\n'
             '    elif a < b:\n'
             '        print("Away wins")\n'
             '    else:\n'
             '        print("Draw")\n'
             '\n'
             'scoreboard(home, away, goals1, goals2)',
 'wrong': [('ничья считается победой хозяев',
            'def scoreboard(home, away, a, b):\n'
            '    print(f"{home} {a}:{b} {away}")\n'
            '    if a >= b:\n'
            '        print("Home wins")\n'
            '    elif a < b:\n'
            '        print("Away wins")\n'
            '    else:\n'
            '        print("Draw")\n'
            '\n'
            'scoreboard(home, away, goals1, goals2)'),
           ('перепутаны голы команд',
            'def scoreboard(home, away, a, b):\n'
            '    print(f"{home} {a}:{b} {away}")\n'
            '    if a > b:\n'
            '        print("Home wins")\n'
            '    elif a < b:\n'
            '        print("Away wins")\n'
            '    else:\n'
            '        print("Draw")\n'
            '\n'
            'scoreboard(home, away, goals2, goals1)')],
 'constructs': ['function'],
 'must_use': [('FunctionDef', 'Создай и вызови свою функцию.')]}),
    OutputTask(**{'skill': 'PY_FUNCTION_BASIC',
 'difficulty': 3,
 'slug': 'py-att28-parcel-marking',
 'title': 'Маркировка посылок',
 'given': ['city', 'weight'],
 'variants': [{'city': '"Kazan"', 'weight': '5'}],
 'hidden': [{'city': '"Perm"', 'weight': '6'},
            {'city': '"Ufa"', 'weight': '0'},
            {'city': '"Omsk"', 'weight': '12'}],
 'intro': 'Посылка направляется в `city = {city}`, её вес `weight = {weight}` кг. Название города содержит '
          'не менее трёх букв.',
 'steps': ['Создай функцию `mark(city, weight)`.',
           'Собери этикетку из первых трёх букв города, дефиса и веса; выведи `Label: <label>`.',
           'Если вес больше 5, выведи `Heavy`, иначе `Standard`.',
           'Вызови функцию для данных посылки.'],
 'hint': 'Проверь порядок аргументов и используй значения параметров функции.',
 'solution': 'def mark(city, weight):\n'
             '    label = city[:3] + "-" + str(weight)\n'
             '    print("Label:", label)\n'
             '    if weight > 5:\n'
             '        print("Heavy")\n'
             '    else:\n'
             '        print("Standard")\n'
             '\n'
             'mark(city, weight)',
 'wrong': [('граница 5 ошибочно считается тяжёлой',
            'def mark(city, weight):\n'
            '    label = city[:3] + "-" + str(weight)\n'
            '    print("Label:", label)\n'
            '    if weight >= 5:\n'
            '        print("Heavy")\n'
            '    else:\n'
            '        print("Standard")\n'
            '\n'
            'mark(city, weight)'),
           ('в этикетке две буквы',
            'def mark(city, weight):\n'
            '    label = city[:2] + "-" + str(weight)\n'
            '    print("Label:", label)\n'
            '    if weight > 5:\n'
            '        print("Heavy")\n'
            '    else:\n'
            '        print("Standard")\n'
            '\n'
            'mark(city, weight)')],
 'constructs': ['function'],
 'must_use': [('FunctionDef', 'Создай и вызови свою функцию.')]}),
]
