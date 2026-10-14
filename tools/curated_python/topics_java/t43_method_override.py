"""METHOD_OVERRIDE — «Переопределение методов» (Java). Taught before: everything up to classes, objects, constructors,
this, private fields, getters/setters, static, inheritance (extends). Here: a child declares a method with the same
name and parameters as the parent's, marked @Override; child objects use the new version, parent objects the old one;
a parent method that calls another method of the object gets the child's version. Not yet: polymorphism through a
parent-type array, interfaces, super (next topics) — so parents have no constructor with parameters and an overriding
method is written in full. The student writes the classes after Solution."""
from java_tasks import JavaOutputTask

SKILL = "METHOD_OVERRIDE"


def exist(*names: str) -> str:
    listed = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " и " + names[-1]
    what = "класс" if len(names) == 1 else "классы"
    condition = " && ".join(f'cls("{n}") != null' for n in names)
    return f'need({condition}, "Опиши {what} {listed} отдельно — ниже класса Solution, после его закрывающей скобки, и без слова public");\n'


def extends(child: str, parent: str) -> str:
    return (f'need(cls("{child}").getSuperclass() == cls("{parent}"), '
            f'"Сделай {child} наследником {parent}: напиши class {child} extends {parent}");\n')


def declares(cls_name: str, method: str, *params: str) -> str:
    """Java expression: the class itself declares the method with exactly these parameter types."""
    types = ", ".join(f"{p}.class" for p in params)
    return (f'Arrays.stream(cls("{cls_name}").getDeclaredMethods()).anyMatch(m -> m.getName().equals("{method}") '
            f'&& Arrays.equals(m.getParameterTypes(), new Class<?>[]{{{types}}}))')


def overridden(child: str, signature: str, method: str, *params: str) -> str:
    return (f'need({declares(child, method, *params)}, "Переопредели в {child} метод {signature} — с тем же именем и '
            f'параметрами, что у родителя, и с пометкой @Override над ним");\n')


SUBSCRIPTION = """\
class Subscription {
    int price(int months) {
        return 299 * months;
    }
}

class StudentSubscription extends Subscription {
    @Override
    int price(int months) {
        return 149 * months;
    }
}"""

SUBSCRIPTION_MAIN = """\
Subscription usual = new Subscription();
StudentSubscription student = new StudentSubscription();
System.out.println("Regular plan for " + months + " months: " + usual.price(months) + " rub");
System.out.println("Student plan for " + months + " months: " + student.price(months) + " rub");"""

BONUS = """\
class Employee {
    String name;
    int salary;

    int bonus() {
        return salary / 10;
    }

    int total() {
        return salary + bonus();
    }
}

class Manager extends Employee {
    @Override
    int bonus() {
        return salary / 4;
    }
}"""

BONUS_MAIN = """\
Employee worker = new Employee();
worker.name = workerName;
worker.salary = workerSalary;
Manager boss = new Manager();
boss.name = managerName;
boss.salary = managerSalary;
System.out.println(worker.name + ": bonus " + worker.bonus() + ", total " + worker.total() + " rub");
System.out.println(boss.name + ": bonus " + boss.bonus() + ", total " + boss.total() + " rub");"""

KNIGHT = """\
class Fighter {
    int health;

    void takeDamage(int amount) {
        health -= amount;
        if (health < 0) {
            health = 0;
        }
    }
}

class Knight extends Fighter {
    @Override
    void takeDamage(int amount) {
        health -= amount / 2;
        if (health < 0) {
            health = 0;
        }
    }
}"""

KNIGHT_MAIN = """\
Fighter archer = new Fighter();
archer.health = health;
Knight knight = new Knight();
knight.health = health;
for (int hit : hits) {
    archer.takeDamage(hit);
    knight.takeDamage(hit);
    System.out.println("Archer: " + archer.health + ", Knight: " + knight.health);
}"""

GREETERS = """\
class Greeter {
    String greet(String name) {
        return "Hello, " + name + "!";
    }
}

class PirateGreeter extends Greeter {
    @Override
    String greet(String name) {
        return "Ahoy, " + name + "!";
    }
}"""

GREETERS_MAIN = """\
Greeter usual = new Greeter();
PirateGreeter pirate = new PirateGreeter();
System.out.println("Bot: " + usual.greet(guest));
System.out.println("Pirate bot: " + pirate.greet(guest));"""

BELLS = """\
class Bell {
    String ring() {
        return "Ding";
    }

    String alarm(int times) {
        String result = ring();
        for (int i = 1; i < times; i++) {
            result += "-" + ring();
        }
        return result;
    }
}

class SchoolBell extends Bell {
    @Override
    String ring() {
        return "Brrr";
    }
}"""

