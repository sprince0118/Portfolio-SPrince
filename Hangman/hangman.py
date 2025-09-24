from tkinter import *
import random
import turtle
#===============================================================================================================================

def getWord(): #opens file to get random word
    file = open(r'output.txt', 'r')
    try:
        data = file.readlines()
        word = data[random.randint(0,len(data))] #gets random word from file
        word = word.rstrip('\n')
        return word
    finally:
        file.close()

def guess(char): #
    global split
    global lives
    global display
    correct = 0
    for i in range(len(split)): #for each letter in solution:
        if split[i] == char: #check if guess letter is in this position in solution
            correct = correct + 1
            display[i] = char
            text['text'] = display #updates display word
    if correct == 0: #if no correct letter in word:
        lives = lives - 1
        livesLeft['text'] = lives #updates lives display
        checkLoss(lives)
        checkDraw(lives)
    else:
        checkWin()

def checkWin():
    global split
    global display
    win = True
    for letter in range(len(split)): #goes through each letter in word and compares against completed split word
        if split[letter] != display[letter]:
            win = False
    if win == True: #sets the window to win config
        root.geometry('380x350')
        livesLeft.config(bg="green")
        livesLeft['text'] = 'YOU WIN'

def checkDraw(val): #draws the graphic according to lives left, val = lives
    if val == 9:
        draw.goto(-50,-70)
    elif val == 8:
        draw.goto(-20,-70)
        draw.goto(-20,60)
    elif val == 7:
        draw.goto(0,60)
        draw.goto(-20,40)
        draw.goto(-20,60)
        draw.goto(30,60)
    elif val == 6:
        draw.goto(30,45)
    elif val == 5:
        draw.penup()
        draw.goto(30,5)
        draw.pendown()
        draw.circle(20)
    elif val == 4:
        draw.goto(30,-35)
    elif val == 3:
        draw.goto(35,-55)
        draw.goto(30,-35)
    elif val == 2:
        draw.goto(25,-55)
        draw.goto(30,-35)
    elif val == 1:
        draw.goto(30,-5)
        draw.goto(40,-5)
    elif val == 0:
        draw.goto(20,-5)
        
def checkLoss(val): #checks for a loss, val = lives
    global split
    if val <= 0: #sets window to lose config
        root.geometry('380x350')
        livesLeft.config(bg="red")
        livesLeft['text'] = 'GAME OVER'
        text['text'] = split #sets display word to solution

def A(): #called by button to pass value through guess()
    guess('a')
    coverA = Button(text='',height=1,width=1).grid(row=2,column=2) #creates empty button to cover used letter
def B():
    guess('b')
    coverB = Button(text='',height=1,width=1).grid(row=2,column=3)
def C():
    guess('c')
    coverC = Button(text='',height=1,width=1).grid(row=2,column=4)
def D():
    guess('d')
    coverD = Button(text='',height=1,width=1).grid(row=2,column=5)
def E():
    guess('e')
    coverE = Button(text='',height=1,width=1).grid(row=2,column=6)
def F():
    guess('f')
    coverF = Button(text='',height=1,width=1).grid(row=2,column=7)
def G():
    guess('g')
    coverG = Button(text='',height=1,width=1).grid(row=2,column=8)
def H():
    guess('h')
    coverH = Button(text='',height=1,width=1).grid(row=2,column=9)
def I():
    guess('i')
    coverI = Button(text='',height=1,width=1).grid(row=2,column=10)
def J():
    guess('j')
    coverJ = Button(text='',height=1,width=1).grid(row=2,column=11)
def K():
    guess('k')
    coverK = Button(text='',height=1,width=1).grid(row=2,column=12)
def L():
    guess('l')
    coverL = Button(text='',height=1,width=1).grid(row=2,column=13)
def M():
    guess('m')
    coverM = Button(text='',height=1,width=1).grid(row=2,column=14)
def N():
    guess('n')
    coverN = Button(text='',height=1,width=1).grid(row=3,column=2)
def O():
    guess('o')
    coverO = Button(text='',height=1,width=1).grid(row=3,column=3)
def P():
    guess('p')
    coverP = Button(text='',height=1,width=1).grid(row=3,column=4)
def Q():
    guess('q')
    coverQ = Button(text='',height=1,width=1).grid(row=3,column=5)
def R():
    guess('r')
    coverR = Button(text='',height=1,width=1).grid(row=3,column=6)
