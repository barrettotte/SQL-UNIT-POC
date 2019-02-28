-- SQL-Unit wrapper for executing SQL string within a T-SQL transaction --

USE [BARRETT_TEST];
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- TODO --------
--   Python: Replace newline chars with &!NL!&, SQL: replace with CHAR(13)+CHAR(10)
--   Python: Replace tab chars with &!TAB!&, SQL: replace with CHAR(9)
----------------

CREATE OR ALTER PROCEDURE [dbo].[SQLUnit_Wrapper](
	@SQL_STRING NVARCHAR(MAX),
	@RES_COLS NVARCHAR(3000)
)  
WITH EXECUTE AS CALLER 
AS
BEGIN
	SET NOCOUNT ON

	-- TODO : Pass as params from Python side ------
	-- SQL_STRING : Load from {test}.sql, sanitize, and replace single quotes with '&!SQ!&'
	-- RES_COLS   : Load from {test}.expected.json - '|,|' delimited list of columns with types
	SET @SQL_STRING = N'
		INSERT INTO [BARRETT_TEST].[dbo].[roles] (role_name) VALUES (&!SQ!&TEST&!SQ!&); 
		SELECT * FROM [BARRETT_TEST].[dbo].[roles];
	';
	SET @RES_COLS = N'id VARCHAR(50)|,|result VARCHAR(50)|,|';
	--------------------------------------------

	DECLARE @POS INT = 0;
	DECLARE @LEN INT = 0;
	DECLARE @VAL VARCHAR(255);
	DECLARE @DELIM_COL VARCHAR(3) = '|,|';


	-- Dynamically create temp table from expected columns --
	IF OBJECT_ID('tempdb..#TMP') IS NOT NULL 
		DROP TABLE #TMP;
	CREATE TABLE #TMP(__IGNORE__ INT);
	WHILE CHARINDEX(@DELIM_COL, @RES_COLS, @POS + 1) > 0 
	BEGIN
		SET @LEN = CHARINDEX(@DELIM_COL, @RES_COLS, @POS + 1) - @POS;
		SET @VAL = SUBSTRING(@RES_COLS, @POS, @LEN);
		EXEC('ALTER TABLE #TMP ADD ' + @VAL);
		SET @POS = CHARINDEX(@DELIM_COL, @RES_COLS, @POS + @LEN) + LEN(@DELIM_COL);
	END
	EXEC('ALTER TABLE #TMP DROP COLUMN __IGNORE__');
	

	-- Execute injected SQL and select result set --
	BEGIN TRANSACTION SQLUnit_Wrapper
		SAVE TRANSACTION SQLUnit_Wrapper
		BEGIN TRY
			SET @SQL_STRING = 'BEGIN ' + REPLACE(@SQL_STRING, '&!SQ!&', CHAR(39)) + ' END';
			EXEC('CREATE OR ALTER PROCEDURE [dbo].[SQLUnit_TmpSP] AS ' + @SQL_STRING);
			INSERT INTO #TMP EXEC [dbo].[SQLUnit_TmpSP];
			SELECT * FROM #TMP;
			EXEC('DROP PROCEDURE [dbo].[SQLUnit_TmpSP]');
			DROP TABLE #TMP;
		END TRY
		BEGIN CATCH
			DECLARE @EXEC_FAILED BIT = 1;
			SELECT
				@EXEC_FAILED AS __SQLUnit_FAILED__,  -- Quick execution fail check for Python side
				@SQL_STRING AS SQL_STRING,
				@RES_COLS AS RES_COLS,
				ERROR_NUMBER() AS ErrorNumber,
				ERROR_SEVERITY() AS ErrorSeverity,
				ERROR_STATE() AS ErrorState,
				ERROR_PROCEDURE() AS ErrorProcedure,
				ERROR_LINE() AS ErrorLine,
				ERROR_MESSAGE() AS ErrorMessage;
			IF @@TRANCOUNT > 0
				ROLLBACK TRANSACTION SQLUnit_Wrapper
		END CATCH
	ROLLBACK TRANSACTION SQLUnit_Wrapper
END