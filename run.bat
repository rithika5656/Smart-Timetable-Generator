@echo off
echo Starting Smart Timetable Generator...
echo Access at http://localhost:5000
set FLASK_APP=app.py
set FLASK_ENV=development
python app.py
pause
