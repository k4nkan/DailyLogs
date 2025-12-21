"""
Fetch daily top tracks from Supabase and return as JSON.
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SONG_SUPABASE_URL = os.getenv("SONG_SUPABASE_URL")
SONG_SUPABASE_KEY = os.getenv("SONG_SUPABASE_KEY")

supabase = create_client(SONG_SUPABASE_URL, SONG_SUPABASE_KEY)


def fetch_top_track_on_date(date_jst: str) -> Optional[Dict]:
    """
    Return top track on a JST date.
    """
    res = supabase.rpc(
        "top_track_on_date_jst",
        {"target_date": date_jst},
    ).execute()

    if not res.data:
        return None

    t = res.data[0]

    print(f"✅ : fetched top track for {date_jst}")

    return {
        "title": t["track_name"],
        "artist": t["artist_name"],
        "plays": t["play_count"],
        "spotify_url": t["track_url"],
        "image_url": t["image_url"],
    }
