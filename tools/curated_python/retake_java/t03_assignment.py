"""ASSIGNMENT — «Присваивание» (Java). Taught before: System.out.println / print, declaring variables (`int`, `String`)
with an initial value. This topic: changing a variable with `=` after its declaration — a new value replaces the old one,
the value is copied from the right side into the variable on the left, a copy keeps the old value (save before
overwriting, swap through a temporary variable). Fields of the starter may be reassigned like variables.
Not yet: arithmetic (no `x = x + 1` — that needs topic 4), string operations (a line is assembled from several print
calls), conditions, loops."""
from java_tasks import JavaOutputTask

SKILL = "ASSIGNMENT"


def _code(*lines: str) -> str:
    return "\n".join(lines)


def _change(code: str, old: str, new: str, nth: int = 1) -> str:
    """The code with the nth line equal to `old` replaced by `new` (a one-line mistake)."""
    lines = code.split("\n")
    found = [i for i, line in enumerate(lines) if line == old]
    assert len(found) >= nth, f"no line {old!r}"
    lines[found[nth - 1]] = new
    return "\n".join(lines)


CHAT = _code(
    'String nick = oldNick;',
    'System.out.print(nick);',
    'System.out.println(" joined the chat");',
    'nick = newNick;',
    'System.out.print(oldNick);',
    'System.out.print(" is now ");',
    'System.out.println(nick);',
    'System.out.print(nick);',
    'System.out.println(" says hi");',
)

BROWSER = _code(
    'String current = page1;',
    'String back = current;',
    'current = page2;',
    'System.out.print("Page: ");',
    'System.out.print(current);',
    'System.out.print(" | Back: ");',
    'System.out.println(back);',
    'back = current;',
    'current = page3;',
    'System.out.print("Page: ");',
    'System.out.print(current);',
    'System.out.print(" | Back: ");',
    'System.out.println(back);',
)

