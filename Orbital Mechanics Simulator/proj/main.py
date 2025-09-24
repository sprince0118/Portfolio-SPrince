#####################################IMPORTS###########################################

import pygame
import engine
import numpy
import math
import asyncio

################################CLASS DEFINITIONS######################################


class Button(pygame.sprite.Sprite):

    def __init__(self, designation, physEng): #init method

        pygame.sprite.Sprite.__init__(self) #initialise Pygame sprite

        self.designation = designation

        self.imageUnclicked = pygame.image.load("UIbutton" + str(designation) + ".png").convert_alpha() #load images from file based on designation
        self.imageClicked = pygame.image.load("UIbutton" + str(designation) + "Clicked.png").convert_alpha()

        self.isClicked = False #set initial state
        self.imageUnscaled = self.imageUnclicked #set initial image
        
        #set unique initial variables for buttons:
        match designation:

            case 0: #if pause button:
                self.isClicked = True #set initial pause state
                self.imageUnscaled = self.imageClicked #set initial image as clicked

            case 5: #if camera focus button:
                self.objectNumber = -1 #initialise variable for object to focus on
        
            case 18: #if build menu move button:
                self.pickedObject = 0 #set initial picked object (cleared)

        self.collideRect = pygame.Rect(0,0,0,0) #initialise rect for collisions

        self.rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height()) #get initial rect

        self.rescale(physEng) #initial rescale


    def rescale(self, physEng):

        screenWidth = screen.get_width() #cache screen width
        screenHeight = screen.get_height() #cache screen height

        match self.designation: #collision rect positioning

            case 0: #pause button:
                self.image = pygame.transform.scale(self.imageUnscaled,(screenWidth*0.063, screenHeight*0.063)) #rescale to window size
                self.rect.update(screenWidth*0.03, screenHeight*0.93, screenWidth*0.063, screenHeight*0.063)
                self.collideRect.update(screenWidth/32, screenHeight*(33/36), screenWidth/16, screenHeight/9)

            case 1 | 2 | 3 | 4 : #main menu buttons:
                self.rect.update((screenWidth/8) * self.designation, screenHeight*(31/36), screenWidth/8, screenHeight*(5/36)) #update rectangular coordinates for mouse cursor detection: menu at base of screen

            case 5: #camera focus button:
                self.image = pygame.transform.scale(self.imageUnscaled, (screenWidth, screenHeight))
                self.collideRect.update(screenWidth*0.9081, screenHeight*0.7333, screenWidth*0.0869, screenHeight*0.0422) #update rectangular coordinates for mouse cursor detection: camera focus
            
            case 6 | 7: #north/south camera movement buttons:                
                self.rect.update(screenWidth*0.944, screenHeight * 0.079 * (self.designation + 1), screenWidth*0.0225, screenHeight*0.08) #update rectangular coordinates for mouse cursor detection: north/south camera movement

            case 8 | 9: #east/west camera movement buttons:
                self.rect.update(screenWidth - screenWidth * 0.0445 * (self.designation - 7), screenHeight*0.6156, screenWidth*0.0425, screenHeight*0.0411) #update rectangular coordinates for mouse cursor detection: north/south camera movement

            case 10: #equipotential resolution increase:

                self.image = pygame.transform.scale(self.imageUnscaled, (screenWidth*0.125, screenHeight*0.069))
                self.rect.update(screenWidth*0.25, screenHeight*0.828, screenWidth*0.125, screenHeight*0.069)
                self.collideRect.update(screenWidth*0.355, screenHeight*0.82, screenWidth*0.0125, screenHeight*0.0411) #update rectangular coordinates for equipotential resolution increase

            case 11: #equipotential resolution decrease:
                self.rect.update(screenWidth*0.253, screenHeight*0.832, screenWidth*0.015, screenHeight*0.025) #update rectangular coordinates for equipotential resolution decrease

            case 12: #hide UI button:
                self.rect.update(screenWidth*0.9081, screenHeight*0.79, screenWidth*0.0869, screenHeight*0.0422) #update rectangular coordinates for mouse cursor detection: hide UI

            case 13: #spacecraft turn left button:

                self.image = pygame.transform.scale(self.imageUnscaled, (screenWidth*0.125, screenHeight*0.033))
                self.rect.update(screenWidth*0.375, screenHeight*0.828, screenWidth*0.125, screenHeight*0.033)
                self.collideRect.update(screenWidth*0.38, screenHeight*0.82, screenWidth*0.035, screenHeight*0.0411) #update rectangular coordinates for spacecraft turn left

            case 14: #spacecraft turn right button:
                self.rect.update(screenWidth*0.46, screenHeight*0.832, screenWidth*0.035, screenHeight*0.028) #update rectangular coordinates for spacecraft turn right

            case 15: #spacecraft accelerate button:
                self.rect.update(screenWidth*0.42, screenHeight*0.832, screenWidth*0.035, screenHeight*0.027) #update rectangular coordinates for spacecraft accelerate

            case 16: #place planet button:

                self.image = pygame.transform.scale(self.imageUnscaled, (screenWidth*0.201, screenHeight*0.139))
                self.rect.update(screenWidth*0.626, screenHeight*0.861, screenWidth*0.201, screenHeight*0.139)
                self.collideRect.update(screenWidth*0.635, screenHeight*0.876, screenWidth*0.06, screenHeight*0.11) #update rectangular coordinates for mouse cursor detection: place planet

            case 17: #place star button:
                self.rect.update(screenWidth*0.703, screenHeight*0.876, screenWidth*0.06, screenHeight*0.11) #update rectangular coordinates for mouse cursor detection: place star

            case 18: #move object button:
                self.rect.update(screenWidth*0.769, screenHeight*0.876, screenWidth*0.024, screenHeight*0.042) #update rectangular coordinates for mouse cursor detection: move object

            case 19: #delete object button:
                self.rect.update(screenWidth*0.797, screenHeight*0.9, screenWidth*0.024, screenHeight*0.042) #update rectangular coordinates for mouse cursor detection: delete object

            case 20: #zoom slider:
                #slider top buffer: height * 0.2
                #slider area: (height * 0.55 - height * 0.2) = height * 0.35
                #zoom factor max. = 5x
                #0.35 / 5 = 0.07

                self.rect.update(screenWidth * 0.931, screenHeight * (0.55 - physEng.zoomScale * 0.07) - screenHeight/44, screenWidth/22, screenHeight/22) #get positioning rect for zoom slider

            case 21: #time scale slider:

                self.image = pygame.transform.scale(self.imageUnscaled,(screenWidth/50, screenHeight/20)) #rescale to window size

                #slider top buffer: width * 0.02
                #slider area: (width * 0.13 - width * 0.02) = width * 0.11
                #half slider area = width * 0.055

                #time scale factor max (1st half) = 20x
                #0.055 / 20 = 0.00275

                #time scale factor max. (2nd half) = 7200x
                #0.055 / 7200 = 0.00000764

                if physEng.timeScale < 3600:
                    self.rect.update(screenWidth * (0.02 + physEng.timeScale * 0.00275) - screenWidth/44, screenHeight * 0.88, screenWidth/50, screenHeight/20) #get positioning rect for time scale slider
                else:
                    self.rect.update(screenWidth * (0.055 + physEng.timeScale * 0.00000764) - screenWidth/44, screenHeight * 0.88, screenWidth/50, screenHeight/20) #get positioning rect for time scale slider

                self.collideRect = self.rect

            case 24: #close info panel button

                self.image = pygame.transform.scale(self.imageUnscaled, (screenWidth*0.143, screenHeight*0.722))
                self.rect.update(0, screenHeight*0.139, screenWidth*0.143, screenHeight*0.722)
                self.collideRect.update(screenWidth/8, screenHeight*(5/36), screenWidth*0.015, screenHeight*0.026) #update rectangular coordinates for mouse cursor detection: top right of info box

            case 26: #lock speed/velocity button
                self.rect.update(screenWidth*0.13, screenHeight*0.52, screenWidth*0.0125, screenHeight*0.05) #update rectangular coordinates for mouse cursor detection: lock speed/velocity (info box)

            case 27: #move to orbit page button

                self.image = pygame.transform.scale(self.imageUnscaled, (screenWidth*0.143, screenHeight*0.037))
                self.rect.update(0, screenHeight*0.822, screenWidth*0.143, screenHeight*0.037)
                self.collideRect.update(screenWidth*0.07, screenHeight*0.82, screenWidth*0.07, screenHeight*0.04) #update rectangular coordinates for mouse cursor detection: move to orbit page

            case 28: #move to object page button

                self.image = pygame.transform.scale(self.imageUnscaled, (screenWidth*0.143, screenHeight*0.037))
                self.rect.update(0, screenHeight*0.822, screenWidth*0.143, screenHeight*0.037)
                self.collideRect.update(0, screenHeight*0.82, screenWidth*0.07, screenHeight*0.04) #update rectangular coordinates for mouse cursor detection: move to object page

            case 29: #lock time period button
                self.rect.update(screenWidth*0.13, screenHeight*0.46, screenWidth*0.0125, screenHeight*0.025) #update rectangular coordinates for mouse cursor detection: lock time period (info box)

            case 30: #lock orbital radius button
                self.rect.update(screenWidth*0.13, screenHeight*0.49, screenWidth*0.0125, screenHeight*0.025) #update rectangular coordinates for mouse cursor detection: lock orbital radius (info box)

            case 31: #lock orbital velocity button
                self.rect.update(screenWidth*0.13, screenHeight*0.52, screenWidth*0.0125, screenHeight*0.025) #update rectangular coordinates for mouse cursor detection: lock orbital velocity (info box)

            case 32: #lock mass button
                self.rect.update(screenWidth*0.13, screenHeight*0.46, screenWidth*0.0125, screenHeight*0.025) #update rectangular coordinates for mouse cursor detection: lock mass (info box)

            case 33: #lock radius button
                self.rect.update(screenWidth*0.13, screenHeight*0.49, screenWidth*0.0125, screenHeight*0.025) #update rectangular coordinates for mouse cursor detection: lock radius (info box)

            case 34: #save/load scenario button
                self.rect.update(screenWidth*0.769, screenHeight*0.93, screenWidth*0.024, screenHeight*0.042) #update rectangular coordinates for mouse cursor detection: save/load scenario

            case 35: #load scenario 1

                self.image = pygame.transform.scale(self.imageUnscaled, (screenWidth*0.201, screenHeight*0.082))
                self.rect.update(screenWidth*0.626, screenHeight*0.779, screenWidth*0.201, screenHeight*0.082)
                self.collideRect.update(screenWidth*0.699, screenHeight*0.797, screenWidth*0.0275, screenHeight*0.049) #update rectangular coordinates for mouse cursor detection: load preset 1

            case 36: #load scenario 2
                self.rect.update(screenWidth*0.744, screenHeight*0.797, screenWidth*0.0275, screenHeight*0.049) #update rectangular coordinates for mouse cursor detection: load preset 2

            case 37: #load scenario 3
                self.rect.update(screenWidth*0.789, screenHeight*0.797, screenWidth*0.0275, screenHeight*0.049) #update rectangular coordinates for mouse cursor detection: load preset 3

            case _: #catch error for undesignated buttons (SHOULD never happen)
                print(f"ERROR: Button designation {self.designation} not recognised for collision rescale.")
        
        #collision rect set + image transformations
        exceptionButtons = [0,5,10,13,16,21,24,27,28,35] #list of buttons that have different rects and collideRects: their images and collideRects are set within the match..case statement above
        
        if not self.designation in exceptionButtons:

            self.image = pygame.transform.scale(self.imageUnscaled, (self.rect[2], self.rect[3])) #rescale image based on screen size
            self.collideRect = self.rect #create collision rect as area of image


    def effect(self, physEng, physObjects, spacecraft=0, buttonGroup=0, buildMenuGroup=0, redco=0, greenco=0, blueco=0): #applies effects of buttons

        global selectedObject #summon the great global variables
        global resolution
        global sidePanelPage

        match self.designation: #compare designation:

            case 0: #pause button

                physEng.isPaused = self.isClicked #sets physics engine to be paused/unpaused based on current state of button

            case 1 | 2: #orbit lines, equipotential lines
                pass #isClicked state is used in main running loop, so nothing is necessary here

            case 3: #spacecraft controls

                if self.isClicked: #if active:
                    spacecraft.angle = 0 #reset spacecraft angle
                    spacecraft.velocity = pygame.Vector2(0,0) #reset spacecraft velocity
                    spacecraft.gamePos = pygame.Vector2(((screen.get_width()/2)/(physEng.zoomScale + screen.get_width()/2)) - physEng.movementOffset[0], ((screen.get_height()/2)/(physEng.zoomScale + screen.get_height()/2)) - physEng.movementOffset[1]) #convert position at centre of screen to gamePos and move spacecraft to position
                    physObjects.add(spacecraft) #add spacecraft to physics object group for physics updates
                else:
                    physObjects.remove(spacecraft)
                    if spacecraft is selectedObject: #if spacecraft is selected object
                        selectedObject = 0 #clear selected object and close info panel

            case 4: #build menu

                if not physEng.isPaused and self.isClicked: #pause simulation if unpaused
                    buttonGroup.sprites()[9].isClicked = True #change pause button to pause state
                    buttonGroup.sprites()[9].imageUnscaled = buttonGroup.sprites()[9].imageClicked
                    buttonGroup.sprites()[9].rescale(physEng)
                    physEng.isPaused = True #switch physics engine state

                if self.isClicked == False: #build menu deactivation: reset build menu buttons
            
                    for i in buildMenuGroup: #for each menu button:
                            if i.isClicked: #if any button is active:
                                i.isClicked = False #turn button off
                                i.imageUnscaled = i.imageUnclicked #reset image
                                i.rescale(physEng)

            case 5: #camera focus

                self.objectNumber += 1 #increment object to focus on

                if self.objectNumber >= len(physObjects.sprites()): #if reached end of list:

                    self.objectNumber = -1 #loop back
                    physEng.updateCamera(0) #set to 0 (no object focused on)
                    selectedObject = 0 #clear selected object

                else:

                    physEng.updateCamera(physObjects.sprites()[self.objectNumber]) #set object to focus on in physics engine
                    selectedObject = physObjects.sprites()[self.objectNumber] #set as selected object

            case 6: #camera south
                physEng.updateCamera("S")

            case 7: #camera north
                physEng.updateCamera("N")

            case 8: #camera east
                physEng.updateCamera("E")

            case 9: #camera west
                physEng.updateCamera("W")

            case 10: #equipotential resolution increase

                if resolution != 1: #if resolution not miniumum:
                    resolution -= 1 #increment resolution

            case 11: #equipotential resolution decrease

                if resolution != 10: #if resolution not maximum:
                    resolution += 1 #decrement resolution

            case 12: #hide UI button
                pass #isClicked state is used in main running loop, so nothing is necessary here
    
            case 13: #turn spacecraft left
                spacecraft.angle += 2

            case 14: #turn spacecraft right
                spacecraft.angle -= 2

            case 15: #move spacecraft forwards
                spacecraft.addVelocity()

            case 16|17|18|19|34: #place planet, place star, move object, delete object (build menu buttons), save/load scenario

                for i in buildMenuGroup: #for each other menu button:
                    if i.isClicked and i is not self: #if any other button is active:
                        i.isClicked = False #turn button off
                        i.imageUnscaled = i.imageUnclicked #reset image
                        i.rescale(physEng)

                if self.designation == 16: #place planet
                    buildMenuGroup.sprites()[2].pickedObject = Planet(50, 10, pygame.Vector2(0,0), (127,51,0), pygame.Vector2(200,0)) #instantiate new planet with placeholder parameters, and set as picked object
                    physObjects.add(buildMenuGroup.sprites()[2].pickedObject) #add to physics objects group

                elif self.designation == 17: #place star
                    buildMenuGroup.sprites()[2].pickedObject = Star(100, 100, pygame.Vector2(0,0), 2000, pygame.Vector2(400,0), redco, greenco, blueco) #instantiate new star with placeholder parameters, and set as picked object
                    physObjects.add(buildMenuGroup.sprites()[2].pickedObject) #add to physics objects group


            case 20: #zoom slider

                screenWidth = screen.get_width() #cache screen width
                screenHeight = screen.get_height() #cache screen height

                screen.blit(font.render(f"Zoom scale: x{str(round(physEng.zoomScale, 2))}", True, (255, 255, 255)), (0, screenHeight*0.05)) #draw time scale value on screen

                if screenHeight * 0.53 > pygame.mouse.get_pos()[1] > screenHeight * 0.2: #checks if mouse cursor is within bounds of the slider area:
                    
                    self.rect.update(screenWidth* 0.931, pygame.mouse.get_pos()[1] - screenHeight/44, screenWidth/22, screenHeight/22) #change position based on mouse position

                    physEng.zoomScale = (0.55 * screenHeight - pygame.mouse.get_pos()[1])/(0.07 * screenHeight) #change zoom value based on Y position

            case 21: #time scale slider

                screenWidth = screen.get_width() #cache screen width
                screenHeight = screen.get_height() #cache screen height

                screen.blit(font.render(f"Time scale: x{str(round(physEng.timeScale, 2))}", True, (255, 255, 255)), (0, screenHeight*0.05)) #draw time scale value on screen

                if screenWidth * 0.115 > pygame.mouse.get_pos()[0] > screenWidth * 0.001: #checks if mouse cursor is within bounds of the slider area:
                    
                    self.rect.update(pygame.mouse.get_pos()[0] - screenWidth*0.005, screenHeight* 0.88, screenWidth/22, screenHeight/22) #change position based on mouse position

                    if pygame.mouse.get_pos()[0] < screenWidth * 0.055: #if in the real time scale side of slider:
                        physEng.timeScale = (pygame.mouse.get_pos()[0])/(0.00275 * screenWidth) #change time scale value based on X position
                    else: #if in celestial time scale side:
                        physEng.timeScale = (pygame.mouse.get_pos()[0])/(0.00000764 * screenWidth * 2) #change time scale value based on X position

            case 24: #close info panel button
                selectedObject = 0 #clear selected object

            case 26: #freeze velocity/speed
                selectedObject.velocityFreezeFlag = self.isClicked #set flag in object

            case 27: #move to orbit page of info panel
                sidePanelPage = 1

            case 28: #move to object page of info panel
                sidePanelPage = 0

            case 29: #freeze time period
                selectedObject.timePeriodFreezeFlag = self.isClicked

            case 30: #freeze orbital radius
                selectedObject.orbitalRadiusFreezeFlag = self.isClicked

            case 31: #freeze orbital velocity
                selectedObject.orbitalVelocityFreezeFlag = self.isClicked

            case 32: #freeze mass
                selectedObject.massFreezeFlag = self.isClicked

            case 33: #freeze radius
                selectedObject.radiusFreezeFlag = self.isClicked

            case 35 | 36 | 37: #load scenario 1/2/3

                physEng.movementOffset = pygame.Vector2(0,0) #reset camera offset
                physEng.zoomScale = 1 #reset zoom offset

                if not physEng.isPaused: #pause simulation if unpaused
                    buttonGroup.sprites()[9].isClicked = True #change pause button to pause state
                    buttonGroup.sprites()[9].imageUnscaled = buttonGroup.sprites()[9].imageClicked
                    buttonGroup.sprites()[9].rescale(physEng)
                    physEng.isPaused = True #switch physics engine state
                
                #delete all objects currently in scene
                for i in physObjects:

                    if i.__class__.__name__ != "Spacecraft": #exclude spacecraft from deletion checks

                        if i is selectedObject:
                            selectedObject = 0 #clear info panel
                        if i is physEng.focusedObject:
                            physEng.focusedObject = 0 #clear object focus

                        physObjects.remove(i) #remove from physics objects group

                loadScenario(self.designation - 34, physObjects, redco, greenco, blueco) #to get number for scenario, subtract 34 from designation

                self.isClicked = False #reset button
                self.imageUnscaled = self.imageUnclicked

            case _: #catch error for undesignated buttons (SHOULD never happen)
                print(f"ERROR: Button designation {self.designation} not recognised for effect.")


    def mouseHoldEnd(self, physEng): #called once when the mouse button is unclicked

        if (self.designation >= 6 and self.designation <= 9) or self.designation > 19 or self.designation == 5 or (self.designation >= 13 and self.designation <= 15): #if a camera control button or a slider:

            self.imageUnscaled = self.imageUnclicked #change graphic
            self.isClicked = False #set logic to be in unclicked state

            self.rescale(physEng) #update button image


    def mouseHoldUpdate(self, physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup): #called every tick when the mouse button is down

        if ((self.designation >= 6 and self.designation <= 9) or self.designation > 19 or (self.designation >= 13 and self.designation <= 15)) and self.isClicked: #if a camera movement button or slider, and is currently active:

            self.effect(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup) #apply button effect


    def update(self, physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup=0, redco=0, greenco=0, blueco=0): #called on mouse click

        if self.collideRect.collidepoint(pygame.mouse.get_pos()): #if mouse cursor is intersecting collision rect:

            if self.isClicked: #if button is in clicked state
                self.imageUnscaled = self.imageUnclicked #change graphic
                self.isClicked = False #set logic to be in unclicked state

            else: #if button is not in clicked state
                self.imageUnscaled = self.imageClicked #change graphic
                self.isClicked = True #set logic to be in clicked state

            self.effect(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup, redco, greenco, blueco) #apply effect of button
            self.rescale(physEng) #update button image



