@echo off
echo ========================================
echo YOLOv12 Damaged Parcel Detection Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.9-3.11 from python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment!
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements (this may take 5-10 minutes)...
pip install -r requirements.txt

REM Create necessary folders
echo Creating project folders...
mkdir dataset\train\images 2>nul
mkdir dataset\train\labels 2>nul
mkdir dataset\valid\images 2>nul
mkdir dataset\valid\labels 2>nul
mkdir dataset\test\images 2>nul
mkdir dataset\test\labels 2>nul
mkdir models\experiments 2>nul
mkdir results\logs 2>nul
mkdir results\plots 2>nul
mkdir results\reports 2>nul
mkdir notebooks 2>nul
mkdir temp 2>nul

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Place your dataset in the 'dataset' folder
echo 2. Open VSCode: code .
echo 3. Select Python interpreter: Ctrl+Shift+P -> Python: Select Interpreter
echo    -> Choose './venv/Scripts/python.exe'
echo 4. Run scripts in order from the 'scripts' folder
echo.
echo To activate environment manually:
echo    venv\Scripts\activate
echo.
pause