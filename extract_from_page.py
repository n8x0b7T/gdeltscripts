#!/usr/bin/env python3

import re
from newspaper import Article
from newspaper import Config
import pandas as pd
import argparse
from alive_progress import alive_bar
# from concurrent.futures import ThreadPoolExecutor, as_completed


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
config.request_timeout = 5


parser = argparse.ArgumentParser()
parser.add_argument('-o', help='select output file')
parser.add_argument('-i', help='select input file', required=True)
parser.add_argument('-min-len', default=50, help='select input file')
args = parser.parse_args()


def make_safe(x):
    text = x.replace('\n', '').replace('\t', '')
    return (re.sub(r'[^\w\-\. ]', '', x))


def parse_sites(df):
    # set up columns
    columns = df.columns.to_list()
    columns += ['title', 'body']

    df_return = pd.DataFrame(columns=columns)
    df = df.to_dict('records')

    with alive_bar(len(df), dual_line=True, title="Extracting Text") as bar:
        for row in df:
            url = row['SOURCEURL']
            article = Article(url, config=config)
            try:
                article.download()
                article.parse()
                body = make_safe(article.text)
                title = make_safe(article.title)
                # print(body)
                if len(body) > args.min_len:
                    row['body'] = body
                    row['title'] = title
                    df_return = pd.concat(
                        [df_return, pd.DataFrame.from_dict(row, orient='index').T], axis=0)
            except:
                pass
            bar()

    return df_return


if __name__ == "__main__":
    df = pd.read_csv(args.i)
    df = df.drop_duplicates(subset=['SOURCEURL'], keep='first')

    # TODO:multithread?
    # with ThreadPoolExecutor(max_workers=6) as pool:
    #     futures = [pool.submit(unzip_file, work) for work in zipped_files]
    #     for result in as_completed(futures):
    #         print(result)
    #         bar()

    out = parse_sites(df)
    print(out)
    if args.o is not None:
        out.to_csv(args.o)
    else:
        out.to_csv(input("Save file to: "))
    print(f"Wrote {len(out)} entries.")
