package ru.teacherstaff.adaptive;

import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import java.time.Clock;
import java.util.*;

/**
 * «Снять освоение» (owner, 2026-11-03): the teacher decides a student has not really learned a closed topic, and the topic
 * starts over: iterations 3 + 2 + 1 in the coming lessons, as a topic never practised. A topic confirmed by the diagnostic
 * loses the confirmation too. Solved tasks, credits, the pair's points and grades stay; the old solutions no longer count
 * for this topic (topic_reopens.last_submission_id: ApiController.replayProgress, ProgressAnalytics, IterationHistoryRestore).
 * <p>Unlike a re-take (TopicRetakes), which is the student's choice and never moves progress, this changes what the lessons
 * give. An open re-take of the topic ends. Rules: backend/README.md, «Снять освоение».
 */
@RestController
@RequestMapping("/api")
class TopicReopens {
    /**
     * topic_retakes.finish_reason of a re-take ended because its topic was reopened.
     */
    static final String REOPENED = "REOPENED";
    private static final Logger log = LoggerFactory.getLogger(TopicReopens.class);
    private final JdbcTemplate db;
    private final Clock clock;
    private final TopicRetakes retakes;

    TopicReopens(JdbcTemplate db, Clock clock, TopicRetakes retakes) {
        this.db = db;
        this.clock = clock;
        this.retakes = retakes;
    }

    @SuppressWarnings("unchecked")
    private static long admin(HttpServletRequest r) {
        var u = (Map<String, Object>) r.getAttribute("user");
        if (u == null || !"ADMIN".equals(u.get("role"))) throw new ApiError("FORBIDDEN", "Нужна роль ADMIN");
        return ((Number) u.get("id")).longValue();
    }

    @PostMapping("/admin/students/{id}/topics/{skill}/reopen")
    @Transactional
    Map<String, Object> reopen(@PathVariable long id, @PathVariable String skill, HttpServletRequest r) {
        long admin = admin(r);
        if (count("select count(*) from users where id=? and role='STUDENT'", id) == 0)
            throw new ApiError("STUDENT_NOT_FOUND", "Студент не найден");
        if (!retakes.closed(id, skill)) throw new ApiError("TOPIC_NOT_CLOSED", "Эта тема у студента не закрыта");
        var progress = db.queryForList("select completed_iterations,iteration_successes,first_iteration_lesson_number,mastered from student_skills where user_id=? and skill_code=?", id, skill);
        var before = progress.isEmpty() ? null : progress.getFirst();
        long lastSubmission = db.queryForObject("select coalesce(max(s.id),0) from submissions s join lessons l on l.id=s.lesson_id where l.user_id=?", Long.class, id);
        int confirmed = count("select count(*) from diagnostic_skill_results where user_id=? and skill_code=? and confirmed=1", id, skill);
        db.update("insert into topic_reopens(user_id,skill_code,reopened_at,reopened_by,last_submission_id,was_completed,was_successes,was_first_lesson,was_mastered,was_confirmed) values(?,?,?,?,?,?,?,?,?,?)",
                  id, skill, clock.instant().toString(), admin, lastSubmission, before == null ? 0 : before.get("completed_iterations"), before == null ? 0 : before.get("iteration_successes"),
                  before == null ? null : before.get("first_iteration_lesson_number"), before == null ? 0 : before.get("mastered"), confirmed);
        db.update("delete from skill_iterations where user_id=? and skill_code=?", id, skill);
        db.update("update student_skills set completed_iterations=0,iteration_successes=0,first_iteration_lesson_number=null,mastered=0 where user_id=? and skill_code=?", id, skill);
        db.update("update diagnostic_skill_results set confirmed=0 where user_id=? and skill_code=?", id, skill);
        for (long retake : db.queryForList("select id from topic_retakes where user_id=? and skill_code=? and kind=? and finished_at is null", Long.class, id, skill, TopicRetakes.TOPIC))
            retakes.finish(retake, REOPENED);
        log.info("Topic {} of student {} reopened by admin {} (was: {} iterations, mastered={}, confirmed={})", skill, id, admin, before == null ? 0 : before.get("completed_iterations"), before == null ? 0 : before.get("mastered"), confirmed);
        return Map.of("skillCode", skill);
    }

    private int count(String sql, Object... args) {
        Integer n = db.queryForObject(sql, Integer.class, args);
        return n == null ? 0 : n;
    }
}
