from random import randint
from telegram.ext import ContextTypes
from telegram import Update

from commands.parse_args import parse_args
from crud.find_or_create_user import find_or_create_user
from texts.reminder import ADD_REMINDER

from texts.reminder import SUCCESS, ERROR, REMINDER_TEXTS
from utils.log_answer import log_answer
from utils.reminder.set_reminder import set_reminder


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    user_data, _ = await find_or_create_user(chat, message)

    args = parse_args("/reminder", message.text)
    repeat = args.get("-r", False)
    time = args.get("-t")

    invalid_format = not time or len(time.split(":")) != 2
    invalid_values = False

    if not invalid_format:
        try:
            hour, minute = map(int, time.split(":"))
            invalid_values = hour < 0 or hour > 23 or minute < 0 or minute > 59
        except ValueError:
            invalid_values = True

    if invalid_format or invalid_values:
        answer = ADD_REMINDER
        await message.reply_text(answer, parse_mode="HTML")
        await log_answer(answer, message)
        return

    rand_index = randint(0, len(REMINDER_TEXTS) - 1)
    success = set_reminder(
        hour=hour,
        minute=minute,
        repeat=repeat,
        context=context,
        chat_id=update.effective_chat.id,
        data=REMINDER_TEXTS[rand_index]
        + "\nИспользуй - /log\n\n Чтобы отменить напоминания - /clear",
    )

    answer = SUCCESS if success else ERROR

    await message.reply_text(answer)
    await log_answer(answer, message)
