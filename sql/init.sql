-- Initialize my testing database --


-- Configure to allow for open query --
sp_configure 'Show Advanced Options', 1
GO
RECONFIGURE
GO

sp_configure 'Ad Hoc Distributed Queries', 1
GO
RECONFIGURE
GO


-- Create BARRETT_TEST database --
BEGIN
    PRINT N'Creating BARRETT_TEST database...'
    IF (db_id(N'BARRETT_TEST') IS NULL) 
        BEGIN
            CREATE DATABASE BARRETT_TEST;
            PRINT N'BARRETT_TEST database created.'
        END
    ELSE
        PRINT N'BARRETT_TEST database already exists.'
END


-- Create users table --
BEGIN
    PRINT N'Creating users table...'
    IF NOT EXISTS (SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME='users' AND TABLE_SCHEMA='dbo'
    )
        BEGIN
            CREATE TABLE [BARRETT_TEST].[dbo].[users](
                id BIGINT IDENTITY(1,1) PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                username VARCHAR(50) NOT NULL,
            )
            PRINT N'persons table created.'
        END
    ELSE
        PRINT N'persons table already exists.';   
END
    

-- Create roles table --
BEGIN
    PRINT N'Creating roles table...'
    IF NOT EXISTS (SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME='roles' AND TABLE_SCHEMA='dbo'
    )
        BEGIN
            CREATE TABLE [BARRETT_TEST].[dbo].[roles](
                id BIGINT IDENTITY(1,1) PRIMARY KEY,
                role_name VARCHAR(50) NOT NULL
            )
            INSERT INTO [BARRETT_TEST].[dbo].[roles] VALUES
                ('ROLE_USER'), ('ROLE_ADMIN'), ('ROLE_DEVELOPER')
            PRINT N'roles table created.'
        END
    ELSE
        PRINT N'roles table already exists.';   
END


-- Create user_roles table --
BEGIN
    PRINT N'Creating user_roles table...'
    IF NOT EXISTS (SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME='user_roles' AND TABLE_SCHEMA='dbo'
    )
        BEGIN
            CREATE TABLE [BARRETT_TEST].[dbo].[user_roles](
                user_id BIGINT FOREIGN KEY REFERENCES users(id),
                role_id BIGINT FOREIGN KEY REFERENCES roles(id)
            )
            PRINT N'user_roles table created.'
        END
    ELSE
        PRINT N'user_roles table already exists.';   
END


SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.routines 
    WHERE ROUTINE_TYPE = 'PROCEDURE' AND ROUTINE_NAME = 'SQLUnit_Runner'


-- Create stored procedure --
USE [BARRETT_TEST];
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

BEGIN
    IF NOT EXISTS (SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.routines 
        WHERE ROUTINE_TYPE = 'PROCEDURE' AND ROUTINE_NAME = 'SQLUnit_Runner' 
    )
    BEGIN
        CREATE PROCEDURE [dbo].[SQLUnit_Runner]
        (
            @sql_input NVARCHAR(max),
            @results NVARCHAR(max)
        )
        AS
        BEGIN
            BEGIN TRANSACTION SqlUnitWrapper
                SAVE TRANSACTION SqlUnitSave
                SET @results = NULL
                BEGIN TRY
                    EXEC (@sql_input)
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
                        ROLLBACK TRANSACTION SqlUnitSave;
                END CATCH
            ROLLBACK TRANSACTION SqlUnitWrapper   
        END
    END
END
GO


-- Display created tables in BARRETT_TEST
SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES;