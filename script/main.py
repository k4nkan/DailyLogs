"""
Fetch daily logs from Supabase (UTC), convert to JST day, and push to Notion.
"""

import os
from datetime import datetime, timedelta, timezone

import requests
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATASOURCE_ID = os.getenv("NOTION_DATASOURCE_ID")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def push_daily_log(date: str, text: str):
    """
    Push daily log to Notion.
    """
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2025-09-03",
        "Content-Type": "application/json",
    }

    body = {
        "parent": {"data_source_id": NOTION_DATASOURCE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": date}}]},
            "Date": {"date": {"start": date}},
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": text}}]},
            }
        ],
    }

    r = requests.post(url, headers=headers, json=body, timeout=10)
    r.raise_for_status()


JST = timezone(timedelta(hours=9))


def main():
    """
    Fetch daily logs from Supabase (UTC), convert to JST day, and push to Notion.
    """
    target_jst = datetime.now(JST) - timedelta(days=1)

    start_jst = target_jst.replace(hour=0, minute=0, second=0, microsecond=0)
    end_jst = start_jst + timedelta(days=1)

    start_utc = start_jst.astimezone(timezone.utc)
    end_utc = end_jst.astimezone(timezone.utc)

    res = (
        supabase.table("logs")
        .select("content, created_at")
        .gte("created_at", start_utc.isoformat())
        .lt("created_at", end_utc.isoformat())
        .order("created_at")
        .execute()
    )

    logs = res.data or []

    if not logs:
        print("no logs for today")
        return

    lines = []

    for log in logs:
        t = datetime.fromisoformat(log["created_at"]).astimezone(JST).strftime("%H:%M")
        lines.append(f"[{t}] {log['content']}")

    logs = "\n".join(lines)

    date_str = start_jst.strftime("%Y-%m-%d")
    push_daily_log(date_str, logs)

    print(f"pushed {len(lines)} logs for {date_str}")


if __name__ == "__main__":
    main()
