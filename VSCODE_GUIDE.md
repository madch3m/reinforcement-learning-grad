# Quick Start Guide: Opening in VS Code

## Method 1: Direct Open (Simplest)

### On Windows:
1. Download all files to a folder (e.g., `C:\Projects\TrafficRL\`)
2. Right-click the folder
3. Select "Open with Code" (if VS Code is installed)

OR

1. Open VS Code
2. File → Open Folder
3. Navigate to your downloaded folder
4. Click "Select Folder"

### On Mac/Linux:
```bash
# Navigate to your download folder
cd ~/Downloads/traffic_rl_project

# Open in VS Code
code .
```

---

## Method 2: Use the Workspace File (Recommended)

### Step 1: Organize Your Files

Create this folder structure:
```
TrafficRL/
├── traffic_rl.code-workspace          # VS Code workspace
├── gradio_traffic_app.py              # Gradio app
├── requirements_gradio.txt
├── README_SPACE.md
├── DEPLOYMENT_GUIDE.md
├── non_episodic_evaluation_guide.ipynb
└── traffic_rl_project/
    ├── traffic_signal_rl.ipynb        # Main notebook
    ├── README.md
    ├── requirements.txt
    └── test_setup.py
```

### Step 2: Open Workspace

**Double-click** `traffic_rl.code-workspace`

OR

In VS Code:
1. File → Open Workspace from File
2. Select `traffic_rl.code-workspace`
3. Click "Open"

---

## Method 3: Command Line

### Windows (PowerShell/CMD):
```powershell
# Navigate to folder
cd C:\Projects\TrafficRL

# Open workspace
code traffic_rl.code-workspace
```

### Mac/Linux (Terminal):
```bash
# Navigate to folder
cd ~/Projects/TrafficRL

# Open workspace
code traffic_rl.code-workspace
```

---

## First Time Setup in VS Code

### 1. Install Python Extension

When you open the workspace, VS Code may prompt you to install recommended extensions. Click "Install All".

Or manually:
1. Click Extensions icon (left sidebar) or press `Ctrl+Shift+X`
2. Search for "Python"
3. Install "Python" by Microsoft
4. Install "Jupyter" by Microsoft

### 2. Select Python Interpreter

1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. Type "Python: Select Interpreter"
3. Choose your Python installation (3.8+)

### 3. Create Virtual Environment (Recommended)

**In VS Code Terminal** (View → Terminal or `` Ctrl+` ``):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r traffic_rl_project/requirements.txt
pip install -r requirements_gradio.txt
```

---

## Opening Specific Files

### Open Jupyter Notebook:
1. Navigate in Explorer (left sidebar)
2. Click `traffic_rl_project/traffic_signal_rl.ipynb`
3. VS Code opens it with Jupyter interface
4. Click "Select Kernel" → Choose your Python environment

### Open Gradio App:
1. Click `gradio_traffic_app.py`
2. To run: Press `F5` or click Run → Start Debugging
3. App will open in browser at http://localhost:7860

### Open Evaluation Guide:
1. Click `non_episodic_evaluation_guide.ipynb`
2. Select kernel
3. Run cells with `Shift+Enter`

---

## Running the Projects

### Run Gradio App:

**Option A: Use Debug Configuration**
1. Go to Run and Debug (sidebar or `Ctrl+Shift+D`)
2. Select "Run Gradio App" from dropdown
3. Press F5 or click green play button

**Option B: Run in Terminal**
```bash
python gradio_traffic_app.py
```

**Option C: Run from File**
1. Open `gradio_traffic_app.py`
2. Right-click in editor
3. Select "Run Python File in Terminal"

### Run Jupyter Notebook:
1. Open `traffic_signal_rl.ipynb`
2. Click "Run All" at the top
3. Or run cells individually with `Shift+Enter`

### Test Your Setup:
```bash
cd traffic_rl_project
python test_setup.py
```

---

## Useful VS Code Shortcuts

### General:
- `Ctrl+P` - Quick file open
- `Ctrl+Shift+P` - Command palette
- `Ctrl+B` - Toggle sidebar
- `` Ctrl+` `` - Toggle terminal

### Jupyter Notebooks:
- `Shift+Enter` - Run cell and move to next
- `Ctrl+Enter` - Run cell (stay in same cell)
- `A` - Insert cell above
- `B` - Insert cell below
- `DD` - Delete cell

### Python Files:
- `F5` - Run with debugger
- `Ctrl+F5` - Run without debugger
- `F9` - Toggle breakpoint
- `Ctrl+/` - Comment/uncomment line

---

## Troubleshooting

### "Python not found"
- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation
- Restart VS Code

### "Jupyter not installed"
```bash
pip install jupyter notebook ipykernel
```

### "Module not found" errors
```bash
# Make sure virtual environment is activated
# Install requirements
pip install -r requirements.txt
```

### Notebook kernel won't start
1. `Ctrl+Shift+P`
2. Type "Jupyter: Select Interpreter to Start Jupyter Server"
3. Choose your Python environment
4. Restart VS Code

---

## Recommended VS Code Extensions

Already included in workspace recommendations:
- ✅ Python (Microsoft)
- ✅ Pylance (Microsoft)
- ✅ Jupyter (Microsoft)

Optional but useful:
- GitLens (Git visualization)
- Path Intellisense (Autocomplete paths)
- Markdown All in One (Better markdown editing)
- Better Comments (Highlight TODO, FIXME, etc.)

---

## Project Structure in VS Code

Your workspace has two folders:

### 📁 Traffic RL Project
- Main RL implementation
- Training notebook
- Environment definitions
- Baseline controllers

### 📁 Gradio App (HF Spaces)  
- Deployment-ready app
- Visualization code
- Hugging Face Space files

---

## Next Steps

1. ✅ Open workspace in VS Code
2. ✅ Install recommended extensions
3. ✅ Create virtual environment
4. ✅ Install dependencies
5. ✅ Run `test_setup.py` to verify
6. 🎯 Start exploring the notebooks!
7. 🚀 Run the Gradio app locally
8. 🌐 Deploy to Hugging Face when ready

---

## Getting Help

**VS Code Documentation:**
- Python: https://code.visualstudio.com/docs/python/python-tutorial
- Jupyter: https://code.visualstudio.com/docs/datascience/jupyter-notebooks

**Keyboard Shortcuts Reference:**
- Help → Keyboard Shortcuts Reference
- Or press `Ctrl+K Ctrl+R`

---

**Happy Coding! 🚀**
