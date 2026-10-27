"""ENCAPSULATION_BASIC — «Инкапсуляция» (Java). Taught before: everything up to static methods of Solution, classes,
creating objects, constructors, this. Here: `private` fields that code outside the class cannot read or change;
the value changes only through methods that check it (a range, a lower and an upper bound), and is read through
a method. Not yet: the getter/setter pair as a convention (next topic), static fields, exceptions."""
from java_tasks import JavaOutputTask

SKILL = "ENCAPSULATION_BASIC"


def find_class(name: str) -> str:
    return (f'Class<?> c = cls("{name}");\n'
            f'need(c != null, "Создай класс {name} ниже класса Solution (после его закрывающей скобки) и без слова public");\n')


def need_private_field(cls: str, name: str, java_type: str, why: str) -> str:
    """A private instance field of the class with this name and type; `why` says what the privacy protects."""
    return (f'{{ Field f = null; try {{ f = c.getDeclaredField("{name}"); }} catch (NoSuchFieldException e) {{ }}\n'
            f'  need(f != null && f.getType() == {java_type}.class, "Объяви в классе {cls} поле private {java_type} {name}");\n'
            f'  need(!Modifier.isStatic(f.getModifiers()), "Объяви поле {name} в классе {cls} без слова static — тогда у каждого объекта будет своё значение");\n'
            f'  need(Modifier.isPrivate(f.getModifiers()), "Сделай поле {name} закрытым: private {java_type} {name} — {why}"); }}\n')


def need_method(cls: str, returns: str, name: str, params: list[str], why: str) -> str:
    """A non-static method with these parameter types and return type."""
    types = ", ".join(f"{p.split()[0]}.class" for p in params)
    return (f'{{ Method m = null; try {{ m = c.getDeclaredMethod("{name}"{", " + types if types else ""}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(m != null && m.getReturnType() == {returns}.class, "Добавь в класс {cls} метод {returns} {name}({", ".join(params)}) — {why}");\n'
            f'  need(!Modifier.isStatic(m.getModifiers()), "Метод {name} в классе {cls} пиши без слова static — он работает с полями своего объекта"); }}\n')


def need_constructor(cls: str, params: list[str], why: str) -> str:
    types = ", ".join(f"{p.split()[0]}.class" for p in params)
    return (f'{{ Constructor<?> k = null; try {{ k = c.getDeclaredConstructor({types}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(k != null, "Добавь в класс {cls} конструктор {cls}({", ".join(params)}) — {why}"); }}\n')


def need_after_calls(ctor_types: str, ctor_args: str, calls: list[tuple[str, str, str]], field: str, expected: str, message: str) -> str:
    """Creates an object, calls its methods (name, parameter type, argument) and compares a field with `expected`:
    the check inside the class's own method, not in main, is what keeps a wrong value out."""
    code = (f'{{ Object o = null; try {{ Constructor<?> k = c.getDeclaredConstructor({ctor_types}); k.setAccessible(true); '
            f'o = k.newInstance({ctor_args}); }} catch (Exception e) {{ }}\n  try {{\n')
    for name, java_type, arg in calls:
        code += f'    {{ Method m = c.getDeclaredMethod("{name}", {java_type}.class); m.setAccessible(true); m.invoke(o, {arg}); }}\n'
    return (code + '  } catch (Exception e) { }\n'
            f'  Field f = c.getDeclaredField("{field}"); f.setAccessible(true);\n'
            f'  need(o != null && Objects.equals(f.get(o), {expected}), "{message}"); }}\n')


# ───────── Metro card ─────────



# ───────── Password ─────────

ACCOUNT = '''class Account {
    private String password = "start";

    void change(String value) {
        if (value.length() >= 6) {
            password = value;
        }
    }

    String getPassword() {
        return password;
    }
}'''

ACCOUNT_MAIN = '''Account account = new Account();
for (int i = 0; i < tries.length; i++) {
    account.change(tries[i]);
}
System.out.println("Password: " + account.getPassword());'''

# ───────── Coffee machine ─────────

