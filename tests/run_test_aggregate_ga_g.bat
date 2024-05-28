@echo off
setlocal

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.
    exit /b 1
)

:: Check if pip is installed
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo pip is not installed. Please install pip.
    exit /b 1
)

:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Run the analysis script
python test_aggregate_ga.py
python test_aggregate_g.py

:: Deactivate and remove the virtual environment
call venv\Scripts\deactivate

rmdir /s /q venv

echo Analysis completed.
endlocal
