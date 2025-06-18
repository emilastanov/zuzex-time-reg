import asyncio
from functools import wraps
from telegram.constants import ChatAction


def with_typing_and_updates(messages=None):
    if messages is None:
        messages = [
            "🔍 Приступил к работе...",
            "💡 Думаю над твоим запросом...",
            "📌 Подбираю варинты ответа...",
            "✍️ Готовлю рекомендации...",
            "🧾 Финализирую выводы...",
            "⏳ Почти готово...",
            "✅ Последние штрихи...",
        ]

    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            chat_id = update.effective_chat.id
            message_index = 0

            async def typing_loop():
                nonlocal message_index
                try:
                    while True:
                        await context.bot.send_chat_action(
                            chat_id=chat_id, action=ChatAction.TYPING
                        )

                        if message_index < len(messages):
                            await context.bot.send_message(
                                chat_id=chat_id, text=messages[message_index]
                            )
                            message_index += 1

                        await asyncio.sleep(3)
                except asyncio.CancelledError:
                    pass

            typing_task = asyncio.create_task(typing_loop())

            try:
                return await func(update, context, *args, **kwargs)
            finally:
                typing_task.cancel()

        return wrapper

    return decorator
