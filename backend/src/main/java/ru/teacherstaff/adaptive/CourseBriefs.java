package ru.teacherstaff.adaptive;

import org.springframework.jdbc.core.JdbcTemplate;
import java.util.List;

/** Course context for the generator: the topic, what the student studied before, its diagnostic questions and existing tasks. */
final class CourseBriefs {
  private CourseBriefs() {}

  static ContentBrief brief(JdbcTemplate db,Long userId,String skillCode,int difficulty,String explanation) { return brief(db,userId,skillCode,difficulty,explanation,false); }
  /** hard: an algorithmic task for hard mode; it is compared only with other hard tasks of the topic. */
  static ContentBrief brief(JdbcTemplate db,Long userId,String skillCode,int difficulty,String explanation,boolean hard) {
    var skill=db.queryForMap("select title,block_no,sort_order,language from skills where code=?",skillCode);
    Language lang=Language.of(skill.get("language"));
    var earlier=db.queryForList("select code,title from skills where language=? and sort_order<? order by sort_order",lang.name(),((Number)skill.get("sort_order")).intValue()).stream().map(x->x.get("code").equals(x.get("title"))?(String)x.get("code"):x.get("code")+" — "+x.get("title")).toList();
    var examples=db.queryForList("select prompt from diagnostic_questions where skill_code=? order by ordinal limit 4",String.class,skillCode);
    var existing=db.queryForList("select t.title,t.difficulty,t.statement from tasks t join task_target_skills ts on ts.task_id=t.id where t.active=1 and ts.skill_code=? and t.mode=? order by t.id desc limit 12",skillCode,hard?"HARD":"NORMAL").stream().map(x->x.get("title")+" (уровень "+(x.get("difficulty")==null?"?":x.get("difficulty"))+"): "+abbreviate((String)x.get("statement"),240)).toList();
    var iteration=userId==null?List.<Integer>of():db.queryForList("select completed_iterations from student_skills where user_id=? and skill_code=?",Integer.class,userId,skillCode);
    return new ContentBrief(lang,skillCode,(String)skill.get("title"),((Number)skill.get("block_no")).intValue(),difficulty,Math.min(3,(iteration.isEmpty()?0:iteration.getFirst())+1),earlier,examples,existing,explanation,hard);
  }
  private static String abbreviate(String value,int max) { String flat=value.replaceAll("\\s+"," ").strip(); return flat.length()<=max?flat:flat.substring(0,max)+"…"; }
}
