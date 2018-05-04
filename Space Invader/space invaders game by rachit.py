#Space Invaders - Part 1
#set up the screen
import turtle
import os
import math
import random      #to put enemies at random position . If this is not used, only one enemy will move and others will stay at one position only
#set up the screen
import winsound
import sys
import pygame

pygame.init()

pygame.mixer.music.load("bgsound.wav")
pygame.mixer.music.play(-1)

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("InvaderBG.gif")

#Register the shapes

turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")






#Draw Border

border_pen = turtle.Turtle()  #create a turtle to make a pen to draw the border
border_pen.speed(0)   #0 is the fastest speed of drawing
border_pen.color("white")
border_pen.penup() #so that the pen while travelling down from centre doesn't draw
border_pen.setposition(-300,-300)
border_pen.pendown() #putting the pen down after bringing it to the position (-300,300)
border_pen.pensize(3)   #pen is 3 pixel wide
for side in range(4):    #drawing a square by the pen. Our entire game will occur within the square
    border_pen.fd(600)  #go forward by 600
    border_pen.lt(90)   #turn left by 90 degrees
    
border_pen.hideturtle()    #hide the turtle so that we just see the black screen and the border when we run the module


#Set the score to 0
score = 0

#Draw the score

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,280)
scorestring = "Score: %s" %score
score_pen.write(scorestring,False,align="left",font=("Arial",14,"normal"))
score_pen.hideturtle()

#Create the player turtle

#for now we are not worrying about graphics and all . We'll use the built in shapes

player = turtle.Turtle()  #creating a turtle object for the player
player.color("blue")    #for now giving it blue color. we'll change it to an image later
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)   #down towards the bottom of the border
player.setheading(90)  #the triangle before using this command was facing towards right. Now we set it's head to up by turning it left by 90 degree. So now the triangle's head faces upward



#Make the player move left or right through arrow keys on the keyboard

playerspeed = 15  #the distance by which the player moves when we press the arrow key




#Choose the no. of enemies
number_of_enemies = 5

#Create an empty list of enemies
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
    #Create the enemy
    enemies.append(turtle.Turtle())



#Create the enemy
for enemy in enemies:
    
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200,200)   #give random value between -200 and 200
    y = random.randint(100,250)    #give random vaalue between 100 and 250
    enemy.setposition(x,y)         #gives position to the enemies

enemyspeed = 2

#Create the player's weapon
bullet = turtle.Turtle()
bullet.color("Yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed = 20

#Define bullet state
#State 1 = ready - ready to fire
#State 2 = fire - bullet is firing,ie, moving
bulletstate = "ready"

#create a function to move the player left and another function for moving the player right and then we need to bind those functions to arrow keys on the keyboard

def move_left():
    x = player.xcor()   #get the present x coordinate of the player
    x-= playerspeed     #subtracts the present coordinate of the player by playerspeed(in this case 15). So the player moves left by 15 coordinates
    if x<-280:          # This is used to keep the player within boundary
        x=-280
    player.setx(x)      #set the x coordinate of the player to the x coordinate which the player reaches after moving left once(i.e., by playerspeed)

def move_right():
    x = player.xcor()   #get the present x coordinate of the player
    x+= playerspeed     #adds the present coordinate of the player by playerspeed(in this case 15). So the player moves right by 15 coordinates
    if x>280:           # This is used to keep the player within boundary
        x=280
    player.setx(x)
    

#bullet firing functions

def fire_bullet():
    #Declare bullet state as a global if it needs changed
    global bulletstate   #declaring it as global even though it's global so that any change in this variable in this function should change the global variable's value and not just it's value in the fuction
    if bulletstate == "ready":     #this is used so that the player can fire only one bullet at a time
        bulletstate = "fire"
        #Move the bullet to just above the player
        winsound.PlaySound('gunshot.wav', winsound.SND_ASYNC)
        x = player.xcor()
        y = player.ycor() +10
        bullet.setposition(x,y)
        bullet.showturtle()

#to check collision
def isCollision(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))   #using pythagorus theorem a2 + b2 = c2
    if distance<15:
        winsound.PlaySound('blast.wav', winsound.SND_ASYNC)
        return True
    else:
        return False
    
    
    


#Create keyboard Bindings

turtle.listen()   #tell the turtle to listen for keyboard actions
turtle.onkey(move_left,"Left")  #when I push the "Left" key on the keyboard the function move_left() executes or is called and thus the player moves left
turtle.onkey(move_right,"Right")  #when I push the "Right" key on the keyboard the function move_right() executes or is called and thus the player moves right
turtle.onkey(fire_bullet,"space")

pygame.mixer.music.play(-1)


#Main Game loop

while True:

    
    
    for enemy in enemies:
        #Move the enemy
        x= enemy.xcor()
        x+= enemyspeed
        enemy.setx(x)

        #once the enemy reaches either side of the screen, we want it to reverse it's direction of motion and all the enemies to come down

        if enemy.xcor()>280:
            for e in enemies:
                #move all the enemies down by 40 units in y-coordinate when one of them reverses its direction
                y = e.ycor()
                y-= 40
                e.sety(y)
                
            enemyspeed *=-1   #reverse the motion from left to right
            
        if enemy.xcor()<-280:
            for e in enemies:
                #move all the enemies down by 40 units in y-coordinate when one of them reverses its direction
                y = e.ycor()
                y-= 40
                e.sety(y)
                
            enemyspeed *=-1 #reverse the motion from right to left
        #check for a collision between enemy and the bullet

        if isCollision(bullet,enemy):
            #Reset the bullet
            bullet.hideturtle
            bulletstate = "ready"
            bullet.setposition(0,-400)    #this is done to bring the bullet down completely while it's hidden(ie, after a collision) to prevent further collisions
            #Update the score
            score+=10
            scorestring = "Score: %s" %score
            score_pen.clear()  #if we don't use this our old score will collide with the new score to we clear the old score when new score is made
            score_pen.write(scorestring,False,align="left",font=("Arial",14,"normal"))

            #Reset the enemy to a random path when it has been destroyed
            x = random.randint(-200,200)   #give random value between -200 and 200
            y = random.randint(100,250)    #give random vaalue between 100 and 250
            enemy.setposition(x,y)         #gives position to the enemies

            
        #check for a collision between enemy and player

        if isCollision(player,enemy):
            player.hideturtle()
            enemy.hideturtle()
            print "GAME OVER"
            break

    #Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y+= bulletspeed
        bullet.sety(y)

    #check to see if the bullet has gone to the top
    if bullet.ycor()>275:
        bullet.hideturtle()
        bulletstate = "ready"
    

    
    

    

    













delay = raw_input("Press enter to finish")
