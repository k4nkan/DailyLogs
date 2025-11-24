"""
This module contains a simple Discord bot that replies to mentions with random messages.
"""

import random
import discord
import config

intents = discord.Intents.all()
client = discord.Client(intents=intents)


# Bot起動時に呼び出される関数
@client.event
async def on_ready():
    """
    Event handler called when the bot is ready.
    """
    print("Ready!")


# メッセージの検知
@client.event
async def on_message(message):
    """
    Event handler called when a message is received.

    Args:
        message (discord.Message): The message object received.
    """
    # 自身が送信したメッセージには反応しない
    if message.author == client.user:
        return

    # ユーザーからのメンションを受け取った場合、あらかじめ用意された配列からランダムに返信を返す
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


# Bot起動
client.run(config.DISCORD_TOKEN)
