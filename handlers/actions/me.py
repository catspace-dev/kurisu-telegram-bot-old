from aiogram.types import Message
import string


async def me_cmd(msg: Message):
    await msg.delete()
    print(msg.get_command())
    _, action = msg.parse_entities().split(' ', 1)
    await msg.answer(f"<pre>* "
                     f"{msg.from_user.full_name} "
                     f"{action}"
                     f"</pre>",
                     parse_mode="HTML"
                     )
