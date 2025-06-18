from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils.to_callback_data_format import to_callback_data_format


def get_keyboard(obj, pageable):

    args = ["page", obj, pageable["limit"]]

    keyboard_line = []
    if pageable["prev_page"]:
        callback_data = to_callback_data_format(*args, pageable["prev_page"])
        keyboard_line.append(
            InlineKeyboardButton("< Назад", callback_data=callback_data)
        )
    if pageable["next_page"]:
        callback_data = to_callback_data_format(*args, pageable["next_page"])
        keyboard_line.append(
            InlineKeyboardButton("Далее >", callback_data=callback_data)
        )

    keyboard = [keyboard_line]
    return InlineKeyboardMarkup(keyboard)
