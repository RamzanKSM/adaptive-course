"""Java task families for the curated bank (see build.py for the Python ones and the overall idea).

Output tasks (goal OUTPUT_TEXT). Java is compiled, so the given data cannot be rewritten in the source and run again
as in Python. Instead it lives in static fields of Solution (`static String count = "4";`), the student writes main,
and the check (TestHarness) sets those fields to other values through reflection and calls Solution.main again —
a program that prints a ready answer fails. Before every run the fields (and any static state the task names in
`reset`) get their values again. What the syntax tree cannot tell — an interface, a private field, a method that
throws — is checked by behaviour in `checks`: Java statements using need(condition, message) and cls(name).

Function tasks (goal FUNCTION_BEHAVIOR) are judged by the platform's own case checker, like generated ones.

Everything runs on Java 15 (Piston): compile locally with --release 15. Check messages must be one line: the
platform shows the student the first line of an AssertionError.
"""
from __future__ import annotations

import base64
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

JAVA_HOME = os.environ.get("JAVA_HOME", "/Users/ramzankibiev/Library/Java/JavaVirtualMachines/corretto-21.0.5/Contents/Home")
JAVAC, JAVA = str(Path(JAVA_HOME, "bin", "javac")), str(Path(JAVA_HOME, "bin", "java"))
PASS_MARKER = "{{PASS_MARKER}}"
STARTER_NOTE = "        // Напиши решение здесь\n"


@dataclass
class JavaOutputTask:
    skill: str
    difficulty: int
    slug: str
    title: str
    given: list[tuple[str, str]]          # (Java type, field name), e.g. ("String", "count"), ("int[]", "scores")
    variants: list[dict[str, str]]        # field -> Java literal source: {"count": '"4"', "scores": "{5, 3, 8}"}
    hidden: list[dict[str, str]]          # other value sets the check sets (≥3)
    intro: str
    steps: list[str]
    hint: str
    solution: str                         # body of main (reference), without indentation
    wrong: list[tuple]                    # (what is wrong, body of main[, classes]) — classes replace `classes`
    classes: str = ""                     # extra top-level classes of the reference (after Solution)
    constructs: list[str] = field(default_factory=list)   # platform-enforced: if, for, while, function, class, list, try …
    checks: str = ""                      # Java statements run before the output check: need(cond, "msg"); cls("Name")
    reset: str = ""                       # Java statements run before every run, e.g. setStatic("Ticket", "sold", 0);


@dataclass
class JavaFunctionTask:
    skill: str
    difficulty: int
    slug: str
    title: str
    function: str
    variants: list[dict[str, object]]
    intro: str
    steps: list[str]
    hint: str
    starter: str                          # template: the whole Solution class with a method stub
    solution: str                         # template: the whole reference Solution class (+ other classes)
    inputs: list[str]                     # argument lists as Java source, distinct; the first `public` are examples
    wrong: list[tuple[str, str]]          # (what is wrong, template of a whole wrong solution)
    public: int = 2


def fmt(text: str, values: dict) -> str:
    return text.format(**values)


def b64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def _array_literal(java_type: str, literal: str) -> str:
    """`{5, 3}` is only valid in a declaration; elsewhere an array needs `new int[]{5, 3}`."""
    return f"new {java_type}{literal}" if java_type.endswith("[]") and literal.strip().startswith("{") else literal


def _boxed(java_type: str, literal: str) -> str:
    """A value for Field.set: primitives box themselves except where the literal's type differs (long, char …)."""
    literal = _array_literal(java_type, literal)
    casts = {"long": "(long) ", "double": "(double) ", "float": "(float) ", "short": "(short) ", "byte": "(byte) "}
    return f"({casts[java_type]}{literal})" if java_type in casts else literal


UTIL = re.compile(r"\b(?:List|ArrayList|LinkedList|Set|HashSet|TreeSet|LinkedHashSet|Map|HashMap|TreeMap|LinkedHashMap|"
                  r"Collections|Arrays|Iterator|Deque|ArrayDeque|Queue|Scanner|Random|Objects)\b")


