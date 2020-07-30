from aiogram.types import Message
from models.action import Action


async def router(message: Message):
    msg = message.parse_entities().split()
    if len(msg) < 2:
        await message.answer("пожалуйста укажите одну из подкоманд:\n"
                             "add [name] [text] - добавление\n"
                             "del [name] - удаление\n"
                             "list - список команд\n")
        return
    _, command, *_ = msg
    if command == 'add':
        await add_action(message)
    elif command == 'del':
        await delete_action(message)
    elif command == 'list':
        await list_actions(message)


async def add_action(message: Message):
    message_splitted = message.parse_entities().split(' ', 3)
    if len(message_splitted) < 4:
        return await message.answer('нужно написать название действия и текст.\
                                    "{active}" и "{passive}" в тексте\
                                    будут заменены на\
                                    воздействующего и \
                                    воздействуемого соответственно')
    command, text = message_splitted[2], message_splitted[3]
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
    if text:
        await message.answer(f"Список ролевых команд в этом диалоге:\n{text}")
    else:
        await message.answer("В этом диалоге нет ролевых команд.")


async def delete_action(message: Message):
    message_splitted = message.parse_entities().split(' ', 1)
    if len(message_splitted) < 2:
        return await message.answer('не знаю что удалять')
    # мне не нравится два запроса но пусть будет пока так
    if await Action.exists(chat_id=message.chat.id,
                           command=message_splitted[1]):
        await Action.get(chat_id=message.chat.id,
                         command=message_splitted[1]).delete()

