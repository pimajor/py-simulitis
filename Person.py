import turtle
import random
import json

with open('config.json') as f:
  config = json.load(f)


size = config["window_size"]
recovery_period = config["recovery_time"] # ticks
incubation_period = config["incubation_time_percent"] * recovery_period
collision_distance =  config["collision_distance"] # if a person gets into a square of 2 * collision_distance, it gets infected, 
# todo instead of distance, use trail where a sick person has gone
max_initial_speed = config["max_initial_speed"]
confinment_distance = config["confinment_distance"]


class Person(turtle.Turtle):
    state = 0 # zero means has not been sick, positive is the number of ticks while being sick, negative is recovered
    has_infected = 0 # number of people one has infected
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("blue")
        self.penup()
        self.speed(0)
        x = random.randint(-size+1,size-1)
        y = random.randint(-size+1,size-1)
        dx = random.randint(-max_initial_speed,max_initial_speed)
        dy = random.randint(-max_initial_speed,max_initial_speed)
        self.goto(x,y)
        self.dy = dx 
        self.dx = dy 
        self.x_o = 0
        self.y_o = 0
        self.edge = size
        self.infected = []
        

    def tick(self):
        self.sety(self.ycor() + self.dy)
        self.setx(self.xcor() + self.dx)
  
        # check for a bounce
        if abs(self.xcor()-self.x_o) > self.edge:
            self.dx *= -1   

        # check for a bounce
        if abs(self.ycor()-self.y_o) > self.edge:
            self.dy *= -1
   
        # update the sickness state and recover after the recovery period is over (starting when sick)
        if self.state > 0 :
            self.state +=1
            if self.state > recovery_period:
                self.recover()
                
            elif self.state > incubation_period:
                self.color("red")
                self.dy = 0
                self.dx = 0
                

    def recover(self):
        self.state = -1 # cannot get sick again
        self.color("green")
        self.dy = max_initial_speed * random.randint(-1,1)
        self.dx = max_initial_speed * random.randint(-1,1)

    def transmit(self):      
        """ sets the Person to sick and Returns True is infected for the first time """ 
        if self.state == 0 :
            self.state += 1
            self.color("pink")
            return True
        
        return False
        
    
    def check_collision(self,other):
      # this  more correct but very slow    if (other.xcor()-self.xcor())**2 + (other.ycor()-self.ycor())**2  < collision_distance**2:
      
         if (abs(other.xcor()-self.xcor()) < collision_distance
                    and  abs(other.ycor()-self.ycor()) < collision_distance):
                    self.dy *= -1
                    self.dx *= -1
                    other.dy *= -1
                    other.dx *= -1

                    if self.is_sick () and other.transmit():
                        self.set_has_infected(other)
                    if other.is_sick() and self.transmit():
                        other.set_has_infected(self)
    
    def get_state(self):
        return self.state

    def is_sick(self):
        """ Returns True if the Person is currently sick """
        return self.state > 0

    def has_reocovered(self):
        """ Returns True if the Person has been infected and recovered """
        return self.state < 0

    def is_clean(self):
        """ Returns True if the Person has not been infected """
        return self.state == 0

    def set_has_infected(self, person):
        """ Increases the counter of Persons this Person has infected """
        self.infected.append(person)

    def get_infected_count(self):
        """ return the number of Persons this Person has infected """
        return len(self.infected)

    def confine(self):
        """ set the person in confinment """
        if self.edge != confinment_distance:
            self.edge = confinment_distance
            self.x_o = self.xcor()
            self.y_o = self.ycor()
            self.color("black")
    
    def unconfine(self):
        """ Deconfines the person  """
        self.edge = config["window_size"]
        self.x_o = 0
        self.y_o = 0
        self.color("blue")
             