-- Earlier scratch seed titles are renamed so the idempotent importer replaces
-- their content instead of adding a second, misleading task bank.
UPDATE tasks SET title='Вывод строки' WHERE title='Верни приветствие';
UPDATE tasks SET title='Две строки' WHERE title='Верни число';
UPDATE tasks SET title='Число' WHERE title='Сложи два числа';
UPDATE tasks SET title='Символ' WHERE title='Верни true';
UPDATE tasks SET title='Логическое значение' WHERE title='Удвой число';
UPDATE tasks SET title='Склеенный вывод' WHERE title='Длина слова';
UPDATE tasks SET title='Пустая строка' WHERE title='Первый символ';
UPDATE tasks SET title='Число и текст' WHERE title='Большее число';
UPDATE tasks SET title='Три вывода' WHERE title='Чётное число';
