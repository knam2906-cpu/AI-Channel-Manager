@echo off
chcp 65001 > nul
echo ========================================================
echo        1. ĐĂNG NHẬP PHIÊN YOUTUBE STUDIO & TIKTOK
echo ========================================================
echo.
cd /d "C:\Users\Mochi\.gemini\antigravity\scratch\ai-channel-manager"

.\venv\Scripts\python studio_manager.py --login
pause
