from aiogram import Bot, Dispatcher
from config_api import api
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#create instances of classes
storage=MemoryStorage()
bot = Bot(token=api)
dp = Dispatcher(bot, storage=storage)