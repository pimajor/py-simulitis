import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.dates import DateFormatter

path = "C:\\Users\\pierre\\Downloads\\files\\Download\\samsunghealth_pierre.major_202008021218\\com.samsung.shealth.sleep.202008021218.csv"
df = pd.read_csv(path, index_col=False)
print(df.columns)
# df.columns = df.columns.str.replace('com.samsung.health.heart_rate.','')  

df=df.drop(columns = ["extra_data","original_efficiency","original_bed_time","datauuid","original_wake_up_time","pkg_name","deviceuuid"])


df["datetime"]=pd.to_datetime(df["start_time"]/1000, unit = 's')
df["original_starttime"]=pd.to_datetime(df["start_time"]/1000, unit = 's')

# df["datetime"]=df["datetime"].apply(lambda x:  x-dt.timedelta(hours=x.hour+1) if x.hour < 2 else x)
df["end_datetime"]=pd.to_datetime(df["end_time"]/1000, unit = 's')

df["diff"]=(df["end_time"] - df["start_time"])/3600000

df_zero=df.loc[df["diff"]<1]
print(df_zero.info())

df_j=df.loc[ df["datetime"] > dt.datetime.strptime("2020-06-12 11:59:24",'%Y-%m-%d %H:%M:%S')]
df_j=df_j.loc[ df_j["datetime"] < dt.datetime.strptime("2020-06-14 12:59:24",'%Y-%m-%d %H:%M:%S')]
# print(df_j.describe())
# print(df_j.head())

df.index  = df["datetime"]

# print(df.head())

dfm =df.resample('D').count()

print(dfm.describe())

fig, ax = plt.subplots()

# dfm.reset_index().plot(x='datetime', y='diff')
dfm.plot(x='datetime', y='diff')
print(dfm.info())

exit()
# print(df["diff"].describe())
# df.plot.scatter(x="datetime",y="diff")
date_form = DateFormatter("%y-%m-%d")
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.show()
# df["sleep_time"]=df["com.samsung.health.sleep.end_time"]-df["com.samsung.health.sleep.start_time"]

df_j=df.iloc[ df["datetime"] > dt.datetime.strptime("2020-06-12 11:59:24",'%Y-%m-%d %H:%M:%S')]
df_j=df_j.iloc[ df_j["datetime"] < dt.datetime.strptime("2020-06-14 12:59:24",'%Y-%m-%d %H:%M:%S')]
print(df_j.head())
print(df_j.info())