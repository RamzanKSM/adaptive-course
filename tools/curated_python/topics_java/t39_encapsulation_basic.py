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

METRO = '''class MetroCard {
    private int balance;

    void topUp(int amount) {
        if (amount >= 1 && amount <= 3000) {
            balance += amount;
        }
    }

    int getBalance() {
        return balance;
    }
}'''

METRO_MAIN = '''MetroCard card = new MetroCard();
for (int i = 0; i < amounts.length; i++) {
    card.topUp(amounts[i]);
}
System.out.println("Card balance: " + card.getBalance() + " rub");'''

# ───────── Elevator ─────────

ELEVATOR = '''class Elevator {
    private int floor;
    private int top;

    Elevator(int top) {
        this.top = top;
        this.floor = 1;
    }

    boolean goTo(int target) {
        if (target < 1 || target > top) {
            return false;
        }
        floor = target;
        return true;
    }

    int getFloor() {
        return floor;
    }
}'''

ELEVATOR_MAIN = '''Elevator elevator = new Elevator(top);
for (int i = 0; i < requests.length; i++) {
    if (elevator.goTo(requests[i])) {
        System.out.println("Going to floor " + requests[i]);
    } else {
        System.out.println("No floor " + requests[i]);
    }
}
System.out.println("Elevator on floor " + elevator.getFloor());'''

# ───────── Hero's health ─────────

HERO = '''class Hero {
    private int health = 100;

    void heal(int amount) {
        health += amount;
        if (health > 100) {
            health = 100;
        }
    }

    void damage(int amount) {
        health -= amount;
        if (health < 0) {
            health = 0;
        }
    }

    int getHealth() {
        return health;
    }
}'''

