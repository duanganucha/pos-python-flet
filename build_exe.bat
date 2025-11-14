@echo off
echo ====================================
echo POS System - Building EXE File
echo ====================================
echo.

echo [1/4] Checking if PyInstaller is installed...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
) else (
    echo PyInstaller is already installed.
)
echo.

echo [2/4] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist pos.spec del /f /q pos.spec
echo Old build files cleaned.
echo.

echo [3/4] Building EXE file...
echo This may take a few minutes...
pyinstaller --name="POS-System" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data "data;data" ^
    --hidden-import=ttkbootstrap ^
    --hidden-import=PIL ^
    src/pos_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo.

echo [4/4] Build completed successfully!
echo.
echo ====================================
echo EXE file location: dist\POS-System.exe
echo ====================================
echo.
echo You can now run the application by double-clicking:
echo   dist\POS-System.exe
echo.
echo Note: Make sure to copy the 'data' folder to the same directory as the EXE file!
echo.
pause
