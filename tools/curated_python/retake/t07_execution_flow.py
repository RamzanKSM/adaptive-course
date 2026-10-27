"""PY_EXECUTION_FLOW_BASIC — «Порядок выполнения». Taught before: print (several values separated by commas), variables,
assignment, arithmetic (+ - *). Commands run from top to bottom; a variable holds the value of its last assignment and does
not recalculate by itself. Not yet: int/float details, strings beyond literals, type conversion, // and %, += -=,
f-strings, conditions, loops, functions."""
from build import OutputTask

SKILL = "PY_EXECUTION_FLOW_BASIC"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-ef-rt-sunflower", title="Как растёт подсолнух",
        given=["height", "growth"],
        variants=[{"height": "12", "growth": "7"}, {"height": "30", "growth": "15"}, {"height": "5", "growth": "4"}],
        hidden=[{"height": "0", "growth": "10"}, {"height": "100", "growth": "1"}, {"height": "48", "growth": "0"}],
        intro="Школьники выращивают подсолнух и каждую неделю его измеряют. Сейчас его высота `height = {height}` см, "
              "и за неделю он вырастает на `growth = {growth}` см.",
        steps=["Сохрани текущую высоту в переменную `start` — до того, как высота изменится.",
               "Первая неделя: присвой `height` значение `height` плюс `growth`. Выведи `Week 1:` и `height`.",
               "Вторая неделя: ещё раз присвой `height` значение `height` плюс `growth`. Выведи `Week 2:` и `height`.",
               "Последней строкой выведи `Grown by:` и `height` минус `start`. Например, при росте 3 см в неделю "
               "это `Grown by: 6`."],
        hint="Строка `height = height + growth` берёт справа то значение `height`, которое лежит в переменной сейчас, "
             "и кладёт результат обратно. Выполни её два раза — и подсолнух вырастет дважды. "
             "А начальную высоту нужно запомнить заранее: потом её в `height` уже не будет.",
        solution='start = height\nheight = height + growth\nprint("Week 1:", height)\n'
                 'height = height + growth\nprint("Week 2:", height)\nprint("Grown by:", height - start)',
        wrong=[("во второй неделе снова считает от начальной высоты — подсолнух не растёт",
                'start = height\nheight = height + growth\nprint("Week 1:", height)\n'
                'height = start + growth\nprint("Week 2:", height)\nprint("Grown by:", height - start)'),
               ("запоминает начальную высоту уже после первой недели",
                'height = height + growth\nstart = height\nprint("Week 1:", height)\n'
                'height = height + growth\nprint("Week 2:", height)\nprint("Grown by:", height - start)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-ef-rt-basketball-lead", title="Отрыв в баскетболе",
        given=["home", "away"],
        variants=[{"home": "54", "away": "48"}, {"home": "70", "away": "71"}, {"home": "33", "away": "25"}],
        hidden=[{"home": "60", "away": "60"}, {"home": "12", "away": "40"}, {"home": "90", "away": "88"}],
        intro="На табло баскетбольного матча хозяева набрали `home = {home}` очков, гости — `away = {away}`. "
              "Табло показывает и отрыв хозяев. Потом гости забивают трёхочковый, а хозяева отвечают двухочковым. "
              "Важно: посчитанный раньше отрыв сам не меняется, когда меняется счёт.",
        steps=["Посчитай `lead` — `home` минус `away`. Выведи `Score:`, `home` и `away` одним `print`, "
               "затем `Lead:` и `lead`.",
               "Гости забили 3 очка: присвой `away` значение `away` плюс 3. Хозяева забили 2 очка: присвой `home` "
               "значение `home` плюс 2.",
               "Выведи `Score:`, `home` и `away`, затем `Old lead:` и `lead` — ничего не пересчитывая.",
               "Пересчитай `lead` по той же формуле и выведи `New lead:` и `lead`."],
        hint="`lead = home - away` вычисляется один раз — когда Python доходит до этой строки. Когда счёт потом меняется, "
             "в `lead` остаётся старое число, пока ты не напишешь формулу ещё раз. Отрыв бывает и отрицательным: "
             "значит, впереди гости.",
        solution='lead = home - away\nprint("Score:", home, away)\nprint("Lead:", lead)\naway = away + 3\nhome = home + 2\n'
                 'print("Score:", home, away)\nprint("Old lead:", lead)\nlead = home - away\nprint("New lead:", lead)',
        wrong=[("не пересчитывает отрыв — думает, что lead обновится сам",
                'lead = home - away\nprint("Score:", home, away)\nprint("Lead:", lead)\naway = away + 3\nhome = home + 2\n'
                'print("Score:", home, away)\nprint("Old lead:", lead)\nprint("New lead:", lead)'),
               ("считает очки гостей, но не сохраняет их в away",
                'lead = home - away\nprint("Score:", home, away)\nprint("Lead:", lead)\naway + 3\nhome = home + 2\n'
                'print("Score:", home, away)\nprint("Old lead:", lead)\nlead = home - away\nprint("New lead:", lead)'),
               ("вычитает в обратном порядке",
                'lead = away - home\nprint("Score:", home, away)\nprint("Lead:", lead)\naway = away + 3\nhome = home + 2\n'
                'print("Score:", home, away)\nprint("Old lead:", lead)\nlead = away - home\nprint("New lead:", lead)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-ef-rt-salary-savings", title="Зарплата и копилка",
        given=["card", "savings", "salary", "save", "rent"],
        variants=[{"card": "3000", "savings": "10000", "salary": "45000", "save": "8000", "rent": "20000"},
                  {"card": "500", "savings": "0", "salary": "30000", "save": "5000", "rent": "15000"},
                  {"card": "12000", "savings": "40000", "salary": "60000", "save": "15000", "rent": "25000"}],
        hidden=[{"card": "0", "savings": "2000", "salary": "20000", "save": "0", "rent": "18000"},
                {"card": "7000", "savings": "7000", "salary": "50000", "save": "20000", "rent": "10000"},
                {"card": "1500", "savings": "300", "salary": "35000", "save": "1000", "rent": "34000"}],
        intro="У Веры два счёта: на карте `card = {card}` руб., на накопительном счёте `savings = {savings}` руб. "
              "Приходит зарплата `salary = {salary}` руб. на карту, Вера сразу переводит `save = {save}` руб. "
              "с карты на накопительный счёт и платит за квартиру `rent = {rent}` руб. с карты.",
        steps=["Посчитай `total` — `card` плюс `savings`. Выведи `Before:` и `total`.",
               "Зарплата: присвой `card` значение `card` плюс `salary`. Выведи `Card:` и `card`.",
               "Перевод: уменьши `card` на `save` и увеличь `savings` на `save`. Выведи `Card:`, `card`, `Savings:`, "
               "`savings` одним `print`.",
               "Квартплата: уменьши `card` на `rent`. Выведи `After rent:` и `card`.",
               "Пересчитай `total` по той же формуле и выведи `After:` и `total`."],
        hint="При переводе деньги уходят с одного счёта и приходят на другой: нужны два присваивания, "
             "`card = card - save` и `savings = savings + save`. `total`, посчитанный в начале, сам не обновится — "
             "в конце его нужно посчитать заново из текущих `card` и `savings`.",
        solution='total = card + savings\nprint("Before:", total)\ncard = card + salary\nprint("Card:", card)\n'
                 'card = card - save\nsavings = savings + save\nprint("Card:", card, "Savings:", savings)\n'
                 'card = card - rent\nprint("After rent:", card)\ntotal = card + savings\nprint("After:", total)',
        wrong=[("при переводе пополняет накопления, но не списывает деньги с карты",
                'total = card + savings\nprint("Before:", total)\ncard = card + salary\nprint("Card:", card)\n'
                'savings = savings + save\nprint("Card:", card, "Savings:", savings)\n'
                'card = card - rent\nprint("After rent:", card)\ntotal = card + savings\nprint("After:", total)'),
               ("не пересчитывает total в конце",
                'total = card + savings\nprint("Before:", total)\ncard = card + salary\nprint("Card:", card)\n'
                'card = card - save\nsavings = savings + save\nprint("Card:", card, "Savings:", savings)\n'
                'card = card - rent\nprint("After rent:", card)\nprint("After:", total)'),
               ("платит за квартиру из суммы до перевода",
                'total = card + savings\nprint("Before:", total)\ncard = card + salary\nprint("Card:", card)\n'
                'after = card - rent\ncard = card - save\nsavings = savings + save\nprint("Card:", card, "Savings:", savings)\n'
                'card = after\nprint("After rent:", card)\ntotal = card + savings\nprint("After:", total)')],
    ),
]
