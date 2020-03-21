import Person
import turtle

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Virus Simulator")
wn.tracer(0) # update screen only when needed

#file_name = "c:\work\simulitis.csv" # will be used to log the statistics
balls = [] 

population_size = 100

for _ in range(population_size):
    balls.append(Person.Person())

balls[0].set_sick()

while True:
    wn.update()
    status=[0,0,0] # to keep and log statistics
    for ball in balls:
        ball.tick()
        for coll in balls:
            if coll != ball:
                ball.check_collision(coll)

        if ball.get_state() == 0:
            status[0]+=1
        elif ball.get_state() > 0:
            status[1]+=1
        else:
            status[2]+=1
               


wn.mainloop()