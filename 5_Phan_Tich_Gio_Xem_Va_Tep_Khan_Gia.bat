@echo off
chcp 65001 > nul
echo ========================================================
echo   5. AI PHÂN TÍCH GIỜ XEM VÀNG & TỆP KHÁN GIẢ KÊNH
echo ========================================================
echo.
cd /d "C:\Users\Mochi\.gemini\antigravity\scratch\ai-channel-manager"

.\venv\Scripts\python audience_insights.py
echo.
pause
