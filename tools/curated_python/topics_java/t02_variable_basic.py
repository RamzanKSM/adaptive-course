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


LIBRARY = _code(
    'String library = "City Library";',
    'int maxBooks = 5;',
    'System.out.println(library);',
    'System.out.print("Reader: ");',
    'System.out.println(reader);',
    'System.out.print("Card: ");',
    'System.out.println(card);',
    'System.out.print("Max books: ");',
    'System.out.println(maxBooks);',
)

PLAYER = _code(
    'String game = "Space Race";',
    'int lives = 3;',
    'System.out.println(game);',
    'System.out.print(nick);',
    'System.out.print(" | level ");',
    'System.out.print(level);',
    'System.out.print(" | lives ");',
    'System.out.println(lives);',
)

FLIGHT = _code(
    'String status = "Boarding";',
    'int terminal = 2;',
    'System.out.print(flight);',
    'System.out.print(" -> ");',
    'System.out.println(city);',
    'System.out.print("Terminal ");',
    'System.out.print(terminal);',
    'System.out.print(", gate ");',
    'System.out.println(gate);',
    'System.out.println(status);',
)

CINEMA = _code(
    'int price = 350;',
    'System.out.print("Film: ");',
    'System.out.println(film);',
    'System.out.print("Row ");',
    'System.out.print(row);',
    'System.out.print(", seat ");',
    'System.out.println(seat);',
    'System.out.print("Price: ");',
    'System.out.print(price);',
    'System.out.println(" rub");',
)

MARATHON = _code(
    'String race = "Kazan Marathon";',
    'int distance = 42;',
    'System.out.print(race);',
    'System.out.print(", ");',
    'System.out.print(distance);',
    'System.out.println(" km");',
    'System.out.print("Runner ");',
    'System.out.print(number);',
    'System.out.print(": ");',
    'System.out.println(name);',
)

