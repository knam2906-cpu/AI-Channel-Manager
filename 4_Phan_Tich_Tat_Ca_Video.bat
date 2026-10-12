@echo off
chcp 65001 > nul
echo ========================================================
echo   4. AI PHÂN TÍCH TOÀN BỘ TẤT CẢ VIDEO TRÊN KÊNH
echo ========================================================
echo.
cd /d "C:\Users\Mochi\.gemini\antigravity\scratch\ai-channel-manager"

.\venv\Scripts\python full_video_audit.py
echo.
pause
