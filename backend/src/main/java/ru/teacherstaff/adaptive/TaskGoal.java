package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import java.util.*;
import java.util.regex.Pattern;

/**
 * What a task teaches, stated explicitly by the generator so the platform can enforce it.
 * <ul>
 *   <li>FIXED_ARITHMETIC — compute a fixed result with one operation over the numbers from the statement
 *       (print(4 * 6), not print(24) and not print(12 * 2));</li>
 *   <li>FUNCTION_BEHAVIOR — a function judged by its results on different inputs; implementation is free;</li>
 *   <li>OUTPUT_TEXT — print exact text;</li>
 *   <li>CONSTRUCT — the statement explicitly requires a construct (loop, assignment, …).</li>
 * </ul>
 * requiredConstructs may accompany any kind. Structure is checked only for FIXED_ARITHMETIC and required constructs.
 */
record TaskGoal(Kind kind, String operation, List<BigDecimal> operands, String expectedOutput, String functionName, List<String> requiredConstructs) {
  enum Kind { FIXED_ARITHMETIC, FUNCTION_BEHAVIOR, OUTPUT_TEXT, CONSTRUCT }
  record Mutant(String description, String source) {}

  static final Set<String> PYTHON_OPERATIONS = Set.of("+", "-", "*", "/", "//", "%", "**");
  static final Set<String> JAVA_OPERATIONS = Set.of("+", "-", "*", "/", "%");
  static final Map<String, String> CONSTRUCTS = new LinkedHashMap<>();
  static {
    CONSTRUCTS.put("assignment", "присваивание переменной");
    CONSTRUCTS.put("augmented_assignment", "составное присваивание (например, +=)");
    CONSTRUCTS.put("if", "условие if");
    CONSTRUCTS.put("for", "цикл for");
    CONSTRUCTS.put("while", "цикл while");
    CONSTRUCTS.put("function", "собственную функцию (метод)");
    CONSTRUCTS.put("return", "return");
    CONSTRUCTS.put("list", "список (массив)");
    CONSTRUCTS.put("dict", "словарь");
    CONSTRUCTS.put("class", "собственный класс");
    CONSTRUCTS.put("try", "обработку исключения try");
  }
  private static final Pattern IDENTIFIER = Pattern.compile("[A-Za-z_][A-Za-z0-9_]*");

  TaskGoal {
    operands = operands == null ? List.of() : List.copyOf(operands);
    requiredConstructs = requiredConstructs == null ? List.of() : List.copyOf(requiredConstructs);
  }

  static TaskGoal outputText(String expected) { return new TaskGoal(Kind.OUTPUT_TEXT, null, List.of(), expected, null, List.of()); }

  /** Parses the generator's goal object; any shape problem rejects the task. */
  static TaskGoal parse(JsonNode node) {
    if (node == null || node.isNull() || node.isMissingNode() || !node.isObject()) throw rejected("missing goal");
    Kind kind;
    try { kind = Kind.valueOf(node.path("kind").asText()); } catch (IllegalArgumentException e) { throw rejected("unknown goal kind " + node.path("kind").asText()); }
    List<BigDecimal> operands = new ArrayList<>();
    for (JsonNode operand : node.path("operands")) {
      if (!operand.isNumber()) throw rejected("operands must be numbers");
      operands.add(operand.decimalValue());
    }
    List<String> constructs = new ArrayList<>();
    for (JsonNode construct : node.path("requiredConstructs")) constructs.add(construct.asText());
    return new TaskGoal(kind, text(node, "operation"), operands, text(node, "expectedOutput"), text(node, "functionName"), constructs);
  }
  static TaskGoal fromJson(ObjectMapper json, String stored) {
    if (stored == null || stored.isBlank()) return null;
    try { return parse(json.readTree(stored)); } catch (Exception e) { return null; }
  }
  String toJson(ObjectMapper json) {
    ObjectNode node = json.createObjectNode();
    node.put("kind", kind.name()); node.put("operation", operation); node.put("expectedOutput", expectedOutput); node.put("functionName", functionName);
    ArrayNode values = node.putArray("operands"); operands.forEach(values::add);
    ArrayNode constructs = node.putArray("requiredConstructs"); requiredConstructs.forEach(constructs::add);
    return node.toString();
  }
  /** What the student hears when the printed answer is not calculated from the statement's numbers. */
  static String calculationHint(String operation, String numbers) {
    return "вычисли ответ в программе действием «" + operation + "» над числами из условия (" + numbers + ") и выведи его — сразу или через переменную; готовое число или другие числа не подойдут";
  }
  private static String text(JsonNode node, String field) { JsonNode value = node.path(field); return value.isNull() || value.isMissingNode() ? null : value.asText(); }

