@echo off
title IMS - Inventory Management System
echo ========================================================
echo   Starting Inventory Management System (Django Server)
echo ========================================================
echo.
cd /d "%~dp0"
echo Opening browser at http://localhost:8000/ ...
start http://localhost:8000/
echo Starting Django server on http://127.0.0.1:8000 ...
python manage.py runserver 127.0.0.1:8000
pause
