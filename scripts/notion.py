"""
This module contains a simple function to get a Notion database using the Notion API.
"""

import requests
import config


def get_database():
    """
    Retrieves the Notion database specified in the config.
    """
    url = f"https://api.notion.com/v1/data_sources/{config.NOTION_DATABASE_ID}"
    headers = {
        "Authorization": f"Bearer {config.NOTION_API_KEY}",
        "Notion-Version": "2025-09-03",
        "Content-Type": "application/json",
    }

    # Using POST for query as per Notion API docs for databases/query
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        return response.json()

    print(f"Error: {response.status_code}")
    print(response.text)
    return None


if __name__ == "__main__":
    data = get_database()
    import json

    print(json.dumps(data, indent=2, ensure_ascii=False))
