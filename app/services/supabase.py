"""
Supabase client + message save/load logic
"""

from datetime import datetime, timedelta
from supabase import create_client
from app.configs.supabase_config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def save_message(content: str, timestamp: datetime):
    """
    Save message to Supabase.
    """
    jst_ts = timestamp + timedelta(hours=9)

    supabase.table("messages").insert(
        {
            "content": content,
            "timestamp": jst_ts.isoformat(),
            "date": jst_ts.date().isoformat(),
        }
    ).execute()


def get_daily_messages(timestamp: datetime):
    """
    Get daily messages from Supabase.
    """
    jst_ts = timestamp + timedelta(hours=9)
    date_str = jst_ts.date().isoformat()

    res = (
        supabase.table("messages")
        .select("*")
        .eq("date", date_str)
        .order("timestamp")
        .execute()
    )

    return res.data
