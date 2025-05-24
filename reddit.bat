@echo off

set batch_file_location=%~dp0

if exist "%batch_file_location%.venv\" (
    echo Using .venv
    "%batch_file_location%.venv\Scripts\python.exe" %batch_file_location%src\cli.py %*
) else if exist "%batch_file_location%venv\" (
    echo Using venv
    "%batch_file_location%.venv\Scripts\python.exe" %batch_file_location%src\cli.py %*
) else (
    python "%batch_file_location%src\cli.py %*"
)