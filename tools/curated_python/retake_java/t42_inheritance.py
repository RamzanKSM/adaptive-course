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




VEHICLES = """\
class Vehicle {
    int speed;

    int minutes(int km) {
        return km * 60 / speed;
    }
}

class Bike extends Vehicle {
}

class Car extends Vehicle {
    int fuel(int km) {
        return km * 8 / 100;
    }
}"""

VEHICLES_MAIN = """\
Bike bike = new Bike();
bike.speed = bikeSpeed;
Car car = new Car();
car.speed = carSpeed;
System.out.println("Bike: " + bike.minutes(distance) + " min");
System.out.println("Car: " + car.minutes(distance) + " min");
System.out.println("Car fuel: " + car.fuel(distance) + " l");"""

STEPS = """\
class StepCounter {
    private int steps;

    void walk(int count) {
        steps += count;
    }

    int getSteps() {
        return steps;
    }
}

class FitnessBand extends StepCounter {
    int goalPercent(int goal) {
        return getSteps() * 100 / goal;
    }
}"""

STEPS_MAIN = """\
FitnessBand band = new FitnessBand();
for (int count : walks) {
    band.walk(count);
}
System.out.println("Walks: " + walks.length);
System.out.println("Steps: " + band.getSteps());
System.out.println("Goal: " + band.goalPercent(goal) + "%");"""

# A beginner's way round inheritance: a separate class with a copy of everything — the output is the same.
STEPS_COPIED = STEPS.replace("""class FitnessBand extends StepCounter {
""", """class FitnessBand {
    private int steps;

    void walk(int count) {
        steps += count;
    }

    int getSteps() {
        return steps;
    }

""")

TAXI = """\
class Ride {
    String passenger;
    int km;

    int cost() {
        return 100 + 30 * km;
    }
}

class LuggageRide extends Ride {
    int bags;

    int totalCost() {
        return cost() + bags * 70;
    }
}"""

