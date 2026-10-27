"""INTEGER_DIVISION — «Целочисленное деление и остаток» (Java). Taught before: println, variables, assignment, arithmetic,
execution order, primitive types, String. The point: int / int drops the fraction, % gives the remainder; together
they split a number into units (hours and minutes, hundreds and tens, rows and seats). Not yet: += -= ++, if/else,
comparisons, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "INTEGER_DIVISION"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-div-rt-egg-boxes", title="Яйца по коробкам",
        given=[("int", "eggs"), ("int", "boxPrice")],
        variants=[{"eggs": "47", "boxPrice": "120"}, {"eggs": "135", "boxPrice": "95"}, {"eggs": "28", "boxPrice": "110"}],
        hidden=[{"eggs": "50", "boxPrice": "100"}, {"eggs": "9", "boxPrice": "130"}, {"eggs": "101", "boxPrice": "90"},
                {"eggs": "10", "boxPrice": "105"}],
        intro="На птицеферме за день собрали `eggs` яиц. Их раскладывают в коробки по 10 штук; продают только полные "
              "коробки по `boxPrice` руб., а яйца, которых не хватило на коробку, остаются на ферме.",
        steps=["Заведи `int boxes` — сколько получится полных коробок, и `int loose` — сколько яиц останется без коробки.",
               "Заведи `int money` — сколько денег принесут полные коробки.",
               "Выведи три строки: `Boxes: ` и `boxes`, `Loose eggs: ` и `loose`, `Money: `, `money` и ` rub`."],
        hint="При делении двух `int` Java отбрасывает дробную часть: `47 / 10` — это `4`. "
             "Остаток от деления даёт оператор `%`: `47 % 10` — это `7`.",
        solution='int boxes = eggs / 10;\n'
                 'int loose = eggs % 10;\n'
                 'int money = boxes * boxPrice;\n'
                 'System.out.println("Boxes: " + boxes);\n'
                 'System.out.println("Loose eggs: " + loose);\n'
                 'System.out.println("Money: " + money + " rub");',
        wrong=[("перепутаны / и %: коробок — остаток",
                'int boxes = eggs % 10;\n'
                'int loose = eggs % 10;\n'
                'int money = boxes * boxPrice;\n'
                'System.out.println("Boxes: " + boxes);\n'
                'System.out.println("Loose eggs: " + loose);\n'
                'System.out.println("Money: " + money + " rub");'),
               ("деньги считает за все яйца поштучно, а не за коробки",
                'int boxes = eggs / 10;\n'
                'int loose = eggs % 10;\n'
                'int money = eggs * boxPrice;\n'
                'System.out.println("Boxes: " + boxes);\n'
                'System.out.println("Loose eggs: " + loose);\n'
                'System.out.println("Money: " + money + " rub");')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-div-rt-school-buses", title="Автобусы на экскурсию",
        given=[("int", "people"), ("int", "seats")],
        variants=[{"people": "95", "seats": "40"}, {"people": "130", "seats": "45"}, {"people": "62", "seats": "30"}],
        hidden=[{"people": "80", "seats": "40"}, {"people": "1", "seats": "50"}, {"people": "41", "seats": "40"},
                {"people": "200", "seats": "33"}],
        intro="Школа везёт на экскурсию `people` человек. В каждом автобусе `seats` мест. Автобусы заполняют по очереди "
              "полностью, а оставшиеся люди едут в последнем, неполном автобусе — если такие люди есть.",
        steps=["Заведи `int full` — сколько автобусов уедут заполненными полностью.",
               "Заведи `int lastBus` — сколько человек останется на последний неполный автобус (0, если не останется никого).",
               "Заведи `int order` — сколько всего автобусов нужно заказать: `(people + seats - 1) / seats`.",
               "Выведи три строки: `Full buses: ` и `full`, `In last bus: ` и `lastBus`, `Buses to order: ` и `order`."],
        hint="Прибавка `seats - 1` перед делением — приём округления вверх: если хоть один человек не поместился в полные "
             "автобусы, частное увеличится на единицу, а если все поместились ровно — не изменится. Проверь: 80 человек по 40 мест — "
             "это 2 автобуса, а 81 человек — уже 3.",
        solution='int full = people / seats;\n'
                 'int lastBus = people % seats;\n'
                 'int order = (people + seats - 1) / seats;\n'
                 'System.out.println("Full buses: " + full);\n'
                 'System.out.println("In last bus: " + lastBus);\n'
                 'System.out.println("Buses to order: " + order);',
        wrong=[("всегда прибавляет лишний автобус, даже если все уместились ровно",
                'int full = people / seats;\n'
                'int lastBus = people % seats;\n'
                'int order = people / seats + 1;\n'
                'System.out.println("Full buses: " + full);\n'
                'System.out.println("In last bus: " + lastBus);\n'
                'System.out.println("Buses to order: " + order);'),
               ("операнды остатка перепутаны: места % люди",
                'int full = people / seats;\n'
                'int lastBus = seats % people;\n'
                'int order = (people + seats - 1) / seats;\n'
                'System.out.println("Full buses: " + full);\n'
                'System.out.println("In last bus: " + lastBus);\n'
                'System.out.println("Buses to order: " + order);')],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-div-rt-date-number", title="Дата одним числом",
        given=[("int", "date")],
        variants=[{"date": "20261028"}, {"date": "19990315"}, {"date": "20080901"}],
        hidden=[{"date": "20000101"}, {"date": "20010101"}, {"date": "18991231"}, {"date": "21000630"}],
        intro="Программа хранит дату одним восьмизначным числом: сначала год, потом две цифры месяца и две цифры дня. "
              "Например, `20261028` — это 28 октября 2026 года. Число записано в поле `date`. Нужно разобрать его на части "
              "и узнать век: годы 1901–2000 — это 20 век, 2001–2100 — 21 век.",
        steps=["Заведи `int year` — год: первые четыре цифры числа.",
               "Заведи `int month` — месяц: третья и четвёртая цифры с конца.",
               "Заведи `int day` — день: две последние цифры.",
               "Заведи `int century` — век: `(year - 1) / 100 + 1`.",
               "Выведи четыре строки: `Day: `, `Month: `, `Year: `, `Century: ` — после каждой надписи её число."],
        hint="Деление на 100 «отрезает» две последние цифры, а остаток от деления на 100 их оставляет: `20261028 / 100` — "
             "это `202610`, а `202610 % 100` — это `10`. Век считается от `year - 1`, чтобы 2000 год попал в 20 век.",
        solution='int year = date / 10000;\n'
                 'int month = date / 100 % 100;\n'
                 'int day = date % 100;\n'
                 'int century = (year - 1) / 100 + 1;\n'
                 'System.out.println("Day: " + day);\n'
                 'System.out.println("Month: " + month);\n'
                 'System.out.println("Year: " + year);\n'
                 'System.out.println("Century: " + century);',
        wrong=[("месяц как date / 100: получаются год и месяц вместе",
                'int year = date / 10000;\n'
                'int month = date / 100;\n'
                'int day = date % 100;\n'
                'int century = (year - 1) / 100 + 1;\n'
                'System.out.println("Day: " + day);\n'
                'System.out.println("Month: " + month);\n'
                'System.out.println("Year: " + year);\n'
                'System.out.println("Century: " + century);'),
               ("век как year / 100 + 1: 2000 год попадает в 21 век",
                'int year = date / 10000;\n'
                'int month = date / 100 % 100;\n'
                'int day = date % 100;\n'
                'int century = year / 100 + 1;\n'
                'System.out.println("Day: " + day);\n'
                'System.out.println("Month: " + month);\n'
                'System.out.println("Year: " + year);\n'
                'System.out.println("Century: " + century);')],
        constructs=["assignment"],
    ),
]
