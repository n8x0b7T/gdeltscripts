#!/usr/bin/env python3

from operator import le
import os
import time
from traceback import print_tb
import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import datetime
import sys
import argparse
import re

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--country', help='two letter country code', default='IZ')
parser.add_argument(
    '--realtime', help='listen in real time for update', action='store_true')
parser.add_argument(
    '--analyze', help='provide a folder of gdelt translated v2 zip files')
parser.add_argument('-n', '--number',
                    help='the number of entries in the output')
parser.add_argument('-d', '--start-date',
                    help='date to at which to start ex. 20150224081500')
parser.add_argument(
    '-o', help='select output file')
args = parser.parse_args()


last_update_url = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'
last_update_url = 'http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt'

req_headers = {'User-Agent': 'Mozilla/5.0'}

csv_headers = ['GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate', 'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode', 'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code', 'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', 'Actor2Code', 'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode', 'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code', 'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code', 'IsRootEvent', 'EventCode', 'EventBaseCode', 'EventRootCode', 'QuadClass', 'GoldsteinScale', 'NumMentions',
               'NumSources', 'NumArticles', 'AvgTone', 'Actor1Geo_Type', 'Actor1Geo_FullName', 'Actor1Geo_CountryCode', 'Actor1Geo_ADM1Code', 'Actor1Geo_ADM2Code', 'Actor1Geo_Lat', 'Actor1Geo_Long', 'Actor1Geo_FeatureID', 'Actor2Geo_Type', 'Actor2Geo_FullName', 'Actor2Geo_CountryCode', 'Actor2Geo_ADM1Code', 'Actor2Geo_ADM2Code', 'Actor2Geo_Lat', 'Actor2Geo_Long', 'Actor2Geo_FeatureID', 'ActionGeo_Type', 'ActionGeo_FullName', 'ActionGeo_CountryCode', 'ActionGeo_ADM1Code', 'ActionGeo_ADM2Code', 'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID', 'DATEADDED', 'SOURCEURL']

country_code = args.country.upper()

# Unzips in memory, and returns a pandas dataframe


def unzip_csv(zip_file):
    with ZipFile(BytesIO(zip_file)) as f:
        df = pd.read_csv(
            f.open(f.filelist[0]), delimiter='\t', names=csv_headers)
        return(df)

# Gets the zip url from GDELTv2


def get_zip_url():
    r = requests.get(last_update_url,
                     headers=req_headers)
    zip_url = r.text.split('/n')[0].split(' ')[2].split('\n')[0]
    return(zip_url)

number_written = 0

# Uses to pandas to filter by country code
def filter_csv(df, file_name=f'./data/{country_code}_{str(datetime.date.today()).replace("-", "_")}.csv'):
    date_string = str(datetime.date.today()).replace('-', '_')
    df = df[df['ActionGeo_CountryCode'] == country_code]
    # number_written += int(df.shape[0])
    df['SQLDATE'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d')
    print(df)
    # df.to_csv(
    #     file_name, mode='a', header=False, index=False, sep='\t')

def main():
    os.makedirs('./data', exist_ok=True)

    if len(sys.argv) == 1:
        parser.print_help()

    if args.realtime:
        last_zip_url = ''
        while True:
            zip_url = get_zip_url()
            if zip_url != last_zip_url:
                print(
                    f'[{str(datetime.datetime.now()).split(".")[0:-1][0]}] Fetching new data from url:')
                print(zip_url)

                r = requests.get(zip_url, headers=req_headers)
                df = unzip_csv(r.content)
                filter_csv(df)
                last_zip_url = zip_url
            else:
                print(
                    f'[{str(datetime.datetime.now()).split(".")[0:-1][0]}] No new data, trying again soon...')
            time.sleep(5*60)
    elif args.analyze:
        zip_archives = sorted(os.listdir(args.analyze))

        try:
            for idx, val in enumerate(zip_archives):
                if len(re.findall(args.start_date + r'*', val)) == 1:
                    zip_archives =zip_archives[idx:]
                    break
        except:
            print("Date not found")
            exit()

        for i in zip_archives:
            with open(f"{args.analyze}{i}", "rb") as f:
                df = unzip_csv(f.read())
                filter_csv(df, args.o)


if __name__ == '__main__':
    main()
