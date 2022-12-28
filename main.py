from aiogram import Bot, Dispatcher, executor, types
from bot_initializate import dp, bot
from handlers import client, admin, others
from data_base import sqlite_db

#Connect to database
async def on_startup(_):
    print('Bot started')
    sqlite_db.sql_start()

admin.register_handler_admin(dp)
client.register_handler_client(dp)
others.register_handlers_others(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup) #remove the mess queue

#launches bot
if __name__ == '__main__':
    on_startup()
