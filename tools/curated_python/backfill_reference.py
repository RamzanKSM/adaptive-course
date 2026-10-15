"""Sets tasks.reference_code of curated tasks already in the course database from a built bank JSON (build.py output,
or Verify.java output — both carry `reference` per task), in one transaction. Nothing else is changed.

A task is matched by its external key («curated:<slug>:<n>») among source='CURATED' tasks. Prints how many were set,
already had the same program, are not in the database, and have no reference in the bank. Needs the V26 migration
(the backend applies it at startup). Run it as the application's user so SQLite's -wal/-shm files keep their owner:

  setpriv --reuid=10001 --regid=$(stat -c %g DB) --clear-groups python3 backfill_reference.py bank.json DB
"""
import json
import sqlite3
import sys


def main(bank_path: str, db_path: str) -> None:
    tasks = json.load(open(bank_path, encoding="utf-8"))["tasks"]
    db = sqlite3.connect(db_path, timeout=15, isolation_level=None)
    db.execute("pragma busy_timeout=15000")
    if "reference_code" not in {row[1] for row in db.execute("pragma table_info(tasks)")}:
        raise SystemExit("tasks.reference_code is missing: start the backend once so that it applies V26__board_tests.sql")
    updated = unchanged = missing = without = 0
    db.execute("begin immediate")
    try:
        for t in tasks:
            reference = t.get("reference")
            if not reference or not reference.strip():
                without += 1
                continue
            row = db.execute("select id, reference_code from tasks where external_key=? and source='CURATED'", (t["key"],)).fetchone()
            if not row:
                missing += 1
            elif row[1] == reference:
                unchanged += 1
            else:
                db.execute("update tasks set reference_code=? where id=?", (reference, row[0]))
                updated += 1
        db.execute("commit")
    except BaseException:
        db.execute("rollback")
        raise
    print(f"reference_code: {updated} set, {unchanged} unchanged, {missing} not in the database, {without} without a reference in the bank")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
