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
  * Init ```cd ./projectfolder && virtualenv venv```
  * Enter ```venv\Scripts\activate```
  * Exit ```deactivate```


## References
* ...


## Future Ideas/Improvements
* CI / CD using GitLab and Docker
* Experimentation with DB2 SQL and UDFs
* Deeper performance measurement
* Generate graphs from result sets and add to reports