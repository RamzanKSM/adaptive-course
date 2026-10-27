"""PY_VARIABLE_BASIC — «Переменные». Taught before: print (several values, empty print(), sep=, end=).
The student creates own variables with a value and uses variables (also one variable several times) in print.
Not yet: changing a variable (reassignment), arithmetic, string concatenation, f-strings, conditions, loops."""
from build import OutputTask

SKILL = "PY_VARIABLE_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-var-rt-cinema-ticket", title="Билет в кино",
        given=["film", "row", "seat"],
        variants=[{"film": '"Space Cats"', "row": "7", "seat": "12"},
                  {"film": '"The Last Train"', "row": "3", "seat": "5"},
                  {"film": '"Deep Ocean"', "row": "15", "seat": "21"}],
        hidden=[{"film": '"Robot Friend"', "row": "1", "seat": "1"},
                {"film": '"Winter Tale"', "row": "10", "seat": "8"},
                {"film": '"Lost City"', "row": "22", "seat": "30"}],
        intro="Кинотеатр печатает билет. Фильм, ряд и место уже есть в заготовке: `film = {film}`, `row = {row}` и "
              "`seat = {seat}`. Номер зала программа хранит в своей переменной.",
        steps=["Создай переменную `hall` со строкой `\"Hall 2\"`.",
               "Первой строкой выведи `Movie:` и название фильма.",
               "Второй строкой выведи значение `hall`.",
               "Третьей строкой одним `print` выведи `Row`, ряд, `Seat` и место. Например: `Row 4 Seat 9`."],
        hint='Переменная создаётся так: `hall = "Hall 2"` — слева имя, справа значение. Создай её до того, '
             'как печатаешь. В последней строке четыре значения через запятую: `print("Row", row, "Seat", seat)`.',
        solution='hall = "Hall 2"\nprint("Movie:", film)\nprint(hall)\nprint("Row", row, "Seat", seat)',
        wrong=[("печатает слово hall вместо номера зала",
                'hall = "Hall 2"\nprint("Movie:", film)\nprint("hall")\nprint("Row", row, "Seat", seat)'),
               ("путает ряд и место",
                'hall = "Hall 2"\nprint("Movie:", film)\nprint(hall)\nprint("Row", seat, "Seat", row)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-var-rt-vet-card", title="Карточка в ветклинике",
        given=["pet", "owner"],
        variants=[{"pet": '"Barsik"', "owner": '"Irina Popova"'}, {"pet": '"Rex"', "owner": '"Artem Volkov"'},
                  {"pet": '"Kesha"', "owner": '"Dilyara Khan"'}],
        hidden=[{"pet": '"Murka"', "owner": '"Petr Zaitsev"'}, {"pet": '"Tuzik"', "owner": '"Sofia Gromova"'},
                {"pet": '"Pirate"', "owner": '"Ali Nazarov"'}],
        intro="Ветеринарная клиника заводит карточку на питомца. Кличка и хозяин уже есть в заготовке: `pet = {pet}` и "
              "`owner = {owner}`. Название клиники и вид животного программа хранит в своих переменных.",
        steps=["Создай переменную `clinic` со строкой `\"Happy Paws\"` и переменную `kind` со строкой `\"cat\"`.",
               "Первой строкой выведи `Clinic:` и `clinic`.",
               "Второй строкой выведи `Patient:`, кличку, `the` и `kind`. Например, для `\"Tom\"`: `Patient: Tom the cat`.",
               "Третьей строкой выведи `Owner:` и хозяина.",
               "Четвёртой строкой выведи `Get well,` и снова кличку. Например: `Get well, Tom`."],
        hint="Одну переменную можно печатать сколько угодно раз: кличка нужна и во второй, и в последней строке. "
             'Не бери имя переменной в кавычки: `print("Get well,", "pet")` выведет само слово `pet`.',
        solution='clinic = "Happy Paws"\nkind = "cat"\nprint("Clinic:", clinic)\nprint("Patient:", pet, "the", kind)\n'
                 'print("Owner:", owner)\nprint("Get well,", pet)',
        wrong=[("в последней строке печатает хозяина вместо клички",
                'clinic = "Happy Paws"\nkind = "cat"\nprint("Clinic:", clinic)\nprint("Patient:", pet, "the", kind)\n'
                'print("Owner:", owner)\nprint("Get well,", owner)'),
               ("берёт имя переменной kind в кавычки",
                'clinic = "Happy Paws"\nkind = "cat"\nprint("Clinic:", clinic)\nprint("Patient:", pet, "the", "kind")\n'
                'print("Owner:", owner)\nprint("Get well,", pet)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-var-rt-phone-number", title="Номер телефона",
        given=["code", "part1", "part2", "part3"],
        variants=[{"code": '"912"', "part1": '"345"', "part2": '"67"', "part3": '"89"'},
                  {"code": '"905"', "part1": '"100"', "part2": '"20"', "part3": '"30"'},
                  {"code": '"999"', "part1": '"812"', "part2": '"04"', "part3": '"56"'}],
        hidden=[{"code": '"917"', "part1": '"222"', "part2": '"33"', "part3": '"44"'},
                {"code": '"903"', "part1": '"007"', "part2": '"91"', "part3": '"10"'},
                {"code": '"981"', "part1": '"560"', "part2": '"78"', "part3": '"02"'}],
        intro="Телефонная книга показывает номер контакта. Части номера уже есть в заготовке: код оператора `code = {code}` "
              "и три группы цифр `part1 = {part1}`, `part2 = {part2}`, `part3 = {part3}`. Код страны и дефис программа "
              "хранит в своих переменных.",
        steps=["Создай переменную `country` со строкой `\"+7\"` и переменную `dash` со строкой `\"-\"`.",
               "Первой строкой выведи полный номер: `country`, код и три группы, например `+7 912 345-67-89`. "
               "Сделай это двумя вызовами `print`: первый выводит `country` и код и заканчивает строку пробелом "
               "(`end=\" \"`), второй выводит три группы с разделителем `sep=dash`.",
               "Второй строкой выведи `Short:` и последние цифры номера тоже двумя вызовами `print`: первый выводит "
               "`Short:` с `end=\" \"`, второй — `part2` и `part3` с разделителем `sep=dash`. "
               "Например: `Short: 67-89`.",
               "Третьей строкой выведи `Operator code:` и код."],
        hint='Значение `sep` можно взять из переменной: `print("a", "b", sep=dash)` выведет `a-b`. '
             'Между `country` и кодом нужен обычный пробел, поэтому их выводи без `sep`: `print(country, code, end=" ")`.',
        solution='country = "+7"\ndash = "-"\nprint(country, code, end=" ")\nprint(part1, part2, part3, sep=dash)\n'
                 'print("Short:", end=" ")\nprint(part2, part3, sep=dash)\nprint("Operator code:", code)',
        wrong=[("забывает end — номер разваливается на две строки",
                'country = "+7"\ndash = "-"\nprint(country, code)\nprint(part1, part2, part3, sep=dash)\n'
                'print("Short:", end=" ")\nprint(part2, part3, sep=dash)\nprint("Operator code:", code)'),
               ("в короткой записи берёт первые группы вместо последних",
                'country = "+7"\ndash = "-"\nprint(country, code, end=" ")\nprint(part1, part2, part3, sep=dash)\n'
                'print("Short:", end=" ")\nprint(part1, part2, sep=dash)\nprint("Operator code:", code)'),
               ("ставит дефис и между кодом страны и кодом оператора",
                'country = "+7"\ndash = "-"\nprint(country, code, sep=dash, end=" ")\nprint(part1, part2, part3, sep=dash)\n'
                'print("Short:", end=" ")\nprint(part2, part3, sep=dash)\nprint("Operator code:", code)')],
    ),
]
