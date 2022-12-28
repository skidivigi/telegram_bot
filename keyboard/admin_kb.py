from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#Admin`s panel buttons
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')

#Admin`s ready keyboard
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_delete)