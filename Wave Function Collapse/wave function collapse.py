#SCP 12/5/23#

from tkinter import *
import random
from PIL import Image, ImageTk

#tile rules
tileRules = [[0,0,0,0],
             [0,1,0,1],
             [1,0,1,0],
             [0,1,1,1],
             [1,0,1,1],
             [1,1,0,1],
             [1,1,1,0],
             [2,1,0,1],
             [0,1,2,1],
             [0,1,2,0],
             [0,0,2,1],
             [0,0,2,0],
             [2,0,0,0]]

#create empty board

boardSize = int(input("Board size: ")) #CHANGE THIS VARIABLE TO CHANGE BOARD SIZE

board = [[0] * boardSize] * boardSize
#board = [[0],[0],[0],[0],[0]],[[0],[0],[0],[0],[0]],[[0],[0],[0],[0],[0]],[[0],[0],[0],[0],[0]],[[0],[0],[0],[0],[0]]

tileList = [[[0] * 4] * boardSize] * boardSize
#tileList = [[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]]],[[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]]],[[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]]],[[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]]],[[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]],[[0],[0],[0],[0]]],

pos = -1
row = 0

window = Tk()
window.title('Wave Function Collapse')

class Tile():
        
    def __init__(self, pos, size):

        rule = [-1,-1,-1,-1] #clear rules

        loop = True
        while loop: #loop for selecting suitable tile

            des = random.randint(0,12) #designate tile as 1 of 11 possible images
            #print(f"TILE {pos}")

            for i in range(0,4): #initialise rules for individual tile
                rule[i] = tileRules[des][i]
            
            #check rules for images around it, check if possible, redesignate if not
            valid = True

            #check north
            if pos%size != 0: #if in top row, do not check
                #print(f"SELF: {rule}") #own rules
                #print(f"TILE @ {pos//size}, {(pos - 1)%size} IS {tileList[pos//size][(pos - 1)%size]}") #previous tile rules
                if tileList[pos//size][(pos - 1)%size][2] != rule[0]: #if connection on north is not the same as connection on tile above:
                    valid = False

            #check west
            if pos//size != 0: #if in top row, do not check
                #print(f"SELF: {rule}") #own rules
                #print(f"TILE @ {pos//size - 1}, {pos%size} IS {tileList[pos//size - 1][pos%size]}") #previous tile rules
                if tileList[pos//size - 1][pos%size][1] != rule[3]: #if connection on north is not the same as connection on tile above:
                    valid = False

            #checks east and south not neccessary in the way tiles are placed
            #if any check fails, redesignate
            if valid:
                loop = False

        tileList[pos//size][pos%size] = rule #set rule of selected tile to list of all rules for every tile

        board[pos//size][pos%size] = 1 #reserve space in board

        img = Image.open(str(des) + ".png")
        img = img.resize((50, 50))
        img = ImageTk.PhotoImage(img)

        block = Label(image=img, borderwidth=0, highlightthickness=0)
        block.image = img

        block.grid(column=pos//size, row=pos%size, sticky="nsew")
        

for i in range(0, boardSize * boardSize): #build board
    Tile(i, boardSize) #creates new tile
    window.update()

window.mainloop()