  boolean structural() { return kind == Kind.FIXED_ARITHMETIC || !requiredConstructs.isEmpty(); }

  /** The goal must be precise enough to enforce and agree with itself; otherwise the task is regenerated. */
  void validate(Language language, String testSource) {
    for (String construct : requiredConstructs) if (!CONSTRUCTS.containsKey(construct)) throw rejected("unknown construct " + construct);
    switch (kind) {
      case FIXED_ARITHMETIC -> {
        Set<String> allowed = language == Language.PYTHON ? PYTHON_OPERATIONS : JAVA_OPERATIONS;
        if (operation == null || !allowed.contains(operation)) throw rejected("arithmetic goal needs one of " + allowed + ", got " + operation);
        if (operands.size() < 2) throw rejected("arithmetic goal needs at least two operands");
        if (expectedOutput == null || expectedOutput.isBlank()) throw rejected("arithmetic goal needs the exact expected output");
        String result = result(language);
        if (result != null && !expectedOutput.contains(result))
          throw rejected("expected output " + quote(expectedOutput) + " does not contain " + operands + " " + operation + " = " + result);
      }
      case FUNCTION_BEHAVIOR -> {
        if (functionName == null || !IDENTIFIER.matcher(functionName).matches()) throw rejected("function goal needs a functionName");
        int calls = occurrences(testSource, functionName + "(");
        if (calls < 3) throw rejected("checks call " + functionName + "() only " + calls + " time(s); at least three different inputs are required");
      }
      case OUTPUT_TEXT -> { if (expectedOutput == null || expectedOutput.isEmpty()) throw rejected("output goal needs the exact expected output"); }
      case CONSTRUCT -> { if (requiredConstructs.isEmpty()) throw rejected("construct goal needs requiredConstructs"); }
    }
  }

  /** Result as the language prints it, or null when it cannot be computed exactly (non-integer operands). */
  String result(Language language) {
    if (kind != Kind.FIXED_ARITHMETIC || operation == null || operands.size() < 2) return null;
    for (BigDecimal operand : operands) if (operand.stripTrailingZeros().scale() > 0) return null;
    List<BigInteger> values = operands.stream().map(BigDecimal::toBigIntegerExact).toList();
    try {
      if ("/".equals(operation) && language == Language.PYTHON) {
        BigDecimal value = new BigDecimal(values.getFirst());
        for (BigInteger next : values.subList(1, values.size())) value = value.divide(new BigDecimal(next), 15, RoundingMode.HALF_EVEN);
        BigDecimal plain = value.stripTrailingZeros();
        return plain.scale() <= 0 ? plain.toBigInteger() + ".0" : plain.toPlainString();
      }
      BigInteger value = values.getFirst();
      for (BigInteger next : values.subList(1, values.size())) value = switch (operation) {
        case "+" -> value.add(next);
        case "-" -> value.subtract(next);
        case "*" -> value.multiply(next);
        case "/" -> value.divide(next); // Java int division truncates toward zero
        case "//" -> floorDiv(value, next);
        case "%" -> language == Language.PYTHON ? value.subtract(floorDiv(value, next).multiply(next)) : value.remainder(next);
        case "**" -> value.pow(next.intValueExact());
        default -> throw new IllegalStateException(operation);
      };
      return value.toString();
    } catch (ArithmeticException e) { return null; }
  }
  private static BigInteger floorDiv(BigInteger a, BigInteger b) {
    BigInteger[] qr = a.divideAndRemainder(b);
    return qr[1].signum() != 0 && (qr[1].signum() != b.signum()) ? qr[0].subtract(BigInteger.ONE) : qr[0];
  }

