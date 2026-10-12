"""PY_LOOP_CONTROL — «break и continue». Taught before: print, variables, arithmetic, strings, type conversion,
// and %, += -=, f-strings, if/elif/else, comparisons, and/or/not, truthiness, for + range, accumulator, while.
Not yet: lists, string slicing and methods, functions."""
from build import OutputTask

SKILL = "PY_LOOP_CONTROL"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-lc-skip-floor", title="Лифт без одного этажа",
        given=["floors", "skip"],
        variants=[{"floors": "7", "skip": "4"}, {"floors": "9", "skip": "6"}, {"floors": "8", "skip": "3"}],
        hidden=[{"floors": "5", "skip": "2"}, {"floors": "6", "skip": "6"}, {"floors": "10", "skip": "4"}],
        intro="В некоторых домах нет этажа с «несчастливым» номером. Кнопки в лифте нашего дома пронумерованы "
              "от 1 до `floors = {floors}`, но кнопки с номером `skip = {skip}` нет.",
        steps=["Перебери циклом `for` номера от 1 до `floors` включительно.",
               "Если номер равен `skip`, пропусти его с помощью `continue`.",
               "Каждый остальной номер выведи на отдельной строке."],
        hint="`continue` сразу переходит к следующему шагу цикла: команды, которые стоят в цикле ниже него, "
             "на этом шаге не выполняются. Поэтому проверка должна стоять перед `print`.",
        solution="for floor in range(1, floors + 1):\n    if floor == skip:\n        continue\n    print(floor)",
        wrong=[("break вместо continue: цикл обрывается на пропущенном этаже",
                "for floor in range(1, floors + 1):\n    if floor == skip:\n        break\n    print(floor)"),
               ("print стоит перед проверкой: пропущенный номер всё равно выводится",
                "for floor in range(1, floors + 1):\n    print(floor)\n    if floor == skip:\n        continue")],
        constructs=["for"],
        must_use=[("Continue", "Используй continue, чтобы пропустить этаж")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-lc-team-size", title="Равные команды",
        given=["n"],
        variants=[{"n": "15"}, {"n": "12"}, {"n": "49"}],
        hidden=[{"n": "7"}, {"n": "9"}, {"n": "10"}, {"n": "35"}],
        intro="Тренер делит `n = {n}` ребят на одинаковые команды так, чтобы никто не остался лишним. "
              "Команды должны быть как можно меньше, но в каждой — хотя бы 2 человека.",
        steps=["Перебирай размер команды циклом `for` от 2 до `n` включительно "
               "(размер `n` тоже подходит: тогда все будут в одной команде).",
               "Как только нашёлся размер, на который `n` делится без остатка, выведи его в формате `В команде: 4` "
               "и сразу останови цикл командой `break`.",
               "Программа должна вывести ровно одну строку."],
        hint="Без `break` цикл продолжит перебор и выведет все подходящие размеры. "
             "`break` выходит из цикла сразу, поэтому выведется только первый найденный — самый маленький — размер.",
        solution='for size in range(2, n + 1):\n    if n % size == 0:\n        print(f"В команде: {size}")\n        break',
        wrong=[("нет break: выводятся все подходящие размеры",
                'for size in range(2, n + 1):\n    if n % size == 0:\n        print(f"В команде: {size}")'),
               ("перебор с 1: на 1 делится любое число",
                'for size in range(1, n + 1):\n    if n % size == 0:\n        print(f"В команде: {size}")\n        break')],
        constructs=["for"],
        must_use=[("Break", "Используй break, чтобы остановить перебор, когда размер найден")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-lc-piggy-bank", title="Копилка до цели",
        given=["weekly", "goal"],
        variants=[{"weekly": "150", "goal": "500"}, {"weekly": "200", "goal": "600"}, {"weekly": "350", "goal": "1000"}],
        hidden=[{"weekly": "100", "goal": "300"}, {"weekly": "250", "goal": "1000"}, {"weekly": "400", "goal": "500"},
                {"weekly": "500", "goal": "400"}],
        intro="Маша копит на наушники за `goal = {goal}` руб. Копилка сначала пустая, "
              "а каждую неделю Маша кладёт в неё `weekly = {weekly}` руб.",
        steps=["Заведи две переменные: номер недели и сумму в копилке. Обе сначала равны 0.",
               "Запусти цикл `while True:`. В нём увеличь номер недели на 1, добавь к сумме `weekly` "
               "и выведи строку вида `Неделя 5: 900 руб.`",
               "Сразу после этого, если сумма стала не меньше `goal`, останови цикл командой `break`.",
               "После цикла выведи `Хватает на покупку!`"],
        hint="`while True` сам по себе никогда не закончится — выйти из него можно только через `break`. "
             "«Не меньше» значит «больше или равно»: если сумма ровно равна цене, денег уже хватает.",
        solution='week = 0\ntotal = 0\nwhile True:\n    week += 1\n    total += weekly\n'
                 '    print(f"Неделя {week}: {total} руб.")\n    if total >= goal:\n        break\n'
                 'print("Хватает на покупку!")',
        wrong=[("строгое сравнение: при сумме ровно goal копит лишнюю неделю",
                'week = 0\ntotal = 0\nwhile True:\n    week += 1\n    total += weekly\n'
                '    print(f"Неделя {week}: {total} руб.")\n    if total > goal:\n        break\n'
                'print("Хватает на покупку!")'),
               ("проверка стоит перед print: последняя неделя не выводится",
                'week = 0\ntotal = 0\nwhile True:\n    week += 1\n    total += weekly\n'
                '    if total >= goal:\n        break\n    print(f"Неделя {week}: {total} руб.")\n'
                'print("Хватает на покупку!")')],
        constructs=["while"],
        must_use=[("Break", "Используй break, чтобы выйти из цикла while True")],
    ),
]
