-- NOTES --
    -- VS Code Extension MSSQL Tools is awesome


-- Allow things like OPENQUERY to be ran
    sp_configure 'Show Advanced Options', 1
    GO
    RECONFIGURE
    GO
    sp_configure 'Ad Hoc Distributed Queries', 1
    GO
    RECONFIGURE
    GO


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


-- Make dynamic temp table from results of sql string query --
DECLARE @COLS AS VARCHAR(MAX) = '';
            
IF EXISTS (SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME=@TMP_TABLE AND TABLE_SCHEMA=@TMP_SCHEMA)
    EXEC('DROP TABLE ' + @TMP_LOC);
EXEC('CREATE TABLE ' + @TMP_LOC + '(SQLUnit_TMPCOL VARCHAR(MAX))');

-- Get results from dynamic temp table --
SELECT @COLS = @COLS + COLUMN_NAME + ',' FROM [BARRETT_TEST].INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME=@TMP_TABLE AND TABLE_SCHEMA=@TMP_SCHEMA;
SELECT @COLS = SUBSTRING(@COLS, 1, LEN(@COLS)-1);


-- XML result-set
SELECT * FROM roles FOR XML PATH('row'), ROOT('result-set'), TYPE

-- JSON result-set
SELECT * FROM roles FOR JSON PATH, INCLUDE_NULL_VALUES, ROOT('result-set') --, WITHOUT_ARRAY_WRAPPER