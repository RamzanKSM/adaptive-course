"""FINALLY_BASIC — «Блок finally» (Java). Taught before: everything up to try/catch (ArithmeticException,
NumberFormatException from Integer.parseInt), methods with return, arrays, classes. Here: finally runs always — after
success, after a caught error and even after return. The syntax tree checks cannot see finally, so the tasks lean on
behaviour: a line that must appear on every path, including a return out of try/catch, where code placed after the
try statement would not run. Not yet: throw, throws."""
from java_tasks import JavaOutputTask

SKILL = "FINALLY_BASIC"


def with_methods(main: str, methods: str) -> str:
    """Body of main followed by more static methods of Solution (the template's closing brace ends the last one)."""
    body = methods.strip()
    assert body.endswith("}")
    return main.rstrip() + "\n}\n\n" + body[:-1].rstrip()


COIN_MAIN = 'int balance = 0;\nfor (String coin : coins) {\n    balance += accept(coin);\n}\nSystem.out.println("Баланс: " + balance + " руб.");'

COIN_ACCEPT = '''static int accept(String coin) {
    try {
        return Integer.parseInt(coin);
    } catch (NumberFormatException e) {
        System.out.println("Монета не распознана, заберите её");
        return 0;
    } finally {
        System.out.println("Лоток свободен");
    }
}'''

