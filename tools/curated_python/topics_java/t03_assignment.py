"""ASSIGNMENT — «Присваивание» (Java). Taught before: System.out.println / print, declaring variables (`int`, `String`)
with an initial value. This topic: changing a variable with `=` after its declaration — a new value replaces the old one,
the value is copied from the right side into the variable on the left, a copy keeps the old value (save before
overwriting, swap through a temporary variable). Fields of the starter may be reassigned like variables.
Not yet: arithmetic (no `x = x + 1` — that needs topic 4), string operations (a line is assembled from several print
calls), conditions, loops."""
from java_tasks import JavaOutputTask

SKILL = "ASSIGNMENT"


def _code(*lines: str) -> str:
    return "\n".join(lines)


def _change(code: str, old: str, new: str, nth: int = 1) -> str:
    """The code with the nth line equal to `old` replaced by `new` (a one-line mistake)."""
    lines = code.split("\n")
    found = [i for i, line in enumerate(lines) if line == old]
    assert len(found) >= nth, f"no line {old!r}"
    lines[found[nth - 1]] = new
    return "\n".join(lines)


THERMOMETER = _code(
    'int temp = morning;',
    'System.out.print("Morning: ");',
    'System.out.println(temp);',
    'temp = noon;',
    'System.out.print("Noon: ");',
    'System.out.println(temp);',
    'temp = evening;',
    'System.out.print("Evening: ");',
    'System.out.println(temp);',
)

SAVE = _code(
    'int current = checkpoint;',
    'int saved = current;',
    'current = reached;',
    'System.out.print("Current level: ");',
    'System.out.println(current);',
    'System.out.print("Saved level: ");',
    'System.out.println(saved);',
)

PLAYLIST = _code(
    'String current = song1;',
    'String next = song2;',
    'System.out.print(current);',
    'System.out.print(" -> ");',
    'System.out.println(next);',
    'current = next;',
    'next = song3;',
    'System.out.print(current);',
    'System.out.print(" -> ");',
    'System.out.println(next);',
)

QUEUE = _code(
    'System.out.print("Served: ");',
    'System.out.println(first);',
    'first = second;',
    'second = third;',
    'third = newcomer;',
    'System.out.print("Waiting: ");',
    'System.out.print(first);',
    'System.out.print(", ");',
    'System.out.print(second);',
    'System.out.print(", ");',
    'System.out.println(third);',
)

CHESS = _code(
    'System.out.print("White: ");',
    'System.out.println(white);',
    'System.out.print("Black: ");',
    'System.out.println(black);',
    'String temp = white;',
    'white = black;',
    'black = temp;',
    'System.out.print("White: ");',
    'System.out.println(white);',
    'System.out.print("Black: ");',
    'System.out.println(black);',
)

