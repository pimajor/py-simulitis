import Person
import turtle
import json

import numpy as np
import matplotlib.pyplot as plt

with open('config.json') as f:
  config = json.load(f)

susceptible_idx = 0
infected_idx = 1
recovered_idx = 2

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Virus Simulator")
wn.tracer(0) # update screen only when needed

file_name = "simulitis.csv" # will be used to log the statistics
persons = [] 
width =  .8 #this is the default, TODO CALCULATE DYNAMICALLY

recovered_rate= config["recovered_rate_perc"] 
infected_rate= config["infected_rate_perc"] 

print("infected rate " + str(infected_rate))

print("recovered rate " +str(recovered_rate))


population_size  = config["population_size"]
infected_start = population_size*infected_rate/100
recovered_start = population_size*recovered_rate/100

print("recovered start " + str(recovered_start) +" , infected start" + str(infected_start))
init_infected =0
init_recovered = 0
for _ in range(population_size):
    person = Person.Person()
    if init_recovered < recovered_start:
        init_recovered +=1
        person.recover()
    elif init_infected < infected_start :
        init_infected +=1
        person.transmit()
    persons.append(person)


status=[0,infected_start,recovered_start] # to keep and log statistics
stats = []
statsInfected  = []
statsSuceptible  = []
statsRecovered  = []

tick_count = 0
with open(file_name,'w+') as f:
    while status[1] > 0:
        status=[0,0,0] # to keep and log statistics
        for person in persons:
            person.tick()
            if(status[infected_idx]>10):
                person.confine()
            for coll in persons:
                if coll != person:
                    person.check_collision(coll)
        
            if person.is_clean() : #not sick (yet)
                status[susceptible_idx]+=1
            elif person.is_sick() : #sick
                status[infected_idx]+=1
            else: #recovered
                status[recovered_idx]+=1
        wn.update()        
        stats.append(status)    
        statsInfected.append(status[infected_idx])
        statsSuceptible.append(status[susceptible_idx])
        statsRecovered.append(status[recovered_idx])
   

    infected_count = 0
    vector_count = 0



    for person in persons:
        if person.has_reocovered :
            #only count the number of sick person who have infected people (who did not have it before)
            vector_count += 1 if person.get_infected_count() > 0 else 0
            infected_count+= person.get_infected_count()

    R_o = infected_count / vector_count if vector_count > 0 else 0 
    print("Only ", infected_count, " persons have transmitted the viues")
    print("Average infection by sick person Ro :", R_o)

    #Plot the results
    #sub sample the array by taking every 10 items
    statsInfected = statsInfected[::10]
    statsSuceptible = statsSuceptible[::10]
    statsRecovered  = statsRecovered[1::10]
    ind = np.arange(len(statsInfected))
    plt.bar(ind, statsInfected, width, color='r')
    plt.bar(ind, statsSuceptible, width, bottom =statsInfected, color='b')
    plt.bar(ind, statsRecovered, width,bottom=[i+j for i,j in zip(statsSuceptible, statsInfected)] , color='g')

    plt.show()
    
    
    f.close()

wn.mainloop()