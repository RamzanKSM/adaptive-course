"""INHERITANCE_BASIC — «Наследование» (Java). Taught before: println, variables, arithmetic, strings, if/else, loops,
arrays, static methods, classes, objects, constructors, this, private fields, getters/setters, static. Here:
`class Child extends Parent`; the child gets the parent's fields and methods without writing them again and adds its own
methods, which use the inherited fields and call inherited methods. Not yet: overriding, polymorphism, interfaces, super
(next topics) — so the parents here have no constructor with parameters (a child would need super(...) for it) and
objects get their data through fields or inherited methods. The student writes the classes after Solution."""
from java_tasks import JavaOutputTask

SKILL = "INHERITANCE_BASIC"


def exist(*names: str) -> str:
    listed = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " и " + names[-1]
    what = "класс" if len(names) == 1 else "классы"
    condition = " && ".join(f'cls("{n}") != null' for n in names)
    return f'need({condition}, "Опиши {what} {listed} отдельно — ниже класса Solution, после его закрывающей скобки, и без слова public");\n'


def extends(child: str, parent: str, why: str) -> str:
    return (f'need(cls("{child}").getSuperclass() == cls("{parent}"), '
            f'"Сделай {child} наследником {parent}: напиши class {child} extends {parent} — {why}");\n')


def declares(cls_name: str, method: str) -> str:
    """Java expression: the class itself (not its parent) declares a method with this name."""
    return f'Arrays.stream(cls("{cls_name}").getDeclaredMethods()).anyMatch(m -> m.getName().equals("{method}"))'


PETS = """\
class Pet {
    String name;
    int weight;

    int dailyFood() {
        return weight * 30;
    }
}

class Cat extends Pet {
}

class Dog extends Pet {
    int walkMinutes() {
        return weight * 5;
    }
}"""

PETS_MAIN = """\
Cat cat = new Cat();
cat.name = catName;
cat.weight = catWeight;
Dog dog = new Dog();
dog.name = dogName;
dog.weight = dogWeight;
System.out.println(cat.name + ": " + cat.dailyFood() + " g of food a day");
System.out.println(dog.name + ": " + dog.dailyFood() + " g of food a day");
System.out.println(dog.name + " walks " + dog.walkMinutes() + " minutes");"""

ACCOUNT = """\
class Account {
    private int balance;

    void deposit(int amount) {
        balance += amount;
    }

    int getBalance() {
        return balance;
    }
}

class SavingsAccount extends Account {
    void addInterest(int percent) {
        deposit(getBalance() * percent / 100);
    }
}"""

ACCOUNT_MAIN = """\
SavingsAccount account = new SavingsAccount();
account.deposit(start);
System.out.println("Account opened: " + account.getBalance() + " rub");
account.addInterest(percent);
System.out.println("After interest: " + account.getBalance() + " rub");
account.deposit(extra);
System.out.println("After deposit: " + account.getBalance() + " rub");
account.addInterest(percent);
System.out.println("After interest: " + account.getBalance() + " rub");"""

# A beginner's way round inheritance: a separate class with a copy of everything — the output is the same.
ACCOUNT_COPIED = ACCOUNT.replace("""class SavingsAccount extends Account {
""", """class SavingsAccount {
    private int balance;

    void deposit(int amount) {
        balance += amount;
    }

    int getBalance() {
        return balance;
    }

""")

PARCELS = """\
class Parcel {
    int weight;

    int price() {
        return 100 + 20 * weight;
    }
}

class FragileParcel extends Parcel {
    int safePrice() {
        return price() + 150;
    }
}"""

