# Adaptive Java Tutor backend

Локальный MVP: Java 21, Spring Boot, SQLite, Flyway и JDBC. Запускать из этой папки:

```bash
JAVA_HOME=$(/usr/libexec/java_home -v 21) mvn package
java -jar target/adaptive-java-tutor-0.1.0.jar
```

## Локальный Docker запуск

Из папки `adaptive_course`:

```sh
cp .env.example .env
# задать непустой APP_BOOTSTRAP_ADMIN_PASSWORD в .env до запуска
docker compose up --build -d
```

Интерфейс будет доступен только с этого компьютера на `http://127.0.0.1:8080`. Compose не публикует Piston наружу: backend обращается к нему по внутреннему адресу `http://piston:2000`. `adaptive-data` хранит SQLite, а `codex-home` — авторизацию Codex и persistent rollout data; оба named volume переживают пересоздание backend container.

## Развёртывание на VPS

Compose намеренно публикует backend только на `127.0.0.1:8080`. На VPS перед ним нужен HTTPS reverse proxy, который принимает внешний трафик и проксирует его на этот loopback-адрес. Есть reviewable [фрагмент Caddyfile для `course.rmzn.net`](../deploy/Caddyfile.course): добавьте только этот фрагмент в существующий Caddyfile, не заменяя конфигурации других хостов. В рабочем `.env` задайте уникальный `APP_BOOTSTRAP_ADMIN_PASSWORD` и `APP_COOKIE_SECURE=true`: иначе защищённая cookie не будет передаваться браузером по HTTPS. `.env`, `codex-home`, SQLite и ключи сертификатов не добавляются в Git.

