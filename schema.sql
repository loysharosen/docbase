CREATE TABLE docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    abbreviation TEXT,
    description TEXT NOT NULL,
    keywords TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER NOT NULL,
    docbase_link TEXT,
    source_link TEXT,
    votes INTEGER DEFAULT 0,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE
);

CREATE TABLE search_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_phrase VARCHAR(255) NOT NULL,
    results_count INTEGER NOT NULL,
    search_time DATE DEFAULT (datetime('now','localtime'))
);