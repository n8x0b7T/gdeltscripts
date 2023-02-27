import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import sys


import datetime


if len(sys.argv) != 3:
    print("Usage: python3 label.py model_name csv_location ")


with open(sys.argv[1], 'rb') as file:
    model = pickle.load(file)


df = pd.read_csv(sys.argv[2])

df['predictions'] = model.predict(df["body"].to_list())

df = df[df['predictions'] == 1]
df = df[df['ActionGeo_CountryCode'] != 'IZ']
print(df)


def get_date_obj(s):
    time = datetime.datetime.strptime(str(s)[:-2], "%Y%m")
    return time


df['date'] = df.SQLDATE.apply(get_date_obj)
df = df[df['date'] > '2015']

grouped = df.groupby(['date'])['date'].count()


print(grouped.index[0])
print()

for date, count in zip(grouped.index, grouped.to_numpy()):
    print(date,count)

times = pd.date_range(start=grouped.index[0],
                      end=grouped.index[-1])

print(times)

fig, ax = plt.subplots(1)
fig.autofmt_xdate()
plt.plot(grouped.index, grouped.to_list())
ax.set_ylim([0, 275])

xfmt = mdates.DateFormatter('%Y-%m')
ax.xaxis.set_major_formatter(xfmt)
plt.savefig("thing_not_iz.png")
