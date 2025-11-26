"""config for discord bot"""

import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATASOURCE_ID = os.getenv("NOTION_DATASOURCE_ID")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
