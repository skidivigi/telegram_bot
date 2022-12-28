from aiogram import Dispatcher, types
from bot_initializate import bot, dp
from keyboard import kb_client
from data_base import sqlite_db
from keyboard import inline_client_kb
from aiogram.dispatcher.filters import Text

#Activate path from HANDLER 'start'
async def start_message(message : types.Message):
    await bot.send_message(message.from_user.id,\
                'Привет\nЯ BOTinok\nВведите слово на русском или английском, чтобы первести!', reply_markup=kb_client)


async def jokes_message(message : types.Message):
    await bot.send_message(message.from_user.id,\
            'Пока не придумал... Но скоро будет!')

#On the button activate path from HANDLER 'test'
async def get_yourself(message: types.Message):
    await message.answer('Узнай судьбу', reply_markup=inline_client_kb.urlkb) #assigns a keyboard value

counter = {} #useless elem, in order to use more different

#Performs functions of callback
@dp.callback_query_handler(Text(startswith='www_'))
async def callback_get_yourself(callback: types.CallbackQuery):
    res = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in counter:
        counter[f'{callback.from_user.id}'] = res
        await callback.answer('Это ты', show_alert=True)
    else:
        await callback.answer('Вы уже знаете кто лох', show_alert=True)
        # await callback.answer('Нажата кнопка')# show_alert=True - нужно подтвердить "ок" #В виде всплывающего окна
        # await callback.message.answer('Нажата кнопка')  # В виде ответа

async def get_table(message: types.Message):
    await sqlite_db.sql_get(message)

#Work piece
# @dp.message_handler(lambda message: 'anything' in message.text):
# async def getanything(message: types.Message):
#     await message.answer('...')

#Respond to chat calls and activate function`s
def register_handler_client(dp : Dispatcher):
    dp.register_message_handler(start_message, commands=['start','help'])
    dp.register_message_handler(jokes_message, commands=['joke'])
    dp.register_message_handler(get_table, commands=['table'])
    dp.register_message_handler(get_yourself, commands=['test'])
    dp.callback_query_handler(callback_get_yourself, commands=['www_1']) #Text(startswith='www_'))