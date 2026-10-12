import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def crawl_competitor_channel(channel_url: str, max_videos: int = 10):
    """
    Quét danh sách video có lượt view cao nhất hoặc mới nhất của đối thủ cạnh tranh bằng yt-dlp hoàn toàn miễn phí.
    """
    import yt_dlp
    print(f"\n[*] Đang quét kênh đối thủ: {channel_url}...")
    
    # Lấy thông tin video bao gồm title, views, duration, description
    ydl_opts = {
        'extract_flat': True,
        'playlistend': max_videos,
        'quiet': True,
        'no_warnings': True,
    }

    videos = []
    channel_name = "Đối thủ"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)
            channel_name = info.get('uploader') or info.get('channel') or info.get('title') or "Đối thủ"
            entries = info.get('entries', [])
            for item in entries:
                if item:
                    videos.append({
                        "title": item.get('title', ''),
                        "url": item.get('url', ''),
                        "views": item.get('view_count', 0),
                        "duration": item.get('duration', 0)
                    })
        except Exception as e:
            print(f"[!] Lỗi khi quét đối thủ: {e}")
            return None

    return {
        "channel_name": channel_name,
        "url": channel_url,
        "total_crawled": len(videos),
        "videos": videos
    }

def generate_viral_ideas_and_scripts(my_channel_topic: str, competitor_data_list: list, specific_goal: str = ""):
    """
    Kết hợp dữ liệu kênh đối thủ + chủ đề kênh của bạn để tìm ra HOOK ĐỘT PHÁ và KỊCH BẢN CHUẨN CHỈ.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Tổng hợp các tiêu đề và ý tưởng triệu view của đối thủ
    competitor_highlights = []
    for comp in competitor_data_list:
        comp_summary = f"Kênh: {comp.get('channel_name')}\n"
        for v in comp.get('videos', [])[:6]:
            views_str = f"{v.get('views'):,} views" if v.get('views') else "N/A"
            comp_summary += f" - Tiêu đề: \"{v.get('title')}\" ({views_str})\n"
        competitor_highlights.append(comp_summary)

    competitor_text = "\n\n".join(competitor_highlights)

    prompt = f"""
Bạn là Chuyên gia Đạo diễn & Sáng tạo nội dung (Content Strategist) đẳng cấp thế giới trên YouTube Shorts và TikTok.

THÔNG TIN ĐẦU VÀO:
1. Chủ đề cốt lõi của kênh tôi: "{my_channel_topic}"
2. Mục tiêu cụ thể / Định hướng: "{specific_goal}"
3. Dữ liệu các video triệu view / hot trend gần đây của CÁC KÊNH ĐỐI THỦ CÙNG NGÀNH:
---
{competitor_text}
---

NHIỆM VỤ CỦA BẠN:
Phân tích công thức thành công (winning patterns, góc tiếp cận, tâm lý tò mò) từ các video của đối thủ, sau đó tạo ra:

### PHẦN 1: BẢN PHÂN TÍCH XU HƯỚNG & GÓC TIẾP CẬN (Trend & Gap Analysis)
- Đâu là điểm mấu chốt khiến video của đối thủ hút view?
- Lỗ hổng nội dung (Content Gap) mà đối thủ chưa làm tốt nhưng kênh của tôi có thể làm hay hơn gấp 2 lần.

### PHẦN 2: 3 Ý TƯỞNG VIDEO ĐỈNH CAO (Độc quyền & Bắt trend)
Với mỗi ý tưởng, cung cấp:
- Tiêu đề giật tít (Title) tối ưu SEO & kích thích tò mò cực đại.
- Đối tượng người xem nhắm tới.
- Điểm khác biệt so với đối thủ.

### PHẦN 3: 1 KỊCH BẢN CHI TIẾT TỪNG GIÂY (Full Production Script - Chuẩn chỉ 45s-60s)
Chọn ra Ý TƯỞNG XUẤT SẮC NHẤT ở trên và viết kịch bản chi tiết:
- **0s - 3s (THE HOOK - QUYẾT ĐỊNH 80% THÀNH CÔNG):** 
  + Câu mở đầu giật tít, đánh trúng tâm lý, cấm người xem lướt đi.
  + Mô tả hình ảnh trên màn hình (Visual cue).
- **4s - 15s (THE CONTEXT / TẠO CĂNG THẲNG):**
  + Đưa ra vấn đề hoặc tình huống bất ngờ.
- **16s - 40s (THE CLIMAX / GIẢI QUYẾT VẤN ĐỀ):**
  + Cung cấp giá trị cao nhất / cú twist bất ngờ.
- **40s - 45s (THE CTA - CALL TO ACTION):**
  + Kêu gọi tương tác tự nhiên (Hỏi ý kiến khán giả / Follow để xem phần 2).
