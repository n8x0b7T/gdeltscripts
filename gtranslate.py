import time
import csv
from googletrans import Translator

translator = Translator()

translated_text = []
grams = ['Hello my name is Zac.', 'Google translate is easy to use.']

f = csv.reader(open('./extracted_text.csv'), delimiter='\t')

for g in f:
    time.sleep(3)
    # print(len(g[3]))
    # translated_text.append(translator.translate("hola", dest='en', src='es'))
    print("\n\n\n\n\n", translator.translate(g[3], dest='en').text)

for t in translated_text:
    print('English: ', t.origin, '  ----->  ', 'Spanish: ', t.text)
