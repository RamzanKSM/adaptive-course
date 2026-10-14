"""SET_BASIC — «Множество Set» (Java). Taught before: everything up to List (add, get, size, for-each). Here: Set,
HashSet and TreeSet, add (and its boolean result), contains, size, a set built from a list, retainAll / removeAll /
addAll. Output never iterates or prints a HashSet: only sizes, booleans or a TreeSet. Not yet: Map."""
from java_tasks import JavaOutputTask

SKILL = "SET_BASIC"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-set-pool-visitors", title="Турникет в бассейне",
        given=[("List<String>", "scans"), ("String", "name")],
        variants=[{"scans": 'new ArrayList<>(List.of("Olya", "Dima", "Olya", "Sergey", "Dima", "Nina", "Olya"))', "name": '"Nina"'},
                  {"scans": 'new ArrayList<>(List.of("Artem", "Vera", "Artem", "Vera", "Artem"))', "name": '"Gleb"'},
                  {"scans": 'new ArrayList<>(List.of("Katya", "Lyosha", "Masha", "Lyosha", "Katya", "Pasha"))', "name": '"Masha"'}],
        hidden=[{"scans": 'new ArrayList<>(List.of("Ira"))', "name": '"Ira"'},
                {"scans": 'new ArrayList<>(List.of("Timur", "Timur", "Timur"))', "name": '"Ira"'},
                {"scans": 'new ArrayList<>(List.of("Anya", "Borya", "Vika", "Gena", "Dasha"))', "name": '"Dasha"'},
                {"scans": 'new ArrayList<>(List.of("Lena", "Petya", "Lena", "Petya"))', "name": '"Petya"'}],
        intro="На входе в бассейн стоит турникет: каждый раз, когда человек прикладывает карту, его имя записывается "
              "в список `scans`. Кто-то выходил и заходил снова, поэтому имена повторяются. Администратор хочет знать, "
              "сколько было разных посетителей и приходил ли сегодня посетитель `name`.",
        steps=["Выведи строку вида `Scans: 9` — сколько всего записей в списке `scans`.",
               "Создай множество `Set<String> visitors = new HashSet<>();` и добавь в него методом `add` каждое имя "
               "из `scans` (цикл for-each). Выведи строку вида `Different visitors: 4` — размер множества.",
               "Проверь методом `contains`, есть ли `name` в множестве. Если есть, выведи имя и слова `was here`, "
               "например `Rita: was here`, а если нет — `Rita: was not here`."],
        hint="Множество хранит каждый элемент только один раз: повторный `add` с тем же именем ничего не меняет. "
             "Поэтому размер множества — это число разных имён.",
        solution='System.out.println("Scans: " + scans.size());\nSet<String> visitors = new HashSet<>();\n'
                 'for (String s : scans) {\n    visitors.add(s);\n}\nSystem.out.println("Different visitors: " + visitors.size());\n'
                 'if (visitors.contains(name)) {\n    System.out.println(name + ": was here");\n} else {\n'
                 '    System.out.println(name + ": was not here");\n}',
        wrong=[("считает разных посетителей по размеру списка — повторы учитываются несколько раз",
                'System.out.println("Scans: " + scans.size());\nSystem.out.println("Different visitors: " + scans.size());\n'
                'if (scans.contains(name)) {\n    System.out.println(name + ": was here");\n} else {\n'
                '    System.out.println(name + ": was not here");\n}'),
               ("ищет повторы только среди соседних записей — повтор через несколько проходов не замечает",
                'System.out.println("Scans: " + scans.size());\nint different = 0;\nfor (int i = 0; i < scans.size(); i++) {\n'
                '    if (i == 0 || !scans.get(i).equals(scans.get(i - 1))) {\n        different++;\n    }\n}\n'
                'System.out.println("Different visitors: " + different);\n'
                'if (scans.contains(name)) {\n    System.out.println(name + ": was here");\n} else {\n'
                '    System.out.println(name + ": was not here");\n}')],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-set-reused-tickets", title="Повторные билеты",
        given=[("List<Integer>", "tickets")],
        variants=[{"tickets": "new ArrayList<>(List.of(1041, 1042, 1043, 1041, 1044, 1045))"},
                  {"tickets": "new ArrayList<>(List.of(207, 315, 207, 118, 315, 207))"},
                  {"tickets": "new ArrayList<>(List.of(880, 881, 882, 880, 883, 884, 885))"}],
        hidden=[{"tickets": "new ArrayList<>(List.of(12))"},
                {"tickets": "new ArrayList<>(List.of(5, 5, 5, 5))"},
                {"tickets": "new ArrayList<>(List.of(300, 301, 302, 303, 304))"},
                {"tickets": "new ArrayList<>(List.of(71, 72, 72, 71))"}],
        intro="На входе в кинотеатр сканируют билеты. Номера отсканированных билетов записаны в список `tickets` "
              "по порядку. По каждому билету можно пройти только один раз, но кое-кто пытается пройти по уже "
              "использованному билету.",
        steps=["Создай пустое множество `Set<Integer> passed = new HashSet<>();` — в нём будут билеты, по которым уже прошли.",
               "Пройди по списку `tickets` по порядку и добавь каждый номер в `passed` методом `add`. Если `add` вернул "
               "`false` (такой билет уже есть в множестве), выведи строку вида `Used ticket: 1500`.",
               "Последней строкой выведи строку вида `Viewers in: 5` — сколько разных билетов оказалось в `passed`."],
        hint="Метод `add` у множества не только добавляет элемент, но и сообщает результат: `true` — элемент новый, "
             "`false` — такой уже был. Его можно проверить прямо в условии `if`.",
        solution='Set<Integer> passed = new HashSet<>();\nfor (int t : tickets) {\n    if (!passed.add(t)) {\n'
                 '        System.out.println("Used ticket: " + t);\n    }\n}\n'
                 'System.out.println("Viewers in: " + passed.size());',
        wrong=[("сначала добавляет билет, а потом проверяет contains — каждый билет кажется повторным",
                'Set<Integer> passed = new HashSet<>();\nfor (int t : tickets) {\n    passed.add(t);\n    if (passed.contains(t)) {\n'
                '        System.out.println("Used ticket: " + t);\n    }\n}\n'
                'System.out.println("Viewers in: " + passed.size());'),
               ("считает зрителей по всему списку — повторные проходы тоже засчитываются",
                'Set<Integer> passed = new HashSet<>();\nfor (int t : tickets) {\n    if (!passed.add(t)) {\n'
                '        System.out.println("Used ticket: " + t);\n    }\n}\n'
                'System.out.println("Viewers in: " + tickets.size());')],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-set-school-clubs", title="Два кружка",
        given=[("List<String>", "chess"), ("List<String>", "drawing")],
        variants=[{"chess": 'new ArrayList<>(List.of("Misha", "Anya", "Petya", "Misha", "Olya"))',
                   "drawing": 'new ArrayList<>(List.of("Olya", "Vera", "Anya", "Kirill"))'},
                  {"chess": 'new ArrayList<>(List.of("Dima", "Sasha", "Zhenya"))',
                   "drawing": 'new ArrayList<>(List.of("Zhenya", "Sasha", "Liza", "Zhenya", "Tanya"))'},
                  {"chess": 'new ArrayList<>(List.of("Timur", "Varya", "Gosha", "Ksyusha", "Boris"))',
                   "drawing": 'new ArrayList<>(List.of("Ksyusha", "Timur", "Varya", "Varya"))'}],
        hidden=[{"chess": 'new ArrayList<>(List.of("Ira"))', "drawing": 'new ArrayList<>(List.of("Ira"))'},
                {"chess": 'new ArrayList<>(List.of("Roman", "Zakhar"))', "drawing": 'new ArrayList<>(List.of("Nelli", "Yana"))'},
                {"chess": 'new ArrayList<>(List.of("Lev", "Lev", "Lev"))', "drawing": 'new ArrayList<>(List.of("Mila", "Lev", "Mila"))'},
                {"chess": "new ArrayList<>()", "drawing": 'new ArrayList<>(List.of("Ulyana", "Elya"))'}],
        intro="В школе открылись два кружка: шахматный и рисования. Списки записавшихся — `chess` и `drawing`. "
              "Некоторые ребята записались сразу в оба кружка, а кто-то по ошибке записался в один кружок дважды. "
              "`TreeSet` — множество, которое хранит элементы по алфавиту, — поможет разобраться.",
        steps=["Создай множество `Set<String> both = new TreeSet<>(chess);` и оставь в нём только тех, кто есть и в "
               "`drawing`, методом `retainAll`. Выведи `Both clubs: ` и сразу за этим множество `both`, например "
               "`Both clubs: [Gena, Lena]`.",
               "Создай ещё одну копию `chess` — тоже `TreeSet` — и убери из неё всех ребят из `drawing` методом `removeAll`. "
               "Выведи `Only chess: ` и это множество.",
               "Собери всех ребят из обоих кружков в одно множество (метод `addAll`) и выведи строку вида "
               "`Total kids: 7` — его размер."],
        hint="`retainAll` и `removeAll` меняют само множество, у которого их вызвали. Поэтому для каждой строки "
             "делай свою новую копию списка `chess`.",
        solution='Set<String> both = new TreeSet<>(chess);\nboth.retainAll(drawing);\nSystem.out.println("Both clubs: " + both);\n'
                 'Set<String> onlyChess = new TreeSet<>(chess);\nonlyChess.removeAll(drawing);\n'
                 'System.out.println("Only chess: " + onlyChess);\nSet<String> all = new TreeSet<>(chess);\n'
                 'all.addAll(drawing);\nSystem.out.println("Total kids: " + all.size());',
        wrong=[("работает с одним и тем же множеством — после retainAll в нём уже нет нужных ребят",
                'Set<String> kids = new TreeSet<>(chess);\nkids.retainAll(drawing);\nSystem.out.println("Both clubs: " + kids);\n'
                'kids.removeAll(drawing);\nSystem.out.println("Only chess: " + kids);\n'
                'kids.addAll(drawing);\nSystem.out.println("Total kids: " + kids.size());'),
               ("складывает размеры списков — ребята из обоих кружков и повторы считаются дважды",
                'Set<String> both = new TreeSet<>(chess);\nboth.retainAll(drawing);\nSystem.out.println("Both clubs: " + both);\n'
                'Set<String> onlyChess = new TreeSet<>(chess);\nonlyChess.removeAll(drawing);\n'
                'System.out.println("Only chess: " + onlyChess);\n'
                'System.out.println("Total kids: " + (chess.size() + drawing.size()));')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-set-sticker-album", title="Альбом с наклейками",
        given=[("List<Integer>", "stickers"), ("int", "total")],
        variants=[{"stickers": "new ArrayList<>(List.of(12, 5, 30, 5, 18, 12, 7))", "total": "40"},
                  {"stickers": "new ArrayList<>(List.of(3, 3, 3, 9, 1))", "total": "10"},
                  {"stickers": "new ArrayList<>(List.of(21, 4, 16, 8, 4, 25, 16, 2))", "total": "25"}],
        hidden=[{"stickers": "new ArrayList<>(List.of(1))", "total": "1"},
                {"stickers": "new ArrayList<>(List.of(6, 6, 6, 6))", "total": "50"},
                {"stickers": "new ArrayList<>(List.of(5, 4, 3, 2, 1))", "total": "5"},
                {"stickers": "new ArrayList<>(List.of(14, 2, 14, 9))", "total": "20"}],
        intro="Дима собирает альбом: в нём `total` мест для наклеек с номерами. Номера наклеек, которые выпали ему "
              "в пакетиках, записаны в список `stickers`, и многие попались дважды. В альбом каждая наклейка "
              "вклеивается только один раз.",
        steps=["Выведи строку вида `Stickers bought: 7` — сколько всего наклеек в списке `stickers`.",
               "Создай множество `Set<Integer> album = new TreeSet<>(stickers);` — оно само уберёт повторы и "
               "расставит номера по возрастанию. Выведи строку вида `Different stickers: 5` — его размер.",
               "Выведи `In the album: ` и сразу за этим множество `album`, например `In the album: [5, 7, 12]`.",
               "Последней строкой выведи строку вида `Missing: 35` — сколько мест в альбоме ещё пустые."],
        hint="Пустых мест столько, сколько всего мест минус число РАЗНЫХ наклеек: повторная наклейка новое место "
             "в альбоме не занимает.",
        solution='System.out.println("Stickers bought: " + stickers.size());\nSet<Integer> album = new TreeSet<>(stickers);\n'
                 'System.out.println("Different stickers: " + album.size());\nSystem.out.println("In the album: " + album);\n'
                 'System.out.println("Missing: " + (total - album.size()));',
        wrong=[("считает пустые места по числу всех наклеек — повторные тоже занимают место",
                'System.out.println("Stickers bought: " + stickers.size());\nSet<Integer> album = new TreeSet<>(stickers);\n'
                'System.out.println("Different stickers: " + album.size());\nSystem.out.println("In the album: " + album);\n'
                'System.out.println("Missing: " + (total - stickers.size()));'),
               ("сложил наклейки в список, а не в множество — повторы остались",
                'System.out.println("Stickers bought: " + stickers.size());\nList<Integer> album = new ArrayList<>(stickers);\n'
                'System.out.println("Different stickers: " + album.size());\nSystem.out.println("In the album: " + album);\n'
                'System.out.println("Missing: " + (total - album.size()));')],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-set-party-guests", title="Охранник на вечеринке",
        given=[("List<String>", "invited"), ("List<String>", "arrivals")],
        variants=[{"invited": 'new ArrayList<>(List.of("Anya", "Boris", "Vika", "Gleb"))',
                   "arrivals": 'new ArrayList<>(List.of("Boris", "Kolya", "Anya", "Boris"))'},
                  {"invited": 'new ArrayList<>(List.of("Lena", "Misha"))',
                   "arrivals": 'new ArrayList<>(List.of("Misha", "Misha", "Lena", "Oleg", "Lena"))'},
                  {"invited": 'new ArrayList<>(List.of("Pasha", "Rita", "Sasha", "Tanya", "Ulyana"))',
                   "arrivals": 'new ArrayList<>(List.of("Tanya", "Rita", "Sasha", "Pasha"))'}],
        hidden=[{"invited": 'new ArrayList<>(List.of("Ira"))', "arrivals": 'new ArrayList<>(List.of("Ira"))'},
                {"invited": 'new ArrayList<>(List.of("Fedya", "Zoya"))', "arrivals": 'new ArrayList<>(List.of("Yasha", "Yasha"))'},
                {"invited": 'new ArrayList<>(List.of("Nina", "Egor"))', "arrivals": 'new ArrayList<>(List.of("Egor", "Egor", "Egor", "Nina"))'},
                {"invited": 'new ArrayList<>(List.of("Kira"))', "arrivals": "new ArrayList<>()"}],
        intro="На день рождения позвали гостей из списка `invited`. Охранник у двери смотрит на каждого, кто подходит, — "
              "по порядку они записаны в список `arrivals`. Кого-то не звали, а кто-то, уже войдя, по ошибке "
              "подходит к двери ещё раз.",
        steps=["Создай множество приглашённых `Set<String> guests = new HashSet<>(invited);` и пустое множество "
               "`Set<String> inside = new HashSet<>();` — тех, кто уже вошёл.",
               "Для каждого имени из `arrivals` по порядку: если его нет среди приглашённых, выведи строку вида "
               "`Kolya is not on the list`; иначе если он уже есть в `inside`, выведи `Boris is already inside`; "
               "иначе добавь его в `inside` и выведи `Welcome, Boris`.",
               "Последней строкой выведи строку вида `Guests inside: 2` — сколько гостей в `inside`."],
        hint="Проверка `contains` у множества работает мгновенно, сколько бы гостей ни было. Порядок проверок важен: "
             "сначала «есть ли в списке приглашённых», потом «не вошёл ли уже».",
        solution='Set<String> guests = new HashSet<>(invited);\nSet<String> inside = new HashSet<>();\n'
                 'for (String name : arrivals) {\n    if (!guests.contains(name)) {\n'
                 '        System.out.println(name + " is not on the list");\n    } else if (inside.contains(name)) {\n'
                 '        System.out.println(name + " is already inside");\n    } else {\n        inside.add(name);\n'
                 '        System.out.println("Welcome, " + name);\n    }\n}\n'
                 'System.out.println("Guests inside: " + inside.size());',
        wrong=[("не проверяет, вошёл ли гость раньше, — повторно здоровается с тем же гостем",
                'Set<String> guests = new HashSet<>(invited);\nSet<String> inside = new HashSet<>();\n'
                'for (String name : arrivals) {\n    if (!guests.contains(name)) {\n'
                '        System.out.println(name + " is not on the list");\n    } else {\n        inside.add(name);\n'
                '        System.out.println("Welcome, " + name);\n    }\n}\n'
                'System.out.println("Guests inside: " + inside.size());'),
               ("сначала добавляет гостя в inside, а потом проверяет — каждый гость кажется уже вошедшим",
                'Set<String> guests = new HashSet<>(invited);\nSet<String> inside = new HashSet<>();\n'
                'for (String name : arrivals) {\n    if (!guests.contains(name)) {\n'
                '        System.out.println(name + " is not on the list");\n        continue;\n    }\n    inside.add(name);\n'
                '    if (inside.contains(name)) {\n        System.out.println(name + " is already inside");\n    } else {\n'
                '        System.out.println("Welcome, " + name);\n    }\n}\n'
                'System.out.println("Guests inside: " + inside.size());')],
        constructs=["for", "if"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-set-word-letters", title="Слова из одних и тех же букв",
        given=[("String", "first"), ("String", "second")],
        variants=[{"first": '"listen"', "second": '"silent"'},
                  {"first": '"apple"', "second": '"paper"'},
                  {"first": '"salad"', "second": '"lads"'}],
        hidden=[{"first": '"abcd"', "second": '"abce"'},
                {"first": '"cat"', "second": '"dog"'},
                {"first": '"aaa"', "second": '"a"'},
                {"first": '"night"', "second": '"thing"'}],
        intro="В игре «Слова» ребята проверяют, составлены ли два слова из одного и того же набора букв (сколько раз "
              "буква повторяется, неважно). Слова записаны в поля `first` и `second` маленькими английскими буквами.",
        steps=["Создай `Set<Character> a = new TreeSet<>();` и циклом по номерам добавь в него все буквы слова "
               "`first` (букву с номером `i` даёт `first.charAt(i)`). Так же собери множество `b` из букв `second`.",
               "Сделай копию `a` — новый `TreeSet` — и оставь в ней только буквы, которые есть и в `b`, методом "
               "`retainAll`. Выведи `Common letters: ` и эту копию, например `Common letters: [a, e, p]`.",
               "Сделай ещё одну копию `a`, добавь в неё все буквы `b` методом `addAll` и выведи строку вида "
               "`All letters: 5` — её размер.",
               "Если множества `a` и `b` равны (`a.equals(b)`), выведи `Same set of letters`, иначе — `Different letters`."],
        hint="`retainAll` и `addAll` меняют то множество, у которого их вызвали. Поэтому для каждой операции делай "
             "свою копию `a`, а сами `a` и `b` не трогай — они ещё нужны для сравнения в конце.",
        solution='Set<Character> a = new TreeSet<>();\nfor (int i = 0; i < first.length(); i++) {\n    a.add(first.charAt(i));\n}\n'
                 'Set<Character> b = new TreeSet<>();\nfor (int i = 0; i < second.length(); i++) {\n    b.add(second.charAt(i));\n}\n'
                 'Set<Character> common = new TreeSet<>(a);\ncommon.retainAll(b);\nSystem.out.println("Common letters: " + common);\n'
                 'Set<Character> all = new TreeSet<>(a);\nall.addAll(b);\nSystem.out.println("All letters: " + all.size());\n'
                 'if (a.equals(b)) {\n    System.out.println("Same set of letters");\n} else {\n'
                 '    System.out.println("Different letters");\n}',
        wrong=[("сравнивает длины слов вместо наборов букв",
                'Set<Character> a = new TreeSet<>();\nfor (int i = 0; i < first.length(); i++) {\n    a.add(first.charAt(i));\n}\n'
                'Set<Character> b = new TreeSet<>();\nfor (int i = 0; i < second.length(); i++) {\n    b.add(second.charAt(i));\n}\n'
                'Set<Character> common = new TreeSet<>(a);\ncommon.retainAll(b);\nSystem.out.println("Common letters: " + common);\n'
                'Set<Character> all = new TreeSet<>(a);\nall.addAll(b);\nSystem.out.println("All letters: " + all.size());\n'
                'if (first.length() == second.length()) {\n    System.out.println("Same set of letters");\n} else {\n'
                '    System.out.println("Different letters");\n}'),
               ("вызывает retainAll и addAll у самого множества a — оно портится",
                'Set<Character> a = new TreeSet<>();\nfor (int i = 0; i < first.length(); i++) {\n    a.add(first.charAt(i));\n}\n'
                'Set<Character> b = new TreeSet<>();\nfor (int i = 0; i < second.length(); i++) {\n    b.add(second.charAt(i));\n}\n'
                'a.retainAll(b);\nSystem.out.println("Common letters: " + a);\n'
                'a.addAll(b);\nSystem.out.println("All letters: " + a.size());\n'
                'if (a.equals(b)) {\n    System.out.println("Same set of letters");\n} else {\n'
                '    System.out.println("Different letters");\n}')],
        constructs=["for", "if"],
    ),
]
