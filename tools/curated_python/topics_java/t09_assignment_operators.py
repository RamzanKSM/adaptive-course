"""ASSIGNMENT_OPERATORS — «Составное присваивание и инкремент» (Java). Taught before: println, variables, assignment,
arithmetic, execution order, primitive types, String, / and %. The point: += -= *= /= %= change a variable using its
own value, ++ and -- add or take one; the order of the updates matters, and `x =+ 5` is not `x += 5`.
Not yet: if/else, comparisons, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "ASSIGNMENT_OPERATORS"

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-aug-pocket-money", title="Карманные деньги за день",
        given=[("int", "money"), ("int", "lunch"), ("int", "bus"), ("int", "gift")],
        variants=[{"money": "500", "lunch": "250", "bus": "60", "gift": "100"},
                  {"money": "1000", "lunch": "320", "bus": "45", "gift": "200"},
                  {"money": "300", "lunch": "180", "bus": "40", "gift": "500"}],
        hidden=[{"money": "100", "lunch": "50", "bus": "50", "gift": "0"}, {"money": "0", "lunch": "0", "bus": "0", "gift": "1000"},
                {"money": "750", "lunch": "400", "bus": "70", "gift": "30"}],
        intro="Утром у Ани в кошельке `money` рублей. Днём она платит за обед (`lunch` рублей) и за автобус (`bus` рублей), "
              "а вечером бабушка дарит ей `gift` рублей.",
        steps=["Выведи `Morning: `, сумму в кошельке и ` rub`.",
               "Уменьши `money` на стоимость обеда, затем на стоимость автобуса — операцией `-=`.",
               "Выведи `After lunch and bus: `, сумму и ` rub`.",
               "Увеличь `money` на подарок операцией `+=` и выведи `Evening: `, сумму и ` rub`."],
        hint="`money -= lunch;` — то же самое, что `money = money - lunch;`: из переменной берётся старое значение, "
             "и туда же записывается новое. Знаки пишутся именно в таком порядке: сначала `+` или `-`, потом `=`.",
        solution='System.out.println("Morning: " + money + " rub");\n'
                 'money -= lunch;\n'
                 'money -= bus;\n'
                 'System.out.println("After lunch and bus: " + money + " rub");\n'
                 'money += gift;\n'
                 'System.out.println("Evening: " + money + " rub");',
        wrong=[("=+ вместо +=: в money записывается просто подарок",
                'System.out.println("Morning: " + money + " rub");\n'
                'money -= lunch;\n'
                'money -= bus;\n'
                'System.out.println("After lunch and bus: " + money + " rub");\n'
                'money =+ gift;\n'
                'System.out.println("Evening: " + money + " rub");'),
               ("+= вместо -=: за автобус деньги прибавляются",
                'System.out.println("Morning: " + money + " rub");\n'
                'money -= lunch;\n'
                'money += bus;\n'
                'System.out.println("After lunch and bus: " + money + " rub");\n'
                'money += gift;\n'
                'System.out.println("Evening: " + money + " rub");')],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-aug-game-level", title="Очки после уровня",
        given=[("int", "score"), ("int", "coins"), ("int", "lives")],
        variants=[{"score": "100", "coins": "7", "lives": "3"}, {"score": "0", "coins": "12", "lives": "5"},
                  {"score": "250", "coins": "3", "lives": "2"}],
        hidden=[{"score": "50", "coins": "0", "lives": "1"}, {"score": "1000", "coins": "25", "lives": "9"},
                {"score": "10", "coins": "1", "lives": "4"}],
        intro="Игрок прошёл уровень в игре. До уровня у него было `score` очков и `lives` жизней. На уровне он собрал "
              "`coins` монет, каждая стоит 10 очков.",
        steps=["Прибавь к `score` очки за монеты: `coins` умножить на `10` — операцией `+=`.",
               "На уровне действовал удвоитель: умножь `score` на `2` операцией `*=`.",
               "Игрок один раз врезался в шип: уменьши `lives` на один операцией `--` и отними от `score` штраф `50` "
               "операцией `-=`.",
               "Выведи `Score: ` и очки, затем `Lives: ` и жизни."],
        hint="Порядок важен: удвоитель умножает очки уже вместе с монетами. `lives--;` — это короткая запись "
             "`lives = lives - 1;`.",
        solution='score += coins * 10;\n'
                 'score *= 2;\n'
                 'lives--;\n'
                 'score -= 50;\n'
                 'System.out.println("Score: " + score);\n'
                 'System.out.println("Lives: " + lives);',
        wrong=[("++ вместо --: жизнь прибавляется",
                'score += coins * 10;\n'
                'score *= 2;\n'
                'lives++;\n'
                'score -= 50;\n'
                'System.out.println("Score: " + score);\n'
                'System.out.println("Lives: " + lives);'),
               ("удвоитель применён до монет: монеты не удваиваются",
                'score *= 2;\n'
                'score += coins * 10;\n'
                'lives--;\n'
                'score -= 50;\n'
                'System.out.println("Score: " + score);\n'
                'System.out.println("Lives: " + lives);')],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-aug-bus-passengers", title="Пассажиры автобуса",
        given=[("int", "passengers"), ("int", "entered"), ("int", "left")],
        variants=[{"passengers": "20", "entered": "7", "left": "4"}, {"passengers": "12", "entered": "9", "left": "2"},
                  {"passengers": "35", "entered": "3", "left": "10"}],
        hidden=[{"passengers": "0", "entered": "5", "left": "0"}, {"passengers": "10", "entered": "0", "left": "10"},
                {"passengers": "40", "entered": "10", "left": "5"}, {"passengers": "8", "entered": "2", "left": "1"}],
        intro="Водитель автобуса считает пассажиров. Со старта едут `passengers` человек. На первой остановке вошли "
              "`entered` человек и вышли `left`. На второй остановке вошёл ещё один человек — контролёр, а потом у "
              "университета вышла половина всех, кто был в автобусе.",
        steps=["Выведи `Start: ` и число пассажиров.",
               "Первая остановка: прибавь вошедших операцией `+=`, отними вышедших операцией `-=` и выведи `After stop 1: ` и число пассажиров.",
               "Вторая остановка: добавь контролёра операцией `++`, затем раздели число пассажиров на `2` операцией `/=` "
               "(при нечётном числе вышло на одного больше, и деление нацело как раз это учитывает).",
               "Выведи `After stop 2: ` и число пассажиров."],
        hint="Все изменения делаются над одной переменной `passengers`, по очереди, как едет автобус. "
             "Следи за порядком знаков: `+=` прибавляет, а `=+` просто записывает новое значение.",
        solution='System.out.println("Start: " + passengers);\n'
                 'passengers += entered;\n'
                 'passengers -= left;\n'
                 'System.out.println("After stop 1: " + passengers);\n'
                 'passengers++;\n'
                 'passengers /= 2;\n'
                 'System.out.println("After stop 2: " + passengers);',
        wrong=[("=+ вместо +=: в автобусе остаются только вошедшие",
                'System.out.println("Start: " + passengers);\n'
                'passengers =+ entered;\n'
                'passengers -= left;\n'
                'System.out.println("After stop 1: " + passengers);\n'
                'passengers++;\n'
                'passengers /= 2;\n'
                'System.out.println("After stop 2: " + passengers);'),
               ("-- вместо ++: контролёр не входит, а выходит",
                'System.out.println("Start: " + passengers);\n'
                'passengers += entered;\n'
                'passengers -= left;\n'
                'System.out.println("After stop 1: " + passengers);\n'
                'passengers--;\n'
                'passengers /= 2;\n'
                'System.out.println("After stop 2: " + passengers);')],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-aug-pancake-recipe", title="Блины на большую семью",
        given=[("int", "flour"), ("int", "milk"), ("int", "eggs"), ("int", "times")],
        variants=[{"flour": "200", "milk": "500", "eggs": "2", "times": "3"},
                  {"flour": "150", "milk": "400", "eggs": "1", "times": "4"},
                  {"flour": "250", "milk": "600", "eggs": "3", "times": "2"}],
        hidden=[{"flour": "100", "milk": "250", "eggs": "1", "times": "1"}, {"flour": "300", "milk": "750", "eggs": "2", "times": "5"},
                {"flour": "180", "milk": "450", "eggs": "3", "times": "10"}],
        intro="В рецепте блинов указано `flour` граммов муки, `milk` миллилитров молока и `eggs` яиц. Гостей много, "
              "поэтому всё нужно взять в `times` раз больше. А ещё бабушка всегда кладёт одно яйцо сверх рецепта и берёт "
              "50 граммов муки, чтобы присыпать стол.",
        steps=["Увеличь `flour`, `milk` и `eggs` в `times` раз — каждую операцией `*=`.",
               "Уже после этого добавь одно яйцо операцией `++` и 50 граммов муки операцией `+=`.",
               "Выведи три строки: `Flour: `, мука и ` g`; `Milk: `, молоко и ` ml`; `Eggs: ` и число яиц."],
        hint="`eggs *= times;` — то же, что `eggs = eggs * times;`. Лишнее яйцо добавляется к уже увеличенному "
             "количеству, поэтому `++` должен идти после `*=`, а не до него.",
        solution='flour *= times;\n'
                 'milk *= times;\n'
                 'eggs *= times;\n'
                 'eggs++;\n'
                 'flour += 50;\n'
                 'System.out.println("Flour: " + flour + " g");\n'
                 'System.out.println("Milk: " + milk + " ml");\n'
                 'System.out.println("Eggs: " + eggs);',
        wrong=[("+= вместо *=: к яйцам прибавлено times, а не умножено",
                'flour *= times;\n'
                'milk *= times;\n'
                'eggs += times;\n'
                'eggs++;\n'
                'flour += 50;\n'
                'System.out.println("Flour: " + flour + " g");\n'
                'System.out.println("Milk: " + milk + " ml");\n'
                'System.out.println("Eggs: " + eggs);'),
               ("лишнее яйцо добавлено до умножения: оно тоже умножается",
                'flour *= times;\n'
                'milk *= times;\n'
                'eggs++;\n'
                'eggs *= times;\n'
                'flour += 50;\n'
                'System.out.println("Flour: " + flour + " g");\n'
                'System.out.println("Milk: " + milk + " ml");\n'
                'System.out.println("Eggs: " + eggs);')],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-aug-cafe-bill", title="Счёт в кафе на компанию",
        given=[("int", "bill"), ("int", "tip"), ("int", "coupon"), ("int", "people")],
        variants=[{"bill": "2000", "tip": "10", "coupon": "150", "people": "4"},
                  {"bill": "3450", "tip": "15", "coupon": "300", "people": "3"},
                  {"bill": "1800", "tip": "5", "coupon": "100", "people": "6"}],
        hidden=[{"bill": "1000", "tip": "0", "coupon": "0", "people": "1"}, {"bill": "999", "tip": "10", "coupon": "99", "people": "7"},
                {"bill": "5000", "tip": "20", "coupon": "500", "people": "9"}, {"bill": "640", "tip": "5", "coupon": "40", "people": "2"}],
        intro="Друзья отмечают день рождения в кафе. Счёт — `bill` рублей. Они оставляют чаевые `tip` процентов от счёта "
              "и расплачиваются купоном на `coupon` рублей. Каждый платит поровну целое число рублей, а то, что не делится "
              "поровну, доплачивает именинник.",
        steps=["Прибавь к `bill` чаевые — `bill * tip / 100` — операцией `+=`.",
               "Отними купон операцией `-=` и выведи `To pay: `, сумму и ` rub`.",
               "Заведи `int each` — сколько целых рублей платит каждый: `bill`, делённый нацело на `people`.",
               "Отними от `bill` всё, что заплатили друзья вместе (`each * people`), операцией `-=` — в `bill` останется доплата.",
               "Выведи `Each pays: `, `each` и ` rub`, затем `Birthday adds: `, доплату и ` rub`."],
        hint="`bill += bill * tip / 100;` сначала вычисляет правую часть по старому значению `bill`, а потом прибавляет. "
             "Чаевые считаются от счёта до купона, поэтому купон вычитается после них.",
        solution='bill += bill * tip / 100;\n'
                 'bill -= coupon;\n'
                 'System.out.println("To pay: " + bill + " rub");\n'
                 'int each = bill / people;\n'
                 'bill -= each * people;\n'
                 'System.out.println("Each pays: " + each + " rub");\n'
                 'System.out.println("Birthday adds: " + bill + " rub");',
        wrong=[("чаевые прибавлены как рубли, а не как проценты",
                'bill += tip;\n'
                'bill -= coupon;\n'
                'System.out.println("To pay: " + bill + " rub");\n'
                'int each = bill / people;\n'
                'bill -= each * people;\n'
                'System.out.println("Each pays: " + each + " rub");\n'
                'System.out.println("Birthday adds: " + bill + " rub");'),
               ("отнята доля только одного друга, а не всех",
                'bill += bill * tip / 100;\n'
                'bill -= coupon;\n'
                'System.out.println("To pay: " + bill + " rub");\n'
                'int each = bill / people;\n'
                'bill -= each;\n'
                'System.out.println("Each pays: " + each + " rub");\n'
                'System.out.println("Birthday adds: " + bill + " rub");')],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-aug-vending-change", title="Сдача монетами в автомате",
        given=[("int", "change")],
        variants=[{"change": "37"}, {"change": "48"}, {"change": "29"}],
        hidden=[{"change": "0"}, {"change": "9"}, {"change": "10"}, {"change": "1"}, {"change": "64"}, {"change": "3"}],
        intro="Автомат с напитками выдаёт сдачу `change` рублей монетами по 10, 5, 2 и 1 рубль — начиная с крупных и "
              "каждый раз как можно больше монет. Сколько сдачи осталось выдать, автомат хранит в той же переменной `change`.",
        steps=["Заведи `int tens` — сколько монет по 10 рублей: `change`, делённый нацело на `10`. "
               "Затем оставь в `change` только остаток операцией `%=`.",
               "Так же по очереди заведи `int fives` (монеты по 5) и `int twos` (монеты по 2), и после каждой — `%=`.",
               "То, что осталось в `change`, — это монеты по 1 рублю.",
               "Выведи четыре строки: `10 rub: `, `5 rub: `, `2 rub: `, `1 rub: ` — после каждой надписи число таких монет."],
        hint="`change %= 10;` — это `change = change % 10;`: после выдачи десяток в переменной остаётся меньше 10 рублей. "
             "Не путай с `/=`: он оставил бы число десяток, а не остаток.",
        solution='int tens = change / 10;\n'
                 'change %= 10;\n'
                 'int fives = change / 5;\n'
                 'change %= 5;\n'
                 'int twos = change / 2;\n'
                 'change %= 2;\n'
                 'System.out.println("10 rub: " + tens);\n'
                 'System.out.println("5 rub: " + fives);\n'
                 'System.out.println("2 rub: " + twos);\n'
                 'System.out.println("1 rub: " + change);',
        wrong=[("/= вместо %=: в change остаётся число десяток, а не остаток",
                'int tens = change / 10;\n'
                'change /= 10;\n'
                'int fives = change / 5;\n'
                'change %= 5;\n'
                'int twos = change / 2;\n'
                'change %= 2;\n'
                'System.out.println("10 rub: " + tens);\n'
                'System.out.println("5 rub: " + fives);\n'
                'System.out.println("2 rub: " + twos);\n'
                'System.out.println("1 rub: " + change);'),
               ("-= 5 вместо %= 5: если пятёрки не было, сдача уходит в минус",
                'int tens = change / 10;\n'
                'change %= 10;\n'
                'int fives = change / 5;\n'
                'change -= 5;\n'
                'int twos = change / 2;\n'
                'change %= 2;\n'
                'System.out.println("10 rub: " + tens);\n'
                'System.out.println("5 rub: " + fives);\n'
                'System.out.println("2 rub: " + twos);\n'
                'System.out.println("1 rub: " + change);')],
        constructs=["augmented_assignment"],
    ),
]
