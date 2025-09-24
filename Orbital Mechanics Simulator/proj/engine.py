from pygame import Vector2
import math

class PhysicsEngine():

    def __init__(self):

        self.timeScale = 1 #set initial time scale (x1)
        self.zoomScale = 1 #set initial zoom level (x1)
        self.isPaused = True #set initial pause state

        self.movementOffset = Vector2(0,0) #set initial offset for camera movement

        self.focusedObject = 0 #set initial object focus (none)


    def update(self, objGroup, screen):

        sprites = objGroup.sprites()
               
        if not self.isPaused: #physics calculations: do not run when simulation is paused

            for i in sprites: #for each sprite in group:

                if not i.velocityFreezeFlag: #if velocity of object has not been frozen:
                    j = 0
                    while j < len(sprites): #for each other sprite:

                        if not sprites[j].gamePos == i.gamePos: #skip over calculation for itself or others in same position

                            i.velocity += Vector2((sprites[j].gamePos[0]-i.gamePos[0])/math.sqrt((sprites[j].gamePos[0]-i.gamePos[0])**2+(sprites[j].gamePos[1]-i.gamePos[1])**2), (sprites[j].gamePos[1]-i.gamePos[1])/math.sqrt((sprites[j].gamePos[0]-i.gamePos[0])**2+(sprites[j].gamePos[1]-i.gamePos[1])**2)) * self.calcGravBetweenObjects(sprites[j], i.gamePos.distance_to(sprites[j].gamePos) * 1e6) * self.getTimeScale() #calculate gravitational force
                        
                        j += 1
        
        if self.focusedObject != 0: #if there is an object to be focused on:

            self.movementOffset += Vector2(screen.get_width()/2, screen.get_height()/2) - self.focusedObject.screenPos #change movement offset to that of focused object
        

    def updateCamera(self, direction): #function to produce uniform movement for all physics objects in cardinal directions

        self.focusedObject = 0 #reset object focus

        match direction:

            case 0: #no direction passed/clear direction
                return

            case "N": #north
                self.movementOffset[1] -= 5

            case "S": #south
                self.movementOffset[1] += 5

            case "E": #east
                self.movementOffset[0] -= 5

            case "W": #west
                self.movementOffset[0] += 5

            case _: #object to focus on passed through

                self.focusedObject = direction #set focused object

                #self.movementOffset += Vector2(screen.get_width()/2, screen.get_height()/2) - self.focusedObject.screenPos #set movement offset to that of focused object and account for previous offset


    def getScreenPos(self, gamePos, screen): #convert gamePos to screenPos

        screenPos = Vector2((self.movementOffset[0] + gamePos[0]) * self.zoomScale + screen.get_width()/2, (self.movementOffset[1] + gamePos[1]) * self.zoomScale + screen.get_height()/2) #set position on screen to position in terms of game, with zoom and focus offset

        return screenPos


    def getTimeScale(self): #check pause state, and return time scale to planets if unpaused

        if self.isPaused:
            return 0 #paused: no movement
        else:
            return self.timeScale / 3600
        

    def calcEquipotential(self, objects, screen, resolution):

        equipotentialArray = []

        #for each point on the visible screen:
        for i in range(0, screen.get_width(), resolution):
            for j in range(0, screen.get_height(), resolution):

                force = 0 #set initial force on point to 0
                for k in objects: #for each physics object:

                    force += self.calcGravBetweenObjects(k, k.screenPos.distance_to(Vector2(i,j))) #calculate force for each individual object on that point

                if (9e9 < force < 10e9) | (19e9 < force < 20e9) | (29e9 < force < 30e9) | (39e9 < force < 40e9) | (49e9 < force < 50e9) | (59e9 < force < 60e9) | (69e9 < force < 70e9) | (79e9 < force < 80e9) | (89e9 < force < 90e9) | (99e9 < force < 100e9): #calculate force at that point, check against list of evenly spaced forces

                    equipotentialArray.append(Vector2(i,j)) #add to 2d array based on force it meets, if is the same as one of the forces
                        
        return equipotentialArray


    def predictOrbit(self, sprites, points, screen):

        pointArray = [[Vector2(0,0) for i in range(points + 1)] for j in range(len(sprites))] #create array of points for number of points to look ahead for, for each object

        velocityArray = [] #create array to store velocity of objects at future points

        for i in range(len(sprites)):
            pointArray[i][0] = sprites[i].gamePos #set the initial line to be drawn as the centre of the planet
            velocityArray.append(Vector2(sprites[i].velocity)) #get velocities of all sprites in object group

        for i in range(1, points + 1): #for the requested number of points:
            masters = self.generatePointSet(i, pointArray, sprites, velocityArray) #generate a set of points for i steps in the future

        for i in pointArray: #for each object:

            for j in range(0, points + 1): #for each vector2 coordinate:

                i[j] = self.getScreenPos(i[j], screen) #convert to screenPos (pass through 0 for object)

        self.calcApoapsisAndPeriapsis(pointArray, sprites, masters) #calculate + append points for apoapsis and periapsis markers

        return pointArray


    def generatePointSet(self, pointLevel, array, sprites, velocities): #generate points of objects for pointLevel steps in the future

        masterObjects = [0 for i in range(len(sprites))] #create array of master sprites for each object for apoapsis/periapsis calculations

        for i in range(len(sprites)): #for each sprite:

            greatestForce = 0 #set greatest force acting on that object to 0 initially

            if not sprites[i].velocityFreezeFlag: #if velocity has not been frozen:

                for j in range(len(sprites)): #for each other sprite in group:

                    if i != j: #skip if object is the same as the object calculating force for
                        force = self.calcGravBetweenObjects(sprites[j], array[i][pointLevel - 1].distance_to(array[j][pointLevel - 1]) * 1e6) #calculate force between objects

                        if force > greatestForce: #if this is new greatest force:

                            greatestForce = force #set new greatest force
                            masterObjects[i] = j #set master object as index in sprites[] of object force was calculated from

                        velocities[i] += Vector2((sprites[j].gamePos[0]-sprites[i].gamePos[0])/math.sqrt((sprites[j].gamePos[0]-sprites[i].gamePos[0])**2+(sprites[j].gamePos[1]-sprites[i].gamePos[1])**2), (sprites[j].gamePos[1]-sprites[i].gamePos[1])/math.sqrt((sprites[j].gamePos[0]-sprites[i].gamePos[0])**2+(sprites[j].gamePos[1]-sprites[i].gamePos[1])**2)) * force * self.timeScale / 3600 #creates vector to move object by, and increase the velocity by the force at that future point

            array[i][pointLevel] = array[i][pointLevel - 1] + velocities[i] #set point at level in array as predicted point
        
        return masterObjects #return array of master objects for apoapsis/periapsis calculations


    def calcApoapsisAndPeriapsis(self, pointArray, sprites, masters):
        
        periapsisArray = []
        apoapsisArray = []
        
        for i in range(len(sprites)): #for each object:

            minDist = 9999999999999999 #set initial min distance as a large number (can't do -1 so this is the best we are getting)
            minPointToAdd = pointArray[i][0] #set initial minimum point as the centre of the object
            maxDist = -1 #set initial max distance as -1
            maxPointToAdd = pointArray[i][0] #set initial maximum point as the centre of the object

            for j in pointArray[i]: #for each point in the object's set of points:

                pointDist = sprites[masters[i]].screenPos.distance_to(j) #calculate distance between point and master object

                if pointDist < minDist: #if master object of sprite's distance to point is less than the minimum:
                    minDist = pointDist #reset min distance
                    minPointToAdd = j

                if pointDist > maxDist: #if master object of sprite's distance to point is greater than the maximum:
                    maxDist = pointDist #reset max distance
                    maxPointToAdd = j
        
            apoapsisArray.append(maxPointToAdd)
            periapsisArray.append(minPointToAdd)

        pointArray.append(apoapsisArray)
        pointArray.append(periapsisArray)


    def calcGravBetweenObjects(self, objB, radius):
        #Force = (G * mass1 * mass2)/radius**2
        #G = 6.67e-11
        #f = ma
        # => a = f/m
        #f = Gmm2/r**2
        #v = at
        # => v = Gmt/r^2

        if radius == 0:
            return 0 #no force - prevents divide by 0 in next step
        
        force = (6.67e-11 * objB.correctedMass)/(radius**2) #physics equation, not including mass of object A as it cancels later

        return force
