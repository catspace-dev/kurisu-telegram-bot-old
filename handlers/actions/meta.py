from aiogram.types import Message

from models.action import Action


def prepare_reply(sender, recipient, action: Action):
    text = action.text.format(active=sender, passive=recipient)
    print(text)
    formatted = f'<i>{text}</i>'
    print(formatted)
    return formatted


async def meta_action(msg: Message):
    command = msg.get_command().replace('/', '')
    sender = msg.from_user.full_name
    id_ = msg.chat.id
    if not await Action.exists(chat_id=id_, command=command):
        return
    recipient = None
    if msg.reply_to_message:
        recipient = msg.reply_to_message.from_user.full_name
    else:
        message_list = msg.text.split(' ', 1)
        if len(message_list) < 2:
            return await msg.answer(
               "Если ты не реплаишь сообщение, будь добр, укажи цель текстом.")
        else:
            recipient = message_list[1]

    if action := await Action.get(chat_id=id_,
                                  command=command):
        response = prepare_reply(sender, recipient, action)
        await msg.answer(response, parse_mode='HTML')
