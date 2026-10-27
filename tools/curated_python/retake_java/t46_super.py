"""SUPER_BASIC — «Ключевое слово super» (Java). Taught before: everything up to classes, objects, constructors, this,
private fields, getters/setters, static, inheritance, overriding, polymorphism, interfaces. Here: the parent has only a
constructor with parameters and private fields, so the child's constructor must call super(...) first to let the parent
fill its part (and run its code, e.g. a shared counter); an overriding method extends the parent's result through
super.method(). Not yet: collections, exceptions. The student writes the classes after Solution."""
from java_tasks import JavaOutputTask

SKILL = "SUPER_BASIC"


def exist(*names: str) -> str:
    listed = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " и " + names[-1]
    what = "класс" if len(names) == 1 else "классы"
    condition = " && ".join(f'cls("{n}") != null' for n in names)
    return (f'need({condition}, "Опиши {what} {listed} отдельно — ниже класса Solution, после его закрывающей скобки, '
            f'и без слова public");\n')


def extends(child: str, parent: str) -> str:
    return (f'need(cls("{child}").getSuperclass() == cls("{parent}"), '
            f'"Сделай {child} наследником {parent}: напиши class {child} extends {parent}");\n')


def no_empty_constructor(parent: str, signature: str, call: str) -> str:
    return (f'need(Arrays.stream(cls("{parent}").getDeclaredConstructors()).noneMatch(k -> k.getParameterCount() == 0), '
            f'"Оставь в {parent} только конструктор {signature}, без пустого: наследник должен передать данные родителю через {call}");\n')


def private_fields(owner: str, *fields: str) -> str:
    variable = f"private{owner}"
    listed = " и ".join(fields)
    probe = " && ".join(f'Modifier.isPrivate(cls("{owner}").getDeclaredField("{f}").getModifiers())' for f in fields)
    return (f'boolean {variable};\n'
            f'try {{ {variable} = {probe}; }} catch (NoSuchFieldException e) {{ {variable} = false; }}\n'
            f'need({variable}, "Объяви в {owner} закрытые поля {listed} (private): их заполняет и читает только сам {owner}, '
            f'а наследник пользуется super");\n')


def declares(cls_name: str, method: str) -> str:
    return f'Arrays.stream(cls("{cls_name}").getDeclaredMethods()).anyMatch(m -> m.getName().equals("{method}"))'


PARCEL = """\
class Parcel {
    private String city;
    private int weight;

    Parcel(String city, int weight) {
        this.city = city;
        this.weight = weight;
    }

    String info() {
        return "to " + city + ", " + weight + " kg";
    }
}

class ExpressParcel extends Parcel {
    private int hours;

    ExpressParcel(String city, int weight, int hours) {
        super(city, weight);
        this.hours = hours;
    }

    int getHours() {
        return hours;
    }
}"""

PARCEL_MAIN = """\
Parcel usual = new Parcel(city, weight);
ExpressParcel fast = new ExpressParcel(city, weight, hours);
System.out.println("Usual: " + usual.info());
System.out.println("Express: " + fast.info() + ", in " + fast.getHours() + " hours");"""

# A beginner's way round super: an empty parent constructor, open fields, and the child fills them itself.
PARCEL_NO_SUPER = (PARCEL.replace("    private String city;\n    private int weight;\n\n    Parcel(String city, int weight) {",
                                  "    String city;\n    int weight;\n\n    Parcel() {\n    }\n\n    Parcel(String city, int weight) {")
                   .replace("        super(city, weight);\n", "        this.city = city;\n        this.weight = weight;\n"))

CONCERT = """\
class Guest {
    static int taken = 0;
    private String name;
    private int seat;

    Guest(String name) {
        this.name = name;
        taken++;
        seat = taken;
    }

    String info() {
        return name + ": seat " + seat;
    }
}

class VipGuest extends Guest {
    private String gift;

    VipGuest(String name, String gift) {
        super(name);
        this.gift = gift;
    }

    @Override
    String info() {
        return super.info() + ", gift: " + gift;
    }
}"""