COIN_CHECKS = '''Method m = null;
try { m = Solution.class.getDeclaredMethod("accept", String.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, "Добавь в класс Solution метод static int accept(String coin): он принимает одну монету и возвращает её номинал");
m.setAccessible(true);
for (String coin : new String[]{"5", "шайба"}) {
  PrintStream saved = System.out;
  ByteArrayOutputStream buffer = new ByteArrayOutputStream();
  System.setOut(new PrintStream(buffer, true, "UTF-8"));
  try { m.invoke(null, coin); }
  catch (InvocationTargetException e) { need(false, "Метод accept не должен падать на нераспознанной монете: перехвати NumberFormatException внутри метода"); }
  finally { System.setOut(saved); }
  need(buffer.toString("UTF-8").contains("Лоток свободен"), "Метод accept должен сам выводить «Лоток свободен» после каждой монеты, и распознанной, и нет: напиши это в блоке finally");
}'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-finally-parking", title="Оплата парковки",
        given=[("String", "hours"), ("int", "rate")],
        variants=[{"hours": '"4"', "rate": "60"}, {"hours": '"два"', "rate": "80"}, {"hours": '"3"', "rate": "120"}],
        hidden=[{"hours": '"1"', "rate": "50"}, {"hours": '"2,5"', "rate": "60"}, {"hours": '"10"', "rate": "75"},
                {"hours": '" "', "rate": "60"}],
        intro="Терминал парковки берёт {rate} руб. за час. Водитель вставляет карту и набирает на экране, сколько часов "
              "стоял, — эта строка попадает в `hours`, а цена часа лежит в `rate`. Что бы ни случилось, терминал "
              "должен вернуть карту.",
        steps=["В блоке `try` преврати `hours` в целое число через `Integer.parseInt` и выведи `К оплате: 240 руб.` — "
               "часы, умноженные на `rate`.",
               "Если в `hours` не число, перехвати `NumberFormatException` и выведи `Введите число часов цифрами`.",
               "Добавь блок `finally` и выведи в нём `Заберите карту` — эта строка нужна всегда: и после оплаты, "
               "и после ошибки."],
        hint="Блок `finally` пишется сразу после `catch` и выполняется в любом случае — было исключение или нет. "
             "В него кладут то, что нужно сделать обязательно, например вернуть карту.",
        solution='try {\n    System.out.println("К оплате: " + Integer.parseInt(hours) * rate + " руб.");\n'
                 '} catch (NumberFormatException e) {\n    System.out.println("Введите число часов цифрами");\n'
                 '} finally {\n    System.out.println("Заберите карту");\n}',
        wrong=[("возвращает карту в конце try — после ошибки карта остаётся в терминале",
                'try {\n    System.out.println("К оплате: " + Integer.parseInt(hours) * rate + " руб.");\n'
                '    System.out.println("Заберите карту");\n} catch (NumberFormatException e) {\n'
                '    System.out.println("Введите число часов цифрами");\n}'),
               ("возвращает карту только в catch — после удачной оплаты карту не отдают",
                'try {\n    System.out.println("К оплате: " + Integer.parseInt(hours) * rate + " руб.");\n'
                '} catch (NumberFormatException e) {\n    System.out.println("Введите число часов цифрами");\n'
                '    System.out.println("Заберите карту");\n}')],
        constructs=["try"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-finally-fuel-pump", title="Колонка на заправке",
        given=[("String", "liters"), ("int", "space")],
        variants=[{"liters": '"30"', "space": "45"}, {"liters": '"50"', "space": "20"}, {"liters": '"полный"', "space": "35"}],
        hidden=[{"liters": '"20"', "space": "20"}, {"liters": '"21"', "space": "20"}, {"liters": '"10 л"', "space": "40"},
                {"liters": '"5"', "space": "60"}],
        intro="Колонка на заправке продаёт бензин по 60 руб. за литр. Водитель набирает, сколько литров залить, — "
              "строка попадает в `liters`, а сколько литров ещё поместится в бак, записано в `space`. После любой "
              "попытки колонка просит повесить пистолет на место.",
        steps=["В блоке `try` преврати `liters` в целое число через `Integer.parseInt`.",
               "Если литров больше, чем `space`, выведи `В бак поместится только 20 л` (число из `space`) и сразу "
               "заверши программу командой `return;`.",
               "Иначе выведи `Залито 30 л, к оплате 1800 руб.` — литры и их стоимость по 60 руб.",
               "Если в `liters` не число, перехвати `NumberFormatException` и выведи `Введите количество литров цифрами`.",
               "В блоке `finally` выведи `Повесьте пистолет на место` — эта строка нужна в любом случае, даже после `return`."],
        hint="Команда `return;` сразу завершает `main`, и строки после всего блока `try`/`catch` уже не выполнятся. "
             "А `finally` выполнится всё равно: Java запускает его перед выходом из метода.",
        solution='try {\n    int amount = Integer.parseInt(liters);\n    if (amount > space) {\n'
                 '        System.out.println("В бак поместится только " + space + " л");\n        return;\n    }\n'
                 '    System.out.println("Залито " + amount + " л, к оплате " + amount * 60 + " руб.");\n'
                 '} catch (NumberFormatException e) {\n    System.out.println("Введите количество литров цифрами");\n'
                 '} finally {\n    System.out.println("Повесьте пистолет на место");\n}',
        wrong=[("последняя строка стоит после try/catch, а не в finally — после return её нет",
                'try {\n    int amount = Integer.parseInt(liters);\n    if (amount > space) {\n'
                '        System.out.println("В бак поместится только " + space + " л");\n        return;\n    }\n'
                '    System.out.println("Залито " + amount + " л, к оплате " + amount * 60 + " руб.");\n'
                '} catch (NumberFormatException e) {\n    System.out.println("Введите количество литров цифрами");\n}\n'
                'System.out.println("Повесьте пистолет на место");'),
               ("последняя строка стоит в конце try — после ошибки и после return её нет",
                'try {\n    int amount = Integer.parseInt(liters);\n    if (amount > space) {\n'
                '        System.out.println("В бак поместится только " + space + " л");\n        return;\n    }\n'
                '    System.out.println("Залито " + amount + " л, к оплате " + amount * 60 + " руб.");\n'
                '    System.out.println("Повесьте пистолет на место");\n'
                '} catch (NumberFormatException e) {\n    System.out.println("Введите количество литров цифрами");\n}')],
        constructs=["try", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-finally-coin-acceptor", title="Монетоприёмник",
        given=[("String[]", "coins")],
        variants=[{"coins": '{"10", "5", "шайба", "2"}'}, {"coins": '{"1", "?", "10"}'}, {"coins": '{"5", "5", "5"}'}],
        hidden=[{"coins": '{"пуговица"}'}, {"coins": '{"2", "1", "10", "5"}'}, {"coins": "{}"},
                {"coins": '{"10", "", "x", "5"}'}],
        intro="Автомат с напитками принимает монеты. Датчик распознаёт каждую и присылает её номинал строкой — все они "
              "по порядку лежат в массиве `coins`; если монету распознать не удалось, вместо числа приходит что-то другое.",
        steps=["Добавь в класс `Solution` метод `static int accept(String coin)`. В блоке `try` он превращает `coin` "
               "в число через `Integer.parseInt` и сразу возвращает его через `return`.",
               "Если монета не распознана (`NumberFormatException`), метод выводит `Монета не распознана, заберите её` "
               "и возвращает `0`.",
               "В блоке `finally` метод выводит `Лоток свободен` — после каждой монеты, распознанной или нет.",
               "В `main` пропусти через `accept` все монеты из `coins` по порядку, сложи то, что вернул метод, и в конце "
               "выведи `Баланс: 17 руб.`"],
        hint="Когда в `try` или `catch` срабатывает `return`, метод завершается не мгновенно: сначала выполняется "
             "`finally`, и только потом значение возвращается в `main`. Поэтому строку из `finally` не придётся "
             "писать дважды.",
        solution=with_methods(COIN_MAIN, COIN_ACCEPT),
        wrong=[("«Лоток свободен» печатается в try перед return — после нераспознанной монеты этой строки нет",
                with_methods(COIN_MAIN, COIN_ACCEPT.replace(
                    '        return Integer.parseInt(coin);\n',
                    '        int value = Integer.parseInt(coin);\n        System.out.println("Лоток свободен");\n        return value;\n').replace(
                    '    } finally {\n        System.out.println("Лоток свободен");\n    }\n', '    }\n'))),
               ("в finally стоит return 0 — он подменяет номинал из try, и баланс всегда 0",
                with_methods(COIN_MAIN, COIN_ACCEPT.replace(
                    '        System.out.println("Лоток свободен");\n    }',
                    '        System.out.println("Лоток свободен");\n        return 0;\n    }')))],
        constructs=["try", "function"],
        checks=COIN_CHECKS,
    ),
]
