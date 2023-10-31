from tkinter import *
import random

GAME_WIDTH=1000
GAME_HEIGHT=550
SPEED=100
SPACE_SIZE=25
BODY_PARTS=3
SNAKE_COLOUR="green"
FOOD_COLOUR="red"
BACKGROUND_COLOUR="black"


class Snake:
    def _init_(self):
        self.body_size=BODY_PARTS
        self.coordinates=[]
        self.squares=[]

        for i in range(0,BODY_PARTS):
            self.coordinates.append([0,0])
        for x,y in self.coordinates:
            square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOUR,tag="snake")
            self.squares.append(square)

class Food:
    def _init_(self):
        x=random.randint(0,(GAME_WIDTH/SPACE_SIZE)-1)* SPACE_SIZE
        y=random.randint(0,(GAME_HEIGHT/SPACE_SIZE)-1)* SPACE_SIZE

        self.coordinates= [x,y]
        canvas.create_oval(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=FOOD_COLOUR,tag="food")


def next_turn(snake,food):
    x,y=snake.coordinates[0]

    if direction=="up":
        y-=SPACE_SIZE
    elif direction=="down":
        y+=SPACE_SIZE
    elif direction=="left":
        x-=SPACE_SIZE
    elif direction=="right":
        x+=SPACE_SIZE
    snake.coordinates.insert(0,(x,y))

    square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOUR)

    snake.squares.insert(0,square)

    if x==food.coordinates[0] and y==food.coordinates[1]:
        global score
        score+=1
        label.config(text="score:{}".format(score))
        canvas.delete("food")
        food=Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED,next_turn,snake,food)


def change_direction(new_direction):
    global direction

    if new_direction=='left':
        if direction!='right':
            direction=new_direction
    elif new_direction=='right':
        if direction!='left':
            direction=new_direction
    elif new_direction=='up':
        if direction!='down':
            direction=new_direction
    elif new_direction=='down':
        if direction!='up':
            direction=new_direction


def check_collisions(snake):
    x,y=snake.coordinates[0]

    if x<0 or x>=GAME_WIDTH:
        #print("GAME OVER")
        return True
    elif y<0 or y>=GAME_HEIGHT:
        #print("GAME OVER")
        return True
    
    for body_part in snake.coordinates[1:]:
        if x==body_part[0] and y==body_part[1]:
            print("GAME OVER")
            return True
        
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,font=("consolas",70),text="GAME OVER",fill="red",tags="gameover")

window=Tk()
window.title("SNAKE GAME")
window.resizable(False,False)

score=0
direction="down"

label=Label(window,text="score : {}".format(score),font=("consolas",40))
label.pack()

canvas=Canvas(window,bg=BACKGROUND_COLOUR,height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

window.update()

window_width=window.winfo_width()
window_heigth=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_heigth=window.winfo_screenheight()

x=int((screen_width/2)-(window_width/2))
y=int((screen_heigth/2)-(window_heigth/2))

window.geometry(f"{window_width}x{window_heigth}+{x}+{y}")

window.bind("<Left>",lambda event:change_direction("left"))
window.bind("<Right>",lambda event:change_direction("right"))
window.bind("<Up>",lambda event:change_direction("up"))
window.bind("<Down>",lambda event:change_direction("down"))


snake=Snake()
food=Food()
next_turn(snake,food)
window.mainloop()