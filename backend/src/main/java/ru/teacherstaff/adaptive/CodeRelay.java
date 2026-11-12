package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.security.SecureRandom;
import java.time.*;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Pattern;

/**
 * «Эстафета»: the whole group solves one task in one editor. One student writes at a time; his turn is one small step of
 * the task (a line or a branch) and lasts turnSeconds (25 s by default). The step is checked on every save of the code —
 * when it passes, the pen goes to the next student in the queue at once. A pass («Пас») or the end of the time is a skip:
 * the step stays for the next student and the group's streak (steps in a row without a skip) drops to 0 — a skip
 * matters to the whole group, the group's record streak is kept. No grades and no points (owner, 2026-10-28); who did
 * what is seen by the teacher only. Students who left (no poll for PRESENT) are passed over without a skip.
 * <p>
 * Only the writer may change the code, so there are no conflicting edits to merge: the writer's browser sends the whole
 * text, everybody else polls it about once a second. The server's clock ends the turns (on any request, under one lock).
 * Tasks: resources/relay-tasks/tasks.json, built by tools/relay/build_relay_tasks.py (the checks and the normalization
 * are described there). The rules: backend/README.md, «Эстафета».
 */
@Component
class CodeRelay {
    static final int DEFAULT_TURN = 25, MIN_TURN = 5, MAX_TURN = 120, MAX_CODE = 20_000, EXTEND = 10;
    static final Duration PRESENT = Duration.ofSeconds(12), SEEN_EVERY = Duration.ofSeconds(3), GRACE = Duration.ofSeconds(1), ACTIVE_FOR = Duration.ofHours(6);
    private static final Logger log = LoggerFactory.getLogger(CodeRelay.class);
    private final JdbcTemplate db;
    private final Clock clock;
    private final ObjectMapper json;
    private final PistonCodeRunner runner;
    private final Map<String, Task> tasks = new LinkedHashMap<>();
    private final Random random = new SecureRandom();
    private final ExecutorService background = Executors.newSingleThreadExecutor(BackgroundThreads.named("relay-run"));
    CodeRelay(JdbcTemplate db, Clock clock, ObjectMapper json, PistonCodeRunner runner) {
        this.db = db;
        this.clock = clock;
        this.json = json;
        this.runner = runner;
        try (var in = CodeRelay.class.getResourceAsStream("/relay-tasks/tasks.json")) {
            for (JsonNode t : json.readTree(in).get("tasks")) {
                var steps = new ArrayList<Step>();
                for (JsonNode s : t.get("steps")) {
                    var checks = new ArrayList<Pattern>();
                    for (JsonNode c : s.get("check")) checks.add(Pattern.compile(c.asText(), Pattern.MULTILINE));
                    steps.add(new Step(s.get("prompt").asText(), List.copyOf(checks), s.get("hint").asText(), s.get("code").asText()));
                }
                tasks.put(t.get("key").asText(), new Task(t.get("key").asText(), Language.of(t.get("language").asText()), t.get("title").asText(), t.get("statement").asText(),
                                                          t.get("starter").asText(), t.get("expectedOutput").asText(), List.copyOf(steps)));
            }
        } catch (IOException | NullPointerException e) {
            throw new IllegalStateException("relay-tasks/tasks.json is missing or broken", e);
        }
    }

    /**
     * The code as the checks see it. Java: one string, whitespace dropped except one space between two word characters,
     * string and char literals kept, // comments dropped. Python: one line per non-empty line, the indentation level as
     * that many «>», the line normalized the same way (# comments dropped).
     */
    static String normalize(String code, Language language) {
        if (language == Language.JAVA) return squeeze(code, "//");
        var out = new StringBuilder();
        var widths = new ArrayDeque<Integer>();
        widths.push(0);
        for (String line : code.replace("\t", "    ").split("\\R")) {
            String body = squeeze(line, "#");
            if (body.isEmpty()) continue;
            int width = 0;
            while (width < line.length() && line.charAt(width) == ' ') width++;
            if (width > widths.peek()) widths.push(width);
            else while (widths.size() > 1 && width < widths.peek()) widths.pop();
            if (!out.isEmpty()) out.append('\n');
            out.append(">".repeat(widths.size() - 1)).append(body);
        }
        return out.toString();
    }

