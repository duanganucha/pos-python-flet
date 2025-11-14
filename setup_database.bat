@echo off
echo ====================================
echo POS System - Database Setup
echo ====================================
echo.

echo [1/2] Creating SQLite database...
python database/seed_db.py

if errorlevel 1 (
    echo.
    echo ERROR: Database setup failed!
    pause
    exit /b 1
)

echo.
echo [2/2] Database setup completed!
echo.
echo ====================================
echo Database ready to use!
echo ====================================
echo.
echo Location: database\pos.db
echo.
pause
