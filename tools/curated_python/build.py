"""Builds the curated Python task bank: hand-written task families where the wording stays and the values change.

Each family (a template) is one formulation of a task with several value sets; every value set becomes its own task
(external key «curated:<slug>:<n>»). Two kinds of tasks:

* Output tasks (goal OUTPUT_TEXT). The starter code already holds the given variables (`a = "14"`); the student writes
  the calculation and prints the result. The check runs the program as is and compares the output with the example,
  then runs it again with other values substituted into those starter lines — so a program that prints a ready answer
  instead of calculating it fails. Required constructs (if, for, …) are enforced by the platform's own goal check.
* Function tasks (goal FUNCTION_BEHAVIOR). The platform records the reference function's answers on the test inputs
  and checks the student's function on them, like the generator's function tasks.

The script checks every task locally (reference passes, wrong solutions fail) and writes bank.json. The Java
verifier (Verify.java) then runs each task through the platform's TaskVerifier on the real Piston before import.

Usage: python3 tools/curated_python/build.py [--only SKILL,...] [--out bank.json]
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import importlib
import io
import json
import os
import pkgutil
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Topic modules import the dataclasses from «build»; make that the running module, not a second copy of it.
sys.modules.setdefault("build", sys.modules[__name__])
TOPICS = HERE / "topics"

# The platform's fixed Python entry point (PistonCodeRunner.PYTHON_ENTRY): reads the pass marker from stdin, runs the
# hidden checks, prints the marker only if they pass.
PYTHON_ENTRY = """import os, sys
def _main():
    marker = sys.stdin.readline().strip()
    sys.stdin = open(os.devnull)
    import test_solution
    test_solution.run_checks()
    sys.stdout.write("\\n" + marker + "\\n")
    sys.stdout.flush()
_main()
"""

STARTER_NOTE = "# Напиши решение здесь\n"


@dataclass
class OutputTask:
    """One formulation; every entry of `variants` becomes a task. Texts are str.format templates over the values
    (use {name} for the value as code, e.g. "14" with quotes, and {name!v} is not needed: plain {name} is code)."""
    skill: str
    difficulty: int
    slug: str
    title: str
    given: list[str]                      # variable names the starter code defines, in order
    variants: list[dict[str, str]]        # value sets: name -> Python literal source, e.g. {"a": '"14"'}
    hidden: list[dict[str, str]]          # other value sets the check substitutes (3–4 of them)
    intro: str                            # the situation, 1–3 sentences
    steps: list[str]                      # «Что нужно сделать»
    hint: str
    solution: str                         # the code after the starter lines (reference)
    wrong: list[tuple[str, str]]          # (what is wrong, code after the starter lines)
    constructs: list[str] = field(default_factory=list)       # platform-enforced: if, for, while, function, list, …
    # Extra structure checks: (ast node class name, message), or ("re:<regex>", message) matched against the source
    # with comments removed — for what is not a node type of its own: @property, super(), finally, __init__.
    must_use: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class FunctionTask:
    """A function judged by its return values on recorded test inputs."""
    skill: str
    difficulty: int
    slug: str
    title: str
    function: str
    variants: list[dict[str, object]]     # constants of the formulation, e.g. {"rate": 10}
    intro: str
    steps: list[str]
    hint: str
    starter: str                          # template; usually the def line, a comment and `pass`
    solution: str                         # template: the reference function
    inputs: list[str]                     # argument lists as source code, distinct; the first `public` are examples
    wrong: list[tuple[str, str]]          # (what is wrong, template of a whole wrong solution)
    public: int = 2
    must_use: list[tuple[str, str]] = field(default_factory=list)


# ───────── Running code locally ─────────

def run_program(source: str) -> str:
    """Output of a program run as a script."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(source, "solution.py", "exec"), {"__name__": "__main__"})
    return out.getvalue()


def substitute(source: str, values: dict[str, str]) -> str:
    """The program with the first top-level assignment of each given variable set to another value."""
    tree = ast.parse(source)
    left = dict(values)
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in left:
            node.value = ast.parse(left.pop(node.targets[0].id), mode="eval").body
    assert not left, f"starter lacks {left}"
    return ast.unparse(tree)


