package ru.teacherstaff.adaptive;

import jakarta.servlet.http.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionTemplate;
import java.util.concurrent.ConcurrentHashMap;
import java.security.SecureRandom;
import java.time.*;
import java.util.*;

@RestController @RequestMapping("/api")
public class ApiController {
  private static final org.slf4j.Logger log=org.slf4j.LoggerFactory.getLogger(ApiController.class);
  /** Verification is strict (reference must pass, wrong solutions must fail), so the generator gets three tries. */
  static final int GENERATION_ATTEMPTS=3;
  private final JdbcTemplate db; private final PistonCodeRunner codeRunner; private final LlmTutor tutor; private final LearningContentGenerator contentGenerator; private final TaskVerifier verifier; private final DiagnosticProfile diagnostics; private final TransactionTemplate tx; private final LlmSettings llmSettings;
  /**
   * Serializes /learning/next per student and course. It replaces what the long transaction never really gave:
   * a second request for the same lesson (double click, React StrictMode) waits and then sees the task the first one
   * assigned, instead of generating and assigning another. Other students are not affected.
   */
  private final ConcurrentHashMap<String,Object> lessonLocks=new ConcurrentHashMap<>(); private final BCryptPasswordEncoder passwords=new BCryptPasswordEncoder();
  @Value("${app.session-hours}") long sessionHours; @Value("${app.cookie-secure}") boolean secureCookie; @Value("${app.piston.base-url}") String pistonUrl;
  ApiController(JdbcTemplate db, PistonCodeRunner codeRunner, LlmTutor tutor, LearningContentGenerator contentGenerator, TaskVerifier verifier, DiagnosticProfile diagnostics, TransactionTemplate tx, LlmSettings llmSettings) { this.db=db; this.codeRunner=codeRunner; this.tutor=tutor; this.contentGenerator=contentGenerator; this.verifier=verifier; this.diagnostics=diagnostics; this.tx=tx; this.llmSettings=llmSettings; }
  @PostMapping("/auth/login") public Map<String,Object> login(@RequestBody Map<String,String> body, HttpServletResponse response) {
    var rows=db.queryForList("select id,login,password_hash,role,display_name,llm_enabled from users where login=?",body.get("login"));
    if(rows.isEmpty() || !passwords.matches(body.getOrDefault("password",""),(String)rows.getFirst().get("password_hash"))) throw bad("INVALID_CREDENTIALS","Неверный логин или пароль");
    var u=rows.getFirst(); if("STUDENT".equals(u.get("role")))LogContext.student(u.get("id"),u.get("login"));else LogContext.admin(u.get("login")); String token=randomToken(); db.update("insert into sessions(token_hash,user_id,expires_at) values(?,?,?)",Hashing.sha256(token),u.get("id"),Instant.now().plus(Duration.ofHours(sessionHours)).toString());
    Cookie c=new Cookie("adaptive_session",token); c.setHttpOnly(true); c.setPath("/api"); c.setMaxAge((int)Duration.ofHours(sessionHours).toSeconds()); c.setSecure(secureCookie); response.addCookie(c); return status(u);
  }
  @PostMapping("/auth/logout") @ResponseStatus(HttpStatus.NO_CONTENT) public void logout(HttpServletRequest r,HttpServletResponse p) { finishOpenLessons(r); cookie(r).ifPresent(t->db.update("delete from sessions where token_hash=?",Hashing.sha256(t))); Cookie c=new Cookie("adaptive_session","");c.setPath("/api");c.setMaxAge(0);p.addCookie(c); }
  @GetMapping("/auth/me") public Map<String,Object> me(HttpServletRequest r) { return status(user(r)); }

  @GetMapping("/diagnostic") public Map<String,Object> diagnostic(@RequestParam(name="language",required=false) String language,HttpServletRequest r) { long id=uid(r); Language lang=Language.parse(language); boolean done=diagnosticDone(id,lang); var qs=db.queryForList("select id,ordinal,skill_code,prompt,options_json from diagnostic_questions where language=? order by ordinal",lang.name()); return Map.of("completed",done,"questions",done?List.of():qs.stream().map(q->Map.of("id",q.get("id"),"ordinal",q.get("ordinal"),"skillCode",q.get("skill_code"),"prompt",q.get("prompt"),"options",json(q.get("options_json")),"unknownOption",Map.of("label","Не знаю"))).toList()); }
  @PostMapping("/diagnostic") @Transactional public Map<String,Object> submitDiagnostic(@RequestBody Map<String,Object> body,@RequestParam(name="language",required=false) String language,HttpServletRequest r) { long user=student(r); Language lang=Language.parse(language); if(diagnosticDone(user,lang)) throw bad("DIAGNOSTIC_ALREADY_COMPLETED","Диагностика уже пройдена");
    @SuppressWarnings("unchecked") List<Map<String,Object>> answers=(List<Map<String,Object>>)body.get("answers"); if(answers==null || answers.size()!=count("select count(*) from diagnostic_questions where language=?",lang.name())) throw bad("INVALID_DIAGNOSTIC","Нужны ответы на все вопросы");
    Map<Long,Integer> received=new HashMap<>(); for(var a:answers) { long id=((Number)a.get("questionId")).longValue(); Integer choice=a.get("selectedOption")==null?null:((Number)a.get("selectedOption")).intValue(); if(choice!=null&&(choice<0||choice>3)||received.containsKey(id)) throw bad("INVALID_DIAGNOSTIC","Ответы должны быть уникальны и иметь допустимый вариант"); received.put(id,choice); }
    var qs=db.queryForList("select id,correct_option,block_no from diagnostic_questions where language=?",lang.name()); Map<Integer,int[]> score=new HashMap<>(); for(var q:qs){long qid=((Number)q.get("id")).longValue(); Integer selected=received.get(qid); if(!received.containsKey(qid))throw bad("INVALID_DIAGNOSTIC","Есть неизвестный вопрос"); boolean ok=selected!=null&&selected.equals(((Number)q.get("correct_option")).intValue()); db.update("insert into diagnostic_answers(user_id,question_id,selected_option,is_correct) values(?,?,?,?)",user,qid,selected,ok?1:0); int[] s=score.computeIfAbsent(((Number)q.get("block_no")).intValue(),x->new int[2]);s[1]++;if(ok)s[0]++;}
    // Practice is chosen per topic now (see DiagnosticProfile); starting_block only records where the first gap is.
    var topics=diagnostics.store(user,lang);
    Integer start=db.query("select min(s.block_no) from skills s join diagnostic_skill_results d on d.skill_code=s.code and d.user_id=? where s.language=? and d.confirmed=0",rs->{rs.next();int v=rs.getInt(1);return rs.wasNull()?null:v;},user,lang.name());
    db.update("insert into student_languages(user_id,language,diagnostic_completed_at,starting_block) values(?,?,?,?) on conflict(user_id,language) do update set diagnostic_completed_at=excluded.diagnostic_completed_at,starting_block=excluded.starting_block",user,lang.name(),Instant.now().toString(),start);
    long confirmed=topics.stream().filter(DiagnosticProfile.TopicResult::confirmed).count();
    return obj("completed",true,"startingBlock",start,"confirmedTopics",confirmed,"gapTopics",topics.size()-confirmed); }

