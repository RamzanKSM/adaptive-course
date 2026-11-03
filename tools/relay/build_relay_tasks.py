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


def py_inc(v: str) -> str:
    return rf"(?:{v}\+=1|{v}={v}\+1|{v}=1\+{v})"


SCORE_AT = r"scores\[i\]"
SCORE_PASS = r"(?:scores\[i\]>=60|60<=scores\[i\]|scores\[i\]>59)"
SCORE_BEST = r"(?:scores\[i\]>best|best<scores\[i\])"
VOWEL_CHECK = r'"aeiou"\.indexOf\(c\)(?:>=0|>-1|!=-1)'
PRIME_CHECK = r"(?:prime|prime==true)"
PY_PASS = r"(?:score>=60|60<=score|score>59)"
PY_BEST = r"(?:score>best|best<score)"
PY_PRIME = r"(?:prime|prime==True)"
PY_FAILED = r"len\(scores\)-passed"

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
        "key": "java-scores", "language": "JAVA", "title": "Оценки группы",
        "statement": "В массиве `scores` — баллы группы, зачёт от 60. Программа выводит сумму баллов, сколько сдали и не сдали, лучший балл и средний: `Total: 545`, `Passed: 5`, `Failed: 3`, `Best: 100`, `Average: 68.125`.",
        "expected": "Total: 545\nPassed: 5\nFailed: 3\nBest: 100\nAverage: 68.125\n",
        "program": """
0|public class Solution {
0|    public static void main(String[] args) {
0|        int[] scores = {72, 45, 90, 58, 66, 100, 33, 81};
1|        int total = 0;
2|        int passed = 0;
3|        int best = scores[0];
4|        for (int i = 0; i < scores.length; i++) {
5|            total += scores[i];
6|            if (scores[i] >= 60) {
7|                passed++;
6|            }
8|            if (scores[i] > best) {
9|                best = scores[i];
8|            }
4|        }
10|        double average = (double) total / scores.length;
11|        System.out.println("Total: " + total);
12|        System.out.println("Passed: " + passed);
13|        System.out.println("Failed: " + (scores.length - passed));
14|        System.out.println("Best: " + best);
15|        System.out.println("Average: " + average);
0|    }
0|}
""",
        "steps": [
            ("Заведи сумму баллов `total`, сначала 0.", [r"int total=0;"]),
            ("Заведи счётчик сдавших `passed`, сначала 0.", [r"int passed=0;"]),
            ("Заведи `best`: пока лучший балл — первый элемент массива.", [r"int best=scores\[0\];"]),
            ("Начни цикл по индексам массива `i`, с нуля до конца.", [rf"for\(int i=0;i<scores\.length;{inc('i')}\)\{{"]),
            ("В цикле прибавь текущий балл к `total`.", [rf"\)\{{{add('total', SCORE_AT)};"]),
            ("Следом проверь, набран ли зачёт: балл не меньше 60.", [rf"{add('total', SCORE_AT)};if\({SCORE_PASS}\)\{{"]),
            ("Если да, увеличь `passed` на 1.", [rf"if\({SCORE_PASS}\)\{{{inc('passed')};"]),
            ("После этого `if` проверь, больше ли балл, чем `best`.", [rf"{inc('passed')};\}}if\({SCORE_BEST}\)\{{"]),
            ("Если больше, запомни его в `best`.", [rf"if\({SCORE_BEST}\)\{{best=scores\[i\];"]),
            ("После цикла посчитай дробное среднее: `double average`, сумма делить на длину массива. Не забудь `(double)`.",
             [r"\}\}double average=(?:\(double\)total/scores\.length|total/\(double\)scores\.length|total\*1\.0/scores\.length|1\.0\*total/scores\.length);"]),
            ("Выведи `Total: ` и значение `total`.", [r";" + java_print_concat("Total:", "total")]),
            ("Выведи `Passed: ` и значение `passed`.", [java_print_concat("Total:", "total") + java_print_concat("Passed:", "passed")]),
            ("Выведи `Failed: ` и число не сдавших: длина массива минус `passed`. Разность возьми в скобки.",
             [java_print_concat("Passed:", "passed") + r'System\.out\.println\("Failed: "\+\(scores\.length-passed\)\);']),
            ("Выведи `Best: ` и значение `best`.", [r'\(scores\.length-passed\)\);' + java_print_concat("Best:", "best")]),
            ("Выведи `Average: ` и значение `average`.", [java_print_concat("Best:", "best") + java_print_concat("Average:", "average")]),
        ],
    },
    {
        "key": "java-letters", "language": "JAVA", "title": "Гласные и согласные",
        "statement": "Разбери строку `text` по символам: сколько в ней гласных, согласных и слов. Слова разделены одним пробелом. Программа выводит `Vowels: 7`, `Consonants: 9`, `Words: 5`.",
        "expected": "Vowels: 7\nConsonants: 9\nWords: 5\n",
        "program": """
0|public class Solution {
0|    public static void main(String[] args) {
0|        String text = "java is fun to learn";
1|        int vowels = 0;
2|        int consonants = 0;
3|        int spaces = 0;
4|        for (int i = 0; i < text.length(); i++) {
5|            char c = text.charAt(i);
6|            if (c == ' ') {
7|                spaces++;
6|            }
8|            else if ("aeiou".indexOf(c) >= 0) {
9|                vowels++;
8|            }
10|            else {
11|                consonants++;
10|            }
4|        }
12|        int words = spaces + 1;
13|        System.out.println("Vowels: " + vowels);
14|        System.out.println("Consonants: " + consonants);
15|        System.out.println("Words: " + words);
0|    }
0|}
""",
        "steps": [
            ("Заведи счётчик гласных `vowels`, сначала 0.", [r"int vowels=0;"]),
            ("Заведи счётчик согласных `consonants`, сначала 0.", [r"int consonants=0;"]),
            ("Заведи счётчик пробелов `spaces`, сначала 0.", [r"int spaces=0;"]),
            ("Начни цикл по индексам строки `i`: с нуля, пока `i` меньше `text.length()`.", [rf"for\(int i=0;i<text\.length\(\);{inc('i')}\)\{{"]),
            ("В цикле достань текущий символ: `char c`, через `text.charAt(i)`.", [r"\)\{char c=text\.charAt\(i\);"]),
            ("Проверь, пробел ли `c`. Символ пиши в одинарных кавычках.", [r"charAt\(i\);if\(c==' '\)\{"]),
            ("Если пробел, увеличь `spaces` на 1.", [rf"if\(c==' '\)\{{{inc('spaces')};"]),
            ("Иначе, если `c` есть среди гласных: `\"aeiou\".indexOf(c) >= 0`…", [rf"{inc('spaces')};\}}else if\({VOWEL_CHECK}\)\{{"]),
            ("…увеличь `vowels` на 1.", [rf"else if\({VOWEL_CHECK}\)\{{{inc('vowels')};"]),
            ("Добавь последнюю ветку «иначе».", [rf"{inc('vowels')};\}}else\{{"]),
            ("В ней увеличь `consonants` на 1.", [rf"else\{{{inc('consonants')};"]),
            ("После цикла заведи `words`: слов на одно больше, чем пробелов.", [r"\}\}int words=(?:spaces\+1|1\+spaces);"]),
            ("Выведи `Vowels: ` и значение `vowels`.", [r"int words=[^;]*;" + java_print_concat("Vowels:", "vowels")]),
            ("Выведи `Consonants: ` и значение `consonants`.", [java_print_concat("Vowels:", "vowels") + java_print_concat("Consonants:", "consonants")]),
            ("Выведи `Words: ` и значение `words`.", [java_print_concat("Consonants:", "consonants") + java_print_concat("Words:", "words")]),
        ],
    },
    {
        "key": "java-primes", "language": "JAVA", "title": "Простые числа",
        "statement": "Выведи все простые числа от 2 до `limit`, а затем их количество и сумму. Число простое, если не делится ни на что, кроме 1 и себя. Для `limit = 30` в конце идут `Count: 10` и `Total: 129`.",
        "expected": "Primes:\n2\n3\n5\n7\n11\n13\n17\n19\n23\n29\nCount: 10\nTotal: 129\n",
        "program": """
0|public class Solution {
0|    public static void main(String[] args) {
0|        int limit = 30;
1|        int count = 0;
2|        int total = 0;
3|        System.out.println("Primes:");
4|        for (int n = 2; n <= limit; n++) {
5|            boolean prime = true;
6|            for (int d = 2; d < n; d++) {
7|                if (n % d == 0) {
8|                    prime = false;
9|                    break;
7|                }
6|            }
10|            if (prime) {
11|                count++;
12|                total += n;
13|                System.out.println(n);
10|            }
4|        }
14|        System.out.println("Count: " + count);
15|        System.out.println("Total: " + total);
0|    }
0|}
""",
        "steps": [
            ("Заведи счётчик простых чисел `count`, сначала 0.", [r"int count=0;"]),
            ("Заведи их сумму `total`, сначала 0.", [r"int total=0;"]),
            ("Выведи заголовок `Primes:`.", [r'int total=0;System\.out\.println\("Primes:"\);']),
            ("Начни цикл: `n` от 2 до `limit` включительно.", [rf'println\("Primes:"\);for\(int n=2;(?:n<=limit|n<limit\+1);{inc("n")}\)\{{']),
            ("В цикле заведи `boolean prime`: пока считаем `n` простым.", [r"\)\{boolean prime=true;"]),
            ("Начни вложенный цикл: делитель `d` от 2, пока `d` меньше `n`.", [rf"boolean prime=true;for\(int d=2;(?:d<n|d\*d<=n|d<=n/2);{inc('d')}\)\{{"]),
            ("Во вложенном цикле проверь, делится ли `n` на `d`.", [r"\)\{if\(n%d==0\)\{"]),
            ("Если делится, `n` не простое: запиши это в `prime`.", [r"if\(n%d==0\)\{prime=false;"]),
            ("И выйди из вложенного цикла.", [r"prime=false;break;"]),
            ("После вложенного цикла проверь, осталось ли `n` простым.", [rf"\}}\}}if\({PRIME_CHECK}\)\{{"]),
            ("Если да, увеличь `count` на 1.", [rf"if\({PRIME_CHECK}\)\{{{inc('count')};"]),
            ("Прибавь `n` к `total`.", [rf"{inc('count')};{add('total', 'n')};"]),
            ("Выведи само число `n`.", [rf"{add('total', 'n')};System\.out\.println\(n\);"]),
            ("После внешнего цикла выведи `Count: ` и значение `count`.", [r"\}\}" + java_print_concat("Count:", "count")]),
            ("Выведи `Total: ` и значение `total`.", [java_print_concat("Count:", "count") + java_print_concat("Total:", "total")]),
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
    {
        "key": "python-scores", "language": "PYTHON", "title": "Оценки группы",
        "statement": "В списке `scores` — баллы группы, зачёт от 60. Программа выводит сумму баллов, сколько сдали и не сдали, лучший балл и средний (без `sum()` и `max()`): `Total: 545`, `Passed: 5`, `Failed: 3`, `Best: 100`, `Average: 68.125`.",
        "expected": "Total: 545\nPassed: 5\nFailed: 3\nBest: 100\nAverage: 68.125\n",
        "program": """
0|scores = [72, 45, 90, 58, 66, 100, 33, 81]
1|total = 0
2|passed = 0
3|best = scores[0]
4|for score in scores:
5|    total += score
6|    if score >= 60:
7|        passed += 1
8|    if score > best:
9|        best = score
10|average = total / len(scores)
11|print("Total:", total)
12|print("Passed:", passed)
13|print("Failed:", len(scores) - passed)
14|print("Best:", best)
15|print("Average:", average)
""",
        "steps": [
            ("Заведи сумму баллов `total`, сначала 0.", [r"^total=0$"]),
            ("Заведи счётчик сдавших `passed`, сначала 0.", [r"^passed=0$"]),
            ("Заведи `best`: пока лучший балл — первый элемент списка.", [r"^best=scores\[0\]$"]),
            ("Начни цикл по списку: каждый балл называй `score`.", [r"^for score in scores:$"]),
            ("В цикле прибавь `score` к `total`.", [rf"^for score in scores:\n>{add('total', 'score')}$"]),
            ("Следом проверь, набран ли зачёт: балл не меньше 60.", [rf"^>{add('total', 'score')}\n>if {PY_PASS}:$"]),
            ("Если да, увеличь `passed` на 1.", [rf"^>if {PY_PASS}:\n>>{py_inc('passed')}$"]),
            ("После этого `if` проверь, больше ли `score`, чем `best`.", [rf"^>>{py_inc('passed')}\n>if {PY_BEST}:$"]),
            ("Если больше, запомни его в `best`.", [rf"^>if {PY_BEST}:\n>>best=score$"]),
            ("После цикла посчитай среднее `average`: сумма делить на длину списка.", [r"^>>best=score\naverage=total/len\(scores\)$"]),
            ("Выведи `Total:` и значение `total`.", [rf"^average=[^\n]*\n{py_print('Total:', 'total')}$"]),
            ("Выведи `Passed:` и значение `passed`.", [rf"^{py_print('Total:', 'total')}\n{py_print('Passed:', 'passed')}$"]),
            ("Выведи `Failed:` и число не сдавших: длина списка минус `passed`.", [rf"^{py_print('Passed:', 'passed')}\n{py_print('Failed:', PY_FAILED)}$"]),
            ("Выведи `Best:` и значение `best`.", [rf"^{py_print('Failed:', PY_FAILED)}\n{py_print('Best:', 'best')}$"]),
            ("Выведи `Average:` и значение `average`.", [rf"^{py_print('Best:', 'best')}\n{py_print('Average:', 'average')}$"]),
        ],
    },
    {
        "key": "python-letters", "language": "PYTHON", "title": "Гласные и согласные",
        "statement": "Разбери строку `text` по символам: сколько в ней гласных, согласных, пробелов и слов. Слова разделены одним пробелом. Программа выводит `Vowels: 6`, `Consonants: 12`, `Spaces: 4`, `Words: 5`.",
        "expected": "Vowels: 6\nConsonants: 12\nSpaces: 4\nWords: 5\n",
        "program": """
0|text = "python is fun to learn"
1|vowels = 0
2|consonants = 0
3|spaces = 0
4|for ch in text:
5|    if ch == " ":
6|        spaces += 1
7|    elif ch in "aeiou":
8|        vowels += 1
9|    else:
10|        consonants += 1
11|words = spaces + 1
12|print("Vowels:", vowels)
13|print("Consonants:", consonants)
14|print("Spaces:", spaces)
15|print("Words:", words)
""",
        "steps": [
            ("Заведи счётчик гласных `vowels`, сначала 0.", [r"^vowels=0$"]),
            ("Заведи счётчик согласных `consonants`, сначала 0.", [r"^consonants=0$"]),
            ("Заведи счётчик пробелов `spaces`, сначала 0.", [r"^spaces=0$"]),
            ("Начни цикл по строке: каждый символ называй `ch`.", [r"^for ch in text:$"]),
            ("В цикле проверь, пробел ли `ch`.", [r'^for ch in text:\n>if ch==(?:" "|\' \'):$']),
            ("Если пробел, увеличь `spaces` на 1.", [rf'^>if ch==[^\n]*:\n>>{py_inc("spaces")}$']),
            ("Иначе, если `ch` есть в строке `\"aeiou\"`…", [rf'^>>{py_inc("spaces")}\n>elif ch in (?:"aeiou"|\'aeiou\'):$']),
            ("…увеличь `vowels` на 1.", [rf'^>elif ch in [^\n]*:\n>>{py_inc("vowels")}$']),
            ("Добавь последнюю ветку «иначе».", [rf'^>>{py_inc("vowels")}\n>else:$']),
            ("В ней увеличь `consonants` на 1.", [rf'^>else:\n>>{py_inc("consonants")}$']),
            ("После цикла заведи `words`: слов на одно больше, чем пробелов.", [rf'^>>{py_inc("consonants")}\nwords=(?:spaces\+1|1\+spaces)$']),
            ("Выведи `Vowels:` и значение `vowels`.", [rf"^words=[^\n]*\n{py_print('Vowels:', 'vowels')}$"]),
            ("Выведи `Consonants:` и значение `consonants`.", [rf"^{py_print('Vowels:', 'vowels')}\n{py_print('Consonants:', 'consonants')}$"]),
            ("Выведи `Spaces:` и значение `spaces`.", [rf"^{py_print('Consonants:', 'consonants')}\n{py_print('Spaces:', 'spaces')}$"]),
            ("Выведи `Words:` и значение `words`.", [rf"^{py_print('Spaces:', 'spaces')}\n{py_print('Words:', 'words')}$"]),
        ],
    },
    {
        "key": "python-primes", "language": "PYTHON", "title": "Простые числа",
        "statement": "Выведи все простые числа от 2 до `limit`, а затем их количество и сумму. Число простое, если не делится ни на что, кроме 1 и себя. Для `limit = 30` в конце идут `Count: 10` и `Total: 129`.",
        "expected": "Primes:\n2\n3\n5\n7\n11\n13\n17\n19\n23\n29\nCount: 10\nTotal: 129\n",
        "program": """
0|limit = 30
1|count = 0
2|total = 0
3|print("Primes:")
4|for n in range(2, limit + 1):
5|    prime = True
6|    for d in range(2, n):
7|        if n % d == 0:
8|            prime = False
9|            break
10|    if prime:
11|        count += 1
12|        total += n
13|        print(n)
14|print("Count:", count)
15|print("Total:", total)
""",
        "steps": [
            ("Заведи счётчик простых чисел `count`, сначала 0.", [r"^count=0$"]),
            ("Заведи их сумму `total`, сначала 0.", [r"^total=0$"]),
            ("Выведи заголовок `Primes:`.", [r'^total=0\nprint\("Primes:"\)$']),
            ("Начни цикл: `n` от 2 до `limit` включительно.", [r'^print\("Primes:"\)\nfor n in range\(2,(?:limit\+1|1\+limit)\):$']),
            ("В цикле заведи `prime`: пока считаем `n` простым.", [r"^for n in range[^\n]*\n>prime=True$"]),
            ("Начни вложенный цикл: делитель `d` от 2, пока `d` меньше `n`.", [r"^>prime=True\n>for d in range\(2,n\):$"]),
            ("Во вложенном цикле проверь, делится ли `n` на `d`.", [r"^>for d in range[^\n]*\n>>if n%d==0:$"]),
            ("Если делится, `n` не простое: запиши это в `prime`.", [r"^>>if n%d==0:\n>>>prime=False$"]),
            ("И выйди из вложенного цикла.", [r"^>>>prime=False\n>>>break$"]),
            ("После вложенного цикла проверь, осталось ли `n` простым.", [rf"^>>>break\n>if {PY_PRIME}:$"]),
            ("Если да, увеличь `count` на 1.", [rf"^>if {PY_PRIME}:\n>>{py_inc('count')}$"]),
            ("Прибавь `n` к `total`.", [rf"^>>{py_inc('count')}\n>>{add('total', 'n')}$"]),
            ("Выведи само число `n`.", [rf"^>>{add('total', 'n')}\n>>print\(n\)$"]),
            ("После внешнего цикла выведи `Count:` и значение `count`.", [rf"^>>print\(n\)\n{py_print('Count:', 'count')}$"]),
            ("Выведи `Total:` и значение `total`.", [rf"^{py_print('Count:', 'count')}\n{py_print('Total:', 'total')}$"]),
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
