"""THROWS_BASIC — «Объявление throws» (Java). Taught before: everything up to try/catch, finally and throw, classes,
inheritance and super. Here: an own checked exception (a small class extending Exception), a method that throws it
and declares it with throws, and a caller that handles it — or passes it further by declaring throws too. The syntax
tree checks cannot see throws, so the checks look at the methods through reflection (getExceptionTypes) and call them
to make sure they really throw. Only our own messages are printed, never Java's."""
from java_tasks import JavaOutputTask

SKILL = "THROWS_BASIC"


def with_methods(main: str, methods: str) -> str:
    """Body of main followed by more static methods of Solution (the template's closing brace ends the last one)."""
    body = methods.strip()
    assert body.endswith("}")
    return main.rstrip() + "\n}\n\n" + body[:-1].rstrip()


def exception_class(name: str) -> str:
    return f"class {name} extends Exception {{\n    {name}(String message) {{\n        super(message);\n    }}\n}}"


def checked_class_check(name: str, why: str) -> str:
    return (f'Class<?> ex = cls("{name}");\n'
            f'need(ex != null && Exception.class.isAssignableFrom(ex) && !RuntimeException.class.isAssignableFrom(ex), '
            f'"Создай класс {name} extends Exception — {why}");\n')


# ── 1. Лифт ──
OVERLOAD = exception_class("OverloadException")
LIFT_MAIN = ('try {\n    checkLoad(load);\n    System.out.println("Лифт поехал");\n} catch (OverloadException e) {\n'
             '    System.out.println(e.getMessage());\n    System.out.println("Снимите часть груза");\n}')
LIFT_CHECK = '''static void checkLoad(int load) throws OverloadException {
    if (load > 400) {
        throw new OverloadException("Перегрузка на " + (load - 400) + " кг");
    }
}'''
LIFT_CHECKS = checked_class_check("OverloadException", "это проверяемое исключение: Java потребует объявить его в throws и обработать") + '''Method m = null;
try { m = Solution.class.getDeclaredMethod("checkLoad", int.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()), "Добавь в класс Solution метод static void checkLoad(int load) throws OverloadException");
need(Arrays.asList(m.getExceptionTypes()).contains(ex), "Объяви в методе checkLoad именно throws OverloadException: так тот, кто вызывает метод, знает, какую ошибку обработать");
m.setAccessible(true);
boolean thrown = false;
try { m.invoke(null, 1000); } catch (InvocationTargetException e) { thrown = ex.isInstance(e.getCause()); }
need(thrown, "При весе больше 400 кг метод checkLoad должен выбрасывать OverloadException через throw");
try { m.invoke(null, 400); } catch (InvocationTargetException e) { need(false, "Ровно 400 кг лифт ещё поднимает: при таком весе checkLoad не должен выбрасывать исключение"); }'''

# ── 2. Дроны ──
TOO_HEAVY = exception_class("TooHeavyException")
DRONE_MAIN = ('int sent = 0;\nfor (int grams : parcels) {\n    try {\n        launch(grams);\n        sent++;\n'
              '    } catch (TooHeavyException e) {\n        System.out.println("Отказ: " + e.getMessage());\n    }\n}\n'
              'System.out.println("Отправлено посылок: " + sent);')
DRONE_METHODS = '''static void checkWeight(int grams) throws TooHeavyException {
    if (grams > 2000) {
        throw new TooHeavyException("Посылка " + grams + " г тяжелее 2000 г");
    }
}

static void launch(int grams) throws TooHeavyException {
    checkWeight(grams);
    System.out.println("Дрон взлетел, груз " + grams + " г");
}'''
DRONE_CHECKS = checked_class_check("TooHeavyException", "это проверяемое исключение для слишком тяжёлой посылки") + '''for (String name : new String[]{"checkWeight", "launch"}) {
  Method m = null;
  try { m = Solution.class.getDeclaredMethod(name, int.class); } catch (NoSuchMethodException e) { }
  need(m != null && Modifier.isStatic(m.getModifiers()), "Добавь в класс Solution метод static void " + name + "(int grams) throws TooHeavyException");
  need(Arrays.asList(m.getExceptionTypes()).contains(ex), "Объяви в методе " + name + " throws TooHeavyException: исключение должно дойти до main");
  m.setAccessible(true);
  boolean thrown = false;
  PrintStream saved = System.out;
  System.setOut(new PrintStream(new ByteArrayOutputStream(), true, "UTF-8"));
  try { m.invoke(null, 5000); } catch (InvocationTargetException e) { thrown = ex.isInstance(e.getCause()); } finally { System.setOut(saved); }
  need(thrown, "Метод " + name + " должен выпускать TooHeavyException наружу, а не ловить его сам: пусть его обработает catch в main");
}'''

