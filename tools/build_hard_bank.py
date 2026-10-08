"""Builds the hard-mode task bank from Exercism problem-specifications (MIT).

Every task: a Russian statement, starter code that already reads the input, a reference solution in Java and Python,
and test cases taken from the exercise's canonical-data.json (converted to stdin/stdout). Where Exercism has fewer than
six usable cases, our own cases are added and marked origin="own". Every reference is run on every case with real
Java and Python; the canonical answer must match, otherwise the bank is not written.
"""
import json, os, subprocess, sys, tempfile, concurrent.futures as cf

# Usage: python3 tools/build_hard_bank.py <problem-specifications checkout> <output json> [java executable]
#   git clone --depth 1 https://github.com/exercism/problem-specifications.git /tmp/ps
#   python3 tools/build_hard_bank.py /tmp/ps backend/src/main/resources/hard-tasks/exercism.json
PS = os.path.join(sys.argv[1], 'exercises')
OUT = sys.argv[2]
JAVA = sys.argv[3] if len(sys.argv) > 3 else 'java'
YES, NO, ERR = 'да', 'нет', 'ошибка'


def canonical(slug):
    data = json.load(open(os.path.join(PS, slug, 'canonical-data.json')))
    def walk(node):
        out = []
        for c in node.get('cases', []):
            out += walk(c) if 'cases' in c else [c]
        return out
    cases = walk(data)
    replaced = {c.get('reimplements') for c in cases if c.get('reimplements')}
    return [c for c in cases if c['uuid'] not in replaced]


def is_error(expected):
    return isinstance(expected, dict) and 'error' in expected


def yes_no(v):
    return (YES if v else NO) + '\n'


def java_main(body, imports='import java.util.Scanner;\n'):
    return imports + '\npublic class Solution {\n    public static void main(String[] args) {\n' + body + '    }\n}\n'


READ_LONG_J = '        Scanner in = new Scanner(System.in);\n        long n = Long.parseLong(in.nextLine().trim());\n'
READ_LINE_J = '        Scanner in = new Scanner(System.in);\n        String s = in.nextLine();\n'
HERE_J = '        // Напиши решение здесь\n'
HERE_P = '# Напиши решение здесь\n'

TASKS = []


def task(slug, title, statement, java, python, convert, extra=(), public=(0, 1), dedupe=False, java_filter=None, python_filter=None):
    """java/python: (skill, difficulty, starter, reference). convert(case) -> (stdin, stdout) or None to skip."""
    TASKS.append(dict(slug=slug, title=title, statement=statement, java=java, python=python, convert=convert,
                      extra=list(extra), public=public, dedupe=dedupe, java_filter=java_filter, python_filter=python_filter))


# ───────── Conditions ─────────

task('leap', 'Високосный год',
     'В календаре, которым мы пользуемся, год високосный, если он делится на 4. Но годы, которые делятся на 100, не високосные — '
     'кроме тех, что делятся на 400. Так 1996 и 2000 — високосные, а 1900 — нет.\n\n'
     'Определи, високосный ли год.\n\n'
     '## Входные данные\nОдно целое число `year` (1 ≤ year ≤ 10000) — год. Оно уже прочитано в переменную в редакторе.\n\n'
     '## Выходные данные\nВыведи `да`, если год високосный, и `нет` — если нет.',
     ('LOGICAL_OR', 2, java_main('        Scanner in = new Scanner(System.in);\n        int year = Integer.parseInt(in.nextLine().trim());\n' + HERE_J),
      java_main('        Scanner in = new Scanner(System.in);\n        int year = Integer.parseInt(in.nextLine().trim());\n'
                '        boolean leap = year % 4 == 0 && year % 100 != 0 || year % 400 == 0;\n        System.out.println(leap ? "да" : "нет");\n')),
     ('PY_LOGICAL_OR', 2, 'year = int(input())\n\n' + HERE_P,
      'year = int(input())\nleap = year % 4 == 0 and year % 100 != 0 or year % 400 == 0\nprint("да" if leap else "нет")\n'),
     lambda c: (f"{c['input']['year']}\n", yes_no(c['expected'])), public=(2, 4))

task('darts', 'Дартс',
     'Мишень для дартса — три круга с общим центром в точке (0, 0): внутренний радиуса 1, средний радиуса 5 и внешний радиуса 10. '
     'Попадание во внутренний круг даёт 10 очков, в средний — 5, во внешний — 1, мимо мишени — 0. Точка на границе круга считается попавшей в него.\n\n'
     'Посчитай очки за бросок.\n\n'
     '## Входные данные\nДва числа `x` и `y` через пробел — координаты точки попадания (могут быть дробными). Они уже прочитаны в редакторе.\n\n'
     '## Выходные данные\nОдно целое число — очки за бросок.\n\n'
     '## Подсказка\nРасстояние до центра сравнивать удобнее в квадрате: x² + y² ≤ r².',
     ('COMPARISON_OPERATORS', 3, java_main('        Scanner in = new Scanner(System.in);\n        double x = Double.parseDouble(in.next());\n        double y = Double.parseDouble(in.next());\n' + HERE_J),
      java_main('        Scanner in = new Scanner(System.in);\n        double x = Double.parseDouble(in.next());\n        double y = Double.parseDouble(in.next());\n'
                '        double d = x * x + y * y;\n        if (d <= 1) System.out.println(10);\n        else if (d <= 25) System.out.println(5);\n'
                '        else if (d <= 100) System.out.println(1);\n        else System.out.println(0);\n')),
     ('PY_ELIF', 2, 'x, y = map(float, input().split())\n\n' + HERE_P,
      'x, y = map(float, input().split())\nd = x * x + y * y\nif d <= 1:\n    print(10)\nelif d <= 25:\n    print(5)\nelif d <= 100:\n    print(1)\nelse:\n    print(0)\n'),
     lambda c: (f"{c['input']['x']} {c['input']['y']}\n", f"{c['expected']}\n"), public=(0, 3))


def triangle_kind(a, b, c):
    if a <= 0 or b <= 0 or c <= 0 or a + b < c or b + c < a or a + c < b:
        return 'не треугольник'
    if a == b == c:
        return 'равносторонний'
    if a == b or b == c or a == c:
        return 'равнобедренный'
    return 'разносторонний'


