from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils.to_callback_data_format import to_callback_data_format


def get_keyboard(*args):

    _args = ["add_creds", *args]

    keyboard_line = []

    callback_data = to_callback_data_format(*_args)
    keyboard_line.append(
        InlineKeyboardButton("Добавить 📲", callback_data=callback_data)
    )

    keyboard = [keyboard_line]
    return InlineKeyboardMarkup(keyboard)