TAXI_MAIN = """\
int revenue = 0;
int withLuggage = 0;
for (int i = 0; i < passengers.length; i++) {
    if (bags[i] > 0) {
        LuggageRide ride = new LuggageRide();
        ride.passenger = passengers[i];
        ride.km = km[i];
        ride.bags = bags[i];
        System.out.println(ride.passenger + " (luggage): " + ride.totalCost() + " rub");
        revenue += ride.totalCost();
        withLuggage++;
    } else {
        Ride ride = new Ride();
        ride.passenger = passengers[i];
        ride.km = km[i];
        System.out.println(ride.passenger + ": " + ride.cost() + " rub");
        revenue += ride.cost();
    }
}
System.out.println("Rides: " + passengers.length + ", with luggage: " + withLuggage);
System.out.println("Revenue: " + revenue + " rub");"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-inh-rt-bike-car", title="Велосипед и машина",
        given=[("int", "bikeSpeed"), ("int", "carSpeed"), ("int", "distance")],
        variants=[{"bikeSpeed": "15", "carSpeed": "60", "distance": "30"},
                  {"bikeSpeed": "20", "carSpeed": "80", "distance": "50"},
                  {"bikeSpeed": "12", "carSpeed": "90", "distance": "24"}],
        hidden=[{"bikeSpeed": "10", "carSpeed": "100", "distance": "200"},
                {"bikeSpeed": "18", "carSpeed": "18", "distance": "36"},
                {"bikeSpeed": "25", "carSpeed": "75", "distance": "15"}],
        intro="Ты выбираешь, на чём доехать до дачи за `distance` км: на велосипеде или на машине. И то и другое — "
              "транспорт: у каждого есть скорость в км/ч, и время в пути считают одинаково. А вот бензин тратит только "
              "машина — 8 литров на 100 км. Скорости записаны в полях `bikeSpeed` и `carSpeed`.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Vehicle` без слова `public`, с полем `int speed`. "
               "Добавь метод `int minutes(int km)`, который возвращает время в пути в минутах: `km * 60 / speed` "
               "(дробная часть отбрасывается).",
               "Опиши класс `Bike`, который наследует `Vehicle`: `class Bike extends Vehicle {{ }}` — внутри ничего не пиши.",
               "Опиши класс `Car` — тоже наследник `Vehicle` — и добавь в него только метод `int fuel(int km)`: сколько литров "
               "бензина уйдёт на дорогу, `km * 8 / 100` (дробная часть отбрасывается).",
               "В `main` создай `Bike bike = new Bike();` и `Car car = new Car();` и запиши в их поле `speed` значения "
               "`bikeSpeed` и `carSpeed`.",
               "Выведи три строки вида `Bike: 120 min`, `Car: 30 min` и `Car fuel: 2 l` — для дороги длиной `distance` км."],
        hint="`class Bike extends Vehicle` значит «велосипед — это транспорт»: у объекта `Bike` сразу есть поле `speed` и "
             "метод `minutes`, хотя в классе `Bike` пусто. В наследнике пишут только то, чего нет у родителя.",
        solution=VEHICLES_MAIN, classes=VEHICLES,
        wrong=[("записал машине скорость велосипеда — скопировал строку и не поправил",
                VEHICLES_MAIN.replace("car.speed = carSpeed;", "car.speed = bikeSpeed;")),
               ("скопировал метод minutes в Car вместо того, чтобы получить его по наследству",
                VEHICLES_MAIN, VEHICLES.replace("class Car extends Vehicle {\n",
                                                "class Car extends Vehicle {\n    int minutes(int km) {\n        return km * 60 / speed;\n    }\n\n"))],
        constructs=["class"],
        checks=exist("Vehicle", "Bike", "Car")
        + extends("Bike", "Vehicle", "тогда велосипед получит поле и метод транспорта без копирования")
        + extends("Car", "Vehicle", "тогда машина получит поле и метод транспорта без копирования")
        + f'need({declares("Vehicle", "minutes")}, "Напиши метод minutes в классе Vehicle: время в пути считают одинаково для любого транспорта");\n'
        + f'need(!{declares("Bike", "minutes")} && !{declares("Car", "minutes")}, '
          '"Напиши метод minutes один раз — только в Vehicle: Bike и Car получат его по наследству");\n'
        + f'need({declares("Car", "fuel")} && !{declares("Vehicle", "fuel")}, '
          '"Метод fuel добавь только в класс Car: бензин тратит только машина");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-inh-rt-fitness-band", title="Фитнес-браслет",
        given=[("int[]", "walks"), ("int", "goal")],
        variants=[{"walks": "{3000, 2500, 1500}", "goal": "10000"},
                  {"walks": "{4200, 5100}", "goal": "8000"},
                  {"walks": "{800, 1200, 2000, 999}", "goal": "6000"}],
        hidden=[{"walks": "{}", "goal": "5000"},
                {"walks": "{10000}", "goal": "10000"},
                {"walks": "{7, 3}", "goal": "1000"},
                {"walks": "{6000, 6000, 3001}", "goal": "12000"}],
        intro="Обычный шагомер просто считает шаги, а фитнес-браслет умеет всё то же самое и ещё показывает, на сколько "
              "процентов выполнена дневная цель. Шаги за каждую прогулку записаны в массиве `walks`, цель на день — в `goal`.",
        steps=["Ниже класса `Solution` опиши класс `StepCounter` (без `public`) с закрытым полем `private int steps` (в начале 0) "
               "и двумя методами: `void walk(int count)` прибавляет шаги, а `int getSteps()` возвращает их число.",
               "Опиши класс `FitnessBand` — наследник `StepCounter` — и добавь в него только метод `int goalPercent(int goal)`: "
               "шаги, умноженные на 100 и делённые на `goal` (дробная часть отбрасывается). Шаги узнавай через "
               "унаследованный `getSteps()`.",
               "В `main` создай `FitnessBand band = new FitnessBand();` и передай методу `walk` все числа из `walks`.",
               "Выведи три строки вида `Walks: 3`, `Steps: 7000` и `Goal: 70%`."],
        hint="Поле `steps` закрыто, поэтому даже наследник не видит его напрямую. Но методы `walk` и `getSteps` браслет "
             "получил от шагомера и вызывает их как свои. Сначала умножай на 100, потом дели — иначе целочисленное "
             "деление даст 0.",
        solution=STEPS_MAIN, classes=STEPS,
        wrong=[("делит шаги на цель раньше, чем умножает на 100, — пока цель не выполнена, выходит 0%",
                STEPS_MAIN, STEPS.replace("getSteps() * 100 / goal", "getSteps() / goal * 100")),
               ("сделал FitnessBand отдельным классом и скопировал в него поле и методы StepCounter",
                STEPS_MAIN, STEPS_COPIED)],
        constructs=["class"],
        checks=exist("StepCounter", "FitnessBand")
        + extends("FitnessBand", "StepCounter", "тогда браслет получит walk и getSteps без копирования")
        + f'need({declares("FitnessBand", "goalPercent")}, "Добавь метод goalPercent в класс FitnessBand: проценты от цели показывает только браслет");\n'
        + f'need(!{declares("FitnessBand", "walk")} && !{declares("FitnessBand", "getSteps")}, '
          '"Методы walk и getSteps напиши только в StepCounter: FitnessBand получит их по наследству");\n'
        + 'boolean stepsPrivate;\n'
          'try { stepsPrivate = Modifier.isPrivate(cls("StepCounter").getDeclaredField("steps").getModifiers()); }\n'
          'catch (NoSuchFieldException e) { stepsPrivate = false; }\n'
          'need(stepsPrivate, "Объяви в StepCounter закрытое поле private int steps: наследник работает с ним через walk и getSteps");\n',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-inh-rt-taxi-luggage", title="Такси с багажом",
        given=[("String[]", "passengers"), ("int[]", "km"), ("int[]", "bags")],
        variants=[{"passengers": '{"Anya", "Boris", "Vika"}', "km": "{4, 10, 6}", "bags": "{0, 2, 0}"},
                  {"passengers": '{"Gleb", "Dina"}', "km": "{15, 3}", "bags": "{1, 3}"},
                  {"passengers": '{"Egor", "Zhanna", "Ira", "Kira"}', "km": "{2, 8, 5, 12}", "bags": "{0, 0, 4, 1}"}],
        hidden=[{"passengers": '{"Lena"}', "km": "{7}", "bags": "{0}"},
                {"passengers": '{"Mark"}', "km": "{0}", "bags": "{5}"},
                {"passengers": "{}", "km": "{}", "bags": "{}"},
                {"passengers": '{"Nina", "Oleg", "Polya"}', "km": "{9, 1, 20}", "bags": "{2, 0, 1}"}],
        intro="Служба такси считает стоимость поездок: посадка 100 руб. и по 30 руб. за каждый километр. Если пассажир "
              "едет с чемоданами, к цене добавляют 70 руб. за каждый чемодан. Имена пассажиров записаны в массиве "
              "`passengers`, длина поездки в километрах — в `km`, число чемоданов — в `bags` (0 — без багажа).",
        steps=["Ниже класса `Solution` опиши класс `Ride` (без `public`) с полями `String passenger` и `int km` и методом "
               "`int cost()` — посадка плюс оплата километров.",
               "Опиши класс `LuggageRide` — наследник `Ride`. Добавь в него своё поле `int bags` и метод `int totalCost()`: "
               "цена из унаследованного `cost()` плюс 70 руб. за каждый чемодан.",
               "В `main` пройди по пассажирам. Если чемоданов больше 0, создай объект `LuggageRide`, заполни его поля и выведи "
               "строку вида `Boris (luggage): 540 rub` с `totalCost()`. Иначе создай `Ride` и выведи строку вида "
               "`Anya: 220 rub` с `cost()`.",
               "В конце выведи строку вида `Rides: 3, with luggage: 1` — сколько всего поездок и сколько из них с багажом, — "
               "и строку вида `Revenue: 1040 rub` — сколько всего заплатили пассажиры (за багаж тоже)."],
        hint="Наследник получает от родителя поля `passenger`, `km` и метод `cost()` и добавляет своё поле `bags`. В "
             "`totalCost` не пересчитывай поездку заново — вызови `cost()`.",
        solution=TAXI_MAIN, classes=TAXI,
        wrong=[("в totalCost считает только багаж и забывает саму поездку",
                TAXI_MAIN, TAXI.replace("return cost() + bags * 70;", "return bags * 70;")),
               ("добавляет в выручку цену поездки с багажом без чемоданов",
                TAXI_MAIN.replace("revenue += ride.totalCost();", "revenue += ride.cost();"))],
        constructs=["class", "for"],
        checks=exist("Ride", "LuggageRide")
        + extends("LuggageRide", "Ride", "поездка с багажом тоже поездка и получит поля passenger, km и метод cost")
        + f'need({declares("LuggageRide", "totalCost")}, "Добавь метод totalCost в класс LuggageRide: доплата за чемоданы есть только у поездок с багажом");\n'
        + f'need(!{declares("LuggageRide", "cost")}, "Не пиши cost в LuggageRide заново: этот метод поездка с багажом получает от Ride");\n'
        + 'boolean ownField;\n'
          'try { cls("LuggageRide").getDeclaredField("bags"); ownField = true; } catch (NoSuchFieldException e) { ownField = false; }\n'
          'need(ownField, "Объяви поле int bags в классе LuggageRide: чемоданы есть только у поездок с багажом");\n',
    ),
]
