import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#pi
global pi
pi = 3.1415926535

#degrees to radians
def dgTR(dg):
    return dg * pi / 180

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
