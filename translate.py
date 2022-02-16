from cgitb import text
import requests

text = ''''''

r = requests.post("http://localhost:5000/translate", json={
    'q': text,
    'source': "fr",
    'target': "en"
})

print(r.text)
