# Importing needed modules
import cv2 as cv
import numpy as np
import math
import time
from platform import system
import urllib

# Image loading
frame = cv.imread('/home/r0302418/repos/penocw/Beeldverwerking/pi_photos/cam4.jpg', 1)

# Stream capturing code copied from
# http://stackoverflow.com/questions/24833149/track-objects-in-opencv-from-incoming-mjpeg-stream

'''stream = urllib.urlopen('http://192.168.137.136:4848//video_feed.mjpg')
byte = ''
while True:
    byte += stream.read(1024)
    a = byte.find('\xff\xd8')
    b = byte.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = byte[a:b+2]
        byte = byte[b+2:]
        frame = cv.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)'''
# Image to grayscale
gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

# Gaussian blur
blur = cv.GaussianBlur(gray, (5, 5), 0)

# Threshold voor bw bepalen adh gemiddelde grijswaarde over de foto
hist = cv.calcHist([blur], [0], None, [32], [0, 256])
for x in range(31, -1, -1):
    if sum(hist[x] > 0):
        threshold = (x-8)*8 + 4
        break

# Thresholding
ret, bw = cv.threshold(blur, threshold, 255, cv.THRESH_BINARY)

# Cutting
cut1 = bw[bw.shape[0]/3:bw.shape[0]]
cut2 = cut1[:,cut1.shape[1]*1/4:cut1.shape[1]*3/4]

# Variable declaration
img_width = cut2.shape[1]
img_height = cut2.shape[0]
img_division = 50

# Pixelation
px = cv.resize(cut2, (img_width/img_division,img_height/img_division), interpolation = cv.INTER_NEAREST)
print px.shape
pxres = cv.resize(px, (img_width, img_height), interpolation = cv.INTER_NEAREST)

# 
for j in xrange(px.shape[0]-1, 0, -1):
    for i in xrange(px.shape[1]):
        if px[j][i] == 255:
            print j, i
'''
[number_of_lines, number_of_colums] = px.shape
j = number_of_lines
while j > 0:
    k = 0
    while k < number_of_colums-1:
        if px[number_of_lines] == 255:
            k += 1
    j += 1
'''

# Image showing
show_original = 1
show_bw = 2
show_cut1 = 3
show_cut2 = 4
show_result = 5
show_x = 5

if show_x is show_original:
    cv.imshow('Result', cv.resize(frame, (frame.shape[1]/4,frame.shape[0]/4),interpolation = cv.INTER_NEAREST))
    cv.waitKey(0)
elif show_x is show_bw:
    cv.imshow('Result', cv.resize(bw, (bw.shape[1]/4,bw.shape[0]/4),interpolation = cv.INTER_NEAREST))
    cv.waitKey(0)
elif show_x is show_cut1:
    cv.imshow('Result', cv.resize(cut1, (cut1.shape[1]/4,cut1.shape[0]/2),interpolation = cv.INTER_NEAREST))
    cv.waitKey(0)
elif show_x is show_cut2:
    cv.imshow('Result', cv.resize(cut2, (cut2.shape[1]/2,cut2.shape[0]/2),interpolation = cv.INTER_NEAREST))
    cv.waitKey(0)
elif show_x is show_result:
    cv.imshow('Result', cv.resize(pxres, (pxres.shape[1]/2,pxres.shape[0]/2),interpolation = cv.INTER_NEAREST))
    cv.waitKey(0)
