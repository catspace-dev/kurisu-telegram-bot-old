from aiogram import Dispatcher
from .me import me_cmd
from .meta import meta_action
from .manage import router
from utlis import from_admin


def setup(dp: Dispatcher):
    dp.register_message_handler(me_cmd, commands=['me'])
    dp.register_message_handler(router, from_admin, commands=['action'])
    dp.register_message_handler(meta_action, lambda m: m.is_command())
