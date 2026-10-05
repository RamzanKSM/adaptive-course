-- Repair the already-generated ticket task: checking only "24\n" accepted print(24).
UPDATE tasks SET test_source = test_source || '

# Platform check: the printed value must come from multiplication.
_check_result = run_checks
def run_checks():
    import ast
    from pathlib import Path
    tree = ast.parse(Path("solution.py").read_text(encoding="utf-8"))
    assert any(
        isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "print"
        and len(call.args) == 1
        and isinstance(call.args[0], ast.BinOp)
        and isinstance(call.args[0].op, ast.Mult)
        for call in ast.walk(tree)
    ), "Используй умножение в выражении внутри print(...)"
    _check_result()
' WHERE language = 'PYTHON' AND skill_code = 'PY_ARITHMETIC_BASIC'
    AND title = 'Считаем стоимость билетов';

-- The single literal submission was incorrectly credited. Keep its history, but make it retryable.
UPDATE submissions SET passed = 0,
    runner_output = 'Неверный результат: используй умножение в выражении внутри print(...)'
WHERE passed = 1
  AND trim(source_code) = '# Напиши решение здесь' || char(10) || 'print(24)'
  AND task_id IN (SELECT id FROM tasks WHERE language = 'PYTHON'
    AND skill_code = 'PY_ARITHMETIC_BASIC' AND title = 'Считаем стоимость билетов');

DELETE FROM successful_task_credit
WHERE task_id IN (SELECT id FROM tasks WHERE language = 'PYTHON'
    AND skill_code = 'PY_ARITHMETIC_BASIC' AND title = 'Считаем стоимость билетов')
  AND NOT EXISTS (
    SELECT 1 FROM submissions s JOIN lessons l ON l.id = s.lesson_id
    WHERE s.task_id = successful_task_credit.task_id AND l.user_id = successful_task_credit.user_id AND s.passed = 1
  );

UPDATE student_skills SET iteration_successes = 0
WHERE skill_code = 'PY_ARITHMETIC_BASIC' AND iteration_successes = 1 AND completed_iterations = 0
  AND user_id IN (
    SELECT l.user_id FROM submissions s JOIN lessons l ON l.id = s.lesson_id
    JOIN tasks t ON t.id = s.task_id
    WHERE t.language = 'PYTHON' AND t.skill_code = 'PY_ARITHMETIC_BASIC'
      AND t.title = 'Считаем стоимость билетов'
      AND trim(s.source_code) = '# Напиши решение здесь' || char(10) || 'print(24)'
  )
  AND NOT EXISTS (
    SELECT 1 FROM successful_task_credit c JOIN task_target_skills ts ON ts.task_id = c.task_id
    WHERE c.user_id = student_skills.user_id AND ts.skill_code = student_skills.skill_code
  );
