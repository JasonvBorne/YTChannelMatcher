import json
import pandas as pd
from pathlib import Path
from ytchannelmatcher.YouTubeSearcher import  YouTubeSearcher

CSV_PATH   = Path("../result/combined_channels.csv")
OUTPUT_JSON = Path("../result/channels_300.json")
MAX_ROWS   = 300        # 只取前 300 行

def build_channel_url_snippet(snippet):
    """根据 snippet 生成频道 URL 与频道 id（@custom 或 UC...）"""
    custom = snippet.get("customUrl")        # 自定义 URL，形如 '@phlearn'
    cid    = snippet.get("channelId") or snippet.get("id")
    if custom:               # 优先用自定义句柄
        return f"https://www.youtube.com/{custom}", custom
    return f"https://www.youtube.com/channel/{cid}", cid

def create_json(youtube, csv_path: Path, output_file: Path, limit: int = 1):
    df = pd.read_csv(csv_path, nrows=limit)
    rows = []

    for _, row in df.iterrows():
        channel_id = row["channelId"]
        first_video_id = row["videoId"].split(",")[0]

        # --- 获取元数据 ---
        ch_meta  = youtube.get_channel_metadata(channel_id) or {}
        vid_meta = youtube.get_video_metadata(first_video_id) or {}

        snippet_ch = ch_meta.get("snippet", {})
        stats_ch   = ch_meta.get("statistics", {})
        branding   = ch_meta.get("brandingSettings", {}).get("channel", {})

        # 频道 URL / 句柄
        ch_url, ch_handle = build_channel_url_snippet({**snippet_ch, "channelId": channel_id})

        # 频道封面（用 high，没有则 default）
        thumb_obj  = snippet_ch.get("thumbnails", {})
        head_pic   = thumb_obj.get("high", thumb_obj.get("default", {})).get("url", "")

        # 视频标题 & 链接
        vid_snippet = vid_meta.get("snippet", {})
        video_item = {
            "title": vid_snippet.get("title", ""),
            "link":  f"https://www.youtube.com/watch?v={first_video_id}"
        }

        rows.append({
            "title":      snippet_ch.get("title", ""),
            "channel_url": ch_url,
            "channel_id":  ch_handle,
            "publishedAt": snippet_ch.get("publishedAt", ""),
            "statistics": {
                "viewCount":      stats_ch.get("viewCount", ""),
                "subscriberCount": stats_ch.get("subscriberCount", ""),
                "videoCount":      stats_ch.get("videoCount", "")
            },
            "head_pic": head_pic,
            "keywords": branding.get("keywords", ""),
            "videos":   [video_item]          # 这里只放了第 0 个视频，如需更多可扩展
        })

    # ⚠️ 写入 JSON，确保非 ASCII 字符保留
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"✅ 生成完成 → {output_file.resolve()}  (共 {len(rows)} 条)")

# === 调用示例 ===
if __name__ == "__main__":
    # 你已有的 YouTubeSearcher 实例
    youtube = YouTubeSearcher(api_key="AIzaSyDwQtpdrdsmuRsawPAAWYa6zZ21KaH39pY", proxy_url="http://127.0.0.1:1080")
    create_json(youtube, CSV_PATH, OUTPUT_JSON, MAX_ROWS)