def checks_pass(test_source: str, solution: str) -> tuple[bool, str]:
    """Runs the hidden checks like Piston does (fixed entry point, pass marker on stdin)."""
    with tempfile.TemporaryDirectory() as job:
        Path(job, "main.py").write_text(PYTHON_ENTRY, encoding="utf-8")
        Path(job, "test_solution.py").write_text(test_source, encoding="utf-8")
        Path(job, "solution.py").write_text(solution, encoding="utf-8")
        p = subprocess.run([sys.executable, "main.py"], cwd=job, input="__PASS__\n", capture_output=True, text=True, timeout=20)
        lines = [l.strip() for l in p.stdout.splitlines() if l.strip()]
        ok = p.returncode == 0 and lines and lines[-1] == "__PASS__"
        last = (p.stderr.strip().splitlines() or [""])[-1]
        return bool(ok), last


# ───────── Output tasks ─────────

OUTPUT_CHECKER = '''import ast
import contextlib
import io
import re
from pathlib import Path

GIVEN = {given!r}
CASES = {cases!r}


def _run(code):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(code, "solution.py", "exec"), {{"__name__": "__main__"}})
    return out.getvalue()


def _show(text):
    text = text.replace("\\n", "↵")
    return text if len(text) <= 200 else text[:200] + "…"


def _substitute(source, values):
    tree = ast.parse(source)
    left = dict(values)
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in left:
            node.value = ast.parse(left.pop(node.targets[0].id), mode="eval").body
    return ast.unparse(tree), left


def run_checks():
    source = Path(__file__).with_name("solution.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
{structure}    actual = _run(source)
    expected = CASES[0][1]
    if actual != expected:
        raise AssertionError("Вывод не совпадает с примером: ожидалось «%s», получилось «%s»" % (_show(expected), _show(actual)))
    for number, (values, expected) in enumerate(CASES[1:], start=1):
        code, missing = _substitute(source, values)
        if missing:
            raise AssertionError("Не удаляй и не переименовывай переменные из заготовки (%s): при проверке в них подставляются другие значения" % ", ".join(sorted(missing)))
        try:
            actual = _run(code)
        except Exception as error:
            raise AssertionError("Проверка %d из %d: с другими значениями переменных программа завершилась с ошибкой %s" % (number, len(CASES) - 1, type(error).__name__))
        if actual != expected:
            raise AssertionError("Проверка %d из %d: с другими значениями переменных ответ неверный. Программа должна вычислять ответ из переменных, а не выводить готовый результат" % (number, len(CASES) - 1))
'''

STRUCTURE_CHECK = '''    if not any(isinstance(node, ast.{node}) for node in ast.walk(tree)):
        raise AssertionError({message!r})
'''
PATTERN_CHECK = '''    if not re.search({pattern!r}, "\\n".join(line.split("#")[0] for line in source.splitlines())):
        raise AssertionError({message!r})
'''


def structure_checks(must_use: list[tuple[str, str]]) -> str:
    return "".join(PATTERN_CHECK.format(pattern=node[3:], message=message) if node.startswith("re:")
                   else STRUCTURE_CHECK.format(node=node, message=message) for node, message in must_use)


def starter_lines(task: OutputTask, values: dict[str, str]) -> str:
    return "".join(f"{name} = {values[name]}\n" for name in task.given)


def newline_note(output: str) -> str:
    lines = output.split("\n")
    if output.endswith("\n"):
        lines = lines[:-1]
    note = "После последней строки нужен перевод строки." if output.endswith("\n") else "После последней строки перевода строки нет."
    if len(lines) > 1 and all(lines):
        note += " Пустых строк нет."
    return note


def fmt(text: str, values: dict) -> str:
    return text.format(**values)


