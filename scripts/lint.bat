@echo off
echo Running Flake8...
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
pause
