import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.dates import DateFormatter


path = "C:\\Users\\pierre\\Downloads\\files\\Download\\samsunghealth_pierre.major_202008021218\\com.samsung.shealth.tracker.heart_rate.202008021218.csv"

df = pd.read_csv(path, skiprows=1,index_col=False)
df.columns = df.columns.str.replace('com.samsung.health.heart_rate.','')  # strip suffix at the left end only.
df=df.drop(columns = ["tag_id","source","comment","datauuid","pkg_name"])



df["datetime"]=pd.to_datetime(df["create_time"]/1000, unit = 's')
df["end_time"]=pd.to_datetime(df["end_time"]/1000, unit = 's')
print(df.info())
print(df.head())
# print(df["diff"].describe())
fig, ax = plt.subplots()
df.plot.scatter(x="datetime",y="heart_rate")
date_form = DateFormatter("%y-%m-%d")
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.show()
