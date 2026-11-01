"""Builds the tasks of «Эстафета» (CodeRelay): one task, the whole group, one writer at a time; every turn is one small
step that a student who follows the code does in ~10 seconds.

A task is written as its final program, each line tagged with the step that adds it («0» — the starter code). A closing
brace carries the step that opened its block: the editor closes brackets itself, so the brace is there from that step on.
A step's check is a list of alternative regular expressions over the normalized code (CodeRelay.normalize):
- Java: the whole program as one string, whitespace dropped except a single space between two word characters, string
  literals kept as they are, // comments dropped;
- Python: one line per non-empty line, the indentation level as that many «>», the line itself normalized as for Java.
A step counts when its check and the checks of all the steps before it match. CodeRelayTest replays every step's
snapshot against the checks; this script also runs the final program locally (java / python3) and compares its output.

Usage: python3 tools/relay/build_relay_tasks.py   →   backend/src/main/resources/relay-tasks/tasks.json
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "backend/src/main/resources/relay-tasks/tasks.json"

INC = r"(?:{v}\+\+|\+\+{v}|{v}\+=1|{v}=(?:{v}\+1|1\+{v}))"


def inc(v: str) -> str:
    return INC.format(v=v)


def add(target: str, value: str) -> str:
    return rf"(?:{target}\+={value}|{target}={target}\+{value}|{target}={value}\+{target})"


def py_print(label: str, var: str) -> str:
    """print("Label:", v), print("Label: " + str(v)), print(f"Label: {v}")."""
    l = re.escape(label)
    return rf'print\((?:"{l}",{var}|"{l} "\+str\({var}\)|f"{l} \{{{var}\}}")\)'


def java_print_concat(label: str, var: str) -> str:
    return rf'System\.out\.println\("{re.escape(label)} "\+{var}\);'


TASKS = [
    {
        "key": "java-evens", "language": "JAVA", "title": "Чётные и нечётные",
        "statement": "Посчитай, сколько чётных чисел от 1 до `n`, и сумму нечётных. Для `n = 10` программа выводит `Even: 5` и `Odd sum: 25`.",
        "expected": "Even: 5\nOdd sum: 25\n",
        "program": """
0|public class Solution {
0|    public static void main(String[] args) {
0|        int n = 10;
1|        int evens = 0;
2|        int oddSum = 0;
3|        for (int i = 1; i <= n; i++) {
4|            if (i % 2 == 0) {
5|                evens++;
4|            }
6|            else {
7|                oddSum += i;
6|            }
3|        }
8|        System.out.println("Even: " + evens);
9|        System.out.println("Odd sum: " + oddSum);
0|    }
0|}
""",
        "steps": [
            ("Заведи счётчик чётных чисел `evens`, сначала он равен 0.", [r"int evens=0;"]),
            ("Заведи сумму нечётных чисел `oddSum`, сначала она равна 0.", [r"int oddSum=0;"]),
            ("Начни цикл: `i` от 1 до `n` включительно.", [rf"for\(int i=1;(?:i<=n|i<n\+1);{inc('i')}\)\{{"]),
            ("В цикле проверь, чётное ли `i`.", [r"\)\{if\(i%2==0\)\{"]),
            ("Если `i` чётное, увеличь `evens` на 1.", [rf"if\(i%2==0\)\{{{inc('evens')};"]),
            ("Добавь ветку «иначе».", [rf"{inc('evens')};\}}else\{{"]),
            ("Иначе прибавь `i` к `oddSum`.", [rf"else\{{{add('oddSum', 'i')};"]),
            ("После цикла выведи `Even: ` и значение `evens`.", [r"\}\}" + java_print_concat("Even:", "evens")]),
            ("Следом выведи `Odd sum: ` и значение `oddSum`.", [java_print_concat("Even:", "evens") + java_print_concat("Odd sum:", "oddSum")]),
        ],
    },
    {
        "key": "java-max", "language": "JAVA", "title": "Самое большое число",
        "statement": "Найди в массиве `nums` самое большое число и его индекс. Программа выводит `Max: 23` и `Index: 3`.",
        "expected": "Max: 23\nIndex: 3\n",
        "program": """