  @GetMapping("/lessons/current") public Map<String,Object> current(@RequestParam(name="language",required=false) String language,HttpServletRequest r){return obj("lesson",active(uid(r),Language.parse(language)));}
  @PostMapping("/lessons/start") public Map<String,Object> start(@RequestParam(name="language",required=false) String language,HttpServletRequest r){long u=student(r);Language lang=Language.parse(language);requireDiagnostic(u,lang);var current=active(u,lang);if(current!=null)return Map.of("lesson",current);int n=count("select coalesce(max(lesson_number),0) from lessons where user_id=?",u)+1;int inLanguage=count("select count(*) from lessons where user_id=? and language=?",u,lang.name())+1;db.update("insert into lessons(user_id,lesson_number,language,language_lesson_number) values(?,?,?,?)",u,n,lang.name(),inLanguage);return Map.of("lesson",active(u,lang));}
  @PostMapping("/lessons/{id}/finish") public Map<String,Object> finish(@PathVariable long id,HttpServletRequest r){long u=student(r);if(!finishLesson(u,id))throw bad("LESSON_NOT_ACTIVE","Активный урок не найден");log.info("Lesson {} finished by the student",id);return Map.of("lesson",lesson(id));}
  /** Logging out ends the student's open lessons in every course, as «Завершить урок» would. */
  private void finishOpenLessons(HttpServletRequest r){
    if(!(r.getAttribute("user") instanceof Map<?,?> user)||!"STUDENT".equals(user.get("role")))return;
    long u=((Number)user.get("id")).longValue();
    for(long id:db.queryForList("select id from lessons where user_id=? and finished_at is null",Long.class,u)) if(finishLesson(u,id)) log.info("Lesson {} finished on logout",id);
  }
  /**
   * Finishes an open lesson. It does not wait for a /learning/next that is still preparing content: that request
   * notices the lesson is over and keeps what it generated (see nextLocked). Returns false if the lesson was not open.
   */
  private boolean finishLesson(long user,long lessonId){
    if(db.update("update lessons set finished_at=? where id=? and user_id=? and finished_at is null",Instant.now().toString(),lessonId,user)==0)return false;
    queueUnsolvedRedos(user,lessonId);
    return true;
  }
  /**
   * Not @Transactional on purpose: this request may wait for the LLM (explanation, task generation) and Piston
   * (verification) for tens of seconds. Holding a SQLite transaction that long blocked every other writer and ended in
   * SQLITE_BUSY. Each database step below is a single statement or a short transaction of its own.
   */
  @GetMapping("/learning/next") public Map<String,Object> next(@RequestParam(name="language",required=false) String language,HttpServletRequest r) {
    long userId=student(r); Language lang=Language.parse(language);
    synchronized(lessonLocks.computeIfAbsent(userId+":"+lang.name(),k->new Object())) { return nextLocked(userId,lang); }
  }
  private Map<String,Object> nextLocked(long userId,Language lang) {
    var lesson=active(userId,lang);
    if(lesson==null) throw bad("NO_ACTIVE_LESSON","Сначала начните урок");
    var assigned=unsolvedTask(lesson);
    if(assigned!=null) return learningResponse(userId,lesson,assigned);
    var redo=pendingRedo(userId,lang);
    if(redo!=null){
      if(!assign(lesson,((Number)redo.get("id")).longValue())) return lessonFinished(lesson);
      db.update("delete from pending_redos where user_id=? and task_id=?",userId,redo.get("id"));
      log.info("Assigned queued task {} ({}) to lesson {} of student {}",redo.get("id"),"GENERATED".equals(redo.get("reason"))?"generated for a lesson finished during generation":"credit revoked by the teacher",lesson.get("id"),userId);
      return learningResponse(userId,lesson,redo);
    }
    var skill=nextSkill(userId,lang,((Number)lesson.get("number")).intValue(),((Number)lesson.get("id")).longValue());
    if(skill==null) return obj("lesson",lesson,"skill",null,"explanation",null,"task",null,"reason",remainingTopics(userId,lang)==0?"COURSE_COMPLETE":"NO_DUE_SKILL","llm",llm(userId));
    String skillCode=(String)skill.get("code");
    long lessonId=((Number)lesson.get("id")).longValue();
    Object explanation=explanation(userId, skillCode);
    // The lesson may have been finished (by the student, an admin or a logout) while the explanation was generated;
    // the explanation is saved for the topic, a task is chosen in the next lesson.
    if(!stillActive(lessonId)) return lessonFinished(lesson);
    int difficulty=targetDifficulty(userId, lessonId, skillCode);
    var tasks=availableTasks(userId, lesson, skillCode, difficulty);
    Long generatedTaskId=null;
    if(!hasDifficulty(tasks, difficulty)) {
      // Generate the missing step of the easy→hard ladder; fall back to the nearest bank task when generation is impossible.
      String reason=null;
      if(!tutor.status(userId).available()) reason="NO_TASK_AVAILABLE";
      else if(!llmSettings.taskGenerationAllowed()) { reason="LLM_RATE_LIMITED"; log.info("Task generation skipped for skill={}: course-wide task generation limit reached",skillCode); }
      else if(!codeRunner.status(lang).available()) reason="RUNNER_UNAVAILABLE";
      else {
        var brief=brief(userId, skillCode, difficulty, explanation instanceof Map<?,?> m ? (String)m.get("content") : null);
        for(int attempt=1;attempt<=GENERATION_ATTEMPTS&&generatedTaskId==null;attempt++) try {
          if(attempt>1&&!stillActive(lessonId)) break; // no new attempts for a finished lesson
          log.info("Generating task: skill={} language={} difficulty={} attempt={}/{}",skillCode,lang,difficulty,attempt,GENERATION_ATTEMPTS);
          generatedTaskId=storeGeneratedTask(contentGenerator.generateTask(userId, brief), difficulty, lang);
          markTaskOutcome(userId,skillCode,"ACCEPTED");
          log.info("Generated task {} accepted for skill={} difficulty={}",generatedTaskId,skillCode,difficulty);
        }
        catch (InvalidGeneratedContentException e) { markTaskOutcome(userId,skillCode,"REJECTED"); log.warn("Generated task rejected (skill={}, attempt {}/{}): {}",skillCode,attempt,GENERATION_ATTEMPTS,e.getMessage()); }
        catch (LlmUnavailableException e) { log.warn("Task generation unavailable for skill={}: {}",skillCode,e.getMessage()); reason="NO_TASK_AVAILABLE"; break; }
        if(generatedTaskId==null&&reason==null) reason="LLM_GENERATION_FAILED_VALIDATION";
        tasks=availableTasks(userId, lesson, skillCode, difficulty);
      }
      if(!stillActive(lessonId)) return lessonFinished(lesson, userId, generatedTaskId);
      if(tasks.isEmpty()) return "RUNNER_UNAVAILABLE".equals(reason)
          ? obj("lesson",lesson,"skill",skill,"explanation",explanation,"task",null,"reason",reason,"llm",llm(userId),"runner",runner(lang))
          : obj("lesson",lesson,"skill",skill,"explanation",explanation,"task",null,"reason",reason==null?"NO_TASK_AVAILABLE":reason,"llm",llm(userId));
    }
    var task=tasks.getFirst();
    if(!assign(lesson,((Number)task.get("id")).longValue())) return lessonFinished(lesson, userId, generatedTaskId);
    return obj("lesson",lesson,"skill",skill,"explanation",explanation,"task",taskView(userId,task));
  }
  private boolean stillActive(long lessonId){ return count("select count(*) from lessons where id=? and finished_at is null",lessonId)>0; }
  /** Assigns a task only to a lesson that is still open: a finish can land at any moment while content is prepared. */
  private boolean assign(Map<String,Object> lesson,long taskId){
    return db.update("insert or ignore into lesson_tasks(lesson_id,task_id) select ?,? where exists(select 1 from lessons where id=? and finished_at is null)",lesson.get("id"),taskId,lesson.get("id"))>0
        || count("select count(*) from lesson_tasks x join lessons l on l.id=x.lesson_id where x.lesson_id=? and x.task_id=? and l.finished_at is null",lesson.get("id"),taskId)>0;
  }
  private Map<String,Object> lessonFinished(Map<String,Object> lesson){ return obj("lesson",lesson(((Number)lesson.get("id")).longValue()),"skill",null,"explanation",null,"task",null,"reason","LESSON_FINISHED"); }
  /** A task generated for a lesson that ended meanwhile is reserved: the student gets it first in the next lesson of the course. */
  private Map<String,Object> lessonFinished(Map<String,Object> lesson,long userId,Long generatedTaskId){
    if(generatedTaskId!=null){
      db.update("insert or ignore into pending_redos(user_id,task_id,reason) values(?,?,'GENERATED')",userId,generatedTaskId);
      log.info("Lesson {} was finished during generation; task {} is kept for the student's next lesson",lesson.get("id"),generatedTaskId);
    }
    return lessonFinished(lesson);
  }
  private Map<String,Object> unsolvedTask(Map<String,Object> lesson) { var rows=db.queryForList("select t.id,t.title,t.statement,t.starter_code,ts.skill_code, s.title as skill_title,s.block_no from lesson_tasks lt join tasks t on t.id=lt.task_id join task_target_skills ts on ts.task_id=t.id join skills s on s.code=ts.skill_code where lt.lesson_id=? and t.active=1 and not exists(select 1 from submissions x where x.lesson_id=lt.lesson_id and x.task_id=lt.task_id and x.passed=1) order by lt.rowid desc limit 1",lesson.get("id"));return rows.isEmpty()?null:rows.getFirst(); }
  /** The oldest task the teacher sent back that is still active; retired ones are dropped from the queue. */
  private Map<String,Object> pendingRedo(long userId,Language lang){
    db.update("delete from pending_redos where user_id=? and task_id in (select id from tasks where active=0)",userId);
    var rows=db.queryForList("select t.id,t.title,t.statement,t.starter_code,ts.skill_code,s.title as skill_title,s.block_no,p.reason from pending_redos p join tasks t on t.id=p.task_id join task_target_skills ts on ts.task_id=t.id join skills s on s.code=ts.skill_code where p.user_id=? and t.language=? order by p.created_at,p.task_id limit 1",userId,lang.name());
    return rows.isEmpty()?null:rows.getFirst();
  }
  private Map<String,Object> learningResponse(long userId,Map<String,Object> lesson,Map<String,Object> task) { String skillCode=(String)task.get("skill_code");Object explanation=explanation(userId,skillCode);return obj("lesson",lesson,"skill",Map.of("code",skillCode,"title",task.get("skill_title"),"blockNo",task.get("block_no")),"explanation",explanation,"task",taskView(userId,task)); }
  /** redo: the teacher cancelled this student's accepted solution, so the task is being solved again. */
  private Map<String,Object> taskView(long userId,Map<String,Object> task) { boolean redo=count("select count(*) from submissions s join lessons l on l.id=s.lesson_id where l.user_id=? and s.task_id=? and s.revoked_at is not null",userId,task.get("id"))>0; return Map.of("id",task.get("id"),"title",task.get("title"),"statement",task.get("statement"),"starterCode",task.get("starter_code"),"redo",redo); }
  /** Unsolved bank tasks for the skill, the requested difficulty first, then the nearest one, legacy tasks without difficulty last. */
  private List<Map<String,Object>> availableTasks(long userId,Map<String,Object> lesson,String skillCode,int difficulty) {
    return db.queryForList("select t.id,t.title,t.statement,t.starter_code,t.difficulty from tasks t join task_target_skills ts on ts.task_id=t.id where t.active=1 and ts.skill_code=? and not exists(select 1 from successful_task_credit c where c.user_id=? and c.task_id=t.id) and not exists(select 1 from lesson_tasks x where x.lesson_id=? and x.task_id=t.id) and not exists(select 1 from task_prerequisite_skills req where req.task_id=t.id and not exists(select 1 from student_skills p where p.user_id=? and p.skill_code=req.skill_code and p.mastered=1)) order by t.difficulty is null, abs(t.difficulty-?), t.difficulty, t.id",skillCode,userId,lesson.get("id"),userId,difficulty);
  }
  private static boolean hasDifficulty(List<Map<String,Object>> tasks,int difficulty) { return !tasks.isEmpty() && tasks.getFirst().get("difficulty") instanceof Number d && d.intValue()==difficulty; }
  /** Step inside the current iteration: the n-th task of the skill solved in this lesson asks for difficulty n+1 (1..3). */
  private int targetDifficulty(long userId,long lessonId,String skillCode) { return Math.min(3, solvedInLesson(userId,lessonId,skillCode)+1); }
  private int solvedInLesson(long userId,long lessonId,String skillCode) { return count("select count(distinct c.task_id) from successful_task_credit c join task_target_skills ts on ts.task_id=c.task_id join submissions s on s.task_id=c.task_id and s.lesson_id=? and s.passed=1 where c.user_id=? and ts.skill_code=?",lessonId,userId,skillCode); }
  private ContentBrief brief(long userId,String skillCode,int difficulty,String explanation) { return CourseBriefs.brief(db,userId,skillCode,difficulty,explanation); }
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
    if(!llmSettings.explanationGenerationAllowed()) { log.info("Explanation generation for {} skipped: course-wide explanation limit reached",skillCode); return null; }
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
    // Piston runs (reference and wrong solutions) happen here, outside any transaction.
    var verified=verifier.verify(lang,task);
    // The task and its skill links appear together or not at all.
    return tx.execute(status->{
      long taskId=db.queryForObject("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,difficulty,language,source,goal_json,quality_version) values(?,?,?,?,?,?,?,?,'LLM',?,?) returning id",Long.class,task.skillCode(),task.title(),task.statement(),task.starterCode()==null?"":task.starterCode(),verified.testSource(),task.testFileName(),difficulty,lang.name(),verified.goalJson(),LearningContentGenerator.TASK_QUALITY_VERSION);
      for(String target:new LinkedHashSet<>(task.targetSkillCodes())) db.update("insert into task_target_skills(task_id,skill_code) values(?,?)",taskId,target);
      for(String prerequisite:new LinkedHashSet<>(task.prerequisiteSkillCodes())) db.update("insert into task_prerequisite_skills(task_id,skill_code) values(?,?)",taskId,prerequisite);
      return taskId;
    });
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

