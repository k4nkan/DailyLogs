"""
Push daily log to Notion.
"""

import requests

from app.configs.notion_config import NOTION_API_KEY, NOTION_DATASOURCE_ID


def push_daily_log(date: str, text: str):
    """Push daily log to Notion."""

    print("DEBUG DB ID =", NOTION_DATASOURCE_ID)

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
