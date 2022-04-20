#!/usr/bin/env python3

import argparse
import requests
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    '-u', '--update', help='update the database',  action='store_true')    
parser.add_argument(
    '-o', '--ouptut', help='update the database',  action='store_true', default="./archives/")
args = parser.parse_args()

master_list = 'http://data.gdeltproject.org/gdeltv2/masterfilelist-translation.txt'
local_database = 'master_file_list.txt'

os.makedirs('./archives', exist_ok=True)


def download_file(url):
    print('Updating local database')
    r = requests.get(url, stream=True)
    with open(local_database, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()


if args.update:
    download_file(master_list)


def get_csv(url):
    r = requests.get(url)
    with open(args.o + url.split('/')[-1], 'wb') as f:
        f.write(r.content)

def splitv2(x):
    return x.split(' ')[-1].replace('\n', '')

def splitv1(x):
    return ""

def download_archives():
    urls = []
    with open(local_database, 'r') as f:
        for i in f.readlines():
            url = splitv2(i)
            if 'export' in url:
                urls.append(url)

    for idx, val in enumerate(urls):
        if not os.path.isfile(args.o + val.split('/')[-1]):
            print(f'Downloading {idx+1}/{len(urls)} archives', end='\r')
            get_csv(val)
    print()


if os.path.exists(local_database):
    download_archives()
else:
    download_file(master_list)
    download_archives()
