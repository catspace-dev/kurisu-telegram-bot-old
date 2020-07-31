from aiogram import Dispatcher
from .querymc import querymc_cmd
from .pingmc import pingmc_cmd

def setup(dp: Dispatcher):
    dp.register_message_handler(querymc_cmd, commands=['querymc'])
    dp.register_message_handler(pingmc_cmd, commands=['pingmc'])
