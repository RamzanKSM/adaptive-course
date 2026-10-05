# Rmzn Tutor backend (Java и Python)

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

Piston остаётся без опубликованного порта и запускается privileged, поэтому его нельзя открывать напрямую в интернет. LLM остаётся выключенной и fail-closed по умолчанию. На `course.rmzn.net` она включена только явными переменными `.env` после проверки sandbox; это opt-in конфигурация развёртывания, а не изменение безопасных дефолтов образа.

Для VPS с 4 GB RAM Compose ограничивает backend до 768 MB, Piston до 2 GB и оставляет память ОС и reverse proxy. Piston одновременно запускает не больше двух jobs. Лимиты одного запуска Java заданы отдельно: 256 MB на компиляцию и 128 MB на выполнение. Образ Piston зафиксирован официальным immutable digest, а не подвижным `latest`; обновление образа требует отдельной проверки и изменения Compose. Перед сборкой или обновлением проверьте свободное место командой `df -h /`, Docker cache и volumes — через `docker system df`, а заполнение логов — отдельно; очистка cache или данных выполняется только отдельной осознанной операцией.

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

Только после второй команды отправка Java-решения сможет пройти Piston.

Для курса Python так же один раз установите Python runtime (рекомендуется 3.12) и проверьте его:

```sh
docker run --rm --network adaptive-course_default \
  -v "$PWD/.piston-cli/cli:/cli" -w /cli node:22-bookworm \
  sh -lc 'node index.js -u http://piston:2000 ppman install python=3.12.0'
docker run --rm --network adaptive-course_default \
  -v "$PWD/.piston-cli/cli:/cli" -w /cli node:22-bookworm \
  sh -lc 'node index.js -u http://piston:2000 ppman list | grep "^python"'
```

