"""EXECUTION_FLOW_BASIC — «Порядок выполнения» (Java). Taught before: System.out.println / print, variables (`int`,
`String`), assignment, arithmetic `+ - *` with parentheses. This topic: statements run top to bottom one after another;
a variable changes step by step (`money = money - spent;` uses the value from the line above), a print shows the value
at that moment, a value must be saved before it changes, and the order of two changes matters.
Not yet: `+=` and `++`, division `/` and `%`, string concatenation (a line is assembled from several print calls),
conditions, loops."""
from java_tasks import JavaOutputTask

SKILL = "EXECUTION_FLOW_BASIC"


def _code(*lines: str) -> str:
    return "\n".join(lines)


def _change(code: str, old: str, new: str, nth: int = 1) -> str:
    """The code with the nth line equal to `old` replaced by `new` (a one-line mistake)."""
    lines = code.split("\n")
    found = [i for i, line in enumerate(lines) if line == old]
    assert len(found) >= nth, f"no line {old!r}"
    lines[found[nth - 1]] = new
    return "\n".join(lines)


def _swap(code: str, a: str, b: str) -> str:
    """The code with lines `a` and `b` exchanged (statements in the wrong order)."""
    lines = code.split("\n")
    i, j = lines.index(a), lines.index(b)
    lines[i], lines[j] = lines[j], lines[i]
    return "\n".join(lines)


BATTERY = _code(
    'int battery = charge;',
    'System.out.print("Start: ");',
    'System.out.print(battery);',
    'System.out.println("%");',
    'battery = battery - video;',
    'System.out.print("After video: ");',
    'System.out.print(battery);',
    'System.out.println("%");',
    'battery = battery + charger;',
    'System.out.print("After charging: ");',
    'System.out.print(battery);',
    'System.out.println("%");',
)

BACTERIA = _code(
    'int cells = start;',
    'cells = cells * 2;',
    'System.out.print("Hour 1: ");',
    'System.out.println(cells);',
    'cells = cells - sample;',
    'System.out.print("After sample: ");',
    'System.out.println(cells);',
    'cells = cells * 2;',
    'System.out.print("Hour 2: ");',
    'System.out.println(cells);',
)

