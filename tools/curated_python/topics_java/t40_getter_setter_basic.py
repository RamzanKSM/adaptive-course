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


# ───────── User profile ─────────

USER = '''class User {
    private String name;
    private int age;

    String getName() {
        return name;
    }

    void setName(String name) {
        this.name = name;
    }

    int getAge() {
        return age;
    }

    void setAge(int age) {
        if (age >= 1 && age <= 120) {
            this.age = age;
        }
    }
}'''

USER_MAIN = '''User user = new User();
user.setName(name);
user.setAge(age);
System.out.println("Name: " + user.getName());
System.out.println("Age: " + user.getAge());
user.setAge(newAge);
System.out.println("Age after change: " + user.getAge());'''

# ───────── Product discount ─────────

PRODUCT = '''class Product {
    private String title;
    private int price;
    private int discount;

    Product(String title, int price) {
        this.title = title;
        this.price = price;
    }

    String getTitle() {
        return title;
    }

    int getPrice() {
        return price;
    }

    int getDiscount() {
        return discount;
    }

    void setDiscount(int discount) {
        if (discount >= 0 && discount <= 50) {
            this.discount = discount;
        }
    }

    int getFinalPrice() {
        return price - price * discount / 100;
    }
}'''

PRODUCT_MAIN = '''Product product = new Product(title, price);
System.out.println(product.getTitle() + ": " + product.getPrice() + " rub");
for (int i = 0; i < discounts.length; i++) {
    product.setDiscount(discounts[i]);
    System.out.println("Sale " + product.getDiscount() + "%: " + product.getFinalPrice() + " rub");
}'''

# ───────── Playlist ─────────

TRACK = '''class Track {
    private String title;
    private int seconds;

    String getTitle() {
        return title;
    }

    void setTitle(String title) {
        this.title = title;
    }

    int getSeconds() {
        return seconds;
    }

    void setSeconds(int seconds) {
        if (seconds > 0) {
            this.seconds = seconds;
        }
    }

    String getDuration() {
        int rest = seconds % 60;
        if (rest < 10) {
            return seconds / 60 + ":0" + rest;
        }
        return seconds / 60 + ":" + rest;
    }
}'''

TRACK_MAIN = '''Track[] tracks = new Track[titles.length];
for (int i = 0; i < titles.length; i++) {
    tracks[i] = new Track();
    tracks[i].setTitle(titles[i]);
    tracks[i].setSeconds(seconds[i]);
}
int total = 0;
for (int i = 0; i < tracks.length; i++) {
    System.out.println(tracks[i].getTitle() + " (" + tracks[i].getDuration() + ")");
    total += tracks[i].getSeconds();
}
System.out.println("Total: " + total / 60 + " min " + total % 60 + " sec");'''

# ───────── Alarm ─────────

ALARM = '''class Alarm {
    private int hour;
    private int minute;

    int getHour() {
        return hour;
    }

    void setHour(int hour) {
        if (hour >= 0 && hour <= 23) {
            this.hour = hour;
        }
    }

    int getMinute() {
        return minute;
    }

    void setMinute(int minute) {
        if (minute >= 0 && minute <= 59) {
            this.minute = minute;
        }
    }
}'''

ALARM_MAIN = '''Alarm alarm = new Alarm();
alarm.setHour(hour);
alarm.setMinute(minute);
System.out.println("Alarm: " + alarm.getHour() + " h " + alarm.getMinute() + " min");
alarm.setHour(newHour);
alarm.setMinute(newMinute);
System.out.println("New alarm: " + alarm.getHour() + " h " + alarm.getMinute() + " min");'''

# ───────── Thermometer ─────────

THERMOMETER = '''class Thermometer {
    private int celsius;

    int getCelsius() {
        return celsius;
    }

    void setCelsius(int celsius) {
        if (celsius >= -273) {
            this.celsius = celsius;
        }
    }

    int getFahrenheit() {
        return celsius * 9 / 5 + 32;
    }
}'''