BELLS_MAIN = """\
Bell door = new Bell();
SchoolBell school = new SchoolBell();
System.out.println("Door bell: " + door.alarm(doorTimes));
System.out.println("School bell: " + school.alarm(schoolTimes));"""

ACCOUNTS = """\
class Account {
    int balance;

    boolean withdraw(int amount) {
        if (amount > balance) {
            return false;
        }
        balance -= amount;
        return true;
    }
}

class CreditAccount extends Account {
    @Override
    boolean withdraw(int amount) {
        if (balance - amount < -1000) {
            return false;
        }
        balance -= amount;
        return true;
    }
}"""

ACCOUNTS_MAIN = """\
Account debit = new Account();
debit.balance = start;
CreditAccount credit = new CreditAccount();
credit.balance = start;
int debitDeclined = 0;
int creditDeclined = 0;
for (int amount : purchases) {
    if (!debit.withdraw(amount)) {
        debitDeclined++;
    }
    if (!credit.withdraw(amount)) {
        creditDeclined++;
    }
    System.out.println("Debit: " + debit.balance + ", Credit: " + credit.balance);
}
System.out.println("Declined: debit " + debitDeclined + ", credit " + creditDeclined);"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ovr-music-subscription", title="Студенческая подписка",
        given=[("int", "months")],
        variants=[{"months": "3"}, {"months": "12"}, {"months": "6"}],
        hidden=[{"months": "1"}, {"months": "24"}, {"months": "2"}],
        intro="Музыкальный сервис продаёт подписку по 299 руб. в месяц, а для студентов — по 149 руб. Студенческая "
              "подписка — это та же подписка, только цена считается по-другому. Покупатель хочет сравнить цены на "
              "`months` месяцев.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Subscription` без слова `public`, с методом `int price(int months)`, который возвращает "
               "цену подписки на `months` месяцев: 299 руб. за каждый месяц.",
               "Опиши класс `StudentSubscription` — наследник `Subscription` — и переопредели в нём метод "
               "`int price(int months)`: студенческая подписка стоит 149 руб. за месяц. Над методом напиши `@Override`.",
               "В `main` создай `Subscription usual = new Subscription();` и "
               "`StudentSubscription student = new StudentSubscription();`.",
               "Выведи две строки вида `Regular plan for 3 months: 897 rub` и "
               "`Student plan for 3 months: 447 rub` — цены возьми из методов `price` этих объектов."],
        hint="Переопределить метод — значит написать в наследнике метод с точно таким же именем и параметрами. "
             "Пометка `@Override` просит Java проверить это: если в имени опечатка, программа не скомпилируется, "
             "и ошибку будет сразу видно.",
        solution=SUBSCRIPTION_MAIN, classes=SUBSCRIPTION,
        wrong=[("в наследнике метод price без параметра — это новый метод, а не переопределение, и срабатывает цена родителя",
                SUBSCRIPTION_MAIN, SUBSCRIPTION.replace("    @Override\n    int price(int months) {\n        return 149 * months;",
                                                        "    int price() {\n        return 149;")),
               ("создаёт студенческую подписку из класса-родителя — новая цена не работает",
                SUBSCRIPTION_MAIN.replace("StudentSubscription student = new StudentSubscription();",
                                          "Subscription student = new Subscription();"))],
        constructs=["class"],
        checks=exist("Subscription", "StudentSubscription")
        + extends("StudentSubscription", "Subscription")
        + overridden("StudentSubscription", "int price(int months)", "price", "int"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ovr-manager-bonus", title="Премия менеджера",
        given=[("String", "workerName"), ("int", "workerSalary"), ("String", "managerName"), ("int", "managerSalary")],
        variants=[{"workerName": '"Olga"', "workerSalary": "40000", "managerName": '"Pavel"', "managerSalary": "60000"},
                  {"workerName": '"Dima"', "workerSalary": "35000", "managerName": '"Irina"', "managerSalary": "80000"},
                  {"workerName": '"Katya"', "workerSalary": "52000", "managerName": '"Sergey"', "managerSalary": "70000"}],
        hidden=[{"workerName": '"Nina"', "workerSalary": "10000", "managerName": '"Oleg"', "managerSalary": "10000"},
                {"workerName": '"Timur"', "workerSalary": "45500", "managerName": '"Alla"', "managerSalary": "99999"},
                {"workerName": '"Yan"', "workerSalary": "0", "managerName": '"Eva"', "managerSalary": "1000"}],
        intro="В конце года каждый сотрудник получает премию: обычный сотрудник — десятую часть зарплаты, а менеджер — "
              "четверть. Выплату считают одинаково для всех: зарплата плюс премия. Значит, в классе менеджера нужно "
              "поменять только расчёт премии.",
        steps=["Ниже класса `Solution` опиши класс `Employee` (без `public`) с полями `String name` и `int salary`.",
               "Добавь в `Employee` метод `int bonus()`, который возвращает премию — зарплату, делённую на 10, и метод "
               "`int total()`, который возвращает зарплату плюс премию. Премию в `total` получай вызовом `bonus()`.",
               "Опиши класс `Manager` — наследник `Employee` — и переопредели в нём только метод `int bonus()` "
               "(с `@Override`): премия менеджера — зарплата, делённая на 4. Метод `total` в `Manager` не пиши.",
               "В `main` создай `Employee worker = new Employee();` и `Manager boss = new Manager();` и заполни их поля "
               "`name` и `salary` значениями из `workerName`, `workerSalary`, `managerName` и `managerSalary`.",
               "Для каждого выведи строку вида `Olga: bonus 4000, total 44000 rub`"],
        hint="Метод `total` написан один раз в `Employee`, но вызывает `bonus()`. Когда `total` работает для менеджера, "
             "Java возьмёт версию `bonus` из `Manager`. Поэтому важно не считать премию в `total` вручную, а вызывать метод.",
        solution=BONUS_MAIN, classes=BONUS,
        wrong=[("в total премия посчитана вручную, а не через bonus() — итог менеджера считается по старой формуле",
                BONUS_MAIN, BONUS.replace("return salary + bonus();", "return salary + salary / 10;")),
               ("опечатка в имени метода менеджера и нет @Override — менеджер получает премию как обычный сотрудник",
                BONUS_MAIN, BONUS.replace("    @Override\n    int bonus() {\n        return salary / 4;",
                                          "    int bonuss() {\n        return salary / 4;"))],
        constructs=["class"],
        checks=exist("Employee", "Manager")
        + extends("Manager", "Employee")
        + overridden("Manager", "int bonus()", "bonus")
        + f'need(!{declares("Manager", "total")}, "Не пиши метод total в Manager: он есть в Employee и сам вызовет новую версию bonus()");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ovr-knight-armor", title="Броня рыцаря",
        given=[("int", "health"), ("int[]", "hits")],
        variants=[{"health": "100", "hits": "{30, 25, 60}"},
                  {"health": "60", "hits": "{50, 70, 40}"},
                  {"health": "120", "hits": "{40, 15, 90, 20}"}],
        hidden=[{"health": "50", "hits": "{60, 60, 20}"},
                {"health": "200", "hits": "{10}"},
                {"health": "30", "hits": "{7, 7, 7, 7}"},
                {"health": "80", "hits": "{81, 1, 200}"}],
        intro="В игре лучник и рыцарь вместе отбиваются от дракона. У обоих в начале `health` очков здоровья, и удары "
              "дракона из массива `hits` достаются обоим. Но рыцарь в броне: она забирает себе половину удара.",
        steps=["Ниже класса `Solution` опиши класс `Fighter` (без `public`) с полем `int health` и методом `void takeDamage(int amount)`: "
               "он уменьшает здоровье на `amount`, но так, чтобы оно не стало меньше 0 — если получилось отрицательное "
               "число, здоровье становится 0.",
               "Опиши класс `Knight` — наследник `Fighter` — и переопредели в нём `void takeDamage(int amount)` "
               "(с `@Override`): рыцарь теряет только `amount / 2` здоровья, и его здоровье тоже не бывает меньше 0.",
               "В `main` создай `Fighter archer = new Fighter();` и `Knight knight = new Knight();` и запиши каждому "
               "из них начальное здоровье: `archer.health = health;` и так же для рыцаря.",
               "Пройди циклом по массиву `hits`: каждый удар получают и лучник, и рыцарь. После каждого удара выведи "
               "строку вида `Archer: 70, Knight: 85`."],
        hint="Переопределённый метод полностью заменяет метод родителя, поэтому в версии `Knight` проверку «не меньше "
             "нуля» нужно написать заново — из `Fighter` она сама не перейдёт.",
        solution=KNIGHT_MAIN, classes=KNIGHT,
        wrong=[("в методе рыцаря забыта проверка — здоровье рыцаря уходит в минус",
                KNIGHT_MAIN, KNIGHT.replace("        health -= amount / 2;\n        if (health < 0) {\n            health = 0;\n        }\n",
                                            "        health -= amount / 2;\n")),
               ("опечатка в имени метода рыцаря и нет @Override — броня не работает, рыцарь получает полный урон",
                KNIGHT_MAIN, KNIGHT.replace("    @Override\n    void takeDamage(int amount) {\n        health -= amount / 2;",
                                            "    void takeDamag(int amount) {\n        health -= amount / 2;"))],
        constructs=["class", "for"],
        checks=exist("Fighter", "Knight")
        + extends("Knight", "Fighter")
        + overridden("Knight", "void takeDamage(int amount)", "takeDamage", "int"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ovr-pirate-greeter", title="Пиратский чат-бот",
        given=[("String", "guest")],
        variants=[{"guest": '"Anya"'}, {"guest": '"Boris"'}, {"guest": '"Captain Vera"'}],
        hidden=[{"guest": '"Timur"'}, {"guest": '"Jack"'}, {"guest": '"Zoya"'}],
        intro="В игре про море есть обычный чат-бот, который здоровается словом Hello, и пиратский бот — он здоровается "
              "по-пиратски, словом Ahoy. Пиратский бот — это тот же бот, только приветствие у него другое. Имя гостя "
              "записано в поле `guest`.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Greeter` без слова `public`, с методом "
               "`String greet(String name)`, который возвращает строку вида `Hello, Anya!`.",
               "Опиши класс `PirateGreeter` — наследник `Greeter` — и переопредели в нём метод `String greet(String name)` "
               "(с `@Override` над ним): он возвращает строку вида `Ahoy, Anya!`.",
               "В `main` создай `Greeter usual = new Greeter();` и `PirateGreeter pirate = new PirateGreeter();`.",
               "Выведи две строки вида `Bot: Hello, Anya!` и `Pirate bot: Ahoy, Anya!` — приветствия возьми из методов "
               "`greet` этих объектов, передав им `guest`."],
        hint="У переопределённого метода те же имя, параметры и тип результата, что у метода родителя, — меняется только "
             "то, что внутри. `@Override` попросит Java проверить, что ты не ошибся в имени или параметрах.",
        solution=GREETERS_MAIN, classes=GREETERS,
        wrong=[("в наследнике метод greet без параметра — это новый метод, а не переопределение, и срабатывает приветствие родителя",
                GREETERS_MAIN, GREETERS.replace('    @Override\n    String greet(String name) {\n        return "Ahoy, " + name + "!";',
                                                '    String greet() {\n        return "Ahoy!";')),
               ("создаёт пиратского бота из класса-родителя — новое приветствие не работает",
                GREETERS_MAIN.replace("PirateGreeter pirate = new PirateGreeter();", "Greeter pirate = new Greeter();"))],
        constructs=["class"],
        checks=exist("Greeter", "PirateGreeter")
        + extends("PirateGreeter", "Greeter")
        + overridden("PirateGreeter", "String greet(String name)", "greet", "String"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ovr-school-bell", title="Дверной и школьный звонки",
        given=[("int", "doorTimes"), ("int", "schoolTimes")],
        variants=[{"doorTimes": "3", "schoolTimes": "2"}, {"doorTimes": "1", "schoolTimes": "4"},
                  {"doorTimes": "2", "schoolTimes": "3"}],
        hidden=[{"doorTimes": "1", "schoolTimes": "1"}, {"doorTimes": "5", "schoolTimes": "2"},
                {"doorTimes": "4", "schoolTimes": "6"}],
        intro="Дверной звонок звенит Ding, а школьный — Brrr. Когда звонок срабатывает несколько раз подряд, звуки "
              "пишутся через дефис: `Ding-Ding-Ding`. Это правило одно для всех звонков, отличается только сам звук. "
              "Дверной звонок нажали `doorTimes` раз, школьный прозвенел `schoolTimes` раз.",
        steps=["Ниже класса `Solution` опиши класс `Bell` (без `public`) с методом `String ring()`, который возвращает `Ding`.",
               "Добавь в `Bell` метод `String alarm(int times)`: он возвращает звук, повторённый `times` раз через дефис "
               "(`times` всегда не меньше 1). Звук в нём получай вызовом `ring()`.",
               "Опиши класс `SchoolBell` — наследник `Bell` — и переопредели в нём только метод `String ring()` "
               "(с `@Override`): он возвращает `Brrr`. Метод `alarm` в `SchoolBell` не пиши.",
               "В `main` создай `Bell door = new Bell();` и `SchoolBell school = new SchoolBell();` и выведи две строки "
               "вида `Door bell: Ding-Ding-Ding` и `School bell: Brrr-Brrr` — с результатами `alarm(doorTimes)` "
               "и `alarm(schoolTimes)`."],
        hint="Метод `alarm` написан один раз в `Bell`, но вызывает `ring()`. Для объекта `SchoolBell` Java возьмёт "
             "версию `ring` из наследника, поэтому `alarm` сам начнёт звенеть Brrr. Начни строку с одного звука, "
             "а в цикле добавляй дефис и ещё один звук.",
        solution=BELLS_MAIN, classes=BELLS,
        wrong=[("в alarm звук записан прямо строкой, а не через ring() — школьный звонок тоже звенит Ding",
                BELLS_MAIN, BELLS.replace('        String result = ring();\n        for (int i = 1; i < times; i++) {\n            result += "-" + ring();',
                                          '        String result = "Ding";\n        for (int i = 1; i < times; i++) {\n            result += "-Ding";')),
               ("опечатка в имени метода школьного звонка и нет @Override — он звенит как дверной",
                BELLS_MAIN, BELLS.replace('    @Override\n    String ring() {\n        return "Brrr";',
                                          '    String rings() {\n        return "Brrr";'))],
        constructs=["class"],
        checks=exist("Bell", "SchoolBell")
        + extends("SchoolBell", "Bell")
        + overridden("SchoolBell", "String ring()", "ring")
        + f'need(!{declares("SchoolBell", "alarm", "int")}, "Не пиши метод alarm в SchoolBell: он есть в Bell и сам вызовет новую версию ring()");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ovr-credit-card", title="Дебетовая и кредитная карты",
        given=[("int", "start"), ("int[]", "purchases")],
        variants=[{"start": "500", "purchases": "{300, 400, 700}"},
                  {"start": "1000", "purchases": "{1200, 500, 300}"},
                  {"start": "200", "purchases": "{100, 100, 900, 300}"}],
        hidden=[{"start": "0", "purchases": "{1000, 1}"},
                {"start": "800", "purchases": "{800}"},
                {"start": "100", "purchases": "{2000, 600, 500}"},
                {"start": "300", "purchases": "{}"}],
        intro="У Ани две карты, и на каждой лежит `start` руб. С дебетовой карты нельзя потратить больше, чем на ней есть. "
              "Кредитная карта разрешает уйти в минус, но не ниже -1000 руб. Аня по очереди пробует оплатить обе картами "
              "одни и те же покупки из массива `purchases`.",
        steps=["Ниже класса `Solution` опиши класс `Account` (без `public`) с полем `int balance` и методом "
               "`boolean withdraw(int amount)`: если `amount` больше баланса, метод ничего не меняет и возвращает `false`, "
               "иначе уменьшает баланс и возвращает `true`.",
               "Опиши класс `CreditAccount` — наследник `Account` — и переопредели в нём `boolean withdraw(int amount)` "
               "(с `@Override`): покупка отклоняется, только если после неё баланс стал бы меньше -1000.",
               "В `main` создай `Account debit` и `CreditAccount credit` и запиши каждому баланс `start`. Для каждой "
               "покупки вызови `withdraw` у обеих карт и выведи строку вида `Debit: 200, Credit: 200`.",
               "Считай, сколько покупок отклонила каждая карта, и в конце выведи строку вида `Declined: debit 2, credit 0`."],
        hint="Переопределённый метод полностью заменяет метод родителя, поэтому в `CreditAccount` проверку и списание "
             "нужно написать целиком. Ровно -1000 руб. на кредитной карте — ещё можно.",
        solution=ACCOUNTS_MAIN, classes=ACCOUNTS,
        wrong=[("кредитная карта не проверяет лимит — уходит в минус без ограничений",
                ACCOUNTS_MAIN, ACCOUNTS.replace("        if (balance - amount < -1000) {\n            return false;\n        }\n", "")),
               ("опечатка в имени метода кредитной карты и нет @Override — она работает как дебетовая",
                ACCOUNTS_MAIN, ACCOUNTS.replace("    @Override\n    boolean withdraw(int amount) {\n        if (balance - amount < -1000)",
                                                "    boolean withdrow(int amount) {\n        if (balance - amount < -1000)"))],
        constructs=["class", "for"],
        checks=exist("Account", "CreditAccount")
        + extends("CreditAccount", "Account")
        + overridden("CreditAccount", "boolean withdraw(int amount)", "withdraw", "int"),
    ),
]
