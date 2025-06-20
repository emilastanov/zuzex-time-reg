import json

from telegram.ext import ContextTypes
from telegram import Update

from commands.parse_args import parse_args
from crud.find_or_create_user import find_or_create_user
from models.ZuzexProfile import ZuzexProfile
from services.zuzex import JiraZuzex
from texts.zuzex import LOG, BAD_PIN, LOG_EXISTS, LOG_CREATED
from utils.crypt import Crypt
from utils.log_answer import log_answer


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    user_data, _ = await find_or_create_user(chat, message)

    zuzex_profile = await ZuzexProfile.find_one(user_id=user_data.id)

    args = parse_args("/log", message.text)
    pin_code = args.get("-c")

    salt = context.user_data.get("salt")

    if not pin_code or not zuzex_profile or not salt:
        answer = LOG

        await message.reply_text(answer, "HTML")
        await log_answer(answer, message)
        return

    try:
        crypt = Crypt(pin_code, salt)
        headers = json.loads(crypt.decrypt(zuzex_profile.hashed_auth_key))
    except:
        answer = BAD_PIN

        await message.reply_text(answer, "HTML")
        await log_answer(answer, message)
        return

    try:
        jira = JiraZuzex(headers, task_key=zuzex_profile.task_key)
        jira.check_credentials()
        jira.log_full_day()

        answer = LOG_CREATED
    except Exception:
        answer = LOG_EXISTS

    await message.reply_text(answer, "HTML")
    await log_answer(answer, message, mask=True)
    return
