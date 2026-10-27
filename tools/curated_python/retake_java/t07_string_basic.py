"""STRING_BASIC — «Строки» (Java). Taught before: println, variables, assignment, arithmetic, execution order, primitive
types. The point: String variables, gluing with + (and that a number glued to a string becomes text), length(),
charAt (indices from 0), substring (the end is not included), indexOf, toUpperCase/toLowerCase (they return a new string).
Not yet: integer division and %, += -= ++, if/else, comparisons and equals, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "STRING_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-str-rt-pet-card", title="Карточка питомца",
        given=[("String", "petName"), ("String", "kind"), ("int", "age")],
        variants=[{"petName": '"Rex"', "kind": '"dog"', "age": "3"},
                  {"petName": '"Murka"', "kind": '"cat"', "age": "7"},
                  {"petName": '"Kesha"', "kind": '"parrot"', "age": "12"}],
        hidden=[{"petName": '"Bo"', "kind": '"hamster"', "age": "1"},
                {"petName": '"Snowball"', "kind": '"rabbit"', "age": "5"},
                {"petName": '"Tom"', "kind": '"cat"', "age": "9"}],
        intro="Ветеринарная клиника печатает карточку питомца. Кличка записана в поле `petName`, вид животного — в поле "
              "`kind`, возраст в годах — в поле `age`.",
        steps=["Заведи строку `title`: кличка, ` the ` (с пробелами по краям) и вид — например `Rex the dog`.",
               "Заведи строку `info`: кличка, ` is `, возраст и ` years old` — например `Rex is 3 years old`.",
               "Выведи `Pet: ` и `title`, затем `info`.",
               "Выведи `Next year: ` и возраст на единицу больше, затем `Name letters: ` и длину клички."],
        hint="Число, приклеенное к строке через `+`, становится текстом: `\"Age \" + 3 + 1` — это `Age 31`. "
             "Чтобы сначала сложить числа, возьми сумму в скобки. Длину строки даёт `length()`.",
        solution='String title = petName + " the " + kind;\n'
                 'String info = petName + " is " + age + " years old";\n'
                 'System.out.println("Pet: " + title);\n'
                 'System.out.println(info);\n'
                 'System.out.println("Next year: " + (age + 1));\n'
                 'System.out.println("Name letters: " + petName.length());',
        wrong=[("нет скобок: к возрасту приклеивается цифра 1",
                'String title = petName + " the " + kind;\n'
                'String info = petName + " is " + age + " years old";\n'
                'System.out.println("Pet: " + title);\n'
                'System.out.println(info);\n'
                'System.out.println("Next year: " + age + 1);\n'
                'System.out.println("Name letters: " + petName.length());'),
               ("нет пробелов вокруг the: слова слипаются",
                'String title = petName + "the" + kind;\n'
                'String info = petName + " is " + age + " years old";\n'
                'System.out.println("Pet: " + title);\n'
                'System.out.println(info);\n'
                'System.out.println("Next year: " + (age + 1));\n'
                'System.out.println("Name letters: " + petName.length());')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-str-rt-phone-format", title="Красивый номер телефона",
        given=[("String", "phone")],
        variants=[{"phone": '"89161234567"'}, {"phone": '"89035550199"'}, {"phone": '"89273408812"'}],
        hidden=[{"phone": '"80000000001"'}, {"phone": '"89998887766"'}, {"phone": '"84951234500"'}],
        intro="Номер телефона пришёл из формы одной строкой из 11 цифр, например `89161234567`, — он записан в поле `phone`. "
              "В адресной книге его нужно показать в привычном виде: `+7 (916) 123-45-67`.",
        steps=["Заведи строку `code` — код оператора: три цифры после первой (символы с номерами 1, 2, 3).",
               "Заведи строки `part1` — следующие три цифры, `part2` — следующие две и `part3` — последние две.",
               "Заведи строку `pretty`: `+7 (`, `code`, `) ` (скобка и пробел), `part1`, дефис, `part2`, дефис и `part3`.",
               "Выведи три строки: `Phone: ` и `pretty`, `Operator: ` и `code`, `First digit: ` и первый символ `phone`."],
        hint="Символы строки нумеруются с нуля. `s.substring(a, b)` берёт символы с номера `a` до номера `b`, но сам `b` "
             "не включает: `phone.substring(1, 4)` — это символы 1, 2 и 3. Первый символ строки — `phone.charAt(0)`.",
        solution='String code = phone.substring(1, 4);\n'
                 'String part1 = phone.substring(4, 7);\n'
                 'String part2 = phone.substring(7, 9);\n'
                 'String part3 = phone.substring(9, 11);\n'
                 'String pretty = "+7 (" + code + ") " + part1 + "-" + part2 + "-" + part3;\n'
                 'System.out.println("Phone: " + pretty);\n'
                 'System.out.println("Operator: " + code);\n'
                 'System.out.println("First digit: " + phone.charAt(0));',
        wrong=[("конец substring посчитан как включённый: код оператора из двух цифр",
                'String code = phone.substring(1, 3);\n'
                'String part1 = phone.substring(3, 6);\n'
                'String part2 = phone.substring(6, 8);\n'
                'String part3 = phone.substring(8, 10);\n'
                'String pretty = "+7 (" + code + ") " + part1 + "-" + part2 + "-" + part3;\n'
                'System.out.println("Phone: " + pretty);\n'
                'System.out.println("Operator: " + code);\n'
                'System.out.println("First digit: " + phone.charAt(0));'),
               ("счёт символов с единицы: charAt(1) — это вторая цифра",
                'String code = phone.substring(1, 4);\n'
                'String part1 = phone.substring(4, 7);\n'
                'String part2 = phone.substring(7, 9);\n'
                'String part3 = phone.substring(9, 11);\n'
                'String pretty = "+7 (" + code + ") " + part1 + "-" + part2 + "-" + part3;\n'
                'System.out.println("Phone: " + pretty);\n'
                'System.out.println("Operator: " + code);\n'
                'System.out.println("First digit: " + phone.charAt(1));')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-str-rt-news-preview", title="Новость в ленте",
        given=[("String", "headline"), ("String", "author")],
        variants=[{"headline": '"Kazan wins the city cup"', "author": '"Anna Petrova"'},
                  {"headline": '"Snow is coming to Sochi"', "author": '"Oleg Ivanov"'},
                  {"headline": '"Students build a robot"', "author": '"Kate Orlova"'}],
        hidden=[{"headline": '"A new park opens today"', "author": '"Li Wei"'},
                {"headline": '"Museums are free on Sunday"', "author": '"Maria Kuznetsova"'},
                {"headline": '"Trains run late tonight"', "author": '"Ivan Sokolov"'}],
        intro="Новостная лента показывает вместо длинного заголовка короткое превью и хештег. Заголовок записан в поле "
              "`headline` (в нём не меньше 10 символов и есть хотя бы один пробел), автор — в поле `author`.",
        steps=["Заведи `int space` — номер первого пробела в заголовке (метод `indexOf`).",
               "Заведи строку `firstWord` — всё, что стоит до этого пробела, и строку `tag`: `#` и `firstWord` маленькими буквами.",
               "Заведи строку `preview`: первые 10 символов заголовка и три точки `...` — например `Kazan wins...`.",
               "Выведи четыре строки: `Preview: ` и `preview`, `Tag: ` и `tag`, `By: ` и имя автора большими буквами, "
               "`Chars: ` и длину всего заголовка."],
        hint="`\"Hello world\".indexOf(\" \")` — это `5`: символы считаются с нуля, поэтому `substring(0, 5)` даёт слово без "
             "пробела. Методы `toLowerCase()` и `toUpperCase()` возвращают новую строку, а исходную не меняют.",
        solution='int space = headline.indexOf(" ");\n'
                 'String firstWord = headline.substring(0, space);\n'
                 'String tag = "#" + firstWord.toLowerCase();\n'
                 'String preview = headline.substring(0, 10) + "...";\n'
                 'System.out.println("Preview: " + preview);\n'
                 'System.out.println("Tag: " + tag);\n'
                 'System.out.println("By: " + author.toUpperCase());\n'
                 'System.out.println("Chars: " + headline.length());',
        wrong=[("первое слово взято вместе с пробелом",
                'int space = headline.indexOf(" ");\n'
                'String firstWord = headline.substring(0, space + 1);\n'
                'String tag = "#" + firstWord.toLowerCase();\n'
                'String preview = headline.substring(0, 10) + "...";\n'
                'System.out.println("Preview: " + preview);\n'
                'System.out.println("Tag: " + tag);\n'
                'System.out.println("By: " + author.toUpperCase());\n'
                'System.out.println("Chars: " + headline.length());'),
               ("toLowerCase() вызван, но результат не сохранён: в хештеге остаётся большая буква",
                'int space = headline.indexOf(" ");\n'
                'String firstWord = headline.substring(0, space);\n'
                'firstWord.toLowerCase();\n'
                'String tag = "#" + firstWord;\n'
                'String preview = headline.substring(0, 10) + "...";\n'
                'System.out.println("Preview: " + preview);\n'
                'System.out.println("Tag: " + tag);\n'
                'System.out.println("By: " + author.toUpperCase());\n'
                'System.out.println("Chars: " + headline.length());')],
        constructs=["assignment"],
    ),
]
