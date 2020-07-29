from aiogram import Dispatcher
from .querymc import querymc_cmd


def setup(dp: Dispatcher):
    dp.register_message_handler(querymc_cmd, commands=['querymc'])
