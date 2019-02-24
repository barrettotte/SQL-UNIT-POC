# SQL-UNIT-POC

A POC MSSQL unit testing framework with Python.


## Project Milestones
- [x] Test generator backend / basic CLI (Scrapped in favor of a directory/file driven test framework)
- [ ] Test framework foundations
- [ ] Test runner basics
- [ ] Tests with SQL and UDFs (MSSQL)
- [ ] Store test collection result set
- [ ] Measure performance: Execution time
- [ ] Error handling and polish of current code
- [ ] Generate Report from Results JSON
- [ ] Create basic Jenkins Job
- [ ] Tests with Stored Procedures (MSSQL)
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
  * Launch MSSMS > right click server > restore database > device > add AdventureWorks2017.bak

## References
* Use SQL Server 2017 in Docker containers for your CI/CD process https://www.youtube.com/watch?v=HkWwaOG3aSw
* Designed basic SQL tests around these:
  * http://www.sqlservertutorial.net/sql-server-basics/
  * https://goalkicker.com/MicrosoftSQLServerBook/
* https://docs.microsoft.com/en-us/sql/?view=sql-server-2017
* https://dba.stackexchange.com/questions/82681/how-to-rollback-when-3-stored-procedures-are-started-from-one-stored-procedure/82697#82697

## Future Ideas/Improvements
* CI / CD using GitLab and Docker
* Experimentation with DB2 SQL and UDFs
* Deeper performance measurement
* Generate graphs from result sets and add to reports