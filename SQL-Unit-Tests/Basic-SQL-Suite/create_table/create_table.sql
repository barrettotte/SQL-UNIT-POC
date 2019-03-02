-- This is a simple test for CREATE TABLE statement --

CREATE TABLE [BARRETT_TEST].[dbo].[HELLOWORLD] (
    id BIGINT PRIMARY KEY,
    col1 VARCHAR(255),
    col2 BIT
);

INSERT INTO [BARRETT_TEST].[dbo].[HELLOWORLD] (col1, col2) VALUES ('WASD', 1);
INSERT INTO [BARRETT_TEST].[dbo].[HELLOWORLD] (col1, col2) VALUES ('QWERTY', 0);