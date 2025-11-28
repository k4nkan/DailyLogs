"""
Discord bot.
"""

import discord
from discord.ext import commands

from app.bot.handlers import handle_message
from app.configs.discord_config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Event handler called when the bot is ready."""
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
    """Event handler called when a message is received."""
    await handle_message(message)


def start_bot():
    """Start the bot."""
    bot.run(DISCORD_TOKEN)