HERO_MAIN = '''Hero hero = new Hero();
for (int i = 0; i < events.length; i++) {
    if (events[i] > 0) {
        hero.heal(events[i]);
    } else {
        hero.damage(-events[i]);
    }
    System.out.println("Health: " + hero.getHealth());
}
if (hero.getHealth() == 0) {
    System.out.println("Hero is out");
} else {
    System.out.println("Hero is still in");
}'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-enc-metro-card", title="Пополнение карты метро",
        given=[("int[]", "amounts")],
        variants=[{"amounts": "{500, -100, 3000, 0, 250}"}, {"amounts": "{1000, 5000, 200}"}, {"amounts": "{-50, 100, 3001, 2999}"}],
        hidden=[{"amounts": "{}"}, {"amounts": "{3000}"}, {"amounts": "{1, 0, -1}"}, {"amounts": "{4000, 3500}"},
                {"amounts": "{700, 800, 900, 3000, 3000}"}],
        intro="Терминал в метро пополняет транспортную карту. За один раз на карту можно положить от 1 до 3000 руб., "
              "но пассажиры иногда вводят ноль, отрицательное число или слишком большую сумму — такие пополнения карта "
              "должна пропускать. Суммы, которые вводили по очереди, записаны в массиве `amounts`.",
        steps=["Ниже класса `Solution` создай класс `MetroCard` (без `public`) с полем `private int balance`. Слово `private` "
               "значит, что поле видно только внутри класса: код снаружи не может ни прочитать, ни изменить его напрямую.",
               "Добавь метод `void topUp(int amount)`: он прибавляет `amount` к балансу, только если сумма от 1 до 3000 "
               "включительно. Иначе баланс не меняется.",
               "Добавь метод `int getBalance()`, который возвращает баланс.",
               "В `main` создай карту, по очереди передай методу `topUp` все суммы из `amounts` и выведи строку вида "
               "`Card balance: 3750 rub` — число получи через `getBalance()`."],
        hint="Раз поле `private`, из `main` нельзя написать `card.balance += amount` — Java не скомпилирует такую строку. "
             "Менять баланс можно только через `topUp`, а значит, каждая сумма обязательно пройдёт проверку.",
        solution=METRO_MAIN,
        classes=METRO,
        wrong=[("topUp не проверяет сумму — отрицательные и слишком большие суммы тоже попадают на карту",
                METRO_MAIN, METRO.replace("        if (amount >= 1 && amount <= 3000) {\n            balance += amount;\n        }",
                                          "        balance += amount;")),
               ("верхняя граница строгая — ровно 3000 руб. карта не принимает",
                METRO_MAIN, METRO.replace("amount <= 3000", "amount < 3000"))],
        constructs=["class"],
        checks=find_class("MetroCard")
               + need_private_field("MetroCard", "balance", "int", "тогда баланс меняется только через topUp с проверкой")
               + need_method("MetroCard", "void", "topUp", ["int amount"], "он пополняет карту, если сумма допустимая")
               + need_method("MetroCard", "int", "getBalance", [], "через него код снаружи узнаёт баланс")
               + need_after_calls("", "", [("topUp", "int", "100")], "balance", "100",
                                  "Метод topUp должен прибавлять к балансу сумму от 1 до 3000")
               + need_after_calls("", "", [("topUp", "int", "100"), ("topUp", "int", "5000"), ("topUp", "int", "-50"), ("topUp", "int", "0")],
                                  "balance", "100", "Проверка суммы должна быть внутри topUp: суммы меньше 1 и больше 3000 метод не прибавляет к балансу"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-enc-elevator", title="Лифт",
        given=[("int", "top"), ("int[]", "requests")],
        variants=[{"top": "9", "requests": "{5, 12, 1, 0, 9}"},
                  {"top": "5", "requests": "{3, 6, -1}"},
                  {"top": "16", "requests": "{16, 8, 17, 2}"}],
        hidden=[{"top": "1", "requests": "{1, 2}"},
                {"top": "12", "requests": "{}"},
                {"top": "25", "requests": "{0, 25, 26, 13}"},
                {"top": "3", "requests": "{-3, 4, 0}"}],
        intro="В доме `top` этажей, а лифт стоит на первом. Лифтом управляет программа диспетчера, и в неё по очереди "
              "приходят номера этажей из массива `requests`. Иногда номер приходит с ошибкой — 0, отрицательный или больше `top`: "
              "такого этажа в доме нет, и лифт должен остаться на месте.",
        steps=["Ниже класса `Solution` создай класс `Elevator` (без `public`) с закрытыми полями `private int floor` "
               "(текущий этаж) и `private int top` (сколько этажей в доме).",
               "Добавь конструктор `Elevator(int top)`: он запоминает число этажей, а лифт ставит на 1-й этаж.",
               "Добавь метод `boolean goTo(int target)`: если этаж `target` есть в доме (от 1 до `top` включительно), метод "
               "перемещает лифт туда и возвращает `true`, иначе лифт остаётся на месте и метод возвращает `false`. "
               "Ещё добавь метод `int getFloor()`, который возвращает текущий этаж.",
               "В `main` создай лифт для дома из `top` этажей и для каждого номера из `requests` вызови `goTo`. Если вызов "
               "вернул `true`, выведи строку вида `Going to floor 5`, иначе — `No floor 12`. В конце выведи строку вида "
               "`Elevator on floor 9` — номер получи через `getFloor()`."],
        hint="Поля закрыты, поэтому `main` не может сам поставить лифт на этаж: `elevator.floor = 12` не скомпилируется. "
             "Единственный путь — метод `goTo`, и проверка в нём сработает при каждом вызове.",
        solution=ELEVATOR_MAIN,
        classes=ELEVATOR,
        wrong=[("не проверяет нижнюю границу — лифт «едет» на 0 и отрицательные этажи",
                ELEVATOR_MAIN, ELEVATOR.replace("target < 1 || target > top", "target > top")),
               ("последний этаж считает несуществующим: условие `target >= top`",
                ELEVATOR_MAIN, ELEVATOR.replace("target > top", "target >= top"))],
        constructs=["class"],
        checks=find_class("Elevator")
               + need_private_field("Elevator", "floor", "int", "тогда лифт перемещается только через goTo с проверкой")
               + need_private_field("Elevator", "top", "int", "число этажей нельзя менять снаружи класса")
               + need_constructor("Elevator", ["int top"], "он запоминает число этажей и ставит лифт на 1-й этаж")
               + need_method("Elevator", "boolean", "goTo", ["int target"], "он перемещает лифт, если такой этаж есть")
               + need_method("Elevator", "int", "getFloor", [], "через него код снаружи узнаёт этаж")
               + need_after_calls("int.class", "5", [("goTo", "int", "3")], "floor", "3",
                                  "Метод goTo должен перемещать лифт на этаж, который есть в доме: записывать его в поле floor")
               + need_after_calls("int.class", "5", [("goTo", "int", "3"), ("goTo", "int", "9"), ("goTo", "int", "0")],
                                  "floor", "3", "Проверка должна быть внутри goTo: если такого этажа в доме нет, лифт остаётся на месте"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-enc-hero-health", title="Здоровье героя",
        given=[("int[]", "events")],
        variants=[{"events": "{-30, -50, 40, -70, 25}"}, {"events": "{50, -20, -90}"}, {"events": "{-45, 30, 30, -100}"}],
        hidden=[{"events": "{-100}"}, {"events": "{10}"}, {"events": "{-99, -1, 5}"}, {"events": "{-60, -60, 100, -40}"},
                {"events": "{}"}],
        intro="В игре здоровье героя всегда лежит от 0 до 100: лечение не поднимает его выше 100, а урон не опускает ниже 0. "
              "Герой начинает со 100. События боя записаны по порядку в массиве `events`: положительное число — лечение "
              "на столько очков, отрицательное — урон (число без минуса).",
        steps=["Ниже класса `Solution` создай класс `Hero` (без `public`) с закрытым полем `private int health`, которое сразу равно 100.",
               "Добавь методы `void heal(int amount)` и `void damage(int amount)`: первый прибавляет `amount` к здоровью, второй "
               "вычитает. После изменения каждый метод следит за границами: больше 100 становится 100, меньше 0 становится 0.",
               "Добавь метод `int getHealth()`, который возвращает здоровье.",
               "В `main` создай героя и пройди по `events`: для положительного числа вызови `heal`, для отрицательного — "
               "`damage` с этим числом без минуса. После каждого события выведи строку вида `Health: 70`.",
               "В конце выведи `Hero is out`, если здоровье равно 0, иначе — `Hero is still in`."],
        hint="Число без минуса — это `-events[i]`: минус перед отрицательным числом делает его положительным. А границы "
             "проверяй внутри методов: тогда никакой код снаружи класса не сможет сделать здоровье, например, 130.",
        solution=HERO_MAIN,
        classes=HERO,
        wrong=[("лечение не ограничено сверху — здоровье поднимается выше 100",
                HERO_MAIN, HERO.replace("        if (health > 100) {\n            health = 100;\n        }\n", "")),
               ("урон не ограничен снизу — здоровье уходит в минус",
                HERO_MAIN, HERO.replace("        if (health < 0) {\n            health = 0;\n        }\n", ""))],
        constructs=["class"],
        checks=find_class("Hero")
               + need_private_field("Hero", "health", "int", "тогда здоровье меняется только через heal и damage, которые следят за границами")
               + need_method("Hero", "void", "heal", ["int amount"], "он лечит героя, но не выше 100")
               + need_method("Hero", "void", "damage", ["int amount"], "он наносит урон, но не ниже 0")
               + need_method("Hero", "int", "getHealth", [], "через него код снаружи узнаёт здоровье")
               + need_after_calls("", "", [("damage", "int", "30"), ("heal", "int", "50")], "health", "100",
                                  "Метод heal не должен поднимать здоровье выше 100: после лечения проверь границу внутри метода")
               + need_after_calls("", "", [("damage", "int", "150")], "health", "0",
                                  "Метод damage не должен опускать здоровье ниже 0: после урона проверь границу внутри метода"),
    ),
]
