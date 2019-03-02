# SQL-UNIT-POC


A very basic POC MSSQL unit testing framework using Python and T-SQL. Directory/file driven unit tests using SQL and JSON.


Developed using Python 3.7 and Microsoft SQL Server 2017. 


## Example directory structure
``` text
./SQL-Unit-POC/SQL-Unit-Tests/
|-- Basic-SQL-Suite
|   |-- inner_join
|   |   |-- inner_join.actual.json
|   |   |-- inner_join.expected.json
|   |   |-- inner_join.sql
|   |-- another_test
|-- another-suite
|   |-- some_test
```


## Sample Suite config.json (.\SQL-Unit-Tests\Basic-SQL-Suite\Basic-SQL-Suite.config.json)
```JSON
/* NOTE: This will only use current Windows user credentials for now. */
{
    "database-config": {
        "server": "BARRETT-MAIN\\BARRETTSQL",
        "database": "BARRETT_TEST",
        "dialect": "MSSQL"
    }    
}
```


## Example SQL Input (inner_join.SQL)
```SQL
-- This is a simple test for an INNER JOIN statement --

INSERT INTO developers (username, fav_language) VALUES ('barrettotte', 'Python');
INSERT INTO developers (username, fav_language) VALUES ('firstlast', 'Java');
INSERT INTO developers (username, fav_language) VALUES ('helloworld123', 'JavaScript');
INSERT INTO developers (username, fav_language) VALUES ('someguy1', 'C++');


SELECT DISTINCT u.first_name, u.last_name, d.fav_language
FROM [BARRETT_TEST].[dbo].[developers] AS d
INNER JOIN [BARRETT_TEST].[dbo].[users] AS u 
	ON u.username = d.username;
```


## Example Expected JSON (inner_join.expected.json)
```JSON
{
    "success": "true",
    "columns": [
        {
            "name": "first_name",
            "type": "VARCHAR(50)"
        },
        {
            "name": "last_name",
            "type": "VARCHAR(50)"
        },
        {
            "name": "fav_language",
            "type": "VARCHAR(50)"
        }
    ],
    "rows": [
        {
            "first_name": "barrett",
            "last_name": "otte",
            "fav_language": "Python"
        },
        {
            "first_name": "hello",
            "last_name": "world",
            "fav_language": "JavaScript"
        }
    ]
}
```


## Example console/log output of executing test suite .\SQL-Unit-Tests\Basic-SQL-Suite\
``` TEXT
[INFO  2019-03-01 20:47:08.035128] SQL Test Runner initializing
[INFO  2019-03-01 20:47:08.038142] SQL Test Runner using directory [D:\Programming\SQL-UNIT-POC\SQL-Unit-Tests]
[INFO  2019-03-01 20:47:08.041107] Loading all test files
[INFO  2019-03-01 20:47:08.045119] Found 1 suite(s) in [D:\Programming\SQL-UNIT-POC\SQL-Unit-Tests]
[INFO  2019-03-01 20:47:08.052078] SQL Test Runner targeted with suite [Basic-SQL-Suite]
[INFO  2019-03-01 20:47:08.055094] Initializing SQLUnit_Wrapper Stored Procedure
[INFO  2019-03-01 20:47:08.058062] Creating database connection to [BARRETT-MAIN\BARRETTSQL\BARRETT_TEST]
[INFO  2019-03-01 20:47:08.091971] Running suite [Basic-SQL-Suite] with 11 test(s)
[INFO  2019-03-01 20:47:08.094988]    Running test [create_table]                (1 of 11)
[INFO  2019-03-01 20:47:08.097956]       Reading files
[INFO  2019-03-01 20:47:08.100973]       Executing [create_table.sql]
[INFO  2019-03-01 20:47:08.106931]       SQL Query failed
[INFO  2019-03-01 20:47:08.112916]       Test Passed
[INFO  2019-03-01 20:47:08.115933]       Test execution in 17.9279 ms
.     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .
.     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .
.     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .
[INFO  2019-03-01 20:47:08.162783]    Running test [fail_onpurpose]              (4 of 11)
[INFO  2019-03-01 20:47:08.165774]       Reading files
[INFO  2019-03-01 20:47:08.167792]       Executing [fail_onpurpose.sql]
[INFO  2019-03-01 20:47:08.177765] X      Test Failed
[INFO  2019-03-01 20:47:08.180734]       Test execution in 14.9822 ms
[INFO  2019-03-01 20:47:08.184723]    Running test [fail_select]                 (5 of 11)
[INFO  2019-03-01 20:47:08.187742]       Reading files
[INFO  2019-03-01 20:47:08.192725]       Executing [fail_select.sql]
[INFO  2019-03-01 20:47:08.197712]       SQL Query failed
[INFO  2019-03-01 20:47:08.201678]       Test Passed
[INFO  2019-03-01 20:47:08.204670]       Test execution in 15.9812 ms
[INFO  2019-03-01 20:47:08.207662]    Running test [inner_join]                  (6 of 11)
[INFO  2019-03-01 20:47:08.211651]       Reading files
[INFO  2019-03-01 20:47:08.214671]       Executing [inner_join.sql]
[INFO  2019-03-01 20:47:08.226654]       Test Passed
[INFO  2019-03-01 20:47:08.230601]       Test execution in 18.9922 ms
.     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .
.     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .
.     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .     .
[INFO  2019-03-01 20:47:08.350281] Results: 10 of 11 test(s) passed
[INFO  2019-03-01 20:47:08.353300] Suite execution in 261.3287 ms
[INFO  2019-03-01 20:47:08.356265] Cleaning up database and connection
[INFO  2019-03-01 20:47:08.367236] SQL Test Runner finished
```


