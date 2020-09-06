import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import datetime as dt
import pandas as pd

word_pop_file = ".\\data\\world_population_2020.csv"

countries  = []

confirmed = []
confirmed_file = "C:\\work\\COVID-19\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_covid19_confirmed_global.csv"
confirmed_subtitle = "Confirmed cases"
confirmed.append(confirmed_file)
confirmed.append(confirmed_subtitle)

recovered = []
recovered_file = "C:\\work\\COVID-19\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_covid19_recovered_global.csv"
recovered_subtitle = "Recovered cases"
recovered.append(recovered_file)
recovered.append(recovered_subtitle)

death = []
death_file = "C:\\work\\COVID-19\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_covid19_deaths_global.csv"
death_subtitle = "Death cases"
death.append(death_file)
death.append(death_subtitle)

world_pop = pd.read_csv(word_pop_file)
print(world_pop.info())
col_country_name = world_pop.columns[0]
col_country_pop = world_pop.columns[1]
case = confirmed

def main():
   
    mat = getMatrixFromCSV(case[0])
    time = getTimeLine(mat)
    state = getMatrix(mat)

    # showCountries(state)

    speed = getSpeedMatrix(mat)
    acc = getAccelerationMatrix(speed)  

    country = "France"

    groups= []

    groups.append(["France", "Germany", "Italy", "Spain","Portugal", "United Kingdom"])
    groups.append(["Mexico", "Brazil", "US", "Russia", "India"])
    groups.append(["Belgium", "Netherlands", "Sweden", "Switzerland"])
    groups.append(["Morocco", "Algeria", "Senegal", "Tunisia"])
    groups.append(["Finland","Iceland","Denmark", "Sweden", "Norway" ])
    groups.append([ "Vietnam", "Singapore", "Japan","Philippines"])
    

    print("Last report ", time[-1])
    print("total ",case[1]," count in ", country," : " , state[country]["values"][-1])
    print("new cases for  ",case[1]," in ", country," : " , speed[country]["values"][-1])

    # plotAgainstTime(country,speed,time,3,True)
    # plotAgainstTime(country,acc,time,10,False)
    # plotAgainstTime(country,state,time,1, True)
    for countries in groups:
        plotCountries(countries,speed,time,14,True,relative=True)
    

    # plot(country,speed,state,7)
    
    
def average(array,window_size):
    avg = []
    for i in range(len(array)):
        a = 0
        count = 0  
        
        for j in range(max(0,i-window_size+1),i +1):
            a +=array[j]
            count +=1
        avg.append(a/(count if count > 0 else 1))
    return avg


def plotCountries(countries,dicto,time,window_size,log,relative):
    title =""
    line, ax = plt.subplots(figsize=(10, 6))
    for country in countries:
        data = dicto[country]["values"]
        if relative:
            c_pop = world_pop.loc[world_pop[col_country_name] == country]
            if c_pop.shape[0]==0:
                print(country + " has no entry in world pop")
            else: 
                pop = c_pop.iloc[0][col_country_pop]
                data /=(pop/100000)

        data_avg = average(data,window_size) 
        title = country if title =="" else title + " vs. " + country
        
        if log:
           
            # line = plt.semilogy(time,data_avg)
            #  

            ax.semilogy(time,data_avg)
            date_form = DateFormatter("%d-%m-%y")
            ax.xaxis.set_major_formatter(date_form)
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

            ax.set_label(country)      
           
            plt.grid(True, which="both")
        else:
            line, = plt.plot(time,data)
            line.set_label(country)
            
    plt.legend(countries)
    plt.title(title +" \n" + case[1] + " " + (dicto[country]["unit"] + "/100000 inhabitants" if relative else dicto[country]["unit"] ))
    plt.xlabel("Time")
    plt.xticks(rotation=90)    
    plt.show()
    
def plot(name,ydico,xdico,window_size):
    data_avg = average(ydico[name]["values"],window_size) 
    xdata = average(xdico[name]["values"],window_size)

    plt.title(name + " " + case[1] + " " + ydico[name]["unit"])
    plt.ylabel(ydico[name]["unit"])
    plt.xlabel(xdico[name]["unit"])
    plt.loglog(xdata,data_avg)
    plt.show()
    

def plotAgainstTime(name,dicto,time,window_size,log):
    data = dicto[name]["values"]
    data_avg = average(data,window_size) 

    
    plt.title(name + " " + case[1] + " " + dicto[name]["unit"])
    plt.ylabel(dicto[name]["unit"])
    plt.xlabel("Time")
    plt.xticks(rotation=90)
    if log:
        plt.semilogy(time,data)
        plt.semilogy(time,data_avg)
        plt.grid(True, which="both")
    else:
        plt.plot(time,data)
        plt.plot(time,data_avg)

    plt.show()
    

def plot(name,ydico,xdico,window_size):
    data_avg = average(ydico[name]["values"],window_size) 
    xdata = average(xdico[name]["values"],window_size)

    plt.title(name + " " + case[1] + " " + ydico[name]["unit"])
    plt.ylabel(ydico[name]["unit"])
    plt.xlabel(xdico[name]["unit"])
    plt.loglog(xdata,data_avg)
    plt.show()
    
def getTimeLine(mat):
   
    dates = mat[0][4:]  
    dates_list = [dt.datetime.strptime(date, '%m/%d/%y') for date in dates]
    print(dates_list[0].isoformat())
    return dates_list
        
def getMatrix(mat):

    state = {}

    rowCount = 0
    for country in mat:
        if rowCount > 1:
            col  = 0
            colCount = 0
            value  = []
            for colCount in range(len(country)):
                if colCount > 3: 
                    value.append(int(country[colCount]))
           
            name = country[1] if country[0] == "" else country[0] + "-" + country[1]
            countries.append(name)
 
            record = {}
            record["unit"] = "# cases"
            record["values"] = value
            state[name] = record
        rowCount +=1
    return state    

def getSpeedMatrix(mat):

    speed = {}

    rowCount = 0
    for country in mat:
        if rowCount > 1:
            col  = 0
            colCount = 0
            diff  = []
          
            for colCount in range(len(country)-1):
                if colCount > 3: 
                    diff.append(int(country[colCount + 1]) - int(country[colCount]))
            
            name = country[1] if country[0] == "" else country[0] + "-" + country[1]
 
            diff.insert(0,0)
            record = {}
            record["unit"] = "new cases/day"
            record["values"] = diff
            speed[name]= record
        rowCount +=1
    return speed    

def getAccelerationMatrix(speed):

    acc = {}
    for country in speed:
        diff = []
        colCount = 0
        for value in speed[country]["values"]:
            if colCount > 0:
                diff.append(speed[country]["values"][colCount]-speed[country]["values"][colCount-1])
            colCount+=1
        diff.insert(0,0)    
        record = {}
        record["unit"] = "Acceleration: new cases/day^2"
        record["values"] = diff
        acc[country] = record
    return acc    

def showCountries(countries):
    for row in countries:
        print(row)

def getMatrixFromCSV(csvFile):
  
    rowCount = 0

    matrix = []

    with open(csvFile, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            colCount = 0
            if rowCount >= len(matrix):
                matrix.append([])

            for col in row:
                matrix[rowCount].append(col)
                colCount += 1
            rowCount += 1

    return matrix

if __name__ == '__main__':
    main()