Если установлено несколько версий Python, backend берёт самую новую; конкретную можно закрепить переменной `PISTON_PYTHON_VERSION`. Пока Python runtime не установлен, курс Python работает, но проверка решений возвращает «проверка недоступна» (`PISTON_PYTHON_NOT_INSTALLED`), а генерация новых задач Python не запускается. `.piston-cli` — локальная служебная папка, её можно удалить после установки. API runtimes можно проверить из backend network запросом `GET http://piston:2000/api/v2/runtimes`. Инструкция основана на [официальном Piston README](https://github.com/engineer-man/piston).

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

### Логи

Backend пишет в stdout (его видно через `docker compose logs -f backend`). Каждая строка содержит `requestId` и `user`, поэтому все записи одного запроса — HTTP, LLM, проверка решения — легко собрать вместе; `requestId` также возвращается клиенту в заголовке `X-Request-Id`.

- На каждый API-запрос — строка `GET /api/... -> 200 in 35 ms`.
- На каждое обращение к LLM — начало (назначение `CHAT`/`TASK`/`EXPLANATION`, курс, навык, размер промпта) и итог: длительность, токены (вход, кэш, выход, reasoning), размер ответа или причина ошибки/таймаута. Запуск и падение Codex App Server, создание и возобновление thread тоже логируются.
- Генерация задач: каждая попытка и точная причина, по которой задача отклонена (например, «reference solution failed its own checks» или «statement mentions platform internals»).
- Отправки решений: задача, курс, результат и время проверки.

Переменные:

- `APP_LOG_LEVEL` — уровень логов приложения (`INFO` по умолчанию, `DEBUG` добавляет служебные события Codex).
- `APP_LLM_LOG_CONTENT=true` — дополнительно писать полный текст промптов и ответов LLM. В них есть сообщения и код студентов, поэтому включайте только на время отладки.
- `APP_LOG_FILE` — путь к файлу логов в дополнение к stdout, например `/app/data/logs/app.log` (ротация по 20 МБ, 14 файлов).

Все обращения к LLM также сохраняются в таблицу `llm_calls`; по ней строится раздел «Аналитика LLM» в админке.

### Два курса: Java и Python

Курсы независимы: у каждого своя диагностика, навыки (коды Python начинаются с `PY_`), уроки с собственной нумерацией и расписанием итераций, прогресс и отдельный thread учебного помощника со своим промптом. Студент выбирает курс сам и может переключаться в любой момент; ограничений доступа нет. Студенческие endpoint'ы принимают `?language=JAVA|PYTHON` (без параметра — Java, как раньше).

Задачи Python проверяются так: студент пишет `solution.py`, скрытые проверки лежат в `test_solution.py` и определяют `run_checks()`, а фиксированная точка входа `main.py` получает секретный маркер успеха через stdin до импорта решения и печатает его, только если `run_checks()` завершилась без исключений. Поэтому маркер не лежит ни в одном файле, который может прочитать код студента.

`APP_PYTHON_DIAGNOSTIC_SOURCE` указывает на диагностику Python (по умолчанию соседний `../python_initial_diagnostic_mvp.md`, в Docker-образе — `/app/python_initial_diagnostic_mvp.md`). Вопросы импортируются при старте, если вопросов Python в базе ещё нет, поэтому уже работающая база получит курс Python после обновления без ручных шагов.

`APP_DIAGNOSTIC_SOURCE` указывает на исходный Markdown диагностики. По умолчанию это соседний `../java_initial_diagnostic_mvp_v2.md`; приложение импортирует вопросы в пустую БД. Этот файл остаётся источником данных и должен быть доступен при первом запуске.

`PISTON_BASE_URL` задаёт URL собственного Piston. Без него отправка решения возвращает `503`; успешный результат не имитируется.

LLM выключена по умолчанию. Адаптер использует один дочерний процесс `codex --disable shell_tool app-server --listen stdio://`, persistent thread в `student_languages` и последовательные turns одного студента. Образ фиксирует Codex CLI `0.159.3`. Без `APP_LLM_ENABLED=true` и `APP_LLM_STUDENT_RUNTIME_VALIDATED=true` чат остаётся **fail-closed** со статусом `STUDENT_RUNTIME_NOT_VALIDATED`; в текущем явно настроенном развёртывании `course.rmzn.net` оба условия прошли проверку sandbox и LLM включена.

Причина: `readOnly` sandbox разрешает чтение, поэтому сам по себе не защищает `auth.json`. Entrypoint копирует управляемый приложением [профиль `student-tutor`](codex-config.toml) в persistent `CODEX_HOME/config.toml`, не затрагивая `auth.json`. Профиль запрещает `:root` и `/app/codex-home`, разрешает только `:minimal` на чтение и отключает сеть. App Server запрашивает этот профиль в `thread/start` и `turn/start`, а `initialize` включает `capabilities.experimentalApi=true`. Перед установкой `APP_LLM_STUDENT_RUNTIME_VALIDATED=true` для нового Linux runtime оператор обязан доказать, что студентский turn не может прочитать `CODEX_HOME/auth.json` и пути вне sandbox. Эта проверка выполнена для текущего `course.rmzn.net`; в другом окружении её нужно повторить. До этого флага вопросы студентов в App Server не передаются.

Модель по умолчанию — `CODEX_MODEL=gpt-6-luna`, уровень размышлений — `CODEX_REASONING_EFFORT=medium`. Уровень передаётся в каждый `turn/start`, включая продолжение существующего диалога. `CODEX_APP_SERVER_COMMAND` позволяет указать другой путь к CLI, но должен запускать App Server с transport `stdio://`; не убирайте `--disable shell_tool` без отдельной проверки безопасности.

### Авторизация Codex и смена аккаунта

Для включённого deployment остановите backend и на том же хосте (либо внутри контейнера с тем же persistent `CODEX_HOME`) выполните вручную:

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

На `course.rmzn.net` пользовательская авторизация используется через этот явный opt-in путь с persistent `codex-home`; при переносе на другой сервер нужно повторить проверку sandbox до включения student runtime. Официальные команды: [OpenAI Codex CLI reference](https://developers.openai.com/codex/cli/reference).

## Осознанные границы первого среза

Есть девять seed-задач и объяснение для `BASIC_CODE_READING` («Вывод в консоль»). Студент дописывает `Solution.main(String[] args)` и использует `System.out.print/println`; скрытый harness запускает `main`, захватывает stdout, восстанавливает `System.out` и сравнивает точный вывод. Старые задачи на предсказание вывода деактивируются при импорте: их идентификаторы, попытки и зачёты остаются в базе, но активный урок их пропускает. Их достаточно для трёх итераций первого навыка при настроенном Piston. Диагностика определяет начальный блок; semantic prerequisite graph в исходных материалах не задан, поэтому `prerequisite_code` пока пустой и готов для заполнения авторами курса. Backend держит студента на одном навыке, пока итерация из трёх задач в уроке не закончена; затем берёт запланированные повторения (итерации 2 и 3), затем новые навыки строго по порядку курса. Внутри итерации задачи идут по сложности 1 → 2 → 3 (`tasks.difficulty`); если в банке нет задачи нужной ступени, при доступной LLM она генерируется, иначе берётся ближайшая по сложности. Объяснения, сгенерированные старой версией промпта (`explanations.prompt_version` < `EXPLANATION_PROMPT_VERSION`), перегенерируются при доступной LLM, а до этого показывается прежний текст.

При отсутствии подходящей задачи backend сначала вызывает `LearningContentGenerator`. Он принимает результат только с названием, условием, starter code, target skill IDs и непустым hidden Java harness, затем сохраняет его в общий банк. Если генератор отключён или не прошёл безопасную проверку App Server, задача не создаётся и API честно отвечает `NO_TASK_AVAILABLE`. При дефолтном fail-closed режиме студентский чат возвращает `503 LLM_UNAVAILABLE` и не запускает App Server; в явно включённом deployment он доступен после проверки sandbox.
