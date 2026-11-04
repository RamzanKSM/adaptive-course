"""PRIMITIVE_TYPES — «Примитивные типы» (Java). Taught before: println, variables, assignment, arithmetic, execution order.
The point: int for whole numbers, double for fractions, long when int is too small, char for one symbol; an (int) cast
drops the fraction, and an int expression overflows before it is stored in a long. Not yet: String variables and their
methods, integer division and %, += -= ++, if/else, comparisons, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "PRIMITIVE_TYPES"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-types-market-apples", title="Яблоки на рынке",
        given=[("double", "weight"), ("int", "price")],
        variants=[{"weight": "2.5", "price": "75"}, {"weight": "1.5", "price": "130"}, {"weight": "0.75", "price": "210"}],
        hidden=[{"weight": "2.0", "price": "100"}, {"weight": "0.5", "price": "99"}, {"weight": "4.25", "price": "60"},
                {"weight": "3.5", "price": "45"}],
        intro="На рынке продавец взвешивает яблоки: вес в килограммах записан в поле `weight` (дробное число), "
              "цена за килограмм в рублях — в поле `price`. Покупатель расплачивается купюрой в 1000 рублей.",
        steps=["Заведи переменную `cost` типа `double` — стоимость покупки: `weight` умножить на `price`.",
               "Заведи переменную `change` типа `double` — сдача: `1000` минус `cost`.",
               "Выведи `Weight: `, вес и ` kg`, например `Weight: 2.5 kg`.",
               "Выведи `Price: `, цену и ` rub per kg`.",
               "Выведи `Cost: `, стоимость и ` rub`, затем `Change: `, сдачу и ` rub` — каждое с новой строки."],
        hint="Вес дробный, значит и стоимость может получиться дробной, например `187.5`. Тип `int` хранит только целые "
             "числа, поэтому для денег здесь нужен `double`. Число типа `double` Java печатает с точкой: `200.0`.",
        solution='double cost = weight * price;\n'
                 'double change = 1000 - cost;\n'
                 'System.out.println("Weight: " + weight + " kg");\n'
                 'System.out.println("Price: " + price + " rub per kg");\n'
                 'System.out.println("Cost: " + cost + " rub");\n'
                 'System.out.println("Change: " + change + " rub");',
        wrong=[("стоимость сохранена в int через (int): дробная часть теряется",
                'int cost = (int) (weight * price);\n'
                'double change = 1000 - cost;\n'
                'System.out.println("Weight: " + weight + " kg");\n'
                'System.out.println("Price: " + price + " rub per kg");\n'
                'System.out.println("Cost: " + cost + " rub");\n'
                'System.out.println("Change: " + change + " rub");'),
               ("(int) применён к весу до умножения: 2.5 kg превращаются в 2 kg",
                'double cost = (int) weight * price;\n'
                'double change = 1000 - cost;\n'
                'System.out.println("Weight: " + weight + " kg");\n'
                'System.out.println("Price: " + price + " rub per kg");\n'
                'System.out.println("Cost: " + cost + " rub");\n'
                'System.out.println("Change: " + change + " rub");')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-types-day-temperature", title="Температура за день",
        given=[("double", "morning"), ("double", "evening")],
        variants=[{"morning": "12.5", "evening": "18.0"}, {"morning": "-3.5", "evening": "2.0"}, {"morning": "20.0", "evening": "27.5"}],
        hidden=[{"morning": "10.0", "evening": "10.0"}, {"morning": "-8.5", "evening": "-1.0"}, {"morning": "15.5", "evening": "22.5"},
                {"morning": "0.5", "evening": "3.0"}],
        intro="Метеостанция записала температуру утром — поле `morning` — и вечером — поле `evening` (в градусах, "
              "дробные числа). Нужно вывести сводку за день.",
        steps=["Заведи переменную `difference` типа `double`: `evening` минус `morning`.",
               "Заведи переменную `average` типа `double`: сумма `morning` и `evening`, делённая на `2`.",
               "Выведи `Morning: ` и утреннюю температуру, затем `Evening: ` и вечернюю.",
               "Выведи `Difference: ` и разницу, затем `Average: ` и среднюю температуру — каждое с новой строки."],
        hint="Средняя температура тоже дробная: из `12.5` и `18.0` получается `15.25`, поэтому её место в `double`. "
             "Сумму возьми в скобки: деление выполняется раньше сложения.",
        solution='double difference = evening - morning;\n'
                 'double average = (morning + evening) / 2;\n'
                 'System.out.println("Morning: " + morning);\n'
                 'System.out.println("Evening: " + evening);\n'
                 'System.out.println("Difference: " + difference);\n'
                 'System.out.println("Average: " + average);',
        wrong=[("средняя сохранена в int через (int): дробная часть теряется",
                'double difference = evening - morning;\n'
                'int average = (int) ((morning + evening) / 2);\n'
                'System.out.println("Morning: " + morning);\n'
                'System.out.println("Evening: " + evening);\n'
                'System.out.println("Difference: " + difference);\n'
                'System.out.println("Average: " + average);'),
               ("нет скобок: на 2 делится только вечерняя температура",
                'double difference = evening - morning;\n'
                'double average = morning + evening / 2;\n'
                'System.out.println("Morning: " + morning);\n'
                'System.out.println("Evening: " + evening);\n'
                'System.out.println("Difference: " + difference);\n'
                'System.out.println("Average: " + average);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-types-vacation-millis", title="Отпуск в миллисекундах",
        given=[("int", "days")],
        variants=[{"days": "30"}, {"days": "45"}, {"days": "90"}],
        hidden=[{"days": "1"}, {"days": "10"}, {"days": "25"}, {"days": "365"}],
        intro="Программа-таймер считает, сколько длится отпуск в разных единицах. Число дней отпуска записано в поле `days`. "
              "Миллисекунд в отпуске получается больше двух миллиардов, а самое большое число типа `int` — 2147483647.",
        steps=["Заведи `int hours` — часы: `days` умножить на `24`; затем `int minutes` — минуты: `hours` умножить на `60`.",
               "Заведи `long seconds` — секунды: `minutes` умножить на `60`; затем `long millis` — миллисекунды: `seconds` умножить на `1000`.",
               "Выведи четыре строки: `Hours: `, `Minutes: `, `Seconds: `, `Millis: ` — после каждой надписи её число."],
        hint="Если число не помещается в `int`, Java не сообщает об ошибке: результат «переполняется» и становится "
             "неправильным, даже отрицательным. Тип `long` хранит гораздо большие числа, а `long`, умноженный на `int`, "
             "считается уже в `long`.",
        solution='int hours = days * 24;\n'
                 'int minutes = hours * 60;\n'
                 'long seconds = minutes * 60;\n'
                 'long millis = seconds * 1000;\n'
                 'System.out.println("Hours: " + hours);\n'
                 'System.out.println("Minutes: " + minutes);\n'
                 'System.out.println("Seconds: " + seconds);\n'
                 'System.out.println("Millis: " + millis);',
        wrong=[("секунды в int: seconds * 1000 считается в int и переполняется",
                'int hours = days * 24;\n'
                'int minutes = hours * 60;\n'
                'int seconds = minutes * 60;\n'
                'long millis = seconds * 1000;\n'
                'System.out.println("Hours: " + hours);\n'
                'System.out.println("Minutes: " + minutes);\n'
                'System.out.println("Seconds: " + seconds);\n'
                'System.out.println("Millis: " + millis);'),
               ("миллисекунды считаются из минут целиком в int и переполняются",
                'int hours = days * 24;\n'
                'int minutes = hours * 60;\n'
                'long seconds = minutes * 60;\n'
                'long millis = minutes * 60 * 1000;\n'
                'System.out.println("Hours: " + hours);\n'
                'System.out.println("Minutes: " + minutes);\n'
                'System.out.println("Seconds: " + seconds);\n'
                'System.out.println("Millis: " + millis);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-types-letter-shift", title="Шифр сдвига для буквы",
        given=[("char", "letter"), ("int", "shift")],
        variants=[{"letter": "'C'", "shift": "3"}, {"letter": "'K'", "shift": "5"}, {"letter": "'P'", "shift": "2"}],
        hidden=[{"letter": "'A'", "shift": "1"}, {"letter": "'X'", "shift": "2"}, {"letter": "'M'", "shift": "0"}, {"letter": "'a'", "shift": "3"}],
        intro="Ребята в лагере шифруют записки: каждую букву заменяют буквой, которая стоит в алфавите на несколько "
              "позиций дальше. Буква записана в поле `letter` типа `char`, сдвиг — в поле `shift`. "
              "Внутри компьютера каждая буква хранится как число — её код: у `A` код 65, у `B` — 66 и так далее.",
        steps=["Заведи `int code` и запиши в неё `letter` — так получится код буквы.",
               "Заведи `char shifted` — зашифрованную букву: `(char) (letter + shift)`.",
               "Заведи `int shiftedCode` и запиши в неё `shifted`.",
               "Выведи четыре строки: `Letter: ` и `letter`, `Code: ` и `code`, `Shifted: ` и `shifted`, "
               "`Shifted code: ` и `shiftedCode`."],
        hint="`letter + shift` — это уже число типа `int`: Java складывает коды. Чтобы снова получить букву, число "
             "приводят к `char`: `(char) 68` — это `D`. А `char`, записанный в переменную `int`, превращается в свой код.",
        solution='int code = letter;\n'
                 'char shifted = (char) (letter + shift);\n'
                 'int shiftedCode = shifted;\n'
                 'System.out.println("Letter: " + letter);\n'
                 'System.out.println("Code: " + code);\n'
                 'System.out.println("Shifted: " + shifted);\n'
                 'System.out.println("Shifted code: " + shiftedCode);',
        wrong=[("зашифрованная буква сохранена в int: печатается код вместо буквы",
                'int code = letter;\n'
                'int shifted = letter + shift;\n'
                'int shiftedCode = shifted;\n'
                'System.out.println("Letter: " + letter);\n'
                'System.out.println("Code: " + code);\n'
                'System.out.println("Shifted: " + shifted);\n'
                'System.out.println("Shifted code: " + shiftedCode);'),
               ("в строке Code печатается сама буква, а не её код",
                'int code = letter;\n'
                'char shifted = (char) (letter + shift);\n'
                'int shiftedCode = shifted;\n'
                'System.out.println("Letter: " + letter);\n'
                'System.out.println("Code: " + letter);\n'
                'System.out.println("Shifted: " + shifted);\n'
                'System.out.println("Shifted code: " + shiftedCode);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-types-fuel-trip", title="Бензин на поездку",
        given=[("int", "distance"), ("double", "consumption"), ("double", "fuelPrice"), ("int", "people")],
        variants=[{"distance": "300", "consumption": "6.5", "fuelPrice": "50.0", "people": "4"},
                  {"distance": "450", "consumption": "7.5", "fuelPrice": "54.0", "people": "3"},
                  {"distance": "180", "consumption": "8.5", "fuelPrice": "60.0", "people": "2"}],
        hidden=[{"distance": "100", "consumption": "5.0", "fuelPrice": "50.0", "people": "1"},
                {"distance": "250", "consumption": "7.0", "fuelPrice": "52.0", "people": "5"},
                {"distance": "200", "consumption": "6.25", "fuelPrice": "56.0", "people": "4"},
                {"distance": "60", "consumption": "9.5", "fuelPrice": "40.0", "people": "2"}],
        intro="Друзья едут на машине за город и делят расходы на бензин поровну. Длина поездки в километрах — поле "
              "`distance`, расход бензина в литрах на 100 км — поле `consumption`, цена литра в рублях — поле "
              "`fuelPrice`, число друзей — поле `people`.",
        steps=["Заведи `double liters` — сколько литров нужно: `distance` умножить на `consumption` и разделить на `100`.",
               "Заведи `double cost` — стоимость бензина: `liters` умножить на `fuelPrice`.",
               "Заведи `double share` — доля каждого: `cost` разделить на `people`.",
               "Выведи `Fuel: `, литры и ` l`, затем `Cost: `, стоимость и ` rub`, затем `Each pays: `, долю и ` rub` — "
               "каждое с новой строки."],
        hint="Литры получаются дробными (например, `19.5`), поэтому все три переменные — `double`. Если сохранить литры "
             "в `int`, дробная часть пропадёт, и вся дальнейшая сумма окажется неверной.",
        solution='double liters = distance * consumption / 100;\n'
                 'double cost = liters * fuelPrice;\n'
                 'double share = cost / people;\n'
                 'System.out.println("Fuel: " + liters + " l");\n'
                 'System.out.println("Cost: " + cost + " rub");\n'
                 'System.out.println("Each pays: " + share + " rub");',
        wrong=[("литры сохранены в int через (int): дробная часть теряется",
                'int liters = (int) (distance * consumption / 100);\n'
                'double cost = liters * fuelPrice;\n'
                'double share = cost / people;\n'
                'System.out.println("Fuel: " + liters + " l");\n'
                'System.out.println("Cost: " + cost + " rub");\n'
                'System.out.println("Each pays: " + share + " rub");'),
               ("забыто деление на 100: расход указан на 100 км, а не на 1 км",
                'double liters = distance * consumption;\n'
                'double cost = liters * fuelPrice;\n'
                'double share = cost / people;\n'
                'System.out.println("Fuel: " + liters + " l");\n'
                'System.out.println("Cost: " + cost + " rub");\n'
                'System.out.println("Each pays: " + share + " rub");')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-types-photo-storage", title="Место под фотографии",
        given=[("int", "width"), ("int", "height"), ("int", "photos")],
        variants=[{"width": "4000", "height": "3000", "photos": "1000"},
                  {"width": "4032", "height": "3024", "photos": "500"},
                  {"width": "6000", "height": "4000", "photos": "200"}],
        hidden=[{"width": "100", "height": "100", "photos": "10"}, {"width": "1920", "height": "1080", "photos": "2000"},
                {"width": "8000", "height": "6000", "photos": "50"}, {"width": "640", "height": "480", "photos": "3"}],
        intro="Фотограф хочет понять, сколько места займут его снимки без сжатия. Размер снимка в пикселях — поля "
              "`width` и `height`, число снимков — поле `photos`. Каждый пиксель занимает 3 байта.",
        steps=["Заведи `int pixels` — пикселей в одном снимке: `width` умножить на `height`.",
               "Заведи `int photoBytes` — байт в одном снимке: `pixels` умножить на `3`.",
               "Заведи `long totalBytes` — байт во всех снимках: `(long) photoBytes * photos`.",
               "Заведи `double gigabytes`: `totalBytes` разделить на `1000000000.0`.",
               "Выведи четыре строки: `Pixels: `, `Photo bytes: `, `Total bytes: `, `Gigabytes: ` — после каждой надписи её число."],
        hint="`photoBytes * photos` — произведение двух `int`, и Java считает его в `int`: больше 2147483647 там не "
             "поместится, число «переполнится» ещё до записи в `long`. Приведение `(long)` перед умножением заставляет "
             "считать сразу в `long`.",
        solution='int pixels = width * height;\n'
                 'int photoBytes = pixels * 3;\n'
                 'long totalBytes = (long) photoBytes * photos;\n'
                 'double gigabytes = totalBytes / 1000000000.0;\n'
                 'System.out.println("Pixels: " + pixels);\n'
                 'System.out.println("Photo bytes: " + photoBytes);\n'
                 'System.out.println("Total bytes: " + totalBytes);\n'
                 'System.out.println("Gigabytes: " + gigabytes);',
        wrong=[("(long) применён к уже переполненному произведению",
                'int pixels = width * height;\n'
                'int photoBytes = pixels * 3;\n'
                'long totalBytes = (long) (photoBytes * photos);\n'
                'double gigabytes = totalBytes / 1000000000.0;\n'
                'System.out.println("Pixels: " + pixels);\n'
                'System.out.println("Photo bytes: " + photoBytes);\n'
                'System.out.println("Total bytes: " + totalBytes);\n'
                'System.out.println("Gigabytes: " + gigabytes);'),
               ("без (long): произведение двух int переполняется",
                'int pixels = width * height;\n'
                'int photoBytes = pixels * 3;\n'
                'long totalBytes = photoBytes * photos;\n'
                'double gigabytes = totalBytes / 1000000000.0;\n'
                'System.out.println("Pixels: " + pixels);\n'
                'System.out.println("Photo bytes: " + photoBytes);\n'
                'System.out.println("Total bytes: " + totalBytes);\n'
                'System.out.println("Gigabytes: " + gigabytes);')],
        constructs=["assignment"],
    ),
]
