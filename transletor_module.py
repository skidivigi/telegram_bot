from translate import Translator

#variables from translate
any_word_ru = Translator(from_lang='ru', to_lang='en')
any_word_en = Translator(from_lang='en', to_lang='ru')

#translate
def choseLanguage(string):
    for c in string[0].lower():
        if c in 'йцукенгшщзхъфываппролджэячсмитьбю': #if the first word is Russian and then English,
            result_ru = any_word_ru.translate(string)   # then it will translate everything into Russian.
            return result_ru
        elif c in 'qwertyuiopasdfghjklzxcvbnm': #backward
            result_en = any_word_en.translate(string)
            return result_en
        else:
            result_error = 'Введите слово/предложение на русском или английском!'
            return result_error