class Textbox(pygame.sprite.Sprite):

    def __init__(self, designation):

        pygame.sprite.Sprite.__init__(self) #initialise Pygame sprite

        self.text = "0" #set intial empty value
        self.active = False #set initial state as inactive
        self.designation = designation

        self.rect = pygame.Rect(0,0,0,0) #set initial rect

        self.colour = (255,255,255) #initially colour textbox white

        self.rescale()


    def textInput(self, input, masterObject=0, redco=0, greenco=0, blueco=0):

        global selectedObject

        validInputs = ["0","1","2","3","4","5","6","7","8","9","[","]",".",",","-"]

        if input.key == pygame.K_BACKSPACE: #if backspace pressed, and there is text in the textbox:

            self.text = str(self.text)[:-1] #set text as itself up to last character (set as string just in case another datatype is passed through)
       
        elif input.key == pygame.K_RETURN: #if enter key pressed:

            if len(self.text) == 0 and self.designation == 3: #if the text box for velocity is empty:
                self.text = "0,0" #set in vector2 format

            if self.designation != 3: #if not velocity:

                self.text = self.text.strip(" ,[]-N/A") #ensure positive and valid value for non-negative variables

                if len(self.text) == 0: #if the text box is empty:
                    self.text = "0" #set to 0

                decimal = False
                tempArray = []
                for char in self.text: #for each character in input:
                    if char == ".": #if decimal point:
                        if not decimal: #if there has already been a decimal point, do not add this character to the array. otherwise:
                            decimal = True #set flag
                            tempArray.append(char) #add to array
                    else: #if a digit:
                        tempArray.append(char) #add to array

                self.text = float("".join(tempArray)) #join chars in array, and convert to float

            #make changes to object based on text
            match self.designation:

                case 1: #mass
                    selectedObject.mass = self.text
                    if selectedObject.__class__.__name__ != "Spacecraft":
                        selectedObject.correctedMass = selectedObject.mass * (10**24) #convert to corrected mass
                    else:
                        selectedObject.correctedMass = self.text #otherwise, mass is corrected mass
                    
                case 2: #radius
                    if selectedObject.__class__.__name__ != "Spacecraft": #check for spacecraft: spacecraft has no radius variable
                        selectedObject.radius = self.text
                        selectedObject.correctedRadius = selectedObject.radius * (10**6) #convert to corrected radius

                case 3: #velocity

                    #split into two values (x,y)
                    values = self.text.split(",")
                    values[0] = float(values[0].strip(" [,]")) #strip values of spaces, commas, square brackets
                    values[1] = float(values[1].strip(" [,]"))
                    selectedObject.velocity = pygame.Vector2(values[0], values[1]) / 1000 #convert back from km/h

                case 4: #speed

                    if selectedObject.velocity[0] == 0: #check for 0 in horizontal component to prevent div by 0 error
                        if selectedObject.velocity[1] < 0: #if negative vertical component:
                            selectedObject.velocity[1] = - self.text / 1000 #speed change affects only vertical velocity, convert to km/h and change sign
                        else: 
                            selectedObject.velocity[1] = self.text / 1000 #speed change affects only vertical velocity, convert to km/h
                        
                    else:
                        magnitude = selectedObject.velocity.magnitude() + abs(selectedObject.velocity.magnitude() - self.text)
                        angle = math.atan(abs(selectedObject.velocity[1]/selectedObject.velocity[0]))

                        if selectedObject.velocity[0] < 0: #if negative horizontal component:
                            selectedObject.velocity[0] = - (magnitude * math.cos(angle)) / 1000 #result should be negative
                        else:
                            selectedObject.velocity[0] = (magnitude * math.cos(angle)) / 1000

                        if selectedObject.velocity[1] < 0: #if negative vertical component:
                            selectedObject.velocity[1] = - (magnitude * math.sin(angle)) / 1000 #result should be negative
                        else: 
                            selectedObject.velocity[1] = (magnitude * math.sin(angle)) / 1000

                case 5: #surface gravity

                    #G = GM/(R**2)
                    if selectedObject.__class__.__name__ != "Spacecraft": #check for spacecraft: spacecraft has no surface gravity variable

                        if selectedObject.massFreezeFlag and selectedObject.radiusFreezeFlag: #if both are frozen, the gravity cannot change while keeping consistent physics
                            self.text = str(round(selectedObject.calcSurfaceGrav(), 3))#reset gravitational force to what it was before
                        
                        elif selectedObject.massFreezeFlag: #if mass frozen, but radius is not:
                            selectedObject.correctedRadius = math.sqrt((6.67e-11*selectedObject.correctedMass)/self.text) #calculate radius
                            selectedObject.radius = selectedObject.correctedRadius / (10**6) #convert to corrected radius

                        else: #if nothing frozen/ radius frozen:
                        #elif selectedObject.radiusFreezeFlag: #if radius frozen, but mass is not: #temporary fix as below section is nonfunctional
                            selectedObject.correctedMass = ((self.text * selectedObject.correctedRadius**2)/6.67e-11) #calculate mass
                            selectedObject.mass = selectedObject.correctedMass / (10**24) #use to calculate corrected mass

                        #else: #if nothing frozen #THIS SECTION IS NONFUNCTIONAL.

                            #oldRadius = selectedObject.correctedRadius #get old radius for mass calc
                            #selectedObject.correctedRadius = math.sqrt((2 * selectedObject.correctedMass * 6.67e-11)/self.text) #calculate new radius                   
                            #selectedObject.radius = selectedObject.correctedRadius / (10**6) #calculate corrected radius
                            #selectedObject.correctedMass = (oldRadius**2 * self.text)/(2 * 6.67e-11) #calculate new mass
                            #selectedObject.mass = selectedObject.correctedMass / (10**24) #calculate corrected mass


                case 6: #surface temperature (STAR OBJECTS ONLY)

                    selectedObject.temperature = self.text
                    selectedObject.colour = selectedObject.getColour(selectedObject.temperature, redco, greenco, blueco) #recalculate + set selected object colour

                case 7: #time period
                    
                    if not selectedObject.orbitalRadiusFreezeFlag: #if orbital radius frozen, cannot change while keeping consistent physics

                        #time period = 2 * pi * ((selectedObject distance to masterObject)**(3/2)) / (sqrt(6.67e-11 * masterObject mass)
                        #=> new d = ((t*sqrt(6.67e-11*mass))/(2*pi))**(2/3)
                        #factor = new d / old d
                        if selectedObject.gamePos.distance_to(masterObject.gamePos) == 0: #prevent div by 0 error if objects are at same position
                            selectedObject.gamePos[0] += 1 #move object very slightly in order to prevent div by 0

                        factor = ((self.text*math.sqrt(6.67e-11*masterObject.correctedMass))/(2*math.pi))**(2/3) / selectedObject.gamePos.distance_to(masterObject.gamePos) 

                        #components: new x or y = factor*(distance to origin - distance to master) + distance from master to origin
                        selectedObject.gamePos[0] = factor*(selectedObject.gamePos[0] - masterObject.gamePos[0]) + masterObject.gamePos[0]
                        selectedObject.gamePos[1] = factor*(selectedObject.gamePos[1] - masterObject.gamePos[1]) + masterObject.gamePos[1]
                    
                case 8: #orbital radius

                    #orbital radius = selectedObject distance to masterObject
                    if selectedObject.gamePos.distance_to(masterObject.gamePos) == 0: #prevent div by 0 error if objects are at same position
                        selectedObject.gamePos[0] = 1 #move object very slightly in order to prevent div by 0

                    #factor = new d / old d
                    factor = self.text / selectedObject.gamePos.distance_to(masterObject.gamePos)

                    #components: new x or y = factor*(distance to origin - distance to master) + distance from master to origin
                    selectedObject.gamePos[0] = factor*(selectedObject.gamePos[0] - masterObject.gamePos[0]) + masterObject.gamePos[0]
                    selectedObject.gamePos[1] = factor*(selectedObject.gamePos[1] - masterObject.gamePos[1]) + masterObject.gamePos[1]

                case 9: #orbital velocity

                    if not selectedObject.orbitalRadiusFreezeFlag: #if orbital radius frozen, cannot change while keeping consistent physics

                        #orbital velocity = sqrt(force on selected object by master object * selectedObject distance to masterObject)
                        #=> new d = (6.67e-11*master object mass) / velocity**2
                        #factor = new d / old d
                        if selectedObject.gamePos.distance_to(masterObject.gamePos) == 0: #prevent div by 0 error if objects are at same position
                            selectedObject.gamePos[0] = 0.00000001 #move object very slightly in order to prevent div by 0
                                            
                        factor = ((6.67e-11*masterObject.correctedMass) / self.text**2) / selectedObject.gamePos.distance_to(masterObject.gamePos)

                        #components: new x or y = factor*(distance to origin - distance to master) + distance from master to origin
                        selectedObject.gamePos[0] = factor*(selectedObject.gamePos[0] - masterObject.gamePos[0]) + masterObject.gamePos[0]
                        selectedObject.gamePos[1] = factor*(selectedObject.gamePos[1] - masterObject.gamePos[1]) + masterObject.gamePos[1]

                case _: #no designation/unknown
                    print(f"ERROR: Textbox designation {self.designation} unrecognised for text input.")

        elif input.unicode in validInputs: #if input is a single digit number or square brackets:

            self.text = str(self.text) + input.unicode #add to text
    

    def rescale(self):

        if self.designation == 6: #if star temperature textbox:
            self.rect.update(0, screen.get_height()*0.605, screen.get_width()*0.13, screen.get_height()*0.03) #update rect for star temperature
        elif self.designation < 7: #if object screen textbox:
            self.rect.update(0, screen.get_height() * (0.425 + 0.03 * self.designation), screen.get_width()*0.13, screen.get_height()*0.03) #position rect according to designation
        else: #if orbit screen textbox:
            self.rect.update(0, screen.get_height() * (0.245 + 0.03 * self.designation), screen.get_width()*0.13, screen.get_height()*0.03) #position rect according to designation


    def clicked(self): #called on mouse click

        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.active: #if this object is clicked:
        
            self.active = True
            self.colour = (172,172,172) #fill with grey

        elif self.active and not self.rect.collidepoint(pygame.mouse.get_pos()): #if object is active, but click was elsewhere on screen

            self.active = False        
            self.colour = (255,255,255) #fill with white


    def update(self, masterObject=0, greatestForce=0): #called per tick to update values to that of the selected object

        global selectedObject

        if self.active: #if textbox is active:
            return #do not update textbox while value is being changed

        match self.designation:

            case 1: #mass
                self.text = str(round(selectedObject.mass, 1))

            case 2: #radius

                if selectedObject.__class__.__name__ != "Spacecraft": #spacecraft has no radius, so this will not be shown
                    self.text = str(round(selectedObject.radius, 1))
                else:
                    self.text = "N/A"

            case 3: #velocity
                self.text = str(selectedObject.velocity * 1000) #convert to km/h

            case 4: #speed
                self.text = str(round(selectedObject.velocity.magnitude() * 1000, 2)) #convert to km/h and round
                
            case 5: #surface gravity

                if selectedObject.__class__.__name__ != "Spacecraft": #spacecraft has no radius, so this will not be shown
                    self.text = str(round(selectedObject.calcSurfaceGrav(), 3))
                else:
                    self.text = "N/A"

            case 6: #surface temperature (STAR OBJECTS ONLY)
                self.text = str(selectedObject.temperature)

            case 7: #time period

                self.text = str(round((2*math.pi*(selectedObject.gamePos.distance_to(masterObject.gamePos)**(3/2)))/(math.sqrt(6.67e-11*masterObject.correctedMass)), 2)) #calculate time period, in seconds
                
            case 8: #orbital radius
                self.text = str(round(selectedObject.gamePos.distance_to(masterObject.gamePos), 1)) #get orbital radius as distance to master sprite
                                 
            case 9: #orbital velocity
                self.text = str(round(math.sqrt(greatestForce*selectedObject.gamePos.distance_to(masterObject.gamePos)), 2)) #get orbital velocity as root(force * distance to sprite)

            case _: #no designation/unknown

                print(f"ERROR: Textbox designation {self.designation} unrecognised for update.")



