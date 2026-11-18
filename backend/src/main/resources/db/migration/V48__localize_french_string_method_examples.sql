-- This explanation contains standalone teaching examples. Change each example
-- together with its labels, discussion and printed output.
WITH RECURSIVE
lesson(source_hash) AS (
    VALUES ('64b6811b8cdab9ee150d672ac89dc0fa02d9bf60ee9fc0644501fde147dd33e6')
),
terms(step, original, french) AS (
    VALUES
        (1, 'строка', 'chaine'),
        (2, 'метод', 'methode'),
        (3, 'аргументы', 'arguments'),
        (4, 'старый_фрагмент', 'ancien_texte'),
        (5, 'новый_фрагмент', 'nouveau_texte'),
        (6, 'Привет', 'Bonjour'),
        (7, 'привет', 'bonjour'),
        (8, 'кот', 'chat'),
        (9, 'пёс', 'chien'),
        (10, 'Я люблю чай', 'Je bois du thé'),
        (11, 'Я люблю какао', 'Je bois du cacao'),
        (12, 'text = "чай"', 'text = "jour"'),
        (13, 'чай', 'thé'),
        (14, 'какао', 'cacao'),
        (15, '"ч"', '"j"'),
        (16, '"д"', '"t"'),
        (17, 'дай', 'tour'),
        (18, 'да', 'oui')
),
revised(step, body) AS (
    SELECT 0, translated_text FROM content_translations
    WHERE source_hash = (SELECT source_hash FROM lesson) AND locale = 'fr' AND kind = 'explanation'
    UNION ALL
    SELECT terms.step, replace(revised.body, terms.original, terms.french)
    FROM revised JOIN terms ON terms.step = revised.step + 1
)
UPDATE content_translations
SET translated_text = (SELECT body FROM revised ORDER BY step DESC LIMIT 1)
WHERE source_hash = (SELECT source_hash FROM lesson) AND locale = 'fr' AND kind = 'explanation';
