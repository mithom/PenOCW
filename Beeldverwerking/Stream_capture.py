import cv2 as cv
import numpy as np
import urllib
import math

# Stream capturing code copied from
# http://stackoverflow.com/questions/24833149/track-objects-in-opencv-from-incoming-mjpeg-stream

stream = urllib.urlopen('http://192.168.137.153:4848//video_feed.mjpg')
byte = ''
while True:
    byte += stream.read(1024)
    a = byte.find('\xff\xd8')
    b = byte.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = byte[a:b+2]
        byte = byte[b+2:]
        frame = cv.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)

        # Gaussian blur
        blur = cv.GaussianBlur(frame, (5, 5), 0)

        # TODO: threshold voor bw bepalen adh gemiddelde grijswaarde over de foto

        # Thresholding
        ret, bw = cv.threshold(blur, 200, 255, cv.THRESH_BINARY)

        # Canny edge detection
        edges = cv.Canny(bw, 5, 5)

        # Hough line transform
        lines = cv.HoughLinesP(edges, 2, np.pi/180, 61, None, 100, 100)

        # Print number of found lines
        # print 'Lines found: ', len(lines)

        # Filtering on/off
        filtering = True

        # TODO: enkel beginpunt en rico opnieuw berekenen als index veranderd is

        # Line filtering
        if filtering is True and lines is not None:
            line1 = 0
            while line1 < len(lines):
                line2 = line1 + 1
                while line2 < len(lines):
                    # Calculating the distance between the line starting points
                    line1_1 = [lines[line1][0][0], lines[line1][0][1]]
                    line1_2 = [lines[line1][0][2], lines[line1][0][3]]
                    line2_1 = [lines[line2][0][0], lines[line2][0][1]]
                    line2_2 = [lines[line2][0][2], lines[line2][0][3]]
                    distance1 = math.sqrt((line1_1[0]-line2_1[0])**2 + (line1_1[1]-line2_1[1])**2)
                    distance2 = math.sqrt((line1_2[0]-line2_2[0])**2 + (line1_2[1]-line2_2[1])**2)
                    distance3 = math.sqrt((line1_1[0]-line2_2[0])**2 + (line1_1[1]-line2_2[1])**2)
                    distance4 = math.sqrt((line1_2[0]-line2_1[0])**2 + (line1_2[1]-line2_1[1])**2)
                    distance = min(distance1, distance2, distance3, distance4)

                    # Calculating line slopes
                    if max(line1_2[0], line1_1[0]) == line1_2[0]:
                        dy = line1_2[1] - line1_1[1]
                        dx = line1_2[0] - line1_1[0]
                    else:
                        dy = line1_1[1] - line1_2[1]
                        dx = line1_1[0] - line1_2[0]
                    if dx != 0:
                        rico1 = dy / float(dx)
                    else:
                        rico1 = 10000
                    if max(line2_2[0], line2_1[0]) == line2_2[0]:
                        dy = line2_2[1] - line2_1[1]
                        dx = line2_2[0] - line2_1[0]
                    else:
                        dy = line2_1[1] - line2_2[1]
                        dx = line2_1[0] - line2_2[0]
                    if dx != 0:
                        rico2 = dy / float(dx)
                    else:
                        rico2 = 10000

                    # Determining wether slopes approximately match
                    flag = 0
                    if abs(rico1) < 1 and abs(rico2) < 1:
                        if (rico1 - rico2) < 1:
                            flag = 1
                    elif abs(rico1) > 7 and abs(rico2) > 7:
                        flag = 1
                    elif (abs(rico1) > 1 and abs(rico2) > 1) and (np.sign(rico1) == np.sign(rico2)):
                        if (rico1 - rico2) < 3:
                            flag = 1

                    # Determining the length of both lines
                    length1 = math.sqrt((line1_1[0]-line1_2[0])**2 + (line1_1[1]-line1_2[1])**2)
                    length2 = math.sqrt((line2_1[0]-line2_2[0])**2 + (line2_1[1]-line2_2[1])**2)

                    # Filtering lines based on similar starting point and slope
                    delete = False
                    switch = False
                    if distance < 200 and flag == 1:
                        # We delete the shortest line
                        if length2 <= length1:
                            lines = np.delete(lines, line2, axis=0)
                            delete = True
                        else:
                            lines = np.delete(lines, line1, axis=0)
                            delete = True
                            line2 = line1 + 1
                            switch = True
                    if delete is False and switch is False:
                        line2 += 1
                line1 += 1
                line2 = 0
            # print 'Lines after filtering: ', len(lines)

        # Grayscale to RGB for color line drawing
        line_image = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)

        # Drawing the lines
        if lines is not None:
            for k in xrange(0, len(lines)):
                for x1, y1, x2, y2 in lines[k]:
                    # cv.line(line_image, (x1,y1),(x2,y2),(0,255,0),2)
                    cv.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Image showing
        cv.imshow('Lines', line_image)

        if cv.waitKey(1) == 27:
            exit(0)