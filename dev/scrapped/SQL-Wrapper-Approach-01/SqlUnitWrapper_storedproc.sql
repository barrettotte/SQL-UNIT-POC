-- SQL-Unit wrapper for executing SQL string within a T-SQL transaction --

USE [BARRETT_TEST];
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



-- https://stackoverflow.com/questions/41057283/t-sql-query-with-dynamic-unknown-number-of-columns
-- http://www.sqlservercentral.com/articles/T-SQL/138306/
-- XML not allowed in FOR Clause http://www.allaboutmssql.com/2012/11/sql-server-xml-error-for-xml-clause-is.html


/*CREATE PROCEDURE [dbo].[SQLUnit_Runner](
    @SQL_STRING NVARCHAR(MAX)
)
WITH EXECUTE AS CALLER
AS */
BEGIN
    SET NOCOUNT ON
    BEGIN TRANSACTION SQLUnit_Wrapper
        SAVE TRANSACTION SQLUnit_Save
        BEGIN TRY
			-- Working with trivial examples, DO NOT TOUCH
			DECLARE @TMP_DB AS VARCHAR(50) = 'BARRETT_TEST';
            DECLARE @TMP_SCHEMA AS VARCHAR(50) = 'dbo';
            DECLARE @TMP_LOC AS VARCHAR(160) = '[' + @TMP_DB + '].[' + @TMP_SCHEMA + '].[SQLUnit_TMP]';

			DECLARE @SQL_STRING AS NVARCHAR(MAX) = N'';
			SET @SQL_STRING = 'SELECT * FROM [BARRETT_TEST].[dbo].[roles]';

			IF OBJECT_ID(@TMP_LOC, 'U') IS NOT NULL 
				EXEC('DROP TABLE ' + @TMP_LOC);
			
			DECLARE @QRY_RES NVARCHAR(MAX) = N'CREATE TABLE ' + @TMP_LOC + ' (result XML)';
            DECLARE @QRY_INS NVARCHAR(MAX) = N'INSERT ' + @TMP_LOC + ' EXEC('' ';

			EXEC('CREATE TABLE ' + @TMP_LOC + ' (result XML)');
            SET @QRY_RES = N'EXEC(''(' + @SQL_STRING + ') FOR XML AUTO, TYPE'');';

			SELECT @QRY_INS = @QRY_INS + REPLACE(@QRY_RES,CHAR(39),CHAR(39)+CHAR(39)) + ''' )';
			--SELECT @QRY_INS = @QRY_INS + @QRY_RES + ''')';
			PRINT @QRY_INS;

			EXEC(@QRY_INS);
			EXEC('SELECT * FROM ' + @TMP_LOC);
			EXEC('DROP TABLE ' + @TMP_LOC);
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
                ROLLBACK TRANSACTION
        END CATCH
    ROLLBACK TRANSACTION SQLUnit_Wrapper   
END
