#start date July 15/21 12:48PM
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import choices, randint, randrange, random

#pi
global pi
pi = 3.1415926535
global padding
padding = 27

#settings
global hungerRate
hungerRate = 100
global genSize
genSize = 10

class organism:
    def __init__(self, name, x, y, genome, energy):
        self.name = name
        self.x = x
        self.y = y
        self.genome = genome
        self.energy = energy
    def __str__ (self):
        return "|" + str(self.name).ljust(padding) + "||" + str(self.x).ljust(padding) + "||" + str(self.y).ljust(padding) + "||" + str(self.genome).ljust(padding) + "||" + str(self.energy).ljust(padding) + "|"

class plant:
    def __init__(self, name, x ,y, energy):
        self.name = name
        self.x = x
        self.y = y
        self.energy = energy
    def __str__(self) -> str:
        return "|" + str(self.name).ljust(padding) + "||" + str(self.x).ljust(padding) + "||" + str(self.y).ljust(padding) + "||" + str(self.energy).ljust(padding) + "|"

#degrees to radians
def dgTR(dg):
    return dg * pi / 180


def formatTableStart(sample):
    kys = vars(sample).keys()
    string = ""
    for x in kys:
        string += "|" + str(x).ljust(padding) + "|"
    return "\n" + string + "\n" + "_" * len(string)

def pFormatTableStart(sample):
    print(formatTableStart(sample))
    return

def showTable(popDict):
    print(formatTableStart(popDict[0]))
    for index, i in enumerate(popDict):
        print(popDict[index])

def lookUp(popDict, target):
    listThing = [popDict[int(target)]]
    pFormatTableStart(popDict[int(target)])
    for i in listThing:
        print(i)


#radians to degrees
def rTDg(rad):
    return rad * 180/pi

#finds to distance between two points
def distance(point1, point2):
    d = float(math.sqrt(float(((float(point1[0]) - float(point2[0])) ** 2) + ((float(point1[1]) - float(point2[1])) ** 2))))
    #print(f"d is {d}")
    return d

#returns the slope of a line from two points
def slope(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    if y1 == y2:
        return "horizon"
    if x1 == x2:
        return "vert"
    m = (y1 - y2) / (x1 - x2)
    return m


#checks if a point is in a circle based on the radius and centre
def pointInCircle(r,point1,point2):
    state = False
    d = distance(point1, point2)
    #print(f"d is {d} and r is {r}")
    if d <= r:
        state = True
    return state

#returns the legnths of the sides of a triangle in an array
def getSide(point1, point2):
    xSide = abs(point1[0] - point2[0])
    ySide = abs(point1[1] - point2[1])
    hSide = distance(point1, point2)
    return [xSide, ySide, hSide]

#gets angle of the line going between the two points realtive to the x axis
#note: returns radians
def getAngle(point1, point2):
    tri = getSide(point1, point2)
    print(tri)
    if tri[0] == 0:
        if point1[1] > point2[1]:
            return 90
        if point1[1] < point2[1]:
            return 360 - 90
    if tri[1] == 0:
        if point1[0] > point2[0]:
            return 180
        if point1[0] < point2[0]:
            return 0
    return rTDg(math.atan(tri[1] / tri[0]))

#finds the angle realtive to the x-axis by finding the angle of the right triangle containing the two points then using  the slope of the hyptoenuse to determine the direction and adjusting the angle accordingly
def findRelative(point1,point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1] 
    m = slope(point1,point2)
    if m == "vert":
        if y1 > y2:
            return 270
        if y1 < y2:
            return 90
        else:
            print("The crap you do to get here{!!}")
    if m == "horizon":
        if x1 > x2:
            return 0
        if x1 < x2:
            return 180
        else:
            print("Like really what you doin to get here{!!}")
    alpha = getAngle(point1 , point2)
    if m < 0:
        if y1 < y2:
            return alpha
        if y1 > y2:
            return alpha + 180
    if m > 0:
        if y1 < y2:
            return 180 - alpha
        if y1 > y2:
            return 360 - alpha
    else:
        print("Uh oh not cool{!!}")
        return -1

def reverseGetAngle(angle):
    if angle <= 90:
        return angle
    elif angle <= 180 and angle >= 90:
        return 180 - angle
    elif angle <= 270 and angle >=180:
        return angle - 180
    elif angle <= 360 and angle >= 270:
        return 360 - angle
    else:
        print("You have more or less angles then physically possible so good for you and you shouldn;t be here {!!}")

def newPosRel (distance, angle):
    a = reverseGetAngle(angle)
    x = distance * math.cos(dgTR(a))
    y = distance * math.cos(dgTR(a))
    return [x,y]

def newPos(distance, direction, origin):
    coords = newPosRel(distance, direction)
    if direction <= 90:
        coords[0] = coords[0] * -1
    elif direction <= 180 and direction >= 90:
        pass
    elif direction <= 270 and direction >=180:
        coords[1] = coords[1] * -1
    elif direction <= 360 and direction >= 270:
        coords[1] = coords[1] * -1
        coords[0] = coords[0] * -1
    else:
        print("You have more or less angles then physically possible so good for you and you shouldn;t be here {!!}")
        coords = ""
    return [origin[0] + coords[0], origin[1] + coords[1]]


#takes the direction or lower side of the view range of a fov and turns it into an array with the lower and upper ranges of that fov realitve to the x axis
def FOVrelative(direction, size):
    return [direction, direction + size]
#direction is the lower side of the range's angle compared to the x axis

#checks if a point is within the vision cone of a point
def checkFOV(fov, fovSize, viewRange, point1, point2):
    if pointInCircle(viewRange, point1, point2):
        if distance(point1, point2) == 0:
            return True
        relative = findRelative(point1, point2)
        print(relative)
        view = FOVrelative(fov, fovSize)
        print(f"if {relative} is greater than {view[0]} and {relative} is less than {view[1]}")
        if view[1] < 361:
            if relative >= view[0] and relative <= view[1]:
                return True
            else:
                return False
        else:
            print(f"{relative} >= {view[0]} and {relative} <= 360 or {relative} <= ({view[1] - 360})")
            if relative >= view[0] and relative <= 360 or relative <= (view[1] - 360):
                return True
            else:
                return False
    else:
        return False

def hunger(pop):
    pop.energy -= hungerRate
    return pop

def applyStatus(popDict):
    for index, x in enumerate(popDict):
        hunger(popDict[index])

def createPop(popSize):
    popDict = {}
    i = -1
    while True:
        if i >= popSize:
            break
        newPop = organism(str(i + 1), randint(0,10), randint(0,10), [1,1,1,0,0,0,1,1,0], randint(0,100))
        i += 1
        popDict [i] = newPop
    return popDict



popDict = createPop(10)
# print(formatTableTop("Specimen", ["bruh", "lolipop"]))
# print(formatTableStart("spec", "1 2 3 4", 3, 100))
# tester = organism("lad", 1,1,[1,1,1,1,1], 332)
# tester2= organism("lil lad", 1, 2, [1,22,1,2,12,21,21,2,12,1,2,21,21], 340)
# plant1 = plant(1,1,1,30)
# plant2 = plant(2,2,2,60)
# plantDict = {0: plant1, 1: plant2}
# showTable(plantDict)
# testDict = {0: tester, 1: tester2}
# hunger(tester)
# lookUp(testDict, 0)
# listThing = [tester]
# # print(vars(tester).keys())
# # for i in listThing:
# #     print(i)
# # print(formatTableStart(tester))
# # for index, i in enumerate(popDict):
# #     print(popDict[index])
# # print(tester.__dict__.keys())
# # print(vars(tester).keys())
# applyStatus(popDict)
# showTable(popDict)
# uin = input()
# lookUp(popDict, uin)

# print(reverseGetAngle(170))
print(newPos(1,315,[0,0]))