  /** Not @Transactional: the Piston run (up to ~20 s) happens between a read-only validation and one short write transaction. */
  @PostMapping("/attempts") public ResponseEntity<?> attempt(@RequestBody Map<String,Object> body,HttpServletRequest r){long u=student(r);long task=((Number)body.get("taskId")).longValue();var taskRows=db.queryForList("select test_source,active,language,goal_json from tasks where id=?",task);Language lang=taskRows.isEmpty()?Language.JAVA:Language.of(taskRows.getFirst().get("language"));var l=active(u,lang);if(l==null)throw bad("NO_ACTIVE_LESSON","Сначала начните урок");if(count("select count(*) from lesson_tasks where lesson_id=? and task_id=?",l.get("id"),task)==0)throw bad("TASK_NOT_IN_LESSON","Задача не назначена этому уроку");if(taskRows.isEmpty()||((Number)taskRows.getFirst().get("active")).intValue()!=1)throw bad("TASK_UPDATED","Задача обновлена. Откройте следующую задачу."); String source=(String)body.get("sourceCode"); if(!codeRunner.status(lang).available()) return ResponseEntity.status(503).body(Map.of("error","RUNNER_UNAVAILABLE","message","Проверка "+lang.title+" сейчас недоступна","runner",runner(lang)));long runStarted=System.nanoTime();var result=verifier.run(lang,source,(String)taskRows.getFirst().get("test_source"),(String)taskRows.getFirst().get("goal_json"));log.info("Attempt on task {} ({}): passed={} in {} ms",task,lang,result.passed(),(System.nanoTime()-runStarted)/1_000_000);long submissionId=tx.execute(status->{
      // Submission, task credit and skill progress change together, so a crash can never leave credit without its submission.
      long id=db.queryForObject("insert into submissions(lesson_id,task_id,source_code,passed,runner_output) values(?,?,?,?,?) returning id",Long.class,l.get("id"),task,source,result.passed()?1:0,result.output());
      if(result.passed()&&db.update("insert or ignore into successful_task_credit(user_id,task_id) values(?,?)",u,task)>0)for(var target:db.queryForList("select skill_code from task_target_skills where task_id=?",task))credit(u,(String)target.get("skill_code"),((Number)l.get("id")).longValue(),((Number)l.get("number")).intValue());
      return id;
    });
    return ResponseEntity.ok(Map.of("id",submissionId,"passed",result.passed(),"output",result.output(),"progress",progress(u,lang))); }
  @GetMapping("/progress") public Map<String,Object> progress(@RequestParam(name="language",required=false) String language,HttpServletRequest r){long u=uid(r);Language lang=Language.parse(language);return Map.of("language",lang.name(),"skills",progress(u,lang),"solvedTasks",count("select count(*) from successful_task_credit c join tasks t on t.id=c.task_id where c.user_id=? and t.language=?",u,lang.name()),"activity",db.queryForList("select s.created_at from submissions s join lessons l on l.id=s.lesson_id where l.user_id=? and l.language=? and s.passed=1 and s.created_at>=datetime('now','-90 days') order by s.id",String.class,u,lang.name()));}
  @GetMapping("/chat") public Map<String,Object> chat(@RequestParam(name="language",required=false) String language,HttpServletRequest r){var l=active(uid(r),Language.parse(language));return Map.of("messages",l==null?List.of():db.queryForList("select id,role,content,created_at as createdAt from chat_messages where lesson_id=? order by id",l.get("id")),"llm",llm(uid(r)),"quota",llmSettings.chatQuota(uid(r)).view());}
  @PostMapping("/chat") public ResponseEntity<?> sendChat(@RequestBody Map<String,Object> body,@RequestParam(name="language",required=false) String language,HttpServletRequest r){long u=student(r);Language lang=Language.parse(language);var l=active(u,lang);if(l==null)throw bad("NO_ACTIVE_LESSON","Сначала начните урок");String question=(String)body.get("content");String editorSource=(String)body.get("sourceCode");Object requestedTask=body.get("taskId");if(editorSource!=null||requestedTask!=null){if(editorSource==null||requestedTask==null)throw bad("INVALID_CHAT_CONTEXT","Для кода нужны taskId и sourceCode");if(editorSource.length()>16_000)throw bad("EDITOR_SOURCE_TOO_LONG","Код в редакторе длиннее 16 000 символов");long requestedTaskId;try{requestedTaskId=requestedTask instanceof Number n?n.longValue():Long.parseLong((String)requestedTask);}catch(RuntimeException e){throw bad("INVALID_CHAT_CONTEXT","taskId должен быть числом");}var current=unsolvedTask(l);if(current==null||requestedTaskId!=((Number)current.get("id")).longValue())throw bad("CHAT_TASK_MISMATCH","Код относится не к текущей задаче урока");}var quota=llmSettings.chatQuota(u);if(!quota.allowed()){log.info("Chat message of student {} rejected by rate limit (hour {}/{}, day {}/{})",u,quota.hourUsed(),quota.hourLimit(),quota.dayUsed(),quota.dayLimit());return ResponseEntity.status(429).header("Retry-After",String.valueOf(quota.retryAfterSeconds())).body(Map.of("error","LLM_RATE_LIMITED","message",rateLimitMessage(quota),"quota",quota.view()));}db.update("insert into chat_messages(lesson_id,role,content) values(?,?,?)",l.get("id"),"STUDENT",question);try {String answer=tutor.reply(u,tutorContext(lang,l,editorSource),question);long id=db.queryForObject("insert into chat_messages(lesson_id,role,content) values(?,?,?) returning id",Long.class,l.get("id"),"ASSISTANT",answer);return ResponseEntity.ok(Map.of("message",Map.of("id",id,"role","ASSISTANT","content",answer,"createdAt",Instant.now().toString()),"llm",llm(u),"quota",llmSettings.chatQuota(u).view()));}catch(LlmUnavailableException e){return ResponseEntity.status(503).body(Map.of("error","LLM_UNAVAILABLE","message",e.getMessage(),"llm",llm(u)));}}

