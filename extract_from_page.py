import requests
from bs4 import BeautifulSoup

url = 'https://www.itespresso.fr/press-release/sectigo-annonce-lvnement-exclusif-du-secteur-de-la-cyberscurit-le-sommet-identity-first-security-2022-de-sectigo'

req_headers = {'User-Agent': 'Mozilla/5.0'}


def parse_site(url):
    r = requests.get(url, headers=req_headers).text

    soup = BeautifulSoup(r, 'html.parser')
    text = soup.find_all(text=True)

    x= {
        'title': soup.find('title'),
        'body': ''
    }

    for i in text:
        if i.parent.name == 'p':
            x.body += f'{i} '

    return x

print(parse_site(url))