def needs_util(task: JavaOutputTask) -> bool:
    """`import java.util.*;` when the task's data or its reference/wrong code uses java.util."""
    code = [t for t, _ in task.given] + [task.solution, task.classes] + [part for w in task.wrong for part in w[1:]]
    return any(UTIL.search(text or "") for text in code)


def starter_source(task: JavaOutputTask, values: dict[str, str], body: str | None = None, classes: str = "") -> str:
    fields = "".join(f"    static {t} {name} = {values[name]};\n" for t, name in task.given)
    main = STARTER_NOTE if body is None else "".join("        " + line + "\n" if line else "\n" for line in body.rstrip().split("\n"))
    tail = ("\n" + classes.strip() + "\n") if classes.strip() else ""
    head = "import java.util.*;\n\n" if needs_util(task) else ""
    return f"{head}public class Solution {{\n{fields}\n    public static void main(String[] args) {{\n{main}    }}\n}}\n{tail}"


HARNESS = """import java.io.*;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class TestHarness {
  static final String[] FIELDS = {%(fields)s};
  static final Object[][] VALUES = {%(values)s};
  static final String[] EXPECTED = {%(expected)s};

  static String dec(String b) { return new String(Base64.getDecoder().decode(b), StandardCharsets.UTF_8); }
  static String show(String s) { String t = s.replace("\\n", "\\u21b5"); return t.length() > 200 ? t.substring(0, 200) + "\\u2026" : t; }
  static void need(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
  static Class<?> cls(String name) { try { return Class.forName(name, false, Solution.class.getClassLoader()); } catch (ClassNotFoundException e) { return null; } }
  static void setStatic(String cls, String field, Object value) throws Exception {
    Class<?> c = cls(cls); if (c == null) return;
    try { Field f = c.getDeclaredField(field); f.setAccessible(true); if (Modifier.isStatic(f.getModifiers()) && !Modifier.isFinal(f.getModifiers())) f.set(null, value); } catch (NoSuchFieldException ignored) { }
  }
  static void reset() throws Exception {
%(reset)s  }
  static void checks() throws Exception {
%(checks)s  }

  static String run(int i) throws Throwable {
    for (int k = 0; k < FIELDS.length; k++) {
      Field f;
      try { f = Solution.class.getDeclaredField(FIELDS[k]); }
      catch (NoSuchFieldException e) { throw new AssertionError("Не удаляй и не переименовывай поле " + FIELDS[k] + " из заготовки: при проверке в него подставляются другие значения"); }
      if (!Modifier.isStatic(f.getModifiers()) || Modifier.isFinal(f.getModifiers())) throw new AssertionError("Поле " + FIELDS[k] + " должно остаться static и без final, как в заготовке");
      f.setAccessible(true); f.set(null, VALUES[i][k]);
    }
    reset();
    PrintStream out = System.out; ByteArrayOutputStream buffer = new ByteArrayOutputStream();
    System.setOut(new PrintStream(buffer, true, "UTF-8"));
    try { Solution.main(new String[0]); } finally { System.setOut(out); }
    return buffer.toString("UTF-8");
  }

  public static void main(String[] args) throws Throwable {
    checks();
    String actual = run(0), expected = dec(EXPECTED[0]);
    if (!actual.equals(expected)) throw new AssertionError("Вывод не совпадает с примером: ожидалось «" + show(expected) + "», получилось «" + show(actual) + "»");
    int total = VALUES.length - 1;
    for (int i = 1; i < VALUES.length; i++) {
      String other;
      try { other = run(i); }
      catch (AssertionError e) { throw e; }
      catch (Throwable e) { Throwable cause = e instanceof InvocationTargetException && e.getCause() != null ? e.getCause() : e; throw new AssertionError("Проверка " + i + " из " + total + ": с другими значениями полей программа завершилась с ошибкой " + cause.getClass().getSimpleName()); }
      if (!other.equals(dec(EXPECTED[i]))) throw new AssertionError("Проверка " + i + " из " + total + ": с другими значениями полей ответ неверный. Проверь, что программа вычисляет ответ из полей и правильно обрабатывает все случаи из условия, включая граничные значения");
    }
    System.out.print("%(marker)s");
  }
}
"""

