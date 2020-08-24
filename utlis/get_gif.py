from typing import Optional

from aiogram.types import Message


def get_gif(message: Message) -> Optional[str]:
    if r := message.reply_to_message:
        if gif := r.animation:
            return gif.file_id
    return None
