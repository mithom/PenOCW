# Importing needed modules
import cv2 as cv
import math

from block import Block
import line as lines
import Image
import copy
import beeldverwerkingNameSpace
from socketIO_client import SocketIO
import urllib
import numpy as np
from threading import Thread


url = '192.168.137.173'
port = 4848
current_route_description = []
socketIO = SocketIO(url, port)
beeldverwerking_namespace = socketIO.define(beeldverwerkingNameSpace.BeeldverwekingNameSpace, '/beeldverwerking')
#waiting = Thread(target=socketIO.wait, name="waiting")

## intitializing variebles needed for steering
street_counter = 0
prev_foto_had_street = False


# Stream capturing code copied from
# http://stackoverflow.com/questions/24833149/track-objects-in-opencv-from-incoming-mjpeg-stream


# Searching blocks
def remove_whites(px, left, right, bottom, top):
    for i in xrange(left, right + 1):
        for j in xrange(bottom, top, -1):
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
            width = a - column
            return width, True
    return 0, False


def long_enough(row, column):
    for i in xrange(min_length, max_length):
        a = row - i
        a = check_top(a)
        if px[a][column] == 255:
            length = row - a
            return length, True
    return 0, False


def go_first_block(power, line):
    #calibrate(power, power) ##nee, je zit niet in car.py!!!
    block = line.get_first_block()
    location = block.get_middle()
    print "locatie eerste blok", location
    img_width = block.get_image().get_img_width()
    img_height = block.get_image().get_img_height()
    print "img width, height", img_width, img_height
    car_width = 11.5
    mid_line = [(location[0] - img_width)/2, (img_height - location[1])/2]
    print "mid line", mid_line
    try:
        rico = (img_height - location[1])/(location[0] - img_width)
        x = (-mid_line[1])*rico + mid_line[0]
    except ZeroDivisionError:
        rico = 10000
        x = 0
    radius = abs(x)
    if (rico < 0.5) and (rico >= 0):
        left_power = int(power/4)
        right_power = -int(power/4)
    elif (abs(rico) < 0.5) and (rico <= 0):
        left_power = -int(power/4)
        right_power = int(power/4)
    elif rico >= 0:
        left_power = int(power * (radius + car_width)/( (radius - car_width)))
        right_power = int(power * (radius - car_width)/( (radius + car_width)))
    else:
        left_power = int(power * (radius - car_width)/( (radius + car_width)))
        right_power = int(power * (radius + car_width)/((radius - car_width)))
    beeldverwerking_namespace.set_powers(left_power, right_power)


