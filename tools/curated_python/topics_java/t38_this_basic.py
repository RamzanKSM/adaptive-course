"""THIS_BASIC — «Ключевое слово this» (Java). Taught before: everything up to static methods of Solution, classes,
creating objects, constructors. Here: a parameter named like a field hides the field, and `this.field` reaches the
field of the current object — in a constructor and in methods that change the object; `this` is the object the
method was called on, as opposed to another object passed in as a parameter. Not yet: private, static fields."""
from java_tasks import JavaOutputTask

SKILL = "THIS_BASIC"


def find_class(name: str) -> str:
    return (f'Class<?> c = cls("{name}");\n'
            f'need(c != null, "Создай класс {name} ниже класса Solution (после его закрывающей скобки) и без слова public");\n')


def need_field(cls: str, name: str, java_type: str, why: str) -> str:
    """An instance (non-static) field of the class with this name and type."""
    return (f'{{ Field f = null; try {{ f = c.getDeclaredField("{name}"); }} catch (NoSuchFieldException e) {{ }}\n'
            f'  need(f != null && f.getType() == {java_type}.class, "Объяви в классе {cls} поле {java_type} {name} — {why}");\n'
            f'  need(!Modifier.isStatic(f.getModifiers()), "Объяви поле {name} в классе {cls} без слова static — тогда у каждого объекта будет своё значение"); }}\n')


def _types(cls: str, params: list[str]) -> str:
    return ", ".join("c" if p.split()[0] == cls else f"{p.split()[0]}.class" for p in params)


def need_constructor(cls: str, params: list[str], why: str) -> str:
    return (f'{{ Constructor<?> k = null; try {{ k = c.getDeclaredConstructor({_types(cls, params)}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(k != null, "Добавь в класс {cls} конструктор {cls}({", ".join(params)}) — {why}"); }}\n')


def need_method(cls: str, returns: str, name: str, params: list[str], why: str) -> str:
    """A non-static method with these parameter types and return type."""
    types = _types(cls, params)
    return (f'{{ Method m = null; try {{ m = c.getDeclaredMethod("{name}"{", " + types if types else ""}); }} catch (NoSuchMethodException e) {{ }}\n'
            f'  need(m != null && m.getReturnType() == {returns}.class, "Добавь в класс {cls} метод {returns} {name}({", ".join(params)}) — {why}");\n'
            f'  need(!Modifier.isStatic(m.getModifiers()), "Метод {name} в классе {cls} пиши без слова static — он работает с полями своего объекта"); }}\n')


def need_built(cls: str, params: list[str], args: str, expect: dict[str, str], message: str) -> str:
    """Creates an object with this constructor and compares its fields with the expected values (Java source)."""
    code = (f'{{ Constructor<?> k = c.getDeclaredConstructor({_types(cls, params)}); k.setAccessible(true);\n'
            f'  Object o = null; try {{ o = k.newInstance({args}); }} catch (Exception e) {{ }}\n')
    conditions = []
    for i, (name, value) in enumerate(expect.items()):
        code += f'  Field f{i} = c.getDeclaredField("{name}"); f{i}.setAccessible(true);\n'
        conditions.append(f"Objects.equals(f{i}.get(o), {value})")
    return code + f'  need(o != null && {" && ".join(conditions)}, "{message}"); }}\n'


# ───────── Game profile ─────────

PROFILE = '''class Profile {
    String nickname;
    int level;

    Profile(String nickname, int level) {
        this.nickname = nickname;
        this.level = level;
    }

    String rank() {
        if (this.level >= 10) {
            return "expert";
        }
        return "beginner";
    }
}'''

PROFILE_MAIN = '''Profile profile = new Profile(nickname, level);
System.out.println("Player: " + profile.nickname);
System.out.println("Level: " + profile.level);
System.out.println("Rank: " + profile.rank());'''

# ───────── Player: points and a new nickname ─────────

PLAYER = '''class Player {
    String nickname;
    int points;

    Player(String nickname) {
        this.nickname = nickname;
    }

    void addPoints(int points) {
        this.points += points;
    }

    void rename(String nickname) {
        this.nickname = nickname;
    }
}'''

PLAYER_MAIN = '''Player player = new Player(nickname);
for (int i = 0; i < rounds.length; i++) {
    player.addPoints(rounds[i]);
}
System.out.println(player.nickname + ", points: " + player.points);
player.rename(newNickname);
System.out.println(player.nickname + ", points: " + player.points);'''

