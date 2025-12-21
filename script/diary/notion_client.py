"""
Push diary page to Notion.
- Daily Logs section first
- Song section second
- Section titles are bold
- One blank line between sections
"""

import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATASOURCE_ID = os.getenv("NOTION_DATASOURCE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json",
}


def push_diary(
    date_str: str,
    diary_text: str,
    top_track: Optional[Dict],
):
    """
    Push diary page to Notion with left-aligned layout.
    """
    children: list[dict] = []

    # =========================
    # 📓 Daily Logs Section (FIRST)
    # =========================
    if diary_text:
        children.append(
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "text": {"content": "/  Daily Logs"},
                            "annotations": {"bold": True},
                        }
                    ],
                    "icon": {"emoji": "📓"},
                    "color": "orange_background",
                },
            }
        )

        children.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": diary_text}}]},
            }
        )

        # --- blank line between sections ---
        children.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []},
            }
        )

    # =========================
    # 🎧 Song Section (SECOND)
    # =========================
    if top_track and top_track.get("spotify_url"):
        children.append(
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "text": {"content": "/  Song"},
                            "annotations": {"bold": True},
                        }
                    ],
                    "icon": {"emoji": "🎧"},
                    "color": "orange_background",
                },
            }
        )

        caption = (
            f"{top_track['title']} / "
            f"by {top_track['artist']} / "
            f"{top_track['plays']} Played"
        )

        # Left-aligned embed via 2 columns
        children.append(
            {
                "object": "block",
                "type": "column_list",
                "column_list": {
                    "children": [
                        {
                            "object": "block",
                            "type": "column",
                            "column": {
                                "children": [
                                    {
                                        "object": "block",
                                        "type": "embed",
                                        "embed": {
                                            "url": top_track["spotify_url"],
                                        },
                                    },
                                    {
                                        "object": "block",
                                        "type": "paragraph",
                                        "paragraph": {
                                            "rich_text": [
                                                {
                                                    "text": {"content": caption},
                                                    "annotations": {"italic": True},
                                                }
                                            ]
                                        },
                                    },
                                ]
                            },
                        },
                        {
                            # Empty right column for spacing
                            "object": "block",
                            "type": "column",
                            "column": {"children": []},
                        },
                    ]
                },
            }
        )

    body = {
        "parent": {"data_source_id": NOTION_DATASOURCE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": date_str}}]},
            "Date": {"date": {"start": date_str}},
        },
        "children": children,
    }

    r = requests.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS,
        json=body,
        timeout=10,
    )
    r.raise_for_status()
