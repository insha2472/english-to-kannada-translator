@echo off
REM Create and activate a Python virtual environment (Windows)
IF NOT EXIST "venv" (
    python -m venv venv
    echo Virtual environment created in .\venv
) ELSE (
    echo Virtual environment already exists in .\venv
)

echo To activate run:
echo    .\venv\Scripts\activate
echo Then run the translator:
echo    python t.py
