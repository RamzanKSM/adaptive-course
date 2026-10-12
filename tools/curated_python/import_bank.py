"""Imports verified curated tasks (Verify.java output) into the course database, in one transaction.

A task is matched by its external key («curated:<slug>:<n>»): a new task is inserted, an existing one is updated in
place, so submissions and credit stay attached and a re-run adds no duplicates. Run it as the application's user so
SQLite's -wal/-shm files keep their owner:

  setpriv --reuid=10001 --regid=$(stat -c %g DB) --clear-groups python3 import_bank.py verified.json DB
"""
import json
import sqlite3
import sys

QUALITY_VERSION = 2  # LearningContentGenerator.TASK_QUALITY_VERSION


def main(bank_path: str, db_path: str) -> None:
    tasks = json.load(open(bank_path, encoding="utf-8"))["tasks"]
    db = sqlite3.connect(db_path, timeout=15, isolation_level=None)
    db.execute("pragma busy_timeout=15000")
    db.execute("pragma foreign_keys=on")
    inserted = updated = 0
    db.execute("begin immediate")
    try:
        for t in tasks:
            if not db.execute("select 1 from skills where code=? and language='PYTHON'", (t["skill"],)).fetchone():
                raise SystemExit(f"unknown topic {t['skill']} ({t['key']})")
            row = db.execute("select id from tasks where external_key=?", (t["key"],)).fetchone()
            values = (t["skill"], t["title"], t["statement"], t["starter"], t["testSource"], t["testFileName"], t["difficulty"], t["goalJson"], QUALITY_VERSION)
            if row:
                task_id = row[0]
                db.execute("update tasks set skill_code=?, title=?, statement=?, starter_code=?, test_source=?, test_file_name=?, difficulty=?, goal_json=?, "
                           "quality_version=?, language='PYTHON', source='CURATED', mode='NORMAL', active=1 where id=?", values + (task_id,))
                db.execute("delete from task_target_skills where task_id=?", (task_id,))
                db.execute("delete from task_cases where task_id=?", (task_id,))
                updated += 1
            else:
                task_id = db.execute("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,difficulty,goal_json,quality_version,"
                                     "language,source,mode,active,external_key) values(?,?,?,?,?,?,?,?,?,'PYTHON','CURATED','NORMAL',1,?) returning id",
                                     values + (t["key"],)).fetchone()[0]
                inserted += 1
            db.execute("insert into task_target_skills(task_id,skill_code) values(?,?)", (task_id, t["skill"]))
            for c in t["cases"]:
                db.execute("insert into task_cases(task_id,ordinal,input,expected,is_public) values(?,?,?,?,?)",
                           (task_id, c["ordinal"], c["input"], c["expected"], 1 if c["public"] else 0))
        db.execute("commit")
    except BaseException:
        db.execute("rollback")
        raise
    print(f"curated tasks: {inserted} inserted, {updated} updated")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
