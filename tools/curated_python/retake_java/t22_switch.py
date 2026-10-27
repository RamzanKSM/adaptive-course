"""SWITCH_BASIC — «Оператор switch» (Java). Taught before: println, variables, assignment, arithmetic, primitive types
(char), String, / and %, += -= ++, if/else, comparisons, && || !. The point: switch on a value, case branches with
break, several values in one branch, default. Not yet: loops, arrays, own methods.

The platform's syntax-tree constructs have no «switch»: `checks` reuses the bytecode check of the regular file."""
from java_tasks import JavaOutputTask
from topics_java.t22_switch import uses_switch

SKILL = "SWITCH_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-switch-rt-smart-speaker", title="Умная колонка",
        given=[("String", "command")],
        variants=[{"command": '"play"'}, {"command": '"louder"'}, {"command": '"stop"'}],
        hidden=[{"command": '"play"'}, {"command": '"stop"'}, {"command": '"louder"'}, {"command": '"quieter"'},
                {"command": '"dance"'}, {"command": '"Play"'}],
        intro="Умная колонка понимает несколько команд. Команда, которую она только что услышала, записана строкой "
              "в поле `command`.",
        steps=["Сделай `switch` по `command` и выведи ответ колонки: `\"play\"` — `Playing music`, "
               "`\"stop\"` — `Music stopped`, `\"louder\"` — `Volume up`, `\"quieter\"` — `Volume down`.",
               "Для любой другой строки (ветка `default`) выведи `Sorry, I did not understand`.",
               "Программа должна выводить ровно одну строку."],
        hint="`switch` работает и со строками: `case \"play\":`. Заканчивай каждую ветку командой `break`, "
             "иначе Java выполнит и следующие ветки.",
        solution="""switch (command) {
    case "play":
        System.out.println("Playing music");
        break;
    case "stop":
        System.out.println("Music stopped");
        break;
    case "louder":
        System.out.println("Volume up");
        break;
    case "quieter":
        System.out.println("Volume down");
        break;
    default:
        System.out.println("Sorry, I did not understand");
}""",
        wrong=[("нет break: после нужного ответа печатаются все следующие",
                """switch (command) {
    case "play":
        System.out.println("Playing music");
    case "stop":
        System.out.println("Music stopped");
    case "louder":
        System.out.println("Volume up");
    case "quieter":
        System.out.println("Volume down");
    default:
        System.out.println("Sorry, I did not understand");
}"""),
               ("нет ветки default: на незнакомую команду колонка молчит",
                """switch (command) {
    case "play":
        System.out.println("Playing music");
        break;
    case "stop":
        System.out.println("Music stopped");
        break;
    case "louder":
        System.out.println("Volume up");
        break;
    case "quieter":
        System.out.println("Volume down");
        break;
}""")],
        checks=uses_switch("command"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-switch-rt-market-shelf", title="Полка на рынке",
        given=[("String", "product")],
        variants=[{"product": '"pear"'}, {"product": '"onion"'}, {"product": '"bread"'}],
        hidden=[{"product": '"apple"'}, {"product": '"pear"'}, {"product": '"plum"'}, {"product": '"carrot"'}, {"product": '"potato"'},
                {"product": '"milk"'}, {"product": '"cherry"'}],
        intro="Продавец на рынке раскладывает товар по полкам: фрукты — на левую, овощи — на правую. "
              "Название товара записано строкой в поле `product`.",
        steps=["Сделай `switch` по `product`: для `\"apple\"`, `\"pear\"` и `\"plum\"` выведи `Fruit: left shelf`, "
               "для `\"carrot\"`, `\"potato\"` и `\"onion\"` — `Vegetable: right shelf`.",
               "Для любого другого товара (ветка `default`) выведи `Unknown product: …`, подставив `product`.",
               "Программа должна выводить ровно одну строку."],
        hint="Несколько значений можно перечислить в одной ветке через запятую: `case \"apple\", \"pear\", \"plum\":`. "
             "Тогда у фруктов и у овощей будет по одной ветке со своим `break`.",
        solution="""switch (product) {
    case "apple", "pear", "plum":
        System.out.println("Fruit: left shelf");
        break;
    case "carrot", "potato", "onion":
        System.out.println("Vegetable: right shelf");
        break;
    default:
        System.out.println("Unknown product: " + product);
}""",
        wrong=[("груша забыта: для pear выводится, что товар неизвестен",
                """switch (product) {
    case "apple", "plum":
        System.out.println("Fruit: left shelf");
        break;
    case "carrot", "potato", "onion":
        System.out.println("Vegetable: right shelf");
        break;
    default:
        System.out.println("Unknown product: " + product);
}"""),
               ("нет break после фруктов: фрукт печатает ещё и строку про овощи",
                """switch (product) {
    case "apple", "pear", "plum":
        System.out.println("Fruit: left shelf");
    case "carrot", "potato", "onion":
        System.out.println("Vegetable: right shelf");
        break;
    default:
        System.out.println("Unknown product: " + product);
}""")],
        checks=uses_switch("product"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-switch-rt-timer-units", title="Таймер в секундах",
        given=[("int", "amount"), ("char", "unit")],
        variants=[{"amount": "90", "unit": "'m'"}, {"amount": "4000", "unit": "'s'"}, {"amount": "2", "unit": "'h'"}],
        hidden=[{"amount": "59", "unit": "'s'"}, {"amount": "3600", "unit": "'s'"}, {"amount": "75", "unit": "'m'"},
                {"amount": "3", "unit": "'h'"}, {"amount": "10", "unit": "'d'"}, {"amount": "5", "unit": "'x'"}],
        intro="Кухонный таймер принимает время числом `amount` и единицей измерения `unit` — одним символом: "
              "`'s'` — секунды, `'m'` — минуты, `'h'` — часы. Внутри таймер всё считает в секундах.",
        steps=["Сделай `switch` по `unit` и узнай, сколько секунд в одной единице: `'s'` — 1, `'m'` — 60, `'h'` — 3600.",
               "Если символ другой (ветка `default`), выведи одну строку `Unknown unit: …`, подставив `unit`, и больше ничего.",
               "Иначе посчитай секунды: `amount`, умноженное на число секунд в единице, и выведи строку в формате "
               "`90 m = 5400 s` (`amount`, пробел, `unit`, затем ` = `, секунды и ` s`).",
               "Следующей строкой выведи `Hours: H, minutes: M`, где H — сколько полных часов в этих секундах, "
               "а M — сколько полных минут остаётся сверх полных часов."],
        hint="Заведи до `switch` переменную со значением 0 и в ветках `case` только присваивай её; после `switch` "
             "значение 0 означает неизвестную единицу. Часы — это `seconds / 3600`, а минуты сверх них — "
             "`seconds % 3600 / 60`.",
        solution="""int perUnit = 0;
switch (unit) {
    case 's':
        perUnit = 1;
        break;
    case 'm':
        perUnit = 60;
        break;
    case 'h':
        perUnit = 3600;
        break;
    default:
        perUnit = 0;
}
if (perUnit == 0) {
    System.out.println("Unknown unit: " + unit);
} else {
    int seconds = amount * perUnit;
    System.out.println(amount + " " + unit + " = " + seconds + " s");
    System.out.println("Hours: " + seconds / 3600 + ", minutes: " + seconds % 3600 / 60);
}""",
        wrong=[("нет break после 'm': минуты считаются как часы",
                """int perUnit = 0;
switch (unit) {
    case 's':
        perUnit = 1;
        break;
    case 'm':
        perUnit = 60;
    case 'h':
        perUnit = 3600;
        break;
    default:
        perUnit = 0;
}
if (perUnit == 0) {
    System.out.println("Unknown unit: " + unit);
} else {
    int seconds = amount * perUnit;
    System.out.println(amount + " " + unit + " = " + seconds + " s");
    System.out.println("Hours: " + seconds / 3600 + ", minutes: " + seconds % 3600 / 60);
}"""),
               ("минуты без остатка: печатает все минуты, а не только сверх полных часов",
                """int perUnit = 0;
switch (unit) {
    case 's':
        perUnit = 1;
        break;
    case 'm':
        perUnit = 60;
        break;
    case 'h':
        perUnit = 3600;
        break;
    default:
        perUnit = 0;
}
if (perUnit == 0) {
    System.out.println("Unknown unit: " + unit);
} else {
    int seconds = amount * perUnit;
    System.out.println(amount + " " + unit + " = " + seconds + " s");
    System.out.println("Hours: " + seconds / 3600 + ", minutes: " + seconds / 60);
}""")],
        constructs=["if"],
        checks=uses_switch("unit"),
    ),
]