def triangle_convert(c):
    a, b, d = c['input']['sides']
    kind = triangle_kind(a, b, d)
    claimed = {'equilateral': kind == 'равносторонний', 'isosceles': kind in ('равносторонний', 'равнобедренный'),
               'scalene': kind == 'разносторонний'}[c['property']]
    assert claimed == c['expected'], (c, kind)  # our classification agrees with every canonical property
    fmt = lambda v: str(v)
    return f"{fmt(a)} {fmt(b)} {fmt(d)}\n", kind + '\n'


task('triangle', 'Какой это треугольник',
     'Даны длины трёх отрезков. Треугольник из них существует, если все длины больше нуля и сумма любых двух не меньше третьей. '
     'Треугольник равносторонний, если все три стороны равны, равнобедренный — если равны ровно две, и разносторонний — если все разные.\n\n'
     'Определи, какой треугольник получится.\n\n'
     '## Входные данные\nТри числа через пробел — длины сторон (могут быть дробными). Они уже прочитаны в редакторе.\n\n'
     '## Выходные данные\nОдно из слов: `равносторонний`, `равнобедренный`, `разносторонний` или `не треугольник`.',
     ('LOGICAL_AND', 3, java_main('        Scanner in = new Scanner(System.in);\n        double a = Double.parseDouble(in.next());\n        double b = Double.parseDouble(in.next());\n        double c = Double.parseDouble(in.next());\n' + HERE_J),
      java_main('        Scanner in = new Scanner(System.in);\n        double a = Double.parseDouble(in.next());\n        double b = Double.parseDouble(in.next());\n        double c = Double.parseDouble(in.next());\n'
                '        if (a <= 0 || b <= 0 || c <= 0 || a + b < c || b + c < a || a + c < b) System.out.println("не треугольник");\n'
                '        else if (a == b && b == c) System.out.println("равносторонний");\n'
                '        else if (a == b || b == c || a == c) System.out.println("равнобедренный");\n'
                '        else System.out.println("разносторонний");\n')),
     ('PY_ELIF', 3, 'a, b, c = map(float, input().split())\n\n' + HERE_P,
      'a, b, c = map(float, input().split())\nif a <= 0 or b <= 0 or c <= 0 or a + b < c or b + c < a or a + c < b:\n    print("не треугольник")\n'
      'elif a == b == c:\n    print("равносторонний")\nelif a == b or b == c or a == c:\n    print("равнобедренный")\nelse:\n    print("разносторонний")\n'),
     triangle_convert, dedupe=True, public=(0, 7))

