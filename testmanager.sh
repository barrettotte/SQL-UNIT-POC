#!/bin/bash
# Simple script to shorten the command for using the test manager CLI (untested)
pd=`$(PWD)`; cd ./testmanager/ && python ./testmanagercli.py "$@" 
cd $pd