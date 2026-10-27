"""METHOD_BASIC — «Методы» (Java): свой static-метод класса Solution, его вызов из main, return. Taught before:
everything up to iterating an array (conditions, loops, arrays, .length, for-each). Not yet: own classes.

Output tasks here need a method of Solution besides main: `with_method` of the regular file closes main early and
leaves the method's last brace to the template. Checks look the method up by reflection: its exact signature and,
where it returns a value, its answer on one call."""
from java_tasks import JavaFunctionTask, JavaOutputTask
from topics_java.t33_method_basic import with_method

SKILL = "METHOD_BASIC"

DRAW_LINE = ('static void drawLine(int length) {{\n    String line = "";\n    for (int i = 0; i < {bound}; i++) {{\n'
             '        line += "=";\n    }}\n    System.out.println(line);\n}}')
DRAW_LINE_CHECKS = (
    'try {\n'
    '    Method m = Solution.class.getDeclaredMethod("drawLine", int.class);\n'
    '    need(Modifier.isStatic(m.getModifiers()) && m.getReturnType() == void.class, '
    '"Объяви метод так: static void drawLine(int length) — он только печатает линию и ничего не возвращает");\n'
    '} catch (NoSuchMethodException e) {\n'
    '    need(false, "Создай в классе Solution, рядом с main, метод static void drawLine(int length) и вызывай его из main");\n'
    '}')
POSTER_MAIN = "drawLine(width);\nSystem.out.println(title);\ndrawLine(width);"

BONUS = ('static int bonus(int purchase) {\n    int points = purchase / 100;\n    if (purchase >= 2000) {\n        points *= 2;\n'
         '    }\n    return points;\n}')
BONUS_CHECKS = (
    'try {\n'
    '    Method m = Solution.class.getDeclaredMethod("bonus", int.class);\n'
    '    need(Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, '
    '"Объяви метод так: static int bonus(int purchase) — он возвращает число баллов");\n'
    '    m.setAccessible(true);\n'
    '    need((int) m.invoke(null, 2550) == 50 && (int) m.invoke(null, 199) == 1, '
    '"Метод bonus должен возвращать через return число баллов: bonus(199) — это 1, bonus(2550) — это 50");\n'
    '} catch (NoSuchMethodException e) {\n'
    '    need(false, "Создай в классе Solution, рядом с main, метод static int bonus(int purchase) и вызывай его из main");\n'
    '}')
BONUS_MAIN = ('int first = bonus(monday);\nint second = bonus(friday);\nSystem.out.println("Monday: " + first + " points");\n'
              'System.out.println("Friday: " + second + " points");\n')

