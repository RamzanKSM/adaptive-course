package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import static ru.teacherstaff.adaptive.CourseConstructs.Construct.*;

class CourseConstructsTest {
  @Test void javaMainOnlyCodeDeclaresNoMethods() {
    var used = CourseConstructs.used(Language.JAVA, """
        public class Solution {
            public static void main(String[] args) {
                int bilet = 5 * 6; // static int fake(int x) {
                if (bilet > 10) { System.out.println("static int total(int a) {"); } else if (bilet < 0) { }
            }
        }
        """);
    assertFalse(used.contains(METHOD), used.toString());
    assertFalse(used.contains(ARRAY), "String[] args of main is not an array task");
    assertFalse(used.contains(CLASS), "Solution is the platform's class");
    assertTrue(used.contains(IF));
  }

  @Test void javaFindsMethodsClassesArraysAndInput() {
    assertTrue(CourseConstructs.used(Language.JAVA, "public class Solution { static int total(int a, int b) { return a + b; } }").contains(METHOD));
    assertTrue(CourseConstructs.used(Language.JAVA, "public class Solution { public static void main(String[] args) { } }\nclass Point { int x; }").contains(CLASS));
    assertTrue(CourseConstructs.used(Language.JAVA, "public class Solution { public static void main(String[] args) { int[] a = {1}; for (int x : a) { } } }").containsAll(java.util.Set.of(ARRAY, FOR)));
    assertTrue(CourseConstructs.used(Language.JAVA, "import java.util.Scanner; public class Solution { public static void main(String[] args) { Scanner in = new Scanner(System.in); } }").contains(INPUT));
    assertTrue(CourseConstructs.checksCallMethods(Language.JAVA, "public class TestHarness { public static void main(String[] a) { Solution.total(1, 2); } }"));
    assertFalse(CourseConstructs.checksCallMethods(Language.JAVA, "public class TestHarness { public static void main(String[] a) { Solution.main(a); } }"));
  }

  @Test void pythonFindsFunctionsOutsideStrings() {
    assertFalse(CourseConstructs.used(Language.PYTHON, "x = 5 * 6\nprint(\"def f():\")  # def g():\nprint(x)\n").contains(METHOD));
    assertTrue(CourseConstructs.used(Language.PYTHON, "def area(w, h):\n    return w * h\n").contains(METHOD));
    var used = CourseConstructs.used(Language.PYTHON, "name = 'Оля'\nprint(f\"Привет, {name}\")\nprint(name[0])\n");
    assertTrue(used.contains(FSTRING)); assertFalse(used.contains(ARRAY), "indexing a string is not a list"); assertFalse(used.contains(MAP), "f-string braces are not a dict");
    assertTrue(CourseConstructs.used(Language.PYTHON, "nums = [1, 2]\nfor n in nums:\n    print(n)\n").containsAll(java.util.Set.of(ARRAY, FOR)));
    assertTrue(CourseConstructs.checksCallMethods(Language.PYTHON, "from solution import area\n\ndef run_checks():\n    assert area(2, 3) == 6\n"));
    assertFalse(CourseConstructs.checksCallMethods(Language.PYTHON, "import contextlib\n\ndef run_checks():\n    import solution\n"));
  }

  @Test void goalRequirementsMapToConstructs() throws Exception {
    var json = new ObjectMapper();
    assertTrue(CourseConstructs.required(json.readTree("{\"kind\":\"FUNCTION_BEHAVIOR\",\"requiredConstructs\":[]}")).contains(METHOD));
    assertTrue(CourseConstructs.required(json.readTree("{\"kind\":\"CONSTRUCT\",\"requiredConstructs\":[\"return\",\"for\"]}")).containsAll(java.util.Set.of(METHOD, FOR)));
  }
}
