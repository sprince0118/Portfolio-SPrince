import importlib.util
import subprocess
import sys

#install matplotlib if missing
required = {'matplotlib'}
missing = {pkg for pkg in required if importlib.util.find_spec(pkg) is None}

if missing:
    print(f"Installing required packages: {missing}")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
    print("Install complete.")


######################################################################################

import matplotlib.pyplot as plt
from tkinter import *

def loadFromFile():

    #create 2D array for holding shows
    data = []

    #DB format: Name|TV/Movie|Main Genre|Tier|Tag1|Tag2|etc
    #therefore data array format: 0 = name, 1 = TV/movie, 2 = genre, 3 = tier, >=4 = tags

    f = open("db.txt", "r")
    try:
        for line in f.readlines():
            line = line.strip("\n")
            data.append(line.split("|"))

    finally:
        f.close()
    
    return data


def getField(masterList, designation): #takes in the master list of data and a designation, then returns a list of all elements in that field (not working for tags (desg. 4+))

    names = [] #initialise name array (2D)

    for show in masterList:

        #data array format: 0 = name, 1 = TV/movie, 2 = genre, 3 = tier (4+ = tags)

        names.append(show[designation])

    return names


def getTags(masterList): #version of the getField method specifically for tags

    tags = [] #initialise array for tags (2D)

    for show in masterList:

        for i in range(len(show) - 4): #for the number of tags on the entry:

            tags.append(show[i + 4])

    return tags


def countInstances(fieldList): #takes in list of a field (from getField), and counts each instance of each entry. returns in the format [[name1, name2], [count of name1, count of name2]]

    instanceList = []
    instanceCount = []

    for instance in fieldList:
        if instance not in instanceList: #prevent repeat counting

            counter = 0
            instanceList.append(instance)

            for item in fieldList: #loop over list again in entirety to count number of instances
                if item == instance:
                    counter += 1
            
            instanceCount.append(counter)

    return [instanceList, instanceCount]


def selectTV(): #tkinter method for radio button functionality
    global tvOrMovie
    tvOrMovie = 1

def selectMovie(): #tkinter method for radio button functionality
    global tvOrMovie
    tvOrMovie = 2


def saveToFile(): #tkinter method for save to file button
    global tvOrMovie
    
    #format data to be written to file
    #DB format: Name|TV/Movie|Main Genre|Tier|Tag1|Tag2|etc

    #check if show is duplicate/entry field is blank by parsing through show names
    if nameText.get("1.0",END).strip("\n") in getField(loadFromFile(), 0) or nameText.get("1.0",END).strip() == "":
        print("Duplicate show. Cancelling add")
        return

    toWrite = "\n" + nameText.get("1.0",END).strip("\n")

    if tvOrMovie == 1:
        toWrite = toWrite + "|TV|"
    elif tvOrMovie == 2:
        toWrite = toWrite + "|Movie|"
    else:
        print("TV/Movie not selected")
        return #check that a radio button has actually been selected

    toWrite = toWrite + genreText.get("1.0",END).strip("\n") + "|" + tierText.get("1.0",END).strip("\n") #genre and tier

    for tag in tagsText.get("1.0",END).split(","): #split tags by commas
        toWrite = toWrite + "|" + tag.strip("\n").strip(" ") #strip whitespace and line breaks, and add to toWrite

    #open file and write
    f = open("db.txt", "a") #append mode
    try:
        f.write(toWrite)
        print("Successful write!")
    finally:
        f.close()

    #clear textboxes ready for next add



def showGraph(): #used by the show graph button to display the graph after all data is entered

    list = loadFromFile()

    fig, axs = plt.subplots(2, 3) #initialise matplotlib

    for i in range(3): #for genre, tier, tv/movie

        data = countInstances(getField(list, i + 1)) #load data

        axs[0, i].pie(data[1], labels=data[0])
        axs[1, i].bar(data[0], data[1])

    axs[0,0].title.set_text("Media")
    axs[0,1].title.set_text("Genre")
    axs[0,2].title.set_text("Rating")

    plt.show()    


def showTierBreakdown(): #show by breakdown of tiers (w/ genres and tags)

    sortedList, labels = sortIntoTiers()

    fig, axs = plt.subplots(2, len(sortedList)) #initialise matplotlib

    for i in range(len(sortedList)): #for each tier:

        genreData = countInstances(getField(sortedList[i], 2)) #get genre
        tagData = countInstances(getTags(sortedList[i]))

        axs[0, i].pie(genreData[1], labels=genreData[0])
        axs[1, i].barh(tagData[0], tagData[1])
        axs[0,i].title.set_text(labels[i])

    plt.show()
    

def sortIntoTiers(): #sort shows into different tiers
    
    sortedByTiers = [] #3d array unfortunately
    tierLabels = []

    list = loadFromFile()
    tierField = getField(list, 3)

    for tier in tierField: #for each entry in the list of tiers:

        if tier not in tierLabels: #if tier has not been sorted yet:

            tierLabels.append(tier)
            buffer = [] #create buffer 2D array to represent one single tier

            for i, dat in enumerate(tierField): #go through the list again and pick out the indexes of shows with the same tier to be sorted
                if tier == dat:
                    buffer.append(list[i]) #add show and associated data to buffer from main list
            
            sortedByTiers.append(buffer) #add buffer to sorted by tiers list
    
    return sortedByTiers, tierLabels

#########################################################################################################################################################
tvOrMovie = 0 #initialise variable for input control tv(1)/movie(2).

root = Tk()
root.title("ShowAnalyze")
root.geometry("550x400")

#graph refresh buttons
Label(text='Graphs', font=("Helvetica", 8)).place(x=40, y=50)
Button(text='Overview', command=showGraph).place(x=40, y=70)
Button(text='Breakdown by tier', command=showTierBreakdown).place(x=40, y=100)

#input controls
Label(text='INPUT NEW SHOW', font=("Helvetica", 16)).place(x=260, y=10)

Label(text='Name', font=("Helvetica", 8)).place(x=200, y=50)
nameText = Text(width=40, height=2)
nameText.place(x=200, y=70)

Label(text='Tier (S/A/B/C/D/F)', font=("Helvetica", 8)).place(x=200, y=110)
tierText = Text(width=2, height=1)
tierText.place(x=200, y=130)

Radiobutton(root, text="TV", variable=tvOrMovie, value=1, command=selectTV).place(x=400, y=120)
Radiobutton(root, text="Movie", variable=tvOrMovie, value=2, command=selectMovie).place(x=450, y=120)

Label(text='Genre', font=("Helvetica", 8)).place(x=200, y=150)
genreText = Text(width=40, height=1)
genreText.place(x=200, y=170)

Label(text='Tags (separate with comma)', font=("Helvetica", 8)).place(x=200, y=200)
tagsText = Text(width=40, height=3)
tagsText.place(x=200, y=220)

#save data to file button
Button(text='Save to File', command=saveToFile).place(x=320, y=300)

root.mainloop() #DO NOT REMOVE
