@echo off
set PYTHON_EXECUTABLE=python.exe
%PYTHON_EXECUTABLE% my_script.py ".\tables" "games.nulls" > output.log