DUTY = _code(
    'String temp = monday;',
    'monday = tuesday;',
    'tuesday = wednesday;',
    'wednesday = temp;',
    'System.out.print("Mon: ");',
    'System.out.println(monday);',
    'System.out.print("Tue: ");',
    'System.out.println(tuesday);',
    'System.out.print("Wed: ");',
    'System.out.println(wednesday);',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-asg-thermometer", title="Термометр за окном",
        given=[("int", "morning"), ("int", "noon"), ("int", "evening")],
        variants=[{"morning": "8", "noon": "15", "evening": "11"}, {"morning": "-3", "noon": "2", "evening": "-1"},
                  {"morning": "17", "noon": "26", "evening": "20"}],
        hidden=[{"morning": "5", "noon": "9", "evening": "7"}, {"morning": "-12", "noon": "-6", "evening": "-9"},
                {"morning": "20", "noon": "31", "evening": "24"}],
        intro="Умный термометр за окном показывает одно число — последнее измерение. Утреннее, дневное и вечернее измерения "
              "записаны в полях `morning`, `noon` и `evening`.",
        steps=["Объяви переменную `int temp` и запиши в неё утреннее измерение. Выведи строку `Morning: ` и значение `temp`.",
               "Присвой `temp` дневное измерение (без нового объявления — `int` второй раз не пиши) и выведи `Noon: ` и значение `temp`.",
               "Присвой `temp` вечернее измерение и выведи `Evening: ` и значение `temp`.",
               "Подписи выводи через `System.out.print`, а значение `temp` — через `System.out.println`."],
        hint="Присваивание `temp = noon;` кладёт значение справа в переменную слева, а старое значение `temp` пропадает.",
        solution=THERMOMETER,
        wrong=[("днём снова кладёт утреннее измерение",
                _change(THERMOMETER, 'temp = noon;', 'temp = morning;')),
               ("присваивание наоборот: записывает temp в поле evening, а temp не меняется",
                _change(THERMOMETER, 'temp = evening;', 'evening = temp;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-asg-game-save", title="Сохранение в игре",
        given=[("int", "checkpoint"), ("int", "reached")],
        variants=[{"checkpoint": "4", "reached": "6"}, {"checkpoint": "10", "reached": "13"}, {"checkpoint": "1", "reached": "2"}],
        hidden=[{"checkpoint": "7", "reached": "9"}, {"checkpoint": "20", "reached": "25"}, {"checkpoint": "3", "reached": "8"}],
        intro="Игра запоминает уровень на последнем сохранении. Игрок сохранился на уровне `checkpoint`, а потом дошёл до уровня `reached`.",
        steps=["Объяви переменную `int current` и запиши в неё `checkpoint`.",
               "Объяви переменную `int saved` и запиши в неё значение `current` — это сохранение.",
               "Присвой `current` значение `reached`: игрок прошёл дальше.",
               "Выведи две строки: `Current level: ` и значение `current`, затем `Saved level: ` и значение `saved`."],
        hint="После `int saved = current;` в `saved` лежит копия числа. Когда `current` потом меняется, копия в `saved` остаётся прежней.",
        solution=SAVE,
        wrong=[("присваивание наоборот: записывает current в поле reached, а current не меняется",
                _change(SAVE, 'current = reached;', 'reached = current;')),
               ("во второй строке печатает текущий уровень вместо сохранённого",
                _change(SAVE, 'System.out.println(saved);', 'System.out.println(current);'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-asg-playlist", title="Следующая песня",
        given=[("String", "song1"), ("String", "song2"), ("String", "song3")],
        variants=[{"song1": '"Yesterday"', "song2": '"Imagine"', "song3": '"Hello"'},
                  {"song1": '"Believer"', "song2": '"Thunder"', "song3": '"Radioactive"'},
                  {"song1": '"Numb"', "song2": '"Faint"', "song3": '"Crawling"'}],
        hidden=[{"song1": '"Help"', "song2": '"Let It Be"', "song3": '"Something"'},
                {"song1": '"Halo"', "song2": '"Hello"', "song3": '"Skyfall"'},
                {"song1": '"One"', "song2": '"Two"', "song3": '"Three"'}],
        intro="Плеер показывает, какая песня играет сейчас и какая будет следующей. Песни плейлиста по порядку записаны "
              "в полях `song1`, `song2` и `song3`.",
        steps=["Объяви переменные `String current` (сейчас играет `song1`) и `String next` (следующая — `song2`).",
               "Выведи строку: значение `current`, ` -> ` и значение `next`, например `Yesterday -> Imagine`.",
               "Песня закончилась: присвой `current` значение `next`, а потом `next` — значение `song3`.",
               "Снова выведи такую же строку из `current` и `next`, например `Imagine -> Hello`."],
        hint="Порядок присваиваний важен: сначала `current` забирает значение у `next`, и только потом `next` получает новую песню.",
        solution=PLAYLIST,
        wrong=[("присваивание наоборот: next = current, и текущая песня не меняется",
                _change(PLAYLIST, 'current = next;', 'next = current;')),
               ("присваивания в обратном порядке: next меняется раньше, чем current его забирает",
                _change(_change(PLAYLIST, 'current = next;', 'next = song3;'), 'next = song3;', 'current = next;', 2))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-asg-checkout-queue", title="Очередь на кассе",
        given=[("String", "first"), ("String", "second"), ("String", "third"), ("String", "newcomer")],
        variants=[{"first": '"Anya"', "second": '"Boris"', "third": '"Vika"', "newcomer": '"Gleb"'},
                  {"first": '"Oleg"', "second": '"Kate"', "third": '"Ilya"', "newcomer": '"Nina"'},
                  {"first": '"Mom"', "second": '"Dad"', "third": '"Lisa"', "newcomer": '"Tom"'}],
        hidden=[{"first": '"Ann"', "second": '"Ben"', "third": '"Cat"', "newcomer": '"Dan"'},
                {"first": '"Lev"', "second": '"Mia"', "third": '"Ned"', "newcomer": '"Ola"'},
                {"first": '"Zoe"', "second": '"Yan"', "third": '"Xenia"', "newcomer": '"Will"'}],
        intro="В очереди на кассе три человека: `first`, `second` и `third`. Первого обслужили, все сдвинулись вперёд, "
              "а в конец встал `newcomer`.",
        steps=["Выведи строку `Served: ` и значение `first`.",
               "Сдвинь очередь присваиваниями полей по порядку: в `first` запиши `second`, в `second` — `third`, в `third` — `newcomer`.",
               "Выведи строку `Waiting: ` и три имени через запятую с пробелом, например `Waiting: Boris, Vika, Gleb`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть — через `System.out.println`."],
        hint="Каждое присваивание забирает значение у следующего в очереди, поэтому идти нужно от начала очереди к концу.",
        solution=QUEUE,
        wrong=[("во второе место снова кладёт first, который уже равен second",
                _change(QUEUE, 'second = third;', 'second = first;')),
               ("сдвигает с конца: first получает уже изменённый second",
                _change(_change(QUEUE, 'first = second;', 'second = third;'), 'second = third;', 'first = second;', 2))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-asg-chess-colors", title="Смена цвета в шахматах",
        given=[("String", "white"), ("String", "black")],
        variants=[{"white": '"Anya"', "black": '"Boris"'}, {"white": '"Magnus"', "black": '"Ian"'}, {"white": '"Dad"', "black": '"Timur"'}],
        hidden=[{"white": '"Vika"', "black": '"Oleg"'}, {"white": '"Kate"', "black": '"Lev"'}, {"white": '"Max"', "black": '"Nina"'}],
        intro="В шахматном клубе играют две партии: во второй партии игроки меняются цветами. Кто играет белыми в первой "
              "партии, записано в поле `white`, кто чёрными — в поле `black`.",
        steps=["Выведи две строки: `White: ` и значение `white`, затем `Black: ` и значение `black`.",
               "Поменяй значения полей местами через временную переменную: объяви `String temp` со значением `white`, "
               "потом присвой `white` значение `black`, а `black` — значение `temp`.",
               "Снова выведи те же две строки — теперь с новыми значениями.",
               "Подписи выводи через `System.out.print`, имена — через `System.out.println`."],
        hint="Если сразу написать `white = black;`, прежнее значение `white` пропадёт. Поэтому его сначала откладывают в `temp`.",
        solution=CHESS,
        wrong=[("в black кладёт уже изменённый white вместо отложенного temp",
                _change(CHESS, 'black = temp;', 'black = white;')),
               ("откладывает в temp не то значение: black вместо white",
                _change(CHESS, 'String temp = white;', 'String temp = black;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-asg-duty-rotation", title="Дежурства по кругу",
        given=[("String", "monday"), ("String", "tuesday"), ("String", "wednesday")],
        variants=[{"monday": '"Anya"', "tuesday": '"Boris"', "wednesday": '"Vika"'},
                  {"monday": '"Gleb"', "tuesday": '"Dina"', "wednesday": '"Egor"'},
                  {"monday": '"Kira"', "tuesday": '"Lev"', "wednesday": '"Mila"'}],
        hidden=[{"monday": '"Ann"', "tuesday": '"Ben"', "wednesday": '"Cat"'},
                {"monday": '"Oleg"', "tuesday": '"Pasha"', "wednesday": '"Rita"'},
                {"monday": '"Sam"', "tuesday": '"Tanya"', "wednesday": '"Ulyana"'}],
        intro="Трое студентов дежурят в лаборатории по понедельникам, вторникам и средам. На этой неделе дежурят `monday`, "
              "`tuesday` и `wednesday`. На следующей неделе все сдвигаются на день раньше, а дежурный понедельника переходит на среду.",
        steps=["Объяви `String temp` и отложи в неё значение `monday`.",
               "Присвой `monday` значение `tuesday`, затем `tuesday` — значение `wednesday`, затем `wednesday` — значение `temp`.",
               "Выведи три строки: `Mon: `, `Tue: `, `Wed: ` и дежурного следующей недели, например `Mon: Boris`.",
               "Подписи выводи через `System.out.print`, имена — через `System.out.println`."],
        hint="Это как обмен двух значений, только по кругу из трёх: временная переменная хранит то значение, которое затрут первым.",
        solution=DUTY,
        wrong=[("в среду кладёт уже изменённый monday вместо отложенного temp",
                _change(DUTY, 'wednesday = temp;', 'wednesday = monday;')),
               ("во вторник кладёт monday, который уже равен tuesday",
                _change(DUTY, 'tuesday = wednesday;', 'tuesday = monday;'))],
        constructs=["assignment"],
    ),
]
