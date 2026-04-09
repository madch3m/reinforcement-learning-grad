#!/bin/bash

# Quick launcher for VS Code workspace

echo ""
echo "========================================"
echo "Traffic Signal RL - VS Code Launcher"
echo "========================================"
echo ""

# Check if VS Code is installed
if ! command -v code &> /dev/null; then
    echo "ERROR: VS Code 'code' command not found!"
    echo ""
    echo "Please either:"
    echo "1. Install VS Code from: https://code.visualstudio.com/"
    echo "2. Or add VS Code to your PATH"
    echo ""
    echo "On Mac: Open VS Code → Command Palette (Cmd+Shift+P) → 'Shell Command: Install code command in PATH'"
    echo ""
    exit 1
fi

# Check if workspace file exists
if [ ! -f "traffic_rl.code-workspace" ]; then
    echo "ERROR: Workspace file not found!"
    echo "Please make sure you're running this script from the correct directory."
    echo ""
    exit 1
fi

echo "Opening VS Code workspace..."
code traffic_rl.code-workspace

echo ""
echo "VS Code should now be opening!"
echo ""
echo "Next steps:"
echo "1. Install recommended extensions (VS Code will prompt)"
echo "2. Select Python interpreter (Cmd+Shift+P → 'Python: Select Interpreter')"
echo "3. Open integrated terminal (Ctrl+\`)"
echo "4. Create virtual environment: python3 -m venv venv"
echo "5. Activate: source venv/bin/activate"
echo "6. Install dependencies: pip install -r requirements.txt"
echo ""
echo "See VSCODE_GUIDE.md for detailed instructions!"
echo ""
