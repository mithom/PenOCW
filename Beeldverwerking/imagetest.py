import cv2 as cv
import numpy as np
import time
import math
from matplotlib import pyplot as plt

# Image loading
img = cv.imread('C:\\Users\\Gilles\\Desktop\\line3.jpg',1)

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
lines = cv.HoughLinesP(edges, 2, np.pi/180, 61, None, 20, 200)

# Print number of found lines
print 'Lines found: ', len(lines)

# Line filtering
line1 = 0
while line1 < len(lines):
    line2 = line1 + 1
    while line2 < len(lines):
        line1_1 = [lines[line1][0][0],lines[line1][0][1]]
        line1_2 = [lines[line1][0][2],lines[line1][0][3]]
        line2_1 = [lines[line2][0][0],lines[line2][0][1]]
        line2_2 = [lines[line2][0][2],lines[line2][0][3]]
        distance1 = math.sqrt((line1_1[0]-line2_1[0])**2 + (line1_1[1]-line2_1[1])**2)
        distance2 = math.sqrt((line1_2[0]-line2_2[0])**2 + (line1_2[1]-line2_2[1])**2)
        distance = min(distance1,distance2)
        if (distance <= 200):
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
