from aiogram import Dispatcher, types
import string, json, transletor_module

#Checks for obscene and translate
async def translate_message(message : types.Message):
    if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json', encoding='utf-8')))) != set():
        await message.reply('Аяйяй')
        await message.delete()

    else:
        await message.reply(transletor_module.choseLanguage(message.text))

def register_handlers_others(dp :Dispatcher):
    dp.register_message_handler(translate_message)