# ── 3. Транспортная карта ──
LOW_BALANCE = exception_class("LowBalanceException")
CARD = '''class TransportCard {
    private int balance;

    TransportCard(int balance) {
        this.balance = balance;
    }

    int getBalance() {
        return balance;
    }

    void pay(int fare) throws LowBalanceException {
        if (fare > balance) {
            throw new LowBalanceException("Не хватает " + (fare - balance) + " руб.");
        }
        balance -= fare;
    }
}'''
CARD_MAIN = ('TransportCard card = new TransportCard(balance);\nfor (int fare : fares) {\n    try {\n'
             '        card.pay(fare);\n        System.out.println("Проход, осталось " + card.getBalance() + " руб.");\n'
             '    } catch (LowBalanceException e) {\n        System.out.println("Отказ: " + e.getMessage());\n    }\n}\n'
             'System.out.println("На карте: " + card.getBalance() + " руб.");')
CARD_CHECKS = checked_class_check("LowBalanceException", "это проверяемое исключение для нехватки денег на карте") + '''Class<?> c = cls("TransportCard");
need(c != null, "Создай класс TransportCard: он хранит баланс и списывает плату за поездку");
Method pay = null;
try { pay = c.getDeclaredMethod("pay", int.class); } catch (NoSuchMethodException e) { }
need(pay != null && Arrays.asList(pay.getExceptionTypes()).contains(ex), "Объяви в классе TransportCard метод void pay(int fare) throws LowBalanceException: так main узнает, что отказ нужно обработать");
boolean closed = false;
try { closed = Modifier.isPrivate(c.getDeclaredField("balance").getModifiers()); } catch (NoSuchFieldException e) { }
need(closed, "Сделай поле balance в классе TransportCard приватным: менять его можно только через pay");
Object card = null;
try { Constructor<?> k = c.getDeclaredConstructor(int.class); k.setAccessible(true); card = k.newInstance(10); } catch (NoSuchMethodException | InvocationTargetException e) { }
need(card != null, "Добавь в класс TransportCard конструктор TransportCard(int balance)");
pay.setAccessible(true);
boolean thrown = false;
try { pay.invoke(card, 50); } catch (InvocationTargetException e) { thrown = ex.isInstance(e.getCause()); }
need(thrown, "Если денег на карте не хватает, метод pay должен выбрасывать LowBalanceException через throw");'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-throws-lift-overload", title="Перегрузка лифта",
        given=[("int", "load")],
        variants=[{"load": "320"}, {"load": "450"}, {"load": "400"}],
        hidden=[{"load": "401"}, {"load": "0"}, {"load": "1000"}, {"load": "399"}, {"load": "520"}],
        intro="Грузовой лифт поднимает не больше 400 кг, а вес груза в кабине записан в поле `load`. Перегрузка — "
              "ожидаемая ситуация, которую нельзя забыть обработать, поэтому для неё нужно своё проверяемое исключение.",
        steps=["Создай класс `OverloadException`, унаследованный от `Exception`, с конструктором "
               "`OverloadException(String message)`, который передаёт текст в `super(message)`.",
               "Добавь в класс `Solution` метод `static void checkLoad(int load) throws OverloadException`. Если `load` "
               "больше 400, он выбрасывает `OverloadException` с сообщением `Перегрузка на 50 кг` — на сколько вес "
               "больше 400.",
               "В `main` в блоке `try` вызови `checkLoad(load)` и выведи `Лифт поехал`.",
               "В `catch (OverloadException e)` выведи сообщение исключения, а следующей строкой — `Снимите часть груза`."],
        hint="Исключение, унаследованное от `Exception`, — проверяемое: Java не скомпилирует метод, который его "
             "выбрасывает, без `throws OverloadException` в объявлении, и не даст вызвать такой метод без `try`/`catch`.",
        solution=with_methods(LIFT_MAIN, LIFT_CHECK),
        classes=OVERLOAD,
        wrong=[("«Снимите часть груза» стоит после try/catch — печатается и тогда, когда лифт поехал",
                with_methods('try {\n    checkLoad(load);\n    System.out.println("Лифт поехал");\n'
                             '} catch (OverloadException e) {\n    System.out.println(e.getMessage());\n}\n'
                             'System.out.println("Снимите часть груза");', LIFT_CHECK)),
               ("в сообщение кладёт весь вес груза, а не превышение над 400 кг",
                with_methods(LIFT_MAIN, LIFT_CHECK.replace("(load - 400)", "load")))],
        constructs=["try", "function", "class"],
        checks=LIFT_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-throws-drone-delivery", title="Доставка дронами",
        given=[("int[]", "parcels")],
        variants=[{"parcels": "{800, 2500, 1200}"}, {"parcels": "{3000, 150}"}, {"parcels": "{2000, 2001, 1999, 5000}"}],
        hidden=[{"parcels": "{}"}, {"parcels": "{2100}"}, {"parcels": "{500, 700, 900}"}, {"parcels": "{2000, 9999, 1}"}],
        intro="Служба доставки отправляет посылки дронами, а дрон поднимает не больше 2000 г. Вес посылок по очереди "
              "записан в массиве `parcels`. Проверка веса и взлёт — два разных метода, а отказ обрабатывает только `main`.",
        steps=["Создай класс `TooHeavyException`, унаследованный от `Exception`, с конструктором "
               "`TooHeavyException(String message)`, который передаёт текст в `super(message)`.",
               "Добавь в класс `Solution` метод `static void checkWeight(int grams) throws TooHeavyException`: если "
               "`grams` больше 2000, он выбрасывает исключение с сообщением `Посылка 2500 г тяжелее 2000 г` (с весом посылки).",
               "Добавь метод `static void launch(int grams) throws TooHeavyException`: он вызывает `checkWeight(grams)`, "
               "а затем выводит `Дрон взлетел, груз 800 г`. Сам он исключение не ловит — только объявляет в `throws`.",
               "В `main` для каждой посылки вызови `launch` в блоке `try`, а в `catch` выведи `Отказ: ` и сообщение "
               "исключения. После цикла выведи `Отправлено посылок: 2`."],
        hint="Счётчик отправленных увеличивай в `try` сразу после вызова `launch`: если посылка слишком тяжёлая, "
             "исключение пролетит из `checkWeight` через `launch` прямо в `catch` в `main`, и эта строка не выполнится.",
        solution=with_methods(DRONE_MAIN, DRONE_METHODS),
        classes=TOO_HEAVY,
        wrong=[("счётчик увеличивается после try/catch — посылки с отказом тоже считаются отправленными",
                with_methods(DRONE_MAIN.replace("        sent++;\n", "").replace("    }\n}\nSystem", "    }\n    sent++;\n}\nSystem"),
                             DRONE_METHODS)),
               ("проверка через >= — посылку ровно 2000 г дрон не берёт",
                with_methods(DRONE_MAIN, DRONE_METHODS.replace("grams > 2000", "grams >= 2000")))],
        constructs=["try", "function", "class"],
        checks=DRONE_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-throws-transport-card", title="Транспортная карта",
        given=[("int", "balance"), ("int[]", "fares")],
        variants=[{"balance": "100", "fares": "{62, 62, 30}"}, {"balance": "50", "fares": "{70, 46}"},
                  {"balance": "150", "fares": "{50, 50, 50}"}],
        hidden=[{"balance": "0", "fares": "{30}"}, {"balance": "200", "fares": "{}"}, {"balance": "60", "fares": "{60, 1}"},
                {"balance": "90", "fares": "{100, 45, 46, 45}"}],
        intro="На транспортной карте лежит `balance` руб. За день пассажир делает несколько поездок, их стоимость "
              "по порядку записана в массиве `fares`. Если денег не хватает, турникет не пропускает, но следующая, "
              "более дешёвая поездка может пройти.",
        steps=["Создай класс `LowBalanceException`, унаследованный от `Exception`, с конструктором "
               "`LowBalanceException(String message)`, который передаёт текст в `super(message)`.",
               "Создай класс `TransportCard` с приватным полем `balance`, конструктором `TransportCard(int balance)` "
               "и методом `int getBalance()`.",
               "Добавь в него метод `void pay(int fare) throws LowBalanceException`: если `fare` больше баланса, он "
               "выбрасывает исключение с сообщением `Не хватает 24 руб.` (сколько не хватает), иначе списывает `fare` с баланса.",
               "В `main` создай карту с `balance` и для каждой поездки в блоке `try` вызови `pay` и выведи "
               "`Проход, осталось 38 руб.`, а в `catch` выведи `Отказ: ` и сообщение исключения.",
               "После всех поездок выведи `На карте: 8 руб.` — баланс карты."],
        hint="Метод `pay` только сообщает о проблеме через `throw` и не решает, что делать дальше, — это решает `main` "
             "в своём `catch`. Поэтому `throws` пишется у `pay`, а `try`/`catch` — там, где его вызывают.",
        solution=CARD_MAIN,
        classes=LOW_BALANCE + "\n\n" + CARD,
        wrong=[("списывает деньги до проверки — после отказа баланс уходит в минус",
                CARD_MAIN,
                LOW_BALANCE + "\n\n" + CARD.replace(
                    '        if (fare > balance) {\n            throw new LowBalanceException("Не хватает " + (fare - balance) + " руб.");\n        }\n        balance -= fare;\n',
                    '        balance -= fare;\n        if (balance < 0) {\n            throw new LowBalanceException("Не хватает " + (-balance) + " руб.");\n        }\n')),
               ("в конце печатает поле balance из Solution, а не баланс карты — там всё ещё начальная сумма",
                CARD_MAIN.replace('"На карте: " + card.getBalance()', '"На карте: " + balance'))],
        constructs=["try", "class"],
        checks=CARD_CHECKS,
    ),
]
