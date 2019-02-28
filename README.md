# SQL-UNIT-POC

A very basic POC MSSQL unit testing framework using Python and T-SQL.


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
    * Reporting
      * HTML report
    * Clean up and Finish
      * remove SQL-Unit wrapper stored procedure and any TMP tables


## Project Milestones
- [x] Test generator backend / basic CLI (Scrapped in favor of a directory/file driven test framework)
- [x] Test framework foundations
- [x] Test runner basics
- [x] SQL-Unit wrapper Stored Procedure
- [x] Testing with basic SQL
- [ ] Test evaluation expected vs actual functionality
- [ ] Testing with more advanced SQL and UDFs
- [ ] Testing with Stored Procedures
- [ ] CI / CD using GitLab and Docker for project
- [ ] Error handling and polish of current code
- [ ] Measure performance: Execution time
- [ ] Generate Report from test suite results
- [ ] Generate formatted reports with HTML


## Development Notes
* Virtual Environment
  * Install ```pip install virtualenv```
  * Init ```cd .\projectfolder && virtualenv venv```
  * Enter ```venv\Scripts\activate```
  * Exit ```deactivate```
* Example database to kick around
  * https://github.com/Microsoft/sql-server-samples/
  * Download AdventureWorks2017.bak and place in C:/.../Microsoft SQL Server/.../MSSQL/Backup/
  * Right click server > restore database > device > add AdventureWorks2017.bak


## References
* Use SQL Server 2017 in Docker containers for your CI/CD process https://www.youtube.com/watch?v=HkWwaOG3aSw
* Designed basic SQL tests around these:
  * http://www.sqlservertutorial.net/sql-server-basics/
  * https://goalkicker.com/MicrosoftSQLServerBook/
* https://docs.microsoft.com/en-us/sql/?view=sql-server-2017


## Future Ideas/Improvements
* GitLab build step and/or Jenkins Job
* Deeper performance measurement
* Generate graphs from test results and add to reports
* Start experimenting with the possiblity of basic DB2 queries?