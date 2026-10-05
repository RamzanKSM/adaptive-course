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

  /** Null when the goal is met or the source cannot be parsed (Piston will report the syntax error); otherwise a message for the student. */
  static String problem(TaskGoal goal, String source) {
    if (goal == null || !goal.structural() || source == null) return null;
    CompilationUnitTree unit = parse(source);
    if (unit == null) return null;
    Scan scan = new Scan();
    scan.scan(unit, null);
    if (goal.kind() == TaskGoal.Kind.FIXED_ARITHMETIC && !scan.calculates(goal)) {
      String numbers = String.join(", ", goal.operands().stream().map(n -> n.stripTrailingZeros().toPlainString()).toList());
      return "вычисли ответ в программе действием «" + goal.operation() + "» над числами из условия (" + numbers + "), а не готовым числом или другими числами";
    }
    for (String construct : goal.requiredConstructs())
      if (!scan.uses(construct, goal.functionName())) return "в решении нужно использовать " + TaskGoal.CONSTRUCTS.getOrDefault(construct, construct);
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

    @Override public Void scan(Tree tree, Void unused) { if (tree != null) kinds.add(tree.getKind()); return super.scan(tree, unused); }
    @Override public Void visitMethod(MethodTree node, Void unused) { if (!"main".contentEquals(node.getName()) && !"<init>".contentEquals(node.getName())) methods.add(node.getName().toString()); return super.visitMethod(node, unused); }
    @Override public Void visitVariable(VariableTree node, Void unused) {
      String name = node.getName().toString();
      if (node.getInitializer() != null) initialized++;
      BigDecimal value = node.getInitializer() == null ? null : literal(node.getInitializer());
      if (value == null || constants.containsKey(name)) reassigned.add(name); else constants.put(name, value);
      return super.visitVariable(node, unused);
    }
    @Override public Void visitAssignment(AssignmentTree node, Void unused) { if (node.getVariable() instanceof IdentifierTree id) reassigned.add(id.getName().toString()); return super.visitAssignment(node, unused); }
    @Override public Void visitCompoundAssignment(CompoundAssignmentTree node, Void unused) { if (node.getVariable() instanceof IdentifierTree id) reassigned.add(id.getName().toString()); return super.visitCompoundAssignment(node, unused); }
    @Override public Void visitMethodInvocation(MethodInvocationTree node, Void unused) {
      if (node.getMethodSelect() instanceof MemberSelectTree select && Set.of("println", "print", "printf").contains(select.getIdentifier().toString())
          && select.getExpression().toString().equals("System.out")) printed.addAll(node.getArguments());
      return super.visitMethodInvocation(node, unused);
    }

    boolean calculates(TaskGoal goal) {
      Tree.Kind kind = switch (goal.operation()) { case "+" -> Tree.Kind.PLUS; case "-" -> Tree.Kind.MINUS; case "*" -> Tree.Kind.MULTIPLY; case "/" -> Tree.Kind.DIVIDE; case "%" -> Tree.Kind.REMAINDER; default -> null; };
      if (kind == null) return false;
      boolean commutative = kind == Tree.Kind.PLUS || kind == Tree.Kind.MULTIPLY;
      for (ExpressionTree argument : printed) {
        List<BinaryTree> candidates = new ArrayList<>();
        new TreeScanner<Void, Void>() { @Override public Void visitBinary(BinaryTree node, Void unused) { if (node.getKind() == kind) candidates.add(node); return super.visitBinary(node, unused); } }.scan(argument, null);
        for (BinaryTree candidate : candidates) {
          List<BigDecimal> values = new ArrayList<>();
          for (ExpressionTree leaf : leaves(candidate, kind)) values.add(value(leaf));
          if (same(values, goal.operands(), commutative)) return true;
        }
      }
      return false;
    }
    private static List<ExpressionTree> leaves(ExpressionTree node, Tree.Kind kind) {
      ExpressionTree bare = unwrap(node);
      if (bare instanceof BinaryTree binary && binary.getKind() == kind) { var all = new ArrayList<>(leaves(binary.getLeftOperand(), kind)); all.addAll(leaves(binary.getRightOperand(), kind)); return all; }
      return List.of(bare);
    }
    private BigDecimal value(ExpressionTree node) {
      ExpressionTree bare = unwrap(node);
      BigDecimal literal = literal(bare);
      if (literal != null) return literal;
      if (bare instanceof IdentifierTree id && !reassigned.contains(id.getName().toString())) return constants.get(id.getName().toString());
      return null;
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
