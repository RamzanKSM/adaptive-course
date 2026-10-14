"""THROW_BASIC — «Выброс исключения throw» (Java). Taught before: everything up to try/catch and finally, methods,
classes with private fields and setters. Here: a method reports a bad value itself with
throw new IllegalArgumentException("своё сообщение"), and main catches it and prints e.getMessage() — our own text,
never one of Java's. The checks call the method through reflection to make sure it really throws. Not yet: throws."""
from java_tasks import JavaOutputTask

SKILL = "THROW_BASIC"


def with_methods(main: str, methods: str) -> str:
    """Body of main followed by more static methods of Solution (the template's closing brace ends the last one)."""
    body = methods.strip()
    assert body.endswith("}")
    return main.rstrip() + "\n}\n\n" + body[:-1].rstrip()


# ── 1. Бронь столика ──
TABLE_MAIN = ('try {\n    checkGuests(guests);\n    System.out.println("Table booked, guests: " + guests);\n'
              '} catch (IllegalArgumentException e) {\n    System.out.println("Refused: " + e.getMessage());\n}')
TABLE_CHECK = '''static void checkGuests(int guests) {
    if (guests < 1 || guests > 8) {
        throw new IllegalArgumentException("Tables are for groups of 1 to 8 people");
    }
}'''
TABLE_CHECKS = '''Method m = null;
try { m = Solution.class.getDeclaredMethod("checkGuests", int.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()), "Добавь в класс Solution метод static void checkGuests(int guests): проверка числа гостей должна жить в нём");
m.setAccessible(true);
for (int bad : new int[]{0, 9}) {
  boolean thrown = false;
  try { m.invoke(null, bad); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
  need(thrown, "Метод checkGuests должен выбрасывать IllegalArgumentException через throw, когда гостей меньше 1 или больше 8");
}
try { m.invoke(null, 4); } catch (InvocationTargetException e) { need(false, "Для компании из 4 человек метод checkGuests не должен выбрасывать исключение"); }'''

# ── 2. Отгрузка со склада ──
SHIP_MAIN = ('try {\n    int left = ship(stock, order);\n'
             '    System.out.println("Shipped: " + order + " pcs, left: " + left + " pcs");\n'
             '} catch (IllegalArgumentException e) {\n    System.out.println("Refused: " + e.getMessage());\n}')
SHIP_METHOD = '''static int ship(int stock, int order) {
    if (order < 1) {
        throw new IllegalArgumentException("An order needs at least one item");
    }
    if (order > stock) {
        throw new IllegalArgumentException("Only " + stock + " pcs in stock");
    }
    return stock - order;
}'''
SHIP_CHECKS = '''Method m = null;
try { m = Solution.class.getDeclaredMethod("ship", int.class, int.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, "Добавь в класс Solution метод static int ship(int stock, int order): он возвращает, сколько останется на складе");
m.setAccessible(true);
for (int[] bad : new int[][]{{10, 0}, {10, 11}}) {
  boolean thrown = false;
  try { m.invoke(null, bad[0], bad[1]); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
  need(thrown, "Метод ship должен выбрасывать IllegalArgumentException через throw, если в заказе меньше 1 штуки или больше, чем есть на складе");
}
Object left = null;
try { left = m.invoke(null, 10, 4); } catch (InvocationTargetException e) { }
need(Integer.valueOf(6).equals(left), "ship(10, 4) должен вернуть 6 — столько штук останется на складе после отгрузки");'''

# ── 3. Термостат ──
THERMOSTAT = '''class Thermostat {
    private int temperature = 20;

    int getTemperature() {
        return temperature;
    }

    void setTemperature(int value) {
        if (value < 10 || value > 30) {
            throw new IllegalArgumentException("Cannot set " + value + ": allowed from 10 to 30");
        }
        temperature = value;
    }
}'''
THERMO_MAIN = ('Thermostat thermostat = new Thermostat();\nfor (int value : requests) {\n    try {\n'
               '        thermostat.setTemperature(value);\n        System.out.println("New temperature: " + value);\n'
               '    } catch (IllegalArgumentException e) {\n        System.out.println(e.getMessage());\n    }\n}\n'
               'System.out.println("Final temperature: " + thermostat.getTemperature());')
