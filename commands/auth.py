import json

from telegram.ext import ContextTypes
from telegram import Update

from commands.parse_args import parse_args
from crud.find_or_create_user import find_or_create_user
from models.ZuzexProfile import ZuzexProfile
from services.zuzex import JiraZuzex
from texts.zuzex import ADD_PROFILE, BAD_CREDS, BAD_TASK, DONE
from utils.animations.with_typing import with_typing
from utils.crypt import Crypt
from utils.log_answer import log_answer


@with_typing
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    user_data, _ = await find_or_create_user(chat, message)

    args = parse_args("/auth", message.text)

    username = args.get("-u")
    password = args.get("-p")
    task_key = args.get("-t")
    pin_code = args.get("-c")

    if not username or not password or not task_key or not pin_code:
        answer = ADD_PROFILE

        await message.reply_text(answer, parse_mode="HTML")
        await log_answer(answer, message, mask=True)
        return

    try:
        headers = JiraZuzex.get_basic_auth_header(username, password)
        zuzex = JiraZuzex(headers=headers)
    except:
        answer = BAD_CREDS
        await message.reply_text(answer, parse_mode="Markdown")
        await log_answer(answer, message, mask=True)
        return

    try:
        zuzex.get_task_id_by_key(task_key)
    except:
        answer = BAD_TASK.format(task_key=task_key)
        await message.reply_text(answer, parse_mode="Markdown")
        await log_answer(answer, message, mask=True)
        return

    salt = Crypt.gen_salt()
    context.user_data["salt"] = salt

    crypt = Crypt(pin_code, salt)
    encrypted_headers = crypt.encrypt(json.dumps(headers))

    exist_profile = await ZuzexProfile.find_one(user_id=user_data.id)
    if exist_profile:
        await ZuzexProfile.delete(id=exist_profile.id)

    await ZuzexProfile.create(
        hashed_auth_key=encrypted_headers, task_key=task_key, user_id=user_data.id
    )
    answer = DONE

    await message.reply_text(answer, parse_mode="Markdown")
    await log_answer(answer, message, mask=True)
