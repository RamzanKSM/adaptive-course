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

# ───────── Weather sensor ─────────

SENSOR = '''class Sensor {
    private int temperature;

    void record(int value) {
        if (value >= -50 && value <= 50) {
            temperature = value;
        }
    }

    int getTemperature() {
        return temperature;
    }
}'''

SENSOR_MAIN = '''Sensor sensor = new Sensor();
for (int i = 0; i < readings.length; i++) {
    sensor.record(readings[i]);
}
System.out.println("Temperature: " + sensor.getTemperature());'''

# ───────── Locker ─────────

LOCKER = '''class Locker {
    private String code;
    private int mistakes;

    Locker(String code) {
        this.code = code;
    }

    boolean tryCode(String attempt) {
        if (mistakes >= 3) {
            return false;
        }
        if (attempt.equals(code)) {
            return true;
        }
        mistakes++;
        return false;
    }

    boolean isBlocked() {
        return mistakes >= 3;
    }
}'''

LOCKER_MAIN = '''Locker locker = new Locker(code);
for (int i = 0; i < attempts.length; i++) {
    if (locker.tryCode(attempts[i])) {
        System.out.println(attempts[i] + ": open");
    } else {
        System.out.println(attempts[i] + ": wrong");
    }
}
if (locker.isBlocked()) {
    System.out.println("Locker is blocked");
} else {
    System.out.println("Locker works");
}'''

LOCKER_BEHAVIOUR = '''{ Object o = null; Method t = null;
  try { Constructor<?> k = c.getDeclaredConstructor(String.class); k.setAccessible(true); o = k.newInstance("42");
        t = c.getDeclaredMethod("tryCode", String.class); t.setAccessible(true); } catch (Exception e) { }
  Object r1 = null, r2 = null;
  try { r1 = t.invoke(o, "42"); t.invoke(o, "1"); t.invoke(o, "2"); t.invoke(o, "3"); r2 = t.invoke(o, "42"); } catch (Exception e) { }
  need(Objects.equals(r1, true), "Метод tryCode должен возвращать true, если код совпал с кодом шкафчика");
  need(Objects.equals(r2, false), "После трёх ошибок tryCode должен возвращать false даже для верного кода — проверь это внутри метода"); }
'''

# ───────── Parking ─────────

PARKING = '''class Parking {
    private int places;
    private int cars;

    Parking(int places) {
        this.places = places;
    }

    boolean enter() {
        if (cars < places) {
            cars++;
            return true;
        }
        return false;
    }

    boolean leave() {
        if (cars > 0) {
            cars--;
            return true;
        }
        return false;
    }

    int getFree() {
        return places - cars;
    }
}'''

PARKING_MAIN = '''Parking parking = new Parking(places);
for (int i = 0; i < events.length; i++) {
    if (events[i].equals("in")) {
        if (parking.enter()) {
            System.out.println("in: ok");
        } else {
            System.out.println("in: full");
        }
    } else {
        if (parking.leave()) {
            System.out.println("out: ok");
        } else {
            System.out.println("out: empty");
        }
    }
}
System.out.println("Free places: " + parking.getFree());'''