PARCELS_MAIN = """\
int total = 0;
for (int w : regular) {
    Parcel parcel = new Parcel();
    parcel.weight = w;
    System.out.println("Regular parcel " + parcel.weight + " kg: " + parcel.price() + " rub");
    total += parcel.price();
}
for (int w : fragile) {
    FragileParcel parcel = new FragileParcel();
    parcel.weight = w;
    System.out.println("Fragile parcel " + parcel.weight + " kg: " + parcel.safePrice() + " rub");
    total += parcel.safePrice();
}
System.out.println("Total: " + total + " rub");"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-inh-pet-food", title="Корм для питомцев",
        given=[("String", "catName"), ("int", "catWeight"), ("String", "dogName"), ("int", "dogWeight")],
        variants=[{"catName": '"Murka"', "catWeight": "4", "dogName": '"Rex"', "dogWeight": "12"},
                  {"catName": '"Barsik"', "catWeight": "6", "dogName": '"Sharik"', "dogWeight": "20"},
                  {"catName": '"Snowball"', "catWeight": "3", "dogName": '"Bim"', "dogWeight": "8"}],
        hidden=[{"catName": '"Fluffy"', "catWeight": "5", "dogName": '"Tuzik"', "dogWeight": "5"},
                {"catName": '"Luna"', "catWeight": "2", "dogName": '"Jack"', "dogWeight": "31"},
                {"catName": '"Sonya"', "catWeight": "7", "dogName": '"Graf"', "dogWeight": "15"}],
        intro="Ветеринар составляет памятку для хозяев кошки и собаки. И кошка, и собака — питомцы: у каждого есть "
              "имя и вес, и корм обоим считают одинаково. А вот гулять нужно только с собакой.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Pet` без слова `public`, с полями `String name` и "
               "`int weight` — вес в килограммах. Добавь в него метод `int dailyFood()`, который возвращает, сколько "
               "граммов корма нужно питомцу в день: по 30 граммов на каждый килограмм веса.",
               "Опиши класс `Cat`, который наследует `Pet`: `class Cat extends Pet {{ }}`. Внутри ничего не пиши — "
               "всё нужное кошка получит от родителя.",
               "Опиши класс `Dog` — тоже наследник `Pet` — и добавь в него только один новый метод `int walkMinutes()`: "
               "сколько минут гулять с собакой — по 5 минут на каждый килограмм веса.",
               "В `main` создай `Cat cat = new Cat();` и `Dog dog = new Dog();` и заполни их поля `name` и `weight` "
               "значениями из `catName`, `catWeight`, `dogName` и `dogWeight`.",
               "Выведи три строки: корм кошки, корм собаки и прогулку собаки — в виде `Murka: 120 g of food a day`, "
               "`Rex: 360 g of food a day` и `Rex walks 60 minutes`."],
        hint="Запись `class Cat extends Pet` значит «кошка — это питомец»: объект `Cat` сразу получает поля `name`, "
             "`weight` и метод `dailyFood()` из `Pet`, хотя в самом `Cat` их нет. В наследнике пишут только то, "
             "чего нет у родителя.",
        solution=PETS_MAIN, classes=PETS,
        wrong=[("создаёт собаку с весом кошки — скопировал строку и не поправил",
                PETS_MAIN.replace("dog.weight = dogWeight;", "dog.weight = catWeight;")),
               ("скопировал метод dailyFood в Dog вместо того, чтобы получить его по наследству",
                PETS_MAIN, PETS.replace("class Dog extends Pet {\n",
                                        "class Dog extends Pet {\n    int dailyFood() {\n        return weight * 30;\n    }\n\n"))],
        constructs=["class"],
        checks=exist("Pet", "Cat", "Dog")
        + extends("Cat", "Pet", "тогда кошка получит поля и методы питомца без копирования")
        + extends("Dog", "Pet", "тогда собака получит поля и методы питомца без копирования")
        + f'need({declares("Pet", "dailyFood")}, "Напиши метод dailyFood в классе Pet: корм считают одинаково для всех питомцев");\n'
        + f'need(!{declares("Cat", "dailyFood")} && !{declares("Dog", "dailyFood")}, '
          '"Напиши метод dailyFood один раз — только в Pet: Cat и Dog получат его по наследству, копировать не нужно");\n'
        + f'need({declares("Dog", "walkMinutes")} && !{declares("Pet", "walkMinutes")}, '
          '"Метод walkMinutes добавь только в класс Dog: гулять нужно с собакой, а не с каждым питомцем");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-inh-savings-account", title="Накопительный счёт",
        given=[("int", "start"), ("int", "percent"), ("int", "extra")],
        variants=[{"start": "1000", "percent": "5", "extra": "500"},
                  {"start": "2000", "percent": "10", "extra": "300"},
                  {"start": "800", "percent": "3", "extra": "1200"}],
        hidden=[{"start": "100", "percent": "50", "extra": "0"},
                {"start": "5000", "percent": "1", "extra": "250"},
                {"start": "0", "percent": "7", "extra": "1000"},
                {"start": "999", "percent": "10", "extra": "1"}],
        intro="Банк открыл клиенту накопительный счёт. Это обычный счёт, на который можно класть деньги, но банк ещё и "
              "начисляет на него проценты. Всё, что умеет обычный счёт, накопительный получает по наследству — дописать "
              "нужно только новое умение. Сколько положили при открытии, записано в `start`, процент — в `percent`, "
              "пополнение — в `extra`.",
        steps=["Ниже класса `Solution` опиши класс `Account` (без `public`) — обычный счёт. Сделай в нём закрытое поле "
               "`private int balance` (в начале оно равно 0) и два метода: `void deposit(int amount)` прибавляет "
               "`amount` к балансу, а `int getBalance()` возвращает баланс.",
               "Опиши класс `SavingsAccount` — наследник `Account` — и добавь в него только один новый метод "
               "`void addInterest(int percent)`. Он считает проценты — баланс, умноженный на `percent` и потом делённый "
               "на 100, — и зачисляет их на счёт. Баланс узнай через унаследованный `getBalance()`, а деньги положи "
               "через унаследованный `deposit(...)`.",
               "В `main` создай `SavingsAccount account = new SavingsAccount();`, положи на него `start` рублей и выведи "
               "строку вида `Account opened: 1000 rub` — с текущим балансом.",
               "Затем по очереди: начисли проценты `percent` и выведи `After interest: … rub`; положи на счёт `extra` "
               "рублей и выведи `After deposit: … rub`; ещё раз начисли проценты и выведи `After interest: … rub` "
               "Вместо `…` — текущий баланс."],
        hint="Поле `balance` закрыто (`private`), поэтому даже наследник не может обратиться к нему напрямую. А методы "
             "`deposit` и `getBalance` не закрыты, и наследник получил их от родителя — внутри `addInterest` вызывай их "
             "так же, как свои собственные.",
        solution=ACCOUNT_MAIN, classes=ACCOUNT,
        wrong=[("делит баланс на 100 раньше, чем умножает на процент, — дробная часть теряется",
                ACCOUNT_MAIN, ACCOUNT.replace("getBalance() * percent / 100", "getBalance() / 100 * percent")),
               ("сделал SavingsAccount отдельным классом и скопировал в него поле и методы Account",
                ACCOUNT_MAIN, ACCOUNT_COPIED)],
        constructs=["class"],
        checks=exist("Account", "SavingsAccount")
        + extends("SavingsAccount", "Account", "тогда накопительный счёт получит deposit и getBalance без копирования")
        + f'need({declares("SavingsAccount", "addInterest")}, "Добавь метод addInterest в класс SavingsAccount: начислять проценты умеет только накопительный счёт");\n'
        + f'need(!{declares("SavingsAccount", "deposit")} && !{declares("SavingsAccount", "getBalance")}, '
          '"Методы deposit и getBalance напиши только в Account: SavingsAccount получит их по наследству");\n'
        + 'boolean balancePrivate;\n'
          'try { balancePrivate = Modifier.isPrivate(cls("Account").getDeclaredField("balance").getModifiers()); }\n'
          'catch (NoSuchFieldException e) { balancePrivate = false; }\n'
          'need(balancePrivate, "Объяви в Account закрытое поле private int balance: наследник работает с ним через deposit и getBalance");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-inh-fragile-parcel", title="Хрупкие посылки",
        given=[("int[]", "regular"), ("int[]", "fragile")],
        variants=[{"regular": "{2, 5}", "fragile": "{3}"},
                  {"regular": "{1}", "fragile": "{4, 2}"},
                  {"regular": "{10, 3, 6}", "fragile": "{1}"}],
        hidden=[{"regular": "{}", "fragile": "{5}"},
                {"regular": "{7, 7}", "fragile": "{}"},
                {"regular": "{1, 2}", "fragile": "{3, 4}"},
                {"regular": "{3}", "fragile": "{2, 2, 2}"}],
        intro="Служба доставки везёт обычные и хрупкие посылки. Доставку любой посылки считают одинаково, но хрупкую ещё "
              "и кладут в защитную упаковку за отдельные деньги. Вес обычных посылок в килограммах записан в массиве "
              "`regular`, хрупких — в массиве `fragile`.",
        steps=["Ниже класса `Solution` опиши класс `Parcel` (без `public`) с полем `int weight` и методом `int price()`: доставка стоит "
               "100 руб. плюс 20 руб. за каждый килограмм.",
               "Опиши класс `FragileParcel` — наследник `Parcel`. Добавь в него только новый метод `int safePrice()`: "
               "цена доставки из унаследованного `price()` плюс 150 руб. за упаковку.",
               "Для каждого веса из `regular` создай объект `Parcel`, запиши вес в его поле `weight` и выведи строку вида "
               "`Regular parcel 2 kg: 140 rub`",
               "Для каждого веса из `fragile` создай объект `FragileParcel`, запиши вес в его поле `weight` и выведи строку "
               "вида `Fragile parcel 3 kg: 310 rub` — с ценой из `safePrice()`.",
               "Последней строкой выведи `Total: … rub` — сумму за все посылки (за хрупкие — вместе с упаковкой)."],
        hint="Не считай цену доставки в `safePrice` заново — вызови `price()`: хрупкая посылка тоже посылка, и этот метод "
             "у неё уже есть от родителя. Если тариф доставки изменится, править его придётся только в одном месте.",
        solution=PARCELS_MAIN, classes=PARCELS,
        wrong=[("считает в safePrice цену заново и забывает базовые 100 руб.",
                PARCELS_MAIN, PARCELS.replace("return price() + 150;", "return 20 * weight + 150;")),
               ("добавляет в итог цену хрупкой посылки без упаковки",
                PARCELS_MAIN.replace("total += parcel.safePrice();", "total += parcel.price();"))],
        constructs=["class", "for"],
        checks=exist("Parcel", "FragileParcel")
        + extends("FragileParcel", "Parcel", "хрупкая посылка тоже посылка и получит поле weight и метод price")
        + f'need({declares("FragileParcel", "safePrice")}, "Добавь метод safePrice в класс FragileParcel: упаковка нужна только хрупким посылкам");\n'
        + f'need(!{declares("FragileParcel", "price")}, "Не пиши price в FragileParcel заново: этот метод хрупкая посылка получает от Parcel");\n',
    ),
]