RECORDER = """import java.io.*;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class Recorder {
  static final String[] FIELDS = {%(fields)s};
  static final Object[][] VALUES = {%(values)s};
  static Class<?> cls(String name) { try { return Class.forName(name, false, Solution.class.getClassLoader()); } catch (ClassNotFoundException e) { return null; } }
  static void setStatic(String cls, String field, Object value) throws Exception {
    Class<?> c = cls(cls); if (c == null) return;
    try { Field f = c.getDeclaredField(field); f.setAccessible(true); if (Modifier.isStatic(f.getModifiers()) && !Modifier.isFinal(f.getModifiers())) f.set(null, value); } catch (NoSuchFieldException ignored) { }
  }
  static void reset() throws Exception {
%(reset)s  }
  public static void main(String[] args) throws Throwable {
    PrintStream out = System.out;
    for (int i = 0; i < VALUES.length; i++) {
      for (int k = 0; k < FIELDS.length; k++) { Field f = Solution.class.getDeclaredField(FIELDS[k]); f.setAccessible(true); f.set(null, VALUES[i][k]); }
      reset();
      ByteArrayOutputStream buffer = new ByteArrayOutputStream();
      System.setOut(new PrintStream(buffer, true, "UTF-8"));
      try { Solution.main(new String[0]); } finally { System.setOut(out); }
      out.println("__CASE__" + i + ":" + Base64.getEncoder().encodeToString(buffer.toString("UTF-8").getBytes(StandardCharsets.UTF_8)));
    }
  }
}
"""


def _indent(code: str, spaces: int) -> str:
    return "".join((" " * spaces + line if line.strip() else line) + "\n" for line in code.strip("\n").split("\n")) if code.strip() else ""


