"""PY_ASSIGNMENT_OPERATORS — «Составное присваивание += -=». Taught before: print, variables, assignment, arithmetic,
order of execution, int/float, strings, type conversion, // and %.
Not yet: f-strings, conditions, comparisons, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_ASSIGNMENT_OPERATORS"
AUG = [("AugAssign", "Используй составное присваивание (+=, -=, *=, //=, %=), чтобы изменить переменную")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ao-rt-elevator", title="Лифт в высотке",
        given=["floor", "up", "down"],
        variants=[{"floor": "1", "up": "12", "down": "5"}, {"floor": "7", "up": "9", "down": "3"},
                  {"floor": "3", "up": "20", "down": "8"}],
        hidden=[{"floor": "1", "up": "1", "down": "0"}, {"floor": "10", "up": "15", "down": "12"},
                {"floor": "2", "up": "6", "down": "4"}],
        intro="Лифт в высотке сейчас стоит на этаже `floor = {floor}`. Сначала он поднимается на `up = {up}` этажей, "
              "потом дважды спускается — каждый раз на `down = {down}` этажей. Табло показывает этаж после каждой поездки.",
        steps=["Подними лифт: прибавь `up` к `floor` с помощью `+=` и выведи `Floor:` и этаж (через `print` с запятой).",
               "Спусти лифт: вычти `down` из `floor` с помощью `-=` и снова выведи `Floor:` и этаж.",
               "Ещё раз спусти лифт на `down` этажей и выведи `Floor:` и этаж.",
               "Например, для этажа 2, `up = 10` и `down = 3` программа выводит `Floor: 12`, `Floor: 9` и `Floor: 6`."],
        hint="`floor -= down` — короткая запись для `floor = floor - down`: из старого этажа вычитается `down`. "
             "А `floor = down` просто стёрло бы этаж, и лифт «телепортировался» бы на этаж `down`.",
        solution='floor += up\nprint("Floor:", floor)\nfloor -= down\nprint("Floor:", floor)\nfloor -= down\nprint("Floor:", floor)',
        wrong=[("спускается только один раз",
                'floor += up\nprint("Floor:", floor)\nfloor -= down\nprint("Floor:", floor)\nprint("Floor:", floor)'),
               ("пишет =- вместо -= — этаж затирается",
                'floor += up\nprint("Floor:", floor)\nfloor =- down\nprint("Floor:", floor)\nfloor -= down\nprint("Floor:", floor)'),
               ("при подъёме затирает этаж вместо прибавления",
                'floor = up\nprint("Floor:", floor)\nfloor -= down\nprint("Floor:", floor)\nfloor -= down\nprint("Floor:", floor)')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ao-rt-bacteria", title="Колония бактерий",
        given=["cells", "added"],
        variants=[{"cells": "300", "added": "50"}, {"cells": "125", "added": "1000"}, {"cells": "64", "added": "8"}],
        hidden=[{"cells": "1", "added": "0"}, {"cells": "999", "added": "3"}, {"cells": "250", "added": "750"}],
        intro="В лаборатории в чашке Петри `cells = {cells}` бактерий. Каждый час их число удваивается. Через 3 часа "
              "в чашку добавляют лекарство, и в живых остаётся только четверть бактерий (дробные бактерии не считаются). "
              "Потом лаборант подсаживает ещё `added = {added}` бактерий.",
        steps=["Три раза удвой `cells` с помощью `*=`, после каждого удвоения выводи `Hour`, номер часа и число бактерий. "
               "Например: `Hour 1: 600`. Двоеточие после номера часа — часть строки: `print(\"Hour 1:\", cells)`.",
               "Лекарство: раздели `cells` на 4 нацело с помощью `//=` и выведи `After medicine:` и число бактерий.",
               "Подсадка: прибавь `added` с помощью `+=` и выведи `Final:` и число бактерий.",
               "Например, для 10 бактерий и `added = 5` программа выводит `Hour 1: 20`, `Hour 2: 40`, `Hour 3: 80`, "
               "`After medicine: 20` и `Final: 25`."],
        hint="`x *= 2` — то же, что `x = x * 2`, а `x //= 4` — то же, что `x = x // 4`. Деление `/=` дало бы "
             "дробное число вроде `600.0`, а бактерии считают целыми — поэтому `//=`.",
        solution='cells *= 2\nprint("Hour 1:", cells)\ncells *= 2\nprint("Hour 2:", cells)\ncells *= 2\nprint("Hour 3:", cells)\n'
                 'cells //= 4\nprint("After medicine:", cells)\ncells += added\nprint("Final:", cells)',
        wrong=[("прибавляет 2 вместо удвоения",
                'cells += 2\nprint("Hour 1:", cells)\ncells += 2\nprint("Hour 2:", cells)\ncells += 2\nprint("Hour 3:", cells)\n'
                'cells //= 4\nprint("After medicine:", cells)\ncells += added\nprint("Final:", cells)'),
               ("делит через /= — число бактерий становится дробным",
                'cells *= 2\nprint("Hour 1:", cells)\ncells *= 2\nprint("Hour 2:", cells)\ncells *= 2\nprint("Hour 3:", cells)\n'
                'cells /= 4\nprint("After medicine:", cells)\ncells += added\nprint("Final:", cells)'),
               ("берёт остаток %= вместо деления",
                'cells *= 2\nprint("Hour 1:", cells)\ncells *= 2\nprint("Hour 2:", cells)\ncells *= 2\nprint("Hour 3:", cells)\n'
                'cells %= 4\nprint("After medicine:", cells)\ncells += added\nprint("Final:", cells)')],
        must_use=AUG,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ao-rt-teacher-gift", title="Сбор на подарок учителю",
        given=["anya", "boris", "vera", "gift"],
        variants=[{"anya": "500", "boris": "300", "vera": "450", "gift": "1000"},
                  {"anya": "200", "boris": "200", "vera": "350", "gift": "600"},
                  {"anya": "1000", "boris": "700", "vera": "800", "gift": "1900"}],
        hidden=[{"anya": "100", "boris": "100", "vera": "100", "gift": "300"},
                {"anya": "400", "boris": "250", "vera": "150", "gift": "500"},
                {"anya": "1000", "boris": "1000", "vera": "1001", "gift": "2000"}],
        intro="Аня, Борис и Вера собирают деньги на подарок учителю: Аня даёт `anya = {anya}` руб., Борис — "
              "`boris = {boris}` руб., Вера — `vera = {vera}` руб. Подарок стоит `gift = {gift}` руб. Оставшиеся деньги "
              "делят поровну и возвращают троим, а то, что не делится на троих без остатка, остаётся в классной копилке.",
        steps=["Заведи переменную `fund = 0` и прибавь к ней деньги каждого — тремя строками с `+=`. "
               "Выведи `Collected:` и `fund` (через `print` с запятой).",
               "Купи подарок: вычти `gift` из `fund` с помощью `-=` и выведи `After gift:` и `fund`.",
               "Посчитай `back` — сколько вернут каждому: `fund`, делённый нацело на 3.",
               "Оставь в `fund` только то, что не поделилось, с помощью `%=`.",
               "Выведи `Back to each:` и `back`, затем `Class fund:` и `fund`. Например, для 100, 100, 110 и подарка 200 "
               "программа выводит `Collected: 310`, `After gift: 110`, `Back to each: 36` и `Class fund: 2`."],
        hint="Порядок важен: `back` нужно посчитать до того, как `fund %= 3` оставит в `fund` только остаток. "
             "`110 // 3` даёт `36`, а `110 % 3` — `2`. Если написать `fund = boris`, деньги Ани пропадут — нужно именно `+=`.",
        solution='fund = 0\nfund += anya\nfund += boris\nfund += vera\nprint("Collected:", fund)\n'
                 'fund -= gift\nprint("After gift:", fund)\nback = fund // 3\nfund %= 3\n'
                 'print("Back to each:", back)\nprint("Class fund:", fund)',
        wrong=[("берёт остаток раньше, чем считает возврат",
                'fund = 0\nfund += anya\nfund += boris\nfund += vera\nprint("Collected:", fund)\n'
                'fund -= gift\nprint("After gift:", fund)\nfund %= 3\nback = fund // 3\n'
                'print("Back to each:", back)\nprint("Class fund:", fund)'),
               ("перезаписывает сумму деньгами Бориса вместо прибавления",
                'fund = 0\nfund += anya\nfund = boris\nfund += vera\nprint("Collected:", fund)\n'
                'fund -= gift\nprint("After gift:", fund)\nback = fund // 3\nfund %= 3\n'
                'print("Back to each:", back)\nprint("Class fund:", fund)'),
               ("оставляет в копилке частное //= вместо остатка",
                'fund = 0\nfund += anya\nfund += boris\nfund += vera\nprint("Collected:", fund)\n'
                'fund -= gift\nprint("After gift:", fund)\nback = fund // 3\nfund //= 3\n'
                'print("Back to each:", back)\nprint("Class fund:", fund)')],
        must_use=AUG,
    ),
]
