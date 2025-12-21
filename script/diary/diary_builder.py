"""
Build daily diary text for a JST date.
"""

import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

JST = timezone(timedelta(hours=9))


def build_daily_diary_text(date_jst: datetime) -> str:
    """
    Build diary text for a JST date.
    """
    start_jst = date_jst.replace(hour=0, minute=0, second=0, microsecond=0)
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

    lines: list[str] = []

    for log in res.data or []:
        t = datetime.fromisoformat(log["created_at"]).astimezone(JST).strftime("%H:%M")
        lines.append(f"[{t}] {log['content']}")

    return "\n".join(lines)
