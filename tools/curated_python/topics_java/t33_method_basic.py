"""METHOD_BASIC — «Методы» (Java): свой static-метод класса Solution, его вызов из main, return. Taught before:
everything up to iterating an array (conditions, loops, arrays, .length, for-each). Not yet: own classes.

Output tasks here need a method of Solution besides main, but JavaOutputTask puts `solution` and `wrong` inside main
(and closes main and the class itself). `with_method` therefore closes main early and leaves the method's last brace
to the template — the reference and wrong sources compile and run normally, only their indentation looks odd; the
student never sees them. Checks look the method up by reflection: its exact signature and, where it returns a
value, its answer on one call."""
from java_tasks import JavaFunctionTask, JavaOutputTask

SKILL = "METHOD_BASIC"


def with_method(main: str, method: str) -> str:
    """Body of main followed by a static method of Solution (see the module docstring)."""
    method = method.strip()
    assert method.endswith("}"), method
    return main.rstrip() + "\n}\n\n" + method[:-1].rstrip()


BADGE = ('static void printBadge(String name) {{\n    System.out.println("Шахматный турнир");\n'
         '    System.out.println("Участник: " + {who});\n}}')
BADGE_CHECKS = (
    'try {\n'
    '    Method m = Solution.class.getDeclaredMethod("printBadge", String.class);\n'
    '    need(Modifier.isStatic(m.getModifiers()) && m.getReturnType() == void.class, '
    '"Объяви метод так: static void printBadge(String name) — он только печатает бейдж и ничего не возвращает");\n'
    '} catch (NoSuchMethodException e) {\n'
    '    need(false, "Создай в классе Solution, рядом с main, метод static void printBadge(String name) и вызывай его из main");\n'
    '}')

TO_MINUTES = 'static int toMinutes(int hours, int minutes) {\n    return hours * 60 + minutes;\n}'
TO_MINUTES_CHECKS = (
    'try {\n'
    '    Method m = Solution.class.getDeclaredMethod("toMinutes", int.class, int.class);\n'
    '    need(Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, '
    '"Объяви метод так: static int toMinutes(int hours, int minutes) — он возвращает число минут");\n'
    '    m.setAccessible(true);\n'
    '    need((int) m.invoke(null, 2, 5) == 125, '
    '"Метод toMinutes должен возвращать через return длительность в минутах: toMinutes(2, 5) — это 125");\n'
    '} catch (NoSuchMethodException e) {\n'
    '    need(false, "Создай в классе Solution, рядом с main, метод static int toMinutes(int hours, int minutes) и вызывай его из main");\n'
    '}')
