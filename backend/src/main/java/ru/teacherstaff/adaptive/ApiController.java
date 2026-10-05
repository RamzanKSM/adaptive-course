package ru.teacherstaff.adaptive;

import jakarta.servlet.http.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.transaction.annotation.Transactional;
import java.security.SecureRandom;
import java.time.*;
import java.util.*;

@RestController @RequestMapping("/api")
public class ApiController {
  private static final org.slf4j.Logger log=org.slf4j.LoggerFactory.getLogger(ApiController.class);
  private final JdbcTemplate db; private final PistonCodeRunner codeRunner; private final LlmTutor tutor; private final LearningContentGenerator contentGenerator; private final BCryptPasswordEncoder passwords=new BCryptPasswordEncoder();
  @Value("${app.session-hours}") long sessionHours; @Value("${app.cookie-secure}") boolean secureCookie; @Value("${app.piston.base-url}") String pistonUrl;
  ApiController(JdbcTemplate db, PistonCodeRunner codeRunner, LlmTutor tutor, LearningContentGenerator contentGenerator) { this.db=db; this.codeRunner=codeRunner; this.tutor=tutor; this.contentGenerator=contentGenerator; }
  @PostMapping("/auth/login") public Map<String,Object> login(@RequestBody Map<String,String> body, HttpServletResponse response) {
    var rows=db.queryForList("select id,login,password_hash,role,display_name,llm_enabled from users where login=?",body.get("login"));
    if(rows.isEmpty() || !passwords.matches(body.getOrDefault("password",""),(String)rows.getFirst().get("password_hash"))) throw bad("INVALID_CREDENTIALS","Неверный логин или пароль");
    var u=rows.getFirst(); String token=randomToken(); db.update("insert into sessions(token_hash,user_id,expires_at) values(?,?,?)",Hashing.sha256(token),u.get("id"),Instant.now().plus(Duration.ofHours(sessionHours)).toString());
    Cookie c=new Cookie("adaptive_session",token); c.setHttpOnly(true); c.setPath("/api"); c.setMaxAge((int)Duration.ofHours(sessionHours).toSeconds()); c.setSecure(secureCookie); response.addCookie(c); return status(u);
  }
  @PostMapping("/auth/logout") @ResponseStatus(HttpStatus.NO_CONTENT) public void logout(HttpServletRequest r,HttpServletResponse p) { cookie(r).ifPresent(t->db.update("delete from sessions where token_hash=?",Hashing.sha256(t))); Cookie c=new Cookie("adaptive_session","");c.setPath("/api");c.setMaxAge(0);p.addCookie(c); }
  @GetMapping("/auth/me") public Map<String,Object> me(HttpServletRequest r) { return status(user(r)); }

  @GetMapping("/diagnostic") public Map<String,Object> diagnostic(@RequestParam(name="language",required=false) String language,HttpServletRequest r) { long id=uid(r); Language lang=Language.parse(language); boolean done=diagnosticDone(id,lang); var qs=db.queryForList("select id,ordinal,skill_code,prompt,options_json from diagnostic_questions where language=? order by ordinal",lang.name()); return Map.of("completed",done,"questions",done?List.of():qs.stream().map(q->Map.of("id",q.get("id"),"ordinal",q.get("ordinal"),"skillCode",q.get("skill_code"),"prompt",q.get("prompt"),"options",json(q.get("options_json")),"unknownOption",Map.of("label","Не знаю"))).toList()); }
  @PostMapping("/diagnostic") @Transactional public Map<String,Object> submitDiagnostic(@RequestBody Map<String,Object> body,@RequestParam(name="language",required=false) String language,HttpServletRequest r) { long user=student(r); Language lang=Language.parse(language); if(diagnosticDone(user,lang)) throw bad("DIAGNOSTIC_ALREADY_COMPLETED","Диагностика уже пройдена");
    @SuppressWarnings("unchecked") List<Map<String,Object>> answers=(List<Map<String,Object>>)body.get("answers"); if(answers==null || answers.size()!=count("select count(*) from diagnostic_questions where language=?",lang.name())) throw bad("INVALID_DIAGNOSTIC","Нужны ответы на все вопросы");
    Map<Long,Integer> received=new HashMap<>(); for(var a:answers) { long id=((Number)a.get("questionId")).longValue(); Integer choice=a.get("selectedOption")==null?null:((Number)a.get("selectedOption")).intValue(); if(choice!=null&&(choice<0||choice>3)||received.containsKey(id)) throw bad("INVALID_DIAGNOSTIC","Ответы должны быть уникальны и иметь допустимый вариант"); received.put(id,choice); }
    var qs=db.queryForList("select id,correct_option,block_no from diagnostic_questions where language=?",lang.name()); Map<Integer,int[]> score=new HashMap<>(); for(var q:qs){long qid=((Number)q.get("id")).longValue(); Integer selected=received.get(qid); if(!received.containsKey(qid))throw bad("INVALID_DIAGNOSTIC","Есть неизвестный вопрос"); boolean ok=selected!=null&&selected.equals(((Number)q.get("correct_option")).intValue()); db.update("insert into diagnostic_answers(user_id,question_id,selected_option,is_correct) values(?,?,?,?)",user,qid,selected,ok?1:0); int[] s=score.computeIfAbsent(((Number)q.get("block_no")).intValue(),x->new int[2]);s[1]++;if(ok)s[0]++;}
    int start=score.keySet().stream().sorted().filter(b->score.get(b)[0]*100<score.get(b)[1]*80).findFirst().orElse(score.keySet().stream().max(Integer::compare).orElse(0)); db.update("insert into student_languages(user_id,language,diagnostic_completed_at,starting_block) values(?,?,?,?) on conflict(user_id,language) do update set diagnostic_completed_at=excluded.diagnostic_completed_at,starting_block=excluded.starting_block",user,lang.name(),Instant.now().toString(),start); return Map.of("completed",true,"startingBlock",start); }

