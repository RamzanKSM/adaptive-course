"""PY_LIST_INDEXING — «Индексы списка». Taught before: print, variables, arithmetic, int/float, strings, type conversion,
// and %, +=, f-strings, conditions, for/while loops. Here: indexes from 0, negative indexes, len, changing an element
by index. Not yet: append, in, iterating a list, slices, string methods, functions."""
from build import OutputTask

SKILL = "PY_LIST_INDEXING"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-li-rt-podium", title="Серебро и бронза",
        given=["ranking"],
        variants=[{"ranking": '["Anya", "Boris", "Vika", "Gosha", "Dasha"]'},
                  {"ranking": '["Timur", "Mila", "Egor", "Sonya"]'},
                  {"ranking": '["Katya", "Lyova", "Nina", "Petya", "Rita", "Oleg"]'}],
        hidden=[{"ranking": '["Ira", "Gleb", "Zoya"]'},
                {"ranking": '["Max", "Eva", "Yana", "Lev", "Osya", "Fil", "Yulya"]'},
                {"ranking": '["Dina", "Artyom", "Vera", "Kira"]'}],
        intro="Олимпиада по программированию закончилась. В списке `ranking` записаны участники по местам: "
              "первый в списке занял первое место, второй — второе, и так далее. Участников не меньше трёх.",
        steps=["Выведи, кто занял второе место, в формате `Silver: Boris`",
               "Следующей строкой выведи, кто занял третье место, в формате `Bronze: Vika`"],
        hint="Индексы списка начинаются с нуля: первое место — `ranking[0]`, значит второе место — под индексом 1. "
             "Место и индекс отличаются на единицу.",
        solution='print(f"Silver: {ranking[1]}")\nprint(f"Bronze: {ranking[2]}")',
        wrong=[("считает индексы с единицы: сдвигает всех на одно место",
                'print(f"Silver: {ranking[2]}")\nprint(f"Bronze: {ranking[3]}")'),
               ("путает серебро с золотом",
                'print(f"Silver: {ranking[0]}")\nprint(f"Bronze: {ranking[1]}")')],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-li-rt-train-seats", title="Свободные места в поезде",
        given=["free", "group"],
        variants=[{"free": "[12, 5, 30, 18]", "group": "6"}, {"free": "[40, 22, 9]", "group": "9"},
                  {"free": "[3, 15, 7, 25, 14]", "group": "4"}],
        hidden=[{"free": "[10, 10]", "group": "1"}, {"free": "[8, 6, 4, 2, 20, 11]", "group": "11"},
                {"free": "[30]", "group": "12"}],
        intro="В списке `free` записано, сколько свободных мест в каждом вагоне поезда: первый элемент — первый вагон, "
              "последний — последний вагон. Группа туристов из `group` человек купила билеты в последний вагон. "
              "Вагонов может быть сколько угодно.",
        steps=["Уменьши число свободных мест в последнем вагоне на `group`. Не считай номер последнего вагона вручную — "
               "используй отрицательный индекс.",
               "Выведи весь список после этого командой `print(free)`.",
               "Следующей строкой выведи, сколько мест осталось в последнем вагоне, в формате `Last car: 12 free`"],
        hint="Элемент списка меняют так же, как переменную, в том числе через `-=`: `free[-1] -= group`. "
             "Индекс `-1` всегда указывает на последний элемент, какой бы длины ни был список.",
        solution='free[-1] -= group\nprint(free)\nprint(f"Last car: {free[-1]} free")',
        wrong=[("меняет первый вагон вместо последнего",
                'free[0] -= group\nprint(free)\nprint(f"Last car: {free[-1]} free")'),
               ("печатает список до изменения",
                'print(free)\nfree[-1] -= group\nprint(f"Last car: {free[-1]} free")'),
               ("считает разницу, но не записывает её в список",
                'print(free)\nprint(f"Last car: {free[-1] - group} free")')],
        constructs=["list"],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-li-rt-round-table", title="Соседи за круглым столом",
        given=["guests", "number"],
        variants=[{"guests": '["Anya", "Boris", "Vika", "Gosha", "Dasha"]', "number": "3"},
                  {"guests": '["Timur", "Mila", "Egor", "Sonya"]', "number": "1"},
                  {"guests": '["Katya", "Lyova", "Nina", "Petya", "Rita", "Oleg"]', "number": "6"}],
        hidden=[{"guests": '["Ira", "Gleb", "Zoya"]', "number": "2"},
                {"guests": '["Max", "Eva", "Yana", "Lev", "Osya"]', "number": "1"},
                {"guests": '["Dina", "Artyom", "Vera", "Kira"]', "number": "4"},
                {"guests": '["Fil", "Yulya", "Sasha", "Roma", "Lena", "Ilya", "Tanya"]', "number": "5"}],
        intro="Гости сидят за круглым столом. В списке `guests` они записаны по кругу: слева от каждого гостя сидит "
              "предыдущий в списке, а справа — следующий. Стол круглый, поэтому слева от первого гостя сидит последний, "
              "а справа от последнего — первый. Гость с номером `number` (номера начинаются с 1) хочет знать своих соседей.",
        steps=["Найди индекс гостя: номер минус 1.",
               "Сосед слева стоит в списке на одну позицию раньше. Для первого гостя такой индекс получится `-1` — "
               "и это как раз последний элемент списка, то есть то, что нужно.",
               "Сосед справа стоит на одну позицию позже. Чтобы после последнего гостя снова получить первого, "
               "возьми остаток от деления этого индекса на длину списка (`% len(guests)`).",
               "Выведи две строки в формате `Left: Boris` и `Right: Gosha`"],
        hint="Если индекс гостя `i`, то сосед слева — `guests[i - 1]`, а справа — `guests[(i + 1) % len(guests)]`. "
             "Без `%` для последнего гостя индекс выйдет за конец списка, и программа упадёт с ошибкой.",
        solution='i = number - 1\nprint(f"Left: {guests[i - 1]}")\nprint(f"Right: {guests[(i + 1) % len(guests)]}")',
        wrong=[("путает номер с индексом: все соседи сдвинуты на одного",
                'i = number\nprint(f"Left: {guests[i - 1]}")\nprint(f"Right: {guests[(i + 1) % len(guests)]}")'),
               ("путает левого и правого соседа",
                'i = number - 1\nprint(f"Left: {guests[(i + 1) % len(guests)]}")\nprint(f"Right: {guests[i - 1]}")')],
        constructs=["list"],
    ),
]
