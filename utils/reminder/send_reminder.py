from telegram.ext import ContextTypes

from services.tg.context import ContextManager
from texts.reminder import REMINDER_LIST
from utils.log_answer import sys_log


async def send_reminder(context: ContextTypes.DEFAULT_TYPE):

    chat_id = context.job.chat_id

    await context.bot.send_message(chat_id=context.job.chat_id, text=context.job.data)

    job_name = context.job.name
    await sys_log("Джоба исполнилась", job_name)
    if job_name.startswith("once"):
        ContextManager.remove_from_list(
            context.application.user_data[chat_id],
            REMINDER_LIST,
            lambda r: r["job_name"] == job_name,
        )
        await ContextManager.commit(context, chat_id)
        await sys_log("Джоба удалилась из контекста", job_name)