PODIUM = _code(
    'String tempName = gold;',
    'gold = bronze;',
    'bronze = tempName;',
    'int tempBib = goldBib;',
    'goldBib = bronzeBib;',
    'bronzeBib = tempBib;',
    'System.out.print("1st: ");',
    'System.out.print(gold);',
    'System.out.print(" (bib ");',
    'System.out.print(goldBib);',
    'System.out.println(")");',
    'System.out.print("3rd: ");',
    'System.out.print(bronze);',
    'System.out.print(" (bib ");',
    'System.out.print(bronzeBib);',
    'System.out.println(")");',
)

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-asg-rt-chat-nick", title="Новый ник в чате",
        given=[("String", "oldNick"), ("String", "newNick")],
        variants=[{"oldNick": '"Anya"', "newNick": '"Rocket"'}, {"oldNick": '"Boris"', "newNick": '"Bear"'},
                  {"oldNick": '"Lena"', "newNick": '"Fox"'}],
        hidden=[{"oldNick": '"Oleg"', "newNick": '"Ghost"'}, {"oldNick": '"Kate"', "newNick": '"Kitty"'},
                {"oldNick": '"Rocket"', "newNick": '"Anya"'}],
        intro="Человек зашёл в чат под ником `oldNick`, а потом сменил его на `newNick`. Чат пишет об этом три сообщения.",
        steps=["Объяви переменную `String nick` и запиши в неё `oldNick`. Выведи строку: значение `nick` и ` joined the chat`.",
               "Присвой `nick` значение `newNick` (без нового объявления — `String` второй раз не пиши).",
               "Выведи строку: значение `oldNick`, ` is now ` и значение `nick`, например `Anya is now Rocket`.",
               "Выведи строку: значение `nick` и ` says hi`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть — через `System.out.println`."],
        hint="После `nick = newNick;` в `nick` лежит уже новый ник, а старый остался только в поле `oldNick`.",
        solution=CHAT,
        wrong=[("присваивание наоборот: записывает nick в поле newNick, а ник не меняется",
                _change(CHAT, 'nick = newNick;', 'newNick = nick;')),
               ("во второй строке печатает nick, который уже стал новым: «Rocket is now Rocket»",
                _change(CHAT, 'System.out.print(oldNick);', 'System.out.print(nick);'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-asg-rt-browser-back", title="Кнопка «Назад» в браузере",
        given=[("String", "page1"), ("String", "page2"), ("String", "page3")],
        variants=[{"page1": '"home"', "page2": '"news"', "page3": '"sport"'},
                  {"page1": '"search"', "page2": '"maps"', "page3": '"route"'},
                  {"page1": '"shop"', "page2": '"cart"', "page3": '"payment"'}],
        hidden=[{"page1": '"mail"', "page2": '"inbox"', "page3": '"letter"'},
                {"page1": '"wiki"', "page2": '"Java"', "page3": '"Python"'},
                {"page1": '"a"', "page2": '"b"', "page3": '"c"'}],
        intro="Браузер помнит открытую страницу и ту, на которую вернёт кнопка «Назад». Пользователь открыл подряд "
              "три страницы: `page1`, `page2` и `page3`.",
        steps=["Объяви `String current` со значением `page1` и `String back` со значением `current`.",
               "Открыта вторая страница: присвой `current` значение `page2`. Выведи строку `Page: `, значение `current`, "
               "` | Back: ` и значение `back`, например `Page: news | Back: home`.",
               "Открыта третья страница: сначала присвой `back` значение `current`, потом `current` — значение `page3`.",
               "Выведи такую же строку ещё раз, например `Page: sport | Back: news`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть — через `System.out.println`."],
        hint="Перед тем как перезаписать `current`, его старое значение надо успеть скопировать в `back` — иначе оно пропадёт.",
        solution=BROWSER,
        wrong=[("присваивания в обратном порядке: back получает уже новую страницу",
                _change(_change(BROWSER, 'back = current;', 'current = page3;'), 'current = page3;', 'back = current;', 2)),
               ("кнопка «Назад» всегда ведёт на первую страницу",
                _change(BROWSER, 'back = current;', 'back = page1;'))],
        constructs=["assignment"],
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-asg-rt-podium-fix", title="Ошибка в протоколе забега",
        given=[("String", "gold"), ("int", "goldBib"), ("String", "bronze"), ("int", "bronzeBib")],
        variants=[{"gold": '"Vika"', "goldBib": "12", "bronze": '"Anya"', "bronzeBib": "7"},
                  {"gold": '"Oleg"', "goldBib": "31", "bronze": '"Timur"', "bronzeBib": "104"},
                  {"gold": '"Kira"', "goldBib": "5", "bronze": '"Lev"', "bronzeBib": "58"}],
        hidden=[{"gold": '"Ann"', "goldBib": "1", "bronze": '"Ben"', "bronzeBib": "2"},
                {"gold": '"Masha"', "goldBib": "77", "bronze": '"Gleb"', "bronzeBib": "40"},
                {"gold": '"Rita"', "goldBib": "300", "bronze": '"Ilya"', "bronzeBib": "9"}],
        intro="Судья перепутал карточки первого и третьего места: в полях `gold` и `goldBib` оказались имя и номер "
              "бегуна, пришедшего третьим, а в `bronze` и `bronzeBib` — пришедшего первым. Нужно поменять их местами.",
        steps=["Поменяй местами имена: объяви `String tempName` со значением `gold`, присвой `gold` значение `bronze`, "
               "а `bronze` — значение `tempName`.",
               "Так же поменяй местами номера через переменную `int tempBib`.",
               "Выведи строку `1st: `, значение `gold`, ` (bib `, значение `goldBib` и `)` — например `1st: Anya (bib 7)`.",
               "Выведи такую же строку для третьего места: `3rd: `, `bronze`, ` (bib `, `bronzeBib` и `)`.",
               "Части одной строки выводи через `System.out.print`, последнюю часть — через `System.out.println`."],
        hint="Для обмена каждой пары нужна своя временная переменная нужного типа: имя — это `String`, номер — `int`.",
        solution=PODIUM,
        wrong=[("обмен имён без временной переменной: в bronze кладёт уже изменённый gold",
                _change(PODIUM, 'bronze = tempName;', 'bronze = gold;')),
               ("меняет местами только имена, номера остаются прежними",
                _change(_change(PODIUM, 'goldBib = bronzeBib;', '// numbers stay'), 'bronzeBib = tempBib;', '// as they were'))],
        constructs=["assignment"],
    ),
]
