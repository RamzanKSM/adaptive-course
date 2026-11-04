"""PY_ASSIGNMENT — «Присваивание». Taught before: print (several values, sep=, end=), creating variables.
Here: giving a variable a new value (the old one is lost), copying one variable into another, the direction of «=»
(the left side gets the value), the order of assignments, swapping through a temporary variable.
Not yet: arithmetic, += -=, string concatenation, f-strings, conditions, loops."""
from build import OutputTask

SKILL = "PY_ASSIGNMENT"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-asg-race-leader", title="Лидер гонки",
        given=["first", "second"],
        variants=[{"first": '"Anya"', "second": '"Boris"'}, {"first": '"Lightning"', "second": '"Comet"'},
                  {"first": '"Team Red"', "second": '"Team Blue"'}],
        hidden=[{"first": '"Oleg"', "second": '"Dina"'}, {"first": '"Falcon"', "second": '"Eagle"'},
                {"first": '"Car 7"', "second": '"Car 12"'}],
        intro="Комментатор следит за гонкой. На старте впереди `first = {first}`, вторым идёт `second = {second}`. "
              "На последнем круге второй обгоняет первого.",
        steps=["Создай переменную `leader` и положи в неё значение `first`.",
               "Выведи `Leader:` и `leader`.",
               "Второй обогнал первого: присвой переменной `leader` значение `second`.",
               "Снова выведи `Leader:` и `leader`.",
               "Последней строкой выведи `Behind:` и `first`."],
        hint="Присваивание `leader = second` кладёт в переменную слева значение справа, старое значение `leader` "
             "при этом пропадает. Направление важно: `second = leader` изменило бы не лидера, а `second`.",
        solution='leader = first\nprint("Leader:", leader)\nleader = second\nprint("Leader:", leader)\nprint("Behind:", first)',
        wrong=[("путает направление присваивания: меняет second вместо leader",
                'leader = first\nprint("Leader:", leader)\nsecond = leader\nprint("Leader:", leader)\nprint("Behind:", first)'),
               ("меняет лидера уже после второй печати",
                'leader = first\nprint("Leader:", leader)\nprint("Leader:", leader)\nleader = second\nprint("Behind:", first)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-asg-new-nickname", title="Смена ника",
        given=["nick", "new_nick"],
        variants=[{"nick": '"cat_lover"', "new_nick": '"TigerKing"'}, {"nick": '"anya2010"', "new_nick": '"AnyaArt"'},
                  {"nick": '"noname"', "new_nick": '"Shadow"'}],
        hidden=[{"nick": '"boris_b"', "new_nick": '"BigBoss"'}, {"nick": '"player1"', "new_nick": '"Hero"'},
                {"nick": '"zzz"', "new_nick": '"Sleepy"'}],
        intro="В чате пользователь меняет ник. Текущий ник — `nick = {nick}`, новый — `new_nick = {new_nick}`. "
              "Чат должен сообщить и старый ник, и новый, поэтому старый нужно сохранить, пока он не пропал.",
        steps=["Создай переменную `old` и скопируй в неё `nick`.",
               "Присвой переменной `nick` значение `new_nick`.",
               "Выведи `Old nick:` и `old`.",
               "Выведи `New nick:` и `nick`."],
        hint="Порядок важен: если сначала присвоить `nick = new_nick`, старый ник пропадёт, и копировать будет уже нечего. "
             "Поэтому сначала `old = nick`, потом `nick = new_nick`.",
        solution='old = nick\nnick = new_nick\nprint("Old nick:", old)\nprint("New nick:", nick)',
        wrong=[("печатает в строке старого ника переменную nick, которая уже изменилась",
                'old = nick\nnick = new_nick\nprint("Old nick:", nick)\nprint("New nick:", nick)'),
               ("копирует старый ник уже после того, как он пропал",
                'nick = new_nick\nold = nick\nprint("Old nick:", old)\nprint("New nick:", nick)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-asg-swap-goalkeepers", title="Смена ворот",
        given=["left", "right"],
        variants=[{"left": '"Ivan"', "right": '"Petr"'}, {"left": '"Masha"', "right": '"Liza"'},
                  {"left": '"Rustam"', "right": '"Gleb"'}],
        hidden=[{"left": '"Ilya"', "right": '"Ann"'}, {"left": '"Kira"', "right": '"Nikita"'}, {"left": '"Sam"', "right": '"Tom"'}],
        intro="После первого тайма вратари меняются воротами. В левых воротах стоит `left = {left}`, в правых — `right = {right}`. "
              "Нужно поменять значения переменных местами.",
        steps=["Создай переменную `temp` и скопируй в неё `left`.",
               "Присвой `left` значение `right`.",
               "Присвой `right` значение из `temp`.",
               "Выведи `Left:` и `left`, затем `Right:` и `right`."],
        hint="Если сразу написать `left = right`, имя из левых ворот потеряется. Поэтому сначала спрячь его во временную "
             "переменную `temp`, а в конце переложи из `temp` в `right`.",
        solution='temp = left\nleft = right\nright = temp\nprint("Left:", left)\nprint("Right:", right)',
        wrong=[("берёт для правых ворот left, который уже изменился",
                'temp = left\nleft = right\nright = left\nprint("Left:", left)\nprint("Right:", right)'),
               ("меняет без временной переменной",
                'left = right\nright = left\nprint("Left:", left)\nprint("Right:", right)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-asg-checkout-queue", title="Очередь на кассе",
        given=["first", "second", "third"],
        variants=[{"first": '"Anna"', "second": '"Boris"', "third": '"Vika"'},
                  {"first": '"Oleg"', "second": '"Pasha"', "third": '"Rita"'},
                  {"first": '"Dima"', "second": '"Egor"', "third": '"Faina"'}],
        hidden=[{"first": '"Kim"', "second": '"Lev"', "third": '"Mila"'},
                {"first": '"Yan"', "second": '"Zoya"', "third": '"Artur"'},
                {"first": '"Sveta"', "second": '"Tanya"', "third": '"Uliana"'}],
        intro="У кассы стоят трое: первым `first = {first}`, вторым `second = {second}`, третьим `third = {third}`. "
              "Кассир обслуживает первого, и очередь сдвигается вперёд, а последнее место остаётся пустым.",
        steps=["Выведи `Served:` и `first`.",
               "Сдвинь очередь: присвой `first` значение `second`, затем `second` — значение `third`, "
               "затем `third` — строку `\"nobody\"`.",
               "Выведи три строки: `1:` и `first`, `2:` и `second`, `3:` и `third`."],
        hint="Сдвигать нужно спереди назад: сначала `first = second`, потом `second = third`. "
             "Если начать с `second = third`, то в `first` попадёт уже не тот человек.",
        solution='print("Served:", first)\nfirst = second\nsecond = third\nthird = "nobody"\nprint("1:", first)\n'
                 'print("2:", second)\nprint("3:", third)',
        wrong=[("путает направление присваивания: копирует second в third",
                'print("Served:", first)\nfirst = second\nthird = second\nthird = "nobody"\nprint("1:", first)\n'
                'print("2:", second)\nprint("3:", third)'),
               ("сдвигает в неправильном порядке",
                'print("Served:", first)\nsecond = third\nfirst = second\nthird = "nobody"\nprint("1:", first)\n'
                'print("2:", second)\nprint("3:", third)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-asg-duty-rotation", title="Дежурство по кругу",
        given=["cook", "washer", "cleaner"],
        variants=[{"cook": '"Anya"', "washer": '"Boris"', "cleaner": '"Vera"'},
                  {"cook": '"Mom"', "washer": '"Dad"', "cleaner": '"Kid"'},
                  {"cook": '"Lena"', "washer": '"Max"', "cleaner": '"Zarina"'}],
        hidden=[{"cook": '"Ira"', "washer": '"Kostya"', "cleaner": '"Lida"'},
                {"cook": '"Amir"', "washer": '"Bella"', "cleaner": '"Chris"'},
                {"cook": '"Ted"', "washer": '"Una"', "cleaner": '"Vlad"'}],
        intro="В походе трое дежурят по кругу. Сегодня готовит `cook = {cook}`, моет посуду `washer = {washer}`, "
              "убирает лагерь `cleaner = {cleaner}`. Завтра каждый переходит на следующую работу по кругу: "
              "кто мыл посуду — готовит, кто убирал — моет посуду, а кто готовил — убирает.",
        steps=["Выведи `Today cook:` и `cook`.",
               "Сохрани `cook` во временную переменную `temp`.",
               "Присвой `cook` значение `washer`, затем `washer` — значение `cleaner`, затем `cleaner` — значение из `temp`.",
               "Выведи три строки: `Tomorrow cook:` и `cook`, `Tomorrow washer:` и `washer`, `Tomorrow cleaner:` и `cleaner`."],
        hint="Это тот же обмен через временную переменную, только по кругу из трёх. Тот, чьё значение затирается первым "
             "(`cook`), должен сначала попасть в `temp`, а забрать его оттуда нужно в самом конце.",
        solution='print("Today cook:", cook)\ntemp = cook\ncook = washer\nwasher = cleaner\ncleaner = temp\n'
                 'print("Tomorrow cook:", cook)\nprint("Tomorrow washer:", washer)\nprint("Tomorrow cleaner:", cleaner)',
        wrong=[("берёт для уборки cook, который уже изменился, а не temp",
                'print("Today cook:", cook)\ntemp = cook\ncook = washer\nwasher = cleaner\ncleaner = cook\n'
                'print("Tomorrow cook:", cook)\nprint("Tomorrow washer:", washer)\nprint("Tomorrow cleaner:", cleaner)'),
               ("сдвигает по кругу в обратную сторону",
                'print("Today cook:", cook)\ntemp = cook\ncook = cleaner\ncleaner = washer\nwasher = temp\n'
                'print("Tomorrow cook:", cook)\nprint("Tomorrow washer:", washer)\nprint("Tomorrow cleaner:", cleaner)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-asg-yesterday-today", title="Вчера и сегодня",
        given=["mon", "tue", "wed"],
        variants=[{"mon": "12", "tue": "15", "wed": "9"}, {"mon": "-3", "tue": "-7", "wed": "0"},
                  {"mon": "21", "tue": "24", "wed": "26"}],
        hidden=[{"mon": "5", "tue": "6", "wed": "7"}, {"mon": "30", "tue": "18", "wed": "-2"},
                {"mon": "-10", "tue": "1", "wed": "14"}],
        intro="Метеостанция за три дня записала температуру: в понедельник `mon = {mon}`, во вторник `tue = {tue}`, "
              "в среду `wed = {wed}`. Каждый день табло показывает вчерашнюю и сегодняшнюю температуру. "
              "Программа хранит их в двух переменных — `before` и `now` — и каждый день обновляет обе.",
        steps=["Создай `before` со строкой `\"none\"` (в понедельник вчерашних данных нет) и `now` со значением `mon`.",
               "Выведи `Yesterday:`, `before`, `Today:`, `now` одним `print`. Например: `Yesterday: none Today: 4`.",
               "Наступил вторник: присвой `before` значение `now`, затем `now` — значение `tue`, и выведи такую же строку.",
               "Наступила среда: точно так же обнови `before` и `now` (теперь `now` берёт `wed`) и выведи такую же строку."],
        hint="Каждый день сначала сегодняшняя температура становится вчерашней (`before = now`), и только потом в `now` "
             "кладётся новая. Если поменять эти строки местами, `before` получит уже новое значение.",
        solution='before = "none"\nnow = mon\nprint("Yesterday:", before, "Today:", now)\n'
                 'before = now\nnow = tue\nprint("Yesterday:", before, "Today:", now)\n'
                 'before = now\nnow = wed\nprint("Yesterday:", before, "Today:", now)',
        wrong=[("путает направление присваивания во вторник",
                'before = "none"\nnow = mon\nprint("Yesterday:", before, "Today:", now)\n'
                'now = before\nnow = tue\nprint("Yesterday:", before, "Today:", now)\n'
                'before = now\nnow = wed\nprint("Yesterday:", before, "Today:", now)'),
               ("в среду сначала берёт новое значение, а потом копирует его во вчерашнее",
                'before = "none"\nnow = mon\nprint("Yesterday:", before, "Today:", now)\n'
                'before = now\nnow = tue\nprint("Yesterday:", before, "Today:", now)\n'
                'now = wed\nbefore = now\nprint("Yesterday:", before, "Today:", now)')],
    ),
]