ROAD = _code(
    'int start = odometer;',
    'odometer = odometer + there;',
    'odometer = odometer + detour;',
    'odometer = odometer + there;',
    'int trip = odometer - start;',
    'int fuel = trip * perKm;',
    'System.out.print("Odometer: ");',
    'System.out.println(odometer);',
    'System.out.print("Trip: ");',
    'System.out.print(trip);',
    'System.out.println(" km");',
    'System.out.print("Fuel: ");',
    'System.out.print(fuel);',
    'System.out.println(" rub");',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-flow-rt-phone-battery", title="Заряд телефона",
        given=[("int", "charge"), ("int", "video"), ("int", "charger")],
        variants=[{"charge": "80", "video": "25", "charger": "30"}, {"charge": "45", "video": "30", "charger": "50"},
                  {"charge": "100", "video": "15", "charger": "10"}],
        hidden=[{"charge": "20", "video": "20", "charger": "60"}, {"charge": "65", "video": "5", "charger": "0"},
                {"charge": "50", "video": "40", "charger": "35"}],
        intro="Утром телефон был заряжен на `charge` процентов. В дороге Дима смотрел видео, и заряд упал на `video` процентов, "
              "а потом телефон полежал на зарядке и получил ещё `charger` процентов.",
        steps=["Объяви переменную `int battery` со значением `charge` и выведи строку `Start: `, значение `battery` и знак `%`, "
               "например `Start: 80%`.",
               "Вычти расход на видео: `battery = battery - video;`. Выведи `After video: `, значение `battery` и `%`.",
               "Прибавь то, что дала зарядка, и выведи `After charging: `, значение `battery` и `%`.",
               "Части одной строки выводи через `System.out.print`, а знак `%` — через `System.out.println`."],
        hint="Команды выполняются сверху вниз: каждое изменение берёт значение `battery`, которое получилось строкой выше.",
        solution=BATTERY,
        wrong=[("при зарядке считает от утреннего заряда и забывает про видео",
                _change(BATTERY, 'battery = battery + charger;', 'battery = charge + charger;')),
               ("печатает After video до того, как вычел расход",
                BATTERY.replace('battery = battery - video;\nSystem.out.print("After video: ");\nSystem.out.print(battery);',
                                'System.out.print("After video: ");\nSystem.out.print(battery);\nbattery = battery - video;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-flow-rt-lab-bacteria", title="Бактерии в пробирке",
        given=[("int", "start"), ("int", "sample")],
        variants=[{"start": "50", "sample": "30"}, {"start": "120", "sample": "100"}, {"start": "15", "sample": "6"}],
        hidden=[{"start": "1", "sample": "1"}, {"start": "200", "sample": "0"}, {"start": "35", "sample": "70"}],
        intro="В пробирке `start` бактерий, и за каждый час их число удваивается. После первого часа лаборант забрал "
              "`sample` бактерий на анализ, а потом прошёл ещё один час.",
        steps=["Объяви переменную `int cells` со значением `start`.",
               "Прошёл час: удвой `cells` командой `cells = cells * 2;` и выведи `Hour 1: ` и значение `cells`.",
               "Вычти забранные на анализ бактерии и выведи `After sample: ` и значение `cells`.",
               "Прошёл второй час: снова удвой `cells` и выведи `Hour 2: ` и значение `cells`.",
               "Подписи выводи через `System.out.print`, числа — через `System.out.println`."],
        hint="Во второй час удваиваются только те бактерии, что остались после анализа, — поэтому вычитание стоит между удвоениями.",
        solution=BACTERIA,
        wrong=[("во второй час удваивает начальное число и теряет первый час и анализ",
                _change(BACTERIA, 'cells = cells * 2;', 'cells = start * 2;', 2)),
               ("пробу забирает до первого удвоения",
                _swap(BACTERIA, 'cells = cells * 2;', 'cells = cells - sample;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-flow-rt-road-trip", title="Поездка на дачу",
        given=[("int", "odometer"), ("int", "there"), ("int", "detour"), ("int", "perKm")],
        variants=[{"odometer": "45210", "there": "60", "detour": "15", "perKm": "7"},
                  {"odometer": "120500", "there": "85", "detour": "10", "perKm": "6"},
                  {"odometer": "8000", "there": "40", "detour": "25", "perKm": "8"}],
        hidden=[{"odometer": "0", "there": "1", "detour": "0", "perKm": "5"},
                {"odometer": "99990", "there": "120", "detour": "30", "perKm": "9"},
                {"odometer": "31000", "there": "55", "detour": "5", "perKm": "10"}],
        intro="Перед поездкой на дачу счётчик пробега машины показывал `odometer` км. До дачи `there` км, на обратном "
              "пути заехали в магазин — крюк в `detour` км, — а потом проехали такой же путь от дачи до дома. "
              "Бензин обходится в `perKm` руб. на километр.",
        steps=["Объяви переменную `int start` и сохрани в неё показание `odometer` до поездки.",
               "Измени поле `odometer` тремя командами по порядку: дорога до дачи, крюк до магазина, дорога обратно.",
               "Объяви переменную `int trip` — сколько километров проехали (новое показание минус старое), и переменную "
               "`int fuel` — сколько стоил бензин на эту поездку.",
               "Выведи три строки: `Odometer: ` и новое показание, `Trip: ` с километрами и ` km`, `Fuel: ` с рублями и ` rub` — "
               "например `Trip: 135 km`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть — через `System.out.println`."],
        hint="Начальное показание нужно в конце, а поле `odometer` к тому моменту уже изменится, — поэтому `start` сохраняют "
             "первой командой.",
        solution=ROAD,
        wrong=[("забывает дорогу обратно",
                _change(ROAD, 'odometer = odometer + there;', 'odometer = odometer + 0;', 2)),
               ("сохраняет начальное показание уже после дороги до дачи",
                _swap(ROAD, 'int start = odometer;', 'odometer = odometer + there;'))],
        constructs=["assignment"],
    ),
]
