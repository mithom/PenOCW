import cv2 as cv
import numpy as np
import math

number_of_test_files = 5

imglist = []
for i in range(0,number_of_test_files):
    path_string = 'C:\\Users\\Gilles\\Dropbox\\Gilles\\Documenten\\School\\PenO_CW\\repo\\Beeldverwerking' +\
                  '\\pi_photos\\cam' + str(i) + '.jpg'
    print path_string
    imglist.append(cv.imread(path_string, 1))

for j in range(len(imglist)):

    img = imglist[j]

    resized_image = cv.resize(img, (0, 0), None, 0.15, 0.15, cv.INTER_AREA)

    # Image to grayscale
    gray = cv.cvtColor(resized_image, cv.COLOR_RGB2GRAY)

    # Gaussian blur
    blur = cv.GaussianBlur(gray, (5, 5), 0)

    # threshold voor bw bepalen adh gemiddelde grijswaarde over de foto
    average = np.average(blur)

    # Thresholding
    ret, bw = cv.threshold(blur, 150, 255, cv.THRESH_BINARY)

    # Canny edge detection
    edges = cv.Canny(bw, 5, 5)

    # Hough Line transform
    lines = cv.HoughLinesP(edges, 2, np.pi/180, 61, None, 50, 200) #(edge image, rho, theta, threshold,
                                                                    # lines, minLineLength, maxLineGap)

    # Filtering on/off
    filtering = False

    # TODO: enkel beginpunt en rico opnieuw berekenen als index veranderd is

    # Line filtering
    if filtering is True and lines is not None:
        line1 = 0
        while line1 < len(lines):
            line2 = line1 + 1
            while line2 < len(lines):
                # Calculating the distance between the Line starting points
                line1_1 = [lines[line1][0][0], lines[line1][0][1]]
                line1_2 = [lines[line1][0][2], lines[line1][0][3]]
                line2_1 = [lines[line2][0][0], lines[line2][0][1]]
                line2_2 = [lines[line2][0][2], lines[line2][0][3]]
                distance1 = math.sqrt((line1_1[0]-line2_1[0])**2 + (line1_1[1]-line2_1[1])**2)
                distance2 = math.sqrt((line1_2[0]-line2_2[0])**2 + (line1_2[1]-line2_2[1])**2)
                distance3 = math.sqrt((line1_1[0]-line2_2[0])**2 + (line1_1[1]-line2_2[1])**2)
                distance4 = math.sqrt((line1_2[0]-line2_1[0])**2 + (line1_2[1]-line2_1[1])**2)
                distance = min(distance1, distance2, distance3, distance4)

                # Calculating Line slopes
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
                    # We delete the shortest Line
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


    # Grayscale to RGB for color Line drawing
    line_image = cv.cvtColor(bw, cv.COLOR_GRAY2RGB)


    # Drawing the lines
    if lines is not None:
        for k in xrange(0, len(lines)):
            for x1, y1, x2, y2 in lines[k]:
                cv.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Image showing
    cv.imshow('Lines', line_image)
    cv.imshow('Original', resized_image)
    cv.waitKey(0)
