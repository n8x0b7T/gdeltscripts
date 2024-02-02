import pandas as pd

df = pd.read_csv("everything/extracted.csv")

m = df['SOURCEURL'].str.extract('(?<=http://)(.*?)(?=/)|(?<=https://)(.*?)(?=/)')
m = m[0].fillna(m[1]).fillna(df['SOURCEURL'])

df['DOMAINNAME'] = m

df = df.groupby(['DOMAINNAME']).count()

df.to_excel("domains.xlsx")