  @PostMapping("/admin/students") public Map<String,Object> createStudent(@RequestBody Map<String,Object>b,HttpServletRequest r){admin(r);String login=(String)b.get("login"),password=(String)b.get("password"),name=(String)b.get("displayName");if(login==null||password==null||name==null)throw bad("INVALID_STUDENT","Нужны login, password, displayName");boolean enabled=!Boolean.FALSE.equals(b.get("llmEnabled"));if(count("select count(*) from users where login=?",login.trim())>0)throw bad("LOGIN_TAKEN","Логин «"+login.trim()+"» уже занят");validatePassword(password);db.update("insert into users(login,password_hash,role,display_name,llm_enabled) values(?,?,?,?,?)",login.trim(),passwords.encode(password),"STUDENT",name.trim(),enabled?1:0);login=login.trim();var created=db.queryForMap("select id,login,role,display_name as displayName,llm_enabled as llmEnabled from users where login=?",login);LogContext.student(created.get("id"),login);log.info("Created student account login={}",login);return created;}
  /** Students with their open lessons, so the teacher sees at a glance who is studying right now. */
  @GetMapping("/admin/students") public Map<String,Object> students(HttpServletRequest r){
    admin(r);
    var students=db.queryForList("select id,login,display_name as displayName,llm_enabled as llmEnabled,created_at as createdAt from users where role='STUDENT' order by id");
    var open=db.queryForList("select user_id,language,coalesce(language_lesson_number,lesson_number) as number,started_at as startedAt from lessons where finished_at is null order by started_at");
    for(var student:students){ var mine=new ArrayList<Map<String,Object>>(); for(var lesson:open) if(lesson.get("user_id").equals(student.get("id"))) mine.add(Map.of("language",lesson.get("language"),"number",lesson.get("number"),"startedAt",lesson.get("startedAt"))); student.put("activeLessons",mine); }
    return Map.of("students",students);
  }