FILM_MAIN = ('int first = toMinutes(hours1, minutes1);\nint second = toMinutes(hours2, minutes2);\n'
             'System.out.println("Первый фильм: " + first + " мин.");\nSystem.out.println("Второй фильм: " + second + " мин.");\n')

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-mb-chess-badge", title="Бейджи для турнира",
        given=[("String", "player1"), ("String", "player2")],
        variants=[{"player1": '"Аня"', "player2": '"Борис"'}, {"player1": '"Тимур"', "player2": '"Вера"'},
                  {"player1": '"Олег"', "player2": '"Зарина"'}],
        hidden=[{"player1": '"Ян"', "player2": '"Мила"'}, {"player1": '"Глеб"', "player2": '"Соня"'},
                {"player1": '"Ульяна"', "player2": '"Ростислав"'}],
        intro="Ты печатаешь бейджи для шахматного турнира. Все бейджи одинаковые, отличается только имя участника, — "
              "поэтому печать бейджа удобно один раз описать в методе и вызывать его для каждого участника. "
              "Имена участников записаны в поля `player1` и `player2`.",
        steps=["Создай в классе `Solution` рядом с методом `main` (но не внутри него) метод `static void printBadge(String name)`.",
               "Метод печатает бейдж из двух строк: `Шахматный турнир` и `Участник: …` — вместо многоточия имя "
               "из параметра `name`.",
               "В `main` вызови `printBadge` два раза: сначала для `player1`, потом для `player2`."],
        hint="Сам по себе метод ничего не делает: его код выполнится, только когда ты его вызовешь — напишешь имя метода "
             "и в скобках аргумент. Внутри метода используй параметр `name`, а не поля: тогда один и тот же метод "
             "напечатает бейдж для любого имени.",
        solution=with_method("printBadge(player1);\nprintBadge(player2);", BADGE.format(who="name")),
        wrong=[("внутри метода печатает поле player1 вместо параметра name: на обоих бейджах одно имя",
                with_method("printBadge(player1);\nprintBadge(player2);", BADGE.format(who="player1"))),
               ("вызывает метод только для первого участника",
                with_method("printBadge(player1);", BADGE.format(who="name")))],
        constructs=["function"],
        checks=BADGE_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-mb-film-minutes", title="Киномарафон",
        given=[("int", "hours1"), ("int", "minutes1"), ("int", "hours2"), ("int", "minutes2")],
        variants=[{"hours1": "2", "minutes1": "15", "hours2": "1", "minutes2": "38"},
                  {"hours1": "1", "minutes1": "45", "hours2": "2", "minutes2": "5"},
                  {"hours1": "3", "minutes1": "2", "hours2": "1", "minutes2": "30"}],
        hidden=[{"hours1": "0", "minutes1": "50", "hours2": "1", "minutes2": "0"},
                {"hours1": "2", "minutes1": "0", "hours2": "2", "minutes2": "0"},
                {"hours1": "1", "minutes1": "59", "hours2": "3", "minutes2": "1"},
                {"hours1": "1", "minutes1": "30", "hours2": "0", "minutes2": "45"}],
        intro="Вечером у тебя киномарафон из двух фильмов. На афише длительность указана в часах и минутах: первый фильм "
              "идёт {hours1} ч {minutes1} мин (поля `hours1` и `minutes1`), второй — {hours2} ч {minutes2} мин "
              "(поля `hours2` и `minutes2`). Удобнее перевести всё в минуты.",
        steps=["Создай в классе `Solution` рядом с `main` метод `static int toMinutes(int hours, int minutes)`. "
               "Он **возвращает** через `return` длительность в минутах: часы, умноженные на 60, плюс минуты.",
               "В `main` вызови `toMinutes` для каждого фильма и выведи две строки: `Первый фильм: … мин.` "
               "и `Второй фильм: … мин.`",
               "Третьей строкой выведи `Всего: … мин.` — сколько минут идут оба фильма вместе."],
        hint="Вызов `toMinutes(...)` превращается в число, которое вернул метод. Его можно сохранить в переменную "
             "типа `int` и дальше работать с ней, как с любым числом.",
        solution=with_method(FILM_MAIN + 'System.out.println("Всего: " + (first + second) + " мин.");', TO_MINUTES),
        wrong=[("склеивает два числа как строки в последней строке",
                with_method(FILM_MAIN + 'System.out.println("Всего: " + first + second + " мин.");', TO_MINUTES)),
               ("дважды считает первый фильм: во втором вызове те же аргументы",
                with_method(FILM_MAIN.replace("toMinutes(hours2, minutes2)", "toMinutes(hours1, minutes1)")
                            + 'System.out.println("Всего: " + (first + second) + " мин.");', TO_MINUTES))],
        constructs=["function", "return"],
        checks=TO_MINUTES_CHECKS,
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=3, slug="java-mb-count-passed", title="Сколько зачётов",
        function="countPassed",
        variants=[{"pass": 50}, {"pass": 60}, {"pass": 40}],
        intro="За контрольную ставят зачёт, если ученик набрал {pass} баллов или больше. Учитель хочет быстро узнать, "
              "сколько учеников получили зачёт.",
        steps=["Допиши метод `countPassed(int[] scores)`: в массиве `scores` записаны баллы учеников, по одному числу "
               "на ученика.",
               "Метод возвращает, сколько учеников набрали {pass} баллов или больше.",
               "Массив может быть любой длины, даже пустым — тогда зачётов 0."],
        hint="Заведи счётчик до цикла и увеличивай его, когда ученик набрал достаточно баллов. А `return` напиши "
             "после цикла: `return` сразу завершает метод, и внутри цикла он сработал бы на первом же ученике.",
        starter="public class Solution {{\n    static int countPassed(int[] scores) {{\n        // Напиши решение здесь\n"
                "        return 0;\n    }}\n}}\n",
        solution="public class Solution {{\n    static int countPassed(int[] scores) {{\n        int count = 0;\n"
                 "        for (int score : scores) {{\n            if (score >= {pass}) {{\n                count++;\n"
                 "            }}\n        }}\n        return count;\n    }}\n}}\n",
        inputs=["new int[]{72, 38, 50, 91}", "new int[]{10, 20}", "new int[]{60, 45, 40, 59, 61, 100}", "new int[]{}",
                "new int[]{50}", "new int[]{39, 60, 50, 0, 49, 80, 99}", "new int[]{30, 75, 90}"],
        wrong=[("строгое сравнение: ровно проходной балл не засчитывается",
                "public class Solution {{\n    static int countPassed(int[] scores) {{\n        int count = 0;\n"
                "        for (int score : scores) {{\n            if (score > {pass}) {{\n                count++;\n"
                "            }}\n        }}\n        return count;\n    }}\n}}\n"),
               ("return внутри цикла: метод заканчивает работу на первом ученике",
                "public class Solution {{\n    static int countPassed(int[] scores) {{\n        int count = 0;\n"
                "        for (int score : scores) {{\n            if (score >= {pass}) {{\n                count++;\n"
                "            }}\n            return count;\n        }}\n        return count;\n    }}\n}}\n")],
    ),
]
