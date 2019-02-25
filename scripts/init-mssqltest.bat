@ECHO OFF
REM Init testing MSSQL Database 
sqlcmd -E -S BARRETT-MAIN\BARRETTSQL -i ..\sql\init.sql
PAUSE