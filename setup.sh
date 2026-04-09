#!/bin/bash

# Quick Setup Script for Traffic Signal RL
# This script helps you get started quickly

echo ""
echo "=========================================="
echo "Traffic Signal RL - Quick Setup"
echo "=========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher is required"
    echo "   Current version: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo "Installing dependencies..."
echo "  - Installing traffic_rl_project requirements..."
pip install -r traffic_rl_project/requirements.txt -q

echo "  - Installing gradio_app requirements..."
pip install -r gradio_app/requirements_gradio.txt -q

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ All dependencies installed"
echo ""

# Run verification
echo "Running setup verification..."
python traffic_rl_project/test_setup.py

echo ""
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run Jupyter notebook:"
echo "     jupyter notebook traffic_rl_project/traffic_signal_rl.ipynb"
echo ""
echo "  3. Or run Gradio app:"
echo "     python gradio_app/gradio_traffic_app.py"
echo ""
echo "  4. Or open in VS Code:"
echo "     code traffic_rl.code-workspace"
echo ""
echo "=========================================="
