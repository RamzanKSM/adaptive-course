# Writing curated Java tasks for Rmzn Tutor

> Since 2026-10-14: every string in code and output is plain English ASCII (statements stay Russian and quote
> the English strings), and each topic has two families per difficulty — see `NEW_STORIES_GUIDE.md`, which overrides
> «What to make» below. Paths to scratch folders below are examples.

You write hand-made Java practice tasks (in Russian) for an adaptive beginner course. These topics have few or no tasks
and the LLM generator is unreliable, so we fill them with curated task families. You ONLY create topic modules and run
the local builder — never touch the database, the server, git, or other files.

## Read first
- `tools/curated_python/java_tasks.py` (in `/Users/ramzankibiev/Stuff/TeacherStaff/adaptive_course`) — read it fully:
  `JavaOutputTask`, `JavaFunctionTask`, the check (TestHarness) template and the local self-check.
- A finished example: `tools/curated_python/topics_java/t17_if_else.py` — copy its structure, tone and statement style.
- Statement style reference (Python twins of many topics, same course): `tools/curated_python/topics/t*.py`.
- What the course intends for each topic: `java_initial_diagnostic_mvp_v2.md` — search for `**Навык:** \`<SKILL>\``
  (the question is just above that line).
- Put each topic in `tools/curated_python/topics_java/tNN_<name>.py` (NN = sort order), exporting `TASKS = [...]`, and
  `from java_tasks import JavaOutputTask, JavaFunctionTask`. **Write each topic file as soon as it is ready** (a network
  error may interrupt you; finished files survive).
- Check: `cd /Users/ramzankibiev/Stuff/TeacherStaff/adaptive_course/tools/curated_python && python3 build.py --only <SKILL,...> --out /tmp/<name>.json`
  (compiles with javac --release 15 locally) — iterate until no ✗ lines. Other agents work in the same folder: do not
  edit build.py, java_tasks.py or files you did not create; if they seem wrong, report it.

## Course order (Java; a topic may use everything with a smaller or equal sort order)
1 println, 2 variables, 3 assignment, 4 arithmetic, 5 execution order, 10 primitive types, 12 String, 14 / and %,
15 += -= ++, 17 if/else, 19 comparison operators, 20 &&, 21 || and !, 22 switch, 23 for, 26 accumulator in a loop,
27 while, 28 loop termination, 29 array indexing, 31 arrays, 32 iterating an array, 33 methods (static methods of
Solution), 34 parameters and return values, 35 classes, 36 creating objects, 37 constructors, 38 this, 39 encapsulation
(private fields), 40 getters/setters, 41 static, 42 inheritance, 43 method override, 44 polymorphism, 45 interfaces,
46 super, 47 List, 48 Set, 49 Map, 50 list operations, 51 choosing a collection, 52 try/catch, 54 finally, 55 throw,
56 throws. The platform rejects a task of a topic that needs methods before 33 or own classes before 35. Never read
input (Scanner, System.in).

## Java 15 only (Piston)
No records, no `instanceof` pattern matching, no sealed classes, no `String.formatted`… — the builder compiles with
`--release 15`, so it will tell you. `var`, switch expressions (`case 1 ->`), text blocks, `List.of` are fine.

## Output tasks (`JavaOutputTask`) — the default before topic 33 and for most class/collection topics
- `given`: the task's input data as static fields of Solution, `[("int", "price"), ("String", "count"), ("int[]", "scores")]`,
  values as Java literal source per variant/hidden set: `{"price": "450", "count": '"3"', "scores": "{5, 3, 8}"}`
  (arrays as `{…}`; for a List field use e.g. `("List<String>", "names")` with `'new ArrayList<>(List.of("Аня", "Борис"))'`).
  The student writes `main` and reads those fields; the check sets them to each `hidden` set through reflection and calls
  `main` again, so the program must really compute. ≥3 hidden sets covering every branch and boundary (e.g. exactly 120
  for `>= 120`), arrays/lists of different lengths where the task is about «last» or «all» elements; at least one hidden
  set must give a different output than each variant.
- `solution`: the reference body of `main` (no indentation needed). `classes`: extra top-level classes of the reference
  (written after Solution, without `public`). `wrong`: 2 realistic beginner mistakes as `(description, main body)` or
  `(description, main body, classes)`; each must make the CHECK fail (wrong output on the example or some hidden set),
  not just crash or not compile — the self-check reports both.
- `constructs` (platform-enforced, checked on the syntax tree): "if", "for", "while", "function" (a method besides
  main), "return", "class" (a class besides Solution), "list" (arrays), "try", "assignment", "augmented_assignment".
- `checks`: Java statements run before the output check, for what the syntax tree cannot see — use
  `need(condition, "Сообщение")` and `cls("ClassName")` (null if missing) with reflection, e.g.
  `Class<?> c = cls("Circle"); need(c != null && cls("Shape") != null && cls("Shape").isInterface() && cls("Shape").isAssignableFrom(c), "Сделай Shape интерфейсом и реализуй его в Circle");`
  or check that a field is private: `need(java.lang.reflect.Modifier.isPrivate(c.getDeclaredField("balance").getModifiers()), "…")`
  (guard getDeclaredField with try/catch → need(false, …)). Messages: Russian, friendly, ONE line, say what to use and why.
- `reset`: Java statements run before each run, for static state the task's classes keep between runs, e.g.
  `setStatic("Ticket", "sold", 0);` — needed in static-counter tasks (topic 41), otherwise counts add up across runs.
- Output must be deterministic: never print a HashSet/HashMap/Set.of/Map.of by iterating or with toString — use
  LinkedHashMap/LinkedHashSet/TreeMap/TreeSet or sort first; never print an object's default toString (`Dog@1b6d3586`);
  no float noise (prefer int; if double, values like 2.5); 1–10 short lines.

## Function tasks (`JavaFunctionTask`) — topics 33–34 and wherever a method's return value is the point
- `starter`: the whole `public class Solution { static int cost(int hours) { // Напиши решение здесь\n return 0; } }`
  (method stub, correct signature, readable indentation); `solution`: the whole reference class; `inputs`: ≥6 distinct
  argument lists as Java source (`"3, 4"`, `'"Аня", 7'`, `"new int[]{1, 2, 3}"`), the first `public` (default 2) are
  shown as examples; answers must not be uniform (≥3 distinct) — so no boolean returns; `wrong`: 2 whole wrong classes.
  `variants` are constants of the formulation used via str.format in texts and code (e.g. a price per hour).
- In str.format templates (texts AND function-task code) literal braces must be doubled `{{ }}` — Java code has many!
  Output-task `solution`/`wrong`/`classes`/`checks` are NOT formatted (single braces).

## What to make
Exactly 3 families per topic (difficulty 1, 2, 3; easy → harder; 3 may combine earlier topics), each with exactly 3
`variants` — the SAME wording, DIFFERENT values; each variant becomes its own task. Texts in Russian, «ты», for absolute
beginners: `title`, `intro` (1–3 sentences, a concrete everyday situation; may show values via `{field}`), `steps`
(2–5 precise numbered instructions: class/method/field names, exact output format, punctuation), `hint` (one idea, not
the answer). Never mention checks, tests, files, «TestHarness», «harness», «solution», Piston, reflection. Slugs
`java-<topic>-<name>`, unique, lowercase. Don't name classes or print text containing «room»/«zoom»/«bloom».

Quality bar: a student who follows the steps literally gets exactly the expected output; re-read rendered statements
from the built JSON as a beginner would and fix grammar with inserted values. Vary situations; no near-duplicates.

When done, reply with the files you created, the builder summary lines for your topics, and anything you were unsure about.
