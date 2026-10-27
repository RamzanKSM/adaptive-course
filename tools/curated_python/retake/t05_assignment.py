"""PY_ASSIGNMENT — «Присваивание». Taught before: print (several values, sep=, end=), creating variables.
Here: giving a variable a new value (the old one is lost), copying one variable into another, the direction of «=»
(the left side gets the value), the order of assignments, swapping through a temporary variable.
Not yet: arithmetic, += -=, string concatenation, f-strings, conditions, loops."""
from build import OutputTask

SKILL = "PY_ASSIGNMENT"

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-asg-rt-order-status", title="Статус заказа",
        given=["order", "courier"],
        variants=[{"order": "1042", "courier": '"Timur"'}, {"order": "77", "courier": '"Galina"'},
                  {"order": "5310", "courier": '"Fedor"'}],
        hidden=[{"order": "1", "courier": '"Lyuba"'}, {"order": "908", "courier": '"Stas"'},
                {"order": "2600", "courier": '"Nail"'}],
        intro="Служба доставки сообщает, что происходит с заказом. Номер заказа и курьер уже есть в заготовке: "
              "`order = {order}` и `courier = {courier}`. Статус заказа хранится в одной переменной и меняется по ходу доставки.",
        steps=["Создай переменную `status` со строкой `\"accepted\"` и выведи `Order`, номер заказа и `status` одним `print`. "
               "Например: `Order 15 accepted`.",
               "Присвой `status` строку `\"on the way\"` и выведи такую же строку.",
               "Присвой `status` строку `\"delivered\"` и снова выведи такую же строку.",
               "Последней строкой выведи `Courier:` и курьера."],
        hint="Новое присваивание `status = \"on the way\"` затирает старое значение: после него в `status` уже нет "
             "`accepted`. Поэтому печатать нужно сразу после каждого присваивания, а не в конце.",
        solution='status = "accepted"\nprint("Order", order, status)\nstatus = "on the way"\nprint("Order", order, status)\n'
                 'status = "delivered"\nprint("Order", order, status)\nprint("Courier:", courier)',
        wrong=[("меняет статус уже после второй печати — дважды печатает accepted",
                'status = "accepted"\nprint("Order", order, status)\nprint("Order", order, status)\n'
                'status = "on the way"\nstatus = "delivered"\nprint("Order", order, status)\nprint("Courier:", courier)'),
               ("печатает слово order вместо номера заказа",
                'status = "accepted"\nprint("Order", "order", status)\nstatus = "on the way"\nprint("Order", "order", status)\n'
                'status = "delivered"\nprint("Order", "order", status)\nprint("Courier:", courier)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-asg-rt-profile-photo", title="Аватарка и обложка",
        given=["photo1", "photo2"],
        variants=[{"photo1": '"cat.jpg"', "photo2": '"sea.png"'}, {"photo1": '"me_2024.jpg"', "photo2": '"me_2026.jpg"'},
                  {"photo1": '"logo.png"', "photo2": '"mountains.jpg"'}],
        hidden=[{"photo1": '"dog.png"', "photo2": '"forest.jpg"'}, {"photo1": '"a.jpg"', "photo2": '"b.jpg"'},
                {"photo1": '"guitar.png"', "photo2": '"sunset.png"'}],
        intro="В соцсети у профиля есть аватарка и обложка. Пользователь поставил на аватарку `photo1 = {photo1}`, "
              "потом скопировал её на обложку, а затем сменил аватарку на `photo2 = {photo2}`. "
              "Обложка при этом не меняется: копия живёт своей жизнью.",
        steps=["Создай переменную `avatar` и положи в неё значение `photo1`.",
               "Создай переменную `cover` и скопируй в неё `avatar`.",
               "Выведи `Avatar:` и `avatar`, затем `Cover:` и `cover`.",
               "Присвой `avatar` значение `photo2`.",
               "Снова выведи `Avatar:` и `avatar`, затем `Cover:` и `cover`."],
        hint="`cover = avatar` копирует значение, которое лежит в `avatar` в этот момент. Когда потом `avatar` получает "
             "новое значение, `cover` об этом не знает и хранит старое. Следи за направлением: слева — кто получает значение.",
        solution='avatar = photo1\ncover = avatar\nprint("Avatar:", avatar)\nprint("Cover:", cover)\n'
                 'avatar = photo2\nprint("Avatar:", avatar)\nprint("Cover:", cover)',
        wrong=[("думает, что обложка меняется вслед за аватаркой, и копирует её ещё раз",
                'avatar = photo1\ncover = avatar\nprint("Avatar:", avatar)\nprint("Cover:", cover)\n'
                'avatar = photo2\ncover = avatar\nprint("Avatar:", avatar)\nprint("Cover:", cover)'),
               ("путает направление присваивания: меняет photo2 вместо аватарки",
                'avatar = photo1\ncover = avatar\nprint("Avatar:", avatar)\nprint("Cover:", cover)\n'
                'photo2 = avatar\nprint("Avatar:", avatar)\nprint("Cover:", cover)')],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-asg-rt-tv-remote", title="Кнопка «Назад» на пульте",
        given=["ch1", "ch2", "ch3"],
        variants=[{"ch1": '"News"', "ch2": '"Sport"', "ch3": '"Cartoons"'},
                  {"ch1": '"Music"', "ch2": '"Movies"', "ch3": '"Science"'},
                  {"ch1": '"Weather"', "ch2": '"Cooking"', "ch3": '"Travel"'}],
        hidden=[{"ch1": '"History"', "ch2": '"Nature"', "ch3": '"Games"'},
                {"ch1": '"Kids"', "ch2": '"Fashion"', "ch3": '"Cars"'},
                {"ch1": '"Ch 1"', "ch2": '"Ch 5"', "ch3": '"Ch 9"'}],
        intro="Телевизор помнит текущий канал и предыдущий: кнопка «Назад» на пульте возвращает на предыдущий канал, "
              "а текущий при этом становится предыдущим. Зритель включает `ch1 = {ch1}`, переключает на `ch2 = {ch2}`, "
              "потом на `ch3 = {ch3}` и жмёт «Назад».",
        steps=["Создай `current` со значением `ch1` и `previous` со строкой `\"none\"`. Выведи `Now:`, `current`, "
               "`Back:`, `previous` одним `print`. Например: `Now: Kids Back: none`.",
               "Переключение на `ch2`: присвой `previous` значение `current`, затем `current` — значение `ch2`. "
               "Выведи такую же строку.",
               "Переключение на `ch3`: обнови обе переменные точно так же (теперь `current` берёт `ch3`) и выведи такую же строку.",
               "Кнопка «Назад»: поменяй значения `current` и `previous` местами через временную переменную `temp` и выведи такую же строку."],
        hint="При переключении сначала текущий канал становится предыдущим (`previous = current`), и только потом в "
             "`current` кладётся новый. Для обмена: `temp = current`, `current = previous`, `previous = temp` — "
             "без `temp` одно из значений потеряется.",
        solution='current = ch1\nprevious = "none"\nprint("Now:", current, "Back:", previous)\n'
                 'previous = current\ncurrent = ch2\nprint("Now:", current, "Back:", previous)\n'
                 'previous = current\ncurrent = ch3\nprint("Now:", current, "Back:", previous)\n'
                 'temp = current\ncurrent = previous\nprevious = temp\nprint("Now:", current, "Back:", previous)',
        wrong=[("меняет местами без временной переменной",
                'current = ch1\nprevious = "none"\nprint("Now:", current, "Back:", previous)\n'
                'previous = current\ncurrent = ch2\nprint("Now:", current, "Back:", previous)\n'
                'previous = current\ncurrent = ch3\nprint("Now:", current, "Back:", previous)\n'
                'current = previous\nprevious = current\nprint("Now:", current, "Back:", previous)'),
               ("при втором переключении сначала берёт новый канал, а потом копирует его в предыдущий",
                'current = ch1\nprevious = "none"\nprint("Now:", current, "Back:", previous)\n'
                'previous = current\ncurrent = ch2\nprint("Now:", current, "Back:", previous)\n'
                'current = ch3\nprevious = current\nprint("Now:", current, "Back:", previous)\n'
                'temp = current\ncurrent = previous\nprevious = temp\nprint("Now:", current, "Back:", previous)'),
               ("путает направление присваивания при первом переключении",
                'current = ch1\nprevious = "none"\nprint("Now:", current, "Back:", previous)\n'
                'current = previous\ncurrent = ch2\nprint("Now:", current, "Back:", previous)\n'
                'previous = current\ncurrent = ch3\nprint("Now:", current, "Back:", previous)\n'
                'temp = current\ncurrent = previous\nprevious = temp\nprint("Now:", current, "Back:", previous)')],
    ),
]
