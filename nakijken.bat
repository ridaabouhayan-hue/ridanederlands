@echo off
title NT2 Huiswerk Nakijker
cd /d "%~dp0"
cls
echo ===================================================
echo             NT2 HUISWERK NAKIJKER
echo ===================================================
echo.
echo 1. Notepad wordt nu geopend...
echo 2. Plak het huiswerk van de cursist in Notepad.
echo 3. Sla het bestand op (Ctrl + S) en sluit Notepad.
echo.
timeout /t 2 >nul
type nul > huiswerk.txt
start /wait notepad.exe huiswerk.txt
echo.
echo ===================================================
echo Bezig met nakijken via Gemini API...
echo ===================================================
echo.
python nakijken.py
echo.
echo ===================================================
pause
