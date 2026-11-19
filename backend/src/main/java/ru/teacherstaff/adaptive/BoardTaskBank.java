package ru.teacherstaff.adaptive;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/** Teacher-initiated search includes archived tasks and every practice mode. */
final class BoardTaskBank {
    record Entry(long id, String title, String statement, String topic, String mode, boolean active) {}
    record Page(List<Entry> tasks, int total) {}
    static final int PAGE_SIZE = 20;

    static Page search(JdbcTemplate db, Language language, String query, int offset) {
        if (offset < 0 || query.length() > 200) throw new ApiError("INVALID_SEARCH", "Некорректные параметры поиска");
        String term = query.strip().toLowerCase(Locale.ROOT);
        var tasks = new ArrayList<Entry>();
        int[] total = {0};
        // SQLite's built-in lower() folds ASCII only. Match Russian titles and statements as well.
        db.query("""
                select t.id,t.title,t.statement,s.title,t.mode,t.active from tasks t
                join skills s on s.code=t.skill_code where t.language=? order by t.id desc
                """, (RowCallbackHandler) rs -> {
            long id = rs.getLong(1);
            String title = rs.getString(2), statement = rs.getString(3), topic = rs.getString(4);
            if (!term.isEmpty() && !Long.toString(id).equals(term) &&
                    !(title + "\n" + statement + "\n" + topic).toLowerCase(Locale.ROOT).contains(term)) return;
            if (total[0]++ >= offset && tasks.size() < PAGE_SIZE)
                tasks.add(new Entry(id, title, statement, topic, rs.getString(5), rs.getBoolean(6)));
        }, language.name());
        return new Page(tasks, total[0]);
    }

    static Map<String, Object> item(JdbcTemplate db, Language language, long taskId) {
        var rows = db.queryForList("""
                select t.id as taskId,t.title,t.statement,t.language,t.starter_code as starterCode,
                       t.external_key as externalKey,t.reference_code as reference,t.skill_code as skillCode,
                       s.title as skillTitle,t.difficulty,'code' as kind,1 as bankTask
                from tasks t join skills s on s.code=t.skill_code where t.id=? and t.language=?
                """, taskId, language.name());
        if (rows.isEmpty()) throw new NotFoundError("TASK_NOT_FOUND", "Задача не найдена в банке выбранного курса");
        return rows.getFirst();
    }
}
