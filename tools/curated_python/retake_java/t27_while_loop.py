"""WHILE_LOOP_BASIC — «Цикл while» (Java). Taught before: println, variables, assignment, arithmetic, primitive types,
String, / and %, += -= ++, if/else, comparisons, && || !, switch, for, accumulating in a loop. The point: a loop that
repeats while a condition holds when the number of steps is not known in advance; the condition is checked before every
step, and the body must move towards the end. Not yet: break/continue (loop termination), arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "WHILE_LOOP_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-while-rt-aquarium-buckets", title="Вёдра для аквариума",
        given=[("int", "volume"), ("int", "bucket")],
        variants=[{"volume": "40", "bucket": "10"}, {"volume": "50", "bucket": "12"}, {"volume": "25", "bucket": "8"}],
        hidden=[{"volume": "5", "bucket": "10"}, {"volume": "30", "bucket": "10"}, {"volume": "31", "bucket": "10"},
                {"volume": "9", "bucket": "3"}, {"volume": "60", "bucket": "7"}],
        intro="Аня наполняет аквариум на `volume` литров, перенося воду ведром по `bucket` литров. Сначала аквариум "
              "пустой. Она носит вёдра, пока в аквариуме меньше `volume` литров.",
        steps=["Заведи две переменные со значением 0: сколько литров уже в аквариуме и сколько вёдер принесено.",
               "С помощью цикла `while` повторяй, пока воды меньше `volume`: добавь `bucket` литров, увеличь число "
               "вёдер на 1 и выведи строку `Bucket …: … l` — номер ведра и сколько литров теперь в аквариуме.",
               "После цикла выведи `The aquarium is full`."],
        hint="Условие `while` проверяется перед каждым повтором. Если воды стало ровно `volume` литров, "
             "нести ещё одно ведро уже не нужно.",
        solution='int water = 0;\nint buckets = 0;\nwhile (water < volume) {\n    water += bucket;\n    buckets++;\n'
                 '    System.out.println("Bucket " + buckets + ": " + water + " l");\n}\nSystem.out.println("The aquarium is full");',
        wrong=[("<= вместо <: при точном совпадении приносит лишнее ведро",
                'int water = 0;\nint buckets = 0;\nwhile (water <= volume) {\n    water += bucket;\n    buckets++;\n'
                '    System.out.println("Bucket " + buckets + ": " + water + " l");\n}\nSystem.out.println("The aquarium is full");'),
               ("выводит до того, как вылить ведро: в строках на ведро меньше воды",
                'int water = 0;\nint buckets = 0;\nwhile (water < volume) {\n    buckets++;\n'
                '    System.out.println("Bucket " + buckets + ": " + water + " l");\n    water += bucket;\n}\nSystem.out.println("The aquarium is full");')],
        constructs=["while"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-while-rt-headphones-sale", title="Ждём скидку на наушники",
        given=[("int", "price"), ("int", "budget")],
        variants=[{"price": "5000", "budget": "3500"}, {"price": "2400", "budget": "2000"}, {"price": "900", "budget": "1000"}],
        hidden=[{"price": "1000", "budget": "900"}, {"price": "1000", "budget": "1000"}, {"price": "8000", "budget": "2500"},
                {"price": "150", "budget": "100"}, {"price": "3000", "budget": "2700"}],
        intro="Наушники стоят `price` руб., а у Димы есть `budget` руб. Магазин каждый день снижает текущую цену на 10% "
              "(от цены на тот день, нацело). Дима ждёт, пока цена станет не больше его бюджета.",
        steps=["Заведи переменную `day` со значением 0.",
               "С помощью цикла `while` повторяй, пока `price` больше `budget`: уменьши `price` на `price / 10`, увеличь "
               "`day` на 1 и выведи строку `Day …: … rub` — номер дня и новую цену.",
               "После цикла выведи `Buy on day … for … rub` с номером дня и ценой. Если цена с самого начала подходит, "
               "цикл не выполнится ни разу, и Дима покупает в день 0."],
        hint="Скидка каждый день считается от текущей цены, поэтому она становится всё меньше. Если цена стала ровно "
             "равна бюджету, Дима уже может купить наушники.",
        solution='int day = 0;\nwhile (price > budget) {\n    price -= price / 10;\n    day++;\n'
                 '    System.out.println("Day " + day + ": " + price + " rub");\n}\n'
                 'System.out.println("Buy on day " + day + " for " + price + " rub");',
        wrong=[(">= вместо >: при цене ровно в бюджет ждёт лишний день",
                'int day = 0;\nwhile (price >= budget) {\n    price -= price / 10;\n    day++;\n'
                '    System.out.println("Day " + day + ": " + price + " rub");\n}\n'
                'System.out.println("Buy on day " + day + " for " + price + " rub");'),
               ("скидка каждый день 10% от начальной цены, а не от текущей",
                'int start = price;\nint day = 0;\nwhile (price > budget) {\n    price -= start / 10;\n    day++;\n'
                '    System.out.println("Day " + day + ": " + price + " rub");\n}\n'
                'System.out.println("Buy on day " + day + " for " + price + " rub");')],
        constructs=["while"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-while-rt-square-tiles", title="Самая большая плитка",
        given=[("int", "width"), ("int", "length")],
        variants=[{"width": "120", "length": "180"}, {"width": "42", "length": "70"}, {"width": "90", "length": "60"}],
        hidden=[{"width": "50", "length": "50"}, {"width": "30", "length": "90"}, {"width": "17", "length": "5"},
                {"width": "1", "length": "1"}, {"width": "84", "length": "36"}],
        intro="Пол в кладовке — прямоугольник `width` на `length` см. Его хотят выложить одинаковыми квадратными плитками "
              "без обрезков, и плитка должна быть как можно больше. Её сторона — наибольший общий делитель двух чисел, "
              "и найти его помогает алгоритм Евклида.",
        steps=["Заведи переменные `a`, равную `width`, и `b`, равную `length`.",
               "С помощью цикла `while` повторяй, пока `b` не равно 0: сохрани остаток `a % b` в новую переменную, "
               "потом положи в `a` значение `b`, а в `b` — сохранённый остаток.",
               "После цикла в `a` — сторона плитки. Выведи `Tile: … cm`.",
               "Следующей строкой выведи `Tiles: …` — сколько плиток понадобится: `width / a`, умноженное на `length / a`."],
        hint="Остаток нужно сохранить до того, как меняешь `a`: иначе он посчитается уже от новых чисел. "
             "Например, для 42 и 70 пары чисел меняются так: (42, 70) → (70, 42) → (42, 28) → (28, 14) → (14, 0).",
        solution='int a = width;\nint b = length;\nwhile (b != 0) {\n    int r = a % b;\n    a = b;\n    b = r;\n}\n'
                 'System.out.println("Tile: " + a + " cm");\nSystem.out.println("Tiles: " + (width / a) * (length / a));',
        wrong=[("остаток считается после того, как a уже изменилось: получается исходная длина",
                'int a = width;\nint b = length;\nwhile (b != 0) {\n    a = b;\n    b = a % b;\n}\n'
                'System.out.println("Tile: " + a + " cm");\nSystem.out.println("Tiles: " + (width / a) * (length / a));'),
               ("число плиток: площадь делится на сторону, а не на площадь плитки",
                'int a = width;\nint b = length;\nwhile (b != 0) {\n    int r = a % b;\n    a = b;\n    b = r;\n}\n'
                'System.out.println("Tile: " + a + " cm");\nSystem.out.println("Tiles: " + width * length / a);')],
        constructs=["while"],
    ),
]
