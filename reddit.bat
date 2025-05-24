@echo off

set batch_file_location=%~dp0

if exist .venv\ (
    echo Using .venv
    "%batch_file_location%.venv\Scripts\python.exe" src\cli.py %*
) else if exist venv (
    echo Using venv
    "%batch_file_location%.venv\Scripts\python.exe" src\cli.py %*
) else (
    python src\cli.py %*
)