## Sample Suite results JSON (Basic-SQL-Suite.results.json)
```JSON
{
    "name": "Basic-SQL-Suite",
    "total": 11,
    "passed": 10,
    "time": 261.3287,
    "tests": [ ... All tests with names and paths ... ]
}
```


## Summary
* Test suites
   * A collection of test cases containing {test}.sql, {test}.expected.json, and {test}.actual.json
   * Each test suite can be configured for different databases/servers in {test-suite}.config.json
* Test cases
  * {test}.sql - SQL to execute
  * {test}.expected.json - expected results (columns, success?, data[])
  * {test}.actual.json - actual results (columns, success?, data[])
* Test runner
    * Launch run.bat / run.sh passing target test suite and config path
    * Initialize SQL-Unit Test Runner, load all test files
    * Init SQL-Unit wrapper stored procedure in target database
    * Loop over all tests within target test collection
    * Load {test}.expected.json and {test}.sql and pass to SQL-Unit wrapper SP
    * SQL-Unit wrapper starts T-SQL transaction and saves before execution
    * {test}.sql is injected into EXEC() command and executed
    * {test}.sql result-set stored in dynamic TMP table defined by columns in {test}.expected.json
    * result-set returned to Python side and transaction rollback
    * Evaluate expected vs actual of {test}.sql
    * Clean up and Finish
      * remove SQL-Unit wrapper stored procedure and any TMP tables


## Limitations
* Only tested with Microsoft SQL Server 2017 and Python 3.7
* Credentials are based on current Windows credentials
* This was a POC project


## Development Notes
* Python Virtual Environment
  * Install ```pip install virtualenv```
  * Init ```cd .\projectfolder && virtualenv venv```
  * Enter ```venv\Scripts\activate```
  * Exit ```deactivate```


## Future Ideas/Improvements
* CI / CD using GitLab and Docker for project
* GitLab build step and/or Jenkins Job using SQLUnit on a test database
* Deeper performance measurement
* Generate graphs from test results/performance and add to reports
* Start experimenting with the possiblity of basic DB2 queries?
* [ ] Generate Report from test suite results
* [ ] Generate formatted reports with HTML


## References
* Heavily inspired by IOUnit https://github.com/ioUnit/ioUnit
* Designed basic SQL tests around these:
  * http://www.sqlservertutorial.net/sql-server-basics/
  * https://goalkicker.com/MicrosoftSQLServerBook/
* https://docs.microsoft.com/en-us/sql/?view=sql-server-2017
