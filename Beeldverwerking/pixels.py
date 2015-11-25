# Importing needed modules
import cv2 as cv
import numpy as np
import math
import time
from platform import system

# Image loading
img = cv.imread('/home/r0302418/Documents/PenO/street3.jpg', 1)

# Image to grayscale
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# Gaussian blur
blur = cv.GaussianBlur(gray, (5, 5), 0)

# Threshold voor bw bepalen adh gemiddelde grijswaarde over de foto
average = np.average(blur)

# Thresholding
ret, bw = cv.threshold(blur, 160, 255, cv.THRESH_BINARY)

# Cutting
cut1 = bw[bw.shape[0]/2:bw.shape[0]]
cut2 = cut1[:,cut1.shape[1]*1/4:cut1.shape[1]*3/4]

# Variable declaration
img_width = cut2.shape[1]
img_height = cut2.shape[0]
img_division = 15

# Pixelation
px = cv.resize(cut2, (img_width/img_division,img_height/img_division), interpolation = cv.INTER_NEAREST)
print px.shape
pxres = cv.resize(px, (img_width, img_height), interpolation = cv.INTER_NEAREST)


# Image showing
show_original = False
show_bw = False
show_result = True

if show_original:
    cv.imshow('Result', img)
    cv.waitKey(0)
elif show_bw:
    cv.imshow('Result', bw)
    cv.waitKey(0)
elif show_result:
    cv.imshow('Result', pxres)
    cv.waitKey(0)
