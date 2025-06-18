from datetime import datetime, timedelta, time
from telegram.ext import ContextTypes

from services.tg.context import ContextManager
from texts.reminder import REMINDER_LIST
from utils.log_answer import sys_log, sync_sys_log
from utils.reminder.send_reminder import send_reminder


def set_reminder(
    *,
    hour: int,
    minute: int,
    repeat: bool,
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    data: str,
):
    try:
        now = datetime.now()
        target = time(hour=hour, minute=minute)

        if repeat:
            # Ежедневное напоминание
            job_name = f"daily_{chat_id}_{target.isoformat()}"
            context.job_queue.run_daily(
                callback=send_reminder,
                time=target,
                chat_id=chat_id,
                name=job_name,
                data=data,
            )
        else:
            # Однократное напоминание
            run_at = datetime.combine(now.date(), target)
            if run_at < now:
                run_at += timedelta(days=1)
            job_name = f"once_{chat_id}_{run_at.isoformat()}"
            context.job_queue.run_once(
                callback=send_reminder,
                when=run_at - now,
                chat_id=chat_id,
                name=f"once_{chat_id}_{run_at.isoformat()}",
                data=data,
            )

        reminder_entry = {
            "hour": hour,
            "minute": minute,
            "repeat": repeat,
            "chat_id": chat_id,
            "data": data,
            "job_name": job_name,
        }

        sync_sys_log("Создалась джоба", job_name)

        if not ContextManager.exists_in_list(
            context.user_data,
            REMINDER_LIST,
            lambda item: item.get("job_name") == job_name,
        ):
            sync_sys_log("Добавилось в контекст", job_name)
            ContextManager.add_to_list(context.user_data, REMINDER_LIST, reminder_entry)

        return True
    except Exception as e:
        # Можно логировать ошибку, если нужно
        return False
