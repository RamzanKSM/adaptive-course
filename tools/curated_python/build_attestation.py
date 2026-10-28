"""Builds the attestation pool («Аттестация» in «К доске»): integrative tasks over the course from its first topic up to
the task's own topic (`skill`), one story each, the whole story different from the others (owner, 2026-10-27: students
called at the same time must not get a hint from a neighbour).

The families are written exactly like the curated bank's (JavaOutputTask / OutputTask …, see build.py and java_tasks.py)
in attestation/*.py, with ONE value set each; the check substitutes the hidden value sets as usual. Every task gets the
key «attest:<slug>». The local self-check runs as for the bank; then verify on Piston with Verify.java and copy the
verified file to backend/src/main/resources/attestation-tasks/bank.json (it ships with a normal deploy, AttestationBank
loads it at startup with tasks.mode = 'ATTESTATION').

The same builder makes two more pools of integrative tasks (owner, 2026-10-28), written the same way:
- `--pool integrative` — integrative/*.py, key «integ:<slug>»: the task of a topic's 3rd iteration in lessons; its `skill`
  is the topic at the task's core (1–2 earlier topics join it), → resources/integrative-tasks/bank.json;
- `--pool practice` — practice/*.py, key «practice:<slug>»: «Тренировочная аттестация», tasks of the attestation's size
  and kind over topics 1…skill, → resources/attestation-practice/bank.json.

Usage: python3 tools/curated_python/build_attestation.py [--pool attestation|integrative|practice] [--only java_k13,...] [--out x.json]
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

# pool → (folder of its family modules, key prefix)
POOLS = {"attestation": ("attestation", "attest:"), "integrative": ("integrative", "integ:"), "practice": ("practice", "practice:")}


def load(pool: str, only: set[str]) -> list:
    folder = POOLS[pool][0]
    found = []
    for module in sorted(pkgutil.iter_modules([str(HERE / folder)]), key=lambda m: m.name):
        if not only or module.name in only:
            found.extend(importlib.import_module(f"{folder}.{module.name}").TASKS)
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", default="attestation", choices=sorted(POOLS))
    parser.add_argument("--out", default=None, help="default: <pool>.json next to this script")
    parser.add_argument("--only", default="", help="module names in the pool's folder, comma-separated (default: all)")
    args = parser.parse_args()
    prefix = POOLS[args.pool][1]
    out = args.out or str(HERE / f"{args.pool}.json")
    tasks = []
    for template in load(args.pool, {m for m in args.only.split(",") if m}):
        if len(template.variants) != 1:
            sys.exit(f"{template.slug}: a family of this pool has exactly one value set (the stories differ, not the values)")
        if isinstance(template, java_tasks.JavaOutputTask):
            built = java_tasks.build_output(template, build.newline_note)
        elif isinstance(template, java_tasks.JavaFunctionTask):
            built = java_tasks.build_function(template)
        elif isinstance(template, build.OutputTask):
            built = build.build_output(template)
        else:
            built = build.build_function(template)
        for task in built:
            task["key"] = f"{prefix}{template.slug}"
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
            print(f"✓ {task['key']} ({task['language']}, {task['skill']})")
    if failed:
        sys.exit(f"{failed} task(s) failed the local check")
    Path(out).write_text(json.dumps({"tasks": tasks}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(tasks)} tasks to {out}")


if __name__ == "__main__":
    main()
