from telegram.ext import ContextTypes
from telegram import Update

from crud.find_or_create_user import find_or_create_user
from services.tg.context import ContextManager
from texts.reminder import REMINDER_LIST
from utils.log_answer import log_answer


def cancel_all_jobs_for_user(context, user_id):
    for job in context.job_queue.jobs():
        if job.chat_id == user_id:
            job.schedule_removal()


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    user_data, _ = await find_or_create_user(chat, message)

    cancel_all_jobs_for_user(context, user_data.id)
    ContextManager.clear_list(context.user_data, REMINDER_LIST)

    answer = "🧹Все напоминания удалены"

    await message.reply_text(answer)
    await log_answer(answer, message)
