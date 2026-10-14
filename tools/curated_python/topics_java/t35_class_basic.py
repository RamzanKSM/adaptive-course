"""CLASS_BASIC — «Классы» (Java). Taught before: println, variables, arithmetic, strings, conditions, loops, arrays,
static methods of Solution with parameters and return values. Here: a class as a template — a top-level class with
instance fields and simple methods that use those fields; one object made with `new` and filled through the dot.
Not yet: constructors (topic 37), this (38), private (39), static fields (41)."""
from java_tasks import JavaOutputTask

SKILL = "CLASS_BASIC"


def find_class(name: str) -> str:
    return (f'Class<?> c = cls("{name}");\n'
            f'need(c != null, "Создай класс {name} ниже класса Solution (после его закрывающей скобки) и без слова public");\n')


def need_field(cls: str, name: str, java_type: str, why: str) -> str:
    """An instance (non-static) field of the class with this name and type."""
    return (f'{{ Field f = null; try {{ f = c.getDeclaredField("{name}"); }} catch (NoSuchFieldException e) {{ }}\n'
            f'  need(f != null && f.getType() == {java_type}.class, "Объяви в классе {cls} поле {java_type} {name} — {why}");\n'
            f'  need(!Modifier.isStatic(f.getModifiers()), "Объяви поле {name} в классе {cls} без слова static — тогда у каждого объекта будет своё значение"); }}\n')


def need_method(cls: str, name: str, returns: str, why: str) -> str:
    """A non-static method without parameters."""
    return (f'{{ Method m = null; try {{ m = c.getDeclaredMethod("{name}"); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(m != null && m.getReturnType() == {returns}.class, "Добавь в класс {cls} метод {returns} {name}() — {why}");\n'
            f'  need(!Modifier.isStatic(m.getModifiers()), "Метод {name} в классе {cls} пиши без слова static — он работает с полями своего объекта"); }}\n')


# ───────── Reader ─────────

READER = '''class Reader {
    String name;
    int grade;
    int books;
}'''

READER_MAIN = '''Reader reader = new Reader();
reader.name = name;
reader.grade = grade;
reader.books = books;
System.out.println("Reader: " + reader.name + ", grade " + reader.grade);
System.out.println("Books: " + reader.books);'''

# ───────── Aquarium ─────────

AQUARIUM = '''class Aquarium {
    int length;
    int width;
    int height;

    int liters() {
        return length * width * height / 1000;
    }
}'''

AQUARIUM_MAIN = '''Aquarium aquarium = new Aquarium();
aquarium.length = length;
aquarium.width = width;
aquarium.height = height;
System.out.println("Size: " + aquarium.length + " x " + aquarium.width + " x " + aquarium.height + " cm");
System.out.println("Volume: " + aquarium.liters() + " liters");'''

# ───────── Workout ─────────

WORKOUT = '''class Workout {
    String sport;
    int[] minutes;

    int total() {
        int sum = 0;
        for (int i = 0; i < minutes.length; i++) {
            sum += minutes[i];
        }
        return sum;
    }

    int longest() {
        int best = minutes[0];
        for (int i = 1; i < minutes.length; i++) {
            if (minutes[i] > best) {
                best = minutes[i];
            }
        }
        return best;
    }
}'''

WORKOUT_MAIN = '''Workout workout = new Workout();
workout.sport = sport;
workout.minutes = minutes;
System.out.println("Sport: " + workout.sport);
System.out.println("Workouts: " + workout.minutes.length);
System.out.println("Total minutes: " + workout.total());
System.out.println("Longest: " + workout.longest() + " min");'''

# ───────── Pet passport ─────────

PET = """class Pet {
    String name;
    String kind;
    int age;
}"""

PET_MAIN = """Pet pet = new Pet();
pet.name = petName;
pet.kind = kind;
pet.age = age;
System.out.println("Pet: " + pet.name + " (" + pet.kind + ")");
System.out.println("Age: " + pet.age + " years");"""

# ───────── Phone tariff ─────────

TARIFF = """class Tariff {
    String title;
    int fee;
    int gigabytes;

    int perGigabyte() {
        return fee / gigabytes;
    }
}"""

