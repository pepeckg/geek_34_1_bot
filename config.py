from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config

TOKEN = config("TOKEN")
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
GROUP_ID = [-1001928876008, ]
DESTINATION = 'C:/Users/User/pythonProject/geek_34_1_bot/media'
