"""THROWS_BASIC — «Объявление throws» (Java). Taught before: everything up to try/catch, finally and throw, classes,
inheritance and super. Here: an own checked exception (a small class extending Exception), a method that throws it
and declares it with throws, and a caller that handles it — or passes it further by declaring throws too. The syntax
tree checks cannot see throws, so the checks look at the methods through reflection (getExceptionTypes) and call them
to make sure they really throw. Only our own messages are printed, never Java's."""
from java_tasks import JavaOutputTask

SKILL = "THROWS_BASIC"


def with_methods(main: str, methods: str) -> str:
    """Body of main followed by more static methods of Solution (the template's closing brace ends the last one)."""
    body = methods.strip()
    assert body.endswith("}")
    return main.rstrip() + "\n}\n\n" + body[:-1].rstrip()


def exception_class(name: str) -> str:
    return f"class {name} extends Exception {{\n    {name}(String message) {{\n        super(message);\n    }}\n}}"


def checked_class_check(name: str, why: str) -> str:
    return (f'Class<?> ex = cls("{name}");\n'
            f'need(ex != null && Exception.class.isAssignableFrom(ex) && !RuntimeException.class.isAssignableFrom(ex), '
            f'"Создай класс {name} extends Exception — {why}");\n')


# ── 1. Аптека ──
CLOSED = exception_class("ClosedException")
PHARMACY_MAIN = ('try {\n    checkHour(hour);\n    System.out.println("The pharmacy is open, come in");\n'
                 '} catch (ClosedException e) {\n    System.out.println(e.getMessage());\n'
                 '    System.out.println("Try the 24-hour pharmacy");\n}')
PHARMACY_CHECK = """static void checkHour(int hour) throws ClosedException {
    if (hour < 9 || hour >= 21) {
        throw new ClosedException("Closed at " + hour + ":00, open from 9:00 to 21:00");
    }
}"""
PHARMACY_CHECKS = checked_class_check("ClosedException", "это проверяемое исключение: Java потребует объявить его в throws и обработать") + """Method m = null;
try { m = Solution.class.getDeclaredMethod("checkHour", int.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()), "Добавь в класс Solution метод static void checkHour(int hour) throws ClosedException");
need(Arrays.asList(m.getExceptionTypes()).contains(ex), "Объяви в методе checkHour именно throws ClosedException: так тот, кто вызывает метод, знает, какую ошибку обработать");
m.setAccessible(true);
for (int bad : new int[]{8, 21}) {
  boolean thrown = false;
  try { m.invoke(null, bad); } catch (InvocationTargetException e) { thrown = ex.isInstance(e.getCause()); }
  need(thrown, "Если аптека в этот час закрыта (раньше 9 или с 21 часа), метод checkHour должен выбрасывать ClosedException через throw");
}
try { m.invoke(null, 9); } catch (InvocationTargetException e) { need(false, "В 9 часов аптека уже открыта: при таком часе checkHour не должен выбрасывать исключение"); }"""

# ── 2. Оценки из файла ──
BAD_MARK = exception_class("BadMarkException")
IMPORT_MAIN = ('try {\n    System.out.println("Total: " + total(marks));\n    System.out.println("Marks: " + marks.length);\n'
               '} catch (BadMarkException e) {\n    System.out.println("Cannot count: " + e.getMessage());\n}')
