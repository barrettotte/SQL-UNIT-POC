-- This is a simple test for a DISTINCT statement --

INSERT INTO [BARRETT_TEST].[dbo].[roles] (role_name) VALUES ('TEST');
INSERT INTO [BARRETT_TEST].[dbo].[roles] (role_name) VALUES ('WASD');
INSERT INTO [BARRETT_TEST].[dbo].[roles] (role_name) VALUES ('QWERTY');
INSERT INTO [BARRETT_TEST].[dbo].[roles] (role_name) VALUES ('TEST');
INSERT INTO [BARRETT_TEST].[dbo].[roles] (role_name) VALUES ('TEST');

SELECT DISTINCT role_name FROM [BARRETT_TEST].[dbo].[roles];