class Planet(pygame.sprite.Sprite):

    def __init__(self, radius, mass, velocity, colour, pos): #init method

        pygame.sprite.Sprite.__init__(self) #initialise Pygame sprite

        self.colour = colour
        self.radius = abs(radius) #absolute to avoid any negative values messing with pygame
        self.mass = mass

        #set initial variable freeze flags
        self.velocityFreezeFlag = False
        self.timePeriodFreezeFlag = False
        self.orbitalRadiusFreezeFlag = False
        self.orbitalVelocityFreezeFlag = False
        self.massFreezeFlag = False
        self.radiusFreezeFlag = False

        self.gamePos = pos
        self.screenPos = pos #set position on screen initially
        self.velocity = velocity

        #correct values for use in calculations
        self.correctedMass = self.mass * (10**24)
        self.correctedRadius = self.radius * (10**6)
        
        self.image = pygame.Surface([self.radius*2, self.radius*2]) #get surface of sprite to draw onto screen
        self.image.set_alpha(0) #set surface as invisible

        self.rect = self.image.get_rect(center=self.screenPos) #gets rectangular coordinates of surface for sprite


    def calcSurfaceGrav(self): #calculate what the gravitational force would be on the surface
    #g = GM/R**2
        
        if self.correctedRadius == 0:
            return 0 #prevent div by 0 error

        g = (6.67*(10**-11)*self.correctedMass) / (self.correctedRadius*self.correctedRadius)

        return g


    def getAtmosphereHeight(self, physicsObjects): #calculate atmospheric height (PLANET OBJECTS ONLY)

        atmosphereHeight = 0 #clear atmospheric height

        for i in physicsObjects: #for each object in simulation:
            if i.__class__.__name__ == "Star": #for each star object:

                if self.gamePos.distance_to(i.gamePos) != 0: #if distance to star is not 0 (prevents div by 0 error):

                    atmosphereHeight += (8.31 * i.temperature * ((0.7 * i.correctedRadius**2) / (4e6 * self.gamePos.distance_to(i.gamePos)))**(1/4)) / (0.029e6 * self.calcSurfaceGrav()) #calculate atmospheric height effect and add to variable

        return atmosphereHeight


    def update(self, physEng, physicsSprites, buildMenuGroup, buttonGroup):

        self.gamePos += self.velocity * physEng.getTimeScale() #move sprite in terms of simulation

        if self is buildMenuGroup.sprites()[2].pickedObject: #if picked object, go to mouse cursor position

            self.screenPos = pygame.Vector2(pygame.mouse.get_pos())
            
        else: #otherwise:

            self.screenPos = physEng.getScreenPos(self.gamePos, screen)  #convert gamePos -> screenPos

        #check for out of bounds, and clamp to within bounds if so
        if self.screenPos[0] < -214748600:
            self.screenPos[0] = -214748600
        elif self.screenPos[0] > 214748600:
            self.screenPos[0] = 214748600
        if self.screenPos[1] < -214748600:
            self.screenPos[1] = -214748600
        elif self.screenPos[1] > 214748600:
            self.screenPos[1] = 214748600

        if self.__class__.__name__ == "Planet" and buttonGroup.sprites()[2].isClicked: #if planet object and spacecraft controls active:

            pygame.draw.circle(screen, (self.colour[0]*0.25, self.colour[1]*0.25, self.colour[2]*0.25), self.screenPos, (self.radius + self.getAtmosphereHeight(physicsSprites)) * physEng.zoomScale, width=3) #draw atmosphere
        
        pygame.draw.circle(screen, self.colour, self.screenPos, self.radius * physEng.zoomScale) #draw planet

        self.rect = self.image.get_rect(center=self.screenPos) #update rect, centred at the planet's position



