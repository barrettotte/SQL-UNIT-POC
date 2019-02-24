-- SQL-Unit wrapper for executing SQL string within a T-SQL transaction --

USE [BARRETT_TEST];
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



-- https://stackoverflow.com/questions/41057283/t-sql-query-with-dynamic-unknown-number-of-columns
-- http://www.sqlservercentral.com/articles/T-SQL/138306/

/*CREATE PROCEDURE [dbo].[SQLUnit_Runner](
	@SQL_STRING NVARCHAR(MAX)
)
WITH EXECUTE AS CALLER
AS 
BEGIN */


	SET NOCOUNT ON
	BEGIN TRANSACTION SQLUnit_Wrapper
		SAVE TRANSACTION SQLUnit_Save
        BEGIN TRY
			
			DECLARE @TMP_DB AS VARCHAR(50) = 'BARRETT_TEST';
			DECLARE @TMP_SCHEMA AS VARCHAR(50) = 'dbo';
			DECLARE @TMP_TABLE AS VARCHAR(50) = 'SQLUnit_TMP';
			DECLARE @TMP_LOC AS VARCHAR(160) = '[' + @TMP_DB + '].[' + @TMP_SCHEMA + '].[' + @TMP_TABLE + ']';
			DECLARE @COLS AS VARCHAR(MAX) = '';

			-- Make dynamic temp table from results of sql string query --
			IF EXISTS (SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME=@TMP_TABLE AND TABLE_SCHEMA=@TMP_SCHEMA)
				EXEC('DROP TABLE ' + @TMP_LOC);
			EXEC('CREATE TABLE ' + @TMP_LOC + '(SQLUnit_TMPCOL VARCHAR(MAX))');

			-- Get results from dynamic temp table --
			SELECT @COLS = @COLS + COLUMN_NAME + ',' FROM [BARRETT_TEST].INFORMATION_SCHEMA.COLUMNS 
				WHERE TABLE_NAME=@TMP_TABLE AND TABLE_SCHEMA=@TMP_SCHEMA;
			SELECT @COLS = SUBSTRING(@COLS, 1, LEN(@COLS)-1);
			
			
			
			DECLARE @SQL_STRING AS VARCHAR(500) = 'SELECT * FROM [BARRETT_TEST].[dbo].[users]';

			EXEC(@SQL_STRING + ' FOR XML RAW')

			IF OBJECT_ID('tempdb..##T1', 'U') IS NOT NULL DROP TABLE ##T1;
			DECLARE @QRY VARCHAR(MAX);
			EXEC('CREATE TABLE ##T1 (result XML)');
			
			INSERT INTO ##T1 EXEC('(' + @SQL_STRING + ') FOR XML PATH('''')');
			SELECT * FROM ##T1;

			
        END TRY
        BEGIN CATCH
            SELECT 
                ERROR_NUMBER() AS ErrorNumber,
                ERROR_SEVERITY() AS ErrorSeverity,
                ERROR_STATE() AS ErrorState,
                ERROR_PROCEDURE() AS ErrorProcedure,
                ERROR_LINE() AS ErrorLine,
                ERROR_MESSAGE() AS ErrorMessage;
            IF @@TRANCOUNT > 0
                 ROLLBACK TRANSACTION SQLUnit_Save;
        END CATCH
    ROLLBACK TRANSACTION SQLUnit_Wrapper   
END;