    private static String squeeze(String code, String comment) {
        var out = new StringBuilder();
        boolean space = false;
        int i = 0, n = code.length();
        while (i < n) {
            char c = code.charAt(i);
            if (c == '"' || c == '\'') {
                int j = i + 1;
                while (j < n && code.charAt(j) != c && code.charAt(j) != '\n') j += code.charAt(j) == '\\' ? 2 : 1;
                j = Math.min(j + 1, n);
                if (space && !out.isEmpty() && word(out.charAt(out.length() - 1))) out.append(' ');
                out.append(code, i, j);
                i = j;
                space = false;
                continue;
            }
            if (code.startsWith(comment, i)) {
                while (i < n && code.charAt(i) != '\n') i++;
                space = true;
                continue;
            }
            if (Character.isWhitespace(c)) {
                space = true;
                i++;
                continue;
            }
            if (space && !out.isEmpty() && word(out.charAt(out.length() - 1)) && word(c)) out.append(' ');
            out.append(c);
            space = false;
            i++;
        }
        return out.toString();
    }

    private static boolean word(char c) {
        return Character.isLetterOrDigit(c) || c == '_' || c == '$';
    }

    /**
     * How many steps from the first are done: each one's check matches (or the teacher credited it), stopping at the first that is not.
     */
    static int doneSteps(Task task, String code, Set<Integer> credited) {
        String normalized = normalize(code, task.language());
        int done = 0;
        for (var step : task.steps()) {
            if (!credited.contains(done) && step.checks().stream().noneMatch(p -> p.matcher(normalized).find())) break;
            done++;
        }
        return done;
    }

    // ---------------------------------------------------------------- checks

    private static void requireTurn(Relay r) {
        if (r.writer() == null || !(r.status().equals("RUNNING") || r.status().equals("PAUSED")))
            throw new ApiError("RELAY_NO_TURN", "Сейчас никто не пишет");
    }

    private static void requireWriter(Relay r, long user, Map<String, Object> body) {
        if (!r.status().equals("RUNNING") || r.writer() == null || r.writer() != user || !(body.get("turn") instanceof Number t) || t.intValue() != r.turnNo())
            throw new ApiError("RELAY_NOT_YOUR_TURN", "Сейчас пишет не ты");
    }

    private static String string(Map<String, Object> body, String key) {
        return body != null && body.get(key) instanceof String s && !s.isBlank() ? s.strip() : null;
    }

    private static int num(Object value) {
        return ((Number) value).intValue();
    }

    // ---------------------------------------------------------------- the relay

    private static Instant at(Object value) {
        return value == null ? null : Instant.parse((String) value);
    }

