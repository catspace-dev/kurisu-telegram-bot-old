from aiogram.types import Message
from configs.actions import actions_dict


def prepare_reply(sender, recipient, action):
    return actions_dict[action]["template"].format(sender=sender, recipient=recipient)


async def meta_action(msg: Message):
    command = msg.get_command()
    sender = msg.from_user.full_name
    recipient = None
    if msg.reply_to_message:
        recipient = msg.reply_to_message.from_user.full_name
    else:
        message_list = msg.parse_entities().split(' ')
        if len(message_list) < 2:
            return await msg.answer("Если ты не реплаишь сообщение, будь добр, укажи цель текстом.")
        else:
            recipient = " ".join(message_list[1:])

    if actions_dict.get(command):
        response = prepare_reply(sender, recipient, command)
        await msg.answer(response)
        await msg.delete()
