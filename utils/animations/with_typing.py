import asyncio
from functools import wraps
from telegram.constants import ChatAction


def with_typing(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        chat_id = update.effective_chat.id

        async def typing_loop():
            try:
                while True:
                    await context.bot.send_chat_action(
                        chat_id=chat_id, action=ChatAction.TYPING
                    )
                    await asyncio.sleep(3)
            except asyncio.CancelledError:
                pass

        typing_task = asyncio.create_task(typing_loop())

        try:
            return await func(update, context, *args, **kwargs)
        finally:
            typing_task.cancel()

    return wrapper
