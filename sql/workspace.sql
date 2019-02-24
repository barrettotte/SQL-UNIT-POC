

SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES;

SELECT * FROM [BARRETT_TEST].[dbo].[users];
SELECT * FROM [BARRETT_TEST].[dbo].[roles];
SELECT * FROM [BARRETT_TEST].[dbo].[user_roles];


INSERT INTO [BARRETT_TEST].[dbo].[users](first_name, last_name, username) VALUES ('barrett', 'otte', 'barrettotte')
INSERT INTO [BARRETT_TEST].[dbo].[users](first_name, last_name, username) VALUES ('some', 'body', 'somebody')
INSERT INTO [BARRETT_TEST].[dbo].[users](first_name, last_name, username) VALUES ('hello', 'world', 'helloworld123')


SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.routines 
    WHERE ROUTINE_TYPE = 'PROCEDURE'