"""CONSTRUCTOR_BASIC — «Конструкторы» (Java). Taught before: everything up to static methods of Solution, classes with
fields and methods, creating objects with `new`. Here: a constructor fills the fields when the object is created;
it has the class's name and no return type; it may set fields that are not passed (a default) or computed ones;
a class may have two constructors with different parameters. Parameters are named differently from the fields —
`this` is the next topic. Not yet: this, private, static fields."""
from java_tasks import JavaOutputTask

SKILL = "CONSTRUCTOR_BASIC"


def find_class(name: str) -> str:
    return (f'Class<?> c = cls("{name}");\n'
            f'need(c != null, "Создай класс {name} ниже класса Solution (после его закрывающей скобки) и без слова public");\n')


def need_field(cls: str, name: str, java_type: str, why: str) -> str:
    """An instance (non-static) field of the class with this name and type."""
    return (f'{{ Field f = null; try {{ f = c.getDeclaredField("{name}"); }} catch (NoSuchFieldException e) {{ }}\n'
            f'  need(f != null && f.getType() == {java_type}.class, "Объяви в классе {cls} поле {java_type} {name} — {why}");\n'
            f'  need(!Modifier.isStatic(f.getModifiers()), "Объяви поле {name} в классе {cls} без слова static — тогда у каждого объекта будет своё значение"); }}\n')


def _types(params: list[str]) -> str:
    return ", ".join(f"{p.split()[0]}.class" for p in params)


def need_constructor(cls: str, params: list[str], why: str) -> str:
    return (f'{{ Constructor<?> k = null; try {{ k = c.getDeclaredConstructor({_types(params)}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(k != null, "Добавь в класс {cls} конструктор {cls}({", ".join(params)}) — {why}"); }}\n')


def need_built(params: list[str], args: str, expect: dict[str, str], message: str) -> str:
    """Creates an object with this constructor and compares its fields with the expected values (Java source)."""
    code = (f'{{ Constructor<?> k = c.getDeclaredConstructor({_types(params)}); k.setAccessible(true);\n'
            f'  Object o = null; try {{ o = k.newInstance({args}); }} catch (Exception e) {{ }}\n')
    conditions = []
    for i, (name, value) in enumerate(expect.items()):
        code += f'  Field f{i} = c.getDeclaredField("{name}"); f{i}.setAccessible(true);\n'
        conditions.append(f"Objects.equals(f{i}.get(o), {value})")
    return code + f'  need(o != null && {" && ".join(conditions)}, "{message}"); }}\n'


# ───────── Train car ─────────

WAGON = '''class Wagon {
    int number;
    int seats;
    int free;

    Wagon(int wagonNumber, int seatCount) {
        number = wagonNumber;
        seats = seatCount;
        free = seatCount;
    }
}'''

WAGON_MAIN = '''Wagon wagon = new Wagon(number, seats);
wagon.free -= sold;
System.out.println("Wagon " + wagon.number + ": " + wagon.seats + " seats");
System.out.println("Free: " + wagon.free);'''

WAGON_PARAMS = ["int wagonNumber", "int seatCount"]

# ───────── Phone calls ─────────

CALL = '''class Call {
    String contact;
    int seconds;
    int minutes;

    Call(String contactName, int duration) {
        contact = contactName;
        seconds = duration;
        minutes = (duration + 59) / 60;
    }
}'''

CALL_MAIN = '''int total = 0;
for (int i = 0; i < contacts.length; i++) {
    Call call = new Call(contacts[i], durations[i]);
    System.out.println(call.contact + ": " + call.seconds + " s, billed " + call.minutes + " min");
    total += call.minutes;
}
System.out.println("Total: " + total + " min");'''

CALL_PARAMS = ["String contactName", "int duration"]

# ───────── Deposits ─────────

DEPOSIT = '''class Deposit {
    String owner;
    int start;
    int result;

    Deposit(String ownerName, int sum, int years, int rate) {
        owner = ownerName;
        start = sum;
        result = sum;
        for (int y = 0; y < years; y++) {
            result += result * rate / 100;
        }
    }
}'''

DEPOSIT_MAIN = '''Deposit best = null;
for (int i = 0; i < owners.length; i++) {
    Deposit deposit = new Deposit(owners[i], sums[i], years, rate);
    System.out.println(deposit.owner + ": " + deposit.start + " -> " + deposit.result + " rub");
    if (best == null || deposit.result > best.result) {
        best = deposit;
    }
}
System.out.println("Best: " + best.owner);'''