  /**
   * Wrong solutions the platform writes itself, so a weak test cannot slip through even if the generator's own wrong
   * examples are poor: the literal answer, the same answer from other numbers, and the right calculation with
   * the output slightly off (proves the test compares output, not just structure).
   */
  List<Mutant> platformMutants(Language language) {
    List<Mutant> mutants = new ArrayList<>();
    if (kind == Kind.FIXED_ARITHMETIC) {
      String result = result(language);
      if (result == null) return mutants;
      String expression = String.join(" " + operation + " ", operands.stream().map(TaskGoal::number).toList());
      boolean newline = expectedOutput.endsWith("\n");
      mutants.add(new Mutant("prints the ready answer instead of calculating", print(language, result, newline)));
      List<BigDecimal> other = otherOperands();
      if (other != null) mutants.add(new Mutant("same answer from other numbers " + other, print(language, String.join(" " + operation + " ", other.stream().map(TaskGoal::number).toList()), newline)));
      mutants.add(new Mutant("right calculation, wrong printed value", print(language, "(" + expression + ") + 1", newline)));
      if (expectedOutput.strip().equals(result)) mutants.add(new Mutant("right calculation, wrong line ending", print(language, expression, !newline)));
    } else if (kind == Kind.OUTPUT_TEXT && expectedOutput != null) {
      boolean newline = expectedOutput.endsWith("\n");
      String body = newline ? expectedOutput.substring(0, expectedOutput.length() - 1) : expectedOutput;
      if (!body.contains("\n")) {
        mutants.add(new Mutant("right text, wrong line ending", print(language, literal(body), !newline)));
        mutants.add(new Mutant("text with an extra space", print(language, literal(body + " "), newline)));
      }
    }
    return mutants;
  }

  /** Same result from different numbers: 4 * 6 -> 12 * 2, 3 + 5 -> 4 + 4. Null when no simple alternative exists. */
  List<BigDecimal> otherOperands() {
    if (operands.size() != 2) return null;
    for (BigDecimal operand : operands) if (operand.stripTrailingZeros().scale() > 0) return null;
    long a = operands.get(0).longValue(), b = operands.get(1).longValue();
    switch (operation) {
      case "*" -> {
        long product = a * b;
        if (product <= 0) return null;
        for (long x = 2; x * x <= product; x++) if (product % x == 0 && !(Set.of(a, b).equals(Set.of(x, product / x)))) return List.of(BigDecimal.valueOf(product / x), BigDecimal.valueOf(x));
        return Set.of(a, b).equals(Set.of(product, 1L)) ? null : List.of(BigDecimal.valueOf(product), BigDecimal.ONE);
      }
      case "+" -> { return b > 1 ? List.of(BigDecimal.valueOf(a + 1), BigDecimal.valueOf(b - 1)) : List.of(BigDecimal.valueOf(a - 1), BigDecimal.valueOf(b + 1)); }
      case "-" -> { return List.of(BigDecimal.valueOf(a + 3), BigDecimal.valueOf(b + 3)); }
      default -> { return null; }
    }
  }

  private static String print(Language language, String expression, boolean newline) {
    return language == Language.PYTHON
        ? "print(" + expression + (newline ? "" : ", end=\"\"") + ")\n"
        : "public class Solution {\n    public static void main(String[] args) {\n        System.out." + (newline ? "println" : "print") + "(" + expression + ");\n    }\n}\n";
  }
  private static String capitalize(String text) { return text.isEmpty() ? text : Character.toUpperCase(text.charAt(0)) + text.substring(1); }
  private static String number(BigDecimal value) { return value.stripTrailingZeros().scale() <= 0 ? value.toBigInteger().toString() : value.toPlainString(); }
  private static String literal(String text) { return "\"" + text.replace("\\", "\\\\").replace("\"", "\\\"") + "\""; }
  private static String quote(String text) { return "\"" + text.replace("\n", "\\n") + "\""; }
  private static int occurrences(String text, String part) { int n = 0; for (int i = text.indexOf(part); i >= 0; i = text.indexOf(part, i + 1)) n++; return n; }
  private static InvalidGeneratedContentException rejected(String reason) { return new InvalidGeneratedContentException(reason); }

