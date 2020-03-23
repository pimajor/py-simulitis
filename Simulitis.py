import Person
import turtle

import numpy as np
import matplotlib.pyplot as plt

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Virus Simulator")
wn.tracer(0) # update screen only when needed

file_name = "simulitis.csv" # will be used to log the statistics
balls = [] 
width =  .8 #this is the default, TODO CALCULATE DYNAMICALLY

population_size = 100

for _ in range(population_size):
    balls.append(Person.Person())

balls[0].set_sick()
status=[0,1,0] # to keep and log statistics
stats = []
statsSick  = []
statsHealthy  = []
statsRecovered  = []

with open(file_name,'w+') as f:
    while status[1] > 0:
       
        status=[0,0,0] # to keep and log statistics
        for ball in balls:
            ball.tick()
            for coll in balls:
                if coll != ball:
                    ball.check_collision(coll)

            if ball.is_clean() : #not sick (yet)
                status[0]+=1
            elif ball.is_sick() : #sick
                status[1]+=1
            else: #recovered
                status[2]+=1

        wn.update()        
        stats.append(status)    
        statsSick.append(status[1])
        statsHealthy.append(status[0])
        statsRecovered.append(status[2])
        
        # write sick, clean, recovered
        #f.write(str(status[1])+ "," + str(status[0])+ "," + str(status[2]) + "\n")   

    ind = np.arange(len(statsSick))
    plt.bar(ind, statsSick, width, color='r')
    plt.bar(ind, statsHealthy, width, bottom =statsSick, color='b')
    plt.bar(ind, statsRecovered, width,bottom=[i+j for i,j in zip(statsHealthy, statsSick)] , color='g')

    plt.show()
    
    f.close()
#wn.update()
wn.mainloop()