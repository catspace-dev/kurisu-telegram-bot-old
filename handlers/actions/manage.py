from aiogram.types import Message
from models.action import ActionCommand, ActionTemplate, ActionAttachs
from typing import Optional

from utlis.getters import get_chat, get_gif


async def router(message: Message):
    text = message.text.replace("/action ", "", 1)
    # args can be optional with *
    subcommand, *args = text.split(' ', 1)
    print(args)
    reply = "неверно заданы аргументы"
    if subcommand == "add":
        if args:
            args = args.pop().split(" ", 1)
            if len(args) == 1:
                reply = await add_action(message.chat.id, args.pop(), None)
            else:
                name, text = args
                reply = await add_action(message.chat.id, name, text)
        else:
            reply = "укажите хотя бы имя команды"

    elif subcommand == "del":
        args = args.pop().split()
        if not args:
            reply = "а чо удалять епта"
        elif len(args) == 1:
            reply = await delete_action(message.chat.id, args[0])
        else:
            try:
                index = int(args[1])
                reply = await delete_variant(message.chat.id, args[0], index)
            except ValueError:
                reply = "индекс должен быть числом"

    elif subcommand == "list":
        if args:
            args = args[0]
            reply = await list_variants(message.chat.id, args)
        else:
            reply = await list_actions(message.chat.id)

    elif subcommand == "gif":
        gif = get_gif(message)
        if gif:
            if args:
                reply = await add_gif(message.chat.id, args.pop(), gif)
            else:
                reply = "укажите название команды"
        else:
            reply = "не удалось найти GIF"

    elif subcommand == "cleargif":
        if args:
            reply = await clear_gifs(message.chat.id, args.pop())
        else:
            reply = "укажите название команды"
    await message.reply(reply)


async def add_action(chat_id,
                     name: str,
                     first_variant: Optional[str]) -> str:

    chat = await get_chat(chat_id)
    await ActionCommand.get_or_create(chat_id=chat, command=name)
    if first_variant:
        await add_variant(chat_id, name, first_variant)
        return "действие добавлено"
    else:
        return "действие добавлено, но "\
               "пока не имеет вариантов текста"


async def delete_action(chat_id, name: str) -> str:
    chat = await get_chat(chat_id)
    print(chat_id, name)
    action = await ActionCommand.get_or_none(chat_id=chat, command=name)
    if action:
        await action.delete()
        return "успешно удалено"
    else:
        return "нельзя удалить то, чего нет!"


async def list_actions(chat_id) -> str:
    chat = await get_chat(chat_id)
    commands = await chat.commands
    if commands:
        return "\n".join(map(lambda c: c.command, commands))
    else:
        return "в этом чате нет действий"


# this can be inlined but i'm lazy.
async def add_variant(chat_id, cmd: str, text: str):
    chat = await get_chat(chat_id)
    command = await ActionCommand.get(chat_id=chat, command=cmd)
    await ActionTemplate.create(command=command, text=text)


async def delete_variant(chat_id, command: str, index: int) -> str:
    chat = await get_chat(chat_id)
    command = await ActionCommand.get(chat_id=chat)
    variants = await command.templates
    try:
        await variants[index].delete()
        return "вариант успешно удалён"
    except IndexError:
        return "индекс уменьши, ежжи"


async def list_variants(chat_id, command: str) -> str:
    chat = await get_chat(chat_id)
    action = await ActionCommand.get(chat_id=chat, command=command)
    variants = await action.templates
    return "\n".join(map(lambda t: t.text, variants))


async def add_gif(chat_id, command, file_id) -> str:
    chat = await get_chat(chat_id)
    command = await ActionCommand.get(chat_id=chat, command=command)
    await ActionAttachs.get_or_create(command=command, file_id=file_id)
    return "прикреплено"


async def clear_gifs(chat_id, command) -> str:
    chat = await get_chat(chat_id)
    command = await ActionCommand.get_or_none(chat_id=chat, command=command)
    if command:
        await ActionAttachs.filter(command=command).delete()
        return "очищено"
    else:
        return "не найдена команда"
