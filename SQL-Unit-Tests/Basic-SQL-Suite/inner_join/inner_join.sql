-- This is a simple test for an INNER JOIN statement --

INSERT INTO developers (username, fav_language) VALUES ('barrettotte', 'Python');
INSERT INTO developers (username, fav_language) VALUES ('firstlast', 'Java');
INSERT INTO developers (username, fav_language) VALUES ('helloworld123', 'JavaScript');
INSERT INTO developers (username, fav_language) VALUES ('someguy1', 'C++');


SELECT DISTINCT u.first_name, u.last_name, d.fav_language
FROM [BARRETT_TEST].[dbo].[developers] AS d
INNER JOIN [BARRETT_TEST].[dbo].[users] AS u 
	ON u.username = d.username;