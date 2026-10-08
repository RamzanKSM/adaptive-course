package ru.teacherstaff.adaptive;

import com.sun.source.tree.*;
import com.sun.source.util.JavacTask;
import com.sun.source.util.TreeScanner;
import javax.tools.*;
import java.math.BigDecimal;
import java.net.URI;
import java.util.*;

/**
 * Enforces a task goal on Java source with the JDK compiler's syntax tree (javac parse only, nothing is compiled
 * or run here). Piston still compiles and runs the code afterwards; this check only answers "did the solution use
 * the calculation or construct the task teaches".
 */
final class JavaStructureCheck {
  private JavaStructureCheck() {}

  /** Null when the goal is met or the source cannot be parsed (Piston will report the syntax error); otherwise the full message for the student. */
  static String problem(TaskGoal goal, String source) {
    if (goal == null || !goal.structural() || source == null) return null;
    CompilationUnitTree unit = parse(source);
    if (unit == null) return null;
    Scan scan = new Scan();
    scan.scan(unit, null);
    if (goal.kind() == TaskGoal.Kind.FIXED_ARITHMETIC && !scan.calculates(goal)) {
      String numbers = String.join(", ", goal.operands().stream().map(n -> n.stripTrailingZeros().toPlainString()).toList());
      return "Неверный подход: " + TaskGoal.calculationHint(goal.operation(), numbers) + ".";
    }
    for (String construct : goal.requiredConstructs())
      if (!scan.uses(construct, goal.functionName())) return TaskGoal.constructProblem(construct, goal.functionName()).strip();
    return null;
  }

  private static CompilationUnitTree parse(String source) {
    JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
    if (compiler == null) throw new IllegalStateException("JDK compiler API is not available; the backend must run on a JDK, not a JRE");
    var file = new SimpleJavaFileObject(URI.create("string:///Solution.java"), JavaFileObject.Kind.SOURCE) {
      @Override public CharSequence getCharContent(boolean ignoreEncodingErrors) { return source; }
    };
    DiagnosticCollector<JavaFileObject> diagnostics = new DiagnosticCollector<>();
    try {
      JavacTask task = (JavacTask) compiler.getTask(null, null, diagnostics, List.of("-proc:none"), null, List.of(file));
      Iterator<? extends CompilationUnitTree> units = task.parse().iterator();
      boolean syntaxError = diagnostics.getDiagnostics().stream().anyMatch(d -> d.getKind() == Diagnostic.Kind.ERROR);
      return syntaxError || !units.hasNext() ? null : units.next();
    } catch (Exception e) { return null; }
  }

  private static final class Scan extends TreeScanner<Void, Void> {
    final Set<Tree.Kind> kinds = EnumSet.noneOf(Tree.Kind.class);
    final Set<String> methods = new HashSet<>();
    final Map<String, BigDecimal> constants = new HashMap<>();
    final Set<String> reassigned = new HashSet<>();
    final List<ExpressionTree> printed = new ArrayList<>();
    /** What is assigned to each variable, returned by each method and the method's parameters: a printed value may come from them. */
    final Map<String, List<ExpressionTree>> definitions = new HashMap<>(), returns = new HashMap<>();
    final Map<String, List<String>> parameters = new HashMap<>();
    private String method;
    /** Parameters are bound per call (Scope), so they neither define nor change a variable of the same name. */
    private final Set<Tree> parameterTrees = Collections.newSetFromMap(new IdentityHashMap<>());

