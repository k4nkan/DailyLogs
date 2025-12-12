"""
Discord bot for DailyLogs.
"""

import os
from datetime import datetime, timezone

import discord
from dotenv import load_dotenv
from supabase import create_client, PostgrestAPIError

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ACK_MESSAGES = [
    "なるほど",
    "ふむふむ",
    "ちゃんと記録しておくよ",
    "そうだったんだ",
]


@client.event
async def on_ready():
    """on_ready event handler."""
    print(f"[bot] logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    """on_message event handler."""
    if message.author.bot:
        return

    content = message.content.strip()
    if not content:
        return

    try:
        supabase.table("logs").insert(
            {
                "content": content,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ).execute()
    except PostgrestAPIError as e:
        print("[error] supabase insert failed:", e)
        return

    ack = ACK_MESSAGES[hash(content) % len(ACK_MESSAGES)]
    await message.channel.send(ack)


client.run(DISCORD_TOKEN)
