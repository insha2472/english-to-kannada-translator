#!/usr/bin/env bash
# Create and activate a Python virtual environment (macOS / Linux)
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "Virtual environment created in ./venv"
else
  echo "Virtual environment already exists in ./venv"
fi

echo "To activate run:"
echo "  source venv/bin/activate"
echo "Then run the translator:"
echo "  python t.py"
