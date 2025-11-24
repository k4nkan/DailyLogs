"""
This module contains a simple Discord bot that replies to mentions with random messages.
"""

import random
import discord
import config

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """
    Event handler called when the bot is ready.
    """
    print("Ready!")


@client.event
async def on_message(message):
    """
    Event handler called when a message is received.

    Args:
        message (discord.Message): The message object received.
    """

    if message.author == client.user:
        return

    if client.user in message.mentions:

        answer_list = [
            "さすがですね！",
            "知らなかったです！",
            "すごいですね！",
            "センスが違いますね！",
            "そうなんですか？",
        ]
        answer = random.choice(answer_list)
        print(answer)
        await message.channel.send(answer)


client.run(config.DISCORD_TOKEN)
