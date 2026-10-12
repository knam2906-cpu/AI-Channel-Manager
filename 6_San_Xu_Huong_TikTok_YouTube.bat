@echo off
chcp 65001 > nul
echo ========================================================
echo   6. AI RADAR SĂN XU HƯỚNG NÓNG (TIKTOK ^& YOUTUBE)
echo ========================================================
echo.
cd /d "C:\Users\Mochi\.gemini\antigravity\scratch\ai-channel-manager"

set /p TOPIC="Nhập chủ đề/tựa game bạn muốn bắt trend (hoặc nhấn ENTER để dùng mặc định FC Online): "

echo.
echo [*] Đang quét làn sóng tìm kiếm nóng trên TikTok và YouTube...
if "%TOPIC%"=="" (
    .\venv\Scripts\python trend_radar.py
) else (
    .\venv\Scripts\python trend_radar.py --topic "%TOPIC%"
)

echo.
echo [+] Mở thư mục outputs để xem bản báo cáo đón sóng...
start "" "C:\Users\Mochi\.gemini\antigravity\scratch\ai-channel-manager\outputs"
pause
