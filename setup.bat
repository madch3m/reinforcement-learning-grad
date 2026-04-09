@echo off
REM Quick Setup Script for Traffic Signal RL (Windows)

echo.
echo ==========================================
echo Traffic Signal RL - Quick Setup
echo ==========================================
echo.

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip -q

REM Install dependencies
echo Installing dependencies...
echo   - Installing traffic_rl_project requirements...
pip install -r traffic_rl_project\requirements.txt -q

echo   - Installing gradio_app requirements...
pip install -r gradio_app\requirements_gradio.txt -q

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo All dependencies installed
echo.

REM Run verification
echo Running setup verification...
python traffic_rl_project\test_setup.py

echo.
echo ==========================================
echo Setup Complete! 🎉
echo ==========================================
echo.
echo Next steps:
echo   1. Activate virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Run Jupyter notebook:
echo      jupyter notebook traffic_rl_project\traffic_signal_rl.ipynb
echo.
echo   3. Or run Gradio app:
echo      python gradio_app\gradio_traffic_app.py
echo.
echo   4. Or open in VS Code:
echo      code traffic_rl.code-workspace
echo.
echo ==========================================
echo.
pause
