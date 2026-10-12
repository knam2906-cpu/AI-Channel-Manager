@echo off
chcp 65001 > nul
echo ========================================================
echo        2. AI QUÉT SỐ LIỆU CHUYÊN SÂU STUDIO KÊNH
echo ========================================================
echo.
cd /d "C:\Users\Mochi\.gemini\antigravity\scratch\ai-channel-manager"

.\venv\Scripts\python studio_manager.py
echo.
pause
