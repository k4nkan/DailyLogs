"""
Fetch daily logs from Supabase (UTC), convert to JST day, and push to Notion.
"""

from datetime import datetime, timedelta, timezone
from diary.diary_builder import build_daily_diary_text
from diary.notion_client import push_diary
from music.spotify_summary import fetch_top_track_on_date

JST = timezone(timedelta(hours=9))


def main():
    """
    Fetch daily logs from Supabase (UTC), convert to JST day, and push to Notion.
    """
    target_jst = datetime.now(JST) - timedelta(days=1)
    date_str = target_jst.strftime("%Y-%m-%d")
    print(f"⌛️ : target_jst: {target_jst}")

    top_track = fetch_top_track_on_date(date_str)
    diary_text = build_daily_diary_text(target_jst)
    print(f"✅ : built diary for {date_str}")

    push_diary(date_str, diary_text, top_track)
    print(f"✅ : pushed diary for {date_str}")


if __name__ == "__main__":
    main()
