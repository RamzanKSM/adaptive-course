"""BASIC_CODE_READING — «Вывод в консоль» (Java). Taught before: nothing — this is the first topic: System.out.println
and System.out.print (the difference: println ends the line), text in quotes is printed as is, a name without quotes
prints the value of a field of the starter. Not yet: declaring own variables, assignment, arithmetic, string operations
(no `+` between strings — a line is assembled from several print calls), conditions, loops."""
from java_tasks import JavaOutputTask

SKILL = "BASIC_CODE_READING"


def _code(*lines: str) -> str:
    return "\n".join(lines)


def _change(code: str, old: str, new: str, nth: int = 1) -> str:
    """The code with the nth line equal to `old` replaced by `new` (a one-line mistake)."""
    lines = code.split("\n")
    found = [i for i, line in enumerate(lines) if line == old]
    assert len(found) >= nth, f"no line {old!r}"
    lines[found[nth - 1]] = new
    return "\n".join(lines)


PIZZA = _code(
    'System.out.println("ORDER READY");',
    'System.out.print("Pizza: ");',
    'System.out.println(pizza);',
    'System.out.print("Size: ");',
    'System.out.print(size);',
    'System.out.println(" cm");',
    'System.out.print("For ");',
    'System.out.println(name);',
)

PARCEL = _code(
    'System.out.print("To: ");',
    'System.out.println(name);',
    'System.out.print(street);',
    'System.out.print(" st. ");',
    'System.out.print(house);',
    'System.out.print("-");',
    'System.out.println(flat);',
    'System.out.println(city);',
)

