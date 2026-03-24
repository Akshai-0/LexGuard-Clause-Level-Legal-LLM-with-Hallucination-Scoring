@echo off
title AI Legal Auditor Starter
color 0B

echo ===================================================
echo   Starting AI Legal Auditor (Black and Blue Theme)
echo ===================================================
echo.

REM Move to the folder where this BAT file exists
cd /d "%~dp0"

REM Launch Streamlit through Python
python -m streamlit run UI.py

pause
