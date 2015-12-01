# Importing needed modules
import cv2 as cv
import block
import Image
import copy
from beeldverwerkingNameSpace import BeeldverwekingNameSpace
from socketIO_client import SocketIO
import urllib
import numpy as np
import time


url = '192.168.137.202'
port = 4848
current_route_description = []
socketIO = SocketIO(url, port)
beeldverwerking_namespace = socketIO.define(BeeldverwekingNameSpace, '/beeldverwerking')

# Stream capturing code copied from
# http://stackoverflow.com/questions/24833149/track-objects-in-opencv-from-incoming-mjpeg-stream


# Searching blocks
def remove_whites(px, left, right, bottom, top):
    for i in xrange(left, right + 1):
        for j in xrange(bottom, top, -1):
            print i, j
            px[j][i] = 0
    return px


def check_right(index):
    if index > (img_width - 1):
        index = (img_width - 1)
    return index


def check_top(index):
    if index < 0:
        index = 0
    return index


def find_whites(y,x,direction):
    count = 0
    if direction == 'left':
        while x > 0:
            x -= 1
            if px[y][x]==255:
                count += 1
            else:
                break
    elif direction == 'right':
        while x < (img_width-1):
            x += 1
            if px[y][x]==255:
                count += 1
            else:
                break
    elif direction == 'up':
        while y > 0:
            y -= 1
            if px[y][x]==255:
                count += 1
            else:
                break
    else:
        while y < (img_height-1):
            y += 1
            if px[y][x]==255:
                count += 1
            else:
                break
    if direction == 'up' or direction == 'down':
        if count > max_length/2:
            count = max_length/2
    else:
        if count > max_width/2:
            count = max_width/2
    return count


def check_middle_x(y,x):
    left = find_whites(y,x,'left')
    right = find_whites(y,x,'right')
    if abs(left-right)>1:
        return False
    else:
        return True

def check_middle_y(y,x):
    up = find_whites(y,x,'up')
    down = find_whites(y,x,'down')
    if abs(up-down)>1:
        return False
    else:
        return True


def wide_enough(row, column):
    for i in xrange(min_width, max_width):
        a = column + i
        a = check_right(a)
        if px[row][a] == 255:
            return True
    return False


def long_enough(row, column):
    for i in xrange(min_length, max_length):
        a = row - i
        a = check_top(a)
        if px[a][column] == 255:
            return True
    return False


stream = urllib.urlopen('http://%(url)s:%(port)i//video_feed.mjpg' % {'url': url, 'port': port})
byte = ''
while True:
    byte += stream.read(1024)
    a = byte.find('\xff\xd8')
    b = byte.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = byte[a:b + 2]
        byte = byte[b + 2:]
        frame = cv.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)

        # Image loading
        #frame = cv.imread('/home/r0302418/repos/penocw/Beeldverwerking/pi_photos/cam4.jpg', 1)

        # Gaussian blur
        blur = cv.GaussianBlur(frame, (5, 5), 0)

        threshold = 150
        # Threshold voor bw bepalen adh gemiddelde grijswaarde over de foto
        hist = cv.calcHist([blur], [0], None, [32], [0, 256])
        for x in range(31, -1, -1):
            if sum(hist[x] > 0):
                threshold = (x - 8) * 8 + 4
                break

        # Thresholding
        ret, bw = cv.threshold(blur, threshold, 255, cv.THRESH_BINARY)

        # Cutting
        cut1 = bw[bw.shape[0] / 3:bw.shape[0]]
        cut2 = cut1[:, cut1.shape[1] * 1 / 4:cut1.shape[1] * 3 / 4]

        # Variable declaration
        img_width = bw.shape[1]
        img_height = bw.shape[0]
        img_division = 50
        min_width = 1
        max_width = 9
        min_length = 1
        max_length = 9
        image = Image.Image(img_width, img_height, [], (min_width, max_width, min_length, max_length))

        # Pixelation
        px = cv.resize(bw, (img_width / img_division, img_height / img_division), interpolation=cv.INTER_NEAREST)
        print px.shape

        pxbackup = copy.deepcopy(px)
        for r in xrange(img_height - 1, 0, -1):
            found_white_row = False
            for c in xrange(0, img_width - 1, 1):
                if px[r][c] == 255:
                    if r != 0 and c != (img_width - 1):
                        if px[r - 1][c] == 0 or px[r][c + 1] == 0:
                            px[r][c] = 0
                        else:                        
                            if (long_enough(r,c) == True) and (wide_enough(r,c) == True):
                                y = r - 1
                                x = c + 1
                                while check_middle_x(y,x) == False or check_middle_y(y,x) == False:
                                    if check_middle_x(y,x) == False:
                                        x += 1
                                    if check_middle_y(y,x) == False:
                                        y -= 1
                                t = x - find_whites(y,x,'left')
                                u = x + find_whites(y,x,'right')
                                v = y + find_whites(y,x,'down')
                                w = y - find_whites(y,x,'up')
                                new_block = block.Block(t, u, v, w, image)
                                image.add_block(new_block)
                                px = remove_whites(px, t, u, v, w)
        ###################
        ## image is ready
        ###################

        main_line = image.get_main_line()
        print main_line

        ##############
        ## visual
        #############
        for t in image.get_blocks():
            location = t.get_middle()
            pxbackup[location[1]][location[0]] = 150

        pxres = cv.resize(pxbackup, (img_width, img_height), interpolation=cv.INTER_NEAREST)

        cv.imshow('Result', cv.resize(pxres, (pxres.shape[1] / 2, pxres.shape[0] / 2),interpolation=cv.INTER_NEAREST))

        if cv.waitKey(1) == 27:
            exit(0)

    """
        # Image showing
        show_original = 1
        show_bw = 2
        show_cut1 = 3
        show_cut2 = 4
        show_result = 5
        show_x = 5

        if show_x is show_original:
            cv.imshow('Result', cv.resize(frame, (frame.shape[1] / 4, frame.shape[0] / 4), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
        elif show_x is show_bw:
            cv.imshow('Result', cv.resize(bw, (bw.shape[1] / 4, bw.shape[0] / 4), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
        elif show_x is show_cut1:
            cv.imshow('Result', cv.resize(cut1, (cut1.shape[1] / 4, cut1.shape[0] / 2), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
        elif show_x is show_cut2:
            cv.imshow('Result', cv.resize(cut2, (cut2.shape[1] / 2, cut2.shape[0] / 2), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
        elif show_x is show_result:
            cv.imshow('Result', cv.resize(pxres, (pxres.shape[1] / 2, pxres.shape[0] / 2), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
    """
        ##########################
        ## hier bebingt de stuur logica
        ##########################
    #beeldverwerking_namespace.set_powers(0, 200)
