from typing import Optional

from aiogram.types import Message

from models.chats import Chats
from models.action import ActionCommand


async def get_chat(chat_id) -> Chats:
    chat = await Chats.get_or_create(id=chat_id)
    return chat[0]


def get_gif(message: Message) -> Optional[str]:
    if r := message.reply_to_message:
        if gif := r.animation:
            return gif.file_id
    return None


async def get_command(chat_id, command: str) -> Optional[ActionCommand]:
    chat = await get_chat(chat_id)
    action = await ActionCommand.get_or_none(chat_id=chat, command=command)
    return action
