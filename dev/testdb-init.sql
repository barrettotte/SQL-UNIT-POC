-- Initialize my testing database --


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


-- Create developers table --
BEGIN
    PRINT N'Creating developers table...'
    IF NOT EXISTS (SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME='developers' AND TABLE_SCHEMA='dbo'
    )
        BEGIN
            CREATE TABLE [BARRETT_TEST].[dbo].[developers](
                id BIGINT IDENTITY(1,1) PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                fav_language VARCHAR(50) NOT NULL
            )
            PRINT N'developers table created.'
        END
    ELSE
        PRINT N'developers table already exists.';   
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


-- Display created tables in BARRETT_TEST
SELECT * FROM [BARRETT_TEST].INFORMATION_SCHEMA.TABLES;