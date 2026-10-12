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
System.out.println("Читатель: " + reader.name + ", " + reader.grade + " класс");
System.out.println("Книг на руках: " + reader.books);'''

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
System.out.println("Размеры: " + aquarium.length + " на " + aquarium.width + " на " + aquarium.height + " см");
System.out.println("Объём: " + aquarium.liters() + " л");'''

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
System.out.println("Вид спорта: " + workout.sport);
System.out.println("Тренировок: " + workout.minutes.length);
System.out.println("Всего минут: " + workout.total());
System.out.println("Самая долгая: " + workout.longest() + " мин");'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-class-library-card", title="Читательский билет",
        given=[("String", "name"), ("int", "grade"), ("int", "books")],
        variants=[{"name": '"Аня"', "grade": "5", "books": "2"},
                  {"name": '"Тимур"', "grade": "7", "books": "4"},
                  {"name": '"Вера"', "grade": "3", "books": "1"}],
        hidden=[{"name": '"Максим"', "grade": "9", "books": "0"},
                {"name": '"Соня"', "grade": "11", "books": "6"},
                {"name": '"Лев"', "grade": "1", "books": "3"}],
        intro="В школьной библиотеке на каждого читателя заводят билет: имя, класс и сколько книг сейчас у него на руках. "
              "Все билеты устроены одинаково, поэтому их удобно один раз описать классом — шаблоном, "
              "по которому потом создаются объекты.",
        steps=["Ниже класса `Solution`, после его последней закрывающей скобки, создай класс `Reader` — без слова `public`. "
               "Объяви в нём три поля: `String name`, `int grade` и `int books`.",
               "В `main` создай объект этого класса: `Reader reader = new Reader();`. Запиши в его поля данные из заготовки: "
               "`reader.name = name;` и так же для `grade` и `books`.",
               "Выведи две строки вида `Читатель: Аня, 5 класс` и `Книг на руках: 2`. Значения бери из полей объекта: "
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
               "Выведи две строки вида `Размеры: 60 на 30 на 40 см` и `Объём: 72 л`. Размеры бери из полей объекта, "
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
        variants=[{"sport": '"Плавание"', "minutes": "{45, 30, 60}"},
                  {"sport": '"Велосипед"', "minutes": "{90, 40, 120, 35}"},
                  {"sport": '"Бег"', "minutes": "{25, 30, 20, 40, 35}"}],
        hidden=[{"sport": '"Йога"', "minutes": "{50}"},
                {"sport": '"Теннис"', "minutes": "{30, 45, 90}"},
                {"sport": '"Лыжи"', "minutes": "{80, 20, 60, 70}"},
                {"sport": '"Бокс"', "minutes": "{15, 15, 15, 15, 15, 15}"}],
        intro="Ты ведёшь дневник тренировок за неделю. Вид спорта записан в поле `sport`, а длительность каждой тренировки "
              "в минутах — в массиве `minutes`. Дневник удобно сделать объектом, который сам умеет считать итоги.",
        steps=["Ниже класса `Solution` создай класс `Workout` (без `public`) с полями `String sport` и `int[] minutes`.",
               "Добавь в класс два метода без `static`: `int total()` возвращает сумму всех чисел из `minutes`, "
               "а `int longest()` — самое большое из них.",
               "В `main` создай объект `Workout` и запиши в его поля значения `sport` и `minutes` из заготовки.",
               "Выведи четыре строки вида `Вид спорта: Плавание`, `Тренировок: 3` (сколько чисел в массиве), "
               "`Всего минут: 135` и `Самая долгая: 60 мин`. Числа получай через объект: длину его массива и методы `total()` и `longest()`."],
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
]
