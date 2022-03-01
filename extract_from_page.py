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

f = csv.reader(open('./data/US_2022_03_01.csv'), delimiter='\t')


def de_duplicate_url(x):
    res = []
    urls = []
    for i in x:
        if i[-1] not in urls:
            res.append(i)
            urls.append(i[-1])
    return(res)

f = de_duplicate_url(f)

def make_safe(x):
    text = x.replace('\n', '')
    return (re.sub(r'[^\w\-\. ]', '', x))


def parse_site(x):
    url = x[-1]
    article = Article(url, config=config)
    try:
        article.download()
        article.parse()

        return [x[37], make_safe(article.title), make_safe(article.text), url]
    except:
        return False

with open("extracted_text.csv", 'w') as file:
    csvwriter = csv.writer(file, delimiter="\t")
    for i in f:
        content = parse_site(i)
        if content != False:
            print(i[-1])
            print(content)
            csvwriter.writerow(content)
