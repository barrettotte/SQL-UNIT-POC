@ECHO OFF
REM Simple script to run SQL-Unit test runner
REM  EX:  run.bat SomeSuite SomeConfig
python .\driver.py %*
PAUSE