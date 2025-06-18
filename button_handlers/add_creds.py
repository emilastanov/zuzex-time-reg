from telegram import Update
from telegram.ext import ContextTypes

from texts.zuzex import ADD_PROFILE


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    answer = ADD_PROFILE

    await query.edit_message_text(
        text=answer,
        parse_mode="HTML",
    )
