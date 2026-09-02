# Install Guide

## 1. Install python

https://www.python.org/ftp/python/

We've tested in py 3.10.5 and py 3.14.2

## 2. Install requirements

Create virtual environment (recommended):

macOS / Linux:
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows (PowerShell):
```
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 3. Download nodejs

https://nodejs.org/en/download

## 4. Install typescript

```
npm install -g typescript
```

## 5. Compile ts to js

Windows:
- Double click to run "\public\js\watch.bat"

macOS / Linux:
```
cd public/js
tsc --watch
```

Compile once (all platforms):
```
cd public/js
tsc
```

## 6. Download assets

You need to download the game to gain its `assets` folder from [itch.io](https://irefrixs.itch.io/marvel-lcg) and put it in the root folder of this project

## 7. Start the game

Windows:
```
py -m venv .venv
.venv\Scripts\Activate.ps1
python main.py
```

macOS / Linux:
```
python3.12 -m venv .venv
source .venv/bin/activate
python main.py
```

## Troubleshooting

### 1. `ImportError: cannot import name 'TypeGuard' from 'typing'`

Your Python is too old (usually 3.9).

Use Python 3.10+ and recreate venv:
```
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. `ModuleNotFoundError: No module named 'numpy'`

Install dependencies from this project's venv:
```
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 3. `AssertionError: ip='127.0.0.1', port=2345` or bind `operation not permitted`

Another process may already use port 2345, or your environment blocks local bind.

Check port usage:
```
lsof -nP -iTCP:2345 -sTCP:LISTEN
```

If a stale Python process is still holding the port, clean it up before restarting:
```
pkill -f 'python.*main.py' || pkill -f 'python3.*main.py' || true
kill -9 (31752)
```

If needed, run from macOS Terminal (outside restricted/sandboxed runner).

### 4. `file_path='./module/card_statistics.js'` (404 / missing js)

TypeScript output is missing. Compile frontend scripts:
```
cd public/js
tsc
```

### 5. `sh: title: command not found`

This was a Windows-only title command. It has been made cross-platform in code and is safe to ignore on older versions.
