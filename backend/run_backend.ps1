
# Run the FastAPI backend for Suffolk KB
# Usage: powershell -ExecutionPolicy Bypass -File run_backend.ps1

$env:PYTHONPATH = "$PSScriptRoot"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
