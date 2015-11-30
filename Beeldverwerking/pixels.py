# Importing needed modules
import cv2 as cv
import numpy as np
import math
import time
from platform import system
import urllib
import block

# Image loading
frame = cv.imread('/home/r0302418/repos/penocw/Beeldverwerking/pi_photos/cam2.jpg', 1)

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
img_width = bw.shape[1]
img_height = bw.shape[0]
img_division = 50

# Pixelation
px = cv.resize(bw, (img_width/img_division,img_height/img_division), interpolation = cv.INTER_NEAREST)
print px.shape
pxres = cv.resize(px, (img_width, img_height), interpolation = cv.INTER_NEAREST)
# 
#opgepast met breedte (blok ernaast)
min_width = 3
max_width = 15
min_length = 3
max_length = 15
start_c = None
start_r = None
stop_c = None
stop_r = None
list_of_blocks = []
'''
for r in xrange(px.shape[0]-1, 0, -1):
    found_white_row = False
    for c in xrange(px.shape[1]-1,0,1):
        if px[r][c] == 255:
            found_white_row = True
            if start_r == None:
                start_r = r
            if (start_c == None) or (c < start_c):
                start_c = c
            if (stop_c == None) or (c > stop_c):
                stop_c = c
    if (start_r != None) and (found_white_row == False):
        stop_r = r - 1
        if not (((start_r - stop_r) < min_length) or ((stop_c - start_c) < min_width)):
            new_block = block.Block([start_c, start_r, stop_c, stop_r])
            list_of_blocks.append(new_block)
        start_c = None
        start_r = None
        stop_c = None
        stop_r = None
        
print list_of_blocks
  '''  

def remove_whites(px, left, right, bottom, top):
    for i in xrange(left, right+1):
        for j in xrange(bottom, top, -1):
            px[j][i]=0 
    return px

for r in xrange(px.shape[0]-1, 0, -1):
    found_white_row = False
    for c in xrange(0,px.shape[1]-1,1):
        if px[r][c] == 255:
            if px[r-1][c]==0 or px[r][c+1]==0:
                px[r][c]=0
            else:
                wide_enough=False
                for i in xrange(min_width,max_width):
                    if px[r][c+i]==255:
                        wide_enough=True
                    if wide_enough==True:
                        break
                long_enough=False
                for i in xrange(min_length,max_length):
                    if px[r-i][c]==255:
                        long_enough=True
                    if long_enough==True:
                        break
                if long_enough==True and wide_enough==True:
                    new_block = block.Block([c, c+max_width, r, r-max_length])
                    list_of_blocks.append(new_block)
                    px = remove_whites(px, c, c+max_width, r, r-max_length)
print list_of_blocks
print list_of_blocks[0].getLocation()

'''        
white_rows = []
for r in xrange(0, px.shape[0]-1,1):
    for c in xrange(0, px.shape[1]-1,1):
        if ((px[r][c] == 255) and (r not in white_rows)):
            white_rows.append(r)

dic = {}
for c in xrange(0, px.shape[1]-1,1):
    found_white = False
    for r in white_rows:
        if px[r][c] == 255:
            found_white = True
            if start_c == None:
                start_c = c
    if (start_c != None) and (found_white == False):
        stop_c = c - 1
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