HOTEL = _code(
    'String checkIn = "14:00";',
    'String checkOut = "12:00";',
    'System.out.print("Floor ");',
    'System.out.print(floor);',
    'System.out.print(", nights: ");',
    'System.out.println(nights);',
    'System.out.print("Check-in ");',
    'System.out.print(checkIn);',
    'System.out.print(", check-out ");',
    'System.out.println(checkOut);',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-var-library-card", title="Читательский билет",
        given=[("String", "reader"), ("int", "card")],
        variants=[{"reader": '"Anya"', "card": "1024"}, {"reader": '"Boris"', "card": "377"}, {"reader": '"Vika"', "card": "5150"}],
        hidden=[{"reader": '"Oleg"', "card": "12"}, {"reader": '"Kate"', "card": "9001"}, {"reader": '"Timur"', "card": "640"}],
        intro="Библиотека печатает читательский билет. Имя читателя записано в поле `reader`, номер билета — в поле `card`.",
        steps=["Объяви переменную `String library` со значением `\"City Library\"` и переменную `int maxBooks` со значением `5`.",
               "Первой строкой выведи значение `library`.",
               "Дальше три строки: `Reader: ` и имя читателя, `Card: ` и номер билета, `Max books: ` и значение `maxBooks`, "
               "например `Max books: 5`.",
               "Подпись выводи через `System.out.print`, а значение — через `System.out.println`."],
        hint="Переменную объявляют так: тип, имя, `=`, значение и точка с запятой — `int maxBooks = 5;`. "
             "Чтобы напечатать её значение, пиши имя без кавычек.",
        solution=LIBRARY,
        wrong=[("имя переменной в кавычках: печатает слово maxBooks вместо числа",
                _change(LIBRARY, 'System.out.println(maxBooks);', 'System.out.println("maxBooks");')),
               ("в строке Card печатает лимит книг вместо номера билета",
                _change(LIBRARY, 'System.out.println(card);', 'System.out.println(maxBooks);'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-var-player-profile", title="Профиль игрока",
        given=[("String", "nick"), ("int", "level")],
        variants=[{"nick": '"Neo"', "level": "12"}, {"nick": '"Shadow"', "level": "3"}, {"nick": '"Alisa"', "level": "27"}],
        hidden=[{"nick": '"Rex"', "level": "1"}, {"nick": '"Tiger"', "level": "50"}, {"nick": '"Bob"', "level": "8"}],
        intro="Игра показывает профиль игрока. Ник записан в поле `nick`, уровень — в поле `level`.",
        steps=["Объяви переменную `String game` со значением `\"Space Race\"` и переменную `int lives` со значением `3`.",
               "Первой строкой выведи значение `game`.",
               "Второй строкой выведи ник, ` | level `, уровень, ` | lives ` и значение `lives` — например `Neo | level 12 | lives 3`.",
               "Части второй строки выводи через `System.out.print`, а последнюю — через `System.out.println`."],
        hint="Вторая строка собирается из пяти команд вывода. Значения переменных и полей печатай без кавычек, "
             "а текстовые куски — в кавычках, вместе с пробелами.",
        solution=PLAYER,
        wrong=[("кусок ` | level ` выведен через println: строка рвётся",
                _change(PLAYER, 'System.out.print(" | level ");', 'System.out.println(" | level ");')),
               ("имя переменной в кавычках: печатает слово lives",
                _change(PLAYER, 'System.out.println(lives);', 'System.out.println("lives");'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-var-flight-board", title="Табло вылета",
        given=[("String", "flight"), ("String", "city"), ("int", "gate")],
        variants=[{"flight": '"SU1402"', "city": '"Sochi"', "gate": "7"},
                  {"flight": '"S7 211"', "city": '"Kazan"', "gate": "15"},
                  {"flight": '"DP405"', "city": '"Omsk"', "gate": "3"}],
        hidden=[{"flight": '"UT360"', "city": '"Perm"', "gate": "22"},
                {"flight": '"SU10"', "city": '"Minsk"', "gate": "1"},
                {"flight": '"FV6011"', "city": '"Samara"', "gate": "2"}],
        intro="Табло в аэропорту показывает рейс, город назначения и выход на посадку. Номер рейса записан в поле `flight`, "
              "город — в поле `city`, номер выхода — в поле `gate`.",
        steps=["Объяви переменную `String status` со значением `\"Boarding\"` и переменную `int terminal` со значением `2`.",
               "Первая строка: рейс, ` -> ` и город, например `SU1402 -> Sochi`.",
               "Вторая строка: `Terminal `, значение `terminal`, `, gate ` и номер выхода, например `Terminal 2, gate 7`.",
               "Третья строка: значение `status`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть строки — через `System.out.println`."],
        hint="Число из переменной `terminal` и число из поля `gate` печатаются одинаково — по имени без кавычек. "
             "Не перепутай, что идёт после `Terminal `, а что после `, gate `.",
        solution=FLIGHT,
        wrong=[("после слова Terminal печатает номер выхода вместо терминала",
                _change(FLIGHT, 'System.out.print(terminal);', 'System.out.print(gate);')),
               ("стрелка выведена через println: город уезжает на следующую строку",
                _change(FLIGHT, 'System.out.print(" -> ");', 'System.out.println(" -> ");'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-var-cinema-ticket", title="Билет в кино",
        given=[("String", "film"), ("int", "row"), ("int", "seat")],
        variants=[{"film": '"Dune"', "row": "5", "seat": "12"}, {"film": '"Cars"', "row": "9", "seat": "3"},
                  {"film": '"Up"', "row": "2", "seat": "18"}],
        hidden=[{"film": '"Avatar"', "row": "11", "seat": "7"}, {"film": '"Coco"', "row": "1", "seat": "1"},
                {"film": '"Shrek"', "row": "14", "seat": "20"}],
        intro="Кинотеатр печатает билет. Название фильма записано в поле `film`, ряд и место — в полях `row` и `seat`. "
              "Любой билет на этот сеанс стоит 350 руб.",
        steps=["Объяви переменную `int price` и запиши в неё цену билета `350`.",
               "Первая строка: `Film: ` и название фильма.",
               "Вторая строка: `Row `, ряд, `, seat ` и место — например `Row 5, seat 12`.",
               "Третья строка: `Price: `, значение `price` и ` rub` — например `Price: 350 rub`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть строки — через `System.out.println`."],
        hint="Сначала ряд, потом место. Цену печатай из переменной `price`, а слово ` rub` — отдельной командой с пробелом впереди.",
        solution=CINEMA,
        wrong=[("вместо ряда печатает место",
                _change(CINEMA, 'System.out.print(row);', 'System.out.print(seat);')),
               ("цена выведена через println: rub уезжает на следующую строку",
                _change(CINEMA, 'System.out.print(price);', 'System.out.println(price);'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-var-marathon-bib", title="Номер марафонца",
        given=[("int", "number"), ("String", "name")],
        variants=[{"number": "105", "name": '"Anya"'}, {"number": "2048", "name": '"Ruslan"'}, {"number": "77", "name": '"Dina"'}],
        hidden=[{"number": "1", "name": '"Ivan"'}, {"number": "3500", "name": '"Lena"'}, {"number": "42", "name": '"Mark"'}],
        intro="На старте марафона каждому бегуну печатают карточку. Номер бегуна записан в поле `number`, имя — в поле `name`.",
        steps=["Объяви переменную `String race` со значением `\"Kazan Marathon\"` и переменную `int distance` со значением `42`.",
               "Первая строка: название забега, запятая с пробелом, дистанция и ` km` — например `Kazan Marathon, 42 km`.",
               "Вторая строка: `Runner `, номер, двоеточие с пробелом и имя — например `Runner 105: Anya`.",
               "Каждая строка собирается из четырёх команд: три `System.out.print` и в конце `System.out.println`."],
        hint="Сначала объяви обе переменные, потом печатай. Число `42` хранится в `int`, а название забега — в `String`.",
        solution=MARATHON,
        wrong=[("после слова Runner печатает дистанцию вместо номера бегуна",
                _change(MARATHON, 'System.out.print(number);', 'System.out.print(distance);')),
               ("дистанция выведена через println: строка рвётся перед km",
                _change(MARATHON, 'System.out.print(distance);', 'System.out.println(distance);'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-var-hotel-booking", title="Бронь в гостинице",
        given=[("int", "floor"), ("int", "nights")],
        variants=[{"floor": "4", "nights": "3"}, {"floor": "11", "nights": "1"}, {"floor": "2", "nights": "7"}],
        hidden=[{"floor": "1", "nights": "2"}, {"floor": "15", "nights": "10"}, {"floor": "3", "nights": "4"}],
        intro="Гостиница присылает гостю подтверждение брони. Этаж записан в поле `floor`, число ночей — в поле `nights`. "
              "Заезд в этой гостинице с 14:00, выезд до 12:00.",
        steps=["Объяви две переменные типа `String`: `checkIn` со значением `\"14:00\"` и `checkOut` со значением `\"12:00\"`.",
               "Первая строка: `Floor `, этаж, `, nights: ` и число ночей — например `Floor 4, nights: 3`.",
               "Вторая строка: `Check-in `, значение `checkIn`, `, check-out ` и значение `checkOut` — "
               "например `Check-in 14:00, check-out 12:00`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть строки — через `System.out.println`."],
        hint="Время с двоеточием — это текст, поэтому переменные для него типа `String`, а значения в кавычках. "
             "Этаж идёт раньше числа ночей, а заезд — раньше выезда.",
        solution=HOTEL,
        wrong=[("после check-out печатает время заезда",
                _change(HOTEL, 'System.out.println(checkOut);', 'System.out.println(checkIn);')),
               ("вместо этажа печатает число ночей",
                _change(HOTEL, 'System.out.print(floor);', 'System.out.print(nights);'))],
        constructs=["assignment"],
    ),
]
