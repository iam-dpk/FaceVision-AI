@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ==========================================
echo       FaceVision AI - Windows Launcher
echo ==========================================
echo.

REM First try the exact "python" command that worked on this PC.
set "PYTHON_CMD=python"
python --version >nul 2>nul
if not errorlevel 1 goto :python_found

REM Then try the Python launcher without requiring a specific version.
set "PYTHON_CMD=py"
py --version >nul 2>nul
if not errorlevel 1 goto :python_found

echo ERROR: Windows cannot find a working Python command.
echo.
echo Run this in PowerShell:
echo     python --version
echo.
echo If that also fails, install Python from python.org and enable
echo "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:python_found
echo Using:
%PYTHON_CMD% --version
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Python was found, but the virtual environment could not be created.
        echo.
        echo Try this manually:
        echo     %PYTHON_CMD% -m venv .venv
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Installing/updating dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo.
    echo ERROR: pip upgrade failed.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    echo.
    echo Copy the error above and send it to ChatGPT.
    pause
    exit /b 1
)

echo.
echo Starting FaceVision AI...
echo.

".venv\Scripts\python.exe" app.py

echo.
echo FaceVision AI has stopped.
pause
