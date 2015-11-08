import cv2
import numpy as np
import urllib

# Stream capturing code copied from
# http://stackoverflow.com/questions/24833149/track-objects-in-opencv-from-incoming-mjpeg-stream

stream = urllib.urlopen('http://192.168.137.67:4848//video_feed.mjpg')
byte = ''
while True:
    byte += stream.read(1024)
    a = byte.find('\xff\xd8')
    b = byte.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = byte[a:b+2]
        byte = byte[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)
        cv2.imshow('Stream', frame)
        if cv2.waitKey(1) == 27:
            exit(0) 