REPORT = _code(
    'System.out.println("REPORT CARD");',
    'System.out.print("Student: ");',
    'System.out.println(student);',
    'System.out.println("----------");',
    'System.out.print("Math: ");',
    'System.out.print(math);',
    'System.out.print(" | Physics: ");',
    'System.out.println(physics);',
    'System.out.print("English: ");',
    'System.out.println(english);',
    'System.out.println("----------");',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-out-rt-pizza-order", title="Заказ в пиццерии",
        given=[("String", "pizza"), ("int", "size"), ("String", "name")],
        variants=[{"pizza": '"Margherita"', "size": "30", "name": '"Anya"'},
                  {"pizza": '"Pepperoni"', "size": "40", "name": '"Boris"'},
                  {"pizza": '"Hawaiian"', "size": "25", "name": '"Lena"'}],
        hidden=[{"pizza": '"Cheese"', "size": "35", "name": '"Oleg"'},
                {"pizza": '"Veggie"', "size": "20", "name": '"Timur"'},
                {"pizza": '"Margherita"', "size": "40", "name": '"Kate"'}],
        intro="В пиццерии на экране над кассой показывают готовый заказ. Название пиццы записано в поле `pizza`, "
              "её размер в сантиметрах — в поле `size`, имя покупателя — в поле `name`.",
        steps=["Первой строкой выведи `ORDER READY`.",
               "Второй строкой — `Pizza: ` и значение `pizza`, например `Pizza: Margherita`.",
               "Третьей — `Size: `, значение `size` и ` cm`, например `Size: 30 cm`.",
               "Четвёртой — `For ` и значение `name`, например `For Anya`.",
               "Части одной строки выводи через `System.out.print`, а последнюю часть строки — через `System.out.println`."],
        hint="Третья строка собирается из трёх частей: `\"Size: \"`, `size` и `\" cm\"` с пробелом впереди. "
             "Имя поля пиши без кавычек — тогда напечатается его значение.",
        solution=PIZZA,
        wrong=[("имя поля в кавычках: печатает слово name вместо имени",
                _change(PIZZA, 'System.out.println(name);', 'System.out.println("name");')),
               ("размер выведен через println: слово cm уезжает на следующую строку",
                _change(PIZZA, 'System.out.print(size);', 'System.out.println(size);'))],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-out-rt-parcel-label", title="Наклейка на посылку",
        given=[("String", "name"), ("String", "street"), ("int", "house"), ("int", "flat"), ("String", "city")],
        variants=[{"name": '"Anya"', "street": '"Lenina"', "house": "12", "flat": "45", "city": '"Kazan"'},
                  {"name": '"Ivan"', "street": '"Mira"', "house": "7", "flat": "103", "city": '"Perm"'},
                  {"name": '"Olga"', "street": '"Gagarina"', "house": "31", "flat": "8", "city": '"Sochi"'}],
        hidden=[{"name": '"Boris"', "street": '"Pushkina"', "house": "3", "flat": "17", "city": '"Omsk"'},
                {"name": '"Masha"', "street": '"Sadovaya"', "house": "120", "flat": "1", "city": '"Tver"'},
                {"name": '"Anya"', "street": '"Lenina"', "house": "45", "flat": "12", "city": '"Kazan"'}],
        intro="На почте печатают наклейку с адресом для посылки. Имя получателя записано в поле `name`, улица — в поле "
              "`street`, номер дома и квартиры — в полях `house` и `flat`, город — в поле `city`.",
        steps=["Первая строка: `To: ` и имя, например `To: Anya`.",
               "Вторая строка: улица, ` st. ` (пробел, st, точка, пробел), номер дома, дефис `-` и номер квартиры — "
               "например `Lenina st. 12-45`.",
               "Третья строка: город.",
               "Каждую часть строки выводи отдельной командой `System.out.print`, а последнюю часть строки — `System.out.println`."],
        hint="Вторая строка собирается из пяти частей: улица, `\" st. \"`, дом, `\"-\"`, квартира. "
             "Перейти на новую строку нужно только после квартиры. Сначала идёт дом, потом квартира.",
        solution=PARCEL,
        wrong=[("номер дома выведен через println: адрес рвётся посередине",
                _change(PARCEL, 'System.out.print(house);', 'System.out.println(house);')),
               ("дом и квартира перепутаны местами",
                _change(_change(PARCEL, 'System.out.print(house);', 'System.out.print(flat);'),
                        'System.out.println(flat);', 'System.out.println(house);'))],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-out-rt-report-card", title="Табель с оценками",
        given=[("String", "student"), ("int", "math"), ("int", "physics"), ("int", "english")],
        variants=[{"student": '"Anya"', "math": "5", "physics": "4", "english": "5"},
                  {"student": '"Denis"', "math": "3", "physics": "5", "english": "4"},
                  {"student": '"Vika"', "math": "4", "physics": "3", "english": "2"}],
        hidden=[{"student": '"Roma"', "math": "2", "physics": "3", "english": "4"},
                {"student": '"Sveta"', "math": "5", "physics": "5", "english": "3"},
                {"student": '"Anya"', "math": "4", "physics": "5", "english": "5"}],
        intro="Классный руководитель печатает табель с оценками за четверть. Имя ученика записано в поле `student`, "
              "оценки по математике, физике и английскому — в полях `math`, `physics` и `english`.",
        steps=["Первая строка: `REPORT CARD`.",
               "Вторая строка: `Student: ` и имя, например `Student: Anya`.",
               "Третья строка: десять минусов `----------`.",
               "Четвёртая строка: `Math: `, оценка по математике, ` | Physics: ` и оценка по физике — например `Math: 5 | Physics: 4`.",
               "Пятая строка: `English: ` и оценка по английскому, шестая — снова `----------`."],
        hint="В четвёртой строке четыре части: `\"Math: \"`, `math`, `\" | Physics: \"`, `physics`. "
             "Первые три выводи через `System.out.print`, последнюю — через `System.out.println`. Следи за пробелами в кавычках.",
        solution=REPORT,
        wrong=[("подпись физики выведена через println: строка с оценками рвётся посередине",
                _change(REPORT, 'System.out.print(" | Physics: ");', 'System.out.println(" | Physics: ");')),
               ("по английскому выводит оценку по математике",
                _change(REPORT, 'System.out.println(english);', 'System.out.println(math);'))],
    ),
]
