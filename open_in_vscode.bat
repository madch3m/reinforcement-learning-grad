@echo off
REM Quick launcher for VS Code workspace

echo.
echo ========================================
echo Traffic Signal RL - VS Code Launcher
echo ========================================
echo.

REM Check if VS Code is installed
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: VS Code 'code' command not found!
    echo.
    echo Please either:
    echo 1. Install VS Code from: https://code.visualstudio.com/
    echo 2. Or add VS Code to your PATH
    echo.
    pause
    exit /b 1
)

REM Check if workspace file exists
if not exist "traffic_rl.code-workspace" (
    echo ERROR: Workspace file not found!
    echo Please make sure you're running this script from the correct directory.
    echo.
    pause
    exit /b 1
)

echo Opening VS Code workspace...
code traffic_rl.code-workspace

echo.
echo VS Code should now be opening!
echo.
echo Next steps:
echo 1. Install recommended extensions (VS Code will prompt)
echo 2. Select Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter")
echo 3. Open integrated terminal (Ctrl+`)
echo 4. Create virtual environment: python -m venv venv
echo 5. Activate: venv\Scripts\activate
echo 6. Install dependencies: pip install -r requirements.txt
echo.
echo See VSCODE_GUIDE.md for detailed instructions!
echo.
pause