PLAYER_BEHAVIOUR = '''{ Constructor<?> k = c.getDeclaredConstructor(String.class); k.setAccessible(true);
  Object o = null; try { o = k.newInstance("Test"); } catch (Exception e) { }
  Field fn = c.getDeclaredField("nickname"); fn.setAccessible(true);
  Field fp = c.getDeclaredField("points"); fp.setAccessible(true);
  need(o != null && Objects.equals(fn.get(o), "Test"), "Конструктор Player(String nickname) должен записать ник в поле объекта: this.nickname = nickname;");
  Method add = c.getDeclaredMethod("addPoints", int.class); add.setAccessible(true);
  try { add.invoke(o, 5); add.invoke(o, 7); } catch (Exception e) { }
  need(Objects.equals(fp.get(o), 12), "Метод addPoints(int points) должен прибавлять очки к полю игрока — к полю обращайся через this.points");
  Method ren = c.getDeclaredMethod("rename", String.class); ren.setAccessible(true);
  try { ren.invoke(o, "Nik"); } catch (Exception e) { }
  need(Objects.equals(fn.get(o), "Nik"), "Метод rename(String nickname) должен заменить ник игрока — к полю обращайся через this.nickname"); }
'''

# ───────── Wallets ─────────

WALLET = '''class Wallet {
    String owner;
    int money;

    Wallet(String owner, int money) {
        this.owner = owner;
        this.money = money;
    }

    boolean sendTo(Wallet other, int amount) {
        if (amount > this.money) {
            return false;
        }
        this.money -= amount;
        other.money += amount;
        return true;
    }
}'''

WALLET_MAIN = '''Wallet first = new Wallet(name1, money1);
Wallet second = new Wallet(name2, money2);
for (int i = 0; i < transfers.length; i++) {
    Wallet from;
    Wallet to;
    if (i % 2 == 0) {
        from = first;
        to = second;
    } else {
        from = second;
        to = first;
    }
    if (from.sendTo(to, transfers[i])) {
        System.out.println(from.owner + " -> " + to.owner + ": " + transfers[i] + " rub");
    } else {
        System.out.println(from.owner + " -> " + to.owner + ": declined");
    }
}
System.out.println(first.owner + ": " + first.money + " rub");
System.out.println(second.owner + ": " + second.money + " rub");'''

WALLET_BEHAVIOUR = '''{ Constructor<?> k = c.getDeclaredConstructor(String.class, int.class); k.setAccessible(true);
  Method send = c.getDeclaredMethod("sendTo", c, int.class); send.setAccessible(true);
  Object a = null, b = null, r = null;
  try { a = k.newInstance("A", 100); b = k.newInstance("B", 50); r = send.invoke(a, b, 30); } catch (Exception e) { }
  Field fm = c.getDeclaredField("money"); fm.setAccessible(true);
  need(r != null && Objects.equals(r, true) && Objects.equals(fm.get(a), 70) && Objects.equals(fm.get(b), 80), "Метод sendTo должен уменьшать деньги отправителя (this.money) и увеличивать деньги получателя (other.money)");
  Object r2 = null; try { r2 = send.invoke(a, b, 75); } catch (Exception e) { }
  need(Objects.equals(r2, false) && Objects.equals(fm.get(a), 70) && Objects.equals(fm.get(b), 80), "Метод sendTo должен проверять, хватает ли денег у отправителя — у this, а не у other, и при нехватке возвращать false"); }
'''

