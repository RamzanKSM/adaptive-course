"""PY_FINALLY_BASIC — «Блок finally». Taught before: everything up to comprehensions, then try/except and separate
except blocks for different error types. Here: finally (runs always — after success, after an error, even after
return) and else (runs only when try had no error). Not yet: raise."""
from build import OutputTask

SKILL = "PY_FINALLY_BASIC"

# A try statement that has an else block: «else:» at the same indentation as an «except» line, right after its body.
TRY_ELSE = r"re:(?m)^([ \t]*)except\b[^\n]*\n(?:\1[ \t]+[^\n]*\n|[ \t]*\n)*\1else\s*:"

SHOP = """\
try:
    count = stock[product]
except KeyError:
    print(f"We do not sell {product}")
else:
    if wanted <= count:
        stock[product] = count - wanted
        print(f"Sold {wanted} {product}, {stock[product]} left")
    else:
        print(f"Only {count} {product} in stock")
finally:
    print("Next customer, please")
"""

ATM = """\
for text in requests:
    try:
        amount = int(text)
        if amount > cash:
            print(f"{amount}: not enough cash, ATM closes")
            break
        cash -= amount
        print(f"{amount}: take your money")
    except ValueError:
        print(f"{text}: wrong amount")
    finally:
        print("Card returned")
print(f"Cash left: {cash}")
"""

