from turtle import Turtle, Screen
from random import randint

# Strings
g_info = None
g_direction = None
# Lists
g_food = []
g_foodLocation = []
g_tailID = []
g_tailPosition = []
# Integers
g_time = 0
g_contact = 0
g_tailLength = 0
g_newLength = 5
# Bool Objects
g_up, g_down, g_left, g_right = False, False, False, False
g_pause = True
g_start = False
g_end = False
# Turtle and Screen Objects
g_snake = None
g_monster = None
g_screen = None

def createScreen(w=500, h=500):
    s = Screen()
    s.setup(w, h)
    s.title('Snake Game | Contacted: %d, Time: %d' %(g_contact, g_time))
    s.bgcolor("lightgreen")  # Set a light green background
    s.tracer(0)
    return s

def createTurtle(shape='square', color='darkgreen', x=0, y=0):
    tt = Turtle(shape)
    tt.up()
    tt.color(color)
    tt.goto(x,y)
    return tt

def intro():
    g_info.up()
    g_info.goto(-200, 200)
    font = ('Arial', 11, 'bold')
    g_info.write('Welcome to Snake Game.', font=font)
    g_info.goto(-200, 170)
    g_info.write('Use the 4 arrow keys to control the snake.', font=font)
    g_info.goto(-200, 140)
    g_info.write('Use space to stop / resume going forward.', font=font)
    g_info.goto(-200, 110)
    g_info.write('Try to eat all the food items before the monster catches you!', font=font)
    g_info.goto(-200, 80)
    g_info.write('Click anywhere to start. Have fun!', font=font)

def placeFood():
    global g_food, g_foodLocation
    for i in range(9):
        g_food.append(Turtle())
        g_food[i].hideturtle()
        g_food[i].up()
        g_food[i].speed(0)
        x = randint(-230, 230)
        y = randint(-230, 230)
        g_food[i].goto(x, y)
        g_food[i].color('orange')
        g_food[i].write(str(i+1), align="center", font=("Arial", 12, "bold"))
        g_foodLocation.append((x, y))

def checkEaten():
    global g_food, g_foodLocation, g_newLength, g_pause, g_end
    for i in range(9):
        if g_foodLocation[i] == '':
            continue
        (x, y) = g_foodLocation[i]
        if abs(g_snake.xcor()-x)<=13 and abs(g_snake.ycor()-y)<=13:
            g_food[i].clear()
            g_foodLocation[i] = ''
            g_newLength = g_newLength + (i+1)
    if g_tailLength == 50:
        g_end = True
        g_pause = True
        g_info.goto(-50, 0)
        g_info.color('blue')
        g_info.write('YOU WIN!', font=('Arial', 20, 'bold'))
    g_screen.update()

def PauseContinueSnake(direction=g_direction):
    global g_pause, g_direction
    if g_pause == True:
        g_pause = False
        if g_direction == 'up':
            snakeUp()
        elif g_direction == 'down':
            snakeDown()
        elif g_direction == 'left':
            snakeLeft()
        elif g_direction == 'right':
            snakeRight()
    else:
        if g_up:
            g_direction = 'up'
        elif g_down:
            g_direction = 'down'
        elif g_left:
            g_direction = 'left'
        elif g_right:
            g_direction = 'right'
        g_pause = True

def modifyUp():
    global g_up, g_down, g_left, g_right
    if not g_up and not g_pause:
        g_down, g_left, g_right = False, False, False
        g_up = True
        g_screen.ontimer(snakeUp, 300)

def modifyDown():
    global g_up, g_down, g_left, g_right
    if not g_down and not g_pause:
        g_up, g_left, g_right = False, False, False
        g_down = True
        g_screen.ontimer(snakeDown, 300)

def modifyLeft():
    global g_up, g_down, g_left, g_right
    if not g_left and not g_pause:
        g_down, g_up, g_right = False, False, False
        g_left = True
        g_screen.ontimer(snakeLeft, 300)

def modifyRight():
    global g_up, g_down, g_left, g_right
    if not g_right and not g_pause:
        g_down, g_left, g_up = False, False, False
        g_right = True
        g_screen.ontimer(snakeRight, 300)

def snakeUp(d=20):
    global g_tailLength
    if g_up and g_snake.ycor()<230 and not g_pause:
        if g_tailLength < g_newLength:
            extend(90)
            checkEaten()
            g_screen.ontimer(snakeUp, 500)
        else:
            extend(90)
            checkEaten()
            g_screen.ontimer(snakeUp, 300)
        refreshContact()

