"""SWITCH_BASIC — «Оператор switch» (Java). Taught before: println, variables, assignment, arithmetic, primitive types
(char), String, / and %, += -= ++, if/else, comparisons, && || !. The point: switch on a value, case branches with
break, several values in one branch, default. Not yet: loops, arrays, own methods.

The platform's syntax-tree constructs have no «switch», so `checks` looks for it in the compiled class without
reflection: it reads Solution.class through getResourceAsStream (also works in Piston's single-file mode, checked on
Java 15) and walks the bytecode of every method looking for tableswitch/lookupswitch — javac compiles every switch
(int, char, String, arrow or colon form, switch expression) to one of them, and an if chain never. If the class bytes
cannot be read or parsed, the check passes rather than reject a correct solution."""
from java_tasks import JavaOutputTask

SKILL = "SWITCH_BASIC"

SWITCH_CHECK = """boolean usesSwitch = true;
try (InputStream in = Solution.class.getResourceAsStream("Solution.class")) {
    if (in != null) {
        DataInputStream d = new DataInputStream(new ByteArrayInputStream(in.readAllBytes()));
        d.skipBytes(8);
        int poolSize = d.readUnsignedShort();
        String[] utf = new String[poolSize];
        for (int i = 1; i < poolSize; i++) {
            int tag = d.readUnsignedByte();
            if (tag == 1) utf[i] = d.readUTF();
            else if (tag == 5 || tag == 6) { d.skipBytes(8); i++; }
            else if (tag == 7 || tag == 8 || tag == 16 || tag == 19 || tag == 20) d.skipBytes(2);
            else if (tag == 15) d.skipBytes(3);
            else d.skipBytes(4);
        }
        d.skipBytes(6);
        d.skipBytes(2 * d.readUnsignedShort());
        usesSwitch = false;
        for (int part = 0; part < 2; part++) {
            int members = d.readUnsignedShort();
            for (int m = 0; m < members; m++) {
                d.skipBytes(6);
                int attributes = d.readUnsignedShort();
                for (int k = 0; k < attributes; k++) {
                    String name = utf[d.readUnsignedShort()];
                    byte[] a = new byte[d.readInt()];
                    d.readFully(a);
                    if (part == 0 || !"Code".equals(name)) continue;
                    int end = 8 + (((a[4] & 255) << 24) | ((a[5] & 255) << 16) | ((a[6] & 255) << 8) | (a[7] & 255));
                    for (int pc = 8; pc < end && !usesSwitch; ) {
                        int op = a[pc] & 255;
                        if (op == 0xaa || op == 0xab) usesSwitch = true;
                        else if (op == 0xc4) pc += (a[pc + 1] & 255) == 0x84 ? 6 : 4;
                        else if (op == 0x10 || op == 0x12 || (op >= 0x15 && op <= 0x19) || (op >= 0x36 && op <= 0x3a) || op == 0xa9 || op == 0xbc) pc += 2;
                        else if (op == 0x11 || op == 0x13 || op == 0x14 || op == 0x84 || (op >= 0x99 && op <= 0xa8) || (op >= 0xb2 && op <= 0xb8) || op == 0xbb || op == 0xbd || op == 0xc0 || op == 0xc1 || op == 0xc6 || op == 0xc7) pc += 3;
                        else if (op == 0xc5) pc += 4;
                        else if (op == 0xb9 || op == 0xba || op == 0xc8 || op == 0xc9) pc += 5;
                        else pc += 1;
                    }
                }
            }
        }
    }
} catch (Exception e) {
    usesSwitch = true;
}
need(usesSwitch, "%s");"""


def uses_switch(field: str) -> str:
    return SWITCH_CHECK % (f"Используй оператор switch по полю {field}: выбор одного варианта из многих "
                           f"по значению так читается проще, чем цепочка if")


TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-switch-school-clubs", title="Кружок на сегодня",
        given=[("int", "day")],
        variants=[{"day": "3"}, {"day": "5"}, {"day": "6"}],
        hidden=[{"day": "1"}, {"day": "2"}, {"day": "4"}, {"day": "7"}],
        intro="После уроков в школе работают кружки, и у каждого дня недели — свой. "
              "Номер дня недели (1 — понедельник, 7 — воскресенье) записан в поле `day`.",
        steps=["Сделай `switch` по `day` и выведи название кружка: 1 — `Chess`, 2 — `Drawing`, 3 — `Swimming`, "
               "4 — `Robotics`, 5 — `Football`.",
               "Для любого другого номера (ветка `default`) выведи `No clubs, rest day`.",
               "Программа должна выводить ровно одну строку."],
        hint="Заканчивай каждую ветку `case` командой `break`: без неё Java продолжит выполнять следующие ветки "
             "и выведет лишние строки.",
        solution="""switch (day) {
    case 1:
        System.out.println("Chess");
        break;
    case 2:
        System.out.println("Drawing");
        break;
    case 3:
        System.out.println("Swimming");
        break;
    case 4:
        System.out.println("Robotics");
        break;
    case 5:
        System.out.println("Football");
        break;
    default:
        System.out.println("No clubs, rest day");
}""",
        wrong=[("нет break: после нужного кружка печатаются все следующие",
                """switch (day) {
    case 1:
        System.out.println("Chess");
    case 2:
        System.out.println("Drawing");
    case 3:
        System.out.println("Swimming");
    case 4:
        System.out.println("Robotics");
    case 5:
        System.out.println("Football");
    default:
        System.out.println("No clubs, rest day");
}"""),
               ("нет ветки default: в выходные ничего не выводится",
                """switch (day) {
    case 1:
        System.out.println("Chess");
        break;
    case 2:
        System.out.println("Drawing");
        break;
    case 3:
        System.out.println("Swimming");
        break;
    case 4:
        System.out.println("Robotics");
        break;
    case 5:
        System.out.println("Football");
        break;
}""")],
        checks=uses_switch("day"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-switch-season", title="Время года по месяцу",
        given=[("int", "month")],
        variants=[{"month": "1"}, {"month": "7"}, {"month": "10"}],
        hidden=[{"month": "12"}, {"month": "2"}, {"month": "3"}, {"month": "5"}, {"month": "6"}, {"month": "8"},
                {"month": "9"}, {"month": "11"}, {"month": "13"}, {"month": "0"}],
        intro="Приложение-календарь показывает время года по номеру месяца. Номер месяца записан в поле `month`: "
              "1 — январь, 12 — декабрь.",
        steps=["Сделай `switch` по `month` и выведи время года: для 12, 1 и 2 — `Winter`, для 3, 4 и 5 — `Spring`, "
               "для 6, 7 и 8 — `Summer`, для 9, 10 и 11 — `Autumn`.",
               "Если месяца с таким номером нет (ветка `default`), выведи `No month number …`, подставив `month`.",
               "Программа должна выводить ровно одну строку."],
        hint="Несколько значений могут вести в одну ветку: их можно перечислить через запятую — `case 3, 4, 5:`. "
             "Тогда каждое время года — это одна ветка со своим `break`.",
        solution="""switch (month) {
    case 12, 1, 2:
        System.out.println("Winter");
        break;
    case 3, 4, 5:
        System.out.println("Spring");
        break;
    case 6, 7, 8:
        System.out.println("Summer");
        break;
    case 9, 10, 11:
        System.out.println("Autumn");
        break;
    default:
        System.out.println("No month number " + month);
}""",
        wrong=[("декабрь забыт: для 12 выводится, что такого месяца нет",
                """switch (month) {
    case 1, 2:
        System.out.println("Winter");
        break;
    case 3, 4, 5:
        System.out.println("Spring");
        break;
    case 6, 7, 8:
        System.out.println("Summer");
        break;
    case 9, 10, 11:
        System.out.println("Autumn");
        break;
    default:
        System.out.println("No month number " + month);
}"""),
               ("нет break после «Summer»: летние месяцы печатают ещё и «Autumn»",
                """switch (month) {
    case 12, 1, 2:
        System.out.println("Winter");
        break;
    case 3, 4, 5:
        System.out.println("Spring");
        break;
    case 6, 7, 8:
        System.out.println("Summer");
    case 9, 10, 11:
        System.out.println("Autumn");
        break;
    default:
        System.out.println("No month number " + month);
}""")],
        checks=uses_switch("month"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-switch-calculator", title="Калькулятор на switch",
        given=[("int", "a"), ("int", "b"), ("char", "op")],
        variants=[{"a": "7", "b": "3", "op": "'*'"}, {"a": "17", "b": "5", "op": "'/'"}, {"a": "12", "b": "20", "op": "'-'"}],
        hidden=[{"a": "4", "b": "5", "op": "'+'"}, {"a": "8", "b": "0", "op": "'/'"}, {"a": "9", "b": "2", "op": "'/'"},
                {"a": "6", "b": "6", "op": "'-'"}, {"a": "3", "b": "4", "op": "'%'"}, {"a": "0", "b": "7", "op": "'*'"}],
        intro="Простой калькулятор получает два целых числа `a` и `b` и знак действия `op` — один символ: "
              "`'+'`, `'-'`, `'*'` или `'/'`.",
        steps=["Сделай `switch` по `op` и для каждого из четырёх знаков выведи пример с ответом: число `a`, пробел, "
               "знак, пробел, число `b`, затем знак `=` с пробелами по бокам и результат, например `7 * 3 = 21`.",
               "Деление целочисленное: `a / b`. Но если делить нужно на 0, вместо примера выведи `You cannot divide by zero`.",
               "Для любого другого знака (ветка `default`) выведи `Unknown operation`."],
        hint="Внутри ветки `case '/'` можно написать обычный `if`. А чтобы числа в ответе сложились, а не склеились "
             "в строку, возьми действие в скобки: `\" = \" + (a + b)`.",
        solution="""switch (op) {
    case '+':
        System.out.println(a + " + " + b + " = " + (a + b));
        break;
    case '-':
        System.out.println(a + " - " + b + " = " + (a - b));
        break;
    case '*':
        System.out.println(a + " * " + b + " = " + (a * b));
        break;
    case '/':
        if (b == 0) {
            System.out.println("You cannot divide by zero");
        } else {
            System.out.println(a + " / " + b + " = " + (a / b));
        }
        break;
    default:
        System.out.println("Unknown operation");
}""",
        wrong=[("нет break после '*': при умножении выводится ещё и деление",
                """switch (op) {
    case '+':
        System.out.println(a + " + " + b + " = " + (a + b));
        break;
    case '-':
        System.out.println(a + " - " + b + " = " + (a - b));
        break;
    case '*':
        System.out.println(a + " * " + b + " = " + (a * b));
    case '/':
        if (b == 0) {
            System.out.println("You cannot divide by zero");
        } else {
            System.out.println(a + " / " + b + " = " + (a / b));
        }
        break;
    default:
        System.out.println("Unknown operation");
}"""),
               ("сумма без скобок: числа склеиваются в строку (4 + 5 = 45)",
                """switch (op) {
    case '+':
        System.out.println(a + " + " + b + " = " + a + b);
        break;
    case '-':
        System.out.println(a + " - " + b + " = " + (a - b));
        break;
    case '*':
        System.out.println(a + " * " + b + " = " + (a * b));
        break;
    case '/':
        if (b == 0) {
            System.out.println("You cannot divide by zero");
        } else {
            System.out.println(a + " / " + b + " = " + (a / b));
        }
        break;
    default:
        System.out.println("Unknown operation");
}""")],
        checks=uses_switch("op"),
    ),
]
