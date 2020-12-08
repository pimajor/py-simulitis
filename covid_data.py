import matplotlib.dates as mdates
import pandas as pd
import datetime as dt
import numpy as np

confirmed_file = "C:\\work\\COVID-19\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_covid19_confirmed_global.csv"
recovered_file = "C:\\work\\COVID-19\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_covid19_recovered_global.csv"
death_file     = "C:\\work\\COVID-19\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_covid19_deaths_global.csv"
word_pop_file = "C:\\work\\py-simulitis\\data\\world_population_2020.csv"



class covid_data_provider:

    def __init__(self):
        self.confirmed  = self.read_csv(confirmed_file)
        self.dead       = self.read_csv(death_file)
        self.recovered  = self.read_csv(recovered_file)
        self.world_pop  = pd.read_csv(word_pop_file)

    def read_csv(self,path):
        df = pd.read_csv(path)
        df = df.replace(np.nan, '', regex=True)
        df = df.drop(columns=["Lat","Long"])
        df['country'] = df["Province/State"] + " - " + df["Country/Region"]
        df['country'] = df['country'].str.strip(" - ")
        df = df.drop(columns=["Province/State","Country/Region"])
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]
        # print(df.head())
        # df.rename(columns={ df.columns[0]: "datetime" }, inplace = True)
        # return df.T
        return df

    def get_death_for_countries(self, countries):
        d = self.dead
        return d.d[d['country'].isin(countries)]
   
    def get_confirmed_for_countries(self, countries):
        d = self.confirmed
        return d[d['country'].isin(countries)]

    def get_recovered_for_countries(self, countries):
        d = self.recovered
        return d[d['country'].isin(countries)]

    def get_timeline(self):
        df = self.dead
        df.rename(columns={ df.columns[0]: "datetime" }, inplace = True)
        df = df.T
        print(df.head())
        return df.index

data = covid_data_provider()

print(data.get_confirmed_for_countries(["France","Germany"]))
print(data.get_timeline())