    static Map<String, Object> obj(Object... entries) {
        var m = new LinkedHashMap<String, Object>();
        for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]);
        return m;
    }

    Collection<Task> tasks() {
        return tasks.values();
    }

    Task task(String key) {
        var t = tasks.get(key);
        if (t == null) throw new ApiError("RELAY_UNKNOWN_TASK", "Нет такой задачи для эстафеты");
        return t;
    }

    private Relay load(long id) {
        var rows = db.queryForList("select * from relays where id=?", id);
        if (rows.isEmpty()) throw new NotFoundError("RELAY_NOT_FOUND", "Эстафета не найдена");
        var r = rows.getFirst();
        var credited = new TreeSet<Integer>();
        for (String s : ((String) r.get("credited")).split(",")) if (!s.isBlank()) credited.add(Integer.parseInt(s));
        return new Relay(id, (String) r.get("group_name"), Language.of(r.get("language")), task((String) r.get("task_key")), num(r.get("turn_seconds")),
                         (String) r.get("status"), (String) r.get("code"), ((Number) r.get("version")).longValue(), num(r.get("step")), num(r.get("turn_no")),
                         r.get("writer_id") == null ? null : ((Number) r.get("writer_id")).longValue(), at(r.get("turn_started_at")), at(r.get("turn_ends_at")),
                         r.get("paused_left_ms") == null ? null : ((Number) r.get("paused_left_ms")).longValue(), num(r.get("streak")), num(r.get("best_streak")),
                         num(r.get("skips")), credited, (String) r.get("run_json"), at(r.get("created_at")), at(r.get("started_at")), num(r.get("on_board")) == 1);
    }

    /**
     * The group's relay that is not finished (started in the last ACTIVE_FOR), or null.
     */
    private Long activeOf(String group) {
        var ids = db.queryForList("select id from relays where group_name=? and status<>'FINISHED' and created_at>? order by id desc limit 1", Long.class,
                                  group, clock.instant().minus(ACTIVE_FOR).toString());
        return ids.isEmpty() ? null : ids.getFirst();
    }

    /**
     * Ends a turn that is over (with the grace for the writer's last save) and gives the pen to somebody when nobody holds it.
     */
    private Relay tick(Relay r) {
        if (!r.status().equals("RUNNING")) return r;
        Instant now = clock.instant();
        if (r.writer() != null && r.turnEnds() != null && !now.isBefore(r.turnEnds().plus(GRACE)))
            return endTurn(r, "TIMEOUT");
        if (r.writer() == null) {
            nextTurn(r);
            return load(r.id());
        }
        return r;
    }

    /**
     * Closes the current turn with its outcome: DONE / TEACHER_DONE move the step on and grow the streak; PASS / TIMEOUT
     * keep the step for the next student and drop the streak; TEACHER_SKIP and STOPPED change neither. Then the next turn.
     */
    private Relay endTurn(Relay r, String outcome) {
        Instant now = clock.instant();
        int step = r.step(), streak = r.streak(), skips = r.skips();
        var credited = new TreeSet<>(r.credited());
        switch (outcome) {
            case "DONE" -> {
                int done = Math.max(r.step() + 1, doneSteps(r.task(), r.code(), credited));
                streak += done - step;
                step = done;
            }
            case "TEACHER_DONE" -> {
                credited.add(step);
                step = Math.max(step + 1, doneSteps(r.task(), r.code(), credited));
                streak++;
            }
            case "PASS", "TIMEOUT" -> {
                streak = 0;
                skips++;
            }
            default -> {
            }
        }
        if (r.writer() != null)
            db.update("update relay_turns set ended_at=?, outcome=?, code_after=? where relay_id=? and turn_no=? and ended_at is null", now.toString(), outcome, r.code(), r.id(), r.turnNo());
        boolean solved = step >= r.task().steps().size();
        db.update("update relays set step=?, streak=?, best_streak=max(best_streak,?), skips=?, credited=?, writer_id=null, turn_ends_at=null, status=? where id=?",
                  step, streak, streak, skips, String.join(",", credited.stream().map(String::valueOf).toList()), solved ? "SOLVED" : r.status(), r.id());
        log.info("Relay {} turn {} of user {}: {} (step {} → {}, streak {})", r.id(), r.turnNo(), r.writer(), outcome, r.step(), step, streak);
        var after = load(r.id());
        if (solved) {
            startRun(after);
            return load(r.id());
        }
        if (after.status().equals("RUNNING")) nextTurn(after, r.writer());
        return load(r.id());
    }

    /**
     * Nobody holds the pen (all had left, or after a pause): it goes on after the last writer.
     */
    private void nextTurn(Relay r) {
        var last = db.queryForList("select user_id from relay_turns where relay_id=? order by turn_no desc limit 1", Long.class, r.id());
        nextTurn(r, last.isEmpty() ? null : last.getFirst());
    }

    // ---------------------------------------------------------------- the final run

    /**
     * The pen goes to the first present member after «after» in the queue (the queue is a circle); nobody present — nobody holds it.
     */
    private void nextTurn(Relay r, Long after) {
        var members = members(r.id());
        var present = members.stream().filter(m -> m.present(clock.instant())).toList();
        if (present.isEmpty()) {
            db.update("update relays set writer_id=null, turn_ends_at=null where id=?", r.id());
            return;
        }
        int from = after == null ? -1 : members.stream().filter(m -> m.userId() == after).findFirst().map(Member::position).orElse(-1);
        var next = present.stream().filter(m -> m.position() > from).findFirst().orElse(present.getFirst());
        Instant now = clock.instant();
        int turn = r.turnNo() + 1;
        db.update("update relays set writer_id=?, turn_no=?, turn_started_at=?, turn_ends_at=? where id=?",
                  next.userId(), turn, now.toString(), now.plusSeconds(r.turnSeconds()).toString(), r.id());
        db.update("insert into relay_turns(relay_id,turn_no,user_id,step,started_at,code_before) values(?,?,?,?,?,?)", r.id(), turn, next.userId(), r.step(), now.toString(), r.code());
    }

    // ---------------------------------------------------------------- teacher

    private List<Member> members(long relay) {
        return db.query("select m.user_id, coalesce(u.display_name,u.login), m.position, m.last_seen_at from relay_members m join users u on u.id=m.user_id where m.relay_id=? order by m.position",
                        (rs, i) -> new Member(rs.getLong(1), rs.getString(2), rs.getInt(3), Instant.parse(rs.getString(4))), relay);
    }

    /**
     * Runs the code on Piston in the background (the run takes seconds and must not hold the lock); run_json is PENDING meanwhile.
     */
    private void startRun(Relay r) {
        db.update("update relays set run_json=? where id=?", write(obj("status", "PENDING")), r.id());
        String code = r.code();
        Language language = r.language();
        String expected = r.task().expectedOutput();
        long id = r.id();
        background.submit(() -> {
            Map<String, Object> result;
            try {
                var console = runner.console(language, code);
                result = console.view();
                result.put("matches", "OK".equals(console.status()) && console.stdout() != null && console.stdout().strip().equals(expected.strip()));
            } catch (RuntimeException e) {
                log.warn("Relay {} run failed: {}", id, e.toString());
                result = obj("status", "UNAVAILABLE", "stdout", "", "error", "Запуск сейчас недоступен.", "matches", false);
            }
            result.put("at", clock.instant().toString());
            synchronized (this) {
                db.update("update relays set run_json=? where id=?", write(result), id);
            }
        });
    }

    synchronized Map<String, Object> create(long admin, Map<String, Object> body) {
        String group = string(body, "group");
        if (group == null) throw new ApiError("RELAY_NO_GROUP", "Выбери группу");
        Task task = task(string(body, "taskKey"));
        int seconds = body.get("turnSeconds") instanceof Number n ? n.intValue() : DEFAULT_TURN;
        if (seconds < MIN_TURN || seconds > MAX_TURN)
            throw new ApiError("RELAY_TURN_SECONDS", "Время хода — от " + MIN_TURN + " до " + MAX_TURN + " секунд");
        Long active = activeOf(group);
        if (active != null) throw new ApiError("RELAY_ALREADY_ACTIVE", "У группы уже идёт эстафета — заверши её");
        long id = db.queryForObject("insert into relays(group_name,language,task_key,turn_seconds,status,code,created_by,created_at) values(?,?,?,?, 'LOBBY',?,?,?) returning id", Long.class,
                                    group, task.language().name(), task.key(), seconds, task.starter(), admin, clock.instant().toString());
        log.info("Relay {} «{}» for group {} created by admin {}", id, task.key(), group, admin);
        return adminView(load(id));
    }

    synchronized Map<String, Object> admin(Long id, String group) {
        Long relay = id != null ? id : group == null ? null : activeOf(group);
        return relay == null ? null : adminView(tick(load(relay)));
    }

    synchronized Map<String, Object> act(long id, String action) {
        var r = tick(load(id));
        Instant now = clock.instant();
        switch (action) {
            case "start" -> {
                if (!r.status().equals("LOBBY")) throw new ApiError("RELAY_STARTED", "Эстафета уже идёт");
                var members = new ArrayList<>(members(id));
                Collections.shuffle(members, random);
                for (int i = 0; i < members.size(); i++)
                    db.update("update relay_members set position=? where relay_id=? and user_id=?", i, id, members.get(i).userId());
                db.update("update relays set status='RUNNING', started_at=? where id=?", now.toString(), id);
                nextTurn(load(id), null);
            }
            case "pause" -> {
                if (!r.status().equals("RUNNING")) throw new ApiError("RELAY_NOT_RUNNING", "Эстафета не идёт");
                Long left = r.turnEnds() == null ? null : Math.max(0, Duration.between(now, r.turnEnds()).toMillis());
                db.update("update relays set status='PAUSED', paused_left_ms=?, turn_ends_at=null where id=?", left, id);
            }
            case "resume" -> {
                if (!r.status().equals("PAUSED")) throw new ApiError("RELAY_NOT_PAUSED", "Эстафета не на паузе");
                String ends = r.writer() == null || r.pausedLeftMs() == null ? null : now.plusMillis(Math.max(r.pausedLeftMs(), 3_000)).toString();
                db.update("update relays set status='RUNNING', paused_left_ms=null, turn_ends_at=? where id=?", ends, id);
            }
            case "extend" -> {
                if (r.status().equals("RUNNING") && r.turnEnds() != null)
                    db.update("update relays set turn_ends_at=? where id=?", r.turnEnds().plusSeconds(EXTEND).toString(), id);
                else if (r.status().equals("PAUSED") && r.pausedLeftMs() != null)
                    db.update("update relays set paused_left_ms=? where id=?", r.pausedLeftMs() + EXTEND * 1000L, id);
            }
            case "credit" -> {
                requireTurn(r);
                endTurn(r, "TEACHER_DONE");
            }
            case "skip" -> {
                requireTurn(r);
                endTurn(r, "TEACHER_SKIP");
            }
            case "restore" -> {
                if (r.turnNo() == 0) throw new ApiError("RELAY_NO_TURN", "Ещё не было ни одного хода");
                String before = db.queryForObject("select code_before from relay_turns where relay_id=? and turn_no=?", String.class, id, r.turnNo());
                db.update("update relays set code=?, version=version+1 where id=?", before, id);
            }
            case "run" -> {
                if (r.runJson() != null && r.runJson().contains("\"PENDING\"")) break;
                startRun(r);
            }
            case "finish" -> {
                if (r.status().equals("FINISHED")) break;
                if (r.writer() != null)
                    db.update("update relay_turns set ended_at=?, outcome='STOPPED', code_after=? where relay_id=? and turn_no=? and ended_at is null", now.toString(), r.code(), id, r.turnNo());
                db.update("update relays set status='FINISHED', writer_id=null, turn_ends_at=null, finished_at=?, on_board=0 where id=?", now.toString(), id);
            }
            case "board" -> {
                if (r.status().equals("FINISHED")) throw new ApiError("RELAY_FINISHED", "Эстафета уже закончилась");
                db.update("update relays set on_board=(id=?) where on_board=1 or id=?", id, id);
            }
            case "unboard" -> db.update("update relays set on_board=0 where id=?", id);
            default -> throw new NotFoundError("RELAY_UNKNOWN_ACTION", "Неизвестное действие");
        }
        log.info("Relay {}: {} by the teacher", id, action);
        return adminView(tick(load(id)));
    }

    // ---------------------------------------------------------------- students

    List<String> groups() {
        return db.queryForList("select distinct group_name from users where role='STUDENT' and group_name is not null and group_name<>'' order by group_name", String.class);
    }

    /**
     * The relay of the student's group (or null), noting that he is here when he is in it.
     */
    synchronized Map<String, Object> mine(long user) {
        String group = db.queryForObject("select group_name from users where id=?", String.class, user);
        Long id = group == null ? null : activeOf(group);
        if (id == null) return obj("relay", null);
        seen(id, user);
        return obj("relay", studentView(tick(load(id)), user));
    }

    synchronized Map<String, Object> join(long user, long id) {
        var r = load(id);
        String group = db.queryForObject("select group_name from users where id=?", String.class, user);
        if (!r.group().equals(group) || r.status().equals("FINISHED"))
            throw new ApiError("RELAY_NOT_YOURS", "Эта эстафета не для твоей группы или уже закончилась");
        String now = clock.instant().toString();
        db.update("insert into relay_members(relay_id,user_id,position,joined_at,last_seen_at) values(?,?,(select coalesce(max(position),-1)+1 from relay_members where relay_id=?),?,?) on conflict do nothing",
                  id, user, id, now, now);
        seen(id, user);
        return studentView(tick(load(id)), user);
    }

    /**
     * PUT /api/relay/{id}/code: the writer's text; when it completes the step, the turn ends at once.
     */
    synchronized Map<String, Object> code(long user, long id, Map<String, Object> body) {
        var r = tick(load(id));
        if (!(body.get("code") instanceof String code) || code.length() > MAX_CODE)
            throw new ApiError("RELAY_BAD_CODE", "Код — строка до " + MAX_CODE + " символов");
        requireWriter(r, user, body);
        seen(id, user);
        db.update("update relays set code=?, version=version+1 where id=?", code, id);
        r = load(id);
        if (doneSteps(r.task(), code, r.credited()) > r.step()) r = endTurn(r, "DONE");
        return studentView(r, user);
    }

    synchronized Map<String, Object> pass(long user, long id, Map<String, Object> body) {
        var r = tick(load(id));
        requireWriter(r, user, body);
        return studentView(endTurn(r, "PASS"), user);
    }

    private void seen(long relay, long user) {
        Instant now = clock.instant();
        db.update("update relay_members set last_seen_at=? where relay_id=? and user_id=? and last_seen_at<?", now.toString(), relay, user, now.minus(SEEN_EVERY).toString());
    }

    // ---------------------------------------------------------------- the projector

    /**
     * The relay the teacher put on the board (at most one, of any group), as everybody sees it; null when none.
     */
    synchronized Map<String, Object> onBoard() {
        var ids = db.queryForList("select id from relays where on_board=1 and status<>'FINISHED' and created_at>? order by id desc limit 1", Long.class,
                                  clock.instant().minus(ACTIVE_FOR).toString());
        return ids.isEmpty() ? null : publicView(tick(load(ids.getFirst())));
    }

    // ---------------------------------------------------------------- views

    /**
     * What everybody sees: the code, the step, who writes, the queue, the streak; never the reference.
     */
    private Map<String, Object> publicView(Relay r) {
        var members = members(r.id());
        Instant now = clock.instant();
        var steps = r.task().steps();
        Integer record = db.queryForObject("select max(best_streak) from relays where group_name=?", Integer.class, r.group());
        var queue = new ArrayList<Map<String, Object>>();
        int from = r.writer() == null ? -1 : members.stream().filter(m -> m.userId() == r.writer()).findFirst().map(Member::position).orElse(-1);
        var ordered = new ArrayList<Member>();
        members.stream().filter(m -> m.position() > from).forEach(ordered::add);
        members.stream().filter(m -> m.position() <= from).forEach(ordered::add);
        for (var m : ordered)
            if (r.writer() == null || m.userId() != r.writer())
                queue.add(obj("userId", m.userId(), "name", m.name(), "present", m.present(now)));
        var writer = r.writer() == null ? null : members.stream().filter(m -> m.userId() == r.writer()).findFirst().map(m -> obj("userId", m.userId(), "name", m.name())).orElse(null);
        var last = db.queryForList("select t.outcome, t.step, t.ended_at, coalesce(u.display_name,u.login) as name from relay_turns t join users u on u.id=t.user_id where t.relay_id=? and t.outcome is not null order by t.turn_no desc limit 1", r.id());
        return obj("id", r.id(), "group", r.group(), "language", r.language().name(), "status", r.status(), "task", r.task().view(),
                   "code", r.code(), "version", r.version(), "step", r.step(), "steps", steps.size(),
                   "stepPrompt", r.step() < steps.size() ? steps.get(r.step()).prompt() : null,
                   "nextPrompt", r.step() + 1 < steps.size() ? steps.get(r.step() + 1).prompt() : null,
                   "donePrompts", steps.subList(0, Math.min(r.step(), steps.size())).stream().map(Step::prompt).toList(),
                   "turn", r.turnNo(), "turnSeconds", r.turnSeconds(), "writer", writer,
                   "turnEndsAt", r.turnEnds() == null ? null : r.turnEnds().toString(), "pausedLeftMs", r.pausedLeftMs(),
                   "queue", queue, "members", members.size(),
                   "streak", r.streak(), "bestStreak", r.bestStreak(), "record", record == null ? 0 : record, "skips", r.skips(),
                   "lastTurn", last.isEmpty() ? null : obj("outcome", last.getFirst().get("outcome"), "step", last.getFirst().get("step"), "at", last.getFirst().get("ended_at"), "name", last.getFirst().get("name")),
                   "run", r.runJson() == null ? null : read(r.runJson()), "now", now.toString());
    }

    private Map<String, Object> studentView(Relay r, long user) {
        var view = publicView(r);
        var members = members(r.id());
        boolean member = members.stream().anyMatch(m -> m.userId() == user);
        @SuppressWarnings("unchecked") var queue = (List<Map<String, Object>>) view.get("queue");
        int ahead = -1;
        if (member && (r.writer() == null || r.writer() != user)) {
            int k = 0;
            for (var q : queue) {
                if (((Number) q.get("userId")).longValue() == user) {
                    ahead = k;
                    break;
                }
                if (Boolean.TRUE.equals(q.get("present"))) k++;
            }
        }
        view.put("me", obj("userId", user, "member", member, "writing", r.writer() != null && r.writer() == user && r.status().equals("RUNNING"), "turnsAhead", ahead));
        return view;
    }

    /**
     * The teacher's view: the public one plus the reference of the step, the members and the log of turns.
     */
    private Map<String, Object> adminView(Relay r) {
        var view = publicView(r);
        var steps = r.task().steps();
        Instant now = clock.instant();
        view.put("hint", r.step() < steps.size() ? steps.get(r.step()).hint() : null);
        view.put("reference", r.step() < steps.size() ? steps.get(r.step()).code() : steps.getLast().code());
        view.put("credited", r.credited());
        view.put("onBoard", r.onBoard());
        var stats = new HashMap<Long, int[]>();
        db.query("select user_id, outcome from relay_turns where relay_id=? and outcome is not null", rs -> {
            int[] s = stats.computeIfAbsent(rs.getLong(1), k -> new int[3]);
            switch (rs.getString(2)) {
                case "DONE", "TEACHER_DONE" -> s[0]++;
                case "PASS", "TIMEOUT" -> s[1]++;
                default -> s[2]++;
            }
        }, r.id());
        view.put("people", members(r.id()).stream().map(m -> {
            int[] s = stats.getOrDefault(m.userId(), new int[3]);
            return obj("userId", m.userId(), "name", m.name(), "present", m.present(now), "done", s[0], "skipped", s[1], "other", s[2]);
        }).toList());
        view.put("log", db.queryForList("select t.turn_no as turn, t.step, t.outcome, t.started_at as startedAt, t.ended_at as endedAt, coalesce(u.display_name,u.login) as name from relay_turns t join users u on u.id=t.user_id where t.relay_id=? order by t.turn_no desc limit 60", r.id()));
        return view;
    }

    // ---------------------------------------------------------------- helpers

    private String write(Object value) {
        try {
            return json.writeValueAsString(value);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    private Object read(String value) {
        try {
            return json.readValue(value, Map.class);
        } catch (IOException e) {
            return null;
        }
    }

    record Step(String prompt, List<Pattern> checks, String hint, String code) {
    }

    record Task(
            String key, Language language, String title, String statement, String starter, String expectedOutput,
            List<Step> steps
    ) {
        Map<String, Object> view() {
            return obj("key", key, "language", language.name(), "title", title, "statement", statement, "steps", steps.size());
        }
    }

    private record Relay(
            long id, String group, Language language, Task task, int turnSeconds, String status, String code,
            long version, int step,
            int turnNo, Long writer, Instant turnStarted, Instant turnEnds, Long pausedLeftMs, int streak,
            int bestStreak, int skips,
            Set<Integer> credited, String runJson, Instant createdAt, Instant startedAt, boolean onBoard
    ) {
    }

    private record Member(long userId, String name, int position, Instant lastSeen) {
        boolean present(Instant now) {
            return lastSeen.isAfter(now.minus(PRESENT));
        }
    }
}