PARKING_BEHAVIOUR = '''{ Object o = null; Method in = null, out = null;
  try { Constructor<?> k = c.getDeclaredConstructor(int.class); k.setAccessible(true); o = k.newInstance(1);
        in = c.getDeclaredMethod("enter"); in.setAccessible(true); out = c.getDeclaredMethod("leave"); out.setAccessible(true); } catch (Exception e) { }
  Field f = c.getDeclaredField("cars"); f.setAccessible(true);
  try { in.invoke(o); in.invoke(o); } catch (Exception e) { }
  need(o != null && Objects.equals(f.get(o), 1), "Проверка должна быть внутри enter: когда все места заняты, машина не заезжает");
  try { out.invoke(o); out.invoke(o); } catch (Exception e) { }
  need(Objects.equals(f.get(o), 0), "Проверка должна быть внутри leave: с пустой парковки машина уехать не может"); }
'''

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
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-enc-weather-sensor", title="Датчик температуры",
        given=[("int[]", "readings")],
        variants=[{"readings": "{12, 15, 99, 14}"}, {"readings": "{-5, -60, -8, 200}"}, {"readings": "{30, 25, -51}"}],
        hidden=[{"readings": "{}"}, {"readings": "{50}"}, {"readings": "{-50}"}, {"readings": "{51, -51, 7}"},
                {"readings": "{3, 4, 5, 6, 77}"}],
        intro="Уличный датчик раз в час передаёт температуру. Иногда он сбоит и присылает невозможные числа — ниже -50 "
              "или выше 50 градусов. Такие показания нужно пропускать, а хранить последнее нормальное. Показания по "
              "порядку записаны в массиве `readings`.",
        steps=["Ниже класса `Solution` создай класс `Sensor` (без `public`) с полем `private int temperature`. Из-за `private` "
               "код снаружи класса не может напрямую ни прочитать, ни изменить это поле.",
               "Добавь метод `void record(int value)`: он записывает `value` в поле, только если число от -50 до 50 "
               "включительно. Иначе температура не меняется.",
               "Добавь метод `int getTemperature()`, который возвращает температуру.",
               "В `main` создай датчик, по очереди передай методу `record` все показания из `readings` и выведи строку "
               "вида `Temperature: 14` — число получи через `getTemperature()`."],
        hint="Поле закрыто, поэтому из `main` нельзя написать `sensor.temperature = 99` — так ошибочное число не попадёт "
             "в датчик в обход проверки. Пока нормальных показаний не было, температура равна 0.",
        solution=SENSOR_MAIN,
        classes=SENSOR,
        wrong=[("record не проверяет число — сбойные показания тоже записываются",
                SENSOR_MAIN, SENSOR.replace("        if (value >= -50 && value <= 50) {\n            temperature = value;\n        }",
                                            "        temperature = value;")),
               ("границы строгие — ровно 50 и ровно -50 датчик не принимает",
                SENSOR_MAIN, SENSOR.replace("value >= -50 && value <= 50", "value > -50 && value < 50"))],
        constructs=["class"],
        checks=find_class("Sensor")
               + need_private_field("Sensor", "temperature", "int", "тогда температура меняется только через record с проверкой")
               + need_method("Sensor", "void", "record", ["int value"], "он сохраняет показание, если оно возможное")
               + need_method("Sensor", "int", "getTemperature", [], "через него код снаружи узнаёт температуру")
               + need_after_calls("", "", [("record", "int", "20"), ("record", "int", "90"), ("record", "int", "-70")],
                                  "temperature", "20", "Проверка должна быть внутри record: числа ниже -50 и выше 50 метод не записывает"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-enc-gym-locker", title="Кодовый шкафчик",
        given=[("String", "code"), ("String[]", "attempts")],
        variants=[{"code": '"2580"', "attempts": '{"1111", "2580", "0000"}'},
                  {"code": '"7314"', "attempts": '{"7341", "1234", "0000", "7314"}'},
                  {"code": '"4096"', "attempts": '{"4096", "4069"}'}],
        hidden=[{"code": '"1000"', "attempts": "{}"},
                {"code": '"5555"', "attempts": '{"1", "2", "5555"}'},
                {"code": '"8642"', "attempts": '{"0", "0", "0", "8642", "0"}'},
                {"code": '"3030"', "attempts": '{"3030", "1", "3030", "2", "3"}'}],
        intro="Шкафчик в спортзале открывается кодом `code`. После трёх неверных попыток он блокируется и больше не "
              "открывается даже верным кодом. Коды, которые вводили по очереди, записаны в массиве `attempts`.",
        steps=["Ниже класса `Solution` создай класс `Locker` (без `public`) с закрытыми полями `private String code` и "
               "`private int mistakes` и конструктором `Locker(String code)`, который запоминает код.",
               "Добавь метод `boolean tryCode(String attempt)`: если ошибок уже 3, сразу верни `false`. Иначе, если "
               "`attempt` совпадает с кодом, верни `true`; если не совпадает, увеличь `mistakes` на 1 и верни `false`.",
               "Добавь метод `boolean isBlocked()` — он возвращает `true`, когда ошибок 3.",
               "В `main` создай шкафчик и для каждого кода из `attempts` выведи строку вида `2580: open`, если `tryCode` "
               "вернул `true`, иначе — `1111: wrong`. В конце выведи `Locker is blocked` или `Locker works`."],
        hint="Строки сравнивай методом `equals`. Счётчик ошибок закрыт, поэтому код снаружи не может его обнулить — "
             "разблокировать шкафчик через `main` не получится.",
        solution=LOCKER_MAIN,
        classes=LOCKER,
        wrong=[("не проверяет блокировку — после трёх ошибок верный код всё равно открывает шкафчик",
                LOCKER_MAIN, LOCKER.replace("        if (mistakes >= 3) {\n            return false;\n        }\n", "")),
               ("блокирует шкафчик уже после двух ошибок",
                LOCKER_MAIN, LOCKER.replace("mistakes >= 3", "mistakes >= 2"))],
        constructs=["class"],
        checks=find_class("Locker")
               + need_private_field("Locker", "code", "String", "код нельзя подсмотреть или поменять снаружи класса")
               + need_private_field("Locker", "mistakes", "int", "тогда счётчик ошибок нельзя обнулить снаружи")
               + need_constructor("Locker", ["String code"], "он запоминает код шкафчика")
               + need_method("Locker", "boolean", "tryCode", ["String attempt"], "он проверяет введённый код")
               + need_method("Locker", "boolean", "isBlocked", [], "через него код снаружи узнаёт, заблокирован ли шкафчик")
               + LOCKER_BEHAVIOUR,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-enc-parking-places", title="Парковка у торгового центра",
        given=[("int", "places"), ("String[]", "events")],
        variants=[{"places": "2", "events": '{"in", "in", "in", "out", "in"}'},
                  {"places": "3", "events": '{"out", "in", "out", "out", "in"}'},
                  {"places": "1", "events": '{"in", "out", "out", "in", "in"}'}],
        hidden=[{"places": "5", "events": "{}"},
                {"places": "1", "events": '{"in", "in"}'},
                {"places": "4", "events": '{"in", "in", "in", "in", "in", "out"}'},
                {"places": "2", "events": '{"out", "out", "in"}'}],
        intro="Шлагбаум на парковке пускает машину, только если есть свободное место, и выпускает, только если на "
              "парковке кто-то стоит. Всего мест `places`, сначала парковка пустая. События по порядку записаны в массиве "
              "`events`: `in` — машина хочет заехать, `out` — выехать.",
        steps=["Ниже класса `Solution` создай класс `Parking` (без `public`) с закрытыми полями `private int places` и "
               "`private int cars` и конструктором `Parking(int places)`.",
               "Добавь метод `boolean enter()`: если машин меньше, чем мест, он добавляет машину и возвращает `true`, "
               "иначе возвращает `false`. И метод `boolean leave()`: если машины есть, он убирает одну и возвращает `true`, "
               "иначе `false`.",
               "Добавь метод `int getFree()` — он возвращает число свободных мест.",
               "В `main` создай парковку и пройди по `events`. Для `in` выведи `in: ok` или `in: full`, для `out` — "
               "`out: ok` или `out: empty`, смотря что вернул метод. В конце выведи строку вида `Free places: 1`."],
        hint="Поле `cars` закрыто, поэтому число машин меняется только в `enter` и `leave`. Если обе проверки стоят "
             "внутри этих методов, машин не станет ни больше, чем мест, ни меньше нуля.",
        solution=PARKING_MAIN,
        classes=PARKING,
        wrong=[("enter пускает машину и на занятое последнее место (`<=` вместо `<`)",
                PARKING_MAIN, PARKING.replace("cars < places", "cars <= places")),
               ("leave не проверяет, есть ли машины, — их число уходит в минус",
                PARKING_MAIN, PARKING.replace("        if (cars > 0) {\n            cars--;\n            return true;\n        }\n        return false;",
                                              "        cars--;\n        return true;"))],
        constructs=["class"],
        checks=find_class("Parking")
               + need_private_field("Parking", "places", "int", "число мест нельзя менять снаружи класса")
               + need_private_field("Parking", "cars", "int", "тогда машины заезжают и выезжают только через enter и leave")
               + need_constructor("Parking", ["int places"], "он запоминает, сколько на парковке мест")
               + need_method("Parking", "boolean", "enter", [], "он пускает машину, если есть место")
               + need_method("Parking", "boolean", "leave", [], "он выпускает машину, если она есть")
               + need_method("Parking", "int", "getFree", [], "через него код снаружи узнаёт число свободных мест")
               + PARKING_BEHAVIOUR,
    ),
]
