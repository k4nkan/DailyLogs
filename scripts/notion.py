"""
Dump Notion page contents to CSV.
"""

import config
import pandas as pd
import requests

BASE_HEADERS = {
    "Authorization": f"Bearer {config.NOTION_API_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json",
}


def query_data_source():
    """
    Query Notion data_source.
    """
    url = f"https://api.notion.com/v1/data_sources/{config.NOTION_DATASOURCE_ID}/query"
    resp = requests.post(url, headers=BASE_HEADERS, json={}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_page_content(page_id: str):
    """
    Get Notion page content.
    """
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    resp = requests.get(url, headers=BASE_HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main():
    """
    Main function.
    """
    data = query_data_source()

    rows = []
    for page in data["results"]:
        page_id = page["id"]
        content = get_page_content(page_id)

        texts = []
        for block in content.get("results", []):
            if block["type"] == "paragraph":
                rich = block["paragraph"]["rich_text"]
                text = "".join([t["plain_text"] for t in rich])
                texts.append(text)

        rows.append(
            {
                "id": page_id,
                "content": "\n".join(texts),
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv("page_contents.csv", index=False)


if __name__ == "__main__":
    main()
