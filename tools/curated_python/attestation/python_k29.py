"""Задания аттестации Python."""
from build import OutputTask

TASKS = [
    OutputTask(**{'skill': 'PY_FUNCTION_RETURN',
 'difficulty': 3,
 'slug': 'py-att29-trip-budget',
 'title': 'Бюджет поездки',
 'given': ['trips', 'fare', 'budget'],
 'variants': [{'trips': '3', 'fare': '40', 'budget': '120'}],
 'hidden': [{'trips': '0', 'fare': '50', 'budget': '0'},
            {'trips': '5', 'fare': '20', 'budget': '99'},
            {'trips': '2', 'fare': '35', 'budget': '100'}],
 'intro': 'Поездок `trips = {trips}`, цена каждой `fare = {fare}`, бюджет `budget = {budget}`.',
 'steps': ['Создай `trip_cost(count, price)`, возвращающую стоимость всех поездок.',
           'Вызови её с `trips` и `fare`, сохрани результат в `cost`.',
           'Выведи `Cost: <cost>` и `Left: <budget - cost>` на отдельных строках.',
           'Выведи `Enough`, если стоимость не больше бюджета, иначе `Not enough`.'],
 'hint': 'Проверь порядок аргументов и используй значения параметров функции.',
 'solution': 'def trip_cost(count, price):\n'
             '    return count * price\n'
             '\n'
             'cost = trip_cost(trips, fare)\n'
             'print("Cost:", cost)\n'
             'print("Left:", budget - cost)\n'
             'if cost <= budget:\n'
             '    print("Enough")\n'
             'else:\n'
             '    print("Not enough")',
 'wrong': [('граница бюджета исключена',
            'def trip_cost(count, price):\n'
            '    return count * price\n'
            '\n'
            'cost = trip_cost(trips, fare)\n'
            'print("Cost:", cost)\n'
            'print("Left:", budget - cost)\n'
            'if cost < budget:\n'
            '    print("Enough")\n'
            'else:\n'
            '    print("Not enough")'),
           ('не умножает на число поездок',
            'def trip_cost(count, price):\n'
            '    return count + price\n'
            '\n'
            'cost = trip_cost(trips, fare)\n'
            'print("Cost:", cost)\n'
            'print("Left:", budget - cost)\n'
            'if cost <= budget:\n'
            '    print("Enough")\n'
            'else:\n'
            '    print("Not enough")')],
 'constructs': ['function'],
 'must_use': [('FunctionDef', 'Создай и вызови свою функцию.'), ('Return', 'Верни результат через return.')]}),
    OutputTask(**{'skill': 'PY_FUNCTION_RETURN',
 'difficulty': 3,
 'slug': 'py-att29-tournament-points',
 'title': 'Очки турнира',
 'given': ['results'],
 'variants': [{'results': '[[2, 1], [0, 3], [1, 0]]'}],
 'hidden': [{'results': '[]'}, {'results': '[[0, 0], [1, 1]]'}, {'results': '[[4, 2]]'}],
 'intro': 'Результаты команд записаны в `results = {results}`: каждая пара — число побед и ничьих.',
 'steps': ['Создай функцию `points(wins, draws)`: она возвращает 3 очка за победу и 1 за ничью.',
           'Пройди циклом по парам в `results`, вызывая функцию для каждой пары.',
           'Для каждой команды выведи `Points: <score>` и прибавь результат к общей сумме.',
           'После цикла выведи `Total: <total>`; для пустого списка сумма равна нулю.'],
 'hint': 'Проверь порядок аргументов и используй значения параметров функции.',
 'solution': 'def points(wins, draws):\n'
             '    return wins * 3 + draws\n'
             '\n'
             'total = 0\n'
             'for result in results:\n'
             '    score = points(result[0], result[1])\n'
             '    print("Points:", score)\n'
             '    total += score\n'
             'print("Total:", total)',
 'wrong': [('за ничью дают три очка',
            'def points(wins, draws):\n'
            '    return wins + draws * 3\n'
            '\n'
            'total = 0\n'
            'for result in results:\n'
            '    score = points(result[0], result[1])\n'
            '    print("Points:", score)\n'
            '    total += score\n'
            'print("Total:", total)'),
           ('прибавляет только победы',
            'def points(wins, draws):\n'
            '    return wins * 3 + draws\n'
            '\n'
            'total = 0\n'
            'for result in results:\n'
            '    score = points(result[0], result[1])\n'
            '    print("Points:", score)\n'
            '    total += result[0]\n'
            'print("Total:", total)')],
 'constructs': ['function'],
 'must_use': [('FunctionDef', 'Создай и вызови свою функцию.'), ('Return', 'Верни результат через return.')]}),
    OutputTask(**{'skill': 'PY_FUNCTION_RETURN',
 'difficulty': 3,
 'slug': 'py-att29-basket-cost',
 'title': 'Стоимость корзины',
 'given': ['apples', 'price', 'delivery'],
 'variants': [{'apples': '4', 'price': '25', 'delivery': '30'}],
 'hidden': [{'apples': '0', 'price': '15', 'delivery': '20'},
            {'apples': '1', 'price': '99', 'delivery': '10'},
            {'apples': '5', 'price': '30', 'delivery': '20'}],
 'intro': 'Количество товаров в корзине — `apples = {apples}`, цена одного — `price = {price}` руб. Доставка `delivery = {delivery}` '
          'руб. бесплатна при стоимости товаров от 100 руб.',
 'steps': ['Создай функцию `basket_cost(count, price, delivery)`.',
           'Внутри посчитай стоимость товаров, добавь доставку только если она меньше 100, и верни итог.',
           'Вызови функцию с данными корзины и выведи `Total: <result>`.',
           'Раздели итог поровну на двоих обычным делением и выведи `Per person: <value>`.'],
 'hint': 'Проверь порядок аргументов и используй значения параметров функции.',
 'solution': 'def basket_cost(count, price, delivery):\n'
             '    total = count * price\n'
             '    if total < 100:\n'
             '        total += delivery\n'
             '    return total\n'
             '\n'
             'result = basket_cost(apples, price, delivery)\n'
             'print("Total:", result)\n'
             'print("Per person:", result / 2)',
 'wrong': [('доставка платная ровно при 100',
            'def basket_cost(count, price, delivery):\n'
            '    total = count * price\n'
            '    if total <= 100:\n'
            '        total += delivery\n'
            '    return total\n'
            '\n'
            'result = basket_cost(apples, price, delivery)\n'
            'print("Total:", result)\n'
            'print("Per person:", result / 2)'),
           ('стоимость доставки всегда прибавляется',
            'def basket_cost(count, price, delivery):\n'
            '    total = count * price\n'
            '    if total >= 0:\n'
            '        total += delivery\n'
            '    return total\n'
            '\n'
            'result = basket_cost(apples, price, delivery)\n'
            'print("Total:", result)\n'
            'print("Per person:", result / 2)')],
 'constructs': ['function'],
 'must_use': [('FunctionDef', 'Создай и вызови свою функцию.'), ('Return', 'Верни результат через return.')]}),
    OutputTask(**{'skill': 'PY_FUNCTION_RETURN',
 'difficulty': 3,
 'slug': 'py-att29-code-validation',
 'title': 'Проверка кода',
 'given': ['code', 'expected'],
 'variants': [{'code': '"AB12"', 'expected': '"AB"'}],
 'hidden': [{'code': '"AB1"', 'expected': '"AB"'},
            {'code': '"XY12"', 'expected': '"AB"'},
            {'code': '"AB00"', 'expected': '"AB"'},
            {'code': '"AB123"', 'expected': '"AB"'}],
 'intro': 'Код `code = {code}` должен состоять ровно из четырёх символов и начинаться с двухбуквенного '
          'префикса `expected = {expected}`.',
 'steps': ['Создай `valid(text, prefix)`, возвращающую `True` только если длина кода равна 4 и первые два '
           'символа совпадают с префиксом.',
           'Во всех остальных случаях функция возвращает `False`.',
           'Вызови функцию для `code` и `expected`, сохрани результат и выведи `Valid: <result>`.',
           'По результату выведи `Accepted` или `Rejected`.'],
 'hint': 'Проверь порядок аргументов и используй значения параметров функции.',
 'solution': 'def valid(text, prefix):\n'
             '    if len(text) != 4:\n'
             '        return False\n'
             '    return text[:2] == prefix\n'
             '\n'
             'result = valid(code, expected)\n'
             'print("Valid:", result)\n'
             'if result:\n'
             '    print("Accepted")\n'
             'else:\n'
             '    print("Rejected")',
 'wrong': [('не проверяет длину',
            'def valid(text, prefix):\n'
            '    if len(text) == 0:\n'
            '        return False\n'
            '    return text[:2] == prefix\n'
            '\n'
            'result = valid(code, expected)\n'
            'print("Valid:", result)\n'
            'if result:\n'
            '    print("Accepted")\n'
            'else:\n'
            '    print("Rejected")'),
           ('берёт последние два символа',
            'def valid(text, prefix):\n'
            '    if len(text) != 4:\n'
            '        return False\n'
            '    return text[-2:] == prefix\n'
            '\n'
            'result = valid(code, expected)\n'
            'print("Valid:", result)\n'
            'if result:\n'
            '    print("Accepted")\n'
            'else:\n'
            '    print("Rejected")')],
 'constructs': ['function'],
 'must_use': [('FunctionDef', 'Создай и вызови свою функцию.'), ('Return', 'Верни результат через return.')]}),
]