def S():
    guess('s')
    coverS = Button(text='',height=1,width=1).grid(row=3,column=7)
def T():
    guess('t')
    coverT = Button(text='',height=1,width=1).grid(row=3,column=8)
def U():
    guess('u')
    coverU = Button(text='',height=1,width=1).grid(row=3,column=9)
def V():
    guess('v')
    coverV = Button(text='',height=1,width=1).grid(row=3,column=10)
def W():
    guess('w')
    coverW = Button(text='',height=1,width=1).grid(row=3,column=11)
def X():
    guess('x')
    coverX = Button(text='',height=1,width=1).grid(row=3,column=12)
def Y():
    guess('y')
    coverY = Button(text='',height=1,width=1).grid(row=3,column=13)
def Z():
    guess('z')
    coverZ = Button(text='',height=1,width=1).grid(row=3,column=14)
    
#===============================================================================================================================
word = getWord() #empty word
split = [] #list of letters in word
display = [] #displayed on label to show the hangman word
lives = 10
root = Tk() #initialise tkinter window
root.resizable(False, False) #prevents players from resizing window to reveal buttons after game end
root.title("Hangman")

exitButton = Button(text='Exit', command=root.destroy).grid(row=0,column=0) #exit button to end program

drawCanvas = Canvas(root) #creates canvas as middle frame
drawCanvas.grid(row=1,column=0)

draw = turtle.RawTurtle(drawCanvas) #initialises turtle
draw.hideturtle() #initial setup for turtle
draw.penup()
draw.goto(10,-70)
draw.pendown()
draw.speed(500)

text = Label(text='loading...', font=("Helvetica", 14))
text.grid(row=2,column=0) #creating + positioning label for displaying word

livesLeft = Label(text=lives)
livesLeft.grid(row=3,column=0) #creating + positioning indicator for lives remaining

buttonA = Button(text='a',height=1,width=1,command=A).grid(row=2,column=2) #creating buttons for guessing
buttonB = Button(text='b',height=1,width=1,command=B).grid(row=2,column=3)
buttonC = Button(text='c',height=1,width=1,command=C).grid(row=2,column=4)
buttonD = Button(text='d',height=1,width=1,command=D).grid(row=2,column=5)
buttonE = Button(text='e',height=1,width=1,command=E).grid(row=2,column=6)
buttonF = Button(text='f',height=1,width=1,command=F).grid(row=2,column=7)
buttonG = Button(text='g',height=1,width=1,command=G).grid(row=2,column=8)
buttonH = Button(text='h',height=1,width=1,command=H).grid(row=2,column=9)
buttonI = Button(text='i',height=1,width=1,command=I).grid(row=2,column=10)
buttonJ = Button(text='j',height=1,width=1,command=J).grid(row=2,column=11)
buttonK = Button(text='k',height=1,width=1,command=K).grid(row=2,column=12)
buttonL = Button(text='l',height=1,width=1,command=L).grid(row=2,column=13)
buttonM = Button(text='m',height=1,width=1,command=M).grid(row=2,column=14)
buttonN = Button(text='n',height=1,width=1,command=N).grid(row=3,column=2) #move to second row for easier layout
buttonO = Button(text='o',height=1,width=1,command=O).grid(row=3,column=3)
buttonP = Button(text='p',height=1,width=1,command=P).grid(row=3,column=4)
buttonQ = Button(text='q',height=1,width=1,command=Q).grid(row=3,column=5)
buttonR = Button(text='r',height=1,width=1,command=R).grid(row=3,column=6)
buttonS = Button(text='s',height=1,width=1,command=S).grid(row=3,column=7)
buttonT = Button(text='t',height=1,width=1,command=T).grid(row=3,column=8)
buttonU = Button(text='u',height=1,width=1,command=U).grid(row=3,column=9)
buttonV = Button(text='v',height=1,width=1,command=V).grid(row=3,column=10)
buttonW = Button(text='w',height=1,width=1,command=W).grid(row=3,column=11)
buttonX = Button(text='x',height=1,width=1,command=X).grid(row=3,column=12)
buttonY = Button(text='y',height=1,width=1,command=Y).grid(row=3,column=13)
buttonZ = Button(text='z',height=1,width=1,command=Z).grid(row=3,column=14)

#===============================================================================================================================
for letter in word: #sets display label and splits word into individual letters
    split.append(letter)
    display.append('_')
text['text'] = display #sets empty display to be displayed in window

root.mainloop() #tkinter event loop
