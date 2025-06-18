from telegram import Update
from telegram.ext import filters, ContextTypes

from texts.hello import RANDOM_MSG_ANSWER
from utils.log_answer import log_answer, sync_sys_log
from utils.animations.with_typing import with_typing

handler_filters = (
    filters.TEXT | filters.Document.ALL | filters.Sticker.ALL | filters.VIDEO
)


@with_typing
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if update.message.video:
        sync_sys_log("📦 video_id:", message.video.file_id)

    await message.reply_text(RANDOM_MSG_ANSWER, parse_mode="Markdown")
    await log_answer(RANDOM_MSG_ANSWER, message)