  /** Reasoning levels per purpose and LLM rate limits; options come from the model when the App Server can tell. */
  @GetMapping("/admin/llm/settings") public Map<String,Object> llmSettings(HttpServletRequest r){ admin(r); return settingsView(); }
  @PutMapping("/admin/llm/settings") public Map<String,Object> updateLlmSettings(@RequestBody Map<String,Object> body,HttpServletRequest r){
    admin(r);
    @SuppressWarnings("unchecked") Map<String,String> efforts=(Map<String,String>)body.get("reasoning");
    Map<String,Integer> limits=null;
    if(body.get("limits") instanceof Map<?,?> raw){ limits=new LinkedHashMap<>(); for(var e:raw.entrySet()) limits.put((String)e.getKey(),e.getValue() instanceof Number n?n.intValue():null); }
    @SuppressWarnings("unchecked") Map<String,String> models=(Map<String,String>)body.get("models");
    Map<String,Boolean> logging=null;
    if(body.get("logging") instanceof Map<?,?> raw){ logging=new LinkedHashMap<>(); for(var e:raw.entrySet()) logging.put((String)e.getKey(),e.getValue() instanceof Boolean v?v:null); }
    var offered=offeredModels();
    var before=llmSettings.models();
    llmSettings.update(models,efforts,limits,logging,offered.stream().map(ModelOption::id).collect(java.util.stream.Collectors.toSet()),id->effortsOf(offered,id));
    log.info("LLM settings changed by admin {}: models={} (was {}) reasoning={} limits={} logging={}",uid(r),llmSettings.models(),before,llmSettings.efforts(),llmSettings.limits(),llmSettings.logging());
    return settingsView();
  }
  /** Levels of a model as the App Server reports them; the safe fallback when it does not. */
  private static List<String> effortsOf(List<ModelOption> models,String id){ return models.stream().filter(m->m.id().equals(id)).findFirst().map(ModelOption::efforts).filter(e->!e.isEmpty()).orElse(LlmSettings.FALLBACK_EFFORTS); }
  private List<String> effortOptions(){ var fromModel=tutor.supportedReasoningEfforts(); return fromModel==null||fromModel.isEmpty()?LlmSettings.FALLBACK_EFFORTS:fromModel; }
  private Map<String,Object> settingsView(){
    var fromModel=tutor.supportedReasoningEfforts();
    var models=offeredModels();
    return obj("purposeModels",llmSettings.models(),"purposeModelDefaults",llmSettings.defaultModels(),"logging",llmSettings.logging(),"loggingDefaults",llmSettings.defaultLogging(),
        "models",models.stream().map(ModelOption::view).toList(),"reasoning",llmSettings.efforts(),"reasoningDefaults",llmSettings.defaultEfforts(),"reasoningOptions",effortOptions(),"reasoningOptionsFromModel",fromModel!=null&&!fromModel.isEmpty(),
        "limits",llmSettings.limits(),"limitDefaults",llmSettings.defaultLimits(),"usageLastHour",Map.of("tasks",llmSettings.tasksLastHour(),"explanations",llmSettings.explanationsLastHour()));
  }
  /**
   * The App Server's own list, plus configured extra models it did not report (safe reasoning levels, marked as
   * unconfirmed), plus the current model so it is always visible.
   */
  private List<ModelOption> offeredModels(){
    var listed=tutor.availableModels()==null?List.<ModelOption>of():tutor.availableModels();
    var all=new ArrayList<>(listed);
    var extras=new ArrayList<>(llmSettings.extraModels()); for(String current:llmSettings.models().values()) if(!extras.contains(current))extras.add(current);
    for(String id:extras) if(all.stream().noneMatch(m->m.id().equals(id)))
      all.add(new ModelOption(id,prettyModelName(id),"",LlmSettings.FALLBACK_EFFORTS,"medium",false));
    return all;
  }
  /** gpt-5.6-terra → GPT-5.6-Terra, the way the App Server names its models. */
  static String prettyModelName(String id){
    var parts=new ArrayList<String>();
    for(String part:id.split("-")) parts.add(part.equalsIgnoreCase("gpt")?"GPT":part.isEmpty()?part:Character.toUpperCase(part.charAt(0))+part.substring(1));
    return String.join("-",parts);
  }
  private static String rateLimitMessage(LlmSettings.ChatQuota q){
    long minutes=Math.max(1,(q.retryAfterSeconds()+59)/60);
    String wait=minutes<60?minutes+" мин.":(minutes+59)/60+" ч.";
    String which=q.hourLimit()>0&&q.hourUsed()>=q.hourLimit()?q.hourLimit()+" в час":q.dayLimit()+" в сутки";
    return "Лимит сообщений помощнику — "+which+". Следующее сообщение можно отправить через "+wait;
  }
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
  /**
   * Deletes a student and everything that belongs only to them: sessions, diagnostic, lessons with their submissions
   * and chat, progress and credit. Shared content (tasks, explanations) stays. LLM usage rows stay for analytics but
   * lose the link to the person. Irreversible, so the client must send the student's login as confirmation.
   */
  @DeleteMapping("/admin/students/{id}") @Transactional public Map<String,Object> deleteStudent(@PathVariable long id,@RequestBody(required=false) Map<String,String> b,HttpServletRequest r){
    admin(r);
    var rows=db.queryForList("select login,display_name from users where id=? and role='STUDENT'",id);
    if(rows.isEmpty())throw bad("STUDENT_NOT_FOUND","Студент не найден");
    String login=(String)rows.getFirst().get("login");
    if(b==null||!login.equals(b.get("confirmLogin")))throw bad("CONFIRMATION_REQUIRED","Для удаления введите логин студента");
    String lessons="(select id from lessons where user_id=?)";
    int submissions=db.update("delete from submissions where lesson_id in "+lessons,id);
    int messages=db.update("delete from chat_messages where lesson_id in "+lessons,id);
    db.update("delete from lesson_tasks where lesson_id in "+lessons,id);
    db.update("delete from skill_iterations where user_id=? or lesson_id in "+lessons,id,id);
    int lessonCount=db.update("delete from lessons where user_id=?",id);
    db.update("update submissions set revoked_by=null where revoked_by=?",id);
    for(String table:List.of("pending_redos","successful_task_credit","student_skills","diagnostic_answers","diagnostic_skill_results","student_languages","sessions"))
      db.update("delete from "+table+" where user_id=?",id);
    int llmCalls=db.update("update llm_calls set user_id=null where user_id=?",id);
    db.update("delete from users where id=?",id);
    log.info("Student account {} ({}) deleted by admin {}: {} lessons, {} submissions, {} chat messages removed; {} LLM usage rows kept without the user",id,login,uid(r),lessonCount,submissions,messages,llmCalls);
    return obj("id",id,"lessons",lessonCount,"submissions",submissions,"chatMessages",messages);
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
    var byPurpose=db.queryForList("select c.purpose,max(c.reasoning_effort) as effort,(select x.model from llm_calls x where x.purpose=c.purpose and x.created_at>=datetime('now',?) order by x.id desc limit 1) as model,count(*) as calls,coalesce(sum(c.status<>'OK'),0) as errors,coalesce(round(avg(case when c.status='OK' then c.duration_ms end)),0) as avgMs,coalesce(sum(c.total_tokens),0) as tokens"+where+" group by c.purpose order by calls desc",since,since);
    var byLanguage=db.queryForList("select c.language,count(*) as calls,coalesce(sum(c.total_tokens),0) as tokens"+where+" group by c.language order by calls desc",since);
    var byStudent=db.queryForList("select c.user_id as userId,coalesce(u.display_name,'—') as displayName,u.login,count(*) as calls,coalesce(sum(c.purpose='CHAT'),0) as chatTurns,coalesce(sum(c.status<>'OK'),0) as errors,coalesce(sum(c.total_tokens),0) as tokens,max(c.created_at) as lastAt from llm_calls c left join users u on u.id=c.user_id where c.created_at>=datetime('now',?) group by c.user_id order by calls desc limit 100",since);
    var errors=db.queryForList("select c.created_at as createdAt,c.purpose,c.language,c.status,c.error,c.duration_ms as durationMs,u.display_name as displayName from llm_calls c left join users u on u.id=c.user_id where c.created_at>=datetime('now',?) and c.status<>'OK' order by c.created_at desc,c.id desc limit 20",since);
    return obj("days",period,"totals",totals,"byDay",byDay,"byPurpose",byPurpose,"byLanguage",byLanguage,"byStudent",byStudent,"recentErrors",errors,"llm",llm(uid(r)));
  }
  @GetMapping("/admin/students/{id}") public Map<String,Object> student(@PathVariable long id,HttpServletRequest r){admin(r);var s=db.queryForMap("select id,login,display_name as displayName,llm_enabled as llmEnabled from users where id=? and role='STUDENT'",id);var byLanguage=new LinkedHashMap<String,Object>();for(Language lang:Language.values())byLanguage.put(lang.name(),progress(id,lang));return Map.of("student",s,"progress",progress(id,Language.JAVA),"progressByLanguage",byLanguage,"llm",llm(id));}
  @GetMapping("/admin/students/{id}/lessons") public Map<String,Object> lessons(@PathVariable long id,HttpServletRequest r){admin(r);return Map.of("lessons",db.queryForList("select id,coalesce(language_lesson_number,lesson_number) as number,language,started_at as startedAt,finished_at as finishedAt from lessons where user_id=? order by lesson_number",id));}
  /** The same as the student's own «Завершить урок», for any student's open lesson. */
  @PostMapping("/admin/students/{id}/lessons/{lessonId}/finish") public Map<String,Object> finishStudentLesson(@PathVariable long id,@PathVariable long lessonId,HttpServletRequest r){
    admin(r);
    if(!finishLesson(id,lessonId))throw bad("LESSON_NOT_ACTIVE","Активный урок не найден");
    log.info("Lesson {} of student {} finished by admin {}",lessonId,id,uid(r));
    return Map.of("lesson",lesson(lessonId));
  }

