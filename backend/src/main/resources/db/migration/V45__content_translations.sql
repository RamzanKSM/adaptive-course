-- Only reviewed translations belong here. The hash ties each translation to the exact source text.
CREATE TABLE content_translations (
    source_hash TEXT NOT NULL,
    kind TEXT NOT NULL,
    locale TEXT NOT NULL CHECK (locale IN ('fr', 'ar-SD')),
    translated_text TEXT NOT NULL,
    PRIMARY KEY (source_hash, locale, kind)
);