TOTAL_FINE = ("public class Solution {{\n    static int totalFine(int[] speeds) {{\n        int total = 0;\n"
              "        for (int s : speeds) {{\n            if (s > {limit} + 20) {{\n                total += 1000;\n"
              "            }} else if (s > {limit}) {{\n                total += 500;\n            }}\n        }}\n"
              "        return total;\n    }}\n}}\n")

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-mb-rt-poster-lines", title="Афиша с рамкой",
        given=[("String", "title"), ("int", "width")],
        variants=[{"title": '"School concert"', "width": "14"}, {"title": '"Chess club"', "width": "10"},
                  {"title": '"Book fair"', "width": "12"}],
        hidden=[{"title": '"Quiz"', "width": "4"}, {"title": '"Football match tonight"', "width": "22"},
                {"title": '"Art"', "width": "1"}],
        intro="Ты печатаешь афишу: название события, а над ним и под ним — линия из знаков `=`. Название записано "
              "в поле `title`, а длина линии — в поле `width`. Линия нужна дважды, поэтому её печать удобно описать "
              "в методе и вызвать два раза.",
        steps=["Создай в классе `Solution` рядом с методом `main` (но не внутри него) метод `static void drawLine(int length)`.",
               "Метод печатает одну строку из `length` знаков `=`: собери её циклом в переменной типа `String` "
               "и выведи после цикла.",
               "В `main` вызови `drawLine(width)`, потом выведи `title`, потом снова вызови `drawLine(width)`."],
        hint="Внутри метода работай с параметром `length`: при вызове `drawLine(width)` в него попадает значение `width`. "
             "Строку можно наращивать так: `line += \"=\";` — начни с пустой строки `\"\"`.",
        solution=with_method(POSTER_MAIN, DRAW_LINE.format(bound="length")),
        wrong=[("цикл до <= length: в линии на один знак больше",
                with_method(POSTER_MAIN, DRAW_LINE.format(bound="length + 1"))),
               ("вызывает метод только над названием: нижней линии нет",
                with_method("drawLine(width);\nSystem.out.println(title);", DRAW_LINE.format(bound="length")))],
        constructs=["function", "for"],
        checks=DRAW_LINE_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-mb-rt-bonus-points", title="Бонусные баллы",
        given=[("int", "monday"), ("int", "friday")],
        variants=[{"monday": "850", "friday": "2400"}, {"monday": "1999", "friday": "350"},
                  {"monday": "3000", "friday": "1270"}],
        hidden=[{"monday": "2000", "friday": "99"}, {"monday": "100", "friday": "1999"},
                {"monday": "5050", "friday": "2001"}, {"monday": "0", "friday": "700"}],
        intro="В магазине за покупки начисляют бонусные баллы: 1 балл за каждые полные 100 руб., а за покупку от "
              "2000 руб. баллов вдвое больше. На этой неделе Аня покупала в понедельник на {monday} руб. (поле `monday`) "
              "и в пятницу на {friday} руб. (поле `friday`).",
        steps=["Создай в классе `Solution` рядом с `main` метод `static int bonus(int purchase)`. Он **возвращает** "
               "через `return` число баллов: `purchase / 100`, а если `purchase` не меньше 2000 — вдвое больше.",
               "В `main` вызови `bonus` для каждой покупки и выведи две строки: `Monday: … points` и `Friday: … points`.",
               "Третьей строкой выведи `Week: … points` — сколько баллов за обе покупки вместе."],
        hint="Вызов `bonus(monday)` превращается в число, которое вернул метод: его можно сохранить в переменную `int`. "
             "Внутри метода можно использовать `if`, как и в `main`.",
        solution=with_method(BONUS_MAIN + 'System.out.println("Week: " + (first + second) + " points");', BONUS),
        wrong=[("строгое сравнение: покупка ровно на 2000 руб. без удвоения",
                with_method(BONUS_MAIN + 'System.out.println("Week: " + (first + second) + " points");',
                            BONUS.replace("purchase >= 2000", "purchase > 2000"))),
               ("сумма без скобок: баллы склеиваются в одну строку",
                with_method(BONUS_MAIN + 'System.out.println("Week: " + first + second + " points");', BONUS))],
        constructs=["function", "return"],
        checks=BONUS_CHECKS,
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=3, slug="java-mb-rt-speed-fines", title="Штрафы за скорость",
        function="totalFine",
        variants=[{"limit": 60}, {"limit": 90}, {"limit": 40}],
        intro="Камера на дороге с ограничением {limit} км/ч записала скорости машин за час. Превышение до 20 км/ч "
              "включительно стоит 500 руб., а больше чем на 20 км/ч — 1000 руб. Кто едет не быстрее {limit} км/ч, "
              "штраф не получает.",
        steps=["Допиши метод `totalFine(int[] speeds)`: в массиве `speeds` записаны скорости машин в км/ч.",
               "Метод возвращает общую сумму штрафов за все машины в рублях.",
               "Массив может быть любой длины, даже пустым — тогда штрафов 0."],
        hint="Сначала проверь большое превышение (скорость больше `{limit} + 20`), а потом обычное (больше {limit}): "
             "иначе каждая быстрая машина попадёт в первую же ветку. `return` пиши после цикла.",
        starter="public class Solution {{\n    static int totalFine(int[] speeds) {{\n        // Напиши решение здесь\n"
                "        return 0;\n    }}\n}}\n",
        solution=TOTAL_FINE,
        inputs=["new int[]{70, 45, 100}", "new int[]{30, 40}", "new int[]{}", "new int[]{60, 61, 80, 81, 41}",
                "new int[]{150}", "new int[]{90, 91, 110, 111, 39, 62}", "new int[]{55, 85, 95, 120, 65, 75}"],
        wrong=[("большое превышение с >=: ровно +20 км/ч штрафуется на 1000 руб.",
                TOTAL_FINE.replace("s > {limit} + 20", "s >= {limit} + 20")),
               ("порядок проверок перепутан: любое превышение стоит 500 руб.",
                TOTAL_FINE.replace("if (s > {limit} + 20) {{\n                total += 1000;\n            }} else if (s > {limit}) {{\n"
                                   "                total += 500;",
                                   "if (s > {limit}) {{\n                total += 500;\n            }} else if (s > {limit} + 20) {{\n"
                                   "                total += 1000;"))],
    ),
]