  /**
   * Cancels an accepted solution: the student has to solve the task again. Accepted submissions in this lesson are
   * kept in history but marked revoked and stop counting as passed; the task credit is removed and the progress of
   * its skills is recomputed by replaying the normal crediting rules over the remaining credited lessons. The task
   * comes back first: it is unsolved again in an open lesson, otherwise it is assigned at the start of the next one.
   */
  @PostMapping("/admin/students/{id}/lessons/{lessonId}/tasks/{taskId}/revoke") @Transactional public Map<String,Object> revokeTask(@PathVariable long id,@PathVariable long lessonId,@PathVariable long taskId,HttpServletRequest r){
    admin(r);
    var lessonRows=db.queryForList("select finished_at,language from lessons where id=? and user_id=?",lessonId,id);
    if(lessonRows.isEmpty())throw bad("LESSON_NOT_FOUND","Урок не найден");
    int revoked=db.update("update submissions set passed=0,revoked_at=?,revoked_by=? where lesson_id=? and task_id=? and passed=1",Instant.now().toString(),uid(r),lessonId,taskId);
    if(revoked==0)throw bad("NOTHING_TO_REVOKE","У этой задачи нет принятого решения в уроке");
    db.update("delete from successful_task_credit where user_id=? and task_id=?",id,taskId);
    var skills=db.queryForList("select skill_code from task_target_skills where task_id=?",String.class,taskId);
    for(String skill:skills) replayProgress(id,skill);
    boolean openLesson=lessonRows.getFirst().get("finished_at")==null;
    if(!openLesson) db.update("insert or ignore into pending_redos(user_id,task_id) values(?,?)",id,taskId);
    log.info("Admin {} revoked accepted task {} of student {} in lesson {} ({} submission(s)); skills {} recalculated",uid(r),taskId,id,lessonId,revoked,skills);
    return obj("revokedSubmissions",revoked,"skills",skills,"redoInOpenLesson",openLesson);
  }

