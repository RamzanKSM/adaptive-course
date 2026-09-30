package ru.teacherstaff.adaptive;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.annotation.Order;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

@Component @Order(1)
class AdminBootstrap implements ApplicationRunner {
  private final JdbcTemplate db; private final String login, password;
  AdminBootstrap(JdbcTemplate db,@Value("${app.bootstrap-admin-login}") String login,@Value("${app.bootstrap-admin-password}") String password){this.db=db;this.login=login;this.password=password;}
  @Override public void run(ApplicationArguments args) {
    if(db.queryForObject("select count(*) from users where role='ADMIN'",Integer.class)>0)return;
    if(login.isBlank()||password.isBlank())throw new IllegalStateException("Set APP_BOOTSTRAP_ADMIN_LOGIN and APP_BOOTSTRAP_ADMIN_PASSWORD before first startup");
    db.update("insert into users(login,password_hash,role,display_name) values(?,?,?,?)",login,new BCryptPasswordEncoder().encode(password),"ADMIN","Администратор");
  }
}
