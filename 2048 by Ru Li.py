# 2048 by Ru Li
# ruxuan.li@uwaterloo.ca
# ruxuan.li@gmail.com

import random
from tkinter import *

# legal places a that numbers can be
legal_coordinates = [[0,0],[0,1],[0,2],[0,3],
                     [1,0],[1,1],[1,2],[1,3],
                     [2,0],[2,1],[2,2],[2,3],
                     [3,0],[3,1],[3,2],[3,3]]

# prints a board to visualize it
def visualize(state):
    print("State: ", state)
    print("-----------")
    coord = []
    for x in state:
        coord.append(x[0])
    for x in range(4):
        print("|", end=" ")
        for y in range(4):
            if [x,y] in coord:
                print(state[coord.index([x,y])][1], end=" ")
            else:
                print(".", end=" ")
        print("|")
    print("-----------")

# spawn the random tiles
def tile_spawn():
    empty_pos = empty_tiles()
    rand_oneten = random.randint(1,10)
    if rand_oneten == 10:
        new_tile = 4
    else:
        new_tile = 2
    state.append ([random.choice(empty_pos), new_tile])
    
# find all current empty tiles on the board
def empty_tiles():
    coord = []
    for x in state:
        coord.append(x[0])
    empty_pos = []
    for x in legal_coordinates:
        if x not in coord:
            empty_pos.append(x)
    return empty_pos

# checks if any tiles on the board can be combined with another
def adjacent(v, h):
    moved = []
    
    for x in state:
        if [[x[0][0]+v,x[0][1]+h],x[1]] in state and [[x[0][0]+v,x[0][1]+h],x[1]] not in moved and x not in moved:
            return False
    return True

# finds and combines any adjacent tiles with the same number
def neighbours(v, h):
    moved = []
    new_state = []
    del_list = []
    
    for x in state:
        if [[x[0][0]+v,x[0][1]+h],x[1]] in state and [[x[0][0]+v,x[0][1]+h],x[1]] not in moved and x not in moved:
            status["score"] += x[1]*2
            if x[1]*2 == 2048:
                status["gamewin"] == True
                canvas.create_text(650,200, text = "WINNER", font = my_font)
                
            new_state.append([[x[0][0],x[0][1]],x[1]*2])
            
            moved.append([[x[0][0]+v,x[0][1]+h],x[1]])
            moved.append(x)
            
            del_list.append([[x[0][0]+v,x[0][1]+h],x[1]])
            del_list.append(x)

    for z in new_state:
        state.append(z)        
    for y in del_list:
        state.remove(y)

# shifts all tiles in a given direction
def move_perform(direction):
    
    empty_shift = move_check(direction)
    
    if direction == "up":
        empty_shift.sort(key=lambda x: x[0])
        empty_shift.reverse()
        
        for a in empty_shift:
            for p in state:
                if p[0][1] == a[1] and p[0][0] > a[0] and [p[0][0]-1,p[0][1]] in legal_coordinates:            
                    state[state.index(p)] = [[p[0][0]-1,p[0][1]],p[1]]

    if direction == "down":
        empty_shift.sort(key=lambda x: x[0])
                    
        for a in empty_shift:
            for p in state:
                if p[0][1] == a[1] and p[0][0] < a[0] and [p[0][0]+1,p[0][1]] in legal_coordinates:            
                    state[state.index(p)] = [[p[0][0]+1,p[0][1]],p[1]]

    if direction == "left":
        empty_shift.sort(key=lambda x: x[1])
        empty_shift.reverse()
        
        for a in empty_shift:
            for p in state:
                if p[0][0] == a[0] and p[0][1] > a[1] and [p[0][0],p[0][1]-1] in legal_coordinates:            
                    state[state.index(p)] = [[p[0][0],p[0][1]-1],p[1]]

    if direction == "right":
        empty_shift.sort(key=lambda x: x[1])
                    
        for a in empty_shift:
            for p in state:
                if p[0][0] == a[0] and p[0][1] < a[1] and [p[0][0],p[0][1]+1] in legal_coordinates:
                    state[state.index(p)] = [[p[0][0],p[0][1]+1],p[1]]

# checks if it's possible to move the tiles in a given direction
def move_check(direction):
    empty_pos = empty_tiles()
       
    #**************************************************************************
    
    empty_shift = []
    if direction == "up":
        for x in empty_pos:
            for y in state:
                if x[1] == y[0][1] and x[0] < y[0][0] and x not in empty_shift:
                    empty_shift.append(x)
                    
    elif direction == "down":
        for x in empty_pos:
            for y in state:
                if x[1] == y[0][1] and x[0] > y[0][0] and x not in empty_shift:
                    empty_shift.append(x)

    elif direction == "left":
        for x in empty_pos:
            for y in state:
                if x[0] == y[0][0] and x[1] < y[0][1] and x not in empty_shift:
                    empty_shift.append(x)
                    
    elif direction == "right":
        for x in empty_pos:
            for y in state:
                if x[0] == y[0][0] and x[1] > y[0][1] and x not in empty_shift:
                    empty_shift.append(x)

    return empty_shift
                    
    #**************************************************************************
                    
