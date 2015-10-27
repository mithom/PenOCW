import cv2 as cv
import numpy as np
import time
import math
from matplotlib import pyplot as plt

# Image loading
img = cv.imread('C:\\Users\\Gilles\\Desktop\\line6.jpg',1)

# Image to grayscale
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# Gaussian blur
blur = cv.GaussianBlur(gray,(5,5),0)

# Thresholding
ret, bw = cv.threshold(blur, 200, 255, cv.THRESH_BINARY)

# Canny edge detection
edges = cv.Canny(bw,5,5)

# plt.subplot(121),plt.imshow(bw,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
# plt.show()

# Hough line transform
lines = cv.HoughLinesP(edges, 2, np.pi/180, 61, None, 100, 200)

# Print number of found lines
print 'Lines found: ', len(lines)

# Line filtering
line1 = 0
while line1 < len(lines):
    line2 = line1 + 1
    while line2 < len(lines):
        # Determining if the lines start close to eachother
        line1_1 = [lines[line1][0][0],lines[line1][0][1]]
        line1_2 = [lines[line1][0][2],lines[line1][0][3]]
        line2_1 = [lines[line2][0][0],lines[line2][0][1]]
        line2_2 = [lines[line2][0][2],lines[line2][0][3]]
        distance1 = math.sqrt((line1_1[0]-line2_1[0])**2 + (line1_1[1]-line2_1[1])**2)
        distance2 = math.sqrt((line1_2[0]-line2_2[0])**2 + (line1_2[1]-line2_2[1])**2)
        distance = min(distance1,distance2)

        # Determining wether the lines have a similar slope
        if max(line1_2[0],line1_1[0])==line1_2[0]:
            dy = line1_2[1] - line1_1[1]
            dx = line1_2[0] - line1_1[0]
        else:
            dy = line1_1[1] - line1_2[1]
            dx = line1_1[0] - line1_2[0]
        if dx != 0:
            rico1 = dy / float(dx)
        else:
            rico1 = 10000
        if max(line2_2[0],line2_1[0])==line2_2[0]:
            dy = line2_2[1] - line2_1[1]
            dx = line2_2[0] - line2_1[0]
        else:
            dy = line2_1[1] - line2_2[1]
            dx = line2_1[0] - line2_2[0]
        if dx != 0:
            rico2 = dy / float(dx)
        else:
            rico2 = 10000

        print 'Flag'
        print 'Rico 1: ', rico1
        print 'Rico 2: ', rico2

        flag = 0
        if abs(rico1) < 1 and abs(rico2) < 1:
            if (rico1 - rico2) < 1:
                flag = 1
        elif abs(rico1) > 7 and abs(rico2) > 7:
            flag = 1
        elif (abs(rico1) > 1 and abs(rico2) > 1) and (np.sign(rico1) ==np.sign(rico2)):
            if (rico1 - rico2) < 3:
                flag = 1

        if flag == 1:
            print 'Deleted!'
            lines = np.delete(lines,line2,axis=0)
        line2 += 1
    line1 += 1
    line2 = 0
print 'Lines after filtering: ', len(lines)

# Grayscale to RGB for color line drawing
line_image = cv.cvtColor(bw, cv.COLOR_GRAY2RGB)

# Drawing the lines
for i in xrange(0,len(lines)):
    for x1,y1,x2,y2 in lines[i]:
        cv.line(line_image, (x1,y1),(x2,y2),(0,255,0),2)

# Image showing
cv.imshow('Lines', line_image)
cv.waitKey(0)