def go_first_block_2(power, line):
    block = line.get_first_block()
    location = block.get_middle()
    width = block.get_image().get_img_width()
    height = block.get_image().get_img_height()
    mid_block = Block(width/2, width/2, height, height, block.get_image())
    rico = lines.get_rico(block,mid_block)
    radians = math.atan(rico)
    if abs(radians)>math.pi/4:
        if math.sin(radians) >= 1: #positief = naar links draaien
            beeldverwerking_namespace.set_powers(0, 100)
        else:
            beeldverwerking_namespace.set_powers(100, 0)
    else:
        degrees = int(math.degrees(radians))
        beeldverwerking_namespace.set_powers(100- degrees, 100 + degrees)


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
        #frame = cv.resize(frame, (2592, 1944), interpolation=cv.INTER_AREA)

        # Image loading
        # frame = cv.imread('C:\\Users\\Gilles\\Dropbox\\Gilles\\Documenten\\School\\PenO_CW\\repo\\Beeldverwerking\\pi_photos\\cam4.jpg', 0)

        # Gaussian blur
        blur = cv.GaussianBlur(frame, (5, 5), 0)

        frame = None

        threshold = 256

        # Threshold voor bw bepalen adh gemiddelde grijswaarde over de foto
        hist = None
        hist = cv.calcHist([blur], [0], None, [32], [0, 256])
        for x in xrange(31, 10, -1):
            if sum(hist[x] > 0):
                threshold = (x - 8) * 8 + 4
                hist = None
                break
        hist = None
        x = None

        blur = cv.resize(blur, (2592, 1944), interpolation=cv.INTER_NEAREST)  # TODO: check waarvoor deze resize is, want is vreemd

        # Thresholding
        ret, bw = cv.threshold(blur, threshold, 255, cv.THRESH_BINARY)

        blur = None

        # Cutting
        #cut1 = bw[bw.shape[0] / 3:bw.shape[0]]
        #cut2 = cut1[:, cut1.shape[1] * 1 / 4:cut1.shape[1] * 3 / 4]

        # Variable declaration
        bw_width = bw.shape[1]
        bw_height = bw.shape[0]
        img_division = 50
        min_width = 1
        max_width = 9
        min_length = 1
        max_length = 9
        # TODO: juiste width en height megeven, dus buitenste blokken van pixelated figuur,
        #  niet van oorspronkelijke image


        # Pixelation
        px = cv.resize(bw, (bw_width / img_division, bw_height / img_division), interpolation=cv.INTER_NEAREST)
        img_width = px.shape[1]
        img_height = px.shape[0]
        image = Image.Image(img_width, img_height, [], (min_width, max_width, min_length, max_length))

        bw = None

        pxbackup = copy.deepcopy(px)

        for r in xrange(img_height - 1, 0, -1):
            for c in xrange(0, img_width - 1, 1):
                if px[r][c] == 255:
                    if r != 0 and c != (img_width - 1):
                        if px[r - 1][c] == 0 or px[r][c + 1] == 0:
                            px[r][c] = 0
                        else:
                            width, wide = wide_enough(r, c)
                            length, long = long_enough(r, c)
                            if wide and long:
                                t = c
                                u = c + width
                                v = r
                                w = r - length
                                # y = r - 1
                                # x = c + 1
                                # y = check_top(y)
                                # x = check_right(x)
                                # flag1 = False
                                # flag2 = False
                                # while (check_middle_x(y,x) == False and flag1 == False) or \
                                #         (check_middle_y(y,x) == False and flag2 == False):
                                #     if check_middle_x(y,x) == False and flag1 == False:
                                #         last_x = x
                                #         x += 1
                                #         x = check_right(x)
                                #         if x == last_x:
                                #             flag1 = True
                                #     if check_middle_y(y,x) == False and flag2 == False:
                                #         last_y = y
                                #         y -= 1
                                #         check_top(y)
                                #         if y == last_y:
                                #             flag2 = True
                                # t = x - find_whites(y,x,'left')
                                # u = x + find_whites(y,x,'right')
                                # v = y + find_whites(y,x,'down')
                                # w = y - find_whites(y,x,'up')
                                new_block = Block(t, u, v, w, image)
                                image.add_block(new_block)
                                px = remove_whites(px, t, u, v, w)
        ###################
        ## image is ready
        ###################
        px = None
        main_line = image.get_main_line()
        print main_line
        socketIO.wait(0.001)
        if len(beeldverwerkingNameSpace.current_route_description) > 0 and beeldverwerkingNameSpace.is_started:
            command = beeldverwerkingNameSpace.current_route_description[0]
            name = command["commandName"]
            if name == "right":
                if len(image.blocks_right_of_line(main_line)) >= 2:  # TODO: liggen deze wel op een lijn
                    if prev_foto_had_street is False:
                        street_counter += 1
                    prev_foto_had_street = True
                else:
                    prev_foto_had_street = False

                if street_counter == command["params"]["nr"]:
                    street_counter = 0
                    beeldverwerking_namespace.finish_command(command["id"])
                else:
                    go_first_block_2(100, main_line)

            elif name == "left":
                if len(image.blocks_left_of_line(main_line)) >= 2:  # TODO: liggen deze wel op een lijn
                    if prev_foto_had_street is False:
                        street_counter += 1
                    prev_foto_had_street = True
                else:
                    prev_foto_had_street = False

                if street_counter == command["params"]["nr"]:
                    street_counter = 0
                    beeldverwerking_namespace.finish_command(command["id"])
                else:
                    go_first_block_2(100, main_line)

            elif name == "stop":
                if len(image.blocks_left_of_line(main_line)) >= 2 or len(image.blocks_right_of_line(main_line)) >= 2:
                    if prev_foto_had_street is False:
                        street_counter += 1
                    prev_foto_had_street = True
                else:
                    prev_foto_had_street = False

                if street_counter == command["params"]["nr"]:
                    street_counter = 0
                    beeldverwerking_namespace.finish_command(command["id"])
                else:
                    go_first_block_2(100, main_line)
            elif name == "start":
                beeldverwerking_namespace.finish_command(command["id"])  # TODO: moet dit wel?
            else:
                print "unsupported action!!!!!!!!!!!"
        else:
            print beeldverwerkingNameSpace.current_route_description
        ##############
        ## visual
        #############

        for t in image.get_blocks():
            location = t.get_middle()
            pxbackup[location[1]][location[0]] = 150

        pxbackup = cv.cvtColor(pxbackup, cv.COLOR_GRAY2RGB)

        # pxres = cv.resize(pxbackup, (img_width, img_height), interpolation=cv.INTER_NEAREST)
        img_width1 = pxbackup.shape[1]
        img_height1 = pxbackup.shape[0]

        width_ratio = (bw_width/4)/img_width1
        height_ratio = (bw_height/4)/img_height1

        foto = cv.resize(pxbackup, (bw_width/4, bw_height/4), interpolation=cv.INTER_NEAREST)
        try:
            for t in image.get_main_line().get_blocks():
                index = image.get_main_line().get_blocks().index(t)-1
               # print index
                if index != -1:
                    cv.line(foto,(t.get_middle()[0]*width_ratio, t.get_middle()[1]* height_ratio),
                            (image.get_main_line().get_blocks()[index].get_middle()[0]* width_ratio,
                             image.get_main_line().get_blocks()[index].get_middle()[1] * height_ratio),
                            [0,0,255])
        except ValueError:
            pass
        pxbackup = None

        cv.imshow('Result', foto)

        #cv.imshow('Result', pxbackup)

        # cv.resize(pxres, (pxres.shape[1] / 2, pxres.shape[0] / 2),interpolation=cv.INTER_NEAREST)

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
