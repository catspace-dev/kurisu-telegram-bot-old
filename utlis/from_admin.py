from aiogram.types import Message


async def from_admin(msg: Message):
    if msg.chat.type == 'private':
        return True
    admins = map(lambda x: x.user, await msg.chat.get_administrators())
    if msg.from_user in admins:
        return True
    else:
        msg.reply("вы должны быть администратором в чате")
        return False