class Star(Planet):

    def __init__(self, radius, mass, velocity, temperature, pos, redco, greenco, blueco): #init method

        self.temperature = abs(temperature) #set temperature variable, absolute

        colour = self.getColour(self.temperature, redco, greenco, blueco) #get colour from temperature/RGB curve

        super().__init__(radius, mass, velocity, colour, pos) #initialise parent class


    def getColour(self, temperature, redco, greenco, blueco): #gets colour for star (code for function by DocLeonard on Stack Overflow)
        
        if temperature > 40000: #clamp temperature if outside range of graph
            return (0, 0, 255)

        red = redco(temperature) #get value for each colour from precalculated curve
        green = greenco(temperature)
        blue = blueco(temperature)

        if red > 255: #clamp values to RGB limits
            red = 255
        elif red < 0:
            red = 0
        if green > 255:
            green = 255
        elif green < 0:
            green = 0
        if blue > 255:
            blue = 255
        elif blue < 0:
            blue = 0

        return (int(red), int(green), int(blue)) #return colour



class Spacecraft(pygame.sprite.Sprite):

    def __init__(self, mass, pos, velocity):

        pygame.sprite.Sprite.__init__(self) #initialise Pygame sprite

        self.mass = mass
        self.correctedMass = mass #spacecraft mass does not need to be upscaled as planets do
        self.imageUnscaled = pygame.image.load("spacecraft.png").convert_alpha(screen) #load spacecraft image from file
        self.image = self.imageUnscaled #set initial image
        self.rect = self.image.get_rect() #set initial rect

        #set initial variable freeze flags
        self.velocityFreezeFlag = False
        self.timePeriodFreezeFlag = False
        self.orbitalRadiusFreezeFlag = False
        self.orbitalVelocityFreezeFlag = False

        self.gamePos = pos
        self.screenPos = pos #set position on screen initially
        self.velocity = velocity
        self.angle = 0 #set initial angle (in degrees) for rotation of spacecraft


    def addVelocity(self):

        radianAngle = (self.angle*math.pi)/180 #convert to radians for sin/cos methods

        if radianAngle <= math.pi/2:
            
            self.velocity[0] += math.cos(radianAngle) 
            self.velocity[1] -= math.sin(radianAngle) 
 
        elif radianAngle <= math.pi:

            self.velocity[0] -= math.cos(math.pi - radianAngle) 
            self.velocity[1] -= math.sin(math.pi - radianAngle) 

        elif radianAngle <= math.pi * (3/2):

            self.velocity[0] -= math.cos(radianAngle - math.pi) 
            self.velocity[1] += math.sin(radianAngle - math.pi) 

        else:

            self.velocity[1] += math.cos(radianAngle - (math.pi * (3/2))) 
            self.velocity[0] += math.sin(radianAngle - (math.pi * (3/2))) 


    def update(self, physEng, physObjects, buildMenuGroup, buttonGroup): #buildMenuGroup, buttonGroup and physObjects passed through here as it is passed through in planet class

        self.image = pygame.transform.rotate(pygame.transform.scale_by(self.imageUnscaled, physEng.zoomScale * 0.1), self.angle) #resize image by zoom factor, and rotate to angle

        self.gamePos += self.velocity * physEng.getTimeScale() #move sprite in terms of simulation

        self.screenPos = physEng.getScreenPos(self.gamePos, screen)  #convert gamePos -> screenPos

        #check for out of bounds, and clamp to within bounds if so
        if self.screenPos[0] < -214748600:
            self.screenPos[0] = -214748600
        elif self.screenPos[0] > 214748600:
            self.screenPos[0] = 214748600
        if self.screenPos[1] < -214748600:
            self.screenPos[1] = -214748600
        elif self.screenPos[1] > 214748600:
            self.screenPos[1] = 214748600
        
        self.rect = self.image.get_rect(center=self.screenPos) #update rect