task('raindrops', 'Капли дождя',
     'Преврати число в «звук дождя». Если число делится на 3, добавь к ответу `Pling`, если делится на 5 — `Plang`, если на 7 — `Plong` (именно в таком порядке). '
     'Если число не делится ни на 3, ни на 5, ни на 7, ответом будет само число.\n\n'
     '## Входные данные\nОдно целое число `n` (1 ≤ n ≤ 10⁶). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\nОдна строка — «звук» числа.',
     ('IF_ELSE_BASIC', 3, java_main('        Scanner in = new Scanner(System.in);\n        int n = Integer.parseInt(in.nextLine().trim());\n' + HERE_J),
      java_main('        Scanner in = new Scanner(System.in);\n        int n = Integer.parseInt(in.nextLine().trim());\n        String sound = "";\n'
                '        if (n % 3 == 0) sound = sound + "Pling";\n        if (n % 5 == 0) sound = sound + "Plang";\n        if (n % 7 == 0) sound = sound + "Plong";\n'
                '        if (sound.isEmpty()) sound = "" + n;\n        System.out.println(sound);\n')),
     ('PY_IF_ELSE_BASIC', 3, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\nsound = ""\nif n % 3 == 0:\n    sound += "Pling"\nif n % 5 == 0:\n    sound += "Plang"\nif n % 7 == 0:\n    sound += "Plong"\nif sound == "":\n    sound = str(n)\nprint(sound)\n'),
     lambda c: (f"{c['input']['number']}\n", c['expected'] + '\n'), public=(1, 13))


def clock_convert(c):
    if c['property'] != 'create':
        return None
    return f"{c['input']['hour']} {c['input']['minute']}\n", c['expected'] + '\n'


task('clock', 'Часы без даты',
     'Электронные часы показывают время в формате `ЧЧ:ММ` — от `00:00` до `23:59`. Им передают часы и минуты, которые могут выходить за пределы суток '
     'и даже быть отрицательными: 25 часов — это `01:00`, а −1 минута от полуночи — `23:59`.\n\n'
     'Покажи, что будет на часах.\n\n'
     '## Входные данные\nДва целых числа через пробел: часы `h` и минуты `m` (−10⁶ ≤ h, m ≤ 10⁶). Они уже прочитаны в редакторе.\n\n'
     '## Выходные данные\nВремя в формате `ЧЧ:ММ`: часы и минуты всегда двумя цифрами.\n\n'
     '## Подсказка\nПереведи всё в минуты от полуночи и учти, что в сутках 1440 минут; остаток отрицательного числа нужно поправить.',
     ('COMPARISON_OPERATORS', 2, java_main('        Scanner in = new Scanner(System.in);\n        long h = Long.parseLong(in.next());\n        long m = Long.parseLong(in.next());\n' + HERE_J),
      java_main('        Scanner in = new Scanner(System.in);\n        long h = Long.parseLong(in.next());\n        long m = Long.parseLong(in.next());\n'
                '        long total = ((h * 60 + m) % 1440 + 1440) % 1440;\n        long hours = total / 60, minutes = total % 60;\n'
                '        String hh = hours < 10 ? "0" + hours : "" + hours;\n        String mm = minutes < 10 ? "0" + minutes : "" + minutes;\n'
                '        System.out.println(hh + ":" + mm);\n')),
     ('PY_IF_ELSE_BASIC', 2, 'h, m = map(int, input().split())\n\n' + HERE_P,
      'h, m = map(int, input().split())\ntotal = (h * 60 + m) % 1440\nhours, minutes = total // 60, total % 60\n'
      'hh = "0" + str(hours) if hours < 10 else str(hours)\nmm = "0" + str(minutes) if minutes < 10 else str(minutes)\nprint(hh + ":" + mm)\n'),
     clock_convert, public=(1, 3))

BOB = {'Sure.': 'Конечно.', 'Whoa, chill out!': 'Эй, полегче!', "Calm down, I know what I'm doing!": 'Спокойно, я знаю, что делаю!',
       'Fine. Be that way!': 'Ну и ладно!', 'Whatever.': 'Как скажешь.'}


def bob_convert(c):
    text = c['input']['heyBob']
    if '\n' in text or '\r' in text:
        return None
    return text + '\n', BOB[c['expected']] + '\n'


task('bob', 'Подросток Боб',
     'Боб — подросток, и его ответы предсказуемы:\n\n'
     '- на вопрос (фраза, которая заканчивается знаком `?`, не считая пробелов в конце) он отвечает `Конечно.`;\n'
     '- если на него кричат (в фразе есть буквы, и все они заглавные), отвечает `Эй, полегче!`;\n'
     '- на крик-вопрос отвечает `Спокойно, я знаю, что делаю!`;\n'
     '- если к нему обращаются, ничего не сказав (пустая строка или одни пробелы и табуляции), отвечает `Ну и ладно!`;\n'
     '- на всё остальное — `Как скажешь.`\n\n'
     '## Входные данные\nОдна строка — что сказали Бобу (может быть пустой). Она уже прочитана в редакторе.\n\n'
     '## Выходные данные\nОтвет Боба.',
     ('LOGICAL_OR', 3, java_main(READ_LINE_J + HERE_J),
      java_main(READ_LINE_J + '        String t = s.trim();\n        boolean question = t.endsWith("?");\n'
                '        boolean yell = !t.equals(t.toLowerCase()) && t.equals(t.toUpperCase());\n'
                '        if (t.isEmpty()) System.out.println("Ну и ладно!");\n        else if (question && yell) System.out.println("Спокойно, я знаю, что делаю!");\n'
                '        else if (yell) System.out.println("Эй, полегче!");\n        else if (question) System.out.println("Конечно.");\n        else System.out.println("Как скажешь.");\n')),
     ('PY_STRING_METHODS', 3, 's = input()\n\n' + HERE_P,
      's = input()\nt = s.strip()\nquestion = t.endswith("?")\nyell = t.isupper()\nif t == "":\n    print("Ну и ладно!")\nelif question and yell:\n'
      '    print("Спокойно, я знаю, что делаю!")\nelif yell:\n    print("Эй, полегче!")\nelif question:\n    print("Конечно.")\nelse:\n    print("Как скажешь.")\n'),
     bob_convert, public=(0, 1))

# ───────── Loops ─────────

task('collatz-conjecture', 'Гипотеза Коллатца',
     'Возьми положительное число. Если оно чётное, раздели его пополам, если нечётное — умножь на 3 и прибавь 1. Повторяй, пока не получится 1. '
     'Гипотеза Коллатца утверждает, что единица получится всегда.\n\n'
     'Посчитай, сколько шагов для этого понадобится.\n\n'
     '## Входные данные\nОдно целое число `n` (−10⁶ ≤ n ≤ 10⁶). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\nКоличество шагов до единицы. Если `n` не положительное, выведи `ошибка`.',
     ('WHILE_LOOP_BASIC', 1, java_main(READ_LONG_J + HERE_J),
      java_main(READ_LONG_J + '        if (n <= 0) { System.out.println("ошибка"); return; }\n        int steps = 0;\n'
                '        while (n != 1) { if (n % 2 == 0) n = n / 2; else n = 3 * n + 1; steps++; }\n        System.out.println(steps);\n')),
     ('PY_WHILE_LOOP_BASIC', 1, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\nif n <= 0:\n    print("ошибка")\nelse:\n    steps = 0\n    while n != 1:\n        if n % 2 == 0:\n            n = n // 2\n'
      '        else:\n            n = 3 * n + 1\n        steps += 1\n    print(steps)\n'),
     lambda c: (f"{c['input']['number']}\n", (ERR if is_error(c['expected']) else str(c['expected'])) + '\n'), public=(1, 4))

task('square-root', 'Квадратный корень без функций',
     'Найди целый квадратный корень числа, не пользуясь готовыми функциями вроде `sqrt`: такое число `r`, что `r · r` равно данному числу. '
     'Гарантируется, что число — точный квадрат.\n\n'
     '## Входные данные\nОдно целое число `n` (1 ≤ n ≤ 10⁹), точный квадрат. Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\nКорень числа.',
     ('WHILE_LOOP_BASIC', 2, java_main(READ_LONG_J + HERE_J),
      java_main(READ_LONG_J + '        long r = 0;\n        while (r * r < n) r++;\n        System.out.println(r);\n')),
     ('PY_WHILE_LOOP_BASIC', 2, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\nr = 0\nwhile r * r < n:\n    r += 1\nprint(r)\n'),
     lambda c: (f"{c['input']['radicand']}\n", f"{c['expected']}\n"),
     extra=[('1000000\n', None), ('998001\n', None)], public=(1, 3))

task('eliuds-eggs', 'Яйца в курятнике',
     'Элюд записывает, в каких гнёздах курятника лежат яйца, одним числом: в двоичной записи числа единица означает яйцо, ноль — пустое гнездо. '
     'Например, число 89 = 1011001₂ означает четыре яйца.\n\n'
     'Посчитай яйца.\n\n'
     '## Входные данные\nОдно целое число `n` (0 ≤ n ≤ 2·10⁹). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\nКоличество единиц в двоичной записи `n`.\n\n'
     '## Подсказка\nОстаток от деления на 2 — последняя двоичная цифра, а деление на 2 её отбрасывает.',
     ('LOOP_TERMINATION', 1, java_main(READ_LONG_J + HERE_J),
      java_main(READ_LONG_J + '        int eggs = 0;\n        while (n > 0) { eggs += n % 2; n = n / 2; }\n        System.out.println(eggs);\n')),
     ('PY_LOOP_TERMINATION', 1, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\neggs = 0\nwhile n > 0:\n    eggs += n % 2\n    n //= 2\nprint(eggs)\n'),
     lambda c: (f"{c['input']['number']}\n", f"{c['expected']}\n"),
     extra=[('255\n', None), ('1024\n', None), ('1023\n', None)], public=(1, 2), dedupe=True)

task('difference-of-squares', 'Разность квадратов',
     'Для числа `n` посчитай три величины: квадрат суммы чисел от 1 до `n`, сумму квадратов этих чисел и разность первого и второго. '
     'Например, для `n = 5`: (1 + 2 + 3 + 4 + 5)² = 225, 1² + 2² + 3² + 4² + 5² = 55, разность — 170.\n\n'
     '## Входные данные\nОдно целое число `n` (1 ≤ n ≤ 1000). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\nТри строки: квадрат суммы, сумма квадратов и их разность.',
     ('ACCUMULATOR_PATTERN', 1, java_main(READ_LONG_J + HERE_J),
      java_main(READ_LONG_J + '        long sum = 0, squares = 0;\n        for (long i = 1; i <= n; i++) { sum += i; squares += i * i; }\n'
                '        System.out.println(sum * sum);\n        System.out.println(squares);\n        System.out.println(sum * sum - squares);\n')),
     ('PY_ACCUMULATOR_PATTERN', 1, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\ntotal = 0\nsquares = 0\nfor i in range(1, n + 1):\n    total += i\n    squares += i * i\nprint(total * total)\nprint(squares)\nprint(total * total - squares)\n'),
     None, extra=[('1\n', None), ('5\n', None), ('100\n', None), ('2\n', None), ('10\n', None), ('1000\n', None)], public=(1, 4))


def armstrong_ok(n):
    digits = str(n)
    return sum(int(d) ** len(digits) for d in digits) == n


task('armstrong-numbers', 'Числа Армстронга',
     'Число Армстронга равно сумме своих цифр, каждая из которых возведена в степень, равную количеству цифр. '
     'Например, 153 = 1³ + 5³ + 3³ — число Армстронга, а 154 — нет.\n\n'
     'Проверь, является ли число числом Армстронга.\n\n'
     '## Входные данные\nОдно целое неотрицательное число `n`. Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\n`да` или `нет`.',
     ('ACCUMULATOR_PATTERN', 3, java_main(READ_LONG_J + HERE_J),
      java_main(READ_LONG_J + '        int digits = 0;\n        for (long t = n; t > 0; t /= 10) digits++;\n        if (n == 0) digits = 1;\n        long sum = 0;\n'
                '        for (long t = n; t > 0; t /= 10) { long d = t % 10, p = 1; for (int i = 0; i < digits; i++) p *= d; sum += p; }\n'
                '        System.out.println(sum == n ? "да" : "нет");\n')),
     ('PY_ACCUMULATOR_PATTERN', 3, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\ndigits = str(n)\ntotal = 0\nfor d in digits:\n    total += int(d) ** len(digits)\nprint("да" if total == n else "нет")\n'),
     lambda c: (f"{c['input']['number']}\n", yes_no(c['expected'])),
     java_filter=lambda stdin: int(stdin) < 10 ** 18, public=(3, 4))

task('perfect-numbers', 'Совершенные числа',
     'Сложи все делители числа, меньшие его самого (для 12 это 1 + 2 + 3 + 4 + 6 = 16). Если сумма равна числу, оно `совершенное`, '
     'если больше — `избыточное`, если меньше — `недостаточное`.\n\n'
     '## Входные данные\nОдно целое число `n` (−10⁹ ≤ n ≤ 10⁹). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\nОдно из слов `совершенное`, `избыточное`, `недостаточное`. Если `n` не положительное, выведи `ошибка`.\n\n'
     '## Подсказка\nПеребирать делители до самого `n` слишком долго для больших чисел: делители идут парами `d` и `n / d`.',
     ('ACCUMULATOR_PATTERN', 2, java_main(READ_LONG_J + HERE_J),
      java_main(READ_LONG_J + '        if (n <= 0) { System.out.println("ошибка"); return; }\n        long sum = 0;\n'
                '        for (long d = 1; d * d <= n; d++) { if (n % d == 0) { sum += d; long pair = n / d; if (pair != d) sum += pair; } }\n'
                '        sum -= n;\n        if (sum == n) System.out.println("совершенное");\n        else if (sum > n) System.out.println("избыточное");\n'
                '        else System.out.println("недостаточное");\n')),
     ('PY_ACCUMULATOR_PATTERN', 2, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\nif n <= 0:\n    print("ошибка")\nelse:\n    total = 0\n    d = 1\n    while d * d <= n:\n        if n % d == 0:\n            total += d\n'
      '            if n // d != d:\n                total += n // d\n        d += 1\n    total -= n\n    if total == n:\n        print("совершенное")\n'
      '    elif total > n:\n        print("избыточное")\n    else:\n        print("недостаточное")\n'),
     lambda c: (f"{c['input']['number']}\n", (ERR if is_error(c['expected']) else {'perfect': 'совершенное', 'abundant': 'избыточное', 'deficient': 'недостаточное'}[c['expected']]) + '\n'),
     public=(0, 3))

task('nth-prime', 'N-е простое число',
     'Простые числа — 2, 3, 5, 7, 11, 13, … Найди простое число с заданным номером: первое — 2, шестое — 13.\n\n'
     '## Входные данные\nОдно целое число `n` (0 ≤ n ≤ 10⁴). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\n`n`-е простое число. Если `n` равно 0, выведи `ошибка`.',
     ('LOOP_TERMINATION', 3, java_main(READ_LONG_J + HERE_J),
      java_main(READ_LONG_J + '        if (n < 1) { System.out.println("ошибка"); return; }\n        long count = 0, candidate = 1;\n'
                '        while (count < n) {\n            candidate++;\n            boolean prime = true;\n'
                '            for (long d = 2; d * d <= candidate; d++) { if (candidate % d == 0) { prime = false; break; } }\n'
                '            if (prime) count++;\n        }\n        System.out.println(candidate);\n')),
     ('PY_LOOP_CONTROL', 3, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\nif n < 1:\n    print("ошибка")\nelse:\n    count = 0\n    candidate = 1\n    while count < n:\n        candidate += 1\n        prime = True\n'
      '        d = 2\n        while d * d <= candidate:\n            if candidate % d == 0:\n                prime = False\n                break\n            d += 1\n'
      '        if prime:\n            count += 1\n    print(candidate)\n'),
     lambda c: (f"{c['input']['number']}\n", (ERR if is_error(c['expected']) else str(c['expected'])) + '\n'),
     extra=[('100\n', None), ('25\n', None)], public=(2, 4))

task('prime-factors', 'Разложение на простые множители',
     'Разложи число на простые множители. Например, 60 = 2 · 2 · 3 · 5.\n\n'
     '## Входные данные\nОдно целое число `n` (1 ≤ n ≤ 10¹²). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\nПростые множители в порядке возрастания через пробел, с повторениями. У числа 1 множителей нет — выведи пустую строку.\n\n'
     '## Подсказка\nДелить достаточно на числа, квадрат которых не больше оставшегося числа: то, что останется больше единицы, — тоже простой множитель.',
     ('LOOP_TERMINATION', 2, java_main(READ_LONG_J + HERE_J),
      java_main(READ_LONG_J + '        String out = "";\n        for (long d = 2; d * d <= n; d++) {\n            while (n % d == 0) { out = out.isEmpty() ? "" + d : out + " " + d; n /= d; }\n        }\n'
                '        if (n > 1) out = out.isEmpty() ? "" + n : out + " " + n;\n        System.out.println(out);\n')),
     ('PY_LOOP_TERMINATION', 3, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\nfactors = []\nd = 2\nwhile d * d <= n:\n    while n % d == 0:\n        factors.append(str(d))\n        n //= d\n    d += 1\n'
      'if n > 1:\n    factors.append(str(n))\nprint(" ".join(factors))\n'),
     lambda c: (f"{c['input']['value']}\n", ' '.join(map(str, c['expected'])) + '\n'), public=(5, 9))

task('hamming', 'Расстояние Хэмминга',
     'Две цепочки ДНК одинаковой длины сравнивают по позициям: расстояние Хэмминга — число позиций, где буквы различаются. '
     'Например, у `GAGCCTACTAACGGGAT` и `CATCGTAATGACGGCCT` оно равно 7.\n\n'
     '## Входные данные\nДве строки — цепочки ДНК (могут быть пустыми). Они уже прочитаны в редакторе.\n\n'
     '## Выходные данные\nРасстояние Хэмминга. Если длины цепочек разные, выведи `ошибка`.',
     ('FOR_LOOP_BASIC', 2, java_main('        Scanner in = new Scanner(System.in);\n        String a = in.nextLine();\n        String b = in.nextLine();\n' + HERE_J),
      java_main('        Scanner in = new Scanner(System.in);\n        String a = in.nextLine();\n        String b = in.nextLine();\n'
                '        if (a.length() != b.length()) { System.out.println("ошибка"); return; }\n        int distance = 0;\n'
                '        for (int i = 0; i < a.length(); i++) if (a.charAt(i) != b.charAt(i)) distance++;\n        System.out.println(distance);\n')),
     ('PY_FOR_RANGE', 2, 'a = input()\nb = input()\n\n' + HERE_P,
      'a = input()\nb = input()\nif len(a) != len(b):\n    print("ошибка")\nelse:\n    distance = 0\n    for i in range(len(a)):\n        if a[i] != b[i]:\n            distance += 1\n    print(distance)\n'),
     lambda c: (f"{c['input']['strand1']}\n{c['input']['strand2']}\n", (ERR if is_error(c['expected']) else str(c['expected'])) + '\n'), public=(4, 5))


def reverse_convert(c):
    v = c['input']['value']
    if v[::-1] != c['expected'] or any(ord(ch) > 0xFFFF for ch in v):
        return None  # grapheme-aware reversal (Thai marks) is beyond this task
    return v + '\n', c['expected'] + '\n'


task('reverse-string', 'Строка задом наперёд',
     'Выведи строку задом наперёд: `robot` → `tobor`.\n\n'
     '## Входные данные\nОдна строка (может быть пустой). Она уже прочитана в редакторе.\n\n'
     '## Выходные данные\nЭта строка в обратном порядке.',
     ('FOR_LOOP_BASIC', 1, java_main(READ_LINE_J + HERE_J),
      java_main(READ_LINE_J + '        String out = "";\n        for (int i = s.length() - 1; i >= 0; i--) out = out + s.charAt(i);\n        System.out.println(out);\n')),
     ('PY_STRING_SLICING', 1, 's = input()\n\n' + HERE_P, 's = input()\nprint(s[::-1])\n'),
     reverse_convert, extra=[('Привет, мир\n', None)], public=(1, 2))

SCRABBLE = {**{c: 1 for c in 'AEIOULNRST'}, **{c: 2 for c in 'DG'}, **{c: 3 for c in 'BCMP'}, **{c: 4 for c in 'FHVWY'}, 'K': 5, 'J': 8, 'X': 8, 'Q': 10, 'Z': 10}
SCRABBLE_TABLE = ('| Буквы | Очки |\n|---|---|\n| A, E, I, O, U, L, N, R, S, T | 1 |\n| D, G | 2 |\n| B, C, M, P | 3 |\n| F, H, V, W, Y | 4 |\n| K | 5 |\n| J, X | 8 |\n| Q, Z | 10 |')
task('scrabble-score', 'Очки в «Эрудите»',
     'В английской версии игры «Эрудит» (Scrabble) каждая буква приносит очки:\n\n' + SCRABBLE_TABLE + '\n\nПосчитай очки за слово. Регистр букв не важен.\n\n'
     '## Входные данные\nОдно слово из латинских букв (может быть пустым). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\nСумма очков за слово.',
     ('FOR_LOOP_BASIC', 3, java_main(READ_LINE_J + HERE_J),
      java_main(READ_LINE_J + '        String w = s.toUpperCase();\n        int score = 0;\n        for (int i = 0; i < w.length(); i++) {\n            switch (w.charAt(i)) {\n'
                '                case \'D\': case \'G\': score += 2; break;\n                case \'B\': case \'C\': case \'M\': case \'P\': score += 3; break;\n'
                '                case \'F\': case \'H\': case \'V\': case \'W\': case \'Y\': score += 4; break;\n                case \'K\': score += 5; break;\n'
                '                case \'J\': case \'X\': score += 8; break;\n                case \'Q\': case \'Z\': score += 10; break;\n                default: score += 1;\n            }\n        }\n'
                '        System.out.println(score);\n')),
     ('PY_DICT_BASIC', 1, 'word = input()\n\n' + HERE_P,
      'word = input()\npoints = {}\nfor letters, value in [("AEIOULNRST", 1), ("DG", 2), ("BCMP", 3), ("FHVWY", 4), ("K", 5), ("JX", 8), ("QZ", 10)]:\n'
      '    for letter in letters:\n        points[letter] = value\nscore = 0\nfor letter in word.upper():\n    score += points[letter]\nprint(score)\n'),
     lambda c: (c['input']['word'] + '\n', f"{c['expected']}\n"), public=(4, 6))

task('pangram', 'Панграмма',
     'Панграмма — фраза, в которой есть все 26 букв латинского алфавита, например «The quick brown fox jumps over the lazy dog». '
     'Регистр букв не важен, остальные символы не учитываются.\n\n'
     '## Входные данные\nОдна строка (может быть пустой). Она уже прочитана в редакторе.\n\n'
     '## Выходные данные\n`да`, если строка — панграмма, иначе `нет`.',
     ('LOOP_TERMINATION', 1, java_main(READ_LINE_J + HERE_J),
      java_main(READ_LINE_J + '        String t = s.toLowerCase();\n        boolean all = true;\n'
                '        for (char c = \'a\'; c <= \'z\'; c++) { if (t.indexOf(c) < 0) { all = false; break; } }\n        System.out.println(all ? "да" : "нет");\n')),
     ('PY_STRING_METHODS', 1, 's = input()\n\n' + HERE_P,
      's = input()\nt = s.lower()\nall_letters = True\nfor letter in "abcdefghijklmnopqrstuvwxyz":\n    if letter not in t:\n        all_letters = False\nprint("да" if all_letters else "нет")\n'),
     lambda c: (c['input']['sentence'] + '\n', yes_no(c['expected'])), public=(2, 4))

# ───────── Arrays, lists, strings ─────────

task('isogram', 'Изограмма',
     'Изограмма — слово или фраза, в которой ни одна буква не повторяется. Пробелы и дефисы могут встречаться сколько угодно, регистр букв не важен: '
     '`lumberjacks` и `six-year-old` — изограммы, `isograms` — нет.\n\n'
     '## Входные данные\nОдна строка из латинских букв, пробелов и дефисов (может быть пустой). Она уже прочитана в редакторе.\n\n'
     '## Выходные данные\n`да`, если это изограмма, иначе `нет`.',
     ('ARRAY_BASIC', 1, java_main(READ_LINE_J + HERE_J),
      java_main(READ_LINE_J + '        boolean[] seen = new boolean[26];\n        boolean ok = true;\n        String t = s.toLowerCase();\n'
                '        for (int i = 0; i < t.length(); i++) {\n            char c = t.charAt(i);\n            if (c < \'a\' || c > \'z\') continue;\n'
                '            if (seen[c - \'a\']) { ok = false; break; }\n            seen[c - \'a\'] = true;\n        }\n        System.out.println(ok ? "да" : "нет");\n')),
     ('PY_STRING_METHODS', 2, 's = input()\n\n' + HERE_P,
      's = input()\nletters = s.lower().replace("-", "").replace(" ", "")\nok = True\nfor i in range(len(letters)):\n    if letters[i] in letters[i + 1:]:\n        ok = False\nprint("да" if ok else "нет")\n'),
     lambda c: (c['input']['phrase'] + '\n', yes_no(c['expected'])), public=(1, 2))

task('luhn', 'Алгоритм Луна',
     'Номера банковских карт проверяют алгоритмом Луна. Пробелы в номере не учитываются; номер из одной цифры или с другими символами, кроме цифр и пробелов, неверный. '
     'Каждую вторую цифру, считая справа, удваивают; если получилось больше 9, вычитают 9. Номер верный, если сумма всех цифр после этого делится на 10.\n\n'
     '## Входные данные\nОдна строка — номер. Она уже прочитана в редакторе.\n\n'
     '## Выходные данные\n`да`, если номер верный, иначе `нет`.',
     ('ARRAY_ITERATION', 2, java_main(READ_LINE_J + HERE_J),
      java_main(READ_LINE_J + '        String digits = s.replace(" ", "");\n        boolean ok = digits.length() > 1;\n        int sum = 0;\n'
                '        for (int i = 0; i < digits.length() && ok; i++) {\n            char c = digits.charAt(digits.length() - 1 - i);\n'
                '            if (c < \'0\' || c > \'9\') { ok = false; break; }\n            int d = c - \'0\';\n            if (i % 2 == 1) { d *= 2; if (d > 9) d -= 9; }\n            sum += d;\n        }\n'
                '        System.out.println(ok && sum % 10 == 0 ? "да" : "нет");\n')),
     ('PY_LIST_ITERATION', 3, 's = input()\n\n' + HERE_P,
      's = input()\ndigits = s.replace(" ", "")\nok = len(digits) > 1 and digits.isdigit()\ntotal = 0\nif ok:\n    for i, c in enumerate(reversed(digits)):\n'
      '        d = int(c)\n        if i % 2 == 1:\n            d *= 2\n            if d > 9:\n                d -= 9\n        total += d\nprint("да" if ok and total % 10 == 0 else "нет")\n'),
     lambda c: (c['input']['value'] + '\n', yes_no(c['expected'])), public=(2, 5))

task('isbn-verifier', 'Проверка ISBN-10',
     'ISBN-10 — номер книги из 10 символов, между которыми могут стоять дефисы: `3-598-21508-8`. Первые девять символов — цифры, последний — цифра или `X` (означает 10). '
     'Номер верный, если сумма `x₁·10 + x₂·9 + … + x₁₀·1` делится на 11.\n\n'
     '## Входные данные\nОдна строка — номер. Она уже прочитана в редакторе.\n\n'
     '## Выходные данные\n`да`, если номер верный, иначе `нет`.',
     ('ARRAY_ITERATION', 3, java_main(READ_LINE_J + HERE_J),
      java_main(READ_LINE_J + '        String t = s.replace("-", "");\n        boolean ok = t.length() == 10;\n        int sum = 0;\n'
                '        for (int i = 0; i < t.length() && ok; i++) {\n            char c = t.charAt(i);\n            int v;\n'
                '            if (c >= \'0\' && c <= \'9\') v = c - \'0\';\n            else if (c == \'X\' && i == 9) v = 10;\n            else { ok = false; break; }\n            sum += v * (10 - i);\n        }\n'
                '        System.out.println(ok && sum % 11 == 0 ? "да" : "нет");\n')),
     ('PY_STRING_METHODS', 3, 's = input()\n\n' + HERE_P,
      's = input()\nt = s.replace("-", "")\nok = len(t) == 10\ntotal = 0\nif ok:\n    for i in range(10):\n        c = t[i]\n        if c.isdigit():\n            v = int(c)\n'
      '        elif c == "X" and i == 9:\n            v = 10\n        else:\n            ok = False\n            break\n        total += v * (10 - i)\nprint("да" if ok and total % 11 == 0 else "нет")\n'),
     lambda c: (c['input']['isbn'] + '\n', yes_no(c['expected'])), public=(0, 2))

task('roman-numerals', 'Римские числа',
     'Запиши число римскими цифрами: I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000. Меньшая цифра перед большей вычитается: '
     'IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900. Например, 1994 = MCMXCIV.\n\n'
     '## Входные данные\nОдно целое число `n` (1 ≤ n ≤ 3999). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\nЧисло римскими цифрами.\n\n'
     '## Подсказка\nПомогут два массива одинаковой длины: значения 1000, 900, 500, …, 1 и их записи M, CM, D, …, I.',
     ('ARRAY_INDEXING', 2, java_main('        Scanner in = new Scanner(System.in);\n        int n = Integer.parseInt(in.nextLine().trim());\n' + HERE_J),
      java_main('        Scanner in = new Scanner(System.in);\n        int n = Integer.parseInt(in.nextLine().trim());\n'
                '        int[] values = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};\n'
                '        String[] digits = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};\n'
                '        String out = "";\n        for (int i = 0; i < values.length; i++) { while (n >= values[i]) { out = out + digits[i]; n -= values[i]; } }\n'
                '        System.out.println(out);\n')),
     ('PY_LIST_INDEXING', 2, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\nvalues = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]\ndigits = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]\n'
      'out = ""\nfor i in range(len(values)):\n    while n >= values[i]:\n        out += digits[i]\n        n -= values[i]\nprint(out)\n'),
     lambda c: (f"{c['input']['number']}\n", c['expected'] + '\n'), public=(3, 20))

READ_FACTORS_J = ('        Scanner in = new Scanner(System.in);\n        int limit = Integer.parseInt(in.nextLine().trim());\n        String line = in.hasNextLine() ? in.nextLine().trim() : "";\n'
                  '        String[] parts = line.isEmpty() ? new String[0] : line.split("\\\\s+");\n        int[] factors = new int[parts.length];\n'
                  '        for (int i = 0; i < parts.length; i++) factors[i] = Integer.parseInt(parts[i]);\n')
task('sum-of-multiples', 'Сумма кратных',
     'В игре за прохождение уровня дают очки: это сумма всех различных чисел меньше заданного предела, которые кратны хотя бы одному из «волшебных» чисел. '
     'Например, при пределе 20 и числах 3 и 5 подходят 3, 5, 6, 9, 10, 12, 15, 18 — сумма 78. Число 0 среди волшебных ничего не даёт.\n\n'
     '## Входные данные\nВ первой строке — предел (1 ≤ предел ≤ 10⁵), во второй — волшебные числа через пробел (строка может быть пустой). Они уже прочитаны в редакторе.\n\n'
     '## Выходные данные\nСумма очков.',
     ('ARRAY_ITERATION', 1, java_main(READ_FACTORS_J + HERE_J),
      java_main(READ_FACTORS_J + '        long sum = 0;\n        for (int k = 1; k < limit; k++) {\n            boolean multiple = false;\n'
                '            for (int f : factors) if (f != 0 && k % f == 0) multiple = true;\n            if (multiple) sum += k;\n        }\n        System.out.println(sum);\n')),
     ('PY_LIST_ITERATION', 1, 'limit = int(input())\nfactors = [int(x) for x in input().split()]\n\n' + HERE_P,
      'limit = int(input())\nfactors = [int(x) for x in input().split()]\ntotal = 0\nfor k in range(1, limit):\n    for f in factors:\n        if f != 0 and k % f == 0:\n            total += k\n            break\nprint(total)\n'),
     lambda c: (f"{c['input']['limit']}\n{' '.join(map(str, c['input']['factors']))}\n", f"{c['expected']}\n"), public=(4, 7))

task('pascals-triangle', 'Треугольник Паскаля',
     'В треугольнике Паскаля первая строка — `1`, а каждая следующая начинается и заканчивается единицей; остальные числа — суммы двух соседних чисел над ними:\n\n'
     '```text\n1\n1 1\n1 2 1\n1 3 3 1\n```\n\nВыведи первые `n` строк треугольника.\n\n'
     '## Входные данные\nОдно целое число `n` (0 ≤ n ≤ 30). Оно уже прочитано в редакторе.\n\n'
     '## Выходные данные\n`n` строк, числа в строке через пробел. При `n = 0` ничего не выводи.',
     ('ARRAY_BASIC', 3, java_main('        Scanner in = new Scanner(System.in);\n        int n = Integer.parseInt(in.nextLine().trim());\n' + HERE_J),
      java_main('        Scanner in = new Scanner(System.in);\n        int n = Integer.parseInt(in.nextLine().trim());\n        long[] row = new long[n + 1];\n'
                '        for (int r = 0; r < n; r++) {\n            row[r] = 1;\n            for (int i = r - 1; i > 0; i--) row[i] = row[i] + row[i - 1];\n'
                '            String line = "";\n            for (int i = 0; i <= r; i++) line = i == 0 ? "" + row[i] : line + " " + row[i];\n            System.out.println(line);\n        }\n')),
     ('PY_LIST_BASIC', 3, 'n = int(input())\n\n' + HERE_P,
      'n = int(input())\nrow = []\nfor r in range(n):\n    row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + ([1] if row else [])\n    print(" ".join(str(x) for x in row))\n'),
     lambda c: (f"{c['input']['count']}\n", ''.join(' '.join(map(str, r)) + '\n' for r in c['expected'])), public=(3, 4))

task('matching-brackets', 'Парные скобки',
     'Проверь, правильно ли расставлены скобки `()`, `[]` и `{}`: каждая открывающая закрыта скобкой того же вида, и пары не пересекаются. '
     'Остальные символы не учитываются: `{[()]}` и `f(x) = [1, 2]` — правильно, `([)]` — нет.\n\n'
     '## Входные данные\nОдна строка (может быть пустой). Она уже прочитана в редакторе.\n\n'
     '## Выходные данные\n`да`, если скобки расставлены правильно, иначе `нет`.\n\n'
     '## Подсказка\nХраните ещё не закрытые скобки: закрывающая должна совпадать с последней открытой.',
     ('ARRAY_BASIC', 2, java_main(READ_LINE_J + HERE_J),
      java_main(READ_LINE_J + '        char[] stack = new char[s.length()];\n        int top = 0;\n        boolean ok = true;\n'
                '        for (int i = 0; i < s.length() && ok; i++) {\n            char c = s.charAt(i);\n            if (c == \'(\' || c == \'[\' || c == \'{\') stack[top++] = c;\n'
                '            else if (c == \')\' || c == \']\' || c == \'}\') {\n                char open = c == \')\' ? \'(\' : c == \']\' ? \'[\' : \'{\';\n'
                '                if (top == 0 || stack[top - 1] != open) ok = false; else top--;\n            }\n        }\n'
                '        System.out.println(ok && top == 0 ? "да" : "нет");\n')),
     ('PY_LIST_BASIC', 2, 's = input()\n\n' + HERE_P,
      's = input()\npairs = {")": "(", "]": "[", "}": "{"}\nstack = []\nok = True\nfor c in s:\n    if c in "([{":\n        stack.append(c)\n'
      '    elif c in ")]}":\n        if not stack or stack[-1] != pairs[c]:\n            ok = False\n            break\n        stack.pop()\nprint("да" if ok and not stack else "нет")\n'),
     lambda c: (c['input']['value'] + '\n', yes_no(c['expected'])), public=(0, 2))

task('acronym', 'Аббревиатура',
     'Составь аббревиатуру из фразы: первые буквы слов, заглавные. Слова разделяются пробелами и дефисами, знаки препинания и подчёркивания не учитываются: '
     '`Portable Network Graphics` → `PNG`, `Complementary metal-oxide semiconductor` → `CMOS`.\n\n'
     '## Входные данные\nОдна строка — фраза. Она уже прочитана в редакторе.\n\n'
     '## Выходные данные\nАббревиатура.',
     None,
     ('PY_STRING_METHODS', 2, 'phrase = input()\n\n' + HERE_P,
      'phrase = input()\nwords = phrase.replace("-", " ").replace("_", " ").split()\nout = ""\nfor word in words:\n    for c in word:\n        if c.isalpha():\n'
      '            out += c.upper()\n            break\nprint(out)\n'),
     lambda c: (c['input']['phrase'] + '\n', c['expected'] + '\n'), public=(0, 3))


# ───────── Build and verify ─────────

def run(language, source, stdin, workdir):
    path = os.path.join(workdir, 'Solution.java' if language == 'JAVA' else 'solution.py')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(source)
    cmd = [JAVA, '-Dfile.encoding=UTF-8', '-Dstdout.encoding=UTF-8', path] if language == 'JAVA' else ['python3', path]
    p = subprocess.run(cmd, input=stdin.encode('utf-8'), capture_output=True, timeout=60, env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    if p.returncode != 0:
        raise SystemExit(f'{language} reference failed on {stdin!r}: {p.stderr.decode()}')
    return p.stdout.decode('utf-8')


def build(t):
    cases, seen = [], set()
    if t['convert']:
        for c in canonical(t['slug']):
            converted = t['convert'](c)
            if converted is None:
                continue
            if converted[0] in seen:
                if t['dedupe']:
                    continue
                raise SystemExit(f"{t['slug']}: duplicate input {converted[0]!r}")
            seen.add(converted[0])
            cases.append(dict(input=converted[0], expected=converted[1], origin='exercism'))
    for stdin, expected in t['extra']:
        if stdin not in seen:
            seen.add(stdin)
            cases.append(dict(input=stdin, expected=expected, origin='own'))
    # Our own cases: the answer comes from the Python reference; the Java reference must then agree with it.
    if any(c['expected'] is None for c in cases):
        with tempfile.TemporaryDirectory() as workdir:
            for c in cases:
                if c['expected'] is None:
                    c['expected'] = run('PYTHON', t['python'][3], c['input'], workdir)
    variants = {}
    for language, spec, keep in (('JAVA', t['java'], t['java_filter']), ('PYTHON', t['python'], t['python_filter'])):
        if spec is None:
            continue
        skill, difficulty, starter, reference = spec
        own = [dict(c) for c in cases if keep is None or keep(c['input'])]
        with tempfile.TemporaryDirectory() as workdir:
            for c in own:
                actual = run(language, reference, c['input'], workdir)
                if actual != c['expected']:
                    raise SystemExit(f"{t['slug']} {language}: reference printed {actual!r}, canonical expects {c['expected']!r} for {c['input']!r}")
        publics = [own[i]['input'] for i in t['public'] if i < len(own)]
        for c in own:
            c['public'] = c['input'] in publics
        assert len(own) >= 6, (t['slug'], language, len(own))
        assert sum(c['public'] for c in own) >= 1, t['slug']
        assert len({c['expected'] for c in own}) >= 2, t['slug']
        variants[language] = dict(skill=skill, difficulty=difficulty, starter=starter, reference=reference, cases=own)
    # Python and Java see the same public examples where both have them
    return dict(slug=t['slug'], title=t['title'], statement=t['statement'], variants=variants)


def examples(variant):
    out = []
    for c in variant['cases']:
        if c['public']:
            show = c['input'] if c['input'].strip() else '(пустая строка)\n'
            out.append('Ввод:\n```text\n' + show + '```\nВывод:\n```text\n' + (c['expected'] or '\n') + '```')
    return out


with cf.ThreadPoolExecutor(8) as pool:
    built = list(pool.map(build, TASKS))
for b in built:
    for language, v in b['variants'].items():
        ex = examples(v)
        newline = 'После каждой строки вывода нужен перевод строки.' if all(c['expected'].endswith('\n') or c['expected'] == '' for c in v['cases']) else ''
        v['statement'] = (b['statement'] + '\n\n## Примеры\n\n' + '\n\n'.join(ex) + ('\n\n' + newline if newline else '')
                          + '\n\n---\n_Задача по мотивам упражнения [' + b['slug'] + '](https://github.com/exercism/problem-specifications/tree/main/exercises/' + b['slug']
                          + ') из Exercism problem-specifications (лицензия MIT); тесты основаны на его эталонных данных._')
json.dump(dict(source='https://github.com/exercism/problem-specifications', license='MIT', tasks=built), open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
total = sum(len(v['cases']) for b in built for v in b['variants'].values())
own = sum(1 for b in built for v in b['variants'].values() for c in v['cases'] if c['origin'] == 'own')
print(f"{len(built)} tasks, {sum(len(b['variants']) for b in built)} variants, {total} cases ({own} own), all references agree with Exercism")
