"""FINALLY_BASIC — «Блок finally» (Java). Taught before: everything up to try/catch (ArithmeticException,
NumberFormatException from Integer.parseInt), methods with return, arrays, classes. Here: finally runs always — after
success, after a caught error and even after return. The platform requires the finally block itself (construct
«finally»); the tasks also lean on behaviour: a line that must appear on every path, including a return out of
try/catch, where code placed after the try statement would not run. Not yet: throw, throws."""
from java_tasks import JavaOutputTask

SKILL = "FINALLY_BASIC"


def with_methods(main: str, methods: str) -> str:
    """Body of main followed by more static methods of Solution (the template's closing brace ends the last one)."""
    body = methods.strip()
    assert body.endswith("}")
    return main.rstrip() + "\n}\n\n" + body[:-1].rstrip()


SCALE = ('try {\n    int g = Integer.parseInt(grams);\n    System.out.println("Cost: " + g * pricePerKg / 1000 + " rub");\n'
         '} catch (NumberFormatException e) {\n    System.out.println("Put the item on the scale again");\n'
         '} finally {\n    System.out.println("Remove the item");\n}')

PIN = ('int used = 0;\nfor (String attempt : attempts) {\n    try {\n        if (Integer.parseInt(attempt) == pin) {\n'
       '            System.out.println("Unlocked");\n            break;\n        }\n        System.out.println("Wrong PIN");\n'
       '    } catch (NumberFormatException e) {\n        System.out.println("Digits only");\n    } finally {\n'
       '        used++;\n        System.out.println("Attempt " + used + " logged");\n    }\n}\n'
       'System.out.println("Attempts used: " + used);')

EXAM_MAIN = ('int passed = 0;\nfor (int i = 0; i < sheets.length; i++) {\n    String r = result(sheets[i]);\n'
             '    System.out.println("Sheet " + (i + 1) + ": " + r);\n    if (r.equals("pass")) {\n        passed++;\n    }\n}\n'
             'System.out.println("Passed: " + passed);')

EXAM_METHOD = '''static String result(String points) {
    try {
        int p = Integer.parseInt(points);
        if (p >= 60) {
            return "pass";
        }
        return "fail";
    } catch (NumberFormatException e) {
        return "no score";
    } finally {
        System.out.println("Sheet checked");
    }
}'''

