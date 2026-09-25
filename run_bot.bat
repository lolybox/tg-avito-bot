@echo off
setlocal enabledelayedexpansion

REM Telegram Avito Bot - Запуск на Windows
REM Быстрый запуск с автоматическим определением настроек

echo ========================================
echo   Telegram Avito Bot Launcher
echo ========================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo [OK] Python detected
python --version

REM Проверка виртуального окружения
if exist venv\Scripts\activate.bat (
    echo [OK] Virtual environment found
    call venv\Scripts\activate
) else (
    echo [*] Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt >nul 2>&1
    echo [OK] Dependencies installed
)

echo.
echo Starting bot...
echo.

REM Запуск бота
python bots/main.py

REM При остановке
echo.
echo Bot stopped
pause
