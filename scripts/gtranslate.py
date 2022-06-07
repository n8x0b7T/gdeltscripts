import time
from googletrans import Translator

translator = Translator()

translated_text = []
grams = ['Hello my name is Zac.', 'Google translate is easy to use.']

for g in grams:
    time.sleep(10)
    translated_text.append(translator.translate(g, dest='es'))
    
for t in translated_text:
    print('English: ', t.origin, '  ----->  ', 'Spanish: ', t.text)
