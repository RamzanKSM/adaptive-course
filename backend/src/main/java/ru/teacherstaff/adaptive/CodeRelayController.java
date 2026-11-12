package ru.teacherstaff.adaptive;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * «Эстафета» (CodeRelay): the teacher's /api/admin/relay…, the student's /api/relay… (the board station gets its relay in /api/station/current)
 * (authenticated by the station cookie, AuthFilter).
 */
@RestController
@RequestMapping("/api")
class CodeRelayController {
    private final CodeRelay relay;

    CodeRelayController(CodeRelay relay) {
        this.relay = relay;
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> user(HttpServletRequest r) {
        return (Map<String, Object>) r.getAttribute("user");
    }

    private static long admin(HttpServletRequest r) {
        var u = user(r);
        if (u == null || !"ADMIN".equals(u.get("role"))) throw new ApiError("FORBIDDEN", "Нужна роль ADMIN");
        return ((Number) u.get("id")).longValue();
    }

    private static long student(HttpServletRequest r) {
        var u = user(r);
        if (u == null || !"STUDENT".equals(u.get("role")))
            throw new ApiError("RELAY_STUDENTS_ONLY", "Эстафета — для студентов");
        return ((Number) u.get("id")).longValue();
    }

    /**
     * The tasks, the groups, and the group's relay that is not finished (or the relay by id).
     */
    @GetMapping("/admin/relay")
    Map<String, Object> admin(@RequestParam(required = false) String group, @RequestParam(required = false) Long id, HttpServletRequest r) {
        admin(r);
        return CodeRelay.obj("tasks", relay.tasks().stream().map(CodeRelay.Task::view).toList(), "groups", relay.groups(), "relay", relay.admin(id, group));
    }

    @PostMapping("/admin/relay")
    Map<String, Object> create(@RequestBody(required = false) Map<String, Object> b, HttpServletRequest r) {
        return relay.create(admin(r), b == null ? Map.of() : b);
    }

    @PostMapping("/admin/relay/{id}/{action}")
    Map<String, Object> act(@PathVariable long id, @PathVariable String action, HttpServletRequest r) {
        admin(r);
        return relay.act(id, action);
    }

    /**
     * The student's relay; for the teacher only his role (the page shows him the way to his console).
     */
    @GetMapping("/relay/me")
    Map<String, Object> mine(HttpServletRequest r) {
        var u = user(r);
        if (u != null && "ADMIN".equals(u.get("role"))) return CodeRelay.obj("role", "ADMIN", "relay", null);
        var view = relay.mine(student(r));
        view.put("role", "STUDENT");
        return view;
    }

    @PostMapping("/relay/{id}/join")
    Map<String, Object> join(@PathVariable long id, HttpServletRequest r) {
        return relay.join(student(r), id);
    }

    @PutMapping("/relay/{id}/code")
    Map<String, Object> code(@PathVariable long id, @RequestBody(required = false) Map<String, Object> b, HttpServletRequest r) {
        return relay.code(student(r), id, b == null ? Map.of() : b);
    }

    @PostMapping("/relay/{id}/pass")
    Map<String, Object> pass(@PathVariable long id, @RequestBody(required = false) Map<String, Object> b, HttpServletRequest r) {
        return relay.pass(student(r), id, b == null ? Map.of() : b);
    }
}
