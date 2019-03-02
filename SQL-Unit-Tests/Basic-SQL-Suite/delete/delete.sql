-- This is a simple test for an DELETE statement --

INSERT INTO [BARRETT_TEST].[dbo].[roles] (role_name) VALUES ('HELLO'); 

DELETE FROM [BARRETT_TEST].[dbo].[roles] WHERE role_name='HELLO';