THERMOMETER_MAIN = '''Thermometer thermometer = new Thermometer();
for (int i = 0; i < values.length; i++) {
    thermometer.setCelsius(values[i]);
    System.out.println(city + ": " + thermometer.getCelsius() + " C = " + thermometer.getFahrenheit() + " F");
}'''

# ───────── Cart ─────────

ITEM = '''class Item {
    private String name;
    private int price;
    private int quantity;

    Item(String name, int price) {
        this.name = name;
        this.price = price;
        this.quantity = 1;
    }

    String getName() {
        return name;
    }

    int getQuantity() {
        return quantity;
    }

    void setQuantity(int quantity) {
        if (quantity >= 1 && quantity <= 10) {
            this.quantity = quantity;
        }
    }

    int getTotal() {
        return price * quantity;
    }
}'''

CART_MAIN = '''Item[] items = new Item[names.length];
for (int i = 0; i < names.length; i++) {
    items[i] = new Item(names[i], prices[i]);
    items[i].setQuantity(quantities[i]);
}
int sum = 0;
Item top = items[0];
for (int i = 0; i < items.length; i++) {
    System.out.println(items[i].getName() + " x" + items[i].getQuantity() + ": " + items[i].getTotal() + " rub");
    sum += items[i].getTotal();
    if (items[i].getTotal() > top.getTotal()) {
        top = items[i];
    }
}
System.out.println("Cart: " + sum + " rub");
System.out.println("Most expensive: " + top.getName());'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-getset-user-age", title="Профиль пользователя",
        given=[("String", "name"), ("int", "age"), ("int", "newAge")],
        variants=[{"name": '"Anya"', "age": "12", "newAge": "13"},
                  {"name": '"Igor"', "age": "35", "newAge": "150"},
                  {"name": '"Mila"', "age": "8", "newAge": "0"}],
        hidden=[{"name": '"Yan"', "age": "40", "newAge": "120"},
                {"name": '"Ksusha"', "age": "20", "newAge": "121"},
                {"name": '"Borya"', "age": "70", "newAge": "1"},
                {"name": '"Eva"', "age": "15", "newAge": "-5"}],
        intro="На сайте у каждого пользователя есть профиль с именем и возрастом. Поля профиля закрыты, а читать и менять "
              "их можно только через специальные методы — геттеры и сеттеры. Возраст должен быть от 1 до 120 лет: "
              "другое число — явная опечатка, и сайт её не сохраняет. Имя и возраст записаны в полях `name` и `age`, "
              "а в поле `newAge` — возраст, который пользователь потом ввёл в настройках.",
        steps=["Ниже класса `Solution` создай класс `User` (без `public`) с закрытыми полями `private String name` и `private int age`.",
               "Добавь геттеры и сеттеры: `String getName()` и `void setName(String name)`, `int getAge()` и `void setAge(int age)`. "
               "Геттер просто возвращает значение поля, сеттер записывает в поле новое значение.",
               "В `setAge` добавь проверку: возраст записывается, только если он от 1 до 120 включительно, иначе остаётся прежним.",
               "В `main` создай `new User()`, задай имя и возраст сеттерами из `name` и `age` и выведи через геттеры строки вида "
               "`Name: Anya` и `Age: 12`. Потом вызови `setAge(newAge)` и выведи строку вида `Age after change: 13`."],
        hint="Параметр сеттера обычно называют так же, как поле, поэтому внутри пиши `this.age = age;`. А проверку ставь "
             "перед присваиванием: если число не подходит, сеттер просто ничего не записывает.",
        solution=USER_MAIN,
        classes=USER,
        wrong=[("setAge без проверки — возраст 150 или 0 тоже записывается",
                USER_MAIN, USER.replace("        if (age >= 1 && age <= 120) {\n            this.age = age;\n        }",
                                        "        this.age = age;")),
               ("в setAge присваивает параметр самому себе (`age = age;`) — возраст так и остаётся 0",
                USER_MAIN, USER.replace("            this.age = age;", "            age = age;"))],
        constructs=["class"],
        checks=find_class("User")
               + need_private_field("User", "name", "String", "имя читают и меняют через getName и setName")
               + need_private_field("User", "age", "int", "возраст читают и меняют через getAge и setAge")
               + need_getter("User", "String", "name")
               + need_setter("User", "String", "name")
               + need_getter("User", "int", "age")
               + need_setter("User", "int", "age", ", и в нём живёт проверка возраста")
               + need_after_calls("", "", [("setAge", "int", "30")], "age", "30",
                                  "Сеттер setAge должен записывать подходящий возраст в поле объекта: this.age = age;")
               + need_after_calls("", "", [("setAge", "int", "30"), ("setAge", "int", "150"), ("setAge", "int", "0")], "age", "30",
                                  "Проверка возраста должна быть внутри setAge: число меньше 1 или больше 120 сеттер не записывает, и остаётся прежний возраст"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-getset-product-discount", title="Скидка на товар",
        given=[("String", "title"), ("int", "price"), ("int[]", "discounts")],
        variants=[{"title": '"Headphones"', "price": "2000", "discounts": "{10, 70, 25}"},
                  {"title": '"Backpack"', "price": "3000", "discounts": "{60, 50, 5}"},
                  {"title": '"Sneakers"', "price": "4500", "discounts": "{20, -10, 0}"}],
        hidden=[{"title": '"Ball"', "price": "800", "discounts": "{50}"},
                {"title": '"Helmet"', "price": "1500", "discounts": "{51, 49}"},
                {"title": '"Skates"', "price": "6000", "discounts": "{}"},
                {"title": '"Scooter"', "price": "9900", "discounts": "{33, -1, 100}"}],
        intro="Менеджер интернет-магазина подбирает скидку для товара `title` с ценой `price` руб. и по очереди пробует "
              "значения из массива `discounts`. Скидка может быть только от 0 до 50 процентов: другое значение магазин "
              "не принимает, и остаётся прежняя скидка.",
        steps=["Ниже класса `Solution` создай класс `Product` (без `public`) с закрытыми полями `private String title`, "
               "`private int price` и `private int discount` и конструктором `Product(String title, int price)`. "
               "Скидка нового товара — 0.",
               "Добавь геттеры `getTitle()`, `getPrice()` и `getDiscount()`, а для скидки — сеттер `void setDiscount(int discount)`, "
               "который записывает значение, только если оно от 0 до 50 включительно.",
               "Добавь метод `int getFinalPrice()`, который возвращает цену со скидкой: `price - price * discount / 100`. "
               "Это тоже геттер, только значение он не хранит в поле, а вычисляет.",
               "В `main` создай товар и выведи строку вида `Headphones: 2000 rub`. Затем для каждого числа из `discounts` вызови "
               "`setDiscount` и выведи строку вида `Sale 10%: 1800 rub` — с текущей скидкой и ценой, полученными через геттеры."],
        hint="Сеттер — единственная дверь к полю `discount`, поэтому проверка в нём защищает от любой неправильной скидки. "
             "Если число не подходит, сеттер ничего не меняет — и геттер вернёт прежнюю скидку.",
        solution=PRODUCT_MAIN,
        classes=PRODUCT,
        wrong=[("сеттер принимает любую скидку — 70% тоже записывается",
                PRODUCT_MAIN, PRODUCT.replace("        if (discount >= 0 && discount <= 50) {\n            this.discount = discount;\n        }",
                                              "        this.discount = discount;")),
               ("цена со скидкой считается через `discount / 100` — целочисленное деление даёт 0, и скидка не действует",
                PRODUCT_MAIN, PRODUCT.replace("price * discount / 100", "price * (discount / 100)"))],
        constructs=["class"],
        checks=find_class("Product")
               + need_private_field("Product", "title", "String", "название читают через getTitle")
               + need_private_field("Product", "price", "int", "цену читают через getPrice")
               + need_private_field("Product", "discount", "int", "скидку меняют только через setDiscount с проверкой")
               + need_constructor("Product", ["String title", "int price"], "он задаёт название и цену нового товара")
               + need_getter("Product", "String", "title")
               + need_getter("Product", "int", "price")
               + need_getter("Product", "int", "discount")
               + need_setter("Product", "int", "discount", ", и в нём живёт проверка от 0 до 50")
               + need_method("Product", "int", "getFinalPrice", [], "он вычисляет цену со скидкой")
               + need_after_calls("String.class, int.class", '"Test", 1000', [("setDiscount", "int", "20")], "discount", "20",
                                  "Сеттер setDiscount должен записывать подходящую скидку в поле объекта: this.discount = discount;")
               + need_after_calls("String.class, int.class", '"Test", 1000', [("setDiscount", "int", "20"), ("setDiscount", "int", "70"), ("setDiscount", "int", "-5")],
                                  "discount", "20", "Проверка скидки должна быть внутри setDiscount: число меньше 0 или больше 50 сеттер не записывает, и остаётся прежняя скидка"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-getset-playlist", title="Плейлист",
        given=[("String[]", "titles"), ("int[]", "seconds")],
        variants=[{"titles": '{"Morning", "Road", "Sunset"}', "seconds": "{185, 242, 300}"},
                  {"titles": '{"Rhythm", "Echo"}', "seconds": "{59, -20}"},
                  {"titles": '{"Storm", "Silence", "Flight", "Final"}', "seconds": "{600, 0, 61, 3599}"}],
        hidden=[{"titles": '{"One"}', "seconds": "{9}"},
                {"titles": '{"Alpha", "Beta", "Gamma"}', "seconds": "{60, 120, 3600}"},
                {"titles": '{"Dream", "Rain"}', "seconds": "{-5, 125}"},
                {"titles": '{"Notes"}', "seconds": "{610}"}],
        intro="Ты собираешь плейлист. Названия треков записаны в массиве `titles`, их длина в секундах — в массиве `seconds` "
              "под теми же номерами. Иногда длина записана с ошибкой (0 или меньше): такую длину трек не принимает "
              "и остаётся с нулевой длиной.",
        steps=["Ниже класса `Solution` создай класс `Track` (без `public`) с закрытыми полями `private String title` и `private int seconds`.",
               "Добавь геттеры и сеттеры: `getTitle()` и `setTitle(String title)`, `getSeconds()` и `setSeconds(int seconds)`. "
               "Сеттер длины записывает значение, только если оно больше 0.",
               "Добавь метод `String getDuration()`, который возвращает длину в виде «минуты:секунды», где секунды всегда "
               "из двух цифр: 185 секунд — это `3:05`, 600 секунд — `10:00`.",
               "В `main` создай массив треков: для каждого названия — `new Track()` и два сеттера. Потом для каждого трека "
               "выведи строку вида `Morning (3:05)`.",
               "Последней строкой выведи строку вида `Total: 12 min 7 sec` — общую длину всех треков (сумму `getSeconds()`), "
               "разделённую на минуты и секунды."],
        hint="Минуты — это `seconds / 60`, секунды — `seconds % 60`. Если секунд меньше 10, перед ними нужно дописать `0`, "
             "иначе вместо `3:05` получится `3:5`.",
        solution=TRACK_MAIN,
        classes=TRACK,
        wrong=[("не дописывает ноль перед секундами — получается 3:5 вместо 3:05",
                TRACK_MAIN, TRACK.replace('return seconds / 60 + ":0" + rest;', 'return seconds / 60 + ":" + rest;')),
               ("сеттер длины принимает и отрицательные числа",
                TRACK_MAIN, TRACK.replace("        if (seconds > 0) {\n            this.seconds = seconds;\n        }",
                                          "        this.seconds = seconds;"))],
        constructs=["class"],
        checks=find_class("Track")
               + need_private_field("Track", "title", "String", "название читают и меняют через getTitle и setTitle")
               + need_private_field("Track", "seconds", "int", "длину читают и меняют через getSeconds и setSeconds")
               + need_getter("Track", "String", "title")
               + need_setter("Track", "String", "title")
               + need_getter("Track", "int", "seconds")
               + need_setter("Track", "int", "seconds", ", и в нём живёт проверка длины")
               + need_method("Track", "String", "getDuration", [], "он возвращает длину в виде минуты:секунды")
               + need_after_calls("", "", [("setSeconds", "int", "100")], "seconds", "100",
                                  "Сеттер setSeconds должен записывать длину больше 0 в поле объекта: this.seconds = seconds;")
               + need_after_calls("", "", [("setSeconds", "int", "100"), ("setSeconds", "int", "-5"), ("setSeconds", "int", "0")], "seconds", "100",
                                  "Проверка длины должна быть внутри setSeconds: 0 и отрицательные числа сеттер не записывает, и остаётся прежняя длина"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-getset-alarm-clock", title="Будильник",
        given=[("int", "hour"), ("int", "minute"), ("int", "newHour"), ("int", "newMinute")],
        variants=[{"hour": "7", "minute": "30", "newHour": "6", "newMinute": "45"},
                  {"hour": "8", "minute": "15", "newHour": "25", "newMinute": "0"},
                  {"hour": "6", "minute": "0", "newHour": "9", "newMinute": "60"}],
        hidden=[{"hour": "23", "minute": "59", "newHour": "24", "newMinute": "-1"},
                {"hour": "0", "minute": "5", "newHour": "-3", "newMinute": "59"},
                {"hour": "12", "minute": "40", "newHour": "0", "newMinute": "0"},
                {"hour": "5", "minute": "70", "newHour": "10", "newMinute": "10"}],
        intro="В телефоне будильник ставят часами и минутами. Часы бывают от 0 до 23, минуты — от 0 до 59; если ввести "
              "что-то другое, будильник оставляет прежнее значение. Сначала будильник ставят на `hour` ч `minute` мин, "
              "потом пробуют перевести на `newHour` ч `newMinute` мин.",
        steps=["Ниже класса `Solution` создай класс `Alarm` (без `public`) с закрытыми полями `private int hour` и `private int minute`.",
               "Добавь геттеры `int getHour()` и `int getMinute()` и сеттеры `void setHour(int hour)` и `void setMinute(int minute)`.",
               "Сеттер часов записывает значение, только если оно от 0 до 23 включительно, сеттер минут — от 0 до 59 включительно.",
               "В `main` создай `new Alarm()`, поставь время сеттерами из `hour` и `minute` и выведи строку вида "
               "`Alarm: 7 h 30 min`. Потом вызови сеттеры с `newHour` и `newMinute` и выведи строку вида `New alarm: 6 h 45 min`. "
               "Числа бери через геттеры."],
        hint="Каждый сеттер проверяет только своё поле: если час неправильный, а минуты правильные, поменяются только минуты.",
        solution=ALARM_MAIN,
        classes=ALARM,
        wrong=[("setMinute без проверки — 60 минут тоже записываются",
                ALARM_MAIN, ALARM.replace("        if (minute >= 0 && minute <= 59) {\n            this.minute = minute;\n        }",
                                          "        this.minute = minute;")),
               ("в setHour граница на единицу больше — 24 часа тоже принимаются",
                ALARM_MAIN, ALARM.replace("hour <= 23", "hour <= 24"))],
        constructs=["class"],
        checks=find_class("Alarm")
               + need_private_field("Alarm", "hour", "int", "часы читают и меняют через getHour и setHour")
               + need_private_field("Alarm", "minute", "int", "минуты читают и меняют через getMinute и setMinute")
               + need_getter("Alarm", "int", "hour")
               + need_setter("Alarm", "int", "hour", ", и в нём живёт проверка от 0 до 23")
               + need_getter("Alarm", "int", "minute")
               + need_setter("Alarm", "int", "minute", ", и в нём живёт проверка от 0 до 59")
               + need_after_calls("", "", [("setHour", "int", "7"), ("setHour", "int", "24"), ("setHour", "int", "-1")], "hour", "7",
                                  "Проверка часов должна быть внутри setHour: число меньше 0 или больше 23 сеттер не записывает")
               + need_after_calls("", "", [("setMinute", "int", "30"), ("setMinute", "int", "60"), ("setMinute", "int", "-1")], "minute", "30",
                                  "Проверка минут должна быть внутри setMinute: число меньше 0 или больше 59 сеттер не записывает"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-getset-thermometer", title="Градусы Цельсия и Фаренгейта",
        given=[("String", "city"), ("int[]", "values")],
        variants=[{"city": '"Kazan"', "values": "{20, -300, 35}"},
                  {"city": '"Sochi"', "values": "{25, 10, -5}"},
                  {"city": '"Murmansk"', "values": "{-500, -20, 0}"}],
        hidden=[{"city": '"Omsk"', "values": "{}"},
                {"city": '"Tula"', "values": "{-273, -274}"},
                {"city": '"Perm"', "values": "{100}"},
                {"city": '"Ufa"', "values": "{-1000, 15, -40}"}],
        intro="Приложение погоды для туристов показывает температуру в городе `city` сразу в градусах Цельсия и Фаренгейта. "
              "Новые значения в градусах Цельсия приходят по очереди из массива `values`. Ниже -273 градусов температуры "
              "не бывает — такое значение термометр не принимает и показывает прежнее.",
        steps=["Ниже класса `Solution` создай класс `Thermometer` (без `public`) с закрытым полем `private int celsius`.",
               "Добавь геттер `int getCelsius()` и сеттер `void setCelsius(int celsius)`, который записывает значение, "
               "только если оно не меньше -273.",
               "Добавь метод `int getFahrenheit()`: он не хранит значение в поле, а вычисляет его — `celsius * 9 / 5 + 32`.",
               "В `main` создай термометр и для каждого числа из `values` вызови `setCelsius`, а потом выведи строку вида "
               "`Kazan: 20 C = 68 F` — с названием города и значениями из геттеров."],
        hint="Геттеру не обязательно иметь своё поле: `getFahrenheit()` каждый раз считает ответ по текущему `celsius`. "
             "Порядок действий важен: если сначала разделить 9 на 5, получится 1.",
        solution=THERMOMETER_MAIN,
        classes=THERMOMETER,
        wrong=[("сеттер принимает любое число — -300 градусов тоже записывается",
                THERMOMETER_MAIN, THERMOMETER.replace("        if (celsius >= -273) {\n            this.celsius = celsius;\n        }",
                                                      "        this.celsius = celsius;")),
               ("в формуле сначала делит 9 на 5 — целочисленное деление даёт 1",
                THERMOMETER_MAIN, THERMOMETER.replace("celsius * 9 / 5 + 32", "celsius * (9 / 5) + 32"))],
        constructs=["class"],
        checks=find_class("Thermometer")
               + need_private_field("Thermometer", "celsius", "int", "температуру читают и меняют через getCelsius и setCelsius")
               + need_getter("Thermometer", "int", "celsius")
               + need_setter("Thermometer", "int", "celsius", ", и в нём живёт проверка на -273")
               + need_method("Thermometer", "int", "getFahrenheit", [], "он вычисляет температуру по Фаренгейту")
               + need_after_calls("", "", [("setCelsius", "int", "12"), ("setCelsius", "int", "-280")], "celsius", "12",
                                  "Проверка должна быть внутри setCelsius: значение ниже -273 сеттер не записывает, и остаётся прежнее"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-getset-shop-cart", title="Корзина покупок",
        given=[("String[]", "names"), ("int[]", "prices"), ("int[]", "quantities")],
        variants=[{"names": '{"Tea", "Honey", "Jam"}', "prices": "{200, 450, 300}", "quantities": "{2, 1, 3}"},
                  {"names": '{"Bread", "Cheese"}', "prices": "{60, 500}", "quantities": "{12, 0}"},
                  {"names": '{"Milk", "Eggs", "Rice", "Salt"}', "prices": "{90, 120, 110, 30}", "quantities": "{4, 3, -2, 10}"}],
        hidden=[{"names": '{"Juice"}', "prices": "{150}", "quantities": "{11}"},
                {"names": '{"Apples", "Pears"}', "prices": "{100, 50}", "quantities": "{1, 2}"},
                {"names": '{"Cake", "Candy", "Cocoa"}', "prices": "{700, 40, 250}", "quantities": "{1, 10, 3}"},
                {"names": '{"Soap", "Towel"}', "prices": "{80, 400}", "quantities": "{5, 0}"}],
        intro="В интернет-магазине в корзину можно положить от 1 до 10 штук одного товара. Если покупатель вводит другое "
              "количество, в корзине остаётся прежнее — у нового товара это 1 штука. Названия товаров записаны в массиве "
              "`names`, цены — в `prices`, введённые количества — в `quantities`, всё под одними номерами.",
        steps=["Ниже класса `Solution` создай класс `Item` (без `public`) с закрытыми полями `private String name`, "
               "`private int price` и `private int quantity` и конструктором `Item(String name, int price)`, который "
               "сохраняет название и цену и ставит количество 1.",
               "Добавь геттеры `getName()` и `getQuantity()` и сеттер `void setQuantity(int quantity)`, который записывает "
               "значение, только если оно от 1 до 10 включительно. Добавь метод `int getTotal()` — цена, умноженная на количество.",
               "В `main` создай массив товаров: для каждого названия — `new Item(names[i], prices[i])`, потом `setQuantity(quantities[i])`.",
               "Для каждого товара выведи строку вида `Tea x2: 400 rub`. Затем выведи строку вида `Cart: 1750 rub` — сумму "
               "`getTotal()` всех товаров, и `Most expensive: Jam` — товар с самой большой суммой (при равенстве — тот, что раньше)."],
        hint="Количество по умолчанию задай в конструкторе: тогда, если сеттер отклонит неправильное число, у товара останется 1. "
             "Для самого дорогого товара заведи переменную `Item top = items[0];` и сравнивай с ним остальные.",
        solution=CART_MAIN,
        classes=ITEM,
        wrong=[("сеттер принимает любое количество — 12 и 0 тоже записываются",
                CART_MAIN, ITEM.replace("        if (quantity >= 1 && quantity <= 10) {\n            this.quantity = quantity;\n        }",
                                        "        this.quantity = quantity;")),
               ("конструктор не ставит количество 1 — после отклонённого числа в корзине 0 штук",
                CART_MAIN, ITEM.replace("        this.quantity = 1;\n", ""))],
        constructs=["class"],
        checks=find_class("Item")
               + need_private_field("Item", "name", "String", "название читают через getName")
               + need_private_field("Item", "price", "int", "цену нельзя менять снаружи класса")
               + need_private_field("Item", "quantity", "int", "количество меняют только через setQuantity с проверкой")
               + need_constructor("Item", ["String name", "int price"], "он задаёт название и цену и ставит количество 1")
               + need_getter("Item", "String", "name")
               + need_getter("Item", "int", "quantity")
               + need_setter("Item", "int", "quantity", ", и в нём живёт проверка от 1 до 10")
               + need_method("Item", "int", "getTotal", [], "он вычисляет стоимость товара в корзине")
               + need_after_calls("String.class, int.class", '"Test", 100', [("setQuantity", "int", "0")], "quantity", "1",
                                  "У нового товара количество 1, и неправильное число сеттер не записывает — задай 1 в конструкторе")
               + need_after_calls("String.class, int.class", '"Test", 100', [("setQuantity", "int", "4"), ("setQuantity", "int", "11")], "quantity", "4",
                                  "Проверка количества должна быть внутри setQuantity: число меньше 1 или больше 10 сеттер не записывает"),
    ),
]
