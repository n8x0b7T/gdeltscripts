#!/usr/bin/env python3

import os
import sys
import argparse
import re
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--country', help='two letter country code', default='IZ')
parser.add_argument('--archives',
                    help='folder where archives are located',
                    default='./archives')
parser.add_argument('-n',
                    '--number',
                    help='the number of entries in the output',
                    default=0)
parser.add_argument('-d',
                    '--start-date',
                    help='date to at which to start ex. 20150224081500')
parser.add_argument('--years',
                    help='how many years of gdelt archive files',
                    default=0)
parser.add_argument('-o', help='select output file')
args = parser.parse_args()

# last_update_url = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'
last_update_url = 'http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt'

req_headers = {'User-Agent': 'Mozilla/5.0'}


csv_headers = [
    'GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate',
    'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode',
    'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code',
    'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', 'Actor2Code',
    'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode',
    'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code',
    'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code', 'IsRootEvent',
    'EventCode', 'EventBaseCode', 'EventRootCode', 'QuadClass',
    'GoldsteinScale', 'NumMentions', 'NumSources', 'NumArticles', 'AvgTone',
    'Actor1Geo_Type', 'Actor1Geo_FullName', 'Actor1Geo_CountryCode',
    'Actor1Geo_ADM1Code', 'Actor1Geo_ADM2Code', 'Actor1Geo_Lat',
    'Actor1Geo_Long', 'Actor1Geo_FeatureID', 'Actor2Geo_Type',
    'Actor2Geo_FullName', 'Actor2Geo_CountryCode', 'Actor2Geo_ADM1Code',
    'Actor2Geo_ADM2Code', 'Actor2Geo_Lat', 'Actor2Geo_Long',
    'Actor2Geo_FeatureID', 'ActionGeo_Type', 'ActionGeo_FullName',
    'ActionGeo_CountryCode', 'ActionGeo_ADM1Code', 'ActionGeo_ADM2Code',
    'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID', 'DATEADDED',
    'SOURCEURL'
]


country_code = args.country.upper()
country_code = ["DZ", "MA", "KM", "TD", "DJ", "IQ", "SO", "BH", "EG",
                "JO", "KW", "LB", "LY", "OM", "QA", "SA", "SD", "TN", "AE", "YE", "PS", "IZ"]

needed_columns = ['GLOBALEVENTID', 'SQLDATE', 'GoldsteinScale', 'EventRootCode',
                  "ActionGeo_Lat", "ActionGeo_Long", 'ActionGeo_CountryCode', 'SOURCEURL']


def main():
    if len(sys.argv) == 1:
        parser.print_help()

    zip_archives = sorted(os.listdir(args.archives))
    if args.start_date is not None:
        try:
            for idx, val in enumerate(zip_archives):
                if re.findall(f'^{args.start_date}.*', val):
                    zip_archives = zip_archives[idx:]
                    break
        except:
            print("Date not found")
            exit()
    if args.years != 0:
        num_files_from_years = int(float(args.years) * 8766 * 4)
        zip_archives = zip_archives[:num_files_from_years]

    def open_csv(name):
        try:
            df = pd.read_csv(os.path.join(args.archives, name),
                             delimiter='\t', names=csv_headers, usecols=needed_columns)
            # filter by country
            df = df[df['ActionGeo_CountryCode'].isin(country_code)]
            # print(df)
            # filter by event code
            # df = df[df['EventRootCode'] == 14]
            return df
        except:
            return None

    dfs = []
    with alive_bar(len(zip_archives), dual_line=True, title="Opening CSVs") as bar:
        with ThreadPoolExecutor(max_workers=16) as pool:
            futures = [pool.submit(open_csv, work)
                       for work in zip_archives]
            for result in as_completed(futures):
                dfs.append(result.result())
                bar()

    print('Concatenating...')
    dfs = [i for i in dfs if i is not None and not i.empty]
    if len(dfs) != 0:
        df = pd.concat(dfs)
    else:
        print("Nothing selected")
        exit()

    # remove duplicates
    df = df.drop_duplicates(subset=['SOURCEURL'], keep='first')

    if args.number != 0:
        df = df.sample(abs(int(args.number)))

    # TODO: format date
    print(
        f"Got {len(df)} items from {zip_archives[0].split('.')[0]} to {zip_archives[-1].split('.')[0]}")

    print(df)

    if args.o is not None:
        df[needed_columns].to_csv(args.o, index=False)
    else:
        df[needed_columns].to_csv(input("Save the file to: "), index=False)


if __name__ == '__main__':
    main()