IMPORT_METHODS = """static int parseMark(String text) throws BadMarkException {
    int mark;
    try {
        mark = Integer.parseInt(text);
    } catch (NumberFormatException e) {
        throw new BadMarkException("not a mark: " + text);
    }
    if (mark < 1 || mark > 5) {
        throw new BadMarkException("mark out of range: " + mark);
    }
    return mark;
}

static int total(String[] marks) throws BadMarkException {
    int sum = 0;
    for (String text : marks) {
        sum += parseMark(text);
    }
    return sum;
}"""
IMPORT_CHECKS = checked_class_check("BadMarkException", "это проверяемое исключение для ошибочной записи в файле оценок") + """Method parse = null;
Method total = null;
try { parse = Solution.class.getDeclaredMethod("parseMark", String.class); } catch (NoSuchMethodException e) { }
try { total = Solution.class.getDeclaredMethod("total", String[].class); } catch (NoSuchMethodException e) { }
need(parse != null && Modifier.isStatic(parse.getModifiers()) && parse.getReturnType() == int.class, "Добавь в класс Solution метод static int parseMark(String text) throws BadMarkException");
need(total != null && Modifier.isStatic(total.getModifiers()) && total.getReturnType() == int.class, "Добавь в класс Solution метод static int total(String[] marks) throws BadMarkException");
need(Arrays.asList(parse.getExceptionTypes()).contains(ex) && Arrays.asList(total.getExceptionTypes()).contains(ex), "Объяви throws BadMarkException и в parseMark, и в total: исключение должно дойти до main");
parse.setAccessible(true);
total.setAccessible(true);
for (String bad : new String[]{"abc", "7"}) {
  boolean thrown = false;
  try { parse.invoke(null, bad); } catch (InvocationTargetException e) { thrown = ex.isInstance(e.getCause()); }
  need(thrown, "Для записи, которая не является оценкой от 1 до 5, метод parseMark должен выбрасывать BadMarkException — и вместо NumberFormatException тоже");
}
boolean passed = false;
try { total.invoke(null, (Object) new String[]{"5", "x"}); } catch (InvocationTargetException e) { passed = ex.isInstance(e.getCause()); }
need(passed, "Метод total должен выпускать BadMarkException наружу, а не ловить его сам: пусть его обработает catch в main");"""

# ── 3. Парковка ──
FULL = exception_class("ParkingFullException")
NOT_HERE = exception_class("CarNotFoundException")
PARKING = """class Parking {
    private List<String> cars = new ArrayList<>();
    private int places;

    Parking(int places) {
        this.places = places;
    }

    void enter(String car) throws ParkingFullException {
        if (cars.size() >= places) {
            throw new ParkingFullException("No place for " + car);
        }
        cars.add(car);
    }

    void leave(String car) throws CarNotFoundException {
        if (!cars.contains(car)) {
            throw new CarNotFoundException("Car " + car + " is not here");
        }
        cars.remove(car);
    }

    int count() {
        return cars.size();
    }
}"""
PARKING_MAIN = ('Parking parking = new Parking(places);\nfor (String event : events) {\n    String car = event.substring(1);\n'
                '    try {\n        if (event.charAt(0) == \'+\') {\n            parking.enter(car);\n'
                '            System.out.println("In: " + car);\n        } else {\n            parking.leave(car);\n'
                '            System.out.println("Out: " + car);\n        }\n    } catch (ParkingFullException e) {\n'
                '        System.out.println("Full: " + e.getMessage());\n    } catch (CarNotFoundException e) {\n'
                '        System.out.println("Error: " + e.getMessage());\n    }\n}\n'
                'System.out.println("Cars inside: " + parking.count());')