0|public class Solution {
0|    public static void main(String[] args) {
0|        int[] nums = {4, 17, 9, 23, 8, 15};
1|        int max = nums[0];
2|        int index = 0;
3|        for (int i = 1; i < nums.length; i++) {
4|            if (nums[i] > max) {
5|                max = nums[i];
6|                index = i;
4|            }
3|        }
7|        System.out.println("Max: " + max);
8|        System.out.println("Index: " + index);
0|    }
0|}
""",
        "steps": [
            ("Заведи `max`: пока самое большое — первый элемент массива.", [r"int max=nums\[0\];"]),
            ("Заведи `index` — где стоит `max`, сначала 0.", [r"int index=0;"]),
            ("Начни цикл по индексам массива `i`, со второго элемента до конца.", [rf"for\(int i=[01];i<nums\.length;{inc('i')}\)\{{"]),
            ("В цикле проверь, больше ли текущий элемент, чем `max`.", [r"\)\{if\((?:nums\[i\]>max|max<nums\[i\])\)\{"]),
            ("Если больше — запомни его в `max`.", [r"if\((?:nums\[i\]>max|max<nums\[i\])\)\{max=nums\[i\];"]),
            ("И запомни его индекс в `index`.", [r"max=nums\[i\];index=i;"]),
            ("После цикла выведи `Max: ` и значение `max`.", [r"\}\}" + java_print_concat("Max:", "max")]),
            ("Следом выведи `Index: ` и значение `index`.", [java_print_concat("Max:", "max") + java_print_concat("Index:", "index")]),
        ],
    },
    {
        "key": "java-fizzbuzz", "language": "JAVA", "title": "FizzBuzz до 15",
        "statement": "Выведи числа от 1 до 15, но вместо кратных 3 — `Fizz`, вместо кратных 5 — `Buzz`, а вместо кратных и 3, и 5 — `FizzBuzz`.",
        "expected": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n",
        "program": """
0|public class Solution {
0|    public static void main(String[] args) {
1|        for (int i = 1; i <= 15; i++) {
2|            if (i % 15 == 0) {
3|                System.out.println("FizzBuzz");
2|            }
4|            else if (i % 3 == 0) {
5|                System.out.println("Fizz");
4|            }
6|            else if (i % 5 == 0) {
7|                System.out.println("Buzz");
6|            }
8|            else {
9|                System.out.println(i);
8|            }
1|        }
0|    }
0|}
""",
        "steps": [
            ("Начни цикл: `i` от 1 до 15 включительно.", [rf"for\(int i=1;(?:i<=15|i<16);{inc('i')}\)\{{"]),
            ("В цикле проверь, делится ли `i` и на 3, и на 5.", [r"\)\{if\((?:i%15==0|i%3==0&&i%5==0|i%5==0&&i%3==0)\)\{"]),
            ("Если да — выведи `FizzBuzz`.", [r"if\((?:i%15==0|i%3==0&&i%5==0|i%5==0&&i%3==0)\)\{System\.out\.println\(\"FizzBuzz\"\);"]),
            ("Иначе, если `i` делится на 3…", [r"println\(\"FizzBuzz\"\);\}else if\(i%3==0\)\{"]),
            ("…выведи `Fizz`.", [r"else if\(i%3==0\)\{System\.out\.println\(\"Fizz\"\);"]),
            ("Иначе, если `i` делится на 5…", [r"println\(\"Fizz\"\);\}else if\(i%5==0\)\{"]),
            ("…выведи `Buzz`.", [r"else if\(i%5==0\)\{System\.out\.println\(\"Buzz\"\);"]),
            ("Добавь последнюю ветку «иначе».", [r"println\(\"Buzz\"\);\}else\{"]),
            ("В ней выведи само число `i`.", [r"\}else\{System\.out\.println\(i\);"]),
        ],
    },
    {
        "key": "python-evens", "language": "PYTHON", "title": "Чётные и нечётные",
        "statement": "Посчитай, сколько чётных чисел от 1 до `n`, и сумму нечётных. Для `n = 10` программа выводит `Even: 5` и `Odd sum: 25`.",
        "expected": "Even: 5\nOdd sum: 25\n",
        "program": """
