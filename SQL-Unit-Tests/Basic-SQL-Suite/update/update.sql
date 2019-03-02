-- This is a simple test for an UPDATE statement --

INSERT INTO [BARRETT_TEST].[dbo].[roles] (role_name) VALUES ('HELLO'); 

UPDATE [BARRETT_TEST].[dbo].[roles] SET role_name='WORLD'
    WHERE role_name='HELLO';
