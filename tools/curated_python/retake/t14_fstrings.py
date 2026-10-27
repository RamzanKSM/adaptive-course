"""PY_FSTRINGS — «f-строки». Taught before: print, variables, assignment, arithmetic, order of execution, int/float,
strings, type conversion, // and %, += -=.
Not yet: format specifiers like :.2f, conditions, comparisons, loops, lists, functions."""
from build import OutputTask

SKILL = "PY_FSTRINGS"
FSTR = [("JoinedStr", "Используй f-строку: f\"...{переменная}...\"")]

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-fs-rt-library-book", title="Карточка книги",
        given=["title", "author", "pages"],
        variants=[{"title": '"The Hobbit"', "author": '"J. R. R. Tolkien"', "pages": "310"},
                  {"title": '"White Fang"', "author": '"Jack London"', "pages": "240"},
                  {"title": '"The Little Prince"', "author": '"Antoine de Saint-Exupery"', "pages": "96"}],
        hidden=[{"title": '"Matilda"', "author": '"Roald Dahl"', "pages": "232"},
                {"title": '"Short Tales"', "author": '"Anon"', "pages": "1"},
                {"title": '"Treasure Island"', "author": '"R. L. Stevenson"', "pages": "304"}],
        intro="Школьная библиотека печатает карточку для каждой книги. О книге известно: название `title = {title}`, "
              "автор `author = {author}` и число страниц `pages = {pages}`. Одну страницу школьник читает примерно за 2 минуты.",
        steps=["Каждую строку выводи через `print` с f-строкой.",
               "Выведи `Book: ` и название, затем `Author: ` и автора.",
               "Выведи `Pages: ` и число страниц.",
               "Последней строкой выведи `Reading time: `, число страниц, умноженное на 2, и ` min`. "
               "Например, для 50 страниц последние строки — `Pages: 50` и `Reading time: 100 min`."],
        hint="Не забудь букву `f` перед кавычкой: без неё Python напечатает фигурные скобки как есть. "
             "Умножение пиши прямо внутри скобок: `f\"{{pages * 2}}\"`, иначе `* 2` попадёт в текст.",
        solution='print(f"Book: {title}")\nprint(f"Author: {author}")\nprint(f"Pages: {pages}")\n'
                 'print(f"Reading time: {pages * 2} min")',
        wrong=[("забыта буква f — печатается {author}",
                'print(f"Book: {title}")\nprint("Author: {author}")\nprint(f"Pages: {pages}")\n'
                'print(f"Reading time: {pages * 2} min")'),
               ("умножение вынесено за фигурные скобки и попадает в текст",
                'print(f"Book: {title}")\nprint(f"Author: {author}")\nprint(f"Pages: {pages}")\n'
                'print(f"Reading time: {pages} * 2 min")')],
        must_use=FSTR,
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fs-rt-lesson-end", title="Когда закончится занятие",
        given=["start_h", "start_m", "length"],
        variants=[{"start_h": "8", "start_m": "30", "length": "80"}, {"start_h": "13", "start_m": "15", "length": "90"},
                  {"start_h": "10", "start_m": "40", "length": "45"}],
        hidden=[{"start_h": "9", "start_m": "10", "length": "100"}, {"start_h": "11", "start_m": "50", "length": "40"},
                {"start_h": "15", "start_m": "20", "length": "75"}],
        intro="Расписание кружка показывает начало и конец занятия. Занятие начинается в `start_h = {start_h}` ч "
              "`start_m = {start_m}` мин и длится `length = {length}` минут. В этой задаче минуты всегда двузначные, "
              "так что нули дописывать не нужно.",
        steps=["Переведи время начала в минуты от полуночи и прибавь длительность: `start_h * 60 + start_m + length`. "
               "Сохрани в переменную `end`.",
               "Посчитай час окончания `end_h` — `end`, делённое нацело на 60, и минуты `end_m` — остаток от деления на 60.",
               "С помощью f-строк выведи три строки: `Start: <start_h>:<start_m>`, `Length: <length> min` и "
               "`End: <end_h>:<end_m>`.",
               "Например, для начала в 9:20 и 70 минут программа выводит `Start: 9:20`, `Length: 70 min` и `End: 10:30`."],
        hint="В одной f-строке может быть несколько фигурных скобок: `f\"{{end_h}}:{{end_m}}\"`. "
             "Если прибавить длительность только к минутам, получится `20 + 70 = 90` минут — так часы не пишут. "
             "Поэтому сначала всё переводим в минуты, а потом раскладываем через `//` и `%`.",
        solution='end = start_h * 60 + start_m + length\nend_h = end // 60\nend_m = end % 60\n'
                 'print(f"Start: {start_h}:{start_m}")\nprint(f"Length: {length} min")\nprint(f"End: {end_h}:{end_m}")',
        wrong=[("прибавляет длительность только к минутам — минут больше 59",
                'end_h = start_h\nend_m = start_m + length\n'
                'print(f"Start: {start_h}:{start_m}")\nprint(f"Length: {length} min")\nprint(f"End: {end_h}:{end_m}")'),
               ("путает // и % — часы и минуты меняются местами",
                'end = start_h * 60 + start_m + length\nend_h = end % 60\nend_m = end // 60\n'
                'print(f"Start: {start_h}:{start_m}")\nprint(f"Length: {length} min")\nprint(f"End: {end_h}:{end_m}")'),
               ("забыта буква f в последней строке",
                'end = start_h * 60 + start_m + length\nend_h = end // 60\nend_m = end % 60\n'
                'print(f"Start: {start_h}:{start_m}")\nprint(f"Length: {length} min")\nprint("End: {end_h}:{end_m}")')],
        must_use=FSTR,
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fs-rt-electricity-bill", title="Квитанция за свет",
        given=["before", "now", "tariff"],
        variants=[{"before": "12450", "now": "12690", "tariff": "647"},
                  {"before": "3020", "now": "3175", "tariff": "598"},
                  {"before": "50812", "now": "51112", "tariff": "712"}],
        hidden=[{"before": "100", "now": "130", "tariff": "500"}, {"before": "7777", "now": "7778", "tariff": "699"},
                {"before": "20000", "now": "20450", "tariff": "633"}],
        intro="Каждый месяц семья передаёт показания счётчика электричества. В прошлом месяце счётчик показывал "
              "`before = {before}` кВт·ч, сейчас — `now = {now}`. Один кВт·ч стоит `tariff = {tariff}` копеек. "
              "В месяце 30 дней.",
        steps=["Посчитай расход за месяц `used` — `now` минус `before`.",
               "Посчитай стоимость в копейках `cost` — `used`, умноженный на `tariff`.",
               "Разложи стоимость на рубли `rub` (деление нацело на 100) и копейки `kop` (остаток от деления на 100).",
               "С помощью f-строк выведи четыре строки: `Meter: <before> -> <now>`, `Used: <used> kWh`, "
               "`Per day: <used // 30> kWh` и `To pay: <rub> rub <kop> kop`.",
               "Например, для показаний 100 и 160 при тарифе 550 программа выводит `Meter: 100 -> 160`, `Used: 60 kWh`, "
               "`Per day: 2 kWh` и `To pay: 330 rub 0 kop`."],
        hint="Внутри фигурных скобок можно писать вычисления: `f\"Per day: {{used // 30}} kWh\"`. "
             "Расход — новое показание минус старое, а не наоборот. Стоимость сначала считай в копейках, "
             "и только потом раскладывай на рубли и копейки.",
        solution='used = now - before\ncost = used * tariff\nrub = cost // 100\nkop = cost % 100\n'
                 'print(f"Meter: {before} -> {now}")\nprint(f"Used: {used} kWh")\nprint(f"Per day: {used // 30} kWh")\n'
                 'print(f"To pay: {rub} rub {kop} kop")',
        wrong=[("вычитает в обратном порядке — расход с минусом",
                'used = before - now\ncost = used * tariff\nrub = cost // 100\nkop = cost % 100\n'
                'print(f"Meter: {before} -> {now}")\nprint(f"Used: {used} kWh")\nprint(f"Per day: {used // 30} kWh")\n'
                'print(f"To pay: {rub} rub {kop} kop")'),
               ("считает тариф в рублях — сумма в 100 раз больше",
                'used = now - before\ncost = used * tariff\nrub = cost\nkop = cost % 100\n'
                'print(f"Meter: {before} -> {now}")\nprint(f"Used: {used} kWh")\nprint(f"Per day: {used // 30} kWh")\n'
                'print(f"To pay: {rub} rub {kop} kop")'),
               ("делит на дни через / — расход в день дробный",
                'used = now - before\ncost = used * tariff\nrub = cost // 100\nkop = cost % 100\n'
                'print(f"Meter: {before} -> {now}")\nprint(f"Used: {used} kWh")\nprint(f"Per day: {used / 30} kWh")\n'
                'print(f"To pay: {rub} rub {kop} kop")')],
        must_use=FSTR,
    ),
]
