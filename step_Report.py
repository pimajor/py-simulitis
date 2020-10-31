import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.dates import DateFormatter


path = "C:\\Users\\pierre\\Downloads\\files\\Download\\samsunghealth_pierre.major_202008021218\\com.samsung.shealth.step_daily_trend.202008021218.csv"

df = pd.read_csv(path, skiprows=1,index_col=False)
print(df.info())
# print(df["com.samsung.health.step_count.count"].head())


df=df.drop(columns = ["binning_data","datauuid","source_pkg_name","pkg_name","deviceuuid"])


df["datetime"]=pd.to_datetime(df["day_time"]/1000, unit = 's')

# df["datetime"]=df["datetime"].apply(lambda x:  x-dt.timedelta(hours=x.hour+1) if x.hour < 2 else x)
# df["end_datetime"]=pd.to_datetime(df["end_time"]/1000, unit = 's')

# df["diff"]=(df["end_time"] - df["start_time"])/3600000

# df_zero=df.loc[df["diff"]<1]
# print(df_zero.info())

# exit()
# df_j=df.loc[ df["datetime"] > dt.datetime.strptime("2020-06-12 11:59:24",'%Y-%m-%d %H:%M:%S')]
# df_j=df_j.loc[ df_j["datetime"] < dt.datetime.strptime("2020-06-14 12:59:24",'%Y-%m-%d %H:%M:%S')]
# print(df_j.describe())
# print(df_j.head())

# df.index  = df["datetime"]

# # print(df.head())

# dfm =df.resample('D').sum()


# print(df["diff"].describe())
fig, ax = plt.subplots()
df.plot.scatter(x="datetime",y="count")
date_form = DateFormatter("%y-%m-%d")
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.show()

print(df["count"].loc[df["count"]>0].describe())
print(df["count"].describe())