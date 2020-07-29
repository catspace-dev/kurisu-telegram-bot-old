from aiogram import Dispatcher
from .me import me_cmd
from .meta import meta_action
from .manage import add_action, list_actions


def setup(dp: Dispatcher):
    dp.register_message_handler(me_cmd, commands=['me'])
    dp.register_message_handler(add_action, commands=['add_action'])
    dp.register_message_handler(list_actions, commands=['list_actions'])
    dp.register_message_handler(meta_action)