def build_output(task: OutputTask) -> list[dict]:
    built = []
    for number, values in enumerate(task.variants, start=1):
        starter = starter_lines(task, values)
        reference = starter + task.solution.rstrip() + "\n"
        expected = run_program(reference)
        assert expected.strip(), f"{task.slug}: empty output"
        assert not re.search(r"\d[eE][+-]\d", expected), f"{task.slug}: exponent in output {expected!r}"
        for line in expected.splitlines():
            for word in line.replace(",", " ").split():
                if "." in word and word.replace(".", "", 1).replace("-", "", 1).isdigit():
                    assert len(word.split(".")[1]) <= 3, f"{task.slug} #{number}: float noise in output {expected!r}"
        cases = [[None, expected]]
        for hidden in task.hidden:
            cases.append([hidden, run_program(substitute(reference, hidden))])
        # A program printing the example's answer must fail on some substituted values (a classification task may
        # legitimately give the same answer for several of them).
        assert any(other != expected for _, other in cases[1:]), f"{task.slug} #{number}: every hidden value set gives {expected!r} — a ready answer would pass"
        assert len(task.hidden) >= 3, f"{task.slug}: need at least 3 hidden value sets"
        structure = structure_checks(task.must_use)
        checker = OUTPUT_CHECKER.format(given=task.given, cases=cases, structure=structure)
        code_values = {name: values[name] for name in task.given}
        statement = render_output_statement(task, code_values, starter, expected)
        wrong = [{"description": d, "source": starter + body.rstrip() + "\n"} for d, body in task.wrong]
        built.append({
            "key": f"curated:{task.slug}:{number}", "skill": task.skill, "difficulty": task.difficulty,
            "title": fmt(task.title, code_values), "statement": statement,
            "starter": starter + STARTER_NOTE, "reference": reference, "testSource": checker, "testFileName": "test_solution.py",
            "goal": {"kind": "OUTPUT_TEXT", "operation": None, "operands": [], "expectedOutput": expected, "functionName": None, "requiredConstructs": task.constructs},
            "wrong": wrong, "testInputs": [],
        })
    return built


def render_output_statement(task: OutputTask, values: dict, starter: str, expected: str) -> str:
    quoted = [f"`{n}`" for n in task.given]
    names = quoted[0] if len(quoted) == 1 else ", ".join(quoted[:-1]) + " и " + quoted[-1]
    steps = "\n".join(f"{i}. {fmt(step, values)}" for i, step in enumerate(task.steps, start=1))
    return (f"{fmt(task.intro, values)}\n\n"
            f"В заготовке уже есть {'переменная' if len(task.given) == 1 else 'переменные'} {names}:\n\n"
            f"```python\n{starter}```\n\n"
            f"Не меняй и не удаляй {'эту строку' if len(task.given) == 1 else 'эти строки'}: при проверке в {'неё' if len(task.given) == 1 else 'них'} подставят другие значения, "
            f"и программа должна выдать правильный ответ и для них.\n\n"
            f"## Что нужно сделать\n\n{steps}\n\n"
            f"## Пример\n\nДля значений из заготовки программа выводит:\n\n```text\n{expected}```\n\n"
            f"{newline_note(expected)}\n\n"
            f"## Подсказка\n\n{fmt(task.hint, values)}\n")


# ───────── Function tasks ─────────

def call_reference(source: str, function: str, args: str):
    scope: dict = {"__name__": "solution"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(source, "solution.py", "exec"), scope)
        return eval(f"{function}({args})", scope)


