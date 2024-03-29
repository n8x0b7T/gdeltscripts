#!/usr/bin/env python3

import re
from newspaper import Article
from newspaper import Config
import pandas as pd
import argparse
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed


req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

config = Config()
config.headers = req_headers
config.request_timeout = 5


parser = argparse.ArgumentParser()
parser.add_argument('-o', help='select output file')
parser.add_argument('-i', help='select input file', required=True)
parser.add_argument('-t', help='thread count', default=10)
parser.add_argument('-min-len', default=75, help='select input file')
args = parser.parse_args()


def make_safe(x):
    text = x.replace('\n', '').replace('\t', '')
    return (re.sub(r'[^\w\-\. ]', '', x))


def parse_site(row):
    url = row['SOURCEURL']
    article = Article(url, config=config)
    try:
        article.download()
        article.parse()
        body = make_safe(article.text)
        title = make_safe(article.title)
        if len(body) > args.min_len:
            row['body'] = body
            row['title'] = title
            return pd.DataFrame.from_dict(row, orient='index').T
    except KeyboardInterrupt:
        exit()
    except:
        pass
    return None


if __name__ == "__main__":
    df = pd.read_csv(args.i)
    df = df.drop_duplicates(subset=['SOURCEURL'], keep='first')

    dfs = []
    with alive_bar(len(df), dual_line=True, title="Extracting Text") as bar:
        with ThreadPoolExecutor(max_workers=int(args.t)) as pool:
            futures = [pool.submit(parse_site, work)
                       for work in df.to_dict('records')]
            for result in as_completed(futures):
                dfs.append(result.result())
                bar()
    dfs = [i for i in dfs if i is not None]
    out = pd.concat(dfs)

    print(out)
    if args.o is not None:
        out.to_csv(args.o, index=False)
    else:
        out.to_csv(input("Save file to: "), index=False)
    print(f"Wrote {len(out)} entries.")