Для Codex `bwrap` backend использует [узкий custom seccomp profile](../deploy/seccomp/backend-bwrap.json). Его baseline — точный [Docker/Moby default profile `docker-v29.6.1`](https://raw.githubusercontent.com/moby/moby/docker-v29.6.1/vendor/github.com/moby/profiles/seccomp/default.json), сохранённый без изменений вне двух добавленных правил. Добавлены только `unshare`, `mount`, `umount2`, `pivot_root` и `clone` при флаге `CLONE_NEWUSER`; `seccomp=unconfined` не используется. На этом VPS нет AppArmor/SELinux, поэтому нельзя приписывать baseline отдельную защиту `socketcall` или AF_ALG: Docker 29.4.3 перенёс её на LSM. Это расширяет syscall surface backend container и требует одноразовой проверки bwrap на VPS. Если bwrap запросит другой syscall, его нужно подтвердить по deny log и добавить отдельно, не ослабляя профиль целиком.

Piston остаётся без опубликованного порта и запускается privileged, поэтому его нельзя открывать напрямую в интернет. LLM по умолчанию остаётся выключенной и fail-closed; пользовательская авторизация Codex App Server разрешена только для локального MVP, не для hosted-сервиса.

Для VPS с 4 GB RAM Compose ограничивает backend до 768 MB, Piston до 2 GB и оставляет память ОС и reverse proxy. Piston одновременно запускает не больше двух jobs. Лимиты одного запуска Java заданы отдельно: 256 MB на компиляцию и 128 MB на выполнение. Образ Piston зафиксирован официальным immutable digest, а не подвижным `latest`; обновление образа требует отдельной проверки и изменения Compose. Сейчас на VPS доступно 8.3 GB и Docker помечает 10.84 GB build cache как reclaimable. Этого достаточно, чтобы продолжить подготовку, но перед сборкой и обновлениями нужно проверять заполнение Docker volumes и логов. Очистка Docker cache или данных выполняется только отдельной осознанной операцией.

Piston запускается пустым: Java runtime нужно поставить один раз после запуска, затем проверить, что он виден API. Runtime хранится в named volume `piston-packages`. Образ API не содержит package-manager CLI, поэтому для установки нужен checkout официального Piston repository и временный Node-контейнер в той же Compose-сети:

```sh
git clone --depth 1 https://github.com/engineer-man/piston.git .piston-cli
docker run --rm --network adaptive-course_default \
  -v "$PWD/.piston-cli/cli:/cli" -w /cli node:22-bookworm \
  sh -lc 'npm ci && node index.js -u http://piston:2000 ppman install java'
docker run --rm --network adaptive-course_default \
  -v "$PWD/.piston-cli/cli:/cli" -w /cli node:22-bookworm \
  sh -lc 'node index.js -u http://piston:2000 ppman list | grep "^java"'
```

Только после второй команды отправка Java-решения сможет пройти Piston. `.piston-cli` — локальная служебная папка, её можно удалить после установки. API runtimes можно проверить из backend network запросом `GET http://piston:2000/api/v2/runtimes`. Инструкция основана на [официальном Piston README](https://github.com/engineer-man/piston).

На текущем официальном каталоге после установки доступен `java` версии `15.0.2`; это отдельный runtime Piston, а не Java 21, на которой работает backend. Поэтому задачи должны быть совместимы с Java 15 и не использовать синтаксис или API, появившиеся только в Java 16–21.

Codex CLI запускают отдельным одноразовым контейнером с **тем же** `codex-home` volume и тем же user, что у backend:

```sh
docker compose run --rm --no-deps backend codex logout
docker compose run --rm --no-deps backend codex login --device-auth
docker compose run --rm --no-deps backend codex login status
```

Для смены аккаунта сначала остановите backend: `docker compose stop backend`. Затем выполните три команды выше в указанном порядке: logout, device auth под новым ChatGPT/Codex-аккаунтом и status. После этого измените в `.env` на новое непустое значение `CODEX_ACCOUNT_NAMESPACE`, затем запустите backend. Старые remote thread ID могут быть недоступны новому аккаунту; локальная история уроков и чата в SQLite сохранится. Не печатайте и не копируйте `auth.json`; volume `codex-home` не попадает в Git.

При первом запуске задайте `APP_BOOTSTRAP_ADMIN_LOGIN` и `APP_BOOTSTRAP_ADMIN_PASSWORD`. Backend создаст единственного первого администратора с bcrypt-хешем пароля. Если в базе уже есть администратор, эти переменные игнорируются. Дефолтной учётной записи и пароля нет.

Чтобы начать локальный MVP с чистой базы и применить новые bootstrap-данные, остановите Compose и удалите только его named volumes:

```sh
docker compose down --volumes
docker compose up --build -d
```

Команда удаляет SQLite, `codex-home` и установленные Piston runtimes этого проекта; она не предназначена для уже нужных пользовательских данных.

`APP_DIAGNOSTIC_SOURCE` указывает на исходный Markdown диагностики. По умолчанию это соседний `../java_initial_diagnostic_mvp_v2.md`; приложение импортирует вопросы в пустую БД. Этот файл остаётся источником данных и должен быть доступен при первом запуске.

`PISTON_BASE_URL` задаёт URL собственного Piston. Без него отправка решения возвращает `503`; успешный результат не имитируется.

LLM выключена по умолчанию. Адаптер подготовлен для одного дочернего процесса `codex --disable shell_tool app-server --listen stdio://`, persistent thread в `student_languages` и последовательных turns одного студента. Образ фиксирует Codex CLI `0.159.3`. Чат студентов сейчас намеренно **fail-closed**: по умолчанию статус `STUDENT_RUNTIME_NOT_VALIDATED`, child process не запускается.

Причина: `readOnly` sandbox разрешает чтение, поэтому сам по себе не защищает `auth.json`. Entrypoint копирует управляемый приложением [профиль `student-tutor`](codex-config.toml) в persistent `CODEX_HOME/config.toml`, не затрагивая `auth.json`. Профиль запрещает `:root` и `/app/codex-home`, разрешает только `:minimal` на чтение и отключает сеть. App Server запрашивает этот профиль в `thread/start` и `turn/start`, а `initialize` включает `capabilities.experimentalApi=true`. Это настройка защиты, а не доказательство её действия: перед установкой `APP_LLM_STUDENT_RUNTIME_VALIDATED=true` оператор обязан на целевом Linux runtime доказать, что студентский turn не может прочитать `CODEX_HOME/auth.json` и пути вне sandbox. До этого флага вопросы студентов в App Server не передаются.

Модель по умолчанию — `CODEX_MODEL=gpt-6-luna`. `CODEX_APP_SERVER_COMMAND` позволяет указать другой путь к CLI, но должен запускать App Server с transport `stdio://`; не убирайте `--disable shell_tool` без отдельной проверки безопасности.

### Локальная авторизация и смена аккаунта

Если безопасный путь будет утверждён, остановите backend и на том же хосте (либо внутри контейнера с тем же persistent `CODEX_HOME`) выполните вручную:

```sh
codex logout
codex login --device-auth
codex login status
```

Device code нужно подтвердить под нужным ChatGPT-аккаунтом. `codex login status` подтверждает режим авторизации, но не личность аккаунта. В `.env` доступны `APP_LLM_ENABLED`, `APP_LLM_STUDENT_RUNTIME_VALIDATED`, `CODEX_MODEL=gpt-6-luna` и `CODEX_ACCOUNT_NAMESPACE`. Первые два значения остаются `false` по умолчанию. `APP_LLM_STUDENT_RUNTIME_VALIDATED=true` допустим только после проверки на целевом Linux, что студентский turn не может прочитать `CODEX_HOME/auth.json` или пути вне sandbox. Токены, `auth.json` и другие файлы авторизации не выводить и не добавлять в Git.

Для Docker `CODEX_HOME` должен переживать пересоздание контейнера и быть одинаковым для ручного входа и backend:

```yaml
services:
  backend:
    environment:
      CODEX_HOME: /app/codex-home
    volumes:
      - ./codex-home:/app/codex-home
```

Это пример локального запуска; `codex-home` содержит секреты и исключается из Git. Скрипта смены аккаунта в репозитории нет: переключение выполняется вручную указанными командами. Persistent thread нужен для `thread/resume`, поэтому `codex exec --ephemeral` здесь не подходит.

Пользовательскую авторизацию App Server нельзя использовать для hosted-сервиса, поэтому эта интеграция предназначена только для локального MVP. Официальные команды: [OpenAI Codex CLI reference](https://developers.openai.com/codex/cli/reference).

## Осознанные границы первого среза

Есть девять seed-задач и объяснение для `BASIC_CODE_READING`: это задания на точное предсказание вывода `System.out.print/println` с литералами. Их достаточно для трёх итераций первого навыка при настроенном Piston. Диагностика определяет начальный блок; semantic prerequisite graph в исходных материалах не задан, поэтому `prerequisite_code` пока пустой и готов для заполнения авторами курса. Backend выбирает самый ранний доступный блок и случайную задачу внутри него.

При отсутствии подходящей задачи backend сначала вызывает `LearningContentGenerator`. Он принимает результат только с названием, условием, starter code, target skill IDs и непустым hidden Java harness, затем сохраняет его в общий банк. Если генератор отключён или не прошёл безопасную проверку App Server, задача не создаётся и API честно отвечает `NO_TASK_AVAILABLE`. В текущем fail-closed режиме студентский чат также возвращает `503 LLM_UNAVAILABLE` и не запускает App Server.
