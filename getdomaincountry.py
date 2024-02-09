import pandas as pd

df = pd.read_csv("everything/extracted.csv")
# df = df.head(500)

m = df['SOURCEURL'].str.extract(
    '(?<=http://)(.*?)(?=/)|(?<=https://)(.*?)(?=/)')
m = m[0].fillna(m[1]).fillna(df['SOURCEURL'])

df['DOMAINNAME'] = m


# df = df.groupby(['DOMAINNAME'])['ActionGeo_CountryCode'].agg(lambda x: x.mode().iloc[0])

most_common_country_per_domain = df.groupby('DOMAINNAME')['ActionGeo_CountryCode'].agg(
    [('Most_Common_Country', lambda x: x.mode().iloc[0]), ('Count', 'count')])


most_common_country_per_domain.to_excel("countries.xlsx")


df['SQLDATE'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d')


df = df.loc[(df['SQLDATE'] >= '2023-10-07')
            & (df['SQLDATE'] < '2023-12-15')]

domain_to_country = most_common_country_per_domain['Most_Common_Country'].to_dict()
df['Domain_Label'] = df['DOMAINNAME'].map(domain_to_country)

df.to_csv("dataset.csv")
df.to_excel("dataset.xlsx")

