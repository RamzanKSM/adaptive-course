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


COIN_MAIN = 'int balance = 0;\nfor (String coin : coins) {\n    balance += accept(coin);\n}\nSystem.out.println("Balance: " + balance + " rub");'

COIN_ACCEPT = '''static int accept(String coin) {
    try {
        return Integer.parseInt(coin);
    } catch (NumberFormatException e) {
        System.out.println("Coin not recognized, take it back");
        return 0;
    } finally {
        System.out.println("Tray is free");
    }
}'''

COIN_CHECKS = '''Method m = null;
try { m = Solution.class.getDeclaredMethod("accept", String.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, "Добавь в класс Solution метод static int accept(String coin): он принимает одну монету и возвращает её номинал");
m.setAccessible(true);
for (String coin : new String[]{"5", "washer"}) {
  PrintStream saved = System.out;
  ByteArrayOutputStream buffer = new ByteArrayOutputStream();
  System.setOut(new PrintStream(buffer, true, "UTF-8"));
  try { m.invoke(null, coin); }
  catch (InvocationTargetException e) { need(false, "Метод accept не должен падать на нераспознанной монете: перехвати NumberFormatException внутри метода"); }
  finally { System.setOut(saved); }
  need(buffer.toString("UTF-8").contains("Tray is free"), "Метод accept должен сам выводить «Tray is free» после каждой монеты, и распознанной, и нет: напиши это в блоке finally");
}'''

COOKIE_MAIN = 'int boxes = 0;\nfor (String batch : batches) {\n    boxes += fullBoxes(batch, perBox);\n}\nSystem.out.println("Boxes: " + boxes);'

COOKIE_METHOD = """static int fullBoxes(String count, int perBox) {
    try {
        return Integer.parseInt(count) / perBox;
    } catch (NumberFormatException e) {
        System.out.println("Cannot read: " + count);
        return 0;
    } catch (ArithmeticException e) {
        System.out.println("Box size is zero");
        return 0;
    } finally {
        System.out.println("Scale reset");
    }
}"""

