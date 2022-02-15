import requests
import csv
from bs4 import BeautifulSoup

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
}

f = csv.reader(open("a.csv"), delimiter='\t')

urls = []
for i in f:
    urls.append(i[-1])

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
