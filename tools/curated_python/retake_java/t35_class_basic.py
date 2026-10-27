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


# ───────── Concert ticket ─────────

TICKET = '''class Ticket {
    String band;
    int row;
    int seat;
}'''

TICKET_MAIN = '''Ticket ticket = new Ticket();
ticket.band = band;
ticket.row = row;
ticket.seat = seat;
System.out.println("Concert: " + ticket.band);
System.out.println("Row " + ticket.row + ", seat " + ticket.seat);'''

# ───────── Pizza party ─────────

PIZZA = '''class Pizza {
    String name;
    int slices;
    int guests;

    int perGuest() {
        return slices / guests;
    }

    int left() {
        return slices % guests;
    }
}'''

PIZZA_MAIN = '''Pizza pizza = new Pizza();
pizza.name = name;
pizza.slices = slices;
pizza.guests = guests;
System.out.println("Pizza: " + pizza.name);
System.out.println("Each guest: " + pizza.perGuest() + " slices");
System.out.println("Left: " + pizza.left());'''

# ───────── Weather log ─────────

WEATHER = '''class WeatherLog {
    String city;
    int[] temps;

    int average() {
        int sum = 0;
        for (int i = 0; i < temps.length; i++) {
            sum += temps[i];
        }
        return sum / temps.length;
    }

    int daysAbove(int limit) {
        int count = 0;
        for (int t : temps) {
            if (t > limit) {
                count++;
            }
        }
        return count;
    }
}'''

