@echo off
echo Running coverage...
pip install coverage
coverage run -m pytest
coverage report -m
coverage html
echo Report generated in htmlcov/index.html
pause