COFFEE = '''class CoffeeMachine {
    private int water;

    CoffeeMachine(int water) {
        this.water = water;
    }

    boolean brew(int ml) {
        if (ml > water) {
            return false;
        }
        water -= ml;
        return true;
    }

    int getWater() {
        return water;
    }
}'''

COFFEE_MAIN = '''CoffeeMachine machine = new CoffeeMachine(tank);
for (int i = 0; i < cups.length; i++) {
    if (machine.brew(cups[i])) {
        System.out.println(cups[i] + " ml: ready");
    } else {
        System.out.println(cups[i] + " ml: not enough water");
    }
}
System.out.println("Water left: " + machine.getWater() + " ml");'''

# ───────── Card with a daily limit ─────────

CARD = '''class BankCard {
    private int balance;
    private int limit;
    private int withdrawn;

    BankCard(int balance, int limit) {
        this.balance = balance;
        this.limit = limit;
    }

    void deposit(int amount) {
        if (amount > 0) {
            balance += amount;
        }
    }

    boolean withdraw(int amount) {
        if (amount > balance || withdrawn + amount > limit) {
            return false;
        }
        balance -= amount;
        withdrawn += amount;
        return true;
    }

    int getBalance() {
        return balance;
    }

    int getWithdrawn() {
        return withdrawn;
    }
}'''

