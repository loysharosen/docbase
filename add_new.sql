/* Här kan jag skriva SQL-kommandon, så att när jag pushat så uppdateras databasen på
server-sidan, istället för lokalt */

-- .import --csv tests.csv tests_temp

-- .import --csv links.csv links_temp

-- INSERT INTO tests (name, description)
-- SELECT name, description FROM tests_temp;

/* How to formulate this to include both test_id and links???? */
-- INSERT INTO links (test_id, docbase_link, source_link)
-- SELECT id FROM tests
-- WHERE name = ""