- **Lời dẫn Voice-Over:** Từng câu thoại người sáng tạo đọc, có đánh dấu nhịp điệu và cảm xúc.
"""

    if not api_key:
        print("[!] Chưa có GEMINI_API_KEY trong .env. Đang tạo kịch bản mẫu cấu trúc chuẩn...")
        return (
            "=== BẢN PHÂN TÍCH VÀ KỊCH BẢN MẪU (CHƯA NẠP GEMINI_API_KEY) ===\n\n"
            "💡 GÓC TIẾP CẬN TỪ ĐỐI THỦ:\n"
            "- Đối thủ tập trung vào tiêu đề câu hỏi kích thích tò mò.\n"
            "- Điểm yếu: Hook mở đầu còn dài dòng (mất 5s mới vào vấn đề chính).\n\n"
            "🔥 KỊCH BẢN CHUẨN CHỈ ĐỀ XUẤT (45 GIÂY):\n"
            "🎯 [0s - 3s HOOK]: 'Đừng bao giờ làm điều này nếu bạn không muốn hối hận!' (Hình ảnh giật zoom nhanh)\n"
            "📖 [4s - 20s BỐI CẢNH]: 'Đa số mọi người đều mắc lỗi này mà không hề nhận ra...'\n"
            "⚡ [21s - 38s CAO TRÀO]: 'Nhưng giải pháp thực sự lại đơn giản hơn bạn nghĩ rất nhiều, hãy xem kỹ bước này...'\n"
            "🚀 [39s - 45s CTA]: 'Bạn đã từng gặp tình huống này chưa? Bình luận bên dưới và follow kênh để không bỏ lỡ mẹo tiếp theo!'"
        )

    print("[*] Đang kết nối Gemini AI để phân tích xu hướng đối thủ & viết kịch bản chuẩn chỉ...")
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        return f"[!] Lỗi khi gọi Gemini: {e}"

def main():
    parser = argparse.ArgumentParser(description="AI Content Ideator & Scriptwriter dựa trên xu hướng đối thủ")
    parser.add_argument("--topic", type=str, default="", help="Chủ đề kênh của bạn (VD: 'Review công nghệ', 'Game hài', 'Kể chuyện kinh dị')")
    parser.add_argument("--competitors", nargs="+", default=[], help="Danh sách link kênh YouTube của các đối thủ cùng chủ đề")
    parser.add_argument("--goal", type=str, default="", help="Mục tiêu hoặc phong cách mong muốn")
    args = parser.parse_args()

    print("==================================================================")
    print(" 🧠 AI AGENT: LÊN Ý TƯỞNG & VIẾT KỊCH BẢN TỪ XU HƯỚNG ĐỐI THỦ")
    print("==================================================================")

    topic = args.topic
    if not topic:
        topic = input("👉 Nhập chủ đề kênh của bạn (VD: Gaming, Review phim, Kinh doanh, Podcast): ").strip()

    competitor_urls = args.competitors
    if not competitor_urls:
        comp_input = input("👉 Nhập Link kênh đối thủ cùng chủ đề (nhiều kênh cách nhau bởi dấu phẩy): ").strip()
        if comp_input:
            competitor_urls = [c.strip() for c in comp_input.split(",") if c.strip()]

    # Quét dữ liệu từng đối thủ
    competitor_data_list = []
    if competitor_urls:
        for url in competitor_urls:
            data = crawl_competitor_channel(url, max_videos=8)
            if data:
                competitor_data_list.append(data)
    else:
        print("[*] Không nhập link đối thủ cụ thể. AI sẽ dựa trên các xu hướng viral phổ biến nhất trong ngành này.")

    # Lập ý tưởng và kịch bản
    result_text = generate_viral_ideas_and_scripts(topic, competitor_data_list, specific_goal=args.goal)

    print("\n" + "="*65)
    print(" 📜 KẾT QUẢ PHÂN TÍCH Ý TƯỞNG & KỊCH BẢN CHUẨN CHỈ:")
    print("="*65)
    print(result_text)
    print("="*65)

    # Cơ chế dọn dẹp bộ nhớ: Xóa các bản kịch bản phân tích cũ trước khi ghi bản mới
    for old_script in OUTPUT_DIR.glob("SCRIPT_IDEAS_*.md"):
        try:
            old_script.unlink()
            print(f"[*] Đã tự động dọn dẹp file phân tích cũ: {old_script.name}")
        except Exception:
            pass

    # Xuất ra file để lưu trữ
    import re
    safe_topic = re.sub(r'[\\/*?:"<>| ]+', '_', topic)[:50]
    out_file = OUTPUT_DIR / f"SCRIPT_IDEAS_{safe_topic}.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# BẢN PHÂN TÍCH XU HƯỚNG & KỊCH BẢN VIDEO CHO CHỦ ĐỀ: {topic}\n\n")
        f.write(result_text)
    print(f"\n[+] Đã lưu toàn bộ bản kịch bản vào: {out_file.name}")

if __name__ == "__main__":
    main()
