from deep_translator import GoogleTranslator

chosen_language = input("what language do you want to translate to?: ")
translator = GoogleTranslator(source = 'auto', target = chosen_language)
what_you_want_to_translate=input("what do you want to translate?: ")
translator_text = translator.translate(what_you_want_to_translate)
print(translator_text)