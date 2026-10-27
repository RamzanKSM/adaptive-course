"""VARIABLE_BASIC — «Переменные» (Java). Taught before: System.out.println / System.out.print, printing text in quotes
and the value of a field by its name. This topic: declaring a variable with a type (`int`, `String` — text is only
stored and printed) and an initial value, choosing names, printing a variable's value (no quotes around the name).
Not yet: changing a variable after its declaration (assignment), arithmetic, string operations (no `+` between strings —
a line is assembled from several print calls), conditions, loops."""
from java_tasks import JavaOutputTask

SKILL = "VARIABLE_BASIC"


def _code(*lines: str) -> str:
    return "\n".join(lines)


def _change(code: str, old: str, new: str, nth: int = 1) -> str:
    """The code with the nth line equal to `old` replaced by `new` (a one-line mistake)."""
    lines = code.split("\n")
    found = [i for i, line in enumerate(lines) if line == old]
    assert len(found) >= nth, f"no line {old!r}"
    lines[found[nth - 1]] = new
    return "\n".join(lines)


POOL = _code(
    'String pool = "Dolphin Pool";',
    'int minutes = 45;',
    'System.out.println(pool);',
    'System.out.print("Swimmer: ");',
    'System.out.println(swimmer);',
    'System.out.print("Lane: ");',
    'System.out.println(lane);',
    'System.out.print("Time: ");',
    'System.out.print(minutes);',
    'System.out.println(" min");',
)

BIKE = _code(
    'String color = "green";',
    'int hours = 2;',
    'System.out.print("Bike ");',
    'System.out.print(bike);',
    'System.out.print(" (");',
    'System.out.print(color);',
    'System.out.println(")");',
    'System.out.print(rider);',
    'System.out.print(" takes it at ");',
    'System.out.println(station);',
    'System.out.print("Rent: ");',
    'System.out.print(hours);',
    'System.out.println(" h");',
)