CONCERT_MAIN = """\
for (String name : guests) {
    Guest guest = new Guest(name);
    System.out.println(guest.info());
}
VipGuest vip = new VipGuest(star, gift);
System.out.println(vip.info());
System.out.println("Seats taken: " + Guest.taken);"""

HOTEL = """\
class Stay {
    private String guest;
    private int nights;

    Stay(String guest, int nights) {
        this.guest = guest;
        this.nights = nights;
    }

    int price() {
        return nights * 2000;
    }

    String info() {
        return guest + ", nights: " + nights;
    }
}

class SpaStay extends Stay {
    private int visits;

    SpaStay(String guest, int nights, int visits) {
        super(guest, nights);
        this.visits = visits;
    }

    @Override
    int price() {
        return super.price() + 700 * visits;
    }

    @Override
    String info() {
        return super.info() + ", spa visits: " + visits;
    }
}"""

HOTEL_MAIN = """\
Stay[] stays = {new Stay(first, nights), new SpaStay(second, nights, visits)};
int total = 0;
for (Stay stay : stays) {
    System.out.println(stay.info() + " - " + stay.price() + " rub");
    total += stay.price();
}
System.out.println("Total: " + total + " rub");"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-super-rt-express-parcel", title="Срочная посылка",
        given=[("String", "city"), ("int", "weight"), ("int", "hours")],
        variants=[{"city": '"Kazan"', "weight": "3", "hours": "24"},
                  {"city": '"Sochi"', "weight": "12", "hours": "48"},
                  {"city": '"Omsk"', "weight": "7", "hours": "36"}],
        hidden=[{"city": '"Tver"', "weight": "1", "hours": "6"},
                {"city": '"Murmansk"', "weight": "25", "hours": "72"},
                {"city": '"Ufa"', "weight": "9", "hours": "12"}],
        intro="Почта отправляет посылки: у каждой есть город, куда она едет, и вес. Срочная посылка — тоже посылка, "
              "только у неё есть ещё срок доставки в часах. Город и вес пусть хранит класс-родитель, а срочная "
              "посылка добавит только свой срок. Данные — в полях `city`, `weight` и `hours`.",
        steps=["Ниже класса `Solution` (после его закрывающей скобки) опиши класс `Parcel` без слова `public`. Дай ему "
               "закрытые поля `private String city` и `private int weight`, конструктор `Parcel(String city, int weight)`, "
               "который их заполняет, и метод `String info()`, который возвращает строку вида `to Kazan, 3 kg`.",
               "Опиши класс `ExpressParcel` — наследник `Parcel` — с полем `private int hours` и конструктором "
               "`ExpressParcel(String city, int weight, int hours)`. Первой строкой конструктора вызови "
               "`super(city, weight);` — родитель сам заполнит город и вес, — а потом сохрани срок.",
               "Добавь в `ExpressParcel` геттер `int getHours()`.",
               "В `main` создай обычную посылку `new Parcel(city, weight)` и срочную `new ExpressParcel(city, weight, hours)` "
               "и выведи две строки: `Usual: ` и `info()` обычной посылки, затем `Express: `, `info()` срочной, "
               "`, in `, срок и ` hours` — например `Express: to Kazan, 3 kg, in 24 hours`."],
        hint="Поля `city` и `weight` закрыты в `Parcel`, поэтому `ExpressParcel` не может записать их сам. "
             "`super(city, weight)` запускает конструктор родителя для того же объекта, а метод `info()` срочная "
             "посылка получает от родителя по наследству.",
        solution=PARCEL_MAIN, classes=PARCEL,
        wrong=[("забыл сохранить срок в конструкторе срочной посылки — печатается 0 часов",
                PARCEL_MAIN, PARCEL.replace("        this.hours = hours;\n", "")),
               ("добавил в Parcel пустой конструктор и заполняет поля в ExpressParcel сам, без super",
                PARCEL_MAIN, PARCEL_NO_SUPER)],
        constructs=["class"],
        checks=exist("Parcel", "ExpressParcel")
        + extends("ExpressParcel", "Parcel")
        + no_empty_constructor("Parcel", "Parcel(String city, int weight)", "super(city, weight)")
        + private_fields("Parcel", "city", "weight"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-super-rt-concert-seats", title="Места на концерте",
        given=[("String[]", "guests"), ("String", "star"), ("String", "gift")],
        variants=[{"guests": '{"Anya", "Boris", "Vika"}', "star": '"Lena"', "gift": '"poster"'},
                  {"guests": '{"Oleg", "Dima"}', "star": '"Sveta"', "gift": '"t-shirt"'},
                  {"guests": '{"Ira", "Kostya", "Nina", "Pavel", "Rita"}', "star": '"Timur"', "gift": '"cap"'}],
        hidden=[{"guests": "{}", "star": '"Gleb"', "gift": '"badge"'},
                {"guests": '{"Zoya"}', "star": '"Artem"', "gift": '"mug"'},
                {"guests": '{"Yura", "Marat", "Alina", "Egor"}', "star": '"Polina"', "gift": '"sticker"'}],
        intro="На маленький концерт гости приходят по одному, и каждый получает следующее свободное место: первый — "
              "место 1, второй — место 2 и так далее. VIP-гость — тоже гость, он занимает место в общей очереди, "
              "но ещё получает подарок. Имена обычных гостей записаны в массиве `guests`, имя VIP-гостя — в `star`, "
              "подарок — в `gift`.",
        steps=["Ниже класса `Solution` опиши класс `Guest` (без `public`) со статическим полем `static int taken = 0;` "
               "и закрытыми полями `private String name` и `private int seat`. В конструкторе `Guest(String name)` "
               "сохрани имя, увеличь `taken` на 1 и запиши в `seat` новое значение `taken`. Метод `String info()` "
               "пусть возвращает строку вида `Anya: seat 1`.",
               "Опиши класс `VipGuest` — наследник `Guest` — с полем `private String gift` и конструктором "
               "`VipGuest(String name, String gift)`. Первой строкой в нём вызови `super(name);`, а потом сохрани "
               "подарок. Счётчик `taken` в `VipGuest` сам не трогай — место выдаёт родитель.",
               "Переопредели в `VipGuest` метод `String info()` (с `@Override`): пусть он берёт строку родителя через "
               "`super.info()` и дописывает к ней `, gift: poster` — с подарком из поля.",
               "В `main` для каждого имени из `guests` создай объект `Guest` и выведи его `info()`. Потом создай "
               "`VipGuest vip = new VipGuest(star, gift);`, выведи `vip.info()` и последней строкой — "
               "`Seats taken: 4`, число возьми из `Guest.taken`."],
        hint="`super(name)` запускает конструктор `Guest` и для VIP-гостя — вместе с выдачей места. Если увеличить "
             "`taken` ещё и в `VipGuest`, одно место пропадёт зря, и счёт занятых мест будет неверным.",
        solution=CONCERT_MAIN, classes=CONCERT,
        wrong=[("после super(name) ещё раз увеличивает taken в VipGuest — занятых мест на одно больше",
                CONCERT_MAIN, CONCERT.replace("        super(name);\n", "        super(name);\n        taken++;\n")),
               ("в info VIP-гостя не вызывает super.info() — пропадают имя и место",
                CONCERT_MAIN, CONCERT.replace('return super.info() + ", gift: " + gift;', 'return "gift: " + gift;'))],
        constructs=["class", "for"],
        checks=exist("Guest", "VipGuest")
        + extends("VipGuest", "Guest")
        + no_empty_constructor("Guest", "Guest(String name)", "super(name)")
        + private_fields("Guest", "name", "seat")
        + f'need({declares("VipGuest", "info")}, "Переопредели в VipGuest метод String info() с пометкой @Override и допиши в нём подарок к super.info()");\n',
        reset='setStatic("Guest", "taken", 0);',
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-super-rt-hotel-spa", title="Гостиница со спа",
        given=[("String", "first"), ("String", "second"), ("int", "nights"), ("int", "visits")],
        variants=[{"first": '"Anya"', "second": '"Boris"', "nights": "3", "visits": "2"},
                  {"first": '"Kira"', "second": '"Maxim"', "nights": "1", "visits": "4"},
                  {"first": '"Denis"', "second": '"Olga"', "nights": "5", "visits": "1"}],
        hidden=[{"first": '"Lev"', "second": '"Mila"', "nights": "2", "visits": "0"},
                {"first": '"Fedor"', "second": '"Inna"', "nights": "7", "visits": "6"},
                {"first": '"Sasha"', "second": '"Tanya"', "nights": "4", "visits": "3"}],
        intro="Двое друзей, `first` и `second`, прожили в гостинице по `nights` ночей. Ночь стоит 2000 руб. Второй "
              "взял проживание со спа: каждое посещение спа добавляет 700 руб., а посещений было `visits`. Описание "
              "и цена проживания со спа должны продолжать описание и цену обычного проживания, а не повторять их код.",
        steps=["Ниже класса `Solution` опиши класс `Stay` (без `public`) с закрытыми полями `private String guest` и "
               "`private int nights`, конструктором `Stay(String guest, int nights)`, методом `int price()`, который "
               "возвращает `nights * 2000`, и методом `String info()`, который возвращает строку вида `Anya, nights: 3`.",
               "Опиши класс `SpaStay extends Stay` с полем `private int visits` и конструктором "
               "`SpaStay(String guest, int nights, int visits)`: первой строкой вызови `super(guest, nights);`, "
               "а потом сохрани число посещений.",
               "Переопредели в `SpaStay` (с `@Override`) метод `price()` — цена родителя через `super.price()` плюс "
               "`700 * visits` — и метод `info()` — строка родителя через `super.info()` и дописка `, spa visits: 2`.",
               "В `main` создай массив `Stay[] stays = {{new Stay(first, nights), new SpaStay(second, nights, visits)}};`. "
               "Одним циклом выведи для каждого проживания строку вида `Anya, nights: 3 - 6000 rub` — `info()`, ` - `, "
               "цену и ` rub`, — а последней строкой — сумму обоих, например `Total: 13400 rub`."],
        hint="Поля `guest` и `nights` закрыты в `Stay`, поэтому `SpaStay` не может сам посчитать цену ночей — он "
             "берёт её у родителя через `super.price()`. Без `super.` вызов `price()` внутри `price()` вызывал бы сам "
             "себя бесконечно.",
        solution=HOTEL_MAIN, classes=HOTEL,
        wrong=[("в info проживания со спа не вызывает super.info() — пропадают имя и ночи",
                HOTEL_MAIN, HOTEL.replace('return super.info() + ", spa visits: " + visits;',
                                          'return "spa visits: " + visits;')),
               ("в цене проживания со спа забыл цену родителя — считает только спа",
                HOTEL_MAIN, HOTEL.replace("return super.price() + 700 * visits;", "return 700 * visits;"))],
        constructs=["class", "for"],
        checks=exist("Stay", "SpaStay")
        + extends("SpaStay", "Stay")
        + no_empty_constructor("Stay", "Stay(String guest, int nights)", "super(guest, nights)")
        + private_fields("Stay", "guest", "nights")
        + f'need({declares("SpaStay", "price")} && {declares("SpaStay", "info")}, "Переопредели в SpaStay методы price() и info() с пометкой @Override и опирайся в них на super");\n',
    ),
]
