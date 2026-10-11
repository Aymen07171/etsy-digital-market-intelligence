@echo off
title eRank Pro - Etsy Digital Market Intelligence Standalone App
cd /d "%~dp0"
echo Starting Etsy Market Intelligence Standalone Application Server...
.\.venv\Scripts\python.exe app.py
pause
