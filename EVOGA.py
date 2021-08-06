#start date July 15/21 12:48PM
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# plt.ylabel('some numbers')
# plt.plot([1, 2, 3, 4], [1, 2, 3, 16], 'ro')
# plt.axis([0, 6, 0, 20])
# plt.show()

# counter = 0
# while True:
#     counter += 1
#     if counter == 10:
#         break
#     uin = input("Input an x")
#     x = uin
#     uin = input("Input a y")
#     y = uin
#     plt.plot ([x], [y])

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

# def animate(i):
#     pullData = open("sampleText.txt","r").read()
#     dataArray = pullData.split('\n')
#     xar = []
#     yar = []
#     for eachLine in dataArray:
#         if len(eachLine)>1:
#             x,y = eachLine.split(',')
#             xar.append(int(x))
#             yar.append(int(y))
#     ax1.clear()
#     ax1.plot(xar,yar)
# ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

