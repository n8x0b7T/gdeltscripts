#!/usr/bin/env python3

import argparse
import requests
import os
import zipfile
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed

parser = argparse.ArgumentParser()
parser.add_argument('-u',
                    '--update',
                    help='update the database',
                    action='store_true')
parser.add_argument('-o',
                    help='choose a folder to store data',
                    action='store_true',
                    default="./archives/")
args = parser.parse_args()

master_list = 'http://data.gdeltproject.org/gdeltv2/masterfilelist-translation.txt'
local_database = 'master_file_list.txt'


os.makedirs(args.o, exist_ok=True)


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

def dl_archive(val):
    if not os.path.isfile(args.o + val.split('/')[-1]) and not os.path.isfile(args.o + val.split('/')[-1].replace('.zip', '')):
                get_csv(val)


def download_archives():
    urls = []
    with open(local_database, 'r') as f:
        for i in f.readlines():
            url = splitv2(i)
            if 'export' in url:
                urls.append(url)
    with alive_bar(len(urls), dual_line=True, title="Downloading CSVs") as bar:
        with ThreadPoolExecutor(max_workers=20) as pool:
            futures = [pool.submit(get_csv, work) for work in urls]
            for result in as_completed(futures):
                bar()

def unzip_file(file):
    with zipfile.ZipFile(os.path.join(args.o, file), "r") as f:
        f.extractall(args.o)
    os.remove(os.path.join(args.o, file))


def unzip_archives():
    zipped_files = [i for i in os.listdir(args.o) if i.split('.')[-1] == 'zip']
    with alive_bar(len(zipped_files), dual_line=True, title="Unzipping CSVs") as bar:
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = [pool.submit(unzip_file, work) for work in zipped_files]
            for result in as_completed(futures):
                bar()


if os.path.exists(local_database):
    download_archives()
    unzip_archives()
else:
    download_file(master_list)
    download_archives()
    unzip_archives()