PARKING_CHECKS = """Class<?> full = cls("ParkingFullException");
Class<?> missing = cls("CarNotFoundException");
need(full != null && missing != null && Exception.class.isAssignableFrom(full) && Exception.class.isAssignableFrom(missing) && !RuntimeException.class.isAssignableFrom(full) && !RuntimeException.class.isAssignableFrom(missing), "Создай два класса, ParkingFullException extends Exception и CarNotFoundException extends Exception, — это проверяемые исключения для двух разных отказов");
Class<?> c = cls("Parking");
need(c != null, "Создай класс Parking: он хранит машины на стоянке и сам проверяет въезд и выезд");
Method enter = null;
Method leave = null;
try { enter = c.getDeclaredMethod("enter", String.class); } catch (NoSuchMethodException e) { }
try { leave = c.getDeclaredMethod("leave", String.class); } catch (NoSuchMethodException e) { }
need(enter != null && Arrays.asList(enter.getExceptionTypes()).contains(full), "Объяви в классе Parking метод void enter(String car) throws ParkingFullException");
need(leave != null && Arrays.asList(leave.getExceptionTypes()).contains(missing), "Объяви в классе Parking метод void leave(String car) throws CarNotFoundException");
Object parking = null;
try { Constructor<?> k = c.getDeclaredConstructor(int.class); k.setAccessible(true); parking = k.newInstance(1); } catch (NoSuchMethodException | InvocationTargetException e) { }
need(parking != null, "Добавь в класс Parking конструктор Parking(int places)");
enter.setAccessible(true);
leave.setAccessible(true);
boolean thrown = false;
try { leave.invoke(parking, "Z1"); } catch (InvocationTargetException e) { thrown = missing.isInstance(e.getCause()); }
need(thrown, "Если такой машины на стоянке нет, метод leave должен выбрасывать CarNotFoundException через throw");
try { enter.invoke(parking, "A1"); } catch (InvocationTargetException e) { need(false, "На пустую стоянку на 1 место метод enter должен пускать машину без исключения"); }
thrown = false;
try { enter.invoke(parking, "B2"); } catch (InvocationTargetException e) { thrown = full.isInstance(e.getCause()); }
need(thrown, "Если все места заняты, метод enter должен выбрасывать ParkingFullException через throw");"""


TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-throws-rt-pharmacy-hours", title="Часы работы аптеки",
        given=[("int", "hour")],
        variants=[{"hour": "14"}, {"hour": "7"}, {"hour": "22"}],
        hidden=[{"hour": "9"}, {"hour": "8"}, {"hour": "21"}, {"hour": "20"}, {"hour": "0"}],
        intro="Аптека работает с 9:00 до 21:00: в 9 часов она уже открыта, а в 21 час — уже закрыта. Который сейчас час, "
              "записано в поле `hour` (целое число от 0 до 23). Закрытая аптека — ожидаемая ситуация, которую нельзя "
              "забыть обработать, поэтому для неё нужно своё проверяемое исключение.",
        steps=["Создай класс `ClosedException`, унаследованный от `Exception`, с конструктором "
               "`ClosedException(String message)`, который передаёт текст в `super(message)`.",
               "Добавь в класс `Solution` метод `static void checkHour(int hour) throws ClosedException`. Если `hour` "
               "меньше 9 или не меньше 21, он выбрасывает `ClosedException` с сообщением вида "
               "`Closed at 7:00, open from 9:00 to 21:00` (с часом из `hour`).",
               "В `main` в блоке `try` вызови `checkHour(hour)` и выведи `The pharmacy is open, come in`.",
               "В `catch (ClosedException e)` выведи сообщение исключения, а следующей строкой — `Try the 24-hour pharmacy`."],
        hint="Слово `throws` в заголовке метода предупреждает того, кто его вызывает: «я могу выбросить такое "
             "исключение». Для проверяемого исключения без этого объявления Java метод не скомпилирует.",
        solution=with_methods(PHARMACY_MAIN, PHARMACY_CHECK),
        classes=CLOSED,
        wrong=[("сравнивает hour > 21 — в 21 час аптека как будто ещё открыта",
                with_methods(PHARMACY_MAIN, PHARMACY_CHECK.replace("hour >= 21", "hour > 21"))),
               ("совет про круглосуточную аптеку стоит после try/catch — печатается и тогда, когда аптека открыта",
                with_methods('try {\n    checkHour(hour);\n    System.out.println("The pharmacy is open, come in");\n'
                             '} catch (ClosedException e) {\n    System.out.println(e.getMessage());\n}\n'
                             'System.out.println("Try the 24-hour pharmacy");', PHARMACY_CHECK))],
        constructs=["try", "function", "class"],
        checks=PHARMACY_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-throws-rt-marks-import", title="Оценки из файла",
        given=[("String[]", "marks")],
        variants=[{"marks": '{"5", "4", "4", "3"}'}, {"marks": '{"5", "five", "4"}'}, {"marks": '{"3", "4", "6", "2", "x"}'}],
        hidden=[{"marks": "{}"}, {"marks": '{"1"}'}, {"marks": '{"0", "5"}'}, {"marks": '{"5", "5", "5", ""}'},
                {"marks": '{"2", "3", "4", "5", "1"}'}],
        intro="Электронный журнал загружает оценки за четверть из файла — каждая запись лежит строкой в массиве `marks`. "
              "Если хоть одна запись ошибочная (не число или не оценка от 1 до 5), сумму считать нельзя: учитель "
              "должен сначала исправить файл. Ошибку замечает метод, который читает одну запись, а сообщает о ней "
              "только `main`.",
        steps=["Создай класс `BadMarkException`, унаследованный от `Exception`, с конструктором "
               "`BadMarkException(String message)`, который передаёт текст в `super(message)`.",
               "Добавь в класс `Solution` метод `static int parseMark(String text) throws BadMarkException`. В блоке "
               "`try` он превращает `text` в число через `Integer.parseInt`; если вышел `NumberFormatException`, в его "
               "`catch` выброси `BadMarkException` с сообщением вида `not a mark: five`. Если число меньше 1 или больше "
               "5, выброси `BadMarkException` с сообщением вида `mark out of range: 6`. Иначе верни оценку.",
               "Добавь метод `static int total(String[] marks) throws BadMarkException`: он складывает `parseMark` всех "
               "записей и возвращает сумму. Сам он исключение не ловит — только объявляет в `throws`.",
               "В `main` в блоке `try` выведи строку вида `Total: 16` с результатом `total(marks)`, а затем строку вида "
               "`Marks: 4` — сколько записей в массиве. В `catch (BadMarkException e)` выведи `Cannot count: ` и "
               "сообщение исключения."],
        hint="Внутри `catch` можно выбросить другое исключение — так «чужая» ошибка `NumberFormatException` "
             "превращается в свою, понятную. Метод `total` пропускает её дальше, потому что в его заголовке тоже "
             "написано `throws BadMarkException`.",
        solution=with_methods(IMPORT_MAIN, IMPORT_METHODS),
        classes=BAD_MARK,
        wrong=[("total сам ловит исключение и пропускает ошибочные записи — сумма считается по неполному файлу",
                with_methods(IMPORT_MAIN, IMPORT_METHODS.replace(
                    "static int total(String[] marks) throws BadMarkException {\n    int sum = 0;\n    for (String text : marks) {\n"
                    "        sum += parseMark(text);\n    }\n",
                    "static int total(String[] marks) throws BadMarkException {\n    int sum = 0;\n    for (String text : marks) {\n"
                    "        try {\n            sum += parseMark(text);\n        } catch (BadMarkException e) {\n        }\n    }\n"))),
               ("проверяет только верхнюю границу — оценка 0 считается правильной",
                with_methods(IMPORT_MAIN, IMPORT_METHODS.replace("mark < 1 || mark > 5", "mark > 5")))],
        constructs=["try", "function", "class", "for"],
        checks=IMPORT_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-throws-rt-parking-gate", title="Шлагбаум на стоянке",
        given=[("int", "places"), ("List<String>", "events")],
        variants=[{"places": "2", "events": 'new ArrayList<>(List.of("+A111", "+B222", "+C333", "-A111", "+C333"))'},
                  {"places": "3", "events": 'new ArrayList<>(List.of("+K500", "-M700", "-K500", "-K500"))'},
                  {"places": "1", "events": 'new ArrayList<>(List.of("+X1", "+Y2", "-Y2", "-X1", "+Y2"))'}],
        hidden=[{"places": "2", "events": "new ArrayList<>()"},
                {"places": "1", "events": 'new ArrayList<>(List.of("+P1"))'},
                {"places": "0", "events": 'new ArrayList<>(List.of("+Q9", "-Q9"))'},
                {"places": "3", "events": 'new ArrayList<>(List.of("+A1", "+B2", "+C3", "+D4", "-B2", "+D4", "-E5"))'}],
        intro="У шлагбаума стоянки на `places` мест камера записывает события по порядку в список `events`: "
              "`+A111` — машина с номером `A111` хочет въехать, `-A111` — выехать. Если мест нет, шлагбаум машину "
              "не пускает, а если выезжает машина, которой на стоянке нет, — это ошибка камеры. Для двух отказов "
              "нужны два разных проверяемых исключения.",
        steps=["Создай классы `ParkingFullException` и `CarNotFoundException`, унаследованные от `Exception`, — у каждого "
               "конструктор с `String message`, который передаёт текст в `super(message)`.",
               "Создай класс `Parking` с приватным списком `private List<String> cars = new ArrayList<>();`, приватным "
               "полем `places`, конструктором `Parking(int places)` и методом `int count()` — сколько машин на стоянке.",
               "Добавь метод `void enter(String car) throws ParkingFullException`: если машин уже `places`, он выбрасывает "
               "исключение с сообщением вида `No place for C333`, иначе добавляет машину. И метод "
               "`void leave(String car) throws CarNotFoundException`: если машины нет в списке, он выбрасывает исключение "
               "с сообщением вида `Car M700 is not here`, иначе убирает её методом `cars.remove(car)`.",
               "В `main` создай стоянку и для каждого события возьми номер машины `event.substring(1)`. В блоке `try`: "
               "если `event.charAt(0) == '+'`, вызови `enter` и выведи строку вида `In: A111`, иначе вызови `leave` и "
               "выведи `Out: A111`. В `catch (ParkingFullException e)` выведи `Full: ` и сообщение, в "
               "`catch (CarNotFoundException e)` — `Error: ` и сообщение.",
               "После всех событий выведи строку вида `Cars inside: 2`."],
        hint="Каждый метод объявляет в `throws` только своё исключение, а `main` ставит после одного `try` два "
             "`catch` — по одному на каждый отказ. `try` стоит внутри цикла, поэтому после отказа события идут дальше.",
        solution=PARKING_MAIN,
        classes=FULL + "\n\n" + NOT_HERE + "\n\n" + PARKING,
        wrong=[("сравнивает cars.size() > places — на стоянку въезжает лишняя машина",
                PARKING_MAIN, FULL + "\n\n" + NOT_HERE + "\n\n" + PARKING.replace("cars.size() >= places", "cars.size() > places")),
               ("не убирает выехавшую машину из списка — место так и остаётся занятым",
                PARKING_MAIN, FULL + "\n\n" + NOT_HERE + "\n\n" + PARKING.replace("        cars.remove(car);\n", "")),
               ("try вокруг всего цикла — после первого отказа шлагбаум перестаёт работать",
                'Parking parking = new Parking(places);\ntry {\n    for (String event : events) {\n'
                '        String car = event.substring(1);\n        if (event.charAt(0) == \'+\') {\n            parking.enter(car);\n'
                '            System.out.println("In: " + car);\n        } else {\n            parking.leave(car);\n'
                '            System.out.println("Out: " + car);\n        }\n    }\n} catch (ParkingFullException e) {\n'
                '    System.out.println("Full: " + e.getMessage());\n} catch (CarNotFoundException e) {\n'
                '    System.out.println("Error: " + e.getMessage());\n}\n'
                'System.out.println("Cars inside: " + parking.count());')],
        constructs=["try", "class", "for", "if"],
        checks=PARKING_CHECKS,
    ),
]
