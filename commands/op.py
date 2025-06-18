from telegram import Update
from telegram.ext import ContextTypes

from commands.parse_args import parse_args
from config import ADMIN_PASS_KEY
from crud.find_or_create_user import find_or_create_user
from models.User import User
from utils.log_answer import log_answer


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    user_data, _ = await find_or_create_user(chat, message)

    args = parse_args("/op", message.text)
    password = args.get("-p")

    if user_data.is_admin:
        text = "Вы уже являетесь администратором."
        await message.reply_text(text)
    elif password != ADMIN_PASS_KEY:
        text = "Ошибка аутентификации."
        await message.reply_text(text)
    else:
        await User.update(user_data.id, is_admin=True)
        text = "Теперь вы администратор."
        await message.reply_text(text)

    await log_answer(text, message)
