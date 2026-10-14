"""WHILE_LOOP_BASIC — «Цикл while» (Java). Taught before: println, variables, assignment, arithmetic, primitive types,
String, / and %, += -= ++, if/else, comparisons, && || !, switch, for, accumulating in a loop. The point: a loop that
repeats while a condition holds when the number of steps is not known in advance; the condition is checked before every
step, and the body must move towards the end. Not yet: break/continue (loop termination), arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "WHILE_LOOP_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-while-phone-battery", title="Пока не сядет батарея",
        given=[("int", "charge"), ("int", "drain")],
        variants=[{"charge": "100", "drain": "25"}, {"charge": "60", "drain": "15"}, {"charge": "90", "drain": "20"}],
        hidden=[{"charge": "10", "drain": "30"}, {"charge": "50", "drain": "50"}, {"charge": "35", "drain": "10"},
                {"charge": "100", "drain": "40"}, {"charge": "1", "drain": "1"}],
        intro="Телефон работает без зарядки. Сейчас его заряд — `charge` процентов, и каждый час он уменьшается "
              "на `drain` процентов.",
        steps=["Заведи переменную `level` и положи в неё значение `charge`.",
               "С помощью цикла `while` повторяй, пока `level` больше 0: выведи строку `Charge: …%` с текущим "
               "значением `level`, а потом уменьши `level` на `drain`.",
               "После цикла выведи `The phone is off`."],
        hint="Условие `while` проверяется перед каждым повтором. Когда заряд дошёл до нуля или ниже, телефон уже "
             "выключен — такой заряд выводить не нужно.",
        solution='int level = charge;\nwhile (level > 0) {\n    System.out.println("Charge: " + level + "%");\n    level -= drain;\n}\n'
                 'System.out.println("The phone is off");',
        wrong=[(">= вместо >: выводится лишняя строка «Charge: 0%»",
                'int level = charge;\nwhile (level >= 0) {\n    System.out.println("Charge: " + level + "%");\n    level -= drain;\n}\n'
                'System.out.println("The phone is off");'),
               ("заряд уменьшается до вывода: первая строка показывает заряд уже через час",
                'int level = charge;\nwhile (level > 0) {\n    level -= drain;\n    System.out.println("Charge: " + level + "%");\n}\n'
                'System.out.println("The phone is off");')],
        constructs=["while"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-while-scooter-savings", title="Копим на самокат",
        given=[("int", "price"), ("int", "weekly")],
        variants=[{"price": "1000", "weekly": "250"}, {"price": "3500", "weekly": "400"}, {"price": "700", "weekly": "1000"}],
        hidden=[{"price": "1001", "weekly": "250"}, {"price": "500", "weekly": "500"}, {"price": "1200", "weekly": "300"},
                {"price": "2900", "weekly": "600"}, {"price": "10", "weekly": "3"}],
        intro="Петя копит на самокат, который стоит `price` руб. Каждую неделю он откладывает `weekly` руб. "
              "Сначала в копилке пусто.",
        steps=["Заведи две переменные со значением 0: сколько накоплено и сколько прошло недель.",
               "С помощью цикла `while` повторяй, пока накоплено меньше `price`: добавь `weekly` к накоплениям "
               "и увеличь число недель на 1.",
               "После цикла выведи две строки: `Weeks: …` и `Saved: … rub`"],
        hint="Заранее неизвестно, сколько недель понадобится, — поэтому здесь `while`, а не `for`. "
             "Если накоплено ровно столько, сколько стоит самокат, копить дальше уже не нужно.",
        solution='int saved = 0;\nint weeks = 0;\nwhile (saved < price) {\n    saved += weekly;\n    weeks++;\n}\n'
                 'System.out.println("Weeks: " + weeks);\nSystem.out.println("Saved: " + saved + " rub");',
        wrong=[("<= вместо <: при точном совпадении копит лишнюю неделю",
                'int saved = 0;\nint weeks = 0;\nwhile (saved <= price) {\n    saved += weekly;\n    weeks++;\n}\n'
                'System.out.println("Weeks: " + weeks);\nSystem.out.println("Saved: " + saved + " rub");'),
               ("счётчик недель начинается с 1: недель на одну больше",
                'int saved = 0;\nint weeks = 1;\nwhile (saved < price) {\n    saved += weekly;\n    weeks++;\n}\n'
                'System.out.println("Weeks: " + weeks);\nSystem.out.println("Saved: " + saved + " rub");')],
        constructs=["while"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-while-digit-sum", title="Цифры номера билета",
        given=[("int", "number")],
        variants=[{"number": "4096"}, {"number": "75"}, {"number": "123456"}],
        hidden=[{"number": "7"}, {"number": "1000"}, {"number": "99999"}, {"number": "10"}, {"number": "2147483647"}],
        intro="Перед розыгрышем лотереи ведущий проверяет номер билета: сколько в нём цифр и чему равна их сумма. "
              "Номер билета — целое положительное число — записан в поле `number`.",
        steps=["Заведи переменную `rest`, равную `number`, и ещё две переменные со значением 0: для суммы цифр "
               "и для количества цифр.",
               "С помощью цикла `while` повторяй, пока `rest` больше 0: прибавь к сумме последнюю цифру `rest`, "
               "увеличь количество цифр на 1 и отбрось последнюю цифру у `rest`.",
               "После цикла выведи одну строку вида `Number 507: digits 3, sum 12` со своими значениями."],
        hint="Последнюю цифру даёт остаток от деления на 10, а целочисленное деление на 10 её отбрасывает: "
             "`4096 % 10` — это 6, а `4096 / 10` — это 409.",
        solution='int rest = number;\nint sum = 0;\nint count = 0;\nwhile (rest > 0) {\n    sum += rest % 10;\n    count++;\n'
                 '    rest /= 10;\n}\nSystem.out.println("Number " + number + ": digits " + count + ", sum " + sum);',
        wrong=[("rest > 9: самая первая цифра числа теряется",
                'int rest = number;\nint sum = 0;\nint count = 0;\nwhile (rest > 9) {\n    sum += rest % 10;\n    count++;\n'
                '    rest /= 10;\n}\nSystem.out.println("Number " + number + ": digits " + count + ", sum " + sum);'),
               ("цифра отбрасывается раньше, чем прибавляется: последняя цифра не попадает в сумму",
                'int rest = number;\nint sum = 0;\nint count = 0;\nwhile (rest > 0) {\n    rest /= 10;\n    sum += rest % 10;\n'
                '    count++;\n}\nSystem.out.println("Number " + number + ": digits " + count + ", sum " + sum);')],
        constructs=["while"],
    ),
]
