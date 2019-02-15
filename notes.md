

### SQL Unit Testing (Python or Java)
* Setup SQL connection details via config file
* Setup Testing framework
* Specify unit tests (SQL and/or function) and expected results (json?) IOUnit?
* Initiate SQL connection
* Start a SQL transaction
* Execute SQL and/or SQL function specified by unit test
* **Keep DB connection alive?**
* Evaluate actual vs expected results
* Rollback SQL transaction
* **Terminate DB connection**
* Display results of unit tests


### Make a GUI Unit-Test Generator
* Simple Python GUI
* Pick test collection name or make new one (database, dialect, credentials)
* test name, description, filename.sql
* generates filename-expected
* Adds generated JSON test to SQL-UNIT.json
* Remove JSON test from SQL-UNIT.json
* Remove test collections


### Unit Test Configuration
```JSON
//SQL-UNIT.json
{
    "test-collections": [
        {
            "id": 0,
            "name": "test-dev-mssql", //used for reports and test DB table name
            "description": "This collection of tests is used to do WASD",
            "config": {
                "server": "DEV", //dev server connection name
                "dialect": "MSSQL", //For possible future SQL types
                "keep-results": 10, //How many result sets to keep of this test collection
                "fail-threshold": 3, //How many tests fail to be considered FAILURE
                "measure-performance": true, //Record performance stats
                "record-results": true, //Record results to test database
                "generate-report": true, //Generate test report
                "allow-stored-procedures": false
            },
            "tests": [
                {
                    "id": 0,
                    "name": "tableselect_QWERTY",
                    "description": "This will test QWERTY's performance",
                    "input": "somefile.sql",
                    "expected": "somefile-expected.json",
                    "output": "somefile-actual.json"
                },
                {
                    "id": 1,
                    "name": "somestoredproc_WASD",
                    "description": "This will test somestoredproc with WASD",
                    "input": "somefile2.sql",
                    "expected": "somefile2-expected.json",
                    "output": "somefile2-actual.json"
                }
            ]
        }
    ]
}
```


### Unit test SQL file
```SQL
    -- somefile.sql
    SELECT * FROM [DEV].[dbo].sometable WHERE someCol = 'WASD';
```


### Testing
* Create a separate testing database on SQL server for unit testing stuff only
* Create a stored procedure as a "wrapper" for executing SQL string
* Stored Procedure
  * Input SQL string from unit test
  * Output results as XML
* Only keep n sets of test results. Otherwise drop oldest results table
* Results_{datetime}
  * A Row
    * ID
    * Result set as JSON string
    * Performance stats
    * timestamp
```SQL
-- Stored Procedure Wrapper
    -- IN:  SQL String
    -- OUT: XML results
    -- TRY/CATCH (Exceptions + Invalid SQL)
    BEGIN TRANSACTION
        -- Execute some SQL
    ROLLBACK TRANSACTION
    -- Write XML results to results_{datetime} table in testing DB
```


### Performance Measuring
* Measure execution time
* http://www.sqlservercentral.com/blogs/matthew-mcgiffen-dba/2017/05/24/measuring-sql-query-performance/
* https://stackify.com/performance-tuning-in-sql-server-find-slow-queries/
* Memory/CPU Usage possible?


### Reporting
* Test pass/fail
* Rows effected by test
* Performance
* Record test results to separate database on server
* Service for generating report of test results
* Service for generating graph of results, data, etc.


### MSSQL
* https://stackoverflow.com/questions/11531352/how-to-rollback-a-transaction-in-a-stored-procedure


### Are there transactions in IBMi?????? -> Rollbacks and Commits (I think)
* https://www.ibm.com/support/knowledgecenter/en/ssw_ibm_i_72/sqlp/rbafydicomm.htm
* https://stackoverflow.com/questions/4947340/is-rollback-can-work-without-savepoints-in-db2


### Misc
* https://www.ibm.com/support/knowledgecenter/en/ssw_ibm_i_73/rzahg/welcome.htm
* https://developer.ibm.com/components/ibm-i/

