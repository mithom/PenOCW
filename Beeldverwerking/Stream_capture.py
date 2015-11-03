import cv2
import numpy as np
import urllib

# Stream capturing code copied from
# http://stackoverflow.com/questions/24833149/track-objects-in-opencv-from-incoming-mjpeg-stream

stream=urllib.urlopen('http://192.168.137.4:4848//video_feed.mjpg')
bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),0)
        cv2.imshow('Stream',frame)
        if cv2.waitKey(1) ==27:
            exit(0) 