"""GETTER_SETTER_BASIC — «Геттеры и сеттеры» (Java). Taught before: everything up to static methods of Solution,
classes, creating objects, constructors, this, private fields changed through checking methods. Here: the
convention — a private field `x` is read by `getX()` and changed by `setX(value)`; the setter checks the new value
and keeps the old one when it does not fit; a getter may compute a value instead of storing it. Not yet: static
fields, inheritance, exceptions."""
from java_tasks import JavaOutputTask

SKILL = "GETTER_SETTER_BASIC"


def find_class(name: str) -> str:
    return (f'Class<?> c = cls("{name}");\n'
            f'need(c != null, "Создай класс {name} ниже класса Solution (после его закрывающей скобки) и без слова public");\n')


def need_private_field(cls: str, name: str, java_type: str, why: str) -> str:
    """A private instance field of the class with this name and type; `why` says how it is reached instead."""
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


def need_getter(cls: str, java_type: str, field: str) -> str:
    name = "get" + field[0].upper() + field[1:]
    return need_method(cls, java_type, name, [], f"геттер, через который код снаружи читает закрытое поле {field}")


def need_setter(cls: str, java_type: str, field: str, rule: str = "") -> str:
    name = "set" + field[0].upper() + field[1:]
    return need_method(cls, "void", name, [f"{java_type} {field}"], f"сеттер, через который меняют поле {field}{rule}")


def need_constructor(cls: str, params: list[str], why: str) -> str:
    types = ", ".join(f"{p.split()[0]}.class" for p in params)
    return (f'{{ Constructor<?> k = null; try {{ k = c.getDeclaredConstructor({types}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(k != null, "Добавь в класс {cls} конструктор {cls}({", ".join(params)}) — {why}"); }}\n')


def need_after_calls(ctor_types: str, ctor_args: str, calls: list[tuple[str, str, str]], field: str, expected: str, message: str) -> str:
    """Creates an object, calls its methods (name, parameter type, argument) and compares a field with `expected`:
    the check inside the setter itself, not in main, is what keeps a wrong value out."""
    code = (f'{{ Object o = null; try {{ Constructor<?> k = c.getDeclaredConstructor({ctor_types}); k.setAccessible(true); '
            f'o = k.newInstance({ctor_args}); }} catch (Exception e) {{ }}\n  try {{\n')
    for name, java_type, arg in calls:
        code += f'    {{ Method m = c.getDeclaredMethod("{name}", {java_type}.class); m.setAccessible(true); m.invoke(o, {arg}); }}\n'
    return (code + '  } catch (Exception e) { }\n'
            f'  Field f = c.getDeclaredField("{field}"); f.setAccessible(true);\n'
            f'  need(o != null && Objects.equals(f.get(o), {expected}), "{message}"); }}\n')



# ───────── Pet card ─────────

PET = '''class Pet {
    private String name;
    private int weight;

    String getName() {
        return name;
    }

    void setName(String name) {
        if (name.length() > 0) {
            this.name = name;
        }
    }

    int getWeight() {
        return weight;
    }

    void setWeight(int weight) {
        if (weight >= 1 && weight <= 100) {
            this.weight = weight;
        }
    }
}'''

PET_MAIN = '''Pet pet = new Pet();
pet.setName(name);
pet.setWeight(weight);
System.out.println("Pet: " + pet.getName() + ", " + pet.getWeight() + " kg");
pet.setName(newName);
pet.setWeight(newWeight);
System.out.println("After edit: " + pet.getName() + ", " + pet.getWeight() + " kg");'''

# ───────── Travel time ─────────

TRIP = '''class Trip {
    private int distance;
    private int speed;

    Trip(int distance) {
        this.distance = distance;
        this.speed = 60;
    }

    int getDistance() {
        return distance;
    }

    int getSpeed() {
        return speed;
    }

    void setSpeed(int speed) {
        if (speed >= 1 && speed <= 130) {
            this.speed = speed;
        }
    }

    int getMinutes() {
        return distance * 60 / speed;
    }
}'''

