"""
Handle message.
"""

from app.services.supabase import save_message


async def handle_message(message):
    """
    Handle message.
    """
    if message.author.bot:
        return

    await save_message(
        content=message.content,
        timestamp=message.created_at,
    )