RECIPE = _code(
    'int flour = 200;',
    'int sugar = 50;',
    'String unit = " g";',
    'System.out.print("Recipe: ");',
    'System.out.println(dish);',
    'System.out.print("Flour ");',
    'System.out.print(flour);',
    'System.out.print(unit);',
    'System.out.print(", sugar ");',
    'System.out.print(sugar);',
    'System.out.println(unit);',
    'System.out.print("Ready in ");',
    'System.out.print(minutes);',
    'System.out.println(" min");',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-var-rt-swim-pass", title="Пропуск в бассейн",
        given=[("String", "swimmer"), ("int", "lane")],
        variants=[{"swimmer": '"Anya"', "lane": "3"}, {"swimmer": '"Kirill"', "lane": "6"}, {"swimmer": '"Dasha"', "lane": "1"}],
        hidden=[{"swimmer": '"Oleg"', "lane": "8"}, {"swimmer": '"Polina"', "lane": "2"}, {"swimmer": '"Artur"', "lane": "5"}],
        intro="Бассейн печатает пропуск на одно занятие. Имя пловца записано в поле `swimmer`, номер дорожки — в поле `lane`.",
        steps=["Объяви переменную `String pool` со значением `\"Dolphin Pool\"` и переменную `int minutes` со значением `45`.",
               "Первой строкой выведи значение `pool`.",
               "Второй строкой — `Swimmer: ` и имя, третьей — `Lane: ` и номер дорожки.",
               "Четвёртой — `Time: `, значение `minutes` и ` min`, например `Time: 45 min`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть строки — через `System.out.println`."],
        hint="Переменную объявляют так: тип, имя, `=`, значение и точка с запятой — `int minutes = 45;`. "
             "Чтобы напечатать её значение, пиши имя без кавычек.",
        solution=POOL,
        wrong=[("имя переменной в кавычках: печатает слово pool вместо названия бассейна",
                _change(POOL, 'System.out.println(pool);', 'System.out.println("pool");')),
               ("в строке Lane печатает длительность занятия вместо дорожки",
                _change(POOL, 'System.out.println(lane);', 'System.out.println(minutes);'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-var-rt-bike-rental", title="Прокат велосипеда",
        given=[("int", "bike"), ("String", "rider"), ("String", "station")],
        variants=[{"bike": "17", "rider": '"Anya"', "station": '"Park"'},
                  {"bike": "204", "rider": '"Gleb"', "station": '"Embankment"'},
                  {"bike": "9", "rider": '"Zarina"', "station": '"Museum"'}],
        hidden=[{"bike": "1", "rider": '"Ivan"', "station": '"Station"'},
                {"bike": "350", "rider": '"Nina"', "station": '"Stadium"'},
                {"bike": "42", "rider": '"Park"', "station": '"Anya"'}],
        intro="Пункт проката печатает квитанцию на велосипед. Номер велосипеда записан в поле `bike`, имя клиента — "
              "в поле `rider`, станция проката — в поле `station`. Все велосипеды этой станции зелёные, и выдают их на 2 часа.",
        steps=["Объяви переменную `String color` со значением `\"green\"` и переменную `int hours` со значением `2`.",
               "Первая строка: `Bike `, номер, пробел и открывающая скобка ` (`, цвет и закрывающая скобка `)` — "
               "например `Bike 17 (green)`.",
               "Вторая строка: имя клиента, ` takes it at ` и станция — например `Anya takes it at Park`.",
               "Третья строка: `Rent: `, значение `hours` и ` h` — например `Rent: 2 h`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть строки — через `System.out.println`."],
        hint="Скобки — тоже текст: `\" (\"` и `\")\"` печатаются в кавычках. Цвет и часы берутся из твоих переменных, "
             "номер, имя и станция — из полей.",
        solution=BIKE,
        wrong=[("имя переменной в кавычках: печатает слово color вместо цвета",
                _change(BIKE, 'System.out.print(color);', 'System.out.print("color");')),
               ("имя клиента выведено через println: строка рвётся",
                _change(BIKE, 'System.out.print(rider);', 'System.out.println(rider);'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-var-rt-pancake-recipe", title="Карточка рецепта",
        given=[("String", "dish"), ("int", "minutes")],
        variants=[{"dish": '"Pancakes"', "minutes": "20"}, {"dish": '"Muffins"', "minutes": "35"},
                  {"dish": '"Waffles"', "minutes": "15"}],
        hidden=[{"dish": '"Cookies"', "minutes": "12"}, {"dish": '"Pie"', "minutes": "50"}, {"dish": '"Cake"', "minutes": "40"}],
        intro="Кулинарный сайт печатает карточку рецепта. Название блюда записано в поле `dish`, время готовки в минутах — "
              "в поле `minutes`. Муки и сахара во всех этих рецептах одинаково: 200 г и 50 г.",
        steps=["Объяви переменные `int flour` со значением `200`, `int sugar` со значением `50` и `String unit` со значением "
               "`\" g\"` (пробел и буква g).",
               "Первая строка: `Recipe: ` и название блюда, например `Recipe: Pancakes`.",
               "Вторая строка: `Flour `, значение `flour`, значение `unit`, `, sugar `, значение `sugar` и снова значение "
               "`unit` — получится `Flour 200 g, sugar 50 g`.",
               "Третья строка: `Ready in `, время готовки и ` min` — например `Ready in 20 min`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть строки — через `System.out.println`."],
        hint="Переменную `unit` объявляешь один раз, а печатаешь дважды — после муки и после сахара. "
             "Пробел перед g уже лежит внутри её значения.",
        solution=RECIPE,
        wrong=[("после слова sugar печатает количество муки",
                _change(RECIPE, 'System.out.print(sugar);', 'System.out.print(flour);')),
               ("имя переменной в кавычках: печатает слово unit вместо g",
                _change(RECIPE, 'System.out.println(unit);', 'System.out.println("unit");'))],
        constructs=["assignment"],
    ),
]
