from telegram.ext import ContextTypes
from datetime import datetime
from telegram import Update

from utils.log_answer import log_answer


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    now = datetime.now()
    formatted = now.strftime("%d:%m:%Y %H:%M")

    await message.reply_text(formatted)
    await log_answer(formatted, message)
