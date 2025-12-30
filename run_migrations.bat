@echo off
echo ========================================
echo Running Django Migrations
echo ========================================
cd /d "%~dp0disease_analyzer"
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Running migrations for analyzer app...
python manage.py migrate analyzer
echo.
echo ========================================
echo Migration completed!
echo ========================================
pause

