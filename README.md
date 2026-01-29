LIVE DEMO: https://english-to-kannada-translator-6-a5ac.onrender.com

# English → Kannada Translator

This workspace contains two interfaces:
- `t.py` — simple command-line translator (no external packages required).
- `t.html` — improved browser UI that uses Google's free translate endpoint when online and falls back to a small offline dictionary.

Quick run (Python):

Windows (PowerShell / CMD):

```powershell
python t.py
```

Linux / macOS:

```bash
python3 t.py
```

Create a virtual environment (optional):

Windows (run in project folder):

```powershell
.\create_venv.bat
# then
.\venv\Scripts\activate
python t.py
```

macOS / Linux:

```bash
./create_venv.sh
source venv/bin/activate
python t.py
```

Open the browser UI:

```powershell
start t.html
# or double-click t.html
```

Notes:
- The HTML UI uses an unofficial Google endpoint; if rate-limited or offline it will use the built-in fallback dictionary.
- `t.py` uses only Python standard library modules.


