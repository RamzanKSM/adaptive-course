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



GRADERS = """\
class Grader {
    String result(int score) {
        if (score >= 50) {
            return "pass";
        }
        return "fail";
    }
}

class StrictGrader extends Grader {
    @Override
    String result(int score) {
        if (score >= 75) {
            return "pass";
        }
        return "fail";
    }
}"""

GRADERS_MAIN = """\
Grader kind = new Grader();
StrictGrader strict = new StrictGrader();
System.out.println("Score: " + score);
System.out.println("Kind teacher: " + kind.result(score));
System.out.println("Strict teacher: " + strict.result(score));"""

COFFEE = """\
class Coffee {
    String name() {
        return "Espresso";
    }

    int price() {
        return 150;
    }

    int cost(int cups) {
        return cups * price();
    }

    String receipt(int cups) {
        return name() + ": " + cups + " x " + price() + " = " + cost(cups) + " rub";
    }
}

class Latte extends Coffee {
    @Override
    String name() {
        return "Latte";
    }

    @Override
    int price() {
        return 220;
    }
}"""

COFFEE_MAIN = """\
Coffee espresso = new Coffee();
Latte latte = new Latte();
System.out.println(espresso.receipt(espressoCups));
System.out.println(latte.receipt(latteCups));
System.out.println("Total: " + (espresso.cost(espressoCups) + latte.cost(latteCups)) + " rub");"""

LOYALTY = """\
class Customer {
    int points;

    void buy(int amount) {
        points += amount / 100;
    }
}

class VipCustomer extends Customer {
    @Override
    void buy(int amount) {
        points += amount / 100 * 2;
        if (amount >= 5000) {
            points += 50;
        }
    }
}"""