TASKS = [
    JavaOutputTask(
        skill=SKILL, difficulty=1, slug="java-this-game-profile", title="Профиль игрока",
        given=[("String", "nickname"), ("int", "level")],
        variants=[{"nickname": '"Neo"', "level": "7"}, {"nickname": '"Dragon"', "level": "15"}, {"nickname": '"Flash"', "level": "3"}],
        hidden=[{"nickname": '"Tiger"', "level": "10"}, {"nickname": '"Hedgehog"', "level": "9"},
                {"nickname": '"Pixel"', "level": "42"}, {"nickname": '"Owl"', "level": "1"}],
        intro="В онлайн-игре у каждого игрока есть профиль с ником и уровнем. С 10-го уровня игрок получает звание "
              "`expert`, а до этого он `beginner`. Ник записан в поле `nickname`, уровень — в поле `level`.",
        steps=["Ниже класса `Solution` создай класс `Profile` (без `public`) с полями `String nickname` и `int level`.",
               "Добавь конструктор, у которого параметры называются так же, как поля: `Profile(String nickname, int level)`. "
               "Чтобы записать параметр в поле с тем же именем, пиши `this.nickname = nickname;` — `this.nickname` значит "
               "«поле nickname этого объекта». Так же сохрани уровень.",
               "Добавь метод `String rank()`: он возвращает `expert`, если уровень 10 или больше, иначе — `beginner`.",
               "В `main` создай профиль `new Profile(nickname, level)` и выведи три строки вида `Player: Neo`, `Level: 7` "
               "и `Rank: beginner` — с полями профиля и результатом `rank()`."],
        hint="Внутри конструктора имя `level` без точки означает параметр: он закрывает собой поле с тем же именем. "
             "Запись `level = level;` просто присвоит параметр самому себе, а поле останется нулём. До поля объекта "
             "можно добраться только через `this.`.",
        solution=PROFILE_MAIN,
        classes=PROFILE,
        wrong=[("в конструкторе забыл this: `nickname = nickname;` — параметры присваиваются сами себе, поля остаются пустыми",
                PROFILE_MAIN, PROFILE.replace("this.nickname = nickname;", "nickname = nickname;").replace("this.level = level;", "level = level;")),
               ("this только у ника, а уровень присваивается сам себе — у всех уровень 0 и звание `beginner`",
                PROFILE_MAIN, PROFILE.replace("this.level = level;", "level = level;"))],
        constructs=["class"],
        checks=find_class("Profile")
               + need_field("Profile", "nickname", "String", "ник игрока")
               + need_field("Profile", "level", "int", "уровень игрока")
               + need_constructor("Profile", ["String nickname", "int level"], "он заполняет поля, когда создаётся объект")
               + need_built("Profile", ["String nickname", "int level"], '"Test", 12', {"nickname": '"Test"', "level": "12"},
                            "Конструктор Profile должен записать параметры в поля объекта: this.nickname = nickname; и this.level = level;")
               + need_method("Profile", "String", "rank", [], "он возвращает звание игрока"),
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=2, slug="java-this-player-rename", title="Очки и новый ник",
        given=[("String", "nickname"), ("int[]", "rounds"), ("String", "newNickname")],
        variants=[{"nickname": '"Neo"', "rounds": "{10, 25, 5}", "newNickname": '"Trinity"'},
                  {"nickname": '"Hedgehog"', "rounds": "{7, 7, 7, 7}", "newNickname": '"Super Hog"'},
                  {"nickname": '"Kat"', "rounds": "{50, 0, 30}", "newNickname": '"Katana"'}],
        hidden=[{"nickname": '"Bob"', "rounds": "{1}", "newNickname": '"Robert"'},
                {"nickname": '"Luna"', "rounds": "{}", "newNickname": '"Sun"'},
                {"nickname": '"Max"', "rounds": "{100, 200, 300, 400, 500}", "newNickname": '"MaxPower"'},
                {"nickname": '"Ri"', "rounds": "{3, 4}", "newNickname": '"Ri"'}],
        intro="В игре очки за раунды копятся в профиле игрока, а ник можно сменить в любой момент — очки при этом "
              "сохраняются. Ник игрока записан в поле `nickname`, очки за раунды по порядку — в массиве `rounds`, "
              "а новый ник — в поле `newNickname`.",
        steps=["Ниже класса `Solution` создай класс `Player` (без `public`) с полями `String nickname` и `int points` "
               "и конструктором `Player(String nickname)`, который сохраняет ник. Очков у нового игрока 0.",
               "Добавь метод `void addPoints(int points)`, который прибавляет `points` к очкам игрока, и метод "
               "`void rename(String nickname)`, который заменяет ник игрока. Параметры названы так же, как поля, "
               "поэтому к полям обращайся через `this`.",
               "В `main` создай игрока с ником из `nickname` и в цикле начисли ему методом `addPoints` очки за все раунды "
               "из `rounds`. Выведи строку вида `Neo, points: 40` — с полями игрока.",
               "Затем смени ник вызовом `rename(newNickname)` и выведи такую же строку ещё раз."],
        hint="В методе `addPoints(int points)` есть две разные вещи с именем `points`: параметр и поле объекта. "
             "Просто `points` — это параметр, а поле — `this.points`.",
        solution=PLAYER_MAIN,
        classes=PLAYER,
        wrong=[("в addPoints забыл this: `points += points;` меняет только параметр, а очки игрока остаются 0",
                PLAYER_MAIN, PLAYER.replace("this.points += points;", "points += points;")),
               ("в rename присваивает параметр самому себе — ник не меняется",
                PLAYER_MAIN, PLAYER.replace("    void rename(String nickname) {\n        this.nickname = nickname;",
                                            "    void rename(String nickname) {\n        nickname = nickname;"))],
        constructs=["class"],
        checks=find_class("Player")
               + need_field("Player", "nickname", "String", "ник игрока")
               + need_field("Player", "points", "int", "сколько очков набрал игрок")
               + need_constructor("Player", ["String nickname"], "он сохраняет ник, когда создаётся объект")
               + need_method("Player", "void", "addPoints", ["int points"], "он прибавляет очки игроку")
               + need_method("Player", "void", "rename", ["String nickname"], "он меняет ник игрока")
               + PLAYER_BEHAVIOUR,
    ),
    JavaOutputTask(
        skill=SKILL, difficulty=3, slug="java-this-wallet-transfers", title="Переводы между кошельками",
        given=[("String", "name1"), ("int", "money1"), ("String", "name2"), ("int", "money2"), ("int[]", "transfers")],
        variants=[{"name1": '"Anya"', "money1": "1000", "name2": '"Boris"', "money2": "500", "transfers": "{300, 900, 200}"},
                  {"name1": '"Misha"', "money1": "200", "name2": '"Katya"', "money2": "600", "transfers": "{250, 100, 150}"},
                  {"name1": '"Den"', "money1": "500", "name2": '"Liza"', "money2": "0", "transfers": "{500, 200, 100, 300}"}],
        hidden=[{"name1": '"Olya"', "money1": "100", "name2": '"Petya"', "money2": "100", "transfers": "{100, 300}"},
                {"name1": '"Roma"', "money1": "50", "name2": '"Sveta"', "money2": "80", "transfers": "{60}"},
                {"name1": '"Tim"', "money1": "1000", "name2": '"Ulya"', "money2": "1000", "transfers": "{}"},
                {"name1": '"Fil"', "money1": "300", "name2": '"Hana"', "money2": "0", "transfers": "{10, 20, 30, 40, 50}"}],
        intro="Два друга по очереди переводят друг другу деньги через приложение-кошелёк: первый перевод делает первый друг, "
              "второй — второй, третий — снова первый, и так далее. Если у отправителя не хватает денег, перевод не проходит. "
              "Имена и начальные суммы — в полях `name1`, `money1`, `name2` и `money2`, суммы переводов по порядку — в массиве `transfers`.",
        steps=["Ниже класса `Solution` создай класс `Wallet` (без `public`) с полями `String owner` и `int money` "
               "и конструктором `Wallet(String owner, int money)`, который записывает параметры в поля через `this`.",
               "Добавь метод `boolean sendTo(Wallet other, int amount)`. Кошелёк, у которого вызвали метод, — это `this`, "
               "получатель — `other`. Если у `this` денег не меньше, чем `amount`, метод уменьшает `this.money`, "
               "увеличивает `other.money` и возвращает `true`; иначе ничего не меняет и возвращает `false`.",
               "В `main` создай кошельки `first` (из `name1` и `money1`) и `second` (из `name2` и `money2`). Пройди по массиву "
               "`transfers`: переводы с чётным индексом (0, 2, 4…) делает `first` для `second`, с нечётным — `second` для `first`.",
               "Для каждого перевода выведи строку вида `Anya -> Boris: 300 rub`, а если он не прошёл — `Anya -> Boris: declined`. "
               "В конце выведи две строки вида `Anya: 500 rub` — сколько денег осталось у первого и у второго."],
        hint="Внутри `sendTo` два кошелька: `this` — тот, у которого вызвали метод (в `first.sendTo(second, 300)` это `first`), "
             "и `other` — тот, что передан в скобках. Хватает ли денег, проверяй у отправителя, то есть у `this`.",
        solution=WALLET_MAIN,
        classes=WALLET,
        wrong=[("проверяет деньги получателя (`other.money`) вместо отправителя",
                WALLET_MAIN, WALLET.replace("amount > this.money", "amount > other.money")),
               ("перепутал this и other: деньги прибавляются отправителю и списываются у получателя",
                WALLET_MAIN, WALLET.replace("this.money -= amount;\n        other.money += amount;",
                                            "this.money += amount;\n        other.money -= amount;"))],
        constructs=["class"],
        checks=find_class("Wallet")
               + need_field("Wallet", "owner", "String", "владелец кошелька")
               + need_field("Wallet", "money", "int", "сколько денег в кошельке")
               + need_constructor("Wallet", ["String owner", "int money"], "он заполняет поля, когда создаётся объект")
               + need_built("Wallet", ["String owner", "int money"], '"Test", 70', {"owner": '"Test"', "money": "70"},
                            "Конструктор Wallet должен записать параметры в поля объекта: this.owner = owner; и this.money = money;")
               + need_method("Wallet", "boolean", "sendTo", ["Wallet other", "int amount"], "он переводит деньги из этого кошелька в кошелёк other")
               + WALLET_BEHAVIOUR,
    ),
]