  @GetMapping("/lessons/current") public Map<String,Object> current(@RequestParam(name="language",required=false) String language,HttpServletRequest r){return obj("lesson",active(uid(r),Language.parse(language)));}
  @PostMapping("/lessons/start") public Map<String,Object> start(@RequestParam(name="language",required=false) String language,HttpServletRequest r){long u=student(r);Language lang=Language.parse(language);requireDiagnostic(u,lang);var current=active(u,lang);if(current!=null)return Map.of("lesson",current);int n=count("select coalesce(max(lesson_number),0) from lessons where user_id=?",u)+1;int inLanguage=count("select count(*) from lessons where user_id=? and language=?",u,lang.name())+1;db.update("insert into lessons(user_id,lesson_number,language,language_lesson_number) values(?,?,?,?)",u,n,lang.name(),inLanguage);return Map.of("lesson",active(u,lang));}
  @PostMapping("/lessons/{id}/finish") public Map<String,Object> finish(@PathVariable long id,HttpServletRequest r){long u=student(r);if(db.update("update lessons set finished_at=? where id=? and user_id=? and finished_at is null",Instant.now().toString(),id,u)==0)throw bad("LESSON_NOT_ACTIVE","Активный урок не найден");return Map.of("lesson",lesson(id));}
  @GetMapping("/learning/next") @Transactional public Map<String,Object> next(@RequestParam(name="language",required=false) String language,HttpServletRequest r) {
    long userId=student(r); Language lang=Language.parse(language); var lesson=active(userId,lang);
    if(lesson==null) throw bad("NO_ACTIVE_LESSON","Сначала начните урок");
    var assigned=unsolvedTask(lesson);
    if(assigned!=null) return learningResponse(userId,lesson,assigned);
    var skill=nextSkill(userId,lang,((Number)lesson.get("number")).intValue(),((Number)lesson.get("id")).longValue());
    if(skill==null) return obj("lesson",lesson,"skill",null,"explanation",null,"task",null,"reason","NO_DUE_SKILL","llm",llm(userId));
    String skillCode=(String)skill.get("code");
    long lessonId=((Number)lesson.get("id")).longValue();
    Object explanation=explanation(userId, skillCode);
    int difficulty=targetDifficulty(userId, lessonId, skillCode);
    var tasks=availableTasks(userId, lesson, skillCode, difficulty);
    if(!hasDifficulty(tasks, difficulty)) {
      // Generate the missing step of the easy→hard ladder; fall back to the nearest bank task when generation is impossible.
      String reason=null;
      if(!tutor.status(userId).available()) reason="NO_TASK_AVAILABLE";
      else if(!codeRunner.status(lang).available()) reason="RUNNER_UNAVAILABLE";
      else {
        boolean stored=false;
        var brief=brief(userId, skillCode, difficulty, explanation instanceof Map<?,?> m ? (String)m.get("content") : null);
        for(int attempt=1;attempt<=2&&!stored;attempt++) try {
          log.info("Generating task: skill={} language={} difficulty={} attempt={}/2",skillCode,lang,difficulty,attempt);
          long taskId=storeGeneratedTask(contentGenerator.generateTask(userId, brief), difficulty, lang);
          markTaskOutcome(userId,skillCode,"ACCEPTED");
          log.info("Generated task {} accepted for skill={} difficulty={}",taskId,skillCode,difficulty);
          stored=true;
        }
        catch (InvalidGeneratedContentException e) { markTaskOutcome(userId,skillCode,"REJECTED"); log.warn("Generated task rejected (skill={}, attempt {}/2): {}",skillCode,attempt,e.getMessage()); }
        catch (LlmUnavailableException e) { log.warn("Task generation unavailable for skill={}: {}",skillCode,e.getMessage()); reason="NO_TASK_AVAILABLE"; break; }
        if(!stored&&reason==null) reason="LLM_GENERATION_FAILED_VALIDATION";
        tasks=availableTasks(userId, lesson, skillCode, difficulty);
      }
      if(tasks.isEmpty()) return "RUNNER_UNAVAILABLE".equals(reason)
          ? obj("lesson",lesson,"skill",skill,"explanation",explanation,"task",null,"reason",reason,"llm",llm(userId),"runner",runner(lang))
          : obj("lesson",lesson,"skill",skill,"explanation",explanation,"task",null,"reason",reason==null?"NO_TASK_AVAILABLE":reason,"llm",llm(userId));
    }
    var task=tasks.getFirst(); db.update("insert into lesson_tasks(lesson_id,task_id) values(?,?)",lesson.get("id"),task.get("id"));
    return obj("lesson",lesson,"skill",skill,"explanation",explanation,"task",taskView(task));
  }
  private Map<String,Object> unsolvedTask(Map<String,Object> lesson) { var rows=db.queryForList("select t.id,t.title,t.statement,t.starter_code,ts.skill_code, s.title as skill_title,s.block_no from lesson_tasks lt join tasks t on t.id=lt.task_id join task_target_skills ts on ts.task_id=t.id join skills s on s.code=ts.skill_code where lt.lesson_id=? and t.active=1 and not exists(select 1 from submissions x where x.lesson_id=lt.lesson_id and x.task_id=lt.task_id and x.passed=1) order by lt.rowid desc limit 1",lesson.get("id"));return rows.isEmpty()?null:rows.getFirst(); }
  private Map<String,Object> learningResponse(long userId,Map<String,Object> lesson,Map<String,Object> task) { String skillCode=(String)task.get("skill_code");Object explanation=explanation(userId,skillCode);return obj("lesson",lesson,"skill",Map.of("code",skillCode,"title",task.get("skill_title"),"blockNo",task.get("block_no")),"explanation",explanation,"task",taskView(task)); }
  private Map<String,Object> taskView(Map<String,Object> task) { return Map.of("id",task.get("id"),"title",task.get("title"),"statement",task.get("statement"),"starterCode",task.get("starter_code")); }
  /** Unsolved bank tasks for the skill, the requested difficulty first, then the nearest one, legacy tasks without difficulty last. */
  private List<Map<String,Object>> availableTasks(long userId,Map<String,Object> lesson,String skillCode,int difficulty) {
    return db.queryForList("select t.id,t.title,t.statement,t.starter_code,t.difficulty from tasks t join task_target_skills ts on ts.task_id=t.id where t.active=1 and ts.skill_code=? and not exists(select 1 from successful_task_credit c where c.user_id=? and c.task_id=t.id) and not exists(select 1 from lesson_tasks x where x.lesson_id=? and x.task_id=t.id) and not exists(select 1 from task_prerequisite_skills req where req.task_id=t.id and not exists(select 1 from student_skills p where p.user_id=? and p.skill_code=req.skill_code and p.mastered=1)) order by t.difficulty is null, abs(t.difficulty-?), t.difficulty, t.id",skillCode,userId,lesson.get("id"),userId,difficulty);
  }
  private static boolean hasDifficulty(List<Map<String,Object>> tasks,int difficulty) { return !tasks.isEmpty() && tasks.getFirst().get("difficulty") instanceof Number d && d.intValue()==difficulty; }
  /** Step inside the current iteration: the n-th task of the skill solved in this lesson asks for difficulty n+1 (1..3). */
  private int targetDifficulty(long userId,long lessonId,String skillCode) { return Math.min(3, solvedInLesson(userId,lessonId,skillCode)+1); }
  private int solvedInLesson(long userId,long lessonId,String skillCode) { return count("select count(distinct c.task_id) from successful_task_credit c join task_target_skills ts on ts.task_id=c.task_id join submissions s on s.task_id=c.task_id and s.lesson_id=? and s.passed=1 where c.user_id=? and ts.skill_code=?",lessonId,userId,skillCode); }
  private ContentBrief brief(long userId,String skillCode,int difficulty,String explanation) {
    var skill=db.queryForMap("select title,block_no,sort_order,language from skills where code=?",skillCode);
    Language lang=Language.of(skill.get("language"));
    var earlier=db.queryForList("select code,title from skills where language=? and sort_order<? order by sort_order",lang.name(),((Number)skill.get("sort_order")).intValue()).stream().map(x->x.get("code").equals(x.get("title"))?(String)x.get("code"):x.get("code")+" — "+x.get("title")).toList();
    var examples=db.queryForList("select prompt from diagnostic_questions where skill_code=? order by ordinal limit 4",String.class,skillCode);
    var existing=db.queryForList("select t.title,t.difficulty,t.statement from tasks t join task_target_skills ts on ts.task_id=t.id where t.active=1 and ts.skill_code=? order by t.id desc limit 12",skillCode).stream().map(x->x.get("title")+" (уровень "+(x.get("difficulty")==null?"?":x.get("difficulty"))+"): "+abbreviate((String)x.get("statement"),240)).toList();
    var iteration=db.queryForList("select completed_iterations from student_skills where user_id=? and skill_code=?",Integer.class,userId,skillCode);
    return new ContentBrief(lang,skillCode,(String)skill.get("title"),((Number)skill.get("block_no")).intValue(),difficulty,Math.min(3,(iteration.isEmpty()?0:iteration.getFirst())+1),earlier,examples,existing,explanation);
  }
  private static String abbreviate(String value,int max) { String flat=value.replaceAll("\\s+"," ").strip(); return flat.length()<=max?flat:flat.substring(0,max)+"…"; }
  /** Cached explanation; LLM explanations from an older prompt version are regenerated when possible and kept otherwise. */
  private Object explanation(long studentId, String skillCode) {
    var rows=db.queryForList("select content,source,prompt_version from explanations where skill_code=?",skillCode);
    var cached=rows.isEmpty()?null:rows.getFirst();
    boolean stale=cached!=null&&"LLM".equals(cached.get("source"))&&((Number)cached.get("prompt_version")).intValue()<LearningContentGenerator.EXPLANATION_PROMPT_VERSION;
    if(cached!=null&&!stale) return Map.of("content",cached.get("content"),"source",cached.get("source"));
    var generated=generatedExplanation(studentId, skillCode);
    if(generated!=null) return generated;
    return cached==null?null:Map.of("content",cached.get("content"),"source",cached.get("source"));
  }
  private Map<String,Object> generatedExplanation(long studentId, String skillCode) {
    if(!tutor.status(studentId).available()) return null;
    return contentGenerator.generateExplanation(studentId, brief(studentId, skillCode, 1, null))
      .filter(ex -> skillCode.equals(ex.skillCode()) && ex.content()!=null && !ex.content().isBlank())
      .map(ex -> {
        db.update("insert into explanations(skill_code,content,source,prompt_version) values(?,?,'LLM',?) on conflict(skill_code) do update set content=excluded.content,source=excluded.source,prompt_version=excluded.prompt_version",skillCode,ex.content(),LearningContentGenerator.EXPLANATION_PROMPT_VERSION);
        return Map.<String,Object>of("content",ex.content(),"source","LLM");
      }).orElse(null);
  }
  /** Stores a generated task only after its reference solution passes its own checks; every rejection names the reason for the logs. */
  private long storeGeneratedTask(GeneratedTask task,int difficulty,Language lang) {
    if(task==null) throw rejected("empty response");
    if(blank(task.skillCode())||blank(task.title())||blank(task.statement())) throw rejected("missing skillCode, title or statement");
    if(blank(task.testSource())||!validHarness(lang,task.testSource())) throw rejected("test harness does not follow the "+lang.title+" contract");
    if(blank(task.testFileName())||blank(task.referenceSolutionSource())) throw rejected("missing testFileName or referenceSolutionSource");
    if(task.targetSkillCodes()==null||!task.targetSkillCodes().contains(task.skillCode())||task.prerequisiteSkillCodes()==null) throw rejected("targetSkillCodes must contain "+task.skillCode());
    if(count("select count(*) from skills where code=? and language=?",task.skillCode(),lang.name())==0) throw rejected("unknown "+lang.title+" skill "+task.skillCode());
    for(String target:task.targetSkillCodes()) if(count("select count(*) from skills where code=?",target)==0) throw rejected("unknown target skill "+target);
    for(String prerequisite:task.prerequisiteSkillCodes()) if(count("select count(*) from skills where code=?",prerequisite)==0) throw rejected("unknown prerequisite skill "+prerequisite);
    String leak=internalTerm(task.statement()); if(leak!=null) throw rejected("statement mentions platform internals: "+leak);
    if(!codeRunner.configured()) throw new LlmUnavailableException("Piston is required to validate generated content");
    var validation=codeRunner.run(lang,task.referenceSolutionSource(),task.testSource());
    if(!validation.passed()) throw rejected("reference solution failed its own checks: "+abbreviate(validation.output(),300));
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,difficulty,language) values(?,?,?,?,?,?,?,?)",task.skillCode(),task.title(),task.statement(),task.starterCode()==null?"":task.starterCode(),task.testSource(),task.testFileName(),difficulty,lang.name());
    long taskId=db.queryForObject("select last_insert_rowid()",Long.class);
    for(String target:new LinkedHashSet<>(task.targetSkillCodes())) db.update("insert into task_target_skills(task_id,skill_code) values(?,?)",taskId,target);
    for(String prerequisite:new LinkedHashSet<>(task.prerequisiteSkillCodes())) db.update("insert into task_prerequisite_skills(task_id,skill_code) values(?,?)",taskId,prerequisite);
    return taskId;
  }
  private static final List<String> INTERNAL_TERMS=List.of("solution.py","test_solution","run_checks","TestHarness","harness","PASS_MARKER","Piston");
  /** Students must not see how checking works; the prompt forbids it and this catches what slips through. */
  static String internalTerm(String statement) { String lower=statement.toLowerCase(Locale.ROOT); for(String term:INTERNAL_TERMS) if(lower.contains(term.toLowerCase(Locale.ROOT))) return term; return null; }
  private static boolean blank(String value) { return value==null||value.isBlank(); }
  private static InvalidGeneratedContentException rejected(String reason) { return new InvalidGeneratedContentException(reason); }
  /** Links validation to the most recent TASK call of this student and skill (turns of one student are serialized). */
  private void markTaskOutcome(long userId,String skillCode,String outcome) { db.update("update llm_calls set outcome=? where id=(select max(id) from llm_calls where user_id=? and purpose='TASK' and skill_code=? and status='OK' and outcome is null)",outcome,userId,skillCode); }
  /** Java harnesses print the pass marker themselves; Python checks expose run_checks() and the fixed entry point prints it. */
  static boolean validHarness(Language lang,String testSource) {
    return lang==Language.PYTHON
        ? testSource.contains("def run_checks(") && testSource.contains("solution")
        : testSource.contains("class TestHarness") && testSource.contains("main(") && testSource.contains(PistonCodeRunner.PASS_MARKER_PLACEHOLDER);
  }

  @PostMapping("/attempts") @Transactional public ResponseEntity<?> attempt(@RequestBody Map<String,Object> body,HttpServletRequest r){long u=student(r);long task=((Number)body.get("taskId")).longValue();var taskRows=db.queryForList("select test_source,active,language from tasks where id=?",task);Language lang=taskRows.isEmpty()?Language.JAVA:Language.of(taskRows.getFirst().get("language"));var l=active(u,lang);if(l==null)throw bad("NO_ACTIVE_LESSON","Сначала начните урок");if(count("select count(*) from lesson_tasks where lesson_id=? and task_id=?",l.get("id"),task)==0)throw bad("TASK_NOT_IN_LESSON","Задача не назначена этому уроку");if(taskRows.isEmpty()||((Number)taskRows.getFirst().get("active")).intValue()!=1)throw bad("TASK_UPDATED","Задача обновлена. Откройте следующую задачу."); String source=(String)body.get("sourceCode"); if(!codeRunner.status(lang).available()) return ResponseEntity.status(503).body(Map.of("error","RUNNER_UNAVAILABLE","message","Проверка "+lang.title+" сейчас недоступна","runner",runner(lang)));long runStarted=System.nanoTime();var result=codeRunner.run(lang,source,(String)taskRows.getFirst().get("test_source"));log.info("Attempt on task {} ({}): passed={} in {} ms",task,lang,result.passed(),(System.nanoTime()-runStarted)/1_000_000);db.update("insert into submissions(lesson_id,task_id,source_code,passed,runner_output) values(?,?,?,?,?)",l.get("id"),task,source,result.passed()?1:0,result.output());long submissionId=db.queryForObject("select last_insert_rowid()",Long.class);if(result.passed()&&db.update("insert or ignore into successful_task_credit(user_id,task_id) values(?,?)",u,task)>0)for(var target:db.queryForList("select skill_code from task_target_skills where task_id=?",task))credit(u,(String)target.get("skill_code"),((Number)l.get("id")).longValue(),((Number)l.get("number")).intValue());return ResponseEntity.ok(Map.of("id",submissionId,"passed",result.passed(),"output",result.output(),"progress",progress(u,lang))); }
  @GetMapping("/progress") public Map<String,Object> progress(@RequestParam(name="language",required=false) String language,HttpServletRequest r){long u=uid(r);Language lang=Language.parse(language);return Map.of("language",lang.name(),"skills",progress(u,lang),"solvedTasks",count("select count(*) from successful_task_credit c join tasks t on t.id=c.task_id where c.user_id=? and t.language=?",u,lang.name()),"activity",db.queryForList("select s.created_at from submissions s join lessons l on l.id=s.lesson_id where l.user_id=? and l.language=? and s.passed=1 and s.created_at>=datetime('now','-90 days') order by s.id",String.class,u,lang.name()));}
  @GetMapping("/chat") public Map<String,Object> chat(@RequestParam(name="language",required=false) String language,HttpServletRequest r){var l=active(uid(r),Language.parse(language));return Map.of("messages",l==null?List.of():db.queryForList("select id,role,content,created_at as createdAt from chat_messages where lesson_id=? order by id",l.get("id")),"llm",llm(uid(r)));}
  @PostMapping("/chat") public ResponseEntity<?> sendChat(@RequestBody Map<String,Object> body,@RequestParam(name="language",required=false) String language,HttpServletRequest r){long u=student(r);Language lang=Language.parse(language);var l=active(u,lang);if(l==null)throw bad("NO_ACTIVE_LESSON","Сначала начните урок");String question=(String)body.get("content");String editorSource=(String)body.get("sourceCode");Object requestedTask=body.get("taskId");if(editorSource!=null||requestedTask!=null){if(editorSource==null||requestedTask==null)throw bad("INVALID_CHAT_CONTEXT","Для кода нужны taskId и sourceCode");if(editorSource.length()>16_000)throw bad("EDITOR_SOURCE_TOO_LONG","Код в редакторе длиннее 16 000 символов");long requestedTaskId;try{requestedTaskId=requestedTask instanceof Number n?n.longValue():Long.parseLong((String)requestedTask);}catch(RuntimeException e){throw bad("INVALID_CHAT_CONTEXT","taskId должен быть числом");}var current=unsolvedTask(l);if(current==null||requestedTaskId!=((Number)current.get("id")).longValue())throw bad("CHAT_TASK_MISMATCH","Код относится не к текущей задаче урока");}db.update("insert into chat_messages(lesson_id,role,content) values(?,?,?)",l.get("id"),"STUDENT",question);try {String answer=tutor.reply(u,tutorContext(lang,l,editorSource),question);db.update("insert into chat_messages(lesson_id,role,content) values(?,?,?)",l.get("id"),"ASSISTANT",answer);long id=db.queryForObject("select last_insert_rowid()",Long.class);return ResponseEntity.ok(Map.of("message",Map.of("id",id,"role","ASSISTANT","content",answer,"createdAt",Instant.now().toString()),"llm",llm(u)));}catch(LlmUnavailableException e){return ResponseEntity.status(503).body(Map.of("error","LLM_UNAVAILABLE","message",e.getMessage(),"llm",llm(u)));}}

  @PostMapping("/admin/students") public Map<String,Object> createStudent(@RequestBody Map<String,Object>b,HttpServletRequest r){admin(r);String login=(String)b.get("login"),password=(String)b.get("password"),name=(String)b.get("displayName");if(login==null||password==null||name==null)throw bad("INVALID_STUDENT","Нужны login, password, displayName");boolean enabled=!Boolean.FALSE.equals(b.get("llmEnabled"));if(count("select count(*) from users where login=?",login.trim())>0)throw bad("LOGIN_TAKEN","Логин «"+login.trim()+"» уже занят");validatePassword(password);db.update("insert into users(login,password_hash,role,display_name,llm_enabled) values(?,?,?,?,?)",login.trim(),passwords.encode(password),"STUDENT",name.trim(),enabled?1:0);log.info("Created student account login={}",login.trim());login=login.trim();return db.queryForMap("select id,login,role,display_name as displayName,llm_enabled as llmEnabled from users where login=?",login);}
  @GetMapping("/admin/students") public Map<String,Object> students(HttpServletRequest r){admin(r);return Map.of("students",db.queryForList("select id,login,display_name as displayName,llm_enabled as llmEnabled,created_at as createdAt from users where role='STUDENT' order by id"));}
  @PatchMapping("/admin/llm") public Map<String,Object> globalLlm(@RequestBody Map<String,Boolean>b,HttpServletRequest r){admin(r);db.update("update app_settings set value=? where key='llm_enabled'",Boolean.TRUE.equals(b.get("enabled"))?"true":"false");return Map.of("enabled",Boolean.TRUE.equals(b.get("enabled")));}
  @PatchMapping("/admin/students/{id}/llm") public Map<String,Object> studentLlm(@PathVariable long id,@RequestBody Map<String,Boolean>b,HttpServletRequest r){admin(r);db.update("update users set llm_enabled=? where id=? and role='STUDENT'",Boolean.TRUE.equals(b.get("enabled"))?1:0,id);return Map.of("id",id,"enabled",Boolean.TRUE.equals(b.get("enabled")));}
  /** Sets a new password and signs the student out everywhere, so an old password cannot keep a session alive. */
  @PatchMapping("/admin/students/{id}/password") public Map<String,Object> studentPassword(@PathVariable long id,@RequestBody Map<String,String> b,HttpServletRequest r){
    admin(r); String password=b.get("password"); validatePassword(password);
    if(db.update("update users set password_hash=? where id=? and role='STUDENT'",passwords.encode(password),id)==0)throw bad("STUDENT_NOT_FOUND","Студент не найден");
    int sessions=db.update("delete from sessions where user_id=?",id);
    log.info("Password changed for student {} by admin {}; {} session(s) closed",id,uid(r),sessions);
    return Map.of("id",id,"sessionsClosed",sessions);
  }
  private void validatePassword(String password){ if(password==null||password.length()<6)throw bad("WEAK_PASSWORD","Пароль должен быть не короче 6 символов"); if(password.length()>200)throw bad("WEAK_PASSWORD","Пароль слишком длинный"); }

  /** Usage of the LLM over the last N days: totals, per day, per purpose, language and student, task acceptance and recent errors. */
  @GetMapping("/admin/llm/usage") public Map<String,Object> llmUsage(@RequestParam(name="days",defaultValue="30") int days,HttpServletRequest r){
    admin(r); int period=Math.max(1,Math.min(365,days)); String since="-"+period+" days";
    String where=" from llm_calls c where c.created_at>=datetime('now',?)";
    var totals=db.queryForMap("select count(*) as calls,coalesce(sum(c.status<>'OK'),0) as errors,coalesce(sum(c.status='TIMEOUT'),0) as timeouts,coalesce(round(avg(case when c.status='OK' then c.duration_ms end)),0) as avgMs,coalesce(sum(c.input_tokens),0) as inputTokens,coalesce(sum(c.cached_input_tokens),0) as cachedTokens,coalesce(sum(c.output_tokens),0) as outputTokens,coalesce(sum(c.reasoning_tokens),0) as reasoningTokens,coalesce(sum(c.total_tokens),0) as totalTokens,coalesce(sum(c.total_tokens is not null),0) as callsWithTokens,count(distinct c.user_id) as students,coalesce(sum(c.outcome='ACCEPTED'),0) as tasksAccepted,coalesce(sum(c.outcome='REJECTED'),0) as tasksRejected"+where,since);
    var durations=db.queryForList("select c.duration_ms"+where+" and c.status='OK' order by c.duration_ms",Long.class,since);
    totals.put("p95Ms",durations.isEmpty()?0:durations.get(Math.min(durations.size()-1,(int)Math.ceil(durations.size()*0.95)-1)));
    var byDay=db.queryForList("select date(c.created_at) as day,count(*) as calls,coalesce(sum(c.status<>'OK'),0) as errors,coalesce(sum(c.total_tokens),0) as tokens"+where+" group by date(c.created_at) order by day",since);
    var byPurpose=db.queryForList("select c.purpose,count(*) as calls,coalesce(sum(c.status<>'OK'),0) as errors,coalesce(round(avg(case when c.status='OK' then c.duration_ms end)),0) as avgMs,coalesce(sum(c.total_tokens),0) as tokens"+where+" group by c.purpose order by calls desc",since);
    var byLanguage=db.queryForList("select c.language,count(*) as calls,coalesce(sum(c.total_tokens),0) as tokens"+where+" group by c.language order by calls desc",since);
    var byStudent=db.queryForList("select c.user_id as userId,coalesce(u.display_name,'—') as displayName,u.login,count(*) as calls,coalesce(sum(c.purpose='CHAT'),0) as chatTurns,coalesce(sum(c.status<>'OK'),0) as errors,coalesce(sum(c.total_tokens),0) as tokens,max(c.created_at) as lastAt from llm_calls c left join users u on u.id=c.user_id where c.created_at>=datetime('now',?) group by c.user_id order by calls desc limit 100",since);
    var errors=db.queryForList("select c.created_at as createdAt,c.purpose,c.language,c.status,c.error,c.duration_ms as durationMs,u.display_name as displayName from llm_calls c left join users u on u.id=c.user_id where c.created_at>=datetime('now',?) and c.status<>'OK' order by c.created_at desc,c.id desc limit 20",since);
    return obj("days",period,"totals",totals,"byDay",byDay,"byPurpose",byPurpose,"byLanguage",byLanguage,"byStudent",byStudent,"recentErrors",errors,"llm",llm(uid(r)));
  }
  @GetMapping("/admin/students/{id}") public Map<String,Object> student(@PathVariable long id,HttpServletRequest r){admin(r);var s=db.queryForMap("select id,login,display_name as displayName,llm_enabled as llmEnabled from users where id=? and role='STUDENT'",id);var byLanguage=new LinkedHashMap<String,Object>();for(Language lang:Language.values())byLanguage.put(lang.name(),progress(id,lang));return Map.of("student",s,"progress",progress(id,Language.JAVA),"progressByLanguage",byLanguage,"llm",llm(id));}
  @GetMapping("/admin/students/{id}/lessons") public Map<String,Object> lessons(@PathVariable long id,HttpServletRequest r){admin(r);return Map.of("lessons",db.queryForList("select id,coalesce(language_lesson_number,lesson_number) as number,language,started_at as startedAt,finished_at as finishedAt from lessons where user_id=? order by lesson_number",id));}
  @GetMapping("/admin/students/{id}/lessons/{lessonId}") public Map<String,Object> lessonDetail(@PathVariable long id,@PathVariable long lessonId,HttpServletRequest r){admin(r);var l=db.queryForMap("select id,coalesce(language_lesson_number,lesson_number) as number,language,started_at as startedAt,finished_at as finishedAt from lessons where id=? and user_id=?",lessonId,id);var tasks=db.queryForList("select t.id,t.title,t.statement from tasks t join lesson_tasks x on x.task_id=t.id where x.lesson_id=?",lessonId);for(var t:tasks)t.put("submissions",db.queryForList("select id,source_code as sourceCode,passed,runner_output as output,created_at as createdAt from submissions where lesson_id=? and task_id=? order by id",lessonId,t.get("id")));return Map.of("lesson",l,"chat",db.queryForList("select id,role,content,created_at as createdAt from chat_messages where lesson_id=? order by id",lessonId),"tasks",tasks);}

  private TutorContext tutorContext(Language lang,Map<String,Object> lesson,String currentEditorSource) { long lessonId=((Number)lesson.get("id")).longValue(); var taskRows=db.queryForList("select t.id,t.title,t.statement,ts.skill_code from lesson_tasks lt join tasks t on t.id=lt.task_id join task_target_skills ts on ts.task_id=t.id where lt.lesson_id=? and t.active=1 and not exists(select 1 from submissions x where x.lesson_id=lt.lesson_id and x.task_id=lt.task_id and x.passed=1) order by lt.rowid desc limit 1",lessonId); String skillCode=null,skillTitle=null; Long taskId=null;String taskTitle=null,taskStatement=null,source=null,output=null;Boolean passed=null; if(!taskRows.isEmpty()){var task=taskRows.getFirst();taskId=((Number)task.get("id")).longValue();taskTitle=(String)task.get("title");taskStatement=(String)task.get("statement");skillCode=(String)task.get("skill_code");var titleRows=db.queryForList("select title from skills where code=?",skillCode);skillTitle=titleRows.isEmpty()?skillCode:(String)titleRows.getFirst().get("title");var submission=db.queryForList("select source_code,passed,runner_output from submissions where lesson_id=? and task_id=? order by id desc limit 1",lessonId,taskId);if(!submission.isEmpty()){var last=submission.getFirst();source=(String)last.get("source_code");passed=((Number)last.get("passed")).intValue()==1;output=(String)last.get("runner_output");}} return new TutorContext(lang,lessonId,((Number)lesson.get("number")).intValue(),skillCode,skillTitle,taskId,taskTitle,taskStatement,currentEditorSource,source,passed,output); }
  private Map<String,Object> status(Map<String,Object> u){return Map.of("user",viewUser(u),"llm",llm(((Number)u.get("id")).longValue()),"runner",runner(Language.JAVA));} private Map<String,Object> viewUser(Map<String,Object> u){return Map.of("id",u.get("id"),"login",u.get("login"),"role",u.get("role"),"displayName",u.get("display_name"),"llmEnabled",u.get("llm_enabled"));}
  private Map<String,Object> llm(long id){return tutor.status(id).asMap();} private Map<String,Object> runner(Language lang){var state=codeRunner.status(lang);return obj("available",state.available(),"reason",state.reason(),"language",lang.name(),"version",state.version());}
  private List<Map<String,Object>> progress(long u,Language lang){return db.queryForList("select s.code as skillCode,s.title,coalesce(x.completed_iterations,0) as completedIterations,coalesce(x.iteration_successes,0) as iterationSuccesses,coalesce(x.mastered,0) as mastered from skills s left join student_skills x on x.skill_code=s.code and x.user_id=? where s.language=? order by s.sort_order",u,lang.name());}
  private void credit(long user,String skill,long lessonId,int lessonNumber){db.update("insert or ignore into student_skills(user_id,skill_code) values(?,?)",user,skill);int successes=count("select count(distinct c.task_id) from successful_task_credit c join task_target_skills ts on ts.task_id=c.task_id join submissions s on s.task_id=c.task_id and s.lesson_id=? and s.passed=1 where c.user_id=? and ts.skill_code=?",lessonId,user,skill);if(successes<3){db.update("update student_skills set iteration_successes=? where user_id=? and skill_code=?",successes,user,skill);return;}var x=db.queryForMap("select completed_iterations,first_iteration_lesson_number from student_skills where user_id=? and skill_code=?",user,skill);int completed=((Number)x.get("completed_iterations")).intValue();Integer first=x.get("first_iteration_lesson_number")==null?null:((Number)x.get("first_iteration_lesson_number")).intValue();boolean due=completed==0||(completed==1&&lessonNumber==first+1)||(completed==2&&lessonNumber==first+3);if(!due||count("select count(*) from skill_iterations where user_id=? and skill_code=? and lesson_id=?",user,skill,lessonId)>0)return;int done=completed+1;db.update("insert into skill_iterations(user_id,skill_code,iteration_number,lesson_id) values(?,?,?,?)",user,skill,done,lessonId);db.update("update student_skills set completed_iterations=?,iteration_successes=0,first_iteration_lesson_number=case when first_iteration_lesson_number is null then ? else first_iteration_lesson_number end,mastered=? where user_id=? and skill_code=?",done,lessonNumber,done>=3?1:0,user,skill);}
  /**
   * Picks one skill and keeps the student on it: an iteration already started in this lesson is finished first,
   * then scheduled repetitions (iterations 2 and 3 are only valid on their lesson), then new topics in course order.
   */
  private Map<String,Object> nextSkill(long userId,Language lang,int lessonNumber,long lessonId) {
    int startBlock=db.queryForObject("select starting_block from student_languages where user_id=? and language=?",Integer.class,userId,lang.name());
    var rows=db.queryForList("select s.code,s.title,s.block_no,coalesce(x.completed_iterations,0) completed,coalesce(x.first_iteration_lesson_number,0) first from skills s left join student_skills x on x.skill_code=s.code and x.user_id=? where s.language=? and coalesce(x.mastered,0)=0 and s.block_no>=? and (s.prerequisite_code is null or exists(select 1 from student_skills p where p.user_id=? and p.skill_code=s.prerequisite_code and p.mastered=1)) order by s.block_no,s.sort_order",userId,lang.name(),startBlock,userId);
    var due=new ArrayList<Map<String,Object>>();
    for(var row:rows) { int completed=((Number)row.get("completed")).intValue(), first=((Number)row.get("first")).intValue(); if(completed==0||(completed==1&&lessonNumber==first+1)||(completed==2&&lessonNumber==first+3)) due.add(row); }
    if(due.isEmpty()) return null;
    for(var row:due) if(solvedInLesson(userId,lessonId,(String)row.get("code"))>0) return skillView(row);
    for(var row:due) if(((Number)row.get("completed")).intValue()>0) return skillView(row);
    // Without generation a topic with an empty bank would block the lesson, so take the first topic that still has tasks.
    if(!tutor.status(userId).available()||!codeRunner.status(lang).available())
      for(var row:due) if(count("select count(*) from tasks t join task_target_skills ts on ts.task_id=t.id where t.active=1 and ts.skill_code=? and not exists(select 1 from successful_task_credit c where c.user_id=? and c.task_id=t.id) and not exists(select 1 from lesson_tasks x where x.lesson_id=? and x.task_id=t.id)",row.get("code"),userId,lessonId)>0) return skillView(row);
    return skillView(due.getFirst());
  }
  private static Map<String,Object> skillView(Map<String,Object> row) { return Map.of("code",row.get("code"),"title",row.get("title"),"blockNo",row.get("block_no")); }
  /** The open lesson of this language; "number" is the per-language lesson number that drives the iteration schedule. */
  private Map<String,Object> active(long u,Language lang){var x=db.queryForList("select id,language_lesson_number as number,language,started_at as startedAt from lessons where user_id=? and language=? and finished_at is null order by id desc",u,lang.name());return x.isEmpty()?null:x.getFirst();} private Map<String,Object> lesson(long id){return db.queryForMap("select id,language_lesson_number as number,language,started_at as startedAt,finished_at as finishedAt from lessons where id=?",id);} private boolean diagnosticDone(long u,Language lang){return count("select count(*) from student_languages where user_id=? and language=? and diagnostic_completed_at is not null",u,lang.name())>0;} private void requireDiagnostic(long u,Language lang){if(!diagnosticDone(u,lang))throw bad("DIAGNOSTIC_REQUIRED","Сначала пройдите диагностику");} private int count(String q,Object...p){return db.queryForObject(q,Integer.class,p);} private long uid(HttpServletRequest r){return ((Number)user(r).get("id")).longValue();} @SuppressWarnings("unchecked") private Map<String,Object> user(HttpServletRequest r){return (Map<String,Object>)r.getAttribute("user");} private long student(HttpServletRequest r){if(!"STUDENT".equals(user(r).get("role")))throw bad("FORBIDDEN","Нужна роль STUDENT");return uid(r);} private void admin(HttpServletRequest r){if(!"ADMIN".equals(user(r).get("role")))throw bad("FORBIDDEN","Нужна роль ADMIN");} private Optional<String> cookie(HttpServletRequest r){return r.getCookies()==null?Optional.empty():Arrays.stream(r.getCookies()).filter(c->c.getName().equals("adaptive_session")).map(Cookie::getValue).findFirst();} private String randomToken(){byte[] b=new byte[32];new SecureRandom().nextBytes(b);return Base64.getUrlEncoder().withoutPadding().encodeToString(b);} private Object json(Object value){try{return new com.fasterxml.jackson.databind.ObjectMapper().readValue((String)value,List.class);}catch(Exception e){throw new IllegalStateException(e);}} private Map<String,Object> obj(Object... entries){var m=new LinkedHashMap<String,Object>();for(int i=0;i<entries.length;i+=2)m.put((String)entries[i],entries[i+1]);return m;} private ApiError bad(String c,String m){return new ApiError(c,m);}
}
@ResponseStatus(HttpStatus.BAD_REQUEST) class ApiError extends RuntimeException { final String code; ApiError(String c,String m){super(m);code=c;} }
class InvalidGeneratedContentException extends RuntimeException { InvalidGeneratedContentException(String reason){super(reason);} }
@RestControllerAdvice class Errors { private static final org.slf4j.Logger log=org.slf4j.LoggerFactory.getLogger(Errors.class); @ExceptionHandler(ApiError.class) ResponseEntity<?> api(ApiError e){log.info("Rejected request: {} ({})",e.code,e.getMessage());return ResponseEntity.badRequest().body(Map.of("error",e.code,"message",e.getMessage()));} }
