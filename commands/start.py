from telegram.ext import ContextTypes
from telegram import Update

from crud.find_or_create_user import find_or_create_user
from keyboards.add_creds import get_keyboard
from texts.hello import HELLO
from utils.log_answer import log_answer


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    await find_or_create_user(chat, message)

    text = HELLO

    await message.reply_text(text, reply_markup=get_keyboard(), parse_mode="HTML")
    await log_answer(text, message)
