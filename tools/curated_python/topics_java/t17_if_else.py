"""IF_ELSE_BASIC — «Условия if / else» (Java). Taught before: println, variables, assignment, arithmetic, primitive
types, strings, / and %, += -=. Comparisons in a condition are part of this topic (the course's diagnostic uses them)."""
from java_tasks import JavaOutputTask

SKILL = "IF_ELSE_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-if-ride-height", title="Рост для аттракциона",
        given=[("int", "height")],
        variants=[{"height": "135"}, {"height": "112"}, {"height": "150"}],
        hidden=[{"height": "120"}, {"height": "119"}, {"height": "99"}, {"height": "180"}],
        intro="На аттракцион «Американские горки» пускают детей ростом от 120 см. Рост ребёнка записан в поле `height`.",
        steps=["Если `height` больше или равен `120`, выведи `You can ride`.",
               "Иначе выведи `Not yet`."],
        hint="Условие «больше или равно» в Java пишется как `>=`. Ребёнок ростом ровно 120 см уже проходит.",
        solution='if (height >= 120) {\n    System.out.println("You can ride");\n} else {\n    System.out.println("Not yet");\n}',
        wrong=[("строгое сравнение: ровно 120 см не пускает",
                'if (height > 120) {\n    System.out.println("You can ride");\n} else {\n    System.out.println("Not yet");\n}'),
               ("ветки перепутаны",
                'if (height >= 120) {\n    System.out.println("Not yet");\n} else {\n    System.out.println("You can ride");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-if-even-teams", title="Команды для эстафеты",
        given=[("int", "students")],
        variants=[{"students": "24"}, {"students": "17"}, {"students": "30"}],
        hidden=[{"students": "9"}, {"students": "2"}, {"students": "41"}, {"students": "0"}],
        intro="Учитель физкультуры делит класс на две равные команды. Сколько учеников пришло на урок, записано в поле `students`.",
        steps=["Если `students` делится на 2 без остатка, выведи `Equal teams: N each`, где N — половина учеников.",
               "Иначе выведи `One student will be the judge`, а следующей строкой — `Teams of N`, где N — сколько учеников останется в каждой команде без судьи."],
        hint="Остаток от деления на 2 даёт оператор `%`: `students % 2 == 0` значит, что число чётное. "
             "Без судьи учеников на одного меньше, и это число уже делится на 2.",
        solution='if (students % 2 == 0) {\n    System.out.println("Equal teams: " + students / 2 + " each");\n} else {\n'
                 '    System.out.println("One student will be the judge");\n    System.out.println("Teams of " + (students - 1) / 2);\n}',
        wrong=[("не вычитает судью: в нечётном классе делит всех учеников",
                'if (students % 2 == 0) {\n    System.out.println("Equal teams: " + students / 2 + " each");\n} else {\n'
                '    System.out.println("One student will be the judge");\n    System.out.println("Teams of " + students / 2 + 1);\n}'),
               ("проверяет остаток от деления на 3 вместо 2",
                'if (students % 3 == 0) {\n    System.out.println("Equal teams: " + students / 2 + " each");\n} else {\n'
                '    System.out.println("One student will be the judge");\n    System.out.println("Teams of " + (students - 1) / 2);\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-if-free-delivery", title="Бесплатная доставка",
        given=[("int", "price"), ("int", "count")],
        variants=[{"price": "450", "count": "3"}, {"price": "700", "count": "3"}, {"price": "1000", "count": "2"}],
        hidden=[{"price": "500", "count": "4"}, {"price": "1999", "count": "1"}, {"price": "100", "count": "25"}, {"price": "50", "count": "1"}],
        intro="Интернет-магазин привозит заказ бесплатно, если товары стоят 2000 руб. или больше, иначе доставка стоит 300 руб. "
              "Цена одного товара — в поле `price`, количество — в поле `count`.",
        steps=["Посчитай стоимость товаров: `price`, умноженная на `count`.",
               "Если стоимость товаров 2000 или больше, доставка стоит 0 руб., иначе — 300 руб.",
               "Выведи три строки: `Goods: … rub`, `Delivery: … rub` и `Total: … rub` (товары плюс доставка)."],
        hint="Заведи переменную для стоимости доставки до `if`, а в ветках только присвой ей 0 или 300. Тогда печатать строки можно один раз — после условия.",
        solution='int goods = price * count;\nint delivery;\nif (goods >= 2000) {\n    delivery = 0;\n} else {\n    delivery = 300;\n}\n'
                 'System.out.println("Goods: " + goods + " rub");\nSystem.out.println("Delivery: " + delivery + " rub");\n'
                 'System.out.println("Total: " + (goods + delivery) + " rub");',
        wrong=[("сравнивает цену одного товара, а не всего заказа",
                'int goods = price * count;\nint delivery;\nif (price >= 2000) {\n    delivery = 0;\n} else {\n    delivery = 300;\n}\n'
                'System.out.println("Goods: " + goods + " rub");\nSystem.out.println("Delivery: " + delivery + " rub");\n'
                'System.out.println("Total: " + (goods + delivery) + " rub");'),
               ("склеивает числа как строки в итоговой сумме",
                'int goods = price * count;\nint delivery;\nif (goods >= 2000) {\n    delivery = 0;\n} else {\n    delivery = 300;\n}\n'
                'System.out.println("Goods: " + goods + " rub");\nSystem.out.println("Delivery: " + delivery + " rub");\n'
                'System.out.println("Total: " + goods + delivery + " rub");')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-if-phone-battery", title="Заряд телефона",
        given=[("int", "battery")],
        variants=[{"battery": "45"}, {"battery": "12"}, {"battery": "87"}],
        hidden=[{"battery": "20"}, {"battery": "19"}, {"battery": "0"}, {"battery": "100"}],
        intro="Телефон предупреждает хозяина, когда заряда остаётся меньше 20 процентов. Текущий заряд в процентах записан в поле `battery`.",
        steps=["Если `battery` меньше `20`, выведи `Charge your phone`.",
               "Иначе выведи `Battery OK`."],
        hint="«Меньше» в Java — это `<`. При заряде ровно 20 процентов предупреждения ещё нет.",
        solution='if (battery < 20) {\n    System.out.println("Charge your phone");\n} else {\n    System.out.println("Battery OK");\n}',
        wrong=[("нестрогое сравнение: при 20 процентах тоже предупреждает",
                'if (battery <= 20) {\n    System.out.println("Charge your phone");\n} else {\n    System.out.println("Battery OK");\n}'),
               ("ветки перепутаны",
                'if (battery < 20) {\n    System.out.println("Battery OK");\n} else {\n    System.out.println("Charge your phone");\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-if-bus-seats", title="Места в автобусе",
        given=[("int", "passengers")],
        variants=[{"passengers": "32"}, {"passengers": "47"}, {"passengers": "40"}],
        hidden=[{"passengers": "40"}, {"passengers": "41"}, {"passengers": "0"}, {"passengers": "39"}, {"passengers": "75"}],
        intro="В экскурсионном автобусе 40 сидячих мест. Сколько пассажиров зашло в автобус, записано в поле `passengers`.",
        steps=["Если `passengers` меньше или равно `40`, выведи `Everyone has a seat`, а следующей строкой — `Free seats: N`, где N — сколько мест осталось свободными.",
               "Иначе выведи `Bus is full`, а следующей строкой — `Standing: N`, где N — сколько пассажирам не хватило мест."],
        hint="Свободные места — это 40 минус пассажиры, а стоящие — пассажиры минус 40. Если пассажиров ровно 40, все сидят и свободных мест 0.",
        solution='if (passengers <= 40) {\n    System.out.println("Everyone has a seat");\n    System.out.println("Free seats: " + (40 - passengers));\n} else {\n'
                 '    System.out.println("Bus is full");\n    System.out.println("Standing: " + (passengers - 40));\n}',
        wrong=[("строгое сравнение: при 40 пассажирах пишет, что автобус переполнен",
                'if (passengers < 40) {\n    System.out.println("Everyone has a seat");\n    System.out.println("Free seats: " + (40 - passengers));\n} else {\n'
                '    System.out.println("Bus is full");\n    System.out.println("Standing: " + (passengers - 40));\n}'),
               ("в обеих ветках вычитает из 40",
                'if (passengers <= 40) {\n    System.out.println("Everyone has a seat");\n    System.out.println("Free seats: " + (40 - passengers));\n} else {\n'
                '    System.out.println("Bus is full");\n    System.out.println("Standing: " + (40 - passengers));\n}')],
        constructs=["if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-if-phone-plan", title="Минуты сверх тарифа",
        given=[("int", "minutes"), ("int", "limit")],
        variants=[{"minutes": "350", "limit": "300"}, {"minutes": "120", "limit": "200"}, {"minutes": "520", "limit": "400"}],
        hidden=[{"minutes": "300", "limit": "300"}, {"minutes": "301", "limit": "300"}, {"minutes": "0", "limit": "100"}, {"minutes": "1000", "limit": "250"}],
        intro="Тариф мобильной связи стоит 400 руб. в месяц, в него входит `limit` минут разговоров. Каждая минута сверх этого стоит 3 руб. "
              "Сколько минут абонент проговорил за месяц, записано в поле `minutes`.",
        steps=["Если `minutes` больше `limit`, лишние минуты — это `minutes` минус `limit`, иначе лишних минут 0.",
               "Плата за месяц — 400 руб. плюс 3 руб. за каждую лишнюю минуту.",
               "Выведи три строки: `Used: … of … min` (сначала `minutes`, потом `limit`), `Extra minutes: …` и `To pay: … rub`."],
        hint="Заведи переменную для лишних минут до `if`, а в ветках только присвой ей значение. Плату и строки посчитай и выведи один раз — после условия.",
        solution='int extra;\nif (minutes > limit) {\n    extra = minutes - limit;\n} else {\n    extra = 0;\n}\nint pay = 400 + extra * 3;\n'
                 'System.out.println("Used: " + minutes + " of " + limit + " min");\nSystem.out.println("Extra minutes: " + extra);\n'
                 'System.out.println("To pay: " + pay + " rub");',
        wrong=[("за лишние минуты забывает абонентскую плату 400 руб.",
                'int extra;\nint pay;\nif (minutes > limit) {\n    extra = minutes - limit;\n    pay = extra * 3;\n} else {\n    extra = 0;\n    pay = 400;\n}\n'
                'System.out.println("Used: " + minutes + " of " + limit + " min");\nSystem.out.println("Extra minutes: " + extra);\n'
                'System.out.println("To pay: " + pay + " rub");'),
               ("вычитает в обратном порядке: limit минус minutes",
                'int extra;\nif (minutes > limit) {\n    extra = limit - minutes;\n} else {\n    extra = 0;\n}\nint pay = 400 + extra * 3;\n'
                'System.out.println("Used: " + minutes + " of " + limit + " min");\nSystem.out.println("Extra minutes: " + extra);\n'
                'System.out.println("To pay: " + pay + " rub");')],
        constructs=["if"],
    ),
]
