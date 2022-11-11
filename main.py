#!/usr/bin/env python3

import os
import sys
import argparse
import re
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
# import modin.pandas as pd
# from modin.config import Engine
# Engine.put("dask")

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
    num_files_from_years = int(float(args.years) * 8766 * 4)
    zip_archives = zip_archives[:num_files_from_years]

    def open_csv(name):
        return pd.read_csv(os.path.join(
            args.archives, name), delimiter='\t', names=csv_headers)

    # with alive_bar(len(zip_archives), dual_line=True, title="Opening CSVs") as bar:
    #     # Read the files into dataframes
    #     df = pd.DataFrame(columns=csv_headers)
    #     # try:
    #     for i in zip_archives:
    #         # print(i)
    #         df = pd.concat([df, ])
    #         bar()

    dfs = []
    with alive_bar(len(zip_archives), dual_line=True, title="Opening CSVs") as bar:
        with ThreadPoolExecutor(max_workers=30) as pool:
            futures = [pool.submit(open_csv, work)
                       for work in zip_archives]
            for result in as_completed(futures):
                dfs.append(result.result())
                bar()
    # dfs = [i for i in dfs if i is not None]

    df = pd.DataFrame(columns=csv_headers)

    df = pd.concat(dfs)

    # with alive_bar(len(dfs), dual_line=True, title="Concatenating CSVs") as bar:
    #     for i in dfs:
    #         df = pd.concat([df, i])
    #         bar()

    # filter by country
    df = df[df['ActionGeo_CountryCode'] == country_code]

    # filter by event code
    df = df[df['EventRootCode'] == 14]

    # remove duplicates
    df = df.drop_duplicates(subset=['SOURCEURL'], keep='first')

    if args.number != 0:
        df = df.sample(abs(int(args.number)))

    write_columns = ['GLOBALEVENTID', 'SQLDATE',
                     'GoldsteinScale', 'EventRootCode', 'ActionGeo_CountryCode', 'SOURCEURL']
    if args.o is not None:
        df[write_columns].to_csv(args.o, index=False)
    else:
        df[write_columns].to_csv(input("Save the file to: "), index=False)
    # TODO: format date
    print(
        f"Got {len(df)} items from {zip_archives[0].split('.')[0]} to {zip_archives[-1].split('.')[0]}"
    )


if __name__ == '__main__':
    main()