CARD_MAIN = '''BankCard card = new BankCard(balance, limit);
for (int i = 0; i < operations.length; i++) {
    if (operations[i] > 0) {
        card.deposit(operations[i]);
        System.out.println("+" + operations[i] + ": ok");
    } else if (card.withdraw(-operations[i])) {
        System.out.println(operations[i] + ": ok");
    } else {
        System.out.println(operations[i] + ": declined");
    }
}
System.out.println("Balance: " + card.getBalance() + " rub");
System.out.println("Withdrawn today: " + card.getWithdrawn() + " rub");'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-enc-rt-new-password", title="Смена пароля",
        given=[("String[]", "tries")],
        variants=[{"tries": '{"cat", "sunflower", "12345"}'},
                  {"tries": '{"qwerty", "abc", "dog"}'},
                  {"tries": '{"x", "summer2026", "moonlight", "no"}'}],
        hidden=[{"tries": "{}"},
                {"tries": '{"abcde"}'},
                {"tries": '{"abcdef"}'},
                {"tries": '{"winter", "hi", "spring1", "ok"}'}],
        intro="На сайте пароль можно поменять, но новый пароль должен быть не короче 6 символов — короткие варианты сайт "
              "молча пропускает. Сначала у пользователя пароль `start`. Варианты, которые пользователь вводил по очереди, "
              "записаны в массиве `tries`.",
        steps=["Ниже класса `Solution` создай класс `Account` (без `public`) с полем `private String password`, которое сразу "
               "равно `\"start\"`. Из-за `private` код снаружи класса не может ни прочитать, ни изменить поле напрямую.",
               "Добавь метод `void change(String value)`: он записывает `value` в пароль, только если в нём 6 символов или "
               "больше. Иначе пароль не меняется.",
               "Добавь метод `String getPassword()`, который возвращает пароль.",
               "В `main` создай аккаунт, по очереди передай методу `change` все варианты из `tries` и выведи строку вида "
               "`Password: sunflower` — пароль получи через `getPassword()`."],
        hint="Длину строки даёт `value.length()`. Раз поле `private`, из `main` нельзя написать `account.password = ...`: "
             "пароль меняется только через `change`, и каждая попытка обязательно проходит проверку.",
        solution=ACCOUNT_MAIN,
        classes=ACCOUNT,
        wrong=[("change не проверяет длину — короткий пароль тоже принимается",
                ACCOUNT_MAIN, ACCOUNT.replace("        if (value.length() >= 6) {\n            password = value;\n        }",
                                              "        password = value;")),
               ("строгое сравнение — пароль ровно из 6 символов не принимается",
                ACCOUNT_MAIN, ACCOUNT.replace("value.length() >= 6", "value.length() > 6"))],
        constructs=["class"],
        checks=find_class("Account")
               + need_private_field("Account", "password", "String", "тогда пароль меняется только через change с проверкой")
               + need_method("Account", "void", "change", ["String value"], "он меняет пароль, если новый достаточно длинный")
               + need_method("Account", "String", "getPassword", [], "через него код снаружи узнаёт пароль")
               + need_after_calls("", "", [("change", "String", '"longpass"')], "password", '"longpass"',
                                  "Метод change должен записывать в поле password пароль из 6 символов или длиннее")
               + need_after_calls("", "", [("change", "String", '"longpass"'), ("change", "String", '"abc"')], "password", '"longpass"',
                                  "Проверка длины должна быть внутри change: пароль короче 6 символов метод не записывает"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-enc-rt-coffee-machine", title="Кофемашина",
        given=[("int", "tank"), ("int[]", "cups")],
        variants=[{"tank": "1000", "cups": "{250, 300, 400, 200}"},
                  {"tank": "500", "cups": "{200, 400, 100}"},
                  {"tank": "800", "cups": "{350, 350, 150, 100}"}],
        hidden=[{"tank": "300", "cups": "{300, 1}"},
                {"tank": "0", "cups": "{50}"},
                {"tank": "1500", "cups": "{}"},
                {"tank": "600", "cups": "{700, 200, 200, 201, 199}"}],
        intro="В баке кофемашины `tank` мл воды. Посетители по очереди заказывают кофе, сколько миллилитров нужно на каждую "
              "чашку, записано в массиве `cups`. Если воды на чашку не хватает, машина её не готовит и воду не тратит.",
        steps=["Ниже класса `Solution` создай класс `CoffeeMachine` (без `public`) с закрытым полем `private int water` и "
               "конструктором `CoffeeMachine(int water)`, который запоминает, сколько воды в баке.",
               "Добавь метод `boolean brew(int ml)`: если воды в баке не меньше, чем `ml`, он уменьшает воду на `ml` и "
               "возвращает `true`; иначе ничего не меняет и возвращает `false`. Ещё добавь метод `int getWater()`, "
               "который возвращает, сколько воды осталось.",
               "В `main` создай машину с баком `tank` и для каждой чашки из `cups` вызови `brew`. Если вызов вернул `true`, "
               "выведи строку вида `250 ml: ready`, иначе — `200 ml: not enough water`.",
               "Последней строкой выведи строку вида `Water left: 50 ml` — число получи через `getWater()`."],
        hint="Поле закрыто, поэтому `main` не может сам слить воду из бака: `machine.water -= 250` не скомпилируется. "
             "Единственный путь — метод `brew`, и проверка в нём сработает при каждой чашке. Если воды ровно столько, "
             "сколько нужно, чашка получается, а бак становится пустым.",
        solution=COFFEE_MAIN,
        classes=COFFEE,
        wrong=[("строгое сравнение: когда воды ровно на чашку, машина отказывает",
                COFFEE_MAIN, COFFEE.replace("ml > water", "ml >= water")),
               ("не проверяет воду — вода в баке уходит в минус",
                COFFEE_MAIN, COFFEE.replace("        if (ml > water) {\n            return false;\n        }\n", ""))],
        constructs=["class"],
        checks=find_class("CoffeeMachine")
               + need_private_field("CoffeeMachine", "water", "int", "тогда вода тратится только через brew с проверкой")
               + need_constructor("CoffeeMachine", ["int water"], "он запоминает, сколько воды в баке")
               + need_method("CoffeeMachine", "boolean", "brew", ["int ml"], "он готовит чашку, если хватает воды")
               + need_method("CoffeeMachine", "int", "getWater", [], "через него код снаружи узнаёт остаток воды")
               + need_after_calls("int.class", "500", [("brew", "int", "200")], "water", "300",
                                  "Метод brew должен уменьшать воду в поле water на объём чашки")
               + need_after_calls("int.class", "500", [("brew", "int", "200"), ("brew", "int", "400")], "water", "300",
                                  "Проверка должна быть внутри brew: если воды не хватает, вода в баке не меняется"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-enc-rt-card-limit", title="Лимит по карте",
        given=[("int", "balance"), ("int", "limit"), ("int[]", "operations")],
        variants=[{"balance": "8000", "limit": "5000", "operations": "{-3000, -2500, 1000, -2000}"},
                  {"balance": "1000", "limit": "3000", "operations": "{-1500, 2000, -1500, -1500}"},
                  {"balance": "20000", "limit": "10000", "operations": "{-4000, -6000, -1, 500}"}],
        hidden=[{"balance": "500", "limit": "1000", "operations": "{-500, -1}"},
                {"balance": "0", "limit": "2000", "operations": "{}"},
                {"balance": "3000", "limit": "1000", "operations": "{-1000, 700, -1}"},
                {"balance": "100", "limit": "5000", "operations": "{300, -401, -400, 5000, -4600, -1}"}],
        intro="Банк защищает карту: снять с неё можно не больше, чем лежит на счёте, и за день — не больше `limit` руб. "
              "Сначала на счёте `balance` руб. Операции за день по порядку записаны в массиве `operations`: "
              "положительное число — пополнение, отрицательное — снятие (сумма без минуса).",
        steps=["Ниже класса `Solution` создай класс `BankCard` (без `public`) с закрытыми полями `private int balance`, "
               "`private int limit` и `private int withdrawn` (сколько уже снято за день) и конструктором "
               "`BankCard(int balance, int limit)`.",
               "Добавь метод `void deposit(int amount)`: он прибавляет `amount` к балансу, если сумма больше 0. Добавь метод "
               "`boolean withdraw(int amount)`: если сумма больше баланса или вместе с уже снятым превысит `limit`, он "
               "возвращает `false` и ничего не меняет; иначе уменьшает баланс, увеличивает `withdrawn` и возвращает `true`.",
               "Добавь методы `int getBalance()` и `int getWithdrawn()`.",
               "В `main` создай карту и пройди по `operations`: пополнение выводи строкой вида `+1000: ok`; для снятия вызови "
               "`withdraw` с суммой без минуса и выведи `-3000: ok` или `-2500: declined`. В конце выведи строки вида "
               "`Balance: 4000 rub` и `Withdrawn today: 5000 rub`."],
        hint="Сумму без минуса даёт `-operations[i]`. Лимит касается суммы всех снятий за день, поэтому проверяй "
             "`withdrawn + amount > limit`. Снять ровно до лимита можно.",
        solution=CARD_MAIN,
        classes=CARD,
        wrong=[("проверяет лимит только для одной операции, а не для суммы снятий за день",
                CARD_MAIN, CARD.replace("withdrawn + amount > limit", "amount > limit")),
               ("строгое сравнение с балансом: снять всё до копейки нельзя",
                CARD_MAIN, CARD.replace("amount > balance ||", "amount >= balance ||"))],
        constructs=["class"],
        checks=find_class("BankCard")
               + need_private_field("BankCard", "balance", "int", "тогда баланс меняется только через методы с проверкой")
               + need_private_field("BankCard", "limit", "int", "лимит нельзя поднять снаружи класса")
               + need_private_field("BankCard", "withdrawn", "int", "снятое за день нельзя «обнулить» снаружи класса")
               + need_constructor("BankCard", ["int balance", "int limit"], "он запоминает баланс и дневной лимит")
               + need_method("BankCard", "void", "deposit", ["int amount"], "он пополняет карту")
               + need_method("BankCard", "boolean", "withdraw", ["int amount"], "он снимает деньги, если это разрешено")
               + need_method("BankCard", "int", "getBalance", [], "через него код снаружи узнаёт баланс")
               + need_method("BankCard", "int", "getWithdrawn", [], "через него код снаружи узнаёт, сколько снято за день")
               + need_after_calls("int.class, int.class", "1000, 500", [("withdraw", "int", "300")], "balance", "700",
                                  "Метод withdraw должен уменьшать баланс на снятую сумму")
               + need_after_calls("int.class, int.class", "1000, 500", [("withdraw", "int", "300"), ("withdraw", "int", "300")],
                                  "balance", "700", "Проверка лимита должна быть внутри withdraw: за день нельзя снять больше limit"),
    ),
]