################################INDEPENDENT METHODS####################################


def loadScenario(scenarioNumber, physObjects, redco, greenco, blueco):

    try: #in case of error, program will continue to run

        file = open(f"scenario{scenarioNumber}.txt", "r") #open file object to read
        for line in file.readlines(): #for each object saved in file:

            objData = line.split("/") #write data for object to array

            #split velocity and gamePos variables to put in correct format
            for i in range(3,6,2): #velocity = objData[3], gamePos = objData[5], step of 2 to skip over objData[4]
                tempArray = objData[i].split(",") #split data into two components
                objData[i] = pygame.Vector2(float(tempArray[0]), float(tempArray[1])) #format as Vector2

            if objData[0] == "s": #if object is a star:

                obj = Star(float(objData[1]), float(objData[2]), objData[3], float(objData[4]), objData[5], redco, greenco, blueco) #create object from data

            elif objData[0] == "p": #if object is a planet:

                #reformat colour data
                tempArray = objData[4].split(",") #split data into three components
                objData[4] = (float(tempArray[0]), float(tempArray[1]), float(tempArray[2])) #format as RGB tuple

                obj = Planet(float(objData[1]), float(objData[2]), objData[3], objData[4], objData[5]) #create object from data

            #set variable freeze flags
            if objData[6] == "1": #mass freeze flag
                obj.massFreezeFlag = True
            if objData[7] == "1": #radius freeze flag
                obj.radiusFreezeFlag = True
            if objData[8] == "1": #speed/velocity freeze flag
                obj.velocityFreezeFlag = True
            if objData[9] == "1": #time period freeze flag
                obj.timePeriodFreezeFlag = True
            if objData[10] == "1": #orbital radius freeze flag
                obj.orbitalRadiusFreezeFlag = True
            if objData[11] == "1": #orbital velocity freeze flag
                obj.orbitalVelocityFreezeFlag = True

            physObjects.add(obj)
                
    finally: #always close file to avoid corruption of data
        file.close()


##############################PROGRAM INITIALISATION###################################

pygame.init() #pygame setup

screen = pygame.display.set_mode(size=(1280, 720), flags=(pygame.RESIZABLE | pygame.DOUBLEBUF)) #sets up window to be able to be resized
pygame.display.set_caption('Orbital Mechanics Simulator') #names window
pygame.display.set_icon(pygame.image.load("icon.png")) #sets window icon

clock = pygame.time.Clock() #initialise pygame clock

font = pygame.font.SysFont('Consolas', 30) #initialise font

