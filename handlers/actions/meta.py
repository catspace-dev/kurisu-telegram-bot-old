from random import choice
from typing import Optional

from aiogram.types import Message

from utlis import get_chat
from models.action import ActionCommand


def get_repicient(msg: Message) -> Optional[str]:
    if msg.reply_to_message:
        return msg.reply_to_message.from_user.full_name
    else:
        _, *who = msg.text.split(' ', 1)
        return who.pop() if who else None


def prepare_reply(sender, recipient, template):
    text = template.format(active=sender, passive=recipient)
    formatted = f'<i>{text}</i>'
    return formatted


async def meta_action(msg: Message):
    chat = await get_chat(msg.chat.id)
    command = msg.get_command(pure=True)
    command = await ActionCommand.get_or_none(chat_id=chat, command=command)
    if not command:
        return
    templates = await command.templates
    gifs = await command.attachs
    sender = msg.from_user.full_name
    repicient = get_repicient(msg)
    template = choice(templates).text
    gif = choice(gifs).file_id
    if '{passive}' in template and not repicient:
        await msg.reply('Либо реплай, либо укажи текстом')
        return
    reply = prepare_reply(sender, repicient, template)
    await msg.reply(reply, parse_mode='HTML')
    if gifs:
        await msg.answer_animation(gif)