THERMO_CHECKS = '''Class<?> c = cls("Thermostat");
need(c != null, "Создай класс Thermostat: он хранит температуру и сам проверяет новые значения");
Method set = null;
try { set = c.getDeclaredMethod("setTemperature", int.class); } catch (NoSuchMethodException e) { }
need(set != null, "Добавь в класс Thermostat метод void setTemperature(int value)");
boolean closed = false;
try { closed = Modifier.isPrivate(c.getDeclaredField("temperature").getModifiers()); } catch (NoSuchFieldException e) { }
need(closed, "Сделай поле temperature в классе Thermostat приватным: менять его можно только через setTemperature с проверкой");
Object thermostat = null;
try { Constructor<?> k = c.getDeclaredConstructor(); k.setAccessible(true); thermostat = k.newInstance(); } catch (NoSuchMethodException | InvocationTargetException e) { }
need(thermostat != null, "Термостат создаётся без параметров: new Thermostat(), а температура по умолчанию — 20");
set.setAccessible(true);
boolean thrown = false;
try { set.invoke(thermostat, 35); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
need(thrown, "Метод setTemperature должен выбрасывать IllegalArgumentException через throw, если температура меньше 10 или больше 30");'''

# ── 4. Пароль ──
PASS_MAIN = ('try {\n    checkPassword(password);\n    System.out.println("Password saved");\n'
             '} catch (IllegalArgumentException e) {\n    System.out.println("Error: " + e.getMessage());\n}')
PASS_CHECK = """static void checkPassword(String password) {
    if (password.length() < 8) {
        throw new IllegalArgumentException("Too short: " + password.length() + " characters, need at least 8");
    }
}"""
PASS_CHECKS = """Method m = null;
try { m = Solution.class.getDeclaredMethod("checkPassword", String.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()), "Добавь в класс Solution метод static void checkPassword(String password): проверка пароля должна жить в нём");
m.setAccessible(true);
boolean thrown = false;
try { m.invoke(null, "abc"); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
need(thrown, "Метод checkPassword должен выбрасывать IllegalArgumentException через throw, если в пароле меньше 8 символов");
try { m.invoke(null, "longpassword"); } catch (InvocationTargetException e) { need(false, "Для длинного пароля метод checkPassword не должен выбрасывать исключение"); }"""

# ── 5. Средний балл ──
AVG_MAIN = ('try {\n    System.out.println("Average: " + average(marks));\n'
            '} catch (IllegalArgumentException e) {\n    System.out.println("Error: " + e.getMessage());\n}')
AVG_METHOD = """static int average(int[] marks) {
    if (marks.length == 0) {
        throw new IllegalArgumentException("No marks yet");
    }
    int sum = 0;
    for (int i = 0; i < marks.length; i++) {
        if (marks[i] < 1 || marks[i] > 5) {
            throw new IllegalArgumentException("Wrong mark: " + marks[i]);
        }
        sum += marks[i];
    }
    return sum / marks.length;
}"""
AVG_CHECKS = """Method m = null;
try { m = Solution.class.getDeclaredMethod("average", int[].class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, "Добавь в класс Solution метод static int average(int[] marks): он возвращает средний балл");
m.setAccessible(true);
for (int[] bad : new int[][]{{}, {3, 9}}) {
  boolean thrown = false;
  try { m.invoke(null, (Object) bad); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
  need(thrown, "Метод average должен выбрасывать IllegalArgumentException через throw, если оценок нет или какая-то оценка не от 1 до 5");
}
Object avg = null;
try { avg = m.invoke(null, (Object) new int[]{4, 5}); } catch (InvocationTargetException e) { }
need(Integer.valueOf(4).equals(avg), "average для оценок 4 и 5 должен вернуть 4 — среднее, округлённое вниз");"""

