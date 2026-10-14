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
LIFT_MAIN = ('try {\n    checkLoad(load);\n    System.out.println("The lift is going up");\n} catch (OverloadException e) {\n'
             '    System.out.println(e.getMessage());\n    System.out.println("Take off some of the load");\n}')
LIFT_CHECK = '''static void checkLoad(int load) throws OverloadException {
    if (load > 400) {
        throw new OverloadException("Overload by " + (load - 400) + " kg");
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
              '    } catch (TooHeavyException e) {\n        System.out.println("Refused: " + e.getMessage());\n    }\n}\n'
              'System.out.println("Parcels sent: " + sent);')
DRONE_METHODS = '''static void checkWeight(int grams) throws TooHeavyException {
    if (grams > 2000) {
        throw new TooHeavyException("Parcel of " + grams + " g is heavier than 2000 g");
    }
}

static void launch(int grams) throws TooHeavyException {
    checkWeight(grams);
    System.out.println("Drone took off, load " + grams + " g");
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
            throw new LowBalanceException("Not enough money: " + (fare - balance) + " rub short");
        }
        balance -= fare;
    }
}'''
CARD_MAIN = ('TransportCard card = new TransportCard(balance);\nfor (int fare : fares) {\n    try {\n'
             '        card.pay(fare);\n        System.out.println("Go ahead, left " + card.getBalance() + " rub");\n'
             '    } catch (LowBalanceException e) {\n        System.out.println("Refused: " + e.getMessage());\n    }\n}\n'
             'System.out.println("On the card: " + card.getBalance() + " rub");')
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

# ── 4. Возрастное ограничение ──
AGE_LIMIT = exception_class("AgeLimitException")
CINEMA_MAIN = ('try {\n    checkAge(age, rating);\n    System.out.println("Enjoy the film");\n} catch (AgeLimitException e) {\n'
               '    System.out.println(e.getMessage());\n    System.out.println("Choose another film");\n}')
CINEMA_CHECK = """static void checkAge(int age, int rating) throws AgeLimitException {
    if (age < rating) {
        throw new AgeLimitException("The film is " + rating + "+, you are " + age);
    }
}"""
CINEMA_CHECKS = checked_class_check("AgeLimitException", "это проверяемое исключение: Java потребует объявить его в throws и обработать") + """Method m = null;
try { m = Solution.class.getDeclaredMethod("checkAge", int.class, int.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()), "Добавь в класс Solution метод static void checkAge(int age, int rating) throws AgeLimitException");
need(Arrays.asList(m.getExceptionTypes()).contains(ex), "Объяви в методе checkAge именно throws AgeLimitException: так тот, кто вызывает метод, знает, какую ошибку обработать");
m.setAccessible(true);
boolean thrown = false;
try { m.invoke(null, 10, 16); } catch (InvocationTargetException e) { thrown = ex.isInstance(e.getCause()); }
need(thrown, "Если зрителю меньше лет, чем указано в ограничении, метод checkAge должен выбрасывать AgeLimitException через throw");
try { m.invoke(null, 16, 16); } catch (InvocationTargetException e) { need(false, "Зрителю ровно 16 лет на фильм 16+ можно: при таком возрасте checkAge не должен выбрасывать исключение"); }"""

# ── 5. Промокод ──
EXPIRED = exception_class("ExpiredCodeException")
UNKNOWN = exception_class("UnknownCodeException")
PROMO_MAIN = ('try {\n    System.out.println("To pay: " + applyCode(price, code) + " rub");\n'
              '} catch (ExpiredCodeException e) {\n    System.out.println(e.getMessage());\n'
              '    System.out.println("To pay: " + price + " rub");\n'
              '} catch (UnknownCodeException e) {\n    System.out.println(e.getMessage());\n'
              '    System.out.println("Check the code and try again");\n}')
PROMO_METHOD = """static int applyCode(int price, String code) throws ExpiredCodeException, UnknownCodeException {
    if (code.equals("SALE20")) {
        return price - price * 20 / 100;
    }
    if (code.equals("SPRING")) {
        throw new ExpiredCodeException("Code SPRING has expired");
    }
    throw new UnknownCodeException("Unknown code: " + code);
}"""
PROMO_CHECKS = """Class<?> expired = cls("ExpiredCodeException");
Class<?> unknown = cls("UnknownCodeException");
need(expired != null && unknown != null && Exception.class.isAssignableFrom(expired) && Exception.class.isAssignableFrom(unknown) && !RuntimeException.class.isAssignableFrom(expired) && !RuntimeException.class.isAssignableFrom(unknown), "Создай два класса, ExpiredCodeException extends Exception и UnknownCodeException extends Exception, — это проверяемые исключения для двух разных отказов");
Method m = null;
try { m = Solution.class.getDeclaredMethod("applyCode", int.class, String.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, "Добавь в класс Solution метод static int applyCode(int price, String code): он возвращает цену после промокода");
need(Arrays.asList(m.getExceptionTypes()).containsAll(Arrays.asList(expired, unknown)), "Объяви в методе applyCode оба исключения: throws ExpiredCodeException, UnknownCodeException");
m.setAccessible(true);
boolean thrown = false;
try { m.invoke(null, 1000, "SPRING"); } catch (InvocationTargetException e) { thrown = expired.isInstance(e.getCause()); }
need(thrown, "Для кода SPRING метод applyCode должен выбрасывать ExpiredCodeException через throw");
thrown = false;
try { m.invoke(null, 1000, "HELLO"); } catch (InvocationTargetException e) { thrown = unknown.isInstance(e.getCause()); }
need(thrown, "Для незнакомого кода метод applyCode должен выбрасывать UnknownCodeException через throw");"""

# ── 6. Библиотека ──
NOT_AVAILABLE = exception_class("NotAvailableException")
LIBRARY = """class Library {
    private List<String> shelf;

    Library(List<String> books) {
        shelf = new ArrayList<>(books);
    }

    void borrow(String title) throws NotAvailableException {
        if (!shelf.contains(title)) {
            throw new NotAvailableException("No free copy of " + title);
        }
        shelf.remove(title);
    }

    int left() {
        return shelf.size();
    }
}"""
LIBRARY_MAIN = ('Library library = new Library(books);\ntry {\n    for (String title : wishlist) {\n'
                '        library.borrow(title);\n        System.out.println("Borrowed: " + title);\n    }\n'
                '    System.out.println("Got the whole list");\n} catch (NotAvailableException e) {\n'
                '    System.out.println("Stopped: " + e.getMessage());\n}\n'
                'System.out.println("Left on the shelf: " + library.left());')
LIBRARY_CHECKS = checked_class_check("NotAvailableException", "это проверяемое исключение для книги, которой нет на полке") + """Class<?> c = cls("Library");
need(c != null, "Создай класс Library: он хранит книги на полке и выдаёт их");
Method borrow = null;
try { borrow = c.getDeclaredMethod("borrow", String.class); } catch (NoSuchMethodException e) { }
need(borrow != null && Arrays.asList(borrow.getExceptionTypes()).contains(ex), "Объяви в классе Library метод void borrow(String title) throws NotAvailableException: так main узнает, что отказ нужно обработать");
boolean closed = false;
try { closed = Modifier.isPrivate(c.getDeclaredField("shelf").getModifiers()); } catch (NoSuchFieldException e) { }
need(closed, "Сделай поле shelf в классе Library приватным: книги с полки берут только через borrow");
Object library = null;
try { Constructor<?> k = c.getDeclaredConstructor(List.class); k.setAccessible(true); library = k.newInstance(new ArrayList<>(List.of("Dune"))); } catch (NoSuchMethodException | InvocationTargetException e) { }
need(library != null, "Добавь в класс Library конструктор Library(List<String> books)");
borrow.setAccessible(true);
try { borrow.invoke(library, "Dune"); } catch (InvocationTargetException e) { need(false, "Книгу, которая есть на полке, метод borrow должен выдавать без исключения"); }
boolean thrown = false;
try { borrow.invoke(library, "Dune"); } catch (InvocationTargetException e) { thrown = ex.isInstance(e.getCause()); }
need(thrown, "Если книги на полке не осталось, метод borrow должен выбрасывать NotAvailableException через throw — и убирать выданную книгу с полки");"""

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
               "больше 400, он выбрасывает `OverloadException` с сообщением `Overload by 50 kg` — на сколько вес "
               "больше 400.",
               "В `main` в блоке `try` вызови `checkLoad(load)` и выведи `The lift is going up`.",
               "В `catch (OverloadException e)` выведи сообщение исключения, а следующей строкой — `Take off some of the load`."],
        hint="Исключение, унаследованное от `Exception`, — проверяемое: Java не скомпилирует метод, который его "
             "выбрасывает, без `throws OverloadException` в объявлении, и не даст вызвать такой метод без `try`/`catch`.",
        solution=with_methods(LIFT_MAIN, LIFT_CHECK),
        classes=OVERLOAD,
        wrong=[("«Take off some of the load» стоит после try/catch — печатается и тогда, когда лифт поехал",
                with_methods('try {\n    checkLoad(load);\n    System.out.println("The lift is going up");\n'
                             '} catch (OverloadException e) {\n    System.out.println(e.getMessage());\n}\n'
                             'System.out.println("Take off some of the load");', LIFT_CHECK)),
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
               "`grams` больше 2000, он выбрасывает исключение с сообщением `Parcel of 2500 g is heavier than 2000 g` (с весом посылки).",
               "Добавь метод `static void launch(int grams) throws TooHeavyException`: он вызывает `checkWeight(grams)`, "
               "а затем выводит `Drone took off, load 800 g`. Сам он исключение не ловит — только объявляет в `throws`.",
               "В `main` для каждой посылки вызови `launch` в блоке `try`, а в `catch` выведи `Refused: ` и сообщение "
               "исключения. После цикла выведи `Parcels sent: 2`."],
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
               "выбрасывает исключение с сообщением `Not enough money: 24 rub short` (сколько не хватает), иначе списывает `fare` с баланса.",
               "В `main` создай карту с `balance` и для каждой поездки в блоке `try` вызови `pay` и выведи "
               "`Go ahead, left 38 rub`, а в `catch` выведи `Refused: ` и сообщение исключения.",
               "После всех поездок выведи `On the card: 8 rub` — баланс карты."],
        hint="Метод `pay` только сообщает о проблеме через `throw` и не решает, что делать дальше, — это решает `main` "
             "в своём `catch`. Поэтому `throws` пишется у `pay`, а `try`/`catch` — там, где его вызывают.",
        solution=CARD_MAIN,
        classes=LOW_BALANCE + "\n\n" + CARD,
        wrong=[("списывает деньги до проверки — после отказа баланс уходит в минус",
                CARD_MAIN,
                LOW_BALANCE + "\n\n" + CARD.replace(
                    '        if (fare > balance) {\n            throw new LowBalanceException("Not enough money: " + (fare - balance) + " rub short");\n        }\n        balance -= fare;\n',
                    '        balance -= fare;\n        if (balance < 0) {\n            throw new LowBalanceException("Not enough money: " + (-balance) + " rub short");\n        }\n')),
               ("в конце печатает поле balance из Solution, а не баланс карты — там всё ещё начальная сумма",
                CARD_MAIN.replace('"On the card: " + card.getBalance()', '"On the card: " + balance'))],
        constructs=["try", "class"],
        checks=CARD_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-throws-cinema-age", title="Фильм с возрастным ограничением",
        given=[("int", "age"), ("int", "rating")],
        variants=[{"age": "12", "rating": "16"}, {"age": "18", "rating": "12"}, {"age": "15", "rating": "18"}],
        hidden=[{"age": "16", "rating": "16"}, {"age": "6", "rating": "0"}, {"age": "11", "rating": "12"},
                {"age": "40", "rating": "18"}],
        intro="Кинотеатр продаёт билет, только если зрителю не меньше лет, чем указано в возрастном ограничении фильма. "
              "Возраст зрителя записан в `age`, ограничение — в `rating` (например, 16 означает «16+»). Отказ — ожидаемая "
              "ситуация, которую нельзя забыть обработать, поэтому для неё нужно своё проверяемое исключение.",
        steps=["Создай класс `AgeLimitException`, унаследованный от `Exception`, с конструктором "
               "`AgeLimitException(String message)`, который передаёт текст в `super(message)`.",
               "Добавь в класс `Solution` метод `static void checkAge(int age, int rating) throws AgeLimitException`. "
               "Если `age` меньше `rating`, он выбрасывает `AgeLimitException` с сообщением вида "
               "`The film is 16+, you are 12`.",
               "В `main` в блоке `try` вызови `checkAge(age, rating)` и выведи `Enjoy the film`.",
               "В `catch (AgeLimitException e)` выведи сообщение исключения, а следующей строкой — `Choose another film`."],
        hint="Слово `throws` в заголовке метода предупреждает всех, кто его вызывает: «я могу выбросить такое "
             "исключение». Для проверяемого исключения Java без этого объявления метод не скомпилирует.",
        solution=with_methods(CINEMA_MAIN, CINEMA_CHECK),
        classes=AGE_LIMIT,
        wrong=[("проверяет через <= — зрителю ровно нужного возраста отказывают",
                with_methods(CINEMA_MAIN, CINEMA_CHECK.replace("age < rating", "age <= rating"))),
               ("«Choose another film» стоит после try/catch — печатается и тогда, когда билет продан",
                with_methods('try {\n    checkAge(age, rating);\n    System.out.println("Enjoy the film");\n'
                             '} catch (AgeLimitException e) {\n    System.out.println(e.getMessage());\n}\n'
                             'System.out.println("Choose another film");', CINEMA_CHECK))],
        constructs=["try", "function", "class"],
        checks=CINEMA_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-throws-promo-code", title="Промокод в интернет-магазине",
        given=[("int", "price"), ("String", "code")],
        variants=[{"price": "1500", "code": '"SALE20"'}, {"price": "2400", "code": '"SPRING"'},
                  {"price": "990", "code": '"FREE"'}],
        hidden=[{"price": "1000", "code": '"sale20"'}, {"price": "50", "code": '"SALE20"'}, {"price": "700", "code": '"SPRING"'},
                {"price": "3333", "code": '""'}],
        intro="Интернет-магазин принимает промокоды. Покупка стоит `price` руб., покупатель ввёл код `code`. Код `SALE20` "
              "даёт скидку 20%, у кода `SPRING` закончился срок, а любой другой код магазину незнаком. Для двух "
              "отказов нужны два разных проверяемых исключения, потому что реагировать на них надо по-разному.",
        steps=["Создай два класса исключений, унаследованных от `Exception`: `ExpiredCodeException` и "
               "`UnknownCodeException`, — у каждого конструктор с `String message`, который передаёт текст в `super(message)`.",
               "Добавь в класс `Solution` метод `static int applyCode(int price, String code) throws ExpiredCodeException, "
               "UnknownCodeException`. Для кода `SALE20` он возвращает `price - price * 20 / 100`; для `SPRING` "
               "выбрасывает `ExpiredCodeException` с сообщением `Code SPRING has expired`; для любого другого кода — "
               "`UnknownCodeException` с сообщением вида `Unknown code: FREE`. Строки сравнивай через `equals`.",
               "В `main` в блоке `try` выведи строку вида `To pay: 1200 rub` с результатом `applyCode(price, code)`.",
               "В `catch (ExpiredCodeException e)` выведи сообщение исключения и строку вида `To pay: 2400 rub` — "
               "полную цену. В `catch (UnknownCodeException e)` выведи сообщение исключения и "
               "`Check the code and try again`."],
        hint="Если метод может выбросить несколько проверяемых исключений, в `throws` их перечисляют через запятую, "
             "а в `main` для каждого пишут свой `catch` со своей реакцией.",
        solution=with_methods(PROMO_MAIN, PROMO_METHOD),
        classes=EXPIRED + "\n\n" + UNKNOWN,
        wrong=[("один общий catch (Exception e) — на просроченный код не показывает полную цену",
                with_methods('try {\n    System.out.println("To pay: " + applyCode(price, code) + " rub");\n'
                             '} catch (Exception e) {\n    System.out.println(e.getMessage());\n'
                             '    System.out.println("Check the code and try again");\n}', PROMO_METHOD)),
               ("возвращает размер скидки, а не цену после скидки",
                with_methods(PROMO_MAIN, PROMO_METHOD.replace("return price - price * 20 / 100;", "return price * 20 / 100;")))],
        constructs=["try", "function", "class", "if"],
        checks=PROMO_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-throws-library-list", title="Книги по списку",
        given=[("List<String>", "books"), ("List<String>", "wishlist")],
        variants=[{"books": 'new ArrayList<>(List.of("Dune", "Emma", "Dune", "Ulysses"))',
                   "wishlist": 'new ArrayList<>(List.of("Dune", "Emma", "Dune"))'},
                  {"books": 'new ArrayList<>(List.of("Hamlet", "Faust", "Ivanhoe"))',
                   "wishlist": 'new ArrayList<>(List.of("Faust", "Faust", "Hamlet"))'},
                  {"books": 'new ArrayList<>(List.of("Robinson Crusoe", "Oliver Twist"))',
                   "wishlist": 'new ArrayList<>(List.of("Oliver Twist", "Moby Dick", "Robinson Crusoe"))'}],
        hidden=[{"books": 'new ArrayList<>(List.of("Odyssey"))', "wishlist": "new ArrayList<>()"},
                {"books": "new ArrayList<>()", "wishlist": 'new ArrayList<>(List.of("Iliad"))'},
                {"books": 'new ArrayList<>(List.of("Beowulf", "Beowulf"))', "wishlist": 'new ArrayList<>(List.of("Beowulf", "Beowulf", "Beowulf"))'},
                {"books": 'new ArrayList<>(List.of("Candide", "Walden", "Oblomov"))', "wishlist": 'new ArrayList<>(List.of("Walden", "Oblomov"))'}],
        intro="Школьник пришёл в библиотеку со списком книг `wishlist` для доклада. На полке стоят книги `books` "
              "(некоторых — по несколько экземпляров). Ему нужен весь список целиком: если какой-то книги не нашлось, "
              "он перестаёт брать остальные и идёт искать её в другую библиотеку.",
        steps=["Создай класс `NotAvailableException`, унаследованный от `Exception`, с конструктором "
               "`NotAvailableException(String message)`, который передаёт текст в `super(message)`.",
               "Создай класс `Library` с приватным полем `List<String> shelf`, конструктором `Library(List<String> books)`, "
               "который кладёт на полку копию списка (`new ArrayList<>(books)`), и методом `int left()` — сколько книг "
               "осталось на полке.",
               "Добавь в него метод `void borrow(String title) throws NotAvailableException`: если на полке нет такой "
               "книги, он выбрасывает исключение с сообщением вида `No free copy of Dune`, иначе убирает один "
               "экземпляр с полки методом `shelf.remove(title)`.",
               "В `main` создай библиотеку из `books`. Поставь `try` вокруг всего цикла по `wishlist`: для каждой книги "
               "вызови `borrow` и выведи строку вида `Borrowed: Dune`, а после цикла, ещё внутри `try`, выведи "
               "`Got the whole list`. В `catch` выведи `Stopped: ` и сообщение исключения.",
               "Последней строкой, после `try`/`catch`, выведи строку вида `Left on the shelf: 2`."],
        hint="Здесь `try` специально стоит вокруг цикла, а не внутри него: исключение из `borrow` прерывает весь "
             "цикл сразу, и следующие книги уже не берутся — именно это и нужно.",
        solution=LIBRARY_MAIN,
        classes=NOT_AVAILABLE + "\n\n" + LIBRARY,
        wrong=[("try внутри цикла — после ненайденной книги школьник продолжает брать остальные",
                'Library library = new Library(books);\nfor (String title : wishlist) {\n    try {\n'
                '        library.borrow(title);\n        System.out.println("Borrowed: " + title);\n'
                '    } catch (NotAvailableException e) {\n        System.out.println("Stopped: " + e.getMessage());\n    }\n}\n'
                'System.out.println("Left on the shelf: " + library.left());'),
               ("не убирает книгу с полки — один экземпляр выдаётся сколько угодно раз",
                LIBRARY_MAIN, NOT_AVAILABLE + "\n\n" + LIBRARY.replace("        shelf.remove(title);\n", ""))],
        constructs=["try", "class", "for"],
        checks=LIBRARY_CHECKS,
    ),
]
