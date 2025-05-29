/* Här kan jag skriva SQL-kommandon, så att när jag pushat så uppdateras databasen på
server-sidan, istället för lokalt */

-- INSERT INTO tests (name, description)
-- VALUES ("", "")

-- INSERT INTO links (test_id, docbase_link, source_link)
-- VALUES ((
--     SELECT id FROM tests
--     WHERE name = ""
--     ),
-- "", ""
-- );