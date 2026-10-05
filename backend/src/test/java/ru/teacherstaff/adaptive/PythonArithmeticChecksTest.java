package ru.teacherstaff.adaptive;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import java.nio.file.Files;
import java.nio.file.Path;
import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

class PythonArithmeticChecksTest {
  @TempDir Path directory;

  @Test void literalOutputCannotPassMultiplicationTask() throws Exception {
    assumeTrue(pythonAvailable());
    String statement = "## Что нужно сделать\nУмножь цену на количество и передай выражение в print(...).\n## Пример\n24";
    String outputCheck = """
        import contextlib
        import io
        def run_checks():
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                import solution
            assert output.getvalue() == "24\\n"
        """;
    Files.writeString(directory.resolve("test_solution.py"), PythonArithmeticChecks.strengthen(statement, outputCheck));
    Files.writeString(directory.resolve("solution.py"), "print(24)\n");
    assertNotEquals(0, runChecks());
    Files.writeString(directory.resolve("solution.py"), "price = 6\ncount = 4\nprint(price * count)\n");
    assertEquals(0, runChecks());
  }

  private int runChecks() throws Exception {
    Process process = new ProcessBuilder("python3", "-B", "-c", "import test_solution; test_solution.run_checks()")
        .directory(directory.toFile()).redirectErrorStream(true).start();
    process.getInputStream().readAllBytes();
    return process.waitFor();
  }

  private boolean pythonAvailable() {
    try { return new ProcessBuilder("python3", "--version").start().waitFor() == 0; }
    catch (Exception ignored) { return false; }
  }
}
