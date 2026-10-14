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
]
