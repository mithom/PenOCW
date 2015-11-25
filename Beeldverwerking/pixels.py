# Importing needed modules
import cv2 as cv
import numpy as np
import math
import time
from platform import system

# Image loading
#frame = cv.imread('/home/r0302418/Documents/PenO/street3.jpg', 1)

# Stream capturing code copied from
# http://stackoverflow.com/questions/24833149/track-objects-in-opencv-from-incoming-mjpeg-stream

stream = urllib.urlopen('http://192.168.137.136:4848//video_feed.mjpg')
byte = ''
while True:
    byte += stream.read(1024)
    a = byte.find('\xff\xd8')
    b = byte.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = byte[a:b+2]
        byte = byte[b+2:]
        frame = cv.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)

	# Image to grayscale
	gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

	# Gaussian blur
	blur = cv.GaussianBlur(gray, (5, 5), 0)

	# Threshold voor bw bepalen adh gemiddelde grijswaarde over de foto
	average = np.average(blur)

	# Thresholding
	ret, bw = cv.threshold(blur, 200, 255, cv.THRESH_BINARY)

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
	    cv.imshow('Result', frame)
	    if cv.waitKey(1) == 27:
            	exit(0)
	elif show_bw:
	    cv.imshow('Result', bw)
	    if cv.waitKey(1) == 27:
            	exit(0)
	elif show_result:
	    cv.imshow('Result', pxres)
	    if cv.waitKey(1) == 27:
            	exit(0)