def build_function(task: FunctionTask) -> list[dict]:
    built = []
    assert len(task.inputs) >= 6 and len(set(task.inputs)) == len(task.inputs), f"{task.slug}: need ≥6 distinct inputs"
    for number, values in enumerate(task.variants, start=1):
        reference = fmt(task.solution, values).rstrip() + "\n"
        answers = [call_reference(reference, task.function, args) for args in task.inputs]
        assert len({repr(a) for a in answers}) >= 3, f"{task.slug}: answers too uniform {answers}"
        examples = "\n".join(f"{task.function}({args})  # → {answer!r}" for args, answer in zip(task.inputs[:task.public], answers[:task.public]))
        steps = "\n".join(f"{i}. {fmt(step, values)}" for i, step in enumerate(task.steps, start=1))
        statement = (f"{fmt(task.intro, values)}\n\n## Что нужно сделать\n\n{steps}\n\n"
                     f"## Примеры\n\n```python\n{examples}\n```\n\n"
                     f"Функция должна **возвращать** результат через `return`, а не печатать его.\n\n"
                     f"## Подсказка\n\n{fmt(task.hint, values)}\n")
        wrong = []
        for description, body in task.wrong:
            source = fmt(body, values).rstrip() + "\n"
            got = []
            for args in task.inputs:
                try:
                    got.append(repr(call_reference(source, task.function, args)))
                except Exception as error:  # noqa: BLE001 — a crash also counts as different
                    got.append(type(error).__name__)
            assert got != [repr(a) for a in answers], f"{task.slug}: wrong solution «{description}» gives the right answers"
            wrong.append({"description": description, "source": source})
        built.append({
            "key": f"curated:{task.slug}:{number}", "skill": task.skill, "difficulty": task.difficulty,
            "title": fmt(task.title, values), "statement": statement,
            "starter": fmt(task.starter, values).rstrip() + "\n", "reference": reference, "testSource": "", "testFileName": "test_solution.py",
            "goal": {"kind": "FUNCTION_BEHAVIOR", "operation": None, "operands": [], "expectedOutput": None, "functionName": task.function, "requiredConstructs": ["function", "return"]},
            "wrong": wrong, "testInputs": [{"input": args, "public": i < task.public} for i, args in enumerate(task.inputs)],
            "mustUse": [list(m) for m in task.must_use],
        })
    return built


# ───────── Main ─────────

def load_tasks() -> list:
    sys.path.insert(0, str(HERE))
    found = []
    for module in sorted(pkgutil.iter_modules([str(TOPICS)]), key=lambda m: m.name):
        found.extend(importlib.import_module(f"topics.{module.name}").TASKS)
    return found


def self_check(task: dict) -> list[str]:
    """Reference passes the checks, each wrong solution fails them (output tasks; function tasks are checked above)."""
    if task["goal"]["kind"] != "OUTPUT_TEXT":
        return []
    problems = []
    ok, why = checks_pass(task["testSource"], task["reference"])
    if not ok:
        problems.append(f"reference fails: {why}")
    for wrong in task["wrong"]:
        ok, _ = checks_pass(task["testSource"], wrong["source"])
        if ok:
            problems.append(f"wrong solution passes: {wrong['description']}")
    hardcoded = task["starter"].replace(STARTER_NOTE, "") + f"print({task['goal']['expectedOutput'].rstrip(chr(10))!r})\n"
    if checks_pass(task["testSource"], hardcoded)[0]:
        problems.append("a ready answer passes")
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", default="")
    parser.add_argument("--out", default=str(HERE / "bank.json"))
    args = parser.parse_args()
    only = {s for s in args.only.split(",") if s}
    tasks = []
    for template in load_tasks():
        if only and template.skill not in only:
            continue
        tasks.extend(build_output(template) if isinstance(template, OutputTask) else build_function(template))
    keys = [t["key"] for t in tasks]
    assert len(keys) == len(set(keys)), "duplicate keys"
    failed = 0
    for task in tasks:
        problems = self_check(task)
        if problems:
            failed += 1
            print(f"✗ {task['key']}: " + "; ".join(problems))
    by_skill: dict[str, list[int]] = {}
    for t in tasks:
        by_skill.setdefault(t["skill"], []).append(t["difficulty"])
    for skill, diffs in by_skill.items():
        print(f"{skill}: {len(diffs)} tasks, difficulties {sorted(diffs)}")
    if failed:
        sys.exit(f"{failed} task(s) failed the local check")
    Path(args.out).write_text(json.dumps({"tasks": tasks}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(tasks)} tasks to {args.out}")


if __name__ == "__main__":
    main()