TASKS = [
    OutputTask(
        skill=SKILL, difficulty=1, slug="py-fin-rt-gym-locker", title="Шкафчик в раздевалке",
        given=["lockers", "name"],
        variants=[{"lockers": '{"Anya": 12, "Boris": 7, "Vera": 31}', "name": '"Boris"'},
                  {"lockers": '{"Anya": 12, "Boris": 7, "Vera": 31}', "name": '"Gleb"'},
                  {"lockers": '{"Anya": 12, "Boris": 7, "Vera": 31}', "name": '"Vera"'}],
        hidden=[{"name": '"Anya"'}, {"name": '"Dina"'}, {"lockers": '{"Egor": 1}', "name": '"Egor"'},
                {"lockers": '{}', "name": '"Zoya"'}],
        intro="В бассейне за каждым посетителем закреплён шкафчик: словарь `lockers` хранит имя и номер шкафчика. "
              "Охранник ищет шкафчик посетителя `name`. Если имени в словаре нет, `lockers[name]` вызывает `KeyError`. "
              "А пожелать хорошей тренировки охранник должен в любом случае.",
        steps=["В блоке `try` возьми номер шкафчика `lockers[name]` и выведи строку вида `Boris, your locker is 7`.",
               "Если возникла `KeyError`, выведи строку вида `Gleb, please register first` — с именем посетителя.",
               "В блоке `finally` выведи `Have a good swim!` — эта строка должна появляться всегда."],
        hint="`finally` пишется последним, после `except`, и выполняется и после удачи, и после ошибки. "
             "Если поставить пожелание в конец `try`, после ошибки до него дело не дойдёт.",
        solution='try:\n    print(f"{name}, your locker is {lockers[name]}")\nexcept KeyError:\n'
                 '    print(f"{name}, please register first")\nfinally:\n    print("Have a good swim!")',
        wrong=[("желает хорошей тренировки в конце try — после ошибки пожелания нет",
                'try:\n    print(f"{name}, your locker is {lockers[name]}")\n    print("Have a good swim!")\n'
                'except KeyError:\n    print(f"{name}, please register first")'),
               ("желает хорошей тренировки только в except — найденному посетителю пожелания нет",
                'try:\n    print(f"{name}, your locker is {lockers[name]}")\nexcept KeyError:\n'
                '    print(f"{name}, please register first")\n    print("Have a good swim!")')],
        constructs=["try"],
        must_use=[("re:finally\\s*:", "Пожелание выведи в блоке `finally:` — он выполняется в любом случае."),
                  ("re:except\\s+KeyError", "Неизвестного посетителя поймай блоком `except KeyError:`.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=2, slug="py-fin-rt-shop-counter", title="Прилавок с фруктами",
        given=["stock", "product", "wanted"],
        variants=[{"stock": '{"apples": 10, "pears": 4, "plums": 25}', "product": '"apples"', "wanted": "3"},
                  {"stock": '{"apples": 10, "pears": 4, "plums": 25}', "product": '"pears"', "wanted": "6"},
                  {"stock": '{"apples": 10, "pears": 4, "plums": 25}', "product": '"kiwi"', "wanted": "2"}],
        hidden=[{"product": '"pears"', "wanted": "4"}, {"product": '"plums"', "wanted": "26"},
                {"product": '"mango"', "wanted": "1"}, {"product": '"plums"', "wanted": "1"},
                {"product": '"Apples"', "wanted": "1"}],
        intro="Продавец на рынке отвечает покупателям. Сколько каких фруктов осталось, записано в словаре `stock`. "
              "Покупатель просит `wanted` штук фрукта `product`. Если такого фрукта на прилавке нет, `stock[product]` "
              "вызывает `KeyError`. После каждого покупателя продавец зовёт следующего.",
        steps=["В блоке `try` только возьми остаток фрукта: `stock[product]`.",
               "В блоке `except KeyError` выведи строку вида `We do not sell kiwi`.",
               "В блоке `else` (он выполняется, только если в `try` не было ошибки): если фруктов хватает, уменьши "
               "остаток в словаре и выведи строку вида `Sold 3 apples, 7 left`; иначе выведи строку вида "
               "`Only 4 pears in stock`.",
               "В блоке `finally` выведи `Next customer, please`."],
        hint="Порядок блоков: `try`, `except`, `else`, `finally`. В `try` оставляй только то, что может сломаться. "
             "Если покупатель просит ровно столько, сколько осталось, продать можно — останется 0.",
        solution=SHOP,
        wrong=[("не продаёт последние фрукты — запрос, равный остатку, отклоняется",
                SHOP.replace("    if wanted <= count:", "    if wanted < count:")),
               ("зовёт следующего в else, а не в finally — после неизвестного фрукта этой строки нет",
                SHOP.replace('        print(f"Only {count} {product} in stock")\nfinally:\n    print("Next customer, please")\n',
                             '        print(f"Only {count} {product} in stock")\n    print("Next customer, please")\n'))],
        constructs=["try", "if"],
        must_use=[(TRY_ELSE, "Добавь блок `else:` сразу после `except` — на том же уровне отступа. Туда переносят "
                             "действия, которые нужны только тогда, когда в `try` не было ошибки."),
                  ("re:finally\\s*:", "Приглашение следующего покупателя выведи в блоке `finally:` — "
                                      "он выполняется в любом случае.")],
    ),
    OutputTask(
        skill=SKILL, difficulty=3, slug="py-fin-rt-atm-requests", title="Банкомат",
        given=["cash", "requests"],
        variants=[{"cash": "5000", "requests": '["1000", "abc", "3000", "2000", "500"]'},
                  {"cash": "3000", "requests": '["500", "1000", "1500"]'},
                  {"cash": "1000", "requests": '["", "1500", "100"]'}],
        hidden=[{"cash": "100", "requests": '["100"]'},
                {"cash": "100", "requests": '["101", "1"]'},
                {"cash": "2000", "requests": '["x", "y", "500"]'},
                {"cash": "700", "requests": '["300", "300", "200", "100"]'}],
        intro="В банкомате осталось `cash` рублей. Люди по очереди вводят сумму, которую хотят снять, — запросы строками "
              "лежат в списке `requests`. Иногда вводят не число. Если денег на запрос не хватает, банкомат закрывается "
              "и следующих в очереди уже не обслуживает. Карту банкомат возвращает всегда — даже тому, на ком он закрылся.",
        steps=["Пройди по `requests`. Для каждого запроса в блоке `try` преврати его в целое число.",
               "Если сумма больше, чем осталось в банкомате, выведи строку вида `3000: not enough cash, ATM closes` "
               "и прерви цикл командой `break`. Иначе уменьши `cash` на эту сумму и выведи строку вида "
               "`1000: take your money`.",
               "Если запрос не число, перехвати `ValueError` и выведи строку вида `abc: wrong amount`.",
               "В блоке `finally` выведи `Card returned` — после каждого запроса, в том числе того, на котором "
               "цикл прервался.",
               "После цикла выведи строку вида `Cash left: 1000`."],
        hint="`finally` выполняется, даже когда из `try` выходят через `break`: сначала сработает `finally`, и только "
             "потом цикл закончится. Снять ровно столько, сколько осталось, можно.",
        solution=ATM,
        wrong=[("возвращает карту после try, а не в finally — на запросе с break карта не возвращается",
                ATM.replace('        print(f"{text}: wrong amount")\n    finally:\n        print("Card returned")\n',
                            '        print(f"{text}: wrong amount")\n    print("Card returned")\n')),
               ("закрывается, даже когда денег ровно на запрос",
                ATM.replace("        if amount > cash:", "        if amount >= cash:")),
               ("возвращает карту в конце try — после неверной суммы карта не возвращается",
                ATM.replace('        print(f"{amount}: take your money")\n    except ValueError:\n'
                            '        print(f"{text}: wrong amount")\n    finally:\n        print("Card returned")\n',
                            '        print(f"{amount}: take your money")\n        print("Card returned")\n'
                            '    except ValueError:\n        print(f"{text}: wrong amount")\n'))],
        constructs=["try", "for"],
        must_use=[("re:finally\\s*:", "Возврат карты выведи в блоке `finally:` — он выполняется даже при выходе "
                                      "из цикла через `break`."),
                  ("re:except\\s+ValueError", "Неверную сумму поймай блоком `except ValueError:`."),
                  ("re:\\bbreak\\b", "Когда денег не хватает, прерви цикл командой `break`.")],
    ),
]
