import requests
import csv
# from bs4 import BeautifulSoup
from newspaper import Article
from newspaper import Config



req_headers = headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
}

config = Config()
config.headers = req_headers
config.request_timeout = 10

f = csv.reader(open('data.csv'), delimiter='\t')

urls = []
for i in f:
    urls.append(i[-1])

def parse_site(url):

    
    article = Article(url, config=config)
    article.download()
    article.parse()

    x = {
        'url': url,
        'title': article.title,
        'body': article.text
    }
    return(x)


page_texts = []

for i in urls:
    print(parse_site(i))
    # page_texts.append(parse_site(i))