COOKIE_CHECKS = """Method m = null;
try { m = Solution.class.getDeclaredMethod("fullBoxes", String.class, int.class); } catch (NoSuchMethodException e) { }
need(m != null && Modifier.isStatic(m.getModifiers()) && m.getReturnType() == int.class, "Добавь в класс Solution метод static int fullBoxes(String count, int perBox): он возвращает, сколько полных коробок получится из одной партии");
m.setAccessible(true);
Object[][] probes = {{"12", 5}, {"cookies", 5}, {"12", 0}};
for (Object[] probe : probes) {
  PrintStream saved = System.out;
  ByteArrayOutputStream buffer = new ByteArrayOutputStream();
  System.setOut(new PrintStream(buffer, true, "UTF-8"));
  try { m.invoke(null, probe[0], probe[1]); }
  catch (InvocationTargetException e) { need(false, "Метод fullBoxes не должен падать: перехвати NumberFormatException и ArithmeticException внутри метода"); }
  finally { System.setOut(saved); }
  need(buffer.toString("UTF-8").contains("Scale reset"), "Метод fullBoxes должен сам выводить «Scale reset» после каждой партии — и удачной, и с ошибкой: напиши это в блоке finally");
}"""

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-finally-parking", title="Оплата парковки",
        given=[("String", "hours"), ("int", "rate")],
        variants=[{"hours": '"4"', "rate": "60"}, {"hours": '"two"', "rate": "80"}, {"hours": '"3"', "rate": "120"}],
        hidden=[{"hours": '"1"', "rate": "50"}, {"hours": '"2,5"', "rate": "60"}, {"hours": '"10"', "rate": "75"},
                {"hours": '" "', "rate": "60"}],
        intro="Терминал парковки берёт {rate} руб. за час. Водитель вставляет карту и набирает на экране, сколько часов "
              "стоял, — эта строка попадает в `hours`, а цена часа лежит в `rate`. Что бы ни случилось, терминал "
              "должен вернуть карту.",
        steps=["В блоке `try` преврати `hours` в целое число через `Integer.parseInt` и выведи `To pay: 240 rub` — "
               "часы, умноженные на `rate`.",
               "Если в `hours` не число, перехвати `NumberFormatException` и выведи `Enter the hours in digits`.",
               "Добавь блок `finally` и выведи в нём `Take your card` — эта строка нужна всегда: и после оплаты, "
               "и после ошибки."],
        hint="Блок `finally` пишется сразу после `catch` и выполняется в любом случае — было исключение или нет. "
             "В него кладут то, что нужно сделать обязательно, например вернуть карту.",
        solution='try {\n    System.out.println("To pay: " + Integer.parseInt(hours) * rate + " rub");\n'
                 '} catch (NumberFormatException e) {\n    System.out.println("Enter the hours in digits");\n'
                 '} finally {\n    System.out.println("Take your card");\n}',
        wrong=[("возвращает карту в конце try — после ошибки карта остаётся в терминале",
                'try {\n    System.out.println("To pay: " + Integer.parseInt(hours) * rate + " rub");\n'
                '    System.out.println("Take your card");\n} catch (NumberFormatException e) {\n'
                '    System.out.println("Enter the hours in digits");\n}'),
               ("возвращает карту только в catch — после удачной оплаты карту не отдают",
                'try {\n    System.out.println("To pay: " + Integer.parseInt(hours) * rate + " rub");\n'
                '} catch (NumberFormatException e) {\n    System.out.println("Enter the hours in digits");\n'
                '    System.out.println("Take your card");\n}')],
        constructs=["try", "finally"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-finally-fuel-pump", title="Колонка на заправке",
        given=[("String", "liters"), ("int", "space")],
        variants=[{"liters": '"30"', "space": "45"}, {"liters": '"50"', "space": "20"}, {"liters": '"full"', "space": "35"}],
        hidden=[{"liters": '"20"', "space": "20"}, {"liters": '"21"', "space": "20"}, {"liters": '"10 l"', "space": "40"},
                {"liters": '"5"', "space": "60"}],
        intro="Колонка на заправке продаёт бензин по 60 руб. за литр. Водитель набирает, сколько литров залить, — "
              "строка попадает в `liters`, а сколько литров ещё поместится в бак, записано в `space`. После любой "
              "попытки колонка просит повесить пистолет на место.",
        steps=["В блоке `try` преврати `liters` в целое число через `Integer.parseInt`.",
               "Если литров больше, чем `space`, выведи `The tank only has room for 20 l` (число из `space`) и сразу "
               "заверши программу командой `return;`.",
               "Иначе выведи `Filled 30 l, to pay 1800 rub` — литры и их стоимость по 60 руб.",
               "Если в `liters` не число, перехвати `NumberFormatException` и выведи `Enter the liters in digits`.",
               "В блоке `finally` выведи `Put the nozzle back` — эта строка нужна в любом случае, даже после `return`."],
        hint="Команда `return;` сразу завершает `main`, и строки после всего блока `try`/`catch` уже не выполнятся. "
             "А `finally` выполнится всё равно: Java запускает его перед выходом из метода.",
        solution='try {\n    int amount = Integer.parseInt(liters);\n    if (amount > space) {\n'
                 '        System.out.println("The tank only has room for " + space + " l");\n        return;\n    }\n'
                 '    System.out.println("Filled " + amount + " l, to pay " + amount * 60 + " rub");\n'
                 '} catch (NumberFormatException e) {\n    System.out.println("Enter the liters in digits");\n'
                 '} finally {\n    System.out.println("Put the nozzle back");\n}',
        wrong=[("последняя строка стоит после try/catch, а не в finally — после return её нет",
                'try {\n    int amount = Integer.parseInt(liters);\n    if (amount > space) {\n'
                '        System.out.println("The tank only has room for " + space + " l");\n        return;\n    }\n'
                '    System.out.println("Filled " + amount + " l, to pay " + amount * 60 + " rub");\n'
                '} catch (NumberFormatException e) {\n    System.out.println("Enter the liters in digits");\n}\n'
                'System.out.println("Put the nozzle back");'),
               ("последняя строка стоит в конце try — после ошибки и после return её нет",
                'try {\n    int amount = Integer.parseInt(liters);\n    if (amount > space) {\n'
                '        System.out.println("The tank only has room for " + space + " l");\n        return;\n    }\n'
                '    System.out.println("Filled " + amount + " l, to pay " + amount * 60 + " rub");\n'
                '    System.out.println("Put the nozzle back");\n'
                '} catch (NumberFormatException e) {\n    System.out.println("Enter the liters in digits");\n}')],
        constructs=["try", "finally", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-finally-coin-acceptor", title="Монетоприёмник",
        given=[("String[]", "coins")],
        variants=[{"coins": '{"10", "5", "washer", "2"}'}, {"coins": '{"1", "?", "10"}'}, {"coins": '{"5", "5", "5"}'}],
        hidden=[{"coins": '{"button"}'}, {"coins": '{"2", "1", "10", "5"}'}, {"coins": "{}"},
                {"coins": '{"10", "", "x", "5"}'}],
        intro="Автомат с напитками принимает монеты. Датчик распознаёт каждую и присылает её номинал строкой — все они "
              "по порядку лежат в массиве `coins`; если монету распознать не удалось, вместо числа приходит что-то другое.",
        steps=["Добавь в класс `Solution` метод `static int accept(String coin)`. В блоке `try` он превращает `coin` "
               "в число через `Integer.parseInt` и сразу возвращает его через `return`.",
               "Если монета не распознана (`NumberFormatException`), метод выводит `Coin not recognized, take it back` "
               "и возвращает `0`.",
               "В блоке `finally` метод выводит `Tray is free` — после каждой монеты, распознанной или нет.",
               "В `main` пропусти через `accept` все монеты из `coins` по порядку, сложи то, что вернул метод, и в конце "
               "выведи `Balance: 17 rub`"],
        hint="Когда в `try` или `catch` срабатывает `return`, метод завершается не мгновенно: сначала выполняется "
             "`finally`, и только потом значение возвращается в `main`. Поэтому строку из `finally` не придётся "
             "писать дважды.",
        solution=with_methods(COIN_MAIN, COIN_ACCEPT),
        wrong=[("«Tray is free» печатается в try перед return — после нераспознанной монеты этой строки нет",
                with_methods(COIN_MAIN, COIN_ACCEPT.replace(
                    '        return Integer.parseInt(coin);\n',
                    '        int value = Integer.parseInt(coin);\n        System.out.println("Tray is free");\n        return value;\n').replace(
                    '    } finally {\n        System.out.println("Tray is free");\n    }\n', '    }\n'))),
               ("в finally стоит return 0 — он подменяет номинал из try, и баланс всегда 0",
                with_methods(COIN_MAIN, COIN_ACCEPT.replace(
                    '        System.out.println("Tray is free");\n    }',
                    '        System.out.println("Tray is free");\n        return 0;\n    }')))],
        constructs=["try", "finally", "function"],
        checks=COIN_CHECKS,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-finally-photo-print", title="Печать фотографий",
        given=[("int", "photos"), ("int", "perPage")],
        variants=[{"photos": "20", "perPage": "4"}, {"photos": "15", "perPage": "0"}, {"photos": "37", "perPage": "6"}],
        hidden=[{"photos": "9", "perPage": "0"}, {"photos": "3", "perPage": "5"}, {"photos": "100", "perPage": "1"},
                {"photos": "0", "perPage": "2"}],
        intro="Фотоателье печатает `photos` фотографий, по `perPage` штук на одном листе. Если размер раскладки не "
              "выбран (`perPage` равно 0), деление выбрасывает `ArithmeticException`. В любом случае после задания "
              "принтер должен сообщить, что снова готов.",
        steps=["В блоке `try` выведи строку вида `Full pages: 5` — сколько листов заполнится целиком (целое деление).",
               "Перехвати `ArithmeticException` и выведи `Choose how many photos fit on a page`.",
               "Добавь блок `finally` и выведи в нём `Printer is ready` — эта строка нужна всегда, последней."],
        hint="`finally` выполняется после `try`, если всё прошло хорошо, и после `catch`, если была ошибка. Поэтому "
             "строку, которая нужна в обоих случаях, пишут один раз — в `finally`.",
        solution='try {\n    System.out.println("Full pages: " + photos / perPage);\n} catch (ArithmeticException e) {\n'
                 '    System.out.println("Choose how many photos fit on a page");\n} finally {\n'
                 '    System.out.println("Printer is ready");\n}',
        wrong=[("пишет «Printer is ready» в конце try — после ошибки этой строки нет",
                'try {\n    System.out.println("Full pages: " + photos / perPage);\n    System.out.println("Printer is ready");\n'
                '} catch (ArithmeticException e) {\n    System.out.println("Choose how many photos fit on a page");\n}'),
               ("печатает «Printer is ready» до try — строка оказывается первой, а не последней",
                'System.out.println("Printer is ready");\ntry {\n    System.out.println("Full pages: " + photos / perPage);\n'
                '} catch (ArithmeticException e) {\n    System.out.println("Choose how many photos fit on a page");\n}')],
        constructs=["try", "finally"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-finally-lift-buttons", title="Кнопки в лифте",
        given=[("String[]", "buttons"), ("int", "floors")],
        variants=[{"buttons": '{"3", "12", "five"}', "floors": "9"},
                  {"buttons": '{"1", "0", "16"}', "floors": "16"},
                  {"buttons": '{"7", "?", "25", "2"}', "floors": "20"}],
        hidden=[{"buttons": "{}", "floors": "5"},
                {"buttons": '{"5"}', "floors": "5"},
                {"buttons": '{"6"}', "floors": "5"},
                {"buttons": '{"", "-1", "4"}', "floors": "10"}],
        intro="В доме `floors` этажей. Пассажиры по очереди нажимают кнопки в лифте, и то, что пришло с каждой "
              "кнопки, записано строкой в массиве `buttons`. Иногда приходит не число, а иногда этажа с таким "
              "номером нет. После каждого нажатия, что бы ни случилось, двери закрываются.",
        steps=["Пройди по массиву `buttons`. Для каждого нажатия в блоке `try` преврати строку в число через "
               "`Integer.parseInt`.",
               "Если этаж меньше 1 или больше `floors`, выведи строку вида `No floor 12` и переходи к следующему "
               "нажатию командой `continue;`.",
               "Иначе выведи строку вида `Going to floor 3`.",
               "Если строка не число, перехвати `NumberFormatException` и выведи `Press a number`.",
               "В блоке `finally` выведи `Doors closed` — эта строка нужна после каждого нажатия, даже после `continue`."],
        hint="`continue` сразу переходит к следующему шагу цикла, и строки после всего `try`/`catch` пропускаются. "
             "А `finally` выполнится и в этом случае — Java запускает его перед переходом.",
        solution='for (String button : buttons) {\n    try {\n        int floor = Integer.parseInt(button);\n'
                 '        if (floor < 1 || floor > floors) {\n            System.out.println("No floor " + floor);\n'
                 '            continue;\n        }\n        System.out.println("Going to floor " + floor);\n'
                 '    } catch (NumberFormatException e) {\n        System.out.println("Press a number");\n'
                 '    } finally {\n        System.out.println("Doors closed");\n    }\n}',
        wrong=[("«Doors closed» стоит после try/catch, а не в finally — после continue её нет",
                'for (String button : buttons) {\n    try {\n        int floor = Integer.parseInt(button);\n'
                '        if (floor < 1 || floor > floors) {\n            System.out.println("No floor " + floor);\n'
                '            continue;\n        }\n        System.out.println("Going to floor " + floor);\n'
                '    } catch (NumberFormatException e) {\n        System.out.println("Press a number");\n'
                '    }\n    System.out.println("Doors closed");\n}'),
               ("«Doors closed» стоит в конце try — после ошибки и после continue её нет",
                'for (String button : buttons) {\n    try {\n        int floor = Integer.parseInt(button);\n'
                '        if (floor < 1 || floor > floors) {\n            System.out.println("No floor " + floor);\n'
                '            continue;\n        }\n        System.out.println("Going to floor " + floor);\n'
                '        System.out.println("Doors closed");\n'
                '    } catch (NumberFormatException e) {\n        System.out.println("Press a number");\n    }\n}')],
        constructs=["try", "finally", "for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-finally-cookie-boxes", title="Печенье по коробкам",
        given=[("String[]", "batches"), ("int", "perBox")],
        variants=[{"batches": '{"24", "30", "abc", "13"}', "perBox": "6"},
                  {"batches": '{"10", "20"}', "perBox": "0"},
                  {"batches": '{"7", "?", "50"}', "perBox": "7"}],
        hidden=[{"batches": "{}", "perBox": "5"},
                {"batches": '{"x"}', "perBox": "0"},
                {"batches": '{"100", "99"}', "perBox": "10"},
                {"batches": '{"5", "", "15"}', "perBox": "5"}],
        intro="На фабрике печенье из каждой партии раскладывают в коробки по `perBox` штук. Весы присылают число "
              "печений в партии строкой — все партии по порядку лежат в массиве `batches`; иногда весы сбоят, и "
              "вместо числа приходит что-то другое. А если размер коробки не задан, `perBox` равно 0. После каждой "
              "партии весы обнуляют.",
        steps=["Добавь в класс `Solution` метод `static int fullBoxes(String count, int perBox)`. В блоке `try` он "
               "превращает `count` в число через `Integer.parseInt`, делит его нацело на `perBox` и сразу "
               "возвращает результат через `return`.",
               "Если `count` не число (`NumberFormatException`), метод выводит строку вида `Cannot read: abc` и "
               "возвращает `0`.",
               "Если `perBox` равно 0 (`ArithmeticException`), метод выводит `Box size is zero` и возвращает `0`.",
               "В блоке `finally` метод выводит `Scale reset` — после каждой партии, удачной или нет.",
               "В `main` пропусти через `fullBoxes` все партии из `batches` по порядку, сложи результаты и в конце "
               "выведи строку вида `Boxes: 11`."],
        hint="Не обходи деление на ноль проверкой `if` с `return` до `try`: такой выход из метода пропустит "
             "`finally`, ведь он стоит не внутри `try`. Пусть ошибку поймает второй `catch` — тогда `finally` "
             "сработает и в этом случае.",
        solution=with_methods(COOKIE_MAIN, COOKIE_METHOD),
        wrong=[("«Scale reset» печатается в try перед return — после ошибки этой строки нет",
                with_methods(COOKIE_MAIN, COOKIE_METHOD.replace(
                    '        return Integer.parseInt(count) / perBox;\n',
                    '        int boxes = Integer.parseInt(count) / perBox;\n        System.out.println("Scale reset");\n        return boxes;\n').replace(
                    '    } finally {\n        System.out.println("Scale reset");\n    }\n', '    }\n'))),
               ("проверяет ноль через if с return до try — для пустой коробки finally не выполняется",
                with_methods(COOKIE_MAIN, COOKIE_METHOD.replace(
                    '    try {\n',
                    '    if (perBox == 0) {\n        System.out.println("Box size is zero");\n        return 0;\n    }\n    try {\n', 1).replace(
                    '    } catch (ArithmeticException e) {\n        System.out.println("Box size is zero");\n        return 0;\n', '')))],
        constructs=["try", "finally", "function"],
        checks=COOKIE_CHECKS,
    ),
]
