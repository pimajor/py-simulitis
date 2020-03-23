import turtle
import random

edge = 350
recovery_period = 1000 # ticks
collision_distance = 3 # if a person gets into a square of 2 * collision_distance, it gets infected, 
# todo instead of distance, use trail where a sick person has gone

class Person(turtle.Turtle):
    state = 0 # zero means has not been sick, positive is the number of ticks while being sick, negative is recovered
    has_infected = 0 # number of people one has infected
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("blue")
        self.penup()
        self.speed(0)
        x = random.randint(-edge+1,edge-1)
        y = random.randint(-edge+1,edge-1)
        dx = random.randint(-3,3)
        dy = random.randint(-3,3)
        self.goto(x,y)
        self.dy = dx 
        self.dx = dy 

    def tick(self):
        self.sety(self.ycor() + self.dy)
        self.setx(self.xcor() + self.dx)
        
        # check for a bounce
        if abs(self.ycor()) > edge:
            self.dy *= -1

        # check for a bounce
        if abs(self.xcor()) > edge:
            self.dx *= -1

        # update the sickness state and recover after the recovery period is over (starting when sick)
        if self.state > 0 :
            self.state +=1
            if self.state > recovery_period:
                self.recover()

    def recover(self):
        self.state = -1 # cannot get sick again
        self.color("green")

    def set_sick(self):      
        """ sets the Person to sick and Returns True is infected for the first time """ 
        if self.state == 0:
            self.state = 1
            self.color("red")
            return True
        
        return False
        
    
    def check_collision(self,other):
         if (abs(other.xcor()-self.xcor()) < collision_distance
                    and  abs(other.ycor()-self.ycor()) < collision_distance):
                    self.dy *= -1
                    self.dx *= -1
                    other.dy *= -1
                    other.dx *= -1

                    if self.is_sick () and other.set_sick():
                        self.set_infected()
                    if other.is_sick() and self.set_sick():
                        other.set_infected()
    
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

    def set_infected(self):
        """ Increases the counter of Persons this Person has infected """
        self.has_infected +=1