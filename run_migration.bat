@echo off
cd disease_analyzer
python manage.py migrate analyzer
pause

