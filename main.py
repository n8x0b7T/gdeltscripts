import time
import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
from threading import Timer


last_update_url = 'http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt'
req_headers = {'User-Agent': 'Mozilla/5.0'}

csv_headers = ['GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate', 'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode', 'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code', 'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', 'Actor2Code', 'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode', 'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code', 'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code', 'IsRootEvent', 'EventCode', 'EventBaseCode', 'EventRootCode', 'QuadClass', 'GoldsteinScale', 'NumMentions',
               'NumSources', 'NumArticles', 'AvgTone', 'Actor1Geo_Type', 'Actor1Geo_FullName', 'Actor1Geo_CountryCode', 'Actor1Geo_ADM1Code', 'Actor1Geo_ADM2Code', 'Actor1Geo_Lat', 'Actor1Geo_Long', 'Actor1Geo_FeatureID', 'Actor2Geo_Type', 'Actor2Geo_FullName', 'Actor2Geo_CountryCode', 'Actor2Geo_ADM1Code', 'Actor2Geo_ADM2Code', 'Actor2Geo_Lat', 'Actor2Geo_Long', 'Actor2Geo_FeatureID', 'ActionGeo_Type', 'ActionGeo_FullName', 'ActionGeo_CountryCode', 'ActionGeo_ADM1Code', 'ActionGeo_ADM2Code', 'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID', 'DATEADDED', 'SOURCEURL']

country_code = 'IQ'
country_code = 'US'

# Takes zip link, unzips in memory, and returns a pandas dataframe
def get_csv(zip_url):
    r = requests.get(zip_url, headers=req_headers)
    with ZipFile(BytesIO(r.content)) as f:
        df = pd.read_csv(f.open(f.filelist[0]), delimiter='\t', names=csv_headers)
        return(df)

# Gets the zip url from GDELTv2
def get_zip_url():
    r = requests.get(last_update_url,
                     headers=req_headers)
    zip_url = r.text.split('/n')[0].split(' ')[2].split('\n')[0]
    return(zip_url)


# Uses to pandas to filter by country code
def filter_csv(df):
    df = get_csv(zip_url)
    print(df[df['ActionGeo_CountryCode'] == country_code])


if __name__ == '__main__':
    last_zip_url = ''
    while True:
        zip_url = get_zip_url()
        if zip_url != last_zip_url:
            print(zip_url)
            df = get_csv(zip_url)
            filter_csv(df)
            last_zip_url = zip_url
        else:
            print('its the same')
        time.sleep(5)

# TODO: store data in parsable format
