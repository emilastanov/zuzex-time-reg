import os
import re
from telegram.ext import ContextTypes
from datetime import datetime
from telegram import Update

from commands.parse_args import parse_args
from config import BASE_DIR
from crud.find_or_create_user import find_or_create_user

LOGS_DIR = os.path.join(BASE_DIR, "log")


def is_valid_date_format(date_str):
    return bool(re.fullmatch(r"\d{2}_\d{2}_\d{4}", date_str))


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    user_data, _ = await find_or_create_user(chat, message)

    if not user_data.is_admin:
        await message.reply_text("Недостаточно прав")
        return

    args = parse_args("/log", message.text)
    date_str = args.get("-d") or datetime.now().strftime("%d_%m_%Y")

    if not is_valid_date_format(date_str):
        await message.reply_text("Неверный формат даты. Используйте dd_mm_yyyy.")
        return

    log_path = os.path.join(LOGS_DIR, f"{date_str}.txt")

    if os.path.exists(log_path):
        with open(log_path, "rb") as f:
            await message.reply_document(document=f, filename=f"{date_str}.txt")
    else:
        await message.reply_text(f"Файл {date_str}.txt не найден.")