0|n = 10
1|evens = 0
2|odd_sum = 0
3|for i in range(1, n + 1):
4|    if i % 2 == 0:
5|        evens += 1
6|    else:
7|        odd_sum += i
8|print("Even:", evens)
9|print("Odd sum:", odd_sum)
""",
        "steps": [
            ("Заведи счётчик чётных чисел `evens`, сначала он равен 0.", [r"^evens=0$"]),
            ("Заведи сумму нечётных чисел `odd_sum`, сначала она равна 0.", [r"^odd_sum=0$"]),
            ("Начни цикл: `i` от 1 до `n` включительно.", [r"^for i in range\(1,(?:n\+1|1\+n)\):$"]),
            ("В цикле проверь, чётное ли `i`.", [r"^for i in range[^\n]*\n>if i%2==0:$"]),
            ("Если `i` чётное, увеличь `evens` на 1.", [r"^>if i%2==0:\n>>(?:evens\+=1|evens=evens\+1|evens=1\+evens)$"]),
            ("Добавь ветку «иначе».", [r"^>>(?:evens\+=1|evens=evens\+1|evens=1\+evens)\n>else:$"]),
            ("Иначе прибавь `i` к `odd_sum`.", [rf"^>else:\n>>{add('odd_sum', 'i')}$"]),
            ("После цикла выведи `Even:` и значение `evens`.", [rf"^>>{add('odd_sum', 'i')}\n{py_print('Even:', 'evens')}$"]),
            ("Следом выведи `Odd sum:` и значение `odd_sum`.", [rf"^{py_print('Even:', 'evens')}\n{py_print('Odd sum:', 'odd_sum')}$"]),
        ],
    },
    {
        "key": "python-max", "language": "PYTHON", "title": "Самое большое число",
        "statement": "Найди в списке `nums` самое большое число и его индекс (без `max()`). Программа выводит `Max: 23` и `Index: 3`.",
        "expected": "Max: 23\nIndex: 3\n",
        "program": """
0|nums = [4, 17, 9, 23, 8, 15]
1|max_value = nums[0]
2|index = 0
3|for i in range(1, len(nums)):
4|    if nums[i] > max_value:
5|        max_value = nums[i]
6|        index = i
7|print("Max:", max_value)
8|print("Index:", index)
""",
        "steps": [
            ("Заведи `max_value`: пока самое большое — первый элемент списка.", [r"^max_value=nums\[0\]$"]),
            ("Заведи `index` — где стоит `max_value`, сначала 0.", [r"^index=0$"]),
            ("Начни цикл по индексам списка `i`, со второго элемента до конца.", [r"^for i in range\((?:[01],)?len\(nums\)\):$"]),
            ("В цикле проверь, больше ли текущий элемент, чем `max_value`.", [r"^for i in range[^\n]*\n>if (?:nums\[i\]>max_value|max_value<nums\[i\]):$"]),
            ("Если больше — запомни его в `max_value`.", [r"^>if [^\n]*\n>>max_value=nums\[i\]$"]),
            ("И запомни его индекс в `index`.", [r"^>>max_value=nums\[i\]\n>>index=i$"]),
            ("После цикла выведи `Max:` и значение `max_value`.", [rf"^>>index=i\n{py_print('Max:', 'max_value')}$"]),
            ("Следом выведи `Index:` и значение `index`.", [rf"^{py_print('Max:', 'max_value')}\n{py_print('Index:', 'index')}$"]),
        ],
    },
    {
        "key": "python-fizzbuzz", "language": "PYTHON", "title": "FizzBuzz до 15",
        "statement": "Выведи числа от 1 до 15, но вместо кратных 3 — `Fizz`, вместо кратных 5 — `Buzz`, а вместо кратных и 3, и 5 — `FizzBuzz`.",
        "expected": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n",
        "program": """
