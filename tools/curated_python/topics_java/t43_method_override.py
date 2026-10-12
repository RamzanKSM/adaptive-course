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
System.out.println("Обычная подписка на " + months + " мес.: " + usual.price(months) + " руб.");
System.out.println("Студенческая подписка на " + months + " мес.: " + student.price(months) + " руб.");"""

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
System.out.println(worker.name + ": премия " + worker.bonus() + ", всего " + worker.total() + " руб.");
System.out.println(boss.name + ": премия " + boss.bonus() + ", всего " + boss.total() + " руб.");"""

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
    System.out.println("Лучник: " + archer.health + ", Рыцарь: " + knight.health);
}"""

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
               "Выведи две строки вида `Обычная подписка на 3 мес.: 897 руб.` и "
               "`Студенческая подписка на 3 мес.: 447 руб.` — цены возьми из методов `price` этих объектов."],
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
        variants=[{"workerName": '"Ольга"', "workerSalary": "40000", "managerName": '"Павел"', "managerSalary": "60000"},
                  {"workerName": '"Дима"', "workerSalary": "35000", "managerName": '"Ирина"', "managerSalary": "80000"},
                  {"workerName": '"Катя"', "workerSalary": "52000", "managerName": '"Сергей"', "managerSalary": "70000"}],
        hidden=[{"workerName": '"Нина"', "workerSalary": "10000", "managerName": '"Олег"', "managerSalary": "10000"},
                {"workerName": '"Тимур"', "workerSalary": "45500", "managerName": '"Алла"', "managerSalary": "99999"},
                {"workerName": '"Ян"', "workerSalary": "0", "managerName": '"Ева"', "managerSalary": "1000"}],
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
               "Для каждого выведи строку вида `Ольга: премия 4000, всего 44000 руб.`"],
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
               "строку вида `Лучник: 70, Рыцарь: 85`."],
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
]
