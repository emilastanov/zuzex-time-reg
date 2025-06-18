from services.tg.context import ContextManager
from texts.reminder import REMINDER_LIST
from utils.log_answer import sys_log
from utils.reminder.set_reminder import set_reminder
from types import SimpleNamespace


def build_user_context(application, user_id):
    return SimpleNamespace(
        application=application,
        job_queue=application.job_queue,
        user_data=application.user_data[user_id],
    )


async def restore_all_reminders(application):
    for user_id, user_data in application.persistence.user_data.items():
        reminders = ContextManager.get_or_create_list(user_data, REMINDER_LIST)
        for reminder in reminders:
            await sys_log("Обнаружилась джоба в контексте:", reminder["job_name"])

            fake_context = build_user_context(application, user_id)
            set_reminder(
                hour=reminder["hour"],
                minute=reminder["minute"],
                repeat=reminder["repeat"],
                context=fake_context,
                chat_id=reminder["chat_id"],
                data=reminder["data"],
            )
