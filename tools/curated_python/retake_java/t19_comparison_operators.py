"""COMPARISON_OPERATORS — «Операторы сравнения» (Java). Taught before: println, variables, assignment, arithmetic,
primitive types, String, / and %, += -= ++, if/else. The point: ==, !=, <, >, <=, >= give a boolean, and the right
operator decides the boundary cases. Not yet: && || !, switch, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "COMPARISON_OPERATORS"


def _taxi(first: str, second: str) -> str:
    return ('int a = 100 + 20 * km;\nint b = 200 + 15 * km;\n'
            'System.out.println("Tariff A: " + a + " rub");\nSystem.out.println("Tariff B: " + b + " rub");\n'
            f'if ({first}) {{\n    System.out.println("Take A");\n}} else if ({second}) {{\n    System.out.println("Take B");\n'
            '} else {\n    System.out.println("Same price");\n}')


def _fever(low: str, normal: str, high: str) -> str:
    return ('System.out.println("Temperature: " + temp / 10 + "." + temp % 10);\n'
            f'if ({low}) {{\n    System.out.println("Too low");\n}} else if ({normal}) {{\n    System.out.println("Normal");\n'
            f'}} else if ({high}) {{\n    System.out.println("Slightly high");\n}} else {{\n    System.out.println("Fever");\n}}')


TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-compare-rt-thermostat", title="Термостат",
        given=[("int", "temp"), ("int", "target")],
        variants=[{"temp": "18", "target": "22"}, {"temp": "25", "target": "21"}, {"temp": "20", "target": "20"}],
        hidden=[{"temp": "21", "target": "22"}, {"temp": "23", "target": "22"}, {"temp": "22", "target": "22"},
                {"temp": "-5", "target": "18"}],
        intro="Умный термостат сравнивает температуру в квартире — поле `temp` — с той, которую выбрал хозяин, — поле "
              "`target` (в градусах). Если холоднее, чем нужно, он включает отопление, если жарче — кондиционер.",
        steps=["Выведи `Heating on: ` и результат сравнения: `temp` меньше `target`.",
               "Выведи `Cooling on: ` и результат сравнения: `temp` больше `target`.",
               "Выведи `At target: ` и результат сравнения: `temp` равно `target`.",
               "Результат каждого сравнения Java напечатает сама — словом `true` или `false`."],
        hint="Сравнение можно сразу прибавить к строке, если взять его в скобки: `\"Bigger: \" + (a > b)`. "
             "Когда температура ровно такая, как нужно, ни отопление, ни кондиционер не включаются. Равенство в Java — "
             "это два знака `==`.",
        solution='System.out.println("Heating on: " + (temp < target));\n'
                 'System.out.println("Cooling on: " + (temp > target));\n'
                 'System.out.println("At target: " + (temp == target));',
        wrong=[("<= вместо <: при нужной температуре отопление всё равно включается",
                'System.out.println("Heating on: " + (temp <= target));\n'
                'System.out.println("Cooling on: " + (temp > target));\n'
                'System.out.println("At target: " + (temp == target));'),
               ("!= вместо ==: последняя строка отвечает наоборот",
                'System.out.println("Heating on: " + (temp < target));\n'
                'System.out.println("Cooling on: " + (temp > target));\n'
                'System.out.println("At target: " + (temp != target));')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-compare-rt-taxi-tariff", title="Какой тариф такси выгоднее",
        given=[("int", "km")],
        variants=[{"km": "8"}, {"km": "35"}, {"km": "20"}],
        hidden=[{"km": "19"}, {"km": "21"}, {"km": "20"}, {"km": "1"}, {"km": "100"}],
        intro="В приложении такси два тарифа. Тариф A: 100 руб. за посадку и 20 руб. за километр. Тариф B: 200 руб. за "
              "посадку и 15 руб. за километр. Длина поездки в километрах записана в поле `km`.",
        steps=["Заведи `int a` — цену поездки по тарифу A, и `int b` — по тарифу B.",
               "Выведи две строки: `Tariff A: `, цена и ` rub`, затем `Tariff B: `, цена и ` rub`.",
               "Третьей строкой: если A дешевле B, выведи `Take A`; если B дешевле A — `Take B`; если цены равны — `Same price`."],
        hint="Исходов три — подойдут `if`, `else if` и `else`. Выполняется только первая подходящая ветка, поэтому равные "
             "цены останутся для последнего `else`, если в обоих сравнениях стоит строгий знак `<`.",
        solution=_taxi('a < b', 'b < a'),
        wrong=[("<= вместо <: при равных ценах советует тариф A",
                _taxi('a <= b', 'b < a')),
               ("сравнение в обратную сторону: советует более дорогой тариф",
                _taxi('a > b', 'b > a'))],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-compare-rt-body-temperature", title="Электронный градусник",
        given=[("int", "temp")],
        variants=[{"temp": "368"}, {"temp": "384"}, {"temp": "373"}],
        hidden=[{"temp": "349"}, {"temp": "350"}, {"temp": "369"}, {"temp": "370"}, {"temp": "379"}, {"temp": "380"},
                {"temp": "402"}],
        intro="Электронный градусник хранит температуру тела целым числом в десятых долях градуса: `368` означает "
              "36.8 градуса. Число записано в поле `temp`. На экране градусник показывает температуру и подсказку.",
        steps=["Выведи `Temperature: `, целые градусы, точку и десятые — например `Temperature: 36.8`.",
               "Следующей строкой выведи подсказку. Ниже 35.0 — `Too low`.",
               "От 35.0 до 36.9 включительно — `Normal`.",
               "От 37.0 до 37.9 включительно — `Slightly high`.",
               "38.0 и выше — `Fever`."],
        hint="Целые градусы — это `temp / 10`, а десятые — `temp % 10`. Сравнивай само число `temp` с границами в десятых: "
             "35.0 — это `350`, 36.9 — `369`. Слово «включительно» подсказывает, где нужен `<=`, а где `<`.",
        solution=_fever('temp < 350', 'temp <= 369', 'temp <= 379'),
        wrong=[("< вместо <=: 36.9 считается повышенной температурой, а 37.9 — жаром",
                _fever('temp < 350', 'temp < 369', 'temp < 379')),
               ("<= вместо < в первой проверке: ровно 35.0 считается слишком низкой",
                _fever('temp <= 350', 'temp <= 369', 'temp <= 379'))],
        constructs=["if"],
    ),
]