TARIFF_MAIN = """Tariff tariff = new Tariff();
tariff.title = title;
tariff.fee = fee;
tariff.gigabytes = gigabytes;
System.out.println("Tariff: " + tariff.title);
System.out.println("Price of 1 GB: " + tariff.perGigabyte() + " rub");"""

# ───────── Piggy bank ─────────

PIGGY = """class PiggyBank {
    String owner;
    int[] coins;

    int sum() {
        int total = 0;
        for (int coin : coins) {
            total += coin;
        }
        return total;
    }

    int countOf(int value) {
        int count = 0;
        for (int coin : coins) {
            if (coin == value) {
                count++;
            }
        }
        return count;
    }
}"""

PIGGY_MAIN = """PiggyBank bank = new PiggyBank();
bank.owner = owner;
bank.coins = coins;
System.out.println("Owner: " + bank.owner);
System.out.println("Coins: " + bank.coins.length);
System.out.println("Sum: " + bank.sum() + " rub");
System.out.println("Fives: " + bank.countOf(5));"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-class-library-card", title="Читательский билет",
        given=[("String", "name"), ("int", "grade"), ("int", "books")],
        variants=[{"name": '"Anya"', "grade": "5", "books": "2"},
                  {"name": '"Timur"', "grade": "7", "books": "4"},
                  {"name": '"Vera"', "grade": "3", "books": "1"}],
        hidden=[{"name": '"Maxim"', "grade": "9", "books": "0"},
                {"name": '"Sonya"', "grade": "11", "books": "6"},
                {"name": '"Lev"', "grade": "1", "books": "3"}],
        intro="В школьной библиотеке на каждого читателя заводят билет: имя, класс и сколько книг сейчас у него на руках. "
              "Все билеты устроены одинаково, поэтому их удобно один раз описать классом — шаблоном, "
              "по которому потом создаются объекты.",
        steps=["Ниже класса `Solution`, после его последней закрывающей скобки, создай класс `Reader` — без слова `public`. "
               "Объяви в нём три поля: `String name`, `int grade` и `int books`.",
               "В `main` создай объект этого класса: `Reader reader = new Reader();`. Запиши в его поля данные из заготовки: "
               "`reader.name = name;` и так же для `grade` и `books`.",
               "Выведи две строки вида `Reader: Anya, grade 5` и `Books: 2`. Значения бери из полей объекта: "
               "`reader.name`, `reader.grade` и `reader.books`."],
        hint="Класс — это только описание: какие поля будут у каждого читателя. Сами значения появляются, когда ты создаёшь "
             "объект через `new` и записываешь их в его поля через точку. В строке `reader.grade = grade;` слева — поле "
             "объекта, справа — поле из заготовки.",
        solution=READER_MAIN,
        classes=READER,
        wrong=[("забыл записать в объект число книг — у нового объекта поле books равно 0",
                READER_MAIN.replace("reader.books = books;\n", "")),
               ("перепутал поля: число книг записал в grade, а класс — в books",
                READER_MAIN.replace("reader.grade = grade;\nreader.books = books;", "reader.grade = books;\nreader.books = grade;"))],
        constructs=["class"],
        checks=find_class("Reader")
               + need_field("Reader", "name", "String", "в нём объект хранит имя читателя")
               + need_field("Reader", "grade", "int", "в нём объект хранит класс, в котором учится читатель")
               + need_field("Reader", "books", "int", "в нём объект хранит число книг на руках"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-class-aquarium-liters", title="Объём аквариума",
        given=[("int", "length"), ("int", "width"), ("int", "height")],
        variants=[{"length": "60", "width": "30", "height": "40"},
                  {"length": "80", "width": "35", "height": "45"},
                  {"length": "40", "width": "25", "height": "30"}],
        hidden=[{"length": "100", "width": "40", "height": "50"},
                {"length": "30", "width": "20", "height": "25"},
                {"length": "45", "width": "25", "height": "30"},
                {"length": "120", "width": "50", "height": "60"}],
        intro="Ты выбираешь аквариум для рыбок. Продавец называет размеры в сантиметрах: длину `length`, ширину `width` "
              "и высоту `height`, а тебе нужно знать, сколько литров воды в него поместится.",
        steps=["Ниже класса `Solution` создай класс `Aquarium` (без `public`) с тремя полями типа `int`: `length`, `width` и `height`.",
               "Добавь в класс метод `int liters()`, который возвращает объём в литрах: длину, умноженную на ширину и на высоту, "
               "делённую на 1000 (в литре 1000 кубических сантиметров, дробную часть отбрось). В отличие от методов в `Solution`, "
               "слово `static` здесь не пиши: метод работает с полями конкретного аквариума.",
               "В `main` создай объект `Aquarium aquarium = new Aquarium();` и запиши в его поля размеры из заготовки.",
               "Выведи две строки вида `Size: 60 x 30 x 40 cm` и `Volume: 72 liters`. Размеры бери из полей объекта, "
               "а объём получи вызовом `aquarium.liters()`."],
        hint="Метод внутри класса видит поля своего объекта по именам, поэтому параметры ему не нужны. А вызов "
             "`aquarium.liters()` посчитает объём именно того аквариума, чьи поля ты заполнил.",
        solution=AQUARIUM_MAIN,
        classes=AQUARIUM,
        wrong=[("опечатка в методе: вместо высоты второй раз умножает на длину",
                AQUARIUM_MAIN, AQUARIUM.replace("length * width * height", "length * width * length")),
               ("забыл записать в объект высоту — она остаётся 0, и объём получается нулевым",
                AQUARIUM_MAIN.replace("aquarium.height = height;\n", ""))],
        constructs=["class"],
        checks=find_class("Aquarium")
               + need_field("Aquarium", "length", "int", "длина аквариума в сантиметрах")
               + need_field("Aquarium", "width", "int", "ширина аквариума в сантиметрах")
               + need_field("Aquarium", "height", "int", "высота аквариума в сантиметрах")
               + need_method("Aquarium", "liters", "int", "он считает объём по полям объекта"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-class-workout-log", title="Дневник тренировок",
        given=[("String", "sport"), ("int[]", "minutes")],
        variants=[{"sport": '"Swimming"', "minutes": "{45, 30, 60}"},
                  {"sport": '"Cycling"', "minutes": "{90, 40, 120, 35}"},
                  {"sport": '"Running"', "minutes": "{25, 30, 20, 40, 35}"}],
        hidden=[{"sport": '"Yoga"', "minutes": "{50}"},
                {"sport": '"Tennis"', "minutes": "{30, 45, 90}"},
                {"sport": '"Skiing"', "minutes": "{80, 20, 60, 70}"},
                {"sport": '"Boxing"', "minutes": "{15, 15, 15, 15, 15, 15}"}],
        intro="Ты ведёшь дневник тренировок за неделю. Вид спорта записан в поле `sport`, а длительность каждой тренировки "
              "в минутах — в массиве `minutes`. Дневник удобно сделать объектом, который сам умеет считать итоги.",
        steps=["Ниже класса `Solution` создай класс `Workout` (без `public`) с полями `String sport` и `int[] minutes`.",
               "Добавь в класс два метода без `static`: `int total()` возвращает сумму всех чисел из `minutes`, "
               "а `int longest()` — самое большое из них.",
               "В `main` создай объект `Workout` и запиши в его поля значения `sport` и `minutes` из заготовки.",
               "Выведи четыре строки вида `Sport: Swimming`, `Workouts: 3` (сколько чисел в массиве), "
               "`Total minutes: 135` и `Longest: 60 min`. Числа получай через объект: длину его массива и методы `total()` и `longest()`."],
        hint="Внутри `total()` и `longest()` перебирай массив `minutes` циклом, как в обычном методе, — это поле своего "
             "объекта. Для самой долгой тренировки начни с первого элемента и сравнивай с ним все остальные.",
        solution=WORKOUT_MAIN,
        classes=WORKOUT,
        wrong=[("в longest() цикл останавливается на элемент раньше — последняя тренировка не проверяется",
                WORKOUT_MAIN, WORKOUT.replace("i < minutes.length; i++) {\n            if", "i < minutes.length - 1; i++) {\n            if")),
               ("в longest() перепутан знак сравнения — находится самая короткая тренировка",
                WORKOUT_MAIN, WORKOUT.replace("minutes[i] > best", "minutes[i] < best"))],
        constructs=["class"],
        checks=find_class("Workout")
               + need_field("Workout", "sport", "String", "вид спорта")
               + need_field("Workout", "minutes", "int[]", "длительности тренировок")
               + need_method("Workout", "total", "int", "он возвращает сумму минут")
               + need_method("Workout", "longest", "int", "он возвращает самую долгую тренировку"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-class-pet-passport", title="Паспорт питомца",
        given=[("String", "petName"), ("String", "kind"), ("int", "age")],
        variants=[{"petName": '"Murka"', "kind": '"cat"', "age": "3"},
                  {"petName": '"Rex"', "kind": '"dog"', "age": "5"},
                  {"petName": '"Kesha"', "kind": '"parrot"', "age": "2"}],
        hidden=[{"petName": '"Bublik"', "kind": '"hamster"', "age": "1"},
                {"petName": '"Tuzik"', "kind": '"dog"', "age": "12"},
                {"petName": '"Snezhok"', "kind": '"rabbit"', "age": "4"}],
        intro="В ветеринарной клинике на каждого питомца заводят паспорт: кличка, вид животного и возраст в годах. "
              "Паспорта у всех одинаковые по устройству, поэтому их удобно описать классом.",
        steps=["Ниже класса `Solution`, после его последней закрывающей скобки, создай класс `Pet` — без слова `public`. "
               "Объяви в нём поля `String name`, `String kind` и `int age`.",
               "В `main` создай объект `Pet pet = new Pet();` и запиши в его поля данные из заготовки: "
               "`pet.name = petName;`, а также `kind` и `age`.",
               "Выведи две строки вида `Pet: Murka (cat)` и `Age: 3 years`. Значения бери из полей объекта `pet`."],
        hint="Поле объекта читается и записывается через точку: `pet.kind`. Обрати внимание, что поле в классе "
             "называется `name`, а данные в заготовке — `petName`.",
        solution=PET_MAIN,
        classes=PET,
        wrong=[("забыл записать в объект возраст — у нового объекта поле age равно 0",
                PET_MAIN.replace("pet.age = age;\n", "")),
               ("перепутал поля: кличку записал в kind, а вид — в name",
                PET_MAIN.replace("pet.name = petName;\npet.kind = kind;", "pet.name = kind;\npet.kind = petName;"))],
        constructs=["class"],
        checks=find_class("Pet")
               + need_field("Pet", "name", "String", "кличка питомца")
               + need_field("Pet", "kind", "String", "вид животного")
               + need_field("Pet", "age", "int", "возраст в годах"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-class-phone-tariff", title="Тариф связи",
        given=[("String", "title"), ("int", "fee"), ("int", "gigabytes")],
        variants=[{"title": '"Smart"', "fee": "600", "gigabytes": "20"},
                  {"title": '"Start"', "fee": "350", "gigabytes": "7"},
                  {"title": '"Max"', "fee": "900", "gigabytes": "40"}],
        hidden=[{"title": '"Mini"', "fee": "200", "gigabytes": "3"},
                {"title": '"Family"', "fee": "1200", "gigabytes": "50"},
                {"title": '"Light"', "fee": "450", "gigabytes": "9"},
                {"title": '"Unlim"', "fee": "1000", "gigabytes": "100"}],
        intro="Ты сравниваешь тарифы мобильной связи. У тарифа есть название `title`, абонентская плата `fee` в рублях "
              "в месяц и объём интернета `gigabytes`. Чтобы сравнивать честно, хочется знать цену одного гигабайта.",
        steps=["Ниже класса `Solution` создай класс `Tariff` (без `public`) с полями `String title`, `int fee` "
               "и `int gigabytes`.",
               "Добавь в класс метод `int perGigabyte()` без слова `static`: он возвращает плату, делённую на число "
               "гигабайтов (дробную часть отбрось).",
               "В `main` создай объект `Tariff tariff = new Tariff();` и запиши в его поля данные из заготовки.",
               "Выведи две строки вида `Tariff: Smart` и `Price of 1 GB: 30 rub`. Цену гигабайта получи вызовом "
               "`tariff.perGigabyte()`."],
        hint="Метод объекта видит поля `fee` и `gigabytes` своего объекта без точки и без параметров — просто по имени.",
        solution=TARIFF_MAIN,
        classes=TARIFF,
        wrong=[("в методе деление перевёрнуто: гигабайты делятся на плату",
                TARIFF_MAIN, TARIFF.replace("fee / gigabytes", "gigabytes / fee")),
               ("забыл записать в объект плату — поле fee остаётся 0",
                TARIFF_MAIN.replace("tariff.fee = fee;\n", ""))],
        constructs=["class"],
        checks=find_class("Tariff")
               + need_field("Tariff", "title", "String", "название тарифа")
               + need_field("Tariff", "fee", "int", "плата в месяц")
               + need_field("Tariff", "gigabytes", "int", "объём интернета")
               + need_method("Tariff", "perGigabyte", "int", "он считает цену гигабайта по полям объекта"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-class-piggy-bank", title="Копилка",
        given=[("String", "owner"), ("int[]", "coins")],
        variants=[{"owner": '"Anya"', "coins": "{10, 5, 10, 2, 1}"},
                  {"owner": '"Timur"', "coins": "{5, 5, 10, 10, 10, 2}"},
                  {"owner": '"Liza"', "coins": "{1, 2, 5, 10}"}],
        hidden=[{"owner": '"Gosha"', "coins": "{2}"},
                {"owner": '"Masha"', "coins": "{10, 10, 10}"},
                {"owner": '"Kolya"', "coins": "{1, 1, 5, 2, 2, 5, 10}"},
                {"owner": '"Nina"', "coins": "{}"}],
        intro="Ты разбиваешь копилку и пересчитываешь монеты. Чья копилка, записано в поле `owner`, а номиналы всех "
              "монет в рублях — в массиве `coins`. Пусть копилка будет объектом, который сам считает свои деньги.",
        steps=["Ниже класса `Solution` создай класс `PiggyBank` (без `public`) с полями `String owner` и `int[] coins`.",
               "Добавь в класс метод `int sum()` без `static` — он возвращает сумму всех монет.",
               "Добавь метод `int countOf(int value)` без `static` — он возвращает, сколько в копилке монет "
               "номиналом `value`.",
               "В `main` создай объект `PiggyBank`, запиши в него данные из заготовки и выведи четыре строки вида "
               "`Owner: Anya`, `Coins: 5` (сколько монет в массиве), `Sum: 28 rub` и `Fives: 1` (результат `countOf(5)`)."],
        hint="Метод объекта может принимать параметры, как обычный метод: внутри `countOf` сравнивай каждую монету "
             "из поля `coins` с параметром `value`. Копилка может оказаться пустой — тогда все числа равны 0.",
        solution=PIGGY_MAIN,
        classes=PIGGY,
        wrong=[("countOf считает монеты номиналом не меньше value, а не ровно value",
                PIGGY_MAIN, PIGGY.replace("coin == value", "coin >= value")),
               ("sum() считает количество монет, а не их сумму",
                PIGGY_MAIN, PIGGY.replace("total += coin;", "total++;"))],
        constructs=["class"],
        checks=find_class("PiggyBank")
               + need_field("PiggyBank", "owner", "String", "владелец копилки")
               + need_field("PiggyBank", "coins", "int[]", "номиналы монет")
               + need_method("PiggyBank", "sum", "int", "он возвращает сумму монет")
               + '{ Method m = null; try { m = c.getDeclaredMethod("countOf", int.class); } catch (NoSuchMethodException e) { }\n'
                 '  need(m != null && m.getReturnType() == int.class && !Modifier.isStatic(m.getModifiers()), '
                 '"Добавь в класс PiggyBank метод int countOf(int value) без static — он считает монеты одного номинала"); }\n',
    ),
]
