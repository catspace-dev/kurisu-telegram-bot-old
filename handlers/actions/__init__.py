from aiogram import Dispatcher
from .me import me_cmd
from .meta import meta_action


def setup(dp: Dispatcher):
    dp.register_message_handler(me_cmd, commands=['me'])
    dp.register_message_handler(meta_action, commands=['pat', 'like', 'dislike', 'kiss'])
