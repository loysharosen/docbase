.mode csv
.separator ";"

.import old.csv docs_temp

INSERT OR IGNORE INTO docs (name, abbreviation, description)
SELECT name, abbreviation, description FROM docs_temp;

INSERT INTO links (doc_id, docbase_link, source_link)
SELECT d.id, dt.docbase_link, dt.source_link FROM docs d
JOIN docs_temp dt ON d.name = dt.name;

DROP TABLE docs_temp;