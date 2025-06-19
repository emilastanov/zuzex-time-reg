from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    MessageHandler,
    PicklePersistence,
)
from config import TOKEN, TOKEN_DEV, ENV
from core.module_loader import load_module
from exceptions.error_handler import error_handler
from utils.log_answer import sync_sys_log
from utils.reminder.restart_reminders import restore_all_reminders


def get_token():
    if ENV == "production":
        return TOKEN
    elif ENV == "development":
        return TOKEN_DEV or TOKEN
    else:
        raise ValueError(f"Unknown ENV: {ENV}")


def main():
    token = get_token()
    persistence = PicklePersistence(filepath="bot_cache.pkl")
    app = (
        ApplicationBuilder()
        .token(token)
        .persistence(persistence)
        .post_init(restore_all_reminders)
        .build()
    )

    app.add_error_handler(error_handler)

    load_module(app, "commands", CommandHandler, named=True)
    load_module(app, "button_handlers", CallbackQueryHandler, pattern=True)
    load_module(app, "inline_query_handlers", InlineQueryHandler)
    load_module(app, "other_handlers", MessageHandler, filters=True)

    sync_sys_log("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
