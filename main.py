#!/usr/bin/env python3

from ast import parse
from operator import le
import os
import time
from traceback import print_tb
from typing import final
import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import datetime
import sys
import argparse
import re
from itertools import groupby
import csv
import random

parser = argparse.ArgumentParser()
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
    '--max-number', help='specify max number of entries to get', default=500)
parser.add_argument('--per-day', help='specify the number to get per day')
parser.add_argument('--per-month', help='specify the number to get per month')
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


def get_df(x):
    return pd.read_csv(x, delimiter='\t', names=csv_headers)


def unzip_csv(zip_file):
    with ZipFile(BytesIO(zip_file)) as f:
        df = get_df(f.open(f.filelist[0]))
        return(df)

# Gets the zip url from GDELTv2


def get_zip_url():
    r = requests.get(last_update_url,
                     headers=req_headers)
    zip_url = r.text.split('/n')[0].split(' ')[2].split('\n')[0]
    return(zip_url)


number_written = 0

# Uses to pandas to filter by country code


def filter_csv(df, file_name='.tempfile.csv'):
    if args.realtime:
        file_name = f'./data/{country_code}_{str(datetime.date.today()).replace("-", "_")}.csv'
    df = df[df['ActionGeo_CountryCode'] == country_code]

    # number_written += int(df.shape[0])
    # df['SQLDATE'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d')
    # print(df)

    df.to_csv(
        file_name, mode='a', header=False, index=False, sep='\t')


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
        if args.start_date is not None:
            try:
                for idx, val in enumerate(zip_archives):
                    if len(re.findall(args.start_date + r'*', val)) == 1:
                        zip_archives = zip_archives[idx:]
                        break
            except:
                print("Date not found")
                exit()

        tempfile_name = '.tempfile.csv'
        for i in zip_archives:
            with open(f"{args.analyze}{i}", "rb") as f:
                df = unzip_csv(f.read())
                filter_csv(df, tempfile_name)

        entries = csv.reader(open(tempfile_name, 'r'), delimiter='\t')

        groups = []

        # How many to get per month or day
        if args.per_day is not None:
            number_to_select = int(args.per_day)
            # group by day
            def group_function(x): return x[1]
            groups = groupby(
                sorted(entries, key=group_function), group_function)
            args.per_month = None

        elif args.per_month is not None:
            number_to_select = int(args.per_month)
            # group by month
            def group_function(x): return x[1][:-2]
            groups = groupby(
                sorted(entries, key=group_function), group_function)
        else:
            number_to_select = 1
            def group_function(x): return x[1][:-2]
            groups = groupby(
                sorted(entries, key=group_function), group_function)

        final_selection = []
        for i in groups:
            if len(final_selection) > abs(int(args.max_number)):
                break
            the_list = list(i[1])
            # print(f'{len(the_list)} <= {number_to_select}')
            if len(the_list) <= number_to_select:
                final_selection += the_list
            else:
                final_selection += random.sample(the_list, number_to_select)

        if args.o is not None:
            with open(args.o, "w") as f:
                csv_writer = csv.writer(f, delimiter='\t')
                csv_writer.writerows(final_selection)
        else:
            for i in final_selection:
                print(i + "\n")

        print(
            f'Found {len(final_selection)} entries\nStarting from {final_selection[0][1]}\nEnding on {final_selection[-1][1]}')

        os.remove(tempfile_name)


if __name__ == '__main__':
    main()
