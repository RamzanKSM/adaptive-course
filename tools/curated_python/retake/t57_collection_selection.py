"""PY_COLLECTION_SELECTION — «Выбор коллекции». Taught before: lists and their methods, tuples, sets, dicts, loops,
conditions, functions, classes. Here: the statement describes what the data must do (no repeats and fast `in` →
set; lookup by key → dict; keep order and repeats → list; fixed records → tuple) and the student picks the
collection; the structure check names the right one and says why. Not yet: comprehensions, try/except, lambda."""
from build import OutputTask

SKILL = "PY_COLLECTION_SELECTION"

COFFEE = """\
counts = {}
drinks = set()
for customer, drink in orders:
    counts[customer] = counts.get(customer, 0) + 1
    drinks.add(drink)
lucky = []
for customer, number in counts.items():
    print(f"{customer}: {number}")
    if number >= 3:
        lucky.append(customer)
if len(lucky) > 0:
    print(f"Free coffee: {', '.join(lucky)}")
else:
    print("Free coffee: nobody")
print("Drinks:", sorted(drinks))
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-sel-rt-ice-cream-line", title="Очередь за мороженым",
        given=["first", "second", "third", "late"],
        variants=[{"first": '"Anya"', "second": '"Boris"', "third": '"Vera"', "late": '"Gleb"'},
                  {"first": '"Dina"', "second": '"Egor"', "third": '"Dina"', "late": '"Zhenya"'},
                  {"first": '"Ilya"', "second": '"Kira"', "third": '"Lev"', "late": '"Ilya"'}],
        hidden=[{"first": '"Mila"', "second": '"Nik"', "third": '"Olya"', "late": '"Pasha"'},
                {"first": '"Rita"', "second": '"Rita"', "third": '"Rita"', "late": '"Rita"'},
                {"first": '"Sava"', "second": '"Tima"', "third": '"Uma"', "late": '"Sava"'}],
        intro="У киоска с мороженым выстроилась очередь: `first`, `second` и `third` — в таком порядке. Потом пришёл "
              "`late` и встал в конец. Иногда один человек покупает и для себя, и для друга, поэтому одно имя может "
              "стоять в очереди несколько раз. Порядок важен: продавец обслуживает с начала очереди.",
        steps=["Сложи три имени в порядке очереди в такую коллекцию, которая хранит порядок и повторы и которую можно "
               "менять — пополнять новыми элементами. Сохрани её в переменную `line`.",
               "Добавь `late` в конец этой коллекции.",
               "Выведи коллекцию командой `print(line)`, а следующей строкой — строку вида `People in line: 4` "
               "с её длиной."],
        hint="Множество выбросит повторы и потеряет порядок, а кортеж нельзя пополнять. Нужна коллекция в квадратных "
             "скобках — у неё есть метод `.append()`, который добавляет элемент в конец.",
        solution='line = [first, second, third]\nline.append(late)\nprint(line)\nprint(f"People in line: {len(line)}")',
        wrong=[("ставит опоздавшего в начало очереди",
                'line = [first, second, third]\nline.insert(0, late)\nprint(line)\nprint(f"People in line: {len(line)}")'),
               ("считает длину до того, как опоздавший встал в очередь",
                'line = [first, second, third]\nsize = len(line)\nline.append(late)\nprint(line)\n'
                'print(f"People in line: {size}")')],
        constructs=["list"],
        must_use=[("List", "Для очереди выбери список [...]: он хранит порядок и повторы, а пополнять его можно "
                           "методом .append().")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-sel-rt-never-came", title="Кто ни разу не пришёл",
        given=["group", "visits"],
        variants=[{"group": '["Anya", "Boris", "Vera", "Gleb", "Dina"]',
                   "visits": '["Boris", "Anya", "Boris", "Dina", "Anya", "Boris"]'},
                  {"group": '["Egor", "Zoya", "Ilya"]', "visits": '["Zoya", "Zoya", "Zoya"]'},
                  {"group": '["Kira", "Lev", "Mila", "Nik", "Olya", "Pasha"]',
                   "visits": '["Olya", "Kira", "Lev", "Olya", "Pasha", "Kira", "Nik"]'}],
        hidden=[{"group": '["Rita"]', "visits": '["Rita"]'},
                {"group": '["Sava", "Tima"]', "visits": '["Tima", "Tima", "Tima", "Tima"]'},
                {"group": '["Uma", "Vlad", "Yana", "Fedya"]', "visits": '["Yana"]'},
                {"group": '["Ada", "Ben", "Cid"]', "visits": '["Cid", "Ben", "Ada", "Ben"]'}],
        intro="В спортивной секции занимаются ребята из списка `group`. Тренер весь месяц записывал в список `visits` "
              "имя каждого, кто пришёл на тренировку, поэтому одно имя там встречается много раз. Тренеру нужно знать, "
              "сколько разных ребят ходило и кто не пришёл ни разу.",
        steps=["Выбери коллекцию, которая сама избавится от повторов в `visits` и умеет находить разницу с другой такой "
               "же коллекцией. Преврати в неё и `visits`, и `group`.",
               "Выведи строку вида `Came at least once: 4` — сколько разных ребят приходило.",
               "Найди тех, кто есть в группе, но ни разу не приходил. Выведи через `print` слово `Never came:` и через "
               "пробел их список, отсортированный функцией `sorted()`, например `Never came: ['Gleb', 'Vera']`."],
        hint="Множество хранит каждый элемент один раз, а `a - b` даёт элементы `a`, которых нет в `b`. Порядок важен: "
             "из группы вычитают тех, кто приходил, а не наоборот. Перед печатью множество нужно отсортировать.",
        solution='came = set(visits)\nprint(f"Came at least once: {len(came)}")\n'
                 'print("Never came:", sorted(set(group) - came))',
        wrong=[("считает все посещения, а не разных ребят",
                'came = set(visits)\nprint(f"Came at least once: {len(visits)}")\n'
                'print("Never came:", sorted(set(group) - came))'),
               ("вычитает в обратном порядке — список всегда пустой",
                'came = set(visits)\nprint(f"Came at least once: {len(came)}")\n'
                'print("Never came:", sorted(came - set(group)))')],
        must_use=[("re:\\bset\\(", "Выбери множество set: оно убирает повторы в посещениях и умеет вычитать одну "
                                   "коллекцию из другой.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-sel-rt-coffee-loyalty", title="Бонусы в кофейне",
        given=["orders"],
        variants=[{"orders": '[("Anya", "latte"), ("Boris", "tea"), ("Anya", "latte"), ("Vera", "cocoa"), '
                             '("Anya", "espresso"), ("Boris", "latte")]'},
                  {"orders": '[("Gleb", "tea"), ("Dina", "tea"), ("Gleb", "tea"), ("Dina", "tea")]'},
                  {"orders": '[("Egor", "mocha"), ("Zoya", "latte"), ("Zoya", "latte"), ("Egor", "cocoa"), '
                             '("Zoya", "tea"), ("Ilya", "mocha"), ("Egor", "latte")]'}],
        hidden=[{"orders": '[("Kira", "tea")]'},
                {"orders": '[("Lev", "latte"), ("Lev", "latte"), ("Lev", "latte"), ("Mila", "tea"), ("Mila", "tea"), '
                           '("Mila", "cocoa")]'},
                {"orders": '[("Nik", "flat white"), ("Olya", "raf"), ("Nik", "raf")]'},
                {"orders": '[("Pasha", "tea"), ("Rita", "tea"), ("Pasha", "tea"), ("Rita", "tea"), ("Pasha", "mocha")]'}],
        intro="Кофейня записывает заказы в список `orders` в том порядке, в котором их делали. Каждый заказ — кортеж "
              "из имени покупателя и напитка. Кто сделал 3 заказа и больше, получает бесплатный кофе. Ещё бариста "
              "хочет знать, какие разные напитки заказывали.",
        steps=["Выбери коллекцию, в которой по имени покупателя сразу находится число его заказов, и посчитай заказы "
               "каждого, пройдя по `orders`. Покупатели должны остаться в порядке своего первого заказа.",
               "В том же цикле собирай напитки в такую коллекцию, которая сама избавляется от повторов.",
               "Для каждого покупателя выведи строку вида `Anya: 3` — имя и число заказов, в порядке первого заказа.",
               "Следующей строкой выведи строку вида `Free coffee: Anya, Vera` — имена тех, у кого 3 заказа и больше, "
               "через запятую и пробел в том же порядке, или `Free coffee: nobody`, если таких нет.",
               "Последней строкой выведи через `print` слово `Drinks:` и через пробел отсортированный функцией `sorted()` "
               "список разных напитков, например `Drinks: ['cocoa', 'tea']`."],
        hint="Для счёта подойдёт словарь: `counts.get(name, 0) + 1` — новое число заказов, даже если покупатель пришёл "
             "впервые. Словарь хранит ключи в порядке добавления. Имена счастливчиков удобно складывать в список "
             'и потом склеить через `", ".join(...)`, а напитки — в множество.',
        solution=COFFEE,
        wrong=[("бесплатный кофе только тем, у кого больше трёх заказов",
                COFFEE.replace("    if number >= 3:", "    if number > 3:")),
               ("считает напитки списком — повторы попадают в вывод",
                COFFEE.replace("drinks = set()\n", "drinks = []\n").replace("    drinks.add(drink)\n",
                                                                         "    drinks.append(drink)\n")),
               ("записывает 1 вместо того, чтобы прибавлять, — у каждого по одному заказу",
                COFFEE.replace("    counts[customer] = counts.get(customer, 0) + 1\n", "    counts[customer] = 1\n"))],
        constructs=["dict", "for"],
        must_use=[("re:\\bset\\(", "Для разных напитков выбери множество set(): каждый напиток попадёт в него один раз."),
                  ("Dict", "Для числа заказов выбери словарь: создай его фигурными скобками {} — ключом будет имя "
                           "покупателя, значением — число заказов.")],
    ),
]
