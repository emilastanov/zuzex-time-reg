from telegram import Update
from telegram.ext import ContextTypes

from texts.errors import COMMON_ERROR
from utils.log_answer import log_answer, sys_log


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    await sys_log(f"Exception occurred: {context.error}")

    try:
        if isinstance(update, Update):
            message = update.message

            await message.reply_text(COMMON_ERROR, parse_mode="Markdown")
            await log_answer(COMMON_ERROR, message)
    except Exception as e:
        await sys_log(f"Ошибка при отправке сообщения об ошибке: {e}")
