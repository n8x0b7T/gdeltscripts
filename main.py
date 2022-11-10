#!/usr/bin/env python3

import os
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
# import modin.pandas as pd
import csv
from io import StringIO
import sys
import argparse
import re
from multiprocessing import Pool
from tqdm import tqdm

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
                    default=".25")
parser.add_argument('-o', help='select output file')
args = parser.parse_args()

last_update_url = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'
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

pbar = tqdm()

# Unzip in memory, and returns a pandas dataframe
def get_df(x):
    return pd.read_csv(x, delimiter='\t', names=csv_headers)


def unzip_csv(zip_file):
    with open(os.path.join(args.archives, zip_file), "rb") as f:
        with ZipFile(BytesIO(f.read())) as f2:
            pbar.update(1)
            return [ i.split('\t') for i in f2.read(f2.filelist[0]).decode('utf-8').split('\n')[:-1]]
            return pd.DataFrame(split)
            return 0
            return get_df(f.open(f.filelist[0]))


def main():
    os.makedirs('./data', exist_ok=True)

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
    num_files_from_years = int(float(args.years) * 8766 * 4)
    zip_archives = zip_archives[:num_files_from_years]

    pbar = tqdm(total=len(zip_archives), bar_format='{l_bar}')

    with Pool(5) as p:
        result = p.map(unzip_csv, zip_archives)
        result = [j for i in result for j in i]

    df = pd.DataFrame(result, columns=csv_headers)

    # for idx, val in enumerate(zip_archives):
    #     print(f'Processing {idx+1}/{zip_archives_len} archives', end='\r')
    #     with open(os.path.join(args.archives, val), "rb") as f:
    #         df = pd.concat([df, unzip_csv(f)], ignore_index=True)
    #         f.close()


    # filter by country
    df = df[df['ActionGeo_CountryCode'] == country_code]

    # print(len(df), 'fasdf')

    # filter by event code
    # selected_event_codes = [7, 13, 14, 19, 20]
    df = df[df['EventRootCode'] == 14]

    if args.number != 0:
        df = df.sample(abs(int(args.number)))

    write_columns = ['GLOBALEVENTID', 'SQLDATE', 'GoldsteinScale', 'SOURCEURL']
    if args.o is not None:
        df[write_columns].to_csv(args.o)
    else:
        df[write_columns].to_csv(input("Save the file to: "))
    #TODO: format date
    print(
        f"Got {len(df)} items from {zip_archives[0].split('.')[0]} to {zip_archives[-1].split('.')[0]}"
    )


if __name__ == '__main__':
    main()
