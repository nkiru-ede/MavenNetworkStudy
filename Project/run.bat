@echo off

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.
    exit /b 1
)

:: Check if pip is installed
where pip >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Please install pip.
    exit /b 1
)

:: Create a virtual environment
python -m venv venv
call venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Run the test suite
python -m unittest discover -s tests

:: Deactivate and remove the virtual environment
call venv\Scripts\deactivate
rmdir /s /q venv

echo Tests completed.
pause
