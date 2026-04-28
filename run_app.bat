@echo off
REM SCM Parcel Damage Inspection - one-click launcher
setlocal
cd /d "%~dp0"

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

echo.
echo ============================================
echo   SCM Parcel Damage Inspection (YOLOv8m)
echo ============================================
echo.
echo Opening dashboard at http://localhost:8501
echo Press Ctrl+C in this window to stop.
echo.

streamlit run streamlit_app.py --server.port 8501 --server.headless false