DEPOSIT_PARAMS = ["String ownerName", "int sum", "int years", "int rate"]

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ctor-rt-train-wagon", title="Вагон поезда",
        given=[("int", "number"), ("int", "seats"), ("int", "sold")],
        variants=[{"number": "5", "seats": "36", "sold": "6"},
                  {"number": "12", "seats": "54", "sold": "40"},
                  {"number": "3", "seats": "18", "sold": "0"}],
        hidden=[{"number": "1", "seats": "36", "sold": "36"},
                {"number": "8", "seats": "64", "sold": "1"},
                {"number": "15", "seats": "40", "sold": "25"}],
        intro="К поезду прицепили вагон с номером `number`, в нём `seats` мест. Когда вагон только появился в расписании, "
              "все места в нём свободны — это удобно задать прямо в конструкторе. Потом касса продала `sold` билетов.",
        steps=["Ниже класса `Solution` создай класс `Wagon` (без `public`) с полями `int number`, `int seats` и `int free`.",
               "Добавь в класс конструктор `Wagon(int wagonNumber, int seatCount)`. Он сохраняет номер в поле `number`, "
               "число мест — в поле `seats`, и то же число мест записывает в поле `free`: у нового вагона свободны все места.",
               "В `main` создай вагон одной строкой: `Wagon wagon = new Wagon(number, seats);`. Затем уменьши `wagon.free` "
               "на `sold`.",
               "Выведи две строки вида `Wagon 5: 36 seats` и `Free: 30` — значения бери из полей объекта `wagon`."],
        hint="У конструктора нет типа результата, а имя совпадает с именем класса. Поле `free` конструктор заполняет сам, "
             "хотя отдельного параметра для него нет: в начале свободных мест столько же, сколько всего мест.",
        solution=WAGON_MAIN,
        classes=WAGON,
        wrong=[("в конструкторе забыл заполнить free — после продажи свободных мест получается отрицательное число",
                WAGON_MAIN, WAGON.replace("        free = seatCount;\n", "")),
               ("уменьшает число всех мест вместо свободных",
                WAGON_MAIN.replace("wagon.free -= sold;", "wagon.seats -= sold;"))],
        constructs=["class"],
        checks=find_class("Wagon")
               + need_field("Wagon", "number", "int", "номер вагона")
               + need_field("Wagon", "seats", "int", "сколько всего мест в вагоне")
               + need_field("Wagon", "free", "int", "сколько мест свободно")
               + need_constructor("Wagon", WAGON_PARAMS, "он заполняет поля, когда создаётся объект")
               + need_built(WAGON_PARAMS, "7, 30", {"number": "7", "seats": "30", "free": "30"},
                            "Конструктор Wagon должен сам заполнить поля number, seats и free — у нового вагона свободны все места"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ctor-rt-phone-calls", title="Счёт за звонки",
        given=[("String[]", "contacts"), ("int[]", "durations")],
        variants=[{"contacts": '{"Mom", "Boris", "Taxi"}', "durations": "{125, 60, 31}"},
                  {"contacts": '{"Anya", "Office"}', "durations": "{301, 59}"},
                  {"contacts": '{"Dad", "Doctor", "Gleb", "Shop"}', "durations": "{240, 61, 15, 119}"}],
        hidden=[{"contacts": '{"Bank"}', "durations": "{1}"},
                {"contacts": '{"Nina", "Oleg"}', "durations": "{120, 121}"},
                {"contacts": '{"Sasha", "Vera", "Lev"}', "durations": "{600, 45, 180}"},
                {"contacts": '{"Masha", "Kolya", "Ira", "Tom", "Ded"}', "durations": "{62, 58, 360, 1, 90}"}],
        intro="Оператор связи берёт плату за каждую начатую минуту: звонок длиной 61 секунда стоит как 2 минуты. "
              "С кем были звонки, записано в массиве `contacts`, а их длительность в секундах — в массиве `durations` "
              "под теми же номерами.",
        steps=["Ниже класса `Solution` создай класс `Call` (без `public`) с полями `String contact`, `int seconds` и `int minutes`.",
               "Добавь конструктор `Call(String contactName, int duration)`. Он сохраняет контакт и секунды, а в `minutes` "
               "записывает оплачиваемые минуты: `(duration + 59) / 60` — так деление округляет вверх.",
               "В `main` пройди циклом по звонкам, создай для каждого объект `new Call(contacts[i], durations[i])` и выведи "
               "строку вида `Mom: 125 s, billed 3 min` с полями этого объекта.",
               "Последней строкой выведи строку вида `Total: 5 min` — сумму полей `minutes` всех звонков."],
        hint="Обычное `duration / 60` отбрасывает остаток: 125 секунд дадут 2 минуты, а платить нужно за 3. Если сначала "
             "прибавить 59, любая начатая минута «дотянется» до следующей целой, а ровно 60 секунд так и останутся одной минутой.",
        solution=CALL_MAIN,
        classes=CALL,
        wrong=[("делит без округления вверх — неполная минута не оплачивается",
                CALL_MAIN, CALL.replace("(duration + 59) / 60", "duration / 60")),
               ("прибавляет к секундам 60 вместо 59 — ровно минута считается как две",
                CALL_MAIN, CALL.replace("(duration + 59) / 60", "(duration + 60) / 60"))],
        constructs=["class"],
        checks=find_class("Call")
               + need_field("Call", "contact", "String", "с кем был звонок")
               + need_field("Call", "seconds", "int", "длительность в секундах")
               + need_field("Call", "minutes", "int", "сколько минут оплатить")
               + need_constructor("Call", CALL_PARAMS, "он заполняет поля звонка, когда создаётся объект")
               + need_built(CALL_PARAMS, '"Test", 61', {"contact": '"Test"', "seconds": "61", "minutes": "2"},
                            "Конструктор Call должен сам заполнить поля contact, seconds и minutes — каждая начатая минута оплачивается целиком"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ctor-rt-bank-deposits", title="Вклады в банке",
        given=[("String[]", "owners"), ("int[]", "sums"), ("int", "years"), ("int", "rate")],
        variants=[{"owners": '{"Anya", "Boris", "Vika"}', "sums": "{1000, 5000, 2000}", "years": "3", "rate": "10"},
                  {"owners": '{"Gleb", "Dina"}', "sums": "{8000, 7000}", "years": "2", "rate": "20"},
                  {"owners": '{"Egor", "Zoya", "Ilya", "Kira"}', "sums": "{3000, 4500, 4000, 500}", "years": "4", "rate": "5"}],
        hidden=[{"owners": '{"Lena"}', "sums": "{1000}", "years": "0", "rate": "10"},
                {"owners": '{"Mark", "Nadya"}', "sums": "{600, 2000}", "years": "1", "rate": "50"},
                {"owners": '{"Oleg", "Pavel", "Rita"}', "sums": "{2000, 2000, 1000}", "years": "5", "rate": "10"},
                {"owners": '{"Sveta", "Timur", "Ulyana"}', "sums": "{100, 9000, 10000}", "years": "6", "rate": "8"}],
        intro="Несколько человек открыли в банке вклады на одинаковый срок `years` лет под `rate` процентов в год. Каждый год "
              "проценты начисляются на всю сумму, которая уже лежит на вкладе. Владельцы записаны в массиве `owners`, "
              "начальные суммы в рублях — в массиве `sums` под теми же номерами.",
        steps=["Ниже класса `Solution` создай класс `Deposit` (без `public`) с полями `String owner`, `int start` и `int result`.",
               "Добавь конструктор `Deposit(String ownerName, int sum, int years, int rate)`. Он сохраняет владельца и начальную "
               "сумму в `start`, а затем считает `result`: начинает с `sum` и `years` раз прибавляет к нему "
               "`result * rate / 100` (дробная часть каждый раз отбрасывается).",
               "В `main` пройди циклом по вкладчикам, создай для каждого вклад `new Deposit(owners[i], sums[i], years, rate)` "
               "и выведи строку вида `Anya: 1000 -> 1331 rub`.",
               "Последней строкой выведи строку вида `Best: Boris` — владельца вклада с самым большим `result`. Если таких "
               "несколько, назови того, кто в массиве раньше."],
        hint="Цикл можно писать прямо в конструкторе. Чтобы найти лучший вклад, храни ссылку на объект: начни с `Deposit best = null;` "
             "и заменяй её, когда `best == null` или у нового вклада `result` строго больше.",
        solution=DEPOSIT_MAIN,
        classes=DEPOSIT,
        wrong=[("начисляет проценты всегда на начальную сумму, а не на накопленную",
                DEPOSIT_MAIN, DEPOSIT.replace("result += result * rate / 100;", "result += sum * rate / 100;")),
               ("при равных вкладах называет последнего, а не первого",
                DEPOSIT_MAIN.replace("deposit.result > best.result", "deposit.result >= best.result"))],
        constructs=["class", "for"],
        checks=find_class("Deposit")
               + need_field("Deposit", "owner", "String", "владелец вклада")
               + need_field("Deposit", "start", "int", "начальная сумма")
               + need_field("Deposit", "result", "int", "сумма в конце срока")
               + need_constructor("Deposit", DEPOSIT_PARAMS, "он заполняет поля и считает итоговую сумму")
               + need_built(DEPOSIT_PARAMS, '"Test", 1000, 2, 10', {"owner": '"Test"', "start": "1000", "result": "1210"},
                            "Конструктор Deposit должен сам посчитать result: каждый год прибавлять result * rate / 100"),
    ),
]
