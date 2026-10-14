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


BADGE = ('static void printBadge(String name) {{\n    System.out.println("Chess tournament");\n'
         '    System.out.println("Player: " + {who});\n}}')
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
             'System.out.println("First film: " + first + " min");\nSystem.out.println("Second film: " + second + " min");\n')

ANNOUNCE = ('static void announce(String city) {{\n    System.out.println("Attention, please!");\n'
            '    System.out.println("Train to " + {where} + " is boarding");\n}}')
ANNOUNCE_CHECKS = (
    'try {\n'
    '    Method m = Solution.class.getDeclaredMethod("announce", String.class);\n'
    '    need(Modifier.isStatic(m.getModifiers()) && m.getReturnType() == void.class, '
    '"Объяви метод так: static void announce(String city) — он только печатает объявление и ничего не возвращает");\n'
    '} catch (NoSuchMethodException e) {\n'
    '    need(false, "Создай в классе Solution, рядом с main, метод static void announce(String city) и вызывай его из main");\n'
    '}')

BOXES = ('static int boxes(int eggs) {\n    int count = eggs / 10;\n    if (eggs % 10 > 0) {\n        count++;\n    }\n'
         '    return count;\n}')
BOXES_CHECKS = (
    'try {\n'
    '    Method m = Solution.class.getDeclaredMethod("boxes", int.class);\n'
    '    need(Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, '
    '"Объяви метод так: static int boxes(int eggs) — он возвращает число коробок");\n'
    '    m.setAccessible(true);\n'
    '    need((int) m.invoke(null, 25) == 3 && (int) m.invoke(null, 30) == 3, '
    '"Метод boxes должен возвращать через return число коробок с учётом неполной: boxes(25) — это 3, boxes(30) — тоже 3");\n'
    '} catch (NoSuchMethodException e) {\n'
    '    need(false, "Создай в классе Solution, рядом с main, метод static int boxes(int eggs) и вызывай его из main");\n'
    '}')
EGGS_MAIN = ('int total = 0;\nfor (int i = 0; i < orders.length; i++) {\n    int count = boxes(orders[i]);\n'
             '    System.out.println("Order " + (i + 1) + ": " + count + " box(es)");\n    total += count;\n}\n'
             'System.out.println("Total: " + total + " box(es)");')