  /**
   * Python AST check appended to the task's checks. It runs before them, so the student first hears about the
   * missing calculation or construct. Operands may be literals, variables assigned a literal at top level, or
   * parameters of the student's function bound to such values; the printed value may come from the calculation
   * through variables or a function's return (the same rules as JavaStructureCheck).
   */
  String pythonCheck() {
    if (!structural()) return "";
    StringBuilder code = new StringBuilder("""


        # Platform check (task goal): the solution must do what the task teaches, not only print the right text.
        _task_checks = run_checks
        def run_checks():
            import ast
            from pathlib import Path
            tree = ast.parse(Path(__file__).with_name("solution.py").read_text(encoding="utf-8"))
        """);
    if (kind == Kind.FIXED_ARITHMETIC) {
      String expected = String.join(", ", operands.stream().map(TaskGoal::number).toList());
      boolean commutative = "+".equals(operation) || "*".equals(operation);
      code.append("""
                ops = {"+": ast.Add, "-": ast.Sub, "*": ast.Mult, "/": ast.Div, "//": ast.FloorDiv, "%%": ast.Mod, "**": ast.Pow}
                op = ops[%s]
                expected = [%s]
                known = {}
                definitions, returns, parameters, scopes = {}, {}, {}, []
                def value(node, scope=None, depth=0):
                    if depth > 16:
                        return None
                    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                        return node.value
                    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
                        inner = value(node.operand, scope, depth + 1)
                        return None if inner is None else -inner
                    if isinstance(node, ast.Name):
                        if scope is not None and node.id in scope[0]:
                            return value(scope[0][node.id], scope[1], depth + 1)
                        return known.get(node.id)
                    return None
                for statement in tree.body:
                    if isinstance(statement, ast.Assign) and len(statement.targets) == 1 and isinstance(statement.targets[0], ast.Name):
                        assigned = value(statement.value)
                        if assigned is None:
                            known.pop(statement.targets[0].id, None)
                        else:
                            known[statement.targets[0].id] = assigned
                # A printed value may come from the calculation through variables or the student's own function.
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                definitions.setdefault(target.id, []).append(node.value)
                    elif isinstance(node, (ast.AnnAssign, ast.AugAssign)) and isinstance(node.target, ast.Name) and node.value is not None:
                        definitions.setdefault(node.target.id, []).append(node.value)
                    elif isinstance(node, ast.FunctionDef):
                        parameters.setdefault(node.name, [a.arg for a in node.args.args])
                        returns.setdefault(node.name, []).extend(n.value for n in ast.walk(node) if isinstance(n, ast.Return) and n.value is not None)
                def leaves(node):
                    if isinstance(node, ast.BinOp) and isinstance(node.op, op):
                        return leaves(node.left) + leaves(node.right)
                    return [node]
                def same(found):
                    if None in found or len(found) != len(expected):
                        return False
                    pairs = zip(sorted(found), sorted(expected)) if %s else zip(found, expected)
                    return all(abs(a - b) < 1e-9 for a, b in pairs)
                def derived(expression, scope, visited, depth):
                    if depth > 16:
                        return False
                    for node in ast.walk(expression):
                        if isinstance(node, ast.BinOp) and isinstance(node.op, op) and same([value(leaf, scope) for leaf in leaves(node)]):
                            return True
                    for node in ast.walk(expression):
                        if isinstance(node, ast.Name) and (node.id, id(scope)) not in visited:
                            visited.add((node.id, id(scope)))
                            if scope is not None and node.id in scope[0]:
                                if derived(scope[0][node.id], scope[1], visited, depth + 1):
                                    return True
                            elif any(derived(d, scope, visited, depth + 1) for d in definitions.get(node.id, [])):
                                return True
                        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in returns:
                            bound = dict(zip(parameters.get(node.func.id, []), node.args))
                            bound.update({k.arg: k.value for k in node.keywords if k.arg})
                            inner = (bound, scope)
                            scopes.append(inner)  # keeps id(inner) unique while the visited set refers to it
                            if any(derived(r, inner, visited, depth + 1) for r in returns[node.func.id]):
                                return True
                    return False
                calculated = any(
                    isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == "print"
                    and any(derived(argument, None, set(), 0) for argument in call.args)
                    for call in ast.walk(tree)
                )
                assert calculated, %s
            """.formatted(literal(operation), expected, commutative ? "True" : "False",
          literal(capitalize(calculationHint(operation, expected)))));
    }
    if (!requiredConstructs.isEmpty()) {
      code.append("    present = {type(node).__name__ for node in ast.walk(tree)}\n");
      for (String construct : requiredConstructs) {
        String condition = switch (construct) {
          case "assignment" -> "{'Assign', 'AnnAssign'} & present";
          case "augmented_assignment" -> "'AugAssign' in present";
          case "if" -> "'If' in present or 'IfExp' in present";
          case "for" -> "'For' in present";
          case "while" -> "'While' in present";
          case "function" -> functionName == null ? "'FunctionDef' in present" : "any(isinstance(n, ast.FunctionDef) and n.name == " + literal(functionName) + " for n in ast.walk(tree))";
          case "return" -> "'Return' in present";
          case "list" -> "{'List', 'ListComp'} & present";
          case "dict" -> "{'Dict', 'DictComp'} & present";
          case "class" -> "'ClassDef' in present";
          case "try" -> "'Try' in present";
          default -> "True";
        };
        code.append("    assert ").append(condition).append(", ").append(literal("В решении нужно использовать " + CONSTRUCTS.get(construct))).append("\n");
      }
    }
    return code.append("    _task_checks()\n").toString();
  }
}
