-- NOTES --
    -- VS Code Extension MSSQL Tools is awesome


-- Get SQL Server version --
    SELECT @@VERSION AS 'SQL Server Version'; -- 2017

-- Get SQL Server Port --
    USE MASTER
    GO 
    EXEC xp_readerrorlog 0, 1, N'Server is listening on' 
    GO


-- Select all tables in database --
    SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES;


-- Select all stored procedures in database
SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.routines 
    WHERE ROUTINE_TYPE = 'PROCEDURE'


-- Drop all tables --
    USE [BARRETT_TEST]
    EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL'
    GO
    -- Drop all PKs and FKs
    DECLARE @sql NVARCHAR(max)
    SELECT @sql = STUFF((SELECT '; ' + 'ALTER TABLE ' + Table_Name  +'  drop constraint ' + Constraint_Name  
        FROM Information_Schema.CONSTRAINT_TABLE_USAGE 
        ORDER BY Constraint_Name FOR XML PATH('')),1,1,'')
    EXECUTE (@sql)
    GO
    -- Drop all tables
    EXEC sp_MSforeachtable 'DROP TABLE ?'
    GO