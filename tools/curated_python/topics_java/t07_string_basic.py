"""STRING_BASIC — «Строки» (Java). Taught before: println, variables, assignment, arithmetic, execution order, primitive
types. The point: String variables, gluing with + (and that a number glued to a string becomes text), length(),
charAt (indices from 0), substring (the end is not included), indexOf, toUpperCase/toLowerCase (they return a new string).
Not yet: integer division and %, += -= ++, if/else, comparisons and equals, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "STRING_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-str-conference-badge", title="Бейдж участника конференции",
        given=[("String", "firstName"), ("String", "lastName"), ("String", "city")],
        variants=[{"firstName": '"Anna"', "lastName": '"Petrova"', "city": '"Kazan"'},
                  {"firstName": '"Boris"', "lastName": '"Ivanov"', "city": '"Sochi"'},
                  {"firstName": '"Elena"', "lastName": '"Smirnova"', "city": '"Omsk"'}],
        hidden=[{"firstName": '"Ian"', "lastName": '"Li"', "city": '"Ufa"'},
                {"firstName": '"Maria"', "lastName": '"Kuznetsova"', "city": '"Saint Petersburg"'},
                {"firstName": '"Oleg"', "lastName": '"Orlov"', "city": '"Tver"'}],
        intro="Организаторы конференции печатают бейджи. Имя участника записано в поле `firstName`, фамилия — в поле "
              "`lastName`, город — в поле `city`.",
        steps=["Заведи строку `fullName`: имя, пробел и фамилия, например `Anna Petrova`.",
               "Заведи строку `badge`: `fullName`, пробел и город в круглых скобках, например `Anna Petrova (Kazan)`.",
               "Выведи `Name: ` и `fullName`, затем `Badge: ` и `badge`.",
               "Последней строкой выведи `Length: ` и длину строки `fullName` (пробел тоже считается)."],
        hint="Строки склеиваются через `+`, а пробел между словами надо добавить самому: `a + \" \" + b`. "
             "Длину строки возвращает метод `length()`: `\"Hi there\".length()` — это `8`.",
        solution='String fullName = firstName + " " + lastName;\n'
                 'String badge = fullName + " (" + city + ")";\n'
                 'System.out.println("Name: " + fullName);\n'
                 'System.out.println("Badge: " + badge);\n'
                 'System.out.println("Length: " + fullName.length());',
        wrong=[("нет пробела между именем и фамилией",
                'String fullName = firstName + lastName;\n'
                'String badge = fullName + " (" + city + ")";\n'
                'System.out.println("Name: " + fullName);\n'
                'System.out.println("Badge: " + badge);\n'
                'System.out.println("Length: " + fullName.length());'),
               ("имя переменной в кавычках: печатается слово city, а не город",
                'String fullName = firstName + " " + lastName;\n'
                'String badge = fullName + " (" + "city" + ")";\n'
                'System.out.println("Name: " + fullName);\n'
                'System.out.println("Badge: " + badge);\n'
                'System.out.println("Length: " + fullName.length());')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-str-bookshop-receipt", title="Чек книжного магазина",
        given=[("String", "title"), ("int", "books"), ("int", "gifts"), ("int", "price")],
        variants=[{"title": '"Dune"', "books": "2", "gifts": "1", "price": "450"},
                  {"title": '"Emma"', "books": "3", "gifts": "2", "price": "300"},
                  {"title": '"Ulysses"', "books": "1", "gifts": "1", "price": "720"}],
        hidden=[{"title": '"It"', "books": "5", "gifts": "0", "price": "100"},
                {"title": '"Hamlet"', "books": "4", "gifts": "3", "price": "250"},
                {"title": '"Moby Dick"', "books": "10", "gifts": "5", "price": "99"}],
        intro="Книжный магазин проводит акцию: к купленным книгам дарят ещё несколько таких же. Название книги — поле "
              "`title`, сколько книг купили — поле `books`, сколько подарили — поле `gifts`, цена одной книги — поле `price`.",
        steps=["Заведи строку `header`: `Book: ` и название книги.",
               "Заведи `int total` — сумма к оплате: `books` умножить на `price` (подарки бесплатные).",
               "Выведи `header`, затем `Paid books: ` и `books`, затем `Free books: ` и `gifts`.",
               "Выведи `Books in bag: ` и сколько книг всего в пакете (купленные плюс подарки).",
               "Последней строкой выведи `To pay: `, сумму и ` rub`."],
        hint="Java читает `+` слева направо: `\"Sum: \" + 2 + 1` — это сначала строка `Sum: 2`, а потом `Sum: 21`. "
             "Чтобы числа сначала сложились, возьми их сумму в скобки: `\"Sum: \" + (2 + 1)`.",
        solution='String header = "Book: " + title;\n'
                 'int total = books * price;\n'
                 'System.out.println(header);\n'
                 'System.out.println("Paid books: " + books);\n'
                 'System.out.println("Free books: " + gifts);\n'
                 'System.out.println("Books in bag: " + (books + gifts));\n'
                 'System.out.println("To pay: " + total + " rub");',
        wrong=[("нет скобок: числа приклеиваются к строке, а не складываются",
                'String header = "Book: " + title;\n'
                'int total = books * price;\n'
                'System.out.println(header);\n'
                'System.out.println("Paid books: " + books);\n'
                'System.out.println("Free books: " + gifts);\n'
                'System.out.println("Books in bag: " + books + gifts);\n'
                'System.out.println("To pay: " + total + " rub");'),
               ("имя переменной в кавычках: печатается слово title, а не название",
                'String header = "Book: " + "title";\n'
                'int total = books * price;\n'
                'System.out.println(header);\n'
                'System.out.println("Paid books: " + books);\n'
                'System.out.println("Free books: " + gifts);\n'
                'System.out.println("Books in bag: " + (books + gifts));\n'
                'System.out.println("To pay: " + total + " rub");')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-str-school-login", title="Логин для школьного портала",
        given=[("String", "firstName"), ("String", "lastName")],
        variants=[{"firstName": '"Anna"', "lastName": '"Petrova"'}, {"firstName": '"Boris"', "lastName": '"Ivanov"'},
                  {"firstName": '"Elena"', "lastName": '"Smirnova"'}],
        hidden=[{"firstName": '"Ian"', "lastName": '"Li"'}, {"firstName": '"Maria"', "lastName": '"Kuznetsova"'},
                {"firstName": '"Gleb"', "lastName": '"Orlov"'}],
        intro="Школьный портал заводит ученику учётную запись. Имя ученика — поле `firstName`, фамилия — поле `lastName`. "
              "Логин составляют из первой буквы имени и фамилии, маленькими буквами.",
        steps=["Заведи строку `initials`: первая буква имени, точка, первая буква фамилии, точка — например `A.P.`.",
               "Заведи строку `login`: первая буква имени и сразу фамилия — например `APetrova`.",
               "Следующей строкой кода сделай `login` маленькими буквами: `login = login.toLowerCase();`.",
               "Заведи `int letters` — сколько букв в имени и фамилии вместе.",
               "Выведи три строки: `Initials: ` и `initials`, `Login: ` и `login`, `Letters: ` и `letters`."],
        hint="Символы строки нумеруются с нуля: первая буква — `name.charAt(0)`. Метод `toLowerCase()` не меняет "
             "саму строку, а возвращает новую — её нужно снова записать в переменную.",
        solution='String initials = firstName.charAt(0) + "." + lastName.charAt(0) + ".";\n'
                 'String login = firstName.charAt(0) + lastName;\n'
                 'login = login.toLowerCase();\n'
                 'int letters = firstName.length() + lastName.length();\n'
                 'System.out.println("Initials: " + initials);\n'
                 'System.out.println("Login: " + login);\n'
                 'System.out.println("Letters: " + letters);',
        wrong=[("toLowerCase() вызван, но результат не сохранён: логин остаётся с большими буквами",
                'String initials = firstName.charAt(0) + "." + lastName.charAt(0) + ".";\n'
                'String login = firstName.charAt(0) + lastName;\n'
                'login.toLowerCase();\n'
                'int letters = firstName.length() + lastName.length();\n'
                'System.out.println("Initials: " + initials);\n'
                'System.out.println("Login: " + login);\n'
                'System.out.println("Letters: " + letters);'),
               ("счёт символов с единицы: charAt(1) — это вторая буква",
                'String initials = firstName.charAt(1) + "." + lastName.charAt(1) + ".";\n'
                'String login = firstName.charAt(0) + lastName;\n'
                'login = login.toLowerCase();\n'
                'int letters = firstName.length() + lastName.length();\n'
                'System.out.println("Initials: " + initials);\n'
                'System.out.println("Login: " + login);\n'
                'System.out.println("Letters: " + letters);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-str-card-mask", title="Номер карты на чеке",
        given=[("String", "card")],
        variants=[{"card": '"4276123456781234"'}, {"card": '"220012345678901234"'}, {"card": '"5536913887654321"'}],
        hidden=[{"card": '"1234567890123456789"'}, {"card": '"5555444433332222"'}, {"card": '"98761234567"'}],
        intro="На кассовом чеке номер банковской карты печатают не полностью: видны только первые 4 и последние 4 цифры. "
              "Номер карты записан строкой в поле `card`; у разных карт номер бывает разной длины.",
        steps=["Заведи `int length` — длину номера.",
               "Заведи строку `first4` — первые четыре цифры номера.",
               "Заведи строку `last4` — последние четыре цифры номера (посчитай, откуда они начинаются, через `length`).",
               "Заведи строку `masked`: `first4`, затем ` **** ` (пробел, четыре звёздочки, пробел) и `last4`.",
               "Выведи две строки: `Digits: ` и длину, затем `Card: ` и `masked`."],
        hint="`s.substring(a, b)` берёт символы с номера `a` до номера `b`, но сам символ `b` не включает: "
             "`\"abcdef\".substring(0, 2)` — это `ab`. А `s.substring(a)` берёт всё с номера `a` до конца строки.",
        solution='int length = card.length();\n'
                 'String first4 = card.substring(0, 4);\n'
                 'String last4 = card.substring(length - 4);\n'
                 'String masked = first4 + " **** " + last4;\n'
                 'System.out.println("Digits: " + length);\n'
                 'System.out.println("Card: " + masked);',
        wrong=[("начало с 1: первая цифра пропадает, берутся только три",
                'int length = card.length();\n'
                'String first4 = card.substring(1, 4);\n'
                'String last4 = card.substring(length - 4);\n'
                'String masked = first4 + " **** " + last4;\n'
                'System.out.println("Digits: " + length);\n'
                'System.out.println("Card: " + masked);'),
               ("конец указан как length - 1: последняя цифра не попадает",
                'int length = card.length();\n'
                'String first4 = card.substring(0, 4);\n'
                'String last4 = card.substring(length - 4, length - 1);\n'
                'String masked = first4 + " **** " + last4;\n'
                'System.out.println("Digits: " + length);\n'
                'System.out.println("Card: " + masked);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-str-file-backup", title="Резервная копия файла",
        given=[("String", "fileName")],
        variants=[{"fileName": '"report.pdf"'}, {"fileName": '"holiday_photo.jpeg"'}, {"fileName": '"notes.txt"'}],
        hidden=[{"fileName": '"a.b"'}, {"fileName": '"presentation.pptx"'}, {"fileName": '"x1.py"'}, {"fileName": '"budget2026.xlsx"'}],
        intro="Программа делает резервную копию файла и должна придумать копии имя. Имя файла записано в поле "
              "`fileName`; в нём ровно одна точка — она отделяет название от расширения.",
        steps=["Заведи `int dot` — номер символа точки в `fileName` (метод `indexOf`).",
               "Заведи строку `name` — всё, что до точки, и строку `extension` — всё, что после точки (без самой точки).",
               "Заведи строку `backup`: `name`, затем `_copy.` и `extension` — например `report_copy.pdf`.",
               "Выведи четыре строки: `Name: ` и `name`, `Extension: ` и расширение большими буквами, "
               "`Backup: ` и `backup`, `Name length: ` и длину `name`."],
        hint="`\"photo.png\".indexOf(\".\")` — это `5`: символы считаются с нуля. Значит, название — это "
             "`substring(0, dot)` (точка не входит), а расширение начинается на один символ дальше точки.",
        solution='int dot = fileName.indexOf(".");\n'
                 'String name = fileName.substring(0, dot);\n'
                 'String extension = fileName.substring(dot + 1);\n'
                 'String backup = name + "_copy." + extension;\n'
                 'System.out.println("Name: " + name);\n'
                 'System.out.println("Extension: " + extension.toUpperCase());\n'
                 'System.out.println("Backup: " + backup);\n'
                 'System.out.println("Name length: " + name.length());',
        wrong=[("расширение взято вместе с точкой",
                'int dot = fileName.indexOf(".");\n'
                'String name = fileName.substring(0, dot);\n'
                'String extension = fileName.substring(dot);\n'
                'String backup = name + "_copy." + extension;\n'
                'System.out.println("Name: " + name);\n'
                'System.out.println("Extension: " + extension.toUpperCase());\n'
                'System.out.println("Backup: " + backup);\n'
                'System.out.println("Name length: " + name.length());'),
               ("название взято вместе с точкой",
                'int dot = fileName.indexOf(".");\n'
                'String name = fileName.substring(0, dot + 1);\n'
                'String extension = fileName.substring(dot + 1);\n'
                'String backup = name + "_copy." + extension;\n'
                'System.out.println("Name: " + name);\n'
                'System.out.println("Extension: " + extension.toUpperCase());\n'
                'System.out.println("Backup: " + backup);\n'
                'System.out.println("Name length: " + name.length());')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-str-train-ticket", title="Код железнодорожного билета",
        given=[("String", "from"), ("String", "to"), ("int", "car"), ("int", "seat")],
        variants=[{"from": '"Moscow"', "to": '"Kazan"', "car": "5", "seat": "14"},
                  {"from": '"Sochi"', "to": '"Rostov"', "car": "12", "seat": "3"},
                  {"from": '"Samara"', "to": '"Perm"', "car": "7", "seat": "29"}],
        hidden=[{"from": '"Ufa"', "to": '"Omsk"', "car": "1", "seat": "1"},
                {"from": '"Tver"', "to": '"Vladivostok"', "car": "20", "seat": "36"},
                {"from": '"Kirov"', "to": '"Tula"', "car": "3", "seat": "9"}],
        intro="На билете поезда печатают короткий код маршрута. Город отправления — поле `from`, город прибытия — поле "
              "`to`, номер вагона — поле `car`, номер места — поле `seat`.",
        steps=["Заведи строки `fromCode` и `toCode`: первые три буквы каждого города, большими буквами — например `MOS` и `KAZ`.",
               "Заведи строку `route`: `fromCode`, дефис и `toCode` — например `MOS-KAZ`.",
               "Заведи строку `ticket`: `route`, косая черта `/`, номер вагона, `/` и номер места — например `MOS-KAZ/5/14`.",
               "Выведи три строки: `Route: ` и `route`, `Ticket: ` и `ticket`, `Next seat: ` и номер места на единицу больше."],
        hint="Методы можно вызывать цепочкой: `city.substring(0, 3).toUpperCase()` — сначала берутся первые три буквы, "
             "потом они становятся большими. И помни: `\"Seat: \" + 5 + 1` даёт `Seat: 51`, а сложить числа помогают скобки.",
        solution='String fromCode = from.substring(0, 3).toUpperCase();\n'
                 'String toCode = to.substring(0, 3).toUpperCase();\n'
                 'String route = fromCode + "-" + toCode;\n'
                 'String ticket = route + "/" + car + "/" + seat;\n'
                 'System.out.println("Route: " + route);\n'
                 'System.out.println("Ticket: " + ticket);\n'
                 'System.out.println("Next seat: " + (seat + 1));',
        wrong=[("нет скобок: к номеру места приклеивается цифра 1",
                'String fromCode = from.substring(0, 3).toUpperCase();\n'
                'String toCode = to.substring(0, 3).toUpperCase();\n'
                'String route = fromCode + "-" + toCode;\n'
                'String ticket = route + "/" + car + "/" + seat;\n'
                'System.out.println("Route: " + route);\n'
                'System.out.println("Ticket: " + ticket);\n'
                'System.out.println("Next seat: " + seat + 1);'),
               ("substring(0, 2): конец не включается, берутся только две буквы",
                'String fromCode = from.substring(0, 3).toUpperCase();\n'
                'String toCode = to.substring(0, 2).toUpperCase();\n'
                'String route = fromCode + "-" + toCode;\n'
                'String ticket = route + "/" + car + "/" + seat;\n'
                'System.out.println("Route: " + route);\n'
                'System.out.println("Ticket: " + ticket);\n'
                'System.out.println("Next seat: " + (seat + 1));')],
        constructs=["assignment"],
    ),
]
