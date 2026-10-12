@echo off
chcp 65001 > nul
echo ========================================================
echo   3. AI PHÂN TÍCH ĐỐI THỦ & TẠO KỊCH BẢN CHUẨN CHỈ
echo ========================================================
echo.
cd /d "C:\Users\Mochi\.gemini\antigravity\scratch\ai-channel-manager"

set /p TOPIC="Nhập chủ đề kênh của bạn (VD: Gaming, Review phim, Mẹo công nghệ): "
set /p COMPS="Nhập link kênh đối thủ cùng ngành (cách nhau bằng dấu phẩy): "

echo.
echo [*] Đang cào dữ liệu đối thủ và dùng AI viết kịch bản...
.\venv\Scripts\python competitor_ideator.py --topic "%TOPIC%" --competitors %COMPS%

echo.
echo [+] Mở thư mục chứa file kịch bản kết quả...
start "" "C:\Users\Mochi\.gemini\antigravity\scratch\ai-channel-manager\outputs"
pause
