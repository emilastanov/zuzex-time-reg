from telegram import Update
from telegram.ext import ContextTypes

from crud.get_user_list_with_pagination import get_user_list_with_pagination
from keyboards.pagination_keyboard import get_keyboard
from texts.formatters import format_user_list_message


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    pagination_data = query.data.split(":")[-1].split(";")
    obj_name, limit, page_number = pagination_data

    if obj_name == "User":
        users, pagination_data = await get_user_list_with_pagination(limit, page_number)

        answer = format_user_list_message(users, pagination_data)
        await query.edit_message_text(
            text=answer,
            reply_markup=get_keyboard("User", pagination_data),
            parse_mode="HTML",
        )