EXAM_CHECKS = '''Method m = null;
try { m = Solution.class.getDeclaredMethod("result", String.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()) && m.getReturnType() == String.class, "Добавь в класс Solution метод static String result(String points): он проверяет один лист и возвращает итог");
m.setAccessible(true);
for (String sheet : new String[]{"75", "30", "absent"}) {
  PrintStream saved = System.out;
  ByteArrayOutputStream buffer = new ByteArrayOutputStream();
  System.setOut(new PrintStream(buffer, true, "UTF-8"));
  try { m.invoke(null, sheet); }
  catch (InvocationTargetException e) { need(false, "Метод result не должен падать на листе без числа: перехвати NumberFormatException внутри метода"); }
  finally { System.setOut(saved); }
  need(buffer.toString("UTF-8").contains("Sheet checked"), "Метод result должен сам выводить «Sheet checked» после каждого листа, с любым итогом: напиши это в блоке finally");
}'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-finally-rt-self-checkout", title="Весы на кассе самообслуживания",
        given=[("String", "grams"), ("int", "pricePerKg")],
        variants=[{"grams": '"1500"', "pricePerKg": "120"}, {"grams": '"err"', "pricePerKg": "90"},
                  {"grams": '"750"', "pricePerKg": "200"}],
        hidden=[{"grams": '"1000"', "pricePerKg": "55"}, {"grams": '""', "pricePerKg": "300"},
                {"grams": '"2.5"', "pricePerKg": "80"}, {"grams": '"250"', "pricePerKg": "400"}],
        intro="На кассе самообслуживания покупатель кладёт яблоки на весы. Весы присылают вес в граммах строкой — "
              "она попадает в `grams`, а цена килограмма лежит в `pricePerKg`. Иногда весы сбоят и присылают не "
              "число. Что бы ни случилось, касса потом просит снять товар с весов.",
        steps=["В блоке `try` преврати `grams` в целое число через `Integer.parseInt` и выведи строку вида "
               "`Cost: 180 rub` — граммы, умноженные на `pricePerKg` и делённые нацело на 1000.",
               "Если в `grams` не число, перехвати `NumberFormatException` и выведи `Put the item on the scale again`.",
               "Добавь блок `finally` и выведи в нём `Remove the item` — эта строка нужна всегда: и после "
               "взвешивания, и после ошибки."],
        hint="`finally` пишется сразу после `catch` и выполняется в любом случае. Строку, которая нужна и после "
             "удачи, и после ошибки, не надо писать дважды — её место в `finally`.",
        solution=SCALE,
        wrong=[("просит снять товар в конце try — после сбоя весов этой строки нет",
                'try {\n    int g = Integer.parseInt(grams);\n    System.out.println("Cost: " + g * pricePerKg / 1000 + " rub");\n'
                '    System.out.println("Remove the item");\n} catch (NumberFormatException e) {\n'
                '    System.out.println("Put the item on the scale again");\n}'),
               ("просит снять товар до try — строка оказывается первой, а не последней",
                'System.out.println("Remove the item");\ntry {\n    int g = Integer.parseInt(grams);\n'
                '    System.out.println("Cost: " + g * pricePerKg / 1000 + " rub");\n} catch (NumberFormatException e) {\n'
                '    System.out.println("Put the item on the scale again");\n}')],
        constructs=["try", "finally"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-finally-rt-pin-attempts", title="Попытки ввести PIN-код",
        given=[("String[]", "attempts"), ("int", "pin")],
        variants=[{"attempts": '{"1111", "12a4", "1234", "9999"}', "pin": "1234"},
                  {"attempts": '{"0000", "4321"}', "pin": "4321"},
                  {"attempts": '{"pin", "7777", "", "5555"}', "pin": "2580"}],
        hidden=[{"attempts": "{}", "pin": "1234"},
                {"attempts": '{"1234"}', "pin": "1234"},
                {"attempts": '{"x", "y"}', "pin": "1"},
                {"attempts": '{"8", "9", "10", "11"}', "pin": "10"}],
        intro="Банкомат принимает PIN-код. Всё, что человек набирал, по порядку записано строками в массив `attempts`, "
              "а правильный код — число `pin`. Как только код верный, банкомат открывает доступ и больше попыток не "
              "ждёт. После каждой попытки, удачной или нет, он записывает её в журнал.",
        steps=["Заведи счётчик попыток `used`, равный 0, и пройди по массиву `attempts` циклом for-each.",
               "Для каждой попытки в блоке `try` преврати строку в число через `Integer.parseInt`. Если оно равно `pin`, "
               "выведи `Unlocked` и выйди из цикла командой `break;`. Иначе выведи `Wrong PIN`.",
               "Если строка не число, перехвати `NumberFormatException` и выведи `Digits only`.",
               "В блоке `finally` увеличь `used` на 1 и выведи строку вида `Attempt 1 logged` — эта строка нужна "
               "после каждой попытки, даже после `break`.",
               "После цикла выведи строку вида `Attempts used: 3`."],
        hint="`break` сразу выходит из цикла, и строки после всего `try`/`catch` в этом шаге не выполняются. "
             "А `finally` Java выполнит и в этом случае — перед выходом из цикла.",
        solution=PIN,
        wrong=[("журнал ведётся после try/catch, а не в finally — после break последняя попытка не записана",
                PIN.replace('    } finally {\n        used++;\n        System.out.println("Attempt " + used + " logged");\n    }\n}',
                            '    }\n    used++;\n    System.out.println("Attempt " + used + " logged");\n}')),
               ("журнал ведётся в конце try — попытки с буквами и удачная не записаны",
                PIN.replace('        System.out.println("Wrong PIN");\n',
                            '        System.out.println("Wrong PIN");\n        used++;\n'
                            '        System.out.println("Attempt " + used + " logged");\n')
                   .replace('    } finally {\n        used++;\n        System.out.println("Attempt " + used + " logged");\n    }\n',
                            '    }\n'))],
        constructs=["try", "finally", "for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-finally-rt-exam-sheets", title="Проверка экзаменационных листов",
        given=[("String[]", "sheets")],
        variants=[{"sheets": '{"75", "40", "absent", "60"}'}, {"sheets": '{"59", "?", "100"}'}, {"sheets": '{"81", "93"}'}],
        hidden=[{"sheets": "{}"}, {"sheets": '{"60"}'}, {"sheets": '{"59"}'}, {"sheets": '{"x", "", "0", "61", "abc"}'}],
        intro="Учитель проверяет экзаменационные листы. Баллы за каждый лист по порядку записаны строками в массив "
              "`sheets`; если ученик не пришёл или лист испорчен, вместо числа стоит что-то другое. Экзамен сдан, "
              "если баллов 60 или больше. После каждого листа, с любым итогом, нужно отметить, что он проверен.",
        steps=["Добавь в класс `Solution` метод `static String result(String points)`. В блоке `try` он превращает "
               "`points` в число через `Integer.parseInt` и сразу возвращает через `return` строку `pass`, если баллов "
               "60 или больше, или `fail`, если меньше.",
               "Если в `points` не число (`NumberFormatException`), метод возвращает `no score`.",
               "В блоке `finally` метод выводит `Sheet checked` — после каждого листа.",
               "В `main` пройди по номерам листов: для каждого вызови `result`, выведи строку вида `Sheet 1: pass` "
               "(листы нумеруются с 1) и посчитай, сколько листов сданы. В конце выведи строку вида `Passed: 2`."],
        hint="`return` в `try` или `catch` не завершает метод мгновенно: сначала выполняется `finally`, и только "
             "потом итог попадает в `main`. Поэтому `Sheet checked` появится в выводе раньше строки с итогом листа. "
             "Строки сравнивай через `equals`.",
        solution=with_methods(EXAM_MAIN, EXAM_METHOD),
        wrong=[("«Sheet checked» печатается в try перед return — после листа без числа этой строки нет",
                with_methods(EXAM_MAIN, EXAM_METHOD.replace(
                    '        int p = Integer.parseInt(points);\n',
                    '        int p = Integer.parseInt(points);\n        System.out.println("Sheet checked");\n').replace(
                    '    } finally {\n        System.out.println("Sheet checked");\n    }\n', '    }\n'))),
               ("в finally стоит return \"fail\" — он подменяет итог, и сданных листов всегда 0",
                with_methods(EXAM_MAIN, EXAM_METHOD.replace(
                    '        System.out.println("Sheet checked");\n    }',
                    '        System.out.println("Sheet checked");\n        return "fail";\n    }')))],
        constructs=["try", "finally", "function"],
        checks=EXAM_CHECKS,
    ),
]