  /**
   * Rebuilds one skill's practice progress from the credited solutions that remain, lesson by lesson, with the same
   * credit() rules that produced it. Diagnostic confirmation is separate and untouched.
   */
  /** A task sent back during a lesson and not solved before the lesson ended must not get lost: it moves to the redo queue. */
  private void queueUnsolvedRedos(long user,long lessonId){
    db.update("insert or ignore into pending_redos(user_id,task_id) select ?,lt.task_id from lesson_tasks lt where lt.lesson_id=? "
        +"and exists(select 1 from submissions s where s.lesson_id=lt.lesson_id and s.task_id=lt.task_id and s.revoked_at is not null) "
        +"and not exists(select 1 from submissions s where s.lesson_id=lt.lesson_id and s.task_id=lt.task_id and s.passed=1)",user,lessonId);
  }
  private void replayProgress(long user,String skill){
    db.update("delete from skill_iterations where user_id=? and skill_code=?",user,skill);
    db.update("update student_skills set completed_iterations=0,iteration_successes=0,first_iteration_lesson_number=null,mastered=0 where user_id=? and skill_code=?",user,skill);
    var lessons=db.queryForList("select distinct l.id,coalesce(l.language_lesson_number,l.lesson_number) as number from lessons l join submissions s on s.lesson_id=l.id and s.passed=1 join successful_task_credit c on c.task_id=s.task_id and c.user_id=l.user_id join task_target_skills ts on ts.task_id=s.task_id and ts.skill_code=? where l.user_id=? order by number",skill,user);
    for(var l:lessons) credit(user,skill,((Number)l.get("id")).longValue(),((Number)l.get("number")).intValue());
  }

  @GetMapping("/admin/students/{id}/lessons/{lessonId}") public Map<String,Object> lessonDetail(@PathVariable long id,@PathVariable long lessonId,HttpServletRequest r){admin(r);var l=db.queryForMap("select id,coalesce(language_lesson_number,lesson_number) as number,language,started_at as startedAt,finished_at as finishedAt from lessons where id=? and user_id=?",lessonId,id);var tasks=db.queryForList("select t.id,t.title,t.statement from tasks t join lesson_tasks x on x.task_id=t.id where x.lesson_id=?",lessonId);for(var t:tasks)t.put("submissions",db.queryForList("select id,source_code as sourceCode,passed,runner_output as output,created_at as createdAt,revoked_at as revokedAt from submissions where lesson_id=? and task_id=? order by id",lessonId,t.get("id")));return Map.of("lesson",l,"chat",db.queryForList("select id,role,content,created_at as createdAt from chat_messages where lesson_id=? order by id",lessonId),"tasks",tasks);}