WEATHER_MAIN = '''WeatherLog log = new WeatherLog();
log.city = city;
log.temps = temps;
System.out.println("City: " + log.city);
System.out.println("Days: " + log.temps.length);
System.out.println("Average: " + log.average());
System.out.println("Warm days: " + log.daysAbove(15));'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-class-rt-concert-ticket", title="Билет на концерт",
        given=[("String", "band"), ("int", "row"), ("int", "seat")],
        variants=[{"band": '"Kino"', "row": "5", "seat": "12"},
                  {"band": '"Splean"', "row": "14", "seat": "3"},
                  {"band": '"Bi-2"', "row": "1", "seat": "27"}],
        hidden=[{"band": '"Aria"', "row": "22", "seat": "8"},
                {"band": '"Zemfira"', "row": "3", "seat": "40"},
                {"band": '"Mumiy Troll"', "row": "9", "seat": "1"}],
        intro="Касса концертного зала печатает билеты. На каждом билете — название группы, ряд и место. "
              "Все билеты устроены одинаково, поэтому их удобно один раз описать классом, а потом создавать по нему объекты.",
        steps=["Ниже класса `Solution`, после его последней закрывающей скобки, создай класс `Ticket` — без слова `public`. "
               "Объяви в нём три поля: `String band`, `int row` и `int seat`.",
               "В `main` создай объект `Ticket ticket = new Ticket();` и запиши в его поля данные из заготовки: "
               "`ticket.band = band;` и так же для `row` и `seat`.",
               "Выведи две строки вида `Concert: Kino` и `Row 5, seat 12`. Значения бери из полей объекта: "
               "`ticket.band`, `ticket.row` и `ticket.seat`."],
        hint="Класс только описывает, какие поля будут у каждого билета. Значения появляются у объекта, созданного через "
             "`new`, когда ты записываешь их через точку: слева от `=` — поле объекта, справа — поле из заготовки.",
        solution=TICKET_MAIN,
        classes=TICKET,
        wrong=[("забыл записать в объект место — у нового объекта поле seat равно 0",
                TICKET_MAIN.replace("ticket.seat = seat;\n", "")),
               ("перепутал поля: ряд записал в seat, а место — в row",
                TICKET_MAIN.replace("ticket.row = row;\nticket.seat = seat;", "ticket.row = seat;\nticket.seat = row;"))],
        constructs=["class"],
        checks=find_class("Ticket")
               + need_field("Ticket", "band", "String", "в нём объект хранит название группы")
               + need_field("Ticket", "row", "int", "в нём объект хранит номер ряда")
               + need_field("Ticket", "seat", "int", "в нём объект хранит номер места"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-class-rt-pizza-party", title="Пицца на всех",
        given=[("String", "name"), ("int", "slices"), ("int", "guests")],
        variants=[{"name": '"Margherita"', "slices": "8", "guests": "3"},
                  {"name": '"Pepperoni"', "slices": "12", "guests": "5"},
                  {"name": '"Hawaii"', "slices": "10", "guests": "4"}],
        hidden=[{"name": '"Four Cheese"', "slices": "12", "guests": "4"},
                {"name": '"Veggie"', "slices": "6", "guests": "1"},
                {"name": '"Bavarian"', "slices": "16", "guests": "7"},
                {"name": '"Diablo"', "slices": "8", "guests": "9"}],
        intro="На праздник заказали пиццу. У неё есть название `name` и число кусков `slices`, а за столом `guests` гостей. "
              "Каждый получает поровну целых кусков, а то, что не делится поровну, остаётся на тарелке.",
        steps=["Ниже класса `Solution` создай класс `Pizza` (без `public`) с полями `String name`, `int slices` и `int guests`.",
               "Добавь в класс два метода без слова `static`: `int perGuest()` возвращает, сколько целых кусков достанется "
               "каждому гостю (`slices / guests`), а `int left()` — сколько кусков останется (`slices % guests`).",
               "В `main` создай объект `Pizza pizza = new Pizza();` и запиши в его поля данные из заготовки.",
               "Выведи три строки вида `Pizza: Margherita`, `Each guest: 2 slices` и `Left: 2`. Числа получи вызовами "
               "`pizza.perGuest()` и `pizza.left()`."],
        hint="Метод внутри класса видит поля своего объекта просто по именам, поэтому параметры ему не нужны. "
             "Если гостей больше, чем кусков, каждому достаётся 0 кусков, а на тарелке остаются все.",
        solution=PIZZA_MAIN,
        classes=PIZZA,
        wrong=[("в left() перепутал деление и остаток: возвращает slices / guests",
                PIZZA_MAIN, PIZZA.replace("return slices % guests;", "return slices / guests;")),
               ("в left() вычитает гостей из кусков вместо остатка от деления",
                PIZZA_MAIN, PIZZA.replace("return slices % guests;", "return slices - guests;"))],
        constructs=["class"],
        checks=find_class("Pizza")
               + need_field("Pizza", "name", "String", "название пиццы")
               + need_field("Pizza", "slices", "int", "число кусков")
               + need_field("Pizza", "guests", "int", "число гостей")
               + need_method("Pizza", "perGuest", "int", "он считает куски на одного гостя")
               + need_method("Pizza", "left", "int", "он считает оставшиеся куски"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-class-rt-weather-log", title="Дневник погоды",
        given=[("String", "city"), ("int[]", "temps")],
        variants=[{"city": '"Kazan"', "temps": "{12, 18, 15, 20, 9}"},
                  {"city": '"Sochi"', "temps": "{22, 25, 19, 24}"},
                  {"city": '"Omsk"', "temps": "{5, 8, 16, 11, 14, 3}"}],
        hidden=[{"city": '"Tver"', "temps": "{15}"},
                {"city": '"Perm"', "temps": "{15, 16, 14, 15}"},
                {"city": '"Ufa"', "temps": "{30, 28, 26, 31, 29, 27, 33}"},
                {"city": '"Pskov"', "temps": "{2, 4, 7}"}],
        intro="Метеостанция ведёт дневник: в поле `city` записан город, а в массиве `temps` — дневная температура "
              "в градусах за несколько дней подряд. Пусть дневник будет объектом, который сам подводит итоги.",
        steps=["Ниже класса `Solution` создай класс `WeatherLog` (без `public`) с полями `String city` и `int[] temps`.",
               "Добавь в класс метод `int average()` без `static`: он возвращает среднюю температуру — сумму всех чисел "
               "из `temps`, делённую на их количество (дробную часть отбрось).",
               "Добавь метод `int daysAbove(int limit)` без `static`: он возвращает, сколько дней температура была "
               "строго больше `limit`.",
               "В `main` создай объект `WeatherLog`, запиши в него данные из заготовки и выведи четыре строки вида "
               "`City: Kazan`, `Days: 5` (сколько чисел в массиве), `Average: 14` и `Warm days: 2` (результат `daysAbove(15)`)."],
        hint="Оба метода перебирают массив `temps` своего объекта циклом. День ровно с 15 градусами тёплым не считается: "
             "нужно именно «больше».",
        solution=WEATHER_MAIN,
        classes=WEATHER,
        wrong=[("daysAbove считает и дни, равные limit",
                WEATHER_MAIN, WEATHER.replace("t > limit", "t >= limit")),
               ("average() делит сумму на 7 — как будто в дневнике всегда неделя",
                WEATHER_MAIN, WEATHER.replace("return sum / temps.length;", "return sum / 7;"))],
        constructs=["class"],
        checks=find_class("WeatherLog")
               + need_field("WeatherLog", "city", "String", "город")
               + need_field("WeatherLog", "temps", "int[]", "температуры по дням")
               + need_method("WeatherLog", "average", "int", "он возвращает среднюю температуру")
               + '{ Method m = null; try { m = c.getDeclaredMethod("daysAbove", int.class); } catch (NoSuchMethodException e) { }\n'
                 '  need(m != null && m.getReturnType() == int.class && !Modifier.isStatic(m.getModifiers()), '
                 '"Добавь в класс WeatherLog метод int daysAbove(int limit) без static — он считает тёплые дни"); }\n',
    ),
]
