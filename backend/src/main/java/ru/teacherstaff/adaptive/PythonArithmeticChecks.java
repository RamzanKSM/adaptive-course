package ru.teacherstaff.adaptive;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** A fixed-output arithmetic task must check the operation, not only the number it prints. */
final class PythonArithmeticChecks {
  private PythonArithmeticChecks() {}

  static String strengthen(String statement, String testSource) {
    String lower = statement.toLowerCase(Locale.ROOT);
    int instructions = lower.indexOf("что нужно сделать");
    if (instructions < 0) throw new InvalidGeneratedContentException("Python arithmetic task needs clear steps");
    lower = lower.substring(instructions);
    int nextSection = lower.indexOf("\n##");
    if (nextSection >= 0) lower = lower.substring(0, nextSection);
    if (!lower.contains("print(")) throw new InvalidGeneratedContentException("Python arithmetic task must print an expression");
    List<String> operations = new ArrayList<>();
    if (lower.contains("слож") || lower.contains("сумм")) operations.add("Add");
    if (lower.contains("вычит") || lower.contains("вычт") || lower.contains("разност")) operations.add("Sub");
    if (lower.contains("умнож") || lower.contains("произвед")) operations.add("Mult");
    if (lower.contains("остаток")) operations.add("Mod");
    if (lower.contains("нацело") || lower.contains("целочисленн")) operations.add("FloorDiv");
    else if (lower.contains("делен") || lower.contains("делени") || lower.contains("раздел")) operations.add("Div");
    if (lower.contains("степен")) operations.add("Pow");
    if (operations.isEmpty()) throw new InvalidGeneratedContentException("Python arithmetic task must name the required operation");
    String required = operations.stream().map(op -> "\"" + op + "\"").reduce((a,b) -> a + ", " + b).orElseThrow();
    return testSource + "\n\n" + """
        # Platform check: a literal answer with the right output is not a calculation.
        _check_result = run_checks
        def run_checks():
            import ast
            from pathlib import Path
            tree = ast.parse(Path("solution.py").read_text(encoding="utf-8"))
            required = (%s,)
            assert any(
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "print"
                and len(call.args) == 1
                and isinstance(call.args[0], ast.BinOp)
                and all(any(isinstance(node, ast.BinOp) and isinstance(node.op, getattr(ast, operator))
                            for node in ast.walk(call.args[0])) for operator in required)
                for call in ast.walk(tree)
            ), "Используй действие из условия в выражении внутри print(...)"
            _check_result()
        """.formatted(required);
  }
}