  private TutorContext tutorContext(Language lang,Map<String,Object> lesson,String currentEditorSource) { long lessonId=((Number)lesson.get("id")).longValue(); var taskRows=db.queryForList("select t.id,t.title,t.statement,ts.skill_code from lesson_tasks lt join tasks t on t.id=lt.task_id join task_target_skills ts on ts.task_id=t.id where lt.lesson_id=? and t.active=1 and not exists(select 1 from submissions x where x.lesson_id=lt.lesson_id and x.task_id=lt.task_id and x.passed=1) order by lt.rowid desc limit 1",lessonId); String skillCode=null,skillTitle=null; Long taskId=null;String taskTitle=null,taskStatement=null,source=null,output=null;Boolean passed=null; if(!taskRows.isEmpty()){var task=taskRows.getFirst();taskId=((Number)task.get("id")).longValue();taskTitle=(String)task.get("title");taskStatement=(String)task.get("statement");skillCode=(String)task.get("skill_code");var titleRows=db.queryForList("select title from skills where code=?",skillCode);skillTitle=titleRows.isEmpty()?skillCode:(String)titleRows.getFirst().get("title");var submission=db.queryForList("select source_code,passed,runner_output from submissions where lesson_id=? and task_id=? order by id desc limit 1",lessonId,taskId);if(!submission.isEmpty()){var last=submission.getFirst();source=(String)last.get("source_code");passed=((Number)last.get("passed")).intValue()==1;output=(String)last.get("runner_output");}} return new TutorContext(lang,lessonId,((Number)lesson.get("number")).intValue(),skillCode,skillTitle,taskId,taskTitle,taskStatement,currentEditorSource,source,passed,output); }
  private Map<String,Object> status(Map<String,Object> u){return Map.of("user",viewUser(u),"llm",llm(((Number)u.get("id")).longValue()),"runner",runner(Language.JAVA));} private Map<String,Object> viewUser(Map<String,Object> u){return Map.of("id",u.get("id"),"login",u.get("login"),"role",u.get("role"),"displayName",u.get("display_name"),"llmEnabled",u.get("llm_enabled"));}
  private Map<String,Object> llm(long id){return tutor.status(id).asMap();} private Map<String,Object> runner(Language lang){var state=codeRunner.status(lang);return obj("available",state.available(),"reason",state.reason(),"language",lang.name(),"version",state.version());}
  /** Practice progress and, separately, the diagnostic result per topic. A confirmed topic is not shown as practiced. */
  private List<Map<String,Object>> progress(long u,Language lang){return db.queryForList("select s.code as skillCode,s.title,s.block_no as blockNo,coalesce(x.completed_iterations,0) as completedIterations,coalesce(x.iteration_successes,0) as iterationSuccesses,coalesce(x.mastered,0) as mastered,d.correct as diagnosticCorrect,d.total as diagnosticTotal,coalesce(d.confirmed,0) as confirmedByDiagnostic from skills s left join student_skills x on x.skill_code=s.code and x.user_id=? left join diagnostic_skill_results d on d.skill_code=s.code and d.user_id=? where s.language=? order by s.sort_order",u,u,lang.name());}
  private void credit(long user,String skill,long lessonId,int lessonNumber){db.update("insert or ignore into student_skills(user_id,skill_code) values(?,?)",user,skill);int successes=count("select count(distinct c.task_id) from successful_task_credit c join task_target_skills ts on ts.task_id=c.task_id join submissions s on s.task_id=c.task_id and s.lesson_id=? and s.passed=1 where c.user_id=? and ts.skill_code=?",lessonId,user,skill);if(successes<3){db.update("update student_skills set iteration_successes=? where user_id=? and skill_code=?",successes,user,skill);return;}var x=db.queryForMap("select completed_iterations,first_iteration_lesson_number from student_skills where user_id=? and skill_code=?",user,skill);int completed=((Number)x.get("completed_iterations")).intValue();Integer first=x.get("first_iteration_lesson_number")==null?null:((Number)x.get("first_iteration_lesson_number")).intValue();boolean due=completed==0||(completed==1&&lessonNumber==first+1)||(completed==2&&lessonNumber==first+3);if(!due||count("select count(*) from skill_iterations where user_id=? and skill_code=? and lesson_id=?",user,skill,lessonId)>0)return;int done=completed+1;db.update("insert into skill_iterations(user_id,skill_code,iteration_number,lesson_id) values(?,?,?,?)",user,skill,done,lessonId);db.update("update student_skills set completed_iterations=?,iteration_successes=0,first_iteration_lesson_number=case when first_iteration_lesson_number is null then ? else first_iteration_lesson_number end,mastered=? where user_id=? and skill_code=?",done,lessonNumber,done>=3?1:0,user,skill);}
  /**
   * Picks one skill and keeps the student on it: an iteration already started in this lesson is finished first,
   * then scheduled repetitions (iterations 2 and 3 are only valid on their lesson), then new topics in course order.
   */
  /**
   * Topics that still need practice: not mastered and not confirmed by the diagnostic, in course order. The diagnostic
   * decides per topic, so a strong block no longer hides a weak topic inside it, and a fully confirmed course has nothing to start.
   */
  private static final String NEEDS_PRACTICE="coalesce(x.mastered,0)=0 and not exists(select 1 from diagnostic_skill_results d where d.user_id=x2.uid and d.skill_code=s.code and d.confirmed=1)";
  private int remainingTopics(long userId,Language lang){return count("select count(*) from skills s cross join (select ? as uid) x2 left join student_skills x on x.skill_code=s.code and x.user_id=x2.uid where s.language=? and "+NEEDS_PRACTICE,userId,lang.name());}
  private Map<String,Object> nextSkill(long userId,Language lang,int lessonNumber,long lessonId) {
    var rows=db.queryForList("select s.code,s.title,s.block_no,coalesce(x.completed_iterations,0) completed,coalesce(x.first_iteration_lesson_number,0) first from skills s cross join (select ? as uid) x2 left join student_skills x on x.skill_code=s.code and x.user_id=x2.uid where s.language=? and "+NEEDS_PRACTICE+" and (s.prerequisite_code is null or exists(select 1 from student_skills p where p.user_id=x2.uid and p.skill_code=s.prerequisite_code and p.mastered=1)) order by s.block_no,s.sort_order",userId,lang.name());
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
