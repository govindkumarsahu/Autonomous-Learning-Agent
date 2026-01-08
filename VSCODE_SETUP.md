# VS Code Setup Guide

## Quick Fix for VS Code Issues

If the code works in PowerShell but not in VS Code, follow these steps:

### 1. Select the Correct Python Interpreter

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: `Python: Select Interpreter`
3. Choose: `.\venv\Scripts\python.exe` (Windows) or `./venv/bin/python` (Mac/Linux)

### 2. Verify Virtual Environment is Activated

In VS Code terminal, you should see `(venv)` at the beginning of the prompt. If not:
- Open a new terminal in VS Code (`Ctrl+`` ` or `View > Terminal`)
- Run: `.\venv\Scripts\Activate.ps1` (Windows PowerShell)
- Or: `.\venv\Scripts\activate.bat` (Windows CMD)

### 3. Check .env File Location

Make sure `.env` file is in the project root (same folder as `main.py`):
```
Autonomous-Learning-Agent/
├── .env              ← Must be here
├── main.py
├── context_manager.py
└── venv/
```

### 4. Verify .env File Contents

Your `.env` file should contain:
```
GOOGLE_API_KEY=your_api_key_here
GEMINI_API_KEY=your_api_key_here
```

### 5. Reload VS Code Window

After making changes:
- Press `Ctrl+Shift+P`
- Type: `Developer: Reload Window`
- Press Enter

### 6. Test the Setup

Run this in VS Code terminal to verify:
```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', 'Found' if os.getenv('GOOGLE_API_KEY') else 'Not Found')"
```

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'dotenv'"
**Solution**: Make sure you're using the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
pip install python-dotenv langchain-google-genai
```

### Issue: "API key not found"
**Solution**: 
1. Check `.env` file exists in project root
2. Verify VS Code settings.json has: `"python.envFile": "${workspaceFolder}/.env"`
3. Restart VS Code

### Issue: "Model not found" error
**Solution**: The model name is already fixed to `gemini-2.5-flash`. If you still get this error, check your API key has access to Gemini models.

## VS Code Configuration Files Created

I've created these files to help VS Code work correctly:
- `.vscode/settings.json` - Configures Python interpreter and .env loading
- `.vscode/launch.json` - Debug configurations

## Still Having Issues?

1. Check VS Code Output panel (`View > Output`, select "Python")
2. Check Terminal output for error messages
3. Verify Python extension is installed and enabled

