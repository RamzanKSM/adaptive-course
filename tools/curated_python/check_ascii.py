"""Reports Cyrillic that a student would have to TYPE or read as program text in built curated tasks.

Usage: python3 check_ascii.py built.json [more.json ...]
Checks: expected output, test inputs, code of the starter / reference / wrong solutions with comments removed,
and inline code (`...`) and code blocks inside the statement. Statement prose, titles, hints and the check
messages inside testSource may stay Russian and are not checked.
"""
import json
import re
import sys

CYR = re.compile("[А-Яа-яЁё]")


def strip_comments(code: str, language: str) -> str:
    if language == "PYTHON":
        out = []
        for line in code.splitlines():
            # drop a trailing # comment that is not inside a string (good enough for these short programs)
            in_str, quote, i = False, "", 0
            cut = len(line)
            while i < len(line):
                c = line[i]
                if in_str:
                    if c == "\\":
                        i += 2
                        continue
                    if c == quote:
                        in_str = False
                elif c in "\"'":
                    in_str, quote = True, c
                elif c == "#":
                    cut = i
                    break
                i += 1
            out.append(line[:cut])
        return "\n".join(out)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    return "\n".join(re.sub(r'//(?=(?:[^"]*"[^"]*")*[^"]*$).*', "", line) for line in code.splitlines())


def problems(task: dict) -> list[str]:
    found = []
    lang = task.get("language", "PYTHON")
    goal = task.get("goal") or {}
    if goal.get("expectedOutput") and CYR.search(goal["expectedOutput"]):
        found.append(f"expected output: {goal['expectedOutput'][:80]!r}")
    for value in task.get("testInputs") or []:
        text = json.dumps(value, ensure_ascii=False)
        if CYR.search(text):
            found.append(f"test input: {text[:80]}")
    for name in ("starter", "reference"):
        code = strip_comments(task.get(name) or "", lang)
        for line in code.splitlines():
            if CYR.search(line):
                found.append(f"{name}: {line.strip()[:100]}")
    for w in task.get("wrong") or []:
        code = strip_comments(w.get("source") or "", lang)
        for line in code.splitlines():
            if CYR.search(line):
                found.append(f"wrong «{w.get('description', '')[:30]}»: {line.strip()[:100]}")
                break
    statement = task.get("statement") or ""
    for block in re.findall(r"```.*?```", statement, flags=re.S):
        code = strip_comments(block.strip("`"), lang)
        for line in code.splitlines():
            if CYR.search(line):
                found.append(f"statement code block: {line.strip()[:100]}")
    prose = re.sub(r"```.*?```", "", statement, flags=re.S)
    for span in re.findall(r"`([^`\n]+)`", prose):
        if CYR.search(span):
            found.append(f"statement inline code: `{span[:80]}`")
    return found


def main() -> None:
    total = bad = 0
    for path in sys.argv[1:]:
        for task in json.load(open(path, encoding="utf-8"))["tasks"]:
            total += 1
            found = problems(task)
            if found:
                bad += 1
                print(f"✗ {task['key']}")
                for f in found[:8]:
                    print(f"    {f}")
    print(f"{total} tasks checked, {bad} with Cyrillic in code")


if __name__ == "__main__":
    main()