# initalizes the game
def initialize_game():
    print("This is the game 2048")
    print("Use the arrow keys to play")
    print("Created by Ru Li")
    print("ruxuan.li@gmail.com")
    print("A Move History will be printed below")
    print("------------------------------------")
    status["gameover"] = False
    status["gamewin"] = False
    status["score"] = 0

    canvas.bind("<ButtonRelease-1>", callback)
    root.bind("<Key>", onkeypress)

    canvas.create_rectangle(2,2,458,458, fill = "white")
    
    for x in [20, 125, 230, 335]:
        for y in [20, 125, 230, 335]:
            canvas.create_rectangle(x, y, x+100, y+100)
            
    canvas.create_rectangle(525, 5, 775, 50, fill = "white")
    canvas.create_text(650, 30, text = "2048 by Ru Li",
                       font = my_font)

    canvas.create_rectangle(550, 100, 750, 150, fill = "white")
    canvas.create_text(650, 125, text = "Restart",
                       font = my_font)

    canvas.create_rectangle(500, 250, 800, 450, fill = "white")
    canvas.create_text(650, 275, text = "Score", font = my_font)
    canvas.create_line(525, 290, 775, 290)

    canvas.create_text(650, 360, text = status["score"], font = my_font,
                       tag = "score")
    
    tile_spawn()
    tile_spawn()
    visualize(state)
    inital_draw_board()

# draws the inital board on the canvas
def inital_draw_board():            
    for x in state:
        canvas.create_rectangle(20+x[0][1]*105, 20+x[0][0]*105,
                                120+x[0][1]*105, 120+x[0][0]*105,
                                tag = "color",
                                fill = color_str[color_num.index(x[1])])
        canvas.create_text(70+x[0][1]*105, 70+x[0][0]*105,
                           text = x[1],
                           font = my_font,
                           tag = "board")
        
# redraws the new state on the canvas  
def redraw():
    canvas.delete("color")
    canvas.delete("board")
    canvas.delete("score")
    for x in state:
        canvas.create_rectangle(20+x[0][1]*105, 20+x[0][0]*105,
                                120+x[0][1]*105, 120+x[0][0]*105,
                                tag = "color",
                                fill = color_str[color_num.index(x[1])])
        canvas.create_text(70+x[0][1]*105, 70+x[0][0]*105,
                           text = x[1],
                           font = my_font,
                           tag = "board")
    canvas.create_text(650, 360, text = status["score"], font = my_font,
                       tag = "score")

# When mouse is clicked, an action is performed                 
def callback(event):
    if 550 < event.x < 750 and 100 < event.y < 150:
        del state[:]
        redraw()
        initialize_game()      

# completes all steps to a move in any direction
def full_move(direction, k1, k2, n, r):
    move_perform(direction)
    state.sort(key=lambda x: x[0][n])
    if r:
        state.reverse()
    neighbours(k1, k2)
    move_perform(direction)
    tile_spawn()
    visualize(state)
    redraw()
    if not move_check("up") and not move_check("down") and not move_check("left") and not move_check("right"):
        if adjacent(1, 0) and adjacent(-1, 0) and adjacent(0, 1) and adjacent(0,1):
            status["gameover"] == True
            canvas.create_text (650,200, text = "Game Over", font = my_font)

# When an arrow key is pressed, an action is performed
def onkeypress(event):
    if (event.keysym == "Up"):
        if not move_check("up"):
            if adjacent(1, 0):
                print("Unable to Perform Move")
            else:
                full_move("up", 1, 0, 0, False)
        else:
            full_move("up", 1, 0, 0, False)
            
    elif (event.keysym == "Down"):
        if not move_check("down"):
            if adjacent(-1, 0):
                print("Unable to Perform Move")
            else:
                full_move("down", -1, 0, 0, True)
        else:
            full_move("down", -1, 0, 0, True)
            
    elif (event.keysym == "Left"):
        if not move_check("left"):
            if adjacent(0, 1):
                print("Unable to Perform Move")
            else:
                full_move("left", 0, 1, 1, False)
        else:
            full_move("left", 0, 1, 1, False)

    elif (event.keysym == "Right"):
        if not move_check("right"):
            if adjacent(0,1):
                print("Unable to Perform Move")
            else:
                full_move("right", 0, -1, 1, True)
        else:
            full_move("right", 0, -1, 1, True)


state = []
status = {}
a = [70, 175, 280, 385]
color_num = [2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768]
color_str = ["linen","peach puff","sandy brown","orange red","salmon",
             "red", "yellow", "aquamarine", "dark turquoise", "light blue",
             "gold"]

my_font = ("ariel", 20, "bold")

root = Tk()
root.title("2048 by Ru Li")
canvas = Canvas(root, width=825, height=460)
canvas.pack()

initialize_game()

root.mainloop()
