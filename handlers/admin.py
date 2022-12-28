from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from bot_initializate import dp, bot
from data_base import sqlite_db
from keyboard import admin_kb, client_kb, inline_admin_kb

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    delete = State()

#Get id user to make sure that he is admin
async def get_started_id(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, '...?', reply_markup=admin_kb.button_case_admin)

#Start of messages
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

#Exit of state`s
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ok')

#Get first reply
async def load_photo(message: types.Message,state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Второй шаг')

#Get second reply
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Третий шаг')

#Get ... reply
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Четвертый шаг')

#Get ... reply
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        # async with state.proxy() as data:
        #     await message.reply(str(data))
        await bot.send_message(message.from_user.id, 'Данные успешно загружены',reply_markup=client_kb.kb_client)
        await sqlite_db.sql_add_command(state)
        await state.finish()

#callback from delete_item_table fuction
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '),  state=FSMAdmin.delete)
async def del_callback_run(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await sqlite_db.sql_delete_command(callback_query.data.replace('del ',''))
        await callback_query.answer(text=f'{callback_query.data.replace("del ","")} удалена!', show_alert=True)
        await state.finish()

#displays a list of objects to delete with button
async def delete_item_table(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read()
        for each in read:
            await bot.send_photo(message.from_user.id, each[0],\
                    f'Наименование:{each[1]}\nОписание: {each[2]}\nЦена: {each[-1]}')
            await bot.send_message(message.from_user.id, text='^^^^^^^^^^^^^^^', reply_markup=inline_admin_kb.admurlkb.\
                                   add(InlineKeyboardButton(f'Удалить {each[1]}', callback_data=f'del {each[1]}')))
            await FSMAdmin.delete.set()

#Registration handler`s
def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(get_started_id, commands=['moderator', 'moderation'])#, is_chat_admin=True)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_item_table, commands=['Удалить'])