# ── 6. Места в вагоне ──
TRAIN = """class Train {
    private boolean[] taken;

    Train(int seats) {
        taken = new boolean[seats];
    }

    void book(int seat) {
        if (seat < 1 || seat > taken.length) {
            throw new IllegalArgumentException("No seat " + seat);
        }
        if (taken[seat - 1]) {
            throw new IllegalArgumentException("Seat " + seat + " is taken");
        }
        taken[seat - 1] = true;
    }

    int free() {
        int count = 0;
        for (boolean t : taken) {
            if (!t) {
                count++;
            }
        }
        return count;
    }
}"""
TRAIN_MAIN = ('Train train = new Train(seats);\nfor (int seat : requests) {\n    try {\n        train.book(seat);\n'
              '        System.out.println("Seat " + seat + " booked");\n    } catch (IllegalArgumentException e) {\n'
              '        System.out.println(e.getMessage());\n    }\n}\nSystem.out.println("Free seats: " + train.free());')
TRAIN_CHECKS = """Class<?> c = cls("Train");
need(c != null, "Создай класс Train: он хранит, какие места заняты, и сам проверяет каждую бронь");
Method book = null;
try { book = c.getDeclaredMethod("book", int.class); } catch (NoSuchMethodException e) { }
need(book != null, "Добавь в класс Train метод void book(int seat)");
Object train = null;
try { Constructor<?> k = c.getDeclaredConstructor(int.class); k.setAccessible(true); train = k.newInstance(3); } catch (NoSuchMethodException | InvocationTargetException e) { }
need(train != null, "Добавь в класс Train конструктор Train(int seats)");
book.setAccessible(true);
boolean thrown = false;
try { book.invoke(train, 0); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
need(thrown, "Метод book должен выбрасывать IllegalArgumentException через throw, если такого места в вагоне нет");
try { book.invoke(train, 2); } catch (InvocationTargetException e) { need(false, "Свободное место 2 в вагоне на 3 места метод book должен бронировать без исключения"); }
thrown = false;
try { book.invoke(train, 2); } catch (InvocationTargetException e) { thrown = e.getCause() instanceof IllegalArgumentException; }
need(thrown, "Метод book должен выбрасывать IllegalArgumentException через throw, если место уже занято");"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-throw-cafe-table", title="Бронь столика в кафе",
        given=[("int", "guests")],
        variants=[{"guests": "4"}, {"guests": "12"}, {"guests": "1"}],
        hidden=[{"guests": "8"}, {"guests": "9"}, {"guests": "0"}, {"guests": "-3"}, {"guests": "5"}],
        intro="Кафе бронирует столики на компанию от 1 до 8 человек. Сколько гостей придёт, записано в поле `guests`. "
              "Проверку вынеси в отдельный метод: если число не подходит, он должен сообщить об этом исключением.",
        steps=["Добавь в класс `Solution` метод `static void checkGuests(int guests)`. Если гостей меньше 1 или больше 8, "
               "он выбрасывает исключение: `throw new IllegalArgumentException(\"Tables are for groups of 1 to 8 people\");`",
               "В `main` в блоке `try` вызови `checkGuests(guests)`, а следующей строкой выведи "
               "`Table booked, guests: 4` (число из `guests`).",
               "В блоке `catch (IllegalArgumentException e)` выведи `Refused: ` и текст исключения — его возвращает "
               "`e.getMessage()`."],
        hint="`throw` прерывает метод так же, как ошибка: строки после вызова `checkGuests` в `try` пропускаются, "
             "и Java переходит в `catch`. Текст, который ты передал в `new IllegalArgumentException(...)`, "
             "достаётся там через `e.getMessage()`.",
        solution=with_methods(TABLE_MAIN, TABLE_CHECK),
        wrong=[("строгая граница guests >= 8 — компании ровно из 8 человек отказывают",
                with_methods(TABLE_MAIN, TABLE_CHECK.replace("guests > 8", "guests >= 8"))),
               ("печатает подтверждение до проверки — при отказе выводятся обе строки",
                with_methods('try {\n    System.out.println("Table booked, guests: " + guests);\n'
                             '    checkGuests(guests);\n} catch (IllegalArgumentException e) {\n'
                             '    System.out.println("Refused: " + e.getMessage());\n}', TABLE_CHECK))],
        constructs=["try", "function", "if"],
        checks=TABLE_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-throw-warehouse", title="Отгрузка со склада",
        given=[("int", "stock"), ("int", "order")],
        variants=[{"stock": "40", "order": "15"}, {"stock": "12", "order": "30"}, {"stock": "100", "order": "0"}],
        hidden=[{"stock": "25", "order": "25"}, {"stock": "25", "order": "26"}, {"stock": "50", "order": "-5"},
                {"stock": "0", "order": "3"}, {"stock": "60", "order": "1"}],
        intro="Склад отгружает товар магазинам. Сколько штук лежит на складе, записано в `stock`, а сколько заказал "
              "магазин — в `order`. Метод отгрузки отказывает в двух случаях, и в каждом — со своим объяснением.",
        steps=["Добавь в класс `Solution` метод `static int ship(int stock, int order)`, который возвращает, сколько "
               "штук останется на складе после отгрузки.",
               "Если `order` меньше 1, метод выбрасывает `IllegalArgumentException` с сообщением "
               "`An order needs at least one item`.",
               "Если `order` больше `stock`, метод выбрасывает `IllegalArgumentException` с сообщением "
               "`Only 12 pcs in stock` — с числом из `stock`.",
               "В `main` в блоке `try` вызови `ship(stock, order)` и выведи `Shipped: 15 pcs, left: 25 pcs`, "
               "а в `catch` выведи `Refused: ` и сообщение исключения."],
        hint="Сообщение исключения собирается так же, как строка для `println`, — из текста и чисел через `+`, "
             "а в `catch` его отдаёт `e.getMessage()`. Так одна строка `catch` напечатает правильную причину для обоих отказов.",
        solution=with_methods(SHIP_MAIN, SHIP_METHOD),
        wrong=[("строгая граница order >= stock — нельзя забрать всё до последней штуки",
                with_methods(SHIP_MAIN, SHIP_METHOD.replace("order > stock", "order >= stock"))),
               ("в catch печатает одну и ту же фразу вместо e.getMessage() — причина отказа теряется",
                with_methods(SHIP_MAIN.replace('"Refused: " + e.getMessage()', '"Refused: Only " + stock + " pcs in stock"'),
                             SHIP_METHOD))],
        constructs=["try", "function", "if"],
        checks=SHIP_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-throw-thermostat", title="Умный термостат",
        given=[("int[]", "requests")],
        variants=[{"requests": "{22, 35, 18}"}, {"requests": "{25, 5}"}, {"requests": "{40, 30, 10, 31}"}],
        hidden=[{"requests": "{}"}, {"requests": "{9}"}, {"requests": "{10, 30}"}, {"requests": "{-5, 21, 50}"}],
        intro="Умным термостатом управляют из приложения. Команды, которые пользователь отправил по очереди, лежат "
              "в массиве `requests`, но термостат умеет держать температуру только от 10 до 30 градусов.",
        steps=["Создай класс `Thermostat` с приватным полем `temperature`, равным `20`, и методом `int getTemperature()`.",
               "Добавь в него метод `void setTemperature(int value)`: если `value` меньше 10 или больше 30, он выбрасывает "
               "`IllegalArgumentException` с сообщением `Cannot set 35: allowed from 10 to 30` (с числом из `value`), "
               "а иначе запоминает новую температуру.",
               "В `main` создай один термостат и для каждой команды из `requests` в блоке `try` вызови `setTemperature` "
               "и выведи `New temperature: 22`; в `catch` выведи только сообщение исключения.",
               "После всех команд выведи `Final temperature: 18` — температуру, которую держит термостат."],
        hint="Проверяй значение до того, как записать его в поле: `throw` сразу прерывает метод, и неподходящая "
             "температура так и не попадёт в термостат.",
        solution=THERMO_MAIN,
        classes=THERMOSTAT,
        wrong=[("записывает температуру до проверки — неподходящее значение остаётся в термостате",
                THERMO_MAIN,
                THERMOSTAT.replace("    void setTemperature(int value) {\n",
                                   "    void setTemperature(int value) {\n        temperature = value;\n").replace(
                    "        }\n        temperature = value;\n    }", "        }\n    }")),
               ("try вокруг всего цикла — после первой неподходящей команды остальные не выполняются",
                'Thermostat thermostat = new Thermostat();\ntry {\n    for (int value : requests) {\n'
                '        thermostat.setTemperature(value);\n        System.out.println("New temperature: " + value);\n'
                '    }\n} catch (IllegalArgumentException e) {\n    System.out.println(e.getMessage());\n}\n'
                'System.out.println("Final temperature: " + thermostat.getTemperature());')],
        constructs=["try", "class"],
        checks=THERMO_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-throw-password", title="Длина пароля",
        given=[("String", "password")],
        variants=[{"password": '"qwerty"'}, {"password": '"sunflower22"'}, {"password": '"cat2024"'}],
        hidden=[{"password": '"abcdefgh"'}, {"password": '""'}, {"password": '"1234567"'}, {"password": '"correct horse"'}],
        intro="Сайт принимает пароль только из 8 символов и больше. Пароль, который придумал пользователь, записан "
              "в поле `password`. Проверку вынеси в отдельный метод: если пароль слишком короткий, он должен "
              "сообщить об этом исключением.",
        steps=["Добавь в класс `Solution` метод `static void checkPassword(String password)`. Если в пароле меньше "
               "8 символов (длину даёт `password.length()`), он выбрасывает `IllegalArgumentException` с сообщением "
               "вида `Too short: 6 characters, need at least 8` — с настоящей длиной пароля.",
               "В `main` в блоке `try` вызови `checkPassword(password)`, а следующей строкой выведи `Password saved`.",
               "В блоке `catch (IllegalArgumentException e)` выведи `Error: ` и текст исключения из `e.getMessage()`."],
        hint="Сообщение для исключения собирается так же, как строка для `println`: `\"Too short: \" + password.length() + ...`. "
             "Пароль ровно из 8 символов уже подходит.",
        solution=with_methods(PASS_MAIN, PASS_CHECK),
        wrong=[("проверяет через <= 8 — пароль ровно из 8 символов не принимается",
                with_methods(PASS_MAIN, PASS_CHECK.replace("password.length() < 8", "password.length() <= 8"))),
               ("печатает «Password saved» до проверки — при ошибке выводятся обе строки",
                with_methods('try {\n    System.out.println("Password saved");\n    checkPassword(password);\n'
                             '} catch (IllegalArgumentException e) {\n    System.out.println("Error: " + e.getMessage());\n}',
                             PASS_CHECK))],
        constructs=["try", "function", "if"],
        checks=PASS_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-throw-average-mark", title="Средний балл",
        given=[("int[]", "marks")],
        variants=[{"marks": "{5, 4, 4, 3}"}, {"marks": "{4, 7, 5}"}, {"marks": "{}"}],
        hidden=[{"marks": "{5}"}, {"marks": "{0, 3}"}, {"marks": "{1, 5, 5}"}, {"marks": "{4, 4, 6}"},
                {"marks": "{2, 3, 3, 3}"}],
        intro="Электронный дневник считает средний балл по оценкам из массива `marks`. Оценки бывают только от 1 "
              "до 5, но после сбоя в массив может попасть что-то другое, а у новичка оценок может ещё не быть. "
              "Метод подсчёта в таких случаях не считает, а сообщает о проблеме исключением.",
        steps=["Добавь в класс `Solution` метод `static int average(int[] marks)`, который возвращает средний балл — "
               "сумму оценок, делённую нацело на их количество.",
               "Если массив пустой, метод выбрасывает `IllegalArgumentException` с сообщением `No marks yet`.",
               "Проходя по оценкам, проверяй каждую: если оценка меньше 1 или больше 5, метод выбрасывает "
               "`IllegalArgumentException` с сообщением вида `Wrong mark: 7` — с этой оценкой.",
               "В `main` в блоке `try` выведи строку вида `Average: 4` с результатом `average(marks)`, а в `catch` "
               "выведи `Error: ` и сообщение исключения."],
        hint="`throw` можно написать и внутри цикла: он сразу прерывает и цикл, и весь метод, так что `return` "
             "с неправильным средним уже не выполнится.",
        solution=with_methods(AVG_MAIN, AVG_METHOD),
        wrong=[("цикл начинается с i = 1 — первая оценка не проверяется и не считается",
                with_methods(AVG_MAIN, AVG_METHOD.replace("for (int i = 0;", "for (int i = 1;"))),
               ("проверяет через >= 5 — пятёрка считается неправильной оценкой",
                with_methods(AVG_MAIN, AVG_METHOD.replace("marks[i] > 5", "marks[i] >= 5")))],
        constructs=["try", "function", "if", "for"],
        checks=AVG_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-throw-train-seats", title="Места в вагоне",
        given=[("int", "seats"), ("int[]", "requests")],
        variants=[{"seats": "4", "requests": "{2, 3, 2, 5}"},
                  {"seats": "6", "requests": "{6, 1, 0}"},
                  {"seats": "3", "requests": "{1, 2, 3, 3}"}],
        hidden=[{"seats": "2", "requests": "{}"},
                {"seats": "1", "requests": "{1}"},
                {"seats": "5", "requests": "{5, 5, 6, -1}"},
                {"seats": "3", "requests": "{3, 4, 1, 1, 2}"}],
        intro="В вагоне `seats` мест с номерами от 1. Пассажиры по очереди бронируют места — номера записаны в массив "
              "`requests`. Бронь не проходит, если такого места нет или его уже заняли, и вагон сам сообщает об этом "
              "исключением.",
        steps=["Создай класс `Train` с приватным массивом `boolean[] taken`, конструктором `Train(int seats)`, который "
               "создаёт массив на `seats` мест, и методом `int free()`, который возвращает, сколько мест свободно.",
               "Добавь метод `void book(int seat)`: если `seat` меньше 1 или больше числа мест, он выбрасывает "
               "`IllegalArgumentException` с сообщением вида `No seat 5`; если место уже занято — с сообщением вида "
               "`Seat 2 is taken`; иначе отмечает место занятым. Место номер `seat` хранится в `taken[seat - 1]`.",
               "В `main` создай один вагон и для каждого номера из `requests` в блоке `try` вызови `book` и выведи "
               "строку вида `Seat 2 booked`; в `catch` выведи только сообщение исключения.",
               "После всех броней выведи строку вида `Free seats: 2`."],
        hint="Сначала проверь, что номер вообще есть в вагоне, и только потом смотри в `taken[seat - 1]`: для номера "
             "вне вагона такого элемента массива нет.",
        solution=TRAIN_MAIN,
        classes=TRAIN,
        wrong=[("сравнивает номер места с длиной массива через >= — последнее место считается несуществующим",
                TRAIN_MAIN, TRAIN.replace("seat > taken.length", "seat >= taken.length")),
               ("try вокруг всего цикла — после первой неудачной брони остальные не обрабатываются",
                'Train train = new Train(seats);\ntry {\n    for (int seat : requests) {\n        train.book(seat);\n'
                '        System.out.println("Seat " + seat + " booked");\n    }\n} catch (IllegalArgumentException e) {\n'
                '    System.out.println(e.getMessage());\n}\nSystem.out.println("Free seats: " + train.free());')],
        constructs=["try", "class", "for"],
        checks=TRAIN_CHECKS,
    ),
]
