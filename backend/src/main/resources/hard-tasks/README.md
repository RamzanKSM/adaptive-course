# Банк задач hard mode

`exercism.json` — алгоритмические задачи для hard mode по мотивам упражнений
[Exercism problem-specifications](https://github.com/exercism/problem-specifications) (лицензия MIT, см. `LICENSE-exercism`).

Для каждой задачи: условие на русском, заготовка, которая уже читает ввод, эталонные решения на Java и Python и тест-кейсы
«ввод → вывод». Кейсы взяты из `canonical-data.json` упражнения (`origin: exercism`); где их меньше шести, добавлены свои
(`origin: own`), их ответы посчитал эталон на Python. При сборке каждый эталон запускается на каждом кейсе, и его вывод
обязан совпасть с ответом Exercism — иначе банк не собирается.

Пересобрать:

```sh
git clone --depth 1 https://github.com/exercism/problem-specifications.git /tmp/ps
python3 tools/build_hard_bank.py /tmp/ps backend/src/main/resources/hard-tasks/exercism.json
```

Банк загружается при старте backend (`HardTaskBank`): задачи с ключом `exercism:<slug>:<язык>` создаются или обновляются.