async def main(): #async function for Pygbag functionality

    #setup for star colour function - global variables so that they do not have to be stored in multiple star objects. code for function by DocLeonard on Stack Overflow
    redco = [ 1.62098281e-82, -5.03110845e-77, 6.66758278e-72, -4.71441850e-67, 1.66429493e-62, -1.50701672e-59, -2.42533006e-53, 8.42586475e-49, 7.94816523e-45, -1.68655179e-39, 7.25404556e-35, -1.85559350e-30, 3.23793430e-26, -4.00670131e-22, 3.53445102e-18, -2.19200432e-14, 9.27939743e-11, -2.56131914e-07,  4.29917840e-04, -3.88866019e-01, 3.97307766e+02]
    greenco = [ 1.21775217e-82, -3.79265302e-77, 5.04300808e-72, -3.57741292e-67, 1.26763387e-62, -1.28724846e-59, -1.84618419e-53, 6.43113038e-49, 6.05135293e-45, -1.28642374e-39, 5.52273817e-35, -1.40682723e-30, 2.43659251e-26, -2.97762151e-22, 2.57295370e-18, -1.54137817e-14, 6.14141996e-11, -1.50922703e-07,  1.90667190e-04, -1.23973583e-02,-1.33464366e+01]
    blueco = [ 2.17374683e-82, -6.82574350e-77, 9.17262316e-72, -6.60390151e-67, 2.40324203e-62, -5.77694976e-59, -3.42234361e-53, 1.26662864e-48, 8.75794575e-45, -2.45089758e-39, 1.10698770e-34, -2.95752654e-30, 5.41656027e-26, -7.10396545e-22, 6.74083578e-18, -4.59335728e-14, 2.20051751e-10, -7.14068799e-07,  1.46622559e-03, -1.60740964e+00, 6.85200095e+02]

    redco = numpy.poly1d(redco) #create curves for star function from above data points
    greenco = numpy.poly1d(greenco)
    blueco = numpy.poly1d(blueco)

    physEng = engine.PhysicsEngine() #initialise physics engine


    ##################################CREATE SPRITE GROUPS#################################


    physObjects = pygame.sprite.Group() #create physics object sprite group
    buttonGroup = pygame.sprite.Group() #initialise main buttons group
    equipotentialResolutionButtonGroup = pygame.sprite.Group() #initialise group for resolution buttons
    hideUIButtonGroup = pygame.sprite.Group() #create button group for the hide UI button
    sidePanelObjectButtons = pygame.sprite.Group() #initialise side menu buttons group
    textboxObjectGroup = pygame.sprite.Group() #initialise group for textbox in side panel object page
    textboxOrbitGroup = pygame.sprite.Group() #initialise group for textbox in side panel orbit page
    sidePanelOrbitButtons = pygame.sprite.Group() #initialise side menu orbit page buttons group
    sidePanelCloseButton = pygame.sprite.Group() #initialise close button group for side panel
    spacecraftGroup = pygame.sprite.Group() #initialise group for spacecraft
    spacecraftControlGroup = pygame.sprite.Group() #initialise group for spacecraft controls
    buildMenuGroup = pygame.sprite.Group() #initialise group for build menu
    loadPresetButtons = pygame.sprite.Group() #initialise group for preset scenario load buttons


    ##################################INITIALISE BUTTONS###################################

    for i in range(1,10): #create buttons
        buttonGroup.add(Button(i, physEng)) #instantiate button and add to update group

    buttonGroup.add(Button(0, physEng)) #create pause button (to be drawn on top of button 5)

    for i in range(20,22): #create slider buttons
        buttonGroup.add(Button(i, physEng)) #instantiate button and add to update group


    hideUIButtonGroup.add(Button(12, physEng)) #create hide UI button and add to its own group


    sidePanelCloseButton.add(Button(24, physEng)) #side panel close button is present on both pages, so it will be drawn in its own group

    for i in range(26,28): #create side panel buttons for object page
        sidePanelObjectButtons.add(Button(i, physEng))

    sidePanelObjectButtons.add(Button(32, physEng)) #create freeze mass button
    sidePanelObjectButtons.add(Button(33, physEng)) #create freeze radius button

    for i in range(28,32): #create side panel buttons for orbit page
        sidePanelOrbitButtons.add(Button(i, physEng))


    for i in range(1,6): #create textboxes for side panel pages
        textboxObjectGroup.add(Textbox(i))
    for i in range(7,10):
        textboxOrbitGroup.add(Textbox(i))

    surfaceTempTextbox = Textbox(6) #create textbox for star surface temperature


    equipotentialResolutionButtonGroup.add(Button(10, physEng)) #create equipotential resolution buttons
    equipotentialResolutionButtonGroup.add(Button(11, physEng))

    spacecraft = Spacecraft(1, (0,0), pygame.Vector2(0,0)) #initialise spacecraft object
    spacecraftGroup.add(spacecraft) #add spacecraft to its draw group
    spacecraftImage = pygame.image.load("spacecraft.png").convert_alpha()#cache spacecraft image for srawing to side panel


    for i in range(13,16): #create spacecraft control buttons:
        spacecraftControlGroup.add(Button(i, physEng))


    for i in range(16,20): #create build menu buttons:
        buildMenuGroup.add(Button(i, physEng))
    buildMenuGroup.add(Button(34, physEng)) #add save/load scenario button


    for i in range(35,38): #create preset scenario selection buttons:
        loadPresetButtons.add(Button(i,physEng))


    loadScenario(1, physObjects, redco, greenco, blueco) #load initial scenario from file


    ###############################GLOBAL VARIABLE SETUP###################################


    global selectedObject
    selectedObject = 0 #set no object to be selected at program start
    global resolution
    resolution = 5 #set initial equipotential line resolution as 5
    global sidePanelPage
    sidePanelPage = 0 #set initial side panel page to 0 (object info)


    ################################MAIN RUNNING LOOP######################################

    running = True

    while running: #running loop

        clock.tick(60)  #limits FPS to 60

        physicsSprites = physObjects.sprites()

        for event in pygame.event.get(): #for every key press:

            if event.type == pygame.QUIT: #if quit button (top right x) pressed:

                running = False

            elif event.type == pygame.WINDOWRESIZED: #if the window has been resized:

                for i in buttonGroup: #for each button on screen:
                    i.rescale(physEng) #rescale all buttons is group

                #side panel rescaling:
                for i in sidePanelObjectButtons:
                    i.rescale(physEng)
                for i in textboxObjectGroup:
                    i.rescale()

                for i in sidePanelOrbitButtons:
                    i.rescale(physEng)
                for i in textboxOrbitGroup:
                    i.rescale()
                surfaceTempTextbox.rescale()
                sidePanelCloseButton.sprites()[0].rescale(physEng)

                hideUIButtonGroup.sprites()[0].rescale(physEng) #rescale hide UI button

                for i in equipotentialResolutionButtonGroup:
                    i.rescale(physEng)

                for i in spacecraftControlGroup:
                    i.rescale(physEng)

                for i in buildMenuGroup:
                    i.rescale(physEng)

                for i in loadPresetButtons:
                    i.rescale(physEng)
            

            elif event.type == pygame.MOUSEBUTTONDOWN: #if the mouse has been clicked (or interactive whiteboard tapped)

                if buildMenuGroup.sprites()[2].pickedObject == 0: #if no object selected:

                    buttonGroup.update(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup) #run checks for buttons
                    hideUIButtonGroup.update(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup)

                    if selectedObject != 0: #if an object is currently selected:

                        sidePanelCloseButton.update(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup)

                        if sidePanelPage == 0: #if on object info page:
                            sidePanelObjectButtons.update(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup)
                            for i in textboxObjectGroup.sprites():
                                i.clicked() #check if textbox clicked
                            surfaceTempTextbox.clicked()
                        elif sidePanelPage == 1: #if on orbit info page:
                            sidePanelOrbitButtons.update(physEng, spacecraft, physObjects, buttonGroup, buildMenuGroup)
                            for i in textboxOrbitGroup.sprites():
                                i.clicked() #check if textbox clicked

                    if buttonGroup.sprites()[1].isClicked: #if equipotential lines are being shown:
                        equipotentialResolutionButtonGroup.update(physEng, physObjects, spacecraft, buttonGroup)

                    if buttonGroup.sprites()[2].isClicked: #if spacecraft controls active:
                        spacecraftControlGroup.update(physEng, physObjects, spacecraft, buttonGroup)
                    
                    if buttonGroup.sprites()[3].isClicked: #if build menu active:
                        buildMenuGroup.update(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup, redco, greenco, blueco)
                        if buildMenuGroup.sprites()[4].isClicked: #if save/load scenarios button pressed:
                            loadPresetButtons.update(physEng, physObjects, spacecraft, buttonGroup, redco=redco, greenco=greenco, blueco=blueco)


                        if buildMenuGroup.sprites()[3].isClicked: #if deletion button is active:

                            #deletion checks
                            for i in physObjects:
                                if i.__class__.__name__ != "Spacecraft" and i.rect.collidepoint(pygame.mouse.get_pos()): #exclude spacecraft from deletion checks. if mouse is over object:

                                    if i is selectedObject:
                                        selectedObject = 0 #clear info panel
                                    if i is physEng.focusedObject:
                                        physEng.focusedObject = 0 #clear object focus

                                    physObjects.remove(i) #remove from physics objects group


                    for i in physObjects: #for each physics object:

                        if i.rect.collidepoint(pygame.mouse.get_pos()): #if mouse is over object:

                            if buildMenuGroup.sprites()[2].isClicked: #if build menu move button is active:

                                if buildMenuGroup.sprites()[2].pickedObject == 0: #if no object has been picked up already:

                                    selectedObject = 0 #clear any selected object
                                    physEng.focusedObject = 0 #clear any focused object
                                    buildMenuGroup.sprites()[2].pickedObject = i #set object as picked object for movement

                            elif i is selectedObject: #if object is already set as selected object:

                                physEng.updateCamera(i) #set object as focused object

                            else: #if not selected object:

                                selectedObject = i #set object as the selected object
                                objectButtons = sidePanelObjectButtons.sprites() #cache for efficiency
                                orbitButtons = sidePanelOrbitButtons.sprites()

                                if i.__class__.__name__ != "Spacecraft": #spacecraft object does not have these flags, so they are skipped over if it is the object:
                                    objectButtons[2].isClicked = i.massFreezeFlag #and mass
                                    objectButtons[3].isClicked = i.radiusFreezeFlag #and radius

                                    if i.massFreezeFlag: #set image of the button as the correct state
                                        objectButtons[2].imageUnscaled = objectButtons[2].imageClicked
                                    else:
                                        objectButtons[2].imageUnscaled = objectButtons[2].imageUnclicked

                                    if i.radiusFreezeFlag: #set image of the button as the correct state
                                        objectButtons[3].imageUnscaled = objectButtons[3].imageClicked
                                    else:
                                        objectButtons[3].imageUnscaled = objectButtons[3].imageUnclicked

                                objectButtons[0].isClicked = i.velocityFreezeFlag #match velocity freeze button to object flag

                                orbitButtons[1].isClicked = i.timePeriodFreezeFlag #do the same for time period
                                orbitButtons[2].isClicked = i.orbitalRadiusFreezeFlag #and orbital radius
                                orbitButtons[3].isClicked = i.orbitalVelocityFreezeFlag #and orbital velocity

                                if i.velocityFreezeFlag: #set image of the button as the correct state
                                    objectButtons[0].imageUnscaled = objectButtons[0].imageClicked
                                else:
                                    objectButtons[0].imageUnscaled = objectButtons[0].imageUnclicked

                                if i.timePeriodFreezeFlag: #set image of the button as the correct state
                                    orbitButtons[1].imageUnscaled = orbitButtons[1].imageClicked
                                else:
                                    orbitButtons[1].imageUnscaled = orbitButtons[1].imageUnclicked

                                if i.orbitalRadiusFreezeFlag: #set image of the button as the correct state
                                    orbitButtons[2].imageUnscaled = orbitButtons[2].imageClicked
                                else:
                                    orbitButtons[2].imageUnscaled = orbitButtons[2].imageUnclicked

                                if i.orbitalVelocityFreezeFlag: #set image of the button as the correct state
                                    orbitButtons[3].imageUnscaled = orbitButtons[3].imageClicked
                                else:
                                    orbitButtons[3].imageUnscaled = orbitButtons[3].imageUnclicked

                                #update buttons
                                for j in objectButtons:
                                    j.rescale(physEng)
                                for j in orbitButtons:
                                    j.rescale(physEng)
                                    
                else: #if an object is already picked up, place down object:

                    buildMenuSprites = buildMenuGroup.sprites() #cache for readability/efficiency

                    pos = buildMenuSprites[2].pickedObject.screenPos #cache for readability/efficiency

                    buildMenuSprites[2].pickedObject.gamePos = pygame.Vector2(((pos[0] - screen.get_width()/2)/physEng.zoomScale) - physEng.movementOffset[0], ((pos[1] - screen.get_height()/2)/physEng.zoomScale) - physEng.movementOffset[1]) #convert position at mouse cursor to gamePos and set as object's position
                    
                    buildMenuSprites[2].pickedObject = 0 #place down picked object

                    for i in range(0,2): #for planet and star placement buttons:
                        
                        if buildMenuSprites[i].isClicked: #if button is active:

                            buildMenuSprites[i].isClicked = False #turn button off
                            buildMenuSprites[i].imageUnscaled = buildMenuSprites[i].imageUnclicked #reset image
                            buildMenuSprites[i].rescale(physEng)


            elif event.type == pygame.MOUSEBUTTONUP: #if mouse button up (after click)

                for i in buttonGroup:
                    i.mouseHoldEnd(physEng) #run effects when mouse is unpressed

                for i in spacecraftControlGroup:
                    i.mouseHoldEnd(physEng) #update spacecraft control buttons for mouse unpress


            elif event.type == pygame.KEYDOWN: #if any key has been pressed:
                
                #check for active text boxes
                for i in textboxObjectGroup:
                    if i.active:
                        i.textInput(event) #update active text boxes with event data

                for i in textboxOrbitGroup:

                    if i.active:

                        if i.designation == 7 or i.designation == 8 or i.designation == 9: #if time period or orbital radius or orbital velocity box:
                            #determine master object
                            greatestForce = -1 #set initial greatest force
                            masterObject = 0 #set master object as 0

                            for j in range(len(physicsSprites)): #for each other sprite in group:

                                if selectedObject is not physicsSprites[j]: #skip if object is the same as the object calculating force for

                                    force = physEng.calcGravBetweenObjects(physicsSprites[j], physicsSprites[j].gamePos.distance_to(selectedObject.gamePos) * 1e6) #calculate force between objects

                                    if force > greatestForce: #if this is new greatest force:

                                        greatestForce = force #set new greatest force
                                        masterObject = physicsSprites[j] #set master object as object force was calculated from

                            if not masterObject == 0: #if a master object has been found:
                                i.textInput(event, masterObject) #pass master object as parameter

                        else:
                            i.textInput(event)

                if surfaceTempTextbox.active:
                    surfaceTempTextbox.textInput(event, redco=redco, greenco=greenco, blueco=blueco)


        ######CAMERA MOVEMENT INPUTS#########
        if pygame.key.get_pressed()[pygame.K_s] | pygame.key.get_pressed()[pygame.K_DOWN]: #down movement key
            physEng.updateCamera("N")

        elif pygame.key.get_pressed()[pygame.K_w] | pygame.key.get_pressed()[pygame.K_UP]: #up movement key
            physEng.updateCamera("S")

        elif pygame.key.get_pressed()[pygame.K_d] | pygame.key.get_pressed()[pygame.K_RIGHT]: #right movement key
            physEng.updateCamera("E")

        elif pygame.key.get_pressed()[pygame.K_a] | pygame.key.get_pressed()[pygame.K_LEFT]: #left movement key
            physEng.updateCamera("W")


        screen.fill("black") #background texture, may replace with image later

        for i in buttonGroup: #for each button:
            i.mouseHoldUpdate(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup) #update methods for holding down mouse button

        physEng.update(physObjects, screen) #run physics calculation step


        ###############ORBIT LINES###################
        if buttonGroup.sprites()[0].isClicked: #if orbit lines are being shown (orbit lines are first in buttonGroup list as pause button is created later):

            pointsToDraw = physEng.predictOrbit(physicsSprites, 300, screen) #calculate orbit lines

            for i in range(len(pointsToDraw) - 2): #for each object's orbit line (-2 for apoapsis and periapsis sections):

                pygame.draw.lines(screen, (255,255,255), False, pointsToDraw[i]) #draw orbit line

            #draw apoapsis markers
            for i in pointsToDraw[len(pointsToDraw) - 2]:
                pygame.draw.circle(screen, (42,128,0), i, 4) #draw marker

            #draw periapsis markers
            for i in pointsToDraw[len(pointsToDraw) - 1]:
                pygame.draw.circle(screen, (0,102,204), i, 4) #draw marker


        physObjects.update(physEng, physicsSprites, buildMenuGroup, buttonGroup) #apply physics calculation results to objects + draw to screen


        #############EQUIPOTENTIAL LINES#################
        if buttonGroup.sprites()[1].isClicked: #if equipotential lines are being shown:

            equipotentialLines = physEng.calcEquipotential(physObjects, screen, resolution) #get array of equipotental points (can get very large on high resolutions)
            for i in equipotentialLines: #for each point on equipotential line:
                pygame.draw.circle(screen, (22,224,224), i, 1) #draw point for each pixel on line

            if not hideUIButtonGroup.sprites()[0].isClicked:
                equipotentialResolutionButtonGroup.draw(screen) #draw resolution settings buttons

            if resolution < 5:
                screen.blit(pygame.transform.smoothscale(font.render("Warning: there may be performance loss at higher equipotential line resolutions.", True, (255,255,255)), (screen.get_width()*0.7, screen.get_height()*0.04)), (0, 0))


        #############SPACECRAFT CONTROLS################
        if buttonGroup.sprites()[2].isClicked: #if spacecraft controls are active and the UI isn't hidden:

            for i in spacecraftControlGroup:
                i.mouseHoldUpdate(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup) #update spacecraft control buttons

            if not spacecraft.velocityFreezeFlag: #if spacecraft velocity/speed is not frozen:
                
                #check for atmospheric slowdown
                for i in physicsSprites: #for each physics object:
                    if i.__class__.__name__ == "Planet": #only planets have atmospheres
                        if spacecraft.gamePos.distance_to(i.gamePos) < i.getAtmosphereHeight(physicsSprites) + i.radius: #if spacecraft is within atmosphere:

                            if spacecraft.velocity[0] == 0: #check for 0 in horizontal component to prevent div by 0 error
                                if spacecraft.velocity[1] < 0: #if negative vertical component:
                                    spacecraft.velocity[1] = - spacecraft.velocity[0] * 0.9**(physEng.getTimeScale()) #speed change affects only vertical velocity (change sign)
                                else: 
                                    spacecraft.velocity[1] = spacecraft.velocity[0] * 0.9**(physEng.getTimeScale()) #speed change affects only vertical velocity
                                
                            else:
                                magnitude = spacecraft.velocity.magnitude() * 0.9**physEng.getTimeScale()
                                angle = math.atan(abs(spacecraft.velocity[1]/spacecraft.velocity[0]))

                                if spacecraft.velocity[0] < 0: #if negative horizontal component:
                                    spacecraft.velocity[0] = - (magnitude * math.cos(angle)) #result should be negative
                                else:
                                    spacecraft.velocity[0] = (magnitude * math.cos(angle))

                                if spacecraft.velocity[1] < 0: #if negative vertical component:
                                    spacecraft.velocity[1] = - (magnitude * math.sin(angle)) #result should be negative
                                else: 
                                    spacecraft.velocity[1] = (magnitude * math.sin(angle))

            spacecraftGroup.draw(screen)

            if not hideUIButtonGroup.sprites()[0].isClicked: #if UI isn't hidden:
                spacecraftControlGroup.draw(screen)

        
        ##################BUILD MENU####################
        if buttonGroup.sprites()[3].isClicked and not hideUIButtonGroup.sprites()[0].isClicked: #if build menu is active and the UI isn't hidden:

            for i in buildMenuGroup:
                i.mouseHoldUpdate(physEng, physObjects, spacecraft, buttonGroup, buildMenuGroup) #update spacecraft control buttons

            buildMenuGroup.draw(screen) #draw build menu to screen

            if buildMenuGroup.sprites()[4].isClicked: #if save/load scenario button is pressed:
                loadPresetButtons.draw(screen) #draw buttons for loading preset scenarios

        
        hideUIButtonGroup.draw(screen) #draw hide UI button to screen

        if not hideUIButtonGroup.sprites()[0].isClicked: #if UI is not hidden:
            buttonGroup.draw(screen) #draw buttons to screen


        ###############SIDE INFO PANEL##################
        if selectedObject != 0 and not hideUIButtonGroup.sprites()[0].isClicked: #if an object is currently selected and the UI isn't hidden:

            sidePanelCloseButton.draw(screen) #draw info panel to screen

            if sidePanelPage == 0: #object info page

                textBuffer = [0,0,0,0,0,0,0] #generate array for text surfaces

                textboxes = textboxObjectGroup.sprites() #cache sprites for efficient call

                sidePanelObjectButtons.draw(screen) #draw buttons on side panel

                if selectedObject.__class__.__name__ == "Spacecraft": #if spacecraft object:
                    textBuffer[2] = font.render(f"Mass: {textboxes[0].text} kg", True, (0,0,0)) #render font for mass
                else:
                    textBuffer[2] = font.render(f"Mass: {textboxes[0].text} x10^24kg", True, (0,0,0)) #render font for mass

                textBuffer[3] = font.render(f"Radius: {textboxes[1].text} x10^6m", True, (0,0,0)) #render font for radius
                textBuffer[4] = font.render(f"Velocity: {textboxes[2].text} km/h", True, (0,0,0)) #render font for velocity, converted to kilometres per hour
                textBuffer[5] = font.render(f"Speed: {textboxes[3].text} km/h", True, (0,0,0)) #render font for speed, converted to kilometres per hour
                textBuffer[6] = font.render(f"Surface gravity: {textboxes[4].text} m/s^2", True, (0,0,0)) #render font for surface gravity

                if selectedObject.__class__.__name__ == "Star": #if selected object is a star

                    textBuffer.append(font.render(f"Surface temperature: {surfaceTempTextbox.text}K", True, (0,0,0))) #render font for surface temperature
                    surfaceTempTextbox.update() #update star surface temperature textbox
                    pygame.draw.rect(screen, surfaceTempTextbox.colour, surfaceTempTextbox.rect) #draw textbox for star surface temperature

                elif selectedObject.__class__.__name__ == "Planet": #if selected object is a planet:

                    textBuffer.append(font.render(f"Atmospheric height: {round(selectedObject.getAtmosphereHeight(physicsSprites), 2)} km", True, (0,0,0))) #render font for atmospheric height

                textboxObjectGroup.update() #set values in textboxes to that of the selected object

                #place textboxes on screen
                for i in textboxObjectGroup.sprites():
                    pygame.draw.rect(screen, i.colour, i.rect)
                

            elif sidePanelPage == 1: #orbit info page

                sidePanelOrbitButtons.draw(screen) #draw buttons on side panel

                #determine master object
                greatestForce = -1 #set initial greatest force as -1
                masterObject = selectedObject #set master object as itself for time being

                for j in range(len(physicsSprites)): #for each other sprite in group:

                    if selectedObject is not physicsSprites[j]: #skip if object is the same as the object calculating force for

                        force = physEng.calcGravBetweenObjects(physicsSprites[j], physicsSprites[j].gamePos.distance_to(selectedObject.gamePos) * 1e6) #calculate force between objects

                        if force > greatestForce: #if this is new greatest force:

                            greatestForce = force #set new greatest force
                            masterObject = physicsSprites[j] #set master object as object force was calculated from


                textBuffer = [0,0,0,0,0] #generate array for text surfaces

                textboxes = textboxOrbitGroup.sprites() #cache sprites for efficient call

                textBuffer[2] = font.render(f"Time period: {textboxes[0].text} hrs", True, (0,0,0)) #calculate time period and render to font
                textBuffer[3] = font.render(f"Orbital radius: {textboxes[1].text} x10^6m", True, (0,0,0)) #render font for orbital radius
                textBuffer[4] = font.render(f"Orbital velocity: {textboxes[2].text} km/h", True, (0,0,0)) #render font for orbital velocity

                textboxOrbitGroup.update(masterObject, greatestForce) #update textbox values to that of the selected object

                #place textboxes on screen
                for i in textboxOrbitGroup.sprites():
                    pygame.draw.rect(screen, i.colour, i.rect)


            #render side info panel
            if selectedObject.__class__.__name__ == "Spacecraft": #if spacecraft object:
                
                image = pygame.transform.rotate(pygame.transform.scale_by(spacecraftImage, screen.get_width()*0.0001), spacecraft.angle) #scale spacecraft image (uses seperate variable to keep quality) and rotate to spacecraft angle
                screen.blit(image, (screen.get_width()*0.07, screen.get_height()*0.17)) #paste to screen
                textBuffer[1] = font.render(f"Colour: N/A", True, (0,0,0)) #render font for colour

            else:
                
                pygame.draw.circle(screen, selectedObject.colour, (screen.get_width()*0.07, screen.get_height()*0.21), screen.get_width()*0.02) #draw copy of selected object at top of info box
                textBuffer[1] = font.render(f"Colour: {selectedObject.colour}", True, (0,0,0)) #render font for colour

            textBuffer[0] = font.render(str(selectedObject.__class__.__name__), True, (0,0,0)) #render font for class name (planet/star/spacecraft)

            #rescale and position text
            for i in range(1, len(textBuffer)): #for each rendered text surface (excludes class name):

                textBuffer[i] = pygame.transform.smoothscale(textBuffer[i], (screen.get_width()*0.13, screen.get_height()*0.03)) #rescale
                
                if i == 1: #if colour text (seperate to add spacing):
                    screen.blit(textBuffer[i], (0, screen.get_height()*0.35)) #blit colour to screen
                else:
                    screen.blit(textBuffer[i], (0, screen.get_height()*(0.425 + 0.03*(i - 1)))) #blit text to screen

            textBuffer[0] = pygame.transform.smoothscale(textBuffer[0], (screen.get_width()*0.06, screen.get_height()*0.05)) #rescale class name text
            screen.blit(textBuffer[0], (0, screen.get_height()*0.28)) #blit class name to screen


        if physEng.focusedObject != 0: #if there is an object in focus:
            screen.blit(font.render(str(physEng.focusedObject.gamePos), True, (255, 255, 255)), (0,0)) #draw coordinates of focused object on screen

        pygame.display.update() #updates the screen

        await asyncio.sleep(0) #delay (pygbag)

    pygame.quit() #destroys window and quits pygame on program end

asyncio.run( main() ) #run main program (pygbag)