LOYALTY_MAIN = """\
Customer usual = new Customer();
VipCustomer vip = new VipCustomer();
for (int amount : purchases) {
    usual.buy(amount);
    vip.buy(amount);
    System.out.println(amount + " rub -> Regular: " + usual.points + ", VIP: " + vip.points);
}
System.out.println("VIP is ahead by " + (vip.points - usual.points) + " points");"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-ovr-rt-strict-teacher", title="Строгий учитель",
        given=[("int", "score")],
        variants=[{"score": "62"}, {"score": "80"}, {"score": "45"}],
        hidden=[{"score": "50"}, {"score": "49"}, {"score": "75"}, {"score": "74"}, {"score": "100"}],
        intro="Контрольную проверяют два учителя. Обычный ставит зачёт, если набрано не меньше 50 баллов, а строгий — "
              "не меньше 75. Строгий учитель проверяет так же, только порог у него другой. Баллы ученика записаны "
              "в поле `score`.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Grader` без слова `public`, с методом "
               "`String result(int score)`: он возвращает `pass`, если `score` не меньше 50, иначе `fail`.",
               "Опиши класс `StrictGrader` — наследник `Grader` — и переопредели в нём метод `String result(int score)` "
               "(с `@Override` над ним): он возвращает `pass`, если `score` не меньше 75, иначе `fail`.",
               "В `main` создай `Grader kind = new Grader();` и `StrictGrader strict = new StrictGrader();`.",
               "Выведи три строки вида `Score: 62`, `Kind teacher: pass` и `Strict teacher: fail` — оценки возьми из "
               "методов `result` этих объектов."],
        hint="Переопределить метод — значит написать в наследнике метод с тем же именем, параметрами и типом результата, "
             "но со своим телом. `@Override` просит Java проверить, что имя и параметры совпали с родительскими.",
        solution=GRADERS_MAIN, classes=GRADERS,
        wrong=[("в наследнике метод result без параметра — это новый метод, а не переопределение, и срабатывает порог родителя",
                GRADERS_MAIN, GRADERS.replace("    @Override\n    String result(int score) {\n        if (score >= 75) {",
                                              "    String result() {\n        int score = 0;\n        if (score >= 75) {")),
               ("строгое сравнение в методе строгого учителя: ровно 75 баллов не дают зачёта",
                GRADERS_MAIN, GRADERS.replace("score >= 75", "score > 75"))],
        constructs=["class"],
        checks=exist("Grader", "StrictGrader")
        + extends("StrictGrader", "Grader")
        + overridden("StrictGrader", "String result(int score)", "result", "int"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-ovr-rt-coffee-receipt", title="Чек в кофейне",
        given=[("int", "espressoCups"), ("int", "latteCups")],
        variants=[{"espressoCups": "2", "latteCups": "3"}, {"espressoCups": "1", "latteCups": "1"},
                  {"espressoCups": "4", "latteCups": "2"}],
        hidden=[{"espressoCups": "0", "latteCups": "5"}, {"espressoCups": "3", "latteCups": "0"},
                {"espressoCups": "10", "latteCups": "7"}],
        intro="Кофейня печатает чек отдельной строкой для каждого напитка: название, сколько чашек, цена одной чашки и "
              "сумма. Эспрессо стоит 150 руб., латте — 220 руб. Правило чека одно для всех напитков, отличаются только "
              "название и цена. Гость взял `espressoCups` чашек эспрессо и `latteCups` чашек латте.",
        steps=["Ниже класса `Solution` опиши класс `Coffee` (без `public`) с методами `String name()` (возвращает `Espresso`) "
               "и `int price()` (возвращает 150).",
               "Добавь в `Coffee` метод `int cost(int cups)` — `cups`, умноженное на `price()`, и метод "
               "`String receipt(int cups)`, который возвращает строку вида `Espresso: 2 x 150 = 300 rub`. Название, цену "
               "и сумму в нём получай вызовами `name()`, `price()` и `cost(cups)`.",
               "Опиши класс `Latte` — наследник `Coffee` — и переопредели в нём только `String name()` (возвращает `Latte`) "
               "и `int price()` (возвращает 220), оба с `@Override`. Методы `cost` и `receipt` в `Latte` не пиши.",
               "В `main` создай `Coffee espresso = new Coffee();` и `Latte latte = new Latte();`, выведи `receipt` для "
               "`espressoCups` и для `latteCups` и последней строкой — строку вида `Total: 960 rub` с суммой обоих `cost`."],
        hint="Методы `cost` и `receipt` написаны один раз в `Coffee`, но вызывают `name()` и `price()`. Для объекта `Latte` "
             "Java возьмёт их версии из наследника, поэтому чек латте сам получится правильным.",
        solution=COFFEE_MAIN, classes=COFFEE,
        wrong=[("в cost цена записана числом, а не через price() — латте считается по цене эспрессо",
                COFFEE_MAIN, COFFEE.replace("return cups * price();", "return cups * 150;")),
               ("опечатка в имени метода цены у латте и нет @Override — латте стоит как эспрессо",
                COFFEE_MAIN, COFFEE.replace("    @Override\n    int price() {\n        return 220;",
                                            "    int prise() {\n        return 220;"))],
        constructs=["class"],
        checks=exist("Coffee", "Latte")
        + extends("Latte", "Coffee")
        + overridden("Latte", "String name()", "name")
        + overridden("Latte", "int price()", "price")
        + f'need(!{declares("Latte", "cost", "int")} && !{declares("Latte", "receipt", "int")}, '
          '"Не пиши методы cost и receipt в Latte: они есть в Coffee и сами вызовут новые версии name() и price()");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-ovr-rt-vip-points", title="Баллы VIP-покупателя",
        given=[("int[]", "purchases")],
        variants=[{"purchases": "{450, 1200, 5000}"},
                  {"purchases": "{150, 99, 7300}"},
                  {"purchases": "{2500, 4999, 300, 6000}"}],
        hidden=[{"purchases": "{5000}"},
                {"purchases": "{4999}"},
                {"purchases": "{}"},
                {"purchases": "{50, 150, 250, 10000, 199}"}],
        intro="В магазине работает программа лояльности. Обычный покупатель получает 1 балл за каждые полные 100 руб. "
              "покупки. VIP-покупатель получает 2 балла за каждые полные 100 руб., а за покупку от 5000 руб. — ещё 50 "
              "бонусных баллов. Два покупателя, обычный и VIP, сделали одинаковые покупки из массива `purchases`.",
        steps=["Ниже класса `Solution` опиши класс `Customer` (без `public`) с полем `int points` и методом "
               "`void buy(int amount)`: он прибавляет к баллам `amount / 100`.",
               "Опиши класс `VipCustomer` — наследник `Customer` — и переопредели в нём `void buy(int amount)` "
               "(с `@Override`): он прибавляет `amount / 100 * 2`, а если `amount` не меньше 5000 — ещё 50.",
               "В `main` создай `Customer usual` и `VipCustomer vip`. Для каждой покупки вызови `buy` у обоих и выведи "
               "строку вида `450 rub -> Regular: 4, VIP: 8`.",
               "В конце выведи строку вида `VIP is ahead by 116 points` — на сколько баллов VIP-покупатель обогнал обычного."],
        hint="Переопределённый метод полностью заменяет метод родителя, поэтому в `VipCustomer` нужно написать подсчёт "
             "целиком. «Полные 100 рублей» — это целочисленное деление: `150 / 100` даёт 1, и VIP получает за них 2 балла, а не 3.",
        solution=LOYALTY_MAIN, classes=LOYALTY,
        wrong=[("сначала умножает на 2, потом делит — за неполную сотню VIP получает лишний балл",
                LOYALTY_MAIN, LOYALTY.replace("points += amount / 100 * 2;", "points += amount * 2 / 100;")),
               ("опечатка в имени метода VIP-покупателя и нет @Override — он получает баллы как обычный",
                LOYALTY_MAIN, LOYALTY.replace("    @Override\n    void buy(int amount) {\n        points += amount / 100 * 2;",
                                              "    void bye(int amount) {\n        points += amount / 100 * 2;"))],
        constructs=["class", "for"],
        checks=exist("Customer", "VipCustomer")
        + extends("VipCustomer", "Customer")
        + overridden("VipCustomer", "void buy(int amount)", "buy", "int"),
    ),
]
