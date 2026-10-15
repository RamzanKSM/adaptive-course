"""Sets tasks.reference_code and tasks.wrong_json of curated tasks already in the course database from a built bank JSON
(build.py output, or Verify.java output — both carry `reference` and `wrong` per task), in one transaction. Nothing else
is changed.

A task is matched by its external key («curated:<slug>:<n>») among source='CURATED' tasks. Prints for each column how
many were set, already had the same value, are not in the database, and have nothing in the bank. Needs the V26 and V28
migrations (the backend applies them at startup). Run it as the application's user so SQLite's -wal/-shm files keep
their owner:

  setpriv --reuid=10001 --regid=$(stat -c %g DB) --clear-groups python3 backfill_reference.py bank.json DB
"""
import json
import sqlite3
import sys

from import_bank import wrong_json


def main(bank_path: str, db_path: str) -> None:
    tasks = json.load(open(bank_path, encoding="utf-8"))["tasks"]
    db = sqlite3.connect(db_path, timeout=15, isolation_level=None)
    db.execute("pragma busy_timeout=15000")
    columns = {row[1] for row in db.execute("pragma table_info(tasks)")}
    if "reference_code" not in columns:
        raise SystemExit("tasks.reference_code is missing: start the backend once so that it applies V26__board_tests.sql")
    if "wrong_json" not in columns:
        raise SystemExit("tasks.wrong_json is missing: start the backend once so that it applies V28__board_test_kinds.sql")
    counts = {column: {"set": 0, "unchanged": 0, "without": 0} for column in ("reference_code", "wrong_json")}
    missing = 0
    db.execute("begin immediate")
    try:
        for t in tasks:
            reference = t.get("reference")
            values = {"reference_code": reference if reference and reference.strip() else None, "wrong_json": wrong_json(t)}
            row = db.execute("select id, reference_code, wrong_json from tasks where external_key=? and source='CURATED'", (t["key"],)).fetchone()
            if not row:
                missing += 1
                continue
            current = {"reference_code": row[1], "wrong_json": row[2]}
            for column, value in values.items():
                if value is None:
                    counts[column]["without"] += 1
                elif current[column] == value:
                    counts[column]["unchanged"] += 1
                else:
                    db.execute(f"update tasks set {column}=? where id=?", (value, row[0]))
                    counts[column]["set"] += 1
        db.execute("commit")
    except BaseException:
        db.execute("rollback")
        raise
    for column, c in counts.items():
        print(f"{column}: {c['set']} set, {c['unchanged']} unchanged, {c['without']} without a value in the bank")
    print(f"{missing} bank tasks not in the database")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
