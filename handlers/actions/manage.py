from aiogram.types import Message
from models.action import Action


async def add_action(message: Message):
    message_splitted = message.parse_entities().split(' ', 2)
    if len(message_splitted) < 3:
        return await message.answer('нужно написать название действия и текст.\
                                    "{active}" и "{passive}" в тексте\
                                    будут заменены на\
                                    воздействующего и \
                                    воздействуемого соответственно')
    command, text = message_splitted[1], message_splitted[2]
    command = command.replace('/', '')
    action = Action.filter(chat_id=message.chat.id,
                           command=command)
    if await action.count():
        await action.update(text=text)
    else:
        await Action.create(chat_id=message.chat.id,
                            command=command,
                            text=text)
    await message.answer("команда успешно добавлена для данного чата")


async def list_actions(message: Message):
    actions = map(lambda x: x.command,
                  await Action.filter(chat_id=message.chat.id))
    text = '\n'.join(actions)
    if actions:
        await message.answer(f"Список ролевых команд в этом диалоге:\n{text}")
    else:
        await message.answer("В этом диалоге нет ролевых команд.")
    print(actions)
