"""PY_NUMBER_TYPES — «Числа: int и float». Taught before: print (several values separated by commas), variables,
assignment, arithmetic, order of execution. Here: whole and fractional numbers, the point in 2.5, `/` always gives a
float (10 / 2 is 5.0), int with float gives float. Not yet: strings beyond literals, int()/float()/str(), round(),
// and %, += -=, f-strings, conditions, loops, functions."""
from build import OutputTask

SKILL = "PY_NUMBER_TYPES"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-nt-rt-hiking-water", title="Вода в поход",
        given=["liters", "people", "days"],
        variants=[{"liters": "1.5", "people": "4", "days": "2"}, {"liters": "2.5", "people": "3", "days": "3"},
                  {"liters": "1.75", "people": "2", "days": "4"}],
        hidden=[{"liters": "2.0", "people": "5", "days": "1"}, {"liters": "0.5", "people": "6", "days": "3"},
                {"liters": "3.25", "people": "4", "days": "2"}],
        intro="Туристы собираются в поход и считают, сколько взять воды. Одному человеку в день нужно `liters = {liters}` л, "
              "в походе `people = {people}` человек, поход длится `days = {days}` дня. Вода продаётся в бутылках по 0.5 л. "
              "Литры — дробное число (`float`), люди и дни — целые (`int`).",
        steps=["Посчитай `per_day` — сколько литров нужно всей группе за день: `liters`, умноженные на `people`.",
               "Посчитай `total` — сколько литров нужно на весь поход: `per_day`, умноженные на `days`.",
               "Посчитай `bottles` — сколько бутылок по 0.5 л это составит: `total`, делённое на 0.5.",
               "Выведи три строки: `Per day:`, `per_day` и `l`; `Total:`, `total` и `l`; `Bottles:` и `bottles`. "
               "Например, для 1.0 л на двоих на 3 дня это `Per day: 2.0 l`, `Total: 6.0 l` и `Bottles: 12.0`."],
        hint="Если в выражении есть хотя бы один `float`, результат тоже `float`: `1.0 * 2` даёт `2.0`, а не `2`. "
             "Поэтому и число бутылок выводится с точкой — так и должно быть. Дробную часть числа в Python пишут через "
             "точку: `0.5`, а не `0,5`.",
        solution='per_day = liters * people\ntotal = per_day * days\nbottles = total / 0.5\n'
                 'print("Per day:", per_day, "l")\nprint("Total:", total, "l")\nprint("Bottles:", bottles)',
        wrong=[("умножает литры на 0.5 вместо деления — бутылок выходит вчетверо меньше",
                'per_day = liters * people\ntotal = per_day * days\nbottles = total * 0.5\n'
                'print("Per day:", per_day, "l")\nprint("Total:", total, "l")\nprint("Bottles:", bottles)'),
               ("забывает умножить на число дней",
                'per_day = liters * people\ntotal = per_day\nbottles = total / 0.5\n'
                'print("Per day:", per_day, "l")\nprint("Total:", total, "l")\nprint("Bottles:", bottles)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-nt-rt-file-download", title="Скачивание файла",
        given=["size", "speed"],
        variants=[{"size": "300", "speed": "8"}, {"size": "450", "speed": "4"}, {"size": "600", "speed": "10"}],
        hidden=[{"size": "120", "speed": "16"}, {"size": "900", "speed": "25"}, {"size": "1500", "speed": "20"}],
        intro="Борис скачивает игру размером `size = {size}` МБ. Интернет качает `speed = {speed}` МБ в секунду. "
              "Нужно узнать, сколько это займёт секунд и минут, и сколько секунд ушло бы при вдвое большей скорости.",
        steps=["Посчитай `seconds` — время в секундах: `size`, делённый на `speed`.",
               "Посчитай `minutes` — то же время в минутах: `seconds`, делённые на 60. В минуте 60 секунд, а не 100.",
               "Посчитай `fast` — время в секундах, если скорость будет вдвое больше: `size`, делённый на "
               "удвоенную скорость (её возьми в скобки).",
               "Выведи три строки: `Seconds:` и `seconds`, `Minutes:` и `minutes`, `Twice as fast:` и `fast`. "
               "Например, для 60 МБ при 2 МБ/с это `Seconds: 30.0`, `Minutes: 0.5` и `Twice as fast: 15.0`."],
        hint="Деление через `/` всегда даёт `float`, даже если делится нацело: `600 / 10` — это `60.0`. "
             "В записи `size / speed * 2` деление выполнится первым, и время удвоится, а не уменьшится — "
             "поэтому пиши `size / (speed * 2)`.",
        solution='seconds = size / speed\nminutes = seconds / 60\nfast = size / (speed * 2)\n'
                 'print("Seconds:", seconds)\nprint("Minutes:", minutes)\nprint("Twice as fast:", fast)',
        wrong=[("забывает скобки — время удваивается вместо того, чтобы уменьшиться",
                'seconds = size / speed\nminutes = seconds / 60\nfast = size / speed * 2\n'
                'print("Seconds:", seconds)\nprint("Minutes:", minutes)\nprint("Twice as fast:", fast)'),
               ("переводит секунды в минуты делением на 100",
                'seconds = size / speed\nminutes = seconds / 100\nfast = size / (speed * 2)\n'
                'print("Seconds:", seconds)\nprint("Minutes:", minutes)\nprint("Twice as fast:", fast)'),
               ("делит скорость на размер",
                'seconds = speed / size\nminutes = seconds / 60\nfast = size / (speed * 2)\n'
                'print("Seconds:", seconds)\nprint("Minutes:", minutes)\nprint("Twice as fast:", fast)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-nt-rt-price-per-kg", title="Какая упаковка выгоднее",
        given=["small_kg", "small_price", "big_kg", "big_price"],
        variants=[{"small_kg": "0.75", "small_price": "240", "big_kg": "1.25", "big_price": "350"},
                  {"small_kg": "0.5", "small_price": "90", "big_kg": "2.0", "big_price": "300"},
                  {"small_kg": "1.5", "small_price": "270", "big_kg": "2.5", "big_price": "400"}],
        hidden=[{"small_kg": "0.25", "small_price": "50", "big_kg": "1.0", "big_price": "210"},
                {"small_kg": "0.75", "small_price": "150", "big_kg": "1.5", "big_price": "270"},
                {"small_kg": "1.25", "small_price": "500", "big_kg": "2.5", "big_price": "900"}],
        intro="В магазине гречка продаётся в двух упаковках: маленькая весит `small_kg = {small_kg}` кг и стоит "
              "`small_price = {small_price}` руб., большая — `big_kg = {big_kg}` кг за `big_price = {big_price}` руб. "
              "Чтобы сравнить, считают цену одного килограмма.",
        steps=["Посчитай `small_per_kg` — цену килограмма в маленькой упаковке: цена, делённая на вес.",
               "Посчитай `big_per_kg` — цену килограмма в большой упаковке.",
               "Посчитай `diff` — на сколько килограмм в маленькой упаковке дороже: `small_per_kg` минус `big_per_kg`.",
               "Выведи четыре строки: `Small:`, `small_per_kg` и `rub/kg`; `Big:`, `big_per_kg` и `rub/kg`; "
               "`Difference:` и `diff`; `Saved on 3 kg:` и `diff`, умноженная на 3. Например, для упаковок 0.5 кг за 100 "
               "и 1.0 кг за 150 это `Small: 200.0 rub/kg`, `Big: 150.0 rub/kg`, `Difference: 50.0` и `Saved on 3 kg: 150.0`."],
        hint="Цена килограмма — это рубли, делённые на килограммы: `small_price / small_kg`, а не наоборот. "
             "Деление даёт `float`, и всё, что посчитано из него, тоже будет `float`. Разница бывает и отрицательной — "
             "тогда выгоднее маленькая упаковка.",
        solution='small_per_kg = small_price / small_kg\nbig_per_kg = big_price / big_kg\ndiff = small_per_kg - big_per_kg\n'
                 'print("Small:", small_per_kg, "rub/kg")\nprint("Big:", big_per_kg, "rub/kg")\n'
                 'print("Difference:", diff)\nprint("Saved on 3 kg:", diff * 3)',
        wrong=[("сравнивает цены упаковок, а не цены килограмма",
                'small_per_kg = small_price / small_kg\nbig_per_kg = big_price / big_kg\ndiff = small_price - big_price\n'
                'print("Small:", small_per_kg, "rub/kg")\nprint("Big:", big_per_kg, "rub/kg")\n'
                'print("Difference:", diff)\nprint("Saved on 3 kg:", diff * 3)'),
               ("умножает цену на вес вместо деления",
                'small_per_kg = small_price * small_kg\nbig_per_kg = big_price * big_kg\ndiff = small_per_kg - big_per_kg\n'
                'print("Small:", small_per_kg, "rub/kg")\nprint("Big:", big_per_kg, "rub/kg")\n'
                'print("Difference:", diff)\nprint("Saved on 3 kg:", diff * 3)')],
    ),
]