LONGEST_RUN = ("public class Solution {{\n    static int longestRun(int[] steps) {{\n        int best = 0;\n"
               "        int current = 0;\n        for (int s : steps) {{\n            if (s >= {goal}) {{\n"
               "                current++;\n                if (current > best) {{\n                    best = current;\n"
               "                }}\n            }} else {{\n                current = 0;\n            }}\n        }}\n"
               "        return best;\n    }}\n}}\n")

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-mb-chess-badge", title="Бейджи для турнира",
        given=[("String", "player1"), ("String", "player2")],
        variants=[{"player1": '"Anya"', "player2": '"Boris"'}, {"player1": '"Timur"', "player2": '"Vera"'},
                  {"player1": '"Oleg"', "player2": '"Zarina"'}],
        hidden=[{"player1": '"Yan"', "player2": '"Mila"'}, {"player1": '"Gleb"', "player2": '"Sonya"'},
                {"player1": '"Ulyana"', "player2": '"Rostislav"'}],
        intro="Ты печатаешь бейджи для шахматного турнира. Все бейджи одинаковые, отличается только имя участника, — "
              "поэтому печать бейджа удобно один раз описать в методе и вызывать его для каждого участника. "
              "Имена участников записаны в поля `player1` и `player2`.",
        steps=["Создай в классе `Solution` рядом с методом `main` (но не внутри него) метод `static void printBadge(String name)`.",
               "Метод печатает бейдж из двух строк: `Chess tournament` и `Player: …` — вместо многоточия имя "
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
               "В `main` вызови `toMinutes` для каждого фильма и выведи две строки: `First film: … min` "
               "и `Second film: … min`",
               "Третьей строкой выведи `Total: … min` — сколько минут идут оба фильма вместе."],
        hint="Вызов `toMinutes(...)` превращается в число, которое вернул метод. Его можно сохранить в переменную "
             "типа `int` и дальше работать с ней, как с любым числом.",
        solution=with_method(FILM_MAIN + 'System.out.println("Total: " + (first + second) + " min");', TO_MINUTES),
        wrong=[("склеивает два числа как строки в последней строке",
                with_method(FILM_MAIN + 'System.out.println("Total: " + first + second + " min");', TO_MINUTES)),
               ("дважды считает первый фильм: во втором вызове те же аргументы",
                with_method(FILM_MAIN.replace("toMinutes(hours2, minutes2)", "toMinutes(hours1, minutes1)")
                            + 'System.out.println("Total: " + (first + second) + " min");', TO_MINUTES))],
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
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-mb-train-announce", title="Объявления на вокзале",
        given=[("String", "city1"), ("String", "city2"), ("String", "city3")],
        variants=[{"city1": '"Kazan"', "city2": '"Sochi"', "city3": '"Omsk"'},
                  {"city1": '"Tver"', "city2": '"Samara"', "city3": '"Perm"'},
                  {"city1": '"Pskov"', "city2": '"Ufa"', "city3": '"Kursk"'}],
        hidden=[{"city1": '"Tula"', "city2": '"Orel"', "city3": '"Vologda"'},
                {"city1": '"Murmansk"', "city2": '"Kirov"', "city3": '"Anapa"'},
                {"city1": '"Yalta"', "city2": '"Tomsk"', "city3": '"Chita"'}],
        intro="Ты пишешь программу для диктора на вокзале. Перед отправлением каждого поезда звучит одно и то же "
              "объявление, меняется только город. Сегодня отправляются три поезда — города записаны в поля "
              "`city1`, `city2` и `city3`.",
        steps=["Создай в классе `Solution` рядом с методом `main` (но не внутри него) метод `static void announce(String city)`.",
               "Метод печатает объявление из двух строк: `Attention, please!` и `Train to … is boarding` — вместо "
               "многоточия город из параметра `city`.",
               "В `main` вызови `announce` три раза: для `city1`, потом для `city2`, потом для `city3`."],
        hint="Метод — это именованный кусок кода, который можно запускать много раз. Каждый вызов `announce(...)` "
             "передаёт в параметр `city` новое значение, и метод печатает объявление именно для него.",
        solution=with_method("announce(city1);\nannounce(city2);\nannounce(city3);", ANNOUNCE.format(where="city")),
        wrong=[("внутри метода печатает поле city1 вместо параметра city: во всех объявлениях один город",
                with_method("announce(city1);\nannounce(city2);\nannounce(city3);", ANNOUNCE.format(where="city1"))),
               ("забыл третий вызов: последний поезд остался без объявления",
                with_method("announce(city1);\nannounce(city2);", ANNOUNCE.format(where="city")))],
        constructs=["function"],
        checks=ANNOUNCE_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-mb-egg-boxes", title="Коробки для яиц",
        given=[("int[]", "orders")],
        variants=[{"orders": "{25, 40, 7}"}, {"orders": "{12, 30, 51, 8}"}, {"orders": "{60, 15}"}],
        hidden=[{"orders": "{10}"}, {"orders": "{1, 9, 11, 20, 99}"}, {"orders": "{30, 30, 30}"},
                {"orders": "{45, 3}"}],
        intro="На птицефабрике яйца раскладывают в коробки по 10 штук. Неполная коробка тоже уходит покупателю, "
              "поэтому для 25 яиц нужно 3 коробки. Сколько яиц в каждом заказе, записано в массиве `orders`.",
        steps=["Создай в классе `Solution` рядом с `main` метод `static int boxes(int eggs)`. Он **возвращает** через "
               "`return`, сколько коробок нужно для `eggs` яиц: число полных десятков, и ещё одна коробка, "
               "если остаток от деления на 10 больше нуля.",
               "В `main` пройди циклом по массиву `orders` и для каждого заказа выведи строку вида "
               "`Order 1: 3 box(es)` — номер заказа (с единицы) и результат вызова `boxes`.",
               "Последней строкой выведи `Total: … box(es)` — сумму коробок по всем заказам."],
        hint="Остаток от деления на 10 (`eggs % 10`) показывает, сколько яиц не поместилось в полные коробки. "
             "Внутри метода можно использовать `if`, как и в `main`.",
        solution=with_method(EGGS_MAIN, BOXES),
        wrong=[("не считает неполную коробку: метод возвращает только eggs / 10",
                with_method(EGGS_MAIN, 'static int boxes(int eggs) {\n    return eggs / 10;\n}')),
               ("всегда добавляет лишнюю коробку, даже когда яйца делятся на 10 ровно",
                with_method(EGGS_MAIN, 'static int boxes(int eggs) {\n    return eggs / 10 + 1;\n}'))],
        constructs=["function", "return", "for"],
        checks=BOXES_CHECKS,
    ),
    JavaFunctionTask(
        skill=SKILL, difficulty=3, slug="java-mb-step-streak", title="Серия активных дней",
        function="longestRun",
        variants=[{"goal": 8000}, {"goal": 10000}, {"goal": 6000}],
        intro="Фитнес-браслет считает шаги за каждый день. День засчитывается как активный, если сделано {goal} "
              "шагов или больше. Приложение хвалит за самую длинную серию активных дней подряд.",
        steps=["Допиши метод `longestRun(int[] steps)`: в массиве `steps` — число шагов за каждый день по порядку.",
               "Метод возвращает длину самой длинной серии активных дней, идущих подряд (без пропусков).",
               "Если активных дней нет или массив пустой, верни 0."],
        hint="Держи две переменные: длину текущей серии и лучшую длину. Активный день продлевает текущую серию, "
             "неактивный обнуляет её; лучшую длину обновляй каждый раз, когда текущая стала больше.",
        starter="public class Solution {{\n    static int longestRun(int[] steps) {{\n        // Напиши решение здесь\n"
                "        return 0;\n    }}\n}}\n",
        solution=LONGEST_RUN,
        inputs=["new int[]{12000, 9000, 3000, 11000, 10500, 10000, 2000}", "new int[]{1000, 2000}",
                "new int[]{}", "new int[]{6000, 7000, 8000, 9000, 10000}", "new int[]{10000, 500, 10000, 500, 10000}",
                "new int[]{5999, 6000, 7999, 8000, 9999, 10000, 10001, 100}", "new int[]{20000}"],
        wrong=[("не обнуляет серию на неактивном дне: считает все активные дни вообще",
                LONGEST_RUN.replace("            }} else {{\n                current = 0;\n            }}", "            }}")),
               ("возвращает длину последней серии, а не самой длинной",
                LONGEST_RUN.replace("        return best;", "        return current;"))],
    ),
]
