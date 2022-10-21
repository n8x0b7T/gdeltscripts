from transformers import pipeline

sa = pipeline('text-classification', model='CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment')

text = ""
sentences = ['']

print(sa(text))
