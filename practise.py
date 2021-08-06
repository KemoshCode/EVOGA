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
    # if pointInCircle(2, point1, point2) == True:
    #     if distance(point1, point2) == 0:
    #         return True
    #     angle = getAngle(point1, point2)
    #     if angle >= fov[0] and angle <= fov[1]:
    #         return True
    # return False
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



# x_data = []
# y_data = []

# fig, ax = plt.subplots()
# ax.set_xlim(0,105)
# ax.set_ylim(0,12)
# line, = ax.plot(0,0)

# def animation_frame(i):
#     x_data.append(i * 10)
#     y_data.append(i)

#     line.set_xdata(x_data)
#     line.set_ydata(y_data)
#     return line,

# animation = FuncAnimation(fig, func = animation_frame, frames = np.arange(0, 10, 0.01), interval = 10)
# plt.show()

# print(pointInCircle(2,[-1,2.4],[1,2]))
# print(dgTR(13))

point1 = [2,0]
point2 = [1,0]

# print(findRelative(point1, point2))

print(checkFOV(180,190,2,point1,point2))
# print(slope([1,1], [2,2]))

# print(getAngle([1.9,0.39], [2,1]))

# print(checkFOV(FOVrelative(-45,90), [1.9,0.39], [2,1]))
