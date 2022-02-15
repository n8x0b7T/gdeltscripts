import requests
import csv
from bs4 import BeautifulSoup

req_headers = {'User-Agent': 'Mozilla/5.0'}

f = csv.reader(open("a.csv"), delimiter='\t')
urls = []

for i in f:
    urls.append(i[-1])

print(urls)

def parse_site(url):
    r = requests.get(url, headers=req_headers).text

    soup = BeautifulSoup(r, 'html.parser')
    text = soup.find_all(text=True)

    x= {
        'title': soup.find_all('title')[0].text,
        'body': ''
    }

    for i in text:
        if i.parent.name == 'p':
            x['body'] += f'{i.text} '

    return x


for i in urls:
    print(parse_site(i))