    @Override public Void scan(Tree tree, Void unused) { if (tree != null) kinds.add(tree.getKind()); return super.scan(tree, unused); }
    @Override public Void visitMethod(MethodTree node, Void unused) {
      String name = node.getName().toString();
      if (!"main".equals(name) && !"<init>".equals(name)) methods.add(name);
      parameters.putIfAbsent(name, node.getParameters().stream().map(p -> p.getName().toString()).toList());
      parameterTrees.addAll(node.getParameters());
      String outer = method; method = name;
      try { return super.visitMethod(node, unused); } finally { method = outer; }
    }
    @Override public Void visitReturn(ReturnTree node, Void unused) {
      if (method != null && node.getExpression() != null) returns.computeIfAbsent(method, k -> new ArrayList<>()).add(node.getExpression());
      return super.visitReturn(node, unused);
    }
    private void define(String name, ExpressionTree value) { if (value != null) definitions.computeIfAbsent(name, k -> new ArrayList<>()).add(value); }
    @Override public Void visitVariable(VariableTree node, Void unused) {
      if (parameterTrees.contains(node)) return super.visitVariable(node, unused);
      String name = node.getName().toString();
      if (node.getInitializer() != null) initialized++;
      define(name, node.getInitializer());
      BigDecimal value = node.getInitializer() == null ? null : literal(node.getInitializer());
      if (value == null || constants.containsKey(name)) reassigned.add(name); else constants.put(name, value);
      return super.visitVariable(node, unused);
    }
    @Override public Void visitAssignment(AssignmentTree node, Void unused) { if (node.getVariable() instanceof IdentifierTree id) { reassigned.add(id.getName().toString()); define(id.getName().toString(), node.getExpression()); } return super.visitAssignment(node, unused); }
    @Override public Void visitCompoundAssignment(CompoundAssignmentTree node, Void unused) { if (node.getVariable() instanceof IdentifierTree id) { reassigned.add(id.getName().toString()); define(id.getName().toString(), node.getExpression()); } return super.visitCompoundAssignment(node, unused); }
    @Override public Void visitMethodInvocation(MethodInvocationTree node, Void unused) {
      if (node.getMethodSelect() instanceof MemberSelectTree select && Set.of("println", "print", "printf").contains(select.getIdentifier().toString())
          && select.getExpression().toString().equals("System.out")) printed.addAll(node.getArguments());
      return super.visitMethodInvocation(node, unused);
    }

    /** Parameters of a call of the student's own method, bound to the call's arguments (evaluated in the caller's scope). */
    private record Scope(Map<String, ExpressionTree> arguments, Scope caller) {}
    private static final int MAX_DEPTH = 16;

    /**
     * The printed value comes from the calculation: println(5 * 6); int cost = 5 * 6; println(cost); a value passed on
     * through other variables; or returned by the student's own method, also from its parameters: cost(6, 5) with
     * return price * count. Variables are matched by name (short single-file solutions), not by scope or order.
     */
    boolean calculates(TaskGoal goal) {
      Tree.Kind kind = switch (goal.operation()) { case "+" -> Tree.Kind.PLUS; case "-" -> Tree.Kind.MINUS; case "*" -> Tree.Kind.MULTIPLY; case "/" -> Tree.Kind.DIVIDE; case "%" -> Tree.Kind.REMAINDER; default -> null; };
      if (kind == null) return false;
      Set<String> visited = new HashSet<>();
      for (ExpressionTree argument : printed) if (derivedFrom(argument, null, kind, goal, visited, 0)) return true;
      return false;
    }
    private boolean derivedFrom(ExpressionTree expression, Scope scope, Tree.Kind kind, TaskGoal goal, Set<String> visited, int depth) {
      if (expression == null || depth > MAX_DEPTH) return false;
      boolean commutative = kind == Tree.Kind.PLUS || kind == Tree.Kind.MULTIPLY;
      List<BinaryTree> candidates = new ArrayList<>();
      List<IdentifierTree> names = new ArrayList<>();
      List<MethodInvocationTree> calls = new ArrayList<>();
      new TreeScanner<Void, Void>() {
        @Override public Void visitBinary(BinaryTree node, Void unused) { if (node.getKind() == kind) candidates.add(node); return super.visitBinary(node, unused); }
        @Override public Void visitIdentifier(IdentifierTree node, Void unused) { names.add(node); return null; }
        @Override public Void visitMethodInvocation(MethodInvocationTree node, Void unused) {
          if (node.getMethodSelect() instanceof IdentifierTree) calls.add(node); else scan(node.getMethodSelect(), null);
          return scan(node.getArguments(), null);
        }
      }.scan(expression, null);
      for (BinaryTree candidate : candidates) {
        List<BigDecimal> values = new ArrayList<>();
        for (ExpressionTree leaf : leaves(candidate, kind)) values.add(value(leaf, scope, 0));
        if (same(values, goal.operands(), commutative)) return true;
      }
      String at = "@" + System.identityHashCode(scope);
      for (IdentifierTree id : names) {
        String name = id.getName().toString();
        if (!visited.add(name + at)) continue;
        if (scope != null && scope.arguments().containsKey(name)) { if (derivedFrom(scope.arguments().get(name), scope.caller(), kind, goal, visited, depth + 1)) return true; }
        else for (ExpressionTree definition : definitions.getOrDefault(name, List.of())) if (derivedFrom(definition, scope, kind, goal, visited, depth + 1)) return true;
      }
      for (MethodInvocationTree call : calls) {
        String name = ((IdentifierTree) call.getMethodSelect()).getName().toString();
        Scope inner = new Scope(bind(name, call.getArguments()), scope);
        for (ExpressionTree result : returns.getOrDefault(name, List.of())) if (derivedFrom(result, inner, kind, goal, visited, depth + 1)) return true;
      }
      return false;
    }
    private Map<String, ExpressionTree> bind(String method, List<? extends ExpressionTree> arguments) {
      List<String> names = parameters.getOrDefault(method, List.of());
      Map<String, ExpressionTree> bound = new HashMap<>();
      for (int i = 0; i < Math.min(names.size(), arguments.size()); i++) bound.put(names.get(i), arguments.get(i));
      return bound;
    }
    private static List<ExpressionTree> leaves(ExpressionTree node, Tree.Kind kind) {
      ExpressionTree bare = unwrap(node);
      if (bare instanceof BinaryTree binary && binary.getKind() == kind) { var all = new ArrayList<>(leaves(binary.getLeftOperand(), kind)); all.addAll(leaves(binary.getRightOperand(), kind)); return all; }
      return List.of(bare);
    }
    /** A number known without running the code: a literal, an unchanged variable set to a literal, or a parameter bound to one. */
    private BigDecimal value(ExpressionTree node, Scope scope, int depth) {
      ExpressionTree bare = unwrap(node);
      BigDecimal literal = literal(bare);
      if (literal != null || !(bare instanceof IdentifierTree id) || depth > MAX_DEPTH) return literal;
      String name = id.getName().toString();
      if (scope != null && scope.arguments().containsKey(name)) return value(scope.arguments().get(name), scope.caller(), depth + 1);
      return reassigned.contains(name) ? null : constants.get(name);
    }
    private static BigDecimal literal(ExpressionTree node) {
      ExpressionTree bare = unwrap(node);
      if (bare instanceof LiteralTree literal && literal.getValue() instanceof Number number) return new BigDecimal(number.toString());
      if (bare instanceof UnaryTree unary && unary.getKind() == Tree.Kind.UNARY_MINUS) { BigDecimal inner = literal(unary.getExpression()); return inner == null ? null : inner.negate(); }
      return null;
    }
    private static ExpressionTree unwrap(ExpressionTree node) { ExpressionTree current = node; while (current instanceof ParenthesizedTree p) current = p.getExpression(); return current; }
    private static boolean same(List<BigDecimal> found, List<BigDecimal> expected, boolean commutative) {
      if (found.size() != expected.size() || found.contains(null)) return false;
      List<BigDecimal> a = new ArrayList<>(found), b = new ArrayList<>(expected);
      if (commutative) { a.sort(Comparator.naturalOrder()); b.sort(Comparator.naturalOrder()); }
      for (int i = 0; i < a.size(); i++) if (a.get(i).compareTo(b.get(i)) != 0) return false;
      return true;
    }

