"""Builds the attestation pool («Аттестация» in «К доске»): integrative tasks over the course from its first topic up to
the task's own topic (`skill`), one story each, the whole story different from the others (owner, 2026-10-27: students
called at the same time must not get a hint from a neighbour).

The families are written exactly like the curated bank's (JavaOutputTask / OutputTask …, see build.py and java_tasks.py)
in attestation/*.py, with ONE value set each; the check substitutes the hidden value sets as usual. Every task gets the
key «attest:<slug>». The local self-check runs as for the bank; then verify on Piston with Verify.java and copy the
verified file to backend/src/main/resources/attestation-tasks/bank.json (it ships with a normal deploy, AttestationBank
loads it at startup with tasks.mode = 'ATTESTATION').

Usage: python3 tools/curated_python/build_attestation.py [--only java_k13,...] [--out attestation.json]
"""
from __future__ import annotations

import argparse
import importlib
import json
import pkgutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
import java_tasks  # noqa: E402

FOLDER = HERE / "attestation"


def load(only: set[str]) -> list:
    found = []
    for module in sorted(pkgutil.iter_modules([str(FOLDER)]), key=lambda m: m.name):
        if not only or module.name in only:
            found.extend(importlib.import_module(f"attestation.{module.name}").TASKS)
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "attestation.json"))
    parser.add_argument("--only", default="", help="module names in attestation/, comma-separated (default: all)")
    args = parser.parse_args()
    tasks = []
    for template in load({m for m in args.only.split(",") if m}):
        if len(template.variants) != 1:
            sys.exit(f"{template.slug}: an attestation family has exactly one value set (the stories differ, not the values)")
        if isinstance(template, java_tasks.JavaOutputTask):
            built = java_tasks.build_output(template, build.newline_note)
        elif isinstance(template, java_tasks.JavaFunctionTask):
            built = java_tasks.build_function(template)
        elif isinstance(template, build.OutputTask):
            built = build.build_output(template)
        else:
            built = build.build_function(template)
        for task in built:
            task["key"] = f"attest:{template.slug}"
        tasks.extend(built)
    keys = [t["key"] for t in tasks]
    assert len(keys) == len(set(keys)), "duplicate keys"
    failed = 0
    for task in tasks:
        problems = build.self_check(task)
        if problems:
            failed += 1
            print(f"✗ {task['key']}: " + "; ".join(problems))
        else:
            print(f"✓ {task['key']} ({task['language']}, up to {task['skill']})")
    if failed:
        sys.exit(f"{failed} task(s) failed the local check")
    Path(args.out).write_text(json.dumps({"tasks": tasks}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(tasks)} tasks to {args.out}")


if __name__ == "__main__":
    main()
