import os
import sys
import json
import re
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_youtube_trending_keywords(keyword: str):
    """Lấy danh sách từ khóa tìm kiếm tăng đột biến trên YouTube qua Suggest Search API."""
    url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q={keyword}"
    trends = []
    try:
        r = requests.get(url, timeout=10)
        # Parse JSONP format: window.google.ac.h(["query",[["item1",...],["item2",...]]])
        match = re.search(r'\[".*?",\[(.*?)\]\]', r.text)
        if match:
            raw_items = re.findall(r'\["(.*?)",', match.group(1))
            trends = [item.encode('utf-8').decode('unicode-escape') if '\\u' in item else item for item in raw_items]
    except Exception as e:
        print(f"[!] Lỗi khi lấy YouTube trends: {e}")
    return trends[:8]

def get_tiktok_trending_keywords(keyword: str):
    """Lấy danh sách từ khóa tìm kiếm thịnh hành trên TikTok qua Auto-Suggest API."""
    url = f"https://www.tiktok.com/api/search/general/preview/?keyword={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    trends = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        sug_list = data.get("sug_list", [])
        for item in sug_list:
            text = item.get("content")
            if text:
                trends.append(text)
    except Exception as e:
        print(f"[!] Lỗi khi lấy TikTok trends: {e}")
    return trends[:8]

def get_viral_videos_yt(keyword: str, max_results: int = 6):
    """Cào các video YouTube Shorts có lượt xem cao nhất gần đây liên quan đến từ khóa."""
    import yt_dlp
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
    }
    videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            res = ydl.extract_info(f"ytsearch{max_results}:{keyword} Shorts", download=False)
            for e in res.get('entries', []):
                if e:
                    videos.append({
                        "title": e.get('title'),
                        "views": e.get('view_count', 'N/A'),
                        "url": f"https://youtu.be/{e.get('id')}"
                    })
        except Exception as e:
            print(f"[!] Lỗi khi quét video viral: {e}")
    return videos

def analyze_trends_with_ai(topic: str, yt_trends: list, tt_trends: list, viral_videos: list):
    """Dùng Gemini AI phân tích làn sóng xu hướng và gợi ý chủ đề 'Đón Sóng' bùng nổ."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "[!] Vui lòng cung cấp GEMINI_API_KEY trong .env."

    from google import genai
    client = genai.Client(api_key=api_key)

    data_payload = {
        "topic": topic,
        "youtube_search_surges": yt_trends,
        "tiktok_search_surges": tt_trends,
        "recent_viral_shorts": viral_videos
    }

    prompt = f"""
Bạn là Chuyên gia Săn Xu Hướng (Trend Hunter & Algorithm Strategist) cho TikTok và YouTube Shorts.
Dưới đây là BÁO CÁO CÁC TỪ KHÓA & VIDEO ĐANG TĂNG TRƯỞNG NÓNG NHẤT VỀ CHỦ ĐỀ: "{topic}":
{json.dumps(data_payload, ensure_ascii=False, indent=2)}

HÃY ĐƯA RA BẢN BÁO CÁO XU HƯỚNG THỰC CHIẾN (TREND RADAR):
1. 🌊 PHÂN TÍCH LÀN SÓNG TÌM KIẾM (Search Demand Spike):
   - Người xem trên TikTok và YouTube đang đổ xô đi tìm kiếm điều gì nhất liên quan đến chủ đề này? (Ví dụ: Mẹo cho người mới, pick cầu thủ, mùa thẻ mới, chỉnh tay cầm...).
   - Tại sao từ khóa này lại đột ngột nóng lên?
2. 🚀 3 Ý TƯỞNG VIDEO 'ĐÓN SÓNG' (RIDE THE WAVE):
   - Đề xuất 3 video ngắn 30s-45s nhắm thẳng vào các từ khóa nóng ở trên để ăn trọn lưu lượng tìm kiếm (Search Traffic) và đề xuất.
   - Mỗi ý tưởng phải kèm theo **1 TIÊU ĐỀ GIẬT TÍT** và **1 HOOK 3 GIÂY ĐẦU** kích thích tò mò tột độ.
3. 🏷️ BỘ HASHTAGS ĐỀ XUẤT ĂN TREND:
   - Danh sách 5-8 hashtag chuẩn SEO thịnh hành nhất để gắn vào caption video.
"""
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        return f"[!] Lỗi khi gọi Gemini: {e}"

def main():
    parser = argparse.ArgumentParser(description="Theo dõi xu hướng nóng trên TikTok & YouTube (Trend Radar)")
    parser.add_argument("--topic", type=str, default="", help="Chủ đề cần bắt trend (VD: 'FC Online', 'FC Mobile', 'Game bắn súng')")
    args = parser.parse_args()

    topic = args.topic
    if not topic:
        print("==================================================================")
        print(" 📡 AI AGENT: RADAR SĂN XU HƯỚNG NÓNG TRÊN TIKTOK & YOUTUBE")
        print("==================================================================")
        topic = input("👉 Nhập chủ đề hoặc tựa game muốn bắt trend (Mặc định: FC Online): ").strip()
        if not topic:
            topic = "FC Online"

    print(f"\n[*] Đang quét làn sóng tìm kiếm nóng cho: '{topic}'...")

    # 1. Quét từ khóa nóng YouTube & TikTok
    yt_trends = get_youtube_trending_keywords(topic)
    tt_trends = get_tiktok_trending_keywords(topic.replace(" ", ""))

    # 2. Quét video viral gần đây
    viral_videos = get_viral_videos_yt(topic, max_results=5)

    print("\n" + "="*65)
    print(f" 📊 TỪ KHÓA & CHỦ ĐỀ ĐANG TĂNG TRƯỞNG NÓNG: {topic.upper()}")
    print("="*65)
    print("▶️ [YOUTUBE SEARCH SURGES]:")
    for kw in yt_trends:
        print(f"  🔥 {kw}")

    print("\n🎵 [TIKTOK SEARCH SURGES]:")
    for kw in tt_trends:
        print(f"  🔥 {kw}")

    print("\n🎬 [TOP VIDEO VIRAL GẦN ĐÂY]:")
    for v in viral_videos[:4]:
        v_str = f"({v['views']:,} views)" if isinstance(v['views'], int) else f"({v['views']})"
        print(f"  ⚡ {v['title']} {v_str}")

    # 3. AI Phân tích đón sóng
    print("\n" + "-"*65)
    print(" 🤖 GEMINI AI PHÂN TÍCH XU HƯỚNG & ĐỀ XUẤT VIDEO ĐÓN SÓNG:")
    print("-"*65)
    ai_analysis = analyze_trends_with_ai(topic, yt_trends, tt_trends, viral_videos)
    print(ai_analysis)
    print("="*65)

    # 4. Cơ chế dọn dẹp bộ nhớ: Xóa các báo cáo trend cũ trước khi lưu mới
    for old_trend in OUTPUT_DIR.glob("TREND_RADAR_*.md"):
        try:
            old_trend.unlink()
            print(f"[*] Đã tự động dọn dẹp file xu hướng cũ: {old_trend.name}")
        except Exception:
            pass

    safe_topic = re.sub(r'[\\/*?:"<>| ]+', '_', topic)[:50]
    out_file = OUTPUT_DIR / f"TREND_RADAR_{safe_topic}.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# BÁO CÁO RADAR XU HƯỚNG NÓNG: {topic}\n\n")
        f.write(ai_analysis)
    print(f"\n[+] Báo cáo đón sóng xu hướng đã lưu tại: {out_file.name}")

if __name__ == "__main__":
    main()