1|for i in range(1, 16):
2|    if i % 15 == 0:
3|        print("FizzBuzz")
4|    elif i % 3 == 0:
5|        print("Fizz")
6|    elif i % 5 == 0:
7|        print("Buzz")
8|    else:
9|        print(i)
""",
        "steps": [
            ("Начни цикл: `i` от 1 до 15 включительно.", [r"^for i in range\(1,16\):$"]),
            ("В цикле проверь, делится ли `i` и на 3, и на 5.", [r"^for i in range[^\n]*\n>if (?:i%15==0|i%3==0 and i%5==0|i%5==0 and i%3==0):$"]),
            ("Если да — выведи `FizzBuzz`.", [r"^>if [^\n]*:\n>>print\(\"FizzBuzz\"\)$"]),
            ("Иначе, если `i` делится на 3…", [r"^>>print\(\"FizzBuzz\"\)\n>elif i%3==0:$"]),
            ("…выведи `Fizz`.", [r"^>elif i%3==0:\n>>print\(\"Fizz\"\)$"]),
            ("Иначе, если `i` делится на 5…", [r"^>>print\(\"Fizz\"\)\n>elif i%5==0:$"]),
            ("…выведи `Buzz`.", [r"^>elif i%5==0:\n>>print\(\"Buzz\"\)$"]),
            ("Добавь последнюю ветку «иначе».", [r"^>>print\(\"Buzz\"\)\n>else:$"]),
            ("В ней выведи само число `i`.", [r"^>else:\n>>print\(i\)$"]),
        ],
    },
]


def parse(program: str) -> list[tuple[int, str]]:
    lines = []
    for raw in program.strip("\n").split("\n"):
        tag, text = raw.split("|", 1)
        lines.append((int(tag), text))
    return lines


def snapshot(lines: list[tuple[int, str]], upto: int) -> str:
    return "".join(text + "\n" for tag, text in lines if tag <= upto)


def run(language: str, program: str) -> str | None:
    """The program's output when java / python3 is at hand, else None."""
    with tempfile.TemporaryDirectory() as tmp:
        if language == "PYTHON":
            path = Path(tmp, "main.py"); path.write_text(program)
            return subprocess.run([sys.executable, "-I", str(path)], capture_output=True, text=True, timeout=20).stdout
        java = Path(os.environ.get("JAVA_HOME", ""), "bin", "java") if os.environ.get("JAVA_HOME") else Path("java")
        path = Path(tmp, "Solution.java"); path.write_text(program)
        try:
            return subprocess.run([str(java), str(path)], capture_output=True, text=True, timeout=60).stdout
        except FileNotFoundError:
            return None


def build() -> list[dict]:
    out = []
    for t in TASKS:
        lines = parse(t["program"])
        steps = []
        for n, (prompt, checks) in enumerate(t["steps"], start=1):
            assert any(tag == n for tag, _ in lines), f"{t['key']}: step {n} adds no line"
            for c in checks: re.compile(c)
            hint = "\n".join(text.strip() for tag, text in lines if tag == n and text.strip() != "}")
            steps.append({"prompt": prompt, "check": checks, "hint": hint, "code": snapshot(lines, n)})
        assert max(tag for tag, _ in lines) == len(steps), f"{t['key']}: lines tagged past the last step"
        final = snapshot(lines, len(steps))
        output = run(t["language"], final)
        if output is None: print(f"  {t['key']}: no local runtime, output not checked")
        elif output != t["expected"]: raise SystemExit(f"{t['key']}: output {output!r} != expected {t['expected']!r}")
        out.append({"key": t["key"], "language": t["language"], "title": t["title"], "statement": t["statement"],
                    "starter": snapshot(lines, 0), "expectedOutput": t["expected"], "steps": steps})
        print(f"  {t['key']}: {len(steps)} steps" + ("" if output is None else ", output ok"))
    return out


if __name__ == "__main__":
    tasks = build()
    OUT.write_text(json.dumps({"tasks": tasks}, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(tasks)} tasks → {OUT.relative_to(ROOT)}")
