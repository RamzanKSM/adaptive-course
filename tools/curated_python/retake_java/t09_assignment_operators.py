"""ASSIGNMENT_OPERATORS — «Составное присваивание и инкремент» (Java). Taught before: println, variables, assignment,
arithmetic, execution order, primitive types, String, / and %. The point: += -= *= /= %= change a variable using its
own value, ++ and -- add or take one; the order of the updates matters, and `x =+ 5` is not `x += 5`.
Not yet: if/else, comparisons, loops, arrays, own methods."""
from java_tasks import JavaOutputTask

SKILL = "ASSIGNMENT_OPERATORS"


def _main(*lines: str) -> str:
    return "\n".join(lines)


def _likes(add: str, minus: str, times: str, plus: str) -> str:
    return _main(add, minus, times, plus,
                 'System.out.println("Likes: " + likes);',
                 'System.out.println("Comments: " + comments);')


def _candies(add: str, eaten: str, split: str) -> str:
    return _main(add, eaten,
                 'System.out.println("Total: " + candies);',
                 'int each = candies / kids;',
                 split,
                 'System.out.println("Each kid: " + each);',
                 'System.out.println("Left for mom: " + candies);')


def _deposit(year1: str, year2: str) -> str:
    return _main('int start = money;',
                 year1,
                 'money += topUp;',
                 'System.out.println("Year 1: " + money + " rub");',
                 year2,
                 'System.out.println("Year 2: " + money + " rub");',
                 'System.out.println("Profit: " + (money - start - topUp) + " rub");')


TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-aug-rt-post-likes", title="Лайки под постом",
        given=[("int", "likes"), ("int", "morning"), ("int", "comments")],
        variants=[{"likes": "40", "morning": "25", "comments": "6"}, {"likes": "120", "morning": "31", "comments": "0"},
                  {"likes": "7", "morning": "14", "comments": "3"}],
        hidden=[{"likes": "1", "morning": "0", "comments": "1"}, {"likes": "300", "morning": "100", "comments": "50"},
                {"likes": "15", "morning": "6", "comments": "9"}],
        intro="Вечером у поста было `likes` лайков и `comments` комментариев. Утром добавилось ещё `morning` лайков, потом "
              "один человек убрал свой лайк, а потом пост попал в рекомендации, и лайков стало втрое больше. "
              "Под конец кто-то оставил ещё один комментарий.",
        steps=["Прибавь утренние лайки к `likes` операцией `+=`.",
               "Убери один лайк операцией `--`.",
               "Утрой лайки операцией `*=`.",
               "Добавь один комментарий операцией `++`.",
               "Выведи `Likes: ` и `likes`, затем `Comments: ` и `comments`."],
        hint="`likes *= 3;` — то же самое, что `likes = likes * 3;`. Порядок важен: утраиваются лайки, которые были "
             "к этому моменту, — уже вместе с утренними и без убранного.",
        solution=_likes('likes += morning;', 'likes--;', 'likes *= 3;', 'comments++;'),
        wrong=[("=+ вместо +=: в likes записываются только утренние лайки",
                _likes('likes =+ morning;', 'likes--;', 'likes *= 3;', 'comments++;')),
               ("утраивает до того, как прибавить утренние лайки",
                _likes('likes *= 3;', 'likes--;', 'likes += morning;', 'comments++;'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-aug-rt-party-candies", title="Конфеты на празднике",
        given=[("int", "candies"), ("int", "packs"), ("int", "kids")],
        variants=[{"candies": "13", "packs": "3", "kids": "5"}, {"candies": "4", "packs": "5", "kids": "8"},
                  {"candies": "21", "packs": "2", "kids": "6"}],
        hidden=[{"candies": "1", "packs": "1", "kids": "2"}, {"candies": "0", "packs": "4", "kids": "3"},
                {"candies": "31", "packs": "0", "kids": "10"}, {"candies": "50", "packs": "6", "kids": "7"}],
        intro="К детскому празднику в вазе лежало `candies` конфет. Мама купила ещё `packs` пачек по 10 конфет и одну "
              "конфету съела сама, пока раскладывала. Потом конфеты поровну раздали `kids` детям, а то, что не делится "
              "поровну, осталось маме.",
        steps=["Добавь к `candies` конфеты из пачек операцией `+=`, затем убери съеденную операцией `--`.",
               "Выведи `Total: ` и `candies`.",
               "Заведи `int each` — сколько конфет получит каждый ребёнок: `candies`, делённое нацело на `kids`.",
               "Оставь в `candies` только остаток от деления на `kids` операцией `%=`.",
               "Выведи `Each kid: ` и `each`, затем `Left for mom: ` и `candies`."],
        hint="`candies %= kids;` — это `candies = candies % kids;`: в переменной остаются конфеты, которые не удалось "
             "раздать поровну. Не путай с `/=` — он оставил бы долю одного ребёнка.",
        solution=_candies('candies += packs * 10;', 'candies--;', 'candies %= kids;'),
        wrong=[("/= вместо %=: маме остаётся столько же, сколько каждому ребёнку",
                _candies('candies += packs * 10;', 'candies--;', 'candies /= kids;')),
               ("прибавляет число пачек, а не конфеты в них",
                _candies('candies += packs;', 'candies--;', 'candies %= kids;'))],
        constructs=["augmented_assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-aug-rt-bank-deposit", title="Вклад на два года",
        given=[("int", "money"), ("int", "percent"), ("int", "topUp")],
        variants=[{"money": "10000", "percent": "10", "topUp": "5000"},
                  {"money": "50000", "percent": "8", "topUp": "10000"},
                  {"money": "20000", "percent": "15", "topUp": "2000"}],
        hidden=[{"money": "1000", "percent": "0", "topUp": "0"}, {"money": "100000", "percent": "12", "topUp": "0"},
                {"money": "3000", "percent": "7", "topUp": "1500"}, {"money": "40000", "percent": "5", "topUp": "25000"}],
        intro="Бабушка положила на вклад `money` рублей под `percent` процентов в год. В конце каждого года банк "
              "прибавляет проценты от того, что лежит на вкладе в этот момент (дробные копейки банк отбрасывает). "
              "После первого года бабушка пополнила вклад на `topUp` рублей.",
        steps=["Заведи `int start` и сохрани в неё начальную сумму `money`.",
               "Первый год: прибавь к `money` проценты — `money * percent / 100` — операцией `+=`, затем пополнение `topUp` "
               "тоже операцией `+=`. Выведи `Year 1: `, сумму и ` rub`.",
               "Второй год: снова прибавь проценты так же и выведи `Year 2: `, сумму и ` rub`.",
               "Выведи `Profit: `, доход по вкладу и ` rub` — итоговая сумма минус `start` и минус пополнение (возьми выражение в скобки)."],
        hint="`money += money * percent / 100;` сначала считает правую часть по текущему значению `money`, а потом "
             "прибавляет. Поэтому во втором году проценты начисляются и на проценты первого года, и на пополнение.",
        solution=_deposit('money += money * percent / 100;', 'money += money * percent / 100;'),
        wrong=[("проценты прибавлены как рубли, а не как доля вклада",
                _deposit('money += percent;', 'money += percent;')),
               ("во втором году проценты считает от начальной суммы",
                _deposit('money += money * percent / 100;', 'money += start * percent / 100;'))],
        constructs=["augmented_assignment"],
    ),
]
