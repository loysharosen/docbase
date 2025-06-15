CREATE TABLE IF NOT EXISTS docs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    abbreviation VARCHAR(30),
    description VARCHAR(255) NOT NULL,
    keywords VARCHAR(255),
    date_added TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Stockholm')
);

CREATE TABLE IF NOT EXISTS links (
    id SERIAL PRIMARY KEY,
    doc_id INTEGER NOT NULL,
    docbase_link TEXT,
    source_link TEXT,
    votes INTEGER DEFAULT 0,
    date_added TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Stockholm'),
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS search_logs (
    id SERIAL PRIMARY KEY,
    search_phrase VARCHAR(255) NOT NULL,
    results_count INTEGER NOT NULL,
    search_time TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Stockholm')
);