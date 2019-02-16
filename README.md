# SQL-UNIT-POC

A POC MSSQL unit testing framework with Python.


(GitLab CI/CD status here)


## TLDR;
* ...


## Repository Details
| Directory/File        | Description                                |
| --------------------- | -------------------------------------------|
| SQL-Unit-Manager.json | The master data file / config for SQL-Unit | 
| testgenerator/        | Generate new unit test stubs and unit test collections |


## Project Milestones
- [x] Test generator backend / basic CLI
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


## Creating new Unit Tests and Unit Test Collections
* ...


## Configuration
* ...


## Test Process
* ...


## Database Integration
* ...


## Reporting
* ...


## CI/CD Integration
* ...


## Development Notes
* Virtual Environment
  * Install ```pip install virtualenv```
  * Init ```cd ./projectfolder && virtualenv venv```
  * Enter ```venv\Scripts\activate```
  * Exit ```deactivate```


## References
* ...


## Future Ideas/Improvements
* Test Generator - generate a test based off existing test
* Test Generator - GUI with PyQt5
* CI / CD using GitLab and Docker
* Experimentation with DB2 SQL and UDFs
* Deeper performance measurement
* Generate graphs from result sets and add to reports