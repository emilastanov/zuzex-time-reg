import os
from datetime import datetime
import asyncio


async def log_answer(answer, message):
    """
    Асинхронно сохраняет сообщение и ответ в лог-файл по дате (не блокирует event loop).
    """

    def write_log():
        log_dir = "log"
        os.makedirs(log_dir, exist_ok=True)

        date_str = datetime.now().strftime("%d_%m_%Y")
        file_path = os.path.join(log_dir, f"{date_str}.txt")

        user = message.from_user
        chat = message.chat
        timestamp = message.date.strftime("%Y-%m-%d %H:%M:%S")

        log_entry = (
            f"---\n"
            f"Time: {timestamp}\n"
            f"Chat ID: {chat.id}\n"
            f"User ID: {user.id}\n"
            f"Name: {user.full_name}\n"
            f"Username: @{user.username if user.username else 'N/A'}\n"
            f"Message: {message.text or '[non-text content]'}\n"
            f"Answer:\n{answer}\n"
        )

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(log_entry)

    await asyncio.to_thread(write_log)


async def sys_log(text):
    await asyncio.to_thread(sync_sys_log, text)


def sync_sys_log(*texts):
    text = " ".join(texts)
    print(text)

    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)

    date_str = datetime.now().strftime("%d_%m_%Y")
    file_path = os.path.join(log_dir, f"{date_str}.txt")

    timestamp = datetime.now()

    log_entry = f"---\n" f"Time: {timestamp}\n" f"Text:\n{text}\n"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(log_entry)
