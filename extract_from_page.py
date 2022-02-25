import requests
import re
import csv
from newspaper import Article
from newspaper import Config


req_headers = {
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

f = csv.reader(open('./data/data_US_2022-02-25.csv'), delimiter='\t')

def make_safe(x):
    text = x.replace('\n', '')
    return (re.sub(r'[^\w\-\. ]','', x))

def parse_site(url):
    article = Article(url, config=config)
    article.download()
    article.parse()


    x = [make_safe(article.title), make_safe(article.text), url]
    return(x)


with open("extracted_text.csv", 'w') as file:
    for i in f:
        csvwriter = csv.writer(file, delimiter="\t")
        content = parse_site(i[-1])
        print(content)
        csvwriter.writerow(content)
