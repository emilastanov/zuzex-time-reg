from telegram.ext import ContextTypes
from telegram import Update

from crud.find_or_create_user import find_or_create_user
from texts.hello import USER_INFO, GROUP_INFO, TECH_HELLO, TECH_GROUP_HELLO
from models.User import UserType
from utils.log_answer import log_answer


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    user_data, is_new = await find_or_create_user(chat, message)

    text = ""

    if UserType(chat.type) == UserType.private:
        user = update.effective_user

        if is_new:
            text = TECH_HELLO

        text += USER_INFO.format(
            user_id=user.id, chat_id=chat.id, username=user.username
        )

    else:
        thread_id_info = "Not applicable"
        if message.message_thread_id:
            thread_id_info = message.message_thread_id

        if is_new:
            text = TECH_GROUP_HELLO

        text += GROUP_INFO.format(
            chat_title=chat.title,
            chat_id=chat.id,
            chat_type=chat.type,
            thread_id_info=thread_id_info,
        )

    await message.reply_html(text)
    await log_answer(text, message)