TRIP_MAIN = '''Trip trip = new Trip(distance);
System.out.println("Distance: " + trip.getDistance() + " km");
for (int i = 0; i < speeds.length; i++) {
    trip.setSpeed(speeds[i]);
    System.out.println("Speed " + trip.getSpeed() + " km/h: " + trip.getMinutes() + " min");
}'''

# ───────── Class register ─────────

PUPIL = '''class Pupil {
    private String name;
    private int mark;

    String getName() {
        return name;
    }

    void setName(String name) {
        this.name = name;
    }

    int getMark() {
        return mark;
    }

    void setMark(int mark) {
        if (mark >= 2 && mark <= 5) {
            this.mark = mark;
        }
    }
}'''

PUPIL_MAIN = '''int sum = 0;
int count = 0;
for (int i = 0; i < names.length; i++) {
    Pupil pupil = new Pupil();
    pupil.setName(names[i]);
    pupil.setMark(marks[i]);
    if (pupil.getMark() == 0) {
        System.out.println(pupil.getName() + ": no mark");
    } else {
        System.out.println(pupil.getName() + ": " + pupil.getMark());
        sum += pupil.getMark();
        count++;
    }
}
if (count == 0) {
    System.out.println("No marks");
} else {
    System.out.println("Average: " + sum / count);
}'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-getset-rt-pet-card", title="Карточка питомца",
        given=[("String", "name"), ("int", "weight"), ("String", "newName"), ("int", "newWeight")],
        variants=[{"name": '"Barsik"', "weight": "5", "newName": '"Tom"', "newWeight": "6"},
                  {"name": '"Sharik"', "weight": "20", "newName": '""', "newWeight": "120"},
                  {"name": '"Kesha"', "weight": "1", "newName": '"Gosha"', "newWeight": "0"}],
        hidden=[{"name": '"Rex"', "weight": "30", "newName": '"Max"', "newWeight": "100"},
                {"name": '"Murka"', "weight": "4", "newName": '""', "newWeight": "101"},
                {"name": '"Bobik"', "weight": "12", "newName": '"Druzhok"', "newWeight": "1"},
                {"name": '"Pushok"', "weight": "7", "newName": '"Snow"', "newWeight": "-3"}],
        intro="В приложении ветклиники у питомца есть кличка и вес в килограммах. Хозяин может их поправить, но пустую кличку "
              "приложение не сохраняет, а вес принимает только от 1 до 100 кг. Кличка и вес записаны в полях `name` и `weight`, "
              "а в полях `newName` и `newWeight` — то, что хозяин потом ввёл при редактировании.",
        steps=["Ниже класса `Solution` создай класс `Pet` (без `public`) с закрытыми полями `private String name` и `private int weight`.",
               "Добавь геттеры и сеттеры: `String getName()` и `void setName(String name)`, `int getWeight()` и "
               "`void setWeight(int weight)`.",
               "В `setName` записывай кличку, только если она не пустая (длина больше 0). В `setWeight` записывай вес, только "
               "если он от 1 до 100 включительно. Иначе значение остаётся прежним.",
               "В `main` создай `new Pet()`, задай кличку и вес сеттерами из `name` и `weight` и выведи строку вида "
               "`Pet: Barsik, 5 kg`. Потом вызови сеттеры с `newName` и `newWeight` и выведи строку вида `After edit: Tom, 6 kg`."],
        hint="Внутри сеттера параметр называется так же, как поле, поэтому пиши `this.weight = weight;`. Проверку ставь перед "
             "присваиванием: если значение не подходит, сеттер просто ничего не делает.",
        solution=PET_MAIN,
        classes=PET,
        wrong=[("setName без проверки — пустая строка затирает кличку",
                PET_MAIN, PET.replace("        if (name.length() > 0) {\n            this.name = name;\n        }",
                                      "        this.name = name;")),
               ("в setWeight верхняя граница строгая — вес ровно 100 кг не принимается",
                PET_MAIN, PET.replace("weight <= 100", "weight < 100"))],
        constructs=["class"],
        checks=find_class("Pet")
               + need_private_field("Pet", "name", "String", "кличку читают и меняют через getName и setName")
               + need_private_field("Pet", "weight", "int", "вес читают и меняют через getWeight и setWeight")
               + need_getter("Pet", "String", "name")
               + need_setter("Pet", "String", "name", ", и в нём живёт проверка на пустую кличку")
               + need_getter("Pet", "int", "weight")
               + need_setter("Pet", "int", "weight", ", и в нём живёт проверка веса")
               + need_after_calls("", "", [("setWeight", "int", "40")], "weight", "40",
                                  "Сеттер setWeight должен записывать подходящий вес в поле объекта: this.weight = weight;")
               + need_after_calls("", "", [("setWeight", "int", "40"), ("setWeight", "int", "101"), ("setWeight", "int", "0")], "weight", "40",
                                  "Проверка веса должна быть внутри setWeight: число меньше 1 или больше 100 сеттер не записывает")
               + need_after_calls("", "", [("setName", "String", '"Bim"'), ("setName", "String", '""')], "name", '"Bim"',
                                  "Проверка клички должна быть внутри setName: пустую строку сеттер не записывает"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-getset-rt-travel-time", title="Время в пути",
        given=[("int", "distance"), ("int[]", "speeds")],
        variants=[{"distance": "120", "speeds": "{90, 200, 40}"},
                  {"distance": "300", "speeds": "{100, 0, 120}"},
                  {"distance": "45", "speeds": "{30, 130, 131}"}],
        hidden=[{"distance": "60", "speeds": "{}"},
                {"distance": "100", "speeds": "{1, -20}"},
                {"distance": "250", "speeds": "{50, 140, 125}"},
                {"distance": "80", "speeds": "{130, 131, 0, 70}"}],
        intro="Навигатор считает, сколько минут займёт дорога длиной `distance` км. Сначала он берёт скорость 60 км/ч, а "
              "водитель по очереди пробует другие скорости из массива `speeds`. Скорость принимается только от 1 до "
              "130 км/ч, иначе остаётся прежняя.",
        steps=["Ниже класса `Solution` создай класс `Trip` (без `public`) с закрытыми полями `private int distance` и "
               "`private int speed` и конструктором `Trip(int distance)`, который запоминает расстояние и ставит скорость 60.",
               "Добавь геттеры `int getDistance()` и `int getSpeed()` и сеттер `void setSpeed(int speed)`: он записывает "
               "скорость, только если она от 1 до 130 включительно.",
               "Добавь геттер `int getMinutes()`, который не хранит значение в поле, а считает его: `distance * 60 / speed` "
               "(дробная часть отбрасывается).",
               "В `main` создай `new Trip(distance)` и выведи строку вида `Distance: 120 km`. Потом для каждого числа из "
               "`speeds` вызови `setSpeed` и выведи строку вида `Speed 90 km/h: 80 min` — числа бери из геттеров."],
        hint="Геттер не обязан просто возвращать поле: `getMinutes()` вычисляет время по текущим полям, поэтому оно само "
             "меняется вместе со скоростью. Если скорость не подошла, выводится прежняя скорость и прежнее время.",
        solution=TRIP_MAIN,
        classes=TRIP,
        wrong=[("setSpeed отсекает только ноль — 200 км/ч и отрицательные скорости принимаются",
                TRIP_MAIN, TRIP.replace("        if (speed >= 1 && speed <= 130) {\n            this.speed = speed;\n        }",
                                        "        if (speed != 0) {\n            this.speed = speed;\n        }")),
               ("в main выводит скорость из массива, а не из геттера — отклонённая скорость печатается как принятая",
                TRIP_MAIN.replace('"Speed " + trip.getSpeed()', '"Speed " + speeds[i]'))],
        constructs=["class"],
        checks=find_class("Trip")
               + need_private_field("Trip", "distance", "int", "расстояние читают через getDistance")
               + need_private_field("Trip", "speed", "int", "скорость читают и меняют через getSpeed и setSpeed")
               + need_constructor("Trip", ["int distance"], "он запоминает расстояние и ставит скорость 60")
               + need_getter("Trip", "int", "distance")
               + need_getter("Trip", "int", "speed")
               + need_setter("Trip", "int", "speed", ", и в нём живёт проверка скорости")
               + need_method("Trip", "int", "getMinutes", [], "он считает время в пути по полям объекта")
               + need_after_calls("int.class", "100", [("setSpeed", "int", "50")], "speed", "50",
                                  "Сеттер setSpeed должен записывать подходящую скорость в поле объекта: this.speed = speed;")
               + need_after_calls("int.class", "100", [("setSpeed", "int", "50"), ("setSpeed", "int", "131"), ("setSpeed", "int", "0")],
                                  "speed", "50", "Проверка скорости должна быть внутри setSpeed: число меньше 1 или больше 130 сеттер не записывает"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-getset-rt-class-register", title="Классный журнал",
        given=[("String[]", "names"), ("int[]", "marks")],
        variants=[{"names": '{"Anya", "Boris", "Vika", "Gosha"}', "marks": "{5, 7, 4, 3}"},
                  {"names": '{"Dima", "Eva", "Fedya"}', "marks": "{2, 5, 0}"},
                  {"names": '{"Ilya", "Kira", "Lena", "Mark", "Nadya"}', "marks": "{4, 4, 1, 5, 6}"}],
        hidden=[{"names": '{"Oleg"}', "marks": "{2}"},
                {"names": '{"Polina", "Rustam"}', "marks": "{1, 6}"},
                {"names": "{}", "marks": "{}"},
                {"names": '{"Semyon", "Tonya", "Ulyana", "Varya"}', "marks": "{5, 5, 4, -5}"}],
        intro="Учитель вносит оценки в электронный журнал. Имена учеников записаны в массиве `names`, а введённые оценки — "
              "в массиве `marks` под теми же номерами. Журнал принимает только оценки от 2 до 5; если учитель ошибся "
              "и ввёл другое число, у ученика пока нет оценки.",
        steps=["Ниже класса `Solution` создай класс `Pupil` (без `public`) с закрытыми полями `private String name` и "
               "`private int mark` и геттерами и сеттерами для обоих: `getName`, `setName`, `getMark`, `setMark`.",
               "В `setMark` записывай оценку, только если она от 2 до 5 включительно. Иначе поле остаётся прежним — у нового "
               "ученика это 0, то есть «оценки нет».",
               "В `main` для каждого ученика создай `new Pupil()` и задай имя и оценку сеттерами. Если `getMark()` вернул 0, "
               "выведи строку вида `Boris: no mark`, иначе — строку вида `Anya: 5`.",
               "Последней строкой выведи `Average: 4` — среднее целых оценок тех, у кого оценка есть (дробная часть "
               "отбрасывается). Если оценки нет ни у кого, выведи `No marks`."],
        hint="Проверку оценки делает сам сеттер, а в `main` ты только смотришь, что вернул геттер. Для среднего заведи "
             "до цикла сумму и счётчик и прибавляй к ним только настоящие оценки.",
        solution=PUPIL_MAIN,
        classes=PUPIL,
        wrong=[("setMark без проверки — оценки 7 и 1 тоже попадают в журнал",
                PUPIL_MAIN, PUPIL.replace("        if (mark >= 2 && mark <= 5) {\n            this.mark = mark;\n        }",
                                          "        this.mark = mark;")),
               ("делит сумму на число всех учеников, а не только тех, у кого есть оценка",
                PUPIL_MAIN.replace('System.out.println("Average: " + sum / count);',
                                   'System.out.println("Average: " + sum / names.length);'))],
        constructs=["class"],
        checks=find_class("Pupil")
               + need_private_field("Pupil", "name", "String", "имя читают и меняют через getName и setName")
               + need_private_field("Pupil", "mark", "int", "оценку читают и меняют через getMark и setMark")
               + need_getter("Pupil", "String", "name")
               + need_setter("Pupil", "String", "name")
               + need_getter("Pupil", "int", "mark")
               + need_setter("Pupil", "int", "mark", ", и в нём живёт проверка оценки")
               + need_after_calls("", "", [("setMark", "int", "4")], "mark", "4",
                                  "Сеттер setMark должен записывать подходящую оценку в поле объекта: this.mark = mark;")
               + need_after_calls("", "", [("setMark", "int", "4"), ("setMark", "int", "6"), ("setMark", "int", "1")], "mark", "4",
                                  "Проверка оценки должна быть внутри setMark: число меньше 2 или больше 5 сеттер не записывает"),
    ),
]