def snakeDown(d=20):
    global g_tailLength
    if g_down and g_snake.ycor()>-230 and not g_pause:
        if g_tailLength < g_newLength:
            speed = 500
        else:
            speed = 300
        extend(270)
        checkEaten()
        g_screen.ontimer(snakeDown, speed)
        refreshContact()

def snakeLeft(d=20):
    global g_tailLength
    if g_left and g_snake.xcor()>-230 and not g_pause:
        if g_tailLength < g_newLength:
            speed = 500
        else:
            speed = 300
        extend(180)
        checkEaten()
        g_screen.ontimer(snakeLeft, speed)
        refreshContact()

def snakeRight(d=20):
    global g_tailLength
    if g_right and g_snake.xcor()<230 and not g_pause:
        if g_tailLength < g_newLength:
            speed = 500
        else:
            speed = 300
        extend(0)
        checkEaten()
        g_screen.update()
        g_screen.ontimer(snakeRight, speed)
        refreshContact()

def extend(heading=0, dist=20):
    global g_tailID, g_tailLength, g_tailPosition
    color = g_snake.color()
    g_snake.color('limegreen', 'green')  # Change body color
    g_tailID.append(g_snake.stamp())
    g_tailPosition.append((g_snake.xcor(), g_snake.ycor()))
    g_snake.setheading(heading)
    g_snake.forward(dist)
    g_snake.color(*color)
    if g_tailLength == g_newLength:
        g_snake.clearstamp(g_tailID[0])
        g_tailID.remove(g_tailID[0])
        g_tailPosition.remove(g_tailPosition[0])
    else:
        g_tailLength += 1
    g_screen.update()

def moveMonster():
    global g_end, g_pause
    DistanceX = g_monster.xcor() - g_snake.xcor()
    DistanceY = g_monster.ycor() - g_snake.ycor()
    if not g_end:
        if abs(DistanceX) >= abs(DistanceY):
            if DistanceX > 0:
                monsterLeft()
            else:
                monsterRight()
        else:
            if DistanceY > 0:
                monsterDown()
            else:
                monsterUp()
        refreshContact()
        g_screen.title('Snake Game | Contacted: %d, Time: %d' %(g_contact, g_time))
        if abs(DistanceX) < 21 and abs(DistanceY) < 21:
            g_end = True
            g_pause = True
            g_info.goto(-50, 0)
            g_info.color('red')
            g_info.write('YOU LOSE!', font=('Arial', 20, 'bold'))
        speed = randint(350, 550)
        g_screen.update()
        g_screen.ontimer(moveMonster, speed)

def monsterUp(d=20):
    g_monster.setheading(90)
    g_monster.forward(d)
    g_screen.update()

def monsterDown(d=20):
    g_monster.setheading(270)
    g_monster.forward(d)
    g_screen.update()

def monsterLeft(d=20):
    g_monster.setheading(180)
    g_monster.forward(d)
    g_screen.update()

def monsterRight(d=20):
    g_monster.setheading(0)
    g_monster.forward(d)
    g_screen.update()

def keyControl(s):
    s.onkey(modifyUp, 'Up')
    s.onkey(modifyDown, 'Down')
    s.onkey(modifyLeft, 'Left')
    s.onkey(modifyRight, 'Right')
    s.onkey(PauseContinueSnake, "space")
    s.listen()

def Start(x, y):
    global g_pause, g_start
    if not g_start:
        g_pause = False
        g_info.clear()
        placeFood()
        g_start = True
        g_screen.update()
        g_screen.ontimer(refreshTime, 1000)
        moveMonster()

def refreshTime():
    global g_time
    if not g_end:
        g_time += 1
        g_screen.ontimer(refreshTime, 1000)

def refreshContact():
    global g_contact
    for (x, y) in g_tailPosition:
        if abs(g_monster.xcor()-x) <= 20 and abs(g_monster.ycor()-y) <= 20:
            g_contact += 1
            break

def main():
    global g_screen, g_snake, g_monster, g_info
    g_screen = createScreen()
    g_snake = createTurtle()
    g_info = createTurtle()
    g_info.hideturtle()
    x = randint(-220, -180)
    y = randint(-220, -180)
    g_monster = createTurtle(color='purple', x=x, y=y)
    intro()
    g_screen.update()
    g_screen.onclick(Start)
    keyControl(g_screen)
    g_screen.mainloop()

if __name__ == '__main__':
    main()