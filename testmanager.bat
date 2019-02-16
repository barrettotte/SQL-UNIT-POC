@ECHO OFF
REM Simple script to shorten the command for using the test manager CLI
SET PD=%CD% && CD ./testmanager/ && CALL python ./testmanagercli.py %* 
CD %PD%