def run_java(files: dict[str, str], main_class: str, timeout: int = 30) -> tuple[int, str, str]:
    """Compiles the files (Java 15 level) and runs main_class; returns (exit code, stdout, stderr)."""
    with tempfile.TemporaryDirectory() as job:
        for name, source in files.items():
            Path(job, name).write_text(source, encoding="utf-8")
        c = subprocess.run([JAVAC, "--release", "15", "-encoding", "UTF-8", "-nowarn", "-d", job] + [str(Path(job, n)) for n in files],
                           capture_output=True, text=True, timeout=120)
        if c.returncode != 0:
            return 99, "", "COMPILE: " + c.stderr
        r = subprocess.run([JAVA, "-Dfile.encoding=UTF-8", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-Xss8m", "-cp", job, main_class],
                           capture_output=True, text=True, timeout=timeout, encoding="utf-8")
        return r.returncode, r.stdout, r.stderr


def _values_source(task: JavaOutputTask, value_sets: list[dict[str, str]]) -> str:
    return ", ".join("{" + ", ".join(_boxed(t, values[name]) for t, name in task.given) + "}" for values in value_sets)


def _fields_source(task: JavaOutputTask) -> str:
    return ", ".join(f'"{name}"' for _, name in task.given)


def record_outputs(task: JavaOutputTask, reference: str, value_sets: list[dict[str, str]]) -> list[str]:
    recorder = RECORDER % {"fields": _fields_source(task), "values": _values_source(task, value_sets), "reset": _indent(task.reset, 4)}
    code, out, err = run_java({"Solution.java": reference, "Recorder.java": recorder}, "Recorder")
    assert code == 0, f"{task.slug}: reference failed: {err[-1500:]}"
    answers = {}
    for line in out.splitlines():
        m = re.match(r"^__CASE__(\d+):(.*)$", line)
        if m:
            answers[int(m.group(1))] = base64.b64decode(m.group(2)).decode("utf-8")
    return [answers[i] for i in range(len(value_sets))]


def harness_source(task: JavaOutputTask, value_sets: list[dict[str, str]], outputs: list[str], marker: str = PASS_MARKER) -> str:
    return HARNESS % {"fields": _fields_source(task), "values": _values_source(task, value_sets), "expected": ", ".join(f'"{b64(o)}"' for o in outputs),
                      "reset": _indent(task.reset, 4), "checks": _indent(task.checks, 4), "marker": marker}


def checks_pass(harness: str, solution: str) -> tuple[bool, str]:
    code, out, err = run_java({"Solution.java": solution, "TestHarness.java": harness.replace(PASS_MARKER, "__PASS__")}, "TestHarness")
    passed = code == 0 and out.strip().endswith("__PASS__")
    reason = err.strip().splitlines()[0] if err.strip() else ""
    return passed, reason


def render_statement(task: JavaOutputTask, values: dict, starter: str, expected: str, newline_note) -> str:
    names = [f"`{n}`" for _, n in task.given]
    listed = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " и " + names[-1]
    single = len(names) == 1
    steps = "\n".join(f"{i}. {fmt(step, values)}" for i, step in enumerate(task.steps, start=1))
    return (f"{fmt(task.intro, values)}\n\n"
            f"Данные уже записаны в {'поле' if single else 'поля'} класса `Solution` — {listed}:\n\n"
            f"```java\n{starter}```\n\n"
            f"Ответ выводит метод `main`, а данные он берёт из {'этого поля' if single else 'этих полей'}. Не меняй и не удаляй "
            f"{'его' if single else 'их'}: при проверке в {'него' if single else 'них'} подставят другие значения, и программа должна выдать правильный ответ и для них.\n\n"
            f"## Что нужно сделать\n\n{steps}\n\n"
            f"## Пример\n\nДля значений из заготовки программа выводит:\n\n```text\n{expected}```\n\n"
            f"{newline_note(expected)}\n\n"
            f"## Подсказка\n\n{fmt(task.hint, values)}\n")


def build_output(task: JavaOutputTask, newline_note) -> list[dict]:
    assert len(task.hidden) >= 3, f"{task.slug}: need at least 3 hidden value sets"
    built = []
    for number, values in enumerate(task.variants, start=1):
        starter = starter_source(task, values)
        reference = starter_source(task, values, task.solution, task.classes)
        value_sets = [values] + task.hidden
        outputs = record_outputs(task, reference, value_sets)
        expected = outputs[0]
        assert expected.strip(), f"{task.slug} #{number}: empty output"
        assert any(o != expected for o in outputs[1:]), f"{task.slug} #{number}: every hidden value set gives {expected!r} — a ready answer would pass"
        assert "@" not in expected, f"{task.slug} #{number}: output looks like an object's default toString: {expected!r}"
        harness = harness_source(task, value_sets, outputs)
        wrong = []
        for w in task.wrong:
            description, body = w[0], w[1]
            classes = w[2] if len(w) > 2 else task.classes
            wrong.append({"description": description, "source": starter_source(task, values, body, classes)})
        built.append({
            "key": f"curated:{task.slug}:{number}", "language": "JAVA", "skill": task.skill, "difficulty": task.difficulty,
            "title": fmt(task.title, values), "statement": render_statement(task, values, starter, expected, newline_note),
            "starter": starter, "reference": reference, "testSource": harness, "testFileName": "TestHarness.java",
            "goal": {"kind": "OUTPUT_TEXT", "operation": None, "operands": [], "expectedOutput": expected, "functionName": None, "requiredConstructs": task.constructs},
            "wrong": wrong, "testInputs": [],
        })
    return built


def self_check(task: dict) -> list[str]:
    problems = []
    ok, why = checks_pass(task["testSource"], task["reference"])
    if not ok:
        problems.append(f"reference fails: {why}")
    for w in task["wrong"]:
        ok, why = checks_pass(task["testSource"], w["source"])
        if ok:
            problems.append(f"wrong solution passes: {w['description']}")
        elif not why.startswith("Exception in thread \"main\" java.lang.AssertionError") and "AssertionError" not in why:
            problems.append(f"wrong solution «{w['description']}» does not fail a check but crashes/does not compile: {why[:200]}")
    literal = task["goal"]["expectedOutput"]
    printed = "".join(f"System.out.println({java_string(line)});\n" for line in literal.rstrip("\n").split("\n"))
    hardcoded = re.sub(r"        // Напиши решение здесь\n", lambda _: _indent(printed, 8), task["starter"])
    if checks_pass(task["testSource"], hardcoded)[0]:
        problems.append("a ready answer passes")
    return problems


def java_string(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ───────── Function tasks ─────────

FMT = """  static String fmt(Object o) {
    if (o == null) return "null";
    if (o instanceof String) return "\\"" + o + "\\"";
    if (o instanceof Character) return "'" + o + "'";
    if (o.getClass().isArray()) { String d = Arrays.deepToString(new Object[]{o}); return d.substring(1, d.length() - 1); }
    return String.valueOf(o);
  }
"""


def call_all(source: str, function: str, inputs: list[str]) -> list[str]:
    calls = "".join(f'    try {{ System.out.println("__CASE__{i}:" + fmt(Solution.{function}({args}))); }} catch (Throwable t) {{ System.out.println("__CASE__{i}:!" + t.getClass().getSimpleName()); }}\n'
                    for i, args in enumerate(inputs))
    runner = f"import java.util.*;\n\npublic class Runner {{\n{FMT}  public static void main(String[] args) {{\n{calls}  }}\n}}\n"
    code, out, err = run_java({"Solution.java": source, "Runner.java": runner}, "Runner")
    assert code == 0, f"does not compile or run: {err[-1500:]}"
    answers = {}
    for line in out.splitlines():
        m = re.match(r"^__CASE__(\d+):(.*)$", line)
        if m:
            answers[int(m.group(1))] = m.group(2)
    return [answers.get(i, "?") for i in range(len(inputs))]


def build_function(task: JavaFunctionTask) -> list[dict]:
    assert len(task.inputs) >= 6 and len(set(task.inputs)) == len(task.inputs), f"{task.slug}: need ≥6 distinct inputs"
    built = []
    for number, values in enumerate(task.variants, start=1):
        reference = fmt(task.solution, values).rstrip() + "\n"
        answers = call_all(reference, task.function, task.inputs)
        assert not any(a.startswith("!") for a in answers), f"{task.slug}: reference throws on some input: {answers}"
        assert len(set(answers)) >= 3, f"{task.slug}: answers too uniform {answers}"
        examples = "\n".join(f"{task.function}({args})  // → {answer}" for args, answer in zip(task.inputs[:task.public], answers[:task.public]))
        steps = "\n".join(f"{i}. {fmt(step, values)}" for i, step in enumerate(task.steps, start=1))
        statement = (f"{fmt(task.intro, values)}\n\n## Что нужно сделать\n\n{steps}\n\n"
                     f"## Примеры\n\n```java\n{examples}\n```\n\n"
                     f"Метод должен **возвращать** результат через `return`, а не печатать его.\n\n"
                     f"## Подсказка\n\n{fmt(task.hint, values)}\n")
        wrong = []
        for description, body in task.wrong:
            source = fmt(body, values).rstrip() + "\n"
            try:
                got = call_all(source, task.function, task.inputs)
            except AssertionError:
                got = ["compile error"]
            assert got != answers, f"{task.slug}: wrong solution «{description}» gives the right answers"
            wrong.append({"description": description, "source": source})
        built.append({
            "key": f"curated:{task.slug}:{number}", "language": "JAVA", "skill": task.skill, "difficulty": task.difficulty,
            "title": fmt(task.title, values), "statement": statement,
            "starter": fmt(task.starter, values).rstrip() + "\n", "reference": reference, "testSource": "", "testFileName": "TestHarness.java",
            "goal": {"kind": "FUNCTION_BEHAVIOR", "operation": None, "operands": [], "expectedOutput": None, "functionName": task.function, "requiredConstructs": ["function", "return"]},
            "wrong": wrong, "testInputs": [{"input": args, "public": i < task.public} for i, args in enumerate(task.inputs)],
        })
    return built