    boolean uses(String construct, String functionName) {
      return switch (construct) {
        case "assignment" -> kinds.contains(Tree.Kind.ASSIGNMENT) || initialized > 0;
        case "augmented_assignment" -> kinds.stream().anyMatch(k -> k.asInterface() == CompoundAssignmentTree.class) || kinds.contains(Tree.Kind.POSTFIX_INCREMENT) || kinds.contains(Tree.Kind.PREFIX_INCREMENT) || kinds.contains(Tree.Kind.POSTFIX_DECREMENT) || kinds.contains(Tree.Kind.PREFIX_DECREMENT);
        case "if" -> kinds.contains(Tree.Kind.IF) || kinds.contains(Tree.Kind.CONDITIONAL_EXPRESSION);
        case "for" -> kinds.contains(Tree.Kind.FOR_LOOP) || kinds.contains(Tree.Kind.ENHANCED_FOR_LOOP);
        case "while" -> kinds.contains(Tree.Kind.WHILE_LOOP) || kinds.contains(Tree.Kind.DO_WHILE_LOOP);
        case "function" -> functionName == null ? !methods.isEmpty() : methods.contains(functionName);
        case "return" -> kinds.contains(Tree.Kind.RETURN);
        case "list" -> kinds.contains(Tree.Kind.NEW_ARRAY) || kinds.contains(Tree.Kind.ARRAY_TYPE);
        case "dict" -> true; // no direct Java equivalent in this course; Map usage is checked by the task's own tests
        case "class" -> classCount > 1;
        case "try" -> kinds.contains(Tree.Kind.TRY);
        default -> true;
      };
    }
    int classCount, initialized;
    @Override public Void visitClass(ClassTree node, Void unused) { classCount++; return super.visitClass(node, unused); }
  }
}
