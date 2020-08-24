from models.chats import Chats


async def get_chat(chat_id) -> Chats:
    chat = await Chats.get_or_create(id=chat_id)
    return chat[0]
