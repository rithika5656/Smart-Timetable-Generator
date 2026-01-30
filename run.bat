@echo off
echo Starting Smart Timetable Generator...
set FLASK_APP=app.py
set FLASK_ENV=development
python app.py
pause
