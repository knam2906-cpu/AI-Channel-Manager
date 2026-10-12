# HƯỚNG DẪN HỆ THỐNG: QUẢN TRỊ KÊNH & LÊN KỊCH BẢN CHUẨN CHỈ TỪ ĐỐI THỦ

Hệ thống được thiết kế hoàn toàn **MIỄN PHÍ 100%**, không cần tạo tài khoản lập trình viên, không cần thẻ visa/thanh toán.

Dự án nằm tại: `C:\Users\Mochi\.gemini\antigravity\scratch\ai-channel-manager`

---

## BƯỚC 1: ĐĂNG NHẬP STUDIO KÊNH CỦA BẠN (Chỉ làm 1 lần)
- Click đúp vào: `1_Dang_Nhap_Studio.bat`
- Một cửa sổ trình duyệt Chrome sẽ mở ra hai trang: `studio.youtube.com` và `tiktok.com/creator-center`.
- Bạn tiến hành đăng nhập tài khoản kênh của bạn.
- Sau khi vào được giao diện Studio, hãy **đóng cửa sổ Chrome lại**. Phiên đăng nhập (Cookies) sẽ được lưu lại vĩnh viễn trên máy tính bạn trong thư mục an toàn `browser_session`.

---

## BƯỚC 2: QUÉT SỐ LIỆU CHUYÊN SÂU NỘI BỘ KÊNH
- Click đúp vào: `2_Doc_So_Lieu_Studio.bat`
- AI Agent sẽ tự động chạy ngầm, vào Studio đọc số liệu Subscribers, hiệu suất video mới nhất, và các thẻ thống kê 28 ngày qua.
- Dữ liệu lưu tại: `outputs\my_channel_studio_data.json`.

---

## BƯỚC 3: PHÂN TÍCH ĐỐI THỦ & VIẾT KỊCH BẢN CHUẨN CHỈ (HOOK 3S ĐỈNH CAO)
- Click đúp vào: `3_Phan_Tich_Doi_Thu_Va_Kich_Ban.bat`
- Nhập chủ đề kênh của bạn (ví dụ: *Review game, Tài chính, Phim tóm tắt*).
- Nhập link các kênh đối thủ triệu view cùng ngành (ví dụ: `https://www.youtube.com/@kenhA, https://www.youtube.com/@kenhB`).
- **AI Agent sẽ tự động:**
  1. Cào toàn bộ danh sách video nhiều view nhất của đối thủ.
  2. Phân tích lỗ hổng nội dung (Content Gap) mà đối thủ chưa làm tốt.
  3. Đề xuất 3 Ý tưởng đột phá bắt trend.
  4. **Viết 1 kịch bản chuẩn chỉ từng giây (Full Production Script):**
     - **0s - 3s (The Hook):** Câu mở đầu giật tít đánh trúng tâm lý tò mò + chỉ đạo hình ảnh giật zoom.
     - **4s - 15s (Context):** Đưa ra vấn đề/căng thẳng.
     - **16s - 40s (Climax):** Giá trị cốt lõi / Cú twist.
     - **40s - 45s (CTA):** Kêu gọi tương tác, follow.
     - Lời dẫn Voice-Over chi tiết từng từ để bạn đọc thu âm.
- File kịch bản sẽ được lưu dưới dạng Markdown tại thư mục: `outputs`.

---

## LƯU Ý KÍCH HOẠT TRÍ TUỆ NHÂN TẠO GEMINI (Miễn phí 100%)
Mở file `.env` trong thư mục dự án và dán API Key miễn phí từ Google AI Studio:
```env
GEMINI_API_KEY=AIzaSy...
```
*(Lấy key miễn phí chỉ trong 30 giây tại: https://aistudio.google.com/app/apikey)*
